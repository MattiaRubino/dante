# PM-07 Recovery / Evolution / Failure Evidence v1

- Status: **COMPLETE — EVIDENCE QUALIFIED / DIRECT DESTRUCTIVE EXECUTION NOT RUN**
- Finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- Direct restore/migration/failure injection: **NOT ADMITTED**

## Question

Can recovery, backup, restore, schema/data evolution, topology or failure evidence materially reverse the current finalist ordering?

## Result

```text
POSTGRESQL 18.4
RECOVERY / EVOLUTION / OPERATIONS
STRONG
confidence HIGH

TYPEDB CE 3.12.3
RECOVERY / EVOLUTION
VIABLE
higher self-hosted operational burden
confidence MEDIUM-HIGH

DIRECT RESTORE                 NOT RUN
DIRECT ANTI-RESURRECTION       NOT RUN
DIRECT V1->V2 MIGRATION        NOT RUN
FAILURE INJECTION              NOT RUN
```

## PostgreSQL 18.4

Official PostgreSQL 18 documentation provides multiple native recovery paths:

- SQL dump/restore;
- filesystem-level backup;
- continuous WAL archiving and point-in-time recovery;
- full and incremental `pg_basebackup` base backups;
- standby creation from base backup;
- asynchronous or synchronous streaming replication;
- hot/warm standby and failover primitives;
- major-version migration through `pg_upgrade`;
- major-version migration using logical replication.

These capabilities do not themselves prove LifeOS anti-resurrection semantics, but they materially reduce infrastructure risk around canonical recovery and evolution.

PostgreSQL's documented incremental base backup support still requires correct backup-chain/WAL retention management. PM-07 records this as an operational responsibility, not as magical zero-maintenance recovery.

## TypeDB CE 3.12.3

Official TypeDB documentation provides viable recovery/evolution mechanisms:

- database export to schema + binary data;
- database import into the same or a later TypeDB version;
- export format intended to bridge incompatible data-layer versions;
- version upgrades through reuse/copy of the data directory where compatible;
- export/import where the data format is incompatible;
- self-hosted disk snapshots;
- schema evolution through TypeDB/TypeQL mechanisms covered by the accepted mapping.

Important exact-subject conditions:

```text
SELF-HOSTED BACKUP IMPLEMENTATION
user responsibility

RECOMMENDED SELF-HOSTED OPTIONS
disk snapshot OR export/import

INCREMENTAL BACKUP
not available through those documented TypeDB self-hosted options

COMMUNITY EDITION TOPOLOGY
single node

CLUSTER / HORIZONTAL READ SCALING / HA
Cloud or Enterprise capability, not CE
```

The TypeDB 3.12.3 release reviewed during this gate includes fixes for database import blockers involving inherited constraints, which is positive evidence that import/evolution is an active supported path. It also reinforces that schema/import compatibility is a real operational surface to manage.

## Scenario treatment

### SC-011 — redaction then old-backup restore

```text
ENGINE RECOVERY CAPABILITY
EVIDENCE QUALIFIED

LIFEOS ANTI-RESURRECTION
POST-SELECTION IMPLEMENTATION VALIDATION

DIRECT PASS
NO
```

The decisive LifeOS guarantee is that a restored old image cannot silently re-authorize material that was later deleted/redacted. That requires selected-implementation reconciliation/tombstone policy, not merely an engine backup command.

### SC-030 — V1 -> V2 mapping evolution

```text
BOTH FINALISTS
ENGINE EVOLUTION PATH VIABLE

LIFEOS MAPPING MIGRATION
POST-SELECTION IMPLEMENTATION VALIDATION
```

PostgreSQL has several mature migration paths. TypeDB has explicit cross-version export/import plus compatible-data-directory upgrades. The remaining question is the actual selected LifeOS V1→V2 transformation, so duplicating a synthetic migration before selection is not decision-worthy.

### SC-031 — destructive backup/restore + semantic verification

```text
ENGINE BACKUP/RESTORE PATH
EVIDENCE QUALIFIED

LIFEOS SEMANTIC RESTORE SUITE
POST-SELECTION IMPLEMENTATION VALIDATION
```

### SC-032 — capacity/backpressure

The persistence engine must fail/degrade truthfully and avoid silent data loss. Current finalist comparison has no unresolved capacity behavior capable of choosing the winner more reliably than documented topology/resource differences. Direct pressure is deferred until the selected implementation has concrete deployment and workload limits.

## Topology pressure

### PostgreSQL

The zero-license-cost self-hosted engine exposes mature physical/logical replication and standby/failover primitives. Achieving a production HA architecture still requires infrastructure, orchestration and operational discipline, but the database capability is available without switching to a paid database edition.

### TypeDB CE

CE is documented as single-node. Cluster replication, horizontal read scaling and automatic leader failover are Cloud/Enterprise concerns. This is a material condition because LifeOS's current economic target is zero direct technology/license cost where realistically possible.

This does not make TypeDB unusable. It means the exact free self-hosted finalist has a narrower recovery/topology envelope than PostgreSQL.

## Comparative conclusion

```text
POSTGRESQL
CLEAR ADVANTAGE
backup breadth
PITR
incremental base backup
replication options
standby/failover primitives
upgrade/migration maturity
zero-license-cost topology flexibility

TYPEDB CE
VIABLE
but self-hosted backup orchestration is ours
non-incremental documented backup paths
single-node CE
cross-version export/import is a real strength
```

This strengthens PostgreSQL's overall lead without erasing TypeDB's semantic advantage.

## Direct execution admission

```text
SC-011 direct run     NOT ADMITTED
SC-030 direct run     NOT ADMITTED
SC-031 direct run     NOT ADMITTED
SC-032 direct run     NOT ADMITTED
PM-04B reopen         NO
benchmark host        HOLD / DORMANT
```

## Post-selection validation obligations

The selected canonical implementation must still prove before production acceptance, at the appropriate implementation/release gate:

1. backup can actually be restored;
2. semantic verification passes after restore;
3. redaction/deletion anti-resurrection policy survives restoration of older data;
4. NativeRef continuity/non-reuse remains correct;
5. actual mapping migration preserves current and historical semantics;
6. backup/recovery automation is monitored and operationally owned;
7. capacity/backpressure behavior is observable and truthful.

Deferring these from pre-selection comparison does **not** waive them.

## Sources

PostgreSQL:

- `https://www.postgresql.org/docs/18/backup.html`
- `https://www.postgresql.org/docs/18/continuous-archiving.html`
- `https://www.postgresql.org/docs/18/app-pgbasebackup.html`
- `https://www.postgresql.org/docs/18/high-availability.html`
- `https://www.postgresql.org/docs/current/warm-standby.html`
- `https://www.postgresql.org/docs/18/upgrading.html`
- `https://www.postgresql.org/docs/18/pgupgrade.html`

TypeDB:

- `https://typedb.com/docs/maintenance-operation/typedb-backups/`
- `https://typedb.com/docs/maintenance-operation/database-export-import/`
- `https://typedb.com/docs/maintenance-operation/typedb-upgrades/`
- `https://typedb.com/docs/core-concepts/typedb/horizontal-scaling/`

## PM-07 verdict

```text
POSTGRESQL OPERATIONS/RECOVERY ADVANTAGE
MATERIAL

TYPEDB RECOVERY/Evolution PATH
SUFFICIENT TO REMAIN FINALIST

NO DIRECT DESTRUCTIVE RUN NEEDED BEFORE PM-08/PM-09
```