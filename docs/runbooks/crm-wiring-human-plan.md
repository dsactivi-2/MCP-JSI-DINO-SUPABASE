<!-- markdownlint-disable MD013 MD024 -->
# Plan: CRM-Suchverdrahtung erfassen

Datum: 2026-09-12

Das ist die **Download-Anleitung für dich**. Du arbeitest am Mac, Schritt
für Schritt. Kein Datenbank-Login, kein OrbStack, kein CRM-Install, kein MCP-Bau.

Bevorzugt die Wizards statt die Befehle unten abzutippen:
[crm-wiring-wizards.md](crm-wiring-wizards.md).
`01` scannen, Tabellen **Codex** oder `02`, Abnahme `03`.

Kompakte Variante für Agenten:
[crm-source-wiring-capture.md](crm-source-wiring-capture.md).
Leere Output-Datei:
[crm-app-wiring.template.md](../discovery/crm-app-wiring.template.md).

Zeit: A–C etwa 20 Minuten, D–E etwa eine Stunde, F–G ein Nachmittag,
H–J etwa eine Stunde.
Du darfst nach jedem Schritt aufhören. Die Arbeitsdatei bleibt liegen.

---

## Was am Ende in der Hand ist

Eine ausgefüllte Markdown-Datei auf deinem Mac:

`/private/tmp/dino-crm-app-wiring.md`

Darin stehen nur vier Dinge:

1. Welche Suchmasken das alte CRM hat.
2. Welches UI-Feld welchen Code und welche Postgres-Funktion füttert.
3. Welche Such-RPCs die App wirklich aufruft.
4. Was unbekannt bleibt (`OFFEN`), statt zu raten.

Das ist **noch nicht** der MCP. Der MCP kommt erst, wenn diese Datei
abgenommen ist.

---

## Drei Orte — merken und nicht vermischen

| Name | Typischer Pfad | Darf ins Git *Dino problem baza crm*? |
| --- | --- | --- |
| Doku-Repo (diese Anleitung) | `/Users/activi/Documents/ChatGPT/Dino problem baza crm` | ja, nur Doku |
| CRM-Quellcode | z. B. `/Users/activi/Documents/crm-legacy` | **nein** |
| Arbeitsdatei | `/private/tmp/dino-crm-app-wiring.md` | nein, erst nach Redaktion |

Das CRM-Repo **nicht** in den Doku-Ordner kopieren, nicht per Drag-and-Drop
dahin ziehen, nicht `git add`en.

---

## Stopp — sofort aufhören

Halt, wenn eines zutrifft:

- Du siehst Passwörter, `.env`, `postgres://`, API-Keys.
- Du siehst echte E-Mails, Telefone, CVs, JMBG oder Kandidatenzeilen.
- Du willst OrbStack, Dump oder ZIP öffnen (das braucht eine **neue** Freigabe).
- Du willst das CRM installieren oder Docker starten.
- Der Supabase-Plugin hängt an Produktion.

Bei einem Treffer: Wert **nicht** in Chat, Mail oder Git. Nur notieren:
`secret gefunden in Datei X, gelöscht`.

---

## Noten, die in jede Tabellenzeile gehören

| Note in die letzte Spalte | Wann |
| --- | --- |
| `BELEGT DURCH QUELLCODE` | Du hast Datei und ungefähre Zeile gesehen. |
| `BELEGT DURCH RPC-KOPF` | Du hast Funktionsname und Argumente, keine Personenwerte. |
| `ARBEITSANNAHME` | Fachlich plausibel, nicht bewiesen. |
| `DURCH DISCOVERY ZU PRÜFEN` | Braucht Katalog oder Funktionskörper, nicht raten. |
| `OFFEN` | Nichts gefunden. Das ist eine gültige Antwort. |
| `R1-AUSSCHLUSS` | Kontakt, CV, Notiz, Vertrag, Ausweis — nicht in den späteren MCP. |

Eine Zeile ohne Note ist unbrauchbar.

---

## A — Werkzeuge einmal prüfen (5 Minuten)

### Ziel

