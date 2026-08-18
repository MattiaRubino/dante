# XTDB 2.1.0 — PM-05 Correctness Evidence Qualification v1

- Candidate: XTDB 2.1.0 / self-hosted qualification subject
- Mapping: `PM02-XT-001`
- PM-05 disposition: **DEFER FROM PRIMARY FINALIST SET / NOT REJECTED**
- Direct LifeOS execution: **NOT RUN**
- Selection: **NONE**

## 1. Qualification thesis

XTDB remains a technically credible and unusually relevant temporal candidate, but PM-05 concludes that its native bitemporal advantage does not currently compensate for the persistent primary-integrity and topology costs enough to justify carrying it into the next finalist campaign.

This is a comparative defer, not a hard-gate rejection.

## 2. Primary semantic scenario coverage

### SC-001 / SC-003 / SC-009 — concurrency and multi-owner correctness

XTDB's serialized/serializable DML transaction model and ASSERT support give it a strong path for stale-base and coordinated-write invariants.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT / COMPARATIVE STRENGTH`.

### SC-010 / SC-014 — correction and historical reconstruction

Native system/valid time is materially useful for knowledge/effective chronology when mapped carefully. Explicit MaterialStateRef remains separate from engine temporal coordinates.

Classification: `PRIMARY-EVIDENCE-SUFFICIENT / DISTINCTIVE STRENGTH`.

### SC-012 / SC-015 — identity, relation/cardinality fidelity

The mapping can preserve identity and relation meaning, but the engine provides no conventional foreign keys and no general uniqueness beyond `_id`.

Therefore every applicable mutation path must maintain referential/cardinality integrity through deterministic IDs, address tables and ASSERT discipline.

Classification:

```text
PRIMARY-KNOWN-COST
```

A local test can show one implementation path working; it cannot turn manual integrity enforcement into native integrity enforcement.

### SC-016 — selective disclosure

Representable, but full WL-H12 proof remains system-level. No unique XTDB advantage emerges here.

### SC-022 / 023 / 024 — temporal/recurrence

Strong temporal substrate, but recurrence/wall-clock semantics still require explicit LifeOS representation. Native bitemporality is helpful, not a replacement for recurrence semantics.

## 3. Known structural/operational costs

```text
no native FK
no general uniqueness beyond _id
manual ASSERT/address integrity discipline across every relevant writer
non-interactive transaction ergonomics
production topology / single-writer sensitivity HOLD
additional operational novelty relative to PostgreSQL
```

These costs remain even if a local functional test succeeds.

## 4. Why defer now

PM-05 found no currently unresolved scenario for which a local XTDB test is sufficiently likely to reverse the aggregate comparison versus PostgreSQL and TypeDB.

The distinctive temporal value remains real, but the present evidence says:

```text
temporal benefit
< current combined primary-integrity + topology burden
for finalist-scope purposes
```

This statement is reopenable if later evidence changes the balance.

## 5. Reopen triggers

```text
native bitemporal query/evolution value becomes materially dominant under accepted LifeOS requirements
or
PostgreSQL/TypeDB finalist qualification exposes a material history/temporal weakness
or
XTDB referential/constraint/topology capability materially changes
or
PM-08/PM-09 sensitivity shows XTDB-specific temporal economics can change the recommendation
```

## 6. Disposition

```text
PRIMARY FINALIST
NO

CURRENT PRIMARY DISPOSITION
DEFER

REJECTED
NO

PM-05 EXECUTION-WORTHY GAP
0

DIRECT HG
NOT RUN

PRODUCTION TOPOLOGY
HOLD

PREFERRED
NO

SELECTED
NO
```
