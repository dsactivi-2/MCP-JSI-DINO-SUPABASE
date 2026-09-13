<!-- markdownlint-disable MD013 -->
# Entwurf: JSON-Filter R1 (alte Kandidati-Filter)

Stand: 2026-09-13

Status: **ENTWURF**, geprüft 2026-09-13 gegen PHP `lista_kandidata` und
Heft (Q4, Q8.5, Q15, Q17–Q22). Kein Runtime-MCP, kein Scaffold, kein
Produktions-SQL, kein abgenommener Vertrag. ADR-0001: LLM liefert nur
dieses JSON; Postgres sucht. Cap 50.

Quellen: PHP-Hauptsuche + Heft (Q17). Alltag Q18 2026-09-13. Filter-SQL:
[crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md). Maske:
[crm-app-wiring.md](crm-app-wiring.md).

## Prüfung 2026-09-13

Die POST-Felder der Hauptsuche sind im JSON. R1 bleibt die alte
Recruiter-Maske, nicht occupation, nicht Ort, nicht Skills.

| Lücke | Stand | Nicht tun |
| --- | --- | --- |
| Struke/Smjer = Ausbildungsberuf? | Wizard 03 **BESTÄTIGT** 2026-09-13. PHP filtert über Schul-Smjer-Namen in `idk_kandidat_edukacija.ke_naziv_kvalifikacije`. | JSON nicht in `ausbildungsberuf` umbenennen; Q8.4 nicht überschreiben |
| „5 Jahre“ / Jahres-Erfahrung | **nicht in R1**, Nutzer 2026-09-13 **BESTÄTIGT** nein. Alte UI nur ja/nein (`has_work_experience`). Q8.5.3–8 bleiben für später. | kein `years`-Feld erfinden; Zettel-2-Aktenzahlen nicht als Filter |

PHP-Nuancen, die der Entwurf **nicht** 1:1 kopiert (Q21), aber kennt:

| PHP | Folge für diesen Entwurf |
| --- | --- |
| Alter nur wenn `starost_od` **und** `starost_do` gesetzt | nur beide Grenzen oder kein Altersfilter; eine Grenze allein ablehnen |
| Führerschein / Erfahrung nur Wert `DA` | JSON nur `true` filtert; `false` ablehnen (kein alter „ohne“-Filter) |
| `filter_smjer` gesetzt | Schule- **und** Struke-Bedingung fallen weg |
| Cookie `archive_status` | SQL nur Status 3; Formularfilter fallen weg. Klassen danach an Liste-SQL und Zähl-SQL; Suchbox `search[value]` nur an Liste-SQL, nicht an Zähl-SQL. R1 übernimmt den PHP-Zählfehler nicht (Q21). Mischung nur-Archiv + andere Filter: ablehnen (`VORLÄUFIGER VORSCHLAG`) |
| `filter_boravak` als Rohstring `LIKE` | später parametrisiert; Semantik bleibt „gewählte Werte“ |
| `INNER JOIN` Gruppe und Status | PHP lässt sie still weg. R1 **nicht**: ohne Gruppe/Bearbeitung bleiben sie sichtbar (`BESTÄTIGT` 2026-09-13). Andere Filter gelten weiter. |

Heft Q8: UND zwischen Kategorien ist dort `VORLÄUFIGER VORSCHLAG`. PHP
ist AND (`BELEGT`). R1 folgt der alten Maske (Q18 Alltag). Sprachen
UND/ODER aus Q8 ändert R1 nicht: Deutsch und Englisch bleiben zwei
Felder, AND dazwischen.

Q19/Q20: alle Status-Ebenen sind **gescannt**. Messenger und Task-Force
stehen **nicht** in dieser Filter-Maske, deshalb **nicht** in diesem
JSON. Welche Statuswerte der Runtime-MCP später anbietet, bleibt fein
**OFFEN**.

## Umfang R1

Nur die Recruiter-Hauptsuche
`kandidati.php?page=list_ajax` → `lista_kandidata`.
Kein Partner, kein QC, kein Nalog.

Drei Berufsschichten und Berufssuchprofile bleiben **Fachmodell** (Q8.4).
R1 hat dafür **keine** neuen Filterfelder.

Nachrichten C 4–9 gehören nicht in diesen Filter (Produkt default aus).

## Nicht in R1 (absichtlich)

