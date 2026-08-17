# LifeOS Roadmap

- Last updated: 2026-08-17
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current LifeOS identity/North Star and supporting V1 product studies are integrated.

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream constraints
```

Logical closure does not select Physical persistence/API/Auth/runtime/backend implementation.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/backend architecture.

## Active backend/architecture preparation track

### Pre-Physical Repository & Architecture Coherence

Branch: `chore/pre-physical-coherence`  
Handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)

Current progress:

```text
Phase 0 — baseline/freeze
PASS

Phase 1 — global current-truth entry-point alignment
QA PASS

Phase 2 — architecture supersession/current-truth cleanup
QA PASS

Phase 3 — Backend Foundation handoff cleanup
QA PASS

Phase 4 — Current Pre-Physical Architecture Baseline
QA PASS

Phase 5 — requirements that can constrain Physical design
QA PASS

Phase 6 — AI/context/runtime/integration boundaries
NEXT
```

This workstream does **not** itself start the Physical Model.

## Documentation architecture rule

Current specifications contain current truth only. Obsolete design chronology does not accumulate inside them.

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit supersession/qualification

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

When a canonical document is physically split, the complete continuation chain is one logical document and must be read before drawing current-state conclusions. Physical splitting is a tooling/layout mechanism, not a reason to create parallel authority.

A split performed only because of file size/tool/connector limits is a **lossless physical partition of the complete logical payload**. It must not summarize, condense, omit or hide a semantic rewrite. Chronological/evidence continuation is a distinct case and may append genuine later evidence after the previous payload.

## Pre-Physical sequence

1. **Phase 0 — freeze/current-state inventory** — PASS.
2. **Phase 1 — global entry-point/current-truth alignment** — QA PASS.
3. **Phase 2 — architecture supersession/current-truth cleanup** — QA PASS.
4. **Phase 3 — Backend Foundation handoff cleanup** — QA PASS.
5. **Phase 4 — current Pre-Physical Architecture Baseline** — QA PASS.
6. **Phase 5 — requirements that can constrain Physical design** — QA PASS:
   - AuthN/AuthZ;
   - security/privacy/retention/security-aware recovery;
   - consistency/side effects;
   - non-functional/multi-device/operational recovery.
7. **Phase 6 — AI/context/runtime/integration boundaries** — NEXT.
8. **Phase 7 — durable workflow / async benchmark**.
9. **Phase 8 — governed API/command/effect contract**.
10. **Phase 9 — search/observability/calendar/solver pressure tests**.
11. **Phase 10 — Physical benchmark specification/register**.
12. **Phase 11 — repository engineering safety alignment**.
13. **Phase 12 — clean-room repository/architecture coherence QA and closure**.
14. **Separate user gate** — decide whether to authorize a Physical Model workstream.

## Current architecture sources

Current navigation:

- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
- [`architecture/requirements/README.md`](architecture/requirements/README.md) plus all four Phase 5 requirement packages
- [`architecture/README.md`](architecture/README.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

The Pre-Physical Architecture Baseline is the current bridge for decided/prohibited/open/mandatory downstream constraints and authorization boundaries. It coordinates but does not replace Domain/Logical/ADR authority.

The Phase 5 requirement package defines what later Physical/runtime/API/backend design must satisfy while separating accepted requirements, explicit open parameters and implementation-deferred mechanisms.

The old mixed `architecture/personal-data-ai-integration.md` current specification has been retired after knowledge-coverage QA. Its surviving valid knowledge is carried by current architecture, ADR, Logical and Pre-Physical sources; the old payload remains recoverable in Git history.

The `architecture/domain-model-logical-readiness*` chain remains historical transition/validation evidence, not a current architecture specification.

## Current Physical technology posture — benchmark, not selection

- **PostgreSQL hybrid:** current preferred baseline, not final selection.
- **TypeDB:** mandatory challenger.
- **Neo4j/property graph:** serious secondary/read-projection challenger.
- **event store/event stream:** bounded history/integration mechanism candidate.
- **document store:** bounded provider/specialist/flexible candidate.
- **pgvector:** bounded semantic-retrieval candidate.
- **generic EAV/generic edge/universal meta-model:** hard reject for canonical kernel.
- **durable workflow technologies:** separate runtime benchmark, not persistence ontology.

Technology selection must use LifeOS-specific correctness/history/governance/concurrency/operability pressure.

## Phase 3 — Backend Foundation handoff cleanup — QA PASS

The future Backend Foundation handoff has been rewritten against current accepted truth.

Current result:

- Backend Foundation remains **NOT STARTED / DEFERRED**;
- no `feature/backend-foundation` branch is authorized or created;
- closed Domain + Logical are prerequisites to consume, not work to recreate inside backend bootstrap;
- SQLAlchemy/Alembic are conditional on accepted Physical persistence;
- PostgreSQL remains a preferred benchmark baseline, not a preselected implementation mandate;
- concrete routes/DTOs/Auth/runtime/outbox/workflow/provider mechanisms wait for their accepted prerequisite contracts;
- the old `Workspace → Goal/Program → Activity → Schedule → Actual/Confirmation` slice is superseded as a canonical backend/domain contract;
- valid future Python/FastAPI/Pydantic/modular-monolith/testing/provider-abstraction requirements are preserved;
- older product documents remain evidence/requirements input and do not override accepted Domain/Logical semantics.

Backend Foundation may become executable only after Pre-Physical closure, separate Physical acceptance and the applicable accepted runtime/security/integration/API prerequisites.

## Phase 4 — current Pre-Physical Architecture Baseline — QA PASS

[`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) provides one current bridge source for:

- decided current direction versus implementation authorization;
- semantic prohibitions/non-collapse guardrails;
- Logical representation/reference and state-layer boundaries;
- mandatory `WL-H01..WL-H12` downstream constraints;
- runtime/product/technical concepts that are not Domain owners by default;
- AI/context/integration boundaries already decided versus still open;
- Physical and durable-workflow benchmark posture;
- explicit Phase 5–12 ownership of unresolved requirements/benchmark work;
- explicit non-authorization of Physical/schema/API/Auth/runtime/provider/backend implementation.

Backend Foundation names this baseline as mandatory downstream reading. Domain and Logical semantics were not reopened or rewritten.

## Phase 5 — requirements before Physical — QA PASS

Current requirement index: [`architecture/requirements/README.md`](architecture/requirements/README.md).

Phase 5 establishes four distinct current logical requirement documents:

### AuthN/AuthZ

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
actual Actor != represented party automatically
```

Consequential effects must preserve bounded governance/authorization provenance, non-human Principals do not bypass governance, delayed effects require valid governance-time semantics, and selective disclosure includes inference/non-interference surfaces.

Provider, protocol, MFA/passkey/password, token/session, policy-engine and enforcement-mechanism choices remain deferred/open where marked.

### Security/privacy/retention/security-aware recovery

Requirements now cover purpose-aware minimization, sensitive-data handling, credential/secret isolation, privacy-minimized observability, category/purpose-sensitive retention, truthful deletion/redaction/anonymization, non-reused identity, propagation to derived/external state, protected/audited backup access and restore behavior that does not resurrect forbidden data.

Exact legal basis, retention schedules, final data classification, residency/processor obligations and concrete security technologies remain explicit later decisions rather than Phase 5 guesses.

### Consistency/side effects

Requirements now cover expected state, idempotency distinct from identity, no silent material last-write-wins, unresolved conflict, semantic multi-owner atomicity where required, truthful staged/partial distributed state, canonical/provider-effect separation, ambiguous-failure retry safety, derived-state freshness, delayed target/governance validation, publication/replay pressure and reconciliation/compensation truthfulness.

Transaction isolation, locks, outbox/inbox, queue/event bus, workflow, saga and CRDT/OT mechanisms remain deferred.

### Non-functional/multi-device/operational recovery

Requirements now cover multi-device divergence, operation-specific offline behavior, consequence-specific consistency/availability classes, truthful provider/degraded state, efficient current-state access alongside long history, temporal/DST preservation, privacy-safe observability, capacity/backpressure, recovery testing and explicit RPO/RTO/latency/availability/scale benchmark inputs.

No arbitrary numeric RPO/RTO/SLA/latency/scale/offline-duration values were invented. They are recorded as mandatory open parameters/scenario inputs for later gates.

### Phase 5 remote content QA

```text
PRE-SCOPE
 e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f

CONTENT HEAD BEFORE GLOBAL CLOSURE MARKERS
 c29cfe4bde47d5df4f46507a5f1717acd1903112

