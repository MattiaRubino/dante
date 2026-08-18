# Project Status

- Last updated: 2026-08-18
- Canonical integrated branch: `main`
- Accepted `main` baseline for the closed Pre-Physical workstream: `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Closed branch-local Pre-Physical state: `chore/pre-physical-coherence`
- Production application code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Main integration of Pre-Physical branch: **PENDING / NOT PERFORMED**

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
DEFINITIVE CLOSED / FINAL QA PASS on chore/pre-physical-coherence
Phase 0–11 QA PASS
Phase 12 QA PASS / CLOSED
Independent total audit PASS
activation checkpoint 9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d

PHYSICAL READINESS
ESTABLISHED

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED

MAIN INTEGRATION
PENDING / NOT PERFORMED
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

## Accepted/current foundations

- Product/North Star — **CURRENT**.
- Core Domain Model / Domain Atlas — **CLOSED**.
- Logical Model — **CLOSED**; `WL-H01..WL-H12` active downstream.
- Pre-Physical Architecture Baseline — **CURRENT / CLOSED workstream result**.
- Phase 5 requirements — **CURRENT**.
- Phase 6 AI/context/runtime + Integration Hub boundaries — **CURRENT**.
- Phase 7 durable execution — **CURRENT / conditional ranking only**.
- Phase 8 governed operation/effect — **CURRENT**.
- Phase 9 search/observability/calendar/solver — **CURRENT**.
- Phase 10 benchmark method — **CURRENT / QA PASS**.
- Phase 11 repository engineering safety — **QA PASS**.
- Phase 12 clean-room QA — **QA PASS / CLOSED**.
- Independent total Pre-Physical audit — **PASS**.
- Web direction — Next.js + React + TypeScript.
- Mobile direction — Expo + React Native + TypeScript.
- Backend direction — Python + FastAPI + Pydantic; modular monolith.
- SQLAlchemy/Alembic — conditional on accepted Physical persistence.

## Domain / Logical closure

```text
DOMAIN
PASS WITH HARDENING
POST-WRITE QA PASS
CLOSED

LOGICAL
PASS WITH HARDENING
REMOTE QA PASS
CLOSED
WD-03 PASS
WD-05 PASS
```

The Pre-Physical workstream made no Domain/Logical semantic edits. Any future semantic contradiction requires a separate explicit reopen scope.

## Current Phase 5–10 posture

### Requirements

AuthN/AuthZ, security/privacy/retention/security-aware recovery, consistency/side effects and non-functional/multi-device/operational recovery remain the four current Phase 5 owners. Open RPO/RTO/latency/availability/scale/offline values remain explicit until later accepted where material.

Phase 10 already defines how those requirements pressure-test Physical candidates. The later separately authorized Physical Model performs actual candidate execution/design/selection.

### AI / context / integration

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Generic AI memory is not a second canonical truth store. Runtime Agent/Principal != Domain Actor automatically; tool invocation != authorization/effect.

Material consequential AI changes require versioned/reproducible evaluation before promotion.

```text
eval result != canonical LifeOS truth
eval PASS != Authority / governed-effect authorization
```

Integration Hub preserves canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration. `ExternalRef != NativeRef`; provider revision != `MaterialStateRef`; provider state/effect != canonical state/effect automatically.

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
structured + lexical/full-text baseline
semantic/vector bounded candidate

OBSERVABILITY
OpenTelemetry-first / equivalent direction
no vendor selected

CALENDAR
iCalendar / JSCalendar / provider APIs = adapter pressure, not ontology

SOLVER
simple deterministic rules/heuristics baseline
OR-Tools CP-SAT preferred benchmark candidate — NOT implemented
```

### Physical benchmark method

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector

EVENT / DOCUMENT
bounded mechanisms first; specialized candidate only on demonstrated gap/benefit
```

Hard correctness gates precede weighted scoring. LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts. Unexecuted tiers remain unverified. `PREFERRED != SELECTED`.

## Repository safety

`lifeos-main-safety` was remotely verified during Phase 11. Current owner-driven `main` policy requires PR integration, blocks deletion/force-push, requires review-thread resolution, uses zero required approvals while no independent reviewer exists and has no required CI checks until real stable contexts exist. Auto-delete merged head branches is enabled.

Current `main` was re-read during final activation and remained `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0` and protected.

## Phase 12 + independent final audit

Phase 12 clean-room QA is **QA PASS / CLOSED**.

The independent total audit then checked the full branch delta and independently confirmed:

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

Bounded repairs addressed stale current-stage prose, Phase10-method-vs-Physical-execution wording, repository bootstrap/hygiene, DBOS coupling precision, explicit consequential AI evaluation and honest treatment of unexecuted upper benchmark envelopes.

The activation checkpoint `9c53e812d13ffd1b3d3d3dc20b8b162799e13c1d` proved:

```text
PRE-SCOPE     1bd142afe51221211bc777f6271a642911c650fc
unique paths  23
added          1
modified      22
deleted        0
unexpected     0
behind_by      0
main unchanged
critical readback PASS
```

Therefore branch-local Pre-Physical Coherence is definitively closed.

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
| Independent final audit | PASS |
| Branch-local Pre-Physical closure | DEFINITIVE CLOSED / FINAL QA PASS |

Exact SHAs/evidence remain in [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md), the audit records and Git history.

## Active / pending workstreams

### Pre-Physical Repository & Architecture Coherence

- **DEFINITIVE CLOSED / FINAL QA PASS on branch**
- Branch: `chore/pre-physical-coherence`
- `main` integration: **PENDING / NOT PERFORMED**

### Phase 4 — Home / Today UX

- **IN PROGRESS — separate product/design workstream**
- Branch: `prototype/phase-4-today-home`

### Physical Model

**READY FOR SEPARATE AUTHORIZATION BUT NOT STARTED.** Do not begin until the user separately authorizes it after Pre-Physical `main` integration/post-merge verification.

### Backend Foundation

**NOT STARTED / DEFERRED.** Do not create `feature/backend-foundation`, SQL/schema/migrations, concrete API/Auth/provider/runtime implementation or persistence-specific bootstrap before all accepted prerequisites exist.

## Immediate next work

```text
PRE-PHYSICAL MAIN INTEGRATION
PENDING / NOT PERFORMED
```

Only after separate user authorization:

```text
protected PR to main
→ merge commit
→ post-merge main verification
```

Physical Model authorization remains a further separate decision after that integration.