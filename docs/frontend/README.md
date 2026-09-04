# DANTE — Frontend Product Contract

- **Status:** CURRENT FRONTEND NAVIGATION / `feature/access-auth`
- **Last reconciled:** 2026-09-02

This directory contains durable product-facing frontend contracts carried into the production React workspace. Current implementation truth is the checked-out code/tests; prototype branches remain design/history evidence only.

## Read order

1. `access.md` — current Access/Auth Web contract
2. `home/current-checkpoint.md`
3. `home/contract.md`
4. `ui-registry.md`
5. `design-tokens.md`
6. `terminology.md`
7. `localization.md`
8. `production-readiness/component-architecture.md`
9. `production-readiness/backend-integration-contract.md`
10. `production-readiness/quality-gates.md`

## Access current state

The old pre-backend Access materialization remains the visual/product baseline, but Access is no longer a fake/pre-backend surface on `feature/access-auth`.

Current branch-local Web capability includes:

```text
email/password signin
session bootstrap/logout
signup/OTP/recovery/reset/reauth
Google official GIS signin/link/reauth flow
Apple browser begin/continuation integration
provider enrollment/link collision flow
passkey signin/register/reauth/rename/remove
password establish/remove
/security authenticator management
backend-authoritative anti-lockout
IT/EN copy
```

Automated product proof at the reviewed checkpoint:

```text
68 / 68 Web unit/component tests PASS
60 / 60 Auth Playwright PASS
Chromium / Firefox / WebKit through canonical HTTPS suite
```

Manual UAT additionally proved real Windows Hello passkeys and real Google authentication.

## Frontend architecture

```text
TanStack Router
→ feature public API
→ TanStack Query
→ Access application boundary
→ platform Web Auth adapters
→ governed @dante/api-client
→ same-origin /api/v1
→ FastAPI/PostgreSQL canonical authority
```

Rules:

```text
feature-first ownership
route adapters remain thin
presentation does not import raw generated operations/platform adapters
no ad-hoc Auth fetch proliferation
no browser-persisted Auth token
provider/browser success != DANTE authenticated success
WebAuthn crypto remains backend-owned
```

## Current maintainability note

The accepted Security UI is functionally proved but has accumulated substantial responsibility in `access-security-page.tsx`. Later hardening should split bounded password/provider/passkey/reauth sections before substantially expanding the page. This is a component-ownership cleanup, not a semantic Auth redesign.

## Home

The accepted Home prototype remains an executable UX/reference specification, not code to transliterate line-by-line. Home React work must preserve accepted behavior while using the production React/TypeScript architecture and current shared semantic tokens.

The true authenticated Home handoff remains an M7/current-product integration obligation; the Access branch must not fake Home completion merely to close Auth.

## Historical prototype rule

Production code never imports prototype implementation. Prototype branches are recoverable evidence, not runtime dependencies.