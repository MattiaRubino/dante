# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 6 QA PASS; coordinated Phase 7–9 read-only tranche next**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Phase 2 PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`
- Phase 2 content HEAD before closure markers: `dfc1f4e124f362d342c336485e166c8ac57afba4`
- Phase 3 PRE-SCOPE: `d2f190de06bf0e4e1e491c0c2dc601eb48668da9`
- Phase 3 content HEAD before closure marker: `50731dbee3d2cc661972700ef0bce521b67098c6`
- Phase 4 PRE-SCOPE: `46b963394e29179fadf20cb3b11c35dbf3b6edc2`
- Phase 4 content HEAD before closure markers: `d67cd83f462611b2cc6d341937432e705f7a8682`
- Phase 5 PRE-SCOPE: `e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`
- Phase 5 content HEAD before global closure markers: `c29cfe4bde47d5df4f46507a5f1717acd1903112`
- Phase 5 propagation HEAD before handoff marker: `26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`
- Phase 6 PRE-SCOPE: `40728080ae7a69703d40d14dd256a556516ccc58`
- Phase 6 content HEAD before global closure markers: `67d6a0d63ecaf39379912606dcf5113550718594`
- Phase 6 propagation HEAD before this handoff marker: `5f9c2285f0de4a0f7c497ad36c12fae9b7548f1f`
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
Phase 5 QA PASS
Phase 6 QA PASS
Coordinated Phase 7–9 READ-ONLY TRANCHE NEXT

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
9. read `docs/architecture/pre-physical-architecture-baseline.md`, `docs/architecture/requirements/README.md`, all four Phase 5 requirement packages, `docs/architecture/ai-context-runtime-boundaries.md`, `docs/architecture/integration-hub-boundaries.md`, `docs/architecture/README.md` and linked current model/architecture sources;
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

A physical split does not create separate logical authority. `*-part-N` continuation chains must be read as one complete logical document.

For size/tool-limit splitting specifically:

```text
ONE COMPLETE LOGICAL PAYLOAD
→ LOSSLESS PHYSICAL PARTITION
→ ONE COMPLETE LOGICAL PAYLOAD
```

A size/tool-limit split is **not** summarization, condensation, omission, paraphrase-as-compression or a hidden semantic cleanup. If content needs semantic/current-truth revision, that is a separate content operation. Chronological/evidence continuation is distinct and may append genuine later evidence after the previous payload.

## Current architecture navigation

Current sources:

- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/requirements/README.md` + all four linked Phase 5 requirement packages;
- `docs/architecture/ai-context-runtime-boundaries.md`;
- `docs/architecture/integration-hub-boundaries.md`;
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

Phase 5 requirement packages and Phase 6 boundary contracts add current downstream requirements without replacing these hardenings.

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

The future Backend Foundation handoff is current but deferred. It consumes Domain + Logical rather than recreating them, treats SQLAlchemy/Alembic as Physical-dependent candidates, keeps PostgreSQL as benchmark posture rather than mandate, defers concrete API/Auth/workflow/provider mechanisms, removes the old fixed product-label slice as a canonical contract, and preserves valid future Python/FastAPI/Pydantic/modular-monolith/testing/provider-boundary requirements.

### Phase 4 — Current Pre-Physical Architecture Baseline — QA PASS

Phase 4 reconstructed current authority across complete split/continuation logical documents and established `docs/architecture/pre-physical-architecture-baseline.md` as the current bridge source.

Key rule:

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
```

Approved PRE-SCOPE:

`46b963394e29179fadf20cb3b11c35dbf3b6edc2`

Content HEAD:

`d67cd83f462611b2cc6d341937432e705f7a8682`

Remote Phase 4 path QA through the first closure marker:

```text
ahead_by       8
behind_by      0
total_commits  8
added           1
modified        7
deleted         0
unexpected      0
```

Domain and Logical semantics were not changed. No Physical/runtime implementation decision was introduced.

## Operational anomaly — accidental branch ref

During Phase 4 execution an incorrect tool invocation created an unrelated temporary branch ref:

```text
__no-op__
→ 46b963394e29179fadf20cb3b11c35dbf3b6edc2
```

It does **not** alter `chore/pre-physical-coherence`, `main` or project content. The available connector exposes no branch/ref deletion action, so this ref remains repository-hygiene cleanup for later. Do not use it as a work branch or source of truth.

### Phase 5 — requirements that can constrain Physical design — QA PASS

Phase 5 audited current Product/Domain/Logical/architecture requirements without reopening Domain/Logical semantics and established four distinct requirement owners:

