# B2 Home Visual Skin v24

This archive preserves the user-approved Home palette/background working baseline from 2026-08-22.

Base lineage:

```text
B2 Central Stage v22 no persistent add
  -> B2 Home Branding v23
  -> B2 Home Visual Skin v24
```

## Durable payload

```text
skin-v23-to-v24.css
size       2949 bytes
SHA-256    a3bfd6e6a09d627055b9b92c0c90f3ac25f832086beaf3a54229d59b4548fb5c

dante-home-cosmos-mirrored-v1.webp.b64.part00 .. part05b
restore-v24-background.py
restored WEBP size       37482 bytes
restored WEBP SHA-256    8ce54b557e7e1cd436ecd6ac672491e619bc61111788b9b0551eeef257f74002
restored geometry        1920 x 1080
```

The exact WEBP source is stored as ordered Base64 text parts so the binary can be reconstructed deterministically through the repository connector. Run `restore-v24-background.py` inside this archive; it concatenates the ordered parts, decodes them, refuses to write on size/SHA mismatch, and restores `dante-home-cosmos-mirrored-v1.webp` beside the CSS. Apply the CSS layer after the v23 branding layer.

## Accepted visual result

- charcoal DANTE-aligned shell/surfaces;
- restrained orange emphasis using the official `#EA5C12` accent family;
- accepted cosmos/neural Home atmosphere behind the UI;
- central stage remains translucent enough for the atmosphere to read;
- obsolete legacy network canvas `#netCanvas` is hidden;
- `#fxCanvas` and `.magnet-line` are intentionally untouched so existing Mondi effects/animation remain available.

## Rejected regression

A broader cleanup that also hid `#fxCanvas` and `.magnet-line` caused Mondi spheres to lose animation/effects. That state is rejected and is not represented by this archive.

## Review evidence

Final accepted local wrapper:

```text
DANTE_Home_ONE_BACKGROUND_MIRRORED_no_net_only.html
size       64678 bytes
SHA-256    2fde54ec03d4540bb7799342e7e5df2b99fa843dbebc395ae93eeb56df4b5e05
```

Exact scope and QA qualification are recorded in `docs/frontend/home/checkpoints/b2-visual-skin-v24.md`.

B2 remains open; this checkpoint does not close final responsive/accessibility QA or production token migration.