| Feld | Warum raus |
| --- | --- |
| Ort / Stadt / Wunschort | Wizard 03: erst alte Filter |
| Skills | Wizard 03 |
| Berufssuchprofil / occupation | Wizard 03 + Q22 |
| Erfahrungsjahre / „5 Jahre“ | **kein R1-Feld** (`BESTÄTIGT`); alte UI nur ja/nein; Q8.5.3–8 gelten erst, wenn Jahre ein Filter werden |
| Freitext-Volltext wie `search.php` | nicht die Kandidatensuche |
| Messenger-Status, Task-Force | nicht in dieser Filter-Maske; Scan liegt in der Status-Datei |
| Partner-/QC-/Nalog-Suche | R1 nur Hauptsuche |
| `has_work_experience: false` / `driving_license: false` | PHP kennt nur DA oder tot; kein „ohne“-Filter |
| ältere Maske `kandidati.php?page=list` | Alltag Q18 = `list_ajax`, nicht der Modal |

Q8.5.3–8 (nur passende Jobs, Überlappung nicht addieren, aktueller Job
bis heute, ähnliche Schreibweisen, Listen zuerst) bleiben bestätigt.
Sie gelten, **wenn** später Jahres-Erfahrung ein Filter wird. In R1 setzen
sie keinen Jahresfilter.

Struke/Smjer: JSON nutzt die PHP-Namen. PHP-Pfad ist Struke →
`idk_skole_smjerovi.ss_naziv` → gleiches Smjer-LIKE auf
`ke_naziv_kvalifikacije`. Das ist bei euch der Ausbildungsberuf
(`BESTÄTIGT` 2026-09-13). Nicht occupation mappen, Q8.4 nicht
überschreiben.

## Regeln

| Regel | Stand |
| --- | --- |
| Unbekanntes JSON-Feld oder unzulässiger Wert | ablehnen |
| Weggelassenes oder leeres Feld | inaktiv, keine Einschränkung (Q8, PHP `1`) |
| Mehrere Kategorien | UND, wie PHP AND (Heft Q8 dazu nur `VORLÄUFIGER VORSCHLAG`) |
| Mehrere Werte in einer Liste | ANY (PHP `IN`) |
| Archiv | default raus (`kandidat_status != 3`); `exclude_archived: false` = nur Status 3, ohne andere Filter |
| Alter | nur wenn `age.min` **und** `age.max` gesetzt; sonst tot oder ablehnen |
| Boolean-Filter | nur `true` schränkt ein; `false` ablehnen |
| Seite | höchstens 50 |
| Null Treffer | bleiben null; Lockerung nur nach Bestätigung (Q7) |
| SQL vom LLM | verboten |
| `crm_api.search_candidates` | nicht wrappen |
| Identität / Rolle | nicht im Filter; kommt aus Auth. Interne sehen Kontakte (Q4) |

Bestätigung vor jeder Suche: `BESTÄTIGT` 2026-09-13. Erst Filter zeigen,
dann eine Datenbanksuche.

## Filterfelder

Englische JSON-Namen. PHP-POST nur zur Spur.

| JSON | PHP | Bedeutung | Werte |
| --- | --- | --- | --- |
| `age.min` / `age.max` | `starost_od` / `starost_do` | Alter | ganze Jahre; nur beide Grenzen; PHP nur Geburtsjahr |
| `driving_license` | `vozacka_dozvola` | Führerschein vorhanden | nur `true`; PHP sucht `Da` im Feld |
| `driving_categories` | `filter_kategorija_vozacke` | Klassen | Liste; PHP: B zieht höhere mit — später modernisieren |
| `has_work_experience` | `radno_iskustvo` | mindestens eine Jobzeile | nur `true`, **keine** Jahre |
| `german` | `znanje_njemacki` | Deutsch | siehe Sprachen |
| `english` | `znanje_engleski` | Englisch | analog |
| `groups` | `filter_grupe` | Kandidatengruppe | ID-Liste |
| `processing_status` | `filter_status` | Bearbeitung 0–8 | ID-Liste |
| `application_status` | `filter_status_prijave` | Prijave; 0 schließt NULL ein | ID-Liste; Labels DB, kein Dump |
| `source` | `filter_izvor` | Herkunft `kandidat_porijeklo` | ID-Liste; Partner 6 nimmt 7 mit (PHP) |
| `citizenship` | `filter_drzavljanstvo` | EU / NON-EU | `eu`, `non_eu`; beide gesetzt = kein Filter |
| `eu_residence` | `filter_boravak` | Boravak EU | Liste; nicht Stadt |
| `struke` | `filter_struke` | Ausbildungsberuf über Schul-Smjer; tot wenn `smjer` gesetzt | ID-Liste; JSON-Name bleibt `struke` |
| `schools` | `filter_skole` | Schulen | Liste/Text wie PHP LIKE |
| `smjer` | `filter_smjer` | Smjer; verdrängt Schule **und** Struke | Text/ID wie PHP |
| `dipl_status` | `filter_dipl_status` | DIPL 0–7; 0 = nicht in DIPL | ID-Liste |
| `nostrification` | `filter_vrsta_nostrifikacije` | Nostrifikation | Liste; 3 = NULL oder in Liste (PHP) |
| `exclude_archived` | Archiv-Cookie | default `true` | `false` nur Archiv (Status 3), ohne andere Filter |
| `q` | DataTables-Suchbox | Name, Statusname, Gruppe; intern auch E-Mail/Mobil | string, optional |
| `limit` | — | Seitengröße | 1–50, default 50 |
| `cursor` | — | nächste Seite | opaque; Ranking OFFEN |

