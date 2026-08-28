# B2 Central Stage v16 — saved WIP

This archive preserves the user-reviewed B2 working state from 2026-08-20 without promoting it to the accepted Home build.

Base: accepted B1 Context Rail v1 output, SHA-256 `a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0`.

Saved states:

- full Mondi state + compact 3-visible Signal carousel;
- partial Mondi state with two existing sphere positions rendered as ghost `+` slots.

Known open defect: global browser/window resize can still break the overall monolithic Home geometry. B2 remains open. Logo/name alignment is also intentionally deferred to the next bounded work.

The patch artifacts use marker `DANTE_GZIP_BASE64_UNIFIED_DIFF_V1` and are unified diffs against the accepted B1 standalone output, gzip-compressed deterministically (`mtime=0`) and Base64 encoded.

Exact reconstructed outputs are recorded in `docs/frontend/home/checkpoints/b2-central-stage-v16-wip.md`.