ahead_by       10
behind_by       0
total_commits   10
added            5
modified         5
deleted          0
unexpected       0
```

No Domain/Logical/ADR/Physical/backend implementation path was changed by the Phase 5 content package.

## Phase 6 — AI/context/runtime/integration boundaries — NEXT

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

Phase 6 must define what may enter AI/runtime context, which state is durable/canonical vs derived/live/transient, how tool/agent actions cross the governed-effect boundary, how provider/runtime identity and provenance are preserved, and how integration modes behave under the Phase 5 security/AuthZ/consistency requirements.

Runtime concepts such as Agent/Workflow/Automation/Notification remain technical/product concepts unless separate semantic evidence proves otherwise.

Integration modes remain:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

MCP/A2A/future protocols are adapters, not ontology.

## Phase 7 — durable workflow / async benchmark

Compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

Pressure: provider retry/sync, human approval, long AI work, reconciliation, cancellation/timeouts, partial external effect and crash recovery.

## Phase 8 — governed API/command/effect contract

Before concrete routes, define consequential-operation requirements around principal/actor, semantic target, operation/effect, expected state, inputs/context/purpose, authorization basis, idempotency/correlation, confirmation and result/provenance/conflict semantics.

```text
HTTP route / UI button / AuthZ action string
!= canonical Governed Operation
```

## Phase 9 — search/observability/calendar/solver pressure

- search/retrieval projection separate from canonical truth;
- structured/full-text baseline and bounded pgvector candidate where applicable;
- specialized search/vector only on demonstrated benefit;
- standards-based observability with privacy minimization;
- iCalendar/JSCalendar/Google/Microsoft semantics as interoperability pressure, not ontology;
- deterministic solver/services for deterministic constraints;
- AI for ambiguity/interpretation/explanation/cross-domain reasoning where useful;
- truthful feasible/infeasible/uncertain/at-risk/conflicting/partial planner outcomes.

## Phase 10 — Physical benchmark specification/register

Benchmark destructive LifeOS scenarios including:

- concurrent consequential edits;
- expected-state conflicts;
- multi-owner changes;
- selective disclosure/inference leakage;
- provider divergence/reconciliation;
- redaction/history reconstruction;
- recurrence across DST;
- stale availability/derived state;
- AuthZ provenance;
- AI proposal → approval → effect;
- revoked consent/authority during execution;
- long-running crash/restart;
- backup/restore;
- schema evolution over historical state;
- multi-device/offline divergence;
- ambiguous external-effect failure/replay;
- restore after deletion/redaction;
- explicit low/base/high scale and performance scenarios where exact forecasts remain open.

Phase 10 must resolve or scenario-model Phase 5 open parameters when their values materially affect candidate scoring.

## Phase 11 — repository engineering safety

Before production backend implementation, establish appropriate main protection/ruleset/CI/required checks when concrete checks exist.

## Phase 12 — clean-room QA and closure

A new agent with no chat context must reconstruct:

```text
what LifeOS is
→ current/canonical sources
→ Domain CLOSED
→ Logical CLOSED
→ current architecture truth
→ requirements constraining downstream design
→ benchmark candidates
→ what remains unauthorized
```

Target closure:

```text
REPOSITORY / ARCHITECTURE COHERENCE
PASS

DOMAIN
UNCHANGED / CLOSED

LOGICAL
UNCHANGED / CLOSED

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED
```

## Backend Foundation / implementation — later

Backend Foundation and production implementation are **NOT STARTED / DEFERRED**.

Only after accepted prerequisites should implementation proceed through bounded vertical slices derived from Domain + Logical + Phase 5 requirements + Physical/current runtime contracts rather than old product-label schemas.

## Explicitly rejected/deferred by default

Do not introduce by default:

- permanent dev/uat/prod Git branches;
- microservices/Kubernetes by fashion;
- document/graph/meta-model storage as universal canonical kernel;
- generic EAV/generic-edge ontology;
- specialized search/cache/vector/analytics/workflow infrastructure without demonstrated benefit;
- implicit collaboration/social implementation inside personal-first V1.

Specialized infrastructure may be justified by measured workload **or** strong structural benefit in correctness/durability/security/evolvability/operations/migration risk.
