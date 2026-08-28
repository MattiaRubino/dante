# B2 Home Branding v23 — DANTE identity alignment

This archive preserves the user-approved Home branding pass from 2026-08-22.

Base behavioral/structural oracle remains **B2 Central Stage v22 no persistent add**.

## Base outputs

```text
v22 FULL
size       761337 bytes
SHA-256    18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76

v22 PARTIAL
size       760579 bytes
SHA-256    f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

## Shared v23 branding layer

The branding change is independent from central-stage data density, so the **same deterministic layer applies to both FULL and PARTIAL v22 outputs**:

```text
brand-v22-to-v23.js
size       4101 bytes
SHA-256    a7a6a08dc2eb174cafe63c6e8b60d90244bfbfa6b98ef57e644ed7bb2a8132df
```

Apply this layer after either v22 output is loaded.

## Accepted visual result

Topbar:
- locked DANTE symbol geometry is retained with its approved charcoal/orange fills;
- locked DANTE wordmark geometry is retained;
- only the wordmark foreground is rendered white for the current dark Home surface;
- this white wordmark treatment is a frontend dark-surface derivative, **not a new brand master**.

AI/conversational surface:
- the old placeholder orb/`LifeOS` identity is replaced by the locked DANTE symbol only;
- no `DANTE` or `LifeOS` text label is shown beside the AI symbol.

## Brand authorities

Assets are pinned to the integrated brand commit:

```text
db02da603f3779d8c7fcb1d7601f6f66f8a23241

assets/brand/logo/master/dante-symbol-master-v0.svg
assets/brand/wordmark/master/dante-wordmark-master-v0.svg
```

## Non-regression

This checkpoint does **not** alter:
- Mondi/Segnali behavior or data states;
- v22 no-persistent-add semantics;
- timeline/day ribbon;
- context rail;
- global Create placement/behavior;
- Home background;
- general palette;
- backend/domain/persistence semantics.

Exact scope and QA qualification are recorded in `docs/frontend/home/checkpoints/b2-branding-v23.md`.
