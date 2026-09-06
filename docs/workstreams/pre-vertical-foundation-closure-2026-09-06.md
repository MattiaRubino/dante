# DANTE Pre-Vertical Foundation — Closure Checkpoint

- **Date:** 2026-09-06
- **Branch:** `feature/pre-vertical-foundation`
- **Status:** IMPLEMENTATION + LOCAL WHOLE-BRANCH QA CLOSED / PROTECTED-MAIN INTEGRATION PENDING
- **Protected-main baseline:** `5258452d7bd4e7a2797922b00035a9068ba41167`
- **Validated implementation/QA head:** `5a820b47f3c1ad59307ee16797e19655f96b1894`
- **PostgreSQL:** 18.6
- **Candidate Alembic:** `20260906_18`
- **Candidate topology:** `89|5|18|77|173|91|272|0|0|0`

This is the durable closure/integration record for the pre-vertical foundation. The former active roadmap is retired when this record lands. The branch has exactly three milestones; QA findings were fixed inside those milestones and did not create a fourth milestone.

```text
PV-01 — Identity / Clock / Time
PV-02 — User Context / Dogfood / Personas
PV-03 — Scale Harness / QA / Closure
```

The commit containing this document is the documentation-cleanup candidate. The final Recovery rehearsal must bind its evidence to the exact pushed branch HEAD after this cleanup. Until that rehearsal, required PR gates and protected-main merge are complete, the candidate remains unmerged branch truth.

## 1. Baseline and integration context

The branch was created from protected `main@5258452d7bd4e7a2797922b00035a9068ba41167`. That baseline already contains the accepted platform history relevant to this work, including:

- Access/Auth M1–M5 and Shared Email Platform integration;
- PostgreSQL Recovery and CP07/CP08 recovery/reopen implementation;
- Platform Observability protected-main integration;
- deterministic AI foundation integrated through PR #63, merge `431fb34029baeacc9ef9f721e9626b39ca10dd39`;
- Home/World Focus reconciliation integrated through PR #65, merge `5258452d7bd4e7a2797922b00035a9068ba41167`.

The pre-vertical branch is additive over that baseline. It does not reopen CP1–CP6, Access/Auth, Recovery, Email, Observability, Intelligence/Search or the accepted frontend foundations.

## 2. PV-01 — Identity / Clock / Time

**Disposition: CLOSED / PASS**

PV-01 established reusable cross-cutting primitives without inventing a product vertical:

- canonical application-issued UUIDv7 reuse;
- backend `Clock`, `SystemClock` and deterministic `FixedClock` behavior;
- strict timezone-aware UTC boundaries;
- named IANA timezone validation;
- `follow_device` and fixed named-zone policy;
- local-time classification/resolution for ordinary, ambiguous and nonexistent wall times;
- 23/25-hour local-day behavior around DST transitions;
- shared frontend Temporal/timezone support;
- explicit prohibition on deriving semantic chronology/currentness from UUID ordering.

Object-owned temporal semantics remain distinct from user/default display timezone and current device timezone.

## 3. PV-02 — User Context / Dogfood / Personas

**Disposition: CLOSED / PASS**

