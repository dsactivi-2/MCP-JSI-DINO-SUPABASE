# Suggested Commands

- Prefix shell commands with `rtk`; use `rtk proxy` for transparent script execution.
- Follow the shared MCP routing file for Git; always bind the global Git MCP to this repository. Do not print remotes or private project endpoints into logs.
- README.md is authoritative for current local documentation and synthetic Fake-psql checks. Run Markdownlint, the working-tree link/fragment checker, each Bash syntax check separately, and the existing local test files.
- The link checker defaults to the working tree including new root/docs Markdown; `--source index` explicitly checks staged artifacts instead.
- No application scaffold or application build/typecheck pipeline exists. Local documentation and discovery tests do exist; they do not prove SQL execution, production RLS, performance or restore.
- Never invoke the production discovery launcher without its separate approved gate. Existing credentials, tool availability and changed hashes are not approval.
