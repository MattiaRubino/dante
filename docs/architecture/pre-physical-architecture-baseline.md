# Pre-Physical Architecture Baseline

- Status: **CURRENT — Phase 12 closed; independent total-audit repairs incorporated**
- Pre-Physical Coherence: **FINAL CLOSURE CANDIDATE — definitive closure activates only after exact remote QA of the final audit gate**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Backend production implementation: **NOT STARTED / DEFERRED**

## Purpose

This is the current bridge from the accepted Product/North Star, CLOSED Domain Atlas and CLOSED Logical Model into later Physical/runtime/API/backend work.

It consolidates the downstream constraints that later engineering must preserve. It does not replace the detailed Domain/Logical sources, ADRs, Phase 5 requirement packages, Phase 6 boundary contracts, Phase 7–9 architecture contracts, Phase 10 benchmark package, Phase 11 repository-safety contract, Phase 12 clean-room evidence or the final independent audit evidence.

## Authority

Read current truth through:

1. Product / North Star;
2. complete Domain Atlas + Language Map cumulative authority, including final closure/status continuations;
3. CLOSED Whole Logical Model + complete decision/assumption-register chain + remote closure evidence;
4. current ADR statuses;
5. all four Phase 5 requirement packages;
6. Phase 6 AI/context/runtime and Integration Hub contracts;
7. Phase 7 durable-execution benchmark;
8. Phase 8 governed-operation/effect contract;
9. Phase 9 search/observability/calendar/solver contract;
10. Phase 10 Physical benchmark specification + scenario corpus + register;
11. Phase 11 repository-engineering-safety contract + verified effective main rules;
12. Phase 12 clean-room evidence;
13. this baseline;
14. final independent audit evidence and active workstream handoff for exact closure state.

A physical split/cumulative continuation is one logical document. Never infer current state from only an early part or an isolated continuation. Size/tool-limit splitting is lossless physical partitioning, not summarization or semantic cleanup.

## Decided != authorized

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
PREFERRED BENCHMARK CANDIDATE != TECHNOLOGY SELECTION
REGISTERED BENCHMARK CANDIDATE != TECHNOLOGY SELECTION
ACCEPTED REQUIREMENT != IMPLEMENTATION MECHANISM SELECTION
ACCEPTED BOUNDARY CONTRACT != PROVIDER / RUNTIME / PROTOCOL SELECTION
BENCHMARK METHOD ACCEPTED != PHYSICAL MODEL STARTED
REPOSITORY SAFETY VERIFIED != BACKEND STARTED
PHASE 12 CLOSED != WHOLE PRE-PHYSICAL DEFINITIVELY CLOSED UNTIL FINAL TOTAL-AUDIT GATE PASSES
```

## Current stage

```text
Product / North Star        CURRENT
Domain Atlas                CLOSED
Logical Model               CLOSED
Phase 5 requirements        CURRENT
Phase 6 boundaries          CURRENT
Phase 7 benchmark           CURRENT
Phase 8 effect contract     CURRENT
Phase 9 pressure contract   CURRENT
Phase 10 benchmark method   CURRENT / QA PASS
Phase 11 repository safety  QA PASS
Phase 12 clean-room QA      QA PASS / CLOSED

Independent total audit
CORE PASS
bounded final repairs incorporated
exact final remote gate QA still required

Pre-Physical Coherence
FINAL CLOSURE CANDIDATE

