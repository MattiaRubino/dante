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
| `home.stage.continuity` | Mondi | Worlds | LOCKED | Accepted B2 projection name for carried-forward significant realities the user wants readily accessible. Technical ID remains independent from the visible noun. |
| historical `home.stage.worlds` / `Worlds` | Mondi / Worlds | Worlds | DEPRECATED | Historical implementation/vocabulary superseded by stable technical projection ID `home.stage.continuity`. |
| `home.stage.signals` | Segnali | Signals | LOCKED | Accepted B2 analytical-projection name for values, deltas, trends, targets, planned-vs-actual and cautious patterns. |
| historical `home.stage.stats` / `Stats` | Stats | Stats | DEPRECATED | Generic Stats framing is superseded by `home.stage.signals`; retained only for historical implementation evidence. |
| old side card | Appunti | Notes | DEPRECATED | Replaced by `home.contextRail.capture`. |
| old side card | Review | Review | DEPRECATED | Replaced by `home.contextRail.resolution`; topbar legacy Review still physically present and separately marked deprecated. |
| `home.contextRail.capture` | Cattura | Capture | WORKING | Functional concept accepted; final product label can still change. |
| `home.contextRail.resolution` | Da risolvere | To resolve | WORKING | Functional concept accepted; final product label can still change. |
| `home.contextRail.capture.history` | Registro completo | Full log | WORKING | Deeper capture history access. |
| `home.topbar.create` | Crea | Create | WORKING | Existing quick-create wording; semantic relationship to Capture to review later. |
| `home.topbar.search` | Cerca | Search | WORKING | Stable functional verb, not yet formally locked. |

## Rename procedure

For a normal wording change:

1. keep technical ID unchanged;
2. update `it-IT.json` / `en-US.json`;
3. update this table and change-log;
4. update the current surface contract only if meaning changed, not for pure copy;
5. rebuild/check the standalone prototype.

A wording-only rename must not require hunting through unrelated CSS/JS files.

## Forbidden shortcut

Do not rename an internal concept merely to match current visible copy. Do not promote historical `Worlds`, `Stats`, historical `Today`, Domain Model nouns or temporary mock wording into canon because they already exist in HTML.