Terminal und Suche funktionieren. Du installierst **kein** CRM.

### Wo

1. Spotlight (`Cmd+Leertaste`), `Terminal` eingeben, Enter.
2. Das Fenster bleibt für den ganzen Plan offen.

### Ausführen

```bash
pwd
date
command -v rg
command -v grep
```

### PASS

- `pwd` druckt irgendeinen Ordner. Egal welchen.
- `command -v rg` druckt einen Pfad, z. B. `/opt/homebrew/bin/rg`.

### FAIL und Reparatur

`rg` fehlt: in demselben Terminal

```bash
command -v brew && brew install ripgrep
```

Ohne Homebrew: die `rg`-Befehle unten durch `grep -R -n -i` ersetzen.
Langsamer, geht.

Editor: TextEdit geht, VS Code/Cursor ist besser für Tabellen.
Datei immer als reinen Text / Markdown speichern, nicht als `.pages`.

---

## B — Arbeitsdatei anlegen (3 Minuten)

### Ziel

Leere Vorlage liegt unter `/private/tmp/`, bereit zum Ausfüllen.

### Wo

Dasselbe Terminal. Du wechselst kurz ins **Doku-Repo**, nicht ins CRM.

### Ausführen

```bash
cd "/Users/activi/Documents/ChatGPT/Dino problem baza crm"
test -f docs/discovery/crm-app-wiring.template.md || { echo FAIL: vorlage fehlt; exit 1; }
cp docs/discovery/crm-app-wiring.template.md /private/tmp/dino-crm-app-wiring.md
open -a TextEdit /private/tmp/dino-crm-app-wiring.md
```

`open -a TextEdit` durch `cursor` oder `code` ersetzen, wenn du den Editor
so startest.

### PASS

- Der Befehl `cp` schweigt.
- Die Datei öffnet sich. Oben steht `# CRM-Suchverdrahtung`.
- `Stand: YYYY-MM-DD` ist noch Platzhalter.

### In die Datei schreiben (jetzt sofort)

1. `Stand:` auf das heutige Datum, z. B. `2026-09-12`.
2. `Status:` auf `ENTWURF` lassen.
3. `Datenbank in diesem Lauf: keine` so lassen.
4. Speichern (`Cmd+S`).

---

## C — Schritt 0: Liegt Quellcode da? (5–15 Minuten)

### Ziel

Du weißt den **absoluten Pfad** des CRM-Codes. Ohne diesen Pfad ist der
Rest `FAIL`.

### Wo

- Finder, oder
- Spotlight nach Ordnern wie `crm`, `idk`, `legacy`, oder
- du weißt den Pfad schon (USB, Git-Klon, Zip entpackt).

Der Ordner muss **Code** enthalten (`*.php`, `*.cs`, `*.ts`, `src/`, `app/`,
`.git`). Ein SQL-Dump oder ein Docker-Volume ist **kein** Quellcode.

### Ausführen (Pfad anpassen)

Ersetze nur die erste Zeile durch deinen echten Pfad. Den Rest nicht ändern.

```bash
CRM="$HOME/Documents/crm-legacy"
ls -ld "$CRM"
ls "$CRM" | head
```

Wenn du den Pfad nicht kennst:

```bash
mdfind -name 'composer.json' 2>/dev/null | head
mdfind 'idk_kandidati' 2>/dev/null | head
```

Die Treffer nur als Pfad notieren. Dateien mit Kandidatenwerten nicht öffnen.

### PASS

`ls -ld` zeigt `drwx...` und den Ordner. `ls` zeigt Projektzeugs, nicht nur
`dump.sql` / `backup.zip`.

### FAIL

| Lage | Was du tust |
| --- | --- |
| Ordner existiert nicht | Code besorgen. Hier aufhören. |
| Nur Image/OrbStack, kein Code | Hier aufhören. Nicht C–H weiter. Fallback ist gesperrt. |
| Ordner liegt **in** `Dino problem baza crm` | rausverschieben, nicht committen. |

### In die Arbeitsdatei

- `CRM-Pfad:` den Wert von `echo "$CRM"` (absolut, nicht `~`).
- Speichern.

