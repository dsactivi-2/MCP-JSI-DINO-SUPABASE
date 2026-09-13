<!-- markdownlint-disable MD013 -->
# PHP-Suchzettel (Wizard 01)

Stand: 2026-09-13

Rohoutput von `scripts/wizards/crm-wiring-01-locate-and-scan.sh` gegen
`/Users/activi/Downloads/crm-master-3/src/crm`. Keine Datensätze, kein Dump.
Jede Zeile: `Dateipfad:Zeile:Textfragment`.

Der erste Lauf schnitt `hits-tables` und `hits-ui` mit `head -200` ab.
Die Hauptsuche `kandidati.php` lag hinter Zeile 200 und fehlte. Rescan ohne
Deckel: RPC 21, Tabellen-Fundstellen 1732, UI-Fundstellen 2487. `*.sql` und
`Info/` bleiben ausgeschlossen (Dump mit INSERT). Den 200-Deckel nicht
wieder einbauen.
200 war die abgeschnittene Liste, nicht 200 Dateien. Die gültige Zahl ist
`wc -l` der ganzen Datei.

**1732 und 2487 sind Fundstellen, keine Tabellen- oder Feldzahl.** Dieselbe
Tabelle kann viele Zeilen haben. Das ist nicht Gate B. Gate-B-Zahlen
stehen in ADR-0002 Q10.2q und im Katalog-Mapping, nicht in diesen Zetteln.

Nicht Punkt für Punkt abschreiben. Lesart und Entscheidungen stehen in
[crm-app-wiring.md](../crm-app-wiring.md) und
[ADR-0002 Q17/Q18](../../decisions/0002-search-design-interview.md).

| Datei | Treffer | Was gesucht wurde | Was man darin sieht |
| --- | ---: | --- | --- |
| [hits-rpc.txt](hits-rpc.txt) | 21 | `search_candidates*` / occupation-Namen | vor allem Partner-App `jobstep_pp` Namenssuche; blieb 21, weil schon unter 200 |
| [hits-tables.txt](hits-tables.txt) | 1732 | `idk_kandidati` und Profiltabellen | inkl. `kandidati.php` (ab ca. Zeile 918) |
| [hits-ui.txt](hits-ui.txt) | 2487 | Suche/Beruf/Sprache/Skill | laut; vollständig, weiterhin Rauschen |

`rg kandidati.php` zählt grob 171 (tables) / 152 (ui). Davon
`src/crm/kandidati.php` 58 / 49; Rest vor allem `public_kandidati.php`
(113 / 102) plus 1 UI-Zeile `kandidati2.php`. Hauptsuche bleibt
`kandidati.php?page=list_ajax`. Lesart:
[crm-app-wiring.md](../crm-app-wiring.md), nicht die Rohzettel.

Status und Cron: Unterordner [status/](status/) (Wizard 04), Lesart
[crm-status-codebefund.md](../crm-status-codebefund.md).
