# DANTE — Frontend Terminology Registry

**Purpose:** keep product wording changeable without coupling user-facing names to implementation IDs.

## Naming statuses

- `LOCKED` — accepted product term; change requires explicit naming decision.
- `WORKING` — current user-facing wording; may change.
- `TECHNICAL_ONLY` — implementation/documentation identifier, never intended as UI copy.
- `DEPRECATED` — previous wording retained for history/compatibility, not preferred.
- `REJECTED` — intentionally not used going forward.

## Core rule

Technical IDs are stable English identifiers. Visible copy is localized separately.

Example:

```text
technical ID    home.contextRail.capture
it-IT label     Cattura
en-US label     Capture
```

Changing `Cattura` to another product term must not require renaming the technical ID, selectors, contracts or persisted semantics.

## Current terminology

| Concept / technical ID | it-IT | en-US | Status | Notes / history |
|---|---|---|---|---|
| product | DANTE | DANTE | LOCKED | Current accepted app/product name. Historical LifeOS refers to same lineage. |
| `home` | Home | Home | WORKING | Current primary surface name. |
| historical surface noun | Today | Today | DEPRECATED | `Today v21` remains historical behavior evidence, not a second current Home name. |
| `home.timeline.now` | Ora | Now | WORKING | Return-to-current-time action / temporal current point. |
| `home.orientation.nowNext` | Ora / Prossimo | Now / Next | WORKING | Current-moment + immediate-continuation composition. |
| `home.orientation.highlight` | In evidenza | Highlight | WORKING | Materially relevant attention, not generic recommendation. |
| `home.orientation.dynamic` | Per te | For you | WORKING | Contextual opportunity/suggestion role. |
| `home.stage.worlds` | Worlds / Mondi | Worlds | WORKING | Historical prototype vocabulary; B2 must redefine the job before final naming. |
| `home.stage.stats` | Stats | Stats | WORKING | Historical prototype vocabulary; B2 must redefine the job before final naming. |
| old side card | Appunti | Notes | DEPRECATED | Replaced by `home.contextRail.capture`. |
| old side card | Review | Review | DEPRECATED | Replaced by `home.contextRail.resolution`; topbar legacy Review still physically present and separately marked deprecated. |
| `home.contextRail.capture` | Cattura | Capture | WORKING | Functional concept accepted; final product label can still change. |
| `home.contextRail.resolution` | Da risolvere | To resolve | WORKING | Functional concept accepted; final product label can still change. |
| `home.contextRail.capture.history` | Registro completo | Full log | WORKING | Deeper capture history access. |
| `home.topbar.create` | Crea | Create | WORKING | Existing quick-create wording; semantic relationship to Capture to review later. |
| `home.topbar.search` | Cerca | Search | WORKING | Stable functional verb, not yet formally locked. |
| `access` | Accesso | Access | TECHNICAL_ONLY | Surface/workstream family covering unauthenticated entry, re-auth and first-run handoff. Not intended as a primary navigation label. |
| `access.signIn` | Accedi a DANTE | Sign in to DANTE | WORKING | Neutral existing-account entry. `Bentornato` / `Welcome back` was rejected because it assumes prior use. |
| `access.signUpEmail` | Crea il tuo account DANTE | Create your DANTE account | WORKING | DANTE-owned account creation begins with email; profile data comes later. |
| `access.signUpPassword` | Proteggi il tuo account | Protect your account | WORKING | Password step after email. Exact backend password policy remains separate. |
| `access.verifyEmail` | Controlla la tua email | Check your email | WORKING | Email verification UX. |
| `access.forgotPassword` | Recupera l’accesso | Recover access | WORKING | Neutral recovery entry. |
| `access.setupName` | Nome preferito | Preferred name | WORKING | Lightweight post-account setup field, not account identity authority. |
| `access.setupLocale` | Lingua e fuso orario | Language and time zone | WORKING | Operational setup, not inferred preference semantics. |
| `access.setupStart` | Da dove vuoi iniziare? | Where do you want to start? | WORKING | First-run branching prompt; choices are not permanent. |
| `access.homeHandoff` | — | — | TECHNICAL_ONLY | Prototype handoff marker. It is not a replacement name/implementation for Home. |
| rejected sign-in heading | Bentornato | Welcome back | REJECTED | Assumes the person has used DANTE before; replaced by neutral sign-in wording. |
| rejected English auth wording | Login to DANTE | Login to DANTE | REJECTED | Less natural as a user-facing heading than `Sign in to DANTE`. |

## Rename procedure

For a normal wording change:

1. keep technical ID unchanged;
2. update `it-IT.json` / `en-US.json`;
3. update this table and change-log;
4. update the current surface contract only if meaning changed, not for pure copy;
5. rebuild/check the standalone prototype.

A wording-only rename must not require hunting through unrelated CSS/JS files.

## Forbidden shortcut

Do not rename an internal concept merely to match current visible copy. Do not promote `Worlds`, `Stats`, historical `Today`, Domain Model nouns or temporary mock wording into canon because they already exist in HTML.
