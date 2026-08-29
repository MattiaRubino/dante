# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION
- **Last reconciled:** 2026-08-29

This file describes current architecture state directly. Phase-time reviews, old overlays and historical workstream evidence do not override this index.

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
Access/Auth M2 architecture freeze   CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED
Access/Auth M3 implementation        NEXT / NOT STARTED
Platform observability runtime       IMPLEMENTED ON INDEPENDENT BRANCH / FINAL GATES PENDING
```

Protected `main` remains integrated authority for closed shared foundations and CP6. Access/Auth M2 truth is current only on `feature/access-auth` until normal protected-main integration.

---

## 2. Current architecture entry points

Read according to subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical compatibility contract;
- [`observability-runtime-contract.md`](observability-runtime-contract.md) —
  backend/Web/PostgreSQL/Alloy/Grafana signal, privacy, cost and failure contract;
- [`access-auth-architecture.md`](access-auth-architecture.md) — Access/Auth identity/authenticator/session/Web-Native/transaction/generated-client architecture;
- [`access-auth-security-contract.md`](access-auth-security-contract.md) — Access/Auth session, CSRF/CORS, password, recovery, email, provider/passkey and transaction security contract;
- [`access-auth-api-contract.md`](access-auth-api-contract.md) — `/api/v1`, RFC 9457, naming, OpenAPI, Orval and first-party client contract;
- [`access-auth-testing-contract.md`](access-auth-testing-contract.md) — real PostgreSQL/API/browser/full-stack proof and CI contract;
- [`../domain/README.md`](../domain/README.md);
- [`../logical-model/README.md`](../logical-model/README.md);
- [`../physical-model/README.md`](../physical-model/README.md);
- [`../database/README.md`](../database/README.md);
- [`../decisions/`](../decisions/);
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md);
- [`frontend-engineering-foundation.md`](frontend-engineering-foundation.md) and accepted companions;
- [`../frontend/README.md`](../frontend/README.md).

Important persistence ADRs:

- [`../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`](../decisions/ADR-007-domain-model-informed-persistence-boundaries.md);
- [`../decisions/ADR-010-postgresql-persistence-constitution.md`](../decisions/ADR-010-postgresql-persistence-constitution.md);
- [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md) where historical PostgreSQL-selection rationale is explicitly relevant.

Important frontend ADRs:

- [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
- [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md).

Current Access/Auth ADR:

- [`../decisions/ADR-011-access-auth-architecture.md`](../decisions/ADR-011-access-auth-architecture.md) — accepted branch-local M2 constitution; not protected-main authority until integration.

---

## 3. Current system direction

DANTE is one product monorepo with accepted ownership for backend, web, mobile, packages, infrastructure/tooling, system tests, documentation, prototypes and GitHub automation. Paths are materialized when real content exists rather than created as empty architecture theatre.

Backend remains a capability-first modular monolith.

Canonical persistence:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority

current repository/runtime patch
= PostgreSQL 18.6
```

The accepted Domain → Logical → Physical chain is concretely materialized through CP6. Later product verticals consume that database constitution rather than reopening it for convenience.

Frontend remains platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Backend/database canonical authority and operation-specific offline governance remain preserved.

The Access/Auth branch adds the first complete post-CP6 product-vertical architecture. M2 is now closed and establishes the constitution under which M3 may materialize the first production Auth slice.

---

## 4. Domain / Logical invariants carried forward

