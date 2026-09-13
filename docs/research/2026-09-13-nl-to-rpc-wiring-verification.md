<!-- markdownlint-disable MD013 -->
# Verifikation: Sprache zu Treffer verdrahten

Datum: 2026-09-13

Status: `PASS_WITH_GAPS`. Keine neue Architektur. Kein MCP-Scaffold.
Keine Produktionsänderung.

Geprüft wurde der Session-Vorschlag: Agent-Skill, drei MCP-Tools,
validiertes JSON, eine Postgres-RPC, Indexe, zuerst synthetisch.
Nicht geprüft wurden Schema-Fakten, Auth-Interop oder gemessene Laufzeit.

## Urteil

Der **Zielweg ist korrekt** und für diesen Use Case der angenommene
Best-Practice-Pfad:

1. Das LLM füllt nur ein kleines JSON-Formular.
2. Der MCP prüft Felder, Identität und Limit.
3. Eine von uns geschriebene Postgres-Funktion weiß, wo und wie gesucht wird.
4. Höchstens 50 Treffer. Kein LLM-SQL. Keine Tabellenliste für das Modell.

Das ist [ADR-0001](../decisions/0001-controlled-query-boundary.md), nicht
ein neuer Plan. Eine frühere Architekturprüfung kam zum selben Kern:
[Plan-Verifikation 2026-09-11](2026-09-11-plan-best-practice-verification.md).

**Jetzt den MCP zu bauen ist nicht optimal.** Der JSON-Filter ist Entwurf.
Struke/Smjer = Ausbildungsberuf. Jahresfilter R1: Q8.5.9. Der nächste
Repo-Schritt: Nutzer nennt den Auftrag. JSON bleibt Entwurf. Kein Scaffold
ohne ausdrückliche Freigabe.
Quelle: [Projektstand](../project.md).

## Analog, nicht nachbauen

