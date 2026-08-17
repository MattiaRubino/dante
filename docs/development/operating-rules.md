# LifeOS Operating Rules

- Status: Accepted project workflow
- Last updated: 2026-08-17

## Purpose

These rules define where work happens, which source wins when information conflicts, how parallel workstreams avoid overwriting one another, and what every human or AI agent must do before and after modifying LifeOS.

The goal is to make the repository resumable and safe across multiple ChatGPT conversations, Claude sessions, Codex tasks and human contributors without relying on conversational memory.

The stricter execution mechanics in [`agent-operating-manual.md`](agent-operating-manual.md) are mandatory and apply together with this file.

## 1. Authority order

When two sources disagree, use this order of authority unless a newer accepted decision explicitly supersedes it:

1. current `main` code, migrations, tests and accepted ADRs/current model decisions;
2. current durable product/domain/logical/architecture documentation on `main`;
3. the active workstream handoff for newer unmerged work on its branch;
4. other files on the active workstream branch that are explicitly in progress;
5. old branches, closed/merged PRs and Git history;
6. conversation history or remembered context.

An old branch never overrides a newer accepted decision simply because its document is more detailed.

An older Accepted ADR or architecture document may be explicitly qualified/superseded by later accepted Domain/Logical/ADR/current-baseline work. Status labels must be interpreted together with chronology and supersession links rather than as timeless authority.

Before copying or merging a document from another branch, compare it with the current `main` version and preserve the newest accepted decisions.

## 2. Where work happens

- `main` is the only integrated source of truth for accepted project state.
- Normal implementation work starts from current `main` on a bounded `feature/*` or `fix/*` branch.
- Documentation/governance/coherence work may use `docs/*` or `chore/*` as appropriate.
- Exploratory UX or technical experiments may use `prototype/*`.
- A long-running workstream keeps one primary active branch. Do not create parallel helper branches unless there is a concrete need.
- Do not work directly on `main` except for an explicitly approved emergency repository repair.
- DEV, UAT and PROD are environments, not branches.

## 3. Workstream path ownership

Parallel workstreams should avoid editing the same files unnecessarily.

Current/typical ownership:

- Phase 4 Home/Today: `docs/phase-4/`, relevant `docs/ux/`, prototype/archive paths, prototype regression material and `docs/workstreams/today-home.md`.
- Pre-Physical Repository & Architecture Coherence: current global/index/architecture/workflow documentation explicitly gated under `chore/pre-physical-coherence`, plus `docs/workstreams/pre-physical-coherence.md`.
- Backend Foundation: **not currently started**; future backend bootstrap/configuration/infrastructure paths, backend tests/docs and `docs/workstreams/backend-foundation.md` only after required architecture/model prerequisites are accepted.
- Core Domain Model / Domain Atlas: **closed and integrated**; `feature/domain-model` is historical. Domain semantic changes require an explicit reopen scope rather than being smuggled into backend/cleanup work.
- Logical Model: **closed and integrated**; `feature/logical-model` is historical. Logical semantic changes likewise require an explicit reopen scope.

Shared/global files such as `README.md`, `docs/PROJECT-STATUS.md`, `docs/ROADMAP.md`, broad architecture documents and ADRs should be edited only when the work actually changes global/current project truth and the exact paths are included in an approved write gate.

If two active workstreams would materially edit the same shared/current architecture sources, sequence them or explicitly synchronize them instead of allowing parallel silent divergence.

## 4. Start-of-work protocol

Before making changes:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read this file and `docs/development/documentation-and-handoff.md`;
6. read `docs/development/branching-and-environments.md`;
7. read the complete relevant `docs/workstreams/<name>.md` logical handoff, including required continuation/split parts;
8. read linked accepted product/domain/logical/architecture documents and ADRs;
9. inspect the current branch/PR and compare it with current `main`;
10. if the active branch is behind `main`, synchronize it before making overlapping changes where practical;
11. inspect existing implementation/tests before assuming something is missing;
12. check whether the requested decision already exists before creating a new one.

Do not start from an old branch merely because it contains a familiar file. Start from `main` unless the current workstream handoff explicitly names another active branch.

## 5. During-work protocol

- Keep the change inside the workstream scope and approved exact write gate.
- Update the workstream handoff after meaningful milestones so another agent can resume without the chat.
- Prefer workstream-local documents/code/tests over editing global status files repeatedly.
- Do not change an Accepted ADR or closed Domain/Logical semantic decision implicitly. If evidence requires a new direction, use the correct explicit supersession/reopen process.
- Do not silently replace a newer `main` document with an older branch version.
- Do not put important new project knowledge only in a chat response.
- Do not create database schema, provider contracts or cross-cutting conventions solely because an AI suggested them; durable changes follow normal stage/gate/review rules.
- Do not force-push shared branches or rewrite accepted history without explicit reason and review.
- Do not delete documentation, branches or historical artifacts merely to make the repository look cleaner.
- Do not treat a technical/runtime convenience concept as a new Domain owner without semantic evidence and the required reopen methodology.

