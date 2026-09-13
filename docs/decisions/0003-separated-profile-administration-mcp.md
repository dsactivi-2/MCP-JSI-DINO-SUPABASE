# ADR-0003: Getrennter MCP für Berufssuchprofile

Datum: 2026-09-11

Status: Akzeptiert

## Kontext

Berufssuchprofile bündeln kontrollierte Ausbildungsberufe,
Erfahrungsberufe und Tätigkeitsarten. Ihre Pflege verändert die fachliche
Suchlogik für alle späteren Suchen. Der öffentliche Runtime-Such-MCP soll
hingegen ausschließlich validierte Filter ausführen und keine Taxonomie- oder
Profiländerungen erlauben. Eine allgemeine Bestätigung vor jeder neuen oder
geänderten Suche ist in ADR-0002 seit 2026-09-13 `BESTÄTIGT` (Filter zeigen,
dann eine Suche). Q7 verlangt weiterhin Zustimmung zu Lockerungen.

Grundlage dieser Entscheidung sind Q8.4 und Q8.4.2 aus
[ADR-0002](0002-search-design-interview.md) sowie die
[Recherche zu Berufssuchprofilen](../research/berufssuchprofile-q8-4-2.md).

Korrekturhinweis 2026-09-11: Dieser akzeptierte ADR bleibt die geltende
Architekturgrenze. Der Audit konnte die ursprüngliche Zustimmung zu jeder
einzelnen Fähigkeit nicht unabhängig rekonstruieren. Diese historische
Rekonstruktionslücke bleibt `OFFEN`; sie ist keine neue Nutzerbestätigung aller
Details. Die Korrektur der allgemeinen Suchbestätigung ist hier ausdrücklich
vermerkt und verändert nicht die getrennte Freigabe von Profilversionen.

## Entscheidung

Nach dem read-only Discovery und der Freigabe des kanonischen Datenmodells wird
ein eigener interner **Profilverwaltungs-MCP** geplant. Er bleibt technisch und
berechtigungsseitig vom Runtime-Such-MCP getrennt.

Der Profilverwaltungs-MCP muss:

- Profile und neue Profilentwürfe anlegen sowie bestehende Versionen anzeigen;
- kontrollierte Ausbildungsberufe, Erfahrungsberufe und Tätigkeitsarten suchen;
- teilautomatische Mitgliedschafts- und Aliasvorschläge mit Quelle, Begründung
  und Konfidenz erzeugen;
- manuelles Hinzufügen, Entfernen und Korrigieren einzelner Zuordnungen erlauben;
- Namen und eindeutige mehrsprachige Aliase eines Profils pflegen;
- einen vollständigen Diff zur letzten veröffentlichten Version anzeigen;
- Entwürfe serverseitig validieren und widersprüchliche Regeln ablehnen;
- eine getrennte, ausdrückliche Veröffentlichungsbestätigung verlangen;
- jede veröffentlichte Version unveränderlich speichern;
- frühere Versionen ersetzen, wieder aktivieren oder archivieren, aber nicht
  unkontrolliert löschen;
- einen Auditverlauf mit Akteur, Zeitpunkt, Grund und Versionsbezug führen;
- für eine Wirkungsvorschau nur minimierte, aggregierte Trefferzahlen verwenden
  und keine Kandidaten- oder CV-Daten in die Profilpflege kopieren.

Automatische Regeln oder ein Sprachmodell dürfen ausschließlich Vorschläge im
Entwurf erzeugen. Sie dürfen keine aktive Zuordnung oder Profilversion direkt
veröffentlichen.

## Nicht exklusive Profilmitgliedschaft

Profile referenzieren bestehende kontrollierte Konzepte über eine
Viele-zu-viele-Beziehung:

- derselbe Beruf darf mehreren Profilen angehören;
- jedes Konzept bleibt unabhängig vom Profil direkt suchbar;
- das Entfernen aus einem Profil verändert keine anderen Profile;
- das Archivieren eines Profils löscht keine Berufe, Kandidaten oder
  Erfahrungsdaten.

Ein Profil hält Ausbildungsberufe, Erfahrungsberufe und Tätigkeitsarten intern
getrennt. Eine Suche aktiviert nur die Kategorien, die der Nutzer ausdrücklich
genannt hat; nicht genannte Kategorien bleiben inaktiv. Eine generelle
zusätzliche Bestätigung in der Filtervorschau ist ein `VORLÄUFIGER VORSCHLAG`.

## Veröffentlichungsablauf

```text
Entwurf
→ teilautomatische Vorschläge
→ manuelle Prüfung und Korrektur
→ Diff und Validierung
→ ausdrückliche Veröffentlichungsbestätigung
→ aktive unveränderliche Version
→ später ersetzt, reaktiviert oder archiviert
```

Der Nutzer übernimmt derzeit alle fachlichen und technischen Rollen; eine
zweite Person ist gemäß Q6 nicht verpflichtend. Trotzdem bleiben Bearbeitung
und Veröffentlichung getrennte Aktionen. Der Server verlangt für die
Veröffentlichung eine erneute Bestätigung der konkreten Version und ihres
Diffs.

## Grenze zum Runtime-Such-MCP

Der Runtime-Such-MCP:

- besitzt nur Leserechte auf aktive, veröffentlichte Profilversionen;
- bietet keine Werkzeuge zum Anlegen, Ändern oder Veröffentlichen von Profilen;
- bindet eine bestätigte Suche an die angezeigte Profilversion und ihre
  aufgelösten Mitglieder;
- speichert, falls Suchverlauf oder Export später separat freigegeben werden,
  Profilversion und Matchgrund dafür; dies ist keine Freigabe dieser Funktionen;
- schlägt bei geänderter Profilversion eine neue Vorschau vor, statt die
  bestätigte Suche stillschweigend umzudeuten.

Die Bindung an die angezeigte Profilversion und das Verbot stiller Änderungen
bleiben Architekturvorgaben. Die allgemeine Vorschau-/Bestätigungspflicht für
jede Suche ist bis zur Klärung nur `VORLÄUFIGER VORSCHLAG`. Eine bereits erteilte
Bestätigung darf dadurch nicht auf andere Filter oder Versionen übertragen werden.

## Konsequenzen für die Planung

- Der Profilverwaltungs-MCP ist ein eigener geplanter Systembestandteil, aber
  kein Bestandteil des ersten Discovery-Berichts.
- Sein Daten- und Werkzeugvertrag wird erst nach dem Schema- und
  Datenqualitätsaudit finalisiert.
- Jede Umsetzungsplanung muss getrennte Identitäten, Rechte, Deployments,
  Tests, Auditierung und Rollback für Such- und Verwaltungs-MCP berücksichtigen.
- SQL-, Schema- und Teständerungen beider MCP-Grenzen folgen dem automatisierten
  Entwicklungs- und Freigabepfad aus
  [ADR-0004](0004-automated-database-development.md).
- Die Umsetzung darf nicht mit einem allgemeinen Werkzeug wie
  `update_profile(anything)` beginnen; Mutationen benötigen kleine, typisierte
  Operationen und erwartete Versionsnummern.
- Ein Linear-Umsetzungsticket wird erst nach Abschluss des laufenden
  Designinterviews und der finalen Spezifikation erstellt.

## Erneute Prüfung

Die Entscheidung wird nur neu bewertet, wenn das Discovery zeigt, dass keine
laufende Profilpflege erforderlich ist oder eine kontrollierte Admin-Oberfläche
dieselben Sicherheits-, Versions- und Auditgarantien mit deutlich geringerem
Aufwand erfüllt.
