# Freigegebene Korrekturen der Entscheidungsrekonstruktion

Datum: 2026-09-11

Umfang: Dokumentkorrekturen im vorhandenen Arbeitsstand; keine Implementierung,
Datenbankzugriffe, externen Änderungen, Tickets, produktiven Aktionen oder Commits.

Der [Auditbericht](decision-reconstruction-audit.md) bleibt unverändert als
historischer Befund des Stands vor diesen Korrekturen erhalten. Sein `FAIL`
bezeichnet diesen früheren Stand, nicht das Ergebnis einer erneuten Vollprüfung
nach den Korrekturen. Dieser Bericht dokumentiert die freigegebene Nacharbeit.

## Freigabe und Evidenz

Die ausdrückliche Nutzerfreigabe im Anschluss an den Audit legt folgende Grenzen
fest. Verweise auf „Freigabe Nr.“ in der Matrix beziehen sich auf diese Liste.
Die Freigabe von Dokumentkorrekturen ist keine Zustimmung zu offenen Designs.

1. Nur durch Audit und vorhandene Entscheidungsevidenz gedeckte Korrekturen.
2. Unbelegte Details als OFFEN, VORLÄUFIGER VORSCHLAG, ARBEITSANNAHME oder
   DURCH DISCOVERY ZU PRÜFEN kennzeichnen.
3. Q8.5 vollständig OFFEN; frühere Fachregeln höchstens als Vorschläge erhalten.
4. Grundsätzliche Zustimmung zu Q8.4 und Berufssuchprofilen erhalten;
   unbelegte Details als Rekonstruktionslücke kennzeichnen.
5. Release 1 vollständig ohne Kontaktausgabe; Kontaktfreigabe und CONTACT-02 später.
6. Nutzer übernimmt derzeit alle Q3-Rollen; RACI, On-call und Prüfprozesse offen.
7. Allgemeine Bestätigung jeder neuen/geänderten Suche nur vorgeschlagener Ablauf.
8. JSON-Vertrag unvollständiger Entwurf; keine Operatoren eigenständig ergänzen.
9. Ungeprüfte Datenbank-, Tabellen-, Feld-, ID- und Bestandsaussagen kennzeichnen.
10. Forschung erhalten; historische, vertagte und durch ADR-0003 überholte
    Empfehlungen ausdrücklich abgrenzen.
11. Globale Q8-Optionen A/B als abgelehnt festhalten, Definitionen nicht erfinden.
12. Q4.5 offen lassen, keinen Fragetext erfinden.
13. Keine Datenbankzugriffe, Implementierung, externen Änderungen, Tickets oder
    produktiven Aktionen; nichts committen.

Die ursprüngliche Entscheidungsevidenz steht im
[Audit-Auftrag](decision-reconstruction-audit-prompt.md). Die Befundnummern F1
bis F9 verweisen auf den Auditbericht. Akzeptierte Architekturgrenzen bleiben
wirksam; ihre Geltung ersetzt keinen Nachweis der historischen Einzelzustimmung.

## Genaue Änderungsmatrix

Vergleichsbasis ist ein vor dieser Korrekturrunde erfasster Snapshot einschließlich
aller bereits vorhandenen unversionierten Dokumente. Dadurch beschreibt die
Matrix diese Korrekturrunde und nicht pauschal alle Änderungen gegenüber Git HEAD.
Vorherige und neue Aussagen sind präzise Zusammenfassungen, keine vollständigen
Textzitate. Rein sprachliche Nachkorrekturen sind separat ausgewiesen.

