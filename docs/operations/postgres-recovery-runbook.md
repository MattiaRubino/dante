# DANTE — PostgreSQL Local Recovery Operator Runbook

- **Status:** CURRENT / CP07 IMPLEMENTED / FINAL LOCAL REHEARSAL PENDING
- **Scope:** whole local PostgreSQL disaster recovery and semantic acceptance
- **Remote backup provider:** TBD / NOT ACTIVATED
- **Production/cloud recovery:** NOT CLAIMED
- **Canonical database:** PostgreSQL 18.6
- **Alembic head:** `20260830_09`
- **Whole-rehearsal harness:** `infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh`

> This runbook is deliberately provider-neutral. It describes the DANTE recovery contract that exists now. A future remote-storage provider is selected only when production deployment actually requires one.

## 1. Operator objective

Recover a lost PostgreSQL cluster without confusing restored physical bytes with accepted DANTE truth.

The whole local recovery flow is:

```text
healthy PostgreSQL
→ verified WAL archiving + FULL backup
→ deterministic restore point
→ later canonical writes
→ durable suppression evidence
→ simulated complete PGDATA loss
→ clean restore + PITR
→ PostgreSQL promotion
→ structural/security acceptance
→ anti-resurrection reconciliation
→ runtime verification
→ database-local reopen decision
```

A recovery is not accepted merely because PostgreSQL starts or `pg_isready` succeeds.

## 2. Hard safety rules

Never delete or repurpose a database/repository because its name "looks right".

Before destructive work identify explicitly:

```text
source PGDATA
backup/WAL repository
suppression ledger
restore target
Git proof HEAD
target restore point
```

Permanent rules:

```text
PGDATA != backup repository
backup repository != suppression ledger
PostgreSQL = canonical DANTE persistence authority
restored bytes != accepted semantic truth
pg_isready != traffic-open permission
PREPARED-only suppression evidence = BLOCK
ambiguous/tampered suppression evidence = BLOCK
retired payload resurrection = BLOCK
derived/object state != canonical authority
```

The CP07 harness uses unique disposable volumes and containers and must never use the ordinary local PostgreSQL volumes, the retained recovery repository, or the retained CP05 target as mutation targets.

## 3. Entry criteria

Operator recovery may begin only when:

```text
incident/rehearsal scope is explicit
correct repository/branch is selected
worktree is clean
local HEAD == remote branch HEAD
PostgreSQL recovery image is present
required ignored local credentials exist
backup/WAL repository identity is known
suppression ledger identity is known
restore target remains isolated from application traffic
```

For the CP07 local rehearsal:

```bash
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

The script is non-interactive because every destructive target is generated uniquely for that run.

## 4. Restore versus PITR decision

Use exact backup restore only when the accepted recovery point is the backup endpoint.

Use PITR when the accepted point is later than the base backup and required WAL is available.

A PITR decision must identify:

```text
base backup label
target restore point / timestamp / LSN as applicable
target timeline
required WAL continuity
expected semantic state at the target
```

Do not choose "latest possible" implicitly when the incident requires a bounded target.

## 5. Target isolation

A restored target remains closed while any of the following are unresolved:

```text
pg_is_in_recovery() != false
wrong PostgreSQL version
wrong Alembic head
topology drift
owner/role/ACL drift
extension drift
ambiguous suppression ledger
retired payload present
runtime-path failure
derived/object reconciliation requirement
```

`archive_mode=off` is used on the isolated verification target so the rehearsal cannot create an accidental archive branch.

## 6. Structural and security acceptance

Current accepted local contract:

```text
PostgreSQL       18.6
Alembic          20260830_09
topology         69|5|15|76|97|69|123|0|0|0
owners           dante_owner
roles            dante_owner / dante_migrator / dante_runtime
runtime Alembic  denied
retirement ACL   SELECT only
extensions       postgis 3.6.4
                 vector 0.8.6
                 pg_trgm 1.6
                 unaccent 1.1
                 pg_stat_statements 1.12
```

Any mismatch blocks reopen.

## 7. Anti-resurrection reconciliation

Old backups may predate a later canonical retirement/redaction.

Required protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical DB read-back
→ COMMITTED bound to PREPARED SHA-256
```

On restore:

```text
load all committed suppression evidence
BLOCK on missing/unavailable records/
BLOCK on unexpected entries
BLOCK on duplicate MaterialStateRef target
BLOCK on orphan PREPARED/COMMITTED
BLOCK on identity/target/hash/canonicalization mismatch
restore/confirm retirement tombstone
remove resurrected protected payload
preserve truthful address/current/history continuity
prove payload reinsertion is rejected
```

Only then may the database-local reopen gate continue.

## 8. Reopen decision

The current project can earn:

```text
DATABASE LOCAL REOPEN = PASS
```

when all PostgreSQL and semantic checks pass.

The current project must **not** claim:

```text
production/cloud recovery PASS
remote object-store recovery PASS
PowerSync/search/vector recovery PASS
```

because those capabilities are not activated here.

When a derived/object capability is not activated, record:

```text
NOT_ACTIVATED / NO FALSE PASS
```

rather than pretending it was recovered.

## 9. Abort / escalation conditions

Stop recovery and keep the target isolated on:

```text
missing backup
missing required WAL
unbootable restore
unexpected timeline
target not reached
recovery still active
schema/head/topology mismatch
owner/role/ACL mismatch
extension mismatch
suppression-ledger ambiguity/tamper
retired payload survives reconciliation
payload reinsertion succeeds
runtime-path failure
protected non-test resource changes
```

Do not "repair" the recovered database by inventing canonical state.

## 10. Evidence capture

Every whole rehearsal records a local ignored JSON report:

```text
infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

It contains:

```text
Git proof HEAD
PostgreSQL/Alembic/topology
backup label/duration/size
WAL archive freshness
restore-point age at simulated disaster
physical restore duration
PITR replay timings
semantic reconciliation duration
structural/security acceptance duration
PGDATA-loss → database-local-reopen duration
A/B deterministic recovery result
anti-resurrection result
non-interference result
remote-provider status
```

These are local observations, never invented production RPO/RTO targets.

<!-- CP07-LOCAL-EVIDENCE: PENDING -->

## 11. Cleanup

The versioned CP07 harness removes its unique disposable:

```text
source/restored containers
PGDATA volume
pgBackRest repository volume
suppression-ledger volume
temporary readback files
```

The ignored JSON evidence report remains.

On failure the default is cleanup. For deliberate diagnosis only:

```bash
DANTE_CP07_KEEP_ON_FAILURE=1 \
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

The operator then owns explicit cleanup of the printed disposable resource names.

## 12. Future remote-provider boundary

No remote provider is selected or activated now.

A future provider must be chosen against capabilities, not brand preference:

```text
pgBackRest-compatible recovery path
durable remote storage
versioning / immutability appropriate to policy
finite policy-bound retention
independent least-privilege credentials
required region/data-residency properties
backup + WAL readback
restore + PITR proof
suppression evidence retained for the full resurrection horizon
```

Provider-specific implementation, costs, credentials, production RPO/RTO and production recovery acceptance are deferred until DANTE actually needs production deployment.
