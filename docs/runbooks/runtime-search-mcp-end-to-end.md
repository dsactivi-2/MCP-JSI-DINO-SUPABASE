<!-- markdownlint-disable MD013 -->
# End-to-end: von der Jobstep-Verdrahtung zum nutzbaren Runtime-Such-MCP

Datum: 2026-09-12

Status: operative Anleitung. Kein Stack-Beschluss, kein Produktions-Apply,
kein Ersatz für Freigaben.

## Optimierte Lage in einem Satz

Nicht die ganze Datenbank scannen und nicht die ganze Repo crawlen.
Den **bereits vorhandenen Postgres-Katalog** als Rückgrat nehmen, die
**Jobstep-Suchmasken gezielt lesen**, daraus den **JSON/RPC-Vertrag**
schreiben, den MCP **zuerst synthetisch** nutzbar machen, und erst nach
Freigabe auf echte Kandidaten schalten.

~~~text
Gate-B-Katalog + Mapping     → was physisch existiert
Jobstep-Suchmasken (PHP)     → wie Recruiter wirklich filtern
JSON-Filter + neue RPC       → was der Agent dürfen soll
MCP SDK v2 lokal synthetisch → Form ist nutzbar
Freigabe + Runtime-Rolle     → echte Kandidaten, ohne Kontakte
~~~

## Warum das optimaler ist als „Repo zuerst“ oder „DB scannen“

| Weg | Urteil |
| --- | --- |
| Ganze Jobstep-Repo als Quelle der Wahrheit | Zu laut. `kandidati.php` allein ist ~650 KiB UI+SQL. Enthält Kontakte. Spricht MySQL, nicht den Runtime-Vertrag. |
| OrbStack/MySQL-Dump scannen | Erklärt die Herkunft, beweist nicht Postgres. Enthält echte Personendaten. Q10.1d derzeit abgelehnt. |
| Synthetische candidate-search-mcp-Demo | Nur Mechanik. Keine echten Tabellen, kein Beweis. |
| Alten `crm_api.search_candidates` wrappen | NO-GO: Signatur mit E-Mail/Telefon, verletzt Q4. |
| Auto-MCP / PostgREST auf `crm.*` | NO-GO: LLM oder Client sieht Tabellen/SQL. ADR-0001. |
| **Katalog (liegt vor) + gezielte Masken + neuer RPC + MCP SDK v2** | Optimal: jede Quelle tut nur das, was sie beweisen kann. |

Der Katalog
[catalog-domain-mapping.md](../discovery/catalog-domain-mapping.md)
existiert schon (Gate B2 V3). Die Masken-Anleitung
[crm-source-wiring-capture.md](crm-source-wiring-capture.md)
existiert schon. Dieses Dokument verbindet beides bis zum nutzbaren MCP
und überspringt keine Gates.

Zwei Nutzbarkeitsstufen, nicht vermischen:

| Stufe | Was du tun kannst | Was du nicht darfst |
| --- | --- | --- |
| **C — lokal nutzbar** | In ChatGPT/Codex/Claude gegen synthetische Kandidaten suchen | Keine echten Personen, kein Produktionsprojekt |
| **D — produktiv nutzbar** | Kleine interne Recruiter-Gruppe gegen echte Akten, ohne Kontakte | Kein Plugin auf Produktion, kein service_role, kein Auto-SQL |

Bekannter lokaler CRM-Pfad (nicht in dieses Git kopieren):

~~~text
/Users/activi/Downloads/crm-master-3
~~~

Erste Maskendateien, nicht der ganze Baum:

~~~text
src/crm/kandidati.php
src/crm/ssdata_search.php
src/crm/components/Kandidati/
~~~

## Verbote, die in jedem Schritt gelten

- Keine Kandidatenzeilen, E-Mails, Telefone, CVs, JMBG, Passwörter in Chat, Git oder Reports.
- CRM-Repo, Dumps, `.env` und RPC-Rohkörper bleiben außerhalb dieses Repos, bis redigiert.
- Kein Supabase-Developer-Plugin auf das Produktionsprojekt.
- MCP-Token ist nie das Datenbankpasswort.
- Runtime hat kein `service_role`, kein Superuser, kein BYPASSRLS.
- Null Treffer bleiben null, bis der Recruiter eine konkrete Lockerung bestätigt (Q7).