```text
AuthN / AuthZ
Security / Privacy / Retention / Security-aware Recovery
Consistency / Side Effects
Non-functional / Multi-device / Operational Recovery
```

Classification discipline:

```text
MUST / MUST NOT = accepted requirement
OPEN PARAMETER / OPEN DECISION = later required value/policy
DEFERRED MECHANISM = intentionally later implementation choice
```

No numeric RPO/RTO/SLA/latency/scale/offline-duration targets, Auth mechanism, security mechanism, workflow mechanism or Physical persistence were invented/selected.

Approved Phase 5 PRE-SCOPE:

`e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f`

Phase 5 content HEAD:

`c29cfe4bde47d5df4f46507a5f1717acd1903112`

Remote content QA:

```text
ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

Propagation HEAD before handoff marker:

`26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`

Remote compare at propagation point:

```text
ahead_by       14
behind_by       0
total_commits   14
added            5
modified         9
deleted          0
unexpected       0
```

The Phase 5 package also hardened the split rule:

```text
SIZE / TOOL-LIMIT SPLIT
= lossless physical partition of one complete logical payload
!= summary / condensation / omission / hidden semantic cleanup
```

### Phase 6 — AI/context/runtime/integration boundaries — QA PASS

#### Read-only inventory result

Phase 6 consumed closed Domain/Logical semantics, the current architecture baseline, all Phase 5 requirements, ADR-005 and product/evidence boundaries.

No new Domain owner is required. Runtime `Agent`, `Memory`, `Context`, `Tool`, `Workflow`, `Automation`, provider object/task and protocol concepts remain technical/product/runtime unless a separately accepted semantic role applies.

The current AI/runtime context categories are:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The current Integration Hub modes are:

```text
canonical import
synchronized/mirrored provider state
live federated read
retrieval/index projection
action/tool integration
```

#### Approved Phase 6 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
40728080ae7a69703d40d14dd256a556516ccc58

CREATE
docs/architecture/ai-context-runtime-boundaries.md
docs/architecture/integration-hub-boundaries.md

UPDATE
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/decisions/ADR-005-ai-gateway.md
docs/workstreams/backend-foundation.md
docs/workstreams/pre-physical-coherence.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

DELETE
none
```

#### Phase 6 content result

Content HEAD before global closure markers:

`67d6a0d63ecaf39379912606dcf5113550718594`

Remote content QA:

```text
ahead_by        8
behind_by       0
total_commits    8
added             2
modified          6
deleted           0
unexpected        0
```

Exact content paths:

```text
ADDED
docs/architecture/ai-context-runtime-boundaries.md
docs/architecture/integration-hub-boundaries.md

MODIFIED
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/decisions/ADR-005-ai-gateway.md
docs/workstreams/backend-foundation.md
```

#### Phase 6 accepted AI/context/runtime contract

Current contract requires:

- purpose-/disclosure-/provenance-/freshness-aware Context Builder;
- no unrestricted full-history/database AI context by default;
- no generic second canonical `AI memory` truth store;
- AI result classification before durable consequence;
- `AI Proposal != Decision != Authority != effective state`;
- configurable autonomy based on consequence/governance/policy rather than universal confirmation;
- `runtime Agent / Principal != Domain Actor automatically`;
- tool invocation / protocol action != authorization / canonical governed operation;
- external/retrieved content cannot self-authorize actions;
- delayed effects preserve Phase 5 target/governance revalidation;
- provider/model fallback cannot silently widen privacy/provider eligibility;
- model/runtime failures do not fabricate canonical semantic negatives.

No AI provider/model, agent framework, memory store, MCP/A2A implementation, workflow engine or tool schema was selected.

#### Phase 6 accepted Integration Hub contract

