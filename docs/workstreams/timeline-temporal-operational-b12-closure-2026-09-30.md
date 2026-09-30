# B12-D and B12 — qualified whole-block closure

- **Date:** 2026-09-30
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CLOSED / USER-REPORTED GENERAL ACCEPTANCE
- **Persistence frontier:** Alembic `20260929_93`; no B12-D schema or Dictionary change
- **CI:** not used; local automated acceptance is run by the user

## Delivered boundary

B12-A diagnoses current Plan conflict truth; B12-B generates bounded alternatives; B12-C admits one explicitly reviewed move through the guarded B04-D operation; B12-D integrates the two linked Activities, qualified Dependency, Actual evidence, hard earliest-start rule, Movement Policy, candidate review, pending confirmation and accepted Schedule read. Alternatives and pending proposals are separate from the current Schedule. The solver does not claim capacity or availability, and no automatic multi-item move or AI scheduling authority is added.

## Evidence and limits

B12-A/B/C passed their respective user-run focused gates, recorded in their closure documents. The original B12-D integrated candidate at `758914479f80bea378e431b31900ee3d890366f4` passed the reported full local gate: generated check (397 files), both typechecks, 11 web tests, 9 backend tests, Ruff and 20 PostgreSQL/catalog tests in 41.19s. That proof predates the real-app click-path repairs.

The original real-app preparation exposed missing authoring controls for a hard earliest-start rule and Movement Policy on a placed Activity. Later repairs added the controls and their API, followed by a fixed-Schedule action. A final correction kept creation of an unplaced Activity free of duration and zone choices, placed the zone choice beside the existing duration input under **Colloca**, and corrected the walkthrough. On the final placement correction, local web typecheck and the Planning Tray test file passed (5 tests). The earlier click-path repair had local frontend/API-client typechecks, targeted web tests and Ruff; its new backend contract/PostgreSQL tests, generated-source check and whole selected gate have no supplied user-run rerun. Do not claim those checks passed on the final candidate.

The user received the complete real-app steps and start commands, then reported “okok chiudiamo va tt diciamo cosi passiamo a sistemare quella meda di ui al prossimo step”. This is a general user acceptance to close and move on. No itemized report of the final Record/Mix candidate, pending proposal, separate confirmation, reload, or negative case was supplied. Do not describe those particular observations as individually witnessed.

## Continuation

B12-D and parent B12 close on this **qualified user-reported acceptance**, with the affected automated rerun and itemized manual observations remaining explicit verification gaps. The next planned UI work is B14 Temporal Create Completeness: account for every editable Create field as canonical, handed off, read-only or hidden. B07 UI/UX consolidation follows B14; the user requested the UI as the next area of work. B14/B07 should keep unsupported behavior visible rather than claim that B12's missing itemized proof was performed.
