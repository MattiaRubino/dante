# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Rule:** protected `main` stores durable workstream records/evidence, not active live/session handoffs

## Purpose

This directory indexes durable workstream records that remain useful after a branch or phase is closed. It is not the permanent home for chat/session save-games.

Temporary branch-operational files may exist on an active feature branch when they materially improve continuity, but before protected-main integration they must pass `../development/documentation-lifecycle-policy.md`:

```text
active branch handoffs
→ knowledge coverage
→ current truth moved to durable current docs
→ important rationale/evidence retained
→ optional ONE consolidated branch-history record
→ temporary handoffs removed
```

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
Access pre-backend frontend        CLOSED / ACCEPTED / branch closure integration
Full-stack Access/Auth vertical    NOT STARTED ON A DEDICATED BRANCH
```

## Durable closed/integrated records

### Backend

- `backend-scaffold.md` — CP1–CP5 production backend scaffold closure/integration evidence, integrated via PR #24.
- `../archive/branches/2026-08-feature-logical-postgresql.md` — consolidated non-authoritative CP6 branch history.

Current CP6/database truth lives in:

- `../database/README.md`
- `../database/dictionary/`
- `../development/backend-cp6-05-whole-database-qa.md`

### Frontend

- `frontend-foundation.md` — frontend engineering foundation design/architecture closure, integrated via PR #22.
- `frontend-materialization.md` — closed production materialization evidence, integrated via PR #28.
- `frontend-materialization-integration.md` — durable integration/calibration/future-activation evidence for PR #28.
- `../frontend/access.md` — current durable contract for the accepted pre-backend Access frontend materialization.
- `../archive/branches/2026-08-feature-access-frontend.md` — consolidated non-authoritative history for `feature/access-frontend`.

The Access branch-local workstream record and live handoff are intentionally not retained after knowledge consolidation. The later full-stack Access/Auth product vertical must start from current protected `main` on a fresh bounded branch; the closed `feature/access-frontend` branch is not a permanent reusable frontend line.

### Engineering / architecture preparation

- `engineering-foundation.md` — closed engineering foundation, integrated via PR #21.
- `physical-model.md` — closed/selected Physical target, integrated via PR #15.
- `pre-physical-coherence.md` — definitive pre-Physical coherence closure, integrated via PR #13 with later alignment as recorded.

### Domain / Logical

Domain and Logical workstream continuations are historical operational records for phases that are now closed. Their semantic current truth is owned by:

- `../domain/README.md`
- `../logical-model/README.md`

The documentation knowledge audit retained detailed continuation/register material only where unique requirements, rationale, assumptions, rejected alternatives, traceability or validation evidence made destructive compaction unsafe. Historical workstream files never override the newer current entry points.

## Historical/superseded planning

- `backend-foundation.md` — historical pre-Engineering-Foundation planning; not current backend implementation authority.

Historical planning records may later move to `docs/archive/` or leave the working tree if knowledge coverage proves Git/current authorities are sufficient.

## `today-home.md`

`today-home.md` is a separate Home/Today product/UX workstream record. Its authority is limited to the scope explicitly stated by that file; it does not override production engineering, current frontend vertical or backend/database authority.

## Active branch-local workstreams

No post-CP6 full-stack product vertical is recorded as active by this index at Access-frontend closure time.

When a new vertical starts, it may have one durable branch-local record plus temporary live/session notes only when they materially improve continuity. Before integration, all temporary handoffs must again pass the documentation lifecycle gate.

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

A closed workstream is not a reusable permanent feature branch and does not remain active merely because its historical record still exists.

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