---

## Teil A — Evidenz (jetzt, ohne MCP-Bau)

### Schritt 1 — Katalog-Mapping lesen, nicht neu scannen

**Tun.** Öffne
[catalog-domain-mapping.md](../discovery/catalog-domain-mapping.md)
und [crm-schema-static-analysis.md](../discovery/crm-schema-static-analysis.md).
Markiere nur, was du als Mensch akzeptierst oder ablehnst.

**Pflichtfragen an dich:**

1. Ist `crm.idk_kandidati` die Hauptsuche-Akte für Release 1?
2. Bleiben `idk_nd_kandidata` / DIPL in R1 draußen, drin, oder `OFFEN`?
3. Ist `occupation` + `job_occupation_map` die Taxonomie, oder nur ein Zusatz?

**PASS.** Jede Zeile des Mappings hat eine Note, und die drei Fragen haben
eine ausdrückliche Antwort in ADR-0002 oder im Mapping-Dokument.
**FAIL.** Neue Tabellen erfunden oder PHP-Namen 1:1 als MCP-Felder übernommen.

### Schritt 2 — Suchmasken gezielt verdrahten

**Tun.** Folge
[crm-source-wiring-capture.md](crm-source-wiring-capture.md)
mit diesem Pfad:

~~~bash
CRM="/Users/activi/Downloads/crm-master-3"
test -d "$CRM/src/crm" || { echo FAIL: crm pfad; exit 1; }
cp docs/discovery/crm-app-wiring.template.md /private/tmp/dino-crm-app-wiring.md
~~~

Nicht `find` über Vendor/TCPDF. Nur Suche:

~~~bash
cd "$CRM/src/crm"
rg -n -g '!vendor' -g '!tcpdf-main' -g '!ckeditor' -g '!node_modules' -g '!*.sql' -g '!Info/**' \
  -i 'ssdata_search|kandidati.php|search_candidates|job_occupation_map|kri_pozicija|ke_smjer'
~~~

Fülle `/private/tmp/dino-crm-app-wiring.md`: Masken, Feldkarte, RPC-Karte,
Beruf/Erfahrung, R1-Ausschluss.

**PASS.** Mindestens die Recruiter-Hauptsuche ist `BELEGT DURCH QUELLCODE`.
Drei Berufsschichten sind getrennt oder ehrlich `OFFEN`.
Keine Kontaktspalte im späteren JSON.
**FAIL.** Leere Vorlage, oder `crm_api.search_candidates` als Ziel markiert.

### Schritt 3 — Katalog und Maske zusammenführen

**Tun.** Eine Tabelle, lokal, später redigiert nach
`docs/discovery/crm-search-field-bridge.md` (erst nach Secret-/PII-Check):

| Kanonisch | UI-Label / PHP | Physisch Postgres | R1-JSON | Note |
| --- | --- | --- | --- | --- |
| Ausbildungsberuf | | | ja/nein | |
| Erfahrungsberuf | | | ja/nein | |
| Tätigkeitsart | | | ja/nein | |
| Erfahrung-Dauer | | | ja/nein; Q8.5 | |
| Ort | | | ja/nein | |
| Sprache+Niveau | | | ja/nein | |
| Skill | | | ja/nein | |
| Alter | | | ja; Pflichtfilter, keine Werte loggen | |
| Status/Verfügbarkeit | | | ja/nein | |
| Freitext | | | ja/nein; nie CV/Notiz | |

**PASS.** Jede kanonische Zeile hat Quelle oder `OFFEN`.
Konflikt Akte vs. Lebenslauf-Liste bei Erfahrung bleibt sichtbar, nicht
still gleichgesetzt (Q8.5.1).

### Schritt 4 — Discovery-Bericht abschließen

**Tun.** Was Gate B2/B3 schon geliefert hat, nicht wiederholen.
Nur Lücken schließen, die der Vertrag braucht:

- autoritative Kandidatenquelle
- ob `kandidat_id`-Spalten wirklich FK sind
- aggregierte Data-Quality nur nach eigener Freigabe (DISC-06)
- keine neuen Produktionsqueries ohne Allowlist

Paket: AUTO-01 in
[release-1-automation-tickets.md](../planning/release-1-automation-tickets.md).

