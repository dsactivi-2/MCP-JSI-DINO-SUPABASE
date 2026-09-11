# Supabase Agent Skills – einfach erklärt

Datum: 2026-09-11

Status: Recherchebericht; beide Skills am 2026-09-11 projektlokal für Codex
installiert und mit der vorhandenen Community-Distribution abgeglichen;
Live-Plugin ebenfalls installiert, aber kein Datenbankzugriff und keine
Architektur- oder Produktionsfreigabe

## Klare Antwort

`npx skills add supabase/agent-skills` lädt zwei offizielle **Arbeitsanleitungen
für KI-Coding-Agenten** in das aktuelle Projekt:

- `supabase`: Regeln und Arbeitsabläufe für Supabase;
- `supabase-postgres-best-practices`: Regeln für sicheres und effizientes
  PostgreSQL.

Ein Skill ist bildlich ein Handbuch, das der Agent bei einer passenden Aufgabe
liest. Er ist **kein Programmteil unseres späteren CRM**, kein SDK und keine
Verbindung zur Datenbank. Der Befehl meldet sich nicht bei Supabase an, verlangt
keinen Supabase-Schlüssel und richtet keinen MCP-Server ein. Supabase trennt diese
Bausteine ausdrücklich: Skills liefern Wissen; MCP stellt eine Live-Verbindung
zum Projekt her; ein Plugin bündelt beides
([Supabase AI Tools](https://supabase.com/docs/guides/ai-tools),
[Agent Skills](https://supabase.com/docs/guides/ai-tools/ai-skills)).

## Was der Befehl konkret macht

Der nackte Befehl findet im öffentlichen GitHub-Repository beide Skills und
installiert beide. Mit `--skill supabase` oder
`--skill supabase-postgres-best-practices` ließe sich nur einer auswählen
([offizielles Repository](https://github.com/supabase/agent-skills),
[Supabase-Installationsanleitung](https://supabase.com/docs/guides/ai-tools/ai-skills)).

Standardmäßig ist die Installation **projektbezogen**. Für Codex ist der
Projektpfad `.agents/skills/`; mit `--global` wäre der Codex-Pfad
`~/.codex/skills/`. Ohne zusätzliche Schalter ist der Ablauf interaktiv: Die CLI
kann erkannte Agenten sowie Symlink oder Kopie zur Auswahl anbieten. Die
empfohlene Symlink-Variante hält eine kanonische Kopie unter `.agents/skills/`
und verlinkt sie bei Bedarf in agentenspezifische Verzeichnisse
([Skills-CLI: Scope und Installationsarten](https://github.com/vercel-labs/skills#installation-scope),
[Codex-Pfade im CLI-Quellcode](https://github.com/vercel-labs/skills/blob/main/src/agents.ts#L214-L221)).

Installiert werden die jeweiligen Skill-Ordner, nicht nur ein kurzer Prompt:

- bei `supabase`: `SKILL.md`, `CHANGELOG.md`, eine Feedback-Referenz und eine
  Issue-Vorlage;
- bei `supabase-postgres-best-practices`: `SKILL.md`, `CHANGELOG.md` sowie die
  Referenzdateien mit einzelnen Regeln und SQL-Beispielen.

Die CLI kopiert bei einer Mehrdatei-Skillquelle alle Dateien des Skill-Ordners.
Die Skills-CLI kann außerdem ein `skills-lock.json` im Projektstamm führen,
damit Quelle und Version später geprüft oder wiederhergestellt werden können
([Installer-Quellcode](https://github.com/vercel-labs/skills/blob/main/src/installer.ts),
[Lockfile-Quellcode](https://github.com/vercel-labs/skills/blob/main/src/local-lock.ts)).
Im aktuellen Repository existiert kein solches Lockfile. Die vorhandenen
Projektkopien stimmen inhaltlich mit der installierten Supabase-Community-
Distribution überein; ihre Provenienz muss bei Updates deshalb über vollständigen
Ordner- und Git-Diff-Review statt nur über eine Frontmatter-Version geprüft werden.

Danach sieht ein unterstützter Agent zunächst Name und Beschreibung. Erkennt er
zum Beispiel eine Supabase-, RLS- oder SQL-Aufgabe, lädt er das passende
`SKILL.md` und bei Bedarf einzelne Dateien aus `references/`. Die Skills werden
also **bei Bedarf gelesen**; sie laufen nicht dauerhaft im Hintergrund
([Supabase-Repository: Usage und Struktur](https://github.com/supabase/agent-skills#usage)).

## Was `supabase` dem Agenten beibringt

Dieser Skill ist das allgemeine Supabase-Handbuch. In einfachen Worten sagt er:

- Verlasse dich nicht auf altes Modellwissen. Prüfe zuerst aktuelle Changelogs
  und offizielle Dokumentation.
- Eine Änderung gilt erst nach einem echten Test als fertig.
- Wiederhole einen fehlgeschlagenen Versuch nicht endlos; prüfe Dokumentation,
  Fehlermeldung und Logs.
- RLS muss für Tabellen in exponierten Schemas wie `public` aktiviert werden.
  Tabellenrechte (`GRANT`) und RLS sind zwei verschiedene Schutzschichten.
- Nutze benutzerveränderbare `user_metadata` niemals zur Autorisierung.
- Gib `service_role`- oder Secret-Schlüssel niemals an Browser oder öffentliche
  Clients weiter.
- Beachte typische Fallen: Views können RLS umgehen, `UPDATE` braucht passende
  `SELECT`- und `WITH CHECK`-Regeln, und `TO authenticated` allein verhindert
  keinen Zugriff auf fremde Datensätze.
- `SECURITY DEFINER` kann RLS umgehen. Falls es wirklich nötig ist, gehört die
  Funktion in ein nicht exponiertes Schema, braucht eine ausdrückliche
  Identitätsprüfung und eng entzogene Ausführungsrechte.
- CLI-Befehle und Flags immer mit `--help` prüfen. Vor Migrationen Advisors und
  Security-Checkliste nutzen; Fehler anhand der aktuellen Debugging-Dokumentation
  untersuchen.

Der aktuelle Originaltext steht im
[`supabase`-Skill](https://github.com/supabase/agent-skills/blob/main/skills/supabase/SKILL.md).

## Was `supabase-postgres-best-practices` erklärt

Dieser Skill ist eine Sammlung einzelner PostgreSQL-Regeln mit falschen und
richtigen SQL-Beispielen. Die Regeln sind nach Wirkung geordnet:

| Priorität | Thema | Bedeutung für uns |
| --- | --- | --- |
| kritisch | Queries | passende Indizes und verständliche Pläne |
| kritisch | Connections | Pooling, Limits und Timeouts richtig wählen |
| kritisch | Security und RLS | Zeilen, Rollen und Tenants korrekt trennen |
| hoch | Schema | Typen, Schlüssel und Constraints sauber entwerfen |
| mittel-hoch | Locks | kurze Transaktionen und keine Deadlocks |
| mittel | Datenzugriff | keine N+1-Abfragen; Batch und Cursor-Pagination |
| niedrig-mittel | Diagnose | `EXPLAIN`, Statistiken und Vacuum verstehen |
| niedrig | Spezialfunktionen | FTS und JSONB gezielt einsetzen |

Die Referenzen enthalten unter anderem Regeln für fehlende, partielle,
zusammengesetzte und abdeckende Indizes, Foreign-Key-Indizes, Datentypen,
Constraints, RLS, Rechte, Keyset-Pagination, Volltextsuche und JSONB. Ein für
unser Projekt besonders passendes Beispiel empfiehlt, in RLS-Prüfungen
verwendete Spalten zu indexieren und stabile Funktionen so aufzurufen, dass sie
nicht unnötig pro Zeile neu ausgewertet werden
([Skill-Übersicht](https://github.com/supabase/agent-skills/blob/main/skills/supabase-postgres-best-practices/SKILL.md),
[Regelverzeichnis](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices/references),
[RLS-Performance-Regel](https://github.com/supabase/agent-skills/blob/main/skills/supabase-postgres-best-practices/references/security-rls-performance.md)).

## Nutzen und Grenzen für unseren CRM-MCP

Der Nutzen ist konkret, aber begrenzt:

- Schon jetzt erinnern die Skills den Agenten bei Plänen und Reviews an
  Sicherheits- und PostgreSQL-Fallen, ohne Kandidatendaten zu öffnen.
- Nach dem genehmigten read-only Discovery helfen sie beim Prüfen von Audit-SQL,
  RLS, Tenant-Trennung, Indizes, Query-Plänen und der kontrollierten RPC-Funktion.
- Sie passen damit gut zu unserer Grenze: Das LLM schlägt nur einen validierten
  JSON-Filter vor; PostgreSQL filtert, autorisiert und paginiert.

Die Skills können aber weder unser unbekanntes Schema entdecken noch beweisen,
dass eine Policy korrekt ist. Sie ersetzen keine Tests, keine Datenschutz- und
Berechtigungsentscheidung und keine Freigabe für Datenbankänderungen. Eine darin
gezeigte SQL-Lösung ist ein Prüfhinweis, nicht automatisch die richtige Lösung
für unsere Datenbank.

Zusätzlich bestehen gewöhnliche Abhängigkeitsrisiken: Der unversionierte
`npx skills`-Aufruf lädt aktuelle CLI- und Repository-Inhalte aus dem Netz;
Supabase aktualisiert die Skills häufig. Änderungen sollten daher vor Übernahme
im Git-Diff geprüft werden. Die Skills-CLI sendet standardmäßig anonyme
Nutzungsdaten; `DISABLE_TELEMETRY=1` oder `DO_NOT_TRACK=1` schaltet dies ab
([Skills-CLI: Telemetrie](https://github.com/vercel-labs/skills#telemetry)).

## Kurze Empfehlung: jetzt, später, nicht

### Jetzt

Beide Skills wurden nach Prüfung ihrer Quelldateien projektbezogen unter
`.agents/skills/` für Codex installiert. Sie stehen ab dem nächsten Codex-Lauf
automatisch zur Verfügung. Beide vollständigen Verzeichnisse einschließlich
Referenzen und Assets sind vorhanden. Die Installation gibt keinen
Datenbankzugriff frei.

### Später

Nach der Discovery-Freigabe die Skills beim Review der read-only Audit-Abfragen
nutzen. Erst danach über RLS, RPC, CLI, pgTAP, `db lint`, generierte Typen und ein
Runtime-SDK entscheiden. Der inzwischen installierte Supabase-MCP bleibt bis zu
einem eigenen projektgebundenen, read-only und feature-reduzierten Gate ohne
Projekt- oder Datenbankzugriff.

### Nicht

Den Skill nicht mit einer Sicherheitskontrolle oder einem Datenbanktool
verwechseln. Den installierten Live-MCP nicht allein wegen seiner Verfügbarkeit
aufrufen. Mehrere Plugin-Distributionen ersetzen weder Projektbindung noch einen
separaten read-only Identitäts- und Output-Gate. Keine Secrets eingeben, keine
Produktionsdaten öffnen und keine SQL- oder RLS-Empfehlung ungeprüft anwenden.

Die verbindliche Nutzungs- und Aktualisierungsroute steht in
[Supabase tooling za agente](../agents/supabase-tooling.md).

## Quellen

- [Supabase: Agent Skills](https://supabase.com/docs/guides/ai-tools/ai-skills)
- [Supabase: AI Tools und Begriffsabgrenzung](https://supabase.com/docs/guides/ai-tools)
- [Supabase: offizielles Agent-Skills-Repository](https://github.com/supabase/agent-skills)
- [Vercel Labs: offizielle Skills-CLI](https://github.com/vercel-labs/skills)
- [Supabase: Plugin für AI Coding Agents](https://supabase.com/docs/guides/ai-tools/plugins)
