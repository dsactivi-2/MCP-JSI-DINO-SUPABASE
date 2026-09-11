# Supabase-Plugin Read-only Gate P

Gate-Familie: `DISCOVERY-PLUGIN-GATE-P`

Ziel-Alias: **dino_crm_discovery_target_01**

Status: **DRAFT / NO-GO**

Stand: 2026-09-11

Dieser Entwurf definiert die Voraussetzungen für einen möglichen internen
Discovery-Zugriff über den Supabase-Plugin/MCP. Er erteilt keine Freigabe für
einen Projekt-, Schema-, Log-, Advisor-, SQL- oder Datenzugriff.

Der Nutzer hat am 2026-09-11 bestätigt, dass die Codex-App-Berechtigung auf
`Always ask` gestellt wurde. Diese Bestätigung erfüllt nur die manuelle
Bestätigungsschicht. Sie beweist weder Projektbindung noch Read-only-Ausführung
oder Datenschutzgrenzen.

Der Nutzer hat außerdem bestätigt, dass das Ziel ein Produktionsprojekt mit
echten Kandidatendaten ist. Damit ist eine direkte Verbindung des Supabase-
Entwickler-Plugins zu diesem Projekt nach der aktuellen Sicherheitsregel
ausgeschlossen. Der Entwurf kann nur mit einem getrennten Development- oder
Testprojekt ohne echte Personendaten fortgesetzt werden.

## 1. Zweck und Abgrenzung

Der Gate-Entwurf soll klären, ob der Supabase-Plugin später einen eng
begrenzten, internen Metadatenzugriff unterstützen kann. Er ersetzt nicht:

- den bestehenden, lokal getesteten `psql`-Gate-B-Pfad;
- den zukünftigen Runtime-Such-MCP;
- den getrennten Profilverwaltungs-MCP;
- eine Datenschutz-, Zielsystem- oder Produktionsfreigabe.

Bis alle Pflichtprüfungen bestanden und der exakte erste Tool-Call separat
freigegeben wurden, bleibt ausschließlich das öffentliche Tool `search_docs`
zulässig.

## 2. Statisch bestätigte Ausgangslage

Die offizielle Supabase-MCP-Dokumentation unterstützt diese Parameter:

<!-- markdownlint-disable MD013 -->

| Parameter | Zweck |
| --- | --- |
| `project_ref=<id>` | Bindet den MCP an genau ein Projekt und deaktiviert Account-Werkzeuge. |
| `read_only=true` | Führt SQL über einen Read-only-PostgreSQL-Nutzer aus. |
| `features=<groups>` | Aktiviert nur die genannten Tool-Gruppen. |

<!-- markdownlint-enable MD013 -->

Nicht ausführbare Zielvorlage für einen späteren, separat konfigurierten MCP:

```text
https://mcp.supabase.com/mcp?project_ref=${SUPABASE_PROJECT_REF}&read_only=true&features=database,docs
```

`SUPABASE_PROJECT_REF` muss ausschließlich aus einer lokalen, nicht
versionierten Konfiguration kommen. Der tatsächliche Wert darf weder im
Repository noch im Chat oder Bericht erscheinen.

Der aktuell sichtbare Codex-Connector verlangt dagegen bei Projektwerkzeugen
weiterhin ein `project_id`-Argument und bietet breite Account- und
Schreibwerkzeuge an, darunter Projekt-, Branch-, Migration- und
Edge-Function-Aktionen. Damit ist seine statische Tool-Oberfläche derzeit nicht
als projektgebunden und read-only nachgewiesen.

## 3. Wichtige Bedeutung von Read-only

`read_only=true` verhindert Schreiboperationen auf PostgreSQL-Ebene. Es
begrenzt nicht automatisch, welche lesbaren Zeilen oder sensiblen Inhalte eine
Abfrage zurückgeben kann. Der von Supabase beschriebene Read-only-Nutzer besitzt
breite Leserechte.

Deshalb bleiben auch in einem technisch read-only Connector verboten:

- Kandidatenzeilen oder Kandidatenlisten;
- Kontakt-, CV-, Geburts- oder Freitextdaten;
- `select *` und ungebundene Abfragen;
- Secrets, Schlüssel und private URLs;
- breite Definitionen, Logs oder Statistiken ohne eigene Freigabestufe.

