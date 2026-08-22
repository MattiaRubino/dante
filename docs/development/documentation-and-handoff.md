# Documentation and Handoff Protocol

- Status: Accepted project workflow
- Last updated: 2026-08-22

## Goal

LifeOS must remain resumable across separate ChatGPT conversations, Claude sessions, Codex tasks, other AI agents and human developers. Repository documentation is part of the implementation, not optional aftercare.

Operational branch/path/authority rules are defined in [`agent-operating-manual.md`](agent-operating-manual.md) and [`operating-rules.md`](operating-rules.md). Repository integration enforcement is defined in [`repository-engineering-safety.md`](repository-engineering-safety.md).

## Canonical reading order

Before modifying the project, read:

1. root `README.md`;
2. `docs/README.md`;
3. `docs/PROJECT-STATUS.md`;
4. `docs/development/agent-operating-manual.md`;
5. `docs/development/operating-rules.md`;
6. this file;
7. `docs/development/branching-and-environments.md`;
8. `docs/development/repository-engineering-safety.md`;
9. the active workstream handoff;
10. current model/architecture index and linked current sources;
11. relevant ADRs/evidence/methodologies;
12. implementation/tests relevant to the task;
13. current branch/ref and relation to `main`.

Repository truth beats conversation memory where they disagree.

## Workstream handoff as save-game

Every active workstream maintains one concise operational source that allows continuation without reconstructing chat history.

The handoff should record:

- status;
- branch/PR;
- scope/purpose;
- current sources of truth;
- last completed milestone;
- exact current task and next steps;
- known issues/open questions;
- important paths;
- validation/QA results;
- decisions that should not be casually reopened;
- validated/current commit where applicable;
- in-flight PRE-SCOPE/write state;
- meaningful failed/no-op tool incidents that affect continuation.

Update it after meaningful progress, not only at the end.

## Durable documentation versus operational state

Use the right document type:

- `PROJECT-STATUS.md` — current global state;
- `ROADMAP.md` — current sequence/broad future direction;
- `workstreams/*.md` — exact operational continuation;
- `product/*.md` — current durable product meaning/behavior where marked current;
- `architecture/*.md` — current durable system/technical model where marked current;
- `decisions/ADR-*.md` — decision rationale plus explicit current status/supersession;
- `database/*` — current database architecture/reference/dictionary/generated-documentation system of record;
- checkpoints/validation/research — historical or current evidence as explicitly labelled;
- code/tests/migrations — executable implementation truth;
- Git/PR history — recoverable detailed history.

Do not use a workstream handoff as the only durable record of an architectural decision.

## Current truth vs historical evidence

