# ADR-0002: Entwurf für Suchablauf und Filtersemantik

Datum: 2026-09-11

Status: Entwurf – Interview läuft

Sprache des Entscheidungsprotokolls: Deutsch

## Zweck

Dieses Dokument sichert die Fragen und ausdrücklichen Antworten des laufenden
Designinterviews. Es ist noch keine akzeptierte Architekturentscheidung. Eine
Antwort gilt nur dann als bestätigt, wenn der Nutzer sie ausdrücklich gegeben
hat; Erläuterungen, Empfehlungen und bloß diskutierte Möglichkeiten bleiben
offen.

## Statusbegriffe

<!-- markdownlint-disable MD013 -->

| Status | Bedeutung |
| --- | --- |
| `BESTÄTIGT` | Der Nutzer hat die Entscheidung ausdrücklich getroffen. |
| `TEILWEISE BESTÄTIGT` | Ein Teil ist entschieden; abhängige Details sind offen. |
| `OFFEN` | Es liegt noch keine ausdrückliche Antwort vor. |
| `ABGELEHNT` | Der Nutzer hat die Möglichkeit ausdrücklich ausgeschlossen. |
| `ERSETZT` | Eine spätere ausdrückliche Entscheidung ersetzt die frühere. |
| `VORLÄUFIGER VORSCHLAG` | Fachlicher oder technischer Vorschlag ohne belegte Nutzerbestätigung. |
| `ARBEITSANNAHME` | Unbestätigte Ausgangsannahme, keine festgestellte Tatsache. |
| `DURCH DISCOVERY ZU PRÜFEN` | Technische Bestandsaussage ohne abgeschlossene Prüfung. |

<!-- markdownlint-enable MD013 -->

## Fragen, Antworten und gekennzeichnete Vorschläge

Korrekturstand 2026-09-11: Der Nutzer hat die Korrekturen aus dem
[Auditbericht](../reviews/decision-reconstruction-audit.md) ausdrücklich
freigegeben. Die Freigabe bestätigt keine unbelegten Detailregeln. Insbesondere
bleiben Q8.4 grundsätzlich bestätigt, Q8.5 vollständig offen und die allgemeine
Bestätigungspflicht vor jeder Suche ein Vorschlag. Die
<!-- markdownlint-disable-next-line MD013 -->
[Änderungsmatrix](../reviews/decision-reconstruction-corrections.md) dokumentiert
die Übernahme und die weiterhin offenen Punkte.

### Q1 – Nächstes verbindliches Ziel

**Frage:** Was soll als Nächstes tatsächlich geliefert werden: nur ein sicherer
Discovery-Bericht, ein technischer Staging-Prototyp oder bereits ein produktiver
MCP für Recruiter?

**Antwort:** `BESTÄTIGT` – Zuerst der sichere Discovery-Bericht, danach der
produktive MCP. Ein Staging-Prototyp wurde nicht als eigener Zielschritt
bestätigt.

### Q2 – Erste Benutzergruppe

**Frage:** Wer soll die erste Version verwenden: eine kleine interne
Recruiter-Gruppe, alle internen Recruiter oder externe Kunden beziehungsweise
mehrere Unternehmen?

**Antwort:** `BESTÄTIGT` – Eine kleine interne Recruiter-Gruppe.

### Q3 – Verantwortliche Rollen

**Frage:** Wer übernimmt Product, Data, Security, Privacy/Legal, Operations und
Discovery?

**Antwort:** `BESTÄTIGT` – Der Nutzer übernimmt derzeit alle genannten Rollen.
RACI,
On-call-Ablauf und konkrete Prüfprozesse bleiben `OFFEN`. Die
organisatorischen und sicherheitsbezogenen Risiken dieser Rollenkombination
bleiben sichtbar und werden nicht als unabhängige Prüfung dargestellt.

### Q4 – Kontaktdaten im ersten Release

**Frage:** Muss der erste Release Telefonnummern oder E-Mail-Adressen anzeigen?

**Antwort:** `BESTÄTIGT` – Nein. Release 1 gibt über keinen seiner
Zugriffspfade Kontaktdaten aus, auch nicht im Kandidatenprofil. Kontaktfreigabe
und CONTACT-02 gehören in eine spätere, separat freizugebende Phase.

### Q5 – Altersfilter

**Frage:** Ist die Suche nach Alter beziehungsweise Geburtsdatum eine zwingende
geschäftliche Anforderung oder nur ein Beispiel?

