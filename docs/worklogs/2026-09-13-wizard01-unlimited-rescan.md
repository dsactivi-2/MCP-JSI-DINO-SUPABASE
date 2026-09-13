<!-- markdownlint-disable MD013 -->
# Worklog: Wizard 01 ohne 200-Zeilen-Deckel

Datum: 2026-09-13

Der erste Lauf schnitt `hits-tables` und `hits-ui` bei 200 Zeilen ab.
Dadurch fehlte die Hauptsuche `kandidati.php` in den Zetteln.

`head -200` ist aus Wizard 01 entfernt. Rescan mit gespeichertem
`CRM_PATH`, ohne die Verdrahtungsdatei zu überschreiben.

Stand: RPC 21, Tabellen-Fundstellen 1732, UI-Fundstellen 2487 (Code-Treffer,
keine Postgres-Tabellen). Grobes `rg kandidati.php`: 171 / 152; davon
`src/crm/kandidati.php` 58 / 49, Rest vor allem `public_kandidati.php`.
`*.sql` und `Info/` ausgeschlossen (Dump mit INSERT).

Dateien: [crm-php-hits](../discovery/crm-php-hits/). ADR-0002 Q18 ergänzt.
