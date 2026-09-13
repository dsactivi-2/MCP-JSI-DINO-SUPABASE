<!-- markdownlint-disable MD013 -->
# Worklog: Bericht-Audit JSON-Filter

Datum: 2026-09-13

Objekt: unabhängiger PASS zu
[crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).
Ablauf: [verify-verifier-report.md](../handoffs/2026-09-13-verify-verifier-report.md).

Vorbericht-PASS nicht haltbar. Archiv in `lista_kandidata`: Cookie nur
Status 3; Klassen an Liste-SQL und Zähl-SQL; `search[value]` nur Liste-SQL.
Testdatei-Satz dazu getrennt. INNER JOIN, Struke/Smjer, „5 Jahre“ bleiben
OFFEN. Kein years-Feld. JSON-Namen `struke` / `smjer` unverändert.

HEAD `e288d3d`. Testdatei-HEAD-Hash
`ae21cb9ed82cb6306cababe738fa67d1134ae9f2b29bbf65c21c999819c522ad`.
Nur-Archiv-Satz-Hash
`08108dac287ce5240253eb2c471b98383aa267219cab0c1d5255e0311aa42563`.
Aktuelle Testdatei nach Status-Satz:
`100c43b7d2d6b5f9112a583e45f9d906c3d7fcc3f5fb0492a3834275778371ed`.

Nutzer 2026-09-13, Punkt 1: **Ja.** Der Vorbericht-PASS zählt nicht.
Nutzer 2026-09-13, Punkt 3: **Ja.** JSON bleibt Entwurf, kein Vertrag.
Kein Runtime, kein SQL-Apply aus diesem Entwurf.
Punkt 2 (Archiv-Satz) **Ja:** Satz bleibt. R1 kopiert den Zählfehler nicht.
Punkt 4 aufgeteilt: Struke/Smjer = Ausbildungsberuf **Ja**;
„5 Jahre“ in R1 **Nein**; INNER JOIN **Nein** (sichtbar lassen).

Nächster Schritt: Nutzer nennt den nächsten Auftrag. Kein Tool-Namen,
kein Eval, kein MCP. Kein Commit.
