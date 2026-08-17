# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 4 QA PASS; Phase 5 read-only requirements inventory next**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Phase 2 PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`
- Phase 3 PRE-SCOPE: `d2f190de06bf0e4e1e491c0c2dc601eb48668da9`
- Phase 3 content HEAD before closure marker: `50731dbee3d2cc661972700ef0bce521b67098c6`
- Phase 4 PRE-SCOPE: `46b963394e29179fadf20cb3b11c35dbf3b6edc2`
- Phase 4 content HEAD before closure markers: `d67cd83f462611b2cc6d341937432e705f7a8682`
- Started: 2026-08-17
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**

## Purpose

This workstream bridges the closed Domain + Logical Models and any later Physical Model authorization.

It makes repository/current architecture truth coherent, defines pre-Physical technical requirements and benchmark inputs, and will close with a clean-room QA before any Physical Model begins.

A genuine material semantic contradiction triggers a separate explicit Domain/Logical reopen. Cleanup or implementation convenience must not silently alter closed semantics.

## Current accepted stage

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL / DOMAIN ATLAS
CLOSED

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active

PRE-PHYSICAL COHERENCE
ACTIVE
Phase 0 PASS
Phase 1 QA PASS
Phase 2 QA PASS
Phase 3 QA PASS
Phase 4 QA PASS
Phase 5 READ-ONLY REQUIREMENTS INVENTORY NEXT

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

## Mandatory bootstrap

Before later work:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read this complete handoff;
9. read `docs/architecture/pre-physical-architecture-baseline.md`, `docs/architecture/README.md` and linked current model/architecture sources;
10. read complete canonical split/continuation chains where a logical document is physically split;
11. read relevant ADR/evidence/methodology;
12. verify current branch/ref and relation to `main`;
13. before any new write phase, issue a fresh exact PRE-SCOPE/write gate.

## Documentation lifecycle rule

Current specifications contain **current truth only**; they are not chronological design logs.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

Before replacing/deleting stale current docs:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

The objective is clean current documentation **without losing useful knowledge**.

A physical split does not create separate logical authority. `*-part-N` continuation chains must be read as one complete logical document. Splitting is a tooling/layout concern, not a reason to create append-only parallel authority.

## Current architecture navigation

Current sources:

- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- accepted complete Domain Atlas + Language Map logical documents;
- closed Whole Logical Model + complete decision/assumption-register logical document + remote closure;
- current ADR statuses;
- this workstream for still-open Pre-Physical obligations.

Historical `docs/architecture/domain-model-logical-readiness*` files remain transition/validation evidence and are not current architecture specifications.

## Non-negotiable Whole-Logical hardenings

Later architecture/Physical/runtime work must preserve:

- `WL-H01` — Agreement terms bind justified material owner/state;
- `WL-H02` — governed operation/effect contract;
- `WL-H03` — bounded projection/disclosure surface;
- `WL-H04` — absence/unknown is not universally false;
- `WL-H05` — expected-state semantics for consequential writes;
- `WL-H06` — idempotency is not semantic identity;
- `WL-H07` — truthful atomic/staged multi-owner consistency;
- `WL-H08` — canonical state != provider sync state;
- `WL-H09` — consequential derived-state use requires freshness/material basis;
- `WL-H10` — retention/redaction/tombstone integrity and non-reused identity;
- `WL-H11` — reconstructible consequential AuthZ provenance;
- `WL-H12` — selective disclosure includes non-interference/inference leakage.

## Semantic non-reopen boundary

Do not create universal Domain owners merely because a product/runtime term is useful.

Unless separately revalidated, terms such as Memory, Agent, Automation, Job, Workflow, Notification, Reminder, Priority, Preference, Context, Task, Workspace, Risk, Focus Time, Out of Office and Working Location remain product/runtime/composition/profile/projection/policy concepts rather than new universal Domain roots.

Product labels such as `Project` and `Program` do not create kernel owners by naming alone; current Domain language maps them to accepted semantics such as a `Plan` profile according to the actual case.

## Completed work

### Phase 0 — freeze/current-state inventory — PASS

The workstream opened from the integrated Domain+Logical baseline with Physical/backend implementation not started. A broader repository-wide clean-room audit remains part of Phase 12 closure.

### Phase 1 — global current-truth entry-point alignment — QA PASS

