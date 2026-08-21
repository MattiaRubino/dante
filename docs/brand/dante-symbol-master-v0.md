# DANTE — Symbol Master v0

- **Status:** LOCKED MASTER
- **Workstream:** `prototype/brand-identity`
- **Created:** 2026-08-17
- **Corrected:** 2026-08-17
- **Locked:** 2026-08-17
- **Source reference:** `assets/brand/logo/reference/dante-living-orbits-approved-reference-2026-08-17.png`
- **Locked vector master:** `assets/brand/logo/master/dante-symbol-master-v0.svg`
- **Production QA:** `docs/brand/dante-symbol-master-v0-qa.md`

## Purpose

This document records the authoritative vector master of the approved DANTE / Living Orbits symbol.

The objective is **not to reinterpret or redesign the logo**. The locked master preserves the selected raster reference closely enough that future production work can generate deterministic derivatives without image-generation drift or geometric reinvention.

Master v0 has completed its required production QA and is now **LOCKED**.

## What LOCKED MASTER means

The exact current SVG is the authority for the DANTE symbol.

The lock freezes:

- the visible geometry;
- the three orbit silhouettes;
- opening relationships;
- external point placement and size;
- characteristic tapered / feathered terminal behavior;
- transparent master canvas / bounds;
- embedded master fills `#222F37` and `#EA5C12`.

Future assets must be derived from this master rather than independently redrawn, regenerated or approximated.

A lock does **not** mean the entire brand system is complete. Wordmark, signatures, app icon, export family, brand-sheet rules and mascot remain separate downstream scopes.

## 2026-08-17 correction — previous Master v0 superseded

The first deterministic Master v0 committed earlier in this workstream was rejected during visual comparison because it was too interpretive relative to the approved reference. It preserved the broad concept but changed actual geometry, opening relationships, terminal character and overall visual balance too much.

That earlier construction remains in Git history but is **SUPERSEDED** and must not be used as production geometry.

Historical characteristics of the superseded construction included:

- `1000 × 1000` viewBox;
- synthetic shared optical center around `x=470, y=520`;
- nominal outer/middle/inner radii of roughly `350 / 245 / 150`;
- nominal body widths around `42 / 37 / 32`;
- parametrically designed openings and taper behavior;
- candidate palette based on `#1F2328`, `#332A25`, `#9A5A33`, `#E87A2F`, `#F07A2E` and presentation ivory `#F4EEE6`.

Those values describe the rejected reconstruction only.

## Current locked master — source-faithful tracing

The current `dante-symbol-master-v0.svg` derives from the approved raster reference by tracing its visible shapes rather than rebuilding the mark from invented circle/radius parameters.

It preserves:

- three open orbital forms;
- empty center;
- one external orange point in the upper-right area;
- the accepted staggered openings;
- the reference's relative orbit proportions and visual weight;
- tapered / brush-like terminals, including characteristic split/feathered details where they materially define the mark;
- charcoal-dominant mass with orange regions positioned according to the selected image;
- no wordmark inside the symbol master;
- no glow, 3D, shadow, metallic treatment or extra central element.

The source-faithful tracing was visually accepted as the correct basis and then passed the required production QA. Geometry is therefore no longer an open-ended design variable.

## Vector construction

### Coordinate system

The locked tracing uses:

```text
viewBox = 0 0 1254 1254
```

The master canvas is transparent.

Warm ivory remains a presentation/background treatment rather than baked artwork.

### Geometry model

The master stores the visible traced regions as deterministic filled vector polygons instead of ideal mathematical rings with generic stroke caps.

This intentionally preserves asymmetric and gestural details that materially belong to the approved reference.

A light contour simplification was applied before lock only to remove redundant pixel-step points while maintaining visual equivalence. Further simplification was tested during QA and was not justified because it did not materially improve 16/24 px behavior.

### Locked artwork bounds

Inside the `1254 × 1254` viewBox the validated artwork bounds are:

```text
x: 188 → 1073
y: 164 → 1077
```

Transparent margins are approximately:

```text
left   188
top    164
right  181
bottom 177
```

These bounds passed optical review and are part of the current locked master canvas.

## Locked master colors

The exact master contains two direct fills:

| Role | HEX | Status |
|---|---|---|
| Primary dark / charcoal | `#222F37` | locked in Master v0 |
| Warm orange | `#EA5C12` | locked in Master v0 |

These values are the colors embedded in the locked symbol artwork.

Future brand-system work may create named tokens, accessibility mappings and context-specific derivatives, but it must not silently alter the locked master file.

Warm ivory remains a presentation/background treatment and is not included inside the SVG master.

## Preserved visual contract

Production use must continue to preserve:

- three distinct open orbit forms;
- intentionally empty center;
- exactly one external orange point;
- no rounded-cap redesign;
- tapered / pointed / controlled gestural terminals;
- charcoal as the dominant visual mass;
- visible orange distribution rather than a hard generic half-black/half-orange split;
- clean adult consumer-brand character;
- no generic AI sparkle, neural, chatbot or assistant symbolism;
- no literal Dante Alighieri / Inferno / occult treatment;
- `Living Orbits` only as an internal concept label, not public-facing copy.

## Production QA result

The authoritative QA record is:

```text
docs/brand/dante-symbol-master-v0-qa.md
```

QA board:

```text
assets/brand/logo/qa/dante-symbol-master-v0-production-qa.png
```

The exact remote/local master identity was verified by matching Git blob SHA:

```text
834bc5820fd7065d326a47832cfcb55163f84a76
```

Reference silhouette comparison returned `IoU = 0.9581` as a technical fidelity check.

Required rendering tests passed at:

```text
16 px
24 px
32 px
48 px
128 px
512 px
1024 px
```

Monochrome dark and monochrome light/inverse versions also passed at all required sizes without geometry changes.

## Small-size rule

The locked master itself must not be simplified merely to optimize favicon rendering.

Current guidance:

- `24 px` and above — normal unmodified-symbol use passes;
- `16 px` — recognition passes, although micro-terminal character is naturally reduced;
- a dedicated small-size/favicon optical derivative may be created later only if platform/export testing demonstrates a real need.

Any optical derivative must remain traceable to this master and may not replace it as authority.

## Monochrome contract

The symbol remains structurally recognizable when all visible shapes are rendered in one color.

Production derivatives must therefore include at least:

- monochrome dark;
- monochrome light / inverse.

These derivatives must preserve locked geometry.

## Allowed downstream production work

The master lock now permits deliberate derivative scopes for:

- standalone production color SVG;
- PNG export family;
- monochrome dark;
- monochrome light/inverse;
- dark-background treatment;
- optional small-size optical derivative if later justified;
- app-icon masters and platform exports;
- favicon/small UI exports;
- DANTE wordmark and signature combinations after the wordmark is separately approved.

## Changes that require reopening the master

The following are **not** ordinary export work and require a deliberate master-revision decision:

- repositioning the external point;
- changing orbit silhouettes or openings;
- redrawing the orbits as generic circles;
- replacing tapered/feathered terminals with round caps;
- materially changing orange coverage inside the master;
- changing the embedded master colors;
- adding or removing symbol elements;
- changing the master viewBox/artwork framing in a way that alters normal rendering.

A future revision must be versioned rather than silently overwriting the meaning of `LOCKED MASTER v0`.

## Explicitly not decided by this lock

Master v0 does not decide:

- final DANTE wordmark typeface;
- wordmark tracking or custom letterforms;
- horizontal or stacked signatures;
- app-icon background treatment;
- full dark-mode brand system;
- complete brand-sheet clear-space/usage rules;
- mascot / brand character;
- trademark/domain decisions;
- global LifeOS → DANTE naming migration.

## Authority rule

`assets/brand/logo/master/dante-symbol-master-v0.svg` is now the **LOCKED MASTER v0**.

All normal production assets must derive from it. Do not regenerate the logo from prompts, reconstruct it from memory, or use the earlier superseded parametric geometry as a substitute.
