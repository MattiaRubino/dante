# Access frontend workstream

**Branch:** `feature/access-frontend`  
**Permanent frontend worktree:** `/home/mattia/projects/dante-frontend`  
**Product authority:** `prototypes/frontend/access/README.md`, `docs/frontend/access/current-checkpoint.md`, `docs/frontend/access/contract.md`, `docs/frontend/access/state-model.md`  
**Desktop visual authority:** Access A3.4  
**Mobile visual authority:** M1.2 + PRG-0

## Purpose

Materialize the approved DANTE Access experience inside the production React/Vite frontend without inventing backend authentication semantics before the real backend contract exists.

## Current production state

### AF-01A — first React materialization

Materialized the unauthenticated SignIn shell on Web:

- DANTE brand stage and locked brand masters;
- email/password visual controls;
- Google/Apple provider affordances;
- Italian/English resource ownership through `@dante/i18n`;
- desktop and narrow responsive composition;
- no real submission, provider transaction, session or backend contract.

### AF-01C — foundation hardening

Completed foundation work includes:

- Access UI behind `features/access/index.ts` and the feature-local `ui/` boundary;
- routes consuming only the feature public API;
- design-token, architecture and generated-output gates;
- production provider marks while provider execution remains deliberately inactive;
- Testing Library component coverage;
- Playwright production-preview coverage;
- axe WCAG A/AA automation;
- React Hooks lint qualification;
- desktop open brand-stage geometry, narrow composition and phone-width overflow coverage;
- professional IT/EN selector with browser-locale fallback and persisted preference.

### AF-01D — shell completion / professional polish — PASS

AF-01D is accepted as the completed pre-auth Web shell after fresh local QA and visual review on 2026-08-25.

Accepted behavior includes:

- production Italian hero copy `Comprendi la vita. / Dai forma al prossimo passo.`;
- English hero copy `Understand life. / Shape what comes next.`;
- locale-aware desktop headline sizing so Italian and English preserve a comparable visual hierarchy;
- `document.documentElement.lang` following the active supported locale;
- user-visible input/visibility-control strings owned by `@dante/i18n` rather than hardcoded in components;
- password visibility as a real local UI behavior that preserves the entered value;
- locale popover focus/Escape/keyboard behavior;
- browser locale fallback plus persisted IT/EN preference;
- unit/E2E coverage for localization, language persistence, document language, password visibility and desktop hero geometry;
- desktop/narrow/phone layout checks, horizontal-overflow guards and axe WCAG A/AA automation.

The accepted desktop production composition keeps the A3.4 product direction while incorporating approved production adjustments: full warm canvas, open left brand stage, large muted Living Orbits, locked DANTE topbar, compact locale control and a separate Access card.

AF-01D does **not** invent a credential submit result, fake provider success, fake session, recovery proof or account mutation.

## Invariants

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple Access authenticates a DANTE account only. It does not grant Gmail, Calendar, iCloud or other provider-data permissions.

## Deliberately not materialized yet

- backend AuthN/AuthZ integration;
- password/session/token physical design;
- Google client ID or Apple Services ID;
- OAuth/OIDC callback handling;
- account-linking backend mutation;
- recovery backend proofs;
- OpenAPI/Orval API client for Access;
- TanStack Query remote-auth integration;
- TanStack Form/Zod real Access forms/state graph;
- Home routing after successful authentication;
- native Mobile Access implementation;
- final Terms/Privacy destinations/content (do not create fake or broken legal routes merely to make the shell look complete).

## Backend-readiness gate — 2026-08-25

The mandatory post-AF-01D backend inspection was performed against `feature/logical-postgresql`.

Current backend evidence shows a FastAPI/bootstrap/PostgreSQL persistence foundation, but no implemented Access authentication surface yet. The application factory currently exposes process/database health endpoints; the backend tree does not yet contain the required Auth/session/OAuth/recovery/account-linking route/domain boundary needed for real frontend Access integration.

Verdict:

```text
AF-01D frontend shell                    PASS
backend PostgreSQL/persistence foundation ADVANCED / ACTIVE
real Access Auth API/OpenAPI              NOT READY
frontend real-auth integration            BLOCKED BY BACKEND AUTH BOUNDARY
```

Therefore **do not start AF-03 real integration yet**.

## Mandatory stop before AF-02/mock

Do **not** automatically create the temporary mock Access adapter now.

The user is continuing backend work in parallel. Keep `feature/access-frontend` parked at the accepted AF-01D checkpoint until the next explicit frontend continuation. At that point re-read backend repository truth first:

```text
Backend Auth still not ready
→ decide whether a thin deterministic temporary Access adapter is now useful

Backend Auth ready enough
→ skip the mock and design the generated/typed real API boundary
```

No mock, API contract or provider behavior should be invented merely to keep frontend work moving.

## QA gate

The normal frontend release-quality gate remains:

```bash
pnpm format:check
pnpm lint
pnpm typecheck
pnpm architecture:check
pnpm generated:check
pnpm test
pnpm --filter @dante/web build
pnpm --filter @dante/web test:e2e
git diff --check
```

## Merge discipline

A merge to protected `main` remains a separate explicit gate after local and hosted QA. Never merge merely because GitHub reports the branch mergeable.

## Continuity

Read `docs/workstreams/access-frontend-live-handoff.md` before continuing this workstream in a new chat/tool/session. Repository truth overrides chat memory.
