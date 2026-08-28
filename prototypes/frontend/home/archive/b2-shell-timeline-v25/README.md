# B2 Home Shell + Timeline v25 archive

This directory preserves the deterministic implementation layer for the user-reviewed **B2 Home Shell + Timeline Quick Add v25** checkpoint.

Base authority:

- B2 Home Visual Skin v24;
- B2 Home Branding v23;
- B2 Central Stage v22 no persistent add.

Files:

```text
shell-v24-to-v25.js
```

Transform integrity:

```text
size       8391 bytes
SHA-256    6e9d3e25270f8d73482aa6a2f48f709e1ffc2324007dde2fa6d40cdea90d1d69
```

The layer performs only the accepted shell/timeline delta:

- real sticky edge-to-edge application bar with 24 px internal inset;
- DANTE + Search left, Home/Mondi/Oggi centered;
- `Crea` first in the right utility group, followed by legacy Review, launcher and account;
- outer Home-shell side-frame cleanup carried by the accepted reviewed state;
- real timeline quick-add grid item before month/year;
- temporal header grid `add / month / now / week / actions`;
- prototype-only quick-add bridge to the existing global `Crea` surface.

It does not change v24 atmosphere/palette, v23 identity, Mondi/Segnali data/behavior, Context Rail semantics, backend contracts or persistence.

User-reviewed local evidence:

```text
DANTE_Home_v24_v13_PLUS_REFINED_MONTH_RIGHT.html
size       80922 bytes
SHA-256    0b9491525a99643837dc42e4150113db50d00bf7ff73549ea4fd3f9994adcdf9
```

The review wrapper itself is not duplicated here; this archive stores the compact deterministic transform that carries the durable checkpoint delta.
