# Audit der rekonstruierten Entscheidungen

Datum: 2026-09-11

Gesamtstatus: **FAIL**

Die zentralen Nutzerentscheidungen sind überwiegend vorhanden. Der Stand ist
jedoch weder vollständig evidenzgesichert noch widerspruchsfrei: Q8.5 wurde
teilweise geschlossen, obwohl die verfügbare Primärevidenz sie offen hält;
Bestätigungsablauf und JSON-Entwurf passen nicht zur gespeicherten
Filtersemantik. Releaseumfang und Rollenstatus sind im Brief nicht vollständig
nachgeführt. `FAIL` bewertet den Dokumentationsstand, nicht eine Implementierung.

## Umfang, Methode und Evidenzgrenze

Geprüft wurde der vorhandene Arbeitsstand im bestehenden Projektordner auf
`main`, einschließlich bereits veränderter und unversionierter Dokumente.
Alle zehn im Auftrag genannten Dateien wurden vollständig gelesen. Ergänzend
wurden die Routingregeln, die lokalen Domänenregeln und die Skill-Anweisungen
gelesen. Kein Git-Festpunkt wurde als ursprünglicher Entscheidungsstand behandelt.

Der Wrapper `/grill-with-docs` ist im verfügbaren Skill-Katalog nicht vorhanden;
auch die Dateisuche in Projekt und lokalen Skill-Verzeichnissen fand keine
gleichnamige Datei. Verwendet wurde der ausdrücklich vorgesehene Fallback
`grilling` zusammen mit `domain-modeling`: Entscheidungen, Abhängigkeiten und
offene Folgefragen wurden rekonstruiert und gegen das Glossar geprüft.
Die spezielle Review-Grenze des Auftrags hat Vorrang vor den allgemeinen
Skill-Anweisungen zum sofortigen Fortschreiben von ADR und Glossar.

Primärevidenz ist ausschließlich die Tabelle unter „Direkte Entscheidungsevidenz
aus dem bisherigen Nutzerverlauf“ im
[Audit-Auftrag](decision-reconstruction-audit-prompt.md). Sie wird für diesen
Auftrag als vorgegebene Evidenz verwendet; ihre Vollständigkeit und Worttreue
gegenüber dem Originalchat sind nicht unabhängig prüfbar. Akzeptierte ADRs
belegen zusätzlich die geltende dokumentierte Architektur. Ein akzeptierter
Status beweist jedoch nicht rückwirkend den genauen Wortlaut einer Zustimmung.
Wiederholungen in Brief, Projektstatus oder Recherche sind keine neue
Primärevidenz.

Die Prüfung führte keine Datenbankzugriffe, externen Writes, Tickets,
Implementierung oder Korrekturen bestehender Dateien aus. Einzige neue Datei
ist dieser Bericht. Die deutsche Berichtssprache folgt dem deutschen Auftrag.

### Bewertungsbegriffe

| Bewertung | Bedeutung |
| --- | --- |
| `VERIFIZIERT` | Durch die vorgegebene direkte Evidenz, eine akzeptierte Architekturentscheidung oder die bezeichnete lokale Prüfung belegt. Kein Nachweis produktiver Funktion. |
| `PLAUSIBEL` | Konsistent und nachvollziehbar, aber nicht vollständig direkt belegt. |
| `UNVERIFIZIERBAR` | Erforderliche ursprüngliche Empfehlung, Antwort oder technische Evidenz fehlt. |
| `WIDERSPRUCH` | Aussagen oder Statusangaben stimmen nicht überein. |
| `FEHLT` | Eine ausdrückliche Entscheidung fehlt an der bezeichneten Stelle. |
| `ÜBERINTERPRETIERT` | Eine Aussage wird stärker oder konkreter als durch die verfügbare Evidenz gedeckt als bestätigt dargestellt. |

### Fundstellenschlüssel

Jede folgende Fundstelle nennt zusätzlich die genaue Überschrift. Diese
Schlüssel stehen jeweils für die vollständige Datei:

| Schlüssel | Datei |
| --- | --- |
| A | [AGENTS.md](../../AGENTS.md) |
| P | [docs/project.md](../project.md) |
| C | [CONTEXT.md](../../CONTEXT.md) |
| B | [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) |
| D1 | [docs/decisions/0001-controlled-query-boundary.md](../decisions/0001-controlled-query-boundary.md) |
| D2 | [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md) |
| D3 | [docs/decisions/0003-separated-profile-administration-mcp.md](../decisions/0003-separated-profile-administration-mcp.md) |
| R | [docs/runbooks/schema-discovery.md](../runbooks/schema-discovery.md) |
| F | [docs/research/berufssuchprofile-q8-4-2.md](../research/berufssuchprofile-q8-4-2.md) |
| M | [README.md](../../README.md) |

