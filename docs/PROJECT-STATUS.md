# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH
- **Last reconciled:** 2026-09-06
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` via PR #66
- **AI protected-main merge:** `431fb34029baeacc9ef9f721e9626b39ca10dd39` via PR #63
- **Home/World Focus protected-main merge:** `5258452d7bd4e7a2797922b00035a9068ba41167` via PR #65
- **Protected-main Alembic:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Pre-vertical closure record:** `workstreams/pre-vertical-foundation-closure-2026-09-06.md`

Protected `main` is the integration authority. The pre-vertical foundation is now protected-main truth through PR #66; the former feature branch is retired.

## 1. Current state

```text
Product / North Star                         CURRENT
Domain / Logical / Physical                  CLOSED / CURRENT
Engineering + Frontend + Backend CP1–CP6    CLOSED / ACCEPTED
PostgreSQL                                   18.6

Access/Auth M1–M5                            CLOSED / INTEGRATED
Shared Email Platform                        CLOSED / INTEGRATED
PostgreSQL Recovery                          CLOSED / INTEGRATED
Platform Observability                       CLOSED / INTEGRATED
AI deterministic low-level foundation        CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation            CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                      CLOSED / INTEGRATED VIA PR #66

AI production/private-data qualification     NOT CLAIMED
Apple registered-domain real UAT             BOUNDED DEFERRED / NON-BLOCKING
remote backup provider                       NOT ACTIVATED
production/cloud recovery                    NOT CLAIMED

Pre-vertical PV-01                           CLOSED / PASS
Pre-vertical PV-02                           CLOSED / PASS
Pre-vertical PV-03 A Scale Harness           CLOSED / PASS
Pre-vertical PV-03 B Whole-Branch QA         CLOSED / PASS
Pre-vertical PV-03 C Integration             CLOSED / PASS
```

There is no PV-04. QA findings were resolved inside PV-03 and did not create additional milestones.

## 2. Database truth

Current protected-main database truth:

```text
Alembic             20260906_18
tables              89
views                5
routines             18
triggers             77
physical indexes     173
foreign keys         91
CHECK constraints    272
```

The pre-vertical delta over the former `20260904_17` baseline is one `account_application_context` table, two routines, one trigger, one PK-backed index, two foreign keys and two CHECK constraints. Exact database/recovery authority remains `database/README.md` plus the executable migration/catalog/Dictionary/tests.

## 3. Pre-vertical foundation result

The integrated foundation closes the cross-cutting seams required before the first real product vertical:

```text
authenticated Account
→ admitted Principal
→ explicit DANTE application context
→ self Person
→ user/default timezone policy
→ effective request timezone
```

It also provides:

- application-issued UUIDv7 and reusable Clock/time primitives;
- named IANA timezone and DST edge handling;
- persistent LOCAL/DEV dogfood;
- exactly three deterministic product-independent personas;
- deterministic `small=12`, `medium=120`, `large=1200` scale plans;
- bounded real-PostgreSQL first-use convergence proof;
- normal Vite LOCAL `/api/v1` proxy topology aligned with the backend Auth origin.

Permanent distinctions remain intact:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual != Outcome != Observation
```

UUID ordering is never semantic chronology/currentness authority.

## 4. Acceptance evidence

The final implementation candidate had direct local evidence for:

```text
Backend Ruff format/lint                     PASS
Backend strict mypy                          PASS
Backend non-PostgreSQL tests                 457 PASS
AI deterministic eval tests                  22 PASS
Backend package build                        PASS
PostgreSQL 18.6 acceptance                   165 PASS

Frontend contracts                           PASS
Prettier / ESLint / TypeScript               PASS
architecture dependency check                PASS
generated-source determinism                 PASS
Web unit tests                               136 files / 636 tests PASS
production build                             PASS
Chromium Web E2E                             127 PASS
Firefox Timeline contract                    10 PASS
Mobile compatibility + Hermes bundle         PASS
```

Persistent dogfood seed/rerun and real browser email/password login were also exercised successfully during PV-02.

PR #66 required checks all passed before merge:

```text
Backend CI Gate                              PASS
Dependency Review                            PASS
Frontend CI Gate                             PASS
```

Detailed evidence and exact branch disposition live in `workstreams/pre-vertical-foundation-closure-2026-09-06.md`.

## 5. Recovery disposition

Historical CP07 database-local and CP08 application/Email reopen evidence remains valid only for the exact historical contracts it executed.

For the final pre-vertical candidate `21353469464f1371f9913dc78933f4ee42698f33` at `20260906_18 / 89|5|18|77|173|91|272|0|0|0`:

```text
exact-head LOCAL Recovery rehearsal            PASS
database-local reopen                           PASS
remote-provider recovery                       NOT ACTIVATED
production/cloud recovery                      NOT CLAIMED
```

The final exact-head rehearsal did not relabel historical CP08 evidence as newly executed application/Email reopen proof. Current Recovery authority is `operations/postgres-recovery-runbook.md`.

## 6. Integration state

Pre-vertical integration is complete:

```text
exact-head Recovery rehearsal                  PASS
bounded PR #66                                 MERGED
Backend CI Gate                                PASS
Dependency Review                              PASS
Frontend CI Gate                               PASS
merge method                                   MERGE COMMIT
integration merge                              1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b
parentage/tree readback                        PASS
feature/pre-vertical-foundation                RETIRED
```

No force push, squash, rebase or direct protected-main rewrite was used.

## 7. Documentation lifecycle

Durable current references are:

- `architecture/authenticated-dante-context.md`
- `database/README.md`
- `development/pre-vertical-dogfood-personas.md`
- `development/pre-vertical-scale-harness.md`
- `operations/postgres-recovery-runbook.md`
- `workstreams/pre-vertical-foundation-closure-2026-09-06.md`
- executable source, migrations, tests and tooling

AI PR #63, Home/World Focus PR #65 and pre-vertical PR #66 are protected-main history, not active integration candidates.

## 8. Next development boundary

The next implementation work starts from then-current protected `main` as a **new deliberately bounded real product vertical**.

Do not fabricate generic Timeline/Activity/Event/Routine CRUD, generic Fact/Version/relationship models, product-specific performance budgets or forced AI integration merely to extend the closed foundation.

## 9. Permanent safety rules

```text
protected main is integration authority
unmerged candidate truth != protected-main truth
applied migration history is immutable
no PASS without executed evidence
no force push for normal integration
no schema claim without Dictionary/mapping/migration/PG/test parity
AI/model output != canonical DANTE truth
Search remains independently usable from Intelligence
telemetry != canonical DANTE state
LOCAL recovery PASS != production/cloud recovery PASS
```

## 10. Authority order

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. durable closure/evidence + Git/PR chronology
6. conversation memory