Each material integration flow identifies one or a bounded composition of:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Current invariants include:

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef by identity
provider state != canonical LifeOS state
provider/tool operation string != canonical governed effect
```

Canonical import requires explicit mapping/validation/acceptance. Sync/mirror preserves provider apply state separately from canonical state. Live reads retain source/freshness/unknown state. Retrieval/index projections remain derived and deletion-aware. Action/tool effects preserve governance, expected state, idempotency, ambiguous-outcome and reconciliation truth. Callback/webhook/polling delivery is adapter state, not arrival-order canonical truth.

MCP/A2A/future protocols remain adapters, not ontology or LifeOS governance.

No provider adapter, provider SDK, sync engine, queue/workflow engine or protocol implementation was selected.

#### Phase 6 propagation result before this handoff marker

Propagation HEAD:

`5f9c2285f0de4a0f7c497ad36c12fae9b7548f1f`

At this point all gated paths except this workstream save-game itself have been written. Final Phase 6 compare must therefore cover the full 13-path gate after this marker.

#### Phase 6 non-reopen / non-authorization result

```text
DOMAIN REOPEN REQUIRED             0
LOGICAL REOPEN REQUIRED            0
NEW DOMAIN OWNER REQUIRED          0
PHYSICAL MODEL SELECTED            0
AI PROVIDER/MODEL SELECTED         0
AGENT FRAMEWORK SELECTED           0
MCP/A2A SELECTED                   0
WORKFLOW ENGINE SELECTED           0
PROVIDER ADAPTER IMPLEMENTED       0
BACKEND IMPLEMENTATION STARTED     0
```

## Current exact task — coordinated Phase 7–9 read-only tranche

The next architecture work may be handled as one coordinated outer tranche to reduce repeated navigation/status churn, but **must preserve three ordered internal acceptance checkpoints**:

```text
PHASE 7
Durable workflow / async benchmark
        ↓
PHASE 8
Governed API / command / effect contract
        ↓
PHASE 9
Search / observability / calendar / solver pressure
```

### Outer-tranche rule

The tranche may share:

- one broad read-only inventory;
- common source reconstruction;
- one later exact outer write gate where path ownership can be proven in advance;
- consolidated final propagation to global status/navigation.

But it must **not** collapse the internal dependencies:

1. Phase 7 gets its own benchmark evidence/verdict before Phase 8 may rely on it;
2. Phase 8 consumes Phase 7 results and gets its own contract QA/verdict before Phase 9 may rely on it;
3. Phase 9 consumes the accepted Phase 8 governed-effect/disclosure boundary;
4. a HOLD/failure in one internal checkpoint stops dependent work rather than being hidden by the outer tranche;
5. no Physical technology is selected by Phases 7–9.

### Internal Phase 7 — durable workflow / async benchmark

Read-only first. Compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

Pressure includes provider retry/sync, human approval, long AI work, reconciliation, cancellation/timeouts, partial/ambiguous external effect, duplicate/replay, delayed governance/target change, crash/restart and recovery.

### Internal Phase 8 — governed API / command / effect contract

Consumes accepted Phase 7 findings. Define the consequential-operation contract before concrete routes/DTOs.

At minimum preserve:

```text
Principal/security context
actual Actor / represented party
semantic target/facet
operation/effect family
material/expected state
input/context/purpose
governance basis
autonomy/confirmation requirement
idempotency/correlation
delayed execution semantics
result/conflict/partial/reconciliation/provenance semantics
```

```text
HTTP route / UI button / tool string / AuthZ action string
!= canonical Governed Operation
```

### Internal Phase 9 — search / observability / calendar / solver pressure

Consumes the accepted Phase 8 effect/disclosure boundary.

Inventory/pressure must cover:

- canonical state vs search/index/retrieval projection;
- `WL-H12` search/ranking/explanation inference leakage;
- privacy-safe observability and effect correlation;
- calendar interoperability semantics as pressure, not ontology;
- recurrence/timezone/DST/history behavior;
- deterministic solver/service vs AI boundary;
- truthful feasible/infeasible/uncertain/at-risk/conflicting/partial outcomes;
- specialized infrastructure only on demonstrated benefit.

No Phase 7–9 write is authorized until the coordinated read-only inventory produces a fresh exact gate.

## Remaining roadmap after Phase 7–9

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

Use destructive LifeOS scenarios including Phase 5/6 pressure: consequential concurrency, multi-owner mutation, selective disclosure, provider divergence, redaction/history, DST recurrence, stale derived state, AuthZ provenance, search inference leakage, AI proposal→approval→effect, revoked governance during execution, long-running crash/restart, restore after deletion/redaction, multi-device/offline divergence, ambiguous external-effect replay and schema evolution.

Resolve or scenario-model Phase 5 open parameters where their values materially affect candidate ranking.

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
- AI provider/model/agent implementation;
- MCP/A2A adoption/implementation;
- provider adapters;
- durable workflow engine implementation;
- frontend/prototype changes inside this workstream;
- direct modification of `main`.

## Exact continuation

```text
PHASE 6
QA PASS

CURRENT REQUIREMENTS
docs/architecture/requirements/README.md
+ four linked packages

CURRENT PHASE 6 BOUNDARIES
docs/architecture/ai-context-runtime-boundaries.md
docs/architecture/integration-hub-boundaries.md

NEXT
COORDINATED PHASE 7–9 READ-ONLY ARCHITECTURE TRANCHE

INTERNAL ORDER
7 → 8 → 9

NO PHASE 7–9 WRITES YET
```
