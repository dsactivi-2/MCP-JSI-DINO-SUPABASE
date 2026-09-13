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
bleiben Q8.4 grundsätzlich bestätigt, Q8.5 teilweise (nur passende Jobs) und
die allgemeine
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

**Frühere Antwort:** `ERSETZT` – 2026-09-11. Nein. Kein Kontaktausgang in
Release 1, auch nicht im Profil; CONTACT-02 später.

**Antwort:** `BESTÄTIGT` – 2026-09-12. Der Kandidat bewirbt sich und gibt alle
Daten ein. Das gilt im gesamten Produkt, nicht nur in einer späteren Phase.

Interne Vermittler-Rollen **Entwickler, Sachbearbeiter, Teamleiter und
Inhaber** sehen von Anfang an **alle Kandidaten** der Kartei und **alle ihre
Daten**, einschließlich E-Mail, Telefon und übriger Kontakte.

Der **Kunde** sieht nie den ganzen Pool. Die Freigabe an ihn hat zwei Schritte:

1. **Vorschlagsfreigabe:** Nach unterschriebenem Vertrag und konkretisierter
   Nachfrage (zum Beispiel zehn Elektriker) schlägt der Vermittler Kandidaten
   vor. Der Kunde sieht deren Daten **ohne** E-Mail, Telefon und andere
   Kontakte.
2. **Einstellungsfreigabe:** Nach Zusage beziehungsweise Einstellung eines
   vorgeschlagenen Kandidaten erhält der Kunde auch die Kontaktdaten **dieses**
   Kandidaten.

CONTACT-02 ist die Einstellungsfreigabe der Kontakte an den Kunden, nicht eine
spätere interne Kontaktphase. Das Entwickler-Plugin an Produktion oder
Restore-Klon bleibt verboten; Produktsicht ist nicht Plugin-Zugang. Export
in R1 ja neben Blättern; Format und Limit Q15.6 `OFFEN`.

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
| Berufserfahrung | `BESTÄTIGT` Kernregel Q8.5.3–8. Listen zuerst, KI nur Vorschlag. |
| Ausschlüsse | `VORLÄUFIGER VORSCHLAG`: ausdrücklich gesetzte Ausschlüsse als `NOT`. |
| Fehlende Werte | `VORLÄUFIGER VORSCHLAG`: kein positiver Pflichtfiltertreffer; das geltende Verbot erfundener Werte bleibt bestehen. |
| Nicht genannte Filter | `BESTÄTIGT`: inaktiv, keine Einschränkung der Suche. |

<!-- markdownlint-enable MD013 -->

**BESTÄTIGT** – 2026-09-13. Vor jeder neuen oder geänderten Suche werden die
aktiven Filter angezeigt. Nach ausdrücklicher Bestätigung folgt genau eine
Datenbanksuche. Q7 bleibt: bei null Treffern erst lockern nach Zustimmung.

**VORLÄUFIGER VORSCHLAG:** Anzeige aufgelöster Profilmitglieder in der
Vorschau. R1 hat kein Berufssuchprofil in der Suche. Ob Pflicht- und
Wunschkriterien zur ersten Regelversion gehören, bleibt `OFFEN`.

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

**Status:** `TEILWEISE BESTÄTIGT`

**Q8.5.3 – Welche Jahre zählen:** `BESTÄTIGT` – 2026-09-13. Option A. Nur Jobs,
die zum gesuchten Beruf passen. Gesamte Lebensarbeitszeit zählt nicht.
Quelle ist die von–bis-Liste, nicht Zettel 2.

**Q8.5.4 – Überlappung:** `BESTÄTIGT` – 2026-09-13. Zeiten nicht addieren.
Überlappende Jobs in demselben Beruf zählen in der Kalenderzeit einmal, nicht
als Summe der Verträge.

**Q8.5.5 – Aktueller Job ohne Enddatum:** `BESTÄTIGT` – 2026-09-13. Option A.
Bis heute zählen.

**Q8.5.6 – Passung des Jobtitels:** `BESTÄTIGT` – 2026-09-13. Option B. Nicht
nur taxonomisch gemappte Jobs. Auch ähnliche Schreibweisen ohne Zuordnung.
Die occupation-Map ist hilfreich, aber keine Pflicht.

**Q8.5.7 – Was „ähnlich“ heißt:** `BESTÄTIGT` – 2026-09-13. A und B. Schreibweise/
Tippfehler **und** andere Wörter (z. B. Monter ≈ Elektriker). Das ist die
Berufspassung für Erfahrungsjahre, nicht der Extra-Knopf „ähnlich wie dieser
Kandidat“.

**Q8.5.8 – Quelle der Verwandtschaft:** `BESTÄTIGT` – 2026-09-13. Option C.
Zuerst kontrollierte Listen (Aliasse, Berufssuchprofil). KI nur Vorschlag, der
bestätigt werden muss, bevor er zählt. Keine frei erfundenen Synonyme in der
live Suche. Passt zu ADR-0003 (Vorschläge nicht selbst publizieren).

**Q8.5.9 – Jahresfilter in R1:** `BESTÄTIGT` – 2026-09-13. Nutzer: R1 soll
„mindestens X Jahre in diesem Job“ können. Quelle sind von–bis-Daten der
Lebenslauf-Liste `idk_kandidat_radno_iskustvo`, nicht die Aktenzahlen.
Es zählen der genannte Job und ähnliche Jobs derselben Jobgruppe
(Berufssuchprofil / kontrollierte Liste, Q8.5.3–8). Überlappungen nicht
addieren; laufender Job bis heute. Ohne genannten Job ist das Jahresfeld
ungültig. `has_work_experience` (ja/nein) bleibt daneben die alte Maske.
Exakte von/bis-Spaltennamen: `DURCH DISCOVERY ZU PRÜFEN`.
Die ältere Wizard-03-Zeile „5 Jahre nicht in R1“ ist durch diese Antwort
ersetzt.

Die frühere Vorschlagszeile zu relevanter Erfahrung ist durch Q8.5.3–8 ersetzt.

**ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN:** Erfahrungsbezeichnungen könnten
als mehrsprachige Freitexte mit unterschiedlichen Schreibweisen vorliegen.
Ein Originalbeleg und technische Verifikation fehlen. Die unter Q8.4
vorgeschlagene Vorabnormalisierung ist keine bestätigte Antwort auf Q8.5.

**Q8.5.1 – Eine Berufserfahrung:** `BESTÄTIGT` – 2026-09-12. Wenn beide
Speicherorte Berufserfahrung meinen, müssen die Zahlen identisch sein. Sind
sie es nicht, ist das Aktenfeld etwas anderes oder ein Datenfehler. Ob sie
identisch sind, ist nicht gemessen (keine Zeilen gelesen).

