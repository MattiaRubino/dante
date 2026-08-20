# DANTE — Shared Frontend Prototype Resources

This directory contains cross-surface pre-production resources that should remain easy to replace without hunting through surface implementation.

## Current authorities

- `theme/tokens.css` — semantic visual tokens for new/touched UI.
- `locales/it-IT.json` — current Italian product copy keys.
- `locales/en-US.json` — working English equivalents.
- `contracts/` — framework-neutral state/view-model/responsive contracts for production-shaped prototype work.
- `fixtures/` — synthetic data shaped against those frontend contracts; never backend/canonical truth.

These resources are intentionally compatible with later production-frontend migration, but they do not decide the production framework/runtime.

## Boundary rule

```text
Domain/canonical model
!= backend DTO
!= frontend view model
!= component state
```

Mock and future real-backend adapters must feed equivalent frontend-facing contracts. Components do not consume database/ORM shapes or make ad-hoc HTTP calls as their architectural boundary.

## Visual/copy rule

New/touched surface code should consume stable semantic IDs/keys and tokens. Legacy inline values are migrated incrementally when their owning surface is touched; do not perform broad visual refactors without a bounded gate and non-regression proof.