## Entscheidungsmatrix

| Entscheidung | Evidenz | Fundstelle | Bewertung | Begründung |
| --- | --- | --- | --- | --- |
| Q1 | „zuerst A danach C“ | D2 › Q1 – Nächstes verbindliches Ziel; P › Prvi isporučivi cilj | `VERIFIZIERT` | Discovery vor produktivem MCP; kein eigener Staging-Liefergegenstand als Nutzerentscheidung behauptet. Ein späterer sicherer technischer Prototyp ist damit nicht verboten. |
| Q2 | „A“: kleine interne Recruiter-Gruppe | D2 › Q2 – Erste Benutzergruppe; B › Rollout | `VERIFIZIERT` | Zielgruppe korrekt, Brief nennt interne Pilotgruppe. |
| Q3 | „für alle Rollen ich“ | D2 › Q3 – Verantwortliche Rollen; P › Trenutno stanje; D3 › Veröffentlichungsablauf | `VERIFIZIERT` | Rollenübernahme ausdrücklich dokumentiert; Risiken nicht als unabhängige Kontrolle ausgegeben. |
| Q3 im Handoff | Dieselbe Antwort | B › Handoff checklista; B › Otvorena pitanja i nedostajuće informacije, Nr. 10 | `WIDERSPRUCH` | Ernennung aller Verantwortlichen bleibt ungeprüft/offen; operativer Eigentümer wird erneut erfragt. Konkrete On-call-Organisation darf weiter offen bleiben. Siehe F4. |
| Q4 | „nein“ zu Kontakten im ersten Release | D2 › Q4 – Kontaktdaten im ersten Release; B › Rollout | `VERIFIZIERT` | Entscheidung und kontaktfreier Pilot vorhanden. |
| Q4 im Releaseumfang | Dieselbe Antwort | B › 6. Sigurnost i kontrola pristupa; B › Test-matrica; B › Preporučeni minimalni release | `WIDERSPRUCH` | Kontaktfreigabe mit erfolgreicher Ausgabe ist als Must-have/Test enthalten, zugleich sollen alle Must-haves in Release 1. Späterer Gate nicht sauber abgegrenzt. Siehe F3. |
| Q5 | „ja ist zwingend“ | D2 › Q5 – Altersfilter; B › 2. Kanonski i normalizirani model kandidata | `VERIFIZIERT` | Altersfilter als Anforderung festgehalten; Rechtmäßigkeit und technische Umsetzung bleiben offen. Keine Rechtsfreigabe abgeleitet. |
| Q6 | „nein“ zur verpflichtenden zweiten Person | D2 › Q6 – Unabhängige Prüfung; P › Trenutno stanje; D3 › Veröffentlichungsablauf | `VERIFIZIERT` | Keine verpflichtende zweite Person. Getrennte Bearbeitung und Veröffentlichung verlangen für sich genommen keine zweite Person. |
| Q7 | Option B: Vorschläge, neue Suche erst nach Zustimmung | D2 › Q7 – Verhalten bei null exakten Treffern; B › 7. Kontrole protiv halucinacija i manipulacije | `VERIFIZIERT` | Exakte Suche bleibt bestehen; Zustimmung für Lockerungen dokumentiert. Brief enthält das Verbot automatischer Lockerung, aber nicht ausdrücklich die Pflicht, konkrete Vorschläge anzubieten. |
| Q8: Ablehnungen | Globale A/B abgelehnt, C anzupassen | D2 › Q8 – Grundrichtung der Filterverknüpfung | `FEHLT` | Ergebnis C gespeichert; ausdrückliche Ablehnung der beiden globalen Optionen fehlt. Ihre ursprünglichen Detailtexte dürfen nicht erfunden werden. |
| Q8/Q8.4: Zustimmung | Alle empfohlenen Q8.4-Punkte für alle Kategorien | D2 › Q8 – Grundrichtung der Filterverknüpfung; D2 › Q8.4 – Berufssuchprofile für breite Anforderungen | `UNVERIFIZIERBAR` | Zustimmung als solche belegt; genauer Umfang der zuvor empfohlenen Regeln fehlt. Defaults, genau eine Suche, Ausschluss von Wunschkriterien und umfassende Normalisierung lassen sich nicht einzeln zuordnen. Siehe F2. |
| Q8.4: Profilprinzip | Breite Anforderungen über kontrollierte wiederverwendbare Profile | D2 › Q8.4 – Berufssuchprofile für breite Anforderungen; C › Rječnik; B › Dnevnik odluka, D-014 | `VERIFIZIERT` | Fachliches Grundprinzip korrekt vorhanden. Das verifiziert nicht pauschal alle ergänzten Detailregeln. |
| Q8.4.2: nicht exklusiv | Mehrere Profile, keine Sperre, direkte Suche bleibt | D2 › Q8.4.2 – Erstellung und Pflege von Berufssuchprofilen; D3 › Nicht exklusive Profilmitgliedschaft; C › Rječnik | `VERIFIZIERT` | Viele-zu-viele und direkte Suchbarkeit korrekt und konsistent dokumentiert. |
| Zusätzlicher Verwaltungs-MCP | Entscheidung, Zweck und Fähigkeiten dauerhaft festhalten; akzeptierter D3 | D3 › Entscheidung; D3 › Konsequenzen für die Planung; A › Architecture boundaries; B › 3.1 Odvojeni Profilverwaltungs-MCP | `VERIFIZIERT` | Eigene spätere Komponente nach Discovery und Modellfreigabe; nicht als implementiert dargestellt. Historische Einzelzustimmung zu jedem Detail bleibt separat unbelegt. |
| Automatische Zuordnungen | Akzeptierter D3 | D3 › Entscheidung; A › Architecture boundaries; B › 2.1 Kontrolisana semantika filtera | `VERIFIZIERT` | Nur Vorschläge, keine automatische Veröffentlichung. Mehrdeutiger Forschungsablauf siehe F8. |
| Nicht genannte Filter | Keine Einschränkung durch unerwähnte Kategorien | D2 › Q8 – Grundrichtung der Filterverknüpfung; C › Rječnik, Aktiver Filter; B › 2.1 Kontrolisana semantika filtera | `VERIFIZIERT` | Explizit inaktiv; Profil aktiviert nicht automatisch Ausbildung. Autorisierung, Limits und Datenschutz bleiben unabhängig davon wirksam. |
| Elektrikerbeispiel | Fünf Jahre Erfahrung verlangen keine ungenannte Ausbildung | D2 › Q8 – Grundrichtung der Filterverknüpfung; B › 2.1 Kontrolisana semantika filtera | `VERIFIZIERT` | Trennung Erfahrung/Ausbildung korrekt. Zwingende Auflösung gerade in ein Berufssuchprofil ist lediglich `PLAUSIBEL`, nicht direkt belegt; direkte Berufssuche muss möglich bleiben. |
| Q8.5 | Noch offen, Rückkehr erst nach Q8.4.2 | D2 › Q8.5 – Bedeutung von Berufserfahrung | `WIDERSPRUCH` | `TEILWEISE BESTÄTIGT` und „nur fachlich passend“ schließen bereits einen Teil. Dafür fehlt eine ausdrücklich zuordenbare Antwort. Siehe F1. |
| Q9 | Option C: Sicherheit, Discovery, danach Interview | D2 › Q9 – Reihenfolge von Interview und Datenbank-Discovery; R › Preduslovi; P › Put do implementacije | `VERIFIZIERT` | Reihenfolge korrekt, keine aktuelle Datenbankfreigabe abgeleitet. Die konkrete Sicherheitscheckliste ist als Runbook-Anforderung nachvollziehbar, nicht als bereits erfüllte Freigabe. |
| Tabellenzahl | 179 als unbestätigte Nutzerangabe | D2 › Q9 – Reihenfolge von Interview und Datenbank-Discovery | `VERIFIZIERT` | Attribution und noch ausstehende Verifikation explizit. Zahl nicht als auditiert ausgegeben. |
| Q4.5 | Ausdrücklich offen; Frage fehlt | D2 › Q4.5 – Vom Nutzer als offen markiert | `VERIFIZIERT` | Offen und ohne erfundenen Fragetext dokumentiert. |
| Physische Datenlage | Discovery steht aus | D2 › Q8 – Grundrichtung der Filterverknüpfung; D2 › Q8.4 – Berufssuchprofile für breite Anforderungen; B › 2. Kanonski i normalizirani model kandidata | `UNVERIFIZIERBAR` | Kontrollierte CRM-Auswahl und vorhandene IDs als Bestand behauptet, aber weder vorgegebene Nutzeraussage noch Audit belegt diese Details. Siehe F7. |
| Kontrollierte Query-Grenze | Akzeptierter D1 | D1 › Odluka; A › Architecture boundaries; B › Ciljna arhitektura | `VERIFIZIERT` | Kein freier Runtime-SQL, maximal 50 pro Suchseite, PostgreSQL autoritativ, physischer Vertrag erst nach Audit. |
| Weitere offene Entscheidungen | Keine dazu vorgegebene Zustimmung | D2 › Weitere offene Entscheidungen; B › Otvorena pitanja i nedostajuće informacije | `PLAUSIBEL` | Verlauf, Export, Cache, Auth, Hosting, Ranking und SLOs sichtbar offen. Vollständigkeit gegenüber dem Gesamtchat nicht prüfbar. |

