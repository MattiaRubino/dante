# DANTE — Home Retained Complete Baseline

This directory keeps the exact complete standalone A2 Home baseline so later accepted prototype work remains recoverable and auditable.

## Baseline identity

`home.html`

- size: `748625` bytes
- SHA-256: `986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df`
- Git blob SHA: `fd9788212fbbd1ee40e53271cc39cedd9275b341`

This file is intentionally **not overwritten by B1**.

## Current accepted Home

The current accepted prototype is **B1 Context Rail v1**, reconstructed deterministically by:

```text
cd prototypes/frontend/home/work
python build.py
```

Expected result:

```text
size     760281 bytes
SHA-256  a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

The build applies the accepted B1 override to this retained complete baseline.

## Why both are kept

- this directory gives an exact complete recovery point;
- `work/` gives maintainable source/build logic;
- accepted checkpoint docs identify the exact resulting standalone output;
- Git + change-log preserve the semantic/history trail.

See `docs/frontend/home/current-checkpoint.md`.
