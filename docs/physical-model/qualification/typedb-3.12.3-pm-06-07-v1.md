# TypeDB CE 3.12.3 — PM-06/07 Finalist Qualification v1

- Status: **PRIMARY FINALIST / SEMANTIC ADVANTAGE PRESERVED**
- Subject: TypeDB Community Edition 3.12.3 / self-hosted single-node / official driver 3.12.3
- Direct execution: **NOT RUN**
- Preferred: **NONE**
- Selected: **NONE**

## PM-06 scale/performance

```text
VIABILITY              MEDIUM-HIGH CONFIDENCE
LOW/BASE/HIGH          NOT RUN
LOCAL BENCHMARK        NOT ADMITTED
QUERY THREADING        one query currently single-threaded
CE HORIZONTAL SCALE    NOT AVAILABLE
```

Official TypeDB documentation states that each query currently executes single-threaded and that more host CPU/memory is utilized through concurrent queries and transactions. It also documents RocksDB cache/transaction-memory considerations, a recommendation that roughly 5% of data fit in memory for index accessibility/performance, and schema-derived index disk overhead.

These are sizing/topology conditions rather than evidence of inadequate performance. Public TypeDB benchmark evidence supports serious viability but is vendor-owned, not exact LifeOS 3.12.3 concurrent proof, and is not promoted to a LifeOS measured result.

## PM-07 recovery/evolution

```text
SELF-HOSTED BACKUP        USER-OWNED IMPLEMENTATION
DOCUMENTED OPTIONS        DISK SNAPSHOT / EXPORT-IMPORT
INCREMENTAL BACKUP        NO for documented self-hosted options
CROSS-VERSION EXPORT      SUPPORTED PATH
UPGRADE                   data-directory reuse when compatible; export/import otherwise
CE TOPOLOGY               SINGLE NODE
CLUSTER / HA / H-SCALE    CLOUD / ENTERPRISE
DIRECT RESTORE            NOT RUN
DIRECT MIGRATION          NOT RUN
```

Export produces a full TypeQL schema plus binary data. Official documentation states the exported binary is designed to be usable across TypeDB versions, making export/import a credible migration mechanism. TypeDB 3.12.3 release evidence includes fixes for import blockers involving inherited constraints, reinforcing both active support and the reality of schema/import operational complexity.

## LifeOS-specific remaining obligations

- every write-skew-sensitive invariant boundary must use correctly scoped consistency guards;
- guard coverage must remain auditable as schema/operations evolve;
- backup automation/retention/monitoring for self-hosted CE would be LifeOS-owned;
- old-backup anti-resurrection remains post-selection implementation validation;
- actual LifeOS V1→V2 mapping migration remains post-selection implementation validation;
- semantic post-restore verification remains post-selection implementation validation.

## Semantic advantage

TypeDB continues to have the cleanest direct expression of:

- concrete semantic entity types;
- first-class relations;
- named roles;
- typed role eligibility;
- n-ary relations;
- schema cardinality/constraint semantics.

This remains a real LifeOS benefit. PM-06/07 does not erase it merely because PostgreSQL is operationally more mature.

## Cost / topology

The evaluated subject remains Community Edition because the operating target is zero direct technology/license cost where realistically possible. Official TypeDB documentation says CE supports single-node deployments, while clustering/horizontal read scaling belongs to TypeDB Cloud/Enterprise.

A paid/Enterprise path is not silently rejected, but it is not the frozen finalist subject and cannot be used to inflate CE's score later without an explicit topology/cost sensitivity case.

## Comparative judgment

TypeDB remains a legitimate finalist because its semantic-model advantage may still win the PM-09 mapping/evolvability dimensions. However, PM-06/07 makes the tradeoff more explicit:

```text
semantic modeling advantage
vs
consistency-guard discipline
+ self-hosted backup ownership
+ single-node CE topology
+ narrower zero-cost recovery/HA envelope
```

```text
PM-06 VERDICT
ADVANCE — PERFORMANCE VIABLE

PM-07 VERDICT
ADVANCE WITH MATERIAL OPERATIONS/TOPOLOGY COST

CURRENT COMPARATIVE POSITION
#2 / PRINCIPAL CHALLENGER

PREFERRED
NONE

SELECTED
NONE
```

## Reopen/direct-test trigger

Reopen a targeted TypeDB run only if PM-09 becomes genuinely tied on a question that execution can settle, especially deep-history efficiency or concurrency-guard ergonomics. Do not run a generic benchmark merely because TypeDB remains a finalist.

## Primary official sources

- https://typedb.com/docs/core-concepts/typedb/vertical-scaling/
- https://typedb.com/docs/core-concepts/typedb/horizontal-scaling/
- https://typedb.com/docs/maintenance-operation/typedb-backups/
- https://typedb.com/docs/maintenance-operation/database-export-import/
- https://typedb.com/docs/maintenance-operation/typedb-upgrades/
