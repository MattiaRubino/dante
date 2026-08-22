# ADR-010: PostgreSQL Persistence Constitution

- Status: **ACCEPTED**
- Date: 2026-08-22
- Scope: reusable PostgreSQL persistence doctrine for DANTE
- Normative detailed authority: `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- Closure evidence: `../development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

## Context

DANTE's Domain, Logical and Physical work closed the semantic model, representation families, high-risk non-collapse invariants and PostgreSQL 18 as the sole canonical persistence/material-history architecture.

CP6-02 then resolved the reusable PostgreSQL implementation doctrine that must hold across the concrete DANTE database rather than being re-decided separately for each later table or product vertical.

Project documentation governance requires a durable ADR for architectural decisions that materially affect persistence strategy, security, data ownership and schema evolution. This ADR records that acceptance without duplicating the full CP6-02 Constitution.

## Decision

DANTE accepts the **PostgreSQL Persistence Constitution** closed by CP6-02 as the reusable normative persistence doctrine for concrete database design, materialization and later application work.

The detailed rules live in:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

This ADR is the architectural decision record and rationale pointer; it is **not** a second copy of the Constitution.

## Durable consequences

### Canonical database family

```text
PostgreSQL 18 major family
= sole canonical DANTE persistence + material-history authority
```

Patch lifecycle remains separate from architectural selection:

```text
Physical / CP2 / CP3 exact patch   18.4 / historical exact evidence
current repository patch           18.6
18.6 technical regression          DIRECT REMOTE QA PASS
```

### Identity and reference addressing

- stable DANTE-owned independently addressable identity uses PostgreSQL native `uuid` with UUIDv7 generation policy;
- UUID order is a technical locality property, not semantic chronology;
- homogeneous `NativeRef` targets prefer direct foreign keys;
- genuinely heterogeneous `NativeRef` contracts require bounded native-address integrity rather than application-only `type + uuid`;
- `NativeRef`, `ScopedRecordRef`, `MaterialStateRef` and `ExternalRef` remain distinct contracts;
- one universal semantic Entity/Thing root is rejected.

### Material state and history

- consequential material state receives explicit material-state addressing/control when the closed model requires it;
- owner-specific rows own semantic state payloads;
- current accepted truth is represented explicitly rather than inferred from newest insertion/revision/UUID order;
- correction/replacement/reconciliation preserve typed historical lineage;
- material history is not a universal Fact/Version/Event ontology.

### Relations and types

- specific semantic relations use specific relational families;
- qualified/material/n-ary relations preserve their accepted semantics;
- native PostgreSQL types and declarative constraints are preferred over generic payload escape hatches;
- PostgreSQL `money` is not the canonical Monetary Amount representation;
- required semantics must not disappear into generic JSONB/EAV/property bags.

### Constraints, transactions and concurrency

- declarative database invariants are preferred where PostgreSQL can truthfully enforce them;
- application operations own the outer transaction;
- persistence adapters may flush but do not implicitly commit;
- `READ COMMITTED` remains the default, with expected-state/conditional-write/locking/`SERIALIZABLE` escalation only where actual semantics require it;
- operation-specific timeout/error classification remains explicit;
- ambiguous commit outcomes are not blindly retried.

### Idempotency

Persistent idempotency uses operation scope + idempotency key as reservation identity, with the normalized material-operation fingerprint retained separately for equality/conflict comparison.

```text
same scope + key + fingerprint       → replay/observe established result
same scope + key + different input   → conflict/reject
```

Idempotency does not become Domain identity.

### Migration and evolution

- Alembic is the deployed application-schema authority;
- one migration DAG/head is maintained;
- applied migration history is immutable;
- autogenerate output is candidate input, not authority;
- expand/backfill/verify/cutover/contract is used where compatibility requires it;
- destructive/history-sensitive operations require truthful recovery/evolution treatment;
- PostgreSQL DDL requiring autocommit/non-transactional execution is isolated deliberately and verified;
- PostgreSQL patch maintenance is platform maintenance, not an Alembic business revision.

### Privilege/security posture

The accepted database role separation remains:

```text
dante_owner      NOLOGIN
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE
dante_runtime    LOGIN NOINHERIT / runtime DML only
```

Runtime DDL is denied. Database security mechanisms do not redefine Domain `Authority`, `Consent`, `Actor`, `Person` or `Principal` semantics.

### Non-default specialist mechanisms

Selected capabilities such as PgBouncer, PowerSync/logical replication, transactional outbox, Restate, R2, recovery storage, pgvector/search projections and other specialist components are activated only when their real trigger exists. Selection does not imply day-one activation.

## Rejected alternatives / shortcuts

The accepted Constitution rejects as canonical defaults:

```text
universal Entity / Thing table
universal Relationship / edge table
canonical EAV/property-bag kernel
universal event ontology
generic Fact/Version semantic root
application-only polymorphic type+uuid integrity
UUID ordering as semantic chronology
global CASCADE delete policy
global SERIALIZABLE isolation
speculative partitioning/sharding
JSONB as a required-semantic escape hatch
```

## Relationship to prior ADRs

- ADR-003 retains historical rationale for PostgreSQL as the original primary-database direction; final current selection comes from the closed Physical Model and this ADR/Constitution.
- ADR-007 remains an active semantic guardrail: persistence representation may not redefine Domain/Logical ontology for convenience. Its old pre-selection Physical comparison is historical.
- This ADR does not reopen Domain, Logical or Physical decisions.

## Relationship to CP6

CP6-02 closed the reusable doctrine. CP6-03 must now derive the maximum non-speculative whole DANTE database blueprint from closed authorities; CP6-04 materializes that database; CP6-05 directly validates it and closes CP6.

The first product vertical remains a separate post-CP6 application phase.

## Reopen rule

Reopen this decision only if concrete contradictory implementation/operational evidence demonstrates that a specific accepted persistence rule or PostgreSQL architecture choice cannot preserve DANTE's closed semantics or required operational guarantees.

Implementation convenience, fewer joins, ORM preference or a generic-schema shortcut is not reopen evidence.