# Physical Model Execution Template v1

- Status: **CURRENT — BOOTSTRAP TEMPLATE**
- Use: one filled record per material mapping review, benchmark run, recovery/evolution run or candidate disposition checkpoint
- Empty template is not evidence

## 1. Record identity

```text
record_id:
record_type: mapping | correctness | performance | recovery | evolution | secondary-lane | sensitivity | recommendation
created_at:
reviewed_at:
author/reviewer:
LifeOS source commit:
Physical workstream commit:
Phase-10 specification commit:
scenario-corpus commit:
benchmark-register commit:
```

## 2. Candidate subject

```text
lane:
candidate:
product:
exact version:
edition/license class:
deployment mode/topology:
container/runtime:
client/driver version:
extensions/plugins:
license/feature assumptions:
```

Rule:

```text
brand name alone != benchmark subject
product + version + edition + deployment mode = benchmark subject
```

## 3. Evidence sources for capability claims

List exact official sources used to freeze the subject.

```text
source title:
source type: official docs | official release notes | official API/driver docs | direct execution evidence
version/edition applicability:
claim supported:
conflict/ambiguity:
resolution:
```

If evidence is contradictory or not version-specific enough, mark the affected item `HOLD`.

## 4. Hardware / environment

```text
host/runner identity:
CPU:
RAM:
storage device/type:
filesystem:
OS/kernel:
container engine/version:
network topology:
virtualization/cloud class:
resource limits:
background load:
clock/timezone:
```

Record differences between candidates. Undisclosed unequal hardware invalidates direct performance comparison.

## 5. Candidate configuration

```text
configuration revision:
config files/flags:
cache/buffer settings:
connection pool:
worker/concurrency settings:
index settings:
durability settings:
replication/HA settings:
backup settings:
manual tuning performed:
reason for tuning:
```

No hidden tuning.

## 6. Physical mapping revision

```text
mapping_id:
mapping_revision:
source path/commit:
schema/query-language revision:
semantic-owner mapping summary:
reference-family mapping summary:
relation/n-ary mapping summary:
current/history representation:
governance/disclosure representation:
provider/derived-state separation:
expected-state mechanism:
multi-owner consistency boundary:
retention/redaction/tombstone approach:
temporal/recurrence approach:
evolution/migration approach:
```

## 7. Mapping guardrail review

For each relevant item:

```text
universal Entity/Thing introduced?          NO required
canonical generic EAV/property bag?         NO required
canonical generic edge root?                NO required
storage token == MaterialStateRef?          NO required
provider revision == MaterialStateRef?      NO required
runtime ID == semantic identity?            NO required
secondary projection == canonical truth?    NO required
semantic shortcut/duplication caveat:
```

## 8. Dataset / fixture

```text
fixture generator version/commit:
seed:
tier: LOW | BASE | HIGH | custom sensitivity
actual current record count:
actual history/provenance count:
actual searchable chunk count:
actual provider object count:
other relation/object counts:
dataset hash/manifest:
fixture generation duration:
fixture storage size:
```

Never record a nominal tier as fully executed if actual counts differ materially. Preserve actual counts.

## 9. Scenario / load

```text
corpus family: C0..C7
scenario IDs: SC-...
load profile: LP-...
concurrency:
read/write mix:
duration/iterations:
warm/cold/cache state:
failure injection:
preconditions:
expected semantic oracle:
```

## 10. Correctness assertions

For every assertion:

| Assertion | Expected | Observed | Result | Evidence |
|---|---|---|---|---|
| | | | PASS/FAIL/HOLD | |

A benchmark summary without traceable correctness assertions is invalid.

## 11. Hard-gate linkage

Primary candidate:

| Gate | Result | Evidence | Condition/caveat |
|---|---|---|---|
| HG-01 | NOT RUN | | |
| HG-02 | NOT RUN | | |
| HG-03 | NOT RUN | | |
| HG-04 | NOT RUN | | |
| HG-05 | NOT RUN | | |
| HG-06 | NOT RUN | | |
| HG-07 | NOT RUN | | |
| HG-08 | NOT RUN | | |
| HG-09 | NOT RUN | | |
| HG-10 | NOT RUN | | |
| HG-11 | NOT RUN | | |
| HG-12 | NOT RUN | | |

Secondary/index lane when applicable:

| Gate | Result | Evidence | Condition/caveat |
|---|---|---|---|
| CG-01 | NOT RUN | | |
| CG-02 | NOT RUN | | |
| CG-03 | NOT RUN | | |
| CG-04 | NOT RUN | | |