## Befunde und konkrete Korrekturvorschläge

### F1 – Q8.5 wurde ohne zuordenbare Evidenz teilweise geschlossen

**Bewertung: `WIDERSPRUCH` / `ÜBERINTERPRETIERT`.**

D2 › „Q8.5 – Bedeutung von Berufserfahrung“ setzt `TEILWEISE BESTÄTIGT` und
bestätigt bereits ausschließlich fachlich passende Beschäftigungszeiten.
Die vorgegebene Evidenz hält Q8.5 offen. Das Elektrikerbeispiel belegt sicher
den Verzicht auf einen ungenannten Ausbildungsfilter, aber weder die vollständige
Relevanzregel noch die Zustimmung zu einer bestimmten Zeitberechnung.

**Vorschlag:** In D2 Q8.5 als `OFFEN` führen, soweit kein Originalbeleg für die
Teilentscheidung nachgereicht wird. Vorhandene plausible Fachregeln als
Vorschlag erhalten. In C › „Rječnik“ die Definition „Relevante Berufserfahrung“
entsprechend als vorläufig markieren. In B › „2. Kanonski i normalizirani model
kandidata“ und „2.1 Kontrolisana semantika filtera“ bestätigte Normalisierungs-
und Profilgrenzen von der noch offenen Relevanzregel trennen. Die bereits
sichtbar offenen Überlappungsfragen bleiben offen.