| Analog | Was wir übernehmen | Was wir nicht kopieren |
| --- | --- | --- |
| [MCP Tools 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | `inputSchema` Pflicht; Server **muss** Inputs validieren, Rechte prüfen, rate-limiten, Output säubern; `structuredContent` plus optionales `outputSchema` | Das Spec-Beispiel `execute_sql`. Genau das wäre hier der Fehler. |
| [MCP TS SDK v2](https://github.com/modelcontextprotocol/typescript-sdk) | Stabile Linie zur Spec 2026-07-28; Tools mit Schema | Ungepinntes Copy-Paste, v1/v2 mischen |
| [Supabase Database Functions](https://supabase.com/docs/guides/database/functions) | Suche als Funktion, Aufruf über `rpc()`, feste Parameter | Freies `.from('idk_kandidati')`, Data-API auf Importtabellen |
| Postgres least privilege, Keyset, Indexe | Nur `EXECUTE` auf die Suchfunktion; Cursor statt OFFSET; Indexe auf WHERE/JOIN | `service_role`, Superuser, OFFSET über 200.000 Zeilen |
| Offizieller Supabase-Developer-MCP | Nur öffentliche Docs | Live auf das Produktionsprojekt mit Personendaten |

Drei erlaubte Bauwege, alle mit derselben JSON-Grenze:
[Top-3-Vergleich](mcp-autowire-top3-vergleich.md).
Default-Kandidat bleibt Option 1 (MCP SDK v2 + Schema-Validierung + eine RPC).
AUTO-02 ist das noch nicht.

## Drei verschiedene „Skills“

Der Chat hat diese drei Dinge vermischt. Getrennt halten:

| Schicht | Aufgabe | Nicht tun |
| --- | --- | --- |
| **Runtime-Tool** | MCP-`inputSchema` der drei Tools. Das ist das Formular. | PHP-Fundstellen (1732), SQL oder Gate-B-Katalog in die Tool-Beschreibung |
| **Runtime-Prompt** | Wie ein Satz auf Felder mappt, wann nachgefragt wird. Vorlage: [mcp-search-agent-prompt.md](mcp-search-agent-prompt.md) | Occupation/Jahre als R1 verkaufen |
| **Builder-Skill** | Wie *wir* Server und SQL entwerfen. Siehe [mcp-server-dev-tooling.md](../agents/mcp-server-dev-tooling.md) | Denselben Skill dem Recruiter-Agenten geben |

`get_filter_options` liefert IDs zur Laufzeit. In R1 nur IDs der **alten
Hauptsuche** (Status, Gruppe, Struke/Smjer/Schule, Sprachen, …). Nicht
occupation, nicht Stadt, nicht Skills: Q22.

## Korrekturen am Session-Vorschlag

1. **Zielbild behalten.** Sprache → JSON → MCP → RPC → Index. Das bleibt.
2. **R1 nicht modernisieren, bevor die alte Maske verdrahtet ist.**
   „Elektriker“ ist heute `struke` / `smjer`, Bedeutung Ausbildungsberuf
   `OFFEN`. `has_work_experience: true` ist ja/nein, kein Jahresfeld.
3. **Schnell** heißt: Filter in Postgres, `LIMIT 50` in der Funktion,
   Keyset-Cursor, Indexe auf Filter-/Join-Spalten, später `EXPLAIN`.
   Nicht: das Modell 200.000 Zeilen lesen lassen.
4. **Bestätigung:** MCP verlangt Human-in-the-loop für sensible Calls.
   Fachlich bleibt Q7 (Lockerung nach Null-Treffer) Pflicht. Eine Bestätigung
   *jeder* Suche ist nur `VORLÄUFIGER VORSCHLAG`.
5. **Funktion:** `SECURITY INVOKER`, enger `search_path`, kein
   `PUBLIC EXECUTE`, Runtime-Rolle ≠ Discovery-Rolle ≠ `service_role`.
6. **Alte RPC** `crm_api.search_candidates` nicht wrappen (Kontakte in der
   Signatur).

## Was schon liegt, nicht neu schreiben

- Vertrag und Reihenfolge: [runtime-search-mcp-end-to-end.md](../runbooks/runtime-search-mcp-end-to-end.md)
- Lokales Fake-MCP: [option-1-mcp-sdk-rpc-setup.md](../runbooks/option-1-mcp-sdk-rpc-setup.md)
- SDK-Kandidat: [sdk-integration-plan.md](../planning/sdk-integration-plan.md)
- R1-Formular: [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md)
- CRM-Matrix für den Server-Skill: [mcp-server-dev-tooling.md](../agents/mcp-server-dev-tooling.md)

## Nächste Schritte

1. **Jetzt:** JSON-Entwurf und ADR-0002 halten. Kein MCP-Scaffold ohne
   ausdrücklichen Auftrag. Hosting/SDK-Version offen.
2. Struke/Smjer und R1-Jahre (Q8.5.9) sind bestätigt. Offene Punkte nur noch
   dort, wo ADR-0002 `OFFEN` sagt.
3. **Dann Vertrag:** eine Feldbrücke JSON → Postgres-Spalte, versioniertes
   JSON-Schema, eine neue RPC-Signatur. AUTO-02.
4. **Dann synthetisch:** Option-1-Server gegen erfundene Kandidaten.
   `/tdd` vor dem Handler. Kein Produktions-DSN.
5. **Erst nach Freigabe:** additive `crm_search`-Objekte, Runtime-Rolle,
   ein Client.

Nicht als Nächstes: `/wayfinder` (Karte existiert), `/implement` im
Doku-Repo, Supabase-Plugin auf Produktion, Auto-SQL-MCP.

## Skills für spätere Sessions

| Wann | Skill / Dokument | Warum |
| --- | --- | --- |
| Jede Supabase-Frage | `.agents/skills/supabase/SKILL.md` | Aktuelle Herstellerregeln |
| SQL, RPC, RLS, Index, EXPLAIN | `supabase-postgres-best-practices` | Least privilege, Keyset, Indexe |
| MCP-Tool-Design, erst nach Schritt 3 | `build-mcp-server` plus [mcp-server-dev-tooling.md](../agents/mcp-server-dev-tooling.md) | Drei Tools, Pattern A, kein `execute_sql` |
| Docs für Agenten | `writing-for-agents` | Keine parallele Architekturdatei |
| Offene Fachfrage | `grill-with-docs` / `domain-modeling` | Nur bei neuer Nutzerantwort |
| Bau einer Ticket-Scheibe | `tdd` → `implement` → `code-review` | Nach Spec/Tickets, synthetisch |
| Mensch muss Secret/Hosting klicken | `wizard` | Agent darf Produktion nicht selbst verdrahten |

Ask-Matt-Routing dieser Session: Verifikation über `/research`, nicht
Main-Flow `/implement`. Das Zielbild ist geschärft. Der Bau wartet auf
das Audit-Verdict und die offenen Filterbedeutungen.