Katalog: Lebenslauf-Liste = `idk_kandidat_radno_iskustvo` (eine Zeile je Job).
Kandidatenakte = `idk_kandidati` (eine Zeile je Person), plus zwei Zahlenfelder
`kandidat_iskustvo_u_struci` und `kandidat_iskustvo_u_struci_trajanje`.
Gesamt-versus-relevante Jahre bleiben OPEN.

**Klarstellung Personalakte:** Der Nutzer kennt Kategorie Berufserfahrung als
mehrere Berufe je mit von–bis. Das ist die Lebenslauf-Liste
(`idk_kandidat_radno_iskustvo`), nicht die zwei Zahlenfelder auf der
Kandidatenzeile. Ob diese Zahlen irgendwo in der Oberfläche als Erfahrung
gezeigt werden, ist ungeprüft.

**Klarstellung Filter vs. Zettel 2:** Die Suchanfrage (z. B. Elektriker,
mindestens 3 Jahre) ist der Filter, nicht Zettel 2. Zettel 2 bleibt nur die
zwei Zahlenfelder auf der Kandidatenzeile. Der Filter wird mit der
Lebenslauf-Liste verglichen, nicht mit der Anfrage selbst verwechselt.

**Q8.5.2 – Bedeutung der Aktenzahlen:** `IGNORIERT` – 2026-09-13. Nutzer:
vorerst ignorieren, Interpretation nicht akzeptiert. `BELEGT` lokal
(MySQL-Kommentar und
Registrierungsformular, nicht Production-SELECT). `kandidat_iskustvo_u_struci`:
null unbekannt, 0 nein, 1 ja. `kandidat_iskustvo_u_struci_trajanje` nur wenn 1:
0 keines in 5 Jahren, 1 weniger als 1 Jahr, 2=1 Jahr … 6=5 Jahre. Das ist
Selbstangabe bei der Bewerbung, nicht die von–bis-Liste.

Lokal 2026-09-13 (OrbStack MySQL, nur COUNT): 122004 Zeilen. Davon 100563 beide
NULL, 8303 nein, Rest ja mit Dauer-Codes. Keine Personendaten gelesen.

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

### Q4.5 – Leere Nummer stillgelegt

**Status:** `BESTÄTIGT`

Die genaue ursprüngliche Frage und ihre Entscheidungsoptionen sind nicht
überliefert. Es wurde kein Fachtext erfunden.

**Antwort:** `BESTÄTIGT` – Option B. Die leere Nummer Q4.5 wird stillgelegt.
Sie ist kein Interview- oder Release-1-Blocker. Eine neue nummerierte Frage
wird nur eröffnet, wenn eine echte verbleibende Kontakt- oder
Datenschutzentscheidung vorliegt. Die unbekannte ursprüngliche Fachfrage gilt
nicht als beantwortet.

### Q8 – Noch offene Unterfragen

**Status:** `TEILWEISE BESTÄTIGT`

Live-Stand in Q8.5: 8.5.1 und 8.5.3–8 `BESTÄTIGT`; 8.5.2 `IGNORIERT`;
8.5.9 `BESTÄTIGT`: R1-Jahresfilter aus von–bis, Job + Jobgruppe.
Überlappung und Enddatum ohne Ende sind beantwortet.

Noch offen unter Q8:

- Exakte von/bis-Spaltennamen in `idk_kandidat_radno_iskustvo`.
- Welche physische Jobgruppe (Berufssuchprofil-Tabelle) die Ähnlichkeit liefert.
- Welches JSON-Feld der „genannte Job“ für `min_relevant_experience_years`
  ist (`struke` ist Ausbildungsberuf, nicht die Lebenslauf-Zeile).

### Weitere offene Entscheidungen

**Status:** `OFFEN`

- Genaue erlaubte Filterlockerungen und deren Bestätigungsablauf.
- Suchverlauf, gespeicherte Suchen, Audit-Protokoll und Ergebnis-Snapshots.
- Zugriffsrechte auf Suchverläufe.
- Darstellung in MCP-Clients und einer möglichen eigenen Oberfläche.
- Schutzmaßnahmen für den Recruiter-Export (Datei verlässt den Chat).
  Umfang Q15.6: Blättern und CSV/Excel, max. 500, inkl. JMBG/Kontakt;
  ganzer Bestand ohne Filter nicht bestätigt.
- Zulässige Cache-Dauer und erforderliche Datenaktualität.
  Nutzer 2026-09-13: kein Redis/Iris in R1. Treffer-Cache speichert keine
  Bewerberakten. Jobnamen-Katalog später im Worker-RAM, nach RPC, nur wenn
  gemessen langsam. Nicht jetzt einführen.
- Tenant-Modell, Hosting (Cloudflare möglich, nicht gewählt), SDK-Version
  und numerische SLOs. Ein Such-MCP mit Tokens je Rolle ist bestätigt (Q11).
  Ranking R1 ist bestätigt: `kandidat_id` absteigend.

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

**Nachtrag Restore-Testlösung:** Der Nutzer hat B und C ausdrücklich nicht
freigegeben. Als Testlösung für A lässt er ein Backup in ein neues
Supabase-Projekt wiederherstellen, ohne das echte Projekt zu überschreiben.
Das entspricht der dokumentierten Funktion Restore to a new project (Beta).

**Q10.2c1 – Restore-Nachweis durch Clone:** `BESTÄTIGT`

**Antwort:** `BESTÄTIGT` – Der Nutzer setzt den erfolgreichen Restore in ein
neues Projekt (Postgres nach PITR wieder oben, Health 200) mit dem Nachweis
gleich, das echte Projekt wiederherstellen zu können. Ein getrennter
In-place-Restore der Produktion und ein Mengen-/Tabellen-/Rollenabgleich sind
für diesen Gate **nicht** zusätzlich verlangt. Die Logs vom 2026-09-11 zeigen
Backup-Recovery, WAL-Redo, vorübergehend `57P03` während der Recovery, danach
wiederholte Health-/Ready-200. Kein Passwortfehler.

Technische Lücke, kein Blocker: kein vollständiger Datenabgleich. Die Kopie
enthält echte Kandidatendaten; der Developer-Plugin bleibt dafür verboten.

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

**Q10.2h – Erweiterter, ausschließlich lesender Funktionsprüfumfang:**
`BESTÄTIGT` – Der Nutzer antwortete am 2026-09-11 ausdrücklich „ja“ auf:
„Darf ich auch diese Wege ausschließlich lesend prüfen: die zwei Funktionen,
indirekte Aufrufe und bestimmte PostgreSQL-Hilfsrechte?“ Zusätzlich beauftragte
er: „dokumentiere das \"v\" und ziehe die docs nach“. Der besprochene V3-Versuch
und seine Rücknahme werden als Versionsstand dokumentiert; daraus folgt keine
Freigabe der verworfenen Lockerung.

