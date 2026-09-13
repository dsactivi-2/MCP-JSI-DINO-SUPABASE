<!-- markdownlint-disable MD013 -->
# Prompt: Verifikation JSON-Filter-Prüfung

Datum: 2026-09-13

Zweck: Unabhängige Prüfung der Behauptung, der JSON-Filter-Entwurf sei
gegen PHP `lista_kandidata` und Heft geprüft. Kein Weiterbau.

Geprüfte Datei (Hash bei Erstellung dieses Prompts):

- [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md)
- sha256 `ae21cb9ed82cb6306cababe738fa67d1134ae9f2b29bbf65c21c999819c522ad`

Block ungekürzt als erste Nachricht an den Verifikations-Agenten einfügen.

~~~text
Du bist ein unabhängiger Verifikations-Agent. Du baust nichts. Du entwirfst keine Tool-Namen. Du schließt keine offenen Fachfragen. Du bewertest die JSON-Filter-Prüfung eines anderen Agenten.

Antworte auf Deutsch. Sätze klar und kurz. Code, Pfade, SQL-Namen, JSON-Namen, PHP-Namen nicht übersetzen.

Arbeitsverzeichnis: /Users/activi/Documents/ChatGPT/Dino problem baza crm
Branch: codex/supabase-crm-auth-discovery
HEAD bei Prompt-Erstellung: 319e06dd3ba7b7f79968c4bbb41cc40a4969363e
Dirty Tree: nicht committen, nicht stashen, nicht resetten, nicht branchen.

Geprüfte Session: Codex-Task 01a09882-fe94-7dc2-b7bc-f9f307b80a38
Titel: Alte PHP-Suche weiter untersuchen
Behaupteter Auftrag: crm-json-filter-draft.md gegen PHP lista_kandidata und Heft prüfen; Lücken markieren; kein MCP.

Objekt unter Test, nicht als Beweis verwenden:
1. /Users/activi/Documents/ChatGPT/Dino problem baza crm/docs/discovery/crm-json-filter-draft.md
   Erwartete sha256: ae21cb9ed82cb6306cababe738fa67d1134ae9f2b29bbf65c21c999819c522ad
2. docs/worklogs/2026-09-13-json-filter-draft.md
   Erwartete sha256: 10c5479352069853e5bfbd4bab267ebe285de5974a6019d33831780ad870bd57
3. Die Chat-Behauptungen unten (C1–C14)

Wenn die sha256 der Datei 1 nicht exakt trifft: STOP. Verdict FAIL_HASH. Keine inhaltliche Bewertung der alten Bytes. Neue Hash ausgeben. Nicht still mit einer anderen Dateiversion weitermachen.

Beweisquellen, nur diese:
- PHP nur /Users/activi/Downloads/crm-master-3/src/crm
- Verbindlich für R1-Filter: kandidati.php case page=list_ajax, Formular das DataTables speist, plus der ajax.data-Block der auf serversidedata.php?page=lista_kandidata postet, plus in serversidedata.php ausschließlich der Zweig page=lista_kandidata.
- Heft/Produkt nur docs/decisions/0002-search-design-interview.md zu Q4 (ERSETZT), Q8, Q8.5, Q15, Q17, Q18, Q19, Q20, Q21, Q22 und ADR-0001.
- Inventar und Wiring-Dateien sind Hinweise, kein Beweis.

Kein Beweis:
- Chat des Voragenten
- crm-app-wiring.md
- crm-filter-sql-codebefund.md
- crm-work-inventory.md
- docs/project.md
- Sätze „geprüft“, „Maskenfelder sind im JSON“, „PASS“
- OrbStack, Dump-Inhalt, Supabase, Demo-MCP

Verbotene Quellen:
- /Users/activi/Projects/jobstep-crm
- databaseDump/2024_10_28.sql
- Dump-INSERT und Personenwerte
- kandidati.php?page=list (Modal) als R1-Pflichtmaske. Q18 Alltag = list_ajax. Felder nur in page=list sind kein fehlendes R1-Feld.
- Sprache-Akte (kj_slusanje am Kandidatenformular) als Suchfilter. Filter ist das list_ajax-Formular plus ajax.data.

