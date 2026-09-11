# Recherche Q8.4.2: Kontrollierte Berufssuchprofile

Datum: 2026-09-11

Status: Historische Recherchegrundlage, keine eigenständige Architekturentscheidung

## Einordnung nach Auditkorrektur vom 2026-09-11

Die Recherche bleibt erhalten. Empfehlungen unterhalb dieses Hinweises sind
`VORLÄUFIGER VORSCHLAG`, soweit nicht ausdrücklich als geltende Grenze aus
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md) bezeichnet.
Sie beweisen keine historische Einzelzustimmung. Q8.4 bleibt grundsätzlich
bestätigt; Q8.5 ist vollständig `OFFEN`. CRM-Bestandsaussagen sind
`ARBEITSANNAHME / DURCH DISCOVERY ZU PRÜFEN`; Beispiele sind keine realen
Profilversionen oder Datenbankverträge.

| Historische Empfehlung | Aktuelle Einordnung |
| --- | --- |
| Vier-Augen-Pflicht / alleinige Freigabe unzulässig | Durch ADR-0003 überholt: keine verpflichtende zweite Person; getrennte Bearbeitung und Veröffentlichung bleiben. |
| Verwaltungs-MCP optional | Durch ADR-0003 überholt: als getrennte spätere Komponente nach Discovery und Modellfreigabe geplant. |
| Pflicht-/Wunschrollen je Mitglied | Vertagt / OFFEN; weder Aufnahme noch Ausschluss aus Release 1 ist aus den ursprünglichen Empfehlungen nachgewiesen. |
| Bestätigung vor jeder Suche | VORLÄUFIGER VORSCHLAG; nur Zustimmung vor Filterlockerung gemäß Q7 ist ausdrücklich belegt. |
| Erfahrungsrelevanz und Zeitberechnung | Gesamte Q8.5 OFFEN; nachfolgende Regeln sind nur Vorschläge. |
| BIBB/KldB/ESCO/O*NET-Auswahl und Normalisierungsdetails | VORLÄUFIGER VORSCHLAG; die Recherche ist keine Freigabe dieser Details. |

Diese Statuszuordnung gilt auch für normativ formulierte historische Sätze
wie „braucht“, „muss“ oder „darf nicht“ in den jeweiligen Empfehlungen. Die
akzeptierten Grenzen Nicht-Exklusivität, direkte Suche und keine automatische
Veröffentlichung bleiben bestehen.

## Fragestellung

Kann ein wiederverwendbares Suchprofil wie „Tiefbauer“ mehrere kontrollierte
Ausbildungsberufe, normalisierte Berufe aus Freitext-Berufserfahrung und
Tätigkeitsarten bündeln, sodass Nutzer nicht jeden Einzelbegriff auswählen
müssen? Ist dieses Modell vollständig, nachvollziehbar und schnell genug für die
CRM-Suche?

## Kurzurteil

**Ja, das Modell ist fachlich und technisch gut machbar.** Die Beschreibung ist
im Kern richtig, aber für eine verlässliche Umsetzung noch nicht vollständig.
Ein Profil darf nicht nur aus einem Namen und einer ungeprüften Liste von
Berufen bestehen. Es braucht mindestens:

- eine stabile interne Profil-ID und mehrsprachige Anzeigenamen;
- einen Zweck und eine klare fachliche Beschreibung;
- getrennte Mitglieder für Ausbildungsberufe, ausgeübte Berufe und Tätigkeiten;
- je Mitglied die Rolle `Pflicht`, `passende Alternative`, `Wunsch` oder
  `Ausschluss`;
- Quellen-IDs aus kontrollierten Klassifikationen;
- eine freigegebene, unveränderliche Version mit Gültigkeitszeitraum;
- einen fachlichen Verantwortlichen und ein Prüfdatum;
- eine sichtbare Auflösung in der Filtervorschau;
- eine gespeicherte Begründung, warum ein Beruf oder eine Tätigkeit dazugehört.

Die beste Lösung ist ein **internes, versioniertes Suchprofil als kontrollierte
Auswahlschicht über amtlichen beziehungsweise etablierten Taxonomien**. Das
Profil ersetzt KldB, BIBB oder ESCO nicht. Es kombiniert gezielt deren Konzepte
für den konkreten Recruiting-Anwendungsfall.

**Eine Profilzuordnung darf ein Berufskonzept niemals besitzen, sperren oder
exklusiv machen.** Zwischen Profilen und Konzepten gilt eine Viele-zu-viele-
Beziehung: Ein Beruf kann in mehreren Profilen vorkommen, und jeder Beruf sowie
jede Tätigkeit bleibt unabhängig vom Profil direkt suchbar. Ein Profil ist nur
eine gespeicherte Auswahl, kein neuer Container für Kandidatendaten.

