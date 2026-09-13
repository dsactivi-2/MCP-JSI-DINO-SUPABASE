# Lokaler Arbeitsplan: Release 1 und Automatisierung

Datum: 2026-09-11. Status: konsolidierter lokaler Entwurf, **keine
Linear-Writes**.

Der [Anforderungsregister](release-1-requirements.md) ist die zentrale Zuordnung
von Quelle, Pflichtstatus und Abnahme. Frühere AUTO-01–08-Schlüssel bleiben
lokale Arbeitspakete; Testfälle heißen TEST-AUTO-01–03. Laut Audit war Linear
am 2026-09-11 leer; das ist keine erneute Live-Prüfung. Keine erfundenen
Issue-IDs.

## Ablauf und unabhängige Vorbereitung

1. Jetzt: DOC-01, ENV-01/02-Diagnoseplanung, synthetische fachliche Testfälle
   und
   Bootstrap-/Restore-Entwürfe unabhängig lokal vorbereiten. Echte Zugriffe und
   globale Toolreparaturen bleiben separat freigabepflichtig.
2. Zugangskette: DISC-01 → gegebenenfalls DISC-02 → DISC-03 → DISC-04 → DISC-05
   und DISC-06 → AUTO-01. Jede Verbindung hat ihren eigenen geprüften Gate.
3. Q9: nach Discovery DEC-01 für offene Entscheidungen; AUTO-02 überführt den
   Abschluss in den gemeinsamen Vertrag und die explizite Stackauswahl.
   AUTO-02 hat keinen zirkulären Auftrag, seinen eigenen Blocker abzuschließen.
4. Nach Scaffold-Freigabe: AUTO-04 (DB) und AUTO-05 (Fake-MCP) parallel
   vorbereiten; AUTH-01 ebenfalls. Tests nutzen getrennte synthetische Zustände,
   niemals gleichzeitige Resets derselben Datenbank.
5. Früh SEARCH-01 vertikal bis zur Datenbank testen; danach alle SEARCH-02-,
   Profile-, Options- und Admin-Fähigkeiten vollständig ausbauen.
6. Vor Rollout: komplette relevante Suite, Upgrade/Rückschaltung/Restore,
   SLO/Last, Privacy, alle Clients und AUTO-07-Monitoring. REL-01 bleibt
   gesperrt,
   solange ein R1-Kriterium fehlt. Erst separate Freigabe, dann
   Apply/Post-Check.

Kein Anwendungscode oder Stack wird durch diesen Plan ausgewählt. Die
bestehende Interview-/Scaffold-Sperre gilt; die gewünschte formale Entkopplung
späterer Interviewthemen ist [ENTWURF E-01](decision-drafts.md).

## SDK-Integration in diesen Plan

Die [angepasste SDK-Fassung](sdk-integration-plan.md) ergänzt bestehende Pakete
um SDK-01–08. Sie ersetzt die frühere pauschale Empfehlung
„MCP-SDK plus Supabase-Wrapper“ durch einen geprüften Kandidaten: MCP v2,
ein zuständiger MCP-Auth-Adapter und ein getrennt kontrollierter DB-Adapter.
Supabase Server wird nur bei passendem Tokenvertrag gewählt; zusätzliche
Alpha-Middleware muss Nutzen und Kompatibilität belegen.

Quellenrecherche und Dokumentation sind jetzt möglich. Installations-, Auth-,
Transport- und DB-Tests bleiben an AUTO-02/03 und ihre bisherigen Blocker
gebunden. Es entstehen keine zusätzlichen Dienste oder Linear-Tickets allein
aufgrund verfügbarer SDKs.

## Pakete mit Owner, Blockern und Evidenz

Die angegebenen Rollen werden derzeit vom Nutzer übernommen. Die verlinkten
REQ-Kriterien sind pro Paket verbindliche Abnahme; ein Paket ohne zugehörigen
Evidenzbericht ist nicht erledigt. Bereiche in REQ-IDs meinen alle Einträge
innerhalb dieser Gruppe. Diese Tabelle ersetzt keinen ausführbaren Test.

<!-- markdownlint-disable MD013 -->

