# XTDB 2.1.0 — PM-04A Evidence Sufficiency v1

- Candidate: XTDB 2.1.0 / self-hosted qualification subject
- Mapping: `PM02-XT-001`
- Status: **EXTERNAL EVIDENCE REVIEW COMPLETE / DIRECT EXECUTION NOT RUN**
- Production topology: **HOLD**
- Selection: **NONE**
- Evidence confidence: **MEDIUM-HIGH chronology/concurrency / MEDIUM overall primary fit**

## 1. PM-04A conclusion

XTDB remains a distinctive temporal/bitemporal challenger. Its documented transaction model is unusually strong for expected-state and co-located multi-owner mutation: DML transactions are serialized through a totally ordered durable log and support transactional assertions.

The PM-03 HG-02/HG-03 uncertainty is now better described as a **known structural cost** rather than an unknown needing local discovery. XTDB documents that it has no native foreign keys and no uniqueness constraints beyond `_id`; referential integrity can still be modeled atomically, but it is explicitly manual/application-transaction responsibility.

A local test can prove one path but cannot remove that ongoing design burden.

```text
EXECUTION-WORTHY GAP NOW
0

PM-04B REQUIRED NOW
NO

DIRECT HG PASS CREATED
NO
```

## 2. Primary source ledger

| Topic | Source | Evidence use |
|---|---|---|
| transactions | https://docs.xtdb.com/about/txs-in-xtdb.html | serialized DML, serializable transactions, ASSERT semantics |
| key concepts | https://docs.xtdb.com/concepts/key-concepts.html | single-writer model, no native FK, uniqueness beyond `_id`, manual atomic integrity |
| time in XTDB | https://docs.xtdb.com/about/time-in-xtdb.html | native system/valid-time model |
| backup/restore overview | https://docs.xtdb.com/ops/backup-and-restore/overview | immutable storage/log recovery model |
| XTDB 2.1 release | https://xtdb.com/blog/attach-database | 2.1 generation context |
| XTDB v2 launch | https://xtdb.com/blog/launching-xtdb-v2 | stable SQL/storage posture and production adoption context |

## 3. Supporting production evidence

Supporting evidence, not proof of LifeOS primary mapping.

| Evidence | Source | Relevance |
|---|---|---|
| energy/VPP case | https://xtdb.com/case-studies/energy-vpp | real bitemporal history for future schedules, late/out-of-order data and audit of what was known at decision time |
| XTDB case-study catalog | https://xtdb.com/case-studies | additional production context |

The VPP case is especially relevant to LifeOS's distinction between effective/world chronology and knowledge/recording chronology, but it does not prove LifeOS ReferenceAddress integrity.

## 4. Gate-by-gate sufficiency

| Gate | PM-04A class | Rationale |
|---|---|---|
| HG-01 | MAP-SUFFICIENT | owner-specific tables plus four segregated address spaces prevent a universal Fact/Entity ontology if mapping discipline holds |
| HG-02 | KNOWN-STRUCTURAL-COST | no native FK; address existence/family eligibility must be asserted manually in all consequential writers |
| HG-03 | KNOWN-STRUCTURAL-COST | no general uniqueness/cardinality constraints beyond `_id`; relation/cardinality obligations require deliberate ID/ASSERT design |
| HG-04 | EXT+MAP-SUFFICIENT | serialized transactions + ASSERT are a strong fit for expected MaterialStateRef preconditions |
| HG-05 | EXT+MAP-SUFFICIENT | co-located mutation in one serialized DML transaction provides a credible atomic boundary |
| HG-06 | EXT+MAP-SUFFICIENT | native bitemporal substrate plus explicit MaterialStateRef/current binding strongly supports reconstruction without replay |
| HG-07 | MAP-SUFFICIENT | canonical/provider/projection/state distinctions are explicit despite shared storage |
| HG-08 | MAP-SUFFICIENT / DEFER-FINALIST | query filtering can implement exposure, but WL-H12 remains system-level non-interference proof |
| HG-09 | DEFER-FINALIST | erase/tombstone and backup policy require LifeOS-specific finalist reconciliation rehearsal |
| HG-10 | EXT+MAP-SUFFICIENT | native temporal axes are valuable where aligned; PM-02 explicitly preserves recurrence/timezone semantics outside valid time when necessary |
| HG-11 | KNOWN-STRUCTURAL-COST + DEFER-FINALIST | gradual/dynamic schema requires strict mapping-revision discipline; actual semantic migration is finalist work |
| HG-12 | KNOWN OPS/TOPOLOGY COST + DEFER-FINALIST | backup capability exists, but topology and single-writer implications remain material conditions |

