#!/usr/bin/env python3
"""Map PHP/JSON filter names to B2 catalog names only. No values, no rows."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIRING = ROOT / "docs/discovery/crm-app-wiring.md"
DRAFT = ROOT / "docs/discovery/crm-json-filter-draft.md"
OUT = ROOT / "docs/discovery/php-filter-catalog-name-map.md"
DEFAULT_B2 = Path(
    "/Users/activi/Library/Application Support/Activi/discovery-raw"
    "/dino_crm_discovery_target_01/DISCOVERY-GATE-B2-V3-RO-2026-09-12/gate-b2.out"
)
IDENT = re.compile(r"^[a-z][a-z0-9_]*$")
TICK = re.compile(chr(96) + r"([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)?)" + chr(96))


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def load_b2_names(path: Path) -> tuple[set[tuple[str, str]], set[tuple[str, str, str]]]:
    if not path.is_file():
        fail("B2 name source missing: " + str(path))
    relations: set[tuple[str, str]] = set()
    columns: set[tuple[str, str, str]] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("SQL-GATE-B2-002,"):
            parts = line.split(",")
            if len(parts) >= 3 and IDENT.match(parts[1]) and IDENT.match(parts[2]):
                relations.add((parts[1], parts[2]))
        elif line.startswith("SQL-GATE-B2-003,"):
            parts = line.split(",")
            if (
                len(parts) >= 5
                and IDENT.match(parts[1])
                and IDENT.match(parts[2])
                and IDENT.match(parts[4])
            ):
                columns.add((parts[1], parts[2], parts[4]))
    if len(relations) < 3 or len(columns) < 3:
        fail("B2 name extract too small")
    return relations, columns


def parse_wiring_filters(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if line.startswith("| UI-Label"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and not line.startswith("|"):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        rows.append(
            {
                "ui": cells[0],
                "php": cells[1],
                "post": cells[2],
                "physical": cells[3],
                "layer": cells[4],
                "note": cells[5],
            }
        )
    if len(rows) < 10:
        fail("wiring filter table too small")
    return rows


def parse_json_fields(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith("| JSON | PHP |"):
            in_table = True
            continue
        if in_table and line.startswith("| ---"):
            continue
        if in_table and (not line.startswith("|") or line.startswith("###")):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[1] not in {"-", "—", ""}:
            mapping[cells[1]] = cells[0]
            for piece in re.split(r"[/,]", cells[1]):
                piece = piece.strip().strip(chr(96))
                if piece:
                    mapping.setdefault(piece, cells[0])
    return mapping


def extract_idents(
    blob: str,
    relations: set[tuple[str, str]],
    columns: set[tuple[str, str, str]],
) -> list[str]:
    found: list[str] = []
    for match in TICK.findall(blob):
        if match not in found:
            found.append(match)
    relnames = {rel for _schema, rel in relations}
    colnames = {col for _schema, _rel, col in columns}
    for word in re.findall(r"[a-z][a-z0-9_]{2,}", blob):
        if word in found:
            continue
        if word in relnames or word in colnames:
            found.append(word)
    return found


def relation_hit(name: str, relations: set[tuple[str, str]]) -> str:
    schemas = sorted({schema for schema, rel in relations if rel == name})
    if not schemas:
        return "nein"
    return "ja (" + ", ".join(schemas) + ")"


def column_hit(table: str, column: str, columns: set[tuple[str, str, str]]) -> str:
    schemas = sorted(
        {schema for schema, rel, col in columns if rel == table and col == column}
    )
    if not schemas:
        return "nein"
    return "ja (" + ", ".join(schemas) + ")"


def status_for(
    idents: list[str],
    relations: set[tuple[str, str]],
    columns: set[tuple[str, str, str]],
) -> str:
    if not idents:
        return "kein Name im PHP-Befund"
    bits: list[str] = []
    for ident in idents:
        if "." in ident:
            table, col = ident.split(".", 1)
            if relation_hit(table, relations).startswith("nein"):
                bits.append(ident + ": Relation nein")
            else:
                bits.append(ident + ": " + column_hit(table, col, columns))
        else:
            rel = relation_hit(ident, relations)
            if rel.startswith("ja"):
                bits.append(ident + ": " + rel)
            else:
                col_schemas = sorted({schema for schema, _rel, col in columns if col == ident})
                if col_schemas:
                    bits.append(ident + ": Spalte ja (" + ", ".join(col_schemas) + ")")
                else:
                    bits.append(ident + ": nein")
    return "; ".join(bits)


def md_escape(text: str) -> str:
    return text.replace("|", "/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--b2-out", type=Path, default=DEFAULT_B2)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    relations, columns = load_b2_names(args.b2_out)
    wiring = parse_wiring_filters(WIRING.read_text(encoding="utf-8"))
    json_by_php = parse_json_fields(DRAFT.read_text(encoding="utf-8"))
    lines = [
        "<!-- markdownlint-disable MD013 -->",
        "# PHP-Filter zu B2-Katalognamen",
        "",
        "Stand: 2026-09-13",
        "",
        "Status: **NAMEN ONLY**. Keine Werte, keine Kandidatenzeilen, kein RLS-Beweis,",
        "kein Vertrag, kein MCP. Erzeugt von",
        "scripts/discovery/build-php-filter-catalog-name-map.py.",
        "B2-Rohdatei bleibt außerhalb Git. Diese Seite enthält nur Identifier.",
        "",
        "Quelle Filter: [crm-app-wiring.md](crm-app-wiring.md),",
        "[crm-json-filter-draft.md](crm-json-filter-draft.md).",
        "Quelle Katalog: Gate B2 V3, nur schema_name / relation_name / column_name.",
        "B3-Rohdatei wird nicht gelesen (Definitionen können Literale enthalten).",
        "",
        "| JSON | PHP | Namen aus PHP-Befund | In B2 | Hinweis |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in wiring:
        idents = extract_idents(row["physical"], relations, columns)
        json_name = json_by_php.get(row["post"], "-")
        if json_name == "-":
            json_name = json_by_php.get(row["php"], "-")
        if json_name == "-" and row["ui"].startswith("fehlt"):
            json_name = "nicht in R1-JSON"
        if json_name == "-":
            for php_key, json_val in json_by_php.items():
                bare = php_key.strip(chr(96))
                if bare and bare in row["php"]:
                    json_name = json_val
                    break
        physical_names = ", ".join(idents) if idents else row["physical"]
        lines.append(
            "| "
            + " | ".join(
                [
                    md_escape(json_name),
                    md_escape(row["php"]),
                    md_escape(physical_names),
                    md_escape(status_for(idents, relations, columns)),
                    md_escape(row["layer"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "B2 Relationen gelesen: %s. B2 Spalten gelesen: %s."
            % (len(relations), len(columns)),
            "Zahlen oben sind Katalog-Anzahlen, keine Kandidatenwerte.",
            "",
            "Das ersetzt nicht das Review von RLS, Grants und PII.",
            "",
        ]
    )
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print("PASS: wrote " + str(args.output))


if __name__ == "__main__":
    main()
