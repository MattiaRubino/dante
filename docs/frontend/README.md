# DANTE — Frontend Product Contract

- **Status:** CURRENT FRONTEND NAVIGATION — integrated Home/Temporal candidate over current `main`
- **Last reconciled:** 2026-09-05
- **Integration state:** `feature/home-timeline` contains `main` through `7bc7c0136cb5579528be1e2be0e71a6399004f90`; no PR is opened by this checkpoint.

This directory contains durable product-facing frontend contracts carried into the production React workspace. Current implementation truth is the checked-out code/tests plus current CI evidence. Prototype branches and dated checkpoints remain design/history evidence only.

Operational handoff documents under `docs/frontend/home/` are retired pointers, not live authority. They remain only so historical links do not break.

## Read order

1. `access.md` — current Access/Auth Web contract
2. `home/home-structural-contract.md` — frozen Whole-Home H0 macro structure and responsive composition
3. `home/current-checkpoint.md` — current Home/Temporal integration state
4. `home/temporal-frontend-roadmap.md` — current Temporal frontend authority
5. `home/temporal-f0-contract.md` — frozen temporal application foundation
6. `home/timeline-t1-frozen-contract.md` — frozen Timeline behavior
7. `home/temporal-create-c1-manual-acceptance.md` — C1 manual product gate
8. `home/world-focus-architecture.md` — World Focus frontend architecture
9. `home/world-focus-frontend-roadmap.md` — World Focus pre-backend roadmap
10. `home/contract.md` — durable Home product/behavior intent
11. `ui-registry.md`
12. `design-tokens.md`
13. `terminology.md`
14. `localization.md`
15. `production-readiness/component-architecture.md`
16. `production-readiness/backend-integration-contract.md`
17. `production-readiness/quality-gates.md`

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

## Home / Temporal integrated candidate

The accepted Home prototype remains an executable UX/reference specification, not code to transliterate line-by-line. The production React Home/AppShell/Timeline/Temporal materialization now lives together on the integration candidate and consumes the current platform, Access/Auth, Recovery, Email, Observability, OpenAPI and shared frontend baseline from `main`.

The Whole-Home macro skeleton is change-controlled by H0. Child feature work consumes that skeleton and may not silently change region ownership, macro hierarchy or responsive composition merely because a local implementation would be easier.

Frozen foundations remain distinct from open product acceptance:

```text
H0 Whole Home structure        FROZEN
P1 AppShell / Topbar           FROZEN
T1 Timeline behavior           FROZEN
F0 Temporal application seam   CLOSED / FROZEN
C1 Manual Temporal Create      OPEN — manual product acceptance not granted
C2 Structured Detail           BLOCKED until C1 closes
```

Merging the integration branch must never be interpreted as `C1 MANUAL PASS — APPROVED`.

Implementation must:

- preserve accepted visual and behavioral contracts before introducing redesigns;
- preserve H0 unless an explicit user-approved change reopens it;
- use the React/TypeScript architecture materialized in the repository;
- componentize by ownership boundary rather than arbitrary pieces of the old monolith;
- separate view models from backend DTOs/domain/persistence shapes;
- preserve semantic IDs, localization keys and machine-readable Home-stage/Whole-Home contracts;
- keep semantic World/group/event colors distinct from generic DANTE chrome;
- keep Timeline/Temporal application seams independent from raw persistence and provider SDKs;
- keep pre-backend C1 behavior truthful: no fake PostgreSQL/provider/recurrence-materialization success.

Machine-readable H0 authority lives in:

- `prototypes/frontend/shared/contracts/home-structure.contract.json`;
- `prototypes/frontend/shared/contracts/home-shell-responsive.matrix.json`.

Those contracts are blocking CI through `tests/prototypes/frontend-preprod-contracts.py`; runtime structure and geometry are additionally protected by React and Playwright regression tests.

## Historical prototype / branch rule

Production code never imports prototype implementation. Prototype branches and retired handoffs are recoverable evidence, not runtime or operating dependencies.

Branch/worktree/SHA labels inside dated frozen or historical records describe provenance. They do not override `home/current-checkpoint.md`, the checked-out branch, or current repository/CI truth.
