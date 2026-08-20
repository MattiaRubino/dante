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

## 2026-08-20 — Access A3.4 selected review checkpoint

- `ADDED` complete Access review contract/state model covering sign-in, DANTE-owned staged sign-up, verification, recovery/reset, provider handoff/error/linking, re-auth and lightweight first-run handoff.
- `ADDED` Italian/English `access.*` locale registry mirrored from the selected standalone prototype.
- `ADDED` semantic `--dante-access-*` token family for the reviewed light Access surface without changing Home token values.
- `ADDED` exact hash-verified A3.4 standalone archive and browser QA evidence.
- `CHANGED` Access selected checkpoint from A3.1 to A3.4.
- `VISUAL_ONLY` replaced the generic desktop orbit decoration with a large cropped locked Living Orbits symbol at the selected muted opacity.
- `REJECTED` A3.5 full-opacity corner-mark experiment as too visually dominant.
- `NO_CHANGE` Home/B1/B2 implementation, backend auth/session/provider contracts, production React/framework choice and locked brand masters.