**PASS.** Ein redigierter Discovery-Bericht mit Fakten / Annahmen / Coverage.
**FAIL.** „Wir haben genug gesehen“ ohne Bericht.

---

## Teil B — Vertrag (noch kein Produktivcode)

### Schritt 5 — Offene Suchregeln entscheiden

**Tun.** Mit der Brücke aus Schritt 3 die Reste in
[ADR-0002](../decisions/0002-search-design-interview.md) schließen.
Mindestens:

| Thema | Warum es den MCP blockiert |
| --- | --- |
| Q8.5 Berufserfahrung | Sonst sucht „5 Jahre Elektriker“ falsch. |
| Welche Tabelle die R1-Akte ist | Sonst doppelte Personen. |
| Ranking | R1: nur `idk_kandidati.kandidat_id` absteigend (ADR-0002). Kein zweites Kriterium. |
| Auth-Modell intern | Sonst keine Runtime-Identität. |

Nur ausdrückliche Antworten gelten. Empfehlungen bleiben Vorschlag.

**PASS.** DEC-01: die für SEARCH-01 nötigen Fragen sind `BESTÄTIGT`.
**FAIL.** MCP bauen und Q8.5 „später sehen“.

### Schritt 6 — Einen JSON/MCP/RPC-Vertrag aufschreiben

**Tun.** AUTO-02. Ein Dokument, das CI später als Schema nutzt. Inhalt:

1. Drei Tools, Namen fest:
   `search_candidates`, `get_candidate_profile`, `get_filter_options`.
2. JSON-Filter: nur Felder aus der Brücke; unbekannte Felder → Fehler.
3. Cap 50, keyset-cursor, match-evidence, keine Kontakte.
4. Fehlercodes (Alter fehlt, unbekannte Taxonomie-ID, null Treffer + Vorschläge).
5. Eine **neue** Postgres-Funktion, z. B. `crm_search.search_candidates_v1(jsonb)`.
   Alte CRM-RPCs nicht wrappen.
6. Stack-Auswahl für die Evaluation: **Option 1**
   (MCP SDK v2 + Zod + diese eine RPC), wie
   [mcp-autowire-top3-vergleich.md](../research/mcp-autowire-top3-vergleich.md).
   `supabase gen types` darf später nur `.rpc()` tippen, nie `.from()`.

**PASS.** Vertrag ist versioniert und von dir abgenommen.
**FAIL.** Tool „query“ oder generisches SQL.

---

## Teil C — Lokal nutzbar (synthetische Kandidaten)

Hier wird der Agent **zum ersten Mal bedienbar**. Noch ohne echte Personen.

### Schritt 7 — Mechanik-Eval (Form des MCP)

**Tun.** Isoliert, anderes Verzeichnis, andere Datenbank:
[option-1-mcp-sdk-rpc-setup.md](option-1-mcp-sdk-rpc-setup.md).

Prüfen:

~~~bash
node -v   # >= 20
~~~

Erwartung nach dem Runbook: ein lokaler Server, JSON rein, ≤50 Zeilen raus,
kein Kontaktfeld, kein CRM-Dump.

**PASS.** Typecheck + die Smoke-Fälle des Eval-Runbooks grün.
**FAIL.** `DATABASE_URL` zeigt auf OrbStack-MySQL, Port 54329-Demo mit
echten Namen, oder auf Produktion.

### Schritt 8 — Scaffold im genehmigten App-Repo

**Tun.** AUTO-03, erst nach AUTO-02. Eigenes App-Verzeichnis, nicht das
Dokumentationsrepo und nicht Jobstep.

Pin: Node, `@modelcontextprotocol/server` v2-Linie, Zod, `pg` oder schmaler
Supabase-Client nur für `.rpc()`, Lockfile.

Drei Tools registrieren. Handler ruft **nur** die Vertrags-RPC.

**PASS.** Tests/Typecheck des Scaffolds grün gegen synthetisches Schema.
**FAIL.** Import von v1-SDK gemischt mit v2, oder `.from('idk_kandidati')`.

### Schritt 9 — Additive Suchschicht gegen Abbild der echten Namen

**Tun.** DATA-01 nach
[database-development-automation.md](database-development-automation.md).

Lokal: synthetische Postgres 17 mit **leeren** Tabellen, deren Namen dem
Katalog entsprechen (`idk_kandidati`, `occupation`, …), plus Schema
`crm_search` mit der neuen Funktion. Importtabellen nicht umbauen.

