# Prompt: Audit der rekonstruierten Entscheidungen

Kopiere den folgenden Auftrag als erste Nachricht in eine neue Codex-Session im
gespeicherten Projekt **Dino problem baza CRM**. Die neue Session soll im
vorhandenen Projektordner arbeiten, nicht in einem neuen Worktree.

## Auftrag an den neuen Agenten

Du arbeitest ausschließlich im bestehenden Projekt:

`/Users/activi/Documents/ChatGPT/Dino problem baza crm`

Prüfe unabhängig, ob die aus einem langen und bereits komprimierten Chat
rekonstruierten Fragen, Antworten und Architekturentscheidungen korrekt,
vollständig und widerspruchsfrei in den Projektdateien gespeichert wurden.

### Verbindlicher Matt-Flow

Verwende zuerst den Matt-Flow `/grill-with-docs`, weil dies eine
zustandsbehaftete Prüfung in einem bestehenden Repository ist. Falls dieser
Wrapper in deiner Session nicht verfügbar ist, verwende den primitiven Skill
`/grilling` zusammen mit `/domain-modeling` und erkläre den Fallback kurz.

Verwende nicht `/code-review`: Für diese Prüfung gibt es keinen verlässlichen
Git-Festpunkt und keine Implementierung, sondern einen Entscheidungs- und
Dokumentationsstand.

### Grenzen

- Dies ist zunächst ein Review, keine Korrekturfreigabe.
- Verändere keine vorhandene Projektdatei.
- Greife nicht auf die Datenbank zu.
- Erstelle keine externen Tickets und führe keine externen Writes aus.
- Die einzige erlaubte neue Datei ist dein Prüfbericht unter
  `docs/reviews/decision-reconstruction-audit.md`.
- Bewahre den vorhandenen Dirty Worktree und alle unversionierten Dateien.
- Behaupte nichts als bestätigt, was nicht durch die unten stehenden
  Nutzeraussagen oder eine akzeptierte Entscheidung belegt ist.
- Behandle eine Zusammenfassung niemals als Ersatz für direkte Evidenz.

### Zuerst vollständig lesen

1. `AGENTS.md`
2. `docs/project.md`
3. `CONTEXT.md`
4. `docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md`
5. `docs/decisions/0001-controlled-query-boundary.md`
6. `docs/decisions/0002-search-design-interview.md`
7. `docs/decisions/0003-separated-profile-administration-mcp.md`
8. `docs/runbooks/schema-discovery.md`
9. `docs/research/berufssuchprofile-q8-4-2.md`
10. `README.md`

Lies außerdem vor jedem Tool-Aufruf
`/Users/activi/Code/Tools/shared/mcp-routing.md` und verwende für
Shell-Befehle `rtk` beziehungsweise `rtk proxy`.

### Direkte Entscheidungsevidenz aus dem bisherigen Nutzerverlauf

Die folgenden Aussagen sind die verfügbare Primärevidenz. Rechtschreibfehler
wurden nur dort normalisiert, wo die Bedeutung eindeutig ist:

| Thema | Direkte Aussage oder eindeutige Bedeutung |
| --- | --- |
| Q1 | „zuerst A danach C“: zuerst Discovery-Bericht, danach produktiver MCP. |
| Q2 | „A“: kleine interne Recruiter-Gruppe. |
| Q3 | „für alle Rollen ich“: Der Nutzer übernimmt alle erläuterten Rollen. |
| Q4 | „nein“: keine Kontaktdaten im ersten Release. |
| Q5 | „ja ist zwingend“: Altersfilter ist zwingend. |
| Q6 | „nein“: keine verpflichtende Prüfung durch eine zweite Person. |
| Q7 | „Option B“: exakte Suche bleibt unverändert; bei null Treffern werden Lockerungen vorgeschlagen und nur nach Zustimmung gesucht. |
| Q8 | Globale Optionen A und B wurden abgelehnt; Option C sollte angepasst werden. |
| Q8-Regeln | Der Nutzer entschied später alle zu Q8.4 empfohlenen Punkte für alle Kategorien. |
| Q8.4 | Breite Anforderungen sollen über kontrollierte, wiederverwendbare Berufssuchprofile abgebildet werden. |
| Q8.4.2 | Berufe dürfen durch ein Profil nicht blockiert werden, können mehreren Profilen angehören und bleiben direkt suchbar. |
| Profilverwaltungs-MCP | Der Nutzer verlangte, die Entscheidung zu einem zusätzlichen MCP, seinem Zweck und seinen Fähigkeiten dauerhaft festzuhalten. |
| Fehlende Filter | Wird ein Filter nicht erwähnt, ist er nicht wichtig und darf die Suche nicht einschränken. |
| Beispiel Erfahrung | „Elektriker mit fünf Jahren Berufserfahrung“ verlangt keine entsprechende Ausbildung, wenn Ausbildung nicht genannt wurde. |
| Q9 | „Option C“: Sicherheitsvoraussetzungen klären, danach read-only Discovery, anschließend Interview fortsetzen. |
| Tabellenzahl | Der Nutzer gab 179 Tabellen an; noch nicht durch Discovery verifiziert. |
| Q4.5 | Der Nutzer erklärte ausdrücklich: „Q4.5 ist offen.“ Der genaue Fragetext fehlt. |
| Q8.5 | Noch offen; der Nutzer wollte erst nach Q8.4.2 dazu zurückkehren. |

