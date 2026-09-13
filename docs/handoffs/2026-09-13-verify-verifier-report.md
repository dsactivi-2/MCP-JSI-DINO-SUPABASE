<!-- markdownlint-disable MD013 -->
# Prompt: Verifikation des Verifikationsberichts

Datum: 2026-09-13

**Historischer Pflichtablauf. Ausgeführt 2026-09-13. Live: ADR-0002.**

Zweck: PASS-Bericht unabhängig prüfen. Pflicht: die zwei Chat-Punkte
und alles, was der Vorbericht nicht sauber bewiesen hat. Nur echte
Fehler in Docs korrigieren. Kein Weiterbau.

Block ungekürzt als erste Nachricht einfügen.

~~~text
Du prüfst einen Verifikationsbericht. Du übernimmst kein PASS. Du baust kein MCP. Du schließt keine OPEN-Lücken. Du erfindest keine JSON-Felder.

Antworte auf Deutsch. Sätze klar und kurz. Code, Pfade, SQL-Namen, JSON-Namen, PHP-Namen nicht übersetzen.

Arbeitsverzeichnis: /Users/activi/Documents/ChatGPT/Dino problem baza crm
Branch: codex/supabase-crm-auth-discovery
Erwartete HEAD: e288d3daee9a040bd216aa780414096c5e83ac2c
Dirty Tree: nicht committen, nicht stashen, nicht resetten, nicht branchen, nicht pushen.

Objekt unter Test: der Bericht mit VERDICT PASS zur Datei
docs/discovery/crm-json-filter-draft.md
sha256 bei Bericht: ae21cb9ed82cb6306cababe738fa67d1134ae9f2b29bbf65c21c999819c522ad
Worklog sha256: 10c5479352069853e5bfbd4bab267ebe285de5974a6019d33831780ad870bd57

Der Vorbericht hat Filter-Fakten mit PHP-Zeilen belegt. Er hat zwei Chat-Punkte nur als CHAT_FALSE markiert, ohne dass du das nochmal nachweist. Die Archiv-Unterscheidung Liste-SQL gegen Zähl-SQL hat er nicht getrennt. Das musst du jetzt beweisen. Keine erwartete Antwort aus diesem Prompt übernehmen.

Beweisquellen, nur diese:
- PHP nur /Users/activi/Downloads/crm-master-3/src/crm
- R1-Filter nur kandidati.php list_ajax → ajax.data auf serversidedata.php?page=lista_kandidata und in serversidedata.php ausschließlich case "lista_kandidata" (beginnt nahe Dateianfang). case "lista_kandidata_dn" ist nicht R1, außer du beweist dass list_ajax ihn aufruft.
- Heft: docs/decisions/0002-search-design-interview.md Q4 ERSETZT, Q8, Q8.5, Q17–Q22; ADR-0001.
- Testdatei crm-json-filter-draft.md, Worklog, git log/status, scripts/check-local.sh.

Kein Beweis: der PASS-Bericht selbst, crm-app-wiring.md, crm-filter-sql-codebefund.md, Inventar, Chat, OrbStack, Dump, Supabase.
Verboten: /Users/activi/Projects/jobstep-crm, 2024_10_28.sql, Dump-INSERT, Personenwerte, page=list-Modal als R1-Pflichtmaske.

Produktregeln, nicht verhandeln:
- Q4 intern sieht Pool + Kontakte. Kunde nie den ganzen Pool.
- ADR-0001: LLM nur JSON. Kein LLM-SQL. Cap 50.
- Q21 nicht PHP-SQL 1:1 kopieren.
- Q22 occupation / Akten-Jahre / Stadt / Skills jetzt kein Scan und kein R1-Feld.
- Struke/Smjer-Deutung OFFEN. JSON-Namen bleiben struke / smjer.
- „5 Jahre“ kein R1-Feld. Q8.5.3–8 nicht als R1-Filter.
- Export Q15.6 OFFEN. Kein crm_api.search_candidates wrappen.

Härte:
- Jede Aussage nur mit Datei:Zeile oder git-Befehl plus Ausgabe.
- Fehlt der Beleg: UNVERIFIED, nie PASS.
- „im Wesentlichen“, „weitgehend“, „praktisch vollständig“, „kann man so lesen“ sind verboten. Dann ganzen Lauf ungültig.
- CHAT_FALSE aus dem Vorbericht ist kein Beweis. Du musst C13b und C14 selbst belegen.
- OPEN-Lücke schließen = FAIL Scope.
- years-Feld oder struke→ausbildungsberuf = FAIL Scope.
- Tool-Namen, Eval, MCP, Wizard 01/04 Apply = FAIL Scope.

Teil A — Pflichtnachweis, vorher nicht oder nicht sauber bewiesen. Darf nicht übersprungen werden.

A1 C13b. Chat sagte „Tree nicht angefasst“. Beweise mit git: git status --short, git log -1 --stat, welche Dateien Commit e288d3d hinzugefügt oder geändert hat. War der Chat wahr oder falsch? Wenn nur Chat falsch und die Testdatei das nicht behauptet: PROVEN_CHAT_FALSE, Datei nicht umschreiben. Wenn eine committed Datei heute „keine Dateischreibe“ behauptet: CONFIRMED, Satz streichen oder korrigieren.

