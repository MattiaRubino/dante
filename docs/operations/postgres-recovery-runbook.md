# DANTE — PostgreSQL Local Recovery Operator Runbook

- **Status:** CURRENT / HISTORICAL CP07 + CP08 PASS / PRE-VERTICAL EXACT-HEAD PASS
- **Scope:** whole local PostgreSQL disaster recovery and semantic/application reopen acceptance
- **Remote backup provider:** TBD / NOT ACTIVATED
- **Production/cloud recovery:** NOT CLAIMED
- **Canonical database:** PostgreSQL 18.6
- **Protected-main Alembic head:** `20260906_18`
- **Protected-main topology:** `89|5|18|77|173|91|272|0|0|0`
- **Pre-vertical exact-head Recovery proof:** `21353469464f1371f9913dc78933f4ee42698f33`
- **Pre-vertical integration merge:** `1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b` via PR #66
- **Historical accepted CP07 proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Historical accepted CP08 proof HEAD:** `1a5a7f1fbbdc1e5723d58fa90721a8693cce49e9`
- **Whole-rehearsal harness:** `infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh`

The historical 2026-09-04 CP07 and CP08 results remain accepted for the exact contracts they executed. The pre-vertical database-local Recovery contract was separately re-executed and passed on exact candidate HEAD `21353469464f1371f9913dc78933f4ee42698f33` at `20260906_18 / 89|5|18|77|173|91|272|0|0|0`, then integrated through PR #66. That final rehearsal does not relabel historical CP08 application/Email reopen evidence as newly executed.

## 1. Operator objective

Recover a lost PostgreSQL cluster without confusing restored physical bytes with accepted DANTE truth or allowing restored external-effect work to escape before reconciliation.

Required flow:

```text
healthy PostgreSQL
→ verified WAL archiving + FULL backup
→ deterministic restore point
→ later canonical writes
→ durable suppression evidence
→ simulated/real PGDATA loss
→ clean restore + PITR
→ PostgreSQL promotion
→ structural/security acceptance
→ MaterialState anti-resurrection reconciliation
→ Email post-restore quarantine while workers remain stopped
→ verify quarantine + sensitive-payload wipe
→ runtime verification
→ database-local reopen decision
→ application/Email reopen only after all activated-effect gates pass
```

`pg_isready` or a booting server is never sufficient recovery acceptance.

## 2. Hard safety rules

Before destructive work identify explicitly:

```text
source PGDATA
backup/WAL repository
suppression ledger
restore target
Git proof HEAD
target restore point
activated external-effect queues/workers
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
restored non-terminal EmailIntent != permission to send
Email workers remain stopped until post-restore quarantine is accepted
derived/object state != canonical authority
```

The repository rehearsal uses unique disposable resources. It must never repurpose the ordinary local PostgreSQL volume, retained Recovery repository or another retained target merely because a name appears familiar.

## 3. Entry criteria

Operator recovery/rehearsal may begin only when:

```text
incident/rehearsal scope is explicit
attached Git branch has configured upstream
worktree is clean
local HEAD == upstream HEAD after fetch
WSL/Linux + uv + Docker/Compose prerequisites are available
repository recovery bootstrap can materialize image + ignored LOCAL credentials
backup/WAL repository identity is known
suppression ledger identity is known
restore target is isolated from application traffic
Email/application workers capable of external effects are stopped
```

Repository prerequisite bootstrap:

```bash
bash infra/local/postgres/recovery/bootstrap-local-recovery.sh
```

Complete LOCAL rehearsal:

```bash
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

The whole runner invokes bootstrap automatically. It is branch-name agnostic, but fails closed unless the attached branch is clean and exactly aligned with its upstream.

The current versioned runner expects `20260906_18 / 89|5|18|77|173|91|272|0|0|0`. Historical proof remains exact-head scoped; do not substitute an older run for a changed current contract.

## 4. Restore versus PITR decision

Use exact backup restore only when the accepted recovery point is the backup endpoint. Use PITR when the accepted point is later and required WAL continuity is available.

A PITR decision identifies:

```text
base backup label
target restore point / timestamp / LSN as applicable
target timeline
required WAL continuity
expected semantic state at target
expected restored external-effect work requiring reconciliation
```

Never choose “latest possible” implicitly when the incident requires a bounded target.

## 5. Target isolation

A restored target remains closed while any of the following is unresolved:

```text
pg_is_in_recovery() != false
wrong PostgreSQL version
wrong Alembic head
topology drift
owner/role/ACL drift
extension drift
suppression-ledger ambiguity
retired payload present
runtime-path failure
Email post-restore quarantine incomplete or ambiguous
Email sensitive restored work not wiped
activated external-effect reconciliation requirement
derived/object reconciliation requirement
```

The isolated verification target uses `archive_mode=off` so a rehearsal cannot accidentally create a new archive branch.

## 6. Structural and security acceptance

Current protected-main contract:

```text
PostgreSQL       18.6
Alembic          20260906_18
topology         89|5|18|77|173|91|272|0|0|0
owners           dante_owner
roles            dante_owner / dante_migrator / dante_runtime / dante_observer
runtime Alembic  denied
observer         pg_read_all_stats only / no DANTE schema access
retirement ACL   SELECT only
extensions       postgis 3.6.4
                 vector 0.8.6
                 pg_trgm 1.6
                 unaccent 1.1
                 pg_stat_statements 1.12
