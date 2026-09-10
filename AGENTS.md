# Supabase CRM MCP

## Mission

Build a secure MCP layer for searching approximately 200,000 CRM candidate
records through controlled, multilingual queries.

The detailed product and technical baseline is documented in
`docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md`. Read `docs/project.md` first for
the concise project state.

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
- Search results exclude contact details unless a separately approved access
  path permits them.
- Do not infer physical tables, columns, relationships, RLS policies, or tenant
  behavior before the approved read-only schema audit.
- Treat CVs, contact data, dates of birth, and candidate records as sensitive
  personal data.
- Never place credentials, raw personal data, private URLs, or production
  extracts in source files, prompts, logs, fixtures, reports, or commits.

## Working sequence

1. Read `docs/project.md` and the implementation brief.
2. Read applicable ADRs under `docs/decisions/`.
3. Follow the relevant runbook under `docs/runbooks/`.
4. Resolve unknown schema facts through approved read-only discovery.
5. Draft implementation changes and verification steps.
6. Require a separate approval before database mutations, external writes,
   deployment, credential changes, or production actions.
7. Record durable architecture changes as ADRs.

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
