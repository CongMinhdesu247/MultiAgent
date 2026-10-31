# Software Factory instructions

This repository is a reusable development workspace, not an application itself.
Respond to the user in Vietnamese unless requested otherwise. Read README.md and
the selected project's AGENTS.md before implementation. Keep each product under
projects/<slug>/; never assume the factory root has an application build command.

## Delivery workflow

1. Inspect existing code and git status. Preserve unrelated user changes.
2. Identify target: web, mobile (Android/iOS), desktop, or a combination. For an
   unspecified "app", ask which platform before choosing platform dependencies;
   continue independent repository analysis while waiting.
3. For new products, use `python tools/factory.py init <slug> --kind <kind>`.
   This creates planning files only. Implement the actual application afterward.
   Fill docs/BRIEF.md, docs/ARCHITECTURE.md and docs/PLAN.md inside the project.
   For a small fix, update only documentation material to that fix.
4. Retain existing stack/package manager and lockfile. For greenfield projects,
   choose a stack based on requirements, deployment and installed SDKs; explain
   the choice. Do not install all web/mobile/desktop frameworks in the factory.
5. Define API payloads, errors, authentication and shared types before parallel
   frontend/backend work. Use docs/CONTRACTS.md for cross-platform contracts.
6. Implement a runnable vertical slice first; then add the remaining features.
7. Configure real lint, typecheck, test, build and smoke commands in
   factory.project.json. Run `python tools/factory.py verify <slug>` from root.
   Smoke commands must terminate and check real behavior. Keep dev servers in a
   separately managed process and stop only processes started for this task.
8. Review changes, fix relevant failures, rerun affected checks, and record
   commands, outcomes and remaining gaps in docs/VERIFICATION.md.

## Multi-agent coordination

For substantial work with independent parts, delegate to specialized subagents
when the current host supports them. Use a single agent for small edits. Select
roles from .github/agents/; Codex definitions in .codex/agents/ are generated copies.
If named roles cannot be loaded, give supported workers the matching role text.
If delegation is unavailable, execute the same responsibilities sequentially and
say so. Agent Markdown files alone do not launch agents or select cheaper models.

The root agent owns integration, shared manifests, lockfiles and final reporting.
Give each worker a bounded task, owned paths, read-only context, dependency
contracts, acceptance criteria and verification commands. Track these in the
project's docs/PLAN.md. Only one writer per file; serialize shared-file changes.
Wait for dependencies and all required results before integration. Reviewers and
researchers return evidence without edits. Workers must not recursively delegate
unless asked by the root. Default to at most three simultaneous workers, subject
to host limits. Inherit the user's model choice unless explicitly configured.

## Product quality

- Web: responsive layouts, keyboard and screen-reader semantics, loading/empty/
  error states, form validation, server-side authorization, and browser checks of
  the main flow at mobile and desktop widths.
- Mobile: safe areas, navigation/back behavior, permission denial, secure token
  storage, network failure and app lifecycle. Test on a named device/emulator;
  a web preview does not verify Android or iOS. Record unavailable SDKs/devices.
- Desktop: window lifecycle, filesystem permissions, narrow native/IPC APIs,
  installer/package build and launch on the target OS. Do not equate a renderer
  build with a working desktop package.
- Backend/data: validate inputs, enforce authorization at the server, keep secrets
  out of client bundles/logs, include reproducible migrations when data changes,
  and test denied access and relevant failure paths. Use applicable skills.
- Keep runtime versions, setup, environment variable names (no secret values),
  run/test/build commands and deployment steps in each product's README.md.

## Completion and boundaries

Never turn a skipped or missing check into PASS. Distinguish implementation,
automated checks, manual smoke checks and target-platform packaging. Do not claim
production readiness from compilation alone. Report blockers with next actions.
Do not disable tests or weaken checks to conceal failures. Execute configured
commands only from trusted project files; they can run arbitrary project code.
Do not publish, deploy, incur paid cloud costs or sign/store releases unless the
user's request authorizes that action. Never commit credentials or signing keys.