A2 C14. Alter Chat: check-local Markdownlint 0, 723 Links. Vorbericht: Ausgang 0, Markdownlint 0, Links 726. Du musst bash scripts/check-local.sh selbst neu laufen. Zahlen nicht kopieren. Trage Ausgang, Markdownlint-Zahl, Link-Zahl ein. Vergleich: 723, 726, deine Zahl. Welche Angabe ist falsch? PROVEN mit Script-Ausgabe. Rot = FILE_FAIL. Nur abweichende historische Zahl = PROVEN_CHAT_FALSE, Testdatei nicht dafür ändern.

A3 Archiv in case lista_kandidata. Beweise getrennt, mit Zeilen:
1. Cookie-Zweig: Formularfilter weg, nur kandidat_status = 3?
2. Führerschein-Klassen: $sql ja/nein, $count_sql ja/nein.
3. search[value]: $sql ja/nein, $count_sql ja/nein.
Wenn Testdatei oder Vorbericht Suchbox und Klassen für Zähl- und Listensql gleichsetzen, PHP aber unterscheidet: CONFIRMED. Fix: ein Satz in crm-json-filter-draft.md. Kein SQL kopieren. R1 übernimmt den PHP-Zählfehler nicht als Vertrag (Q21).

A4 Vorbericht GAPS: NONE. Haltbar nur wenn A3 keinen Unterschied findet, den Entwurf oder Bericht verwischt. Sonst CONFIRMED: GAPS NONE war falsch. Fix nur wenn die Testdatei den Unterschied verschweigt oder falsch gleichsetzt.

A5 lista_kandidata_dn. Beweise ob list_ajax ihn aufruft. Nein: PROVEN_NOT_R1, nicht nach R1 ziehen. Ja: CONFIRMED Vollständigkeit.

A6 INNER JOIN Gruppe/Status. Beweise PHP-Join. Testdatei muss OFFEN oder PHP-Fakt ohne R1-Pflicht sein. Als entschieden oder heimlich übernommen: CONFIRMED, zurück auf OFFEN.

Teil B — Filterfakten des Vorberichts, trotzdem an PHP halten, nicht den Bericht zitieren.

B1 Hash Testdatei. Weicht sha256 ab und du hast die Datei nicht selbst geändert: STOP FAIL_HASH.
B2 HEAD notieren. Kein Reset.
B3 Menge B aus ajax.data, Menge C aus case lista_kandidata, Menge J aus Testdatei. B/C ohne J oder J ohne B/C (ohne limit/cursor) = CONFIRMED. Fix: Feld in die Tabelle oder nach „Nicht in R1“ mit PHP-Grund. Kein neues Fachfeld.
B4 Alter nur wenn starost_od UND starost_do gesetzt.
B5 Smjer tot für Schule UND Struke (filter_smjerExp).
B6 Request-Name ajax.data znanje_njemacki / znanje_engleski, nicht Formular kj_znanje_*. Hörfeld kj_slusanje Stufe oder höher.
B7 has_work_experience = Jobzeile in idk_kandidat_radno_iskustvo, keine Jahre.
B8 struke/smjer nicht umbenannt, kein years-Feld, OFFEN bleibt OFFEN.
B9 ADR-Anker im Vorbericht (Q4 :85-94, Q8 :148, Q8.5.3–8 :236-259, Q18 :911-929, Q19 :952-953, Q20 :978-1006, Q22 :1064-1075): zeigt der Anker denselben Inhalt? Falsche Zeile, richtiger Inhalt = Berichtfehler ohne Dateifix. Anderer Inhalt = CONFIRMED; Testdatei nur bei gleichem Fehler ändern.
B10 Vorbericht-PASS nur haltbar wenn A3/A4 und B3–B8 wahr sind.

Fix-Regeln, nur nach CONFIRMED an der Testdatei:
- Nur crm-json-filter-draft.md und bei Bedarf docs/worklogs/2026-09-13-json-filter-draft.md.
- Nur den falschen Satz.
- Keine neuen JSON-Felder außer B3-Pflicht aus ajax.data.
- Keine OPEN-Lücke schließen.
- Kein Commit, kein Push.
- Danach bash scripts/check-local.sh.
- PROVEN_CHAT_FALSE, PROVEN_NOT_R1, DISMISSED: Datei nicht anfassen.

Nicht tun: Tool-Namen, Eval, MCP, Scaffold, Wizard Apply, Dump lesen, Inventar „fertig für Eval“ vorschreiben.

Ausgabe, erste Zeile Verdict:

VERDICT: PASS
Teil A und B wahr. Kein CONFIRMED an der Testdatei. Chat-Punkte dürfen PROVEN_CHAT_FALSE sein.

VERDICT: PASS_WITH_FIXES
Mindestens ein CONFIRMED, alle in der Testdatei korrigiert, check-local grün, OPEN bleibt OPEN.

VERDICT: FAIL
A1–A6 oder B3–B8 ohne eigenen Beleg, oder CONFIRMED ohne Fix, oder Scope, oder weiche Worte.

VERDICT: FAIL_HASH
Testdatei-Hash unerwartet und nicht durch deinen Fix in diesem Lauf.

HASH:
HEAD:
GIT_STATUS_SHORT:
A1–A6: je PROVEN / PROVEN_CHAT_FALSE / PROVEN_NOT_R1 / CONFIRMED / CONFIRMED_FIXED plus Beleg
B1–B10: je PASS / CONFIRMED / CONFIRMED_FIXED / FAIL plus Datei:Zeile
FIXES: geänderte Sätze oder NONE
CHECK_LOCAL: Ausgang und Zahlen, neu gelaufen, nicht kopiert
NAECHSTER SCHRITT: genau:
Nicht Tool-Namen. Nicht Eval. Nicht MCP. Erst Nutzer liest dieses Verdict.

Ende.
~~~