Ab hier gilt: **jedes neue Terminal** muss `CRM=...` wieder setzen.
Praktisch: die Zeile oben in einem Textsnippet behalten.

---

## D — Schritt 1: Repo ansehen, nicht starten (10 Minuten)

### Ziel

Stack erkennen (PHP, .NET, Node, …). App **nicht** bauen, **nicht** starten.

### Wo

Terminal, Variable `CRM` gesetzt. Finder darfst du parallel auf denselben
Ordner legen (`open "$CRM"`), aber nichts Doppelklicken das die App startet.

### Ausführen

```bash
CRM="$HOME/Documents/crm-legacy"
test -d "$CRM" || { echo FAIL: pfad; exit 1; }
echo "CRM=$CRM"
find "$CRM" -maxdepth 3 -type d | head -80
ls "$CRM"/composer.json "$CRM"/package.json "$CRM"/*.sln "$CRM"/*.csproj 2>/dev/null
git -C "$CRM" rev-parse --short HEAD 2>/dev/null || echo 'kein git'
```

Nicht ausführen: `npm install`, `composer install`, `dotnet run`, `docker compose up`.

### PASS

- `find` listet Unterordner wie `src`, `app`, `backend`, `public`.
- Mindestens eine Stack-Datei **oder** viele Quellcode-Endungen.
- Git-Hash oder ehrliches `kein git`.

### In die Arbeitsdatei

- `Stack:` z. B. `php` / `dotnet` / `node` / `OFFEN`.
- `Git-Revision CRM:` Kurz-Hash oder `unbekannt`.
- Unter Lücken, falls `.env` existiert: `env-Datei vorhanden, nicht geöffnet`.

`.env` nicht mit `cat` ausgeben.

---

## E — Schritt 2: Suchcode finden (20–40 Minuten)

### Ziel

Eine Trefferliste **von Dateipfaden**, nicht der ganze Dateiinhalt im Chat.

### Wo

Terminal im CRM-Ordner. Ausgabe darfst du in eine lokale Textdatei lenken.

### Ausführen

```bash
CRM="$HOME/Documents/crm-legacy"
cd "$CRM"
mkdir -p /private/tmp/dino-crm-wiring-work

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!dist' -g '!*.min.js' -g '!*.sql' -g '!Info/**' -i 'search_candidates(_filtered|_by_occupation)?|job_occupation_map|occupation_alias' > /private/tmp/dino-crm-wiring-work/hits-rpc.txt

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!*.sql' -g '!Info/**' -i 'idk_kandidati|idk_kandidat_radno_iskustvo|idk_kandidat_edukacija|idk_kandidat_jezici|idk_kandidat_vjestine' > /private/tmp/dino-crm-wiring-work/hits-tables.txt

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!*.sql' -g '!Info/**' -i 'kandidat.*such|candidate.*search|filter.*beruf|ausbildung|erfahrung|jezik|sprache|vjestina|skill' > /private/tmp/dino-crm-wiring-work/hits-ui.txt

wc -l /private/tmp/dino-crm-wiring-work/hits-*.txt
open /private/tmp/dino-crm-wiring-work
```

Ohne `rg`:

```bash
grep -R -n -i --exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=.git --exclude='*.sql' 'search_candidates' "$CRM"
```

### PASS

- Mindestens eine der drei Dateien hat mehr als 0 Zeilen, **oder**
- du findest per Dateinamen eine Suchmaske (`Search`, `Suche`, `Filter`).

`wc -l` darf `0` für eine der drei Dateien sein. Nicht für alle drei.
Kein `head -200`: der Deckel hat die Hauptsuche in den Zetteln versteckt.
Die gültige Zahl ist `wc -l` der ganzen Datei. Eine Chat-Ausgabe, die bei
200 Zeilen endet, ist unvollständig — nicht 200 Dateien, sondern abgeschnitten.

### FAIL

Alle drei `0` Zeilen: Muster sind zu eng. Dann im Finder nach Ordnern
`search`, `suche`, `kandidat` sehen und **einen** Trefferpfad notieren.
Nicht die Datenbank öffnen, um das zu ersetzen.

