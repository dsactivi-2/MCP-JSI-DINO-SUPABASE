<!-- markdownlint-disable MD013 -->
# PHP-Suchzettel (Wizard 01)

Stand: 2026-09-12

Rohoutput von `scripts/wizards/crm-wiring-01-locate-and-scan.sh` gegen
`/Users/activi/Downloads/crm-master-3/src/crm`. Keine Datensätze, kein Dump.
Jede Zeile: `Dateipfad:Zeile:Textfragment`. Ab 2026-09-13 ohne 200-Zeilen-Deckel
(Rescan). `*.sql` und `Info/` bleiben ausgeschlossen — dort lag ein Dump.

Nicht Punkt für Punkt abschreiben. Lesart und Entscheidungen stehen in
[crm-app-wiring.md](../crm-app-wiring.md) und
[ADR-0002 Q17/Q18](../../decisions/0002-search-design-interview.md).

| Datei | Treffer | Was gesucht wurde | Was man darin sieht |
| --- | ---: | --- | --- |
| [hits-rpc.txt](hits-rpc.txt) | 21 | `search_candidates*` / occupation-Namen | vor allem Partner-App `jobstep_pp` Namenssuche |
| [hits-tables.txt](hits-tables.txt) | 1732 | `idk_kandidati` und Profiltabellen | inkl. `kandidati.php` |
| [hits-ui.txt](hits-ui.txt) | 2487 | Suche/Beruf/Sprache/Skill | laut; jetzt vollständig, weiterhin Rauschen |

`kandidati.php` kommt in tables/ui vor. Lesart bleibt
[crm-app-wiring.md](../crm-app-wiring.md), nicht die Rohzettel.

Status und Cron: Unterordner [status/](status/), Lesart
[crm-status-codebefund.md](../crm-status-codebefund.md).