Allowed results: `PASS`, `PASS-CONDITIONAL`, `HOLD`, `REJECT`, `NOT-APPLICABLE` with rationale.

## 12. Performance / resource measurements

Only count toward primary weighted scoring after applicable hard gates pass.

```text
sample count:
latency p50:
latency p95:
latency p99:
throughput:
conflicts:
retries:
error classes:
CPU average/peak:
RAM average/peak:
disk/storage before/after:
index/projection size:
write amplification where measured:
network where material:
```

Attach raw metrics location.

## 13. Query / plan evidence

```text
query/mutation ID:
query text/path:
plan/profile artifact:
index/constraint usage:
rows/objects touched:
notes:
```

## 14. Backup / restore / recovery

```text
backup method:
backup start/end:
backup size:
destructive action:
restore method:
restore start/end:
observed recovery time:
observed recovery point/data loss:
post-restore semantic verification:
redaction/deletion anti-resurrection verification:
manual intervention:
raw evidence:
```

Measured observations are not business RPO/RTO commitments.

## 15. Evolution / migration

```text
from mapping/schema version:
to version:
fixture/history depth:
migration method:
duration:
rollback path:
identity/reference verification:
history semantic verification:
tombstone/redaction verification:
pending reconciliation verification:
raw evidence:
```

## 16. Failure / backpressure

```text
fault injected:
injection point:
expected truthful state:
observed state:
data loss:
duplicate consequence:
reconciliation path:
recovery action:
result:
```

## 17. Security / disclosure checks

```text
visibility/scope filter:
hidden fixture count:
observable count/ranking/error behavior:
timing class observation where material:
index/projection stale state:
post-access-change propagation:
leakage result:
```

## 18. Search/vector metrics when applicable

```text
exact oracle:
embedding/model basis:
vector dimensionality:
index type/parameters:
unfiltered recall@k:
filtered recall@k:
precision@k:
latency:
candidate count before filter:
candidate count after filter:
access/deletion propagation result:
```

## 19. Secondary graph metrics when applicable

```text
G0 baseline query:
G1 projection/query:
projection build duration:
projection update lag:
rebuild duration:
traversal latency/throughput:
access/deletion propagation:
additional operational burden:
net benefit observation:
```

## 20. Weighted score evidence when eligible

Do not fill if an applicable primary hard gate has not passed.

| Dimension | Weight | Score basis | Evidence | Weighted result |
|---|---:|---|---|---:|
| Semantic mapping simplicity/evolvability | 20 | | | |
| Transaction/concurrency ergonomics | 15 | | | |
| Query/report/traversal | 15 | | | |
| History/current efficiency | 10 | | | |
| Operations/backup/restore/HA | 15 | | | |
| Schema evolution/migration | 10 | | | |
| Performance/resource efficiency | 10 | | | |
| Python/tooling/cost/exit risk | 5 | | | |
| **Total** | **100** | | | |

## 21. Sensitivity

```text
variable changed:
baseline condition:
alternate condition:
ranking/disposition impact:
material? yes/no
result: stable | SENSITIVITY-DEPENDENT | insufficient/HOLD
```

## 22. Raw artifact manifest

```text
artifact:
kind:
location:
size:
hash:
retention note:
contains secrets/personal data? MUST BE NO for committed fixtures/evidence
```

Large evidence may live outside Git only if its durable location/hash/reproduction instructions are recorded. Ephemeral CI artifacts alone are not durable closure evidence.

## 23. Caveats / invalidations

Record anything that makes comparison weaker or non-equivalent:

```text
version mismatch:
hardware mismatch:
failed fixture equivalence:
uncontrolled cache effect:
manual tuning asymmetry:
missing scenario:
unexecuted tier:
known product issue:
documentation ambiguity:
```

## 24. Result

```text
hard-gate result:
score eligibility:
weighted result:
sensitivity result:
recommended disposition:
PASS | PASS-CONDITIONAL | HOLD | REJECT | SENSITIVITY-DEPENDENT | PREFERRED
```

Never write `SELECTED` here unless PM-11 explicit selection gate has already been approved and the result register/accepted Physical authority is updated in that separate scope.

## 25. Reviewer conclusion

Explain:

- what the evidence actually proves;
- what it does not prove;
- what conditions materially apply;
- whether rerun is required;
- exact next action.