Genehmigt ist der Zusatzumfang aus dem
[PUBLIC-Prüfbericht](../reviews/2026-09-11-public-definer-audit.md): die zwei
PUBLIC-EXECUTE-Definer-Funktionen auch ohne PUBLIC schema USAGE, ihre
Katalogabhängigkeiten und relevanten indirekten View-/Routinenrechte sowie die
dort aufgezählten PostgreSQL-Large-Object-Funktionsrechte. Verarbeitung erfolgt
über den geprüften lokalen psql-Weg mit begrenzter, redigierter Ausgabe.
Keine Funktions- oder Viewausführung, Kandidaten- oder Large-Object-Inhalte,
Dateiinhalte, DB-Mutation, Rechteänderung oder Lockerung der Rollen-Gates.
Rohe Definitionen, Identitäten und Literale bleiben außerhalb von Modell,
Chat und Git. Diese Freigabe muss nicht erneut eingeholt werden; offene
Prüfergebnisse bleiben als solche dokumentiert.

**Q10.2i – Konkreten, getesteten Rechteplan vorbereiten:** `BESTÄTIGT` – Auf
den beschriebenen nächsten Schritt antwortete der Nutzer „mach das“:
bestehende betroffene Konten und Rechte prüfen, einen getesteten Entwurf
vorbereiten, bestehende Zugriffe erhalten und die bekannten Schreibrechte vom
neuen Prüfzugang fernhalten. Der fertige Entwurf wird zur Freigabe vorgelegt.
Die Zustimmung umfasst die dafür erforderliche begrenzte read-only Prüfung
von Rollen, Objekt-/Grantrechten und den bekannten Zielen sowie lokale
SQL-Entwürfe und bereits erlaubte isolierte Tests. Sie autorisiert noch keine
Produktionsmutation oder Änderung bestehender PUBLIC-Rechte. Ein erhaltender
Entwurf darf bestehende effektive Zugriffe bewahren, aber keine unbestätigte
fachliche Notwendigkeit einzelner Rechte behaupten.

**Q10.2j – Freigabe des beschriebenen Rechteplans:** `BESTÄTIGT` – Nach
Erklärung der acht LO-Funktionen und der fehlenden Verwaltungsrechte antwortet
der Nutzer: „ja es ist mögloch und ich gebe die freigeb dazu“. Die Zustimmung
gilt für die beschriebene gezielte Rechteänderung unter Erhalt bestehender
Zugriffe. Dafür ist keine erneute pauschale Zustimmung anzufordern.
Die Aussage, dass ein berechtigter Weg möglich ist, ist als Nutzeraussage
bestätigt; ein konkreter zusätzlicher Zugang oder eine tatsächlich geänderte
Datenbankberechtigung ist damit noch nicht technisch nachgewiesen.
Die vorhandenen Identitäts-, Rechte- und Transaktionsprüfungen bleiben bestehen.
Keine Erweiterung auf andere Objekte, Datenänderungen oder unbenannte Zugänge.

**Q10.2k – Zugangskonzept trotz fehlender LO-ACL-Rechte:** `BESTÄTIGT`

**Frage:** Soll die beauftragte Rolle trotzdem angelegt werden, ohne die acht
PUBLIC-REVOKEs der Large-Object-Hilfsfunktionen?

**Antwort:** `BESTÄTIGT` – Option A. Die acht PUBLIC-REVOKEs entfallen für
diesen Schritt. Q10.2b bleibt: die dedizierte Discovery-Rolle wird angelegt.
Ein zusätzlicher Administratorbenutzer ist nicht der nächste Schritt und ändert
diese ACL nicht. Eine spätere Härtung genau dieser acht Ziele ist ein eigener,
separat freizugebender Arbeitspfad.

PostgreSQL kennt kein per-Rolle-`DENY`. Solange PUBLIC EXECUTE auf diesen acht
Funktionen bleibt, erbt auch die neue Rolle dieses Privileg. Die frühere
Formulierung, Gate B1 könne fehlendes EXECUTE beweisen, ist deshalb nicht
haltbar; das Rest-Risiko bleibt eine eigene Folgefrage. Q10.2k hebt Q10.2j nicht
auf und verwandelt den Rechteplan nicht stillschweigend in ein reduziertes
Ausführungspaket für TEMP oder die zwei Definer-Funktionen.

Keine Freigabe für B1/B2/B3, Funktionsausführung, Kandidatenabfragen,
pauschale PUBLIC-REVOKEs oder die konkrete Mutationsausführung.

**Q10.2l – PUBLIC-Reste vor der Rollenanlage:** `BESTÄTIGT`

**Frage:** Welche PUBLIC-Rechte darf die neue Discovery-Rolle bei der Anlage
noch erben? Zuerst härten, was der aktuelle Zugang ändern kann (`TEMPORARY`
und die zwei SECURITY-DEFINER-Funktionen), Rolle sofort mit allen heutigen
PUBLIC-Resten, oder warten bis auch die acht LO-REVOKEs möglich sind?

**Antwort:** `BESTÄTIGT` – Option A. Zuerst erhalten die bestehenden Rollen
Direktgrants für Datenbank-`TEMPORARY` und EXECUTE auf den zwei
Definer-Funktionen; danach entzieht PUBLIC genau diese drei Rechte. Erst dann
wird die Discovery-Rolle angelegt. Als PUBLIC-Rest bleiben ausschließlich die
acht LO-EXECUTE-Privilegien, die der aktuelle Zugang nicht ändern kann.

Q10.2k bleibt: die acht LO-REVOKEs sind nicht Teil dieses Schnitts. Q10.2j
gilt nicht automatisch für dieses verkleinerte Paket. Q10.2d (Restore-Ausnahme)
gilt nur für die Rollenanlage, nicht für diese ACL-Änderung. Q10.2a bleibt für
diesen Schnitt: frisches Inventar, gebundenes SQL, Dry-run/Preflight, eigene
Mutationsfreigabe. Keine Ausführung, kein B1/B2/B3, keine Funktionsausführung
und keine Kandidatenabfrage.

**Q10.2m – Apply-Freigabe für den Q10.2l-A-Schnitt:** `BESTÄTIGT`

**Frage:** Ist die Mutationsfreigabe für den verkleinerten ACL-Schnitt erteilt?

