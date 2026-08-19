# DANTE — Home Current Prototype Oracle

This directory preserves the exact corrected standalone Home HTML accepted before the transition from the historical Phase 4 branch to `prototype/frontend`.

## Artifact identity

`home.html`

- size: `748625` bytes
- SHA-256: `986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df`
- Git blob SHA: `fd9788212fbbd1ee40e53271cc39cedd9275b341`

The HTML is migrated by reusing the exact existing Git blob. No compression, regeneration or semantic reconstruction is required.

Historical source lineage:

- branch: `prototype/phase-4-today-home`
- corrective source commit: `cb58b1528292398ccedeaedb60b44a4ff6e6235f`
- final historical branch state before migration: `861f73b2932f3092fe6dca5f37b77732bb32bc65`

The correction replaced an earlier wrong local variant and changed exactly one source line: `drRoadGrad` uses `gradientUnits:'userSpaceOnUse'` and percentage x coordinates.

## Status

This is an immutable **pre-production coded UX / visual-behavior oracle**, not production application code and not a Domain/Logical/Physical Model decision.

A later A2 scope may derive modular editable source under a separate `work/` path. A2 must not alter this oracle.

See:

- `docs/workstreams/frontend.md`
- `docs/frontend/home/current-checkpoint.md`
- `docs/frontend/research-index.md`
- `qa-static.json`
