# LifeOS Operating Rules

- Status: Accepted project workflow
- Last updated: 2026-08-10

## Purpose

These rules define where work happens, which source wins when information conflicts, how parallel workstreams avoid overwriting one another, and what every human or AI agent must do before and after modifying LifeOS.

The goal is to make the repository resumable and safe across multiple ChatGPT conversations, Claude sessions, Codex tasks and human contributors without relying on conversational memory.

## 1. Authority order

When two sources disagree, use this order of authority unless a newer accepted decision explicitly supersedes it:

1. current `main` code, migrations, tests and accepted ADRs;
2. current durable product/architecture documentation on `main`;
3. the active workstream handoff for unmerged work on its branch;
4. other files on the active workstream branch that are explicitly in progress;
5. old branches, closed/merged PRs and Git history;
6. conversation history or remembered context.

An old branch never overrides a newer accepted decision simply because its document is more detailed.

Before copying or merging a document from another branch, compare it with the current `main` version and preserve the newest accepted decisions.

## 2. Where work happens

- `main` is the only integrated source of truth for accepted project state.
- Normal implementation work starts from current `main` on a bounded `feature/*` or `fix/*` branch.
- Documentation/governance work uses `docs/*`.
- Exploratory UX or technical experiments may use `prototype/*`.
- A long-running workstream keeps one primary active branch. Do not create parallel helper branches unless there is a concrete need.
- Do not work directly on `main` except for an explicitly approved emergency repository repair.
- DEV, UAT and PROD are environments, not branches.

## 3. Workstream path ownership

Parallel workstreams should avoid editing the same files unnecessarily.

Typical ownership:

- Phase 4 Home/Today: `docs/phase-4/`, relevant `docs/ux/`, `prototypes/today/`, prototype regression tests and `docs/workstreams/today-home.md`.
- Backend Foundation: backend bootstrap/configuration/infrastructure paths, backend tests, backend documentation and `docs/workstreams/backend-foundation.md`.
- Domain Model: domain-model code/tests/docs and `docs/workstreams/domain-model.md`; if it is being developed inside Backend Foundation, use that same branch rather than opening two branches that edit the same files.

Shared/global files such as `README.md`, `docs/PROJECT-STATUS.md`, `docs/ROADMAP.md`, cross-cutting architecture documents and ADRs should be edited only when the work actually changes global project truth.

## 4. Start-of-work protocol

Before making changes:

1. read `README.md`;
2. read `docs/PROJECT-STATUS.md`;
3. read this file and `docs/development/documentation-and-handoff.md`;
4. read the relevant `docs/workstreams/<name>.md`;
5. read linked accepted product/architecture documents and ADRs;
6. inspect the current branch/PR and compare it with current `main`;
7. if the active branch is behind `main`, synchronize it before making overlapping changes where practical;
8. inspect existing implementation/tests before assuming something is missing;
9. check whether the requested decision already exists before creating a new one.

Do not start from an old branch merely because it contains a familiar file. Start from `main` unless the workstream handoff explicitly names another active branch.

## 5. During-work protocol

- Keep the change inside the workstream scope.
- Update the workstream handoff after meaningful milestones so another agent can resume without the chat.
- Prefer code/tests/domain documents local to the workstream over editing global status files repeatedly.
- Do not change an Accepted ADR implicitly. If evidence requires a new direction, create/update an ADR and state what it supersedes.
- Do not silently replace a newer `main` document with an older branch version.
- Do not put important new project knowledge only in a chat response.
- Do not create database schema, provider contracts or cross-cutting conventions solely because an AI suggested them; durable changes follow normal review/documentation rules.
- Do not force-push shared branches or rewrite accepted history without explicit reason and review.
- Do not delete documentation, branches or historical artifacts merely to make the repository look cleaner.

## 6. Global-status rule

The workstream handoff is the live save game for incremental work.

`docs/PROJECT-STATUS.md` is the global project view and should change only when something globally meaningful changes, for example:

- a workstream starts, finishes, becomes blocked or changes branch/PR;
- an accepted architectural/product decision changes;
- a major milestone is integrated into `main`;
- the immediate project sequence changes.

Do not edit `PROJECT-STATUS.md` for every prototype iteration, local refactor or small implementation step. This prevents parallel branches from constantly conflicting on the same global file.

The same principle applies to root `README.md` and broad architecture indexes.

## 7. Documentation status semantics

Use status labels consistently:

- **Accepted**: durable decision/current baseline.
- **Current**: authoritative operational state.
- **In progress**: active unmerged work that may still change.
- **Draft / Proposed**: not yet accepted.
- **Study / Exploration**: evidence or discovery, not binding implementation truth.
- **Historical / Superseded**: preserved for context but not current instruction.

When a document is superseded, identify the newer source where practical instead of leaving future agents to infer which version wins.

## 8. Pre-merge coherence gate

Before merging a branch into `main`:

1. compare the branch against current `main`;
2. synchronize/rebase/merge current `main` as appropriate if the branch is behind;
3. inspect every shared documentation file changed by both sides;
4. verify that no older decision overwrites a newer Accepted decision;
5. verify ADR status and supersession links;
6. verify workstream handoff, tests and validation results;
7. update global status only if the merge changes global state;
8. confirm no secrets, production personal data, credentials or local-only artifacts were introduced;
9. merge through PR after the branch is coherent.

A clean Git merge is not enough: semantic/documentation coherence must also be checked.

## 9. After-merge protocol

After an important merge:

- verify `main` contains the intended final versions;
- refresh `PROJECT-STATUS.md` if the merge changed global state;
- update the workstream status to completed/next phase where applicable;
- synchronize any long-running active branch that now shares changed global files;
- leave old branches/history intact until normal housekeeping; they are no longer authoritative once their work is integrated.

## 10. Handoff to another AI or chat

A new agent should be able to continue from the repository by reading:

```text
README.md
→ docs/PROJECT-STATUS.md
→ docs/development/operating-rules.md
→ docs/workstreams/<active-workstream>.md
→ linked product/architecture docs and ADRs
→ relevant code/tests
```

The outgoing agent must record:

- last completed change;
- exact current task;
- next exact steps;
- branch and PR;
- important files;
- validation already performed;
- known problems/open questions;
- last validated commit when implementation exists.

If that information exists only in the conversation, the handoff is incomplete.

## 11. Current repository coherence baseline

As of 2026-08-10, the historical documentation branches have been integrated into `main` and no longer contain unique accepted work ahead of it. The active `prototype/phase-4-today-home` branch is intentionally ahead only for Phase 4 UX/prototype/test work and is synchronized with the current accepted project baseline.

Future contributors must re-check this statement against Git rather than assuming it remains true forever.