Downstream implementation preserves at least:

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
method != factor != assurance
```

---

## 5. Frontend foundation direction

Accepted frontend foundation fixes, among other things:

- TypeScript/React/Vite/Expo/pnpm/Turbo baseline;
- feature-first Web/Mobile architecture;
- public-API-only and acyclic dependency direction;
- selective shared-package policy;
- Data Authority Matrix and feature data firewall;
- Mobile local/offline capability with backend-governed canonical effects;
- Web online-first posture;
- identity-scoped local data;
- design-token/UI/i18n/time/config boundaries;
- LOCAL/DEV/UAT/PROD environment vocabulary;
- GitHub Actions CI/CD authority.

M3 is the first real remote product-API trigger and must materialize the already-selected:

```text
FastAPI OpenAPI
→ Orval Fetch
→ @dante/api-client
→ Web application/data-source boundary
```

TanStack Query may activate for remote request/cache state but does not become canonical Auth state or replace the Access product/UI reducer.

---

## 6. Access/Auth M2 closed constitution

Accepted M2 subject owners:

```text
architecture/access-auth-architecture.md
architecture/access-auth-security-contract.md
architecture/access-auth-api-contract.md
architecture/access-auth-testing-contract.md
decisions/ADR-011-access-auth-architecture.md
```

M2 accepted:

```text
same-origin browser security boundary
opaque server-authoritative multi-session model
CSRF / Origin / Fetch Metadata / no broad CORS
Account / EmailIdentity / credential / Principal boundaries
password Argon2id + pepper + HIBP policy
recovery/revocation/account-disable lifecycle
passkey/MFA-ready architecture
email comparison/normalization policy
/api/v1 + RFC 9457 machine error contract
READ COMMITTED + targeted Account row locking
signin stale-credential/ambiguous-commit behavior
OpenAPI → Orval → framework-neutral generated client
TanStack Query application ownership boundary
real PostgreSQL/API/Chromium+Firefox+WebKit proof contract
```

M2 does not claim any production Auth table, endpoint, session or browser signin has been implemented. That proof begins in M3.

---

## 7. Current bounded deferrals

Still owned by later stages rather than guessed now:

- exact Auth SQL/table/index names and material shape, resolved slice-by-slice under M3+;
- exact operation-specific DB timeout values and KDF concurrency numbers after runtime benchmarking;
- exact native credential transport/secure-storage implementation, finalized in M6;
- exact provider protocol adapters and provider-specific callback details, finalized in M5 against then-current official mechanisms;
- exact passkey library/materialized credential columns where M5 evidence is required;
- future MFA/TOTP/recovery-code implementation;
- provider-data integrations such as Gmail/Calendar/iCloud authorization;
- third-party developer platform/public external SDK lifecycle unless product scope later requires it;
- cloud compute/IaC and remote infrastructure materialization;
- platform release/store activation details beyond current accepted target architecture.

A deferral never authorizes violating already accepted Domain/Logical/Physical/database/Access/Auth invariants.

---

## 8. Evidence vs current authority

Files such as:

```text
*-final-review.md
*-post-closure-qa.md
*-part-N.md transition continuations
phase audits / readiness records
workstream closure records
```

remain reference/evidence according to explicit lifecycle role and do not automatically override consolidated current contracts.

`workstreams/access-auth.md` remains the branch operational save-game. Durable M2 truth belongs in the four subject-oriented contracts + ADR-011.

---

## 9. Architecture reopen discipline

Closed Domain, Logical, Physical, Engineering, Frontend Foundation and Access/Auth M2 decisions are not casually reselected.

Implementation evidence first reopens the smallest affected technology/adapter/boundary. A wider reopen requires demonstrated contradiction that cannot be resolved locally.

Do not reopen architecture because of:

```text
ORM convenience
table-count preference
provider naming
UI naming
framework fashion
generator fashion
test-suite convenience
one isolated implementation annoyance
```

Reopen when accepted requirements, safety/privacy constraints, real runtime evidence or standards/provider incompatibility proves the boundary materially wrong.

---

## 10. Current next architecture posture

```text
DATABASE / CP6
CLOSED / INTEGRATED

ACCESS FRONTEND BASELINE
CLOSED / ACCEPTED

FULL ACCESS/AUTH VERTICAL
ACTIVE ON feature/access-auth

M2 AUTH ARCHITECTURE FREEZE
CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED

M3 EMAIL/PASSWORD SIGNIN + AUTHSESSION SPINE
NEXT / NOT STARTED
```

M3 production implementation begins only through a separate exact production-code write gate. Direct implementation evidence is claimed only after the relevant real artifact/scenario executes.
