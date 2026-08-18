# Project Status

- Last updated: 2026-08-18
- Canonical integrated branch: `main`
- Accepted `main` baseline for this Pre-Physical workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Active backend/architecture preparation branch: `chore/pre-physical-coherence`
- Production application code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Main integration of Pre-Physical branch: **NOT PERFORMED**

## Current stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated through PR #10
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED — integrated through PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
FINAL CLOSURE CANDIDATE
Phase 0–11 QA PASS
Phase 12 QA PASS / CLOSED
Independent total audit CORE PASS
bounded final repairs incorporated
exact final remote activation QA pending

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

MAIN INTEGRATION
NOT PERFORMED
```

Phase 4 UX remains a separate active product/design workstream on `prototype/phase-4-today-home`.

## Read this first

1. [`README.md`](../README.md)
2. [`docs/README.md`](README.md)
3. this file
4. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
5. [`development/operating-rules.md`](development/operating-rules.md)
6. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
7. [`development/branching-and-environments.md`](development/branching-and-environments.md)
8. [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md)
9. [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md)
10. [`architecture/README.md`](architecture/README.md) and [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md)
11. complete Phase 5 requirement package + Phase 6–10 current contracts/method package
12. [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md)
13. [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md)
14. relevant ADR/evidence/methodology and implementation/tests

Conversation history is secondary to repository truth.

A canonical split/cumulative continuation chain is one logical document. A size/tool-limit split is lossless physical partitioning, not summary/condensation/hidden semantic rewrite.

## Accepted/current foundations

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current Product/North Star.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- [`architecture/pre-physical-architecture-baseline.md`](architecture/pre-physical-architecture-baseline.md) — **CURRENT** bridge; `DECIDED != AUTHORIZED TO IMPLEMENT`.
- Phase 5 requirement package — **CURRENT**.
- [`architecture/ai-context-runtime-boundaries.md`](architecture/ai-context-runtime-boundaries.md) — **CURRENT** Phase 6 AI/context/runtime contract, including consequential AI evaluation/regression requirement.
- [`architecture/integration-hub-boundaries.md`](architecture/integration-hub-boundaries.md) — **CURRENT** Phase 6 Integration Hub contract.
- [`architecture/durable-execution-benchmark.md`](architecture/durable-execution-benchmark.md) — **CURRENT** Phase 7 posture.
- [`architecture/governed-operation-effect-contract.md`](architecture/governed-operation-effect-contract.md) — **CURRENT** Phase 8 contract.
- [`architecture/search-observability-calendar-solver-boundaries.md`](architecture/search-observability-calendar-solver-boundaries.md) — **CURRENT** Phase 9 contract.
- Phase 10 benchmark-method package — **CURRENT / QA PASS**.
- [`development/repository-engineering-safety.md`](development/repository-engineering-safety.md) — **CURRENT / Phase 11 QA PASS**.
- [`architecture/pre-physical-clean-room-qa.md`](architecture/pre-physical-clean-room-qa.md) — **Phase 12 QA PASS / CLOSED evidence**.
- [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md) — independent total-audit/final activation record.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional on accepted Physical persistence.
- DEV/UAT/PROD — deployment environments, not permanent Git branches.

## Domain / Logical closure

Domain closure remains:

```text
WHOLE-DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED
```

Logical closure remains:

```text
WHOLE-LOGICAL
PASS WITH HARDENING
REMOTE QA PASS
CLOSED
WD-03 PASS
WD-05 PASS
```

The Pre-Physical workstream made no Domain/Logical semantic edits. Any future semantic contradiction requires a separate explicit reopen scope.

## Current Phase 5 requirement inputs

Current owners:

- AuthN/AuthZ;
- security/privacy/retention/security-aware recovery;
- consistency/side effects;
- non-functional/multi-device/operational recovery.

Requirements include `Person != Account != Principal != Actor`, consequential AuthZ provenance, actual Actor vs represented party, purpose-aware minimization, truthful deletion/redaction/tombstones, secure restore, expected-state writes, idempotency != identity, no silent material last-write-wins, truthful multi-owner consistency, canonical/provider separation, multi-device divergence, operation-specific offline semantics and recovery testing.

Open RPO/RTO/latency/availability/scale/offline-duration values remain explicit parameters until accepted later where needed. Phase 10 defines synthetic/sensitivity treatment; the later Physical workstream executes candidate evidence.

## Current Phase 6 boundary inputs

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Context is purpose/minimization/disclosure/provenance/freshness bounded. Generic AI memory is not a second canonical truth store. Runtime Agent/Principal != Domain Actor automatically; tool invocation != authorization/governed effect.

Material consequential changes to model/model version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Integration Hub modes remain canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration. `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical state/effect automatically.

## Current Phase 7–9 inputs

### Durable execution

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional challenger — NOT selected
          SQLite-capable local/bounded Python use
          PostgreSQL-recommended production
          distributed multi-server PostgreSQL-coupled