LifeOS deliberately distinguishes current specifications from historical evidence.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit current status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable complete change history
```

### Current specifications

Current specifications should not accumulate obsolete design chronology.

If `A` is replaced by `B`, the current specification describes `B`. It may include only the minimum prior context needed to understand the current constraint.

Do not leave `A`, `A failed`, `B proposed`, `B revised` as a running story inside a current architecture/product/status document.

### ADRs

ADRs preserve material decision rationale. When superseded/qualified, update the status and replacement authority explicitly without pretending the original decision never existed.

### Historical evidence/checkpoints

Historical checkpoints, validation records and transition evidence preserve what was true/tested at the time. Do not rewrite them to look current.

### Git as history

A stale document does not need to remain in the current working tree merely because history matters. Git retains the old payload. Keep a historical file in-tree only when it still provides continuing evidentiary/rationale value that is useful enough to justify its presence.

## Knowledge-coverage gate before replacing/deleting stale current docs

Before replacing or deleting a stale current document, classify every meaningful statement.

Possible dispositions:

- current truth → keep in current source;
- current truth → move to the correct current source;
- rationale → ADR;
- evidence → checkpoint/research/history source;
- later requirement → explicit roadmap/requirement register;
- superseded → Git history is sufficient;
- duplicate/no continuing value → discard.

Required deletion/replacement gate:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

The goal is **clean current documentation without knowledge loss**.

## Global-file discipline

To reduce conflicts:

- normal incremental progress → update workstream handoff;
- global state/sequence changes → update `PROJECT-STATUS.md` / `ROADMAP.md` as appropriate;
- current architecture/product meaning changes → update the current durable source;
- significant architectural decision/rationale changes → update/create ADR;
- structural database changes → update the applicable `docs/database/` system-of-record artifacts in the same reviewed change;
- repository protection/runtime policy changes → update `repository-engineering-safety.md` and effective remote settings as applicable;
- before merging shared/global files, compare against current `main` and preserve newest current truth.

A clean textual merge is not enough if documentation becomes stale.

## When an ADR is required

Create/update an ADR when a decision materially affects architecture, persistence strategy, security, deployment model, provider boundaries, data ownership, major framework choice or another durable cross-cutting constraint.

Normal implementation details do not require ADRs.

Accepted ADRs may be superseded; mark that explicitly.

A requirement hardening that preserves an existing architectural decision does not automatically require a new ADR. For example, requiring reproducible evaluation before promoting consequential AI behavior changes strengthens the current AI boundary without selecting a provider/model/evaluation product.

## Documentation in the same PR

A change is incomplete if behavior/architecture changes while current documentation still describes the old state.

Update as applicable:

- implementation;
- tests;
- migrations;
- current product/architecture docs;
- database reference/dictionary/generated artifacts for structural DB changes;
- workstream handoff;
- global status/roadmap when meaningful;
- ADR;
- significant milestone/change record where useful.

### Database same-change rule

`docs/database/README.md` defines the DANTE Database System of Record.

A structural DANTE database change is incomplete when the executable schema changes but the affected current database documentation does not change with it.

As applicable, one reviewed database change keeps aligned:

```text
Alembic migration
SQLAlchemy metadata / mapping
Database Dictionary
human-readable Database Architecture & Reference
generated schema reference / diagrams
direct database tests
```

A new table without its required dictionary entry is incomplete. A structural change that leaves current database reference material describing the old schema is incomplete.

Prefer generation for facts that can be derived reliably from SQLAlchemy/PostgreSQL; preserve human-authored semantic purpose/invariant/rationale where DDL cannot explain meaning.

## AI-agent protocol

AI agents must:

- not assume chat history is complete;
- not invent state that Git can verify;
- follow bootstrap/operating rules;
- verify `main` and active branch before writes;
- preserve accepted semantics unless deliberate evidence justifies change;
- not promote historical detail over newer current truth;
- keep current specifications current rather than append-only;
- run knowledge coverage before replacing/deleting stale current docs;
- record durable decisions/continuation in repo;
- keep structural database changes synchronized with the Database System of Record;
- distinguish documented repository policy from remotely effective repository settings;
- avoid secrets, production personal data and credentials in prompts/logs/docs.

## Split-document handoff rule

A canonical split is one logical document with multiple physical Git paths.

```text
domain-model.md + domain-model-part-2.md + domain-model-part-3.md
= 1 logical document
= 3 physical paths
```

Git gates/QA enumerate each physical path.

### Size / tool-limit split

When a split exists only because of file size, connector limits, write limits or another tooling/transport constraint, it is a **lossless physical partition of one complete logical payload**.

```text
complete logical payload
→ physical parts
→ complete logical payload reconstructible from all canonical parts
```

A size/tool-limit split must **not** summarize, condense, replace prior detail with a recap, paraphrase away substantive content, omit requirements/evidence/decisions, or hide semantic cleanup inside the split.

If the document also needs semantic/current-truth editing, perform and describe that as a separate content operation. Do not call a summary or rewrite a `split`.

### Chronological / evidence continuation

For chronological/evidence chains, a new session reads the complete required sequence. Do not treat Part 1 as current merely because it carries the original filename.

Later evidence may legitimately be appended after the previous final payload in a continuation part. That evidence-continuation behavior is distinct from losslessly partitioning one already-defined payload because of size/tool limits.

### Current specifications

Current specifications should not be split merely to preserve obsolete history; rewrite them cleanly where safe through an explicit current-truth edit. A current-truth rewrite must not be disguised as a lossless split.

## Tool-limit handoff rule

When Git/GitHub/connector/network limitations prevent safe work, the handoff states:

- exact attempted operation/error;
- writes that actually landed;
- writes that did not;
- current verified branch/HEAD where possible;
- remaining scope;
- QA already done/still required;
- safe next action.

A failed/conflicted call is not a completed change.

## Repository-safety handoff rule

A workstream that depends on branch rules, required checks or security/integration settings must distinguish:

```text
documented intended policy
!= remotely verified effective state
```

If the connector cannot read a security setting because of integration permissions, record it as connector-unverifiable rather than inventing PASS/FAIL. If a required check does not yet exist as a stable real check context, do not manufacture it merely to make a policy look complete.

## Completion checklist

Before handoff or merge:

- [ ] branch relation to current `main` verified;
- [ ] workstream status reflects reality;
- [ ] last completed milestone explicit;
- [ ] next exact step explicit;
- [ ] open questions listed;
- [ ] current source-of-truth docs linked;
- [ ] tests/validation/QA recorded;
- [ ] validated/current commit recorded where relevant;
- [ ] no historical source overrides newer current truth;
- [ ] current specs contain current truth rather than obsolete chronology;
- [ ] any replaced/deleted stale current doc passed knowledge coverage;
- [ ] global status changed only when globally meaningful;
- [ ] significant durable decisions have ADR treatment;
- [ ] structural database changes keep Database System-of-Record artifacts aligned;
- [ ] repository settings relied on as evidence were remotely verified where the connector permits;
- [ ] no knowledge was lost because of tool/context limits;
- [ ] any size/tool-limit split preserves the complete logical payload losslessly rather than summarizing it.