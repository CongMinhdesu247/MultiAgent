# Product workspace

Status: planning only; application source has not been generated.

Before implementation, fill in:

- Purpose and supported platforms/OS versions.
- Stack, runtime/SDK versions, package manager and source directories.
- Setup and environment variables (names and placeholders only).
- Development, lint, typecheck, test, build and smoke commands.
- Device/browser checks, packaging, deployment and known limitations.

Keep this directory as the product root. Scaffold application source in a child
directory such as apps/web, apps/mobile or apps/desktop if the framework requires
an empty directory. Configure each check's cwd accordingly.

From the factory root: `python tools/factory.py verify <product-slug>`.
This executes commands in factory.project.json; review them before execution.
