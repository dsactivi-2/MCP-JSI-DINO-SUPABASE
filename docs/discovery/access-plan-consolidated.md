# Konsolidierter Discovery-Zugangsplan

Stand: 2026-09-11. Status: **ENTWURF / NO-GO**.
Ziel-Alias: `dino_crm_discovery_target_01`.

## Bootstrap vor der ersten Verbindung

Q10.2a verlangt Audit und Restore vor Produktionsänderungen. Q10.2d nimmt
ausschließlich die beauftragte Leserollenanlage vom vorherigen Restore-Test
aus. Die neue Rolle darf weiterhin nicht als bereits vorhandene Voraussetzung
des eigenen Audits behandelt werden.

Der Nutzer hat am 2026-09-11 bestätigt, dass keine dedizierte Discovery-Rolle
besteht, und ihre Einrichtung beauftragt
([ADR-0002 Q10.2b](../decisions/0002-search-design-interview.md)). Damit ist
Weg 2 gewählt; die Grundsatzentscheidung muss nicht erneut erfragt werden.
Die technischen Ausführungsvoraussetzungen sind weiterhin offen.

1. **Vorhandene passende Identität, nicht gewählt:** Der Nutzer/Operations
   liefert eine
   minimierte Attestation eines bereits existierenden, dedizierten Zugangs.
   Danach werden Zielbindung und B1-Paket neu geprüft. B1 muss die effektiven
   Rechte tatsächlich bestätigen; Dateiexistenz oder Rollenname genügen nicht.
2. **Neue Rolle, beauftragt:** Der Nutzer/Operations lässt zuerst einen separat
   begrenzten
   Owner-Attest über Ziel, Rollen-Bootstrap, PUBLIC-Abhängigkeiten und mögliche
   Auswirkungen prüfen. Dieser Evidenzweg braucht einen eigenen Scope,
   Ausgabeschutz und Freigabe. Er ist kein B1-Lauf mit privilegiertem Login.
   Falls der Attest den verlangten Audit nicht ersetzen kann, bleibt der Weg
   gesperrt; jede Ausnahme von Q10.2a wäre eine neue ausdrückliche Entscheidung.
   Vor Rollenanlage müssen die synthetische Lifecycle-Probe,
   Setup-/Rollback-Preflight und exakte Mutationsfreigabe vorliegen.

Der Nutzer ist derzeit auch Data-, Security-, Privacy- und Operations-Owner.
Er bestätigt Evidenz, Akteur und Scope. Der Agent bereitet nur lokale Entwürfe
vor. Ein scheiternder PUBLIC-Rechtecheck autorisiert weder globale REVOKEs noch
eine Lockerung von B1.

## Restore-Voraussetzung

Laut Nutzer bestehen tägliche Backups, aber kein erfolgreicher Restore-Test
(ADR-0002 Q10.2c, 2026-09-11). Das ist eine Nutzerangabe ohne technische
Verifikation. Q10.2d erlaubt ausdrücklich die Leserollenanlage nach bestandenen
Sicherheitsprüfungen ohne vorherigen Restore-Test. Vor Änderungen an Tabellen
oder Daten bleibt der Restore-Nachweis erforderlich.

Die abgelehnten lokalen SQL-Dump-, OrbStack- und ZIP-Prüfungen bleiben
ausgeschlossen. Für spätere Tabellen-/Datenänderungen ist ein **anderer,
separat freizugebender
Restore-Prüfweg** nötig: Herkunft/Umfang, autorisierter Ausführender, isoliertes
Ziel, Wiederherstellungsschritte, Integritäts-/Mengenprüfung und gemessene
Wiederherstellungszeit. Ein Anbieter-Backupstatus allein belegt keinen Restore.
RTO/RPO und etwaige Storage-Objekte werden ausdrücklich als offen geführt.
Es wird kein gehostetes Staging-Projekt vorausgesetzt oder stillschweigend
bereitgestellt. Ohne zulässiges Ziel und Nachweis bleiben diese späteren
Änderungen NO-GO; der Restore blockiert die reine Rollenanlage nicht mehr.

## Versions- und Evidenzstatus

Der nachfolgende Dashboard-Abgleich am 2026-09-11 hat die Zielbindung inzwischen
aufgelöst: Nach Korrektur durch den Nutzer passt „JSI Base“ exakt zum gespeicherten
Pooler-Benutzernamen. Eine separate lokale Identitätsdatei mit Modus `0600`
bindet `expected_database_role` und `transport_user_sha256`; die vorhandenen
Service-, Credential- und B1-Attestdateien wurden nicht geändert.

