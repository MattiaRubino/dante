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
AI architecture                      ACTIVE / AI-02.1 v0.4 REENGINEERING / DESIGN ONLY ON feature/ai-architecture
```

Protected `main` is the integrated authority for closed shared foundations, CP6 and the integrated Recovery evolution. Active unmerged product/architecture work remains branch-local until normal protected-main integration.

## 2. Current architecture entry points

Read according to the subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`dante-ai-foundation.md`](dante-ai-foundation.md) — branch-local AI-00 semantic/architectural baseline; inherited constraints remain active and are not superseded by AI-02.1;
- [`ai-production-engineering-state-of-the-art-2026.md`](ai-production-engineering-state-of-the-art-2026.md) — branch-local production AI/agent engineering research thesis; state-of-the-art evidence and DANTE applicability boundaries, explicitly **not** the final DANTE Intelligence Architecture;
- [`dante-ai-02-1-intelligence-reengineering.md`](dante-ai-02-1-intelligence-reengineering.md) — **current active AI-02.1 architecture checkpoint**; v0.4 after Round I, Round II and the broad Final Kill-Test, explicitly **NOT CLOSED** with one last mega stress-test still required;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical semantic compatibility contract;
- [`../domain/README.md`](../domain/README.md) — current Domain entry point;
- [`../logical-model/README.md`](../logical-model/README.md) — current Logical Model entry point and closure routing;
- [`../physical-model/README.md`](../physical-model/README.md) — accepted Physical Model target;
- [`../database/README.md`](../database/README.md) — current concrete PostgreSQL System of Record;
- [`../decisions/`](../decisions/) — ADR authority;
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md) — backend engineering foundation;
- [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md) and its accepted companion/review records — frontend engineering foundation;
- [`../frontend/README.md`](../frontend/README.md) — current frontend documentation entry point.

Important persistence ADRs:

- [`../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`](../decisions/ADR-007-domain-model-informed-persistence-boundaries.md) — semantic persistence guardrails;
- [`../decisions/ADR-010-postgresql-persistence-constitution.md`](../decisions/ADR-010-postgresql-persistence-constitution.md) — accepted reusable PostgreSQL persistence doctrine;
- [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md) — historical PostgreSQL-selection rationale where explicitly historical.

Important frontend ADRs:

- [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
- [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md).

## 3. Current system direction

DANTE is one product monorepo with accepted ownership for backend, web, mobile, packages, infrastructure/tooling, system tests, documentation, prototypes and GitHub automation. Paths are materialized when real content exists rather than created as empty architecture theatre.

The backend remains a capability-first modular monolith.

Canonical persistence direction:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current repository/runtime patch
= PostgreSQL 18.6

current Alembic head
= 20260830_09
```

The accepted Domain → Logical → Physical chain has already been concretely materialized through CP6 and the bounded Recovery lifecycle evolution. Later backend/product/AI work consumes that database rather than reopening the architecture merely because a new feature or AI framework is implemented.

Frontend remains platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Backend/database canonical authority and operation-specific offline governance remain preserved.

AI architecture consumes the same rule: model/provider/runtime output is not accepted canonical effect, and no AI-specific persistence shortcut may redefine closed Domain/Logical/Physical/database semantics.

AI-02.1 pressure-tests the intelligence architecture against actual DANTE obligations rather than against one preferred AI technology. Round I produced first-class responsibility boundaries for Interaction Session, Semantic Query / Projection, hypothetical Scenario Workspace, compound ChangeSet / EffectGraph, verification, proactivity/attention, recipient-aware Disclosure Projection and mixed DANTE-native/open-world reasoning.

Round II hardened that model with:

```text
cumulative / cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest + dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo already-dispatched effects
```

The broad Final Kill-Test then attacked v0.3 across agriculture, education, shift work, caregiving, legal/sensitive work, family, business, public/institutional boundaries, offline operation, high fan-out and future rich conversational surfaces. The current v0.4 additionally requires:

```text
Reference / Target Resolution Gate
Policy Composition / Precedence
ConsequenceProfile
Safe Result Publication / Streaming Gate
BasisManifest temporal validity
DANTE representation != external institutional System-of-Record authority
sent != delivered != seen != acknowledged != accepted
```

These are responsibility/runtime contracts, not automatic services, new Domain owners or persistence tables. Three completed pressure-test rounds have not produced evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

The production-engineering research additionally records a current DANTE applicability boundary without selecting a provider or SDK: frontier intelligence is expected to be **API-first**; DANTE does not plan to train a foundation model, require fine-tuning as a baseline, own a frontier model or operate a large always-on self-hosted model fleet. Small/local inference remains optional and benchmark-gated. These are project constraints for later architecture work, not implementation claims.

## 4. Domain / Logical invariants carried into implementation

Downstream implementation must continue to preserve at least:

```text
no universal Entity / Thing ontology
no generic Relation as semantic escape hatch
no untyped property bag as canonical semantic truth
provider IDs != DANTE canonical identity

Person != Account != Actor
Person != Living Referent != Asset
Subject / Resource contextual roles != native identity
Possibility != Goal / Proposal / Decision / Plan
Schedule != Actual
Actual != Observation
Evidence != Provenance
Authority != Visibility
Responsibility != Participation
Ownership != Possession

shared canonical reality + actor-scoped overlays where required
material history reconstructible where consequential
specialist Transaction / Movement lifecycle != Observation
AI/solver/provider output != accepted canonical effect
```

Logical hardenings `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded by later accepted authority.

AI-02.1 additionally requires that display names/model guesses do not become consequential target identity, conflicting policies are composed outside model improvisation, and model output/streaming does not bypass disclosure or verification.

## 5. Frontend foundation direction

The accepted frontend foundation fixes, among other things:

- TypeScript/React/Vite/Expo/pnpm/Turbo baseline;
- feature-first Web/Mobile architecture;
- public-API-only and acyclic dependency direction;
- selective shared-package policy;
- Data Authority Matrix and feature data firewall;
- mobile local/offline capability with backend-governed canonical effects;
- Web online-first posture;
- identity-scoped local data;
- design-token/UI/i18n/time/config boundaries;
- LOCAL/DEV/UAT/PROD environment vocabulary;
- GitHub Actions CI/CD authority.

Foundation/materialization is closed and integrated. Product vertical work such as Access remains separately scoped until its own full-stack/release gates close.

## 6. Current bounded deferrals

Architecture is closed where evidence was sufficient, but not every future product choice is pre-decided.

Still bounded to the stage that owns them:

- exact product APIs/routes/versioning for future verticals;
- specific AuthN/AuthZ application protocol beyond already accepted persistence/security doctrine;
- provider adapters and specialist modules activated only by real need;
- cloud compute/IaC and remote infrastructure materialization;
- platform release activation details;
- dormant frontend capabilities activated only when product requirements justify them;
- exact final AI chat/voice/UI interaction design, while Interaction Session and safe publication are AI-02.1 responsibilities;
- exact AI model/provider strategy and routing policy;
- AI agent/runtime/SDK selection;
- AI conversation/memory physical persistence;
- AI tool/capability registry implementation, autonomy policy implementation and evaluation stack;
- optional local-model choice and activation;
- exact Context / Retrieval / Memory architecture owned by the later AI-03 phase;
- exact implementation for target resolution, policy composition, consequence profiling and safe streaming;
- exact physical representation, if any, for AI-02.1 runtime-only responsibilities such as Scenario Workspace, ChangeSet, BasisManifest, work lineage and bounded disclosure accounting.

The branch-local AI authority is layered: [`dante-ai-foundation.md`](dante-ai-foundation.md) owns inherited semantic constraints; [`ai-production-engineering-state-of-the-art-2026.md`](ai-production-engineering-state-of-the-art-2026.md) owns external engineering evidence/applicability boundaries; [`dante-ai-02-1-intelligence-reengineering.md`](dante-ai-02-1-intelligence-reengineering.md) owns the current active reengineering checkpoint. None authorizes backend/database implementation merely by documentation.

A deferral does not authorize violating already accepted Domain/Logical/Physical/database invariants.

## 7. Evidence vs current authority

The following kinds of files may remain useful but are not current-status authorities merely because they were written later in a phase:

```text
*-final-review.md
*-post-closure-qa.md
*-part-N.md transition continuations
phase audits / readiness records
workstream closure records
```

Use them as reference/evidence according to their explicit role.

For example, `domain-model-logical-readiness-part-2.md` through `part-5.md` are transition/closure evidence; the consolidated [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) now states the current satisfied contract directly.

The production AI/agent engineering thesis is intentionally research evidence. It may classify technologies as strong defaults, challengers, watch items or anti-defaults without converting those classifications into DANTE implementation decisions.

The AI-02.1 checkpoint is branch-local architectural work, but it remains **ACTIVE / NOT CLOSED**. Round I, Round II and the broad Final Kill-Test are complete; one last mega stress-test and the other explicitly required pre-AI-03 acceptance work are still pending. Do not read `v0.4` as implementation status or final architecture closure.

## 8. Architecture reopen discipline

Closed Domain, Logical, Physical, Engineering and Frontend Foundation decisions are not casually reselected.

Implementation evidence first reopens the smallest affected technology/adapter/boundary. A wider architectural reopen requires a demonstrated contradiction that cannot be resolved locally.

Do not reopen architecture because of:

```text
ORM convenience
table shape preference
provider naming
UI naming
framework fashion
agent-framework conventions
vector-store convenience
one isolated implementation annoyance
```

Reopen when accepted requirements, safety/privacy constraints, real runtime evidence or incompatibility with a current invariant proves that the existing boundary is materially wrong.

New research technologies such as an alternative durable runtime, relationship-authorization engine, sandbox implementation, model router or inference server remain challengers until a real DANTE requirement and direct evidence justify the smallest relevant reopen.

## 9. Current next architecture posture

There is no pending CP6 architecture gate.

```text
DATABASE / CP6 + RECOVERY EVOLUTION
CLOSED / INTEGRATED

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE ON feature/access-auth
UNMERGED

