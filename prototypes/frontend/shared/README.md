# DANTE — Shared Frontend Prototype Resources

This directory contains cross-surface pre-production resources that should remain easy to replace without hunting through surface implementation.

## Current authorities

- `theme/tokens.css` — semantic visual tokens for new/touched UI.
- `locales/it-IT.json` — current Italian product copy keys.
- `locales/en-US.json` — working English equivalents.

These resources are intentionally compatible with later production-frontend migration, but they do not decide the production framework/runtime.

## Rule

New/touched surface code should consume stable semantic IDs/keys and tokens. Legacy inline values are migrated incrementally when their owning surface is touched; do not perform broad visual refactors without a bounded gate and non-regression proof.