### F2 – Pauschale Zustimmung ist keinem historischen Empfehlungssatz zugeordnet

**Bewertung: `UNVERIFIZIERBAR`; vorbehaltlose Einzelbestätigung wäre
`ÜBERINTERPRETIERT`.**

D2 › „Q8 – Grundrichtung der Filterverknüpfung“ und „Q8.4 – Berufssuchprofile für
breite Anforderungen“ enthalten viele konkrete Regeln: `ANY`-Defaults,
Bereichslogik, `NOT`, fehlende Werte, Bestätigung jeder Suche, genau eine
Datenbanksuche, keine Pflicht-/Wunschkriterien in Version 1, Normalisierung mit
Originaltext und kontrollierten IDs. Der Auftrag belegt „alle empfohlenen
Punkte“, liefert aber die damalige Liste und ihre Reihenfolge nicht.

F › „Empfohlene Entscheidung für Q8.4.2“ ersetzt diesen Beleg nicht: Dort werden
beispielsweise Pflicht- und Wunschrollen empfohlen, die D2 vorerst ausschließt.
Nicht beweisbar ist, welche Fassung der Nutzer tatsächlich bestätigte.
D3 ist als akzeptierter Architekturstand zu respektieren; dessen Wiederholung
derselben Regeln ist kein unabhängiger Beleg ihrer historischen Annahme.

**Vorschlag:** D2 um die zuordenbare Empfehlungsliste mit Antwortbeleg ergänzen,
oder bei den betreffenden Details ausdrücklich die Rekonstruktionslücke nennen.
Dass Q8.4 grundsätzlich bestätigt wurde, darf dabei nicht wieder geöffnet
werden. B › „Dnevnik odluka“, D-013 bis D-015, und P › „Trenutno stanje“ sollten
diese Unterscheidung übernehmen. In D3 › „Kontext“ den Unterschied zwischen
geltendem ADR und noch ungeprüfter historischer Detailprovenienz kennzeichnen;
keine akzeptierte Sicherheitsgrenze stillschweigend entfernen.

### F3 – Kontaktfreier erster Release und Must-have-Kontaktfreigabe kollidieren

**Bewertung: `WIDERSPRUCH`.**

D2 › „Q4 – Kontaktdaten im ersten Release“ sagt Nein. B › „Rollout“ sieht einen
kontaktfreien Pilot vor. B › „6. Sigurnost i kontrola pristupa“ verlangt jedoch
einen Kontakt-Gate; „Test-matrica“, `CONTACT-02`, erwartet erfolgreiche Ausgabe
eines Kontakts. „Preporučeni minimalni release“ verlangt sämtliche Must-haves,
„Handoff checklista“ deren Implementierung. Kontaktunterdrückung ist nötig;
Kontaktfreigabe als erste Releasefunktion ist nicht beschlossen.

**Vorschlag:** B in diesen Abschnitten ausdrücklich in Release 1 ohne
Kontakt-Ausgabe und spätere separat freizugebende Kontaktfunktion aufteilen.
`CONTACT-02` als späteren Test kennzeichnen; für Release 1 die verweigerte
Kontaktausgabe auch über `get_candidate_profile` verlangen. A › „Architecture
boundaries“ kann die allgemeine spätere Ausnahme behalten, sollte Q4 aber
explizit referenzieren. Keine neue Nutzerentscheidung über Q4 erforderlich.