### Wie du eine Trefferzeile liest

Beispiel:

`src/Search/CandidateSearch.php:142: search_candidates_filtered(`

Bedeutung: Datei `src/Search/CandidateSearch.php`, Zeile 142, Aufruf der
Funktion. In die Vorlage kommt dieser Pfad, nicht die ganze PHP-Datei.

Datei im Editor öffnen:

```bash
open -a TextEdit "$CRM/src/Search/CandidateSearch.php"
```

Pfad aus **deiner** Trefferliste einsetzen, nicht diesen Beispielpfad.

Wenn die Datei E-Mails oder Telefonnummern von Personen zeigt: Fenster
schließen. In die Vorlage nur: `R1-AUSSCHLUSS, Datei nicht zitiert`.

### In die Arbeitsdatei

Noch keine fertige Masken-Tabelle. Nur unter **Lücken**:

- `Treffer RPC: N Zeilen`
- `Treffer Tabellen: N Zeilen`
- `Treffer UI: N Zeilen`

Die Rohlisten bleiben in `/private/tmp/dino-crm-wiring-work/`. Nicht Git.

---

## F — Schritt 3: Masken inventarisieren (30–60 Minuten)

### Ziel

Abschnitt **1. Suchmasken** der Arbeitsdatei hat echte Zeilen.

### Wo

- Links: Trefferliste `hits-ui.txt` / `hits-rpc.txt`.
- Rechts: Arbeitsdatei `/private/tmp/dino-crm-app-wiring.md`.
- Bei Bedarf eine Quelldatei im Editor, **eine** nach der anderen.

### Wie du eine Maske erkennst

Typisch sind getrennte Oberflächen. Jede wird eine Tabellenzeile:

- Schnellsuche / erweiterte Kandidatensuche
- Suche am Auftrag / Stellenprofil
- Gruppensuche / gespeicherte Filter
- Detailkarte eines Kandidaten (das ist **keine** Suche; nur notieren,
  wenn sie dieselben Filter teilt)

Pro Maske brauchst du vier Felder:

1. Name, den ein Recruiter auf dem Bildschirm lesen würde.
2. Datei und Funktion/Methode.
3. Was beim Klick Suchen aufgerufen wird (RPC-Name oder SQL-Name).
4. Ob das Ergebnis E-Mail/Telefon enthält (`ja` → `R1-AUSSCHLUSS`).

### Ausführen

Keine neuen Shell-Pflichtbefehle. Du liest die Trefferdateien und öffnest
nur die Dateien, deren Namen nach Suche aussehen.

Hilfssuche in einer schon bekannten Datei (Pfad ersetzen):

```bash
CRM="$HOME/Documents/crm-legacy"
rg -n -i 'function |def |search|filter|rpc|select ' "$CRM/pfad/zur/Suchdatei" | head -80
```

### Beispielzeile (nur Format, keine Wahrheit über euer CRM)

| Maske (UI-Name) | Datei / Symbol | Ruft | Kontakte im Ergebnis | Note |
| --- | --- | --- | --- | --- |
| Erweiterte Suche | `app/Controllers/Search.php:search()` | `search_candidates_filtered` | ja | `BELEGT DURCH QUELLCODE` |

Wenn du den UI-Namen nicht siehst: Dateinamen in Spalte 1, Note `ARBEITSANNAHME`.

### PASS

- Mindestens **eine** Zeile mit Datei und Note.
- Jede weitere vermutete Maske steht entweder als Zeile oder als `OFFEN`.
- Detailkarte ist nicht als einzige „Suche“ eingetragen.

### In die Arbeitsdatei

- Tabelle **1. Suchmasken** füllen.
- Zeile `Hauptsuche laut Code:` setzen oder `OFFEN` lassen.
- Speichern.

---

## G — Schritt 4: Felder auf Parameter legen (1–2 Stunden)

### Ziel

Tabelle **2. Feldkarte**: jedes Filterfeld der Hauptsuche eine Zeile.

### Wo

