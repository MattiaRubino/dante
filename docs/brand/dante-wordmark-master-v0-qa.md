# DANTE — Wordmark Master v0 Production QA

- **Status:** QA PASS
- **Date:** 2026-08-18
- **Workstream:** `prototype/brand-identity`
- **Approved direction:** A1 — Classical Modern
- **Master:** `assets/brand/wordmark/master/dante-wordmark-master-v0.svg`
- **Reference:** `assets/brand/wordmark/reference/dante-wordmark-a1-approved-reference-2026-08-18.png`
- **QA board:** `assets/brand/wordmark/qa/dante-wordmark-master-v0-production-qa.png`

## Scope

Validate that the user-approved A1 wordmark has been converted into a deterministic vector master **by direct tracing of the approved reference**, without substitute-font geometry, regeneration or typography redesign.

This QA does not approve any symbol + wordmark lockup, app-icon treatment, mascot, export pack or global product rename.

## Approval chain

```text
A1 direction selected
→ approved raster isolated
→ direct contour trace produced
→ reference vs trace shown side-by-side
→ user explicitly approved the traced result
→ repository write authorized
```

A prior substitute-font reconstruction was rejected and reverted before this scope. It is not part of Master v0 authority.

## Structural checks

```text
uppercase DANTE only                         PASS
direct trace of approved reference           PASS
substitute-font production geometry          0
SVG <text> dependency                        0
runtime font dependency                      0
transparent master canvas                    PASS
master fill #222F37                          PASS
unexpected decorative elements               0
```

## Reference fidelity

The production geometry was derived from the approved raster's visible contour rather than reconstructed from nominal font metrics.

A binary silhouette comparison is retained as a supporting technical check, but visual approval outranks threshold-dependent raster metrics because anti-aliasing changes the measured contour depending on threshold.

At the production trace threshold the silhouette comparison returned approximately:

```text
IoU ≈ 0.8944
```

This value is not used as the acceptance criterion by itself. The decisive gate was direct visual comparison of the approved reference and traced output, followed by explicit user approval.

## Rendering checks

The exact SVG was rendered at representative wordmark heights:

```text
24 px
32 px
48 px
74 px
128 px
```

Results:

```text
24 px     PASS
32 px     PASS
48 px     PASS
74 px     PASS
128 px    PASS
```

No additional small-size optical wordmark derivative is justified at this stage.

## Monochrome / inverse

The same locked geometry was reviewed as:

```text
charcoal #222F37 on light context             PASS
light / inverse on charcoal context           PASS
```

Inverse use changes fill only; it does not authorize geometry changes.

## Remote object identities

```text
approved reference Git blob
bb60108342fb29d5fa32ca7977c98b1c5c04820c

SVG Git blob
5985990461a25833e04db5b8972e9c4569d54273

QA board Git blob
bfd8b8284f9eb1a39a1dc631f8755c554a858ac5
```

## Master-lock verdict

```text
A1 USER APPROVAL                             PASS
DIRECT REFERENCE TRACE                       PASS
NO SUBSTITUTE FONT                           PASS
NO RUNTIME FONT DEPENDENCY                   PASS
STANDARD-SIZE LEGIBILITY                     PASS
MONOCHROME / INVERSE                         PASS
WORDMARK MASTER v0                           LOCKED
```

## Downstream boundary

Still separate:

- symbol + wordmark composition;
- horizontal / stacked signatures;
- lockup spacing and relative scale;
- logo export family;
- app icon;
- compact brand sheet;
- mascot / brand character;
- global `LifeOS` → `DANTE` rename.

Neither this QA nor the next lockup scope authorizes modification of the locked symbol master or the locked wordmark master.