### F4 – Bereits übernommene Rollen stehen im Brief weiter als unerledigt

**Bewertung: `WIDERSPRUCH`.**

D2 › „Q3 – Verantwortliche Rollen“ und P › „Trenutno stanje“ sind eindeutig.
B › „Handoff checklista“ beginnt dagegen mit der offenen Ernennung von
Product, Data, Security, Privacy/Legal und Operations. B › „Otvorena pitanja i
nedostajuće informacije“, Nr. 10, fragt erneut nach dem operativen Eigentümer.

**Vorschlag:** Rollenübernahme dort als entschieden mit Q3-Verweis führen.
Auditfreigabe, RACI-Ausarbeitung und On-call-Verfahren weiterhin offen lassen.
Nr. 12 und D-012 im Brief betreffen zusätzlich Taxonomiepflege und
Genehmigungsprozesse: Diese Detailprozesse nicht allein aus „alle Rollen ich“
als fertig ableiten. Q6 erfordert keine Aufhebung von Security-/Privacy-Prüfungen
durch den Nutzer selbst.

### F5 – Bestätigung vor jeder Suche fehlt im dargestellten Produktionsablauf

**Bewertung: `WIDERSPRUCH` innerhalb des gespeicherten Sollzustands.**

D2 › „Q8 – Grundrichtung der Filterverknüpfung“ und B › „2.1 Kontrolisana
semantika filtera“ verlangen Vorschau, ausdrückliche Bestätigung und erneute
Validierung vor jeder neuen/geänderten Suche. B › „Tok produkcijskog upita“
geht von Validierung direkt zum RPC. B › „4. Strogi JSON Schema ugovor“ erlaubt
Filteranzeige „prije ili uz rezultate“, also vor oder zusammen mit Ergebnissen;
bei leeren Filtern ist eine Bestätigung nur eine Alternative zum restriktiven
Limit. Dieselbe Alternative steht in „Test-matrica“, `EMPTY-01`.

**Vorschlag:** Nach Klärung der Detailprovenienz aus F2 den Ablauf, das
Architekturbild, die zusätzlichen Validierungsregeln und `EMPTY-01` auf dieselbe
Bestätigungspflicht bringen. Bis dahin die Abweichung ausdrücklich markieren.
Eine Zustimmung zu Lockerungen gemäß Q7 bleibt unabhängig davon belegt.

### F6 – JSON-Entwurf kann nicht alle gespeicherten Operatoren ausdrücken

**Bewertung: `WIDERSPRUCH`; strukturell lokal `VERIFIZIERT`.**

B › „4. Strogi JSON Schema ugovor“ enthält Arrays für Berufe, Orte und
Verfügbarkeit, aber keinen Ausschlussoperator und keine wählbare
UND-Verknüpfung für diese Arrays. `match_all_skills` und `match_all_languages`
decken nur zwei Kategorien ab. Gleichzeitig verlangt D2 › „Q8 – Grundrichtung
der Filterverknüpfung“ ausdrückliches UND/ODER für gültige Kombinationen sowie
`NOT`; B › „2.1 Kontrolisana semantika filtera“ verlangt ebenfalls `NOT`.

Beispiel: „Deutsch, aber nicht Standort X“ lässt sich als expliziter
Standortausschluss im beschriebenen strukturierten Vertrag nicht darstellen.
Das generische Feld `text` definiert dafür keinen kontrollierten Operator.
Eine direkte Suche nach zwei nachgewiesenen Ausbildungsberufen mit UND hat
ebenfalls kein entsprechendes Feld. Ein Ausführungsfehler wurde nicht getestet,
weil noch kein Runtime existiert.

**Vorschlag:** Den JSON-Block als unvollständigen Vertragsentwurf kennzeichnen
und nach Bestätigung der Semantik gezielt ergänzen; keine beliebigen Ausdrücke
oder SQL-Fragmente einführen. Positive und negative Beispiele in „Test-matrica“
ergänzen. Q8.5 dabei nicht durch eine implizite AND-Regel zwischen Beruf und
Tätigkeit entscheiden.

### F7 – Ungeprüfte Bestandsaussagen erscheinen als bestätigte Fakten

**Bewertung: `UNVERIFIZIERBAR` / `ÜBERINTERPRETIERT`.**