### docs/decisions/0002-search-design-interview.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Statusbegriffe | Nur Interviewstatus definiert. | Zusätzliche Evidenz- und Vorschlagsstatus definiert. | Freigabe Nr. 2 | Keine neue Entscheidung erforderlich. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Bestätigte Fragen und Antworten | Überschrift suggeriert ausschließlich bestätigte Antworten. | Gemischte Status und aktuelle Korrekturfreigabe ausdrücklich dokumentiert. | Freigabe Nr. 1–4, 7 | Keine neue Entscheidung erforderlich. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q3 – Verantwortliche Rollen | Alle Rollen übernommen, organisatorische Details nicht getrennt. | Derzeitige Rollenübernahme bestätigt; RACI, On-call und Prüfprozesse offen. | Q3; Freigabe Nr. 6 | RACI, On-call-Ablauf und konkrete Prüfprozesse. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q4 – Kontaktdaten im ersten Release | Nein zu Kontakten. | Vollständiger Ausschluss in Release 1; Kontaktfreigabe und CONTACT-02 später. | Q4; Freigabe Nr. 5 | Spätere Kontaktphase separat freigeben. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q8 – Grundrichtung der Filterverknüpfung | Detaillierte C-Regeln, Suchbestätigung und CRM-Auswahl als bestätigt. | A/B abgelehnt; Detailregeln und allgemeine Suchbestätigung Vorschlag; ungenannte Filter bestätigt; Bestandsaussagen Annahme. | Audit F2, F7, F9; Freigabe Nr. 2, 4, 7, 9, 11 | Historische Empfehlungsliste, Operatoren, Bestätigungsablauf, Pflicht-/Wunschkriterien und CRM-Bestand. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q8.4 – Berufssuchprofile für breite Anforderungen | Grundprinzip und alle Normalisierungs-/Vorschaudetails als bestätigt. | Grundprinzip bestätigt; geltenden ADR von historischer Zustimmung getrennt; Normalisierung vorläufig, IDs ungeprüft. | Audit F2, F7; Freigabe Nr. 4, 7, 9 | Originalempfehlungen, Normalisierungsverfahren, Bestand und Q8.5. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q8.5 – Bedeutung von Berufserfahrung | Q8.5 teilweise bestätigt; relevante Erfahrung und Freitextbestand festgelegt. | Q8.5 vollständig offen; Fachregeln nur Vorschlag, Freitextbestand Annahme. | Audit F1; Freigabe Nr. 3, 9 | Gesamte Relevanz- und Zeitberechnungsentscheidung Q8.5. |
| [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) › Q8 – Noch offene Unterfragen | Nur Detailfragen der Relevanz offen. | Auch Grundfrage Q8.5 ausdrücklich in der Frontier offen. | Freigabe Nr. 3 | Q8.5 vollständig. |

### CONTEXT.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [CONTEXT.md](../../CONTEXT.md) › Rječnik – Ausbildungsberuf | Vorhandene kontrollierte CRM-Liste. | Domänenbegriff von ungeprüfter CRM-Abbildung getrennt. | Audit F7; Freigabe Nr. 9 | Existenz und Struktur der CRM-Liste. |
| [CONTEXT.md](../../CONTEXT.md) › Rječnik – Relevante Berufserfahrung | Ausschließlich fachlich passende Zeiten verbindlich definiert. | Begriff ausdrücklich vorläufig; Q8.5 vollständig offen. | Audit F1; Freigabe Nr. 3 | Q8.5. |
| [CONTEXT.md](../../CONTEXT.md) › Dokumenteinleitung | koristeći B/H/S, njemački ili engleski. | koristeći B/H/S, njemački ili engleski. Obim je projektna procjena (DURCH DISCOVERY ZU PRÜFEN), ne potvrđen broj zapisa. | Audit F7; Freigabe Nr. 9: Schätzung von geprüftem Bestand trennen. | Tatsächlicher Umfang nach Discovery. |

