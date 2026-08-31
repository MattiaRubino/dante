# DANTE — World Focus VFX Research / WF-V4

**Status:** implementation candidate — visual approval pending  
**Date:** 2026-08-31  
**Visual candidate:** `wf-v4-candidate`  
**Frozen dependencies:** WF0 structure `1.0.0`, WF-G3 geometry `wf-g3`

## Target

World Focus must read as an immersive cosmic / magic-portal environment rather than a stroked ellipse or luminous tube.

The approved WF-G3 ellipses remain structural reference geometry, but they are **not a hard clipping boundary for VFX**.

Current visual boundary:

```text
WF-G3 origin ellipse
= invisible trajectory / seed / reveal guide

worldFocus.workspace
= protected application area

route area outside workspace
= usable VFX field
```

The workspace remains rectangular and structurally frozen. VFX may occupy corners, side gutters and top/bottom peripheral space but must not alter or clip the workspace.

## External implementation research

### LinearAbilityExtThreeJS — Fire Portal / particle system

Repository: `achrefelouafi/LinearAbilityExtThreeJS`  
License: MIT, Copyright (c) 2026 mohamedachrefelouafi.

Relevant source concepts:

- `src/abilities/FirePortalAbility.js`
- `src/particles/ParticleSystem.js`

The important reusable design insight is architectural rather than copied source:

- the portal contour acts as an **emitter**, not the whole visual;
- sparks are emitted tangentially from the contour;
- drag/turbulence/swirl create long curved trajectories;
- the opening is progressively drawn by a moving head / scribe;
- particle motion is evaluated primarily on the GPU rather than simulated particle-by-particle in the main-thread render loop;
- fixed-capacity pooled/ring-buffer approaches avoid allocation growth.

DANTE independently implements these concepts in native WebGL2 against its own frozen WF-G3/workspace geometry.

### r3f-portal

Repository: `ryan-j-parker/r3f-portal`.

Useful confirmation:

- shader material driven by `uTime`;
- procedural noise/displacement is appropriate for living portal material;
- React/animation controls should feed uniforms rather than rebuild DOM geometry.

DANTE does not adopt the Three/R3F runtime from this example.

## Why native WebGL2

DANTE did not already depend on Three.js / React Three Fiber when this surface was designed. Adding a 3D framework solely for this effect would increase dependency and bundle surface without providing product-semantic value.

WF-V4 therefore uses one route-owned WebGL2 canvas with two GPU passes:

1. **Peripheral field pass** — nebula/plasma/filament density over the non-workspace region;
2. **Particle pass** — fixed-capacity GPU-rendered sparks/streaks seeded from the WF-G3 origin ellipse and moved analytically along tangent/outward trajectories.

No React DOM node exists per particle.

## Performance contract for the candidate

- one WebGL2 context;
- two draw calls per animated frame;
- capped DPR (`1.4` currently);
- particle count bounded by viewport class;
- particle attributes allocated/generated when the renderer is configured, not each frame;
- RAF pauses when the document is hidden;
- `prefers-reduced-motion` renders a settled static frame;
- WebGL failure falls back without changing World Focus structure;
- no World Focus visual may reauthor WF-G3 or workspace geometry.

## Entry motion

WF-V4 introduces a first reveal candidate inspired by the scribe/emitter pattern:

```text
entry
→ reveal head travels around the invisible WF-G3 origin trajectory
→ peripheral field becomes available behind the head
→ particle emission becomes available for reached sectors
→ settled ambient field continues
```

This is a visual capability, not a navigation dependency. Future user settings may disable ornamental motion without changing the stable World Focus end state.

## Visual approval rule

`wf-v4-candidate` is not frozen.

Do not promote it to a visual baseline until real-browser screenshots/video are reviewed. Tuning or replacing the VFX renderer must not reopen WF0 or WF-G3 unless an explicit structural/geometry change is separately approved.
