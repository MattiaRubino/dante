# Physical Model

- **Status:** CLOSED AT TARGET-ARCHITECTURE LEVEL — SELECTED / ACCEPTED / INTEGRATED VIA PR #15
- **Product:** DANTE (`LifeOS` remains historical working-name evidence where present)
- **Physical integration commit:** `e6f191bad947388a44defe2c15f4939345084f58`
- **PostgreSQL architecture family:** 18 / sole canonical persistence + material-history authority
- **Physical phase-time exact patch:** 18.4 / historical selection evidence
- **Current PostgreSQL patch:** 18.6
- **Protected-main baseline at current Timeline vertical selection:** Alembic `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Active Timeline candidate:** `feature/timeline-temporal-operational` / Alembic `20260923_57` / `145|5|88|92|285|223|408|0|0|0`
- **Last downstream reconciliation:** 2026-09-23

## 1. Purpose and boundary

This directory preserves the accepted Physical architecture translating the closed DANTE Domain + Logical model into implementation mechanisms.

The Physical Model is closed. Later implementation consumes it; later implementation does not rewrite phase-time evidence.

Historical Physical statements such as:

```text
PostgreSQL 18.4 selected
DATABASE DEPLOYMENT NOT STARTED
DIRECT HG PASS 0
```

remain valid only for the checkpoint at which they were written.

For current implementation status use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../database/README.md
../database/dictionary/README.md
../workstreams/timeline-temporal-operational-map.md   # while the candidate is active
```

## 2. Version/status truth

```text
ARCHITECTURE FAMILY
PostgreSQL 18
sole canonical persistence / material-history authority

PHYSICAL PHASE-TIME EXACT PATCH
18.4 / historical selection evidence

CURRENT IMPLEMENTATION PATCH
18.6

PROTECTED-MAIN BASELINE AT TIMELINE SELECTION
20260906_18
89|5|18|77|173|91|272|0|0|0

ACTIVE UNMERGED TIMELINE CANDIDATE
20260923_57
145|5|88|92|285|223|408|0|0|0
```

A compatible maintenance patch inside PostgreSQL 18 is lifecycle maintenance and does not reopen the accepted Physical architecture. A major-version change is a separate architecture/revalidation boundary.

## 3. Closed Physical result

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   COMPLETE
PM-03   STATIC COMPLETE / 0 REJECTS
PM-04A  COMPLETE / 0 EXECUTION-WORTHY GAPS
PM-04B  NOT ADMITTED
PM-05   COMPLETE
PM-06   EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN
PM-07   EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN
PM-08   SECONDARY/SPECIALIST QUALIFICATION COMPLETE
PM-09   EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10   FINAL STACK RECOMMENDATION COMPLETE
PM-11   EXPLICIT TARGET STACK SELECTION COMPLETE
PM-12   ACCEPTED PHYSICAL MODEL COMPLETE
PM-13   CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14   BRANCH / WORKSTREAM CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
```

## 4. Physical authority order

Read the closed target from:

1. `pm-11-explicit-selection-v1.md` — selected target stack at phase time;
2. `pm-12-accepted-physical-model-v1.md` — accepted ownership/topology contract;
3. `pm-13-clean-room-qa-v1.md` — clean-room QA;
4. `pm-14-closure-v1.md` — workstream closure evidence;
5. `recommendation/post-selection-validation-register-v1.md` — carry-forward validation;
6. `result-register-v1.md` — Physical result ledger.

Current concrete persistence is owned downstream by the PostgreSQL constitution/ADR, `../database/README.md`, Dictionary, current migrations/mappings/tests and real PostgreSQL.

## 5. Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
SELECTED != DEPLOYED
POSTGRESQL PATCH REFRESH != PHYSICAL REOPEN
DATABASE MATERIALIZATION != PRODUCT-VERTICAL APPLICATION IMPLEMENTATION
LOCAL RECOVERY PASS != REMOTE/CLOUD PRODUCTION RECOVERY PASS
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut is accepted.

## 6. Accepted target stack

```text
CANONICAL PRIMARY
PostgreSQL 18