**Antwort:** `BESTÄTIGT` – Der Nutzer erteilte ausdrücklich die Apply-Freigabe.
Geltung nur für: Direktgrants und anschließend PUBLIC-REVOKE von
Datenbank-`TEMPORARY` sowie EXECUTE der zwei Definer-Funktionen. Die acht
LO-EXECUTE bleiben unverändert. Keine Rollenanlage, kein B1/B2/B3, keine
LO-REVOKEs, keine Funktionsausführung, keine Kandidatenabfrage.

Restore-Nachweis gilt laut Q10.2c1 als erbracht. Q10.2d bleibt zusätzlich für
die Rollenanlage bestehen. Weiter offen:
Mutationslauncher ohne read-only Default, Zeitfensterattest und SQL-Hash-Attest.
Das vorhandene Gate-B1-Freigabeattest gilt nicht für diesen Schnitt.

**Q10.2n – Schreibweg, Zeitfenster und Attest:** `BESTÄTIGT`

**Antwort:** `BESTÄTIGT` – Der Nutzer beauftragte Einrichtung des Schreibwegs,
sofortiges Zeitfenster ohne parallele Rechteänderungen und Erstellung des
Attests. Gate-ID `RIGHTS-Q10-2L-A-2026-09-11`. Attest-Datei getrennt vom
B1-Attest: `dino_crm_discovery_target_01.rights-q102l.approval`. Launcher
`scripts/discovery/run-rights-q102l.py`: zuerst Dry-run mit ROLLBACK, dann
Apply mit COMMIT, danach read-only Post-Check. Kein Retry. Keine Rollenanlage,
kein B1, keine LO-REVOKEs.

**Ausführung 2026-09-11:** `APPLIED`. Dry-run rollback, dann Commit. Post-Check:
PUBLIC TEMP weg, PUBLIC EXECUTE der zwei Definer weg, acht LO-EXECUTE bleiben,
33 Rollen, Discovery-Rolle nicht angelegt, keine Kandidatendaten gelesen.
SQL-SHA-256 `0eb267f963bbb3b6c63522354f5febfc4931674706a4c99fe1a61f0082434488`.

**Q10.2o – Prüfrolle jetzt anlegen:** `BESTÄTIGT`

**Antwort:** `BESTÄTIGT` – Der Nutzer beauftragte die Anlage von
`dino_crm_discovery_ro_v1` jetzt. V2-SQL ohne Passwort in der Transaktion;
Passwort danach interaktiv. Eigener Launcher, Dry-run, Apply, Post-Check.
Kein B1, keine LO-REVOKEs, kein Clone-Projekt.

**Ausführung 2026-09-12:** `APPLIED`. Rolle `dino_crm_discovery_ro_v1` existiert.
CONNECT ja, TEMP nein, CREATE nein, keine Definer-EXECUTE, Connection-Limit 1.
Passwort wurde interaktiv gesetzt. SQL-SHA-256
`fadf20f065a7df625aa3ba3b788a65002f5c986ad4c2215d6d26c3bbd1ae570c`.

**Q10.2p – Login-Datei und Gate B1 als Prüfrolle:** `BESTÄTIGT` / `AUSGEFÜHRT`

Eigene Service-/pgpass-Dateien für `dino_crm_discovery_ro_v1`, Owner-Dateien
unberührt. Login-Rauchtest `LOGIN_OK`, `read_only=on`. Gate B1 V3 als diese
Rolle: `DISCOVERY-GATE-B1-V3-RO-2026-09-12` Status PASS, ein Versuch.
B2/B3 nicht gestartet.

**Q10.2q – Gate B2 und B3 als Prüfrolle:** `BESTÄTIGT` / `AUSGEFÜHRT`

Nutzerauftrag, B2 und B3 weiterzuführen. Wizard war unnötig: kein Dashboard,
kein neues Secret. B2 V3 PASS (14 Queries, u. a. 3 Schemas, 398 Relationen,
1960 Spalten). B3 V3 PASS (11 Queries). Rohdaten nur außerhalb Git. Keine
Kandidatendaten gelesen.

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

### Q11 – SDK-Erkenntnisse in die Projektplanung übernehmen

**Auftrag vom 2026-09-11, normalisiert:** Die gelesenen MCP-/Supabase-SDK-
Informationen mit `ask-matt` in die passenden Projektunterlagen einarbeiten,
die Spezifikation konsistent aktualisieren und parallel Integrationslücken
sowie weitere Optimierungen prüfen.

**Status:** `BESTÄTIGT` für lokale Dokumentationsaktualisierung und parallele
Recherche. Die SDKs sind dokumentarisch untersucht; ihre Installation und das
reibungslose Zusammenspiel im Projekt sind nicht nachgewiesen.

**Planungsvorschlag:** Offizielles MCP-SDK v2 als Protokollschicht und zuerst
seine nativen Auth-Hilfen evaluieren; `@supabase/server` als möglicher Adapter
bei passendem
Identitätsvertrag; `@supabase/middleware` nur bei nachgewiesenem Zusatznutzen.
Die TypeScript-Variante passt direkt zu diesen JavaScript-Paketen. Dieser
Vorteil ist keine endgültige Sprach-, Hosting- oder Authentscheidung.

**BESTÄTIGT** – 2026-09-13. R1 Runtime-Suche: **ein** Such-MCP, verschiedene
Tokens/Scopes je Akteur (interner Vermittler vs. später Kunde). Postgres
bleibt letzte Sperre. Kein zweiter Such-MCP in R1. Kein generic Postgres-MCP.
Profilverwaltungs-MCP bleibt getrennt (ADR-0003). Entwickler-Plugin nie auf
Produktion.

**OFFEN:** Stack-/Versionsauswahl, Alpha-Akzeptanz, OAuth-/Tokenvertrag,
DB-Identitätsabbildung und praktische Integrationsnachweise. Q9 und Q8.5,
ADR-0001/0003/0004 sowie bestehende Discovery- und Produktionsfreigaben bleiben
unverändert. Q4.5 ist als leere Nummer stillgelegt. Es wurden weder Installation
noch Datenbankzugriff, Deployment
oder Linear-Writes beauftragt.

Die aktualisierte technische Fassung liegt im
[SDK-Integrationsplan](../planning/sdk-integration-plan.md); Quellen und
unabhängige Prüfung stehen in der
[SDK-Recherche](../research/mcp-supabase-sdk-integration.md).

### Q12 – Privilegierte Sicht und Export

**Status:** `TEILWEISE BESTÄTIGT`

**Nutzeraussage vom 2026-09-12:** User und Superuser sollen alles sehen und
exportieren können; das soll gleich mit eingebaut werden.

**Klarstellung danach:** Der Nutzer bestätigt das Plugin-Verbot und sagt,
bestimmte Permissions sollen „das“ trotzdem haben dürfen.

