# Supabase CRM MCP

## Mission

Build a secure MCP layer for searching approximately 200,000 CRM candidate
records through controlled, multilingual queries. This volume is a project
estimate, DURCH DISCOVERY ZU PRÜFEN, not an audited record count.

Read [docs/project.md](docs/project.md) first for the concise project state.
The [implementation brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md)
contains the detailed product and technical baseline.

## Response style

- Keep progress updates and final replies brief, using short paragraphs or
  compact lists. Avoid large text blocks, repetition, and unnecessary detail.
- Expand only when a shorter reply would omit information needed to understand
  the result, make a decision, or take the next step. Preserve essential context,
  verification results, and material limitations.
- Link to detailed repository documents instead of repeating their contents.

## Current phase

The repository is in governance and read-only discovery preparation. No
application stack, package manager, deployment target, database contract, or
production access workflow has been approved yet.

Do not add stack-specific commands or claim that build, lint, typecheck, or test
checks exist until an application scaffold establishes them.

## Architecture boundaries

- The LLM may translate natural language into a strictly validated JSON filter.
- The runtime LLM must never generate or execute arbitrary SQL.
- PostgreSQL remains authoritative for filtering, ranking, authorization, and
  pagination.
- Never send the full candidate database or bulk candidate records to an LLM.
- Search responses are capped at 50 candidates per page.
- Release 1 excludes contact details from every output, including candidate
  profiles. Contact access and CONTACT-02 belong to a later, separately approved
  phase.
- The profile-administration MCP is a separate planned trust boundary from the
  read-only runtime search MCP. It may manage drafts and published profile
  versions only after schema discovery and data-model approval; follow
  `docs/decisions/0003-separated-profile-administration-mcp.md` in every plan.
- Automated or LLM-based profile mappings are proposals only. They never publish
  themselves or silently change active search semantics.
- Do not infer physical tables, columns, relationships, RLS policies, or tenant
  behavior before the approved read-only schema audit.
- Treat CVs, contact data, dates of birth, and candidate records as sensitive
  personal data.
- Never place credentials, raw personal data, private URLs, or production
  extracts in source files, prompts, logs, fixtures, reports, or commits.

## Working sequence

1. Read [docs/project.md](docs/project.md) and the implementation brief.
2. Read applicable ADRs under [docs/decisions/](docs/decisions/).
3. Follow the relevant runbook under [docs/runbooks/](docs/runbooks/).
4. Resolve unknown schema facts through approved read-only discovery.
5. Draft implementation changes and verification steps.
6. Require a separate approval before database mutations, external writes,
   deployment, credential changes, or production actions.
7. Record durable architecture changes as ADRs.

## Agent skills

### Supabase tooling

- For every Supabase task, load `.agents/skills/supabase/SKILL.md`. Before
  drafting or reviewing SQL, schemas, migrations, RLS, functions, indexes or
  query plans, also load
  `.agents/skills/supabase-postgres-best-practices/SKILL.md` and only the
  relevant reference files.
- Skills provide guidance only. They do not prove schema facts, authorize a
  database connection or override this repository's approvals and ADRs.
- Treat any Supabase plugin/MCP as internal development tooling, not
  as the Runtime-Such-MCP or Profilverwaltungs-MCP. Tool availability is never
  authorization.
- Gate B remains bound to its reviewed local `psql` launcher. Do not use the
  Supabase plugin for project, schema, data or SQL access until a separately
  approved plugin-specific gate proves project scope, read-only enforcement,
  minimal feature groups and reviewed output handling. Follow
  [Supabase tooling](docs/agents/supabase-tooling.md).

### Issue tracker

Use the dedicated Linear project Dino problem baza CRM in team Activi (`ACT`).
See [issue tracker](docs/agents/issue-tracker.md) for its identity and workflow.

### Triage labels

Use the five canonical labels mapped in
[triage labels](docs/agents/triage-labels.md).

### Domain docs

Use the single root [CONTEXT.md](CONTEXT.md) and `docs/decisions/` as the only
ADR directory. See [domain docs](docs/agents/domain.md) for consumer rules.

### Design interview persistence

The active search-design interview is recorded in
[ADR-0002](docs/decisions/0002-search-design-interview.md). Before asking its
next question, read the draft. After every explicit user answer, update the
question and normalized answer immediately in the same file.

Do not infer a decision from a request for explanation, a recommendation, or an
unanswered question. Keep unresolved items marked `OFFEN` and partial decisions
marked `TEILWEISE BESTÄTIGT`. Q8.5 is entirely `OFFEN`; Q8.4 remains accepted
in principle. Reconstructed filter details and confirmation before every new
or changed search are `VORLÄUFIGER VORSCHLAG` until evidenced. Label unverified
physical facts `ARBEITSANNAHME` or `DURCH DISCOVERY ZU PRÜFEN`.
When the user confirms shared understanding and
the interview frontier is empty, follow ADR-0002's completion procedure to
reconcile accepted ADRs, `CONTEXT.md`, the implementation brief, project status,
and later Linear tickets.

## Repository conventions

- Domain documentation uses B/H/S Latin unless a deliverable requires another
  language.
- Source code, identifiers, schemas, and code comments use English.
- Keep project instructions concise and repository-specific.
- Preserve accepted ADRs and update superseded decisions explicitly.
- Add executable commands here only after the selected stack and scaffold make
  them reproducible.
- Keep generated files, secrets, database exports, and raw audit data out of Git.

## Verification

For documentation-only changes:

- verify Markdown structure and relative links;
- run `git diff --check`;
- inspect `git status --short`;
- report unavailable Markdown linting as a gap.

Reproducible documentation commands are in
[README.md](README.md#provjera-dokumentacije).

For implementation changes, run the repository's actual build, lint, typecheck,
test, security, and contract checks after those commands have been established.

Database discovery is successful only when its documented outputs contain no
secrets or unnecessary personal data and no mutation occurred.

## Definition of done

Work is complete only when it:

- matches the active implementation phase and acceptance criteria;
- preserves the architecture and privacy boundaries above;
- includes reproducible verification evidence;
- documents remaining gaps without presenting them as completed;
- introduces no placeholders, invented schema facts, or unapproved external
  changes.