### docs/project.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/project.md](../project.md) › Dokumentkopf | Alter Aktualisierungsstand. | Datum der Korrektur. | Dokumentkorrektur | Keine neue Entscheidung erforderlich. |
| [docs/project.md](../project.md) › Trenutno stanje | Filterdetails und allgemeine Bestätigung bestätigt; offene IDs nicht genannt. | Profilgrundsatz bestätigt, Details Vorschlag, Q8.5/Q4.5 offen, Release 1 kontaktfrei. | Audit F1–F3, F9; Freigabe Nr. 3–5, 7, 12 | Q8-Details, Q8.5 und Q4.5. |
| [docs/project.md](../project.md) › Trenutno stanje – Rollen | Rollen übernommen. | Derzeit übernommen; organisatorische Details offen. | Q3; Freigabe Nr. 6 | RACI, On-call, Prüfprozesse. |
| [docs/project.md](../project.md) › Put do implementacije | Discovery-Verweis ohne explizite Interviewreihenfolge. | Q9-Ablauf und ungeprüfte Nutzerangabe 179 sichtbar. | Q9; Audit F9 | Auditvoraussetzungen und Inventar. |
| [docs/project.md](../project.md) › Svrha | zapisa kandidata na B/H/S, njemačkom i engleskom. | zapisa kandidata na B/H/S, njemačkom i engleskom. Obim je projektna procjena, DURCH DISCOVERY ZU PRÜFEN. | Audit F7; Freigabe Nr. 9: Schätzung von geprüftem Bestand trennen. | Tatsächlicher Umfang nach Discovery. |

### AGENTS.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [AGENTS.md](../../AGENTS.md) › Architecture boundaries | Allgemeine Ausnahme für separat autorisierte Kontakte. | Release 1 auf allen Pfaden kontaktfrei; spätere Phase separat. | Q4; Audit F3; Freigabe Nr. 5 | Spätere Kontaktfreigabe. |
| [AGENTS.md](../../AGENTS.md) › Design interview persistence | Generische Statusregeln. | Aktuelle explizite Grenzen Q8.4/Q8.5, Vorschau und Bestandsaussagen. | Freigabe Nr. 2–4, 7, 9 | Fehlende Primärevidenz und Discovery. |
| [AGENTS.md](../../AGENTS.md) › Mission | Build a secure MCP layer for searching approximately 200,000 CRM candidate records through controlled, multilingual queries. | Build a secure MCP layer for searching approximately 200,000 CRM candidate records through controlled, multilingual queries. This volume is a project estimate, DURCH DISCOVERY ZU PRÜFEN, not an audited record count. | Audit F7; Freigabe Nr. 9: Schätzung von geprüftem Bestand trennen. | Tatsächlicher Umfang nach Discovery. |

### docs/decisions/0003-separated-profile-administration-mcp.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) › Kontext | Runtime führt ausschließlich bestätigte Filter aus. | Validierte Filter; allgemeine Suchbestätigung Vorschlag, Q7 bleibt verbindlich. | Audit F2, F5; Freigabe Nr. 7 | Allgemeiner Suchbestätigungsablauf. |
| [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) › Kontext – Evidenz | Nur Verweis auf rekonstruierte Quellen. | Geltender ADR von fehlender historischer Einzelzustimmung getrennt. | Audit F2; Freigabe Nr. 1, 2, 7 | Historische Detailprovenienz. |
| [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) › Nicht exklusive Profilmitgliedschaft | Kategorie erfordert Nennung und allgemeine Vorschau-Bestätigung. | Unbenannte Kategorien inaktiv; generelle Bestätigung vorläufig. | Freigabe Nr. 7 | Suchbestätigungsablauf. |
| [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) › Grenze zum Runtime-Such-MCP | Speicherung für Verlauf und Export unbedingt formuliert. | Versionsbindung bedingt auf spätere Funktionsfreigabe. | Audit: offene Fragen; Freigabe Nr. 1 | Verlauf- und Exportumfang. |
| [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) › Grenze zum Runtime-Such-MCP – Vorschau | Versionstreue und allgemeine Suchbestätigung nicht getrennt. | Versionsgarantie erhalten, allgemeine Bestätigung ausdrücklich vorläufig. | Freigabe Nr. 7; akzeptierter ADR-0003 | Bestätigung jeder Suche. |

### docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Dokumentkopf | Umfang geschätzt; Endpoint ohne Evidenzvorbehalt. | Umfang ungeprüfte Projektbasis; Endpoint-Herkunft und Dokumentationsfreigabe offen. | Audit F7; Freigabe Nr. 9 | Bestand, Endpoint-Provenienz und Dokumentationsfreigabe. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Izvršni sažetak | Alle Must-haves ohne Releaseabgrenzung. | Kontaktphase aus Release 1 ausgeschlossen; Details und Vertrag vorläufig. | Audit F1–F3, F6; Freigabe Nr. 3, 5, 8 | Endgültiger Vertrag und spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Potvrđene činjenice | Plattform, Endpoint und Umfang als bestätigte Fakten. | Projektbasis, Annahmen und akzeptierte Architektur getrennt. | Audit F7; Freigabe Nr. 9 | Discovery-Bestätigung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Projektna osnova – Platforma | Bestehende Plattform bestätigt. | Projektbasis, tatsächliche Umgebung ungeprüft. | Audit F7; Freigabe Nr. 9 | Umgebung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Projektna osnova – Projekt | Konkreter Endpoint als öffentlich bestätigte Tatsache wiederholt. | Verweis auf Kopf mit ungeklärter Herkunft/Freigabe; keine erneute URL-Kopie. | Audit F7; Freigabe Nr. 9 | Provenienz und Dokumentationsfreigabe. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Projektna osnova – Obim | 200.000 als bestätigter Bestand. | Schätzung und Nutzerangabe 179 ausdrücklich unbestätigt. | Q9; Audit F7; Freigabe Nr. 9 | Inventar und tatsächliche Anzahl. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Ciljna arhitektura / Tok produkcijskog upita | Diagramm direkt von Validierung zum RPC. | Vorgeschlagene Vorschau-Bestätigung sichtbar als vorläufig. | Audit F5; Freigabe Nr. 7 | Allgemeine Bestätigungspflicht. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Tok produkcijskog upita | Ablauf ohne Evidenzstatus der Suchbestätigung. | Vorgeschlagener Ablauf und gesicherte Q7-Zustimmung getrennt. | Audit F5; Freigabe Nr. 7 | Genereller Ablauf. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Tok produkcijskog upita – Schritt 6 | Nur technische Gates vor RPC. | Vorschlag durchgängig mit Vorschau und erneuter Validierung. | Audit F5; Freigabe Nr. 7 | Bestätigungspflicht bleibt offen. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 2. Kanonski i normalizirani model kandidata – Iskustvo | Vorabnormalisierung und nur relevante Dauer verbindlich. | Normalisierung Vorschlag, gesamte Erfahrungssemantik offen. | Audit F1, F2; Freigabe Nr. 3, 4 | Q8.5, Normalisierung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 2. Kanonski i normalizirani model kandidata – Ausbildungsberufe | Existierende kontrollierte IDs vorausgesetzt. | Existenz prüfen, Nutzung bedingter Vorschlag. | Audit F7; Freigabe Nr. 9 | CRM-IDs. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 2.1 Kontrolisana semantika filtera | Alle Filterregeln normativ ohne Evidenztrennung. | Gesicherte Kernaussagen von vorläufigen Operator-/Vorschauregeln getrennt. | Audit F2, F5; Freigabe Nr. 4, 7 | Historische Regeln und finale Semantik. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 2.1 – Normalisierung | Normalisierung und Nichtzählung als beschlossen. | Normalisierung vorläufig; gesamte Q8.5 offen; Publikationsgrenze bleibt. | Audit F1, F2; Freigabe Nr. 3, 4, 9 | Q8.5 und Normalisierung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 3. Minimalni MCP interfejs | Profilkontakt bei Rolle und Zweck möglich. | Release 1 auch mit Rolle/Zweck ohne Kontakte; spätere Phase. | Q4; Freigabe Nr. 5 | Späteres Kontaktmodell. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 4. Strogi JSON Schema ugovor | JSON als Zielvertrag. | Unvollständiger Entwurf mit benannten Operatorlücken; JSON unverändert. | Audit F6; Freigabe Nr. 8, 9 | Operatoren, Q8.5 und finaler Vertrag. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 4. – zusätzliche Validierung | Validierungsliste als vollständige verbindliche Ergänzung. | Explizit vorgeschlagener unvollständiger Validierungs-/Anzeigefluss. | Audit F5, F6; Freigabe Nr. 7, 8 | Finale Validierung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 4. – leere Filter | Bestätigung oder enger Default als Alternative. | Einheitlicher vorläufiger Ablauf; keine finale Policy. | Audit F5; Freigabe Nr. 7 | Leere Suche. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 4. – Filteranzeige | Anzeige vor oder mit Ergebnis. | Vorgeschlagene Anzeige vor Suche; Status ausdrücklich vorläufig. | Audit F5; Freigabe Nr. 7 | Allgemeine Bestätigung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 6. Sigurnost i kontrola pristupa | Kontakt-Gate als Must-have ohne Phase. | Release-1-Sperre; positive Freigabe nur später. | Audit F3; Freigabe Nr. 5 | Spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 7. Kontrole protiv halucinacija i manipulacije | Nur Verbot automatischer Lockerung. | Konkrete Vorschläge und Zustimmung zur neuen Suche explizit. | Q7; Audit F9 | Erlaubte Lockerungen und Ablauf. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 9. Verifikacija, testovi i mjerljivi ciljevi | Kontakt-Gate-Test im Must-have-Testset. | Release 1 prüft Unterdrückung; positiver Gate-Test später. | Audit F3; Freigabe Nr. 5 | Spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Test-matrica – EMPTY-01 | Alternatives Verhalten als Testziel. | Vorläufiger Ablauf, finale Entscheidung offen. | Audit F5; Freigabe Nr. 7 | Leere Suche und Bestätigung. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Test-matrica – CONTACT-02 | Positiver Kontakt-Test ohne Phasengrenze. | CONTACT-02 später; Release-1-Unterdrückung ausdrücklich geprüft. | Audit F3; Freigabe Nr. 5 | Spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Test-matrica – ZERO-01 | Nur Nulltreffer und keine automatische Lockerung. | Q7-Vorschläge und Zustimmung als Testziel. | Q7; Audit F9 | Konkrete erlaubte Lockerungen. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Kriteriji prihvata | Nur Search-Ausgabe kontaktfrei. | Alle Release-1-Ausgaben kontaktfrei. | Q4; Audit F3; Freigabe Nr. 5 | Spätere Kontaktfreigabe. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Otvorena pitanja i nedostajuće informacije – Q8.5 | Nur Kombination und Intervalldetails offen. | Grundentscheidung zu Erfahrung vollständig offen. | Freigabe Nr. 3 | Gesamte Q8.5. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Otvorena pitanja i nedostajuće informacije – Operations | Operativer Eigentümer erneut offen. | Eigentümer Nutzer; organisatorische Details offen. | Q3; Audit F4; Freigabe Nr. 6 | Hosting/RACI/On-call/Prüfprozesse. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Otvorena pitanja i nedostajuće informacije – Ergänzungen | Q4.5 und Rekonstruktionslücken nicht ausdrücklich genannt. | Offene Frage ohne erfundenen Inhalt und Q8-Detailklärung sichtbar. | Audit F2, F9; Freigabe Nr. 7, 12 | Q4.5-Fragetext und Q8-Details. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Dnevnik odluka – D-013 | Filteroperatoren vollständig akzeptiert. | Rekonstruierte Details Vorschlag; Q7 erhalten. | Audit F2; Freigabe Nr. 4, 7 | Originalempfehlungen und finale Operatoren. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Dnevnik odluka – D-015 | Gesamte Normalisierung akzeptiert. | Normalisierung Vorschlag; akzeptierte Publikationsgrenze getrennt. | Audit F2, F7; Freigabe Nr. 4, 9 | Normalisierungsdetails und IDs. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Preporučeni minimalni release | Alle Must-haves uneingeschränkt. | Release-1-Scope und offene Entwurfsentscheidungen ausdrücklich abgegrenzt. | Audit F3; Freigabe Nr. 5, 8 | Finalisierung und spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Handoff checklista – Rollen | Rollenbenennung offen. | Rollenübernahme erledigt; organisatorische Umsetzung separat offen. | Q3; Audit F4; Freigabe Nr. 6 | RACI, On-call, Prüfprozesse. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Handoff checklista – Kontakt | Kontakt-Gate als erster Handoff. | Kontaktunterdrückung jetzt; Gate/Test später. | Q4; Audit F3; Freigabe Nr. 5 | Spätere Kontaktphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Izvršni sažetak | Kontaktna freigabe | Odobrenje pristupa kontaktima | Sprachliche Präzisierung der Releaseabgrenzung. | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Test-matrica – CONTACT-02 | tek nakon posebne freigabe. | tek nakon posebnog odobrenja. | Sprachliche Präzisierung. | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Preporučeni minimalni release | Kontaktfreigabe i CONTACT-02 | Odobrenje pristupa kontaktima i CONTACT-02 | Sprachliche Präzisierung. | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Handoff checklista – spätere Phase | kasniju zasebnu freigabe. | kasnije zasebno odobrenje. | Sprachliche Präzisierung. | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 3. Minimalni MCP interfejs – Profil | Dozvoljeni detalji profila; kontakti su zasebno zaštićeni. | Dozvoljeni detalji profila; Release 1 uvijek bez kontakata. | Q4; Freigabe Nr. 5 | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Kriteriji prihvata – Scope | - Svaka Must-have stavka ima implementaciju, vlasnika i testni dokaz. | - Svaka Must-have stavka primjenjiva na Release 1 ima implementaciju, vlasnika   i testni dokaz; kontaktna funkcija i CONTACT-02 su izvan tog opsega. | Audit F3; Freigabe Nr. 5 | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Good-to-have zahtjevi – Kontakt | 10. Korisničke role i obavezna potvrda prije punog prikaza kontakta ili izvoza. | 10. Kasnija zasebno odobrena faza: kontaktne/izvozne role i potvrda prije prikaza     kontakta ili izvoza; bez izuzetka od zabrane kontakata u Releaseu 1. | Audit F3; Freigabe Nr. 5 | Spätere Kontakt-/Exportphase. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › Dnevnik odluka – D-006 | Hard cap je 50 kandidata po search stranici; kontakti nisu dio search rezultata. | Hard cap je 50 kandidata po search stranici; Release 1 nema kontaktnih izlaza ni u searchu ni u profilu. | Q4; Freigabe Nr. 5 | Keine neue Entscheidung erforderlich. |
| [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) › 3.1 Odvojeni Profilverwaltungs-MCP – Evidenz | obavezne planske posljedice nalaze se u [ADR-0003](../decisions/0003-separated-profile-administration-mcp.md). | obavezne planske posljedice nalaze se u [ADR-0003](../decisions/0003-separated-profile-administration-mcp.md). Njegov prihvaćeni status ostaje važeći; historijska pojedinačna saglasnost za svaku funkciju nije nezavisno rekonstruisana. Opća potvrda svake pretrage nije isto što i obavezno odobrenje objave profila. | Audit F2; Freigabe Nr. 1, 2, 7 | Historische Detailprovenienz. |

