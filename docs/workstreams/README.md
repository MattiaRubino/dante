# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Rule:** protected `main` stores durable workstream records/evidence, not active live/session handoffs

## Purpose

This directory indexes durable workstream records that remain useful after a branch or phase is closed.

It is **not** the permanent home for chat/session save-games.

Temporary branch-operational files may exist on an active feature branch when needed for continuity, but before protected-main integration they must pass the lifecycle gate in:

`../development/documentation-lifecycle-policy.md`

```text
active branch handoffs
→ knowledge coverage
→ current truth moved to durable current docs
→ important rationale/evidence retained
→ optional ONE consolidated branch-history record
→ temporary handoffs removed
```

Protected `main` should never require a reader to find the newest `live-handoff` in order to know project truth.

## Current project/workstream state

Protected-main current truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Current high-level state:

```text
Domain Model                       CLOSED
Logical Model                      CLOSED
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
Engineering Foundation             CLOSED / ACCEPTED
Frontend Foundation                CLOSED / INTEGRATED
Frontend Materialization           CLOSED / PASS / INTEGRATED
Backend CP1–CP5 Scaffold           CLOSED / DIRECT QA / INTEGRATED
Backend CP6 Database               CLOSED / DIRECT QA / INTEGRATED VIA PR #42
Access frontend                    ACTIVE / UNMERGED ON feature/access-frontend
Post-CP6 backend product vertical  NOT STARTED ON A DEDICATED BRANCH
```

The active Access frontend workstream is **branch-local** on `feature/access-frontend`. Its `docs/workstreams/access-frontend.md` and temporary live handoff exist on that branch and are not protected-main authority until reconciliation/integration. The temporary live handoff must be removed/consolidated before that branch merges.

## Durable closed/integrated records

### Backend

- `backend-scaffold.md` — CP1–CP5 production backend scaffold closure/integration evidence, integrated via PR #24.

CP6 no longer uses an active `logical-postgresql` handoff as current routing. Its final durable state is represented by current database authority plus final QA, with a consolidated non-authoritative branch history under:

- `../archive/branches/2026-08-feature-logical-postgresql.md`

Current CP6/database truth lives in:

- `../database/README.md`
- `../database/dictionary/`
- `../development/backend-cp6-05-whole-database-qa.md`

### Frontend

- `frontend-foundation.md` — frontend engineering foundation design/architecture closure, integrated via PR #22.
- `frontend-materialization.md` — closed production materialization evidence, integrated via PR #28.
- `frontend-materialization-integration.md` — durable integration/calibration/future-activation evidence for PR #28.

These records do not represent active generic frontend foundation/materialization work anymore.

### Engineering / architecture preparation

- `engineering-foundation.md` — closed engineering foundation, integrated via PR #21.
- `physical-model.md` — closed/selected Physical target, integrated via PR #15.
- `pre-physical-coherence.md` — definitive pre-Physical coherence closure, integrated via PR #13 with later alignment as recorded.

### Domain / Logical

Domain and Logical workstream files/continuations are historical operational records for phases that are now closed.

Their **semantic current truth** is not owned by this directory. Start instead at:

- `../domain/README.md`
- `../logical-model/README.md`

The documentation knowledge audit classified the large Domain/Logical continuation families conservatively:

```text
current status/routing
→ consolidated current entry points

concept/reference continuations
→ retained when they contain durable specification payload

validation/checkpoint continuations
→ retained as evidence/history where they contain meaningful test/rationale payload

large Logical registers/ledgers
→ retained because assumptions, rejected alternatives, traceability and tests are not losslessly duplicated by the Whole summary
```

No destructive compaction was performed merely to reduce file count. A future compaction may proceed only when the complete logical family passes the lossless knowledge-coverage gate.

Historical Domain/Logical workstream records and continuation files must not override their newer current entry points merely because they are detailed or chronologically later within an old phase.

## Historical/superseded planning

- `backend-foundation.md` — historical pre-Engineering-Foundation planning; not current backend implementation authority.

Historical planning records may later move to `docs/archive/` or leave the working tree entirely if knowledge coverage proves Git/current authorities are sufficient.

## `today-home.md`

`today-home.md` is a separate Home/Today product/UX workstream record. Its authority is limited to the scope explicitly stated by that file; it does not override production engineering, current frontend vertical or backend/database authority.

## Branch-local active workstreams

An active unmerged workstream should have one durable branch-local record when needed, plus temporary live/session notes only when they materially improve continuity.

Example current branch-local work:

```text
feature/access-frontend
→ docs/workstreams/access-frontend.md
→ docs/workstreams/access-frontend-live-handoff.md  TEMPORARY / BRANCH-LOCAL ONLY
```

Before integration:

```text
access-frontend-live-handoff.md
→ knowledge coverage
→ durable Access current/closure docs updated
→ optional one branch-history record if useful
→ DELETE temporary handoff
```

Do not copy branch-local live handoffs into `main` as historical documentation.

## Operational continuation rule

Before continuing work:

1. read `../PROJECT-STATUS.md` and `../ROADMAP.md`;
2. read development operating/safety/lifecycle policy;
3. verify exact current branch and relation to `main`;
4. if the target workstream is active and unmerged, read its branch-local durable record;
5. use a temporary handoff only when the active branch genuinely needs one;
6. consume the relevant accepted model/architecture/reference/code/tests;
7. do not let an old workstream record override newer current truth.

## Closed-workstream rule

Once a workstream is integrated:

```text
current semantics / architecture
→ current subsystem docs / ADRs

implementation truth
→ code / migrations / tests

important acceptance evidence
→ durable QA / validation record

useful branch narrative
→ at most one branch-history record

chat/session continuation detail
→ Git history only
```

A closed workstream is not a reusable permanent feature branch and does not remain “active” merely because its historical record still exists.

## Current carry-forward engineering rules

```text
SELECTED != IMPLEMENTED
SELECTED != DIRECT PASS
UNMERGED BRANCH TRUTH != protected-main TRUTH
VERSION-SENSITIVE CLAIMS REQUIRE CURRENT EVIDENCE
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
CURRENT SPECIFICATION != CHRONOLOGICAL DIARY
```

Durable architecture changes belong in current specs/ADRs. Historical workstream records never override later accepted current truth.
