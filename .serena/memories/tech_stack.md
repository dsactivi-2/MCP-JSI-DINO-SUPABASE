# Tech Stack

- Data platform: Supabase PostgreSQL.
- Architecture boundary: the LLM produces validated JSON; the MCP server validates it and calls controlled PostgreSQL RPC functions instead of executing arbitrary model-generated SQL.
- Application language, framework, runtime, package manager, and build tool are not selected yet.
- Do not infer missing stack choices from the directory name or future scaffold files; update this memory after the application scaffold establishes them.
- Development host is macOS with Zsh.