| Paket | Verantwortlich | Blockiert durch | Liefergegenstand / überprüfbare Abnahme | Anforderungen | Status |
| --- | --- | --- | --- | --- | --- |
| GOV-01 | Product/Privacy/Security | Keine | Nur Discovery-Sicherheits-/Privacy-Scope und ausführender Akteur; keine vorgezogene Alters-/Suchentscheidung | REQ-GOV-01 | VORZUBEREITEN; Nutzerentscheidungen offen |
| ENV-01 | Operations | Keine | CLI-Diagnose: Sandbox-Telemetriefehler getrennt von Installation; reproduzierbare Version/Help-Prüfung ohne globale Reparatur | REQ-AUTO-01 | Lokale Diagnose als eigener Ticketentwurf |
| ENV-02 | Operations | Keine | Promptfoo-Diagnose: dokumentierter better-sqlite3 ABI-Konflikt, Lösung/Versionen erst separat freigeben; vor Pflichtnutzung erfolgreicher synthetischer Lauf | REQ-LANG-01, REQ-AUTO-03 | Lokale Diagnose als eigener Ticketentwurf |
| DOC-01 | Data/Discovery | Keine | Dokument-, Link-, ID- und Scope-Prüfbericht; lokale Vorbereitung ohne Datenzugriff | REQ-DISC-01–06 | In dieser Korrekturrunde vorbereitet |
| DISC-01 | Operations/Security | GOV-01 | Bootstrap-Evidenzplan aus access-plan-consolidated; neue Rolle beauftragt, begrenzte Restore-Ausnahme Q10.2d; Ziel-/Owner-Nachweis | REQ-DISC-01 | TEILWEISE; Entscheidung bestätigt, Evidenz offen |
| DISC-02 | Operations/Security | DISC-01 | Setup-/Rollback-Probe im gemäß Q10.2e erlaubten synthetischen Container; target/hash/actor/mutation preflight; Restore-Ausnahme nur für Rollenanlage | REQ-DISC-02 | Synthetisch V1 12 / V2 16 Prüfungen; Ziel-/Owner-Nachweis, V2-Review und gebundenes Ausführungspaket offen |
| DISC-03 | Discovery/Security | DISC-01; DISC-02 bei neuer Rolle | B1-Identitätsvertrag: V2 nur nach neuem Review vorhandener Identität, V3 eigenes Paket für neue Rolle; Fake-Protokoll und minimiertes echtes Manifest | REQ-DISC-03 | BLOCKED bis Evidenz und separate Freigabe |
| DISC-04 | Discovery/Security | DISC-03 | B2-Marker/Launcher/Tests/Hash-Freigabe, per-query Coverage und redigierter Strukturbericht; Rechteattest als eigener Scope | REQ-DISC-04 | SQL-Entwurf; Mechanismen und Lauf offen |
| DISC-05 | Discovery/Security | DISC-04 | B3-Objektallowlist, sensitiver Outputreview, Marker/Launcher/Tests/Freigabe und redigierte Definitionsbefunde | REQ-DISC-05 | DRAFT / BLOCKED |
| DISC-06 | Data/Discovery | DISC-04, DISC-05 | Relevante Objekte wählen; eigene DQ-/EXPLAIN-Gates, genehmigte Last, aggregierter Qualitäts- und Planbericht; globale Scope-Lücken schließen | REQ-DISC-06 | DISCOVERY NÖTIG |
| AUTO-01 | Discovery/Data | DISC-03, DISC-04, DISC-05, DISC-06 | Abgenommener vollständiger Discovery-Bericht mit Fakten/Annahmen/Coverage; kein eigener Sammellauf aller Gates | REQ-DISC-03–06 | BLOCKED |
| DEC-01 | Product/Data/Security | AUTO-01 | Verbleibendes Interview gemäß Q9 abschließen; Q8.5, Q4.5, Operatoren, Auth, Alter, Ranking, Betrieb entscheiden; Quellen sofort in ADR-0002 erfassen | REQ-CONTRACT-01, REQ-FILTER-01 | OFFEN; E-01 nicht vorausgesetzt |
| AUTO-02 | Product/Data/Security | DEC-01 | Gemeinsamer JSON/MCP/RPC/Error/Cursor-Vertrag; Stack/Hosting und SDK-01-Auswahl mit Protokollgeneration, Alpha-Abwägung und Token-/Adaptervertrag; Freigabe | REQ-CONTRACT-01, REQ-SDK-01 | BLOCKED |
| AUTO-03 | Operations | AUTO-02, ENV-01 | Isolierter lokaler Scaffold, gepinnte Runtime/CLI/Images/SDKs und Dependency-Lockfile (SDK-01/08), synthetische Seeds; getestete lokale Zielbindung; keine gehostete Stagingpflicht | REQ-AUTO-01, REQ-SDK-01 | BLOCKED |
| DATA-01 | Data | AUTO-02, AUTO-03 | D-kompatibler additiver Modell-/Migrationsentwurf mit lineage; erste Implementierungsmigration erst nach AUTO-04-Gates | REQ-MODEL-01 | BLOCKED |
| TAX-01 | Data/Product | DATA-01 | Versionierter Taxonomie-/Profilvertrag und multilingualer Referenzsatz; nicht exklusive Mitgliedschaften und direkt suchbare Konzepte | REQ-TAX-01, REQ-PROF-01 | BLOCKED |
| AUTO-04 | Data/Security | AUTO-03 | Gemeinsamer lokaler/CI-DB-Gate: lint nonzero, pgTAP, Negativkontrollen, Frischaufbau, Upgrade und Rückschaltung; Katalogassertions statt nur Schema-Diff | REQ-AUTO-02 | BLOCKED |
| AUTO-05 | Security/Product | AUTO-02, AUTO-03 | MCP-Fake-Adapter/Contract- und Injection-Gates parallel zu AUTO-04; SDK-04: Schemas/Typen und minimierte Ausgaben; Promptfoo nur nach ENV-02-Nachweis | REQ-AUTO-03, REQ-INJECT-01, REQ-SDK-01 | BLOCKED; Integration benötigt AUTO-04 |
| AUTH-01 | Security | AUTO-02, AUTO-03 | SDK-02/03: MCP issuer/audience/scope, OAuth metadata, getrennte Downstream-Credentials und parallele Kontextisolation im bestätigten Identitätsvertrag; Client-Matrix | REQ-AUTH-01, REQ-TRANSPORT-01, REQ-SDK-01 | BLOCKED |
| AUTH-02 | Security/Privacy | AUTH-01, DATA-01, AUTO-04, AUTO-05 | DB-Rechte/RLS/Views/Routinen und sämtliche Ausgabewege negativ prüfen; Kontakt-Projektion nach Q4 und stored injection | REQ-AUTH-02, REQ-CONTACT-01, REQ-INJECT-01, REQ-ACCESS-REV-01 | BLOCKED |
| SEARCH-01 | Data/Security | DATA-01, TAX-01, AUTH-01, AUTO-04, AUTO-05 | Ein durchgängiger Suchfall bis zur tatsächlichen DB-Autorisierung/RPC und MCP-Ausgabe, mit einem negativen Rechtefall | REQ-SEARCH-01 | BLOCKED; Durchstich ist noch kein Release |
| SEARCH-02 | Product/Data | SEARCH-01 | Alle bestätigten Filter und Randfälle, fachlich unabhängige BS/DE/EN-Sollwerte, zero/relaxation, DB-Ranking, evidence und signed cursor | REQ-FILTER-01–03, REQ-LANG-01, REQ-SEARCH-02, REQ-RANK-01, REQ-PAGE-01, REQ-ADMIN-05 | BLOCKED |
| TOOL-02 | Product/Security | DATA-01, AUTH-01, AUTO-05 | Eigenständiger Profile-Tool-Vertrag und Adapter; ein autorisierter Kandidat mit Q4-Projektion, missing/denied ohne Existenzleck | REQ-TOOL-02 | BLOCKED; parallel zu SEARCH-02 |
| TOOL-03 | Product/Data | TAX-01, AUTH-01, AUTO-05 | Eigenständiger Options-Tool-Vertrag und Adapter; begrenzte kontrollierte IDs/Profile und validiertes field/query | REQ-TOOL-03 | BLOCKED; parallel zu SEARCH-02 |
| ADMIN-01 | Security/Operations | AUTO-02, AUTO-03, AUTO-05 | Getrennte MCP-Identität/Deploy-/Rechte-/Audit-/Rollback-Grenze; kleine typisierte Operationen und expected version | REQ-ADMIN-01 | BLOCKED |
| ADMIN-02 | Product/Data | ADMIN-01, TAX-01, AUTO-04 | Draft-/Versionslesen, Begriffssuche, manuelle Korrekturen, Aliaspflege und quellbelegte Vorschläge; aggregierte Vorschau | REQ-ADMIN-02/03 | BLOCKED |
| ADMIN-03 | Product/Security | ADMIN-02 | Diff/Validierung/publish confirmation/immutable versions, reactivation/archive/audit und Runtime-Versionstreue | REQ-ADMIN-04/05 | BLOCKED |
| PRIV-01 | Privacy/Data | GOV-01, AUTO-02 | Rechts-/Datenschutzentscheidung, Retention, purpose/consent und nachweisbare Lösch-/Korrekturpropagation aller vorhandenen Schichten | REQ-PRIV-01, REQ-PRIV-03 | BLOCKED |
| OPS-01 | Operations/Security | AUTO-03, AUTO-05 | SDK-05/06: versionsgerechter HTTP/SSE-/Proxy-/Body-Test, timeout/cancel/rate/concurrency/backpressure/size und sichere Fehler; Health-/Readiness-Vertrag | REQ-LIMIT-01, REQ-TRANSPORT-01, REQ-SDK-01 | BLOCKED |
| OPS-02 | Operations/Privacy | AUTO-03, AUTO-05 | PII-freies Logging/Tracing/Audit, Retention und Zugriffsprüfung; versionierte Metrikdefinitionen | REQ-PRIV-02, REQ-TRANSPORT-01 | BLOCKED |
| OPS-03 | Operations/Data | AUTO-04, GOV-01 | Separat genehmigter echter Restore-Prüfweg mit Integrität und RTO/RPO; Rückschaltung zusätzlich testen; keine abgelehnten Backupartefakte | REQ-RESTORE-01 | BLOCKED; vor Tabellen-/Datenänderungen weiterhin Pflicht |
| AUTO-06 | Operations/Data | SEARCH-02, TOOL-02, TOOL-03, ADMIN-03, AUTH-02, OPS-01 | Vorab numerische SLO-/Kosten-/Ressourcengrenzen, repräsentative Plan-/Last-/Soakprüfung, explizite Index-Nutzenentscheidung | REQ-PERF-01, REQ-INDEX-01 | BLOCKED |
| AUTO-07 | Operations | OPS-01, OPS-02, AUTO-06 | Vor Rollout getestete Dashboards/Minimalalarme, Incident-/On-call-/Mitigation-Runbook; kein automatischer DB-Fix | REQ-OPS-01, REQ-ACCESS-REV-01 | BLOCKED; keine Abhängigkeit von Rollout |
| CLIENT-01 | Product/Security | SEARCH-02, TOOL-02, TOOL-03, AUTH-02, OPS-01 | Alle fünf Zielclients gegen identische Eingabe/Ausgabe/Auth/Cursor/Error/Timeout/PII-/Zugänglichkeitskriterien; SDK-05/08: explizite Protokollmatrix und Upgrade-Kompatibilität | REQ-CLIENT-01, REQ-CONTACT-01, REQ-PRIV-03, REQ-SDK-01 | BLOCKED |
| REL-01 | Operations/Product/Security | AUTO-06, AUTO-07, CLIENT-01, PRIV-01, OPS-03, ADMIN-03 | Vollständige R1-Matrix, dry-run, upgrade, Rückschaltung, Restore, genaue Diff-/Zielbindung; separate Freigabe, Pilot, Post-Checks und Beobachtungsfenster | REQ-RELEASE-01, REQ-SDK-01 | BLOCKED |
| MIG-D-01 | Data/Operations | REL-01 | Weitere kleine D-Schnitte: lineage/ID-/Mengengleichheit, RLS/contract/cutover/rollback; Quellarchivierung erst separat | REQ-D-01 | SPÄTER |
| AUTO-08 | Operations/Data | AUTO-07; 4–8 Wochen repräsentativer Workload | Optionaler pganalyze-Vergleich mit Nutzen/Kosten/Exit-Kriterium; E-02 ist unbeschlossener Ersatzvorschlag | REQ-OPT-02 | OPTIONAL |
| OPT-01 | Product/Privacy | DEC-01; separate spätere Freigabe | Kontakte, Export, Verlauf, gespeicherte Suchen und Benachrichtigungen jeweils eigenständig spezifizieren und prüfen | REQ-OPT-01 | AUSSERHALB R1 |
| OPT-02 | Product/Data | Messbarer Bedarf; separate Freigabe | Vektor-/Cache-/Replika-/Search-Evaluation gegen native baseline, Qualität, Recall bei ANN, Lifecycle, Kosten und Rückbau | REQ-OPT-02 | OPTIONAL; kein R1-Blocker |

