<!-- markdownlint-disable MD013 -->
# Prompt: nächste Session (aktuell)

Datum: 2026-09-13

Live: [docs/project.md](../project.md),
[crm-work-inventory.md](../discovery/crm-work-inventory.md),
[ADR-0002](../decisions/0002-search-design-interview.md).
Handoff: [2026-09-13-session-handoff.md](2026-09-13-session-handoff.md).
Einheitlich (OS-Temp): `/private/tmp/dino-crm-unified-handoff-2026-09-13.md`.

Block ungekürzt als erste Nachricht einfügen.

~~~text
Du setzt die Arbeit am Supabase CRM MCP fort. Antworte auf Deutsch, einfache Worte. Code, Pfade, SQL-Namen, JSON-Namen, PHP-Namen nicht übersetzen.

Lies zuerst docs/project.md, docs/discovery/crm-work-inventory.md, docs/decisions/0002-search-design-interview.md, docs/discovery/crm-json-filter-draft.md, docs/handoffs/2026-09-13-session-handoff.md. Nichts von vorn scannen.

JSON-Filter bleibt ENTWURF, kein Vertrag. Du baust kein MCP, bis der Nutzer das ausdrücklich startet.

Schon bestätigt in ADR-0002, nicht neu aufrollen: Bericht-Audit (alter PASS zählt nicht; Archiv-Zählfehler nicht nachbauen); Struke/Smjer = Ausbildungsberuf (JSON-Namen struke/smjer); Jahresfilter R1 Q8.5.9 von-bis Job+Jobgruppe; INNER JOIN nicht kopieren; JMBG intern ja, kein Filter; Ranking größte kandidat_id zuerst; Filter zeigen dann eine Suche; ein Such-MCP Tokens je Rolle; Export Blättern plus CSV/Excel max. 500 inkl. JMBG/Kontakt, nicht Kunde.

ACT-103 Done (1A 2A 3A). ACT-100 In Progress; Linear-Text dort ist alt, nicht ohne Auftrag schreiben. Offen: JSON-Vertrag AUTO-02; JSON-Feld für den genannten Job bei Jahren; Hosting/SDK-Version (Cloudflare möglich, nicht gewählt), Tenant, SLOs. Worker-RAM später; kein Redis/Iris in R1.

Arbeitsverzeichnis: /Users/activi/Documents/ChatGPT/Dino problem baza crm
Branch: codex/supabase-crm-auth-discovery
HEAD: 777fbd4, origin gleich. Dirty Tree (33 Dateien): nicht committen, nicht stashen, nicht resetten, außer der Nutzer sagt es.
check-local.sh zuletzt Exit 0, 753 Links.

PHP nur /Users/activi/Downloads/crm-master-3/src/crm. Dump nicht lesen.

Ende.
~~~
