<!-- markdownlint-disable MD013 -->
# Worklog: JSON-Filter-Entwurf R1

Datum: 2026-09-13

Wizard-03-Alltag aus ADR-0002 Q18 übernommen, nicht neu befragt.
Entwurf: [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).
Nur alte Kandidati-Filter. Q8.5.3–8 nicht überschrieben.
Kein MCP, kein Scaffold, kein Produktions-SQL.

Prüfung gegen PHP `lista_kandidata` und Heft: Maskenfelder decken sich.
Später bestätigt: Struke/Smjer = Ausbildungsberuf; Jahresfilter R1 Q8.5.9.
PHP-Nuancen (beide Altersgrenzen, `true`-only, Smjer verdrängt Struke)
stehen im Entwurf, ohne 1:1-SQL-Kopie.
Bericht-Audit 2026-09-13: Vorbericht-PASS nicht haltbar. Archiv-Satz in der
Testdatei getrennt (Klassen an Liste-SQL und Zähl-SQL; search[value] nur
Liste-SQL). INNER JOIN später: nicht kopieren, sichtbar lassen.
