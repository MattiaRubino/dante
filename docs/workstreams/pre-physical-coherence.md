# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 3 QA PASS; Phase 4 read-only baseline inventory next**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Phase 2 PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`
- Phase 3 PRE-SCOPE: `d2f190de06bf0e4e1e491c0c2dc601eb48668da9`
- Phase 3 content HEAD before this closure marker: `50731dbee3d2cc661972700ef0bce521b67098c6`
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
Phase 4 READ-ONLY BASELINE INVENTORY NEXT

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
9. read `docs/architecture/README.md` and linked current model/architecture sources;
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

A physical split does not create separate logical authority. `*-part-N` continuation chains must be read as the complete logical document before current-state conclusions are drawn.

## Current architecture navigation

Current sources:

- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- accepted Domain Atlas;
- closed Whole Logical Model;
- current ADR statuses;
- this workstream for open pre-Physical obligations.

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

Approved/final physical path set:

```text
CREATE
docs/architecture/README.md

UPDATE
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md
docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/decisions/ADR-002-backend.md
docs/decisions/ADR-003-primary-database.md
docs/decisions/ADR-005-ai-gateway.md
docs/decisions/ADR-006-hybrid-personal-data-model.md
docs/decisions/ADR-007-domain-model-informed-persistence-boundaries.md

DELETE
docs/architecture/personal-data-ai-integration.md
```

Verified content delta:

```text
linear content commits 17
added                  1
modified              15
deleted                 1
unexpected              0
main changed            0
```

The native GitHub compare endpoint returned `404` and was **not** counted as PASS. Equivalent scope was proven through remote branch/main refs, a bounded linear commit chain, one approved physical path per content commit, per-commit path status, remote payload readback, remote absence of the retired file and proof that historical readiness evidence retained its original blob.

### Phase 2 architecture result

Current architecture now states only current truth:

- Physical persistence is open/benchmark-driven rather than already selected;
- PostgreSQL hybrid is preferred baseline, not final selection;
- TypeDB is mandatory challenger;
- Neo4j/property graph remains a secondary/read-projection candidate;
- event/document mechanisms remain bounded candidates;
- generic EAV/generic-edge/universal meta-model remains rejected;
- Python + FastAPI + Pydantic remain backend direction;
- SQLAlchemy/Alembic are conditional on accepted Physical design;
- AI remains provider-neutral, proposal/candidate/governed-effect bounded;
- provider state remains distinct from canonical LifeOS state;
- integration modes are separated;
- specialized infrastructure uses the demonstrated-benefit rule;
- historical Domain→Logical readiness files are explicitly evidence, not current architecture.

ADR status is now explicit:

- ADR-001 — accepted;
- ADR-002 — accepted with ORM/migration qualification;
- ADR-003 — superseded as final database selection, PostgreSQL rationale retained;
- ADR-004 — accepted;
- ADR-005 — accepted/current with Logical-model qualification;
- ADR-006 — superseded as canonical generic hybrid semantic architecture;
- ADR-007 — accepted semantic guardrail, qualified for Physical posture.

### Phase 2 knowledge-coverage verdict

The retired `docs/architecture/personal-data-ai-integration.md` was deleted only after all meaningful content was classified.

Final coverage verdict:

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

#### Read-only audit result

The complete current Backend Foundation handoff was audited against current entry points, current architecture, current ADR statuses, the closed Whole Logical Model, its final decision/hardening register and closure evidence, and the current accepted Domain Atlas/language disposition including relevant continuation parts.

The audit confirmed:

```text
Domain reopen required                 0
Logical reopen required                0
unclassified meaningful content        0
valid future requirement lost          0
stale execution assumptions identified PASS
current prerequisite chain identified  PASS
```

Key classification:

```text
old READY TO START
SUPERSEDED

Domain Model v0 inside Backend Foundation
SUPERSEDED / REMOVE

Python + FastAPI + Pydantic
KEEP CURRENT DIRECTION

modular monolith first
KEEP CURRENT DIRECTION

pytest / testability / config / error+logging baseline
KEEP FOR FUTURE BACKEND

Storage provider abstraction
KEEP

SQLAlchemy / Alembic
DEFER / CONDITIONAL ON ACCEPTED PHYSICAL MODEL

PostgreSQL local bootstrap / relational migrations
DEFER / PHYSICAL-DEPENDENT

concrete versioned API routes / DTOs
DEFER TO GOVERNED API CONTRACT

Auth runtime / workflow / outbox / provider adapters
DEFER TO APPLICABLE ACCEPTED RUNTIME/SECURITY/INTEGRATION CONTRACTS

old Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation slice
SUPERSEDED AS CANONICAL BACKEND/DOMAIN CONTRACT

Phase-4 UI must not dictate backend schema
KEEP

API/persistence layers != Domain Model
KEEP / HARDEN
```

Older product docs remain useful product evidence/requirements input where applicable, but they do not override accepted Domain/Logical/current architecture truth.

#### Approved Phase 3 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
d2f190de06bf0e4e1e491c0c2dc601eb48668da9

CREATE
none

UPDATE
docs/workstreams/backend-foundation.md
docs/workstreams/pre-physical-coherence.md
docs/workstreams/README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

DELETE
none
```

Phase 3 content HEAD before this closure marker:

`50731dbee3d2cc661972700ef0bce521b67098c6`

The five preceding content commits modify one approved path each. This handoff update is the sixth approved physical path and serves as the Phase 3 closure marker.

#### Phase 3 result

`docs/workstreams/backend-foundation.md` is now a **current deferred future handoff**, not a stale executable plan.

It establishes the future prerequisite chain:

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

It explicitly does **not** authorize creating `feature/backend-foundation` now.

Valid future bootstrap requirements were retained without preselecting Physical/runtime mechanisms. The old Domain-v0-inside-backend and fixed product-label slice instructions were removed from current execution authority.

Phase 3 remote scope/readback QA activates this `QA PASS` state when the exact PRE-SCOPE→closure delta contains only the six approved modified paths, `main` remains unchanged, and the current payloads read back coherently.

## Current exact task — Phase 4 read-only baseline inventory

Next work is **read-only**. Do not write yet.

Phase 4 must determine the exact contents and ownership of one current **Pre-Physical Architecture Baseline** bridge source.

Inventory at minimum:

- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- current ADR statuses;
- complete accepted Domain Atlas sources/continuations needed for current semantics;
- closed Whole Logical Model, final decision/assumption register continuation and remote closure;
- this workstream's open Phase 5–10 obligations;
- the cleaned deferred `backend-foundation.md` as a downstream consumer, not an authority over the baseline.

Classify candidate baseline statements as:

```text
DECIDED / CURRENT
SEMANTICALLY PROHIBITED
MANDATORY DOWNSTREAM HARDENING
OPEN / REQUIREMENT NEEDED
OPEN / BENCHMARK NEEDED
RUNTIME / TECHNICAL — NOT DOMAIN
PHYSICAL — NOT YET AUTHORIZED
EVIDENCE / NOT CURRENT SPEC
DUPLICATE / DO NOT COPY
DECISION REQUIRED
```

The Phase 4 bridge should make it possible to answer, from one current source plus linked authorities:

```text
what is already decided?
what is prohibited?
what is still open?
which WL-H01..WL-H12 constraints must downstream work preserve?
which concepts are runtime/backend rather than Domain owners?
which choices require requirements first?
which choices require Physical/runtime benchmark evidence?
what remains explicitly unauthorized?
```

Only after the read-only inventory may a **separate exact Phase 4 write gate** be presented.

## Remaining roadmap

### Phase 4 — current Pre-Physical Architecture Baseline — NEXT

Create one current bridge source stating decided/open/prohibited architecture, `WL-H01..WL-H12`, runtime-vs-Domain boundaries and future benchmark obligations.

### Phase 5 — requirements that can constrain Physical design

Define requirements, not implementation, for:

1. AuthN/AuthZ;
2. security/privacy/retention/recovery;
3. transaction/consistency/outbox/side effects;
4. non-functional/multi-device/recovery envelope.

AuthN/AuthZ minimum boundary:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

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

Compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

No winner is preselected.

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
- historical branch cleanup/deletion;
- direct modification of `main`.

## Exact continuation

```text
PHASE 3
QA PASS

NEXT
PHASE 4 — READ-ONLY CURRENT PRE-PHYSICAL ARCHITECTURE BASELINE INVENTORY

NO PHASE 4 WRITES YET
```