**Antwort:** `BESTÄTIGT` – Der Altersfilter ist zwingend erforderlich. Die
rechtliche, datenschutzbezogene und technische Ausgestaltung ist noch offen.

### Q6 – Unabhängige Prüfung

**Frage:** Müssen Security und Datenschutz vor dem Produktivstart von einer
zweiten Person unabhängig geprüft werden?

**Antwort:** `BESTÄTIGT` – Nein. Eine unabhängige Prüfung durch eine zweite
Person ist nicht verpflichtend vorgesehen.

### Q7 – Verhalten bei null exakten Treffern

**Frage:** Soll das System Filter automatisch lockern, null Ergebnisse anzeigen
und Lockerungen vorschlagen oder sofort ähnliche Kandidaten anzeigen?

**Antwort:** `BESTÄTIGT` – Option B: Die exakte Suche bleibt unverändert. Bei
null
Treffern werden konkrete Lockerungen vorgeschlagen; eine geänderte Suche beginnt
erst nach ausdrücklicher Zustimmung. Die genaue Gestaltung eines vorab
genehmigten Fallback-Plans ist noch offen.

### Q8 – Grundrichtung der Filterverknüpfung

**Frage:** Wie sollen mehrere Kategorien und mehrere Werte innerhalb einer
Kategorie miteinander verbunden werden?

**Belegter Entscheidungsstand:** Globale Optionen A und B sind `ABGELEHNT`.
Ihre ursprünglichen Definitionen sind nicht überliefert und werden nicht
ergänzt. Option C sollte angepasst werden. Die spätere Zustimmung zu allen
empfohlenen Q8.4-Punkten für alle Kategorien ist belegt; die damalige
vollständige
Empfehlungsliste fehlt. Deshalb ist die genaue Detailsemantik eine
**Rekonstruktionslücke**, keine pauschal bestätigte Regelmenge.

<!-- markdownlint-disable MD013 -->

| Kategorie | Regel und Evidenzstatus |
| --- | --- |
| Unterschiedliche Kategorien | `VORLÄUFIGER VORSCHLAG`: Verknüpfung mit `UND`. |
| Alter und andere Bereiche | `VORLÄUFIGER VORSCHLAG`: beide angegebenen Grenzen müssen erfüllt sein. |
| Ausbildungsberufe und Erfahrungsberufe | `VORLÄUFIGER VORSCHLAG`: mehrere Werte standardmäßig als Alternativen (`ANY`). |
| Standorte und Verfügbarkeitswerte | `VORLÄUFIGER VORSCHLAG`: mehrere Werte standardmäßig als Alternativen (`ANY`). |
| Sprachen und Fähigkeiten | `VORLÄUFIGER VORSCHLAG`: ausdrückliches `UND`/`ODER` übernehmen; unklare Listen in der Vorschau klären. |
| Berufserfahrung | `OFFEN`: gesamte Q8.5 einschließlich Relevanzregel und Zeitberechnung. |
| Ausschlüsse | `VORLÄUFIGER VORSCHLAG`: ausdrücklich gesetzte Ausschlüsse als `NOT`. |
| Fehlende Werte | `VORLÄUFIGER VORSCHLAG`: kein positiver Pflichtfiltertreffer; das geltende Verbot erfundener Werte bleibt bestehen. |
| Nicht genannte Filter | `BESTÄTIGT`: inaktiv, keine Einschränkung der Suche. |

<!-- markdownlint-enable MD013 -->

**VORLÄUFIGER VORSCHLAG – Soll-Ablauf:** Vor jeder neuen oder geänderten Suche
werden Filter, Operatoren und aufgelöste Profilmitglieder angezeigt. Nach
ausdrücklicher Bestätigung und erneuter Servervalidierung folgt genau eine
Datenbanksuche. Diese allgemeine Bestätigungspflicht und die Ein-Suche-Regel
sind nicht endgültig bestätigt. Die ausdrücklich belegte Zustimmung vor einer
gelockerten Suche gemäß Q7 bleibt verbindlich. Ob Pflicht- und Wunschkriterien
zur ersten Regelversion gehören, bleibt `OFFEN`.

**BESTÄTIGT:** „Elektriker mit fünf Jahren Berufserfahrung“ verlangt keine
entsprechende Ausbildung, wenn Ausbildung nicht genannt wurde. Auch andere
ungenannte Kategorien bleiben inaktiv. Die konkrete Abbildung auf direkte
Berufs-IDs oder ein Berufssuchprofil und die Erfahrungsberechnung sind noch
festzulegen; direkte Berufssuche bleibt möglich.

**ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN:** Ausbildungsberufe könnten im
CRM über kontrollierte Auswahloptionen erfasst sein. Vorhandensein, IDs und
Filterbarkeit sind nicht auditiert; die ursprüngliche Aussagequelle fehlt.
Davon unabhängig ist das bestätigte Ziel, breite Anforderungen über Profile
abzubilden, ohne jeden Einzelberuf eingeben zu müssen.

### Q8.4 – Berufssuchprofile für breite Anforderungen

**Frage:** Sollen breite Kundenanforderungen über wiederverwendbare,
kontrollierte Berufssuchprofile auf mehrere Ausbildungsberufe abgebildet werden?

**Antwort:** `BESTÄTIGT` – Breite Anforderungen werden über kontrollierte,
wiederverwendbare Berufssuchprofile abgebildet. Diese grundsätzliche Zustimmung
bleibt bestehen.

**Geltender Architekturstand gemäß ADR-0003:** Profile unterscheiden
Ausbildungsberufe, Erfahrungsberufe und Tätigkeitsarten, sind versioniert und
nicht exklusiv. Automatische oder KI-gestützte neue Zuordnungen bleiben
Vorschläge und veröffentlichen sich nicht selbst. Die historische Zustimmung
zu jeder einzelnen Fähigkeit ist damit nicht unabhängig rekonstruiert.

**VORLÄUFIGER VORSCHLAG / Rekonstruktionslücke:** Originaltexte erhalten,
Erfahrungsfreitext vorab auf kontrollierte Berufs- und Tätigkeits-IDs
normalisieren und nicht bei jeder Suche neu interpretieren. Auch die
Nichtzählung unaufgelöster Werte als relevante Erfahrung bleibt Teil der
offenen Q8.5. Vorschau und allgemeine Suchbestätigung haben den unter Q8
beschriebenen Vorschlagsstatus.

**DURCH DISCOVERY ZU PRÜFEN:** Ob kontrollierte CRM-IDs und entsprechende
Erfahrungsfreitexte vorhanden sind und wie sie strukturiert sind. Vorhandene
geeignete IDs zu verwenden ist ein Vorschlag, keine bestätigte Bestandsaussage.

### Q8.4.2 – Erstellung und Pflege von Berufssuchprofilen

**Frage:** Wie sollen benannte Profile wie „Tiefbauer“ erstellt, gepflegt und
für direkte Suchen verwendet werden?

**Antwort:** `BESTÄTIGT` – Ein Profil darf kontrollierte
Ausbildungsberufe, Erfahrungsberufe und Tätigkeitsarten referenzieren, ohne
diese
Elemente zu besitzen oder für andere Verwendungen zu sperren. Derselbe Beruf
darf gleichzeitig mehreren Profilen zugeordnet und weiterhin direkt gesucht
werden. Die Beziehungen sind damit nicht exklusiv und viele-zu-viele.

Die Verwaltung erfolgt nach Discovery und Freigabe des Datenmodells über einen
getrennten Profilverwaltungs-MCP. Er verwaltet Entwürfe, teilautomatische
Vorschläge, manuelle Zuordnungen und Korrekturen, Diff, Validierung,
Veröffentlichungsbestätigung, unveränderliche Versionen, Archivierung und Audit.
Der Runtime-Such-MCP liest nur veröffentlichte Profilversionen und besitzt keine
Profil-Schreibrechte. Verbindliche Details stehen in
<!-- markdownlint-disable-next-line MD013 -->
[ADR-0003](0003-separated-profile-administration-mcp.md); die fachliche Grundlage
enthält der [Recherchebericht](../research/berufssuchprofile-q8-4-2.md).

### Q8.5 – Bedeutung von Berufserfahrung

**Frage:** Soll eine Anforderung an Berufserfahrung die gesamte bisherige
Berufserfahrung eines Kandidaten oder nur fachlich passende Beschäftigungszeiten
berücksichtigen?

**Status:** `OFFEN` – vollständig. Der bisherige Status `TEILWEISE BESTÄTIGT`
wurde mit ausdrücklicher Nutzerfreigabe vom 2026-09-11 korrigiert. Weder die
Auswahl relevanter Beschäftigungszeiten noch ihre Berechnung gilt als bestätigte
Nutzerentscheidung. Die Fortsetzung erfolgt gemäß Q9 nach Discovery.