Zwei begrenzte Read-only-Vorabprüfungen wurden anschließend ausgeführt. Ergebnis:
PostgreSQL 17, Nicht-Superuser mit CREATEROLE und DB-Ownership; neue Rolle fehlt.
PUBLIC besitzt TEMP sowie ausführbare SECURITY-DEFINER-Funktionen in mindestens
einem für PUBLIC zugänglichen Schema. Keine PUBLIC-Schema-CREATE-, Relations-,
Spalten- oder Sequenzschreibrechte wurden im geprüften Scope gefunden; die
bekannte `pg_settings`-UPDATE-Ausnahme wurde berücksichtigt. Dies ist kein
Beweis, dass die Funktionen Daten verändern: Definitionen wurden nicht gelesen
und Funktionen nicht ausgeführt. Beide Setup-Entwürfe bleiben deshalb NO-GO.
`MAINTAIN` fehlte im ersten Live-Prüffilter; der nachfolgend lokal korrigierte
Check wurde synthetisch geprüft. Sein Produktionszustand bleibt ausdrücklich
offen und wird nicht aus dem früheren Ergebnis abgeleitet.
<!-- markdownlint-disable-next-line MD013 -->
Beleg: [Produktions-Preflight](../reviews/2026-09-11-production-role-preflight.md).

Historischer Vorzustand vor dem erfolgreichen Dashboard-Abgleich:

Der lokale Rollen-Preflight wurde am 2026-09-11 vor der ersten Verbindung
gestoppt: Das vorhandene Zielattest bindet bei der Pooler-Verbindung nur den
gemeinsamen Hostnamen. Es fehlen die unabhängig bestätigte Datenbankrolle
(`expected_database_role`) und der Hash des vollständigen Transportbenutzers
einschließlich Projektzusatz (`transport_user_sha256`). Diese Werte dürfen
nicht aus derselben ungeprüften Service-Datei als eigene Bestätigung erzeugt
werden. Ein Abgleich mit dem richtigen Projekt im Dashboard ist angefragt.
<!-- markdownlint-disable-next-line MD013 -->
Prüfer: [check-role-bootstrap.py](../../scripts/discovery/check-role-bootstrap.py).
Seine einzige spätere Read-only-Verbindung liefert acht Flags/Zahlen zu
Zielidentität, Version, Erstellerrechten, Rollenexistenz und PUBLIC-Datenbank-
CREATE/TEMP. Kein B1-Ersatz, keine Kandidaten- oder Schema-Inhalte. Das vorhandene
TLS `require` wird nicht als kryptografisch verifizierte Serveridentität
ausgegeben. Credential-Inhalte wurden nicht geöffnet.

Die synthetische Rollenprobe lief inzwischen mit PostgreSQL 17.11 erfolgreich
für den Superuser-Pfad. Der separat vorbereitete V2-Entwurf unterstützt im Test
auch den Nicht-Superuser-Ersteller mit genau seinem automatischen ADMIN-only-
Grant; er ersetzt die strengere V1-Mitgliedschaftsregel nicht automatisch.
Details und Grenzen stehen im [Rollenpaket](least-privilege-discovery-role-v1.md).

<!-- markdownlint-disable MD013 -->

| Gegenstand | Belegt | Nicht belegt / Folge |
| --- | --- | --- |
| B1 V1 | Historischer SQL-/Freigabeentwurf. | Nicht erteilt; kein aktueller Lauf. |
| B1 V2 | Vorhandenes SQL, Launcher und Fake-Prozessprüfungen. | Keine Ausführungsfreigabe, keine effektive Rechteprüfung. Kein automatischer nächster Schritt. |
| B1 V3 | Als Nachfolger für eine neue Rolle eingeplant. | Noch kein SQL-/Launcher-/Attestpaket. Erst nach gewähltem Bootstrap und Identität konkret binden und testen. V2 nicht als V3 umetikettieren. |
| Zielattest, Service, Credential-Datei | Früherer lokaler Metadatenpreflight: regulär, symlinkfrei, eigener Nutzer, `0600`. | Inhalte, Zielrichtigkeit und Rollenrechte nicht geprüft. In dieser Runde nicht geöffnet. |
| Freigabeattest | Im früheren Preflight nicht vorhanden. | Keine aktuelle Existenz- oder Inhaltsbehauptung; keine Freigabe erteilt. |
| B2 | Schemaobergrenze `crm`, `crm_api`, `crm_auth`; SQL-Entwurf. | Streammarker, gebundener Launcher, Coverage-Nachweis und eigenes Freigabepaket fehlen. |
| B3 | Sensitiver SQL-Entwurf mit derselben Schemaobergrenze. | Exakte Objektallowlist erst aus B2; Launcher, Marker, Coverage und Freigabe fehlen. |

<!-- markdownlint-enable MD013 -->

## Coverage ist ein eigenes Ergebnis

