# DANTE Mascot Hybrid Master v0 QA

- **Status:** QA PASS — package/structural
- **Branch:** `prototype/brand-identity`
- **Validated:** 2026-08-19

## QA artifact

```text
assets/brand/mascot/qa/dante-mascot-master-v0-production-qa.png
```

SHA-256:

```text
1e4946303b049873f00ee2786b52fd44ad153cfc845e168a32ab6b41899b295a
```

## Validated inputs

Approved reference SHA-256:

```text
d8f719e695466d8fc0104d30acfe671e82cb27f21c769122203cf38b432b4bf6
```

Hybrid master SHA-256:

```text
0760ade2f884426fb7dcbf422ed90349c9de6aad3f2ce5275c4ae08ef039f28b
```

## Checks

- exact approved PNG preserved as canonical visual reference;
- SVG render layer points only to that canonical reference;
- render layer uses the native `1254 × 1254` dimensions with no master-level scaling;
- transparent `1536 × 1536` production framing is explicit;
- vector construction guides are present as non-rendering structural layers;
- no symbol, wordmark or primary-signature dependency is introduced;
- pre-write visual review of the accepted mascot/framing was explicitly approved by the user.

## Renderer note

The current execution environment does not allow a reliable browser/Cairo render of the relative linked raster resource. QA therefore does **not** claim a pixel-comparison result for the linked SVG. Runtime/export rendering must be rechecked when the first concrete derivative/export pipeline is introduced. The source reference itself remains unchanged and authoritative.

## Verdict

**QA PASS — LOCKED HYBRID MASTER v0**, with downstream renderer/export verification deferred to the first derivative/export scope.