**VORLÄUFIGER VORSCHLAG:** Nur fachlich passende Berufsgruppen oder Tätigkeiten
zählen; beispielsweise Verkaufserfahrung nicht als Elektrikererfahrung werten.
Die Kombination aus Beruf und Tätigkeit, überlappende Intervalle und fehlende
Zeitangaben bleiben zu entscheiden. Der Vorschlag schließt keinen Teil von
Q8.5 vorweg.

**ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN:** Erfahrungsbezeichnungen könnten
als mehrsprachige Freitexte mit unterschiedlichen Schreibweisen vorliegen.
Ein Originalbeleg und technische Verifikation fehlen. Die unter Q8.4
vorgeschlagene Vorabnormalisierung ist keine bestätigte Antwort auf Q8.5.

### Q9 – Reihenfolge von Interview und Datenbank-Discovery

**Frage:** Sollen zuerst alle verbleibenden Fragen beantwortet werden, soll
sofort die Datenbank untersucht werden oder sollen nur die
Discovery-Sicherheitsvoraussetzungen geklärt und danach die technischen Fragen
durch einen read-only Audit präzisiert werden?

**Antwort:** `BESTÄTIGT` – Option C. Zuerst werden Auditfreigabe,
Least-Privilege-Read-only-Identität, Query-Allowlist, sicherer Ausgabeort,
Zeitfenster, Timeout und Stopkriterien bestätigt. Danach werden alle Tabellen
über Metadaten inventarisiert, die fachlich relevanten Tabellen ausgewählt und
nur dort tiefere aggregierte Qualitätsprüfungen durchgeführt. Anschließend
werden beantwortete Technikfragen geschlossen und die verbleibenden
Geschäftsentscheidungen mit den tatsächlichen Befunden fortgesetzt.

**Vom Nutzer angegebene Ausgangslage:** Die Datenbank enthält 179 Tabellen.
Diese Zahl ist noch durch das Metadateninventar zu verifizieren.

**Vom Nutzer am 2026-09-11 ergänzte Ausgangslage:** Die vorhandenen Daten seien
im Supabase-Projekt im Wesentlichen nur hochgeladen worden; die Datenbank sei
noch nicht auf das Zielvorhaben ausgerichtet, korrekt eingerichtet oder mit den
benötigten Zugriffspfaden verdrahtet. Diese Beschreibung ist
`DURCH DISCOVERY ZU PRÜFEN`. Insbesondere sind Beziehungen, Constraints,
RLS-Aktivierung und -Wirksamkeit, Grants und Rollen, Indizes, API-Grenzen,
Authentifizierung, Tenant-Isolation und operative Datenflüsse nicht als
funktionsfähig bestätigt.

## Offene Fragen

### Q4.5 – Vom Nutzer als offen markiert

**Status:** `OFFEN`

Die genaue Frage und ihre Entscheidungsoptionen sind noch nicht dokumentiert.
Bis zur Präzisierung wird keine Antwort abgeleitet.

### Q8 – Noch offene Unterfragen

**Status:** `OFFEN`

- Q8.5 insgesamt: gesamte oder fachlich passende Berufserfahrung?
- Wann gilt eine Beschäftigungszeit als relevant: über den Beruf, die Tätigkeit
  oder eine kontrollierte Kombination aus beiden?
- Wie werden überlappende Beschäftigungszeiten bei der Berechnung relevanter
  Erfahrungsmonate behandelt?

### Weitere offene Entscheidungen

**Status:** `OFFEN`

- Genaue erlaubte Filterlockerungen und deren Bestätigungsablauf.
- Suchverlauf, gespeicherte Suchen, Audit-Protokoll und Ergebnis-Snapshots.
- Zugriffsrechte auf Suchverläufe.
- Darstellung in MCP-Clients und einer möglichen eigenen Oberfläche.
- Exportumfang, Formate, Felder, Limits und Schutzmaßnahmen.
- Zulässige Cache-Dauer und erforderliche Datenaktualität.
- Authentifizierung, Tenant-Modell, Hosting, Ranking und numerische SLOs.

### Q10 – Datenbank-Zielzustand und Übergang

**Status:** `TEILWEISE BESTÄTIGT`

