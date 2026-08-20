# DANTE Access A3.1 — approved review checkpoint

Status: **APPROVED REVIEW CHECKPOINT / NOT PRODUCTION / NOT BACKEND-FROZEN**

This archive preserves the exact A3.1 HTML prototype approved for continued design work on 2026-08-20. It includes the refined DANTE-owned email/password sign-up flow and remains the restore point before visual background experiments.

## Artifact identity

- Source filename: `dante-access-a3-signup-review.html`
- Size: `86687` bytes
- SHA-256: `1e9161c6f22ab3355eda674355f857132b59208986867b01d27f6760378f03c1`
- XZ payload size: `18164` bytes
- XZ SHA-256: `ae18b29478f0fe5a34070af8d58ccc091be855e9b3cff18156cae6ab4114827f`

## Archive parts

The XZ payload is Base64-split only to avoid transport truncation in the GitHub connector. Concatenate parts in lexical order; the split does not change the artifact.

- `part-001.b64` — 5000 Base64 characters; file SHA-256 `5e93b2d387f044ea7402355fdef02c76c6ec53e07a54296a87ffcac5ac78b403`
- `part-002.b64` — 5000 Base64 characters; file SHA-256 `987a64ae581f2afe2f5b2549a75d6f09253517df1065f2e8009fe244b35a2c66`
- `part-003.b64` — 5000 Base64 characters; file SHA-256 `c93d813ae41a50c0f9829ebd8845e821894c011c2cde1d0355105b5b30008477`
- `part-004.b64` — 5000 Base64 characters; file SHA-256 `d96743d94dfc586787ab6546a0c9a4f5420035bcf23a7674f2e9d2eca27f33cf`
- `part-005.b64` — 4220 Base64 characters; file SHA-256 `5902380bea203d4a608f67f45965c77edf6203aa0a4356d0e478ceb1f0742803`

## Restore

```bash
cat part-*.b64 | tr -d '\n\r' | base64 -d | xz -d > dante-access-a3-signup-review.html
sha256sum dante-access-a3-signup-review.html
```

The restored SHA-256 must be:

```text
1e9161c6f22ab3355eda674355f857132b59208986867b01d27f6760378f03c1
```

## Scope note

A3.1 is the approved design-review reference before the decorative background experiment. Fine polish may still change during production frontend implementation and backend integration. This checkpoint does not freeze backend auth/session/password policy.