### Sprachen

Objekt oder weggelassen:

- `min_listening`: A1–C2 → Hörfeld `kj_slusanje` diese Stufe **oder höher**
- `none`: BEZ ZNANJA
- `no_info`: keine Deutsch-/Englisch-Zeile mit A1–C2/BEZ ZNANJA
- `any` / leer: Filter aus (`svi`)

Nur Hörfeld, wie PHP. Tippfehler doppeltes B1 in A1-Zweig nicht übernehmen.

## Beispiel

Weggelassene Felder zählen nicht.

```json
{
  "age": { "min": 22, "max": 45 },
  "driving_license": true,
  "has_work_experience": true,
  "german": { "min_listening": "B1" },
  "processing_status": [1, 2],
  "struke": [12],
  "exclude_archived": true,
  "limit": 50
}
```

Kein Berufssuchprofil, keine Jahre, keine Stadt.

## Treffer (interner Vermittler)

PHP-SELECT enthält unter anderem ID, Name, Geburt, Geschlecht, JMBG,
Bearbeitung, Messenger, E-Mail, Mobil, Gruppe, Herkunft, CV-Flags,
Nalog-Name, Statusname.

Q4: intern ja inklusive Kontakt. Kunde ist nicht Aufrufer dieser
Pool-Suche. Discovery speichert keine Werte. JMBG ist besonders
sensibel; ob R1 ihn wirklich ausgibt, bleibt vor Implementierung
zu bestätigen.

Zusätzlich später (nicht in diesem Entwurf fest): stabile ID,
Match-Beweis, `next_cursor`. Ranking/Tie-Breaker OFFEN.

Kunde-Projektion (ohne Kontakt, nur Vorschlag) ist ein anderer
Aufrufer, nicht R1-Hauptsuche.

## Was das JSON nicht ist

- kein MCP-Server und keine Zod-Installation
- keine Postgres-Funktion und kein Apply
- kein Ersatz für Auth, RLS, Tenant
- kein 1:1-Abbild des PHP-SQL-Strings (Q21)

Spätere Runtime darf eine **neue** Funktion nutzen
(Vorschlagname nur: `crm_search.search_candidates_v1(jsonb)`).
Alte CRM-RPCs nicht wrappen.

## Offen, ehrlich

| Thema | Stand |
| --- | --- |
| Struke/Smjer = Ausbildungsberuf? | **BESTÄTIGT**; JSON bleibt `struke` / `smjer` |
| Wie „5 Jahre“ im Filter zählen | **kein** R1-Feld (`BESTÄTIGT`); Q8.5.3–8 unberührt |
| Messenger / Task-Force im JSON | nicht in der Maske; Q19 fein **OFFEN** |
| Archiv plus andere Filter | PHP wirft Formularfilter weg; Entwurf lehnt die Mischung ab |
| Stille PHP-Joins ohne Gruppe/Status | **BESTÄTIGT** nein; sichtbar lassen, nicht INNER JOIN kopieren |
| Prijave-Labels | DB, kein Dump |
| Ranking / Cursor-Spalte | OFFEN |
| JMBG in der Trefferliste | PHP ja; R1-Ausgabe unbestätigt |
| Bestätigung vor jeder Suche | `BESTÄTIGT`: Filter zeigen, dann eine Suche |
| Auth / Hosting / SDK | ein Such-MCP, Tokens je Rolle (`BESTÄTIGT`); Hosting/SDK-Version OFFEN |
| Export | CSV/Excel, Recruiter wählt; max. 500; inkl. JMBG und Kontakt; nicht Kunde |

## Nächster Schritt

Bericht-Audit Punkte 1–3 bestätigt. Archiv-Satz bleibt: PHP-Zählfehler
nicht nachbauen. Struke/Smjer = Ausbildungsberuf. „5 Jahre“ nicht in R1.
Ohne Gruppe/Bearbeitung sichtbar. JSON bleibt Entwurf, kein Vertrag.
Nicht Tool-Namen, keine Produktion, kein MCP-Bau, kein Wizard 01/04.
