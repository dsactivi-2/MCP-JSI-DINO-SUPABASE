#!/usr/bin/env python3
"""Reduce untrusted routine metadata to fixed labels; never emit source text."""

import argparse
import hashlib
import json
import re
import sys


MAX_BYTES = 4 * 1024 * 1024
MAX_FUNCTIONS = 256
MAX_SOURCE_BYTES = 256 * 1024
WRITE_WORDS = {"INSERT", "UPDATE", "DELETE", "MERGE", "TRUNCATE", "COPY"}
DDL_WORDS = {"CREATE", "ALTER", "DROP", "GRANT", "REVOKE", "COMMENT", "REINDEX",
             "VACUUM", "ANALYZE", "REFRESH"}
EXTERNAL_WORDS = {"DBLINK", "DBLINK_EXEC", "HTTP_POST", "HTTP_GET", "PG_NOTIFY",
                  "LO_IMPORT", "LO_EXPORT", "PG_WRITE_FILE"}
WORDS = WRITE_WORDS | DDL_WORDS | EXTERNAL_WORDS | {"EXECUTE", "CALL", "SELECT"}
FIELDS = {"oid", "schema", "name", "arguments", "owner", "owner_superuser",
          "owner_bypassrls", "owner_createrole", "language", "kind", "volatility",
          "source", "sql_standard", "config", "extension", "acl"}


def need(condition):
    if not condition:
        raise ValueError("audit input rejected")


def lexical_labels(source):
    """Mask all identifiers/literals/comments before deriving finite labels."""
    tokens = []
    i = 0
    while i < len(source):
        if source[i].isspace():
            i += 1
        elif source.startswith("--", i):
            end = source.find("\n", i + 2)
            i = len(source) if end < 0 else end + 1
        elif source.startswith("/*", i):
            depth = 1
            i += 2
            while i < len(source) and depth:
                if source.startswith("/*", i):
                    depth += 1
                    i += 2
                elif source.startswith("*/", i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            need(depth == 0)
        elif source[i] in "'\"" or (source[i] in "Ee" and source[i:i + 2].lower() == "e'"):
            escaped = source[i] in "Ee"
            if escaped:
                i += 1
            quote = source[i]
            i += 1
            closed = False
            while i < len(source):
                if escaped and source[i] == "\\":
                    i += 2
                elif source[i] == quote:
                    if i + 1 < len(source) and source[i + 1] == quote:
                        i += 2
                    else:
                        i += 1
                        closed = True
                        break
                else:
                    i += 1
            need(closed)
            tokens.append("MASKED")
        elif source[i] == "$" and (tag := re.match(r"\$(?:[A-Za-z_][A-Za-z_0-9]*)?\$", source[i:])):
            delimiter = tag.group()
            end = source.find(delimiter, i + len(delimiter))
            need(end >= 0)
            i = end + len(delimiter)
            tokens.append("MASKED")
        elif source[i].isalpha() or source[i] == "_":
            end = i + 1
            while end < len(source) and (source[end].isalnum() or source[end] in "_$"):
                end += 1
            word = source[i:end].upper()
            tokens.append(word if word in WORDS else "IDENT")
            i = end
        else:
            tokens.append("(" if source[i] == "(" else "PUNCT")
            i += 1
    return {
        "write_indicators": sorted(set(tokens) & WRITE_WORDS),
        "ddl_indicators": sorted(set(tokens) & DDL_WORDS),
        "external_indicators": sorted(set(tokens) & EXTERNAL_WORDS),
        "dynamic_sql": "EXECUTE" in tokens,
        "procedure_call": "CALL" in tokens,
        "unresolved_call_syntax": any(a in {"IDENT", "MASKED"} and b == "("
                                       for a, b in zip(tokens, tokens[1:])),
    }


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result)
        result[key] = value
    return result


