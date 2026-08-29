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

Current high-level state on `feature/access-auth`:

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
Access pre-backend frontend        CLOSED / ACCEPTED
Full-stack Access/Auth vertical    ACTIVE
M1 Access Visual / UX Freeze       CLOSED / PASS WITH DEFERRED INTEGRATION CHECKS
M2 Auth Architecture Freeze        ACTIVE
M3 Signin + AuthSession Spine      NOT STARTED
```

## Active branch-local workstream

- `access-auth.md` — single durable branch-local workstream record, authority map, decision register, definitive seven-macro-phase roadmap and continuation entry point for `feature/access-auth`.

Current Access/Auth state:

```text
branch                         feature/access-auth
baseline                       f011e252b6a294a12c38927ef2d528244ea1fee6
last closed macro-phase        M1 — Access Visual / UX Freeze
active macro-phase             M2 — Auth Architecture Freeze
production Auth module         NOT STARTED
Auth DB migrations             NOT STARTED
real Access API wiring         NOT STARTED
native Mobile Access           NOT STARTED
first executable target        M3 — email/password signin + AuthSession spine
```

M2 is intentionally architecture/security work before production Auth code. It must ratify deployment topology, Web session/cookie/CSRF/CORS behavior, core Account/AuthSession semantics, multi-session lifecycle, password implementation, passkey-ready/MFA-compatible boundaries, email comparison, API/error contract, M3 concurrency/transactions, generated-client boundary and the exact M3 test harness before migrations/endpoints begin.

Independent platform work also exists on a separately pinned branch:

- `platform-observability.md` — OpenTelemetry/Faro/Alloy/Grafana Cloud Free,
  PostgreSQL observer, dashboards, alerts, failure handling and acceptance
  evidence for `feature/platform-observability`.

That workstream does not advance or override the Access/Auth macro-roadmap and
does not absorb later Access commits merely because both touch shared backend
runtime boundaries.

The current definitive macro-roadmap is:

```text
M1  Access Visual / UX Freeze                         CLOSED
M2  Auth Architecture Freeze                         ACTIVE
M3  Email/Password Signin + AuthSession Spine        NOT STARTED
M4  Signup + Verify + Recovery + Reset + Reauth      NOT STARTED
M5  Google + Apple + Passkeys + Explicit Linking     NOT STARTED
M6  Native Mobile Access                             NOT STARTED
M7  Security Hardening + Home Handoff + Closure      NOT STARTED
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
- `../frontend/access.md` — current durable contract for the accepted Web Access frontend and its current full-stack integration obligations.
- `../archive/branches/2026-08-feature-access-frontend.md` — consolidated non-authoritative history for `feature/access-frontend`.

The closed Access-frontend branch-local workstream record and live handoff are intentionally not retained after knowledge consolidation. The current full-stack Access/Auth workstream started from protected `main` on `feature/access-auth`; the closed `feature/access-frontend` branch is not a permanent reusable frontend line.

### Engineering / architecture preparation

- `engineering-foundation.md` — closed engineering foundation, integrated via PR #21.
- `physical-model.md` — closed/selected Physical target, integrated via PR #15.
- `pre-physical-coherence.md` — definitive pre-Physical coherence closure, integrated via PR #13 with later alignment as recorded.

### Domain / Logical

Domain and Logical workstream continuations are historical operational records for phases that are now closed. Their semantic current truth is owned by:

- `../domain/README.md`
- `../logical-model/README.md`

Historical workstream files never override newer current entry points.

## Historical/superseded planning

- `backend-foundation.md` — historical pre-Engineering-Foundation planning; not current backend implementation authority.

Historical planning records may later move to `docs/archive/` or leave the working tree if knowledge coverage proves Git/current authorities are sufficient.

## `today-home.md`

`today-home.md` is a separate Home/Today product/UX workstream record. Its authority is limited to the scope explicitly stated by that file; it does not override production engineering, current frontend vertical or backend/database authority.

## Operational continuation rule

Before continuing work:

1. read `../PROJECT-STATUS.md` and `../ROADMAP.md`;
2. read development operating/safety/lifecycle policy;
3. verify exact current branch and relation to `main`;
4. if continuing Access/Auth, read `access-auth.md` completely;
5. read `../frontend/access.md` and the subsystem authorities required by the active macro-phase;
6. use a temporary handoff only when the active branch genuinely needs one;
7. consume relevant accepted model/architecture/reference/code/tests;
8. do not let an old workstream record override newer current truth.

## Macro-phase closure rule

For Access/Auth, a macro-phase is not CLOSED until the current record captures:

```text
accepted decisions
+ implementation/evidence if any
+ deferred/open items
+ reopen triggers
+ updated decision register
+ affected durable authority docs
+ next active macro-phase / safe action
```

A phase must never rely on chat memory for durable truth.

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
NEW CHAT != NEW BRANCH
```

Durable architecture changes belong in current specs/ADRs. Historical workstream records never override later accepted current truth.
