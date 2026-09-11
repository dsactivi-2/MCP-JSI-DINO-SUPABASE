#!/usr/bin/env python3

import argparse
import csv
import io
import json
import os
import selectors
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path


EXPECTED_QUERY_IDS = [f"SQL-GATE-B1-{number:03d}" for number in range(1, 12)]
FINDING_QUERY_IDS = {f"SQL-GATE-B1-{number:03d}" for number in range(3, 11)}
PER_QUERY_LIMIT = 2 * 1024 * 1024
TOTAL_LIMIT = 12 * 1024 * 1024
ROW_SENTINEL = 5001
csv.field_size_limit(PER_QUERY_LIMIT)


class ProtocolStop(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--psql", required=True)
    parser.add_argument("--sql", required=True)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--gate-id", required=True)
    parser.add_argument("--target-alias", required=True)
    parser.add_argument("--sql-sha256", required=True)
    parser.add_argument("--window-end-epoch", required=True, type=int)
    parser.add_argument("--timeout-seconds", required=True, type=int)
    return parser.parse_args()


def update_quote_state(data: bytes, in_quotes: bool) -> bool:
    index = 0
    while index < len(data):
        if data[index] == 34:
            if in_quotes and index + 1 < len(data) and data[index + 1] == 34:
                index += 2
                continue
            in_quotes = not in_quotes
        index += 1
    return in_quotes


def terminate(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except PermissionError:
        process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            process.kill()
        process.wait()


def write_manifest(path: Path, payload: dict) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    expected_database = os.environ.pop("GATE_B1_EXPECTED_DATABASE_NAME", "")
    if not expected_database:
        print("STOP: expected database value missing", file=sys.stderr)
        return 1

    boundary_token = uuid.uuid4().hex
    boundary_prefix = f"__GATE_B1_BOUNDARY__|{boundary_token}|".encode("ascii")
    raw_path = Path(args.raw)
    manifest_path = Path(args.manifest)
    started_at = int(time.time())
    started_monotonic = time.monotonic()
    query_rows = {query_id: 0 for query_id in EXPECTED_QUERY_IDS}
    query_bytes = {query_id: 0 for query_id in EXPECTED_QUERY_IDS}
    total_bytes = 0
    stop_reason = ""
    query_index = 0
    current_query: str | None = None
    record_buffer = bytearray()
    in_quotes = False

    child_env = {
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
        "PGSERVICE": os.environ["PGSERVICE"],
        "PGSERVICEFILE": os.environ["PGSERVICEFILE"],
        "PGPASSFILE": os.environ["PGPASSFILE"],
        "PGCONNECT_TIMEOUT": "5",
    }
    command = [
        args.psql,
        "-X",
        "--no-psqlrc",
        "--no-password",
        "--quiet",
        "--set=ON_ERROR_STOP=on",
        "--csv",
        "--tuples-only",
        f"--set=expected_database_name={expected_database}",
        f"--set=boundary_token={boundary_token}",
        f"--file={args.sql}",
    ]

    process: subprocess.Popen[bytes] | None = None
    selector: selectors.BaseSelector | None = None
    handling_signal = False
    spawn_in_progress = False
    pending_interrupt = False
    previous_signal_handlers: dict[int, signal.Handlers] = {}
    pending = bytearray()

    def handle_signal(_signal_number: int, _frame: object) -> None:
        nonlocal handling_signal, pending_interrupt
        if handling_signal:
            return
        if spawn_in_progress:
            pending_interrupt = True
            return
        handling_signal = True
        raise ProtocolStop("launcher_interrupted")

    def consume_line(line: bytes, raw_handle: io.BufferedWriter) -> None:
        nonlocal current_query, in_quotes, query_index, total_bytes, record_buffer
        semantic_finding_id: str | None = None

        begin_marker = None
        end_marker = None
        if query_index < len(EXPECTED_QUERY_IDS):
            query_id = EXPECTED_QUERY_IDS[query_index]
            begin_marker = boundary_prefix + f"BEGIN|{query_id}\n".encode("ascii")
            end_marker = boundary_prefix + f"END|{query_id}\n".encode("ascii")

        is_begin = current_query is None and line == begin_marker
        is_end = current_query is not None and not in_quotes and line == end_marker

        if is_begin:
            current_query = EXPECTED_QUERY_IDS[query_index]
        elif is_end:
            if record_buffer:
                raise ProtocolStop("incomplete_csv_record")
            current_query = None
            query_index += 1
        elif current_query is None:
            raise ProtocolStop("unexpected_protocol_output")
        else:
            query_bytes[current_query] += len(line)
            if query_bytes[current_query] > PER_QUERY_LIMIT:
                raise ProtocolStop("query_byte_limit")
            record_buffer.extend(line)
            in_quotes = update_quote_state(line, in_quotes)
            if not in_quotes:
                try:
                    rows = list(
                        csv.reader(
                            io.StringIO(record_buffer.decode("utf-8")),
                            strict=True,
                        )
                    )
                except (UnicodeDecodeError, csv.Error) as error:
                    raise ProtocolStop("invalid_csv_output") from error
                if len(rows) != 1 or not rows[0] or rows[0][0] != current_query:
                    raise ProtocolStop("query_identity_mismatch")
                query_rows[current_query] += 1
                if current_query in FINDING_QUERY_IDS:
                    semantic_finding_id = current_query
                record_buffer.clear()
                if query_rows[current_query] >= ROW_SENTINEL:
                    raise ProtocolStop("row_sentinel_5001")

        total_bytes += len(line)
        if total_bytes > TOTAL_LIMIT:
            raise ProtocolStop("total_byte_limit")
        raw_handle.write(line)
        raw_handle.flush()
        if semantic_finding_id is not None:
            raise ProtocolStop(f"semantic_finding_{semantic_finding_id}")

    try:
        for signal_number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous_signal_handlers[signal_number] = signal.signal(signal_number, handle_signal)
        spawn_in_progress = True
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=child_env,
            start_new_session=True,
        )
        spawn_in_progress = False
        if pending_interrupt:
            handling_signal = True
            raise ProtocolStop("launcher_interrupted")
        assert process.stdout is not None
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        raw_descriptor = os.open(raw_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(raw_descriptor, "wb") as raw_handle:
            while True:
                now = time.time()
                if now >= args.window_end_epoch:
                    raise ProtocolStop("time_window_expired")
                if time.monotonic() - started_monotonic >= args.timeout_seconds:
                    raise ProtocolStop("launcher_timeout")

                events = selector.select(timeout=0.1)
                if events:
                    chunk = os.read(process.stdout.fileno(), 65536)
                    if chunk:
                        pending.extend(chunk)
                        while b"\n" in pending:
                            line, remainder = pending.split(b"\n", 1)
                            pending = bytearray(remainder)
                            consume_line(line + b"\n", raw_handle)
                        if current_query is not None and query_bytes[current_query] + len(pending) > PER_QUERY_LIMIT:
                            raise ProtocolStop("query_byte_limit")
                        if total_bytes + len(pending) > TOTAL_LIMIT:
                            raise ProtocolStop("total_byte_limit")
                    elif process.poll() is not None:
                        break
                elif process.poll() is not None:
                    break

            if pending:
                raise ProtocolStop("unterminated_output")
            return_code = process.wait()
            if return_code != 0:
                raise ProtocolStop("psql_error")
            if current_query is not None or query_index != len(EXPECTED_QUERY_IDS):
                raise ProtocolStop("incomplete_query_protocol")
    except ProtocolStop as error:
        stop_reason = str(error)
    finally:
        handling_signal = True
        try:
            if process is not None:
                terminate(process)
        finally:
            try:
                if selector is not None:
                    selector.close()
            finally:
                for signal_number, previous_handler in previous_signal_handlers.items():
                    signal.signal(signal_number, previous_handler)

    ended_at = int(time.time())
    status = "STOP" if stop_reason else "PASS"
    write_manifest(
        manifest_path,
        {
            "ended_at_epoch": ended_at,
            "gate_id": args.gate_id,
            "psql_attempts": 1,
            "query_bytes": query_bytes,
            "query_rows": query_rows,
            "sql_sha256": args.sql_sha256,
            "started_at_epoch": started_at,
            "status": status,
            "stop_reason": stop_reason or None,
            "target_alias": args.target_alias,
            "total_bytes": total_bytes,
        },
    )
    if stop_reason:
        print(f"STOP: {stop_reason}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception:
        print("STOP: launcher_internal_error", file=sys.stderr)
        exit_code = 1
    raise SystemExit(exit_code)
