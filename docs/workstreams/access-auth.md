# DANTE — Access/Auth Full-Stack Vertical Workstream

- **Status:** ACTIVE VERTICAL / M1–M4 CLOSED / M5 FINAL EXTERNAL ACCEPTANCE OPEN
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Current branch checkpoint before this docs reconciliation:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **Current review:** `access-auth-m5-review-2026-09-02.md`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`

> Continue this existing vertical. Do not restart Access/Auth, create a replacement Account/session model, or reopen accepted Groups 1–3 absent direct defect evidence.

## 1. Current state

```text
M1–M4                                      CLOSED / ACCEPTED
M5.1 / M5.2                                COMPLETE
M5-A persistence                           COMPLETE / PG PROVEN
M5-B provider/crypto/WebAuthn               COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend                         COMPLETE / ENGINEERING PASS
GROUP 1 lifecycle/passwordless             COMPLETE / ENGINEERING PASS
GROUP 2 passkeys                           COMPLETE / ENGINEERING PASS
GROUP 3 public API/generated client         COMPLETE / ENGINEERING PASS
GROUP 4 product engineering                AUTOMATED QA PASS
GROUP 4 local manual UAT                    PASS
GROUP 4 real Google UAT                    PASS
real Internet email delivery               OPEN
real Apple Web UAT                         DEFERRED / OPEN
whole M5                                   ACTIVE / NOT CLOSED
```

## 2. Frozen Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived, never persisted
multiple AuthSessions normal
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Forbidden without a new architecture gate: JWT/localStorage browser Auth, persisted Principal, silent provider-email merge, provider token as DANTE session, provider-specific Account authority, ad-hoc raw Auth fetch clients, hand-written WebAuthn crypto, biometric/PIN/device-fingerprint persistence.

## 3. Current product evidence

Automated gate at `ab2716...`:

```text
format/typecheck/lint/architecture PASS
68 / 68 Web unit/component PASS
60 / 60 Auth Playwright PASS
Chromium / Firefox / WebKit through canonical HTTPS suite
```

Live local UAT proved:

```text
password signin/logout
session/reload authority
password reauth + rotated bearer persistence
real Windows Hello passkey registration
passkey reauth
passwordless passkey signin
passkey rename persistence
password removal with alternate authenticator
last-authenticator anti-lockout
password restore + fresh signin
direct PostgreSQL coherence
```

Real Google UAT proved official GIS → real Google token → backend verification → third-party mailbox proof → passwordless DANTE Account → canonical AuthSession. Direct DB inspection proved `ExternalIdentity(provider=google, issuer=https://accounts.google.com)`, zero PasswordCredential and an active AuthSession.

See `access-auth-m5-review-2026-09-02.md` for the full evidence and defect history.

## 4. UAT defects closed

```text
AuthSession rotation/read race            FIXED + LIVE VERIFIED
cross-chunk remote-error identity         FIXED
WebAuthn options.publicKey envelope       FIXED + WINDOWS HELLO LIVE VERIFIED
```

These defects justify retaining manual UAT as a separate proof layer.

## 5. Database truth

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables / 5 views / 15 routines / 75 triggers
156 physical indexes / 85 FKs / 233 CHECKs
103 standalone Dictionary entries
```

Group-4 product work did not create a new DB topology. `20260831_13` is the bounded runtime ACL required by authenticator lifecycle.

## 6. Current next work

### 6.1 Email delivery architecture — NEXT

Pause vendor selection until a dedicated research gate compares:

```text
external transactional provider
vs self-hosted SMTP
vs hybrid/provider-neutral adapter
SMTP vs HTTP API
SPF/DKIM/DMARC and domain ownership
bounce/complaint/suppression lifecycle
retry ambiguity / idempotency / queues
privacy / observability / secrets
Apple relay requirements
cost and operational burden
```

The opt-in real-SMTP support at `9c0587...` is only UAT tooling and still needs targeted qualification. Loopback SMTP remains the deterministic default.

### 6.2 Apple real UAT — OPEN / DEFERRED

Requires a real Apple account plus registered-domain setup. Do not fake a production acceptance claim.

### 6.3 M7 — planned maturity hardening

Session/device management, remote revoke, security-event alerts, production observability and final authenticated Home handoff belong here unless a correctness defect forces earlier work.

## 7. Maintainability note

The current security surface is functionally proved, but `access-security-page.tsx` has accumulated substantial orchestration/rendering responsibility. Before adding much more account-security UX, split it by bounded password/provider/passkey/reauth ownership while preserving the accepted application/platform boundaries. This is a maintainability hardening, not a reason to reopen Auth semantics.

## 8. Documentation authority

Current operational status lives here plus:

```text
../PROJECT-STATUS.md
../ROADMAP.md
access-auth-m5-review-2026-09-02.md
```

The old dated live handoff is superseded. M5 architecture/persistence contracts remain semantic authority, but phase-progress text inside them is historical where it conflicts with these current operational documents.

## 9. Branch/worktree safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch `main`, `feature/home-react`, `feature/access-frontend` or `/home/mattia/projects/dante-frontend` without explicit topology authorization. No merge/rebase/history rewrite/force push/protected-main write without explicit authorization.