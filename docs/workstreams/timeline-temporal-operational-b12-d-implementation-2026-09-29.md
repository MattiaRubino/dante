# B12-D — whole-block integration — implementation checkpoint

- **Status:** ORIGINAL LOCAL GATE PASSED / B12 CLOSED ON QUALIFIED USER ACCEPTANCE; POST-REPAIR RERUN UNREPORTED
- **Approved scope:** `timeline-temporal-operational-b12-d-scope-2026-09-29.md` (user approved 2026-09-29)
- **Entry:** B12-A/B/C closed on focused proof; Alembic `20260929_93`
- **Persistence:** no B12-D schema or Dictionary change; click-path repair adds Movement Policy API and generated client
- **Acceptance:** one real Home/Timeline walkthrough after automated proof, before B12 and B12-D closure

The new `test_b12_d_whole_block.py` composes a two-Activity Plan, directional Actual-qualified Dependency, a hard earliest-start conflict, bounded candidates, a reviewed B04-D pending proposal and explicit confirmation. It reads Timeline before and after the effect, checks that a changed Actual prevents acceptance without a Schedule move, refreshes the review, then checks replay, Plan/Dependency identity and accepted current Schedule after fresh application instances. Another self Person cannot search the Plan.

The new Home panel test exercises the click path through diagnosis, unknown prerequisite, candidate search, old/new review, pending proposal, confirmation and refreshed current Schedule. It also checks unsupported placement and blocked Movement Policy do not offer review. Capacity and availability remain visibly unassessed.

The user-run original gate passed on commit `75891447`: generated 397, both typechecks, 11 focused web tests, 9 backend tests, Ruff and 20 PostgreSQL/catalog tests. It exposed an incomplete real-app path: the Python integration test provisioned the hard conflict and confirmation Policy directly, but the Home panel did not let a user set either for a placed Activity. The repair adds a self-scoped CAS Movement Policy endpoint and two controls under the selected Plan Step. The hard rule uses the existing Temporal Constraint endpoint. The candidate basis is refreshed after each write. No persistence migration is needed. The repaired generated API source, backend contract test and frontend click test are included; the user's affected gate and real-app observation remain pending. Exact commands and clicks are in `timeline-temporal-operational-b12-d-gate-2026-09-29.md`. The user subsequently accepted qualified B12-D/B12 closure; see `timeline-temporal-operational-b12-closure-2026-09-30.md`. The final affected rerun and itemized walkthrough remain unreported.