Bei Aussagen wie „alle empfohlenen Punkte“ musst du besonders prüfen, ob eine
Datei mehr festlegt, als die vorher tatsächlich beschriebenen Empfehlungen
umfassten. Markiere nicht direkt belegbare Details als `UNVERIFIZIERBAR` oder
`ÜBERINTERPRETIERT`, statt sie stillschweigend zu akzeptieren.

### Prüfachsen

Prüfe jede Entscheidung entlang dieser sechs Achsen:

1. **Evidenztreue:** Entspricht die gespeicherte Antwort der direkten
   Nutzeraussage?
2. **Status:** Ist sie korrekt als bestätigt, teilweise bestätigt, offen,
   abgelehnt oder ersetzt markiert?
3. **Vollständigkeit:** Fehlt eine ausdrückliche Nutzerentscheidung in ADR,
   Brief, Projektstatus oder Glossar?
4. **Überinterpretation:** Wurde eine Empfehlung oder Nachfrage fälschlich als
   Entscheidung gespeichert?
5. **Dokumentkonsistenz:** Widersprechen sich ADR-0002, ADR-0003,
   Implementierungsbrief, Projektstatus, `CONTEXT.md` oder `AGENTS.md`?
6. **Phasenkonsistenz:** Behauptet ein Dokument Datenbankfakten, Tabellen,
   Felder, Rechte oder technische Verträge, die erst der Discovery bestätigen
   kann?

Prüfe besonders:

- Q3 und Q6, weil sie zwischenzeitlich fälschlich als offen rekonstruiert waren;
- die Grenze zwischen vollständig bestätigter Q8.4 und offener Q8.5;
- ob Q4.5 wirklich nur als offen ohne erfundenen Inhalt gespeichert ist;
- ob der Profilverwaltungs-MCP korrekt als spätere Komponente nach Discovery
  und nicht als bereits implementiert dargestellt wird;
- ob automatische Berufszuordnungen nur Vorschläge bleiben;
- ob ein Beruf in mehreren Profilen und weiterhin direkt suchbar bleibt;
- ob nicht genannte Filter tatsächlich inaktiv bleiben;
- ob Q9 Option C korrekt gespeichert ist;
- ob die Zahl 179 als Nutzerangabe und nicht als verifizierte Datenbanktatsache
  behandelt wird;
- ob alle offenen Fragen weiterhin sichtbar sind.

### Erforderlicher Bericht

Schreibe `docs/reviews/decision-reconstruction-audit.md` mit:

1. Gesamtstatus `PASS`, `PASS_WITH_GAPS` oder `FAIL`;
2. einer Tabelle mit den Spalten
   `Entscheidung`, `Evidenz`, `Fundstelle`, `Bewertung`, `Begründung`;
3. bestätigten korrekten Einträgen;
4. Widersprüchen und falschen Statusangaben;
5. fehlenden Entscheidungen;
6. überinterpretierten oder nicht beweisbaren Aussagen;
7. offenen Fragen, die versehentlich geschlossen wurden;
8. konkreten Korrekturvorschlägen pro Datei und Abschnitt;
9. einer Liste aller Punkte, die nur der Nutzer klären kann;
10. einer klaren Aussage, welche Prüfung ohne vollständiges ursprüngliches
    Chatprotokoll nicht möglich ist.

Zitiere bei jedem Befund die genaue Datei und Überschrift. Trenne strikt:

- `VERIFIZIERT`: durch direkte Evidenz oder technische Prüfung belegt;
- `PLAUSIBEL`: konsistent, aber nicht vollständig direkt belegt;
- `UNVERIFIZIERBAR`: erforderliche Primärevidenz fehlt;
- `WIDERSPRUCH`: Quellen stimmen nicht überein;
- `FEHLT`: ausdrückliche Entscheidung wurde nicht gespeichert;
- `ÜBERINTERPRETIERT`: Dokument behauptet mehr als die Evidenz.

Nimm noch keine Korrekturen vor. Zeige dem Nutzer zuerst den vollständigen
Bericht und frage anschließend ausdrücklich, ob die vorgeschlagenen Änderungen
übernommen werden sollen.

### Verifikation

Nach Erstellung des Berichts ausführen:

```bash
rtk proxy markdownlint-cli2 '*.md' 'docs/**/*.md'
rtk git diff --check
rtk git status --short
```

Melde die tatsächlichen Ergebnisse. Ein nicht ausführbarer Check ist ein Gap,
kein Erfolg.
