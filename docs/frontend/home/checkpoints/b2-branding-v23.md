# B2 Home Branding v23 — DANTE identity alignment

**Branch:** `prototype/frontend`  
**Date:** 2026-08-22  
**Status:** **USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN**  
**Base:** B2 Central Stage v22 no persistent add

## Decision

The Home identity anchors are aligned to the approved DANTE brand without reopening Home structure or behavior.

### Topbar

Accepted composition:
- DANTE symbol uses the locked master geometry and approved charcoal/orange colors;
- DANTE wordmark uses the locked master geometry;
- wordmark foreground is rendered white on the current dark topbar;
- no extra card, white panel, mount, glow, or decorative container is added.

The white wordmark is a **dark-surface frontend derivative only**. It does not modify or supersede the locked brand master.

### AI surface

Accepted composition:
- show the locked DANTE symbol only;
- remove the old placeholder orb;
- remove the visible `LifeOS` label;
- do **not** add a visible `DANTE` text label beside the symbol.

## FULL / PARTIAL propagation

The accepted change touches shared shell/AI identity markup only and is independent from stage population.

Therefore one common deterministic layer is applied to both existing v22 states:

```text
FULL base SHA-256
18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76

PARTIAL base SHA-256
f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3

shared layer
prototypes/frontend/home/archive/b2-branding-v23/brand-v22-to-v23.js

layer size
4101 bytes

layer SHA-256
a7a6a08dc2eb174cafe63c6e8b60d90244bfbfa6b98ef57e644ed7bb2a8132df
```

No FULL-only branding rule exists. No PARTIAL-only branding rule exists.

## Brand source authority

Pinned integrated brand commit:

```text
db02da603f3779d8c7fcb1d7601f6f66f8a23241
```

Source assets:
- `assets/brand/logo/master/dante-symbol-master-v0.svg`
- `assets/brand/wordmark/master/dante-wordmark-master-v0.svg`

No geometry is redrawn or regenerated.

## User review

The final FULL treatment was explicitly accepted by the user after rejecting:
- a generated mockup unrelated to the actual Home;
- a white backing panel around the signature;
- an all-light symbol treatment;
- a visible `DANTE` label inside the AI card;
- a dark/unreadable wordmark.

Accepted result:
- topbar symbol = charcoal/orange;
- topbar `DANTE` wordmark = white;
- AI identity = symbol only.

## QA qualification

```text
v22 behavioral baseline                PRESERVED
brand geometry                         SOURCE MASTER / PINNED
FULL branding review                   USER PASS
PARTIAL propagation                    SHARED LAYER
fresh 24-case browser matrix           NOT CLAIMED
fresh full accessibility rerun         NOT CLAIMED
fresh partial visual browser review    NOT CLAIMED
```

The next visual scope may review Home background/atmosphere and palette. Those decisions must not be folded retroactively into this checkpoint.

## Explicit non-change

No change to:
- `home.stage.continuity` / Mondi;
- `home.stage.signals` / Segnali;
- central-stage geometry;
- `Crea` placement or semantics;
- Capture/Resolution semantics;
- timeline behavior;
- responsive contract;
- backend/API/Domain/logical/physical semantics;
- production frontend framework choices.

B2 remains open.