```

Former protected-main contract before pre-vertical integration, retained as historical context only:

```text
PostgreSQL       18.6
Alembic          20260904_17
topology         88|5|16|76|172|89|270|0|0|0
```

Any mismatch against the current contract blocks reopen.

Historical Recovery-only topology `20260830_09 / 69|5|15|76|97|69|123|0|0|0` is evidence only and must never be used to accept a restore of the current enriched database.

## 7. Semantic and external-effect reconciliation

### 7.1 MaterialState anti-resurrection

Old backups may predate later canonical retirement/redaction.

Required suppression protocol:

```text
PREPARED
→ canonical PostgreSQL retirement/redaction commit
→ canonical DB readback
→ COMMITTED bound to PREPARED SHA-256
```

On restore:

```text
load committed suppression evidence
BLOCK missing/unavailable records
BLOCK unexpected entries
BLOCK duplicate MaterialStateRef target
BLOCK orphan PREPARED/COMMITTED
BLOCK identity/target/hash/canonicalization mismatch
restore/confirm retirement tombstone
remove resurrected protected payload
preserve truthful address/current/history continuity
prove payload reinsertion is rejected
```

A PREPARED-only state is intentionally ambiguous and blocks automatic suppression.

### 7.2 Email post-restore quarantine

Restored EmailIntent work that was non-terminal at the recovery point may already have been sent, failed ambiguously, superseded or resolved later in real history. Restoring that state never makes it automatically sendable.

Before Email workers resume:

```text
Email workers stopped
→ restored database structurally accepted
→ MaterialState anti-resurrection accepted
→ DurableEmailOutbox.quarantine_after_restore() in explicit transaction
→ pending / claimed / retryable_failure -> recovery_quarantined
→ in_progress attempt -> ambiguous
→ claim_token / claimed_until / next_attempt_at cleared
→ terminal/recovery marker recorded
→ sensitive key / nonce / ciphertext cleared
→ sensitive_wiped_at recorded
→ COMMIT + readback
→ second reconciliation idempotent
→ claimable Email work = 0
→ only then may Email/application traffic resume
```

If quarantine cannot execute or readback is ambiguous, application Email traffic remains closed.

## 8. Reopen decisions

DANTE keeps database recovery acceptance separate from application/external-effect reopen acceptance.

Historical direct evidence:

```text
CP07 DATABASE LOCAL REOPEN        PASS for its exact historical contract
CP08 APPLICATION / EMAIL REOPEN   PASS for its exact historical contract
```

Final pre-vertical direct evidence:

```text
proof HEAD                                    21353469464f1371f9913dc78933f4ee42698f33
PostgreSQL                                    18.6
Alembic                                       20260906_18
topology                                      89|5|18|77|173|91|272|0|0|0
PRE-VERTICAL DATABASE LOCAL REOPEN            PASS
observer provisioning / least privilege       PASS
deterministic PITR A-present / B-absent       PASS
MaterialState anti-resurrection               PASS
payload reinsertion after retirement          REJECTED
ordinary LOCAL resource non-interference      PASS
disposable cleanup                            PASS
PRE-VERTICAL APPLICATION / EMAIL REOPEN       NOT RE-EXECUTED BY THIS RUN
```

The final run proved database-local reopen for the current contract. Application/Email reopen remains governed by the CP08 procedure and historical direct evidence until re-executed for a future scope that requires it.

There is no PV-04. The applicable pre-vertical Recovery proof belonged to PV-03 C closure and is now complete.

The project still does **not** claim:

```text
production/cloud recovery PASS
remote object-store recovery PASS
PowerSync/search/vector recovery PASS
```

When a derived/object capability is not activated, record `NOT_ACTIVATED / NO FALSE PASS` rather than pretending it was recovered.

## 9. Abort / escalation conditions

Stop and keep the target isolated on:

```text
missing backup or required WAL
unbootable restore
unexpected timeline / target not reached
recovery still active
schema/head/topology mismatch
owner/role/ACL/extension mismatch
suppression-ledger ambiguity/tamper
retired payload survives reconciliation
payload reinsertion succeeds
Email workers start before quarantine acceptance
Email quarantine failure/ambiguity
restored sendable EmailIntent remains after quarantine
restored sensitive Email payload remains after quarantine
runtime-path failure
protected non-test resource changes
```

Do not “repair” a recovered database by inventing canonical state.

## 10. Evidence capture

The whole rehearsal writes an ignored local report:

```text
infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

