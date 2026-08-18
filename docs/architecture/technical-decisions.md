# Technical Decisions

- Status: **Current technical direction — Pre-Physical DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED**
- Last updated: 2026-08-18
- Closure activation checkpoint: `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`
- Main integration checkpoint: `74593ae283ce5a1d22335502480ee3fa54be0436` via PR #13 — **POST-MERGE VERIFIED**

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
Phase 10 Physical benchmark method       CURRENT / QA PASS
Phase 11 repository engineering safety   QA PASS
Phase 12 clean-room QA                    QA PASS / CLOSED
Independent total Pre-Physical audit     PASS

Pre-Physical Coherence
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED INTO MAIN VIA PR #13
POST-MERGE VERIFIED

Physical readiness
ESTABLISHED

Physical Model
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

Backend Foundation
NOT STARTED / DEFERRED

Main integration
COMPLETE / POST-MERGE VERIFIED
```

## Clients and backend direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Architecture direction: modular monolith first.
- Clients use versioned governed backend contracts, not direct primary-persistence access.
- Domain/application logic remains independent from HTTP/framework handling.
- SQLAlchemy/Alembic remain conditional on the later accepted Physical design.

No production backend implementation is authorized by these directions.

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

## Physical persistence posture

No Physical technology is selected.

```text
PRIMARY CANONICAL
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / SEMANTIC RETRIEVAL
structured + lexical/full-text baseline vs bounded pgvector where applicable

EVENT / DOCUMENT
bounded native mechanisms first
specialized product only on demonstrated gap/benefit

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

Phase 10 defines the benchmark method, not the winner.

Mandatory benchmark posture:

```text
hard semantic/correctness gates
→ role-specific scoring only after PASS
→ LOW / BASE / HIGH + NFR sensitivity
→ exact version / edition / deployment evidence
→ PASS / PASS-CONDITIONAL / HOLD / REJECT /
  SENSITIVITY-DEPENDENT / PREFERRED
```

`PREFERRED != SELECTED`.

LOW/BASE/HIGH are synthetic qualification envelopes, not business forecasts. An unexecuted upper envelope must not be reported as `VERIFIED-RUN`; progressive saturation/scaling evidence is acceptable only when its limits are explicit.

## State/history/consistency direction

Future implementation must preserve, where applicable:

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

Before promotion of a materially consequential change to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy, LifeOS requires versioned/reproducible evaluation appropriate to the affected behavior.

Pressure includes, where material:

```text
structured-output correctness
false canonical claims / semantic overreach
candidate-vs-canonical classification
tool-selection / tool-argument errors
governance bypass
privacy / inference leakage
stale-context behavior
model/provider substitution regression
fallback / refusal / malformed-output behavior
confirmation / human-approval flows
cost / latency
```

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

DBOS coupling is deployment-dependent rather than universally PostgreSQL-required in Python. No workflow runtime creates exactly-once external reality by itself, and runtime state does not become canonical Domain history/ontology.

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
- Neo4j remains a secondary/read-projection challenger against the no-specialized-store baseline;
- OR-Tools CP-SAT remains a solver benchmark candidate;
- event/document/policy/analytics/time-series systems remain bounded candidates requiring evidence.

## Repository safety

Phase 11 verified effective `main` protections remotely:

```text
PR integration required
main deletion blocked
non-fast-forward / force-push blocked
review-thread resolution required
required approvals 0 while no independent reviewer exists
required status checks 0 until real stable contexts exist
auto-delete merged head branches enabled
```

A documented setting is not evidence of application by itself; remote state must be re-read for future changes.

PR #13 subsequently exercised those rules successfully: the Pre-Physical branch merged through protected `main`, and the head branch was auto-deleted after merge.

## Definitive Pre-Physical closure and integration evidence

Phase 12 is QA PASS/CLOSED. The subsequent independent total audit found no major semantic/architectural contradiction, Domain/Logical reopen need, material knowledge loss, accidental technology selection or accidental Physical/backend start.

The bounded final repair gate was activated at:

`9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d`

with exact evidence:

```text
PRE-SCOPE     1bd142afe51221211bc777f6271a642911c650fc
unique paths  23
added          1
modified      22
deleted        0
unexpected     0
behind_by      0
main           148a4cb5d5741b4a5b9667cf8d30231ebc0545f0 unchanged
critical readback PASS
```

That evidence established definitive branch-local closure. PR #13 then integrated final branch HEAD `34e9ea3b547922600cb472adf1549a321e6ddfe4` into protected `main` at merge commit `74593ae283ce5a1d22335502480ee3fa54be0436`. Post-merge compare proved one merge commit and zero file differences.

Therefore Pre-Physical Coherence is **DEFINITIVE CLOSED / FINAL QA PASS / INTEGRATED / POST-MERGE VERIFIED**.

## Explicit next boundary

```text
PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED
```

Pre-Physical integration is complete. No Physical or backend implementation is authorized by that fact. Starting the Physical Model requires a new explicit user authorization and fresh workstream gate; Backend Foundation remains deferred until the Physical result is separately accepted.