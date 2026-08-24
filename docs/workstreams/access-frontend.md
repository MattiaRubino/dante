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

### AF-01D — shell completion / professional polish

AF-01D closes all shell behavior that can be completed safely before choosing the real Auth integration boundary:

- the production Italian hero copy is localized; the immutable A3.4 prototype remains historical evidence and is not rewritten;
- `document.documentElement.lang` follows the active supported locale;
- user-visible input/visibility-control strings are owned by `@dante/i18n` rather than hardcoded in components;
- password visibility is a real local UI behavior and preserves the entered value;
- locale popover semantics/focus/Escape/keyboard entry are hardened without pretending to be a WAI-ARIA menu implementation;
- unit/E2E coverage is extended for localization, language persistence, document language and password visibility;
- visual/accessibility/format/lint/type/architecture/build gates remain mandatory before AF-01D is accepted.

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

## Mandatory stop before AF-02/mock

Do **not** automatically create the temporary mock Access adapter after AF-01D.

At the AF-01D acceptance gate, first inspect the current backend workstream/repository truth. If real backend Auth + a stable API/OpenAPI contract is sufficiently ready, skip the mock and design the direct real integration boundary. Only create the thin temporary mock adapter if backend readiness still makes it useful.

The intended alternatives are:

```text
Backend Auth not ready
React Access → thin Access interface → deterministic temporary adapter

Backend Auth ready
React Access → generated/typed API boundary → real backend Auth
```

The UI/state model must not be redesigned merely because one integration path is more convenient.

## Merge discipline

A merge to protected `main` remains a separate explicit gate after local and hosted QA. Never merge merely because GitHub reports the branch mergeable.

## Continuity

Read `docs/workstreams/access-frontend-live-handoff.md` before continuing this workstream in a new chat/tool/session. Repository truth overrides chat memory.
