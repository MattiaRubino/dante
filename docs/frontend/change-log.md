# DANTE — Frontend Change Log

Append-only operational history. This is not a Git substitute; it records product/UI meaning.

## 2026-08-19 — A1 workstream migration

- `ADDED` `prototype/frontend` as active pre-production frontend workstream.
- `DEPRECATED` `prototype/phase-4-today-home` as active branch; retained as historical evidence.
- `ADDED` frontend research index and migrated Phase 4 interaction references.
- `ADDED` exact corrected Home baseline.

## 2026-08-19 — A2 modular source

- `ADDED` deterministic modular/copy-on-write Home work source.
- `ADDED` named CSS/JS module map and build QA.
- `CHANGED` workflow so the complete standalone artifact is retained while work can happen in bounded modules.
- `VISUAL_ONLY`: none.
- `BEHAVIOR_CHANGED`: none.

## 2026-08-19 — B1 Context Rail v1

- `REMOVED` old side `Appunti` card from the accepted B1 output.
- `REMOVED` old side `Review` card from the accepted B1 output.
- `ADDED` `home.contextRail` as one integrated secondary surface.
- `ADDED` `home.contextRail.capture` (`user -> DANTE`) with free capture, voice/attachment affordances, submit and recent-capture trace.
- `ADDED` `home.contextRail.resolution` (`DANTE -> user`) with unresolved count, real quick-action controls and deeper-detail affordance.
- `CHANGED` rail height to stretch with the timeline column instead of leaving arbitrary unused lower space.
- `REJECTED` focus/expand chevrons and the hidden balanced/focus state machine because the interaction was ambiguous and added no clear user value.
- `DEPRECATED` topbar legacy Review Queue as a duplicate concept; it remains physically present until a later explicit cleanup scope.
- `NO_CHANGE` timeline semantics, calendar/day ribbon, timeline toolbar, current `Worlds`/`Stats`, global brand/skin and backend semantics.

## 2026-08-19 — documentation invariant

- `ADDED` permanent frontend operational rule: registry + surface contract + terminology/localization/tokens + append-only history must stay synchronized with implementation.
- `ADDED` stable English technical IDs independent from visible labels.
- `ADDED` localization and semantic design-token authorities for new/touched UI.

## 2026-08-20 — B2 Central Stage v16 WIP checkpoint

- `ADDED` a non-accepted WIP checkpoint preserving the current B2 central-stage direction before resize hardening and brand/logo alignment.
- `CHANGED` working central-stage labels/direction to `Mondi` and `Segnali` in the saved preview lineage.
- `CHANGED` working Signal composition to a maximum of three visible items with a centered compact track.
- `CHANGED` working Signal navigation to follow the Mondi carousel grammar: previous/next, selection and drag/swipe.
- `ADDED` working partial-Mondi empty-slot treatment using existing sphere positions rendered ghosted with `+` instead of adding new geometry.
- `REMOVED` the experimental external add control from the saved WIP checkpoint.
- `KNOWN_ISSUE` global browser/window resize is not stable; responsive/global geometry QA remains open.
- `NO_CHANGE` accepted Home build remains B1 Context Rail v1. This WIP save does not close B2, does not promote new backend semantics, and does not finalize branding/logo treatment.

## 2026-08-20 — B2.5 Frontend Pre-Production Foundation v0

- `ADDED` production-readiness authorities for component architecture, backend integration, quality gates and production-web handoff.
- `ADDED` framework-neutral Home-stage machine-readable state/event/geometry/data-boundary contract.
- `ADDED` JSON Schema for the Home-stage frontend view model and synthetic full/partial fixtures.
- `ADDED` 24-case desktop responsive matrix: six widths × AI expanded/collapsed × continuity/signals.
- `ADDED` executable stdlib contract-drift guard under `tests/prototypes/frontend-preprod-contracts.py`.
- `CHANGED` frontend workflow so touched durable behavior is expected to carry production-shaped contracts before `apps/web` migration.
- `NO_CHANGE` accepted Home visual build remains B1; B2 responsive defect remains open.
- `NO_CHANGE` no production framework/package versions, backend endpoints, database schema or auth transport strategy are selected by this scope.
