# Documentation and Handoff Protocol

- **Status:** CURRENT / ACCEPTED PROJECT WORKFLOW
- **Last updated:** 2026-08-26

## Goal

DANTE must remain resumable across separate ChatGPT conversations, Claude sessions, Codex tasks, other AI agents and human developers without turning protected `main` into a transcript of every session.

Repository documentation is part of the implementation. The documentation system must preserve both:

```text
fast continuation while a branch is active
+
clean current truth after the branch is integrated
```

Operational branch/path/authority rules live in:

- `agent-operating-manual.md`
- `operating-rules.md`
- `branching-and-environments.md`
- `repository-engineering-safety.md`

Documentation lifecycle/compaction rules live in:

- `documentation-lifecycle-policy.md`

## Canonical reading order

Before modifying the project:

1. root `README.md`;
2. `docs/README.md`;
3. `docs/PROJECT-STATUS.md`;
4. `docs/ROADMAP.md` when sequence matters;
5. `docs/development/agent-operating-manual.md`;
6. `docs/development/operating-rules.md`;
7. this file;
8. `docs/development/documentation-lifecycle-policy.md`;
9. `docs/development/branching-and-environments.md`;
10. `docs/development/repository-engineering-safety.md`;
11. current subsystem/model/architecture sources relevant to the task;
12. current implementation/tests/migrations relevant to the task;
13. current branch/ref and relation to protected `main`;
14. **only if the target branch is active and unmerged**, its branch-local workstream record and temporary handoff if one genuinely exists.

Repository truth beats conversation memory where they disagree.

## Documentation classes

Use the right document type.

### Current specification / status

Examples:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
current product specs
current architecture specs
current Database System of Record
```

These describe **current truth only**. They must not accumulate obsolete chronology as overlays.

### Durable reference / contract

Examples:

```text
ADRs
accepted engineering contracts
PostgreSQL Persistence Constitution
Database Dictionary schema/metadata
current subsystem contracts
```

These retain durable semantics/rationale and evolve deliberately.

### Evidence / validation

Examples:

```text
closure QA
benchmark/research evidence
checkpoints
acceptance matrices
materialization-stage evidence
```

These may preserve historical truth when clearly labelled. They do not automatically become current routing.

### Active branch workstream record

An active unmerged branch may maintain one durable workstream record describing:

- branch/worktree;
- purpose/scope;
- current authority;
- accepted checkpoints;
- exact open boundary;
- next work;
- required validation;
- decisions not to reopen casually.

This record is branch-local until integration.

### Temporary live/session handoff

A temporary handoff exists only to survive a context/session/tool boundary while the branch is active.

It may contain:

- exact current HEAD/PRE-SCOPE;
- in-flight write state;
- immediate resume point;
- tool incidents that materially affect continuation;
- unresolved tactical issues;
- exact commands/QA already executed when useful.

It is **not** durable architecture and **must not merge into protected `main`**.

### Branch history / closure record

After integration, at most one consolidated branch-history record may remain when the branch narrative has continuing audit/debug/maintenance value beyond Git/PR history.

It is non-authoritative and belongs under `docs/archive/branches/` or another explicitly historical location.

## Active branch handoff rule

A new chat/session does **not** create a new branch or worktree.

While a branch is active:

```text
same real workstream
→ same branch
→ same intended worktree
```

A branch may update its durable workstream record after meaningful progress. A temporary live/session handoff is created only when context continuity genuinely needs one; do not generate one for every routine checkpoint.

The handoff should record only what is necessary to resume the branch safely. It must not become the only location for a durable architectural/product decision.

## Protected-main handoff rule

Protected `main` must not contain active-session continuation documents such as:

```text
*-live-handoff*.md
*-session-handoff*.md
chat-transfer notes
resume-this-chat files
```

Before a branch can merge:

```text
temporary handoff payload
        ↓
knowledge coverage
        ↓
current truth → current specs/status
rationale → ADR/reference
important evidence → QA/checkpoint/branch history
later requirement → roadmap/register
superseded tactical state → Git only
        ↓
optional ONE consolidated branch-history record
        ↓
all temporary handoff files deleted
```

Merge gate:

```text
temporary handoffs entering main = 0
unclassified meaningful handoff content = 0
valid requirement lost = 0
important rationale/evidence lost = 0
current routing references repaired = PASS
```

## Current truth vs historical evidence

DANTE deliberately distinguishes:

```text
CURRENT SPECIFICATION
= current truth only

ADR / DURABLE REFERENCE
= accepted rationale/contract + explicit evolution/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology/evidence

GIT / PR
= complete recoverable change history
```

If `A` is replaced by `B`, a current specification describes `B`. Do not leave:

```text
A current
→ A failed
→ B proposed
→ B revised
→ B current
```

inside a current status/spec and expect a reader to resolve the newest banner.

Historical evidence may preserve that chronology when the chronology itself remains useful.

## Git as history

Git is the complete backup/history mechanism.

A stale document does not remain in the current tree merely because history exists. Keep historical files in-tree only when they have enough continuing evidentiary/rationale value to justify the navigation cost.

Do not create `old/`, `backup/` or dated copies of every current file merely to preserve earlier versions.

Selective historical material uses `docs/archive/`, whose contents are explicitly non-authoritative.

## Knowledge-coverage gate before replace/delete/compact

Before replacing, deleting or compacting stale documentation, classify every meaningful statement.

Possible dispositions:

```text
current truth
→ keep/rewrite in current source

