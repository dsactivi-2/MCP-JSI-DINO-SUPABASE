# Entscheidungsentwürfe zur Planverkürzung

Stand: 2026-09-11. **ENTWURF / NICHT BESCHLOSSEN**.
Die akzeptierten ADR-Texte bleiben maßgeblich. Diese Vorschläge heben keine
heutige Sperre auf und verlangen keine Entscheidung über Q8.5 vor Discovery.

## ENTWURF E-01: Releasebezogener Interviewabschluss

Betroffen: [ADR-0002](../decisions/0002-search-design-interview.md), Abschnitt
„Abschluss des Interviews“, und der daran gebundene Ticket-/Scaffold-Gate.

Vorgeschlagener Ersatz: Der Nutzer kann nach Discovery den Release-1-Vertrag
bestätigen, wenn alle R1-relevanten Fragen beantwortet sind und jede übrige
Frage ausdrücklich einer späteren Phase zugeordnet ist. Kontakt, Export,
gespeicherte Suchen und optionale Vektoren bleiben in einer eigenen offenen
Liste. Q4.5 muss zunächst als Frage identifiziert und eingeordnet werden;
Q8.5, Filtersemantik, Auth, Altersausgestaltung und R1-Betrieb bleiben Blocker.

Auswirkung: spätere optionale Funktionen blockieren R1 nicht durch ihre
Detailplanung. Risiko: eine scheinbar optionale Frage betrifft doch R1;
deshalb muss jede Verschiebung im Anforderungsregister begründet werden.
Bis zur ausdrücklichen Annahme gilt weiter der vollständige Interviewabschluss.

## ENTWURF E-02: Workload statt fester Wartezeit

Betroffen: [ADR-0004](../decisions/0004-automated-database-development.md),
Abschnitt „Izbor dodatnih alata“, erster Punkt.

Vorgeschlagener Ersatz: pganalyze nur evaluieren, wenn ein repräsentativer,
dokumentierter Workload eine mit nativen Werkzeugen nicht ausreichend lösbare
Diagnose- oder Performance-Lücke zeigt. Vor dem POC werden Nutzen, Zeitaufwand,
Kosten, Datenschutz, Abbruch und Rückbaukriterien festgelegt; behalten nur bei
gemessenem Mehrwert. Keine allein kalendarisch ausgelöste Evaluation.

Auswirkung: die feste Wartezeit von vier bis acht Wochen entfällt. Risiko:
frühe unrepräsentative Messungen; Gegenmaßnahme ist ein vorab geprüftes
Workload-Profil mit realistischen Selektivitäten und Lastspitzen.
Bis zur Annahme bleiben vier bis acht Wochen **und** Nutzenbeleg erforderlich.

## Bereits ohne ADR-Änderung planbar

Ein gemeinsamer Vertragssatz, unabhängige Testvorbereitungen, frühe vertikale
Integration, gemeinsame lokale/CI-Prüfläufe, getrennte Frischaufbau-/Upgrade-
Nachweise und Monitoring vor Rollout konkretisieren bestehende Anforderungen.
Sie ändern keine fachliche Suchregel und streichen keinen Release-1-Nachweis.
