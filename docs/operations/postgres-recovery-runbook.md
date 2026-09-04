# DANTE — PostgreSQL Local Recovery Operator Runbook

- **Status:** CURRENT / DATABASE-LOCAL CP07 PASS / EMAIL REOPEN REMEDIATION REQUIRED
- **Scope:** whole local PostgreSQL disaster recovery and semantic acceptance
- **Remote backup provider:** TBD / NOT ACTIVATED
- **Production/cloud recovery:** NOT CLAIMED
- **Canonical database:** PostgreSQL 18.6
- **Current protected-main Alembic head:** `20260904_17`
- **Access integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56`
- **Historical accepted CP07 implementation proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Whole-rehearsal harness:** `infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh`

> This runbook is deliberately provider-neutral. It describes the DANTE LOCAL recovery contract now owned by protected `main`. The 2026-09-04 CP07 run remains valid for the PostgreSQL/database-local and MaterialState scope it actually executed. A post-merge audit found that the same whole-flow run did not directly prove Email post-restore quarantine before Email workers resume; application Email traffic reopen after PITR is therefore blocked until that forward remediation is implemented and rehearsed.

## 1. Operator objective

Recover a lost PostgreSQL cluster without confusing restored physical bytes with accepted DANTE truth or allowing restored external-effect work to escape before reconciliation.

The required whole local recovery flow is:

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
→ MaterialState anti-resurrection reconciliation
→ Email post-restore quarantine while Email workers remain stopped
→ verify quarantined state + sensitive-payload wipe
→ runtime verification
→ database-local reopen decision
→ application/Email traffic reopen only after all activated-effect gates pass
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
Email workers must remain stopped until post-restore quarantine is accepted
derived/object state != canonical authority
```

The CP07 harness uses unique disposable volumes and containers and must never use the ordinary local PostgreSQL volumes, the retained recovery repository, or the retained CP05 target as mutation targets.

## 3. Entry criteria

Operator recovery may begin only when:

```text
incident/rehearsal scope is explicit
an attached Git branch with configured upstream is selected
worktree is clean
local HEAD == configured upstream HEAD after fetch
WSL/Linux + uv + Docker/Compose machine prerequisites are available
repository recovery bootstrap can materialize image + ignored LOCAL credentials
backup/WAL repository identity is known
suppression ledger identity is known
restore target remains isolated from application traffic
Email/application workers capable of external effects are stopped
```

For repository-level prerequisite bootstrap only:

```bash
bash infra/local/postgres/recovery/bootstrap-local-recovery.sh
```

For the complete CP07 local rehearsal:

```bash
bash infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

CP07 invokes the bootstrap automatically. Neither command requires the historical `feature/postgres-recovery` branch name; both fail closed unless the current attached branch is clean and exactly aligned with its configured upstream.

The CP07 destructive topology is non-interactive because every mutation target is generated uniquely for that run.

**Current limitation:** until the Email recovery remediation is merged, the versioned CP07 harness does not itself prove the Email quarantine/reopen ordering described in sections 7–8. A `LOCAL_PASS` report from the historical/current harness therefore earns only the database-local scope it directly executes; it must not be interpreted as application Email traffic reopen acceptance.

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
expected restored external-effect work requiring reconciliation
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
Email post-restore quarantine incomplete or unproved
Email sensitive restored work not wiped
activated external-effect reconciliation requirement
derived/object reconciliation requirement
```

`archive_mode=off` is used on the isolated verification target so the rehearsal cannot create an accidental archive branch.

## 6. Structural and security acceptance

Accepted current protected-main LOCAL database contract:

```text
PostgreSQL       18.6
Alembic          20260904_17
topology         88|5|16|76|172|89|270|0|0|0
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

Historical protected-main Recovery-only contract before PR #52:

```text
Alembic          20260830_09
topology         69|5|15|76|97|69|123|0|0|0
```

That historical contract must not be used to accept a restore of the current enriched protected-main database.

## 7. Semantic and external-effect reconciliation

### 7.1 MaterialState anti-resurrection

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
BLOCK on missing/unavailable records
BLOCK on unexpected entries
BLOCK on duplicate MaterialStateRef target
BLOCK on orphan PREPARED/COMMITTED
BLOCK on identity/target/hash/canonicalization mismatch
restore/confirm retirement tombstone
remove resurrected protected payload
preserve truthful address/current/history continuity
prove payload reinsertion is rejected
```

A PREPARED-only ledger state is intentionally ambiguous and must block automatic suppression. The historical 2026-09-04 CP07 directly exercised this fail-closed path before canonical retirement + COMMITTED suppression were completed.

### 7.2 Email post-restore quarantine

A backup/PITR target may contain EmailIntent work that was non-terminal at the target but was already sent, failed ambiguously, superseded or otherwise resolved later in real history. Restoring that old state must not automatically make it sendable again.

The existing shared Email Platform owns `DurableEmailOutbox.quarantine_after_restore()`. Before Email workers can resume after restore, the accepted operator/runtime sequence must guarantee:

```text
Email workers stopped
→ restored database structurally accepted
→ MaterialState anti-resurrection accepted
→ quarantine_after_restore() runs in an explicit transaction
→ every restored pending / claimed / retryable_failure intent becomes recovery_quarantined
→ claim_token / claimed_until / next_attempt_at cleared
→ terminal/recovery marker recorded
→ sensitive key / nonce / ciphertext cleared
→ sensitive_wiped_at recorded
→ commit + read-back verification
→ only then may Email workers/application traffic resume
```