Original Phase 0+1 PRE-SCOPE:

`148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`

Phase 0+1 final HEAD:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Verified physical classification:

```text
added      1
modified   7
deleted    0
unexpected 0
```

### Phase 2 — architecture supersession/current-truth cleanup — QA PASS

Approved Phase 2 PRE-SCOPE:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Verified content HEAD before closure markers:

`dfc1f4e124f362d342c336485e166c8ac57afba4`

Verified content delta:

```text
linear content commits 17
added                  1
modified              15
deleted                 1
unexpected              0
main changed            0
```

Architecture now states current truth only: Physical persistence remains benchmark-driven; PostgreSQL hybrid is preferred baseline, TypeDB mandatory challenger, Neo4j a secondary/read-projection candidate, event/document bounded candidates, generic universal meta-model rejected, Python/FastAPI/Pydantic retained, SQLAlchemy/Alembic conditional, AI/provider/canonical-state boundaries explicit.

The retired `docs/architecture/personal-data-ai-integration.md` passed knowledge coverage before deletion:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
retired file absent = PASS
historical evidence unchanged = PASS
Domain reopen = 0
Logical reopen = 0
```

### Phase 3 — Backend Foundation handoff cleanup — QA PASS

Approved Phase 3 PRE-SCOPE:

`d2f190de06bf0e4e1e491c0c2dc601eb48668da9`

Phase 3 content HEAD before closure marker:

`50731dbee3d2cc661972700ef0bce521b67098c6`

The future Backend Foundation handoff is now current but deferred. It consumes Domain + Logical rather than recreating them, treats SQLAlchemy/Alembic as Physical-dependent candidates, keeps PostgreSQL as benchmark posture rather than mandate, defers concrete API/Auth/workflow/provider mechanisms, removes the old fixed product-label slice as a canonical contract, and preserves valid future Python/FastAPI/Pydantic/modular-monolith/testing/provider-boundary requirements.

Current prerequisite chain:

```text
CLOSED Domain Atlas
+
CLOSED Logical Model
+
CLOSED Pre-Physical Coherence
+
separately accepted Physical Model
+
applicable accepted runtime/security/integration/API contracts
        ↓
Backend Foundation may become READY TO START
        ↓
fresh branch + fresh PRE-SCOPE/write gate
        ↓
implementation
```

### Phase 4 — Current Pre-Physical Architecture Baseline — QA PASS

#### Read-only inventory result

Phase 4 reconstructed current authority across complete split/continuation logical documents, including the full Domain Atlas/Language Map chains, Whole-Domain closure evidence, the complete Logical decision/register chain and the dedicated Whole-Logical remote closure.

The inventory established that the bridge must coordinate current truth without duplicating or reopening Domain/Logical semantics.

Key rule:

```text
DECIDED CURRENT DIRECTION
!= IMPLEMENTATION AUTHORIZATION

PREFERRED BENCHMARK BASELINE
!= TECHNOLOGY SELECTION
```

#### Approved Phase 4 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
46b963394e29179fadf20cb3b11c35dbf3b6edc2

CREATE
docs/architecture/pre-physical-architecture-baseline.md

UPDATE
docs/architecture/README.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md
docs/workstreams/backend-foundation.md

DELETE
none
```

Phase 4 content HEAD before closure markers:

`d67cd83f462611b2cc6d341937432e705f7a8682`

#### Phase 4 result

`docs/architecture/pre-physical-architecture-baseline.md` is now the current bridge source for:

- current decided architecture direction versus implementation authorization;
- high-risk semantic non-collapse/prohibited shortcuts;
- Logical representation/reference and canonical/history/derived/provider/candidate/security-runtime state separation;
- mandatory `WL-H01..WL-H12` downstream hardenings;
- runtime/product/technical concepts that do not become Domain owners automatically;
- AI/context/integration boundaries already decided versus still open;
- current Physical benchmark posture without technology selection;
- durable-workflow benchmark posture without runtime selection;
- Phase 5–12 ownership for unresolved requirements/benchmark work;
- explicit prohibition on starting Physical/schema/API/Auth/runtime/provider/backend implementation implicitly.

`docs/architecture/README.md` exposes the bridge as current architecture navigation and reinforces that physical split chains are one logical authority.