D2 › „Q8 – Grundrichtung der Filterverknüpfung“ nennt unter „Bestätigte fachliche
Ausgangslage“ eine kontrollierte CRM-Auswahlliste. D2 › „Q8.4 – Berufssuchprofile
für breite Anforderungen“ und B › „2. Kanonski i normalizirani model kandidata“
setzen vorhandene kontrollierte CRM-IDs voraus. D2 › „Q8.5 – Bedeutung von
Berufserfahrung“ behauptet mehrsprachige Freitext-Erfahrungsdaten als Bestand.
Diese Angaben können zutreffen, sind aber in der vorgegebenen Primärevidenz
nicht enthalten und wurden nicht durch Discovery bestätigt.

B › „Potvrđene činjenice“ bezeichnet auch Plattform, Umfang und Projektbezug
als bestätigt. Der ungefähre Umfang ist in D1 › „Kontekst“ als Projektbasis
enthalten, aber kein technisch geprüfter Datenbestand. Die Herkunft des
konkreten Projekt-Endpunkts ist hier nicht belegt; er wird im Bericht nicht
wiedergegeben. Seine Bezeichnung als öffentlich verifiziert keine Freigabe
zur Ablage im Repository.

**Vorschlag:** In D2 und B sauber zwischen belegter Nutzerangabe, Arbeitsannahme,
akzeptiertem Zielmodell und Discovery-Befund unterscheiden. „Vorhandene IDs“
bis zur Prüfung als bedingte Designanforderung formulieren. Für den bereits im
Brief enthaltenen Endpunkt die Freigabe zur Dokumentation klären und bei Bedarf
nach Freigabe entfernen. Keine neuen Tabellen, Spalten oder Beziehungen erfinden.

### F8 – Rechercheempfehlungen sind nicht gegen spätere Entscheidungen abgegrenzt

**Bewertung: `PLAUSIBEL` als historische Empfehlung; aktuelle Geltung teils
`UNVERIFIZIERBAR`, fachliche Begriffe teils `WIDERSPRUCH`.**

F ist ausdrücklich Recherche und keine Architekturentscheidung. Deshalb sind
abweichende Empfehlungen nicht automatisch falsch gespeicherte Nutzerantworten.
Ohne Statushinweise können sie jedoch als aktuelle Vorgaben gelesen werden:

- F › „Rollen und Rechte“ empfiehlt Vier-Augen-Prüfung und formuliert „darf
  dieselbe Version nicht allein freigeben“. D3 › „Veröffentlichungsablauf“
  erlaubt alle Rollen beim Nutzer ohne verpflichtende zweite Person.
- F › „Kurzurteil“, „3. Mitgliedschaften statt automatischer Obergruppe“ und
  „Empfohlene Entscheidung für Q8.4.2“ fordern Pflicht-/Wunschrollen; D2 › „Q8 –
  Grundrichtung der Filterverknüpfung“ vertagt diese für Version 1.
- F › „Empfohlene Entscheidung für Q8.4.2“, Nr. 12, nennt den Verwaltungs-MCP
  optional; D3 › „Entscheidung“ plant ihn verbindlich nach Discovery.
- F › „Normalisierung vorhandener Freitext-Berufserfahrung“ sagt „sichere Regeln
  automatisch übernehmen“. Die Anwendung eines bereits freigegebenen Alias kann
  dazu passen; die automatische Freigabe einer neuen Zuordnung widerspräche
  A › „Architecture boundaries“. Der Ablauf trennt beides nicht ausdrücklich.
- F › „Berechnung relevanter Berufserfahrung“ fragt nach einem passenden
  **Ausbildungsberuf** oder Tätigkeit; D2 › „Q8 – Noch offene Unterfragen“
  fragt nach Beruf oder Tätigkeit im Beschäftigungsabschnitt. Formale Ausbildung
  und ausgeübter Beruf sind laut C › „Rječnik“ getrennte Begriffe.

**Vorschlag:** In F die betroffenen Empfehlungen als historische, vertagte oder
durch D3 überholte Optionen kennzeichnen; die Recherche nicht löschen.
Deterministische Anwendung freigegebener Regeln von neuen Mappingvorschlägen
trennen. In der Q8.5-Passage ausgeübten Beruf und Ausbildung präzise auseinander-
halten, ohne die noch offene Relevanzentscheidung selbst zu treffen.

### F9 – Fehlende Übernahme expliziter Antworten und schwache Nachverfolgbarkeit

**Bewertung: `FEHLT` an den jeweils bezeichneten Stellen.**

- D2 › „Q8 – Grundrichtung der Filterverknüpfung“: globale Optionen A und B
  ausdrücklich als abgelehnt festhalten; genaue ursprüngliche Definitionen
  fehlen weiterhin und dürfen nicht rekonstruiert erfunden werden.
- B › „7. Kontrole protiv halucinacija i manipulacije“ und „Test-matrica“,
  `ZERO-01`: Q7 verlangt nicht nur keine automatische Lockerung, sondern
  konkrete Vorschläge bei null Treffern und Zustimmung vor der neuen Suche.
  Dies dort ergänzen; erlaubte Lockerungen bleiben offen.
