# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 5 QA PASS; Phase 6 read-only boundaries next**
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
- Phase 5 propagation HEAD before this handoff marker: `26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`
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
Phase 6 READ-ONLY BOUNDARY INVENTORY NEXT

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
9. read `docs/architecture/pre-physical-architecture-baseline.md`, `docs/architecture/requirements/README.md`, all four Phase 5 requirement packages, `docs/architecture/README.md` and linked current model/architecture sources;
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

Phase 5 adds current downstream requirement contracts without replacing these hardenings.

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

`docs/architecture/pre-physical-architecture-baseline.md` is the current bridge source for:

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

`docs/architecture/README.md` exposes the bridge as current architecture navigation.

`docs/workstreams/backend-foundation.md` names the baseline as mandatory downstream reading while remaining **NOT STARTED / DEFERRED**.

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

The eight unique changed paths were exactly the approved gate. `main` remained unchanged.

## Operational anomaly — accidental branch ref

During Phase 4 execution an incorrect tool invocation created an unrelated temporary branch ref:

```text
__no-op__
→ 46b963394e29179fadf20cb3b11c35dbf3b6edc2
```

It does **not** alter `chore/pre-physical-coherence`, `main`, the Phase 4/5 file deltas or any project content. The currently available GitHub connector exposes branch create/update but no `delete_ref`, so this ref could not be removed in-session. It should be deleted as repository hygiene when a branch-delete mechanism is available (for example `git push origin --delete __no-op__`). Do not use it as a work branch or source of truth.

### Phase 5 — requirements that can constrain Physical design — QA PASS

#### Read-only inventory result

Phase 5 audited current Product/Domain/Logical/architecture requirements without reopening Domain/Logical semantics.

The inventory converged on four distinct requirement owners:

```text
AuthN / AuthZ
Security / Privacy / Retention / Security-aware Recovery
Consistency / Side Effects
Non-functional / Multi-device / Operational Recovery
```

Required classification discipline:

```text
MUST / MUST NOT
= accepted requirement

OPEN PARAMETER / OPEN DECISION
= required later value/policy not responsibly fixed yet

DEFERRED MECHANISM
= implementation choice intentionally left to later work
```

No numeric RPO/RTO/SLA/latency/scale/offline-duration targets were invented. No Auth provider/policy engine/token/session mechanism, security/KMS mechanism, transaction/outbox/workflow/CRDT mechanism or Physical persistence was selected.

#### Approved Phase 5 write gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f

CREATE
docs/architecture/requirements/README.md
docs/architecture/requirements/authn-authz.md
docs/architecture/requirements/security-privacy-retention-recovery.md
docs/architecture/requirements/consistency-side-effects.md
docs/architecture/requirements/nonfunctional-multidevice-recovery.md

UPDATE
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md
docs/workstreams/backend-foundation.md
docs/development/agent-operating-manual.md
docs/development/documentation-and-handoff.md

DELETE
none
```

#### Phase 5 content result

Phase 5 content HEAD before global closure markers:

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

Exact content paths:

```text
ADDED
5 / 5 requirement-package paths

MODIFIED
architecture/README.md
architecture/pre-physical-architecture-baseline.md
workstreams/backend-foundation.md
development/agent-operating-manual.md
development/documentation-and-handoff.md
```

#### Phase 5 propagation result before handoff marker

Propagation HEAD:

`26882e376f1a6ad826d5aabfb4364f2a2ba30dd5`

Remote compare from Phase 5 PRE-SCOPE:

```text
ahead_by       14
behind_by       0
total_commits   14
added            5
modified         9
deleted          0
unexpected       0
```

The only gated UPDATE not yet included in that 14-path compare is this workstream save-game itself, intentionally written as the final closure marker.

#### Phase 5 accepted requirement contracts

##### AuthN/AuthZ

Current requirements preserve at minimum:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
actual Actor != represented party automatically
technical allow/deny != canonical governance truth
```

Consequential authorization/effect provenance, non-human Principal governance, delayed-effect governance revalidation and inference/non-interference disclosure are mandatory downstream.

##### Security/privacy/retention/security-aware recovery

Current requirements include purpose-aware minimization, sensitive-data handling, secret/credential isolation, privacy-minimized observability, category/purpose-sensitive retention, truthful deletion/redaction/anonymization, non-reused native identity, propagation to derived/external state, privileged/audited backup/restore and prevention of forbidden-data resurrection.