`docs/workstreams/backend-foundation.md` now names the baseline as mandatory downstream reading while remaining **NOT STARTED / DEFERRED**.

Domain and Logical semantics were not changed. No ADR was changed. No Physical/runtime implementation decision was introduced.

Remote Phase 4 path QA from PRE-SCOPE through the first closure marker returned:

```text
ahead_by       8
behind_by      0
total_commits  8
added           1
modified        7
deleted         0
unexpected      0
```

The eight unique changed paths are exactly the approved gate. `main` remained unchanged.

## Operational anomaly — accidental branch ref

During Phase 4 execution an incorrect tool invocation created an unrelated temporary branch ref:

```text
__no-op__
→ 46b963394e29179fadf20cb3b11c35dbf3b6edc2
```

It does **not** alter `chore/pre-physical-coherence`, `main`, the Phase 4 file delta or any project content. The currently available GitHub connector exposes branch create/update but no `delete_ref`, so this ref could not be removed in-session. It should be deleted as repository hygiene when a branch-delete mechanism is available (for example `git push origin --delete __no-op__`). Do not use it as a work branch or source of truth.

## Current exact task — Phase 5 read-only requirements inventory

Next work is **read-only**. Do not write yet.

Phase 5 must define requirements that can constrain later Physical design without choosing implementation mechanisms.

Inventory and classify at minimum:

1. AuthN/AuthZ;
2. security/privacy/retention/recovery;
3. transaction/consistency/outbox/side effects;
4. non-functional/multi-device/recovery envelope.

Minimum AuthN/AuthZ semantic boundary:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

The Phase 5 read-only pass must identify requirements, assumptions, evidence, unresolved decisions and implementation-deferred mechanisms, then present a fresh exact write gate before any write.

## Remaining roadmap

### Phase 5 — requirements that can constrain Physical design — NEXT

Define requirements, not implementation, for AuthN/AuthZ; security/privacy/retention/recovery; transaction/consistency/outbox/side effects; and non-functional/multi-device/recovery.

### Phase 6 — AI/context/runtime/integration boundaries

Keep distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate/unresolved state
transient LLM working context
```

Runtime Agent/Workflow/Automation/Notification concepts do not become Domain owners automatically.

Integration modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Protocols such as MCP/A2A/future equivalents are adapters, not ontology.

### Phase 7 — durable workflow / async benchmark

Compare at least PostgreSQL + worker + transactional outbox, Temporal, Restate and DBOS. No winner is preselected.

### Phase 8 — governed API/command/effect contract

```text
HTTP route / UI button / AuthZ action string
!= canonical Governed Operation
```

Define the consequential-operation contract before concrete routes.

### Phase 9 — search/observability/calendar/solver pressure

Define requirements/benchmark pressure without premature infrastructure selection.

### Phase 10 — Physical benchmark specification/register

Current posture:

```text
PostgreSQL hybrid — preferred baseline, not selected
TypeDB — mandatory challenger
Neo4j/property graph — secondary/read-projection candidate
event/document mechanisms — bounded candidates
pgvector — bounded semantic-retrieval candidate
generic EAV/generic edge/universal meta-model — hard reject
```

Use destructive LifeOS scenarios: consequential concurrency, multi-owner mutation, selective disclosure, provider divergence, redaction/history, DST recurrence, stale derived state, AuthZ provenance, search inference leakage, AI proposal→approval→effect, revoked governance during execution, crash/restart, restore and schema evolution.

### Phase 11 — repository engineering safety

Establish appropriate main protection/ruleset/CI/required checks before production backend implementation.

### Phase 12 — clean-room QA and closure

Target:

```text
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

Only after Phase 12 closure may the user separately decide whether to authorize a Physical Model workstream.

## Specialized infrastructure rule

Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

## Explicitly out of scope until separately gated

- Domain semantic changes;
- Logical semantic changes;
- Physical Model;
- SQL/schema/indexes/migrations;
- concrete API/backend implementation;
- concrete Auth provider/runtime selection;
- provider adapters;
- frontend/prototype changes inside this workstream;
- direct modification of `main`.

## Exact continuation

```text
PHASE 4
QA PASS

NEXT
PHASE 5 — READ-ONLY REQUIREMENTS THAT CAN CONSTRAIN PHYSICAL DESIGN

NO PHASE 5 WRITES YET
```