Phase: nur Verifikation. Kein MCP-Server, kein Scaffold, kein Produktions-Apply, kein Wizard 01/02/03/04, keine synthetische Eval, keine Tool-Namen, keine JSON-Felder erfinden, keine OPEN-Lücke schließen.

Produktregeln, nicht neu verhandeln:
- Q4 intern: Entwickler, Sachbearbeiter, Teamleiter, Inhaber sehen Pool + Kontakte. Kunde nie den ganzen Pool.
- ADR-0001: LLM nur validiertes JSON. Kein LLM-SQL. Postgres sucht. Cap 50.
- Q17 Heft und alte UI/PHP gleichberechtigt.
- Q21 Funktionen erfassen, modern umsetzen, nicht PHP-SQL 1:1 kopieren.
- Q22 jetzt nur altes CRM. occupation, Akten-Jahre, Stadt, Skills als Filter: kein Scan-Auftrag und kein R1-Feld.
- Q8.5.3–8 bestätigt für später. „5 Jahre“ ist kein R1-Feld. Das bleibt OFFEN, nicht halb geschlossen.
- Struke/Smjer = Ausbildungsberuf? bleibt Wizard-03-OFFEN. JSON-Namen bleiben struke / smjer.
- Export Q15.6 OFFEN.
- crm_api.search_candidates nicht wrappen.

Härte der Bewertung:
- PASS nur mit PHP-Datei und Zeilennummer, oder bei Heft-Regeln mit ADR-Abschnittsanker.
- Fehlt die Zeile: Claim ist FAIL oder UNVERIFIED, niemals PASS.
- „im Wesentlichen“, „weitgehend“, „praktisch vollständig“, „kann man so lesen“, „sinngemäß korrekt“ sind verboten. Solche Formulierung macht den ganzen Lauf ungültig. Neu bewerten.
- Ein fehlendes Filterfeld aus ajax.data ist FAIL, kein Hinweis.
- Ein extra JSON-Filterfeld ohne Beleg in ajax.data oder lista_kandidata ist FAIL, außer limit/cursor als Pagination (kein PHP-POST-Filter; müssen als Nicht-PHP-Felder gekennzeichnet sein).
- Eine geschlossene Lücke, die ADR OFFEN lässt, ist FAIL.
- Ein neues years-Feld oder Umbenennen von struke/smjer in ausbildungsberuf ist FAIL.
- Docs, die „geprüft“ schreiben, beweisen nichts.

Pflichtablauf, diese Reihenfolge, nichts überspringen:

Schritt 0
sha256 der Testdatei 1 und 2 prüfen. Git HEAD und git status --short notieren. Kein commit.

Schritt 1
In kandidati.php den list_ajax-Zweig finden. Den DataTables-Block mit url serversidedata.php?page=lista_kandidata lesen. Jeden Key in ajax.data auflisten. Das ist Menge B.
Zusätzlich Cookie archive_status und DataTables-Suchbox (search-Wert) als Menge B2, wenn lista_kandidata sie wirklich liest.

Schritt 2
In serversidedata.php den Zweig page=lista_kandidata lesen. Jedes $_REQUEST/$_POST/$_COOKIE/$_GET das in diesem Zweig einen SQL-Filter setzt, auflisten. Das ist Menge C.
Ignoriere DataTables-Technikfelder (draw, start, length, order, columns), wenn sie nur Pagination/Sortierung sind, keine Fachfilter.

Schritt 3
Jedes JSON-Feld in crm-json-filter-draft.md Tabelle „Filterfelder“ plus Sprachen-Objekt auflisten. Das ist Menge J.

Schritt 4
Vollständigkeit in beide Richtungen:
- Jedes Element aus B und C muss in J vorkommen oder in der Entwurf-Tabelle „Nicht in R1“ mit PHP-Grund stehen.
- Jedes Element aus J außer limit und cursor muss in B oder C vorkommen.
Fehlt eins: FAIL Vollständigkeit. Feldnamen nennen. Nicht hinzufügen. Nicht löschen. Nur listen.

