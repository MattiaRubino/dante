# Pre-Physical Architecture Baseline

- Status: **CURRENT — Phase 6 boundaries incorporated**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Backend: **NOT STARTED / DEFERRED**

## Purpose

Current bridge between the closed Domain + Logical Models and later requirements, benchmark, Physical and backend work. It does not replace Domain, Logical, ADRs, `system-overview.md`, `technical-decisions.md`, the detailed Phase 5 requirement packages or the detailed Phase 6 boundary contracts; it states the downstream assumptions, prohibitions, mandatory hardenings, current requirement/boundary inputs, open owners and authorization boundary.

## Authority

Read current truth through Product/North Star, the complete Domain Atlas + Language Map logical documents, the closed Whole Logical Model + full decision/register chain + remote closure, current ADR status, current architecture specs, the complete Phase 5 requirement package set, the Phase 6 AI/context/runtime and Integration Hub contracts, this baseline, then the active workstream for open obligations.

A physical `*-part-N` chain is one logical document. Never infer current state from only the first or last physical part. A tool/size split preserves the complete logical payload losslessly and is not a summary/condensation operation.

## Decided != authorized

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
ACCEPTED REQUIREMENT != IMPLEMENTATION MECHANISM SELECTION
ACCEPTED BOUNDARY CONTRACT != PROVIDER / RUNTIME / PROTOCOL SELECTION
```

Current stage:

```text
Product/North Star        CURRENT
Domain Atlas              CLOSED
Logical Model             CLOSED
Pre-Physical Coherence    IN PROGRESS
Physical Model            NOT STARTED / NOT AUTHORIZED
Backend Foundation        NOT STARTED / DEFERRED
```

## Current direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Modular monolith first.
- Domain/application logic stays independent from HTTP/framework handling.
- Clients use governed backend contracts, not direct canonical persistence.
- Object/file storage stays behind a provider abstraction.
- AI stays behind replaceable/provider-neutral boundaries and a bounded Context Builder.
- Provider state remains distinct from canonical LifeOS state.
- Specialized infrastructure requires demonstrated measured or structural benefit.
- SQLAlchemy/Alembic remain conditional on accepted Physical design.

## Semantic guardrails

Do not manufacture universal owners or collapse accepted distinctions for implementation convenience.

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Actor / Subject / Resource = contextual roles/capabilities, not universal native owners
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Responsibility != Participation != Coordination Stewardship
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical state
derived projection != canonical truth
AI/solver inference != accepted canonical effect
```

Product/runtime labels such as Project, Program, Workspace, Task, Reminder, Agent, Workflow or Notification do not create new universal Domain roots by naming alone.

Hard rejects for the canonical kernel include universal Entity/Thing, universal generic Relationship/edge, generic EAV/property-bag ontology, generic unresolved-AI relation/property fallback, provider schema/IDs as ontology/identity, and product/UI vocabulary as ontology authority.

Storage coincidence != semantic equivalence. Addressability != Domain identity.

## Representation and state separation

The Logical Model keeps `LR-01..LR-13` distinct and uses discriminated `NativeRef`, `ScopedRecordRef`, `MaterialStateRef`, `ExternalRef`; do not collapse them into one identifier model.

Preserve separation among:

```text
canonical state
material history / lineage / correction
derived or effective projection
provider / external state
unresolved / candidate interpretation
security / AuthZ runtime state
```

Phase 6 additionally fixes the runtime context distinction:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The detailed contract lives in [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md).

## Mandatory WL-H01..WL-H12

- **H01** Agreement terms bind justified material owner/facet/state; no universal Terms root.
- **H02** consequential operations use a governed operation/effect contract; route/UI/AuthZ strings are not the canonical effect.
- **H03** projection/disclosure surfaces are bounded by source, derivation/version, purpose and exposure/disclosure boundaries.
- **H04** absence/unknown != false.
- **H05** consequential writes require expected-state semantics.
- **H06** idempotency != semantic identity; conflicting reuse rejects.
- **H07** multi-owner mutation is atomic where required or explicitly staged/partial with reconciliation/compensation.
- **H08** canonical LifeOS state != provider sync state.
- **H09** consequential derived-state use requires freshness revalidation or bound material basis/snapshot.
- **H10** retention/redaction/tombstone handling preserves historical integrity; native identity is not reused.
- **H11** consequential AuthZ provenance reconstructs Actor, represented party, Principal/security context, Authority/Consent/Visibility basis, policy/model version and effect.
- **H12** non-interference/inference leakage includes existence, counts, ranking, errors, timing, free-busy, candidates, explanations and aggregates.

## Phase 5 current requirement package

The current detailed requirements live under [`requirements/README.md`](requirements/README.md) and its four packages.

### AuthN/AuthZ