Jede Query erhält im späteren Manifest: Query-ID, erwarteten Objektumfang,
beobachteten Umfang, Identitätsbindung, Sichtbarkeitsklasse, Sentinelstatus
und offene Lücken. Null Ergebniszeilen sind keine Vollständigkeitsattestation.

- B2-001–005, 007, 009–010: nur struktureller Katalogscope. FK-Ziel- und
  Triggerfunktionsnamen außerhalb des Scopes sind bloße Referenzen; kein
  Zugriff auf Definitionen oder Daten der referenzierten Ziele.
- B2-006/008: `ROLE_VISIBLE_ONLY`. `information_schema` zeigt rollenabhängige
  Grants. Ein separat freigegebener ACL-Katalog-/Owner-Attest muss direkte,
  PUBLIC-, Spalten-, Sequenz-, Schema-, Default- und effektive Rechte sowie
  Rollenvererbung ergänzen. Keine automatischen SELECT-Grants zur Auflösung.
- B2-011: Extensions nur innerhalb der drei Schemas. Benötigte Extensions
  außerhalb davon sind eine explizite Coverage-Lücke und brauchen Nachtrag.
- B2-012/013: nur Publications mit Beziehungen zum Scope; kein globales
  Replikationsinventar. B2-014 prüft Sitzungsschutz, keine fachliche Abdeckung.
- B3-006: `pg_stats` nur für lesbare Tabellen; Abwesenheit kann Rechte oder
  fehlende Analyse bedeuten. Statistik ist außerdem kein aktueller DQ-Zensus.
- B3-001/009 behandeln Policy-Rolle OID 0 als PUBLIC. B3-002 inventarisiert
  View-Sicherheitsflags; B3-011 Funktionsbody und `proconfig`. Diese können
  Secrets/Literale enthalten und brauchen gesonderten Sensitivitätsreview.

B2 beansprucht keinen vollständigen datenbankweiten Audit. Nach seinem Review
wird entschieden, welche weiteren Schemas für Q9 erforderlich sind. Der erste
enge Scope darf den von Q9 verlangten Gesamtinventar-Abschluss nicht
vortäuschen.

## Fehlende Mechanismen und Stopkriterien

<!-- markdownlint-disable-next-line MD013 -->
Die Pakete DISC-04/05 im [Arbeitsplan](../planning/release-1-automation-tickets.md)
müssen je Gate eigene tokengebundene Marker, Queryreihenfolge, CSV-Grenzen,
Zeilen-/Bytebudgets, feste Identität und Zielwerte, Zeitfenster, SQL-/Launcher-
Hashes, eine Verbindung ohne Retry, Prozessgruppenabbruch und minimiertes
Manifest beweisen. B1-Code kann als Ausgangspunkt geprüft werden; seine
Finding-Regel „jede Zeile ist STOP“ ist nicht die B2/B3-Ergebnisregel.

Fehlende/zusätzliche Marker, 5001 Zeilen, Größenüberschreitung, Timeout,
SQL-/Clientfehler, Signal, Identitätswechsel und unvollständige Coverage dürfen
keinen PASS erzeugen. Erst danach ein genauer Freigabetext. Ein neuer Hash
aktualisiert nur die Entwurfsbindung, niemals ein bestehendes Approval.

DQ-Aggregate und Query-Pläne haben eigene objektgebundene Nachträge nach
fachlicher Auswahl. Keine Kandidatenzeilen und keine Anwendungsfunktionen im
B2/B3-Entwurf ausführen. Auch `EXPLAIN ANALYZE` führt den geprüften Query aus;
Funktionen, Last und Ausgaben müssen vorher einzeln zugelassen sein.

## Nächster Freigabepunkt

Der Auftrag zur neuen Rolle und die begrenzte Restore-Ausnahme liegen vor.
Der unabhängige Pooler-/Projektabgleich und die beschränkte Owner-Prüfung sind
erfolgt. Offen ist jetzt ein konkret begrenzter Prüfweg für die öffentlich
aufrufbaren SECURITY-DEFINER-Funktionen und den Umgang mit PUBLIC TEMP. Es gilt
keine Freigabe für pauschale PUBLIC-REVOKEs oder eine Lockerung des Rollen-Gates.
Review der V2-Mitgliedschaftsregel und gebundener Mutationslauncher bleiben
ebenfalls erforderlich. Die synthetischen
Lifecycle-Proben wurden ausgeführt; Passwort-Login und Produktionskompatibilität
sind damit nicht belegt. Danach wird das konkrete Ausführungspaket mit Ziel,
Zeitfenster und bestandenem Preflight zur abschließenden Freigabe vorgelegt.
Der Einrichtungsauftrag ist keine Freigabe für B1, B2 oder B3. Q9 verschiebt
weitere Geschäftsentscheidungen bis nach Discovery.
