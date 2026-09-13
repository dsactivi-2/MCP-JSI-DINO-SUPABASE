<!-- markdownlint-disable MD013 -->
# Wizards: CRM-Suchverdrahtung

Datum: 2026-09-12

Drei interaktive Bash-Wizards für die Schritte, die nur du auf dem Mac
machen kannst. Sie öffnen Dateien, fragen Pfade ab und scannen Quellcode.
Sie bauen **keinen** MCP, schreiben **kein** Projekt-`.env` und legen
**keine** GitHub-Secrets an.

Nachschlagewerk ohne Script:
[crm-wiring-human-plan.md](crm-wiring-human-plan.md).

## Optimaler Weg (nicht ein Riesen-Wizard)

Ein Wizard, der jede Tabellenzeile im Terminal abfragt, ist langsamer und
fehleranfälliger als Code lesen. Deshalb drei Phasen:

```text
01 locate-and-scan     du: Pfad + Verbote
                       script: Vorlage kopieren, rg/grep, Treffer speichern
                    → Codex den CRM-Pfad schicken   ← empfohlen
                       oder 02 selbst mappen
03 accept              du: drei Abnahmefragen + Secret-Check
```

Nach 01 ist **Codex mit dem CRM-Pfad** der kürzere Weg für Tabellen 1–3.
Wizard 02 nur, wenn du die Zuordnung selbst im Editor machen willst.

## Welchen Wizard du wann startest

| Situation | Wizard |
| --- | --- |
| Noch kein CRM-Pfad, keine Trefferlisten | `crm-wiring-01-locate-and-scan.sh` |
| 01 ist durch, Tabellen soll Codex füllen | **kein** Wizard. Pfad in diesen Chat. |
| 01 ist durch, du mapst selbst | `crm-wiring-02-map-search.sh` |
| Tabellen stehen, Abnahme fehlt | `crm-wiring-03-accept.sh` |
| Codebefund steht in der Arbeitsdatei | **nicht** 02. `crm-wiring-03-accept.sh` (jetzt gegen den Befund) |
| Status-Ebenen, Cron, Trigger | **nicht** 01. `crm-wiring-04-status-and-triggers.sh` |
| Kein Quellcode, nur OrbStack | **keinen** Wizard. Q10.1d ist gesperrt. |
| MCP / JSON-Filter / Produktion | **keinen** dieser Wizards. |

Wenn 01 schon gelaufen ist: `/private/tmp/dino-crm-wiring.env` existiert.
Dann nicht nochmal bei null anfangen, ausser du willst den Scan wiederholen.

## Starten

Im Terminal (einmal `chmod` ist schon gesetzt):

```bash
cd "/Users/activi/Documents/ChatGPT/Dino problem baza crm"
scripts/wizards/crm-wiring-01-locate-and-scan.sh
```

Später:

```bash
scripts/wizards/crm-wiring-02-map-search.sh
scripts/wizards/crm-wiring-03-accept.sh
```

Stoppen: `Ctrl-C`. Erneut starten ist idempotent: bekannte Werte in
`/private/tmp/dino-crm-wiring.env` mit Enter behalten.

## Was wo landet

| Datei | Inhalt | Git? |
| --- | --- | --- |
| `/private/tmp/dino-crm-wiring.env` | CRM-Pfad, Stack, Trefferzahlen, Abnahme | nein |
| `/private/tmp/dino-crm-app-wiring.md` | ausgefüllte Verdrahtung | nein, erst nach Redaktion |
| `/private/tmp/dino-crm-wiring-work/` | Roh-Treffer `hits-*.txt` | nein |
| Doku-Repo | nur diese Anleitung und Scripts | ja |

Kein Wizard schreibt ins Projekt-`.env`. Kein `gh secret`.

## Phasen im Detail

### 01 — Pfad und Scan

Entspricht Plan A–E.

1. Verbote bestätigen (kein Install, kein OrbStack, kein Copy ins Doku-Repo).
2. CRM-Pfad eingeben; Script prüft Ordner und Lage außerhalb des Doku-Repos.
3. Vorlage nach `/private/tmp/dino-crm-app-wiring.md` kopieren (existierende
   Datei nur nach Rückfrage überschreiben).
