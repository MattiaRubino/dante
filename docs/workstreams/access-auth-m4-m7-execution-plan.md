# DANTE — Access/Auth Integration + M7 Transition Plan

- **Status:** CURRENT EXECUTION PLAN / M5 CLOSED / PRE-INTEGRATION AUDIT ACTIVE
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Last reconciled:** 2026-09-04
- **Current branch Alembic head:** `20260903_15`
- **Protected-main Alembic head:** `20260830_09`
- **Current workstream authority:** `access-auth.md`
- **Closure record:** `access-auth-closure-2026-09-03.md`
- **Email Platform acceptance:** `../development/email-platform-acceptance-2026-09-03.md`

This file originally planned M4 through M7. Its execution role is now narrowed to the safe transition from the closed M5 branch into protected `main` and then toward later M7 work. Old phase-time instructions such as “Email architecture research next”, “durable Email Platform open”, or “real Internet email UAT open” are superseded by observed implementation and real-provider evidence.

## 1. Closed Access/Auth state

```text
M1 Access Visual / UX Freeze                 CLOSED / ACCEPTED
M2 Auth Architecture Freeze                  CLOSED / ACCEPTED
M3 Signin + AuthSession                      CLOSED / ACCEPTED
M4 Signup / Recovery / Reauth                CLOSED / ACCEPTED
M5 Multi-authenticator Account               CLOSED / ACCEPTED

M5 persistence / provider backend            COMPLETE / ENGINEERING PASS
authenticator lifecycle/passwordless         COMPLETE / ENGINEERING PASS
passkeys / WebAuthn                          COMPLETE / ENGINEERING PASS
FastAPI / OpenAPI / generated client         COMPLETE / ENGINEERING PASS
Web product engineering                      AUTOMATED QA PASS
local password/passkey UAT                   PASS
real Windows Hello UAT                       PASS
real Google UAT                              PASS
shared Email Platform                        CLOSED / ACCEPTED
real SES signup/recovery/reset UAT            PASS
real Apple registered-domain UAT             BOUNDED DEFERRED / NON-BLOCKING
```

Apple is not labelled PASS. Real Apple Web/provider UAT remains a future enablement/release prerequisite when a usable Apple account and registered HTTPS domain are available.

## 2. Permanent implementation boundaries

```text
Account = durable security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
Secure HttpOnly host-only Web session
session-bound CSRF + exact Origin/Fetch Metadata
provider identity = issuer + subject
provider token/assertion != DANTE AuthSession
passwordless Account valid
WebAuthn private-key/biometric material never stored by DANTE
OpenAPI → governed @dante/api-client → bounded Web remote
```

The shared Email Platform is separate infrastructure. Access/Auth is its first consumer, not its owner.

## 3. Current integration problem

Both accepted lines descend from CP6 revision `20260826_08` but are not yet converged.

Access/Auth + Email branch:

```text
20260826_08
→ 20260827_09
→ 20260827_10
→ 20260829_11
→ 20260830_12
→ 20260831_13
→ 20260903_14
→ 20260903_15
```

Protected `main` Recovery line:

```text
20260826_08
→ 20260830_09  recovery_material_state_retirement
```

This is an Alembic DAG divergence, not permission to rewrite either applied history.

## 4. Required pre-integration gate

Before merging protected `main` into `feature/access-auth`:

```text
documentation lifecycle debt                    CLOSED
current docs contain current truth               PASS
branch-only handoffs removed/consolidated        PASS
Dictionary scope/schema parity                   PASS
Dictionary current counts                        PASS
SQLAlchemy mapped-table inventory parity         PASS
single Access/Auth Alembic head                  PASS
fresh DB → 20260903_15                           PASS
head → base → head                               PASS
Alembic drift check                              PASS
current catalog ↔ Dictionary ↔ mappings          PASS
runtime ACL exactness                            PASS
backend static/test/build gates                  PASS
Web/API generated-contract gates                 PASS
```

A PASS is recorded only from executed evidence.

## 5. Main convergence procedure

Integration is forward-only and history-preserving:

```text
1. fetch protected main
2. merge main into feature/access-auth
3. resolve ordinary source/document conflicts without discarding either accepted workstream
4. preserve both Alembic heads
5. add one explicit Alembic merge revision whose down_revision contains both heads
6. reconcile Dictionary/current DB counts against the combined schema
7. run fresh-database, migration, catalog, ACL, Auth, Email and Recovery regressions
8. run full backend/Web gates
9. open PR feature/access-auth → main
10. merge only after required evidence is green
```

No rebase, force push, migration renumbering or edit of already-applied revisions is allowed.

## 6. Combined-database acceptance

After convergence the combined topology must be **measured**, not calculated by casually adding old counts.

Required proof includes:

```text
Recovery material_state_retirement still materializes and enforces anti-resurrection
Access/Auth M3–M5 persistence remains unchanged semantically
Email Platform durable intent/attempt/event/suppression remains intact
all SQLAlchemy mapped tables equal current Dictionary/current PostgreSQL catalog
all migration heads collapse to one repository head through the merge revision
runtime least privilege remains exact
Recovery and Email post-restore doctrines do not contradict each other
no generic Entity/EAV/JSONB/event-log shortcut is introduced by conflict resolution
```

## 7. Production-email boundary

Email engineering closure does not equal production sender deployment.

Future deployment still owns, as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity
SES production account/quota/reputation posture
live cloud provider-event ingress
production alerting/SLOs
traffic/reputation segmentation
Apple Private Email Relay sender-domain compatibility
```

These tasks do not reopen the shared Email Platform without concrete defect evidence.

## 8. M6

Native Mobile remains future/optional and requires an explicit re-gate. It is not required merely to complete Access/Auth integration.

## 9. M7 after protected-main integration

M7 remains later maturity work:

```text
session/device list
per-session revoke
revoke all others / log out everywhere
new-login/security-event alerts
“this wasn't me” response
security-event retention/observability
production operational dashboards/alerts
final accessibility/legal/release checks
final authenticated Home handoff
bounded componentization/hardening of Security UI
```

The accepted Account/AuthSession/authenticator architecture is intentionally capable of supporting this without semantic rewrite.

## 10. Safety

```text
no rebase/history rewrite
no force push
no direct protected-main write
no applied-migration rewrite
no fake PASS
no feature work mixed into integration repair unless required by a demonstrated regression
```

Repository/executable truth beats this plan if later evidence exposes a contradiction; in that case update this file in the same reviewed change.