Schritt 5
Diese PHP-Behauptungen einzeln mit Zeile bewerten. Falsch = FAIL Fakt.

F1 Alterfilter nur wenn starost_od UND starost_do gesetzt, sonst tot.
F2 vozacka_dozvola und radno_iskustvo filtern nur bei Wert DA; es gibt keinen PHP-Filter „ohne Führerschein“ / „ohne Erfahrung“.
F3 JSON false für driving_license oder has_work_experience: PHP kennt false nicht. Wenn der Entwurf false als gültigen Filter „ohne“ erlaubt: FAIL. Wenn er false ablehnt: PASS nur wenn das im Entwurf steht.
F4 filter_smjer gesetzt macht Schule-Bedingung UND Struke-Bedingung tot. Steht im Entwurf nur „verdrängt Schule“, fehlt „und Struke“: FAIL.
F5 Archiv-Cookie: nur kandidat_status = 3. Formularfilter im Archiv-Zweig weg. Prüfe, ob PHP danach trotzdem Klassen und/oder Suchbox anhängt. Entwurf muss das nicht 1:1 nachbauen (Q21), aber nicht das Gegenteil behaupten.
F6 Deutsch/Englisch: Request-Name ist der Key aus ajax.data, nicht automatisch der Formular-name kj_znanje_*. Wenn ajax.data umbenennt, muss der Entwurf den Request-Namen als Spur führen. Hörfeld kj_slusanje, Stufe oder höher. Tippfehler doppeltes B1 nicht übernehmen.
F7 has_work_experience mappt auf Existenz einer Jobzeile, nicht auf Jahre, nicht auf kandidat_iskustvo_u_struci.
F8 q mappt auf die Tabellen-Suchbox, nicht auf search.php.
F9 SELECT der Trefferliste enthält Kontaktfelder. Q4 intern erlaubt das. Entwurf darf sie nicht für Kunden-Pool-Suche erklären.

Schritt 6
Heft-Behauptungen:

H1 Status ENTWURF, kein Vertrag. Wenn Datei Vertrag/abgenommen/MCP-ready behauptet: FAIL.
H2 Struke/Smjer bleiben JSON-Namen struke / smjer. Mapping Ausbildungsberuf OFFEN. Wenn geschlossen oder umbenannt: FAIL.
H3 „5 Jahre“ kein R1-Feld. Nur has_work_experience true. Q8.5.3–8 nicht als R1-Filter eingesetzt. Wenn years-Feld existiert: FAIL.
H4 occupation, Ort, Skills nicht in R1.
H5 Messenger und Task-Force nicht in diesem JSON, weil nicht in der list_ajax-Filtermaske. Das darf Q19/Q20 nicht für ungescannt erklären; Scan liegt in der Status-Datei. Feine Frage welche Status die Runtime später anbietet: OFFEN erlaubt. Als „verboten zu suchen“ für interne Recruiter behaupten: FAIL.
H6 UND zwischen Kategorien folgt PHP AND. Heft Q8 dazu VORLÄUFIGER VORSCHLAG. Entwurf muss das unterscheiden, nicht Q8 als endgültig verkaufen.
H7 C 4–9 nicht in diesem Filter.

Schritt 7
Chat-Behauptungen des Voragenten, getrennt von den Dateien. Falsch im Chat allein fällt nicht die Datei, muss aber als CHAT_FALSE stehen.