**Teilentscheidung:** Das Entwickler-Plugin/MCP bleibt an Produktion und
Restore-Klon verboten, unabhängig von CRM-Rechten. Privilegierte *Produkt*-
Berechtigungen für mehr Sicht oder Export sind gewollt. Sie sind nicht dasselbe
wie der Plugin-Schlüssel und nicht dasselbe wie PostgreSQL-Superuser.

Q4 `ERSETZT` 2026-09-12: interne Vermittler-Rollen sehen alle Kandidaten und
alle Felder inklusive Kontakt. Der Kunde erhält Kontakte nur in der
Einstellungsfreigabe. Export in R1: siehe Q15.6.

„User“ und „Superuser“ sind kein Glossarbegriff. Der bestätigte R1-Akteur ist
der Recruiter (Q2). In `crm_auth` gibt es `roles.role_key` / `role_name`; die
Werte wurden nicht gelesen (keine Tabellen-Grants der Prüfrolle).

Kataloghinweis, keine Freigabe: `crm_api.search_candidates` listet in der
Signatur bereits E-Mail und Telefon. Das ist der alte CRM-Pfad, nicht der
R1-MCP-Vertrag.

**Noch offen:** Feindetails und Freigabe des Vorschlags in Q15.

### Q13 – Generierte Lebensläufe

**Status:** `OFFEN` – ausdrücklich später, nicht Release 1.

**Nutzeraussage vom 2026-09-12:** Später sollen Lebensläufe erstellt werden
können.

Das ist eine eigene Produkt- und Trust-Grenze, kein Suchwerkzeug. Katalog:
`idk_kandidat_cv` ist klein; additiv existieren `candidate_documents` und
`candidate_document_text`. Keine Entscheidung über Generator, Speicherung oder
wer das auslösen darf.

### Q14 – Semantische Ähnlichkeitssuche als Standard

**Status:** `BESTÄTIGT`

**Frage:** Soll „finde Leute, die ungefähr so klingen“ der Standard der Suche
sein?

**Antwort:** `BESTÄTIGT` – 2026-09-12. Nicht der Standard (nicht C). Expliziter
Extra-Knopf „ähnlich wie dieser Kandidat“ (Nutzeroption D / SEM-UC-02). Kein
automatischer Fallback bei null Treffern (Q7 bleibt). Harte Filter bleiben
vor dem Limit gültig.

**Q14.1 – Wann der Knopf:** `BESTÄTIGT` – Option A. In den Vertrag jetzt,
ausliefern nach dem Evaluations-Gate. Release 1 bleibt die normale
Filter-/Occupation-Suche. Keine Freigabe, echte CV-Embeddings zu füllen oder
das Plugin zu nutzen. Die Embedding-Tabelle ist katalogisch leer/winzig, ohne
HNSW/IVFFlat.

**Katalogbefund Gate B2 V3 (Namen und Schätzungen, keine Datensätze):**

- Additive Tabellen `candidate_documents`, `candidate_document_text`,
  `candidate_document_embeddings` mit `extensions.vector(1536)`. Größe jeweils
  unter 1 MiB, `reltuples` -1. Kein HNSW/IVFFlat-Indexname.
- Dagegen Taxonomie: `occupation` ~702, `occupation_alias` ~1241,
  `job_occupation_map` ~87844. `idk_kandidati` ~122004 (Katalogschätzung, nicht
  gezählter Stand).
- Trigram-Indizes auf Freitext. RPCs `search_candidates_by_occupation` und
  `search_candidates_filtered` existieren. Das belegt nicht, dass der Runtime-MCP
  sie nutzen darf.

Berufssuchprofile und Occupation-Filter bleiben der belegte Kern. Der Extra-Knopf
ist beschlossen als Modus, nicht als Default, und nicht als R1-Must-have.

### Q15 – Akteure und Berechtigungsstufen

**Status:** `TEILWEISE BESTÄTIGT` / Vorschlag `VORLÄUFIGER VORSCHLAG`

**Nutzeraussage vom 2026-09-12:** Es gibt den Kunden (Firma, die einstellt), den
Kandidaten (bewirbt sich, gibt Daten ein) und den Vermittler mit Inhaber,
Entwickler, Teamleiter in der Firma und Sachbearbeiter. Bestimmte Permissions
sollen mehr dürfen; das Entwickler-Plugin an Produktion/Klon bleibt verboten.

**Q15.1 – R1-Nutzer intern:** `BESTÄTIGT` – 2026-09-12. Release-1-Nutzer der
Suche sind intern beim Vermittler. Kunde und Kandidat sind keine R1-Nutzer
des Runtime-Such-MCP. Das bestätigt Q2 (kleine interne Recruiter-Gruppe) und
grenzt sie gegen Kunde/Kandidat ab.

**Q15.4 – Interne R1-Suche:** `BESTÄTIGT` – 2026-09-12, Kontaktteil
`ERSETZT` 2026-09-12. In Release 1 suchen Sachbearbeiter, Teamleiter, Inhaber
und Entwickler in der echten Kartei. Sie sehen den gesamten Pool und alle
Felder inklusive Kontakt. Das Entwickler-Plugin an Produktion oder Klon bleibt
verboten.

**Q15.2 – Kundenfirma nur Freigaben:** `BESTÄTIGT` – 2026-09-12, Zweistufen-
Freigabe `BESTÄTIGT` 2026-09-12. Die Kundenfirma sieht nur von uns freigegebene
Kandidaten, nie den ganzen Pool. Das ist die Auslage, nicht der Schrank. Zuerst
Vorschlagsfreigabe ohne Kontakte; nach Zusage/Einstellung Einstellungsfreigabe
mit Kontakten nur für diesen Kandidaten.

**Q15.3 – Entwickler:** `ERSETZT` – 2026-09-12. Im Produkt sieht der Entwickler
wie die anderen internen Rollen alle Kandidaten und alle Daten. Das
Entwickler-Plugin nie an Produktion oder Restore-Klon. Plugin-Arbeit bleibt
auf Testdaten ohne echte Personen.

**Empfohlene kanonische Akteure** (nicht auf Tabellen gemappt):

- Kandidat, Kunde, Vermittler
- intern: Inhaber, Teamleiter, Sachbearbeiter, Entwickler

**Empfohlene Einstellung:**

- Kandidat: nur eigene Daten.
- Kunde: `BESTÄTIGT` nur von uns freigegebene Kandidaten, nie den ganzen Pool;
  Vorschlagsfreigabe ohne Kontakt, Einstellungsfreigabe mit Kontakt.