- P › „Trenutno stanje“: Q4.5 und Q8.5 sind nur über den allgemeinen D2-Link
  auffindbar. Die beiden bekannten offenen Punkte und den Q9-Ablauf ausdrücklich
  nennen, damit „Q8.4 bestätigt“ nicht als Interviewabschluss gelesen wird.
- B › „Otvorena pitanja i nedostajuće informacije“: Q4.5 fehlt als offener
  Platz im Entscheidungsregister; auf den fehlenden Fragetext in D2 verweisen.
  Das ist keine Erlaubnis, einen Fragetext zu ergänzen.

Keine der vorgegebenen Entscheidungen fehlt vollständig in sämtlichen Dateien,
außer der ausdrücklichen Ablehnung der globalen Q8-Optionen. Eine Entscheidung
muss nicht wörtlich in jedem Dokument wiederholt werden; präzise Verweise genügen.

## Korrekt gespeicherte Grenzen und offene Fragen

Q1 bis Q7 sind in D2 in ihren durch den Auftrag belegten Kernaussagen korrekt.
Q3 und Q6 sind dort ausdrücklich entschieden. Q4.5 ist offen, ohne erfundenen
Inhalt. Q9 und die unbestätigte Herkunft der Zahl 179 sind korrekt. Profile sind
nicht exklusiv; direkte Berufssuche bleibt erhalten. Nicht genannte Filter sind
inaktiv. D3 und A halten automatische Veröffentlichung ausdrücklich ausgeschlossen.

A › „Current phase“, P › „Trenutno stanje“, D1 › „Odluka“, D3 › „Konsequenzen für
die Planung“, R › „Svrha“ und M › „Supabase CRM MCP“ stellen Discovery,
Implementierung und produktive Freigabe zutreffend als ausstehend dar. Der
konzeptionelle SQL-Block in B › „5. Kontrolisana PostgreSQL RPC pretraga“ ist
ausdrücklich keine Migration. Keine vorgegebenen physischen Tabellen oder
bereits eingerichteten RLS-Rechte werden daraus abgeleitet.

**Versehentlich geschlossene Fragen:** Nachweisbar betroffen ist der Teilstatus
von Q8.5 (F1). Für Q4.5 gibt es keinen solchen Befund. Die übrigen bekannten
Interviewthemen sind in D2 › „Weitere offene Entscheidungen“ sichtbar offen.
D3 › „Grenze zum Runtime-Such-MCP“ verlangt Versionsbezug für Verlauf und Export;
das belegt eine Bedingung für diese Funktionen, nicht deren Releasefreigabe.
Diese Bedingtheit sollte dort ausdrücklich stehen.

Die offene Frontier bleibt:

- Q4.5: ursprüngliche Frage und Optionen wiederherstellen.
- Q8.5: Relevanz von ausgeübtem Beruf und Tätigkeit, Überlappungen und
  unvollständige Zeitintervalle entscheiden; technische Datenlage zuvor prüfen.
- Lockerungen und Bestätigungsablauf; Verlauf, gespeicherte Suchen, Audit,
  Snapshots und Zugriffsrechte; Darstellung; Export; Cache und Aktualität.
- Authentifizierung, Tenant-Modell, Hosting, Ranking, SLOs sowie rechtliche und
  organisatorische Ausgestaltung; Schemafakten durch Discovery, nicht durch Raten.

Es wurden keine neuen Interviewantworten eingeholt oder in Entscheidungen
umgewandelt. Die nächsten fachlichen Fragen bleiben gemäß Q9 hinter der
Klärung der Discovery-Sicherheitsvoraussetzungen und dem Audit eingeordnet.

## Punkte, die nur der Nutzer klären kann

1. Den fehlenden Fragetext und die Optionen von Q4.5 liefern.
2. Die ursprüngliche Empfehlungsliste zu „alle empfohlenen Punkte“ zuordnen
   oder die in F2 genannten Details erneut ausdrücklich bestätigen; vorhandene
   Originalauszüge würden eine erneute Entscheidung vermeiden.
3. Klären, ob eine ausdrückliche Teilantwort zu Q8.5 existierte. Falls nicht,
   die Frage später gemäß Q9 entscheiden; das Audit ersetzt diese Antwort nicht.
4. Die Herkunft der in F7 behaupteten CRM-Bestandsangaben und gegebenenfalls die
   Dokumentationsfreigabe für den Projekt-Endpunkt klären. Technische Richtigkeit
   bestätigt anschließend der genehmigte Audit.