### docs/research/berufssuchprofile-q8-4-2.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Status und Einordnung | Recherche ohne explizite Abgrenzung überholter Empfehlungen. | Historische, offene und durch ADR-0003 überholte Regeln tabellarisch markiert. | Audit F8; Freigabe Nr. 3, 4, 7, 9, 10 | Vertagte Details und ursprüngliche Empfehlungsliste. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Normalisierung vorhandener Freitext-Berufserfahrung | Sichere Regeln automatisch übernehmen mehrdeutig. | Freigegebene Regelanwendung von neuer Mappingfreigabe getrennt. | Audit F8; akzeptierter ADR-0003 | Konkretes Normalisierungsverfahren bleibt Vorschlag. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Berechnung relevanter Berufserfahrung | Erfahrungsgrundregeln ohne aktuellen Offenstatus. | Gesamte Erfahrungsfrage ausdrücklich offen. | Audit F1, F8; Freigabe Nr. 3 | Q8.5. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Berechnung relevanter Berufserfahrung – Begriffe | Ausbildungsberuf mit Erfahrungsberuf verwechselt. | Ausgeübter Beruf und Tätigkeit als offene Relevanzkriterien. | Audit F8; bestätigte Trennung Ausbildung/Erfahrung | Q8.5. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Rollen und Rechte | Alleinfreigabe im Empfehlungstext untersagt. | Passage ausdrücklich als überholt markiert. | Q6; ADR-0003; Audit F8; Freigabe Nr. 10 | Konkrete Prüfprozesse, keine zweite Person vorgeschrieben. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Empfohlene Entscheidung für Q8.4.2 – Verwaltungs-MCP | Verwaltungs-MCP optional. | Optionalität ausdrücklich durch akzeptierten ADR überholt. | ADR-0003; Audit F8; Freigabe Nr. 10 | Vertrag nach Discovery. |
| [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) › Vor der Umsetzung noch zu prüfen | Vier-Augen-Möglichkeit erneut als Voraussetzung gefragt. | Offene Prüfprozesse bei bestätigter Rollen-/Q6-Entscheidung. | Q3/Q6; Audit F8; Freigabe Nr. 6, 10 | Prüfprozesse. |