Dieselbe Hauptsuche-Datei aus Schritt F. Arbeitsdatei daneben.

### Pflichtzeilen, auch wenn die Maske sie nicht hat

Wenn ein Feld in der UI fehlt: Spalte UI-Label `fehlt in UI`, Note `OFFEN`.

- Ausbildungsberuf
- Erfahrungsberuf
- Tätigkeitsart
- Berufssuchprofil
- Erfahrung (Dauer)
- Ort / Wunschort
- Sprache + Niveau
- Skill
- Alter / Geburtsdatum (nur ob gefiltert wird, **keine** Geburtsdaten kopieren)
- Verfügbarkeit / Status
- Freitext

### Ausführen

```bash
CRM="$HOME/Documents/crm-legacy"
rg -n -i 'beruf|occupation|erfahrung|iskustvo|ausbildung|edukacija|grad|jezik|sprache|vjestina|skill|alter|datum' "$CRM/pfad/zur/Suchdatei"
```

Pro Treffer entscheidest du die **Schicht** (Spalte in der Vorlage):

| Schicht | Bedeutung |
| --- | --- |
| Ausbildungsberuf | formaler Lehrberuf / Abschluss |
| Erfahrungsberuf | ausgeübter Beruf in der Biografie |
| Tätigkeitsart | Art der Arbeit, feiner als Berufsname |
| Erfahrung | Dauer in Monaten/Jahren |
| sonst | nur wenn es wirklich nicht passt |

Ein einziges UI-Feld „Beruf“ ohne Schicht: Zeile anlegen, Schicht `OFFEN`,
nicht heimlich auf Ausbildungsberuf setzen.

Zwei Erfahrungsfelder (Akte vs. Lebenslauf-Liste): **zwei Zeilen**, nicht
zusammenwerfen.

### Beispielzeile (nur Format)

| UI-Label | Code-Symbol | RPC-Argument | Physisch | Schicht | Note |
| --- | --- | --- | --- | --- | --- |
| Berufserfahrung (Jahre) | `$minExp` | `min_experience_years` | `idk_kandidati.kandidat_iskustvo_u_struci` | Erfahrung | `ARBEITSANNAHME` |

Physikalische Spalten nur schreiben, wenn der Code sie nennt. Sonst
`DURCH DISCOVERY ZU PRÜFEN`.

### PASS

- Alle Pflichtzeilen existieren (Inhalt oder `fehlt in UI`).
- Keine E-Mail-/Telefon-Spalte als Suchfeld für den späteren MCP.
- Drei Berufsschichten sind getrennt oder ausdrücklich `OFFEN`.

### In die Arbeitsdatei

Tabelle **2. Feldkarte** und Abschnitt **4. Beruf und Erfahrung**.

---

## H — Schritt 5: RPC-Köpfe zuordnen (30–60 Minuten)

### Ziel

Tabelle **3. RPC-Karte**. Du liest **keine** Kandidatenzeilen.

### Wo

Zuerst nur der **CRM-Code** (welche Funktion die Maske ruft).
Funktionskörper aus Postgres nur, wenn du sie schon als Gate-B3-Rohausgabe
**außerhalb Git** hast. Keinen neuen Dump ziehen, kein `psql` auf Produktion.

Namen nur als Suchhilfe:

- `search_candidates_by_occupation`
- `search_candidates_filtered`
- `crm_api.search_candidates` — wenn E-Mail/Telefon in der Signatur:
  `R1-AUSSCHLUSS`, nicht wrappen.

### Ausführen

```bash
CRM="$HOME/Documents/crm-legacy"
rg -n -g '!vendor' -g '!node_modules' -g '!.git' 'search_candidates' "$CRM" | head -100
```

Pro Treffer in die RPC-Karte:

1. Schema und Name, so weit der Code sie nennt (`crm_api.search_candidates`).
2. Argumentnamen/Typen, **ohne** Beispielwerte von Personen.
3. Welche Maske aus Abschnitt 1 sie ruft.
4. Kontaktfelder ja/nein.

Funktionskörper unbekannt: Note `DURCH DISCOVERY ZU PRÜFEN`, nicht aus dem
Namen erfinden, was die Funktion filtert.

