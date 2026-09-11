# Least-Privilege-Discovery-Rolle V1

Status: **SYNTHETISCH PASS_WITH_GAPS / PRODUKTION NO-GO**

## Zweck

Der Nutzer hat die Einrichtung am 2026-09-11 ausdrücklich beauftragt; siehe
[ADR-0002 Q10.2b](../decisions/0002-search-design-interview.md). Die Rolle wurde
noch nicht angelegt. Der Status NO-GO bezeichnet die fehlenden
Ausführungsvoraussetzungen, nicht einen fehlenden grundsätzlichen Auftrag.

Dieses Paket bereitet eine dedizierte PostgreSQL-Loginrolle für spätere,
separat freizugebende Discovery-Gates vor. Es ist kein Datenbankscan und keine
Freigabe für eine Produktionsmutation.

Die feste Rolle `dino_crm_discovery_ro_v1` erhält ausschließlich `CONNECT`.
Sie erhält keine Mitgliedschaften, keine Objekt-Ownership und keine direkten
Rechte auf Anwendungsdaten. Sitzungsdefaults setzen Read-only und kurze Timeouts
als Vorgaben; sie sind
kein unveränderlicher Rechteentzug. B1 muss die effektiven Rechte separat
prüfen.

Der [Zugangsplan](access-plan-consolidated.md) löst die Bootstrap-Abhängigkeit
als getrennten Entscheidungspunkt auf. Bestehende Credentials oder ein V2-
Freigabetext dürfen nicht auf die neue Rolle übertragen werden.

## Dateien

<!-- markdownlint-disable-next-line MD013 -->
- Setup: [01-create-least-privilege-discovery-role-v1.sql](sql/01-create-least-privilege-discovery-role-v1.sql)
<!-- markdownlint-disable-next-line MD013 -->
- Rollback: [01-drop-least-privilege-discovery-role-v1.sql](sql/01-drop-least-privilege-discovery-role-v1.sql)
<!-- markdownlint-disable-next-line MD013 -->
- Separater V2-Entwurf: [02-create-least-privilege-discovery-role-v2-draft.sql](sql/02-create-least-privilege-discovery-role-v2-draft.sql)

## Fail-closed-Verhalten

Das Setup läuft in genau einer Transaktion. Vor `COMMIT` prüft es die effektiven
Rechte der neuen Rolle. Jeder der folgenden Befunde erzeugt einen SQL-Fehler;
die Verbindung beendet die Transaktion ohne Teilzustand:

- administrative Attribute oder `INHERIT`;
- abweichendes Connection-Limit;
- direkte oder geerbte Rollenmitgliedschaft;
- Datenbank-`CREATE` oder `TEMP`;
- Schema-Ownership oder Schema-`CREATE`;
- Relations-, Spalten- oder Sequenz-Schreibrechte;
- Objekt-Ownership;
- ausführbare `SECURITY DEFINER`-Routine;
- fehlende Read-only- oder Timeout-Rollensettings.

