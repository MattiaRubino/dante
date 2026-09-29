# B12-D — whole-block integration — implementation checkpoint

- **Status:** IMPLEMENTED CANDIDATE / USER-RUN LOCAL GATE PENDING
- **Approved scope:** `timeline-temporal-operational-b12-d-scope-2026-09-29.md` (user approved 2026-09-29)
- **Entry:** B12-A/B/C closed on focused proof; Alembic `20260929_93`
- **Persistence:** no B12-D schema, Dictionary or generated API changes
- **Acceptance:** one real Home/Timeline walkthrough after automated proof, before B12 and B12-D closure

The new `test_b12_d_whole_block.py` composes a two-Activity Plan, directional Actual-qualified Dependency, a hard earliest-start conflict, bounded candidates, a reviewed B04-D pending proposal and explicit confirmation. It reads Timeline before and after the effect, checks that a changed Actual prevents acceptance without a Schedule move, refreshes the review, then checks replay, Plan/Dependency identity and accepted current Schedule after fresh application instances. Another self Person cannot search the Plan.

The new Home panel test exercises the click path through diagnosis, unknown prerequisite, candidate search, old/new review, pending proposal, confirmation and refreshed current Schedule. It also checks unsupported placement and blocked Movement Policy do not offer review. Capacity and availability remain visibly unassessed.

No application behavior was changed for this checkpoint. If the user's local PostgreSQL gate or real walkthrough exposes an integration defect, repair the owning layer, publish and rerun the affected proof. The authoring environment has no PostgreSQL service: the new PostgreSQL test collected successfully; Ruff passed; 11 focused web tests in five files and 9 backend contract/solver tests passed; web and API-client typechecks passed. The exact local commands are in `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. Do not close B12-D or B12 from this candidate alone.