## 6. Global-status rule

The workstream handoff is the live save game for incremental work.

`docs/PROJECT-STATUS.md` is the global project view and should change only when something globally meaningful changes, for example:

- a workstream starts, finishes, becomes blocked or changes branch/PR;
- an accepted architectural/product/model decision changes;
- a major milestone merges;
- the immediate project sequence changes.

Do not edit `PROJECT-STATUS.md` for every prototype iteration, local refactor or small implementation step. This prevents parallel branches from constantly conflicting on the same global file.

The same principle applies to root `README.md`, `docs/README.md`, `docs/ROADMAP.md`, broad architecture indexes and ADRs.

## 7. Documentation status semantics

Use status labels consistently:

- **Accepted**: durable decision/current baseline at its stated stage; later explicit supersession may qualify it.
- **Current**: authoritative operational state at the time of the last update.
- **In progress**: active unmerged work that may still change.
- **Draft / Proposed**: not yet accepted.
- **Study / Exploration**: evidence or discovery, not binding implementation truth.
- **Historical / Superseded**: preserved for context but not current instruction.
- **Partially superseded / Qualified**: some content remains useful/accepted while later sources constrain or replace specific claims.

When a document is superseded or materially qualified, identify the newer source where practical instead of leaving future agents to infer which version wins.

## 8. Pre-merge coherence gate

Before merging a branch into `main`:

1. compare the branch against current `main`;
2. synchronize/rebase/merge current `main` as appropriate if the branch is behind;
3. inspect every shared documentation file changed by both sides;
4. verify that no older decision overwrites a newer Accepted/current decision;
5. verify ADR/model status and supersession/reopen links;
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
- leave old branches/history intact until normal housekeeping; they are no longer authoritative once accepted work is integrated.

## 10. Handoff to another AI or chat

A new agent should be able to continue from the repository by following the mandatory bootstrap order in the agent operating manual and reading the active workstream handoff.

The outgoing agent/workstream must record:

- last completed change;
- exact current task;
- next exact steps;
- branch and PR;
- important files;
- validation already performed;
- known problems/open questions;
- last validated commit when implementation exists;
- current approved PRE-SCOPE/write state when a gate is in flight;
- relevant failed/no-op tool operations when they affect continuation.

If that information exists only in the conversation, the handoff is incomplete.

## 11. Current repository coherence baseline

The 2026-08-10 coherence baseline is historical and must not be assumed indefinitely.

As of the start of the 2026-08-17 Pre-Physical Coherence workstream:

- current accepted `main` baseline is `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`;
- Core Domain Model / Domain Atlas is closed and integrated via PR #10;
- Logical Model is closed and integrated via PR #11;
- `main` was globally aligned after those merges via PR #12;
- `chore/pre-physical-coherence` is the active bounded backend/architecture preparation branch;
- `prototype/phase-4-today-home` remains a separate active UX/prototype branch;
- Backend Foundation is not started and must not run from its stale pre-Domain handoff;
- Physical Model is not started and requires separate future authorization.

Future contributors must re-check all refs and current handoffs rather than assuming this statement remains true forever.

## 12. Current stage boundary — Pre-Physical Coherence

Until the active Pre-Physical workstream closes:

- do not start the Physical Model implicitly;
- do not start SQL/schema/migrations/API/backend/Auth/provider implementation implicitly;
- do not reopen Domain/Logical semantics as part of documentation cleanup;
- if a genuine material semantic contradiction is discovered, record it and open a separate explicit reopen scope;
- older architecture/ADR wording may be marked qualified/superseded, but historical checkpoints must retain truthful chronology;
- benchmark preparation may evaluate technologies without adopting them.

The active detailed roadmap is [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md).

## 13. 2026-08-15 mandatory agent-execution hardening

The stricter cross-session execution standard is defined in [`agent-operating-manual.md`](agent-operating-manual.md) and remains mandatory.

In particular:

- exact Git write gate with branch, pre-scope SHA, exact CREATE/UPDATE/DELETE paths, purpose and explicit out-of-scope;
- re-fetch of branch HEAD before the first approved write; SHA drift requires STOP/re-gate;
- post-write compare against the approved pre-scope; unexpected physical paths are QA failure;
- no silent out-of-scope fixes or scope expansion;
- preservation-first documentation updates and truthful historical amendments;
- no truncation/knowledge loss because of connector/context limits;
- canonical split documents count as one logical document while their physical paths remain individually auditable in Git scope/QA;
- chronological amendments belong at the end of the logical canonical document;
- explicit STOP/report behavior for Git/connector/network/tool failures;
- remote repository evidence, not attempted tool calls, determines whether a write is complete;
- workstream-specific mandatory methodologies remain binding, including Domain Validation Methodology v3 for any separately authorized Domain reopen/new validation.

The detailed manual is authoritative for these stricter mechanics unless a higher-authority current accepted project decision explicitly supersedes it.