Physical Model              NOT STARTED / NOT AUTHORIZED
Backend Foundation          NOT STARTED / DEFERRED
Main integration            NOT PERFORMED
```

## Current technical direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Modular monolith first.
- Domain/application logic remains independent from HTTP/framework handling.
- Clients use governed backend contracts, not direct canonical persistence.
- Object/file storage remains behind a provider abstraction.
- AI remains behind replaceable/provider-neutral boundaries and a bounded Context Builder.
- Material consequential AI changes are promotion-gated by versioned/reproducible evaluation; evaluation evidence is not canonical truth or authorization.
- Provider state remains distinct from canonical LifeOS state.
- Consequential operations use an engine-/transport-neutral governed operation/effect contract.
- Bounded async work and material long-running durable execution are distinct runtime classes.
- Restate remains preferred dedicated durable candidate; Temporal remains the strongest mandatory challenger; DBOS remains conditional, with deployment-dependent PostgreSQL coupling rather than universal PostgreSQL requirement in Python.
- Structured + lexical/full-text search is the baseline; semantic/vector retrieval is bounded.
- OpenTelemetry-first or equivalent standards-based observability is the current direction, not a vendor selection.
- Calendar standards/providers are interoperability/adaptor pressure, not ontology authority.
- Deterministic rules/heuristics remain baseline for explicit constraints; OR-Tools CP-SAT is a preferred specialized solver benchmark candidate, not selected implementation.
- Physical candidate comparison is role-specific, not one universal leaderboard.
- Physical correctness hard gates precede performance/operability scoring.
- Unknown NFR/business-scale values remain explicit sensitivity/scenario inputs rather than invented forecasts.
- An unexecuted synthetic upper envelope cannot be reported as verified benchmark evidence.
- Specialized infrastructure requires demonstrated structural or measured benefit.
- SQLAlchemy/Alembic remain conditional on the accepted Physical design.

## Semantic guardrails

Later implementation must preserve accepted distinctions rather than manufacturing universal owners for storage convenience.

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

Product/runtime labels such as Project, Program, Workspace, Task, Reminder, Agent, Workflow or Notification do not create new Domain roots by naming alone.

Hard rejects for the canonical kernel include:

```text
universal Entity / Thing
universal generic Relationship / edge
generic EAV / property-bag ontology
generic unresolved-AI semantic fallback
provider schema / identifier as ontology or native identity
product/UI vocabulary as ontology authority
```

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
PRODUCT LABEL != ONTOLOGY ROOT
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
```

## Logical representation and state separation

The closed Logical Model preserves `LR-01..LR-13` representation families and discriminated reference families including:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Do not collapse them into a universal identifier model.

State categories remain distinct where applicable:

```text
canonical state
material history / lineage / correction
derived or effective projection
provider / external state
unresolved / candidate interpretation
security / AuthZ runtime state
```

Phase 6 context categories further distinguish:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

## Mandatory WL-H01..WL-H12

All later Physical/API/runtime/backend work must preserve:

1. **WL-H01** — Agreement terms bind a justified owner/facet/material state; no universal Terms root.
2. **WL-H02** — consequential work uses a governed operation/effect contract; route/UI/AuthZ strings are not canonical effects.
3. **WL-H03** — projection/disclosure surfaces remain bounded by source/facet/derivation/version/purpose/exposure/disclosure.
4. **WL-H04** — absence/unknown != false.
5. **WL-H05** — consequential writes preserve expected-state semantics.
6. **WL-H06** — idempotency != identity; conflicting key/equivalence reuse rejects.
7. **WL-H07** — multi-owner changes are atomic where required or explicitly staged/partial with reconciliation/compensation.
8. **WL-H08** — canonical LifeOS state != provider sync state.
9. **WL-H09** — consequential derived/live-state use revalidates freshness or binds material basis/snapshot.
10. **WL-H10** — retention/redaction/tombstone handling preserves integrity; native identity is not reused.
11. **WL-H11** — consequential authorization/effect provenance can reconstruct Actor, represented party, Principal/security context, Authority/Consent/Visibility basis, policy/model version and effect.
12. **WL-H12** — non-interference/inference leakage includes existence, counts, ranking, errors, timing, free-busy, candidates, explanations and aggregates.

## Phase 5 requirement envelope

### AuthN / AuthZ

