# DANTE — Access/Auth M4–M7 Execution Plan

- **Status:** CURRENT EXECUTION PLAN / M4 CLOSED / M5 ACTIVE / GROUPS 1–3 COMPLETE / GROUP 4 NEXT
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **Current execution block:** **GROUP 4 — M5-J + M5-K+ — Access Web + Final Browser / Provider / Security / UAT**
- **Last accepted execution block:** **GROUP 3 — M5-H + M5-I — COMPLETE / ENGINEERING PASS**
- **Group 3 PRE-SCOPE:** `ee099dc7c6bef4742c6e66e5d15f9a0428dd8ffa`
- **Group 3 engineering checkpoint:** `05b348e9e0293cd9cd0cc3f190824527761b24d9`
- **Accepted Alembic head:** `20260831_13`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact M5 design authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Live handoff:** `access-auth-m5-live-handoff-2026-08-29.md`

> This plan is the current execution authority. The M5-E/F/G/H/I/J/K+ labels remain semantic ownership labels from the frozen M5 design; they do not imply seven sequential implementation gates.

## 1. Continuation rules

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Before writes follow `docs/development/agent-operating-manual.md`: exact PRE-SCOPE, exact paths, purpose/out-of-scope, explicit approval, branch race-check, post-write compare.

No merge/rebase/history rewrite/protected-main write without explicit authorization.

Implementation/debug responsibility belongs to the assistant. The user runs requested QA commands and returns raw output; do not push manual source patches or formatter debugging onto the user.

## 2. Frozen foundations

Reuse, do not replace:

```text
Account = durable access/security root
EmailIdentity separate from Account
PasswordCredential optional
Principal runtime-derived
opaque PostgreSQL-backed AuthSession
multiple independent AuthSessions normal
same-origin Web Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF
Origin + Fetch Metadata + X-Dante-Client
/api/v1 + RFC9457
Account security serialization point
READ COMMITTED + targeted locking
no blind mutation retry
FastAPI/Pydantic → deterministic OpenAPI → Orval Fetch → governed @dante/api-client
TanStack Query remote lifecycle
TanStack Router critical-session bootstrap
real PostgreSQL proof
real HTTPS Chromium + Firefox + WebKit proof at the appropriate browser boundary
```

Permanent Auth rules:

```text
provider identity = issuer + subject
provider email != Account/link authority
provider authentication != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account valid
PasskeyCredential = authenticator, not Account
WebAuthn user_handle = opaque discoverable Account binding
normal provider/passkey removal = logical revoke
no Account before accepted mailbox proof
reauth rotates exact bearer on same AuthSession
network/expensive external verification outside DB mutation transaction
commit ambiguity → operation-specific reconciliation only
```

## 3. Closed M5 implementation

```text
M5.1 architecture/external-authority freeze            COMPLETE
M5.2 exact persistence/API design                      COMPLETE
M5-A persistence foundations                           COMPLETE / REAL POSTGRESQL PROVEN
M5-B provider/JWK/JOSE/AEAD/WebAuthn infrastructure    COMPLETE / ENGINEERING PASS
M5-C Google authentication                             COMPLETE / ENGINEERING PASS
M5-D Apple authentication + grant/notifications        COMPLETE / ENGINEERING PASS
GROUP 1 / M5-E + M5-G                                  COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                                         COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H + M5-I                                  COMPLETE / ENGINEERING PASS
```

Current accepted DB is Alembic `20260831_13`, PostgreSQL 18.6, 83 tables, 5 views, 15 routines, 75 triggers, 156 physical indexes, 85 FKs, 233 CHECKs and 103 standalone Dictionary entries. Group 2 and Group 3 required no DB structural or ACL widening.

## 4. Grouped M5 execution

```text
GROUP 1
M5-E + M5-G
Authenticator Lifecycle + Password/Passwordless Adaptation
COMPLETE / ENGINEERING PASS

GROUP 2
M5-F
WebAuthn / Passkeys
COMPLETE / ENGINEERING PASS

GROUP 3
M5-H + M5-I
Public FastAPI + Deterministic OpenAPI / Governed Client
COMPLETE / ENGINEERING PASS

GROUP 4 — CURRENT / NEXT
M5-J + M5-K+
Access Web + Security / Provider / Browser / UAT / Acceptance
NEXT
```

Execution order remains Group 1 → Group 2 → Group 3 → Group 4. Do not restore the old E→F→G→H→I→J→K sequence.

