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
READ-ONLY AUDIT NEXT
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

## Pre-Physical sequence

1. **Phase 0 — freeze/current-state inventory** — PASS.
2. **Phase 1 — global entry-point/current-truth alignment** — QA PASS.
3. **Phase 2 — architecture supersession/current-truth cleanup** — QA PASS.
4. **Phase 3 — Backend Foundation handoff cleanup** — read-only audit next, then separate exact write gate.
5. **Phase 4 — current Pre-Physical Architecture Baseline**.
6. **Phase 5 — requirements that can constrain Physical design**:
   - AuthN/AuthZ;
   - security/privacy/retention/recovery;
   - transaction/consistency/outbox/side effects;
   - non-functional/multi-device/recovery envelope.
7. **Phase 6 — AI/context/runtime/integration boundaries**.
8. **Phase 7 — durable workflow / async benchmark**.
9. **Phase 8 — governed API/command/effect contract**.
10. **Phase 9 — search/observability/calendar/solver pressure tests**.
11. **Phase 10 — Physical benchmark specification/register**.
12. **Phase 11 — repository engineering safety alignment**.
13. **Phase 12 — clean-room repository/architecture coherence QA and closure**.
14. **Separate user gate** — decide whether to authorize a Physical Model workstream.

## Current architecture sources

Current navigation:

- [`architecture/README.md`](architecture/README.md)
- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

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

## Phase 3 — Backend Foundation handoff cleanup

Next action is a **read-only audit** of `docs/workstreams/backend-foundation.md` against the current closed Domain + Logical models and the current architecture sources.

Only after that inventory may a separate exact Phase 3 write gate be proposed.

Backend Foundation must eventually consume:

```text
CLOSED Domain Atlas
+
CLOSED Logical Model
+
future accepted Physical Model
+
current architecture/runtime/security/integration contracts
```

It must not instruct contributors to create Domain Model v0 inside backend bootstrap or treat old persistence assumptions as current truth.

## Phase 4 — current Pre-Physical Architecture Baseline

Create one current bridge source stating:

- what is decided;
- what is semantically prohibited;
- what remains open;
- which `WL-H01..WL-H12` constraints are mandatory;
- what is runtime/backend rather than Domain;
- what must be benchmarked during Physical design.

## Phase 5 — requirements before Physical

Define requirements, not implementation, for:

### AuthN/AuthZ

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

Include represented party, session/device/service/external-agent context and reconstructible consequential AuthZ provenance.

### Security/privacy/retention/recovery

Data classification, sensitive-data handling, encryption/key/secret boundaries, isolation, retention/redaction/deletion propagation, audit/log minimization, backup/recovery and AI/provider minimization.

### Transaction/consistency/side effects

Expected state, transaction boundaries, idempotency, outbox/publication pressure, external acknowledgement, staged partial state, reconciliation/compensation and derived-state freshness.

### Non-functional/multi-device/recovery

Scale/concurrency assumptions, material latency classes, long-term history, multi-device conflicts, online/offline posture and RPO/RTO/restore expectations.

## Phase 6 — AI/runtime/integration boundaries

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

Runtime concepts such as Agent/Workflow/Automation/Notification remain technical/product concepts unless separate semantic evidence proves otherwise.

Integration modes:

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
- schema evolution over historical state.

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

Backend Foundation and production implementation are **NOT STARTED**.

Only after accepted prerequisites should implementation proceed through bounded vertical slices derived from Domain + Logical + Physical/current runtime contracts rather than old product-label schemas.

## Explicitly rejected/deferred by default

Do not introduce by default:

- permanent dev/uat/prod Git branches;
- microservices/Kubernetes by fashion;
- document/graph/meta-model storage as universal canonical kernel;
- generic EAV/generic-edge ontology;
- specialized search/cache/vector/analytics/workflow infrastructure without demonstrated benefit;
- implicit collaboration/social implementation inside personal-first V1.

Specialized infrastructure may be justified by measured workload **or** strong structural benefit in correctness/durability/security/evolvability/operations/migration risk.
