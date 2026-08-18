# PM-13 — Independent Clean-Room QA v1

- Status: **QA PASS — PHYSICAL ARCHITECTURE/DOCUMENTATION COHERENCE**
- Workstream: `feature/physical-model`
- QA subject: PM-11 selected target stack + PM-12 Accepted Physical Model + current Physical registers
- Direct implementation execution: **NOT PART OF THIS QA / REMAINS NOT RUN**
- Backend implementation: **NOT STARTED**

## 1. Clean-room rule

PM-13 re-evaluates the selected/accepted Physical architecture as a closed target contract rather than reusing the PM-09 score as proof.

This QA distinguishes:

```text
ARCHITECTURE / DOCUMENTATION COHERENCE QA
!=
DIRECT DATABASE / RUNTIME / RECOVERY VALIDATION
```

A PM-13 `QA PASS` therefore cannot discharge any unexecuted item in `recommendation/post-selection-validation-register-v1.md`.

## 2. Inputs re-read

The clean-room pass checked the current selected/accepted records against the main supporting evidence layers:

```text
PM-10 final recommendation
PM-10 final stack audit
PM-10 capability matrix
PM-10 representative simulation
PM-11 explicit selection
PM-12 Accepted Physical Model
current execution methodology
current acceptance matrix
current result register
current Physical README
current workstream handoff
post-selection validation register
technology exclusion register
```

The Restate deployment statement was independently rechecked against current official Restate documentation before QA:

- Restate supports self-hosting as a self-contained binary/container;
- Restate Cloud supports an EU region;
- current Cloud client-side journal encryption is documented only for the TypeScript SDK;
- therefore the selected Restate technology may use self-hosted or Cloud EU deployment, with no global mandatory default for the current Python path.

## 3. Canonical-authority check

Expected:

```text
CANONICAL PERSISTENCE AUTHORITIES
1
```

Observed:

```text
PostgreSQL 18.4
1
```

Noncanonical mechanisms remain correctly bounded:

```text
PowerSync / SQLite        local/sync projection
Restate                   execution runtime
R2                        raw object bytes
S3                        recovery copy
pgvector/search indexes   derived retrieval
OR-Tools                  candidate solver output
OTel/Grafana              operational telemetry
```

Verdict: **PASS**.

## 4. Domain / Logical non-reopen check

PM-11/12 do not introduce:

```text
universal Entity/Thing root
universal generic semantic edge root
EAV/property-bag canonical kernel
provider/system identity as canonical identity
MVCC/storage token as MaterialStateRef
technical AuthZ as Domain Authority/Consent
solver/runtime/projection result as accepted semantic truth
```

`WL-H01..WL-H12` remain downstream obligations.

Verdict: **PASS**.

## 5. Selection consistency check

PM-11 selection matches the PM-10 recommended target with one approved hardening only:

```text
PostgreSQL 18.4                    selected
PostGIS 3.6.4                      selected
pgvector 0.8.6                     selected
native FTS / pg_trgm / unaccent    selected
pg_stat_statements                 selected
PgBouncer 1.25.2                   selected
PowerSync 1.25.0 OE                selected
encrypted SQLite                   selected
PG outbox + bounded worker         selected
Restate runtime                    selected
R2 Standard EU/private             selected
pgBackRest 2.59.0                  selected
AWS S3 eu-south-1 recovery target  selected
OR-Tools 9.15 CP-SAT               selected
OTel + Alloy + Grafana Cloud EU    selected
```

Approved hardening:

```text
Restate Cloud EU
NOT a mandatory global default

Restate deployment
SELF-HOSTED OR CLOUD EU
profile/privacy/operability decision
```

No unapproved engine was introduced.

Verdict: **PASS**.

## 6. Offline / multi-device check

The accepted flow preserves server authority:

```text
PostgreSQL canonical
→ approved PowerSync projection
→ encrypted SQLite
→ offline mutation
→ LifeOS backend revalidation
→ PostgreSQL canonical commit if valid
```

Checks:

```text
LOCAL != CANONICAL                         PASS
arrival order != semantic conflict winner PASS
universal consequential LWW               ABSENT
Visibility/delete propagation obligation  PRESENT
PowerSync liveness hardening obligation   PRESENT
```

Verdict: **PASS**.

## 7. Durable-execution check

Class A and Class B remain separated:

```text
bounded/reconstructible async
→ PG outbox + worker

material long-running durable work
→ Restate
```

Restate runtime state is not Domain history. Current Python journal-encryption limitations are not hidden; journal minimization and deployment-mode privacy review remain explicit obligations.

Verdict: **PASS**.

## 8. Object / recovery check

Accepted ownership remains:

```text
ContentArtifact identity/metadata/authority → PostgreSQL
raw bytes                                  → R2
DB backup                                  → pgBackRest/S3
object backup                              → separate S3 repository
```

Recovery copies are not canonical. Anti-resurrection/reconciliation obligations are preserved. Object Lock Compliance is not the default.

Verdict: **PASS**.

## 9. Search / graph / vector check

Accepted target uses:

```text
lexical       PostgreSQL native FTS + pg_trgm + unaccent
vector        pgvector
traversal     explicit PostgreSQL mappings + recursive SQL
```

No initial Neo4j/Qdrant/OpenSearch service is silently required. Visibility/freshness/deletion validation remains registered.

Verdict: **PASS**.

## 10. Solver check

OR-Tools remains candidate-only. The Accepted Physical Model explicitly preserves:

```text
UNKNOWN != INFEASIBLE
solver status != accepted LifeOS Decision
```

Verdict: **PASS**.

## 11. Observability/privacy check

OTel/Alloy/Grafana/pg_stat_statements remain operational telemetry only. Privacy minimization and telemetry-outage non-interference remain implementation obligations.

Verdict: **PASS**.

## 12. Direct-evidence truth check

Observed current truth:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE                   NOT RUN
MIGRATION                 NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                  NOT RUN
RESTATE                    NOT RUN
OBJECT RECOVERY            NOT RUN
SOLVER                     NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

No current selected/accepted record converts these values to PASS.

Verdict: **PASS**.

## 13. Post-selection obligation preservation

The expanded PSV register remains active. PM-13 does **not** declare its direct entries passed.

```text
UNEXECUTED PSV ITEMS RELABELED PASS
0

REQUIRED IMPLEMENTATION VALIDATION LOST
0
```

Verdict: **PASS**.

## 14. Technology-exclusion consistency

No accepted initial target dependency requires the excluded engine set. No hidden Kafka/Redis/Neo4j/Qdrant/OpenSearch/Temporal/DBOS/etc. dependency was discovered in PM-12.

Verdict: **PASS**.

## 15. Development-profile boundary

PM-12 correctly separates target architecture from later `Development Profile v0` decisions.

```text
TARGET TECHNOLOGY DECISION
closed by Physical Model

DEV-v0 ACTIVATION / FREE / LOCAL / MANAGED CHOICES
separate later operational scope
```

Verdict: **PASS**.

## 16. Clean-room defect register

```text
BLOCKING ARCHITECTURE DEFECTS      0
CANONICAL-AUTHORITY CONFLICTS      0
UNAPPROVED TECHNOLOGIES            0
FALSE DIRECT PASS CLAIMS           0
LOST PSV OBLIGATIONS               0
DOMAIN/LOGICAL IMPLICIT REOPENS    0

HARDENING FOUND BEFORE QA
Restate Cloud mandatory-default wording
STATUS
REPAIRED BEFORE FINAL QA
```

## 17. PM-13 verdict

```text
PM-13
QA PASS

SCOPE
ARCHITECTURE / DOCUMENTATION COHERENCE

SELECTED TARGET STACK
COHERENT

ACCEPTED PHYSICAL MODEL
COHERENT

DIRECT IMPLEMENTATION VALIDATION
STILL REQUIRED / NOT RUN

NEXT
PM-14 closure + protected-main integration
```