## 5. Group 2 closeout authority

Group 2 is closed at the engineering layer with real `python-fido2`, real PostgreSQL and concurrency proof.

```text
Ruff / mypy                     PASS
non-PostgreSQL                  191 PASS
PostgreSQL                      132 PASS
total                           323 PASS
backend build                   PASS
scope audit                     PASS
```

Browser/hardware passkey acceptance is intentionally deferred to Group 4.

## 6. Group 3 closeout authority

Group 3 delivered one deterministic contract pipeline:

```text
application services
→ FastAPI/Pydantic public M5 routes
→ RFC 9457 + no-store + request IDs
→ Origin / Fetch Metadata / X-Dante-Client / CSRF
→ opaque HttpOnly provider continuation cookies
→ Apple bounded form_post ingress + notifications
→ deterministic OpenAPI
→ frozen operationIds / typed success unions / typed problems
→ Orval Fetch + generated Zod
→ governed @dante/api-client
→ strict runtime contract validation
→ generated drift + two-run determinism proof
```

Final proof:

```text
uv lock --check                        PASS / 57 packages
Ruff                                  PASS
mypy                                  PASS / 56 source files
focused M5 HTTP/OpenAPI               35 PASS
full non-PostgreSQL                   225 PASS
provider-continuation PostgreSQL      2 PASS
full PostgreSQL                       134 PASS
backend build                         PASS
api-client lint/typecheck             PASS
api-client tests                      11 PASS
generated drift/determinism           PASS / 78 files
architecture check                    PASS / 151 modules / 287 dependencies
workspace typecheck                   PASS / 6 of 6
workspace build                       PASS / 2 of 2
git diff / clean synced tree          PASS
PRE-SCOPE scope audit                 PASS
```

PRE-SCOPE `ee099dc7...` → engineering checkpoint `05b348e9...` is ahead-only and contains only the approved Group-3 backend/contract/generated-client/test surface. No migration, mapping, Dictionary, ACL or frontend implementation entered Group 3.

Do not reopen Group 3 absent direct defect evidence.

## 7. GROUP 4 — M5-J + M5-K+ — NEXT

### 7.1 Purpose

Materialize the actual Access Web experience against the already-governed backend/client contract and complete the real browser/provider/passkey acceptance required to close M5.

### 7.2 Required Web materialization

```text
email/password signin/signup/recovery/reauth
Google begin/complete
Apple begin and returned callback outcome handling
passkey registration/authentication/reauthentication
provider enrollment flow
provider link-required + explicit confirmation
provider unlink
password establish/remove
passkey label/remove
methods/security management projection
loading/cancel/error/recovery states
backend-authoritative success only
```

Browser rules:

```text
no JWT/localStorage auth
no sessionStorage auth authority
no frontend-authenticated cache as source of truth
no provider SDK result treated as DANTE login success
no raw generated-operation export
no ad-hoc fetch proliferation around @dante/api-client
no continuation capability exposed to JavaScript
```

### 7.3 Final Group-4 acceptance

```text
Chromium
Firefox
WebKit
real Google smoke/UAT
real Apple registered-domain smoke/UAT
Apple Private Email Relay sender configuration
real WebAuthn/passkey browser/hardware UAT
provider enrollment collision/link-required flow
reauth + authenticator management
same-origin/session/CSRF behavior in real browser
manual integrated M5 UAT
final docs reconciliation
explicit user acceptance
```

Backend/DB regressions should be rerun only where Group-4 changes justify them. Do not mechanically repeat heavy PostgreSQL suites for frontend-only edits unless authority changes or a defect demands it.

M5 closes only after Group 4 acceptance.

## 8. M6 — Native Mobile Access

```text
FUTURE / OPTIONAL / ONLY IF DELIBERATELY RE-GATED
```

Do not automatically insert M6 between M5 and M7 merely because it exists in the historical roadmap.

## 9. M7 — Security Hardening + Observability + Authenticated Handoff

```text
PLANNED / FINAL WHOLE-VERTICAL GATE
```

M7 owns production hardening, security/observability completeness and the final authenticated handoff into the rest of DANTE. It does not absorb unfinished M5 browser/provider acceptance.

## 10. Current authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
docs/workstreams/access-auth-m4-m7-execution-plan.md
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

The M5 architecture contracts remain frozen design authority. Operational status lives in the status/roadmap/workstream/handoff documents.