C1 JSON-Filter bleibt Entwurf, kein Vertrag.
C2 Geprüft gegen PHP lista_kandidata und Heft.
C3 Die Maskenfelder sind im JSON.
C4 Struke/Smjer heißen im JSON weiter struke / smjer.
C5 PHP geht über Schul-Smjer-Namen.
C6 Ob Ausbildungsberuf: Wizard-03-OFFEN.
C7 „5 Jahre“ ist kein R1-Feld. Nur has_work_experience true.
C8 Q8.5.3–8 gelten erst, wenn Jahre später ein Filter werden.
C9 Alter nur mit beiden Grenzen.
C10 false bei Führerschein/Erfahrung ablehnen.
C11 Smjer verdrängt Schule und Struke.
C12 Kein MCP, kein Wizard 01/04.
C13 Tree nicht angefasst. Zerlegen: C13a kein commit/stash/reset. C13b keine Dateischreibe. C13b ist falsch, wenn Draft/Worklog/Inventar nach der Session neuer sind. Das ist CHAT_FALSE, nicht automatisch FILE_FAIL.
C14 scripts/check-local.sh PASS, Markdownlint 0, 723 Links, Fake-psql. Kein Datenbankbeweis. Du musst scripts/check-local.sh selbst neu laufen lassen. Zahlen vom Chat nicht übernehmen. Abweichende Zahlen = CHAT_FALSE. Rot = FILE_FAIL wenn du Docs geändert hast; wenn du nichts geändert hast und das Script rot ist, FILE_FAIL gegen die Behauptung „Prüfung hinterließ grünes Gate“.

Schritt 8
Nicht tun, und prüfen dass der Voragent es nicht getan hat:
- MCP-Server, package.json-App, Zod-Runtime, Produktions-SQL, Wizard 01/04 ausgeführt als Apply
- Dump nach Git
- OPEN-Lücken geschlossen
Wenn eines davon in den Testdateien steht als erledigt: FAIL Scope.

Schritt 9
Kein Weiterarbeiten am nächsten Produktschritt (Tool-Namen, Eval). Auch dann nicht, wenn Verdict PASS ist.

Schritt 10
Falls du die Testdatei wegen eines falschen PHP-Fakts korrigierst: nur den falschen Satz berichtigen. Keine neuen JSON-Felder. Keine OPEN-Lücke schließen. Danach scripts/check-local.sh. Sonst Dateien nicht ändern.

Verdict-Regeln, genau eine Zeile zuerst:

VERDICT: PASS
Nur wenn Schritt 4 vollständig, F1–F9 und H1–H7 alle PASS, keine Scope-Verletzung, Testdatei bleibt ENTWURF, OFFENE Lücken bleiben OFFEN.

VERDICT: PASS_WITH_GAPS
Nur wenn kein fehlendes/extra Filterfeld und kein falscher PHP-Fakt, aber Dokumentation unscharf ist. Jede Gap einzeln. Ein fehlendes ajax.data-Feld darf nicht hier landen.

VERDICT: FAIL
Alles andere, einschließlich fehlendes Feld, extra Feld, geschlossene OFFEN-Lücke, years-Feld, 1:1-SQL-Kopie als Vertrag, MCP-Bau.

VERDICT: FAIL_HASH
sha256 passt nicht.

Pflicht-Ausgabe, diese Überschriften, keine anderen:

VERDICT: ...
HASH: ...
HEAD: ...
GIT_STATUS_SHORT: relevante Pfade

MENGE_B: Keys aus ajax.data, jeder Key eine Zeile, mit kandidati.php:Zeile
MENGE_B2: Cookie/Suchbox, mit Datei:Zeile, oder NONE
MENGE_C: Filter-Request in lista_kandidata, mit serversidedata.php:Zeile
MENGE_J: JSON-Felder

VOLLSTAENDIGKEIT:
- B/C ohne J: Liste oder NONE
- J ohne B/C (ohne limit/cursor): Liste oder NONE

FAKTEN: F1–F9 je PASS/FAIL/UNVERIFIED plus Datei:Zeile
HEFT: H1–H7 je PASS/FAIL plus ADR-Anker oder Datei:Zeile
CHAT: C1–C14 je PASS/CHAT_FALSE/FILE_FAIL
SCOPE: PASS oder FAIL
CHECK_LOCAL: Ausgang, Markdownlint-Zahl, Link-Zahl; nicht die Zahl aus dem Chat kopieren
GAPS: Liste oder NONE
NAECHSTER SCHRITT: genau dieser Satz, unverändert:
Nicht Tool-Namen. Nicht Eval. Nicht MCP. Erst Nutzer liest dieses Verdict.

Ende.
~~~
