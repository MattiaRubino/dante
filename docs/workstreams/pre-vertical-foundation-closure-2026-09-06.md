# DANTE Pre-Vertical Foundation — Closure Checkpoint

- **Date:** 2026-09-06
- **Branch:** `feature/pre-vertical-foundation` — RETIRED
- **Status:** CLOSED / PROTECTED-MAIN INTEGRATED
- **Protected-main baseline before integration:** `5258452d7bd4e7a2797922b00035a9068ba41167`
- **Final exact-head candidate:** `21353469464f1371f9913dc78933f4ee42698f33`
- **Integration PR:** #66
- **Integration merge:** `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b`
- **PostgreSQL:** 18.6
- **Current Alembic:** `20260906_18`
- **Current topology:** `89|5|18|77|173|91|272|0|0|0`

This is the durable closure record for the pre-vertical foundation. The former active roadmap is retired. The work had exactly three milestones; QA findings were fixed inside those milestones and did not create a fourth milestone.

```text
PV-01 — Identity / Clock / Time
PV-02 — User Context / Dogfood / Personas
PV-03 — Scale Harness / QA / Closure
```

There is no PV-04.

## 1. Baseline and integration context

The branch was created from protected `main@5258452d7bd4e7a2797922b00035a9068ba41167`. That baseline already contained the accepted platform history relevant to this work, including:

- Access/Auth M1–M5 and Shared Email Platform integration;
- PostgreSQL Recovery and CP07/CP08 recovery/reopen implementation;
- Platform Observability protected-main integration;
- deterministic AI foundation integrated through PR #63, merge `431fb34029baeacc9ef9f721e9626b39ca10dd39`;
- Home/World Focus reconciliation integrated through PR #65, merge `5258452d7bd4e7a2797922b00035a9068ba41167`.

The pre-vertical branch was additive over that baseline. It did not reopen CP1–CP6, Access/Auth, Recovery, Email, Observability, Intelligence/Search or the accepted frontend foundations.

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

**Disposition: CLOSED / PASS**

### Backend

Canonical local whole-branch validation on the final implementation candidate produced:

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

The PostgreSQL lane covered migrations/current catalog/Dictionary and the branch's account-context/scale acceptance. CP1–CP6 migration history was not rewritten.

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

QA also exposed two repository-wide Prettier drifts and a normal-Vite LOCAL development topology gap. Those findings were fixed inside PV-03: normal `@dante/web dev` owns `localhost:5173` and proxies `/api/v1` to the canonical local backend, with LOCAL Auth origin examples aligned to the same origin.

## 6. Database result

Current protected-main truth after PR #66:

```text
Alembic       20260906_18
topology      89|5|18|77|173|91|272|0|0|0
```

The delta over the former `20260904_17 / 88|5|16|76|172|89|270|0|0|0` baseline is one Account application-context table, two routines, one trigger, one PK-backed index, two foreign keys and two CHECK constraints. There are no new enums/domains, sequences, materialized views, partitioned tables or RLS policies.

## 7. Recovery disposition

Historical CP07 and CP08 evidence remains accepted for the exact heads/contracts it executed. It is not silently widened.

The final pre-vertical candidate was separately exercised on exact clean/pushed HEAD `21353469464f1371f9913dc78933f4ee42698f33`:

```text
PostgreSQL 18.6                                 PASS
Alembic 20260906_18                             PASS
topology 89|5|18|77|173|91|272|0|0|0           PASS
observer provisioning / least privilege         PASS
deterministic PITR A-present / B-absent         PASS
old protected payload physical resurrection     PROVEN
anti-resurrection reconciliation                PASS
payload reinsertion after retirement            REJECTED
database-local reopen                           PASS
ordinary LOCAL resource non-interference        PASS
disposable cleanup                              PASS
remote backup provider                          NOT ACTIVATED
production/cloud recovery                       NOT CLAIMED
```

This final rehearsal proved database-local reopen. Historical CP08 application/Email reopen evidence remains historical direct evidence and was not falsely relabeled as newly executed by the final CP07-style rehearsal.

## 8. PV-03 C — Protected-main closure

**Disposition: CLOSED / PASS**

Executed order:

```text
final current-truth documentation cleanup       PASS
clean worktree + pushed exact candidate HEAD    PASS
exact-head Recovery rehearsal                   PASS
re-read/fetch protected main                    PASS
main reconciliation                             NOT REQUIRED — main unchanged
bounded PR #66                                  PASS
Backend CI Gate                                 PASS
Dependency Review                               PASS
Frontend CI Gate                                PASS
merge method                                    MERGE COMMIT
protected-main merge                            1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b
parentage/tree/readback                         PASS
feature/pre-vertical-foundation                 RETIRED
```

Merge commit `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` has the expected parents:

```text
5258452d7bd4e7a2797922b00035a9068ba41167
21353469464f1371f9913dc78933f4ee42698f33
```

and the merged tree matches the final candidate tree.

No squash, rebase, force push or direct rewrite of protected `main` was used.

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

New feature work must start from then-current protected `main` under a new bounded product-vertical scope. Do not continue development on the retired branch.