### README.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [README.md](../../README.md) › Mapa dokumentacije | Kein Einstieg zur Korrekturevidenz. | Änderungsmatrix als Einstieg verlinkt. | Nutzerauftrag: genaue Änderungsübersicht | Keine neue Entscheidung erforderlich. |
| [README.md](../../README.md) › Dokumenteinleitung | scaffold i pristup bazi još nisu uspostavljeni. | scaffold i pristup bazi još nisu uspostavljeni. Navedeni obim je projektna procjena (DURCH DISCOVERY ZU PRÜFEN), ne potvrđen broj zapisa. | Audit F7; Freigabe Nr. 9: Schätzung von geprüftem Bestand trennen. | Tatsächlicher Umfang nach Discovery. |

### docs/decisions/0001-controlled-query-boundary.md

| Datei und Abschnitt | Vorherige Aussage | Neue Aussage | Evidenz oder Begründung | Weiterhin offene Frage |
| --- | --- | --- | --- | --- |
| [docs/decisions/0001-controlled-query-boundary.md](../decisions/0001-controlled-query-boundary.md) › Kontekst | MCP klijente. Slanje cijele baze | MCP klijente. Broj kandidata je projektna procjena, DURCH DISCOVERY ZU PRÜFEN; prihvaćena arhitekturna odluka ne predstavlja audit stvarnog broja zapisa. Slanje cijele baze | Audit F7; Freigabe Nr. 9: Schätzung von geprüftem Bestand trennen. | Tatsächlicher Umfang nach Discovery. |