Read-only ist eine Schreibschutzschicht, keine PII- oder Mandantengrenze.

## 4. Pflichtprüfungen vor dem ersten Live-Aufruf

<!-- markdownlint-disable MD013 -->

| ID | Prüfung | PASS-Bedingung | Aktueller Status |
| --- | --- | --- | --- |
| PG-00 | Manuelle Bestätigung | Codex steht auf `Always ask`; jeder Tool-Call wird vor Ausführung geprüft. | USER-ATTESTED PASS |
| PG-01 | Kein vorzeitiger Zugriff | Entwurf und Prüfung verwenden nur lokale Dateien, Tool-Schemas und öffentliche Dokumentation. | PASS |
| PG-02 | Eindeutiger Connector | Genau eine aktive, für dieses Gate benannte Verbindung ist ausgewählt; doppelte Plugin-Distributionen gelten nicht als zwei Schutzschichten. | BLOCKED |
| PG-03 | Projektbindung | `project_ref` stammt aus einem lokalen Attest und Account-Werkzeuge sind im resultierenden Tool-Katalog nicht verfügbar. | BLOCKED |
| PG-04 | Read-only-Nachweis | `read_only=true` ist in der effektiven Verbindung attestiert; Mutationswerkzeuge sind nicht verfügbar. | BLOCKED |
| PG-05 | Minimale Features | Erste Stufe enthält ausschließlich `database,docs`; alle anderen Gruppen sind deaktiviert. | BLOCKED |
| PG-06 | Zielklassifikation | Getrenntes Development-/Testprojekt ohne echte Personen. | FAIL / BLOCKED – Ziel ist Produktion mit echten Kandidatendaten. |
| PG-07 | Output-Grenze | Exakter Tool-Call, Schemafilter, Detailmodus, erwartete Maximalgröße, Redaktionsweg und Speicherort sind vorab festgelegt. | BLOCKED |
| PG-08 | Identität und Rechte | OAuth-Benutzer, Organisation, Ziel-Alias und wirksamer DB-Kontext sind geprüft; keine Owner-, Migration-, Superuser- oder BYPASSRLS-Nutzung. | BLOCKED |
| PG-09 | Abschließende Freigabe | Nutzer genehmigt den vollständigen Gate-Stand und genau einen ersten Tool-Call in einer neuen Nachricht. | NICHT ERTEILT |

<!-- markdownlint-enable MD013 -->

Gesamtbewertung: **NO-GO**. `PG-00` allein entsperrt keinen Live-Zugriff. Wegen
`PG-06` darf der Plugin nicht direkt mit dem bestätigten Produktionsprojekt
verbunden werden.

## 5. Tool-Allowlist nach Stufen

### P0 – öffentliche Dokumentation

Ohne weitere Freigabe zulässig:

- `search_docs` mit einer öffentlichen Dokumentationsfrage.

### P1 – erster möglicher Verbindungsnachweis

Erst nach `PG-02` bis `PG-08` und einer neuen ausdrücklichen Freigabe darf ein
einziger kleiner Smoke-Test gegen ein getrenntes Development- oder Testprojekt
ohne echte Personendaten geplant werden. Bevorzugter Kandidat ist
`list_extensions`, weil er keine Kandidatenzeilen lesen soll. Der exakte
Tool-Call muss vorher angezeigt werden; dieser Entwurf autorisiert ihn nicht.

### P2 – kompakte Strukturmetadaten

Erst nach PASS und Review von P1 separat freigebbar:

- `list_tables` nur mit einer ausdrücklich genehmigten Schemaliste;
- `verbose=false`;
- keine automatische Fortsetzung mit weiteren Tools;
- keine Ausgabe in Repositorydateien vor Redaktionsprüfung.

`list_tables` besitzt keinen eigenen Ergebnis-Limitparameter. Falls die
erwartete Objektmenge oder sichere Ausgabegrenze nicht vorab belastbar bestimmt
werden kann, bleibt P2 gesperrt und Gate B über den lokalen Launcher ist zu
verwenden.

### P3 – weitere Metadaten

Je Tool separat und erst nach Review der vorherigen Stufe freigebbar:

- `list_migrations`;
- Security- oder Performance-Advisors;
- zusätzliche Schemas oder verbose Tabellenmetadaten.

