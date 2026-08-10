# Contributing

## Source of truth

- `main` contains the accepted integrated project state: code, tests, documentation and decisions.
- Repository documentation is the canonical project memory when chat/session context is incomplete.
- Before working, read `README.md`, `docs/PROJECT-STATUS.md`, `docs/development/operating-rules.md`, the relevant `docs/workstreams/*.md` file and linked ADR/product/architecture documents.
- When sources conflict, current accepted `main` wins over old branches or conversation memory; an active workstream branch is authoritative only for its unmerged scoped work.

## Branching

Use bounded branches:

- `feature/*` for implementation work;
- `fix/*` for fixes;
- `docs/*` for documentation/governance;
- `prototype/*` for exploratory prototypes.

Changes should be reviewed through pull requests before merging into `main`.

Start new production work from current `main` unless the workstream handoff explicitly requires an existing active prototype branch. Keep one primary branch per workstream where practical.

Do not use permanent `dev`, `uat` or `prod` branches. DEV/UAT/PROD are deployment environments; see `docs/development/branching-and-environments.md`.

## Parallel-work discipline

Avoid editing shared/global files from multiple branches unless the change is genuinely cross-cutting.

- Incremental workstream state belongs in `docs/workstreams/<name>.md`.
- `docs/PROJECT-STATUS.md`, root `README.md`, broad architecture documents and ADRs change only when global truth actually changes.
- If Domain Model work is performed inside Backend Foundation, use the same branch rather than opening two branches that modify the same domain files.
- Never copy an older branch document over `main` without comparing the two versions first.

See `docs/development/operating-rules.md` for path ownership and source precedence.

## Documentation and handoff

A change is not Done if it leaves the repository documentation describing the previous state.

Update as applicable in the same PR:

- code/design;
- tests/validation;
- migrations;
- relevant product/architecture documentation;
- the active workstream handoff;
- `docs/PROJECT-STATUS.md` only when global state changes;
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

## Pull requests and coherence gate

Keep PR scope understandable. Draft PRs are appropriate for active work.

Before merge:

1. compare the branch with current `main`;
2. synchronize when needed;
3. inspect overlapping shared documentation semantically, not only for text conflicts;
4. verify no older decision overwrites a newer Accepted decision;
5. verify tests/validation and workstream handoff;
6. update global status only when the merge changes global state.

A branch being technically mergeable is not sufficient if its documentation would make the project state less accurate.

## Architecture changes

Do not casually reopen Accepted ADRs. If new evidence requires a different durable architecture decision, document the context and superseding decision explicitly.

AI agents may propose changes but must not invent project state, bypass domain validation, expose secrets or silently change accepted architectural constraints.

## Secrets and personal data

Never commit API keys, OAuth secrets, signing certificates, production configuration, personal production data, uploaded user files, database backups or credentials.

Use environment-specific secret/configuration mechanisms when deployment environments are introduced.