5. Soweit die ursprüngliche Zustimmung nicht auffindbar ist: den detaillierten
   Funktionsumfang von D3 gegenüber den damaligen Empfehlungen bestätigen.
   Der aktuell akzeptierte ADR bleibt bis zu einer ausdrücklichen Änderung gültig.
6. Über die im Bericht vorgeschlagenen Dokumentkorrekturen entscheiden.
   Bestehende klare Antworten wie Q3, Q4, Q6 und die Nicht-Exklusivität werden
   dabei nicht erneut zur Abstimmung gestellt.

Die bekannten weiteren Geschäftsentscheidungen bleiben beim Nutzer. Datenbank-
fakten, Feldnamen, tatsächliche Zugriffsrechte und technische Machbarkeit sind
hingegen durch genehmigte Discovery zu ermitteln, nicht als Nutzerpräferenz zu
beantworten.

## Was ohne vollständigen Originalchat nicht geprüft werden kann

Nicht prüfbar sind die Vollständigkeit aller damaligen Fragen und Antworten,
ihre genaue Reihenfolge, der Umfang einer pauschalen Zustimmung, spätere
Widerrufe und der ursprüngliche Fragetext von Q4.5. Ebenso fehlt der Beleg,
welche Detailfähigkeiten des Verwaltungs-MCP und welche Normalisierungsregeln
vor der jeweiligen Zustimmung tatsächlich vorgeschlagen wurden.

Der jetzige Recherchebericht und die rekonstruierte ADR-Fassung beweisen diese
Historie nicht. Aus dem Fehlen eines Belegs folgt nicht, dass eine Aussage
falsch ist; es verhindert die Einstufung als unabhängig bestätigte Nutzerantwort.
Die externen Fachquellen der Recherche wurden nicht neu sachlich auditiert.

## Verifikation

Prüfdatum: 2026-09-11. Ausführung aus dem Projektverzeichnis über die lokale
Shell; Bash wurde für die zusätzlichen strukturellen Prüfungen verwendet.

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| `rtk proxy markdownlint-cli2 '*.md' 'docs/**/*.md'` | `PASS`: Exit 0, markdownlint-cli2 0.23.2 / markdownlint 0.41.1, 15 Dateien, 0 Befunde. |
| `rtk git diff --check` | `PASS`: Exit 0, keine Ausgabe. Prüft die bestehenden getrackten Änderungen; unversionierte Dateien werden dadurch nicht inhaltlich geprüft. |
| `rtk git status --short` | Exit 0. Bestehende Änderungen an `AGENTS.md`, Brief und Projektstatus sowie unversionierte Dateien bleiben vorhanden. Bericht liegt im weiterhin unversionierten Verzeichnis `docs/reviews/`. |
| Relative Markdown-Ziele und Überschriftenfragmente | `PASS`: 102 lokale Verweise in Root- und `docs`-Markdown geprüft, 0 fehlende Ziele/Fragmente. |
| JSON-Block des Briefs | `PASS` für JSON-Syntax. Strukturell keine Felder für Ausschluss oder explizites Berufs-UND vorhanden; F6 ist keine Behauptung über einen ausgeführten Runtime. |
| Erhalt bestehender Dateien | `PASS`: SHA-256-Vergleich der 26 vor Berichtserstellung erfassten Dateien außerhalb `.git` zeigt keine Änderung oder Löschung. |

**Verifikationsgrenzen:** Während der Prüfung erschienen zusätzlich `.DS_Store`
und `docs/.DS_Store`. Es wurde kein Schreibbefehl für diese Dateien ausgeführt;
ihre Herkunft ist nicht verifiziert. Sie wurden nicht entfernt. Der
Dateivergleich zeigt deshalb neben dem Bericht zwei zusätzliche Umgebungsdateien;
die Aussage „im gesamten Ordner entstand ausschließlich der Bericht“ wäre falsch.
Der Agent hat ausschließlich diesen Bericht geschrieben.

Öffentliche externe Links und die Fachbehauptungen der Recherche wurden nicht
neu geprüft; dies bleibt ein Gap gegenüber der breiteren README-Linkprüfung.
Keine Datenbank-, Build-, Runtime-, RLS- oder Anwendungstests wurden ausgeführt;
sie gehören nicht zu diesem Dokumentationsaudit. Die grünen Formatprüfungen
heben das inhaltliche Gesamturteil `FAIL` nicht auf.

## Freigabepunkt

Es wurden keine vorgeschlagenen Korrekturen übernommen. Der Audit-Auftrag
verlangt zuerst diesen vollständigen Bericht und anschließend eine ausdrückliche
Entscheidung zur Übernahme. Unbelegte fachliche Details werden auch bei einer
Korrekturfreigabe nicht ohne zusätzliche Evidenz als bestätigt eingetragen.