Nur das `UPDATE` der exakten Systemview `pg_catalog.pg_settings` ist von den
Relations-/Spaltenschreibchecks ausgenommen: Es entspricht einem sitzungslokalen
`SET`, keinem Daten-DML. Ownership und andere Rechte bleiben geprüft; dieselbe
Viewbezeichnung in einer Anwendungsschema ist nicht ausgenommen. Beleg:
[PostgreSQL 17 pg_settings](https://www.postgresql.org/docs/17/view-pg-settings.html).

PostgreSQL kennt kein individuelles `DENY`. Rechte, die `PUBLIC` besitzt,
können daher nicht nur für diese Rolle widerrufen werden. Erkennt das Setup
solche effektiven Rechte, rollt es zurück. Es verändert `PUBLIC` ausdrücklich
nicht, weil dies andere Produktionsnutzer beeinflussen könnte.

## Credential-Regel

`psql` fordert das neue Passwort interaktiv über `\password` an. Das Passwort
darf nicht als Argument, Umgebungsvariable, Repositorydatei, Chatnachricht oder
Logwert übergeben werden. Eine spätere lokale Credential-Datei muss außerhalb
des Repositories liegen, dem aktuellen Benutzer gehören, Modus `0600` besitzen
und darf erst nach erfolgreichem Setup separat erstellt werden.

## Vor einer Ausführung zwingend offen

Der tatsächliche begrenzte Produktionspreflight am 2026-09-11 bestätigt zwei
Blocker: PUBLIC TEMP und mindestens eine für PUBLIC erreichbare
SECURITY-DEFINER-Funktion. V1 und V2 müssen diese Befunde weiterhin ablehnen.
Der Funktionsinhalt und seine Auswirkungen sind ungeprüft. Kein globaler REVOKE
und keine Lockerung sind durch den Rollenauftrag automatisch freigegeben.
<!-- markdownlint-disable-next-line MD013 -->
Siehe [Produktions-Preflight](../reviews/2026-09-11-production-role-preflight.md).

1. Zulässiger synthetischer Laufzeitnachweis für Setup und Rollback. Der vorherige
   Restore-Test entfällt ausschließlich für diese Rollenanlage gemäß der
   bestätigten Ausnahme ADR-0002 Q10.2d.
2. Eigener Mutations-Preflight mit Zielattest, SQL-Hash, genau einer Verbindung,
   keinem Retry und klaren Stopkriterien.
3. Exakter, zeitlich begrenzter Freigabetext für ausschließlich dieses Setup.
4. Lokaler Launcher, der Ziel, Hash, Prozesszahl und Ausgabe fail-closed bindet.
5. Nach erfolgreichem Setup eine neue
   Connection-Service-/Credential-Konfiguration
   für die neue Rolle und ein neuer Gate-B1-V3-Preflight.

Gate B2 und B3 bleiben unabhängig davon gesperrt.

## Rollback

Der Rollback widerruft ausschließlich den im Setup erteilten `CONNECT`-Grant
auf der attestierten Datenbank und löscht danach die feste Rolle. Er verwendet
weder
`REASSIGN OWNED` noch `DROP OWNED` noch `CASCADE`. Bestehen Abhängigkeiten,
stoppt PostgreSQL und rollt die Transaktion zurück. Auch der Rollback benötigt
eine eigene Produktionsfreigabe.

## Synthetischer Laufzeitnachweis und Grenzen

Q10.2e erlaubt einen neuen temporären Testcontainer. Der Lauf auf PostgreSQL
17.11 nutzte ausschließlich das vorhandene feste Image, kein Netzwerk, keine
Hostdateien und keine echten Daten. Der eigene Container wurde entfernt.
<!-- markdownlint-disable-next-line MD013 -->
Prüfer: [role_lifecycle_integration.py](../../tests/discovery/role_lifecycle_integration.py).

Folgende beobachtbare Fälle wurden geprüft; die Benutzergrenze ist
Rolle/Rechte/Transaktionszustand:

1. Synthetischer Baseline-Setup mit isoliertem DB-Ziel, sauberem PUBLIC-Scope
   und interaktivem Testcredential: alte qualifizierte `current_user`-Form
   reproduziert Fehler; korrigierter Entwurf erzeugt exakt die Rolle und
   CONNECT.
2. Falsches Ziel, bestehende Rolle oder unerwartetes PUBLIC TEMP/Write-Recht:
   Nonzero und keine teilweise angelegte/veränderte Rolle.
3. Der korrigierte Rollback entfernt den eigenen Grant und die Rolle atomar.
4. Zusätzliche synthetische Objekt-/Grant-Abhängigkeit: Rollback scheitert,
   Rolle und CONNECT bleiben durch Transaktionsabbruch erhalten. Keine fremden
   Grants, Objekte oder PUBLIC-Rechte werden verändert.
5. Öffentliches Tabellen-UPDATE, reines Spalten-UPDATE und UPDATE auf eine
   Anwendungsview namens `pg_settings` werden atomar abgewiesen.
6. V1 scheitert mit einem Nicht-Superuser-Ersteller ohne Teilzustand.

Die Loginprobe verwendet lokale Trust-Authentifizierung. Sie beweist Identität
und Sitzungsvorgaben, aber keinen Passwort-Login und keine Produktionsrechte.
Die alte qualifizierte `current_user`-Form und der `pg_settings`-Fehlalarm wurden
vor den jeweiligen erfolgreichen Prüfungen tatsächlich reproduziert.

## Separater V2-Entwurf für den verwalteten Administrator

PostgreSQL 17 vergibt beim Anlegen durch einen Nicht-Superuser automatisch ein
ADMIN-Verwaltungsrecht an den Ersteller, ohne SET oder INHERIT. Dieser Ersteller
kann den vom Bootstrap-Superuser vergebenen Grant nicht selbst widerrufen.
Die V1-Forderung nach keinerlei Mitgliedschaft und ihr `SET ROLE` sind damit
nicht vereinbar. Beleg:
[PostgreSQL Rollenattribute](https://www.postgresql.org/docs/17/role-attributes.html).

V2 prüft Rechte explizit für die feste neue Rolle und erlaubt ausschließlich
dieses eingehende ADMIN-only-Recht an den ausführenden Ersteller. Mitgliedschaft
der Leserolle in anderen Rollen, SET/INHERIT-Zugriff und andere Mitglieder bleiben
verboten. Der Entwurf ist auf die getestete Hauptversion 17 begrenzt. Anlage und
Rollback mit einem Nicht-Superuser wurden synthetisch erfolgreich geprüft.
V2 bleibt ein separat zu prüfender Entwurf und ersetzt V1 nicht automatisch.
Das ADMIN-Recht erlaubt dem Administrator spätere Änderungen der Mitgliedschaft.
SET/INHERIT=false beschreiben den geprüften Anfangszustand, keine unveränderbare
Sperre gegenüber dem Administrator. Diese Verwaltungsbefugnis muss im konkreten
V2-Ausführungspaket ausdrücklich berücksichtigt werden.

Reproduktion ausschließlich nach Q10.2e:

```bash
rtk proxy python3 tests/discovery/role_lifecycle_integration.py \
  --allow-new-isolated-container
rtk proxy python3 tests/discovery/role_lifecycle_integration.py \
  --allow-new-isolated-container --owner-compatible-draft
```

Testvoraussetzungen dürfen ausschließlich im synthetischen Testsystem
hergestellt werden. Keine Produktionsrechte verändern, um einen Test grün
zu machen. Setup-/Rollback-Launcher, Identitäts-/Owner-Attest und neue B1-V3-
Hashbindung bleiben eigene Pakete vor jeder Ausführungsfreigabe.

## Aktuelle Entwurfsbindung

Diese Hashes identifizieren nur die korrigierten Entwürfe, kein Approval.

Setup SHA-256:
`94b5234417d3bbdc8940629442619b56f19404baf308de2115f8f0f9d0e62ee6`

V2-Entwurf SHA-256:
`8904405171f547631225f07cc7927f2317e587ff9717b01460a844ff9147438e`

Rollback SHA-256:
`c57e37514dd824bdbfed1d3a8b5075faeca986014b4dd264f4aea2d6fafac49a`

## Naknadno utvrđena granica PUBLIC funkcija

Ograničeni [audit i kontraprimjeri](../reviews/2026-09-11-public-definer-audit.md)
ne daju dozvolu za primjenu. Dvije rutine imaju PUBLIC EXECUTE, bez PUBLIC
schema USAGE. To ne isključuje indirektan poziv preko viewa. Sintetički je
potvrđeno i kreiranje trajnog large objecta preko PUBLIC invoker funkcije.
Read-only zadana postavka se može isključiti. V1/V2 nisu dokaz potpune zabrane
svih trajnih upisa; njihovi postojeći strogi gateovi ostaju nepromijenjeni.
Privremena V3 ideja je povučena nakon kontraprimjera. Produkcija nije mijenjana.

Korisnik je dodatni isključivo read-only scope odobrio u Q10.2h. Odobrenje
ne mijenja V1/V2 gateove niti vraća povučeni V3 pokušaj. Razlika između verzija
role i Gate-B1-V3 paketa je u [registru verzija](role-version-register.md).
