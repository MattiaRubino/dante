# DANTE — Frontend Product Contract

- **Status:** CURRENT FRONTEND NAVIGATION / current `main` platform + Home/Temporal workstream
- **Last reconciled:** 2026-09-05

This directory contains durable product-facing frontend contracts carried into the production React workspace. Current implementation truth is the checked-out code/tests; prototype branches remain design/history evidence only.

## Read order

1. `access.md` — current Access/Auth Web contract
2. `home/home-structural-contract.md` — frozen Whole-Home H0 macro structure and responsive composition
3. `home/production-depth-handoff.md` — current Home workstream handoff
4. `home/current-checkpoint.md`
5. `home/contract.md`
6. `ui-registry.md`
7. `design-tokens.md`
8. `terminology.md`
9. `localization.md`
10. `production-readiness/component-architecture.md`
11. `production-readiness/backend-integration-contract.md`
12. `production-readiness/quality-gates.md`

Engineering/runtime authority remains the materialized frontend workspace, repository architecture, CI and local-development documentation. Product contracts do not replace those engineering authorities.

## Access current state

The old pre-backend Access materialization remains historical visual/product evidence, but Access is no longer a fake/pre-backend surface. Current Web capability is integrated with the governed backend and includes:

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

Current architecture:

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

The accepted Security UI is functionally proved but has accumulated substantial responsibility in `access-security-page.tsx`. Later hardening should split bounded password/provider/passkey/reauth sections before substantially expanding the page. This is a component-ownership cleanup, not a semantic Auth redesign.

## Home / Temporal React workstream

The accepted Home prototype remains an executable UX/reference specification, not code to transliterate line-by-line. The production React materialization on the Home/Temporal workstream must preserve accepted behavior while consuming the current platform, Access/Auth and shared frontend architecture from `main`.

The Whole-Home macro skeleton is change-controlled by H0. Child feature work consumes that skeleton and may not silently change region ownership, macro hierarchy or responsive composition merely because a local implementation would be easier.

Implementation must:

- preserve the accepted visual and behavioral contract before introducing redesigns;
- preserve the frozen H0 Whole-Home structural contract unless an explicit user-approved change reopens it;
- use the React/TypeScript architecture already materialized in the repository;
- componentize by ownership boundary rather than arbitrary pieces of the old monolith;
- separate view models from backend DTOs/domain/persistence shapes;
- preserve semantic IDs, localization keys and machine-readable Home-stage/Whole-Home contracts;
- keep semantic World/group/event colors distinct from generic DANTE chrome;
- keep Timeline/Temporal application seams independent from raw persistence and provider SDKs.

Machine-readable H0 authority lives in:

- `prototypes/frontend/shared/contracts/home-structure.contract.json`;
- `prototypes/frontend/shared/contracts/home-shell-responsive.matrix.json`.

Those contracts are blocking CI through `tests/prototypes/frontend-preprod-contracts.py`; runtime structure and geometry are additionally protected by React and Playwright regression tests.

## Historical prototype rule

Production code never imports prototype implementation. Prototype branches are recoverable evidence, not runtime dependencies.