PV-02 materialized the authenticated DANTE application-context seam while preserving the permanent distinctions:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
```

The request-level contract is:

```text
AuthSession
→ admitted Principal
→ Account
→ AccountApplicationContext
→ self Person
→ user/default timezone policy
→ effective request timezone
```

The forward migration `20260906_18` adds `dante.account_application_context`, the bounded `ensure_account_application_context(...)` capability and named-IANA timezone validation while generic runtime `INSERT Person` remains denied. First use is serialized on the owning Account. The initial self Person uses an application-issued UUIDv7 and receives its native address atomically.

The Web boundary carries the governed `X-Dante-Time-Zone` header. Invalid device timezone input is a client/request error; invalid persisted policy remains an internal integrity failure.

### LOCAL/DEV dogfood

The retained LOCAL/DEV tooling under `apps/backend/tooling/pre_vertical_foundation/` provides one persistent dogfood Account and deterministic persona materialization without becoming product signup or production fixture infrastructure.

Direct operational evidence obtained during this workstream:

```text
persistent dogfood seed                         PASS
repeat seed / idempotence                       PASS
same Account on rerun                           PASS
same self Person on rerun                       PASS
backend bootstrap                               PASS
real browser email/password login               PASS
AuthSession/access path                         PASS
```

Secrets remain outside Git and are not printed by the tooling.

### Deterministic personas

Exactly three product-independent personas are retained:

```text
normal         follow_device / Europe-Rome ordinary use
temporal_edge  fixed America/New_York / Rome device / DST gap+overlap
historical     fixed Europe/Rome / Los_Angeles device / explicit 2016→2026 anchors
```

No Timeline, Activity, Event, Routine, Occurrence, Session, Actual, Outcome or Observation rows are fabricated merely to populate a database.

## 4. PV-03 A — Scale Harness

**Disposition: CLOSED / PASS**

The deterministic scale harness reuses the PV-02 personas and remains product-independent.

```text
small     12
medium   120
large   1200
```

Each block of 12 is the exact matrix:

```text
3 personas × 4 synthetic history input shapes
```

The four history input shapes are fixture inputs only: `metadata_free`, `incomplete`, `corrected`, `mixed`. Explicit source timestamps carry chronology when present; UUID ordering never does.

The large profile is generated in memory and does not mass-materialize password credentials or product rows. The real PostgreSQL correctness check uses the small-profile cardinality for bounded concurrent first use and requires all contenders to converge on exactly one Account application context, one self Person and one native address.

Observed targeted PostgreSQL scale acceptance:

```text
PostgreSQL 18.6 bounded convergence test    PASS — 1 passed
```

The cardinalities are fixture sizes, not throughput, concurrency, latency, capacity or SLA claims.

## 5. PV-03 B — Whole-Branch QA

**Disposition: CLOSED / LOCAL PASS**

### Backend

Canonical local whole-branch validation on the candidate produced:

```text
uv lock / locked environment                  PASS
Ruff format                                   PASS — 257 files formatted
Ruff lint                                     PASS
strict mypy                                   PASS
non-PostgreSQL pytest                         PASS — 457 passed / 165 deselected
AI eval deterministic tests                   PASS — 22 passed
backend wheel + sdist build                   PASS
canonical PostgreSQL 18.6 image               PASS
real PostgreSQL acceptance                    PASS — 165 passed
```

The PostgreSQL lane covers the repository's real database acceptance harness, including migrations/current catalog/Dictionary and the branch's new account-context/scale acceptance. CP1–CP6 migration history was not rewritten.

### Frontend

Canonical frontend validation produced:

```text
frontend pre-production contracts             PASS
World Focus pre-production contracts           PASS
Prettier format                                PASS
ESLint                                         PASS
TypeScript typecheck                           PASS — 6 packages
architecture dependency rules                  PASS — 533 modules / 1676 dependencies
tracked generated-source drift                 PASS — 78 files deterministic
Web unit tests                                 PASS — 136 files / 636 tests
shared package unit tests                      PASS
production build                               PASS
Chromium Web E2E                               PASS — 127 tests
frozen Timeline Firefox contract               PASS — 10 tests
Expo mobile compatibility                      PASS
Android Hermes bundle smoke                    PASS
```

The final QA also exposed two repository-wide Prettier drifts and a real normal-Vite LOCAL development topology gap. Those findings were fixed inside PV-03: normal `@dante/web dev` now owns `localhost:5173` and proxies `/api/v1` to the canonical local backend, with LOCAL Auth origin examples aligned to the same origin. The final format/lint/typecheck/build check passed on that fix.

### Exact scope

The QA-fix commits were checked against explicit pre-scopes before remote writes. No force push or direct protected-main write was used. The last implementation fix at `5a820b47f3c1ad59307ee16797e19655f96b1894` changed exactly its four approved paths.

## 6. Database candidate

Protected-main baseline remains:

```text
Alembic       20260904_17
topology      88|5|16|76|172|89|270|0|0|0
```

Pre-vertical candidate is:

```text
Alembic       20260906_18
topology      89|5|18|77|173|91|272|0|0|0
```

The delta is one Account application-context table, two routines, one trigger, one PK-backed index, two foreign keys and two CHECK constraints. There are no new enums/domains, sequences, materialized views, partitioned tables or RLS policies.

Real PostgreSQL acceptance is locally green. Protected-main database truth does not advance to `20260906_18` until the branch is merged.

## 7. Recovery disposition

Historical CP07 and CP08 evidence remains accepted for the exact heads/contracts it executed. It is not silently widened to this newer schema.

For this candidate:

```text
pre-vertical exact-head Recovery rehearsal     PENDING
remote backup provider                          NOT ACTIVATED
production/cloud recovery                       NOT CLAIMED
```

The versioned runner has been updated for `20260906_18 / 89|5|18|77|173|91|272|0|0|0`. The next mandatory closure action is to execute it on the exact clean/pushed documentation-closure HEAD and retain the ignored local report bound to that SHA.

## 8. PV-03 C — Protected-main closure

**Disposition: IN PROGRESS / ONLY INTEGRATION LIFECYCLE REMAINS**

Required order:

```text
final current-truth documentation cleanup
→ clean worktree + pushed exact candidate HEAD
→ exact-head Recovery rehearsal
→ reread/fetch protected main
→ reconcile only if main moved
→ bounded PR to main
→ Backend CI Gate PASS
→ Dependency Review PASS
→ Frontend CI Gate PASS
→ branch remains up to date
→ owner-authorized merge commit only
→ protected-main parentage/tree/readback verification
→ post-merge current-truth reconciliation if required
→ retire feature/pre-vertical-foundation
```

No squash, rebase, force push or direct write to protected `main` is part of this integration path.

## 9. Explicit non-goals retained

This foundation does not implement the first real product vertical and does not pre-build generic product semantics. In particular it does not add:

- `/v1/timeline` or generic Timeline APIs;
- generic Activity/Event/Routine CRUD;
- product Session lifecycle endpoints;
- Actual/Outcome product surfaces;
- a new generic `Execution` owner;
- generic Fact/Version/relationship/EAV models;
- generic `(kind, uuid)` semantic references;
- product-specific performance budgets before operations exist;
- real Search owner/data integration or Ask DANTE product integration;
- production/private-data AI activation;
- production/cloud Recovery qualification.

## 10. Durable references after merge

The live foundation contracts remain in:

- `../architecture/authenticated-dante-context.md`
- `../database/README.md`
- `../development/pre-vertical-dogfood-personas.md`
- `../development/pre-vertical-scale-harness.md`
- `../operations/postgres-recovery-runbook.md`
- executable code, migrations, tests and tooling

This file is the single retained pre-vertical closure record. Full chronology remains in Git/PR history rather than an active append-only workstream diary.

After protected-main acceptance, new feature work must start from then-current `main` under a new bounded product-vertical scope. Do not continue development on this retired branch.