**Q10.1 – Herkunft und maßgebliche Datenquelle:** `BESTÄTIGT` – Die
Datenbank wurde aus dem bestehenden CRM gedumpt und anschließend in Supabase
geladen. Das ursprüngliche CRM wird nicht weiter betrieben und erhält keine
neuen oder geänderten Kandidatendaten. Supabase ist nicht die einzige Kopie;
als weitere Sicherungs- oder Referenzstände nennt der Nutzer einen lokalen
SQL-Dump, einen Container in OrbStack und ein ZIP-Backup. Diese Artefakte wurden
nicht geöffnet, ausgeführt, entpackt oder inhaltlich geprüft. Noch `OFFEN` sind
Zeitpunkt, Vollständigkeit, Gleichstand und vorgesehene Rolle der drei Stände
sowie die Entscheidung, welcher Datenbestand als maßgebliche Ausgangsbasis
dient. Ihre Existenz belegt ohne Prüfung weder Wiederherstellbarkeit noch
Gleichstand mit dem Supabase-Datenbestand. Alle drei Stände sind als sensible
Rohartefakte außerhalb von Git zu behandeln; Inhalte oder personenbezogene
Daten dürfen nicht in Chat, Logs oder Repository-Ausgaben gelangen.

**Q10.1d – Lokaler Preflight der Sicherungsstände:** `ABGELEHNT` – Der Nutzer
möchte derzeit keine lokale read-only Bestandsprüfung von SQL-Dump,
OrbStack-Container oder ZIP-Backup durchführen. Die drei Stände bleiben daher
unverifiziert und dürfen vorerst weder als Beleg für Vollständigkeit und
Gleichstand noch als nachgewiesener Restore verwendet werden. Ein späterer
Restore-Nachweis gemäß Q10.2a benötigt einen anderen, separat freizugebenden
Prüfweg.

**Q10.1e – Vorläufige Ausgangsbasis:** `BESTÄTIGT` – Die aktuelle
Supabase-Datenbank ist trotz der ungeprüften Sicherungsstände die vorläufige
Arbeitsbasis für read-only Discovery und weitere Planung. Diese Entscheidung
bestätigt weder Vollständigkeit noch fachliche oder technische Eignung des
Datenbestands. Die anderen Kopien bleiben unangetastet; vor der ersten Mutation
ist weiterhin der separat geprüfte Restore-Nachweis gemäß Q10.2a erforderlich.

**Q10.2 – Getrennte Development-/Staging-Umgebung:** `BESTÄTIGT` – Der Nutzer
möchte kein separates Development-/Staging-Projekt bereitstellen. Planung,
Prüfung und eine später separat freizugebende Umsetzung sollen direkt am
bestehenden Produktionsprojekt erfolgen; als Begründung nennt der Nutzer
vorhandene Backups.

Diese Entscheidung hebt die bestehenden Sicherheitsgates nicht auf. Bis zur
separaten Freigabe einer konkreten Mutation bleiben ausschließlich die
dokumentierten read-only Discovery-Schritte zulässig. Vor einem späteren
In-place-Umbau sind Backup-Umfang, Wiederherstellbarkeit, zulässiges
Zeitfenster,
Transaktions- und Rollback-Strategie sowie Stopkriterien noch `OFFEN`.

**Q10.2a – Sicherheitsstandard für direkte Produktionsänderungen:**
`BESTÄTIGT` – Für jede spätere Änderungsstufe gilt die Reihenfolge read-only
Audit, konkreter Migrationsplan, nachgewiesener Restore, Dry-run beziehungsweise
Preflight, separate Freigabe, kleine kontrollierte Änderung, Prüfung und erst
danach der nächste Schritt. Die Zustimmung zu diesem Ablauf ist keine
Freigabe eines Datenbankzugriffs oder einer konkreten Mutation.

**Q10.2b – Dedizierter Discovery-Zugang:** `BESTÄTIGT` – Am 2026-09-11 wurde
gefragt: „Gibt es bereits eine eigens angelegte PostgreSQL-Read-only-Rolle für
diesen Discovery-Zugriff?“ Der Nutzer antwortete: „nein richte einen ein“.
Normalisierte Antwort: Eine solche Rolle besteht laut Nutzer nicht; ihre
Einrichtung ist beauftragt. Der Bootstrap-Zweig „neue Rolle“ ist damit gewählt.
Eine erneute Grundsatzbestätigung der Rollenanlage ist nicht erforderlich.

