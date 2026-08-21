# DANTE — Wordmark Master v0

- **Status:** LOCKED MASTER
- **Workstream:** `prototype/brand-identity`
- **Approved:** 2026-08-18
- **Locked:** 2026-08-18
- **Approved direction:** A1 — Classical Modern
- **Approved reference:** `assets/brand/wordmark/reference/dante-wordmark-a1-approved-reference-2026-08-18.png`
- **Locked vector master:** `assets/brand/wordmark/master/dante-wordmark-master-v0.svg`
- **Production QA:** `docs/brand/dante-wordmark-master-v0-qa.md`

## Purpose

This document records the authoritative standalone `DANTE` wordmark selected from the reviewed wordmark directions.

The accepted direction is **A1 — Classical Modern**. The production objective is source fidelity: preserve the approved visible letterforms and spacing as deterministic vector geometry rather than replace them with a similar font or reinterpret the design.

## Correction history

An earlier 2026-08-18 attempt created a wordmark from substitute-font outlines and normalized them toward the approved reference. That attempt was rejected because it was not the approved A1 letterform. The entire invalid lock scope was reverted before this master was created.

The current Master v0 therefore uses a **direct contour trace of the user-approved A1 raster reference**. It does not use Inter, another substitute font, or regenerated typography as production geometry.

The rejected attempt remains only in Git history for provenance and must not be used.

## What LOCKED MASTER means

The exact current SVG is the authority for the standalone DANTE wordmark.

The lock freezes:

- the visible uppercase `DANTE` letter geometry;
- relative letter proportions;
- inter-letter spacing / tracking;
- the approved horizontal rhythm;
- the `530 × 110` reference-aligned master framing;
- master fill `#222F37`.

Future signatures and exports must derive from this exact SVG. Do not retype `DANTE`, substitute another font, regenerate it from an image prompt, or independently redraw the letters.

## Approved A1 visual contract

The selected direction is intentionally restrained:

- uppercase sans-serif appearance;
- clean geometric / humanist character;
- subtle classical influence without becoming serif, epigraphic or fantasy-styled;
- open but controlled spacing;
- high legibility;
- adult, calm and contemporary presence;
- no decorative Greek gimmicks;
- no AI / crypto / occult visual language;
- no texture, glow, 3D or raster effects in the master.

## Production construction

The master is **outline-only SVG geometry** traced directly from the approved raster reference.

```text
viewBox              0 0 530 110
runtime font         none
SVG <text> element   none
master fill          #222F37
canvas               transparent
```

The source raster is approval evidence; after lock the SVG is the production authority.

Anti-aliased raster edge pixels are not semantic design instructions. The trace captures the approved visible silhouette while converting it into deterministic vector geometry.

## Repository integrity

```text
approved reference Git blob
bb60108342fb29d5fa32ca7977c98b1c5c04820c

locked SVG Git blob
5985990461a25833e04db5b8972e9c4569d54273

QA-board Git blob
bfd8b8284f9eb1a39a1dc631f8755c554a858ac5
```

The SVG payload SHA-256 prepared and visually approved before the write is:

```text
dd8c609669a4f6a323df820607fcac25c563875f0b6deb6eb95499efdaf03afa
```

Repository state remains the final source of truth.

## Relationship to the DANTE symbol

The wordmark master is independent from the already locked symbol master:

```text
assets/brand/logo/master/dante-symbol-master-v0.svg
```

Locking the wordmark does **not** approve a symbol + wordmark composition. Horizontal and stacked signatures require a separate visual-composition scope using both masters unchanged.

## Downstream boundary

Still separate:

- horizontal symbol + wordmark signature;
- stacked symbol + wordmark signature;
- lockup clear-space / relative scale rules;
- production export family;
- dark/light contextual derivatives;
- app icon;
- compact brand sheet;
- mascot / brand character;
- global `LifeOS` → `DANTE` rename.

Any future change to the letter geometry or spacing requires an explicit versioned master revision.
