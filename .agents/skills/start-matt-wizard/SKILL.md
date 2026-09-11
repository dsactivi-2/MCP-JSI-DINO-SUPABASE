---
name: start-matt-wizard
description: Launch the interactive project-local Matt skills workflow wizard when the user explicitly asks to start or run the new-project skill setup guide. Do not use for ordinary project setup that can be completed directly.
---

# Start Matt Wizard

Launch the repository's interactive wizard. It guides the user through a safe sequence for preparing a new project and creates a tailored prompt pack for the Matt Pocock skills.

## Procedure

1. Resolve the current repository root with Git; use the current working directory only when it is not a Git repository.
2. Locate `.scratch/start-matt-wizard.sh` at that root.
3. Verify that the script exists and passes `bash -n`. If it does not, stop and report the exact problem.
4. Start it in an interactive PTY with `rtk proxy bash "$REPO_ROOT/.scratch/start-matt-wizard.sh"`.
5. Open the running terminal in the Codex panel when that UI action is available.
6. Let the user answer every prompt. Never invent values, provide secrets, bypass confirmations, or run the wizard non-interactively.
7. Report the script path and terminal session. If the user interrupts it, explain that rerunning the same command safely starts the guide again.

The wizard may initialize only the exact target folder the user enters. Its own confirmation gates govern local writes. Linear, deployment, publishing, credential changes, and other external or production writes still require separate explicit approval.
