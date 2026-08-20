# DANTE Access A3 — review checkpoint

Status: **REVIEW CHECKPOINT / NOT ACCEPTED / NOT CURRENT**

This archive preserves the exact A3 HTML prototype reviewed on 2026-08-20 before the email/password sign-up flow is refined.

## Artifact identity

- Source filename: `dante-access-a3-review.html`
- Size: `74373` bytes
- SHA-256: `8818ff2430efc53dfa357521620a54c496de97c502b538f2909bf07ff91f67ce`
- XZ payload size: `15512` bytes
- XZ SHA-256: `a71eab79c5514a69c194723cc380d1da07175268b60a786ce8b5d71322eba8cd`

## Archive parts

The XZ payload is Base64-split only to avoid transport truncation in the GitHub connector. Concatenate parts in lexical order; the split does not change the artifact.

- `part-001.b64` — 5200 Base64 characters; file SHA-256 `55eaed411e990c5758273cb90f934e6cb4aa5ce66dd6b2bf45ed04627f784aa6`
- `part-002.b64` — 5200 Base64 characters; file SHA-256 `d5e1a5c998c8645b568f1bfede74ba0d441681f29c1dbba70ab6e85ad58e1f8e`
- `part-003.b64` — 5200 Base64 characters; file SHA-256 `3d1c937dcfe14fd1a748603fb1e89e62a43044a5935ce37bc7c2570843db540e`
- `part-004.b64` — 5084 Base64 characters; file SHA-256 `54f22c636c4d51048865b57f1962f6f28446fb23510dcdbfb02275dff5fae6e7`

## Restore

```bash
cat part-*.b64 | tr -d '\n\r' | base64 -d | xz -d > dante-access-a3-review.html
sha256sum dante-access-a3-review.html
```

The restored SHA-256 must be:

```text
8818ff2430efc53dfa357521620a54c496de97c502b538f2909bf07ff91f67ce
```

## Scope note

A3 is intentionally frozen only as a design-review reference. It must not be treated as an accepted Access contract, production frontend, auth/backend contract, or final onboarding flow. The next design scope refines DANTE-owned email/password account creation while preserving the A3 visual-system direction and the existing canonical onboarding/first-run boundaries.