Exact legal basis, retention schedules, final classification/residency/processor obligations and concrete security mechanisms remain later explicit decisions.

##### Consistency/side effects

Current requirements include expected-state semantics, idempotency != identity, no silent material last-write-wins, unresolved conflict, semantic multi-owner atomicity where required, truthful staged/partial state, canonical/provider-effect separation, ambiguous-failure retry safety, derived-state freshness, delayed target/governance revalidation, publication/replay integrity and explicit reconciliation/compensation truth.

Transaction isolation, locks, outbox/inbox, queues, workflow/saga and CRDT/OT remain mechanism decisions.

##### Non-functional/multi-device/operational recovery

Current requirements include multi-device divergence, operation-specific offline behavior, consequence-specific consistency/availability classes, truthful provider/degraded state, efficient current-state access alongside long history, timezone/DST semantic preservation, privacy-safe observability, capacity/backpressure, destructive recovery testing and explicit later RPO/RTO/latency/availability/scale inputs.

Open parameters are mandatory later inputs, not silent implementation defaults.

#### Split-rule hardening

The operating manual and handoff protocol now explicitly distinguish:

```text
SIZE / TOOL-LIMIT SPLIT
= lossless physical partition of one complete logical payload
!= summary
!= condensation
!= paraphrase-as-compression
!= omission
!= hidden semantic cleanup
```

from:

```text
CHRONOLOGICAL / EVIDENCE CONTINUATION
= may append genuine later evidence after the previous payload
```

This hardening does not rewrite old Domain/Logical split evidence; it governs future handling and any separately gated future split repair.

#### Phase 5 non-reopen / non-authorization result

```text
DOMAIN REOPEN REQUIRED             0
LOGICAL REOPEN REQUIRED            0
PHYSICAL MODEL SELECTED            0
AUTH/RUNTIME MECHANISM SELECTED    0
BACKEND IMPLEMENTATION STARTED     0
ADR CHANGED                        0
```

Phase 5 requirements constrain later work; they do not authorize it.

## Current exact task — Phase 6 read-only boundary inventory

Next work is **read-only**. Do not write Phase 6 yet.

Phase 6 must define current AI/context/runtime/integration boundaries while consuming the closed Domain/Logical model, current architecture baseline and all Phase 5 requirements.

At minimum keep distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate/unresolved state
transient LLM working context
```

The Phase 6 read-only pass must inventory and classify at least:

1. Context Builder inputs/outputs, minimization, provenance and freshness;
2. AI-generated proposals/candidates versus governed canonical effects;
3. deterministic service/solver boundary versus AI reasoning;
4. Agent/tool/automation runtime identity and Principal/Actor/Authority handling;
5. durable vs transient AI memory/context boundaries;
6. provider-neutral AI gateway responsibilities and model/provider isolation;
7. Integration Hub mode-specific contracts for:
   - canonical import;
   - synchronized/mirrored provider state;
   - live federated read;
   - retrieval/index projection;
   - action/tool integration;
8. ExternalRef/provider revision/provenance/reconciliation behavior;
9. security/privacy/retention/deletion behavior across AI and provider copies;
10. delayed/queued tool effects under Phase 5 AuthZ/consistency requirements;
11. protocol adapter boundary: MCP/A2A/future equivalents are adapters, not ontology;
12. unresolved decisions versus implementation-deferred mechanisms.

No Phase 6 write is authorized until a fresh exact gate is presented and approved.

## Remaining roadmap

### Phase 5 — requirements that can constrain Physical design — QA PASS

Current source: `docs/architecture/requirements/README.md` + all four linked packages.

### Phase 6 — AI/context/runtime/integration boundaries — NEXT

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

Use destructive LifeOS scenarios including Phase 5 pressure: consequential concurrency, multi-owner mutation, selective disclosure, provider divergence, redaction/history, DST recurrence, stale derived state, AuthZ provenance, search inference leakage, AI proposal→approval→effect, revoked governance during execution, crash/restart, restore after deletion/redaction, multi-device/offline divergence, ambiguous external-effect replay and schema evolution.

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
- provider adapters;
- frontend/prototype changes inside this workstream;
- direct modification of `main`.

## Exact continuation

```text
PHASE 5
QA PASS

CURRENT REQUIREMENTS
docs/architecture/requirements/README.md
+ four linked packages

NEXT
PHASE 6 — READ-ONLY AI / CONTEXT / RUNTIME / INTEGRATION BOUNDARY INVENTORY

NO PHASE 6 WRITES YET
```