Die konkrete Ausführung ist noch nicht erfolgt. Restore-Nachweis,
zulässiger synthetischer Laufzeitnachweis und gebundener Produktionspreflight
fehlen weiterhin. Die Antwort bestätigt diese Nachweise nicht und ändert
weder Q10.2a noch die ausgeschlossenen Backup-Prüfungen oder das Verbot des
Produktionszugriffs über den Supabase-Developer-Plugin. Diese Voraussetzungen
bleiben getrennt von dem erteilten Einrichtungsauftrag offen.

**Q10.2c – Backup-Rhythmus und Restore-Test:** `BESTÄTIGT ALS NUTZERANGABE` –
Am 2026-09-11 wurde gefragt, ob bereits ein Backup dieser Supabase-Datenbank
erfolgreich wiederhergestellt wurde. Der Nutzer antwortete: „nein aber es gibt
jeden tag ein backup“. Normalisierte Antwort: Es bestehen laut Nutzer tägliche
Backups; ein erfolgreicher Wiederherstellungstest liegt nicht vor. Backupstatus,
Umfang und Wiederherstellbarkeit wurden nicht technisch geprüft. Diese Angabe
ersetzt keinen Restore-Nachweis und ist keine Ausnahme von Q10.2a.

**Q10.2d – Begrenzte Restore-Ausnahme für die Leserolle:** `BESTÄTIGT` –
Am 2026-09-11 wurde vorgeschlagen: „Rollenanlage nach bestandenen
Sicherheitsprüfungen; Wiederherstellungstest weiterhin vor Änderungen an
Tabellen oder Daten.“ Auf die Frage, ob diese Ausnahme von der bisherigen
Regel festgehalten und damit fortgefahren werden darf, antwortete der Nutzer
„ja“.

Normalisierte Entscheidung: Für die beauftragte Anlage der dedizierten Rolle
`dino_crm_discovery_ro_v1` entfällt der vorherige Restore-Test. Diese enge
Ausnahme ersetzt insoweit Q10.2a und die älteren Voraussetzungen in Q10.2b/c.
Sie akzeptiert für diesen Schritt das verbleibende Risiko ungeprüfter
Wiederherstellbarkeit der laut Nutzer täglich erstellten Backups. Vor Änderungen
an Tabellen oder Daten bleibt ein erfolgreicher Restore-Nachweis erforderlich.

Ziel-/Identitätsbindung, Prüfung effektiver Rechte, synthetischer
SQL-Laufzeitnachweis, begrenzte Ausführung und Post-Check bleiben erforderlich.
Die Ausnahme erlaubt weder globale PUBLIC-Rechteänderungen noch Zugriff über
den Supabase-Developer-Plugin, Öffnen abgelehnter Backup-Artefakte oder spätere
Discovery-Gates. Neue Testumgebungen und globale Installationen sind damit
nicht automatisch freigegeben. Die Rolle ist noch nicht angelegt.

**Q10.2e – Isolierter synthetischer Rollentest:** `BESTÄTIGT` – Am 2026-09-11
wurde gefragt, ob ein neuer temporärer PostgreSQL-17-Container aus dem bereits
vorhandenen Image ohne Netzwerk, eingebundene Dateien oder echte Daten für den
Rollentest gestartet und anschließend entfernt werden darf. Der Nutzer
antwortete: „Ja, isolierten Testcontainer erlauben“.
Dies erweitert ausschließlich die bisherige Testgrenze „bereits vorhandene
Umgebung“. Backup-Importe, gehostetes Staging und globale Installationen bleiben
ausgeschlossen. Die Entfernung betrifft nur den eigens erzeugten Testcontainer.

**Q10.2f – Sichtbarer Projektabgleich:** `BESTÄTIGT` – Der Nutzer wurde gebeten,
die Übersicht des richtigen CRM-Projekts in Chrome zu öffnen. Zunächst war
„JSI AI“ sichtbar; dessen Kennung passte nicht zur gespeicherten Verbindung.
Nach dem Hinweis antwortete der Nutzer: „jetzt ist es die richitge ich habs
geändert“. Die anschließende Übersicht zeigte „JSI Base“. Ihre sichtbare
Projektkennung stimmt nach unabhängigem Hashvergleich exakt mit dem vollständigen
gespeicherten Pooler-Benutzernamen überein. Die reine Zielauswahl autorisiert
keine Änderungen an bestehenden PUBLIC- oder Funktionsrechten.

