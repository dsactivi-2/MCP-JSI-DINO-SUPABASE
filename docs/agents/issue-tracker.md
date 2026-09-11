# Issue tracker: Linear

Ovaj repozitorij koristi postojeći namjenski projekt **Dino problem baza CRM**.
Identitet projekta i pripadnost timu potvrđeni su read-only provjerom
2026-09-10.

Read-only inventar 2026-09-11 vratio je nula issuea u ovom projektu. Lokalni
[plan Release-1 automatizacijskih ticketa](../planning/release-1-automation-tickets.md)
zato koristi privremene ključeve `AUTO-01` do `AUTO-08`; oni nisu Linear ID-ovi.
Vanjski upis i povezivanje zavisnosti čeka zasebnu freigabe i završetak blokirajućih
design odluka.

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

Pristup servisu slijedi globalno MCP-routing pravilo. Ova konfiguracija
određuje projekt; sama ne odobrava vanjske upise. Granice rada su u
[AGENTS.md](../../AGENTS.md#working-sequence).
