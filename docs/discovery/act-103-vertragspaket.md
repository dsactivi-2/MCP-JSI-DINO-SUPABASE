<!-- markdownlint-disable MD013 -->
# ACT-103 Vertragspaket

Stand der Quellen: 2026-09-13

Status: **PACK / KEIN VERTRAG**. Dieses Dokument schließt
[ACT-103](https://linear.app/activi/issue/ACT-103/pflichtartefakt-des-scans-festlegen)
nicht. Es macht den JSON-Filter nicht zum Vertrag. Es startet keinen MCP.
Erzeugt von scripts/discovery/build-act-103-vertragspaket.py.
Bei Konflikt gilt die neueste ausdrückliche Antwort in
[ADR-0002](../decisions/0002-search-design-interview.md).

## Wozu das Paket da ist

ACT-103 fragt, welches Scan-Stück die Wayfinder-Karte beenden darf:
redigiertes Data Dictionary, Mapping auf den Suchvertrag, JSON-Filter- und
RPC-Allowlist-Vorschlag, oder eine andere Kombination. Ein Runtime-MCP, ein
ER-Diagramm oder ein 1:1-Dump der Datenbank zählen nicht.

Linear lässt ACT-103 offen wegen INNER JOIN, Archiv-Satz und weil JSON
Entwurf bleibt. Unten siehst du, was lokal schon bestätigt ist, und
kreuzt nur die drei offenen ACT-103-Fragen.

## Quellen

| Datei | Rolle |
| --- | --- |
| [crm-work-inventory.md](crm-work-inventory.md) | PHP-Scan-Landkarte |
| [crm-json-filter-draft.md](crm-json-filter-draft.md) | R1 JSON-Entwurf |
| [ADR-0002](../decisions/0002-search-design-interview.md) | neueste ausdrückliche Antworten |
| [issue-tracker.md](../agents/issue-tracker.md) | Linear ACT-103 ist Todo |

## Schon bestätigt — nicht neu aufrollen

| ID | Stand | Kern |
| --- | --- | --- |
| Q4 | `ERSETZT` 2026-09-12 | Interner Vermittler sieht Pool + Kontakte. Kunde nie den ganzen Pool. Vorschlagsfreigabe ohne Kontakt, Einstellungsfreigabe = CONTACT-02. Plugin nie auf Produktion. Discovery ohne Datensatz-Dump. |
| Q8.4 | bestätigt im Prinzip | drei Berufsschichten + Berufssuchprofile, auch wenn die alte Maske sie nicht so trennt |
| Q8.5 | `TEILWEISE` | 8.5.3–8 und 8.5.9: R1-Jahre aus von–bis, Job + Jobgruppe |
| Q15.6 | `TEILWEISE` | Blättern und Datei; CSV+Excel; max. 500; JMBG+Kontakt; nicht ganzer Bestand |
| Q17 | `BESTÄTIGT` | Heft und alte UI/PHP gleichberechtigt; Heft ist keine Whitelist |
| Q18 | `TEILWEISE` | Codebefund + Alltag; Struke/Smjer = Ausbildungsberuf; R1-Jahre Q8.5.9; INNER JOIN nicht kopieren |
| Q19 | `TEILWEISE` | Status-Ebenen und Automatik als Codebefund |
| Q20 | `TEILWEISE` | Jetzt: Filter, alle Status, Auslöser, A, B7, C 4–9 Codebefund. Produkt default aus. 10 und 11–16 später |
| Q21 | `BESTÄTIGT` | Funktionen erfassen, modern umsetzen, nicht 1:1 PHP-SQL |
| Q22 | `BESTÄTIGT` | Jetzt nur altes CRM. occupation / Akten-Jahre / Stadt-Skills-als-Filter kein jetziger Scan |
| ADR-0001 | akzeptiert | LLM nur JSON-Filter; Postgres sucht; Cap 50 |

Zusätzlich aus ADR-0002 Q18 / Bericht-Audit 2026-09-13:

- INNER JOIN Gruppe/Status in R1: **nicht** kopieren. Ohne Gruppe/Bearbeitung sichtbar.
- Archiv-Satz: PHP-Zählfehler kennen, in R1 nicht kopieren. Punkt 2 **Ja**.
- JSON bleibt Entwurf, kein Vertrag. Punkt 3 **Ja**.
- Vorbericht-PASS zählt nicht. Punkt 1 **Ja**.
- Struke/Smjer = Ausbildungsberuf; JSON-Namen bleiben struke / smjer.
- Jahresfilter R1 Q8.5.9: von–bis, Job + Jobgruppe. Alte UI bleibt ja/nein.
- Ranking R1: größte kandidat_id zuerst.
- JMBG intern in der Trefferliste ja, kein Filter, Discovery ohne Werte.

## Bleibt Entwurf oder OFFEN — nicht hier schließen

| Thema | Stand im JSON-Entwurf |
| --- | --- |
| Struke/Smjer = Ausbildungsberuf? | **BESTÄTIGT**; JSON bleibt `struke` / `smjer` |
| Wie „mindestens X Jahre“ zählen | **R1** Q8.5.9: von–bis, Job + Jobgruppe; Q8.5.3–8 |
| Messenger / Task-Force im JSON | nicht in der Maske; Q19 fein **OFFEN** |
| Archiv plus andere Filter | PHP wirft Formularfilter weg; Entwurf lehnt die Mischung ab |
| Stille PHP-Joins ohne Gruppe/Status | **BESTÄTIGT** nein; sichtbar lassen, nicht INNER JOIN kopieren |
| Prijave-Labels | DB, kein Dump |
| Ranking / Cursor-Spalte | OFFEN |
| JMBG in der Trefferliste | PHP ja; R1-Ausgabe unbestätigt |
| Bestätigung vor jeder Suche | `BESTÄTIGT`: Filter zeigen, dann eine Suche |
| Auth / Hosting / SDK | ein Such-MCP, Tokens je Rolle (`BESTÄTIGT`); Hosting/SDK-Version OFFEN |
| Export | CSV/Excel, Recruiter wählt; max. 500; inkl. JMBG und Kontakt; nicht Kunde |

- JSON-Filter R1: **ENTWURF**, geprüft, kein Vertrag.
- Q15.6 Export: siehe ADR-0002. Nicht eine der drei ACT-103-Fragen unten.
- Auth, Hosting, SDK, Tenant: nicht gewählt. Nicht ACT-103.
- RPC-Allowlist / redigiertes Data Dictionary: in den Scan-Dateien nicht als abgenommenes Pflichtartefakt geführt.

## Quellenkonflikt

- JSON-Entwurf: Ranking/Cursor OFFEN. ADR-0002 Q18: Ranking R1 bestätigt, kandidat_id absteigend.
- JSON-Entwurf: JMBG-Ausgabe unbestätigt. ADR-0002 Q18: JMBG intern bestätigt ja, kein Filter.

Neueste ausdrückliche Antwort in ADR-0002 gewinnt. Der JSON-Entwurf wird
dadurch nicht still zum Vertrag.

## Drei Fragen — nur du kreuzt

Eine Option pro Zeile. Leere Kreuze bedeuten: noch keine Antwort. Ein Kreuz
in dieser Datei ist erst eine Antwort, wenn du sie ausdruecklich sagst; das
Script füllt sie nicht.

| # | Frage | Option A | Option B | Option C | Dein Kreuz |
| --- | --- | --- | --- | --- | --- |
| 1 | Welches Pflichtartefakt beendet ACT-103? | Inventar + Codebefunde + JSON-Entwurf reichen | Zusätzlich redigiertes Data Dictionary oder Mapping auf den kanonischen Vertrag | Zusätzlich RPC-Allowlist, bevor die Karte endet | |
| 2 | INNER JOIN und Archiv-Satz | Für ACT-103 geschlossen (Antworten 2026-09-13 in ADR-0002 / Inventar / Entwurf) | Bleiben offen, bis sie im JSON-Vertrag stehen | Linear-Text anpassen, Inhalt bleibt bestätigt | |
| 3 | Darf ACT-103 Done werden, solange JSON ENTWURF ist? | Ja; Pflichtartefakt ist der geprüfte Entwurf, Vertrag kommt später (AUTO-02) | Nein; erst JSON zum Vertrag, dann ACT-103 Done | Ja, aber nur zusammen mit Option 1A und 2A | |

Nicht ankreuzen und nicht in dieser Runde entscheiden: MCP-Bau, Tool-Namen,
Eval-MCP, Produktions-Apply, Q15.6, Auth.

## Was dieses Paket nicht tut

- ACT-103 nicht auf Done setzen
- JSON nicht zum Vertrag erklären
- keine Linear-Writes
- keinen MCP scaffolden
- keine Schema-Tatsachen erfinden