It records the implemented local observations, including:

```text
Git proof HEAD + branch/upstream
recovery image identity
PostgreSQL/Alembic/topology
backup label/duration/size
WAL freshness and restore-point age
physical restore / PITR / ready timings
semantic reconciliation timing
structural/security acceptance timing
PGDATA-loss → database-local-reopen timing
A/B deterministic result
MaterialState anti-resurrection result
non-interference result
remote-provider status
```

Historical reports are never relabeled as new evidence. The pre-vertical closure report is bound to exact candidate HEAD `21353469464f1371f9913dc78933f4ee42698f33`.

These are local observations, not invented production RPO/RTO targets.

## 11. Historical accepted evidence

### CP07 database-local evidence — 2026-09-04

```text
proof HEAD                                      81639c61478b476c995652d0060dde8f53aef089
PostgreSQL                                      18.6
Alembic                                         20260904_17
topology                                        88|5|16|76|172|89|270|0|0|0
database-local reopen                           PASS
deterministic PITR A-present / B-absent         PASS
old protected payload physical resurrection     PROVEN
PREPARED-only ambiguity                         BLOCKED / PASS
anti-resurrection reconciliation                PASS
payload reinsertion after retirement            REJECTED
structural/security/runtime acceptance          PASS
ordinary local resources non-interference       PASS
disposable cleanup                              PASS
remote backup provider                          NOT ACTIVATED
production/cloud recovery                       NOT CLAIMED
application/Email reopen by this run             NOT CLAIMED
```

Historical measured run `cp07-20260904T135801Z-15861` completed the whole harness in approximately `103.912062 s`; those measurements remain historical LOCAL observations only.

### CP08 application/Email reopen evidence — 2026-09-04

```text
proof HEAD                                      1a5a7f1fbbdc1e5723d58fa90721a8693cce49e9
Alembic                                         20260904_17
sendable Email work at PITR target              PHYSICALLY RESURRECTED / PROVEN
Email workers                                   STOPPED
all sendable intents quarantined                PASS
in-progress attempt -> ambiguous                PASS
sensitive + claim/retry state wiped             PASS
second reconciliation                           IDEMPOTENT / 0
claimable Email work                             0
APPLICATION / EMAIL REOPEN                      PASS
```

PR #55 merged the accepted CP08 implementation at `c67a18c24a6cf22b003ffd2c14243af53fec5077`.

These historical results prove what their exact heads executed. They are not silently widened to later contracts.

## 12. Cleanup

The versioned runner removes its unique disposable source/restored containers, PGDATA volume, pgBackRest repository volume, suppression-ledger volume and temporary readback files. The ignored JSON evidence report remains.

On failure cleanup is the default. Deliberate diagnosis only:

```bash
DANTE_CP07_KEEP_ON_FAILURE=1 \
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

The operator then owns explicit cleanup of the printed disposable resource names.

## 13. Future remote-provider boundary

No remote provider is selected or activated now.

A future provider must be selected against capabilities:

```text
pgBackRest-compatible recovery path
durable remote storage
appropriate versioning / immutability
finite policy-bound retention
independent least-privilege credentials
required region/data-residency properties
backup + WAL readback
restore + PITR proof
suppression evidence retained for full resurrection horizon
```

Provider-specific implementation, cost, credentials, production RPO/RTO and production recovery acceptance are deferred until a real deployment needs them.

## 14. Permanent conclusion

```text
runner does not depend on a historical branch name
bootstrap is repository-owned and idempotent
recovery target must be exact-head/current-contract aware
LOCAL database recovery evidence != application external-effect reopen evidence
application/external-effect reopen requires direct proof
LOCAL rehearsal evidence is not production RPO/RTO
remote/provider recovery is never claimed without real activation + proof
```