- Sachbearbeiter: `BESTÄTIGT` gesamte interne Kartei inklusive Kontakt.
- Teamleiter: `BESTÄTIGT` gesamte interne Kartei inklusive Kontakt.
- Inhaber: `BESTÄTIGT` gesamte interne Kartei inklusive Kontakt; kein Plugin.
- Entwickler: `BESTÄTIGT` gesamte interne Kartei inklusive Kontakt; Plugin nie
  an Prod/Klon.

Keine physischen `role_key`-Werte wurden gelesen.

**Q15.5 – Spätere Kontakte und Export:** `ERSETZT` im Kontaktteil – 2026-09-12
durch Q4. Interne Rollen inklusive Sachbearbeiter sehen Kontakte von Anfang an.
Kontakte an den Kunden folgen der Zweistufen-Freigabe.

**Q15.6 – Exportumfang:** `TEILWEISE BESTÄTIGT` – 2026-09-13. Recruiter hat
**beides:** Blättern (höchstens 50 pro Seite, `kandidat_id` absteigend)
**und** Datei-Export. Plugin bleibt kein Exportweg. Dateityp: CSV und
Excel, Recruiter wählt (`BESTÄTIGT` 2026-09-13). Limit: höchstens 500
Zeilen pro Datei, gleiche Ordnung wie Blättern (`kandidat_id` absteigend).
Mehr Treffer bleiben über Seiten erreichbar. Datei wie interne Trefferliste:
inkl. JMBG und Kontakt (`BESTÄTIGT` 2026-09-13). Nur Recruiter-Export, nicht
Kunde. Export des ganzen Bestands ohne Filter ist nicht bestätigt.

### Q16 – Nächster Schritt nach den Rechten

**Status:** `BESTÄTIGT`

**Frage:** Zuerst Tabellen in Fachbegriffe übersetzen, oder zuerst Q8.5?

**Antwort:** `BESTÄTIGT` – 2026-09-12. Das Sinnvollere: zuerst Mapping. Option A.
Erste Zuordnung: [Katalog zu Domäne](../discovery/catalog-domain-mapping.md).
Q8.5.3–8 und 8.5.9 stehen. Overlap und Enddatum sind beantwortet;
offen bleiben von/bis-Spalten und die physische Jobgruppe.

### Q17 – Quellenrang: Heft und alte CRM-UI

**Status:** `BESTÄTIGT` – 2026-09-12

**Frage:** Gilt das Interviewheft als Filter, der alles ausschließt, was
darin nicht vorkommt? Oder stehen Heft und die heute laufende CRM-Suche
gleichberechtigt nebeneinander?

**Antwort:** `BESTÄTIGT` – Beide Quellen sind gleichberechtigt.

- **Heft (dieses ADR):** was als Ziel beschrieben wurde.
- **Alte UI / PHP:** wie heute wirklich gesucht wird.

Das Heft ist kein Deckel und keine Whitelist. Was der Code neu zeigt
(zum Beispiel Struke, Schule, Smjer, Gruppe, DIPL-Status, Führerscheinklasse),
wird nicht verworfen, nur weil eine frühere Interviewfrage es nicht kannte.
Umgekehrt gelten bestätigte Heft-Ziele (drei Berufsschichten als Fachmodell,
Q8.5 offen, Q4 interne Kontakte) nicht als tot, nur weil die alte Filter-UI
sie anders oder gar nicht abbildet. Neue Codefakten erzeugen neue Fragen;
sie überschreiben eine ausdrückliche Antwort nur, wenn der Nutzer das
ausdrücklich sagt. Die neueste ausdrückliche Entscheidung bleibt vorrangig.

### Q18 – PHP-Codebefund der alten Recruiter-Filter-UI

**Status:** `TEILWEISE BESTÄTIGT` — Codebefund + Alltag; nicht MCP-Vertrag

**Frage:** Was zeigt der lokale CRM-Quellcode für die Recruiter-Suche?

**Antwort:** Wizard 01 ist gelaufen gegen
`/Users/activi/Downloads/crm-master-3/src/crm` (Legacy-PHP, Stack `php`).
Rohzettel: [crm-php-hits](../discovery/crm-php-hits/). Lesart:
[crm-app-wiring.md](../discovery/crm-app-wiring.md). Wizard 02 ist optional,
weil das Mapping aus dem PHP erstellt wurde, nicht weil 02 gelaufen ist.

**Rescan 2026-09-13:** Der erste Wizard-01-Lauf schnitt `hits-tables` und
`hits-ui` bei 200 Zeilen ab. Das war unvollständig (`kandidati.php` fehlte
in den Zetteln). Der Deckel ist entfernt. Neuer Stand ohne Zeilenlimit,
ohne `*.sql` und ohne `Info/` (Dump): RPC 21, Tabellen-Fundstellen 1732, UI 2487.
`kandidati.php` kommt grob in tables (171) und ui (152) vor; das zählt
auch `public_kandidati.php` mit. Nur `src/crm/kandidati.php`: 58 / 49.
1732 und 2487 sind Code-Fundstellen, keine Postgres-Tabellen. Ein 200-Deckel
darf in Wizard 01 nicht wieder eingeführt werden.

Codebefund, `BELEGT DURCH QUELLCODE`; Alltag 2026-09-13 bestätigt (siehe unten):

- vermutete Hauptsuche: `kandidati.php?page=list_ajax`, Filter an
  `serversidedata.php?page=lista_kandidata`;
- Filterfelder unter anderem Alter, Führerschein, Erfahrung als ja/nein,
  Deutsch/Englisch, Gruppe, Status, Quelle, Staatsangehörigkeit, EU-Aufenthalt,
  Struke, Schule, Smjer, DIPL-Status, Nostrifikation;
- nicht in dieser Maske: drei getrennte Berufsschichten, Jahres-Erfahrung,
  Stadt/Wunschort, Skills, Freitext, occupation-Berufssuchprofil;
- `search.php` ist Menü-Volltext, nicht Kandidatensuche;
- keine Nutzung von `crm_api.search_candidates` in dieser PHP-Hauptsuche.

**Update 2026-09-13:** Filter-SQL von `lista_kandidata` ist gelesen und in
[crm-filter-sql-codebefund.md](../discovery/crm-filter-sql-codebefund.md)
dokumentiert (leere Filter = tot, UND zwischen Kategorien, Erfahrung =
Existenz von Jobzeilen, Deutsch ab Stufe aufwärts). Kein Datensatz-Dump.
Kandidatenzeilen werden nicht in Git oder Chat kopiert. Q4 bleibt: interne
Rollen sehen Kontakte im Produkt; Discovery-Artefakte bleiben ohne
Datensatz-Dump.

**Alltag 2026-09-13 (Wizard 03, Nutzer):**

