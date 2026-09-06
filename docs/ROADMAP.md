# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP + PRE-VERTICAL FINAL INTEGRATION CANDIDATE
- **Last reconciled:** 2026-09-06
- **Protected-main HEAD:** `5258452d7bd4e7a2797922b00035a9068ba41167`
- **Protected-main Alembic:** `20260904_17`
- **Pre-vertical candidate Alembic:** `20260906_18`
- **Pre-vertical closure:** `workstreams/pre-vertical-foundation-closure-2026-09-06.md`

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access/Auth M1–M5 + Shared Email + Recovery
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
Platform Observability
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
AI deterministic low-level foundation
        CLOSED / PROTECTED-MAIN INTEGRATED VIA PR #63
              ↓
Home / World Focus reconciliation
        CLOSED / PROTECTED-MAIN INTEGRATED VIA PR #65
              ↓
PRE-VERTICAL FOUNDATION
        PV-01 CLOSED / PASS
        PV-02 CLOSED / PASS
        PV-03 A CLOSED / PASS
        PV-03 B CLOSED / LOCAL PASS
        PV-03 C INTEGRATION IN PROGRESS
              ↓
exact-head Recovery rehearsal
              ↓
PR required gates
              ↓
protected-main merge commit + readback
              ↓
FIRST REAL BOUNDED PRODUCT VERTICAL
```

There are exactly three pre-vertical milestones:

```text
PV-01 — Identity / Clock / Time
PV-02 — User Context / Dogfood / Personas
PV-03 — Scale Harness / QA / Closure
```

There is no PV-04.

## 2. What the pre-vertical foundation closes

The branch supplies only the small cross-cutting seams required before a real vertical owns operations:

- canonical application-issued UUIDv7 reuse;
- backend Clock abstraction and deterministic time testing;
- named IANA timezone policy and DST edge handling;
- explicit authenticated Account → DANTE application context → self Person mapping;
- user/default timezone policy distinct from object-owned temporal semantics;
- governed Web device-timezone transport;
- persistent LOCAL/DEV dogfood;
- exactly three deterministic product-independent personas;
- deterministic scale/readiness profiles `12 / 120 / 1200`;
- bounded real-PostgreSQL first-use convergence proof;
- normal LOCAL Vite `/api/v1` proxy topology.

It deliberately does **not** implement the first product vertical.

## 3. Current database boundary

Protected-main database truth:

```text
PostgreSQL          18.6
Alembic             20260904_17
Topology            88|5|16|76|172|89|270|0|0|0
```

Pre-vertical integration candidate:

```text
PostgreSQL          18.6
Alembic             20260906_18
Topology            89|5|18|77|173|91|272|0|0|0
```

The candidate is locally accepted by the real PostgreSQL suite but does not become protected-main truth until integration completes.

## 4. Final pre-vertical gate

No additional foundation feature work is planned. The only remaining branch work is closure/integration:

```text
current-truth docs cleanup                COMPLETE IN FINAL DOC CANDIDATE
clean pushed exact branch HEAD            REQUIRED
LOCAL whole Recovery rehearsal            REQUIRED ON EXACT HEAD
re-read/fetch current protected main      REQUIRED
main reconciliation                       ONLY IF MAIN MOVED
bounded PR                                REQUIRED
Backend CI Gate                           REQUIRED
Dependency Review                         REQUIRED
Frontend CI Gate                          REQUIRED
merge method                              MERGE COMMIT ONLY
post-merge parentage/tree/readback         REQUIRED
branch retirement                         AFTER ACCEPTANCE
```

If QA or CI finds a concrete defect, fix only that defect inside PV-03 under a new exact scope. Do not create another milestone.

## 5. Stable semantic boundaries carried into future work

Future verticals must preserve the existing distinctions rather than flattening them for convenience:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual != Outcome != Observation
identity != material state != chronology
```

UUID ordering is never semantic chronology/currentness authority.

PostgreSQL remains canonical persistence authority. Provider/network I/O remains outside authoritative PostgreSQL transactions. No generic repository/UoW/EAV/Fact/Version/relationship framework is pre-authorized by this roadmap.

## 6. First work after merge

After the pre-vertical branch is merged and retired, start the next branch from then-current protected `main` and choose **one real bounded product vertical** with concrete owners and operations.

Only then define operation-specific:

- API surface;
- idempotency/CAS semantics where actually needed;
- concurrency behavior;
- product fixtures;
- performance/load budgets;
- AI/Search integration when a real owner/data/product seam exists;
- new Alembic revision if the vertical genuinely needs persistence evolution.

Do not continue from `feature/pre-vertical-foundation` after closure.

## 7. Existing integrated foundations

The following are protected-main foundations, not pending feature candidates:

```text
Access/Auth M1–M5 + Shared Email          INTEGRATED
PostgreSQL Recovery CP07/CP08             INTEGRATED
Platform Observability                    INTEGRATED VIA PR #58
AI deterministic low-level foundation     INTEGRATED VIA PR #63
Home / World Focus reconciliation          INTEGRATED VIA PR #65
```

AI production/private-data activation remains a separate future qualification. Real Search owner/data integration and Ask DANTE remain trigger-gated product work. Remote backup-provider and production/cloud recovery remain unclaimed.

## 8. Later bounded work

Future scopes may include, only when their real trigger exists:

```text
first real product vertical                NEXT AFTER PRE-VERTICAL MERGE
AI real Search owner/data adapter          REAL OWNER/DATA TRIGGER
AI real Ask DANTE integration              PRODUCT-READINESS TRIGGER
AI memory / solver integration             FUTURE / OWNER-DRIVEN
FTS / pg_trgm / embeddings / pgvector      NEED-DRIVEN
voice / realtime                           FUTURE
browser / computer / code execution        SEPARATE SECURITY GATE
second provider / failover / local model   EVIDENCE-TRIGGERED
deep-reasoning physical binding            EVIDENCE-TRIGGERED
AI production/private-data qualification   SEPARATE ACCEPTANCE
M6 Native Mobile                           OPTIONAL / RE-GATE
later Access/security maturity             FUTURE
vertical observability metrics             NEED-DRIVEN
production observability tuning            MEASURED-EVIDENCE ONLY
production/cloud recovery                  SEPARATE ACCEPTANCE
```

## 9. Integration rule

Every future workstream begins from then-current protected `main`. Closed feature branches are not continuing development bases.

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
NO PASS WITHOUT EXECUTED EVIDENCE
```
