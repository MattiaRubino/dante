# B12-A — Current-truth conflict diagnosis — closure

- **Status:** CLOSED / PROVEN on focused user-run local gate, 2026-09-29
- **Implementation:** `61289587e9496ed9a9543fc199ab1ddf31094355`
- **Walkthrough clarification:** `db6a568de8d2907ed99d8cdb9f91c7577a266411`
- **Source DB head:** `20260929_92`; no B12-A migration
- **Scope:** `timeline-temporal-operational-b12-a-scope-2026-09-29.md`

The authenticated Home Plan control diagnoses current Plan, linked Activity Schedule placements, supported hard Temporal Constraints and active qualified Dependencies. It reports a known hard violation, blocked prerequisite, unknown/unsupported basis or no known conflict only within supported rules. It does not search or accept a replacement Schedule, infer free capacity or mutate canonical state.

## User-run evidence

The user pulled the branch through `db6a568` and reported the complete command output:

| Gate | Result |
| --- | --- |
| Generated-source determinism | PASS — 389 files current |
| API client and web typechecks | PASS / PASS |
| Focused web component tests | 4 passed / 2 files |
| B12-A OpenAPI contract | 1 passed |
| Ruff on changed backend paths | PASS |
| B12-A and B13-D PostgreSQL integration plus current catalog probes | 11 passed in 26.14s |

The PostgreSQL test covers Record → Mix unknown, non-occurrence blocked and corrected satisfied results alongside a hard duration violation, current Schedule/Plan non-effects, self ownership and stale Plan rejection. The generated client and web panel are checked on the same pulled worktree.

**Acceptance boundary:** This is a focused automated B12-A closure. The user explicitly reserved the real-app walkthrough for B12-D, immediately before closing parent B12. No B12-A real-app acceptance is claimed. B12-B candidate generation requires a separately approved scope; B12-C governs admission; B12-D proves their integrated product path.