### PASS

- Jede Suchmaske aus F zeigt auf 0..n RPCs (0 ist erlaubt, dann `OFFEN`).
- Keine Zeile „ganze Tabelle `crm` als API“.
- Kontakt-RPC ist als Ausschluss markiert.

### In die Arbeitsdatei

Tabelle **3. RPC-Karte** und Abschnitt **5. R1-Ausschluss**.

---

## I — Schritt 6: Redigieren und sichern (15 Minuten)

### Ziel

Die Arbeitsdatei enthält keine Secrets und keine Personen. Rohcode bleibt
außerhalb des Doku-Repos.

### Wo

Terminal plus Arbeitsdatei.

### Ausführen

```bash
rg -n -i 'password|api[_-]?key|postgres://|eyJ' /private/tmp/dino-crm-app-wiring.md || true
cd "/Users/activi/Documents/ChatGPT/Dino problem baza crm"
git status --short
```

`git status` darf **nicht** das CRM-Repo oder Dumps zeigen. Falls doch:
diese Dateien nicht `git add`en, aus dem Doku-Ordner entfernen.

Optional, nur wenn die Datei sauber ist, ins Doku-Repo kopieren:

```bash
cp /private/tmp/dino-crm-app-wiring.md "/Users/activi/Documents/ChatGPT/Dino problem baza crm/docs/discovery/crm-app-wiring.md"
```

Das ist **kein** Muss in diesem Plan. Die Datei unter `/private/tmp/` reicht
als Liefergegenstand an den nächsten Chat.

### PASS

- Secret-Suche findet nichts, oder du hast die Treffer gelöscht.
- Jede Pflichttabelle hat Zeilen oder `keine gefunden`.
- Jede Behauptung hat eine Note.

---

## J — Schritt 7: Abnahme (10 Minuten, du allein)

Lies die Arbeitsdatei und beantworte schriftlich unten in Abschnitt 4 oder 6:

1. Welche Maske ist die Recruiter-Hauptsuche?
2. Kann diese Maske Ausbildungsberuf, Erfahrungsberuf und Tätigkeitsart
   **getrennt** setzen — oder nicht?
3. Welches Feld zählt „5 Jahre Erfahrung“ — Akte, Lebenslauf-Liste, beide,
   oder `OFFEN`?

Wenn Frage 3 `OFFEN` ist: richtig so. Nicht erfinden. Das bleibt Q8.5.

`Status:` in der Arbeitsdatei setzen:

- `PASS_WITH_GAPS` wenn Masken + Feldkarte stehen und Lücken ehrlich sind.
- `FAIL` wenn keine Maske belegt ist.

Danach: Pfad der Datei in den Chat legen. Nicht den CRM-Code mitschicken.

---

## Was du in diesem Plan nicht tust

- CRM auf dem Mac installieren
- OrbStack / Dump / ZIP öffnen
- Produktion per Plugin oder `psql` anfassen
- MCP-Server bauen
- JSON-Filter erfinden, bevor J beantwortet ist

Fallback ohne Quellcode existiert nur nach **neuer** Freigabe Q10.1d.
Der steht bewusst nicht als ausführbare Schritte hier.

---

## Checkliste zum Abhaken

- [ ] A Terminal und `rg` oder `grep` gehen
- [ ] B `/private/tmp/dino-crm-app-wiring.md` existiert
- [ ] C `CRM=` ist ein existierender Code-Ordner außerhalb des Doku-Repos
- [ ] D Stack notiert, nichts installiert
- [ ] E mindestens eine Trefferliste > 0 oder eine Suchdatei gefunden
- [ ] F Tabelle Suchmasken hat eine belegte Zeile
- [ ] G Pflichtfelder stehen, Schichten nicht vermischt
- [ ] H RPC-Karte oder ehrliches `OFFEN`
- [ ] I keine Secrets, CRM-Code nicht in Git
- [ ] J drei Abnahmefragen beantwortet

Fertig ist nur die abgehakte Liste plus Datei unter `/private/tmp/`.
