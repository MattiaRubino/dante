# LifeOS Home vNext — Soft Surfaces working snapshot

This directory preserves the exact 2026-08-15 Home vNext standalone prototype as a deterministic delta from the already archived `integrated-v1` baseline.

## Identity

Final restored file:

- filename: `lifeos_home_vnext_soft_surfaces.html`
- bytes: `297872`
- SHA-256: `5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56`

Delta:

- source baseline SHA-256: `66f1f8af4795aa579394ec07bc872798141907c6c216f5af0daed4f96e5c32b4`
- patch file SHA-256: `d5923360b211c8cf4941554a1749fb61a3e661ec6b72befb1708e96b560271a2`
- stored as: `home_vnext_from_integrated_v1.patch.gz.b64`

## Restore

1. Restore the existing `integrated-v1` checkpoint so you have the exact baseline HTML with SHA-256 `66f1f8af...`.
2. Decode/decompress the delta:

```bash
base64 -d home_vnext_from_integrated_v1.patch.gz.b64 | gzip -d > home_vnext_from_integrated_v1.patch
```

3. Apply it to the restored baseline:

```bash
patch restored_integrated_v1.html home_vnext_from_integrated_v1.patch -o lifeos_home_vnext_soft_surfaces.html
```

4. Verify:

```bash
sha256sum lifeos_home_vnext_soft_surfaces.html
```

Expected:

`5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56`

This is a **visual/behavior prototype checkpoint**, not production React code and not a final information-architecture decision. See `docs/phase-4/home-vnext-soft-surfaces-v1.md`.