def summarize(payload, token):
    need(len(payload) <= MAX_BYTES and re.fullmatch(r"[0-9a-f]{32}", token))
    doc = json.loads(payload, object_pairs_hook=reject_duplicates)
    need(isinstance(doc, dict) and set(doc) ==
         {"token", "identity_matches", "server_major", "total_count", "functions"})
    need(doc["token"] == token and doc["identity_matches"] is True)
    need(type(doc["server_major"]) is int and doc["server_major"] == 17)
    need(type(doc["total_count"]) is int and 0 <= doc["total_count"] <= MAX_FUNCTIONS)
    need(isinstance(doc["functions"], list) and len(doc["functions"]) == doc["total_count"])
    output = []
    seen = set()
    for index, entry in enumerate(doc["functions"], 1):
        need(isinstance(entry, dict) and set(entry) == FIELDS)
        need(type(entry["oid"]) is int and 0 < entry["oid"] < 2**32 and entry["oid"] not in seen)
        seen.add(entry["oid"])
        for key in ("schema", "name", "arguments", "owner", "language", "source"):
            need(isinstance(entry[key], str))
        for key in ("owner_superuser", "owner_bypassrls", "owner_createrole", "sql_standard"):
            need(type(entry[key]) is bool)
        need(entry["kind"] in {"f", "p", "w"} and entry["volatility"] in {"i", "s", "v"})
        need(entry["extension"] is None or isinstance(entry["extension"], str))
        need(isinstance(entry["config"], list) and all(isinstance(v, str) for v in entry["config"]))
        need(isinstance(entry["acl"], list) and len(entry["acl"]) <= 256)
        for acl in entry["acl"]:
            need(isinstance(acl, dict) and set(acl) == {"role", "grantable"})
            need(isinstance(acl["role"], str) and type(acl["grantable"]) is bool)
        need(any(a["role"] == "PUBLIC" for a in entry["acl"]))
        source = entry["source"]
        need(len(source.encode()) <= MAX_SOURCE_BYTES)
        analyzed = entry["language"] in {"sql", "plpgsql"}
        labels = lexical_labels(source) if analyzed else {
            "write_indicators": [], "ddl_indicators": [], "external_indicators": [],
            "dynamic_sql": False, "procedure_call": False, "unresolved_call_syntax": True,
        }
        role_classes = {a["role"] for a in entry["acl"]}
        output.append({
            "alias": f"F{index:03d}", "routine_oid": entry["oid"],
            "identity_sha256": hashlib.sha256(json.dumps(
                [entry["schema"], entry["name"], entry["arguments"]], ensure_ascii=True).encode()).hexdigest(),
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "schema_class": entry["schema"] if entry["schema"] in
                {"public", "crm", "crm_api", "crm_auth", "pg_catalog"} else "other",
            "language_class": entry["language"] if analyzed else "opaque",
            "routine_kind": {"f": "function", "p": "procedure", "w": "window"}[entry["kind"]],
            "source_representation": ("create_definition_including_wrapper" if entry["sql_standard"]
                                      else "routine_body" if analyzed else "opaque"),
            "extension_managed": entry["extension"] is not None,
            "owner_superuser": entry["owner_superuser"],
            "owner_bypassrls": entry["owner_bypassrls"],
            "owner_createrole": entry["owner_createrole"],
            "direct_grants": sorted(role_classes & {"PUBLIC", "anon", "authenticated", "service_role"}),
            "other_direct_grantee_count": len(role_classes - {"PUBLIC", "anon", "authenticated", "service_role"}),
            "has_search_path_setting": any(v.startswith("search_path=") for v in entry["config"]),
            "source_analyzed_lexically": analyzed,
            "safety_status": "NOT_PROVEN_READ_ONLY", **labels,
        })
    return {"status": "PASS_WITH_GAPS", "scope": "PUBLIC EXECUTE and PUBLIC schema USAGE routines; indirect paths unassessed",
            "raw_definitions_retained": False, "routines_executed": False,
            "candidate_data_read": False, "database_mutated": False,
            "count": len(output), "functions": output,
            "limitations": ["lexical indicators are not behavioral proof",
                            "SQL-standard CREATE definitions include wrapper DDL indicators",
                            "called routines and actual consumers are not resolved",
                            "absence of write indicators does not prove read-only behavior"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    try:
        payload = sys.stdin.buffer.read(MAX_BYTES + 1)
        report = summarize(payload, args.token)
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError):
        print("STOP: protected audit input rejected; no raw output", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