## Warum mehrere Quellen benötigt werden

| Quelle | Geeignet für | Grenze für dieses Projekt |
| --- | --- | --- |
| BIBB | Amtlich anerkannte deutsche Ausbildungsberufe und deren aktuelle Rechtsgrundlagen | Beschreibt formale Ausbildung, nicht jede tatsächlich ausgeübte Tätigkeit |
| KldB 2010, Fassung 2020 | Deutsche Berufs- und Tätigkeitsbezeichnungen, Synonyme, Hierarchie und Anforderungsniveau | Eine Hierarchiegruppe ist nicht automatisch dasselbe wie ein Recruiting-Suchprofil |
| ESCO | Mehrsprachige Berufe, alternative Begriffe, Skills/Tätigkeiten und Beziehungen zwischen ihnen | Die fachliche Passung eines konkreten Kundenprofils muss intern geprüft werden |
| O*NET | Detaillierte Tasks und Work Activities als ergänzende Referenz | Auf den US-Arbeitsmarkt und die US-SOC-Systematik ausgerichtet; nicht als primäre DACH-Taxonomie verwenden |

Das BIBB führt das jährlich aktualisierte Verzeichnis der nach BBiG/HwO
anerkannten Ausbildungsberufe. Die Ausgabe 2026 enthält 324 anerkannte
Ausbildungsberufe sowie Ausbildungsdauer, Rechtsgrundlagen, Fachrichtungen und
DQR-Zuordnung. Damit eignet sie sich als Referenz für den formalen
Ausbildungsberuf, nicht als Beweis für tatsächlich ausgeübte Arbeit
([BIBB, Verzeichnis 2026](https://www.bibb.de/dienst/publikationen/de/21008)).

Die KldB ordnet Berufe in fünf Ebenen und trennt horizontal die
„Berufsfachlichkeit“ von dem vertikalen „Anforderungsniveau“. Berufsfachlichkeit
ist ein Bündel beruflicher Fachkompetenzen; das Anforderungsniveau beschreibt
die Komplexität der Tätigkeit. Diese Trennung spricht dafür, Berufsfeld und
Qualifikationsniveau im Suchprofil nicht in einem einzigen Wert zu vermischen
([Bundesagentur für Arbeit, KldB Band 1, S. 25](https://statistik.arbeitsagentur.de/DE/Statischer-Content/Grundlagen/Klassifikationen/Klassifikation-der-Berufe/KldB2010-Fassung2020/Printausgabe-KldB-2010-Fassung2020/Generische-Publikationen/KldB2010-PDF-Version-Band1-Fassung2020.pdf)).

Das Berufs- und Tätigkeitsverzeichnis der Bundesagentur enthält knapp 18.900
Bezeichnungen, darunter aktuelle Bezeichnungen, Synonyme, verwandte Formen,
Vorläuferberufe und andere arbeitsmarktrelevante Namen. Alle werden einer
KldB-Systematikposition zugeordnet. Das ist eine geeignete kontrollierte Basis
für viele Varianten in historischen Freitextfeldern
([Bundesagentur für Arbeit, Systematik und Verzeichnisse](https://statistik.arbeitsagentur.de/DE/Navigation/Grundlagen/Klassifikationen/Klassifikation-der-Berufe/KldB2010-Fassung2020/Systematik-Verzeichnisse/Systematik-Verzeichnisse-Nav.html)).

ESCO trennt die Säulen „occupations“ und „skills/competences“ und nutzt
Hierarchien sowie ISCO-Zuordnungen. Konzepte besitzen bevorzugte und alternative
Bezeichnungen in 28 Sprachen. Alternative Bezeichnungen umfassen ausdrücklich
Synonyme, Schreibvarianten, Beugungsformen und Abkürzungen. Das ist besonders
hilfreich für deutsche, englische und B/H/S-nahe Freitextvarianten, ersetzt aber
keine lokale Prüfung der CRM-Begriffe
([ESCO-Klassifikation](https://esco.ec.europa.eu/en/classification),
[ESCO FAQ zu alternativen Bezeichnungen](https://esco.ec.europa.eu/en/about-esco/faq)).

ESCO verbindet Berufe mit als „essential“ oder „optional“ eingeordneten
Kenntnissen, Skills und Kompetenzen. Das unterstützt die Trennung zwischen
berufstypischen Kerntätigkeiten und kontextabhängigen Tätigkeiten
([ESCO, Two pillar structure](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/two-pillar-structure-esco)).

O*NET trennt ebenfalls Berufsbezeichnungen, Tasks und hierarchische Work
Activities. Es wird jedoch vom US Department of Labor getragen und basiert auf
O*NET-SOC. Daher ist es höchstens eine ergänzende Quelle für fehlende
Tätigkeitsbegriffe, nicht die führende Berufsquelle für Deutschland oder DACH
([O*NET Resource Center, Overview](https://www.onetcenter.org/overview.html),
[O*NET Content Model](https://www.onetcenter.org/content.html)).

## Empfohlenes fachliches Modell

### 1. Kontrollierte Basiskonzepte

Jeder relevante Begriff erhält eine stabile interne ID. Externe IDs und
Quellversionen werden zusätzlich gespeichert.

| Konzeptart | Beispiel | Zweck |
| --- | --- | --- |
| Ausbildungsberuf | `training_occupation:tiefbaufacharbeiter` | Formale, kontrollierte CRM-Auswahl |
| Ausgeübter Beruf | `occupation:road_construction_worker` | Normalisierte Berufsbezeichnung einer Beschäftigung |
| Tätigkeit | `activity:excavate_trenches` | Tatsächlich ausgeführte Arbeit |
| Skill/Kompetenz | `skill:operate_excavator` | Nachgewiesene oder dokumentierte Fähigkeit |
| Suchprofil | `profile:tiefbauer` | Wiederverwendbare Recruiting-Auswahl |

Diese Typen dürfen nicht gleichgesetzt werden:

- Ein Ausbildungsabschluss zeigt eine formale Qualifikation.
- Eine Berufsbezeichnung beschreibt eine berufliche Rolle.
- Eine Tätigkeit beschreibt, was eine Person tatsächlich getan hat.
- Berufserfahrung ist die Dauer nachgewiesener Beschäftigungsabschnitte, die
  fachlich zur bestätigten Suche passen.

### 2. Profildefinition

Ein freigegebenes Profil sollte ungefähr folgende fachliche Struktur besitzen:

```yaml
profile_id: profile:tiefbauer
version: 3
status: approved
display_name:
  de: Tiefbauer
  en: Civil engineering and groundworks workers
  bs: Radnici u niskogradnji
description: Arbeiten an Straßen, Gleisen, Leitungen, Kanälen und Spezialtiefbau
members:
  training_occupations: []
  experience_occupations: []
  activities: []
  excluded_concepts: []
member_semantics:
  relationship: many_to_many
  concepts_remain_directly_searchable: true
governance:
  owner: recruiting-taxonomy-owner
  approved_at: 2026-09-11
  valid_from: 2026-09-11
sources:
  bibb_release: "2026"
  kldb_release: "KldB 2010, Fassung 2020; Verzeichnisstand 2026"
  esco_release: "1.2.1"
```

Das YAML ist ein fachliches Beispiel, keine bereits freigegebene technische
Schnittstelle.

### 3. Mitgliedschaften statt automatischer Obergruppe

Ein Profil soll seine Mitglieder ausdrücklich speichern. Eine ganze
KldB- oder ESCO-Obergruppe darf nicht automatisch und dauerhaft übernommen
werden. Amtliche Hierarchien sind für Klassifikation und Statistik gebaut; ein
Recruiting-Profil kann dagegen Konzepte aus mehreren Zweigen benötigen oder
einzelne Nachbarberufe bewusst ausschließen. Auch die Europäische Kommission
beschreibt alternative Cluster als Ergänzung zur bestehenden ESCO-Monohierarchie,
nicht als deren Ersatz
([EU-Kommission, Alternative clustering of ESCO concepts](https://esco.ec.europa.eu/system/files/2024-03/ESCO%20MSWG%20focus%20meeting_%20Alternative%20clustering%20of%20ESCO%20concepts_final.pdf)).

Jede Mitgliedschaft braucht deshalb:

- `concept_id` und `concept_type`;
- fachliche Rolle: `required`, `accepted`, `preferred` oder `excluded`;
- kurze Begründung;
- Quelle und Quellversion;
- Gültigkeit ab/bis;
- Freigabestatus.

Die Zuordnungstabelle muss Viele-zu-viele erlauben:

```text
Beruf A → Profil Tiefbauer
Beruf A → Profil Straßenbau
Beruf A → weiterhin direkt als Beruf A suchbar
```

Das Entfernen eines Berufs aus einem Profil löscht oder deaktiviert weder das
Berufskonzept noch dessen Zuordnungen zu anderen Profilen. Ebenso darf das
Archivieren eines Profils keine Kandidaten-, Berufs- oder Erfahrungsdaten
verändern.

## Beispielprofil „Tiefbauer“

Die offizielle Tiefbauberufe-Verordnung nennt unter anderem
Tiefbaufacharbeiter, Straßenbauer, Kanalbauer für Infrastrukturtechnik,
Leitungsbauer für Infrastrukturtechnik, Brunnenbauer, Spezialtiefbauer und
Gleisbauer. Das BIBB beschreibt Tiefbau als Herstellung von Infrastruktur für
Straßen, Kanäle, Leitungen und Gleise
([BIBB, Tiefbauberufe](https://www.bibb.de/de/182943.php),
[Tiefbauberufeausbildungsverordnung](https://www.bibb.de/dienst/berufesuche/de/index_berufesuche.php/download/doc/ao/bauberufe2024.pdf)).

Diese Berufe sind daher **fachlich plausible Kandidaten** für die erste
Profilversion. Sie sind nicht allein durch diese Recherche endgültig als
Mitglieder beschlossen. Ein Recruiting-Fachverantwortlicher muss prüfen, ob das
Profil für den tatsächlichen Kundenbedarf alle oder nur einen Teil davon
enthalten soll.

Beispiel einer sichtbaren Auflösung:

```text
Profil: Tiefbauer, Version 3

Passende Ausbildungsberufe:
- Tiefbaufacharbeiter/in mit passenden Schwerpunkten
- Straßenbauer/in
- Kanalbauer/in für Infrastrukturtechnik
- Leitungsbauer/in für Infrastrukturtechnik
- Brunnenbauer/in
- Spezialtiefbauer/in
- Gleisbauer/in

Passende Erfahrung:
- normalisierte Tätigkeiten im Straßen-, Kanal-, Leitungs-, Gleis-, Brunnen-
  oder Spezialtiefbau

Nicht automatisch eingeschlossen:
- Hochbauberufe
- reine Verkaufs-, Büro- oder Logistikerfahrung
```

Die Bundesagentur beschreibt beim Tiefbaufacharbeiter als Tätigkeiten unter
anderem Erdarbeiten, Baugruben und Gräben, Verkehrswege sowie Ver- und
Entsorgungssysteme. Solche Tätigkeiten können als kontrollierte Aktivitäts-IDs
ergänzend zur Berufsbezeichnung verwendet werden
([BERUFENET, Tiefbaufacharbeiter/in](https://web.arbeitsagentur.de/berufenet/beruf/132673.pdf)).

## Suche über den Profilnamen

Die Eingabe „Tiefbauer“ soll nicht direkt eine unsichtbare Freitextsuche über
Kandidatendaten auslösen. Empfohlen ist:

```text
Nutzertext „Suche Tiefbauer mit 3 Jahren relevanter Erfahrung“
→ Profilname/Alias auf stabile Profil-ID auflösen
→ aktuell freigegebene Profilversion laden
→ Mitglieder nach Ausbildungsberuf, Erfahrungsberuf und Tätigkeit auflösen
→ vollständige Filtervorschau anzeigen
→ Nutzer bestätigt
→ Server validiert Profil-ID und Version erneut
→ Suche über kontrollierte IDs ausführen
```

Profilnamen dürfen mehrsprachige Aliase besitzen, zum Beispiel „Tiefbau“,
„Tiefbauarbeiter“ oder eine bestätigte englische/B/H/S-Bezeichnung. Ein Alias
darf nur dann automatisch aufgelöst werden, wenn er eindeutig ist. Bei mehreren
möglichen Profilen muss die Vorschau eine Auswahl verlangen.

Die Vorschau sollte mindestens zeigen:

- Profilname und Version;
- eingeschlossene Ausbildungsberufe;
- eingeschlossene Erfahrungsberufe und Tätigkeiten;
- Pflicht-, Alternativ-, Wunsch- und Ausschlussregeln;
- Berechnung der relevanten Erfahrungszeit;
- Abweichungen oder nicht auflösbare Nutzereingaben.

## Normalisierung vorhandener Freitext-Berufserfahrung

Die vielen Schreibweisen werden nicht in das Profil selbst kopiert. Sie werden
in einer kontrollierten Alias- und Zuordnungsschicht behandelt:

```text
Originaltext bleibt erhalten
→ Text technisch vereinheitlichen
→ exakten freigegebenen Alias prüfen
→ Beruf und Tätigkeiten als getrennte Konzepte vorschlagen
→ bereits ausdrücklich freigegebene deterministische Regeln anwenden
→ neue oder geänderte Zuordnungen ausschließlich als Vorschläge speichern
→ unsichere Vorschläge fachlich prüfen
→ Zuordnung mit Quelle, Version und Konfidenz speichern
```

Wichtige Felder pro Zuordnung:

- unveränderter Originaltext;
- normalisierte Schreibform;
- Sprache;
- Zielkonzept-ID und Konzeptart;
- Zuordnungsquelle: amtliche Liste, freigegebener Alias, manuelle Prüfung oder
  maschineller Vorschlag;
- Konfidenz und Prüfstatus;
- verwendete Taxonomie- und Mappingversion;
- Zeitpunkt und verantwortliche Stelle der Freigabe.

ESCO bietet hierfür bevorzugte und alternative Begriffe sowie stabile URIs pro
Konzept. Die Web-API kann bestimmte Klassifikationsversionen adressieren
([ESCO Web Service API](https://esco.ec.europa.eu/en/use-esco/use-esco-services-api/esco-web-service-api)).
Die aktuelle ESCO-Veröffentlichung stellt zudem Delta-Dateien bereit, um
Änderungen zwischen Versionen nachzuführen
([ESCO v1.2.1](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-v121)).

Ein Sprachmodell darf unbekannte Freitexte klassifizieren **vorschlagen**, aber
nicht stillschweigend neue verbindliche Aliase oder Profilmitglieder anlegen.
Das verhindert, dass zum Beispiel „Bauhelfer“ ohne fachliche Prüfung als
„Spezialtiefbauer“ gilt.

## Berechnung relevanter Berufserfahrung

**OFFEN: gesamte Q8.5.** Alle nachfolgenden fachlichen Regeln sind
`VORLÄUFIGER VORSCHLAG`, keine bestätigte Teilantwort.

Die Suchprofile lösen das Berufsproblem, aber nicht allein die Zeitberechnung.
Für jeden Beschäftigungsabschnitt werden Start, Ende, normalisierter Beruf und
normalisierte Tätigkeiten benötigt. Ein Abschnitt zählt nur, wenn seine
Zuordnung die bestätigte Profilregel erfüllt.

Empfohlene Grundregeln:

- fachfremde Abschnitte zählen nicht;
- unklare, ungeprüfte Zuordnungen zählen nicht als sicherer Treffer;
- parallel laufende Zeiträume werden nicht doppelt gezählt;
- fehlende oder ungenaue Datumsangaben werden sichtbar als Datenlücke behandelt;
- das Ergebnis zeigt relevante Monate und die dafür verwendeten Abschnitte;
- Ausbildungsberuf und Berufserfahrung bleiben getrennte Filter und Belege.

Ob bereits ein passender ausgeübter Beruf genügt, ob eine passende Tätigkeit
genügt oder ob beides gemeinsam erforderlich ist, bleibt eine eigene
Filtersemantik-Entscheidung in Q8.5. Das Profilmodell kann alle drei Varianten
abbilden; es sollte diese Entscheidung nicht verstecken.

## Bewertung eines getrennten Verwaltungs-MCP

### Urteil

Ein **separates administratives Einrichtungs-MCP ist sinnvoll**, wenn mehrere
Profile und laufende Taxonomiepflege erwartet werden. Es sollte jedoch erst nach
dem read-only Discovery und dem freigegebenen Datenmodell umgesetzt werden. Für
wenige einmalige Profile würde zunächst eine kontrollierte Admin-Oberfläche oder
ein geprüfter Importprozess genügen; MCP ist kein Selbstzweck.

Die Trennung zum Runtime-Such-MCP ist eine wichtige Sicherheitsgrenze:

| Runtime-Such-MCP | Administratives Profil-MCP |
| --- | --- |
| liest freigegebene Profilversionen | erstellt und bearbeitet Entwürfe |
| sucht Kandidaten read-only | schlägt Zuordnungen vor |
| kann keine Taxonomie ändern | erlaubt manuelle Zuordnung und Korrektur |
| ist für Recruiter gedacht | ist nur für wenige Taxonomie-Verantwortliche gedacht |
| benötigt ausschließlich Suchrechte | benötigt getrennte Schreib- und Freigaberechte |

Die MCP-Spezifikation unterstützt geschützte Server und empfiehlt
Least-Privilege-Scopes. Tokens müssen für den konkreten MCP-Server bestimmt sein
und von diesem als Zielressource validiert werden. Das spricht für getrennte
Ressourcen beziehungsweise Berechtigungsgrenzen für Suche und Verwaltung
([MCP Authorization Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)).

### Empfohlene Admin-Funktionen

Das Verwaltungs-MCP sollte kleine, klar getrennte Werkzeuge anbieten:

- Profile und Profilversionen lesen;
- einen neuen Profilentwurf anlegen oder aus einer Version kopieren;
- kontrollierte Berufs-, Ausbildungs- und Tätigkeitskonzepte suchen;
- Zuordnungsvorschläge mit Quelle, Begründung und Konfidenz erzeugen;
- einzelne Mitglieder manuell hinzufügen, ändern oder entfernen;
- Profilaliase pflegen und auf Mehrdeutigkeit prüfen;
- Entwurf validieren;
- Diff zur letzten freigegebenen Version anzeigen;
- eine unveränderliche Review-Version erzeugen;
- Freigabe durch eine berechtigte Person erfassen;
- Version aktivieren, ersetzen oder archivieren;
- vollständigen Auditverlauf ohne personenbezogene Kandidatendaten anzeigen.

Automatische Vorschläge dürfen nur den Status `proposed` erhalten. Sie dürfen
nie direkt in eine aktive Profilversion gelangen. Vor jedem Write muss das Tool
das konkrete Ziel, die erwartete Ausgangsversion und die Änderung angeben. Für
mutierende Tools ist eine sichtbare Bestätigung erforderlich; die offizielle
MCP-Tools-Spezifikation empfiehlt bei Tool-Aufrufen einen Menschen im Prozess
und verständliche Bestätigungsmöglichkeiten
([MCP Tools Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)).

### Rollen und Rechte

Empfohlene minimale Rollen:

| Rolle | Darf |
| --- | --- |
| Recruiter | suchen, aufgelöste Profile ansehen, Fehler melden |
| Profile editor | Entwürfe und Vorschläge bearbeiten, aber nicht freigeben |
| Profile approver | Diff prüfen und eine Version freigeben |
| Auditor | Versionen, Quellen und Änderungen lesen |
| Service account | nur freigegebene Quelldaten synchronisieren, keine fachliche Freigabe |

**Historische, durch ADR-0003 überholte Empfehlung; keine aktuelle Pflicht:**
Für die erste Version ist ein Vier-Augen-Prinzip empfehlenswert: Die Person oder
Automatisierung, die eine fachlich relevante Zuordnung ändert, darf dieselbe
Version nicht allein freigeben. Mindestens sollten Scopes wie
`profiles:read`, `profiles:draft`, `profiles:review` und `profiles:approve`
getrennt sein. Das Runtime-Such-MCP erhält ausschließlich `profiles:read` auf
freigegebene Versionen und keinerlei Profil-Schreibrecht.

### Erforderliche Sicherheitsregeln

- Admin- und Such-MCP verwenden getrennte Serveridentitäten oder mindestens
  strikt getrennte Zielressourcen und Scopes.
- Der Suchserver akzeptiert keine Admin-Tools und keine Profilmutationen.
- Freigaben sind keine Chatnachricht, sondern serverseitig geprüfte Zustands-
  übergänge mit berechtigtem Akteur, Zeit, Diff und erwarteter Version.
- Optimistische Versionsprüfung verhindert, dass ein älterer Entwurf neuere
  Änderungen überschreibt.
- Jede Mutation besitzt einen eindeutigen Idempotenzschlüssel, damit ein
  unsicherer Netzwerk-Retry keine Doppeländerung erzeugt.
- Auditprotokolle enthalten Profilmetadaten und Änderungsgründe, aber keine
  unnötigen Kandidatendaten oder kompletten CV-Freitexte.
- Import- und KI-Vorschläge laufen im Entwurfsbereich; nur freigegebene,
  unveränderliche Versionen sind für die Suche sichtbar.
- Löschen wird vermieden: Profile und Versionen werden archiviert, damit
  gespeicherte Suchen reproduzierbar bleiben.

### Hauptrisiko des Verwaltungs-MCP

Ein MCP-Werkzeug kann durch einen Agenten aufgerufen werden. Ein zu breites Tool
wie `update_profile(anything)` würde fachliche Fehler, Prompt-Injection und
unübersichtliche Freigaben begünstigen. Kleine typisierte Operationen,
serverseitige Validierung, engste Rechte, Vorschau/Diff und getrennte Freigabe
sind deshalb wichtiger als Komfort. Ein Sprachmodell soll den Editor
unterstützen, nicht zum Taxonomie-Eigentümer werden.

## Governance und Versionierung

### Empfohlener Lebenszyklus

```text
Entwurf → fachliche Prüfung → Freigabe → aktive unveränderliche Version
                                      → später ersetzt/archiviert
```

Änderungen an einem aktiven Profil erzeugen eine neue Version. Bereits
ausgeführte oder gespeicherte Suchen behalten die verwendete Version. Dadurch
bleibt erklärbar, warum dieselbe Texteingabe zu zwei Zeitpunkten verschiedene
Treffer erzeugen konnte.

Eine Profilversion sollte nur veröffentlicht werden, wenn:

- jedes Mitglied eine Quelle und Begründung besitzt;
- keine Pflicht- und Ausschlussregel einander widersprechen;
- alle Profilaliase eindeutig sind;
- Stichprobentests typische Treffer und Fehlzuordnungen abdecken;
- Änderungen gegenüber der vorherigen Version sichtbar sind;
- ein fachlicher Verantwortlicher die Version freigegeben hat.

Amtliche Grundlagen ändern sich ebenfalls. Die KldB-Fassung 2020 ist seit dem
Berichtsjahr 2021 gültig; Berufsbezeichnungen werden in der Online-Ausgabe
aktualisiert. Die Bauausbildungen wurden zum 1. August 2026 neu geordnet, wobei
unter anderem Bezeichnungen im Kanal- und Leitungsbau geändert wurden. Deshalb
sind Quellversionen und Gültigkeitsdaten zwingend
([Bundesagentur für Arbeit, KldB Online-Ausgabe](https://statistik.arbeitsagentur.de/DE/Navigation/Grundlagen/Klassifikationen/Klassifikation-der-Berufe/KldB2010-Fassung2020/Onlineausgabe-KldB-2010-Fassung2020/Onlineausgabe-KldB-2010-Fassung2020-Nav.html),
[BIBB, Neuordnung der Bauwirtschaft](https://www.bibb.de/de/pressemitteilung_218417.php)).

## Suchperformance

Die Profile sind auch für die Geschwindigkeit sinnvoll, wenn ihre Auflösung
nicht bei jeder Suche über Freitext und ein Sprachmodell erfolgt.

Empfohlener Ablauf:

1. Bestandsfreitexte einmalig beziehungsweise inkrementell normalisieren.
2. Freigegebene Zuordnungen als kontrollierte IDs speichern.
3. Profilversionen beim Freigeben in ihre Mitglieds-IDs auflösen.
4. Suchrelevante IDs und Zeitabschnitte passend indizieren.
5. Zur Laufzeit nur die bestätigte Profilversion und die vorbereiteten IDs
   abfragen.

Damit wird die teure semantische Interpretation aus dem eigentlichen Suchlauf
entfernt. Das ist eine technische Schlussfolgerung aus dem Modell und muss nach
dem Schema-Audit mit realistischen Datenmengen durch `EXPLAIN`- und
Lasttests bestätigt werden. ESCO bietet zusätzlich eine lokale API gerade für
höhere Leistung und Unabhängigkeit vom gehosteten Dienst an
([ESCO FAQ, Local API](https://esco.ec.europa.eu/en/about-esco/faq)).

## Hauptrisiken und Gegenmaßnahmen

| Risiko | Auswirkung | Gegenmaßnahme |
| --- | --- | --- |
| Profil ist zu breit | Viele fachlich schwache Treffer | Mitgliedsrollen, Ausschlüsse, Testfälle und sichtbare Vorschau |
| Profil ist zu eng | Passende Kandidaten fehlen | Trefferlücken auswerten, geprüfte Ergänzung als neue Version |
| Ausbildung wird mit Erfahrung verwechselt | Kandidat wirkt erfahrener als belegt | Getrennte Konzeptarten und getrennte Trefferbegründung |
| Freitext wird falsch normalisiert | Falsche Erfahrungsmonate | Originaltext erhalten, Konfidenz, Review und keine sichere Zählung ungeprüfter Fälle |
| Amtliche Begriffe ändern sich | Alte Suchen sind nicht reproduzierbar | Quellen- und Profilversion speichern, Delta-Review durchführen |
| Alias ist mehrdeutig | Falsches Profil wird gewählt | Keine stille Auflösung; Nutzer muss in der Vorschau wählen |
| LLM ändert Mitgliedschaften | Nicht nachvollziehbare Ergebnisse | LLM nur für Vorschläge; Freigabe und Suche serverseitig kontrollieren |
| Profilname wird zur Blackbox | Nutzer versteht Treffer nicht | Vollständige Auflösung und Matchgrund vor Bestätigung anzeigen |
| Profilzuordnung wird exklusiv modelliert | Beruf verschwindet aus anderen Suchen | Viele-zu-viele-Zuordnung; Beruf bleibt direkt suchbar |
| Admin-MCP hat Suchserver-Rechte | Agent kann aktive Suchlogik verändern | Getrennte Serverressource, Scopes, Rollen und Approval |
| Parallele Admin-Änderungen überschreiben sich | Freigegebene Regeln gehen verloren | Erwartete Versionsnummer und Konflikt statt stillem Überschreiben |

## Bewertung der Nutzerbeschreibung

### Was bereits korrekt ist

- Ein kundenverständlicher Profilname kann viele passende Einzelberufe bündeln.
- Dasselbe Profil kann kontrollierte Ausbildungsberufe und normalisierte
  Berufserfahrung berücksichtigen.
- Der Nutzer muss nicht jeden Beruf einzeln kennen oder auswählen.
- Wiederverwendung verbessert Konsistenz und Geschwindigkeit.
- Ein Beruf kann mehreren Profilen angehören und trotzdem einzeln gesucht
  werden.

### Was ergänzt werden muss

- „Alle Berufe im Profil“ genügt nicht: Ausbildung, ausgeübter Beruf und
  Tätigkeit müssen getrennte Mitgliedstypen sein.
- Das Profil braucht klare UND-/ODER-, Pflicht-, Wunsch- und Ausschlussrollen.
- Es braucht Freigabe, Version, Gültigkeit, Quellen und Änderungsverlauf.
- Freitextvarianten gehören in eine eigene Alias-/Normalisierungsschicht.
- Die Filtervorschau muss alle aufgelösten Mitglieder und die
  Erfahrungszeitregel anzeigen.
- Gespeicherte Suchen müssen die konkrete Profilversion referenzieren.

## Empfohlene Entscheidung für Q8.4.2

Das Projekt sollte kontrollierte, wiederverwendbare und versionierte
Berufssuchprofile einführen. Ein Profil:

1. besitzt eine stabile ID und mehrsprachige Namen;
2. bündelt getrennt Ausbildungsberufe, ausgeübte Berufe und Tätigkeiten;
3. referenziert bevorzugt BIBB/KldB als deutsche Grundlage und ESCO für
   Mehrsprachigkeit sowie Tätigkeits-/Skillbeziehungen;
4. verwendet O*NET höchstens ergänzend für fehlende Tätigkeitskonzepte;
5. legt je Mitglied Pflicht, Alternative, Wunsch oder Ausschluss fest;
6. wird fachlich geprüft, versioniert und unveränderlich freigegeben;
7. löst einen Profilnamen vor der Suche vollständig und sichtbar auf;
8. nutzt nur vorab normalisierte und indexierte IDs in der Datenbanksuche;
9. speichert bei Suchverlauf und Export die verwendete Profilversion und den
   Matchgrund;
10. lässt ein Sprachmodell Vorschläge machen, aber keine produktiven
    Mitgliedschaften stillschweigend verändern.
11. verwendet eine Viele-zu-viele-Zuordnung; Konzepte bleiben immer direkt und
    über andere Profile suchbar;
12. historisch optional empfohlen, durch ADR-0003 inzwischen als spätere
    getrennte Komponente geplant: Verwaltungs-MCP mit Entwurf, Diff, Validierung,
    Freigabe, Versionierung und Audit vollständig vom read-only Runtime-Such-MCP.

## Vor der Umsetzung noch zu prüfen

- Welche Ausbildungs- und Beschäftigungsfelder existieren tatsächlich im CRM?
- Sind Beschäftigungen als einzelne Abschnitte mit Start- und Enddatum
  gespeichert?
- Welche Sprachen, Abkürzungen und Tippfehler kommen real im Freitext vor?
- Welche Nutzerrolle darf Profile entwerfen, prüfen, freigeben und archivieren?
- Welche konkreten Prüfprozesse sind mit den derzeit vom Nutzer übernommenen
  Rollen vorgesehen? Eine zweite Person ist gemäß Q6 nicht verpflichtend.
- Welche Profilmitglieder sind für „Tiefbauer“ wirklich Pflicht, Alternative
  oder nur Wunsch?
- Wie wird in Q8.5 die Relevanz von Beruf gegenüber Tätigkeit festgelegt?
- Welche Trefferquote und welche maximal akzeptierte Fehlzuordnungsquote gelten
  für die Normalisierung?

Diese Punkte benötigen den vorgesehenen read-only Schema- und Datenqualitätsaudit.
Die Recherche enthält keine Annahmen über vorhandene Tabellen, Spalten oder
Produktionsdaten.