## 5. Referential integrity is a known burden, not a mystery

XTDB's own documentation is explicit that conventional foreign keys are absent.

LifeOS therefore cannot honestly treat a column containing another `_id` as safe by default.

PM-02's contract remains:

```text
consequential reference write
→ assert target address exists
→ assert correct address space
→ assert Reference Contract allows target family
→ assert target lifecycle permits operation
→ perform all related writes in the same transaction
```

This can be atomic. The comparative penalty is that LifeOS must keep this discipline complete across every consequential write path.

A successful local test of one insert/update path would not prove global future coverage. PM-04A therefore records the burden directly rather than creating a false sense of safety from a small harness.

## 6. Uniqueness/cardinality treatment

The absence of general uniqueness constraints beyond `_id` has the same implication.

Where identity can encode the uniqueness boundary, XTDB can exploit `_id`. Other semantic cardinality/predicate obligations must be expressed through deterministic IDs and transaction assertions.

This is viable but shifts complexity from declarative database schema to mutation design.

```text
VIABLE
YES

NATIVE CONSTRAINT ERGONOMICS
LOWER THAN POSTGRESQL / TYPEDB

LOCAL TEST REMOVES STRUCTURAL COST
NO
```

## 7. Transaction/concurrency advantage

XTDB's serialized DML path is a genuine differentiator.

PM-02 can express a governed mutation as:

```text
ASSERT expected MaterialStateRef
ASSERT reference/invariant predicates
INSERT/UPDATE material state
UPDATE current binding
UPDATE all co-located owners/relations
WRITE provenance/idempotency
```

The non-interactive transaction model is still an ergonomics constraint: complex operations must be formulable as submitted DML/ASSERT logic without arbitrary client-side dialogue inside the transaction.

PM-04A counts this as design/operability evidence, not a blocker requiring a laptop run.

## 8. Bitemporal advantage

XTDB is the strongest candidate-native fit for LifeOS chronology among the four current primaries.

Important boundary remains:

```text
SYSTEM_TIME != MaterialStateRef
VALID_TIME  != every LifeOS time meaning
```

Native bitemporality can reduce accidental history machinery, but Schedule vs Actual, recurrence, named-zone intent, provider revision and explicit semantic acceptance chronology remain governed by the closed Logical Model.

## 9. Production topology / single-writer sensitivity

This HOLD remains important.

A local test cannot answer future questions about:

```text
write-throughput ceiling
multi-region/geographic topology
HA/failover design
infrastructure/TCO
operational maturity at target scale
```

Therefore:

```text
PRODUCTION TOPOLOGY HOLD
REMAINS

LOCAL LAPTOP TEST TO CLOSE IT
INVALID METHOD
```

It belongs in later topology/cost/sensitivity analysis if XTDB remains a finalist.

## 10. Recovery/evolution

XTDB's immutable-storage/log model provides a real recovery path, while its dynamic schema reduces some migration mechanics and increases interpretation discipline.

PM-04A records:

```text
ENGINE CAPABILITY
externally sufficient for comparison

LIFEOS OLD-BACKUP ANTI-RESURRECTION
DEFER-FINALIST

LIFEOS MAPPING V1 -> V2
DEFER-FINALIST

STRUCTURAL MAPPING-REVISION BURDEN
KNOWN COST
```

## 11. Current disposition

```text
P2 XTDB 2.1.0
DISTINCTIVE TEMPORAL CHALLENGER
HG-02/HG-03 UNKNOWN -> KNOWN STRUCTURAL COST
HG-04/HG-05 STRONGLY SUPPORTED BY ENGINE MODEL
PRODUCTION TOPOLOGY HOLD REMAINS
NO PM-04B EXECUTION ADMITTED
EXECUTED HG STILL NOT RUN
NO SCORE
NO SELECTION
```
