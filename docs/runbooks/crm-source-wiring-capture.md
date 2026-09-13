<!-- markdownlint-disable MD013 -->
# Runbook: CRM-Suchverdrahtung aus dem Quellcode

Datum: 2026-09-12

Status: Anleitung für den Menschen. Kein Datenbankzugriff, kein MCP-Bau,
keine Freigabe von OrbStack, Dump oder Produktion.

Ausführliche Download-Anleitung mit Ort, Befehl und Eintrag in die Vorlage:
[crm-wiring-human-plan.md](crm-wiring-human-plan.md).

Interaktive Scripts: [crm-wiring-wizards.md](crm-wiring-wizards.md).

Zielartefakt: ausgefülltes Verdrahtungsdokument
(`docs/discovery/crm-app-wiring.md` nach Redaktion).

Vorlage zum Kopieren: Abschnitt [Output-Vorlage](#output-vorlage-zum-kopieren).

## Optimaler Weg in einem Satz

Zuerst das **CRM-Repo lesen**. Danach die **Köpfe und Körper der Such-RPCs**
zuordnen. OrbStack oder eine Mac-Installation nur, wenn kein Quellcode
da ist.

```text
CRM-Quellcode
  → welche Maske welche Parameter schickt
Such-RPCs in Postgres
  → wie diese Parameter wirklich filtern
redigiertes Verdrahtungsdokument
  → Felder für den späteren JSON-Filter
erst danach MCP (nicht Teil dieser Anleitung)
```

Nicht tun: CRM auf den Mac installieren, ganze Datenbank dem Agenten geben,
alte `crm_api.search_candidates` 1:1 wrappen, Kandidatenzeilen, Kontakte
oder CVs kopieren.

## Was fertig bedeutet

Diese Anleitung ist fertig, wenn das Output-Dokument existiert und jede
Suchmaske eine der Noten hat:

| Note | Bedeutung |
| --- | --- |
| `BELEGT DURCH QUELLCODE` | Datei + Symbol/Zeile im CRM-Repo. |
| `BELEGT DURCH RPC-KOPF` | Funktionsname und Argumente, ohne Datenzeilen. |
| `ARBEITSANNAHME` | fachliche Lesart, nicht bewiesen. |
| `DURCH DISCOVERY ZU PRÜFEN` | braucht Katalog oder RPC-Körper, nicht raten. |
| `OFFEN` | keine Evidenz. |
| `R1-AUSSCHLUSS` | Kontakt, CV, Notiz, Vertrag, Ausweis. |

Ohne Quellcode-Pfad ist Schritt 1 `FAIL`. Ohne mindestens eine belegte
Suchmaske ist das Dokument `FAIL`. Ein Diagramm ohne Feldliste ist
`FAIL`.

## Stopp

Sofort anhalten, wenn:

- `.env`, Passwörter, Connection-Strings oder API-Keys im Output landen;
- Kandidatenzeilen, E-Mails, Telefone, CVs oder JMBG auftauchen;
- das CRM-Repo in **dieses** Git-Repo kopiert oder committet wird;
- OrbStack/Dump geöffnet werden soll, ohne neue ausdrückliche Freigabe
  (Q10.1d ist derzeit `ABGELEHNT`);
- der Supabase-Developer-Plugin auf Produktion oder Klon zeigt.

Rohes CRM-Repo, Dumps und unredigierte RPC-Körper bleiben **außerhalb Git**.

## Schritt 0 — Lage in 5 Minuten

**Tun.** Entscheide einen Pfad. Nicht kombinieren.

| Lage | Nächster Schritt |
| --- | --- |
| CRM-Quellcode liegt auf der Platte | Schritt 1 |
| Nur lauffähiges Image/Container, kein Code | Halt. OrbStack-Fallback nur nach neuer Freigabe |
| Weder Code noch Image | Halt. Code beschaffen, nicht die DB scannen |

**Prüfen.**

```bash
# Pfad anpassen. Erwartung: Projektwurzel mit app/src/sql o. ä.
ls -ld "/Users/activi/Downloads/crm-master-3"
```

| Check | PASS | FAIL |
| --- | --- | --- |
| Ordner existiert und ist lesbar | weiter zu Schritt 1 | Code holen |
| Enthält `.git` oder `src`/`app`/`*.php`/`*.cs`/`*.ts` | Repo plausibel | vielleicht nur Dump; nicht als Code behandeln |
| Liegt **nicht** in `Dino problem baza crm` | gut | nicht hineinkopieren |

**Output.** Eine Zeile im späteren Dokument: `CRM-Pfad`, Datum, ob Git-Repo.

## Schritt 1 — Repo bereitstellen (kein Install)

**Tun.** Repo bleibt, wo es ist. Kein `npm install`, kein Docker-Start,
keine Datenbank.

**Ausführen.**

```bash
CRM="/Users/activi/Downloads/crm-master-3"   # deinen Pfad einsetzen
test -d "$CRM" || { echo FAIL: pfad; exit 1; }

# Grobe Landkarte, keine Inhalte dump
find "$CRM" -maxdepth 3 -type d | head -80

# Stack-Hinweise
rg -l --glob 'composer.json' --glob 'package.json' --glob '*.csproj' --glob 'Gemfile' --glob 'go.mod' --glob '*.sln' "$CRM" | head
```

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Kein `.env` ins Chat- oder Git-Diff | Datei ignorieren | nicht öffnen, nicht kopieren |
| Keine `*.sql.gz` / Dumps im Arbeitsordner dieses Repos | gut | Datei nicht hierher bewegen |
| Stack grob erkennbar (PHP, .NET, Node, …) | notieren | `OFFEN`, weiter suchen |

**Output.** Felder `stack`, `ausgeschlossene_pfade`.

## Schritt 2 — Suchcode finden

**Tun.** Zuerst zählen, dann nur Trefferpfade notieren. Keine ganzen Dateien
in Git oder Chat.

**Ausführen.**

Die Treffer **vollständig in Dateien** schreiben, dann zählen. Nicht `head`,
nicht die Chat-Ausgabe als Liste verwenden. Eine Ausgabe mit genau 200 Zeilen
ist der alte Fehl-Lauf (vollständiger Rescan: RPC 21, Tabellen 1732, UI 2487
Fundstellen).

```bash
CRM="/Users/activi/Downloads/crm-master-3/src/crm"
OUT=/private/tmp/dino-crm-wiring-work
mkdir -p "$OUT"
cd "$CRM"

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!dist' -g '!*.min.js' -g '!*.sql' -g '!Info/**' -i 'search_candidates(_filtered|_by_occupation)?|job_occupation_map|occupation_alias' > "$OUT/hits-rpc.txt"

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!*.sql' -g '!Info/**' -i 'idk_kandidati|idk_kandidat_radno_iskustvo|idk_kandidat_edukacija|idk_kandidat_jezici|idk_kandidat_vjestine' > "$OUT/hits-tables.txt"

rg -n -g '!node_modules' -g '!vendor' -g '!.git' -g '!*.sql' -g '!Info/**' -i 'kandidat.*such|candidate.*search|filter.*beruf|ausbildung|erfahrung|jezik|sprache|vjestina|skill' > "$OUT/hits-ui.txt"

wc -l "$OUT"/hits-*.txt
```

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Mindestens ein Treffer auf `search_candidates*` **oder** eine Suchmaske | weiter | Muster erweitern; nicht die DB öffnen |
| `wc -l` der Datei, nicht der Chat-Ausschnitt; nicht genau 200 bei tables/ui | vollständige Liste | 200-Deckel oder abgeschnittene Chat-Ausgabe |
| Trefferliste enthält Dateipfad + Symbol, keine Personenwerte | gut | Treffer mit E-Mail/Telefon verwerfen, nur Dateiname behalten |
| Mehr als eine plausible Such-UI (Schnellsuche, Auftrag, Profil) | alle in die Tabelle | fehlende als `OFFEN` führen, nicht erfinden |

**Output.** Rohliste der Dateipfade, nur lokal, z. B.
`/private/tmp/dino-crm-wiring-work/hits-*.txt`. Nicht committen.

## Schritt 3 — Masken inventarisieren

**Tun.** Für jede Suchoberfläche eine Zeile. Typische Kandidaten:

- Kandidaten-Schnellsuche / erweiterte Suche
- Suche am Auftrag / Stellenprofil
- Gruppensuche / gespeicherte Filter
- Detailkarte (ist **keine** Suche; trotzdem notieren, wenn sie Filter teilt)

Pro Maske festhalten:

1. Anzeigename in der UI (Sprache der Maske).
2. Datei der Form / des Controllers / der API.
3. Welche Funktion oder welcher SQL-Aufruf beim Klick Suchen.
4. Ob Kontakte im Ergebnis stehen (`R1-AUSSCHLUSS` markieren, nicht übernehmen).

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Jede Maske hat Quelle (Datei) oder steht auf `OFFEN` | gut | keine namenlosen Masken |
| Suchen ist vom Datensatz öffnen getrennt | gut | Detailkarte nicht als Such-RPC zählen |
| Alte RPC mit E-Mail/Telefon ist als Altlast markiert | gut | nicht als Ziel-MCP übernehmen |

**Output.** Tabelle `Suchmasken` in der Vorlage.

## Schritt 4 — Felder auf Parameter legen

**Tun.** Pro Filterfeld der Maske eine Zeile: Label → Code → RPC-Argument →
physikalische Spalte. Unbekannte Zellen `OFFEN` oder
`DURCH DISCOVERY ZU PRÜFEN`, nie raten.

Pflichtfelder, die ihr später für den JSON-Filter braucht (auch wenn die
Maske sie nicht hat — dann `fehlt in UI`):

- Ausbildungsberuf
- Erfahrungsberuf
- Tätigkeitsart
- Berufssuchprofil (falls die Maske Auftragsprofile nutzt)
- Erfahrung (Dauer) — welches Speicherfeld?
- Ort / Wunschort
- Sprache + Niveau
- Skill
- Alter / Geburtsdatum (sensibel; nur ob die Maske filtert, keine Werte)
- Verfügbarkeit / Status
- Freitext

**Ausführen (Beispiel, Pfade aus Schritt 2 einsetzen).**

```bash
CRM="/Users/activi/Downloads/crm-master-3"
# Eine belegte Suchdatei genauer lesen, lokal
rg -n -i 'beruf|occupation|erfahrung|iskustvo|grad|jezik|vjestina' "$CRM/pfad/zur/Suchdatei"
```

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Drei Berufsschichten sind getrennt oder ausdrücklich `OFFEN` | gut | ein Feld Beruf ohne Schicht ist unvollständig |
| Erfahrung benennt **eine** Quelle oder zwei mit Konflikt | gut | beide Speicher als identisch behandeln ohne Beleg |
| Keine Kontaktspalte im vorgeschlagenen JSON | gut | E-Mail/Telefon raus |

**Output.** Tabelle `Feldkarte`.

## Schritt 5 — RPC-Köpfe zuordnen (ohne Zeilen zu lesen)

Die Filterlogik liegt oft in Postgres, nicht in der UI. Köpfe und Körper
kommen aus schon vorhandenem Katalog / Gate-B3-Rohausgabe **außerhalb Git**,
nicht aus einem neuen Produktionsdump.

Bekannte Namen nur als Suchhilfe, nicht als Beweis dass die UI sie ruft:

- `search_candidates_by_occupation`
- `search_candidates_filtered`
- `crm_api.search_candidates` (Signatur mit Kontakt → nicht wrappen)

**Tun.** Für jede in Schritt 3 belegte Funktion:

1. Schema + Name.
2. Argumentliste (Typen, keine Beispielwerte mit Personen).
3. Welche Maske sie ruft (`BELEGT DURCH QUELLCODE` oder `OFFEN`).
4. Ob die Signatur Kontaktfelder enthält (`R1-AUSSCHLUSS`).

Funktionskörper nur lokal redigiert zitieren: Joins und Filterprädikate,
keine Literale mit Personenbezug. Fehlt der Körper: `DURCH DISCOVERY ZU PRÜFEN`.

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Jede Suchmaske zeigt auf 0..n RPCs, nicht die ganze crm-Shema | gut | PostgREST/CRUD als Suchweg vorschlagen |
| Kontakt-RPC ist ausgeschlossen | gut | 1:1-Wrap vorschlagen |
| Körper unbekannt bleibt unbekannt | gut | Semantik aus dem Funktionsnamen erfinden |

**Output.** Tabelle `RPC-Karte`.

## Schritt 6 — Dokument schreiben und redigieren

**Tun.** Vorlage unten nach
`/private/tmp/dino-crm-app-wiring.md` kopieren, ausfüllen, dann eine
redigierte Fassung nach `docs/discovery/crm-app-wiring.md` nur wenn
keine Secrets und keine Personenwerte enthalten sind.

**Ausführen.**

```bash
test -f docs/runbooks/crm-source-wiring-capture.md

# Grobes Netz gegen Secrets. Treffer nicht in den Chat kopieren.
rg -n -i 'password|api[_-]?key|postgres://|eyJ' /private/tmp/dino-crm-app-wiring.md || true
```

Bei Treffer: Wert löschen, nur Kategorie notieren (`secret`, `email`, …).

**Prüfen.**

| Check | PASS | FAIL |
| --- | --- | --- |
| Jede Tabelle der Vorlage hat Zeilen oder ein ehrliches `keine gefunden` | gut | leere Pflichttabelle |
| Jede Behauptung hat eine Note aus der Legende | gut | nackte Tabellennamen als Wahrheit |
| Datei enthält keine Connection-Strings, keine Personen | gut | nicht nach `docs/` kopieren |
| CRM-Repo selbst nicht in `git status` dieses Repos | gut | `git add` des CRM-Codes rückgängig |

Danach im Dokumentationsrepo:

```bash
scripts/check-local.sh
```

Erwartung: der Script-Lauf ist grün für Doku; er beweist **nicht** die
Verdrahtung.

## Schritt 7 — Abnahme

Mensch liest das Dokument gegen drei Fragen:

1. Welche Maske ist die Recruiter-Hauptsuche?
2. Welche drei Berufsschichten kann diese Maske unterscheiden — oder nicht?
3. Welches Erfahrungsfeld zählt 5 Jahre — oder steht Q8.5 weiter `OFFEN`?

Erst nach dieser Abnahme darf der JSON-Filter entworfen werden. Das ist
eine **andere** Arbeit ([ADR-0001](../decisions/0001-controlled-query-boundary.md),
[Katalog-Mapping](../discovery/catalog-domain-mapping.md)).

## Fallback: kein Quellcode

Nur wenn Schritt 0 kein Repo ergibt **und** eine neue ausdrückliche
Freigabe Q10.1d vorliegt:

1. CRM und Postgres lokal, Dump nicht auf Produktion zeigen.
2. Statements der Suche mitschneiden, lokal, mit striktem Output-Schutz.
3. Eine Maske klicken, SQL-Text der Suche zuordnen, dieselben Tabellen
   wie oben füllen.
4. Keine Ergebniszeilen speichern.

Ohne diese Freigabe bleibt der Fallback geschlossen. Mac-Installation
ist kein besserer Fallback.

## Was diese Anleitung nicht liefert

- Runtime-Such-MCP
- neue Postgres-Funktion
- Entscheidung Q8.5
- Berufssuchprofil-Verwaltung
- Restore- oder Gleichstandsnachweis für OrbStack/Dump/ZIP

## Output-Vorlage zum Kopieren

Arbeitskopie: Vorlage [crm-app-wiring.template.md](../discovery/crm-app-wiring.template.md)
nach `/private/tmp/dino-crm-app-wiring.md` kopieren und ausfüllen.
Nach Redaktion optional nach `docs/discovery/crm-app-wiring.md`.

````markdown
# CRM-Suchverdrahtung

Stand: YYYY-MM-DD
Status: ENTWURF
CRM-Pfad: /absoluter/pfad   # nicht committen, wenn privat
Stack: OFFEN | php | dotnet | node | …
Git-Revision CRM: unbekannt | <kurz-sha>
Datenbank in diesem Lauf: keine

## 1. Suchmasken

| Maske (UI-Name) | Datei / Symbol | Ruft | Kontakte im Ergebnis | Note |
| --- | --- | --- | --- | --- |
| | | RPC oder SQL-Name | ja/nein | |

Hauptsuche laut Code: OFFEN

## 2. Feldkarte

| UI-Label | Code-Symbol | RPC-Argument | Physisch (Tabelle.spalte) | Schicht | Note |
| --- | --- | --- | --- | --- | --- |
| | | | | Ausbildungsberuf / Erfahrungsberuf / Tätigkeitsart / Erfahrung / Ort / Sprache / Skill / Alter / Status / Freitext / sonst | |

## 3. RPC-Karte

| Schema.funktion | Argumente (ohne Werte) | Von Maske | Kontaktfelder | Note |
| --- | --- | --- | --- | --- |
| | | | ja/nein | |

Nicht wrappen: crm_api.search_candidates, falls Kontakt in der Signatur.

## 4. Beruf und Erfahrung

| Frage | Befund | Note |
| --- | --- | --- |
| Kann die Hauptsuche Ausbildung ohne Erfahrung setzen? | | |
| Kann sie Erfahrung ohne Ausbildung setzen? | | |
| Tätigkeitsart getrennt? | | |
| Welches Feld zählt Dauer? | Akte / Lebenslauf-Liste / beide / OFFEN | |
| Berufssuchprofil = welche Tabelle? | occupation-Hierarchie / idk_kandidat_pozicija / idk_nalog_profil / OFFEN | |

## 5. R1-Ausschluss in der alten Suche

| Fläche | Vorkommen in Maske/RPC | Folge |
| --- | --- | --- |
| E-Mail / Telefon | | nicht in JSON-Filter, nicht in MCP-Output |
| CV-Text | | |
| Notizen | | |

## 6. Lücken

- OFFEN:
- DURCH DISCOVERY ZU PRÜFEN:
- ARBEITSANNAHME:

## 7. Nicht entschieden (bewusst leer)

JSON-Filter, MCP-Tools, Ranking, Auth. Erst nach Abnahme von Abschnitt 1-4.
````

## Verwandte Dokumente

- [End-to-end Runtime-Such-MCP](runtime-search-mcp-end-to-end.md) — von
  dieser Verdrahtung bis zum nutzbaren MCP, inklusive Gates.
- [Katalog zu Domäne](../discovery/catalog-domain-mapping.md) — physische
  Objekte aus Gate B2, ohne App-Verdrahtung.
- [Discovery-Runbook](schema-discovery.md) — read-only Schema-Audit.
- [ADR-0001](../decisions/0001-controlled-query-boundary.md) — JSON statt SQL.
- [ADR-0002](../decisions/0002-search-design-interview.md) — Q10.1d OrbStack.
- [Autowire-Befund](../research/mcp-autowire-candidates.md) — kein Auto-MCP.
