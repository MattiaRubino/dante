# Documentation and Handoff Protocol

- Status: Accepted project workflow
- Last updated: 2026-08-10

## Goal

LifeOS must remain resumable across separate ChatGPT conversations, Claude sessions, Codex tasks, other AI agents and human developers. Repository documentation is therefore part of the implementation, not optional aftercare.

## Canonical reading order

Before modifying the project, a new contributor/agent should read:

1. root `README.md`;
2. `docs/PROJECT-STATUS.md`;
3. the relevant `docs/workstreams/<name>.md` handoff;
4. linked product/architecture documents;
5. linked accepted ADRs;
6. implementation code/tests relevant to the current task.

If repository documentation and conversational memory disagree, stop treating the conversation as authoritative and verify the current repository state.

## Workstream handoff as save game

Every active workstream must maintain one concise operational file that lets another contributor continue without reconstructing the entire project history.

The handoff should record:

- status;
- branch and PR;
- scope/purpose;
- current source-of-truth documents;
- last completed work;
- current task;
- next exact steps;
- known issues/open questions;
- important files/paths;
- tests/validation commands and results;
- decisions that should not be reopened casually;
- last validated commit when code exists.

The handoff should be updated after meaningful progress, not only at the end of a large phase.

## Durable documentation versus operational state

Use the right document for the right job:

- `PROJECT-STATUS.md`: current global project state.
- `ROADMAP.md`: sequencing and broad future direction.
- `workstreams/*.md`: exact operational continuation state.
- `product/*.md`: durable product meaning/behavior.
- `architecture/*.md`: durable system/technical model.
- `decisions/ADR-*.md`: important accepted decisions and rationale.
- code/tests/migrations: executable implementation truth.
- Git history/PR discussion: detailed historical evidence when needed.

Do not turn `PROJECT-STATUS.md` into a giant design document and do not use a workstream handoff as the only record of an architectural decision.

## When an ADR is required

Create or update an ADR when a decision materially affects architecture, persistence strategy, security, deployment model, provider boundaries, data ownership, major framework choice or another durable cross-cutting constraint.

A normal implementation detail does not require an ADR.

Accepted ADRs may be superseded by later ADRs, but should not be silently rewritten to hide the previous decision. Mark supersession explicitly.

## Documentation in the same PR

A change is incomplete if it changes behavior/architecture but leaves documentation describing the previous state.

The same PR should update, when applicable:

- implementation;
- tests;
- migrations;
- durable product/architecture docs;
- workstream handoff;
- global status;
- ADR;
- changelog of significant internal milestones.

## AI-agent protocol

When an AI agent works on LifeOS:

- do not assume conversation history is complete;
- do not invent project state that can be checked in Git;
- read the handoff before continuing a workstream;
- preserve accepted decisions unless new evidence justifies a deliberate change;
- record new durable decisions in the repository;
- record exact remaining work before handing off;
- avoid leaving critical context only inside a chat response;
- do not expose secrets, production personal data or private credentials in prompts, logs or committed docs.

## Historical preservation

Existing documentation should not be deleted merely because a newer summary/index is introduced. Consolidation should normally add navigation/status and integrate accepted work into the canonical branch.

If a document is obsolete, prefer marking it historical/superseded or leaving it in Git history while updating current indexes. Delete only when keeping the file creates real correctness, security, legal or maintenance problems.

## Completion checklist

Before handing a workstream to another chat/agent or merging it:

- [ ] Workstream status reflects reality.
- [ ] Last completed work is explicit.
- [ ] Next exact step is explicit.
- [ ] Important open questions are listed.
- [ ] Relevant source-of-truth docs are linked.
- [ ] Tests/validation are recorded where applicable.
- [ ] Last validated commit is recorded when code exists.
- [ ] `PROJECT-STATUS.md` reflects global changes.
- [ ] Significant durable decisions have an ADR.
