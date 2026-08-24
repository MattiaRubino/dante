# Access frontend workstream

**Branch:** `feature/access-frontend`  
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

Current hardening boundary:

- Access UI implementation lives behind `features/access/index.ts` and the feature-local `ui/` boundary;
- routes consume only the feature public API;
- repeated product colors/radii move to production `@dante/design-tokens` semantic authority;
- provider placeholder characters are replaced by provider-brand marks while provider execution remains deliberately inactive;
- the obsolete diagnostic Web E2E is replaced by Access production-preview coverage;
- desktop, narrow and phone-width browser compositions are checked for horizontal overflow and essential controls;
- keyboard focus receives an explicit baseline check.

Testing Library component coverage, axe automation and React Hooks lint qualification are the next AF-01C micro-step because their dependencies must be added through the real pnpm lockfile, not handwritten.

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

- backend AuthN/AuthZ;
- password/session/token physical design;
- Google client ID or Apple Services ID;
- OAuth/OIDC callback handling;
- account-linking backend mutation;
- recovery backend proofs;
- OpenAPI/Orval/API client;
- TanStack Query;
- TanStack Form/Zod form behavior;
- PowerSync;
- Home routing after successful authentication;
- native Mobile Access implementation.

## Next production boundary

AF-02 materializes the approved Access state graph and real client-side form/state behavior behind thin temporary interfaces. AF-03 replaces those interfaces with the real backend/OpenAPI contract when backend Access exists.

A merge to protected `main` remains a separate explicit gate after local and hosted QA.