Later implementation must preserve at least:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
actual Actor != represented party automatically
technical allow/deny != canonical governance truth
```

Consequential authorization/effect provenance must be reconstructible where required; non-human Principals do not bypass governance; delayed effects must not rely indefinitely on stale governance state; disclosure enforcement includes inference/non-interference surfaces.

Provider/protocol/session/policy-engine and enforcement mechanism selection remains deferred.

### Security / privacy / retention / security-aware recovery

Later design must support purpose-aware minimization, sensitive-data handling, secure secret/credential isolation, privacy-minimized observability, category/purpose-sensitive retention, truthful deletion/redaction/anonymization, non-reused native identity, propagation to derived/external state, security-governed backup/restore and prevention of unauthorized resurrection after restore.

Exact legal basis, retention durations, final classification catalogue, residency/processor obligations and concrete security mechanisms remain explicit open decisions.

### Consistency / side effects

Later design must preserve expected-state semantics, idempotency distinct from identity, no silent material last-write-wins, unresolved conflict, semantic multi-owner atomicity where required, truthful staged/partial state where distributed atomicity is impossible, canonical/provider-effect separation, ambiguous-failure retry safety, derived-state freshness, delayed target/governance revalidation, publication/replay integrity and reconstructible consequential effect history.

Transaction/outbox/inbox/queue/workflow/CRDT/locking/isolation mechanisms remain deferred.

### Non-functional / multi-device / operational recovery

Later design must prevent silent multi-device consequential overwrite, preserve divergent states for reconciliation, define offline capability per operation rather than globally, classify consistency/availability by consequence, maintain truthful provider/degraded state, support efficient current-state access alongside long history, explicitly set RPO/RTO/latency/availability/scale inputs before dependent Physical scoring, preserve temporal/DST semantics, protect privacy in observability and prove recovery through destructive tests.

Numeric RPO/RTO/SLA/latency/scale/offline-duration targets remain explicit open parameters; they must be resolved or benchmarked as scenarios before final Physical acceptance, not guessed during Phase 5.

## Runtime/technical != Domain

Account, Principal, Credential, AuthZ decision, Agent, Tool, Workflow, Automation runtime, Notification delivery, Job, queue/outbox, cache/index, API DTO/route and protocol adapter are technical/product concepts unless separately revalidated. Authentication/security session concepts must not be conflated with Domain `Session`.

## Phase 6 AI/context/runtime boundary

Current detailed contract: [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md).

Accepted boundary:

```text
AI/context/runtime representation != canonical LifeOS truth by default
model output != accepted canonical effect
tool invocation != governed operation
runtime Agent / Principal != Domain Actor automatically
```

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware and does not default to unrestricted user-history/database exposure.

LifeOS does not create a second generic `AI memory` truth store. Durable information must receive an accepted canonical/history/candidate/derived/source/provider disposition.

AI output is classified as answer/explanation, candidate/unresolved interpretation, structured extraction, Proposal/proposal-like candidate, scenario/recommendation or governed-effect request as applicable. None becomes effective solely because a model produced it.

Configurable autonomy remains consequence/governance/policy based; Phase 6 does not impose universal human confirmation.

AI provider/model selection, agent framework, tool registration format, conversation retention and concrete runtime mechanisms remain open/deferred.

## Phase 6 Integration Hub boundary

Current detailed contract: [`integration-hub-boundaries.md`](integration-hub-boundaries.md).

Five modes remain distinct:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider success/failure does not automatically determine canonical LifeOS effect truth.

Sync/mirror requires explicit direction/conflict semantics; live reads retain source/freshness/unknown state; retrieval/index projections remain derived/deletion-aware; action/tool effects preserve governance, idempotency, partial-state and reconciliation truth.

MCP/A2A/future protocols are adapters, not ontology or LifeOS governance.

Provider/adapter/protocol selection remains deferred.

## Benchmark posture

No Physical technology is selected:

```text
PostgreSQL hybrid         preferred baseline — not selected
TypeDB                     mandatory challenger
Neo4j/property graph       serious secondary/read-projection candidate
event/document mechanisms bounded candidates
pgvector                   bounded semantic-retrieval candidate
generic EAV/generic edge/universal meta-model HARD REJECT
```

No durable-workflow winner is selected. Phase 7 compares at least PostgreSQL+worker+transactional outbox, Temporal, Restate and DBOS.

## Open owners before Physical authorization

- **Phase 7:** durable workflow/async benchmark.
- **Phase 8:** governed API/command/effect contract before concrete routes/DTOs.
- **Phase 9:** search/observability/calendar/solver pressure.
- **Phase 10:** Physical benchmark specification/register, including resolution/scenario treatment of Phase 5 open parameters whose values affect candidate scoring.
- **Phase 11:** repository engineering safety.
- **Phase 12:** clean-room coherence QA and closure.

Phase 5 requirements and Phase 6 boundary contracts are current downstream inputs; open parameters/decisions recorded inside them remain obligations, not permission to ignore the requirement/boundary family.

## Explicitly unauthorized now

No Physical schema/tables/keys/indexes/constraints, concrete PostgreSQL/TypeDB/Neo4j design, SQL/migrations, concrete API routes/DTOs, AuthN/AuthZ engine/provider implementation, workflow/automation/notification engine, provider adapters, AI provider/model/agent implementation, MCP/A2A adoption, production backend code or `feature/backend-foundation`. Domain/Logical changes require a separate explicit reopen gate.

## Backend consumption contract

Backend Foundation must consume this baseline plus the complete Phase 5 requirement packages, both Phase 6 boundary contracts, complete current Domain/Logical authorities and later accepted Physical/runtime/API contracts. Implementation convenience, product labels and stale evidence cannot redefine semantics.

## Documentation/evidence rule

Current specs = current truth. ADRs = rationale + explicit supersession/qualification. Historical checkpoints = truthful chronology. Git = recoverable history.

This baseline does not close Pre-Physical Coherence or authorize Physical work. After Phase 6 remote QA, the next current work is the coordinated Phase 7–9 architecture tranche, beginning with read-only inventory/benchmark preparation and preserving the dependency order among durable execution, governed effects and search/observability/calendar/solver pressure.