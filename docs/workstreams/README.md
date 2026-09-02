# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-02
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

Protected-main shared-foundation truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Current high-level state on `feature/access-auth`:

```text
Domain Model                       CLOSED
Logical Model                      CLOSED / 57 OF 57
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
Engineering Foundation             CLOSED / ACCEPTED
Frontend Foundation                CLOSED / INTEGRATED
Frontend Materialization           CLOSED / PASS / INTEGRATED
Backend CP1–CP5 Scaffold           CLOSED / DIRECT QA / INTEGRATED
Backend CP6 Database               CLOSED / DIRECT QA / INTEGRATED VIA PR #42
Access pre-backend frontend        CLOSED / ACCEPTED

Full-stack Access/Auth vertical    ACTIVE / M5 FINAL EXTERNAL ACCEPTANCE OPEN
M1 Access Visual / UX Freeze       CLOSED / ACCEPTED
M2 Auth Architecture Freeze        CLOSED / ACCEPTED
M3 Signin + AuthSession Spine      CLOSED / ACCEPTED
M4 Signup/Recovery/Reauth          CLOSED / ACCEPTED
M5 Groups 1–3                     COMPLETE / ENGINEERING PASS
M5 Group 4 Web engineering         AUTOMATED QA PASS
Local password/passkey UAT         PASS
Real Google UAT                    PASS
Email architecture                 ACCEPTED DIRECTION
Email platform implementation      OPEN
Real Internet email UAT            OPEN
Real Apple registered-domain UAT   DEFERRED / OPEN
```

The former index text that said `M2 ACTIVE / M3 NOT STARTED / production Auth NOT STARTED` is superseded and was stale relative to the executable branch.

## Active branch-local Access/Auth workstream

Primary current record:

- `access-auth.md` — durable current branch-local workstream authority and continuation entry point.

Current review/evidence:

- `access-auth-m5-review-2026-09-02.md` — engineering/UAT/deprecation/external-benchmark evidence.

Current email architecture:

- `../architecture/access-auth-email-delivery.md`
- `../decisions/ADR-012-email-delivery-platform.md`

Temporary active-branch continuation:

- `access-auth-m5-live-handoff-2026-09-02.md` — branch-operational only; must be consolidated/removed before protected-main integration.

Historical/superseded:

- `access-auth-m5-live-handoff-2026-08-29.md` — historical milestone-time handoff, not current authority.
- `access-auth-m4-live-handoff-2026-08-29.md` — historical milestone-time handoff, not current authority.
- `access-auth-m4-m7-execution-plan.md` — useful historical planning where still accurate, but current execution status is owned by `../ROADMAP.md` and `access-auth.md`.

## Current Access/Auth branch state

```text
branch                         feature/access-auth
intended worktree              /home/mattia/projects/dante
protected-main relationship    branch-local newer Auth truth; not yet integrated
accepted Alembic head          20260831_13
PostgreSQL                     18.6
DB topology                    83 tables / 5 views / 15 routines /
                               75 triggers / 156 indexes / 85 FKs / 233 CHECKs

reviewed product checkpoint    ab2716abe40de658d99d1908ba31c5d5744e3c57
real-SMTP UAT tooling          9c0587af5891249d8a6e6b6a5d6e3af6934c6943
```

Automated final product-code evidence at `ab2716...`:

```text
format/typecheck/lint/architecture     PASS
Web unit/component                     68 / 68 PASS
Auth Playwright HTTPS                  60 / 60 PASS
Chromium / Firefox / WebKit            PASS through canonical suite
```

Live UAT additionally proved real Windows Hello passkeys, password/passwordless lifecycle, session rotation, anti-lockout, real Google Identity Services and direct PostgreSQL coherence.

Do not reopen accepted implementation blocks absent direct defect evidence.

## Current macro-roadmap

```text
M1  Access Visual / UX Freeze                         CLOSED
M2  Auth Architecture Freeze                         CLOSED
M3  Email/Password Signin + AuthSession Spine        CLOSED
M4  Signup + Verify + Recovery + Reset + Reauth      CLOSED
M5  Google + Apple + Passkeys + Explicit Linking     ACTIVE / FINAL EXTERNAL ACCEPTANCE OPEN
    ├── engineering Groups 1–3                       COMPLETE / PASS
    ├── Group 4 Web QA                               PASS
    ├── local password/passkey UAT                   PASS
    ├── real Google UAT                              PASS
    ├── email architecture                           ACCEPTED
    ├── email provider/operations qualification      NEXT
    ├── durable Email Platform implementation        OPEN
    ├── real Internet email UAT                      OPEN
    └── Apple real registered-domain UAT             DEFERRED / OPEN
M6  Native Mobile Access                             FUTURE / OPTIONAL / RE-GATE
M7  Security Hardening + Home Handoff + Closure      PLANNED
```

## Email workstream direction inside M5

Email is no longer an unspecified “pick an SMTP vendor” task.

Accepted direction:

```text
DANTE owns email lifecycle/state
external specialist owns last-mile delivery
PostgreSQL transactional outbox is durable target
Amazon SES API v2 is primary production adapter target
SMTP is retained for deterministic tests/UAT/compatibility
```

Still open:

```text
SES operational/provider qualification
exact outbox/delivery persistence design
sensitive OTP/recovery payload protection
SES API adapter
provider event ingestion
bounce/complaint suppression lifecycle
sender domain + SPF/DKIM/DMARC
real inbox signup/recovery UAT
failure/ambiguous-outcome proof
```

`SELECTED != IMPLEMENTED != DIRECT PASS` remains binding.

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
- `../frontend/access.md` — current durable contract for the accepted full-stack Access Web surface.
- `../archive/branches/2026-08-feature-access-frontend.md` — consolidated non-authoritative history for `feature/access-frontend`.

The closed Access-frontend branch is not a permanent reusable frontend line. Current full-stack Access/Auth continues on `feature/access-auth`.

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

The authenticated Access → real Home handoff remains M7 work on this vertical; current successful Auth UAT legitimately lands on the accepted Access/onboarding return rather than pretending Home is already integrated here.

## Operational continuation rule

Before continuing work:

1. read `../PROJECT-STATUS.md` and `../ROADMAP.md`;
2. read `../development/agent-operating-manual.md` and documentation lifecycle policy;
3. verify exact current branch/remote HEAD and relation to `main`;
4. if continuing Access/Auth, read `access-auth.md` completely;
5. read `access-auth-m5-review-2026-09-02.md`;
6. for email, read ADR-012 + `../architecture/access-auth-email-delivery.md` before researching or writing code;
7. consume the subsystem authorities relevant to the next gate;
8. do not let an old handoff/workstream record override newer current truth;
9. version-sensitive external claims require current official evidence.

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
NO PASS WITHOUT EXECUTED EVIDENCE
DO NOT REOPEN ACCEPTED WORK WITHOUT DEFECT EVIDENCE
```

Durable architecture changes belong in current specs/ADRs. Historical workstream records never override later accepted current truth.