**Q10.2g – Gezielte Prüfung öffentlich erreichbarer Definer-Funktionen:**
`BESTÄTIGT` – Auf die Frage, ob genau die bestehenden öffentlich erreichbaren
SECURITY-DEFINER-Funktionen und ihre Berechtigungen lesend untersucht werden
dürfen, ohne sie auszuführen oder Kandidatendaten zu lesen, antwortete der Nutzer
„ja“. Der in der Produktions-Preflight-Dokumentation beschriebene Prüfbereich
ist damit freigegeben: Identität/Signatur, Eigentümer, ACL, Sprache und Definition
nur der betroffenen Funktionen im bereits bestätigten Projekt „JSI Base“.
Rohe Definitionen und enthaltene Werte bleiben ausschließlich in begrenzter
lokaler Verarbeitung; an Modell, Chat und Git gehen nur redigierte Befunde.
Unsichere oder unvollständige Verarbeitung ist STOP. Die Freigabe umfasst
keine Funktionsausführung, Kandidatenabfrage, Rechteänderung oder Aufweichung
des Rollen-Gates.

**Q10.3 – Kurzfristig Option A, schrittweise zu Option D:** `BESTÄTIGT` – Die
importierten CRM-Tabellen bleiben in der kurzfristigen Phase unverändert. Für
Release 1 werden nur die benötigten kontrollierten Strukturen, Beziehungen und
Suchzugriffe additiv ergänzt. Diese Erweiterungen sind keine Wegwerflösung,
sondern kompatible erste Bausteine des späteren kanonischen Zielmodells.

Der Übergang zu Option D erfolgt anschließend in kleinen, separat geprüften und
freigegebenen Migrationsschnitten. Jeder Schnitt benötigt Quellen-Mapping,
Data-Lineage, Abgleich von IDs, Mengen und fachlichen Ergebnissen, RLS- und
Vertragstests sowie einen nachgewiesenen Rückweg. Die bisherige Quelle wird
nicht
im selben Schritt destruktiv entfernt. Erst nach vollständiger Abnahme darf sie
separat archiviert und in einer späteren Freigabe zur Löschung vorgeschlagen
werden.

Da das ursprüngliche CRM nicht weiter betrieben wird, ist keine dauerhafte
Synchronisierung mit diesem Altsystem vorgesehen. Ob andere aktive Schreiber auf
den Supabase-Datenbestand zugreifen, bleibt `DURCH DISCOVERY ZU PRÜFEN`.
Der read-only Audit bestimmt die physischen Strukturen, Mappings und sicheren
Schnittgrenzen; er ändert nicht mehr die bestätigte Grundrichtung A nach D.

## Fortschreibung während des Interviews

Vor jeder neuen Interviewrunde wird dieses Dokument gelesen. Nach jeder
ausdrücklichen Nutzerantwort wird die betreffende Frage im selben Arbeitsgang
aktualisiert. Dabei gelten folgende Regeln:

1. Frage und normalisierte Antwort werden gemeinsam gespeichert.
2. Aus Nachfragen oder Erläuterungswünschen wird keine Entscheidung abgeleitet.
3. Teilentscheidungen werden von offenen Folgefragen getrennt.
4. Die neueste ausdrückliche Nutzerentscheidung ersetzt ältere Antworten.
5. Empfehlungen bleiben als offen markiert, bis der Nutzer sie bestätigt.
6. Der Status dieses Dokuments bleibt bis zur Abschlussbestätigung `Entwurf`.

## Abschluss des Interviews

Wenn der Nutzer das gemeinsame Verständnis ausdrücklich bestätigt und keine
Frage mehr offen ist, wird der Stand bereinigt:

1. Dauerhafte, schwer umkehrbare Entscheidungen werden in akzeptierte ADRs
   überführt oder dieser ADR wird entsprechend aufgeteilt und akzeptiert.
2. Ausschließlich aufgelöste Domänenbegriffe werden in `CONTEXT.md` gepflegt.
3. Anforderungen, Schemas, Fehlerfälle und Abnahmekriterien werden in den
   Implementierungsbrief übernommen.
4. Der Projektstatus und die nächste Phase werden in `docs/project.md`
   aktualisiert.
5. Erst die fertige Spezifikation wird in abhängige Linear-Tickets zerlegt.
6. Markdown-Struktur, relative Links, `git diff --check` und
   `git status --short` werden geprüft; fehlendes Markdown-Linting wird als Gap
   gemeldet.
