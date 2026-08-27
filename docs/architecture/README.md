# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-08-27

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
Current Alembic head                 20260826_08
Current DB topology                  68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs
Access frontend baseline             CLOSED / ACCEPTED / RELEASE-HARDENED
Full Access/Auth vertical            ACTIVE / UNMERGED ON feature/access-auth
Access/Auth M2 architecture freeze   ACTIVE / M2.1–M2.8 ACCEPTED
```

Protected `main` is the integrated authority for closed shared foundations and CP6. Active unmerged product work remains branch-local until normal protected-main integration.

## 2. Current architecture entry points

Read according to the subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical semantic compatibility contract;
- [`access-auth-architecture.md`](access-auth-architecture.md) — current branch-local Access/Auth identity/authenticator/session/Web-Native architecture for accepted M2.1–M2.8 decisions;
- [`access-auth-security-contract.md`](access-auth-security-contract.md) — current branch-local Access/Auth security contract for session, CSRF/CORS, password, email, recovery and passkey-ready behavior;
- [`access-auth-api-contract.md`](access-auth-api-contract.md) — current branch-local `/api/v1` / RFC 9457 / machine-error / naming contract;
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

Current Access/Auth ADR:

- [`../decisions/ADR-011-access-auth-architecture.md`](../decisions/ADR-011-access-auth-architecture.md) — accepted branch-local Access/Auth architecture constitution for M2.1–M2.8; not protected-main authority until integration.

## 3. Current system direction

DANTE is one product monorepo with accepted ownership for backend, web, mobile, packages, infrastructure/tooling, system tests, documentation, prototypes and GitHub automation. Paths are materialized when real content exists rather than created as empty architecture theatre.

The backend remains a capability-first modular monolith.

Canonical persistence direction:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current repository/runtime patch
= PostgreSQL 18.6
```

The accepted Domain → Logical → Physical chain has already been concretely materialized through CP6. Later backend/product work consumes that database rather than reopening the architecture merely because a new feature is implemented.

Frontend remains platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Backend/database canonical authority and operation-specific offline governance remain preserved.

The active Access/Auth branch adds a branch-local current architecture for the first complete post-CP6 product vertical. Its accepted M2.1–M2.8 rules consume rather than replace the existing DANTE semantic, persistence and frontend constitutions.

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
```

Logical hardenings `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded by later accepted authority.

Access/Auth additionally preserves:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
provider identity != provider email
signin != provider-data integration authorization
client/device signal != identity
```

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

Foundation/materialization is closed and integrated. The active Access/Auth vertical consumes that foundation and must preserve the frontend application/data-source/generated-client boundary; it does not authorize provider/server success to be faked locally.

## 6. Current bounded deferrals

Architecture is closed where evidence was sufficient, but not every future product choice is pre-decided.

Still bounded to the stage that owns them:

- M2.9 exact M3 transaction/concurrency/session-expiry contract;
- M2.10 exact OpenAPI → generated TypeScript client → Web application boundary/tooling;
- M2.11 exact M3 test matrix/full-stack harness;
- exact Auth SQL/table names and material persistence shape, resolved slice-by-slice;
- exact native credential transport, finalized in M6 under the canonical AuthSession semantics;
- exact provider/passkey implementation details owned by M5 where not already fixed as architecture/security principles;
- provider adapters and specialist modules activated only by real need;
- cloud compute/IaC and remote infrastructure materialization;
- platform release activation details;
- dormant frontend capabilities activated only when product requirements justify them.

A deferral does not authorize violating already accepted Domain/Logical/Physical/database or branch-local Access/Auth invariants.

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

The active `workstreams/access-auth.md` remains the branch operational save-game. Durable accepted M2.1–M2.8 architecture/security/API truth now lives in the subject-oriented Access/Auth architecture contracts and ADR-011 instead of depending on chat chronology.

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
one isolated implementation annoyance
```

Reopen when accepted requirements, safety/privacy constraints, real runtime evidence or incompatibility with a current invariant proves that the existing boundary is materially wrong.

The same smallest-reopen rule applies to accepted Access/Auth M2 decisions. Another product's undocumented internals or a desire for fewer tables is not reopen evidence.

## 9. Current next architecture posture

There is no pending CP6 architecture gate.

```text
DATABASE / CP6
CLOSED / INTEGRATED

ACCESS FRONTEND BASELINE
CLOSED / ACCEPTED

FULL ACCESS/AUTH VERTICAL
ACTIVE ON feature/access-auth

M2 AUTH ARCHITECTURE FREEZE
M2.1–M2.8 ACCEPTED
M2.9–M2.11 OPEN
NO PRODUCTION AUTH CODE YET
```

Direct implementation evidence is claimed only after the relevant real artifact/scenario executes. M3 production implementation begins only after M2 closure and a separate explicit write gate.