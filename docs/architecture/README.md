# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-09-01

This file describes the current architecture state directly. Phase-time reviews, old branch overlays and pre-closure status remain evidence in their owning documents/Git history and do not override this index.

## 1. Current architecture state

```text
Domain Model                         CLOSED
Logical Model                        CLOSED / 57 OF 57 / REMOTE QA PASS
WD-03 / WD-05                        PASS
Pre-Physical coherence               CLOSED / FINAL QA PASS
Physical target                      CLOSED / ACCEPTED
Engineering Foundation               CLOSED / ACCEPTED
Frontend Engineering Foundation      CLOSED / INTEGRATED VIA PR #22
Frontend Materialization             CLOSED / PASS / INTEGRATED VIA PR #28
Backend CP1–CP5 scaffold             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
Backend CP6 PostgreSQL database       CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL architecture              18 major family / sole canonical persistence + material-history authority
Current PostgreSQL patch             18.6
Current Alembic head                 20260830_09
Current DB topology                  69 tables / 5 views / 15 routines / 76 triggers / 97 indexes / 69 FKs / 123 CHECKs
PostgreSQL local Recovery            CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
Full Access/Auth product vertical    ACTIVE / UNMERGED ON feature/access-auth
AI architecture                      ACTIVE / AI-02.1 v0.5 CANDIDATE STRUCTURAL FREEZE / DESIGN ONLY ON feature/ai-architecture
AI mega/pressure-test program        COMPLETE
AI targeted v0.5 verification        COMPLETE
AI-02.1 closure                      NOT YET / ADDITIONAL PRE-AI-03 REVIEW PENDING
```

Protected `main` is the integrated authority for closed shared foundations, CP6 and the integrated Recovery evolution. Active unmerged product/architecture work remains branch-local until normal protected-main integration.

## 2. Current architecture entry points

Read according to the subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`dante-ai-foundation.md`](dante-ai-foundation.md) — AI-00 semantic/architectural baseline; inherited constraints remain active and are not superseded by AI-02.1;
- [`ai-production-engineering-state-of-the-art-2026.md`](ai-production-engineering-state-of-the-art-2026.md) — production AI/agent engineering research thesis; state-of-the-art evidence and DANTE applicability boundaries, explicitly **not** the final DANTE Intelligence Architecture;
- [`dante-ai-02-1-intelligence-reengineering.md`](dante-ai-02-1-intelligence-reengineering.md) — **current active AI-02.1 architecture checkpoint**; v0.5 candidate structural freeze after all pressure/kill-test rounds and targeted consistency verification; **NOT CLOSED** pending the additional pre-AI-03 review;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical semantic compatibility contract;
- [`../domain/README.md`](../domain/README.md) — current Domain entry point;
- [`../logical-model/README.md`](../logical-model/README.md) — current Logical Model entry point and closure routing;
- [`../physical-model/README.md`](../physical-model/README.md) — accepted Physical Model target;
- [`../database/README.md`](../database/README.md) — current concrete PostgreSQL System of Record;
- [`../decisions/`](../decisions/) — ADR authority;
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md) — backend engineering foundation;
- [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md) and accepted companion/review records — frontend engineering foundation;
- [`../frontend/README.md`](../frontend/README.md) — current frontend documentation entry point.

Important persistence ADRs:

- [`../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`](../decisions/ADR-007-domain-model-informed-persistence-boundaries.md);
- [`../decisions/ADR-010-postgresql-persistence-constitution.md`](../decisions/ADR-010-postgresql-persistence-constitution.md);
- [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md) — historical PostgreSQL-selection rationale where explicitly historical.

Important frontend ADRs:

- [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
- [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md).

## 3. Current system direction

DANTE remains one product monorepo. The backend remains a capability-first modular monolith. Responsibility boundaries are not automatically deployable services.

Canonical persistence direction:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current repository/runtime patch
= PostgreSQL 18.6

current Alembic head
= 20260830_09
```

The accepted Domain → Logical → Physical chain has already been concretely materialized through CP6 and the bounded Recovery lifecycle evolution. Later backend/product/AI work consumes that database rather than reopening the architecture because a feature/framework/provider prefers a different shape.

AI architecture inherits the same rule: model/provider/runtime output is not accepted canonical effect, and no AI-specific persistence shortcut may redefine closed Domain/Logical/Physical/database semantics.

## 4. AI authority layering

Current branch-local AI authority is deliberately layered:

```text
AI-00
DANTE AI Foundation
→ inherited / derived semantic guardrails

Production AI / Agent Engineering Research
→ technology landscape / engineering evidence
→ NON-DANTE-DECISION

AI-02.1
DANTE Intelligence Reengineering
→ current structural responsibility architecture
→ v0.5 CANDIDATE STRUCTURAL FREEZE
```

AI-02.1 does not normatively rewrite AI-00. AI-00's original sequencing toward AI-01 is historical workstream chronology; later product-form/research/reengineering work has already superseded that scheduling note.

## 5. AI-02.1 v0.5 structural model

The completed test program converged on the following responsibilities.

### Interaction / work

```text
Interaction Edge
Interaction Session
Work Intake
WorkContract
Work lineage / continuation / supersession
ConsequenceProfile
Reference / Target Resolution
```

`Interaction Session != Run != Worker`.

`WorkContract` preserves the authoritative execution meaning across decomposition and child Runs:

```text
objective
scope
resolved target bindings
protected constraints
purpose
consequence/governance obligations
approval conditions
```

Derived work may refine this contract but must not silently drop a protected requirement. A material relaxation requires a new/superseding decision.

### State / context / scenarios

```text
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
```

Semantic Query and Context are distinct. Structured DANTE-native state is accessed through application-owned semantic query/projection contracts; arbitrary unstructured/external/contextual material is assembled by the Context Engine.

Scenario Workspace is hypothetical/derived and does not create a second canonical reality.

`BasisManifest` tracks relevant dependencies, source identity/version, temporal validity, assumptions and constraints. It also captures **Basis coherence**: independently fresh values are not automatically one coherent world-state.

### Reasoning / capabilities

```text
ModelTarget + HarnessProfile
Deterministic Compute
Solver
Capability Runtime
Verifier
Execution Environment
```

A simple deterministic request must stay on the cheap path and may use no model and no isolated environment.

`Execution Environment` is a runtime/security responsibility for workloads whose threat model requires isolation, such as generated code, hostile executable artifacts, browser/computer-use or comparable workloads.

```text
Execution Environment != mandatory sandbox/container
```

Isolation is selected lazily by workload and may use different techniques. Generated/untrusted code does not receive raw privileged DANTE/provider/database credentials; privileged operations flow through bounded trusted capabilities/brokers.

### Governance / effects

```text
Policy Composition / policy mesh
Authority / AuthZ / Consent / Visibility
Autonomy
ConsequenceProfile
ChangeSet / EffectGraph
Effect Runtime
Approval binding
Verification / Reconciliation
```

Policy is not one model-chosen linear verdict. Enforcement may occur at context, capability, effect and publication/egress boundaries.

Approval binds to the materially approved target/proposal/basis/effect semantics. A materially changed ChangeSet cannot silently reuse an old approval.

`ChangeSet / EffectGraph` coordinates compound change but does not bypass individual governed effects.

`CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS`.

Resource exhaustion may stop optional work but must not erase a reconciliation obligation created by an already-dispatched ambiguous effect.

### Publication / privacy / attention

```text
Context Projection
Disclosure Projection
cumulative inference protection
Safe Result Publication
Result Maturity
publication currentness
Attention + Attention budgeting
causal-loop / oscillation guard
```

```text
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SAFE SINGLE DISCLOSURE != AUTOMATICALLY SAFE CUMULATIVE DISCLOSURE
```

Safe Publication rechecks recipient/surface eligibility, result maturity and work currentness. A superseded/stale Run may reconcile old work but must not continue presenting obsolete output as the current result.

Disclosure is surface-aware: lock screen, voice/realtime, shared UI and another recipient may require different safe representations.

Attention is a scarce resource and may aggregate/suppress individually relevant signals.

### External AI / agents

DANTE supports both directions conceptually:

```text
AI inside DANTE
DANTE exposed to external AI/agent clients
```

External protocol adapters such as MCP/A2A remain edge adapters, not internal Domain ontology.

A delegated external intelligent system may perform consequential effects only when either:

```text
1. the effect returns through governed DANTE capabilities
or
2. it is honestly treated as an externally performed effect whose outcome must be observed/reconciled
```

DANTE must not falsely claim its own governance for a side effect performed outside that boundary.

## 6. Non-negotiable AI invariants

```text
DANTE != chatbot/model/provider/thread
MODEL != canonical truth
MODEL != authorization engine
MODEL != policy-precedence authority
MODEL != effect success
PostgreSQL = sole canonical persistence/material-history authority
AI inference != confirmed fact
AI confidence != Confirmation
provider state != canonical DANTE state
DISPLAY NAME != EFFECT TARGET
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
SCENARIO STATE != CANONICAL CURRENT STATE
CONTEXT ACCESS != DISCLOSURE PERMISSION
INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
DANTE REPRESENTATION != EXTERNAL SYSTEM-OF-RECORD AUTHORITY
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
TELEMETRY/EVAL PIPELINE != PRIVILEGED DATA SINK
```

## 7. Pressure-test acceptance state

```text
Round I                         COMPLETE
Round II                        COMPLETE
Final Kill-Test                 COMPLETE
Last Mega Stress-Test           COMPLETE
Targeted v0.5 verification      COMPLETE
Additional mega-test cycles     NONE
```

Targeted v0.5 structural checks:

```text
generated-code secret isolation                         PASS
environment crash vs Run durability                     PASS
browser/computer-use effect verification                PASS
superseded publication                                  PASS
Basis coherence                                         PASS
approval rebinding                                      PASS
external-agent side effects                             PASS
resource exhaustion after ambiguous effect              PASS
deterministic fast path bypassing unnecessary isolation PASS
```

The completed tests produced no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

The future-extensibility structural criterion also passes: future substantially stronger general-purpose conversational intelligence can be added without transferring canonical memory, Authority, application state, Domain semantics or effect ownership to the provider/model.

## 8. Current bounded deferrals

Still open or trigger-bound:

- exact AI model/provider set and routing policy;
- AI agent/runtime/SDK implementation;
- exact policy-engine technology;
- exact Execution Environment/sandbox technology;
- exact target-resolution implementation;
- exact safe-streaming/publication implementation;
- exact Scenario Workspace representation;
- exact ChangeSet physical persistence, if any;
- exact Interaction Session persistence, if any;
- exact Context / Retrieval / Memory architecture — AI-03;
- conversation history persistence;
- embeddings/index lifecycle;
- optional local-model choice/activation;
- provider-specific commercial/cost selections;
- cloud compute/IaC and production infrastructure activation.

A deferral does not authorize violating already accepted semantic/runtime invariants.

## 9. Architecture reopen discipline

Closed Domain, Logical, Physical, Engineering and Frontend Foundation decisions are not casually reselected.

Implementation evidence first reopens the smallest affected technology/adapter/boundary. A wider architectural reopen requires a demonstrated contradiction that cannot be resolved locally.

Do not reopen architecture because of ORM convenience, table shape preference, provider naming, UI naming, framework fashion, agent-framework conventions, vector-store convenience or one isolated implementation annoyance.

## 10. Current next architecture posture

```text
DATABASE / CP6 + RECOVERY EVOLUTION
CLOSED / INTEGRATED

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE ON feature/access-auth / UNMERGED

AI ARCHITECTURE
ACTIVE ON feature/ai-architecture
DESIGN / REENGINEERING ONLY

AI-02.1
v0.5 CANDIDATE STRUCTURAL FREEZE
ALL PRESSURE/MEGA TESTS COMPLETE
TARGETED v0.5 VERIFICATION COMPLETE
NO MORE MEGA TESTS
NOT CLOSED
ADDITIONAL PRE-AI-03 REVIEW PENDING

THEN, ONLY AFTER EXPLICIT AI-02.1 ACCEPTANCE:
AI-03 CONTEXT / RETRIEVAL / MEMORY
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.
