# Korrekturmatrix A01–A12

Stand: 2026-09-11 (Korrekturrunde). Live-Status nicht hier, sondern in
ADR-0002 und docs/project.md. Arbeitsgrundlage ist der
[Audit](../reviews/2026-09-11-project-plan-audit.md) mit seiner
[Primärprüfung](../research/2026-09-11-plan-best-practice-verification.md).
Historische Berichte bleiben unverändert. Alle Änderungen dieser Runde sind
lokal; kein Hash und kein Status ersetzt eine Ausführungsfreigabe.

## Maßnahmen und Abschluss

Die Statusspalte enthält den Abschlussstand nach Korrektur und Verifikation.
`BEHOBEN` bezeichnet den lokalen Befund, keine implementierte Releasefunktion.

<!-- markdownlint-disable MD013 -->

| Befund | Maßnahme | Abhängigkeit | Prüfverfahren | Status |
| --- | --- | --- | --- | --- |
| A01 | Neue Rolle beauftragt; begrenzte Restore-Ausnahme Q10.2d bestätigt. Ziel-/Owner-Attest und Sicherheitsprüfungen bleiben offen; keine privilegierte Ersatzverbindung. | Q10.2b/d/e; gebundenes Ausführungspaket. | Review der Zugangskette, synthetischer Lifecycle und Stopkriterien. | TEILWEISE |
| A02 | `current_user` korrigieren; ausschließlich eigenen CONNECT-Grant vor DROP widerrufen; unerwartete Abhängigkeiten stoppen. | Eindeutig isolierter synthetischer PostgreSQL-Test. | Bestehende statische Checks; echte Setup-/Abbruch-/Rollback-Zustände bleiben offen. | TEILWEISE |
| A03 | Rollenabhängige Sichtbarkeit in SQL und Coverage-Vertrag kennzeichnen, Vollständigkeitsattest separat planen. | B1, B2 und bewilligter Metadaten-Evidenzweg. | SQL-Review, Hashbindung; beobachtbare Rechte-/Coverage-Probe nach Freigabe. | DISCOVERY NÖTIG |
| A04 | Drei bedeutungsgleiche Sprachbeispiele plus Weglassungsfall mit unabhängigem fachlichem Soll. | Taxonomie und Q8.5 erst nach Discovery finalisieren. | Manueller Vergleich der genannten Kategorien und Sollwerte. | BEHOBEN |
| A05 | B1 V1/V2/V3, Dateiexistenz, Inhalt, Rechte und Freigabe getrennt synchronisieren. | Keine Live-Prüfung. | Quervergleich Status, Karte, Rollenpaket und Preflight. | BEHOBEN |
| A06 | B3-Schemaobergrenze, PUBLIC und sicherheitsrelevante Definitionen korrigieren; fehlende B2/B3-Mechanismen und DQ/Plan-Gates als Pakete erfassen. | B2-Objektinventar und separate Gates. | Statischer Review; keine ausführbare B2/B3-Pipeline behaupten. | DISCOVERY NÖTIG |
| A07 | Pflichtstatus vereinheitlichen; optionale Werkzeuge von verpflichtendem Ergebnis trennen. | Keine neue fachliche Entscheidung. | Brief gegen Anforderungsregister und Abnahmekriterien. | BEHOBEN |
| A08 | Vollständiges Register und lokale Pakete mit Owner, Evidenz, Abhängigkeiten und Abnahme; separate Tooldiagnose. | Implementierungs-/Linear-Gates bleiben bestehen. | Vollständigkeit, eindeutige Kennungen und zyklenfreier Plan. | BEHOBEN |
| A09 | Verlässliche Exitcodes, negative Kontrollen, Frischaufbau/Upgrade, Rückschaltung/Restore und Monitoring vor Rollout präzisieren. | Späterer genehmigter Scaffold. | Runbook-/Ticketreview, lokaler Dokument-/Fake-Testlauf. | BEHOBEN |
| A10 | Working Tree als Default einschließlich neuer Dateien; Index explizit; Fragmente exakt prüfen. | Synthetischer Dateibaum. | Red/Green-Verhaltenstests, beide Prüfmodi. | BEHOBEN |
| A11 | Zeitbezogene Toolbefunde und strengere Projektgrenze klarstellen. | Vorhandene Auditprimärquellen. | Aktive Angaben gegen Audit/Projektregeln prüfen. | BEHOBEN |
| A12 | Endpoint durch Alias ersetzen; aktive Dokumente formatieren; historische Beweise bewahren. | Keine Historienbereinigung. | Markdownlint, Link-/Fragmentprüfung, Diff-Whitespace, Snapshotvergleich. | BEHOBEN |

<!-- markdownlint-enable MD013 -->

## Verbindliche Grenzen

Stand dieser Runde 2026-09-11: Q8.5 vollständig `OFFEN`, Q4.5 ohne
erfundene Frage, allgemeine Suchbestätigung `VORLÄUFIGER VORSCHLAG`.
Live 2026-09-13 in ADR-0002: Q8.5.3–9 `BESTÄTIGT`, Bestätigung vor jeder
Suche `BESTÄTIGT`; Q7 vor Lockerung bleibt. Änderungsvorschläge an
akzeptierten ADRs stehen separat unter
[Entscheidungsentwürfe](decision-drafts.md).

Der Abschlussnachweis dieser Runde steht im
[Prüfbericht](../reviews/2026-09-11-local-correction-verification.md).

## Ergebnisgrenzen

A09 ist als konkrete Planung korrigiert; der spätere DB-/CI-Scaffold ist noch
nicht implementiert. A12 gilt für aktive Dokumente und Endpoint-Alias; die
historischen Auditbelege bleiben byteidentisch und behalten ihren dokumentierten
Formatbedarf. Vollständiges Git-Whitespace ist durch eine fremde Skilländerung
außerhalb dieses Diffs rot. Diese Grenzen stehen im Prüfbericht und werden
nicht zu PASS umgedeutet.