## Weiterhin offene Fragen und bewusst erhaltene Grenzen

- Q8.5 bleibt vollständig offen; auch „nur relevante Erfahrung“ ist ein Vorschlag.
- Q4.5 bleibt offen, sein Fragetext ist weiterhin unbekannt.
- Q8.4 bleibt grundsätzlich bestätigt. Ursprüngliche Empfehlungsliste,
  Operatorregeln, allgemeine Suchbestätigung und Normalisierungsdetails bleiben
  unbelegt beziehungsweise vorläufig.
- Rollenübernahme ist entschieden; RACI, On-call und konkrete Prüfprozesse nicht.
- Datenbestand, Schema, IDs und Zahlen sind nicht durch dieses Dokument geprüft.
  Die Zahl 179 bleibt eine ungeprüfte Nutzerangabe, 200.000 eine Projektabschätzung.
- Der vorhandene Projekt-Endpunkt wurde nicht aufgerufen. Seine Herkunft und
  Dokumentationsfreigabe bleiben offen; der bestehende Kopfwert wurde nicht
  ersetzt, eine redundante Wiederholung im Brief entfernt. Diese Übersicht
  enthält keine Kopie des Endpunkts.
- Der JSON-Codeblock bleibt inhaltlich unverändert. Seine Unvollständigkeit ist
  ausdrücklich dokumentiert; fehlende Operatoren werden erst nach Entscheidung
  entworfen. Kein neuer ausführbarer Vertrag und keine Anwendungstests entstanden.
- Die akzeptierten Grenzen aus ADR-0001 und ADR-0003 bleiben erhalten. Nur der
  Evidenzstatus und der vorbehaltliche Suchbestätigungsablauf wurden präzisiert.
  Die separate Bestätigung der Veröffentlichung von Profilversionen bleibt gültig.
