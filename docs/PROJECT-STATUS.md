# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH + PRE-VERTICAL FINAL INTEGRATION CANDIDATE
- **Last reconciled:** 2026-09-06
- **Protected-main HEAD:** `5258452d7bd4e7a2797922b00035a9068ba41167`
- **AI protected-main merge:** `431fb34029baeacc9ef9f721e9626b39ca10dd39` via PR #63
- **Home/World Focus protected-main merge:** `5258452d7bd4e7a2797922b00035a9068ba41167` via PR #65
- **Protected-main Alembic:** `20260904_17`
- **Pre-vertical candidate Alembic:** `20260906_18`
- **Pre-vertical closure record:** `workstreams/pre-vertical-foundation-closure-2026-09-06.md`

Protected `main` is the integration authority. The pre-vertical status below is final-candidate truth only until the required exact-head Recovery rehearsal, PR gates and protected-main merge complete.

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

AI production/private-data qualification     NOT CLAIMED
Apple registered-domain real UAT             BOUNDED DEFERRED / NON-BLOCKING
remote backup provider                       NOT ACTIVATED
production/cloud recovery                    NOT CLAIMED

Pre-vertical PV-01                           CLOSED / PASS
Pre-vertical PV-02                           CLOSED / PASS
Pre-vertical PV-03 A Scale Harness           CLOSED / PASS
Pre-vertical PV-03 B Whole-Branch QA         CLOSED / LOCAL PASS
Pre-vertical PV-03 C Integration             IN PROGRESS
```

There is no PV-04. QA findings are fixed inside PV-03 and do not create additional milestones.

## 2. Database truth

Protected-main truth remains:

```text
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

The pre-vertical candidate is:

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

The candidate has passed the real PostgreSQL 18.6 acceptance suite locally. That does not make it protected-main truth before merge. Exact database/recovery authority remains `database/README.md` plus the executable migration/catalog/Dictionary/tests.

## 3. Pre-vertical foundation result

The foundation closes the cross-cutting seams required before the first real product vertical:

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

## 4. Local acceptance evidence

The final implementation candidate has direct local evidence for:

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

Detailed evidence and exact branch disposition live in `workstreams/pre-vertical-foundation-closure-2026-09-06.md`.

## 5. Recovery disposition

Historical CP07 database-local and CP08 application/Email reopen evidence remains valid only for the exact historical contracts it executed.

For `20260906_18 / 89|5|18|77|173|91|272|0|0|0`:

```text
exact-head LOCAL Recovery rehearsal            PENDING
remote-provider recovery                       NOT ACTIVATED
production/cloud recovery                      NOT CLAIMED
```

The final Recovery rehearsal must run on the clean pushed documentation-closure HEAD before the integration PR is accepted.

## 6. Integration state

Current required sequence:

```text
pre-vertical current-truth documentation       THIS CANDIDATE
exact-head Recovery rehearsal                  NEXT
fetch/re-read protected main                    REQUIRED
reconcile only if main moved                   CONDITIONAL
bounded PR                                     REQUIRED
Backend CI Gate                                REQUIRED
Dependency Review                              REQUIRED
Frontend CI Gate                               REQUIRED
merge method                                   MERGE COMMIT ONLY
post-merge main readback                       REQUIRED
feature branch retirement                      AFTER ACCEPTANCE
```

No force push, squash, rebase or direct protected-main write is part of the normal closure path.

## 7. Documentation lifecycle

The former active `workstreams/pre-vertical-foundation.md` roadmap is retired at closure. Durable current references are:

- `architecture/authenticated-dante-context.md`
- `database/README.md`
- `development/pre-vertical-dogfood-personas.md`
- `development/pre-vertical-scale-harness.md`
- `operations/postgres-recovery-runbook.md`
- `workstreams/pre-vertical-foundation-closure-2026-09-06.md`
- executable source, migrations, tests and tooling

AI PR #63 and Home/World Focus PR #65 are already protected-main history; they are not active integration candidates anymore. Their detailed chronology belongs to retained closure/evidence records and Git/PR history rather than this current-status file.

## 8. Next development boundary

After the pre-vertical branch is merged and retired, the next implementation work starts from then-current protected `main` as a **new deliberately bounded real product vertical**.

Do not fabricate generic Timeline/Activity/Event/Routine CRUD, generic Fact/Version/relationship models, product-specific performance budgets or forced AI integration merely to keep the foundation branch alive.

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
