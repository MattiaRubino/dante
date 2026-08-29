# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION FOR `feature/access-auth`
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
Protected-main Alembic baseline      20260826_08
Protected-main DB topology           68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs
Access/Auth branch Alembic head      20260829_11
Access/Auth branch DB topology       74 tables / 5 views / 15 routines / 75 triggers / 113 indexes / 72 FKs / 149 CHECKs
Access frontend baseline             CLOSED / ACCEPTED / RELEASE-HARDENED
Full Access/Auth vertical            ACTIVE / UNMERGED ON feature/access-auth
Access/Auth M2 architecture freeze   CLOSED / ACCEPTED
Access/Auth M3 implementation        CLOSED / ENGINEERING PASS / USER ACCEPTED
Access/Auth M4 lifecycle             CLOSED / ENGINEERING PASS / USER ACCEPTED
Access/Auth M5                       ACTIVE
Access/Auth M5.1 architecture freeze COMPLETE
Access/Auth M5.2                     NEXT / EXACT PERSISTENCE + API DESIGN
```

Protected `main` remains integrated authority for closed shared foundations. Newer Access/Auth truth is branch-local on `feature/access-auth` until normal protected-main integration.

---

## 2. Current architecture entry points

Read according to subject:

- [`system-overview.md`](system-overview.md) — system/component/authority overview;
- [`technical-decisions.md`](technical-decisions.md) — current architecture decision register;
- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md) — satisfied Domain → Logical compatibility contract;
- [`access-auth-architecture.md`](access-auth-architecture.md) — durable Access/Auth identity/authenticator/session/Web-Native architecture;
- [`access-auth-security-contract.md`](access-auth-security-contract.md) — session, CSRF/CORS, password, email, provider/passkey and transaction security;
- [`access-auth-api-contract.md`](access-auth-api-contract.md) — `/api/v1`, RFC 9457, OpenAPI/Orval and generated-client constitution;
- [`access-auth-testing-contract.md`](access-auth-testing-contract.md) — proof layers, real PostgreSQL/browser/full-stack requirements;
- [`access-auth-m4-contract.md`](access-auth-m4-contract.md) — closed M4 signup/recovery/reset/reauth lifecycle authority;
- [`access-auth-m5-contract.md`](access-auth-m5-contract.md) — current M5 Google/Apple/passkey/linking/multi-authenticator authority;
- [`../workstreams/access-auth.md`](../workstreams/access-auth.md) — active vertical save-game;
- [`../workstreams/access-auth-m5-live-handoff-2026-08-29.md`](../workstreams/access-auth-m5-live-handoff-2026-08-29.md) — exact M5 continuation handoff;
- [`../database/README.md`](../database/README.md) and [`../database/access-auth.md`](../database/access-auth.md);
- [`../frontend/access.md`](../frontend/access.md);
- [`../domain/README.md`](../domain/README.md);
- [`../logical-model/README.md`](../logical-model/README.md);
- [`../physical-model/README.md`](../physical-model/README.md);
- [`../development/engineering-foundation-v0.md`](../development/engineering-foundation-v0.md).

Important ADRs:

- [`../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`](../decisions/ADR-007-domain-model-informed-persistence-boundaries.md);
- [`../decisions/ADR-008-frontend-engineering-stack.md`](../decisions/ADR-008-frontend-engineering-stack.md);
- [`../decisions/ADR-009-frontend-architecture-boundaries.md`](../decisions/ADR-009-frontend-architecture-boundaries.md);
- [`../decisions/ADR-010-postgresql-persistence-constitution.md`](../decisions/ADR-010-postgresql-persistence-constitution.md);
- [`../decisions/ADR-011-access-auth-architecture.md`](../decisions/ADR-011-access-auth-architecture.md).

---

## 3. Current system direction

DANTE is one product monorepo with accepted ownership for backend, Web, mobile, packages, infrastructure/tooling, system tests, documentation, prototypes and GitHub automation.

Backend remains a capability-first modular monolith.

Canonical persistence:

```text
PostgreSQL 18 major family
= sole canonical persistence + material-history authority
```

The accepted Domain → Logical → Physical chain is concretely materialized through CP6. Product verticals consume that constitution rather than reopening it for convenience.

Frontend remains platform-specific at renderer/UI/platform-adapter level with selective semantic sharing. Backend/database canonical authority and operation-specific offline governance remain preserved.

The Access/Auth branch is the first complete post-CP6 product vertical. M3 and M4 have now materialized and proved the first Auth spine/lifecycle; M5 extends the accepted architecture into federated/passkey multi-authenticator behavior.

---

## 4. Domain / Logical invariants carried forward

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

## 5. Frontend / generated-client direction

Accepted frontend foundation remains:

```text
TypeScript / React / Vite / Expo / pnpm / Turbo
feature-first Web/Mobile architecture
public-API-only dependency direction
Data Authority Matrix / feature data firewall
Web online-first
identity-scoped local data
design-token/UI/i18n/time/config boundaries
LOCAL/DEV/UAT/PROD vocabulary
```

Materialized Auth API chain through M4:

```text
FastAPI/Pydantic
→ deterministic OpenAPI 3.1
→ Orval Fetch
→ generated TypeScript/Zod
→ governed @dante/api-client
→ Web Auth remote
→ TanStack Query
→ Access application
```

TanStack Query owns remote lifecycle, never canonical Auth truth. Router-first session bootstrap remains permanent.

---

## 6. Access/Auth closed constitution and implementation

M2 durable subject owners remain:

```text
access-auth-architecture.md
access-auth-security-contract.md
access-auth-api-contract.md
access-auth-testing-contract.md
ADR-011
```

M3/M4 materialized that constitution without replacing it.

Current permanent foundations include:

```text
same-origin browser security boundary
opaque server-authoritative multi-session model
CSRF / Origin / Fetch Metadata / no broad CORS
Account / EmailIdentity / credential / Principal boundaries
Argon2id + pepper + HIBP
recovery/revocation lifecycle
/api/v1 + RFC9457
READ COMMITTED + targeted Account locking
ambiguous-commit reconciliation only where explicitly designed
OpenAPI → Orval → governed framework-neutral client
real PostgreSQL/API/Chromium+Firefox+WebKit proof
```

M4 adds:

```text
no Account before accepted mailbox proof
anti-enumeration before existing-account disclosure
purpose-specific signup/recovery challenges
single-use reset + revoke all sessions + fresh signin
same-AuthSession reauth bearer rotation
memory-only Web recovery bearer
bounded SMTP outside DB transaction
```

---

## 7. M5 architecture freeze — current

Current M5 authority:

```text
architecture/access-auth-m5-contract.md
```

M5.1 is complete and freezes:

```text
ExternalIdentity = issuer + subject
Google GIS/OIDC direction
Sign in with Apple Web/REST direction
provider key/nonce/state/replay handling
provider email authority classification
explicit link only; no email auto-merge
provider-enriched first-account bootstrap
profile provenance + no later provider overwrite
Apple one-shot name preservation
Apple Hide My Email
Apple protected grant/revocation/account-change lifecycle
PasskeyCredential 0..N
opaque WebAuthn user handle
WebAuthn Level 3-compatible passkey semantics
passwordless Accounts
add-password and lost-authenticator recovery posture
safe authenticator removal / anti-lockout
Auth vs provider-data integration isolation
future Home Security & Access readiness
```

M5.1 does **not** freeze exact SQL table names or public endpoint spellings. Those are M5.2 deliverables.

---

## 8. Current bounded deferrals

Still unresolved intentionally:

```text
M5 exact table/column/index/ACL names
M5 exact API paths/operationIds/problem codes
M5 dependency pins after qualification
exact provider client/project configuration isolation after real provider setup
exact profile/bootstrap durable owner after Domain/Logical owner review
native credential transport/secure storage → M6
full session/device management UX → M7
full security-event retention/observability → M7 unless correctness requires earlier state
future TOTP/recovery-code/MFA policy
provider-data integrations such as Gmail/Calendar/iCloud
third-party developer-platform/public-SDK lifecycle
cloud/IaC materialization
```

A deferral never authorizes violating accepted invariants.

---

## 9. Evidence vs current authority

Historical review/closure/evidence files remain useful but do not automatically override current consolidated contracts.

Operational state:

```text
workstreams/access-auth.md
+ workstreams/access-auth-m5-live-handoff-2026-08-29.md
```

Durable M5 meaning:

```text
architecture/access-auth-m5-contract.md
```

Repository/current code beats conversation memory.

---

## 10. Architecture reopen discipline

Closed Domain, Logical, Physical, Engineering, Frontend Foundation and Access/Auth M2–M4 decisions are not casually reselected.

Implementation evidence first reopens the smallest affected technology/adapter/boundary.

Do not reopen architecture because of:

```text
ORM convenience
table-count preference
provider naming
UI naming
framework fashion
generator fashion
test-suite convenience
one isolated provider annoyance
```

Reopen only when accepted requirements, safety/privacy constraints, real runtime evidence or current standards/provider incompatibility prove the boundary materially wrong.

---

## 11. Current next architecture posture

```text
DATABASE / CP6
CLOSED / INTEGRATED FOUNDATION

ACCESS FRONTEND BASELINE
CLOSED / ACCEPTED

M3
CLOSED / ENGINEERING PASS / USER ACCEPTED

M4
CLOSED / ENGINEERING PASS / USER ACCEPTED

M5
ACTIVE

M5.1 ARCHITECTURE / EXTERNAL-AUTHORITY FREEZE
COMPLETE

M5.2 EXACT PERSISTENCE + API DESIGN
NEXT / NOT STARTED
```

No M5 runtime capability is claimed until separately gated implementation and truthful proof execute.