4. Stack grob erkennen, `.env` im CRM nicht öffnen.
5. Drei Suchläufe (`rg`, sonst `grep`), **ohne** Zeilen-Deckel. `*.sql` und
   `Info/` ausgeschlossen (Dump). Stand 2026-09-13: RPC 21, Tabellen 1732,
   UI 2487.
6. Trefferordner öffnen und den nächsten Schritt nennen.

### 02 — Mapping (optional)

Entspricht Plan F–H, nur wenn du **nicht** Codex die Tabellen füllen lässt.
Wenn die Arbeitsdatei schon `BELEGT DURCH QUELLCODE` enthält, bricht 02
standardmäßig ab und verweist auf 03.

1. Prüft, dass 01 gelaufen ist.
2. Fragt: selbst mappen? **Nein** = Pfad anzeigen, Ende (empfohlen).
3. Tabelle Suchmasken, dann Feldkarte, dann RPC-Karte — je Editor + Enter.
4. Kurze Notizen ans Ende der Arbeitsdatei hängen.

### 03 — Abnahme

Nicht die drei Hit-Dateien abfragen. Quelle ist
`/private/tmp/dino-crm-app-wiring.md` nach dem Codebefund.

1. Hauptsuche = Kandidati-Filter? ja/nein/OFFEN
2. Release 1 nur diese Suche, keine Nebenmasken?
3. Struke/Smjer = Ausbildungsberuf? MCP trotzdem drei Berufsschichten?
4. Was zählt 5 Jahre? (alte UI hat nur ja/nein)
5. R1 trotzdem Ort, Skills, Berufssuchprofil — obwohl die alte UI sie nicht filtert?
6. SQL/PHP mit Personenfeldern lesen, ohne Datensatz-Dump (Q4: interne Kontakte im Produkt).
7. Secret-Netz, Git-Check, Status.

Antworten 2026-09-13 in ADR-0002: 1–2 ja; 3 Ausbildungsberuf (JSON struke/smjer);
4 R1-Jahre Q8.5.9; 5 nein für Ort/Skills/Profil in R1.

Rohzettel: [crm-php-hits](../discovery/crm-php-hits/). Lesart:
[crm-app-wiring.md](../discovery/crm-app-wiring.md). Quellenrang: ADR-0002 Q17.

Bewusst nicht im Wizard abfragen. Ranking/Auth/Export: ADR-0002. Filter-SQL liegt in
[crm-filter-sql-codebefund.md](../discovery/crm-filter-sql-codebefund.md).
Status-Klicks: [crm-status-codebefund.md](../discovery/crm-status-codebefund.md).

### 04 — Status und Automatik

Nicht 01 wiederholen. Nutzt den gespeicherten CRM-Pfad. Schreibt Zettel nach
[crm-php-hits/status](../discovery/crm-php-hits/status/). Lesart:
[crm-status-codebefund.md](../discovery/crm-status-codebefund.md).

Liefergegenstand bleibt `/private/tmp/dino-crm-app-wiring.md`.

## Stopp

Wizards abbrechen, wenn sie nach Passwörtern, Connection-Strings oder
Kandidatenzeilen fragen würden — das tun sie nicht. Wenn der Scan Treffer
mit Personenwerten in **Kommentaren** zeigt: Datei schließen, nur den
Dateinamen notieren, nichts in die Arbeitsdatei kopieren.

## Verwandte Dateien

- [scripts/wizards/crm-wiring-01-locate-and-scan.sh](../../scripts/wizards/crm-wiring-01-locate-and-scan.sh)
- [scripts/wizards/crm-wiring-02-map-search.sh](../../scripts/wizards/crm-wiring-02-map-search.sh)
- [scripts/wizards/crm-wiring-03-accept.sh](../../scripts/wizards/crm-wiring-03-accept.sh)
- [Vorlage](../discovery/crm-app-wiring.template.md)
- [Kompakt-Runbook](crm-source-wiring-capture.md)
