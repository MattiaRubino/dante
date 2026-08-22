# B2 Home Visual Skin v24 — charcoal/orange palette + cosmos atmosphere

**Branch:** `prototype/frontend`  
**Date:** 2026-08-22  
**Status:** **USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN**  
**Base:** B2 Home Branding v23 over B2 Central Stage v22 no persistent add

## Decision

The current Home working visual baseline is promoted from the branding-only v23 state to the user-reviewed **v24 visual skin**.

v24 is intentionally a bounded frontend-prototype skin pass. It changes palette/background presentation and removes one obsolete decorative network canvas; it does not reopen Home structure, stage semantics, timeline behavior, Context Rail meaning, or backend/domain contracts.

## Accepted palette direction

The accepted working palette replaces the generic navy/purple emphasis with DANTE-aligned charcoal surfaces and restrained orange emphasis.

Prototype skin values:

```text
surface            #151D21
surface-raised     #1B252A
control            #202B30
text-primary       #F2F4F2
text-secondary     #B2BDC1
text-muted         #7D8A90
accent             #EA5C12
accent-soft        rgba(234,92,18,.095)
accent-border      rgba(234,92,18,.255)
```

This checkpoint records the **approved working prototype appearance**. It does not yet rewrite `prototypes/frontend/shared/theme/tokens.css` or declare these preview `--f-*` variables to be the final production semantic-token names. Token productionization remains a later bounded implementation task.

The current preview also renders the existing topbar `Crea` control with orange fill as part of the skin. This is a visual treatment only: `Crea` placement, Create-vs-Capture semantics and backend behavior remain explicitly open/unchanged.

## Accepted background / atmosphere

The Home shell uses the accepted 1920×1080 cosmos/neural artwork as a fixed cover background, with the stage kept translucent enough for the atmosphere to read through without changing layout.

Deterministic archive representation:

```text
prototypes/frontend/home/archive/b2-visual-skin-v24/
  dante-home-cosmos-mirrored-v1.webp.b64.part00
  dante-home-cosmos-mirrored-v1.webp.b64.part01
  dante-home-cosmos-mirrored-v1.webp.b64.part02
  dante-home-cosmos-mirrored-v1.webp.b64.part03a
  dante-home-cosmos-mirrored-v1.webp.b64.part03b
  dante-home-cosmos-mirrored-v1.webp.b64.part04a
  dante-home-cosmos-mirrored-v1.webp.b64.part04b
  dante-home-cosmos-mirrored-v1.webp.b64.part05a
  dante-home-cosmos-mirrored-v1.webp.b64.part05b
  restore-v24-background.py

restored file   dante-home-cosmos-mirrored-v1.webp
size            37482 bytes
SHA-256         8ce54b557e7e1cd436ecd6ac672491e619bc61111788b9b0551eeef257f74002
format          WEBP RGB
geometry        1920 × 1080
```

The restore script concatenates the ordered Base64 parts and validates both exact byte size and SHA-256 before writing the WEBP beside the CSS, so the accepted background is reproducible without silently accepting a corrupted binary transfer. The artwork is a Home atmosphere asset, not a replacement for the locked DANTE brand masters.

## Shared v23 -> v24 layer

```text
prototypes/frontend/home/archive/b2-visual-skin-v24/skin-v23-to-v24.css
size       2949 bytes
SHA-256    a3bfd6e6a09d627055b9b92c0c90f3ac25f832086beaf3a54229d59b4548fb5c
```

The layer contains exactly three bounded concerns:
- palette-F working skin overrides;
- cosmos background/stage translucency;
- removal of the obsolete `#netCanvas` decorative network only.

It does **not** hide or override `#fxCanvas` or `.magnet-line`.

## Regression caught and corrected before save

An intermediate cleanup attempt hid `#netCanvas`, `#fxCanvas` and `.magnet-line` together. User review detected that the Mondi spheres had lost animation/effects.

That intermediate state is **rejected and not the saved baseline**.

The accepted fix starts from the pre-cleanup working preview and hides **only `#netCanvas`**. `#fxCanvas` and `.magnet-line` remain untouched, restoring the prior Mondi motion/effect behavior while removing the unwanted legacy network overlay.

## User-reviewed preview evidence

The exact final local review wrapper accepted immediately before this checkpoint was:

```text
DANTE_Home_ONE_BACKGROUND_MIRRORED_no_net_only.html
size       64678 bytes
SHA-256    2fde54ec03d4540bb7799342e7e5df2b99fa843dbebc395ae93eeb56df4b5e05
```

The repository does not need to duplicate that local review wrapper: its durable v24 payload is the v23 baseline plus the archived CSS layer and the deterministic, hash-verified background reconstruction above.

## QA qualification

```text
final combined visual review by user       PASS
Mondi regression after broad cleanup       DETECTED / REJECTED
final cleanup scope                         #netCanvas ONLY
#fxCanvas / .magnet-line overrides          NONE IN v24 LAYER
outer local review-wrapper JS syntax        PASS (node --check)
v22 Home semantics                          PRESERVED
v23 DANTE identity treatment                PRESERVED
fresh 24-case browser matrix                NOT CLAIMED
fresh accessibility rerun                   NOT CLAIMED
separate PARTIAL browser visual review      NOT CLAIMED
```

## Explicit non-change

No change to:
- `home.stage.continuity` / Mondi meaning or data contract;
- `home.stage.signals` / Segnali meaning or data contract;
- v22 no-persistent-add rule;
- timeline/day-ribbon semantics;
- Context Rail Capture/Resolution semantics;
- Create/Capture semantic separation;
- central-stage geometry or item-count rules;
- backend/API/Domain/logical/physical semantics;
- production frontend framework/runtime selection.

B2 remains open for the remaining shell/detail decisions and final responsive/visual/accessibility QA.