- Der Forschungsbericht bleibt vollständig als Recherche erhalten; markierte
  historische Empfehlungen sind keine aktuellen Nutzerentscheidungen.
- Das Interview ist nicht abgeschlossen. Q9 bleibt maßgeblich: Sicherheits-
  voraussetzungen, genehmigte read-only Discovery, danach Interviewfortsetzung.

## Verifikation

Prüfdatum: 2026-09-11. Die folgenden Prüfungen wurden tatsächlich ausgeführt.

| Prüfung | Ergebnis |
| --- | --- |
| `rtk proxy markdownlint-cli2 '*.md' 'docs/**/*.md'` | PASS: Exit 0; 16 Dateien, keine Befunde; markdownlint-cli2 0.23.2 / markdownlint 0.41.1. |
| Alle relativen Markdown-Links | PASS: 186 Verweise in 22 Markdown-Dateien einschließlich versteckter Verzeichnisse; Dateiziele und Überschriftenfragmente vorhanden. Externe URLs wurden nicht aufgerufen. |
| `rtk git diff --check` | PASS: Exit 0, keine Ausgabe. Der Check erfasst getrackte Änderungen; unversionierte Dokumente sind zusätzlich durch Lint, Linkprüfung und Snapshot-Vergleich erfasst. |
| `rtk git status --short` | PASS: ausgeführt, Exit 0. Vier getrackte Dokumente geändert; weitere bearbeitete Dokumente und die neue Matrix bleiben unversioniert. Vorhandene unversionierte Verzeichnisse und beide `.DS_Store`-Dateien bleiben erhalten. |
| JSON-Entwurf | PASS: Codeblock gegenüber dem Start dieser Korrekturrunde exakt unverändert; JSON-Syntax lesbar. Kein Nachweis eines vollständigen oder implementierten Vertrags. |
| Entscheidungsstatus | PASS: Q8.5 vollständig OFFEN, Q4.5-Abschnitt unverändert, Q8.4-Grundsatz weiterhin BESTÄTIGT. |
| Erhalt des vorhandenen Markdown-Stands | PASS: genau neun bestehende Dokumente geändert, zwölf weitere einschließlich historischem Audit unverändert; einzige neue Markdown-Datei ist diese Matrix. |

Die erste Linkprüfung fand zwei aus dem Brief übernommene relative Ziele in
dieser Matrix. Beide wurden auf den Standort unter `docs/reviews/` angepasst;
die erneute Prüfung ergab null Fehler. Für die zusätzlichen Leseprüfungen wurde
ein temporäres Python-Script über Bash verwendet, ohne Repository-Testframework
oder Anwendungsimplementierung hinzuzufügen.

### Umfang der Änderungen gegenüber dem Start dieser Korrekturrunde

Die Zahlen umfassen auch Umbrüche und Statushinweise; sie sind kein Git-HEAD-
Vergleich und überschreiben keine älteren Nutzeränderungen.

| Bestehende Datei | Hinzugefügte Zeilen | Entfernte Zeilen |
| --- | --- | --- |
| `AGENTS.md` | 10 | 4 |
| `CONTEXT.md` | 4 | 3 |
| `README.md` | 3 | 1 |
| `docs/project.md` | 16 | 5 |
| `docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md` | 99 | 44 |
| `docs/decisions/0001-controlled-query-boundary.md` | 3 | 1 |
| `docs/decisions/0002-search-design-interview.md` | 91 | 60 |
| `docs/decisions/0003-separated-profile-administration-mcp.md` | 20 | 4 |
| `docs/research/berufssuchprofile-q8-4-2.md` | 36 | 5 |

**Ergebnis der Nacharbeit: PASS_WITH_GAPS.** Die freigegebenen Korrekturen sind
übernommen und die lokalen Dokumentprüfungen erfolgreich. Die fachlichen und
historischen Evidenzlücken oben bleiben ausdrücklich offen. Es erfolgten weder
eine erneute Rekonstruktion des fehlenden Originalchats noch Datenbank- oder
Anwendungstests, externe Änderungen oder ein Commit.
