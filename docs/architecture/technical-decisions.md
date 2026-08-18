# Technical Decisions

- Status: **Current technical direction — Physical Model authorized / PM-00 bootstrap**
- Last updated: 2026-08-18
- Pre-Physical closure activation: `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`
- Pre-Physical integration: `74593ae283ce5a1d22335502480ee3fa54be0436` via PR #13
- Post-merge alignment / Physical base: `3de84bb49f9cef30e88e9bde4961ed84335daa79` via PR #14

This document is a current technical summary. Detailed requirements/contracts remain authoritative in their dedicated sources; historical rationale remains in ADRs, evidence and Git.

## Stage boundary

```text
Product / North Star                      CURRENT
Domain Model / Domain Atlas              CLOSED
Logical Model                            CLOSED
Phase 5 requirements                     CURRENT
Phase 6 AI/context/runtime/integration   CURRENT
Phase 7 durable execution                CURRENT
Phase 8 governed operation/effect        CURRENT
Phase 9 search/observability/calendar/solver CURRENT
Phase 10 Physical benchmark method       CURRENT / QA PASS / ACTIVE INPUT
Phase 11 repository engineering safety   QA PASS
Phase 12 + independent audit             CLOSED / PASS
Pre-Physical Coherence                   CLOSED / INTEGRATED / VERIFIED

Physical Model
AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP
feature/physical-model
mapping NOT STARTED
benchmark NOT STARTED
selection NONE

Backend Foundation
NOT STARTED / DEFERRED
```

## Clients and backend direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Architecture direction: modular monolith first.
- Clients use versioned governed backend contracts, not direct primary-persistence access.
- Domain/application logic remains independent from HTTP/framework handling.
- SQLAlchemy/Alembic remain conditional on the later accepted Physical design.

No production backend implementation is authorized by these directions or by the active Physical benchmark workstream.

## Semantic/model authority

Technical design follows the accepted Domain Atlas and closed Logical Model; storage/runtime convenience does not create ontology.

Rejected for the canonical kernel:

```text
universal semantic Entity / Thing
universal generic Relationship / edge
generic EAV / property-bag ontology
provider schema as LifeOS ontology
AI-output schema as LifeOS ontology
unresolved AI meaning persisted as fabricated generic canonical truth
```

Bounded technical registries, discriminators, references, JSON/provider metadata, indexes and projections remain allowed where semantic ownership stays explicit.

## Active Physical persistence posture

No Physical technology is selected.

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
G0 no-specialized-store baseline vs G1 Neo4j

SEARCH / SEMANTIC RETRIEVAL
S0 structured + lexical/full-text baseline vs S1 bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first
specialized product only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Phase 10 defines the benchmark method. `feature/physical-model` now executes it under `docs/physical-model/**`.

Mandatory posture:

```text
hard semantic/correctness gates
→ role-specific scoring only after PASS
→ LOW / BASE / HIGH + NFR sensitivity
→ exact product / version / edition / deployment evidence
→ PASS / PASS-CONDITIONAL / HOLD / REJECT /
  SENSITIVITY-DEPENDENT / PREFERRED
→ explicit PM-11 selection gate
```

```text
NOT RUN != PASS
unexecuted tier != VERIFIED-RUN
PREFERRED != SELECTED
official capability claim != direct execution evidence
```

PM-00 bootstrap does not authorize candidate schemas, SQL/TypeQL/Cypher, harness code, database deployment or selection. After PM-00 QA, PM-01 is read-only candidate/environment freeze.

## State/history/consistency direction

Physical design must preserve, where applicable:

- intended/planned vs accepted/current vs actual realization;
- Actual vs Observation/Outcome;
- canonical vs provider/external state;
- material state/history vs derived projection;
- candidate/unresolved vs established canonical meaning;
- correction/version/reconciliation vs silent overwrite;
- owner identity vs storage/provider/runtime identity;
- expected-state semantics for consequential writes;
- atomic multi-owner changes where required or truthful staged/partial state with reconciliation/compensation.

```text
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
ETag / MVCC token / provider revision != MaterialStateRef by identity
idempotency != semantic identity
absence / unknown != false
```

## Flexible/provider data and object storage

JSON/metadata may represent genuinely flexible, low-consequence, provider-specific or specialist detail; it must not hide unresolved kernel semantics.

Large file bytes remain behind a StorageProvider/object-storage abstraction. Content Artifact identity is not identical to blob/path/URL/provider-object identity.

## Integration Hub

Five modes remain distinct:

```text
canonical import
sync / mirror
live federated read
retrieval / index projection
action / tool integration
```

```text
ExternalRef != NativeRef
provider revision != MaterialStateRef
provider state/effect != canonical LifeOS state/effect automatically
provider/tool operation string != canonical governed effect
```

Callbacks/webhooks/polling/push are adapter mechanisms. MCP/A2A/future protocols remain adapters, not ontology/governance authority.

## AI / context / runtime

AI remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

```text
AI memory != second canonical truth store
model output != accepted canonical effect
tool invocation != authorization
runtime Agent / Principal != Domain Actor automatically
```

### Consequential AI change evaluation

Before promotion of materially consequential changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy, LifeOS requires versioned/reproducible evaluation appropriate to affected behavior.

Pressure includes structured-output correctness, false canonical claims, candidate/canonical classification, tool errors, governance bypass, privacy/inference leakage, stale context, substitution regression, fallback/refusal, approval flows and material cost/latency.

```text
eval result != canonical LifeOS truth
eval PASS != Authority
eval PASS != governed-effect authorization
```

Concrete eval framework/datasets/runners/thresholds/CI remain later engineering choices.

## Governed operations/effects

Consequential operation meaning remains independent from route/UI/tool/AuthZ/workflow implementation.

```text
request accepted != effect completed
provider acknowledgement != canonical completion automatically
workflow completion != Actual automatically
technical cancellation != Domain cancellation automatically
```

Where material, preserve contract/version, semantic target/effect, input/candidate, purpose/context, expected/material state, freshness basis, Principal/Actor/represented party, governance, autonomy/confirmation, idempotency/equivalence, correlation/causation, execution class, deadlines/cancellation semantics and independent canonical/provider/runtime/reconciliation outcomes.

## Security / AuthZ

Later implementation preserves:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Consequential authorization/effect provenance must be reconstructible where required. Non-human Principals do not bypass semantic governance.

## Durable execution

LifeOS does not adopt one universal async/workflow mechanism.

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable local/bounded Python use
          PostgreSQL recommended for production
          distributed multi-server topology PostgreSQL-coupled
```

Physical evidence may affect runtime infrastructure coupling/cost, but cannot select a runtime implicitly. No workflow runtime creates exactly-once external reality by itself and runtime state does not become Domain ontology/history by identity.

## Search / observability / calendar / solver

```text
SEARCH
structured filters + lexical/full-text = baseline
semantic/vector retrieval = bounded candidate
search miss != canonical nonexistence
index/embedding/ranking != canonical truth

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected
telemetry != Domain Provenance / security audit automatically

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure
provider schema/token != LifeOS ontology / MaterialStateRef

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred specialized benchmark candidate — NOT implemented
UNKNOWN != INFEASIBLE
solver result != accepted canonical effect
```

## Specialized-infrastructure rule

A specialized system is admitted only on demonstrated measured or strong structural benefit in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Current consequences:

- dedicated durable execution is structurally justified for material long-running classes, but no engine is selected;
- dedicated search/vector infrastructure is not justified by default;
- Neo4j remains a secondary/read-projection challenger against G0;
- OR-Tools CP-SAT remains a solver benchmark candidate;
- event/document/policy/analytics/time-series systems remain bounded candidates requiring evidence.

## Repository safety

Effective `main` protections are remotely verified:

```text
PR integration required
main deletion blocked
non-fast-forward / force-push blocked
review-thread resolution required
required approvals 0 while no independent reviewer exists
required status checks 0 until real stable contexts exist
auto-delete merged head branches enabled
```

`feature/physical-model` is an active bounded branch. Benchmark harness/evidence does not become production infrastructure or a required status check automatically.

No secrets or personal production data may enter benchmark fixtures/artifacts.

## Pre-Physical closure/integration

Phase 12 + independent audit passed. PR #13 integrated Pre-Physical; PR #14 aligned current truth. The Physical workstream starts from accepted `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79` and does not reopen those completed phases by convenience.

## Explicit next boundary

```text
PM-00 BOOTSTRAP
remote QA required

THEN
PM-01 READ-ONLY FIRST
freeze exact current PostgreSQL/TypeDB versions/editions/deployment modes
freeze available benchmark hardware/environment
verify version-sensitive capabilities from official primary sources
produce execution inventory/evidence plan
STOP before first mapping/schema/harness write
```

Backend Foundation remains **NOT STARTED / DEFERRED** until a Physical result is explicitly selected/accepted and its remaining prerequisites are satisfied.