Later implementation must preserve at minimum:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
actual Actor != represented party automatically
technical allow/deny != canonical governance truth
```

Consequential authorization/effect provenance must be reconstructible where required. Non-human Principals do not bypass governance. Delayed effects cannot rely indefinitely on stale target/governance state. Disclosure enforcement includes inference/non-interference surfaces.

Provider/protocol/session/policy-engine/enforcement mechanism selection remains deferred.

### Security / privacy / retention / security-aware recovery

Later design must support purpose-aware minimization, sensitive-data handling, secure credential/secret isolation, privacy-minimized observability, retention by category/purpose, truthful deletion/redaction/anonymization, non-reused native identity, propagation to derived/external state, security-governed backup/restore and prevention of unauthorized resurrection after restore.

Exact legal basis, retention durations, final classification catalogue, residency/processor obligations and concrete mechanisms remain open where not yet accepted.

### Consistency / side effects

Later design must preserve expected-state semantics, idempotency distinct from identity, no silent material last-write-wins, unresolved conflict where appropriate, semantic multi-owner atomicity where required, truthful staged/partial state where distributed atomicity is impossible, canonical/provider-effect separation, ambiguous-failure retry safety, derived-state freshness, delayed target/governance revalidation, publication/replay integrity and reconstructible consequential effect history.

Transaction/outbox/inbox/queue/workflow/CRDT/locking/isolation mechanisms remain later decisions except for the engine-neutral Phase 7 posture.

### Non-functional / multi-device / operational recovery

Later design must prevent silent consequential overwrite across devices, preserve divergence for reconciliation, define offline capability per operation, classify consistency/availability by consequence, preserve provider/degraded-state truth, support current-state access alongside long history, set material RPO/RTO/latency/availability/scale inputs before dependent scoring, preserve temporal/DST semantics, protect privacy in observability and prove recovery through destructive tests.

Numeric targets remain explicit open parameters where not accepted. Phase 10 defines synthetic/sensitivity treatment; the later Physical workstream executes the applicable benchmark evidence.

## Runtime / technical != Domain

Account, Principal, Credential, AuthZ decision, Agent, Tool, Workflow, Automation runtime, Notification delivery, Job, queue/outbox, cache/index, API DTO/route and protocol adapter are technical/product constructs unless separately revalidated. Authentication/security-session concepts must not be conflated with Domain `Session`.

## AI/context/runtime boundary

```text
AI/context/runtime representation != canonical LifeOS truth by default
model output != accepted canonical effect
tool invocation != governed operation
runtime Agent / Principal != Domain Actor automatically
```

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware and does not default to unrestricted history/database exposure.

LifeOS does not create a second generic AI-memory truth store. Durable information receives an accepted canonical/history/candidate/derived/source/provider disposition.

Configurable autonomy remains consequence/governance/policy based; no universal human-confirmation rule is imposed.

### Consequential AI evaluation

Before promoting a material change to model/provider/version, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy, the applicable behavior must pass versioned/reproducible evaluation pressure.

Minimum material pressure includes structured-output correctness, false canonical claims, candidate/canonical classification, tool errors, governance bypass, privacy/inference leakage, stale-context behavior, provider/model substitution regression, fallback/refusal behavior, approval flows and material cost/latency.

```text
eval result != canonical truth
eval PASS != Authority / governed-effect authorization
```

Concrete eval tooling and thresholds remain later engineering choices.

AI provider/model, agent framework, concrete tool protocol and conversation-runtime mechanisms remain open/deferred.

## Integration Hub boundary

Five modes remain explicit:

```text
canonical import
synchronized / mirrored provider state
live federated read
retrieval / index projection
action / tool integration
```

`ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider outcome != canonical LifeOS effect truth automatically.

Mapping may remain candidate/unresolved. Sync direction/conflict semantics are explicit. Live reads retain source/freshness/unknown state. Retrieval/index projections remain derived/deletion-aware. External actions preserve governance, idempotency, partial/unknown effect and reconciliation truth.

MCP/A2A/future protocols remain adapters, not ontology or governance.

## Durable execution posture

```text
BOUNDED ASYNC WORK
short / bounded / cheaply reconstructible
→ DB + worker/outbox style remains a valid baseline mechanism class

MATERIAL DURABLE PROCESS
long waits / human review / provider callbacks / crash-resume /
material cancellation / compensation / reconciliation
→ dedicated durable execution is structurally justified
```

Current dedicated candidate ranking:

```text
Restate   preferred structural-fit candidate — NOT SELECTED
Temporal  strongest mandatory challenger — NOT SELECTED
DBOS      conditional challenger — NOT SELECTED
          SQLite-capable for local/bounded Python use
          PostgreSQL recommended for production
          distributed multi-server topology PostgreSQL-coupled
```

No runtime can create exactly-once external reality by itself. Runtime completion/cancellation does not manufacture Domain Actual/Outcome/Confirmation/cancellation.

## Governed operation/effect contract

Consequential operations preserve by materiality:

```text
contract / operation version
semantic target / facet
requested effect
input / candidate
purpose / context
material / expected state
freshness/material basis
Principal / actual Actor / represented party
governance basis
autonomy / preview / confirmation
idempotency + operation equivalence
correlation / causation
execution requirement
expiry / deadline / technical cancellation
canonical result
provider/external result
runtime result
conflict / partial / reconciliation state
provenance / execution receipt
```

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
runtime cancellation != Domain cancellation automatically
workflow completed != Actual automatically
```

Concrete routes/DTOs/transports remain deferred.

## Search / observability / calendar / solver

### Search

Structured + lexical/full-text search is baseline. Semantic/vector retrieval is bounded. Search ranking/result omission/count/timing are disclosure surfaces; search miss != nonexistence; vector similarity != truth. Index state is projection, not canonical state.

### Observability

OpenTelemetry-first/equivalent is current direction. Telemetry identifiers do not become `NativeRef`, `MaterialStateRef`, durable execution identity or idempotency identity. Telemetry may be sampled/expired and does not replace required Domain Provenance/security audit/material history.

### Calendar

LifeOS time semantics remain Domain/Logical-owned. iCalendar/JSCalendar/provider schemas pressure-test recurrence, overrides, occurrence history, all-day/floating/zoned time, DST, provider resync/token invalidation and cancellation/deletion, but do not define ontology. Provider sync token != `MaterialStateRef`.

### Solver

Simple deterministic rules/heuristics remain baseline. OR-Tools CP-SAT is a preferred specialized benchmark candidate. `UNKNOWN != INFEASIBLE`. Solver output is candidate/projection bound to input/model/objective basis and crosses the governed-effect boundary before canonical change.

## Physical benchmark posture

Phase 10 defines the method; it does not authorize Physical work.

```text
PRIMARY CANONICAL LANE
PostgreSQL hybrid — current preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH LANE
no-specialized-store baseline vs Neo4j