<!-- markdownlint-enable MD013 -->

## Gemeinsame Verträge, unabhängige Sollwerte

AUTO-02 benennt einen kanonischen versionierten Vertragssatz für Eingabe,
Ausgabe, Fehler und Cursor. AUTO-05 erzeugt daraus Schemas, Validatoren,
freigegebene Typen und Dokumentauszüge; CI prüft driftfrei wiederholte
Erzeugung.
Fachliche erwartete Filter, Kandidaten-IDs, Reihenfolgen und Rechte stammen aus
separat von Product/Data geprüften synthetischen Fällen. Generator und
Implementierung dürfen nicht ihr einziges eigenes Testorakel liefern.

Kurze lokale Auswahl dient der Entwicklung. Vor Abnahme läuft der gemeinsame
vollständige relevante Gate mit zuverlässigem Nonzero-Exit für FAIL, fehlende
Pflichtprüfungen oder unakzeptierte Gaps. Das spätere DB-Verfahren steht im
[Automatisierungsrunbook](../runbooks/database-development-automation.md).

## Linear preflight

Erst nach dem geltenden Interview-/Spezifikationsgate und einer separaten
Linear-Freigabe: nativen Connector read-only auf Projekt/Team/Duplikate prüfen,
konkrete Titel/Owner/Status/kanonische Labels/Prioritäten und Blocking-Kanten
vorlegen. Danach ausschließlich bestätigte Pakete anlegen und echte IDs
zurückführen. Keine automatische Anlage aus diesem lokalen Dokument.