- Tägliche Recruiter-Suche = `kandidati.php?page=list_ajax` →
  `lista_kandidata`: `BESTÄTIGT`.
- Release 1 nur diese Hauptsuche, ohne Partner-/QC-/Nalog-Suche:
  `BESTÄTIGT`.
- Ort, Skills, Berufssuchprofil in R1-Suche: `BESTÄTIGT` nein, erst nur
  die alten Filter (passt zu Q22 als Scan; das ist jetzt auch der
  Produktumfang der ersten Suche).
  - Q8.5 / Jahresfilter in R1: `BESTÄTIGT` 2026-09-13 ja, über von–bis der
    passenden und gruppenähnlichen Jobs (Q8.5.9). Alte UI bleibt ja/nein;
    R1 ergänzt das. Aktenzahlen nicht verwenden.
- Q8.4 drei Berufsschichten bleibt bestätigt, nicht neu befragt.
- Struke/Smjer in der alten Maske = Ausbildungsberuf: `BESTÄTIGT`
  2026-09-13. JSON-Namen bleiben `struke` / `smjer`. Nicht Q8.4
  überschreiben, nicht occupation mappen.

Noch `OFFEN` in Wizard 03: Secret-Check (Betriebsfrage).

INNER JOIN Gruppe/Status in R1: `BESTÄTIGT` nein, 2026-09-13. Kandidaten
ohne Gruppen- oder Bearbeitungszeile bleiben sichtbar. PHP-INNER-JOIN
nicht übernehmen. Die alte Suche behält `INNER JOIN` in `lista_kandidata`
(Liste und Zählung); das ist PHP-Ist, kein R1-Soll. Andere Filter gelten weiter.

**Update 2026-09-13 JSON-Filter:** Entwurf nur der alten Filter:
[crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).
Kein Runtime-MCP. Berufssuchprofil, Ort und Skills nicht in R1.
Jahre in R1 über Q8.5.9.

**Update 2026-09-13 JSON-Filter-Prüfung:** Entwurf gegen PHP
`lista_kandidata` und Heft geprüft. Die Maskenfelder decken sich.
Struke/Smjer = Ausbildungsberuf: `BESTÄTIGT`. Jahresfilter R1 Q8.5.9:
von–bis, Job + Jobgruppe. Alte UI bleibt ja/nein. JSON-Namen
`struke` / `smjer`.
Kein Vertrag, kein MCP.
Bericht-Audit 2026-09-13: Vorbericht-PASS nicht haltbar. Archiv-Satz in
[crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md) getrennt.
Nutzer 2026-09-13 Punkt 1 **Ja:** Vorbericht-PASS zählt nicht.
Punkt 3 **Ja:** JSON bleibt Entwurf, kein Vertrag.
Punkt 2 (Archiv-Satz) **Ja:** PHP-Zählfehler kennen, in R1 nicht kopieren.
INNER JOIN: Nutzer **Nein**, Leute ohne Gruppe/Bearbeitung bleiben sichtbar.
JMBG in der internen Trefferliste: `BESTÄTIGT` ja. Kein Filter, nicht
wichtig für Auswahl. Bleibt besonders sensibel. Discovery ohne Werte.
Ranking R1: `BESTÄTIGT` 2026-09-13. Sortierung nach `kandidat_id`
absteigend, größte Nummer zuerst (neueste). Ein Kriterium, kein Tie-Breaker.

**ACT-103 Kreuze:** `BESTÄTIGT` – 2026-09-13. Nutzer: **1A 2A 3A**.
Pflichtartefakt = Inventar + Codebefunde + JSON-Entwurf. INNER JOIN und
Archiv-Satz für ACT-103 geschlossen. Done darf bei JSON-Entwurf (Vertrag
später AUTO-02). Linear-Kommentar 2026-09-13; Status Done.

Index: [crm-work-inventory.md](../discovery/crm-work-inventory.md).
C 4–9: [crm-notify-codebefund.md](../discovery/crm-notify-codebefund.md).

### Q19 – Status-Ebenen und Automatik im alten CRM

**Status:** `TEILWEISE BESTÄTIGT` als Codebefund

**Frage:** Soll die Discovery außer Suchfiltern auch alle Kandidatenstatus
und automatischen Übergänge erfassen?

**Antwort:** `BESTÄTIGT` – 2026-09-12. Ja, gleichberechtigt zur Filter-UI
(Q17). Dafür wird **nicht** Wizard 01 erweitert oder wiederholt. Eigener
Scan: [Wizard 04](../../scripts/wizards/crm-wiring-04-status-and-triggers.sh),
Lesart: [crm-status-codebefund.md](../discovery/crm-status-codebefund.md).

Erste PHP-Ebenen: Bearbeitung `kandidat_status` (IDs 0–8, Labels in
`getStatusList`), Anmeldung `kandidat_status_prijave`, Messenger
`kandidat_status_messenger`, DIPL-Status 0–7, dazu Task-Force
(`kandidat_tf_status`). Automatik in Cron und `do.php` (Beispiel:
Go-Online setzt Prijave 3; Bot-Cron schiebt 1→7 / 5→8).
Welche konkreten Statuswerte der Runtime-MCP als Filter anbietet, bleibt
fein `OFFEN`; die Ebenen selbst gehören laut Q20 zur Suche.

**Update 2026-09-13 B7:** Manuelle Klicks sind gelesen, ohne Datensatz-Dump.
Lesart: [crm-status-codebefund.md](../discovery/crm-status-codebefund.md).
Bearbeitungs-Leiste: `ajax.php?page=candidate_status` →
`candidate_status_edit` setzt nur `kandidat_status`, schreibt
`idk_log_kandidat_statusi`. Status 2 ruft `checkCandidateInputs`
(BOT-Projekte, Prijave 6 oder 2). Messenger-Labels stehen in derselben
UI (0 manuell, 1 SMS wartet, 2 eingeloggt, 3 Install abgelehnt, 5/6
Profil unvollständig). `do.php`: Go-Online, Termin 15/18, Interview
gekommen/nicht gekommen, Validierung → Dopuna 5. Das ist Codebefund,
kein neuer Produktvertrag.

### Q20 – Welche CRM-Flächen jetzt, welche später

**Status:** `TEILWEISE BESTÄTIGT` – 2026-09-13

**Frage:** Welche nummerierten Flächen aus der Landkarte gehören in den
ersten Runtime-Such-MCP, welche nur als Default-aus-Automatik, welche in
einen späteren zweiten MCP?

**Antwort:**

**Jetzt zur Suche/Akte (tief scannen, R1-Suche):**