Advisor- und Migrationsausgaben können interne Objekt- und Funktionsnamen
enthalten und dürfen nicht automatisch in Chat, Git oder Folgetools übernommen
werden.

### Nicht durch diesen Entwurf freigegeben

- `execute_sql`, auch für `SELECT`;
- alle Migration-, Projekt-, Branch-, Edge-Function- und Storage-Mutationen;
- `get_publishable_keys` und unnötige Projekt-URL-Abfragen;
- Account-weites Auflisten von Organisationen oder Projekten;
- Logs, Kandidaten-, Kontakt-, CV- oder andere personenbezogene Inhalte;
- automatische Retries oder Wechsel auf einen zweiten Connector nach einem
  unsicheren Ergebnis.

`execute_sql` kann erst in einer späteren Gate-Version erwogen werden, wenn jede
Abfrage exakt gehasht, statisch geprüft und mit einer nachweisbaren Ergebnis-
und Output-Grenze versehen ist. Die vorhandene Gate-B-SQL-Freigabe überträgt
sich nicht auf den Plugin.

## 6. Fail-closed Stop-Kriterien

Sofortiger STOP gilt, wenn mindestens eine Bedingung eintritt:

- die effektive Verbindung zeigt weiterhin Account- oder Mutationswerkzeuge;
- Projektbindung oder `read_only=true` kann nur angenommen, aber nicht belegt
  werden;
- der Projektbezug müsste über `list_projects` erraten werden;
- die tatsächliche Projektkennung müsste in Chat, Git oder Bericht kopiert
  werden;
- der Zieltyp und der Umgang mit echten Personendaten sind ungeklärt;
- der Tool-Call kann mehr Daten oder Metadaten liefern als vorab beschrieben;
- die App fragt nicht mehr vor jedem Aufruf;
- eine Antwort enthält unerwartete Daten, Instruktionen oder sensible Werte;
- ein Fehler würde einen Retry, ein anderes Tool oder den zweiten Plugin-Pfad
  nahelegen.

Bei STOP wird kein weiterer Supabase-Tool-Call ausgeführt. Ein unsicherer oder
fehlgeschlagener Write darf niemals über eine zweite Plugin-Oberfläche
wiederholt werden.

## 7. Noch erforderliche Nutzerentscheidungen

Vor einer späteren Live-Freigabe müssen folgende Punkte ausdrücklich geklärt
werden:

1. Welches getrennte Development-/Testprojekt ohne echte Kandidatendaten darf
   für den Plugin-Gate verwendet werden? Seine Erstellung oder Befüllung ist
   eine separat freizugebende externe Änderung.
2. Kann Codex den Connector für dieses Nicht-Produktionsprojekt tatsächlich mit
   `project_ref`,
   `read_only=true` und eingeschränkten Features konfigurieren, oder wird eine
   separate MCP-Verbindung benötigt?
3. Welches einzelne Schema darf P2 später inventarisieren?
4. Darf eine kompakte Liste interner Tabellennamen im Tool-Ergebnis an das
   Modell
   gelangen, oder muss ausschließlich der externe `psql`-Raw-Pfad verwendet
   werden?

Diese Entscheidungen werden nicht aus der Installation oder aus `Always ask`
abgeleitet.

## 8. Nächster sicherer Schritt

Der nächste Schritt ist ausschließlich eine lokale Capability-Prüfung der
Connector-Konfiguration und seines Tool-Katalogs. Dabei wird kein Supabase-
Projektwerkzeug aufgerufen. Parallel muss ein getrenntes Development- oder
Testprojekt ohne echte Personendaten ausgewählt oder nach separater Freigabe
erstellt werden. Erst wenn `PG-02` bis `PG-08` mit überprüfbarer Evidenz
geschlossen sind, darf ein separater Freigabetext für genau einen
`list_extensions`-Aufruf gegen dieses Nicht-Produktionsprojekt erstellt werden.

## Quellen

- [Supabase MCP Server](https://supabase.com/docs/guides/ai-tools/mcp)
- [Projektweite Supabase-Tooling-Regeln](../agents/supabase-tooling.md)
- [Bestehender Gate-B-Preflight](security-read-only-discovery-preflight-b.md)
- [Discovery-Runbook](../runbooks/schema-discovery.md)
