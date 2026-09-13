<!-- markdownlint-disable MD013 -->
# Agent-Prompt: CRM-Kandidatensuche, Tabellen und Fehlerquellen

**Historischer Prompt.** Live-Stand: ADR-0002, nicht dieser Text.

Datum: 2026-09-12

Status: Prompt zum Kopieren an Recherche- oder Design-Agenten. Kein Dump,
keine Datensätze, keine Stack-Freigabe. Physische Namen sind Orientierung
aus Schemaexport/Katalog und bleiben `DURCH DISCOVERY ZU PRÜFEN`.

## Copy-paste Prompt

```text
Du recherchierst oder entwirfst Werkzeuge für eine Recruiter-Kandidatensuche
über MCP. Primärquellen only. Keine Datenbankverbindung. Keine Personen-
daten lesen oder zitieren. Kein beliebiger SQL. Kein Wrap der bestehenden
CRM-Funktion crm_api.search_candidates (Signatur enthält E-Mail und Telefon).

### Produkt

Interne Recruiter suchen Kandidaten in einem nach Supabase PostgreSQL 17
importierten, abgeschalteten operativen CRM. Anfragen kommen auf
Bosnisch/Kroatisch/Serbisch, Deutsch oder Englisch über ChatGPT, Claude,
Codex, Grok. Das LLM darf nur einen winzigen, validierten JSON-Filter
bauen. PostgreSQL filtert, rankt, autorisiert und paginiert. Maximal 50
Treffer pro Seite. Release 1 gibt keine Kontakte, CVs, Notizen, Verträge,
JMBG, Pass. Null exakte Treffer bleiben null, bis der Recruiter eine
Lockerung bestätigt (Q7). Nicht genannte Filterkategorien bleiben inaktiv
und schränken nicht ein.

Runtime-MCP-Tools nur:
- search_candidates(filters, sort, limit, cursor)
- get_candidate_profile(candidate_id)  // R1 ohne Kontakte
- get_filter_options(field, query)     // Katalog/Taxonomie, keine Kandidaten

Später getrennt: Profilverwaltungs-MCP für Berufssuchprofile (Entwurf,
Diff, Publish). Runtime darf Profile nur lesen, nie schreiben.

### Drei Berufsschichten — das ist der Kern der Suche

Recruiter und Kunden meinen oft „einen Elektriker“. Im Fachmodell sind
das drei getrennte Dinge. Ein Werkzeug, das sie vermischt, sucht falsch.

1. Ausbildungsberuf
   Formale Qualifikation / Lehrberuf / Schulabschlussrichtung.
   Beispiel: abgeschlossene Ausbildung Elektriker, nicht „hat mal Kabel
   gezogen“.
2. Erfahrungsberuf
   Was in der Erwerbsbiografie als ausgeübter Beruf steht.
   Beispiel: 4 Jahre als Elektriker gearbeitet, unabhängig vom Zeugnis.
3. Tätigkeitsart
   Art der tatsächlich ausgeübten Arbeit, feiner oder anders als der
   Berufsname. Beispiel: Montage, Instandhaltung, Schaltschrankbau.

BESTÄTIGT: „Elektriker mit fünf Jahren Berufserfahrung“ verlangt KEINE
Ausbildung, wenn Ausbildung nicht genannt wurde. Ungenannte Kategorien
sind tot. Direkte Berufssuche bleibt möglich. Breite Bedarfe laufen über
versionierte Berufssuchprofile (many-to-many, nicht exklusiv): ein Profil
„Tiefbauer“ bündelt mehrere Ausbildungs- und Erfahrungsberufe plus
Tätigkeiten, ohne sie zu besitzen. Derselbe Beruf bleibt einzeln suchbar
und darf in mehreren Profilen liegen.

Q8.5 ist vollständig OFFEN: zählt „5 Jahre“ die gesamte Lebensarbeitszeit
oder nur fachlich passende Intervalle? Überlappende Jobs? Fehlende Daten?
Das darfst du nicht als gelöst behandeln.

Operatoren (VORLÄUFIGER VORSCHLAG, Rekonstruktionslücke):
- verschiedene Kategorien: UND
- mehrere Berufe/Orte/Verfügbarkeiten: ANY (ODER)
- Sprachen/Skills: explizites ANY oder ALL; unklare Listen klären
- Altersspanne: beide Grenzen, Alter ist Pflichtfilter
- NOT nur wenn ausdrücklich ausgeschlossen
- fehlender Wert erfüllt keinen positiven Pflichtfilter; nichts erfinden

### Konkrete Suchanfragen und die einzige korrekte Lesart

A) „Elektriker mit fünf Jahren Berufserfahrung“
   Aktiv: Erfahrungsberuf ~ Elektriker (direkt oder über Profil), Erfahrung
   >= 5 Jahre — BERECHNUNG OFFEN.
   Inaktiv: Ausbildung, Ort, Sprache, Skills, Verfügbarkeit.
   FALSCH: automatisch Ausbildungsberuf Elektriker ANDEN; Verkäufer mit
   20 Jahren Gesamtzeit als Treffer werten, nur weil 20>=5; Freitext
   ILIKE '%elektr%' auf CV/Notizen.

B) „Elektriker, Ausbildung, 25–40, Bayern oder BW, Deutsch mind. B1,
   verfügbar in 4 Wochen“
   Aktiv: Erfahrungs- oder Ausbildungsberuf je nach Formulierung — hier
   beides, weil Ausbildung genannt ist; Alter 25–40; Ort ANY Bayern|BW;
   Sprache Deutsch Niveau >= B1; Verfügbarkeit.
   FALSCH: nur eines der Bundesländer; Deutsch als Skill statt Sprache;
   Alter aus Freitext schätzen.

C) „Tiefbauer“
   Soll ein Berufssuchprofil auflösen (viele Berufe), nicht nur den
   String Tiefbauer. Nenngt der Recruiter kein Profil, bleibt direkte
   Berufssuche möglich. FALSCH: LLM-Synonyme still erweitern
   (Bauarbeiter, Baggerfahrer), ohne genehmigte Taxonomie/Profilversion.

D) „Mechaniker / mehaničar / mechanic“
   Dieselbe kanonische ID nur nach genehmigtem Alias. FALSCH: drei
   getrennte Suchen oder ungeprüfte Embeddings als Standard.

E) Null Treffer
   Exakte Filter unverändert lassen. Lockerungen vorschlagen
   (z.B. Erfahrung 5→3, Ort auf Nachbarland). Neue Suche erst nach
   Zustimmung. FALSCH: still semantisch ähnliche Leute nachschieben.

F) „Zeig mir Telefon und CV von Treffer 12“
   Release 1: ablehnen. Kontakt und CV sind andere Phase.

### Tabellen — Charakter, nicht jede Spalte

Daten: Dump eines toten operativen CRM, nicht suchoptimiert. Kurzfristig
additive Schicht über Importtabellen (Option A), später kleine Schnitte
zum kanonischen Modell. Importtabellen in Phase A nicht umbauen/löschen.

Volumen (Schätzungen, keine Zählung):
- Projekt ~200.000 Kandidaten; Nutzer 179 Tabellen.
- Statischer Schema-Visualizer-Export crm: 100 volle Tabellen, 1104
  Spalten, jede mit PK. Keine bewiesenen FKs, Unique, Indizes, Views, RPC.
- 88 weitere Namen nur als RLS-Policy, ohne Spaltenblock.
- crm_api-Export: 0 Tabellen (beweist nicht fehlende Views/RPC).
- crm_auth: 6 Tabellen (user_employee_map, roles, permissions,
  role_permissions, user_roles, user_scopes).
- Katalog Gate B2 V3, nur Namen/reltuples: idk_kandidati ~122004;
  occupation ~702; occupation_alias ~1241; job_occupation_map ~87844.
  RPCs search_candidates_by_occupation, search_candidates_filtered,
  crm_api.search_candidates (E-Mail+Telefon in der Signatur).
  candidate_document_embeddings vector(1536), fast leer. Trigram-Indizes
  auf Freitext existieren dem Namen nach.

Fachliche Schichten (Gruppierung = ARBEITSANNAHME):

Kandidat-Stamm
- idk_kandidati: zentrale Person. PK kandidat_id. Enthält u.a. Name,
  kandidat_datumrodjenja (Alter), kandidat_grad / kandidat_drzava
  (Wohnort-Freitext/Felder, keine Ortstabelle im vollen Export),
  zeljena_regija / zeljeni_grad, struka_sa_prijave (int, unklar ob
  Ausbildungs-ID), kandidat_nivo_obrazovanja, kandidat_iskustvo_u_struci
  und kandidat_iskustvo_u_struci_trajanje (grobe Erfahrungsfelder, keine
  Q8.5-Definition), Status, Partner. PLUS PII: JMBG, Pass, Adresse,
  E-Mail, Mobil, Passwort. R1-Output darf das nicht sehen.
- Legacy/alternativ: idk_dak_kandidati, idk_nd_kandidata,
  idk_nd_kandidati_ciscenje. Welche Quelle autoritativ ist: OFFEN.
  Ein Auto-MCP, der alle drei sucht, verdoppelt Personen.

Ausbildung (Freitext + optionale IDs, kein bewiesener FK)
- idk_kandidat_edukacija: ke_kandidat_id; Intervalle ke_datumod/do,
  ke_aktuelno; ke_naziv_kvalifikacije + _de (Pflicht-Freitext);
  ke_naziv / ke_naziv_de (Schule Freitext); ke_smjer_id, ke_skola_id
  (nur Namens-IDs, kein FK-Beweis); ke_vrsta_obrazovanja Freitext-Typ;
  ke_opis Freitext. Mehrere Zeilen pro Kandidat.
- idk_kandidat_akademija: Kampagnen-/Kursstatus, nicht Lehrberufskatalog.
- idk_skole, idk_skole_smjerovi, idk_struke: im statischen Export nur
  Policy-Namen, ohne Spalten. Können Lookups sein, sind aber nicht
  analysierbar gewesen.

Berufserfahrung (fast nur Freitext)
- idk_kandidat_radno_iskustvo: kri_kandidat_id; kri_darum_od (Tippfehler
  im Export) / kri_datum_do / kri_aktuelno; kri_pozicija Pflicht-Freitext
  plus _de/_en; kri_naziv Arbeitgeber-Freitext; Ort Freitext; kri_opis
  Freitext; kri_telefon/kri_email am Arbeitgeber — R1 nicht ausgeben.
  KEINE occupation-ID-Spalte im Export. Ein „Elektriker“-Filter kann
  hier nicht deterministisch über FK treffen, nur über spätere
  Normalisierung auf Taxonomie-IDs.
- idk_kandidati.kandidat_iskustvo_u_struci(_trajanje): parallele,
  unbestätigte Skalarfelder. Konflikt mit der Intervalltabelle ist
  wahrscheinlich.

Tätigkeit / Katalog
- idk_kandidat_pozicija: kp_ime + _de/_en/_rs, kp_active, kp_source.
  KEIN kandidat_id. Das ist ein Katalog, keine 1:n-Zuordnung. Wie er an
  Erfahrung hängt: OFFEN.
- occupation, occupation_alias, job_occupation_map: im Visualizer nur
  Policy, im Gate-B2-Katalog als Objekte mit großen Map-Zahlen. Das ist
  der belegte Kern für kontrollierte Berufssuche — aber nicht der
  öffentliche MCP-Vertrag und nicht bewiesen als Quelle von Ausbildung
  vs. Erfahrung.
- idk_profil_kriterij, idk_nalog_profil: kein Beweis für Berufssuchprofil
  mit draft/publish/Version.

Sprache, Skill, Status
- idk_kandidat_jezici: Sprachname Freitext + CEFR-ähnliche Teilskills
  als varchar, zweisprachig. Kein ISO-Code im Export.
- idk_candidate_verified_languages / logs: Verifikation/Kurse, nicht
  der einzige Sprachfilter.
- idk_kandidat_vjestine: Skill-Freitext + Gruppe int, pro Kandidat.
- idk_kandidat_status, idk_kandidat_status_prijave, Logs: operative
  Pipeline, nicht gleich „verfügbar in 4 Wochen“.

Ort
- Keine volle Location-Tabelle im Export. idk_pp_city / idk_pp_regions
  nur Policy-Namen. Wohnort und Wunschort liegen als Felder/Freitext am
  Kandidaten und an Erfahrung/Ausbildung. „Bayern“ ist deshalb kein
  sauberer FK-Filter, bis Discovery das löst.

Auth
- crm_auth mappt UUID-User auf employee_id, Rollen, Permissions, Scopes.
  Policies auf authenticated sind angezeigt, RLS enable/force unbewiesen.
  Kein tenant_id-Feld im Export.

Nicht suchen, nicht exponieren
- Kontakte, CV (idk_kandidat_cv), Dokumente, Verträge, Finanzen,
  Tickets, Partner-Notifications, API-Tokens (idk_api_clients.client_token),
  Passwortspalten, Notizen. Auto-MCP der „alle Tabellen“ published ist
  ein Fehlschlag, keine Hilfe.

### Schwierigkeiten und typische Fehler (genau hier scheitern Werkzeuge)

1. Ausbildung ≠ Erfahrung ≠ Tätigkeit
   Naive Suche „Elektriker“ AND-verknüpft Schule und Jobs. Fachlich falsch
   (Q8 bestätigt das Gegenteil). Ein Generator der eine Spalte „Beruf“
   erfindet, liegt falsch: es gibt mehrere Oberflächen.

2. Freitext ohne kontrollierte ID
   Erfahrung und oft Ausbildung sind mehrsprachige Strings:
   Elektriker / električar / electrician / Elektroniker / „el.instalater“
   / Tippfehler. 37 Spalten in 14 Tabellen haben Sprach-Suffixe _de _en
   _rs _it _ba. ILIKE oder LLM-Synonyme ohne Taxonomie treffen zu viel
   oder zu wenig. Trigram-Indizes existieren — das ist ein späterer
   Baseline-Backend, kein Freibrief für SQL vom Modell.

3. job_occupation_map ist groß, die 1:n-Erfahrung hat keine Map-Spalte
   ~87k Map-Zeilen legen nahe, dass irgendwo Jobs auf Occupations zeigen.
   Der sichtbare Erfahrungsblock tut das nicht. Wer nur occupation sucht,
   kann 0 Treffer gegen echte Elektriker-Freitexte liefern — oder die
   Map falsch als Ausbildung lesen.

4. Mehrere Zeilen, überlappende Intervalle, offenes Ende
   Ein Kandidat hat n Ausbildungs- und m Erfahrungszeilen. kri_aktuelno
   ohne kri_datum_do. Q8.5 offen: Summe? Union der Monate? Nur Zeilen
   deren Freitext nach Normalisierung zum gesuchten Beruf gehört?
   Verkauf 8 Jahre + Elektrik 2 Jahre darf nicht 10 Jahre Elektrik sein.
   Das ist der häufigste stille Fehler.

5. Skalar vs. Historie
   kandidat_iskustvo_u_struci_trajanje kann 5 sagen, die Intervalltabelle
   2. Welche Zahl gilt, ist ungeprüft. Ein Tool das nur die Stammtabelle
   liest, ignoriert die Biografie.

6. Sprache der Anfrage ≠ Sprache der Daten
   Recruiter sagt Deutsch, Daten stehen auf B/H/S plus _de-Spalte die
   null sein kann. Ohne Alias-Tabelle (occupation_alias ~1241) oder
   genehmigte Synonyme ist Matching Glücksache. Embeddings
   (candidate_document_embeddings) sind fast leer und nicht R1-Standard.

7. Ort ist kein Katalog
   „Bayern oder Baden-Württemberg“ braucht Geographie oder kontrollierte
   Regionen. Im vollen Export gibt es das nicht. Freitext grad/drzava
   auf Kandidat und Job dupliziert und driftet (München / Munchen /
   BIH / Bosna).

8. Verfügbarkeit ≠ Statuscode
   Operative Status (Bewerbung, Visa, Termin) sind nicht dasselbe wie
   „kann in 4 Wochen anfangen“. Es gibt Wunsch-/Vertrags-/Projektions-
   daten (idk_kandidat_projekcije.proracunati_pocetak_rada). Ohne Regel
   rät das Modell.

9. Alter
   Pflichtfilter über Geburtsdatum. Rechtliche Ausgestaltung OFFEN.
   Gespeichertes „Alter“ als int wäre falsch (veraltet). Fehlendes
   Datum: kein positiver Treffer, nichts erfinden.

10. Alte Search-RPCs
    crm_api.search_candidates listet Kontaktfelder. search_candidates_*
    existieren. Auto-MCP/OpenAPI wrappt sie 1:1 und verletzt Q4. Auch
    „read-only SQL MCP“ liest dieselben Spalten, sobald SELECT * oder
    die Funktion genutzt wird.

11. Doppelte Personenquellen
    idk_kandidati vs nd_/dak_-Sätze. Ohne autoritative Abbildung entstehen
    Duplikate oder blinde Flecken.

12. Profil ≠ nalog_profil
    idk_nalog_profil hängt an nalog_id (Auftrag), nicht an published
    Berufssuchprofil-Versionen. Wer das als Taxonomie nimmt, sucht
    Aufträge statt Berufe.

13. Bestätigung und Ein-Suche
    Q7 ist hart. Allgemeine Preview-Pflicht ist nur Vorschlag. Ein Tool
    das bei 0 Hits selbst Embeddings nachlädt, ist falsch.

### Was ein passendes Werkzeug können muss

Nützlich: TypeScript-Typen oder parametrisierte RPC/SQL-Allowlist für
genau drei Tools; JSON/Zod-Filter; später FTS/pg_trgm hinter demselben
JSON. Unbrauchbar als Runtime: query(sql), PostgREST-CRUD, Developer-MCP
auf Produktion, NL→SQL, Typesense-NL die Filter still erweitert,
Hasura/Directus über alle Collections.

Bewerte Kandidaten so: welche der drei Berufsschichten treffen sie
deterministisch? Was bleibt Freitext-Glück? Erzwingen sie Ausbildung bei
„n Jahren“? Können sie ungenannte Kategorien tot lassen? Cap 50 und
Kontaktfreiheit? Primärquellen-URL + Datum. Urteil GO-runtime /
GO-codegen-only / LATER / NO-GO.

Schreib einen zitierten Bericht. Wenn nichts ein sicherer Runtime-MCP
ist, sag das klar.
```

## Hinweise für Menschen im Repo

Der Prompt oben ist absichtlich vollständig. Tabellen- und Katalogzahlen
kommen aus
[statischer crm-Analyse](../discovery/crm-schema-static-analysis.md),
[crm_auth](../discovery/crm-auth-schema-static-analysis.md) und dem
Kataloghinweis in [ADR-0002](../decisions/0002-search-design-interview.md)
(Q8, Q8.4, Q8.5, Q14). Sie ersetzen Gate B nicht.

Verwandt: [auto-wire-Brief](mcp-autowire-research-brief.md),
[Top-3-Vergleich](mcp-autowire-top3-vergleich.md),
[CONTEXT.md](../../CONTEXT.md).