SEARCH / SEMANTIC RETRIEVAL LANE
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded mechanisms first; specialized candidate only on demonstrated need/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Benchmark rules include:

- semantic/correctness hard gates before weighted scoring;
- candidate-idiomatic physical mappings against common semantic assertions;
- expected-state races, multi-owner consistency, deep history, selective disclosure, provider divergence, deletion+restore, recurrence/DST, vector filtering, solver freshness, recovery and schema evolution;
- synthetic LOW/BASE/HIGH qualification tiers, not forecasts;
- exact product version + edition/license + deployment-mode evidence pinning;
- sensitivity-dependent outcomes where open NFR assumptions materially change preference;
- unexecuted scale envelopes remain unverified rather than fabricated as runs;
- `PREFERRED != SELECTED`.

## Repository engineering safety

Phase 11 is QA PASS. Effective remote protection for `main` was verified rather than inferred from documentation.

Current owner-driven safety posture:

```text
PR required
main deletion blocked
force-push / non-fast-forward blocked
review-thread resolution required
required approvals = 0 while no independent reviewer exists
required status checks = none until real stable checks exist
merge-commit history preserved by current policy
```

Required CI checks are introduced only after real workflows/check contexts exist and demonstrate stable blocking value. Backend/Physical work must not weaken repository protections for convenience.

Connector-unverifiable security-setting state remains explicitly distinguished from remotely verified branch/ruleset state.

## Open decisions before/during Physical

Open parameters remain obligations, not permission for arbitrary defaults. They include as applicable:

- accepted operational RPO/RTO/availability/latency/scale targets where candidate scoring materially depends on them;
- final Physical primary-store mapping and adjunct-store justification;
- concrete consistency/isolation/index/history/recovery mechanisms;
- concrete AuthN/AuthZ provider/policy/enforcement mechanisms;
- durable runtime implementation binding;
- concrete API/DTO/transport design;
- provider adapter/runtime integration mechanisms;
- search/vector physical design;
- observability backend/vendor;
- solver service/implementation design;
- AI evaluation framework/datasets/runners/thresholds and promotion automation.

## Explicitly unauthorized now

No Physical schema/tables/keys/indexes/constraints, PostgreSQL/TypeDB/Neo4j mapping, SQL/TypeQL/Cypher benchmark implementation, migrations, concrete API routes/DTOs, AuthN/AuthZ implementation, Restate/Temporal/DBOS adoption, queue/outbox implementation, provider adapters, AI provider/model/agent implementation, MCP/A2A adoption, dedicated search/vector deployment, telemetry vendor, solver implementation, production backend code or `feature/backend-foundation` may be started from this baseline.

Domain/Logical changes require a separate explicit reopen gate.

## Final independent-audit boundary

Phase 12 clean-room QA is closed. A subsequent independent total audit rechecked the entire Pre-Physical branch delta and found no major semantic/architectural contradiction, accidental Physical/backend start or material knowledge loss. It found only bounded current-truth/factual/engineering hardening repairs, including the DBOS coupling correction and explicit consequential AI evaluation requirement.

This baseline incorporates those repairs but does **not self-certify definitive closure**.

Definitive closure activates only when the final audit gate proves remotely:

```text
approved final-audit paths only
no unexpected delete/path
branch not behind PRE-SCOPE
main baseline unchanged
critical current authorities readable/coherent
Domain/Logical unchanged
Physical/backend not started
```

Main integration remains separate and is not performed by this closure gate.

## Documentation/evidence rule

```text
CURRENT SPECIFICATION = current truth
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

Current sources must not retain stale execution instructions merely to preserve history. Historical checkpoints must not be rewritten to look current.