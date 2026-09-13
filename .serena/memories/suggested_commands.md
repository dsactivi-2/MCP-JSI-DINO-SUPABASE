# Suggested Commands

- Prefix shell commands with `rtk`; use `rtk proxy` for transparent script execution.
- Documentation and synthetic Fake-psql proof: `rtk proxy /bin/bash scripts/check-local.sh`. It is the single local entry point.
- CRM PHP wiring wizards live under `scripts/wizards/`; follow `docs/runbooks/crm-wiring-wizards.md`. Wizard 01 must not use a 200-line cap.
- Follow shared MCP routing for Git; bind the global Git MCP to this repository. Do not print remotes or private project endpoints.
- Linear issues belong to project Dino problem baza CRM. Read `docs/agents/issue-tracker.md` before creating or duplicating tickets.
- No application scaffold or application build/typecheck pipeline exists. Local documentation and discovery tests do not prove SQL execution, production RLS, performance or restore.
- Never invoke the production discovery launcher without its separate approved gate. Existing credentials, tool availability and changed hashes are not approval.
