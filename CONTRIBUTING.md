# Contributing

## Source of truth

- `main` contains the accepted integrated project state: code, tests, documentation and decisions.
- Repository documentation is the canonical project memory when chat/session context is incomplete.
- Before working, read `README.md`, `docs/PROJECT-STATUS.md`, the relevant `docs/workstreams/*.md` file and linked ADR/product/architecture documents.

## Branching

Use bounded branches:

- `feature/*` for implementation work;
- `fix/*` for fixes;
- `docs/*` for documentation/governance;
- `prototype/*` for exploratory prototypes.

Changes should be reviewed through pull requests before merging into `main`.

Do not use permanent `dev`, `uat` or `prod` branches. DEV/UAT/PROD are deployment environments; see `docs/development/branching-and-environments.md`.

## Documentation and handoff

A change is not Done if it leaves the repository documentation describing the previous state.

Update as applicable in the same PR:

- code/design;
- tests/validation;
- migrations;
- relevant product/architecture documentation;
- the active workstream handoff;
- `docs/PROJECT-STATUS.md` when global state changes;
- an ADR for significant durable architectural decisions.

When handing work to another chat, AI agent or developer, the workstream handoff must state what is complete, what is currently being done, what comes next, known issues and the last validated commit when implementation exists.

See `docs/development/documentation-and-handoff.md`.

## Commit style

Use concise imperative commits, for example:

- `docs: define product vision`
- `docs: consolidate project handoff`
- `feat: add activity creation flow`
- `feat: bootstrap backend foundation`
- `fix: prevent schedule version conflict`

## Pull requests

Keep PR scope understandable. Include validation and update the handoff/docs required by the change. Draft PRs are appropriate for active work.

## Architecture changes

Do not casually reopen Accepted ADRs. If new evidence requires a different durable architecture decision, document the context and superseding decision explicitly.

AI agents may propose changes but must not invent project state, bypass domain validation, expose secrets or silently change accepted architectural constraints.

## Secrets and personal data

Never commit API keys, OAuth secrets, signing certificates, production configuration, personal production data, uploaded user files, database backups or credentials.

Use environment-specific secret/configuration mechanisms when deployment environments are introduced.