If quarantine cannot run or verification is ambiguous, application Email traffic remains closed.

The direct PostgreSQL Email test already proves quarantine state transition and sensitive wipe in isolation. The missing acceptance item discovered after PR #52 is **whole-recovery ordering proof**, not absence of the quarantine implementation itself.

## 8. Reopen decisions

DANTE separates database recovery acceptance from application/external-effect reopen acceptance.

The historical/current CP07 can earn:

```text
DATABASE LOCAL REOPEN = PASS
```

when all PostgreSQL and database-semantic checks it executes pass.

For an Email-enabled restored system, the stronger gate is:

```text
APPLICATION / EMAIL REOPEN = PASS
```

and it may be earned only after section 7.2 has been implemented as an authoritative recovery step and directly exercised by the whole-recovery acceptance harness.

Until that remediation lands:

```text
DATABASE LOCAL REOPEN          historical proof available
APPLICATION / EMAIL REOPEN     NOT YET PROVEN BY WHOLE CP07
```

The current project must also **not** claim:

```text
production/cloud recovery PASS
remote object-store recovery PASS
PowerSync/search/vector recovery PASS
```

because those capabilities are not activated/proved here.

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
Email workers started before quarantine acceptance
Email post-restore quarantine failure/ambiguity
restored sendable EmailIntent remains after quarantine
restored sensitive Email payload remains after quarantine
runtime-path failure
protected non-test resource changes
```

Do not "repair" the recovered database by inventing canonical state.

## 10. Evidence capture

Every whole rehearsal records a local ignored JSON report:

```text
infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

It contains the database-local observations implemented by the harness, including:

```text
Git proof HEAD + current branch/upstream
recovery image identity
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
MaterialState anti-resurrection result
non-interference result
remote-provider status
```

Until the Email remediation extends the harness/report, the JSON does **not** provide Email post-restore whole-flow acceptance evidence.

These are local observations, never invented production RPO/RTO targets.

### Historical accepted database-local CP07 evidence — 2026-09-04

Exact proof relation:

```text
historical branch  integration/access-auth-main-20260904
proof HEAD         81639c61478b476c995652d0060dde8f53aef089
recovery image     dante-postgres-recovery:18.6-pgbackrest-2.59.1
```

Direct whole-rehearsal result:

```text
whole local operator rehearsal                  PASS
PostgreSQL                                      18.6
Alembic                                         20260904_17
topology                                        88|5|16|76|172|89|270|0|0|0
database-local reopen                           PASS
deterministic PITR A-present / B-absent         PASS
old protected X physical resurrection           PROVEN
PREPARED-only suppression ambiguity             BLOCKED / PASS
ledger anti-resurrection reconciliation         PASS
payload reinsertion after retirement            REJECTED
structural/security/runtime acceptance          PASS
ordinary local volume non-interference          PASS
real recovery repository non-interference       PASS
retained CP05 target non-interference            PASS
disposable cleanup                              PASS
remote backup provider                          TBD / NOT ACTIVATED
production/cloud recovery                       NOT CLAIMED
Email post-restore whole-flow quarantine         NOT EXERCISED BY THIS RUN
application / Email reopen                      NOT CLAIMED BY THIS RUN
```

Measured LOCAL observations:

```text
run id                                    cp07-20260904T135801Z-15861
backup label                              20260904-135821F
backup duration                           65.226133 s
backup repository size                    5897962 bytes
WAL archive freshness at disaster         0.817316 s
restore-point age at disaster             3.748588 s
physical restore                          8.171384 s
PITR replay to target                     0.144118 s
recovery to ready                         0.372819 s
semantic reconciliation                   0.584630 s
structural/security acceptance            2.857058 s
PGDATA loss → database-local reopen       17.679584 s
whole harness                             103.912062 s
```

The historical report status was `LOCAL_PASS`. That status is preserved as evidence of what the harness executed; this runbook narrows its interpretation rather than rewriting the measurement.

PR #52 subsequently merged the CP07-proven schema/database-local recovery contract into protected `main` at `5f76ec54ad78542f137e8730e904f805d9e59e56`; the merge tree is identical to the final candidate tree and post-merge real PostgreSQL plus Backend/Frontend CI passed. `20260904_17 / 88|5|16|76|172|89|270` is therefore the current protected-main database recovery target, with the Email whole-flow reopen gate explicitly outstanding.

Durable repository-level integration evidence is summarized in `../workstreams/access-auth-integration-acceptance-2026-09-04.md`; the ignored local JSON remains the machine observation for that workstation run.

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

## 13. Historical reusable-runner proof

The Recovery workstream previously proved the branch-agnostic/idempotent bootstrap and runner on its own exact pushed Recovery-only implementation heads, including fresh-clone secret bootstrap, image build, exact branch/upstream gating, PITR, anti-resurrection and cleanup.

Those older measurements remain historical evidence in Git/archive records. They must not override the current protected-main contract or the post-merge Email reopen limitation documented above.

The permanent conclusion carried forward is:

```text
runner does not depend on historical branch name
bootstrap is repository-owned and idempotent
recovery target must be exact-head/current-contract aware
LOCAL database recovery evidence != application external-effect reopen evidence
LOCAL rehearsal evidence is not production RPO/RTO
remote/provider recovery is never claimed without real activation + proof
```
