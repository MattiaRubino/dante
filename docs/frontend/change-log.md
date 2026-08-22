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

## 2026-08-20 — B2 Central Stage v21 responsive working baseline

- `ADDED` user-reviewed B2 v21 responsive checkpoint and deterministic full/partial delta archive from the saved v16 artifacts.
- `CHANGED` current B2 working oracle from v16 to v21 after resize hardening.
- `BEHAVIOR_CHANGED` central-stage rendering now follows real stage geometry during window/parent reflow rather than relying only on early global resize timing.
- `CHANGED` Continuity spacing can adapt enough to keep the five-sphere desktop target inside the narrow critical stage state.
- `CHANGED` Signal track remains centered and constrained to its intended inner stage footprint with a maximum of three complete visible items.
- `RENAMED` stable B2 projection vocabulary to technical IDs `home.stage.continuity` / `home.stage.signals` with locked visible names `Mondi` / `Segnali`; historical `Worlds` / `Stats` vocabulary is deprecated, not erased from history.
- `QA` user review accepted v21 as the current working visual/behavior baseline; static evidence reports zero duplicate IDs and zero inline-JS syntax failures.
- `QA_LIMIT` a fresh automated browser PASS for every one of the 24 matrix cases is not claimed in this write; the matrix remains the executable target for final QA.
- `OPEN` persistent/add affordance for full Mondi/Segnali/future projections remains undecided.
- `OPEN` DANTE logo/name alignment, palette review and background/atmosphere remain the next visual scope.
- `NO_CHANGE` no backend endpoint/schema, Domain model or production-framework selection is introduced.

## 2026-08-21 — B2 Central Stage v22 no persistent add

- `ADDED` user-reviewed B2 v22 checkpoint and deterministic full/partial delta archive from v21.
- `CHANGED` current B2 working oracle from v21 to v22.
- `BEHAVIOR_CHANGED` Home central stage is now explicitly a read/navigate/open projection rather than a configuration CRUD surface.
- `REMOVED` persistent/add-slot affordances from Home; there is no persistent `+` for Mondi or Segnali.
- `REMOVED` partial-Mondi ghost `+` slots; partial state now contains only real items.
- `CHANGED` true empty state may expose a contextual management CTA so the surface is not a dead end; the CTA opens the dedicated management/creation surface rather than mutating Home directly.
- `CHANGED` Mondi creation/edit/order/archive/removal and Segnali selection/configuration/order/removal are assigned to dedicated management surfaces outside Home.
- `CHANGED` machine-readable Home-stage contract from `0.1.0` to `0.2.0`; `ADD_REQUEST` is removed and `OPEN_MANAGEMENT` is the management-entry intent.
- `CHANGED` empty fixture active indexes to `null` and added an explicit empty fixture; no placeholder entity/item is manufactured.
- `QA` v0.2.0 stdlib contract-drift guard passes locally and verifies no persistent add, partial-real-items-only and empty-management-entry semantics.
- `QA_LIMIT` a fresh automated browser PASS for every 24 responsive matrix combination is still not claimed.
- `OPEN` DANTE logo/name alignment, palette review, background/atmosphere and final QA remain.
- `NO_CHANGE` no backend endpoint/schema, Domain model or production-framework selection is introduced.

## 2026-08-22 — B2 Home Branding v23

- `ADDED` user-reviewed B2 v23 branding checkpoint over the existing v22 structural/behavioral oracle.
- `ADDED` one deterministic shared branding layer for both FULL and PARTIAL v22 states; no variant-specific brand behavior is introduced.
- `CHANGED` topbar identity from the historical placeholder lockup to the approved DANTE symbol geometry plus approved wordmark geometry.
- `VISUAL_ONLY` topbar wordmark foreground is white on the current dark surface; the symbol retains approved charcoal/orange fills. This is a frontend dark-surface derivative, not a new brand master.
- `CHANGED` AI identity from placeholder orb + visible `LifeOS` label to the approved DANTE symbol only; no visible `DANTE` label is added there.
- `REJECTED` white backing panel around the brand signature, all-light symbol treatment, dark/unreadable wordmark, and text label beside the AI symbol.
- `PINNED` brand source geometry to integrated commit `db02da603f3779d8c7fcb1d7601f6f66f8a23241`.
- `NO_CHANGE` Mondi/Segnali behavior, v22 no-add semantics, timeline, context rail, `Crea`, background, general palette, backend/API/Domain semantics.
- `QA` FULL final visual treatment explicitly accepted by user; PARTIAL receives the identical shared layer.
- `QA_LIMIT` fresh 24-case browser matrix, accessibility rerun and separate PARTIAL browser visual review are not claimed.
- `OPEN` background/atmosphere, overall palette/color system, later explicit `Crea` placement review, and final QA remain.

## 2026-08-22 — B2 Home Visual Skin v24

- `ADDED` user-reviewed B2 v24 visual-skin checkpoint over v23 branding / v22 Home-stage semantics.
- `CHANGED` working Home palette from generic navy/purple emphasis to charcoal surfaces with restrained DANTE orange emphasis.
- `ADDED` accepted 1920×1080 cosmos/neural atmosphere, stored as ordered Base64 parts plus a size/SHA-verified restore script, and one shared v23 -> v24 CSS layer.
- `CHANGED` central-stage background opacity only enough to expose the accepted atmosphere; stage layout/geometry is unchanged.
- `REMOVED` obsolete decorative `#netCanvas` from the accepted visual composition.
- `REGRESSION_CAUGHT` an intermediate cleanup also hid `#fxCanvas` and `.magnet-line`, causing Mondi spheres to lose animation/effects; that state was rejected before save.
- `FIXED` final v24 cleanup hides only `#netCanvas`; `#fxCanvas` and `.magnet-line` are deliberately untouched.
- `VISUAL_ONLY` the existing `Crea` control is orange-filled in the accepted working skin; Create-vs-Capture semantics/placement remain open and unchanged.
- `NO_CHANGE` Mondi/Segnali contract, no-persistent-add rule, timeline, Context Rail semantics, backend/API/Domain/logical/physical semantics.
- `QA` final combined preview accepted by user after the Mondi regression fix; outer review-wrapper JavaScript passes `node --check`.
- `QA_LIMIT` fresh 24-case browser matrix, accessibility rerun, separate PARTIAL browser review and production semantic-token migration are not claimed.
- `OPEN` remaining shell/detail decisions, semantic-token productionization and final responsive/visual/accessibility QA.