Die Funktion:

- liest nur allowlistete Spalten
- erzwingt `LIMIT LEAST(..., 50)`
- projiziert keine Kontakt-/CV-/Notizspalten
- ist `SECURITY INVOKER`, nicht frei `PUBLIC EXECUTE`
- setzt ungenannte Filter nicht

Seeds: erfundene Testdaten, keine Dumps.

**PASS.** pgTAP + Negativtest „Kontaktspalte nicht im Result“.
**FAIL.** Funktion kopiert die alte Signatur mit Telefon.

### Schritt 10 — Taxonomie-Minimum

**Tun.** TAX-01 so weit, dass ein Recruiter „Elektriker“ über eine
kontrollierte ID findet, nicht über `ILIKE '%elektr%'`.

Quelle: `occupation` / `occupation_alias` laut Katalog, plus die Masken-
Lesart aus Schritt 2. Berufssuchprofile nur lesen, nicht in diesem MCP
schreiben (ADR-0003).

**PASS.** Mindestens ein synonymfähiger Referenzsatz BS/DE/EN.
**FAIL.** LLM erfindet Synonyme zur Laufzeit.

### Schritt 11 — Erster echter Durchstich

**Tun.** SEARCH-01 + TOOL-02/03 gegen die synthetische DB:

1. Recruiter sagt: „Elektriker, 5 Jahre.“
2. Client füllt JSON (nur Erfahrungsberuf + Dauer; Ausbildung inaktiv).
3. Zod lehnt Extrafelder ab.
4. RPC filtert in Postgres.
5. MCP gibt ≤50 Treffer + Evidence, ohne Kontakt.
6. Negativ: fremde Rolle sieht 0, nicht die Existenz.

Alter bleibt Pflichtfilter laut Q5 — im Vertrag verankern. Testdaten haben
Geburtsdatum; Output zeigt kein Datum, nur Treffer/kein Treffer.

**PASS.** Ein unabhängiger Sollwert bestätigt die Treffermenge.
SQL-Injection-String bleibt Wert, wird nicht SQL.
**FAIL.** Demo „sieht gut aus“ ohne Oracle.

### Schritt 12 — Einen Client lokal anschließen

**Tun.** Zuerst **ein** Client, nicht fünf.

| Client | Lokaler Weg |
| --- | --- |
| Codex / Claude Code | stdio-MCP aus dem Scaffold |
| ChatGPT | HTTP-MCP hinter Loopback, Dev-Bearer, kein öffentliches Internet |
| Claude Desktop | stdio, gleiche Binary |

Prompt an den Client: nur die drei Tools, JSON-Filter, bei Unklarheit
nachfragen, nie SQL, nie Kontakte verlangen.
Hilfstext:
[mcp-search-agent-prompt.md](../research/mcp-search-agent-prompt.md)

**PASS Stufe C.** Du kannst lokal in einfachen Worten suchen, und die
Antworten stammen aus der synthetischen RPC.
Das ist **noch nicht** der Vermittler-Alltag.

---

## Teil D — Produktiv nutzbar (echte Kandidaten)

Jeder Schritt braucht eine **eigene ausdrückliche Freigabe**.

### Schritt 13 — Auth und Rechte hart machen

**Tun.** AUTH-01/02.

- MCP prüft Issuer, Audience, Scope, Ablauf.
- Downstream-DB-Rolle ist eine neue **Runtime-Suchrolle**, nicht
  `dino_crm_discovery_ro_v1` und nicht `service_role`.
- Nur `EXECUTE` auf `crm_search.*` plus nötiges `SELECT` auf
  allowlistete Objekte, oder besser: nur RPC, Tabellen nicht direkt.
- RLS/Policies negativ testen.
- Parallelrequests teilen keinen User-Kontext.

**PASS.** Gestohlener/fremder Token → 401/403. Kontaktweg bleibt 403/leer.
**FAIL.** Discovery-Rolle im Runtime, oder MCP-Token = DB-URL.

### Schritt 14 — Suchregeln vollständig gegen synthetische Orakel

**Tun.** SEARCH-02: alle bestätigten Filter, BS/DE/EN, Zero-Hit + Vorschläge,
Cursor, Ranking. TOOL-02 Profil ohne Kontakt. TOOL-03 Options ohne
Kandidatendaten.

