# Tech Stack

- Data platform: Supabase PostgreSQL. Runtime search must use controlled RPC, not model-generated SQL.
- Application language, framework, runtime, package manager, and build tool are not selected yet. MCP SDK v2 + Zod is a documented candidate, not an installed dependency.
- Project skills: vendored `supabase` and `supabase-postgres-best-practices`; `start-matt-wizard` only on explicit request; `mcp-server-dev` is design-only.
- Linear native plugin is the issue tracker. Git MCP must bind `repo_path` to this repository. Serena memories live in `.serena/memories/`.
- Supabase developer plugin/MCP stays blocked against the production CRM project. Gate P is NO-GO. Gate B stays the local `psql` launcher.
- Do not infer missing stack choices from the directory name. Update this memory after the application scaffold establishes them.
- Development host is macOS with Zsh.
