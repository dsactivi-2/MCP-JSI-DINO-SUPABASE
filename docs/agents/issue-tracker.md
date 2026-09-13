# Issue tracker: Linear

Ovaj repozitorij koristi postojeći namjenski projekt **Dino problem baza CRM**.
Identitet projekta i pripadnost timu potvrđeni su read-only provjerom
2026-09-10. Live inventar issuea osvježen je 2026-09-13.

Wayfinder mapa **ACT-100**–**ACT-109** postoji od 2026-09-12. Naslovi još
koriste Jobstep/OrbStack framing. Izričite odgovore za izvor, opseg skena i
Verdrahtung daju [ADR-0002](../decisions/0002-search-design-interview.md)
Q17 i Q20–Q22; ta pitanja se ne otvaraju ponovo iz Linear naslova.

Lokalni [plan Release-1 automatizacijskih ticketa](../planning/release-1-automation-tickets.md)
i dalje koristi privremene ključeve `AUTO-01` do `AUTO-08`; oni nisu Linear
ID-ovi i nisu ista mapa kao ACT-100. Drugi wayfinder map za isti cilj se ne
kreira. Vanjski upis novih issuea i dalje čeka zasebnu freigabe, osim kada
korisnik izričito naloži ažuriranje postojećih.

| Polje | Vrijednost |
| --- | --- |
| Workspace | `activi` |
| Workspace ID | `51583ced-d671-47d0-8b58-df855f1525e3` |
| Team | `Activi` (`ACT`) |
| Team ID | `24546ac9-b38e-4bf7-bc13-c29840dfa39b` |
| Projekt | `Dino problem baza CRM` |
| Project ID | `53e5feb7-1589-4609-8a90-40dd6b54c0d0` |

## Rad s issueima

- Pri pretrazi i kreiranju issuea eksplicitno koristiti navedeni projekt i tim.
  Prije izmjene postojećeg issuea provjeriti njegovu pripadnost projektu.
- Ponovo koristiti ovaj projekt pri nastavku rada ili ponavljanju setupa.
- Prije kreiranja provjeriti postoji li već issue za isti problem.
- Issue treba sadržavati problem, opseg, kriterije prihvata, odgovornu osobu,
  zavisnosti i relevantne rizike. Otvorene odluke označiti kao otvorene.
- Koristiti izvorne Linear veze za zavisnosti. Status toka rada birati iz
  postojećih stanja tima; potvrđeni tok je `Backlog` → `In Progress` →
  `In Review` → `Done`.
- Za spremnost koristiti [triage mapiranje](triage-labels.md). Oznaka ne
  zamjenjuje stanje issuea niti potvrđuje ispunjenost kriterija prihvata.
- Lokalne specifikacije i radne mape referenciraju Linear identifikator issuea;
  Linear ostaje izvor statusa i zavisnosti.

## Live inventar 2026-09-13

<!-- markdownlint-disable MD013 -->

| Issue | Uloga | Stanje pri syncu |
| --- | --- | --- |
| [ACT-100](https://linear.app/activi/issue/ACT-100/lokalen-crm-scan-in-den-runtime-suchvertrag-ubersetzen) | wayfinder:map, roditelj | In Progress nakon synca |
| [ACT-101](https://linear.app/activi/issue/ACT-101/erlaubten-scan-umfang-festlegen) | opseg skena | Done: nema kandidatskih redova |
| [ACT-102](https://linear.app/activi/issue/ACT-102/verdrahtungsbegriff-festlegen) | pojam Verdrahtung | Done: Q20/Q21 slojevi |
| [ACT-103](https://linear.app/activi/issue/ACT-103/pflichtartefakt-des-scans-festlegen) | obavezni artefakt | otvoren: INNER JOIN i Archiv-Satz |
| [ACT-104](https://linear.app/activi/issue/ACT-104/lokale-scan-quelle-festlegen) | izvor skena | Done: Q22 stari PHP-CRM |
| [ACT-105](https://linear.app/activi/issue/ACT-105/metadaten-dokumentationstools-fur-mysql-8-und-postgres-17-bewerten) | MySQL/PG alati | Done: van Q22 opsega |
| [ACT-106](https://linear.app/activi/issue/ACT-106/jobstep-php-suchpfade-ohne-personenwerte-extrahieren) | PHP metoda | Done: wizards 01–04 |
| [ACT-107](https://linear.app/activi/issue/ACT-107/bestehende-jobstep-mcp-artefakte-gegen-die-suchgrenze-prufen) | gotovi MCP obrasci | Done: auto-SQL nije runtime |
| [ACT-108](https://linear.app/activi/issue/ACT-108/mysql-jobstep-und-postgres-supabase-als-quellen-ordnen) | izvori | Done: PHP objašnjava, Postgres ugovor |
| [ACT-109](https://linear.app/activi/issue/ACT-109/verhaltnis-von-lokalem-scan-zu-gate-b-festlegen) | Scan vs Gate B | Done: dopuna, ne zamjena |

<!-- markdownlint-enable MD013 -->

Otvoreno u mapi ostaje ACT-103 uz INNER JOIN Gruppe/Status i Bericht-Audit
Punkt 2. JSON-Filter je nacrt, ne ugovor.

Pristup servisu slijedi globalno MCP-routing pravilo i
[tool routing](tool-routing.md). Ova konfiguracija određuje projekt; sama ne
odobrava vanjske upise. Granice rada su u
[AGENTS.md](../../AGENTS.md#working-sequence).