**PASS.** Die R1-Matrix in
[release-1-requirements.md](../planning/release-1-requirements.md)
für SEARCH/TOOL/FILTER ist an synthetischen Fällen grün.

### Schritt 15 — Produktions-SQL nur additiv, mit Gate

**Tun.** Nach ADR-0004:

1. Migration lokal: lint, pgTAP, Frischaufbau, Rollback.
2. CI grün.
3. Dry-run gegen ein nicht-produktives Ziel, falls vorhanden; sonst
   dokumentierter Dry-run des SQL-Textes plus Freigabe.
4. Apply auf Produktion **nur** der additiven `crm_search`-Objekte und
   Grants. Keine Änderung importierter Tabellen.

**PASS.** Apply-Bericht: welche Objekte, welcher Hash, wer freigegeben hat.
**FAIL.** Plugin-Migration, oder Wrap der alten Kontakt-RPC.

### Schritt 16 — MCP an die Runtime-Rolle hängen

**Tun.** Hosting laut AUTO-02 (noch zu wählen). Bis dahin gilt: privater
HTTP-Endpunkt, TLS, erlaubte Origins, Rate-Limit, Timeout, Body-Limit.

Downstream-Credential nur für die Runtime-Rolle. Logs ohne PII (OPS-02).

Smoke gegen Produktion, Output redigieren:

- Suche ergibt IDs ohne Telefon/E-Mail
- Profil ebenso
- Options keine Personen
- Cap 50
- unbekannte JSON-Felder 4xx

**PASS.** Schriftlicher Smoke-Report ohne Personenwerte.

### Schritt 17 — Pilot der kleinen Recruiter-Gruppe

**Tun.** Q2: kleine interne Gruppe. CLIENT-01 nach und nach, nicht alle
Clients am ersten Tag.

Alltagstest, drei Sätze:

1. „Elektriker mit fünf Jahren Berufserfahrung.“
2. Dieselbe Anfrage auf B/H/S und Deutsch.
3. Eine Anfrage mit null Treffern — Vorschläge, keine stillen Ähnlichen.

**PASS Stufe D.** Recruiter findet echte Akten, versteht warum, sieht keine
Kontakte, kann den Treffer in Jobstep anhand der ID nachschlagen.
REL-01 bleibt separat: Monitoring, Restore-Beweis, Rollback.

### Schritt 18 — Release-Haken, die nicht „Suche geht“ ersetzen

| Noch offen nach dem Pilot | Paket |
| --- | --- |
| Restore-Beweis | OPS-03 |
| Last/SLO | AUTO-06 |
| Alarme/On-call | AUTO-07 |
| Berufssuchprofil-Admin-MCP | ADMIN-01–03, ADR-0003 |
| Kontakte/Export | spätere Phase, Q4 |

Ohne REL-01 ist der MCP **pilotnutzbar**, nicht „Release 1 fertig“.

---

## Was du heute konkret als Nächstes tust

1. Schritt 1: Mapping-Fragen beantworten.
2. Schritt 2: `/private/tmp/dino-crm-app-wiring.md` aus den drei PHP-Pfaden
   füllen.
3. Nicht OrbStack öffnen, nicht Demo als Beweis nehmen, nicht MCP auf
   Produktion zeigen.

Wenn Schritt 2 steht, ist der JSON-Filter entwurfsfähig. Erst dann lohnt
Schritt 7 (lokales Eval), parallel zu Schritt 5/6, aber ohne echte Daten.

## Verwandte Dokumente

- [crm-source-wiring-capture.md](crm-source-wiring-capture.md)
- [catalog-domain-mapping.md](../discovery/catalog-domain-mapping.md)
- [option-1-mcp-sdk-rpc-setup.md](option-1-mcp-sdk-rpc-setup.md)
- [schema-discovery.md](schema-discovery.md)
- [database-development-automation.md](database-development-automation.md)
- [sdk-integration-plan.md](../planning/sdk-integration-plan.md)
- [release-1-automation-tickets.md](../planning/release-1-automation-tickets.md)
- [ADR-0001](../decisions/0001-controlled-query-boundary.md)
- [ADR-0002](../decisions/0002-search-design-interview.md)
