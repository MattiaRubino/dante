# DANTE — Access/Auth + Email + Recovery Integration Acceptance — 2026-09-04

- **Class:** DURABLE INTEGRATION ACCEPTANCE EVIDENCE
- **Authority:** historical/executed evidence; current truth remains in `PROJECT-STATUS.md`, `ROADMAP.md`, subsystem references and executable repository state
- **Integration branch:** `integration/access-auth-main-20260904`
- **Protected-main base at acceptance:** `fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282`
- **Accepted implementation proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Candidate Alembic head:** `20260904_17`
- **PostgreSQL:** 18.6
- **Disposition:** COMBINED INTEGRATION QA PASS / READY FOR PROTECTED-MAIN MERGE AFTER DOCUMENTATION-ONLY CI + FINAL REF RECHECK

## 1. Purpose

This record captures the executed evidence that closes the combined Recovery + Access/Auth + shared Email Platform integration candidate before protected-main merge.

It is not a temporary chat/session handoff and does not replace current subsystem documentation.

It also does **not** claim that PR #52 has already been merged. Protected `main` remains Recovery-only at `20260830_09` until the protected-main PR actually lands and post-merge verification passes.

## 2. Accepted scope

The candidate combines without history rewrite:

```text
protected-main Recovery
  20260830_09

Access/Auth M1–M5
+ shared Email Platform
  through 20260904_16

20260830_09 + 20260904_16
            ↓
        20260904_17
```

`20260904_17` is a forward no-DDL Alembic merge revision.

Accepted capability scope:

```text
Access/Auth M1–M5                            CLOSED / ACCEPTED
password/session lifecycle                   ACCEPTED
signup/recovery/reset/reauth                  ACCEPTED
Google real UAT                              PASS
Windows Hello / passkeys real UAT            PASS
Apple backend engineering                    PASS
Apple real registered-domain UAT             BOUNDED DEFERRED / NON-BLOCKING
Shared Email Platform                        CLOSED / ACCEPTED
Email shared-ownership refactor              VERIFIED / ACCEPTED
real SES signup/recovery/reset notification  PASS
Recovery integration                         ACCEPTED
CP07 whole LOCAL recovery                     PASS
```

No M6/M7 feature expansion belongs in this candidate.

## 3. Candidate database contract

Exact accepted materialized contract:

```text
PostgreSQL          18.6
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

Machine topology string used by CP07:

```text
88|5|16|76|172|89|270|0|0|0
```

Cross-representation invariant:

```text
current DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

## 4. GitHub Actions evidence on exact implementation proof HEAD

Exact HEAD:

```text
81639c61478b476c995652d0060dde8f53aef089
```

Observed workflow results:

```text
Dependency Review   run 33864047483   SUCCESS
Frontend CI         run 33864047466   SUCCESS
Backend CI          run 33864047467   SUCCESS
```

Backend CI contained three mandatory jobs:

```text
Backend Quality      SUCCESS
Backend PostgreSQL   SUCCESS
Backend CI Gate      SUCCESS
```

Backend Quality observed successful locked-dependency verification, Ruff format/lint, mypy strict, fast tests and backend package build.

Backend PostgreSQL observed successful canonical PostgreSQL image build and the real PostgreSQL acceptance suite.

This is exact-HEAD CI evidence for the implementation candidate before the documentation-only acceptance reconciliation commit.

## 5. CP07 whole LOCAL operator recovery evidence

The complete command was executed from the repository checkout on branch `integration/access-auth-main-20260904`.

An attempted preliminary `cd /home/mattia/projects/dante-access` failed because that directory did not exist. This did **not** invalidate the rehearsal: the shell remained in the actual repository checkout and the versioned CP07 runner then independently failed closed on and printed the correct branch, configured upstream and exact proof HEAD before destructive work began.

Runner Git proof:

```text
Git branch    integration/access-auth-main-20260904
Git upstream  origin/integration/access-auth-main-20260904
Git HEAD      81639c61478b476c995652d0060dde8f53aef089
```

Bootstrap/runtime envelope:

```text
PostgreSQL image  dante-postgres-recovery:18.6-pgbackrest-2.59.1
PostgreSQL        18.6
pgBackRest        2.59.1
bootstrap         PASS
```

### Structural contract

```text
Alembic head      20260904_17
upgrade drift     no new upgrade operations detected
topology          88|5|16|76|172|89|270|0|0|0
structural/security contract PASS
```

### Recovery chronology

The rehearsal:

```text
created real protected MaterialState X
created FULL B0 containing X
created deterministic restore point R1
committed A before R1
committed B after R1
created PREPARED suppression evidence
proved PREPARED-only ledger ambiguity blocks
committed canonical retirement + payload deletion
committed matching suppression evidence
proved final source A|B|TOMBSTONE|X = 1|1|1|0
simulated complete disposable PGDATA loss
proved repository + suppression ledger survived
restored B0 + PITR to R1
proved A present / B absent
proved old X physically resurrected while tombstone absent
loaded committed ledger before reopen
reconciled retirement/tombstone and removed resurrected X
proved protected payload reinsertion rejected
passed final runtime/reopen gate
cleaned disposable recovery resources
```

Observed acceptance:

```text
A PRESENT / B ABSENT                       PASS
old X physically resurrected              PROVEN
PREPARED-only recovery block              PASS
ledger anti-resurrection reconciliation   PASS
payload reinsertion                       REJECTED
DATABASE LOCAL REOPEN                     PASS
DERIVED STORE GATE                        NOT_ACTIVATED / NO FALSE PASS
OBJECT STORE GATE                         NOT_ACTIVATED / NO FALSE PASS
REMOTE PROVIDER                           TBD / NOT ACTIVATED
```

### Local measured observations

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

The generated ignored report recorded:

```text
status  LOCAL_PASS
path    infra/compose/secrets/postgres_recovery_cp07_report.json.local
```

These measurements are LOCAL rehearsal observations only. They are not production RPO/RTO targets.

## 6. Recovery claims deliberately not made

The integration candidate does **not** claim:

```text
production/cloud recovery PASS
remote backup-provider recovery PASS
object-store recovery PASS
PowerSync/search/vector recovery PASS
production RPO/RTO targets
```

The correct current states are:

```text
remote backup provider   TBD / NOT ACTIVATED / NOT EXERCISED
production/cloud         NOT CLAIMED
derived store            NOT_ACTIVATED / NO FALSE PASS
object store             NOT_ACTIVATED / NO FALSE PASS
```

## 7. Email acceptance reconciliation

Historical real-provider evidence from 2026-09-03 remains accepted:

```text
signup verification email      RECEIVED / OTP USED
password recovery email        RECEIVED / LINK USED
password reset                 PASS
no auto-login after reset      PASS
prior AuthSession revocation   PASS
reset security notification    RECEIVED
provider MessageId             PRESENT
terminal sensitive wipe        PASS
```

The subsequent 2026-09-04 shared-ownership refactor and forward migration `20260904_16` are not justified by that older UAT alone. They are accepted separately by the current architecture/replay tests, static/unit regression, real PostgreSQL acceptance and exact-HEAD combined CI.

Therefore:

```text
real SES UAT evidence                 ACCEPTED HISTORICAL EVIDENCE
shared ownership refactor             VERIFIED / ACCEPTED
migration 20260904_16                 PG PROVEN / ACCEPTED
production sender-domain deployment   SEPARATE FUTURE GATE
```

## 8. Protected-main merge conditions

The implementation acceptance is complete. Before PR #52 may be marked ready/merged:

```text
current documentation reconciled to this measured truth
final candidate commit contains documentation/evidence changes only
fresh mandatory CI passes on that final candidate commit
protected main ref is fetched/rechecked
candidate still contains the expected protected-main base/history
PR remains mergeable
```

If `main` has advanced, stop. Integrate the new main delta forward and rerun all affected gates. If the database or recovery contract changes, CP07 must be rerun against that new exact candidate.

## 9. Post-merge conditions

Merge is not branch closure.

After PR #52 lands:

```text
fetch exact resulting protected main
verify candidate payload/ancestry
verify mandatory CI on resulting main
verify one Alembic head and expected migration DAG
verify current DB references now identify 20260904_17 as protected-main truth
remove/replace candidate-only wording from current status/roadmap/workstream docs
keep this acceptance record historical
only then retire/delete/archive the integration branch according to repository policy
```

The next intended bounded integration is `feature/platform-observability`, which must absorb the enriched protected main and rerun its release/integration gates before its own protected-main PR.

## 10. Final disposition at this record

```text
IMPLEMENTATION CANDIDATE                     ACCEPTED
COMBINED RECOVERY + ACCESS + EMAIL QA       PASS
CP07 WHOLE LOCAL OPERATOR RECOVERY          PASS
CURRENT DOCUMENT RECONCILIATION             INCLUDED IN FOLLOWING DOC-ONLY COMMIT
PROTECTED-MAIN MERGE                         NOT YET CLAIMED
POST-MERGE ACCEPTANCE                        NOT YET CLAIMED
BRANCH RETIREMENT                            NOT YET CLAIMED
```

This distinction is intentional: **accepted candidate != merged main != safely closed branch**.
