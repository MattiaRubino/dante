# B12-B — bounded Plan Step candidate search — closure

- **Status:** CLOSED / PROVEN on focused user-run local automated gate, 2026-09-29
- **Implementation:** `a5b487728c5c3ecc87ea76de230705cac954b47f`
- **DB head:** `20260929_92`; no B12-B migration
- **Scope:** `timeline-temporal-operational-b12-b-scope-2026-09-29.md`

The Home Plan diagnosis now offers a read-only search for up to three nearby, fixed-duration intervals for one linked Activity with one accepted absolute Schedule. Supported current hard Temporal Constraints filter the 15-minute grid in a ±12-hour start horizon; OR-Tools 9.15 CP-SAT selects the nearest alternatives. Dependency unknown/blocked, unsupported placement, model-scoped infeasibility and solver unknown are distinct. The response carries current material evidence and says capacity/availability were not assessed. No candidate changes a Schedule or becomes a Proposal/Decision.

## User-run evidence

The user pulled through `a5b48772` and supplied the complete output from one `set -e` gate in `~/projects/dante`:

| Gate | Result |
| --- | --- |
| Generated-source determinism | PASS — 393 files current |
| API client and web typechecks | PASS / PASS |
| Focused Plan UI tests | 3 passed / 2 files |
| Ruff on changed backend paths | PASS |
| B12-B solver/OpenAPI plus B12-A contract | 8 passed in 2.35s |
| B12-B/B12-A PostgreSQL integration and current catalog probes | 11 passed in 24.63s |

The PostgreSQL case covers ordered fixed-duration hard-rule alternatives, deterministic repeatability, unchanged Plan/Schedule, unknown/unsatisfied/satisfied qualified Dependency, unsupported/unplaced Step, hard-rule model infeasibility, changed constraint evidence, cross-Person isolation and stale Plan rejection. The source/client and backend tests ran against the same pulled revision. No CI or GitHub Actions were used.

**Acceptance boundary:** This closes focused automated B12-B. The integrated real-app walkthrough is reserved for B12-D immediately before parent B12 closure. B12-C governed admission requires a separate scope approval and proof.