POSTGRESQL CAPABILITIES
PostGIS
pgvector
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer target

OFFLINE / SYNC TARGETS — NOT CURRENT TIMELINE-VERTICAL SCOPE
PowerSync Open Edition target
encrypted SQLite
PostgreSQL-backed bucket storage
explicit client-safe sync projections

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B
Restate runtime target

OBJECT BYTES
Cloudflare R2 Standard / private

RECOVERY TARGET
pgBackRest
remote provider remains activation-time decision

SOLVER
OR-Tools CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy
Grafana Cloud EU
pg_stat_statements
```

Selection does not mean activation. In particular, PowerSync/native-offline/provider work is not activated by the current Timeline vertical.

## 7. Canonical ownership

```text
PostgreSQL
= canonical DANTE truth + material history

PostGIS
= geospatial capability over PostgreSQL state

FTS / pg_trgm / unaccent / pgvector
= derived/query retrieval

SQLite / PowerSync
= bounded local/sync target, not current canonical truth

Restate
= future durable execution runtime target where justified

R2
= raw object bytes

remote recovery object storage
= recovery copies only, never canonical DANTE state

OR-Tools
= candidate deterministic solver state

OTel / Grafana
= operational telemetry
```

Canonical persistence authorities: **1 — PostgreSQL**.

## 8. Accepted PostgreSQL mapping thesis

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/control structures only for genuine heterogeneous addressing
+
separate provider / projection / technical concerns
```

Explicitly rejected:

```text
universal Entity / Thing table
universal Relationship table
generic canonical EAV/property bag
universal event-log ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
PostgreSQL inheritance as ontology
```

Reference/state rules:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ stable semantic address
→ bounded material-state control
→ owner-specific material-state row
→ explicit current accepted-state binding where required
→ retained history + typed lineage
```

`MaterialStateRef` remains distinct from MVCC/xmin/xid, timestamps, hashes, ETags and provider revisions.

## 9. Current activation posture

```text
PostgreSQL canonical persistence       ACTIVE
pgBackRest LOCAL recovery              ACTIVE / directly rehearsed in its recorded scope
Platform observability stack           ACTIVE for current platform scope
OR-Tools solver target                 SELECTED / NOT YET ACTIVATED by Timeline vertical
PowerSync / native offline             SELECTED TARGET / OUTSIDE CURRENT VERTICAL
remote backup provider                 NOT ACTIVATED
external calendar/provider sync        FUTURE / OUTSIDE CURRENT VERTICAL
```

The current `+`/Timeline vertical may activate existing selected mechanisms only when an owning semantic capability requires them and direct validation is performed.

## 10. Timeline candidate carry-forward

Current candidate semantics through B06 preserve the accepted mapping thesis:

```text
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
```

B06 reused the existing Schedule authority for Occurrence instead of creating a second temporal engine. Runtime Occurrence provenance remains behind bounded least-privilege capabilities.

The next active block is B08 Session Runtime. B08 must first inspect accepted Domain/Logical/Physical Session mappings and existing CP6 materialization before proposing new DDL.

## 11. Current boundary summary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 architecture family
phase-time exact patch 18.4 / historical

CURRENT PROTECTED-MAIN BASELINE AT TIMELINE SELECTION
PostgreSQL 18.6
Alembic 20260906_18
89|5|18|77|173|91|272|0|0|0

ACTIVE TIMELINE CANDIDATE
PostgreSQL 18.6
Alembic 20260923_57
145|5|88|92|285|223|408|0|0|0
B00–B06 CLOSED / PROVEN
B08 NEXT

OUTSIDE CURRENT VERTICAL
external provider integration
native/offline/multi-device
broad analytics
account collaboration
```

Exact present-tense status always comes from live Git + current project/workstream/database authority; historical PM files remain phase-time evidence.