AI ARCHITECTURE
ACTIVE ON feature/ai-architecture
DESIGN / REENGINEERING ONLY
NO BACKEND / DB / PROVIDER IMPLEMENTATION CLAIMED

AI-00
SEMANTIC / ARCHITECTURAL FOUNDATION RECORDED

PRODUCTION AI / AGENT ENGINEERING RESEARCH
STATE-OF-THE-ART EVIDENCE RECORDED
NON-DANTE-DECISION

AI-02.1
ACTIVE / REENGINEERED TO v0.4
ROUND I COMPLETE
ROUND II COMPLETE
FINAL KILL-TEST COMPLETE
ONE LAST MEGA STRESS-TEST REQUIRED
NOT CLOSED

THEN: AI-03
CONTEXT / RETRIEVAL / MEMORY
BLOCKED UNTIL AI-02.1 STRUCTURAL ACCEPTANCE
```

AI-02.1 starts from what DANTE must actually be able to do: Product/North Star, existing simulations and adversarial scenarios, accepted Domain/Logical/Physical/database authority, AI-00 and external engineering evidence. The completed rounds identified bounded architecture gaps and responsibility-level fixes without creating a parallel ontology or automatic new infrastructure.

A specific AI-02.1 acceptance question is future extensibility: if DANTE later exposes a much richer integrated general-purpose conversational intelligence, realtime voice/multimodal surface or consumes future frontier models/providers with substantially better capabilities, the architecture must absorb them without transferring canonical memory, Authority, application truth or effect ownership to the model/provider, without bypassing safe publication, and without requiring a fundamental redesign.

AI-03 follows only after the one last mega stress-test and other required pre-AI-03 review. It owns detailed Context / Retrieval / Memory rather than having those choices pre-committed by the current checkpoint.

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.