current truth owned elsewhere
→ verify representation there

accepted rationale/contract
→ durable reference / ADR

important evidence
→ evidence/checkpoint/closure/branch history

future requirement
→ roadmap/register

superseded tactical chronology
→ Git history sufficient

duplicate/no continuing value
→ discard
```

Required gate:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
continuing rationale represented = PASS
important evidence represented = PASS
references/navigation repaired = PASS
```

The goal is **clean current documentation without knowledge loss**.

## Split-document rule

A canonical split may be one logical document across multiple Git paths.

Example:

```text
domain-model.md
+ domain-model-part-2.md
+ domain-model-part-3.md
= one logical document
```

### Tool/size split

If splitting exists only because of connector/write/size limits, the physical parts must reconstruct the complete logical payload losslessly.

A tool-limit split must not:

- summarize away detail;
- replace requirements with a recap;
- paraphrase away material semantics;
- omit decisions/evidence;
- hide semantic cleanup inside a claimed structural split.

### Frozen/read-only compaction

When a logical document is closed/frozen and no longer needs frequent incremental writes, it may be recomposed into fewer files or stable topic-based partitions when that materially improves maintainability.

Compaction is allowed only if:

```text
all still-valid substantive content preserved
all accepted decisions/invariants preserved
all valid requirements preserved
all continuing rationale preserved
all important evidence preserved or durably rehomed
all links/authority routing repaired
```

Do not turn a 20-part frozen reference into a short summary and call it lossless compaction.

### Chronological continuation

A sequence of amendments/continuations created over time is not automatically a good final current specification.

After closure, classify it:

```text
current substance
→ rewrite into current reference

important chronology/evidence
→ evidence/archive if useful

superseded status/routing wrappers
→ remove / Git
```

Prefer stable semantic/topic boundaries over endless `part-17`, `part-18`, `part-19` chronology when the document is frozen and can be safely reorganized.

## Global-file discipline

To reduce conflicts:

- normal incremental branch progress → branch-local workstream record;
- temporary session continuity → branch-local temporary handoff only when needed;
- global state/sequence change → `PROJECT-STATUS.md` / `ROADMAP.md`;
- current architecture/product meaning change → current durable source;
- significant architectural decision → ADR/reference update;
- structural database change → Database System-of-Record artifacts in the same reviewed change;
- repository policy change → safety/branching/lifecycle docs + live setting where applicable;
- before merging shared/global files → reconcile against current protected `main`.

A clean textual merge is not enough if documentation becomes stale.

## Documentation in the same product/code change

A change is incomplete if behavior/architecture changes while current documentation still describes the old state.

Update as applicable:

- implementation;
- tests;
- migrations;
- current product/architecture docs;
- Database Dictionary/reference/generated artifacts for structural DB changes;
- branch-local workstream record while active;
- global status/roadmap when globally meaningful;
- ADR/durable reference;
- significant evidence/closure record.

Do **not** merge temporary session handoffs merely because they were useful during implementation.

## Database same-change rule

`docs/database/README.md` defines the DANTE Database System of Record.

A structural database change is incomplete when executable schema changes but affected current database documentation does not change with it.

As applicable keep aligned:

```text
Alembic migration
SQLAlchemy metadata / mapping
Database Dictionary
human-readable Database Architecture & Reference
generated schema reference / diagrams
direct database tests
```

A new table without its required Dictionary entry is incomplete. Prefer generation for mechanically derivable facts; preserve human-authored purpose/invariant/rationale where DDL cannot explain meaning.

## AI-agent protocol

AI agents must:

- not assume conversation history is complete;
- not invent state Git/GitHub can verify;
- verify branch/ref relation before writes;
- preserve accepted semantics unless deliberately changing them;
- not promote historical evidence over newer current truth;
- keep current specs current rather than append-only;
- run knowledge coverage before delete/replace/compaction;
- keep structural DB changes synchronized with the Database System of Record;
- distinguish documented intended policy from remotely effective settings;
- keep temporary handoffs branch-local;
- remove/consolidate temporary handoffs before integration;
- avoid secrets, production personal data and credentials in prompts/logs/docs.

## Tool-limit failure rule

When Git/GitHub/connector/network limits prevent safe work, record in the active branch only as needed:

- exact attempted operation/error;
- writes that actually landed;
- writes that did not;
- current verified branch/HEAD;
- remaining scope;
- QA done/still required;
- safe next action.

A failed/conflicted call is not a completed change.

Once the branch closes, these tactical details remain only if they have continuing audit value; otherwise Git/tool history is sufficient.

## Completion checklist

Before branch integration:

- [ ] branch relation to current protected `main` verified;
- [ ] workstream state reflects reality;
- [ ] current source-of-truth docs updated;
- [ ] tests/validation/QA recorded where meaningful;
- [ ] no historical source overrides newer current truth;
- [ ] current specs contain current truth rather than obsolete chronology;
- [ ] any replaced/deleted/compacted docs passed knowledge coverage;
- [ ] significant durable decisions have ADR/reference treatment;
- [ ] structural DB changes keep Database System-of-Record artifacts aligned;
- [ ] live repository settings relied on as evidence were remotely verified where possible;
- [ ] temporary live/session handoff count entering `main` = 0;
- [ ] optional branch history count ≤ 1 and clearly non-authoritative;
- [ ] no knowledge lost because of tool/context limits;
- [ ] any split-doc compaction is demonstrably lossless.