1. Recruiter-Kandidatenfilter — `BESTÄTIGT`
2. Alle Status-Ebenen — `BESTÄTIGT`
3. Was ein Statuswechsel auslöst — `BESTÄTIGT`

Zusätzlich 2026-09-13 `BESTÄTIGT`, tief scannen:

- **A:** Filter-SQL in `serversidedata.php` (wie die Maske wirklich rechnet)
  und welche Spalten die Trefferliste zurückgibt.
- **B7:** manuelle Statuswechsel über `do.php` / `ajax.php` (Klick im CRM,
  nicht nur Cron). Vom Nutzer ausdrücklich als **sehr wichtig** bestätigt.
  Gehört zu Punkt 3, ist der Alltagsweg neben den Zeitjobs.

**Benachrichtigung/Erinnerung (C, Punkte 4–9) — `BESTÄTIGT`, tief scannen,
sehr wichtig, alles aufnehmen. Im Produkt Default aus:**

| Punkt | Fläche |
| --- | --- |
| 4 | Kandidat benachrichtigen (Zusage, Vertrag, Status) |
| 5 | Kunde benachrichtigen (Unterschrift, Zusage) |
| 6 | Erinnerung bei ausbleibender Antwort |
| 7 | Messenger/Bot-Erinnerung (Profil unvollständig) |
| 8 | Termin: Einladung, nicht erschienen, Casting → Interview |
| 9 | Geburtstagsmail |

2026-09-13: Nutzer bestätigt **alle** Punkte 4–9. Sie gehören in denselben
Tief-Scan wie A/B (welche Mail/Erinnerung an welchem Status, welcher Klick
oder Cron). Im **laufenden** Produkt bleiben sie **default aus** und
einschaltbar. Einschalten ist eine spätere ausdrückliche Aktion, kein
Default nach Deploy.

**Update 2026-09-13 C 4–9:** PHP gelesen, ohne Datensatz-Dump.
Lesart: [crm-notify-codebefund.md](../discovery/crm-notify-codebefund.md).
Die Bearbeitungs-Leiste sendet keine Nachricht. C4: Onboarding-SMS
(vier Infobip-Texte) und Push bei Dopuna 5; Kandidaten-Mail-Funktionen
tot. C5: kein Mail an den einstellenden Kunden am Kandidatenstatus;
Partner-Push bei Nalog 8 und Firmenstatus; PP-Reminder-Mails aus.
C6/C7: Bot-Cron, max drei Erinnerungen, dann Status 7/8+5/6 bzw. 6+3.
C8: Einladungs-SMS/Viber mit Bestätigungs-Link; Go-Online und
Nicht-erschienen ohne Kandidaten-Nachricht; Mitarbeiter-Mail am
Termintag. C9: Geburtstags-Viber/SMS, kein Statuswechsel.
Das ist Codebefund, kein eingeschaltetes Produkt.

**10 DIPL-Erinnerungen:** `BESTÄTIGT` als **spätere Option**, nicht im
jetzigen Tief-Scan von 1–3 und nicht im Default-aus-Paket 4–9. Gleicher
Korb wie 11–16: später, bei Bedarf, eher zweiter MCP oder nachträgliche
Funktion.

**Andere Module 11–16 (Partner, QC, Nalog-Profile, Finanzen/Inkaso,
Viber/Marketing, Vertragsfluss):** `TEILWEISE BESTÄTIGT` — werden später
alle gebraucht, voraussichtlich in einem **zweiten MCP**, nicht zwingend im
ersten Such-MCP. Ob wir sie **jetzt nur oberflächlich** (Menü/Cron-Namen)
für später mitinventarisieren, ist vom Nutzer als sinnvoll angedeutet, noch
keine Scan-Freigabe der Tiefe von 1–3.

Finanzen/Inkaso bleiben außerhalb der Recruiter-**Suche**; sie sind nur im
Korb „späterer MCP“.

### Q21 – PHP scannen, modern umsetzen, nicht 1:1 kopieren

**Status:** `BESTÄTIGT` – 2026-09-13

**Frage:** Sollen wir das alte PHP-CRM 1:1 nach Supabase spiegeln, oder die
Funktionen erfassen und in einer modernen Suche für den Agenten neu bauen?

**Antwort:** `BESTÄTIGT` – Der Scan dient dazu, dass niemand aus dem Kopf
raten muss, **welche Funktionen** das CRM hat. Diese Funktionen (oder mehrere
davon gebündelt) sollen im neuen System **verfügbar** sein. Die Umsetzung
ist **kein** blinder 1:1-Map von PHP-SQL auf Supabase. Alles, was sich
aktualisieren, verbessern, optimieren oder auf heutige Technik heben lässt,
soll das tun.

Ziel der ersten MCP-Arbeit: Der Agent versteht eine Textanfrage, weiß **wie
und wonach** er filtern darf, und welche Tools/Skills er dafür braucht.
PostgreSQL bleibt ausführend (ADR-0001: JSON-Filter, kein LLM-SQL).
Die alte Maske und der Katalog bleiben gleichberechtigte Quellen (Q17);
Lücken (z. B. Struke in der UI vs. occupation in der DB) sind Chancen zum
Modernisieren, kein Zwang zur Gleichheit.

Die Beispiele occupation / Akten-Jahre / Stadt-als-Filter sind laut Q22
**jetzt kein Scan-Auftrag**; Modernisieren kommt nach der Dokumentation der
alten Abläufe.

### Q22 – Aktueller Scan: altes CRM, nicht PG-Zusatzfelder

**Status:** `BESTÄTIGT` – 2026-09-13

**Frage:** Sind Felder, die nur in der Supabase-Kartei liegen und die alte
Filter-UI nicht nutzt (occupation, Erfahrungsjahre auf der Akte, Stadt/
Skills als Suchfelder), jetzt Teil der Discovery?

**Antwort:** `BESTÄTIGT` – **Nein, jetzt nicht relevant.** Gescant und
dokumentiert werden **altes Frontend und alte Businesslogik**: Masken,
Verdrahtung, Status, Trigger, komplette Abläufe (Punkte 1–3, A, B7, C 4–9).
Quelle ist das PHP-CRM und die Tabellen, die es **wirklich benutzt**.

Supabase wird danach **anhand dieser Dokumentation** eingerichtet und der
MCP verdrahtet (Q21: modern umsetzen). Extra-DB-Felder, die der alte Ablauf
nicht kennt, sind kein jetziger Scan-Auftrag.

Die Linear-Karte ACT-100 (2026-09-12) stellte Quellen- und Scanfragen unter
Jobstep/OrbStack-Titeln. Q17 und Q20–Q22 sind die ausdrücklichen Antworten.
Diese Fragen nicht aus den Linear-Titeln neu öffnen.

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