```

### Governed operation/effect

Consequential semantics preserve target/effect, expected material state, purpose/context, Principal/Actor/represented party, governance, confirmation/autonomy, idempotency/equivalence, correlation/causation, execution class and independent canonical/provider/runtime/reconciliation outcomes.

```text
HTTP/UI/tool/AuthZ/workflow step != canonical governed operation
request accepted != effect complete
provider acknowledgement != canonical completion automatically
workflow completed != Actual automatically
technical cancellation != Domain cancellation automatically
```

### Search / observability / calendar / solver

```text
SEARCH
structured + lexical/full-text = baseline
semantic/vector = bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent = direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics = baseline
OR-Tools CP-SAT = preferred benchmark candidate — NOT implemented
```

## Current Phase 10 benchmark posture

Phase 10 defines how a later separately authorized Physical benchmark must run. It does not select or implement a Physical Model.

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector

EVENT / DOCUMENT
bounded native mechanisms first; specialized candidate only on demonstrated gap/benefit
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Unexecuted tiers remain unverified. Evidence pins exact product/version/edition/deployment. `PREFERRED != SELECTED`.

## Phase 11 repository engineering safety — QA PASS

Verified core state:

```text
ruleset                              lifeos-main-safety
ruleset enforcement                  active
target                               default branch
main deletion                        blocked
force-push / non-fast-forward        blocked
pull request before merge            required
required approvals                   0
review-thread resolution             required
required status checks               0 while no real stable contexts exist
auto-delete merged head branches     enabled
confirmed accidental refs            absent
```

Security endpoints inaccessible to the connector remain explicitly connector-unverifiable rather than inferred.

## Phase 12 result

Phase 12 clean-room QA is **QA PASS / CLOSED**. Its exact 11-path final gate was independently rechecked before this final audit.

It found bounded current-consumer/discoverability issues only; no Domain/Logical/Physical/backend semantic change was required.

## Independent total Pre-Physical audit

The broader post-Phase-12 audit rechecked the full branch delta against the accepted `main` baseline.

Core verdict:

```text
CORE ARCHITECTURE HOLDS                 PASS
DOMAIN REOPEN REQUIRED                     0
LOGICAL REOPEN REQUIRED                    0
NEW DOMAIN OWNER REQUIRED                  0
MAJOR SEMANTIC CONTRADICTION                0
MAJOR ARCHITECTURAL CONTRADICTION           0
PHYSICAL WORK ACCIDENTALLY STARTED          0
BACKEND ACCIDENTALLY STARTED                0
MAJOR KNOWLEDGE LOSS                        0
TECHNOLOGY ACCIDENTALLY SELECTED            0
```

Bounded repairs included stale current-stage prose, Phase10-method-vs-Physical-execution wording, documentation bootstrap/hygiene, DBOS coupling precision and explicit consequential AI evaluation requirements.

Final evidence: [`architecture/pre-physical-final-coherence-audit.md`](architecture/pre-physical-final-coherence-audit.md).

## Final closure activation contract

The branch is not declared definitively closed merely because the audit record exists.

Definitive closure requires final remote evidence:

```text
branch        chore/pre-physical-coherence
PRE-SCOPE     1bd142afe51221211bc777f6271a642911c650fc
main          148a4cb5d5741b4a5b9667cf8d30231ebc0545f0
unique paths  23
added          1
modified      22
deleted        0
unexpected     0
behind_by      0
critical current-authority readback PASS
```

If these conditions pass, the operative result becomes:

```text
PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

INDEPENDENT TOTAL AUDIT
PASS

PHYSICAL READINESS
ESTABLISHED
PHYSICAL MODEL NOT STARTED / NOT AUTHORIZED

BACKEND
NOT STARTED / DEFERRED

MAIN INTEGRATION
PENDING / NOT PERFORMED
```

Until that final proof is complete, current status is `FINAL CLOSURE CANDIDATE`.

## Milestone ledger

| Scope | Result |
|---|---|
| Phase 0–1 | QA PASS |
| Phase 2 | QA PASS |
| Phase 3 | QA PASS |
| Phase 4 | QA PASS |
| Phase 5 | QA PASS |
| Phase 6 | QA PASS |
| Phase 7 | PASS WITH CONDITIONAL RANKING |
| Phase 8 | QA PASS |
| Phase 9 | QA PASS |
| Phase 10 | QA PASS |
| Phase 11 | QA PASS |
| Phase 12 | QA PASS / CLOSED |
| Independent final audit | CORE PASS / activation QA pending |

Exact SHAs and continuation evidence remain in [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md), audit records and Git history.

## Active workstreams

### Pre-Physical Repository & Architecture Coherence

- **FINAL CLOSURE CANDIDATE**
- Branch: `chore/pre-physical-coherence`
- final remote activation QA pending
- `main` integration: **NOT PERFORMED**

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`

## Deferred production/model workstreams

### Physical Model

**NOT STARTED / NOT AUTHORIZED.** A separate explicit user authorization is required only after definitive Pre-Physical closure and later protected `main` integration.

### Backend Foundation

**NOT STARTED / DEFERRED.** Current handoff: [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md).

Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/Auth/provider/runtime implementation or persistence-specific bootstrap before accepted prerequisites exist.

## Documentation policy

```text
CURRENT SPECIFICATION = current truth
ADR = rationale + explicit supersession/qualification
HISTORICAL / VALIDATION EVIDENCE = truthful chronology
GIT / PR HISTORY = recoverable history
```

## Immediate next work

```text
FINAL PRE-PHYSICAL AUDIT ACTIVATION QA
remote compare + critical readback
```

If PASS, branch-local Pre-Physical Coherence becomes definitively closed. **Do not merge to `main` in this gate.** The later integration is a separate protected PR/merge/post-merge verification step.