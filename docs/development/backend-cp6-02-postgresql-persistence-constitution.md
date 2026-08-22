# Backend CP6-02 — PostgreSQL Persistence Constitution

- **Status:** ACTIVE / CANDIDATE / PRE-CLOSURE / GATE 02 NOT PASSED
- **Created:** 2026-08-22
- **Branch:** `feature/logical-postgresql`
- **Original candidate PRE-SCOPE:** `b556f96d05889c8962efc0e727c208a56a4a0012`
- **Upstream checkpoint:** CP6-01 **CLOSED / GATE 01 PASS**
- **CP6 authority:** `docs/workstreams/logical-postgresql.md`
- **Business schema / migrations / SQLAlchemy business mappings / adapters:** **NOT AUTHORIZED / NOT STARTED**
- **Purpose:** close reusable PostgreSQL persistence doctrine for DANTE without designing every business table, reopening Domain/Logical/Physical architecture, or implementing Vertical #1.

This document is the **active CP6-02 candidate constitution**. It records the full design position after repository reconstruction, PostgreSQL/standard review, external engineering benchmark, the PostgreSQL 18.6 technical refresh and direct remote regression. It does not itself close Gate 02.

Current pre-closure flow:

```text
CP6-01
CLOSED / GATE 01 PASS
        ↓
CP6-02
POSTGRESQL PERSISTENCE CONSTITUTION
ACTIVE / CANDIDATE / PRE-CLOSURE
        ↓
PostgreSQL 18.6 foundation refresh
DIRECT REMOTE QA PASS
run 32568664940 @ ec3dc795b5e044daa3a77723c94a1b4b5b92865c
        ↓
18.6 release-note impact review
PASS / NO CURRENT POST-UPGRADE ACTION
        ↓
current-truth reconciliation
        ↓
final independent whole-Constitution review
        ↓
separate Gate 02 closure
```

Gate 02 remains **NOT PASSED** until the final independent review is clean and a separate closure write is explicitly authorized and verified.

---

## 1. Authority and non-reinterpretation rule

The constitution consumes, in precedence order:

1. current protected-main backend code/migrations/tests and accepted model/ADR truth;
2. closed Domain and Whole-Logical authority;
3. accepted PostgreSQL Physical mapping and Physical selection;
4. CP6-01 owner + cross-cutting coverage and Gate-01 closure;
5. CP3 real PostgreSQL persistence contract and direct technical evidence;
6. current official PostgreSQL/Python/SQLAlchemy/Alembic/psycopg documentation;
7. external engineering evidence used only as a comparison/pressure test, never as DANTE semantic authority.

This checkpoint **does not** reopen:

```text
57 / 57 Logical classification
15 LR-01 native owners
LR-01..LR-13 meanings
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef semantic separation
PostgreSQL as sole canonical persistence/material-history authority
owner-specific table/history/relation thesis
WL-H01..WL-H12
CP3 one-engine / one-session-per-operation / outer-transaction ownership
CP3 schema = dante
CP3 Alembic single-DAG/single-head governance
CP3 owner / migrator / runtime role model
```

Implementation convenience cannot create a new semantic root.

---

## 2. Rule vocabulary

Each rule is classified using:

```text
MUST
required DANTE persistence behavior

MUST NOT / FORBIDDEN
prohibited behavior

SHOULD
strong default; deviation requires explicit evidence and local rationale

MAY
allowed only when the stated trigger exists

VERTICAL-SPECIFIC
not a global CP6-02 choice; exact application belongs to CP6-03/05 or later vertical implementation

DIRECT-PROOF
architecture/mechanism is defined; executable proof remains at the assigned stage
```

A rule may be reopened only by concrete contradictory implementation/evidence, not by preference for simpler ORM code or fewer joins.

---

## 3. External evidence register

External evidence is deliberately separated from DANTE authority. It answers: “Does this design survive comparison with current platform standards and large real systems?”

| Evidence | Observation | DANTE disposition |
|---|---|---|
| EB-001 PostgreSQL 18.6 release notes — https://www.postgresql.org/docs/release/18.6/ | 18.6 released 2026-08-13; 18.5 skipped; fixes from 18.4 including security/maintenance items; 18.x update does not require dump/restore | **ADOPT lifecycle implication**: PostgreSQL major 18 remains architecture; patch target moves to latest vetted 18.x; CP3 18.4 evidence remains historically exact |
| EB-002 PostgreSQL UUID — https://www.postgresql.org/docs/18/datatype-uuid.html | PostgreSQL supports RFC 9562 UUID and native UUIDv7 | **ADOPT** UUIDv7 for stable DANTE-owned independent identities |
| EB-003 PostgreSQL UUID functions — https://www.postgresql.org/docs/18/functions-uuid.html | `uuidv7()` is time-ordered and exposes extractable timestamp | **ADOPT with barrier**: ordering/locality aid only; timestamp is not semantic chronology |
| EB-004 Python 3.14 UUID — https://docs.python.org/3.14/library/uuid.html | Python 3.14 supports `uuid.uuid7()` with within-millisecond monotonicity | **ADOPT** application-side UUIDv7 generation capability |
| EB-005 RFC 9562 — https://www.rfc-editor.org/rfc/rfc9562.html | UUIDv7 defines Unix-time-ordered 128-bit identifiers | **ADOPT standard** |
| EB-006 PostgreSQL constraints — https://www.postgresql.org/docs/18/ddl-constraints.html | FK, CHECK, UNIQUE, EXCLUDE and NULL semantics are DB-enforceable; CHECK is row-local | **ADOPT** declarative-first constraint doctrine |
| EB-007 PostgreSQL 18 temporal constraints — https://www.postgresql.org/docs/18/sql-createtable.html | `WITHOUT OVERLAPS` and `PERIOD` can express temporal uniqueness/coverage | **ADOPT WHEN SEMANTICS MATCH**, never blanket-use |
| EB-008 PostgreSQL RLS — https://www.postgresql.org/docs/18/ddl-rowsecurity.html | owner/BYPASSRLS bypass exists; referential integrity bypasses RLS and may create covert channels | **ADAPT** as defense-in-depth only; **REJECT** RLS as Domain Authority/Consent/Visibility truth |
| EB-009 IANA TZDB — https://www.iana.org/time-zones | TZDB changes with political offset/DST rules; current review version 2026c | **ADOPT** IANA-zone semantics for future civil time |
| EB-010 ISO 4217 — https://www.iso.org/iso-4217-currency-codes.html | explicit three-letter/three-digit currency representation and minor-unit metadata | **ADOPT** explicit currency semantics |
| EB-011 Stripe idempotency — https://docs.stripe.com/api/idempotent_requests | same key replays prior result; incompatible parameters under same key error | **ADAPT** scope + key + material-operation fingerprint |
| EB-012 Stripe online migrations — https://stripe.com/blog/online-migrations | dual-write/backfill/read-cutover/write-cutover/removal for large online changes | **ADAPT** expand → migrate/backfill → verify → cutover → contract |
| EB-013 GitLab migration guide — https://docs.gitlab.com/development/migration_style_guide/ | zero-downtime discipline, staged operations, roll-forward production practice, explicit irreversible cases | **ADAPT** migration classes, lock-risk review, truthful reversibility |
| EB-014 Linear local-first — https://linear.app/now/rebuilding-delta-sync-read-path | clients keep local DB; checkpoint/delta-sync is permission-aware | **ADAPT**: local identity/sync can exist without granting local canonical effect authority |
| EB-015 Linear CASCADE incident — https://linear.app/now/linear-incident-on-jan-24th-2024 | destructive cascade in migration deleted broad dependent production data | **ADOPT barrier**: `ON DELETE NO ACTION` default; CASCADE requires explicit semantic proof |
| EB-016 Notion Postgres sharding — https://www.notion.com/blog/sharding-postgres-at-notion | single Postgres served five years/four orders growth; sharding introduced under measured CPU/VACUUM/TXID pressure | **REJECT premature sharding/partitioning**; preserve future locality possibilities |
| EB-017 Notion re-shard — https://www.notion.com/blog/the-great-re-shard | PgBouncer + Postgres fleet, data locality by workspace, zero-downtime re-shard | **ADAPT principle only**; no present DANTE sharding topology |

External evidence never overrides the closed Logical/Physical model. `ADOPT` means “compatible and useful for DANTE”, not “copy company architecture”.

---

## 4. Technology lifecycle constitution

### TECH-01 — Architecture binds capability/major family, not a forever patch

```text
PostgreSQL architecture authority
= PostgreSQL major 18

maintenance patch
= lifecycle-managed dependency
```

A compatible PostgreSQL 18 maintenance/security patch does **not** reopen Domain, Logical or Physical architecture.

### TECH-02 — Current PostgreSQL patch and exact evidence

Current version truth:

```text
Physical exact phase-time PostgreSQL patch       18.4
CP2 / CP3 directly executed PostgreSQL version   18.4
current supported PostgreSQL 18 technical patch  18.6
```

Therefore:

```text
CP2 / CP3 18.4 direct evidence
REMAINS TRUE HISTORICAL EXACT EVIDENCE

PostgreSQL 18.6
CONFIGURATION REFRESH APPLIED
DIRECT REMOTE FOUNDATION REGRESSION PASS
Backend CI run 32568664940
executed HEAD ec3dc795b5e044daa3a77723c94a1b4b5b92865c
```

The 18.6 regression directly built the pinned `postgres:18.6-trixie` base, preserved PostGIS 3.6.4 and pgvector 0.8.6, passed the 32-test fast lane, passed the 18-test real-PostgreSQL lane and passed the aggregate Backend CI Gate.

No prior test record is rewritten as if it ran on 18.6.

### TECH-03 — Stable release channel only

Production/foundation targets MUST use stable supported releases. Alpha/beta/RC releases MUST NOT replace a selected stable dependency merely to obtain new features.

At review time:

```text
Python       3.14.7
SQLAlchemy   2.0.52
Alembic      1.19.1
psycopg      3.3.4
PostGIS      3.6.4 stable line
pgvector     0.8.6
PgBouncer    1.25.2
```

PostGIS 3.7 beta and SQLAlchemy 2.1 pre-release are not reasons to move DANTE now.

### TECH-04 — Extension/dependency patch review

Before a major persistence/release checkpoint:

- supported patch status SHOULD be checked;
- security/critical fixes MUST be reviewed;
- upgrade impact MUST be classified as patch maintenance vs architecture change;
- direct evidence MUST remain tied to the exact executed version.

PostgreSQL 18.6 release-note impact was reviewed for the materialized DANTE boundary. Current DANTE has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring a current post-upgrade action.

Result:

```text
POSTGRESQL 18.6 RELEASE-NOTE IMPACT
PASS / NO CURRENT POST-UPGRADE ACTION
```

This result is bounded to the current materialized foundation. When PowerSync/logical replication is activated, the activation boundary MUST review the then-current PostgreSQL logical-decoding policy, including `output_plugin_libraries`, and all then-applicable upgrade actions.

### TECH-05 — No activation by selection alone

Selected capabilities MUST NOT be materialized merely because they appear in the Physical stack. Activation requires a real consumer/need.

This applies to PgBouncer, PowerSync, Restate, R2, pgBackRest/S3, OR-Tools and any later specialist component.

---

# Part I — Identity and reference addressing

## 5. ID — Physical identity constitution

### ID-01 — Stable DANTE-owned independent identity uses PostgreSQL `uuid` + UUIDv7

`NativeRef`, justified `ScopedRecordRef`, and `MaterialStateRef` MUST use PostgreSQL `uuid` values generated as UUIDv7.

Rationale:

- independent issuance across DANTE families;
- no dependence on one database sequence;
- compatibility with future bounded offline issuance;
- time-ordered locality without using identity as chronology;
- first-class PostgreSQL/Python support.

### ID-02 — UUIDv7 is not universal row decoration

The following MUST NOT be inferred from ID-01:

```text
every table has UUID PK
every relation has surrogate identity
every value has identity
every lookup has UUID
```

A simple relation MAY use its natural endpoint/composite key when that is the full semantic identity. LR-04 values inherit identity from their owner. Bounded local technical rows MAY use another appropriate key when no DANTE-stable address is required.

### ID-03 — Generation authority is application-boundary, backend-default

Default online canonical creation:

```text
backend application boundary
→ Python uuid.uuid7()
```

The database MAY generate UUIDv7 for bounded technical records where DB-side generation is specifically justified, but the database MUST NOT become the only possible issuer of DANTE stable identity.

A future explicitly authorized offline/local-first protocol MAY permit client-side UUIDv7 issuance when stable pre-sync identity is required. That future permission does not grant the client authority to accept a canonical effect.

### ID-04 — Identity is immutable and never reused

Once assigned, DANTE stable identity MUST NOT change and MUST NOT be reused for another semantic referent, including after retirement/redaction/tombstoning.

### ID-05 — UUIDv7 timestamp is non-semantic

UUIDv7 ordering/timestamp MUST NOT substitute for:

```text
created_at
recorded_at
accepted_at
effective_at
MaterialState revision
world chronology
knowledge chronology
```

Semantic time is stored explicitly.

### ID-06 — Identity is not secrecy or authorization

A UUID MUST NOT be treated as a capability token, authorization proof or privacy boundary. If external exposure of a stable ID creates WL-H12 leakage, a bounded public locator/token MAY be introduced later without changing canonical identity.

### ID-07 — Semantic reference types remain distinct above SQL

Even when persisted as the same PostgreSQL `uuid` type, application/domain contracts MUST preserve the distinction among `NativeRef`, `ScopedRecordRef`, `MaterialStateRef` and technical IDs. Raw UUID interchange MUST NOT erase reference-family eligibility.

### ID-08 — No embedded semantic type bits

DANTE MUST NOT encode owner family, lifecycle or authorization semantics into custom UUID bits. Owner/family eligibility remains explicit schema/contract data.

### ID-09 — Sequence/integer IDs remain allowed for bounded technical locality

Sequences/identity integers MAY be used for technical counters/order positions/internal append identifiers where global DANTE addressability is not required. They MUST NOT silently become NativeRef/ScopedRecordRef/MaterialStateRef.

---

## 6. REF — Reference addressing constitution

### REF-01 — Homogeneous Reference Contract → direct FK

When a reference slot accepts one concrete persistent target family, it MUST use a direct PostgreSQL foreign key unless concrete contradictory evidence exists.

### REF-02 — Small closed heterogeneous contract MAY use explicit one-of-N FKs

When a heterogeneous reference:

- accepts a small explicit stable set of target families;
- appears in few concrete contracts;
- is not itself a cross-cutting reusable address;

it MAY use one nullable FK column per eligible family plus a row-local exactly-one presence constraint.

No numeric threshold such as “three types” is constitutional; topology is justified by reuse/evolution/query pressure.

### REF-03 — Reusable/cross-cutting heterogeneous address MAY use bounded anchor

A separate address anchor is justified only when the heterogeneous address itself must be stable/reusable across multiple consumers or when repeating one-of-N FKs would obscure the accepted ReferenceAddress contract.

### REF-04 — Anchor is technical address infrastructure only

An address anchor MUST contain only bounded address/control data, such as:

```text
address identifier
reference family / eligible owner-family discriminator
owner existence binding
minimal retirement/tombstone continuity metadata when required
```

It MUST NOT own generic Domain fields such as name/title/description/status/generic properties/business lifecycle payload.

### REF-05 — No universal address root

Native, scoped, material-state and external addressing MUST NOT collapse into one universal semantic `kind + id` table.

If physical anchors are required, their families remain separated by semantic address class.

### REF-06 — `type + uuid` without DB integrity is FORBIDDEN

A polymorphic pair checked only by application code does not satisfy DANTE referential integrity. The database MUST be able to reject an ineligible family and a dangling target through FK/anchor/constraint/trigger machinery appropriate to the concrete topology.

### REF-07 — ScopedRecordRef remains contextual

An LR-02/qualified relation receives a stable ScopedRecordRef only when independent addressability, history, reconciliation or cross-record referencing justifies it. Persistence convenience MUST NOT inflate every dependent record into a native owner.

### REF-08 — MaterialStateRef references exact semantic state

MaterialStateRef MUST point to an explicit accepted material-state address. It MUST NOT be represented by MVCC token, updated timestamp, row hash, ETag, provider revision or “latest row”.

### REF-09 — ExternalRef is issuer-scoped

ExternalRef persistence MUST preserve enough issuer scope to make the external identifier unambiguous, potentially including:

```text
provider/source
integration instance / tenant / account / realm
provider object kind
opaque provider identifier
```

Provider revision/state is separate from ExternalRef identity.

### REF-10 — Composite optional FK presence is all-or-none

When a composite reference is optional, partially-populated tuples MUST be rejected. Use `MATCH FULL` or an equivalent explicit all-present/all-absent constraint where applicable.

### REF-11 — Delete action default is `NO ACTION`

Foreign-key delete behavior MUST be explicit in reviewed business DDL.

Default:

```text
ON DELETE NO ACTION
```

`CASCADE` MAY be used only when the child is semantically lifecycle-dependent, owns no required independent history/addressability/provenance, and deletion with the parent is the truthful domain behavior.

`SET NULL` MAY be used only when “referent no longer available” is semantically valid and distinguishable from “never known”.

### REF-12 — Primary semantic IDs do not update

Stable DANTE identity is immutable; `ON UPDATE CASCADE` is not a normal DANTE pattern for NativeRef/ScopedRecordRef/MaterialStateRef.

### REF-13 — Deferrable reference validity is semantic, not convenience

A FK/unique constraint SHOULD be immediate by default. `DEFERRABLE` MAY be used when a valid transaction legitimately passes through a temporarily-invalid intermediate state but MUST be valid at transaction commit.

### REF-14 — Current canonical topology stays one PostgreSQL authority

No cross-database canonical FK/reference strategy is introduced in CP6-02. Future sharding/partitioning requires measured evidence and a separate architecture boundary.

---

# Part II — Material truth, history, time, missingness and lifecycle

## 7. MAT — Material-state constitution

### MAT-01 — Materiality threshold

A state/facet MUST receive explicit MaterialStateRef/history when at least one of the following applies:

1. a later consequential decision/effect must bind the exact accepted state;
2. stale-write detection must compare semantic state rather than storage revision;
3. historical correction/reconstruction changes meaning;
4. multiple parties/governance acts bind to the same exact terms/state;
5. provider/reconciliation must distinguish competing accepted versions;
6. a consequential LR-08 projection must retain exact source basis;
7. retention/audit requirements require truthful past material state.

Low-consequence mutable descriptive data MUST NOT be forced into full material history without one of these pressures.

### MAT-02 — Owner/facet-specific material state

Material state is owned by the concrete semantic owner/facet. DANTE MUST NOT create a universal canonical Fact/Version/Event payload table to hold all business state.

### MAT-03 — Accepted material state is immutable-by-policy

After acceptance, semantic payload of a material state SHOULD be append-retained/immutable. Correction/replacement creates a new material state plus lineage rather than silently overwriting the old meaning.

Privacy/redaction operations MAY remove or replace protected payload under LIFE rules while preserving only permitted continuity.

### MAT-04 — Current accepted state is explicit binding

Where an owner/facet has material current truth, currentness MUST be represented by an explicit binding/relation/pointer to one accepted MaterialStateRef. `MAX(revision)`, insertion order or UUIDv7 order MUST NOT define semantic current truth.

### MAT-05 — One current accepted state per owner/facet where the model requires singular currentness

The concrete schema MUST enforce the relevant uniqueness/invariant through declarative constraint or transaction-safe mechanism. Exact table shape is CP6-03/05.

### MAT-06 — Material-state address and storage revision are separate

A storage mapping/schema revision MAY accompany a material row for migration/evidence needs, but it MUST NOT become material-state identity or semantic revision ordering.

### MAT-07 — Lineage is typed

Correction, replacement, supersession and reconciliation are not one generic edge. Where lineage is persisted it MUST preserve the applicable typed reason/relationship.

### MAT-08 — Derived/provider state cannot become current canonical binding automatically

LR-08/LR-09 data may propose or inform a new canonical state but MUST NOT overwrite current accepted material state without the governed acceptance path.

### MAT-09 — Expected-state uses semantic basis

A stale-write-sensitive operation MUST bind the expected MaterialStateRef or a documented semantic equivalent. Comparing only `updated_at`, ETag, MVCC xid/xmin or provider revision is insufficient.

### MAT-10 — No universal material-state table is mandated at CP6-02

The constitution defines semantics and reusable constraints. Whether a bounded material-state address/control anchor is physically justified is decided in CP6-03 from real cross-family consumers; owner-specific material-state rows remain the default accepted thesis.

---

## 8. HIST — Historical truth constitution

### HIST-01 — History is materiality-driven

DANTE MUST retain history where meaning/reconstruction requires it; it MUST NOT event-source every mutable row.

### HIST-02 — Current reads do not replay lifetime history

Normal current-state queries SHOULD use owner/current-binding structures directly. Lifetime replay is not the canonical current-state read model.

### HIST-03 — Historical reconstruction uses retained semantic states

Historical queries MUST reconstruct from retained material states + typed lineage/provenance, never by interpreting today’s mutable row as yesterday’s truth.

### HIST-04 — Technical audit and Domain history stay distinct

Technical operation/provenance records MAY reference Domain/material states, but a technical audit log MUST NOT become the Domain history ontology.

### HIST-05 — Old rows keep old meaning

Schema evolution MUST NOT silently reinterpret historical rows under a new semantic shape. Migration/backfill must explicitly preserve or transform meaning with evidence.

### HIST-06 — Historical payload changes require exceptional policy

Material history SHOULD NOT be updated in place except for controlled privacy/redaction/repair operations that preserve truthful allowed continuity and explicit provenance.

### HIST-07 — History retention is minimal but sufficient

Retain only history justified by semantic, legal, product and recovery obligations. “Store everything forever” is not a constitution rule.

---

## 9. TIM — Temporal constitution

### TIM-01 — Absolute instants use `timestamptz`

An absolute instant MUST use PostgreSQL `timestamp with time zone` (`timestamptz`). Application serialization MUST make timezone/offset explicit.

### TIM-02 — Date-only semantics use `date`

Birthdays, all-day dates, due dates or other true civil dates MUST NOT be converted to midnight UTC merely for storage uniformity.

### TIM-03 — Time-of-day uses `time without time zone` only for true wall-clock semantics

`timetz` SHOULD NOT be used as a substitute for named-zone civil-time semantics.

### TIM-04 — Future named-zone civil time preserves IANA zone

A future wall-clock meaning such as “09:00 Europe/Rome” MUST preserve local civil date/time semantics plus an IANA zone identifier. A historical UTC offset alone MUST NOT freeze future recurrence behavior.

### TIM-05 — Consequential resolved instants may preserve resolution basis

When later reconstruction matters, persist the resolved instant and enough accepted offset/zone/material-state basis to explain how a civil time became that instant.

### TIM-06 — Interval semantics SHOULD use range/multirange types when they match meaning

PostgreSQL date/timestamp range and multirange types SHOULD be preferred for genuine intervals/sets of intervals, with boundary semantics explicit.

Half-open `[start,end)` is the default engineering convention for contiguous scheduling/availability unless the Domain contract requires different inclusion semantics.

### TIM-07 — Precision/granularity is explicit

Do not infer semantic precision from missing seconds, rounding or display formatting. Persist granularity/precision/frame when it changes meaning.

### TIM-08 — Dual chronology is conditional, not universal

Store separate world/effective and recorded/learned/accepted chronology only where material. DANTE MUST NOT introduce a universal bitemporal Fact table.

### TIM-09 — Recurrence binds rule version

A differentiated/lazy occurrence must retain the governing source and applicable MaterialStateRef of the recurrence/routine/event state used to derive it.

### TIM-10 — PostgreSQL 18 temporal constraints are preferred when exact

`WITHOUT OVERLAPS`, `PERIOD`, EXCLUDE and range constraints MAY enforce temporal uniqueness/coverage where their exact semantics match the DANTE invariant. They MUST NOT be used as approximate replacements for richer scheduling/capacity logic.

---

## 10. MISS — Missing/unknown/negative constitution

### MISS-01 — SQL NULL has local contract meaning only

`NULL` means “no SQL value for this attribute under this concrete contract”. It MUST NOT globally mean false, declined, inactive, unknown, unavailable, redacted or not-applicable.

### MISS-02 — Row absence is not explicit negative

No record MUST NOT be interpreted as a known negative unless the owner-specific contract explicitly defines that closed-world meaning.

### MISS-03 — Explicit negative is stored explicitly

When “no/false/rejected/not-realized” is meaningful, persist the appropriate boolean/state/result semantics rather than relying on absence.

### MISS-04 — Unknown / N-A / redacted / unavailable / retired remain distinguishable where observable

These states MAY use owner-specific typed status/reason fields or records. DANTE MUST NOT introduce one universal MissingReason enum for every concept.

### MISS-05 — Sentinel values are FORBIDDEN

Do not encode missingness as `0`, empty UUID, magic date, empty currency, empty string or provider-specific pseudo-value when the semantic state is different.

### MISS-06 — UNIQUE + NULL semantics must be deliberate

Where multiple NULLs would violate the intended invariant, use `NULLS NOT DISTINCT`, explicit predicate constraints or another truthful representation rather than assuming NULL equality semantics.

### MISS-07 — Composite optional semantics are complete tuples

Partial owner/ref/time/value tuples that have no valid semantic interpretation MUST be rejected.

---

## 11. LIFE — Lifecycle / retention / tombstone constitution

### LIFE-01 — No universal soft-delete column

DANTE MUST NOT add `deleted_at`/`is_deleted` to every table by convention. Lifecycle semantics are owner-specific.

### LIFE-02 — Hard deletion is policy-driven

Native/material/governance/history data MUST NOT be hard-deleted merely for cleanup convenience. Physical removal is permitted when the applicable retention/privacy contract requires it and the allowed continuity semantics are preserved.

### LIFE-03 — Tombstone is minimal continuity, not hidden full data

A tombstone/address-retention record may preserve only the minimal permitted identity/lineage/chronology needed to avoid false “never existed” reconstruction and dangling history.

### LIFE-04 — NativeRef non-reuse is absolute

A retired/redacted/deleted NativeRef MUST never be reassigned to another semantic referent.

### LIFE-05 — Cascade deletion is exceptional

`CASCADE` requires explicit semantic lifecycle proof under REF-11. ORM cascade configuration MUST NOT silently exceed database/domain lifecycle semantics.

### LIFE-06 — Redaction/unavailable are not non-existence

Where policy permits continuity, downstream history/projections must preserve the distinction between redacted/unavailable and never existed.

### LIFE-07 — Deletion/redaction propagation has explicit owners

Activated projection/search/local/provider/object systems MUST have an invalidation/purge/reconciliation path. Canonical deletion alone is not sufficient evidence of downstream erasure.

### LIFE-08 — Old-backup anti-resurrection remains direct-proof work

Restore/recovery must reconcile restored data with current deletion/redaction policy. PSV-01/HG-09 remain unpassed until destructive evidence exists.

---

# Part III — Types, relations, constraints and indexes

## 12. TYP — PostgreSQL type constitution

### TYP-01 — Prefer native typed columns over generic payloads

Required semantics SHOULD use PostgreSQL native scalar/range/array/geo/vector types and explicit relational structure rather than text/JSON encoding.

### TYP-02 — `text` is default variable-length string

`varchar(n)` SHOULD be used only when the length bound itself is a real semantic/external-protocol invariant. Arbitrary UI-era length limits do not belong in canonical schema.

### TYP-03 — Finite-state choice is evolution-driven

Use:

```text
PostgreSQL ENUM
MAY — genuinely closed/stable database-level vocabulary

text + CHECK
SHOULD — small application-owned vocabulary expected to evolve

reference/lookup relation
SHOULD — runtime-extensible, metadata-bearing, governed or relationship-bearing vocabulary
```

Integer-coded application enums MUST NOT be the default because they obscure persisted meaning; they require a measured/storage or compatibility reason.

### TYP-04 — Boolean is only true binary semantics

If unknown/not-applicable/withheld is materially distinct, a nullable boolean without explicit contract MUST NOT pretend to be tri-state domain modeling.

### TYP-05 — Exact quantities use `numeric`

Financial/decimal exact values MUST use exact numeric representation. Floating types MAY be used for inherently approximate measurements where precision/error semantics are accepted.

### TYP-06 — PostgreSQL `money` is FORBIDDEN for DANTE Monetary Amount

MonetaryAmount uses exact numeric amount plus explicit currency code. Locale-dependent PostgreSQL `money` is not canonical DANTE money semantics.

### TYP-07 — Currency uses explicit ISO 4217 code semantics

Currency code MUST be explicit. Decimal/minor-unit rules MUST come from currency/domain metadata, not one global hard-coded scale.

### TYP-08 — Integer width is evidence-driven

Use the smallest practical type that safely covers the semantic/operational range. `bigint` MAY be the default for unbounded technical counters expected to grow, but it is not a universal business scalar.

### TYP-09 — JSONB is bounded

JSONB MAY be used for:

```text
LR-10 low-consequence flexible metadata
provider/raw payload
bounded specialist extension detail
bounded technical diagnostic/provenance metadata
```

Required owner identity, relation, material state, governance, history or concurrency semantics MUST NOT disappear into JSONB.

### TYP-10 — Arrays require true value-collection semantics

PostgreSQL arrays MAY store bounded homogeneous values when elements have no independent identity/history/governance and do not need relational integrity/querying as first-class rows. Otherwise use a related table.

### TYP-11 — Range/multirange types are preferred for genuine interval sets

Use them when inclusion/overlap/coverage semantics are intrinsic, especially when declarative constraints can enforce the invariant.

### TYP-12 — DOMAIN/composite types are reusable structural tools, not semantic roots

They MAY reduce repeated low-level validation/value structure when evolution remains manageable. They MUST NOT create generic Domain identity.

### TYP-13 — Generated columns are derived

Generated columns MAY support query/index convenience; required canonical source meaning MUST remain explicit and recoverable.

### TYP-14 — Provider IDs preserve provider comparison semantics

External identifiers are normally text/opaque values; case sensitivity/normalization follows the provider contract. DANTE MUST NOT globally lowercase/casefold provider IDs.

### TYP-15 — Deterministic equality is required for keys/references

Key/FK identity comparisons SHOULD use deterministic collation/equality semantics. Locale-aware search comparison belongs to query/search layers, not canonical identity.

---

## 13. REL — Relation constitution

### REL-01 — Simple binary LR-03 uses dedicated relation table/family

If the relation has no independent lifecycle/history/addressability beyond endpoints and relation-specific key fields, a composite endpoint key is preferred over an unnecessary surrogate identity.

### REL-02 — Qualified/material relation becomes contextual record

When a relation needs history, governance, provenance, state binding or independent addressability, it MUST become a qualified contextual record with ScopedRecordRef/MaterialStateRef as justified.

### REL-03 — N-ary semantics remain n-ary

Agreement and other true n-ary relations MUST NOT be decomposed into pairwise edges if doing so loses shared terms/state semantics. Use a relation/context header + typed participants/roles or equivalent concrete shape.

### REL-04 — Endpoint roles are explicit

Relation endpoints MUST preserve role meaning; generic `from/to` is insufficient where subject/owner/member/representative/etc. roles differ.

### REL-05 — Governance relation families stay distinct

Authority, Consent, Visibility, Representation, Responsibility, Membership, Participation, Ownership, Possession and Allocation MUST NOT collapse into a generic Permission/Relationship table.

### REL-06 — Material relation history follows MAT/HIST

A qualified relation whose past state changes consequential interpretation uses explicit MaterialStateRef/history rather than mutating one row in place.

### REL-07 — Symmetry/order normalization is vertical-specific

For symmetric relations, endpoint canonical ordering MAY be used to enforce uniqueness, but only where the Domain relation is truly symmetric. This is not a global relation rule.

### REL-08 — Relation deletion follows lifecycle semantics

No relation receives `CASCADE` simply because it is implemented as a join table.

---

## 14. CON — Constraint constitution

### CON-01 — Declarative DB enforcement first

A canonical structural invariant that PostgreSQL can express correctly SHOULD be enforced by the database, not only by Python validation.

Preferred order:

```text
NOT NULL / CHECK / FK / UNIQUE
→ partial UNIQUE / NULLS NOT DISTINCT
→ range / WITHOUT OVERLAPS / PERIOD / EXCLUDE
→ DEFERRABLE constraint
→ narrow trigger / transactional application invariant when declarative SQL is insufficient
```

### CON-02 — Required means `NOT NULL`

A CHECK expression that returns NULL does not replace `NOT NULL`.

### CON-03 — CHECK is row-local

CHECK constraints MUST NOT be used to pretend to enforce other-table/current-world facts. Cross-row/table invariants require FK/UNIQUE/EXCLUDE/transaction/trigger mechanisms.

### CON-04 — Uniqueness semantics include NULL policy

Each uniqueness rule MUST state whether missing values are distinct, equal, forbidden or outside the invariant.

### CON-05 — Referential integrity uses actual FK/anchor machinery

Application existence checks alone are insufficient for canonical DB-local references.

### CON-06 — DEFERRABLE is explicit

Use only when transaction-end validity is the semantic requirement. It is not a generic fix for insert-order problems.

### CON-07 — Temporal overlap/coverage uses native mechanisms when exact

Prefer range/EXCLUDE/`WITHOUT OVERLAPS`/`PERIOD` where they exactly represent the invariant.

### CON-08 — Trigger is last-resort invariant mechanism

A trigger MAY be used for a DB-local invariant that cannot be expressed declaratively. It must be narrow, deterministic, schema-qualified where applicable, documented, tested and MUST NOT become hidden business workflow/orchestration.

### CON-09 — Constraint rollout may be staged

For large/existing tables, migrations MAY create constraints with staged validation (`NOT VALID` then `VALIDATE`) or equivalent safe sequence when supported and justified.

### CON-10 — Constraint names remain deterministic

Consume the existing CP3 naming convention; constraint naming must remain stable enough for migrations, diagnostics and review.

---

## 15. IDX — Index constitution

### IDX-01 — Indexes exist for proven access/invariant needs

No “index every field” or “index every FK blindly” rule.

### IDX-02 — Referencing FK index review is mandatory

PostgreSQL does not automatically index referencing FK columns. Every FK MUST be reviewed for joins, parent delete/update checks and filter access; an index SHOULD be added when those paths justify it.

### IDX-03 — Composite index order follows real query shape

Leading equality/range/sort/filter usage determines column order. ORM field order is irrelevant.

### IDX-04 — Partial indexes require stable predicates

Use only when a real high-value workload repeatedly matches a stable predicate. Multiple partial indexes MUST NOT simulate partitioning.

### IDX-05 — INCLUDE is evidence-driven

Covering indexes MAY use INCLUDE when index-only scans materially help and payload columns remain narrow/stable. Bloat/write cost must be justified.

### IDX-06 — Range/geo/search/vector use appropriate access method

GiST/SP-GiST/GIN/HNSW/IVFFlat/etc. are selected by actual operator/query/capability requirements, not by technology enthusiasm.

### IDX-07 — Redundant indexes are FORBIDDEN

Before adding an index, review PK/UNIQUE/other indexes for prefix/equivalent coverage.

### IDX-08 — Large index construction uses migration-safe method

`CREATE INDEX CONCURRENTLY` or other staged approach MAY be required for live large tables. Transaction/lock behavior must be planned explicitly.

### IDX-09 — Patch upgrade maintenance findings are part of lifecycle QA

If PostgreSQL/extension release notes require REINDEX or cleanup, that becomes an explicit upgrade action/evidence item; it is not ignored because the major version stayed the same.

The PostgreSQL 18.6 review found no current DANTE GIN/`btree_gist`/`ltree` object requiring such action. This does not waive future release-specific review.

### IDX-10 — No speculative partitioning/sharding

Partitioning/sharding requires measured table/query/maintenance pressure and an explicit later architecture decision. CP6-02 does not pre-partition the 57-owner model.

---

# Part IV — Transactions, idempotency and provenance

## 16. TX — Transaction/concurrency constitution

### TX-01 — Outer application operation owns transaction

Inherited from CP3. Persistence adapters MAY flush but MUST NOT implicitly commit.

### TX-02 — Default isolation remains READ COMMITTED

DANTE MUST NOT switch the whole application to SERIALIZABLE. Stronger isolation/locking is selected by invariant/race class.

### TX-03 — Use narrowest truthful concurrency mechanism

Preferred progression:

```text
declarative invariant
conditional update / expected-state compare
row/key lock with deterministic order
predicate-safe SERIALIZABLE when required
```

### TX-04 — Expected-state check occurs inside the protecting transaction

A stale-write-sensitive mutation MUST compare current semantic state to expected MaterialStateRef within the same transaction that commits the new state/effect.

### TX-05 — SERIALIZABLE retry means whole application transaction

On a retryable serialization failure, retry the complete application operation logic that selected/read/computed/wrote the transaction, never merely the last SQL statement.

### TX-06 — Retry is explicit and bounded

No hidden SQLAlchemy/driver automatic transaction retry. Retry policy must identify retryable SQLSTATE classes, maximum attempts/backoff and external-effect safety.

Deadlock/serialization retry MAY be added only where the operation is safe to repeat under IDEM/provenance rules.

### TX-07 — Lock ordering is deterministic where multiple rows/owners are locked

Vertical design SHOULD define stable lock order to reduce deadlock risk.

### TX-08 — SAVEPOINT is exceptional partial-failure semantics

Inherited CP3 rule: nested transaction/savepoint is not default service composition. Use only when partial failure inside the outer operation is itself the truthful requirement.

### TX-09 — No network/human wait inside DB transaction

Long-lived waits, provider calls and human approval MUST NOT hold a PostgreSQL transaction open. Use staged state/outbox/durable runtime when real need exists.

### TX-10 — External atomicity is never fabricated

PostgreSQL transaction can atomically protect co-located canonical state. External/provider effect requires explicit pending/partial/reconciliation/compensation semantics.

### TX-11 — Advisory locks are a bounded fallback

PostgreSQL advisory locks MAY be used only when the invariant has a stable lock key and no clearer row/constraint/serialization mechanism is suitable. Advisory lock state is never semantic state.

### TX-12 — Ambiguous commit cannot be blind-retried

If the client loses connection after commit may have occurred, recovery MUST use idempotency/result lookup/reconciliation, not assume rollback and execute a second effect.

---

## 17. IDEM — Idempotency constitution

### IDEM-01 — Identity tuple

A persistent idempotency record, where required, is keyed by:

```text
operation scope
+ caller-provided/generated idempotency key
+ normalized material-operation fingerprint
```

### IDEM-02 — Same key + same material operation

May replay/return the prior accepted execution/result according to the operation contract rather than execute a duplicate effect.

### IDEM-03 — Same key + different material operation

MUST conflict. A key cannot be silently rebound to another operation.

### IDEM-04 — Concurrent duplicate requests serialize on the idempotency identity

Only one material execution may win. Waiting/replaying callers observe the established result/state rather than race into duplicate effects.

### IDEM-05 — Validation-before-reservation is bounded

Pure syntactic/authorization/precondition failures MAY occur before an idempotency record is reserved if no material execution started. Once execution is reserved/started, its fingerprint is immutable.

### IDEM-06 — Retention horizon is operation-specific

No universal Stripe-style 24-hour rule. Retain idempotency state for the actual retry/reconciliation horizon plus policy requirements, then expire only when replay ambiguity is acceptably closed.

### IDEM-07 — Fingerprint format is versioned

Normalization/fingerprinting rules MUST be deterministic and versioned if they may evolve. Raw sensitive request payload SHOULD NOT be duplicated merely for fingerprinting.

### IDEM-08 — Idempotency is not Domain identity/auth

Key/record MUST NOT become NativeRef, Request/Decision identity, authorization token or semantic provenance replacement.

### IDEM-09 — Provider effect requires provider-safe semantics

For external side effects, use provider idempotency where available plus DANTE reconciliation. DANTE retry must not assume an external effect failed merely because its response was lost.

---

## 18. PROV — Consequential provenance constitution

### PROV-01 — Consequential effect is reconstructible

Where consequence warrants it, retained provenance MUST be able to reconstruct applicable:

```text
operation family
semantic target/facet
expected MaterialStateRef
actual Actor
represented party
Principal/security-context reference
Authority / Consent / Visibility / Agreement material basis
purpose/context
idempotency reference
correlation/causation
resulting canonical effect/material state
provider/runtime outcome separately
```

### PROV-02 — Provenance is bounded, not universal payload logging

Store references, identifiers, fingerprints and minimal context needed for reconstruction. Do not duplicate sensitive business payloads into a generic audit blob.

### PROV-03 — AuthZ decision is technical evidence, not Authority

Persist policy/model version and technical allow/deny where required, while preserving separate Domain Authority/Consent/Visibility basis.

### PROV-04 — Principal != Actor != represented party

The persisted model must permit those axes to differ.

### PROV-05 — Correlation/causation IDs are technical

They MAY use stable technical identifiers to connect request, transaction, provider and workflow evidence. They MUST NOT become universal Domain Operation identity.

### PROV-06 — Runtime/provider outcome is separate from canonical effect

A workflow/provider receipt can link to the canonical effect but cannot define it automatically.

### PROV-07 — Privacy/retention applies to provenance too

Technical provenance is not exempt from minimization/redaction/retention policy.

---

# Part V — Capabilities, migrations, security and proof

## 19. CAP — PostgreSQL capability boundaries

### CAP-01 — PostGIS

PostGIS MAY store/query accepted geometry/geography attributes. Geometry/geography is not `Place` identity. Exact SRID/type/index design is Place/geo-vertical-specific. PSV-36 remains direct proof.

### CAP-02 — FTS / pg_trgm / unaccent

Search structures are derived/query state. Source canonical fields remain explicit. Ranking/result existence remains subject to WL-H12. SC-017/018 and PSV-06/07 remain staged.

### CAP-03 — pgvector

Vector embeddings/indexes are LR-08 derived retrieval state. Any material vector row MUST retain/reconstruct model/version/source/material-basis/freshness/security scope needed for safe use. Vector result is never canonical truth. PSV-37 remains staged.

### CAP-04 — JSONB

Bounded by TYP-09. JSONB is not the schema-evolution escape hatch for required semantics.

### CAP-05 — Views/materialized views/cache

Views are preferred for cheap derivation. Materialized/cache tables require demonstrated cost/latency benefit and explicit freshness/material-basis behavior.

### CAP-06 — PostgreSQL RLS is optional defense-in-depth

RLS MAY supplement application disclosure/security enforcement. It MUST NOT become DANTE Authority, Consent or Visibility semantics. Any activated RLS design must test owner/BYPASSRLS behavior and covert leakage through FK/UNIQUE/errors/counts/timing.

### CAP-07 — PgBouncer remains selected, not active by default

Activation requires connection-pressure value and compatibility proof. Migration/provisioning connections SHOULD bypass transaction pooling when session/DDL behavior requires it. PSV-38/39 remain staged.

### CAP-08 — PowerSync/local SQLite remains noncanonical

Only approved downstream projections/local staging may sync. Local mutation never becomes canonical solely because it exists offline. Consequential conflict/governance is resolved by backend acceptance. PSV-11..20 remain staged.

When PowerSync/logical replication is activated, its technical gate MUST review current PostgreSQL logical-decoding restrictions and allowlisting, including `output_plugin_libraries` in PostgreSQL 18.6+, rather than assuming the current dormant posture qualifies future replication runtime.

### CAP-09 — Transactional outbox is Class-A runtime mechanism

Activate only on real asynchronous external/publication need. Outbox is technical runtime state, not Domain history or universal event store.

### CAP-10 — Restate remains Class-B trigger-bound

No Restate state/schema is introduced until a real durable workflow needs it.

### CAP-11 — R2/pgBackRest/S3/OR-Tools/telemetry remain bounded by their accepted triggers

Selection does not authorize materialization in CP6-02.

### CAP-12 — No sharding/partitioning until measured pressure

DANTE remains one canonical PostgreSQL authority. Future sharding/partitioning requires measured CPU/I/O/VACUUM/table-size/query/locality pressure, not hypothetical scale. Future design should preserve locality possibilities without paying distributed-system cost now.

---

## 20. MIG — Migration/evolution constitution

### MIG-01 — Alembic remains deployed-schema authority

One environment, one DAG, one canonical integrated head, online migrations, `dante.alembic_version`, reviewed revisions.

### MIG-02 — Applied migration history is immutable

Never edit a merged/applied revision to “fix history”. Create a new forward correction.

### MIG-03 — Autogenerate is candidate only

Alembic autogenerate may discover structural changes, including current named CHECK support, but humans must verify semantics, lock behavior, ownership, data migration and downgrade truth.

### MIG-04 — Every migration gets a class

Use at least:

```text
MIG-A simple transactional schema change
MIG-B additive compatibility change
MIG-C expand → backfill/migrate → verify → cutover → contract
MIG-D destructive/history-sensitive change
MIG-E capability/runtime activation change
```

Class drives review/evidence.

### MIG-05 — Compatibility-first evolution

Changes SHOULD be additive/backward-readable while old/new application versions may overlap. Destructive rename/drop/type replacement normally requires staged rollout.

### MIG-06 — Large data movement is separated from blocking DDL

Backfills SHOULD be chunked/resumable/observable and separated from short schema DDL when scale/lock risk warrants it.

### MIG-07 — Backfill has checkpoint and verification

A material backfill must define selection, batching, restart safety, validation/reconciliation and completion evidence.

### MIG-08 — Read/write cutover is explicit

For MIG-C changes, document when reads switch, when writes switch, how consistency is verified, and when old structure can be removed.

### MIG-09 — Heavy index/constraint work uses safe PostgreSQL mechanics

Use concurrent index creation, `NOT VALID` + validation, split migrations or other safe sequence where table size/live traffic makes ordinary DDL lock risk unacceptable.

### MIG-10 — Lock/statement timeout is deliberate

Potentially blocking migration statements SHOULD have bounded lock-risk policy. Disabling a timeout requires an explicit reason and operational plan.

### MIG-11 — Reversibility must be truthful

A downgrade MUST NOT fabricate restoration of deleted/rewritten semantic evidence. If a migration is inherently irreversible, document it explicitly and define forward-fix/recovery strategy.

Production recovery normally prefers roll-forward when rollback would conflict with deployed data/code semantics.

### MIG-12 — Destructive changes require stronger gate

Dropping canonical data/history/reference structures requires evidence that:

- reads/writes are cut over;
- required data/history is migrated or lawfully removed;
- references/material states remain valid;
- recovery/backup implications are known.

### MIG-13 — Stable-address continuity is mandatory

Schema evolution MUST preserve NativeRef, ScopedRecordRef and MaterialStateRef semantics unless a separately-approved semantic migration explicitly maps them.

### MIG-14 — Historical/governance meaning survives evolution

An old Agreement/Consent/Authority/Schedule/etc. material state must remain interpretable under its accepted meaning after schema evolution.

### MIG-15 — No `schema_version` on every row by default

Migration/mapping revision is an evidence/technical concern. Per-row revision metadata is added only where historical decoding actually requires it.

### MIG-16 — PostgreSQL patch upgrade is platform maintenance, not business Alembic migration

18.4 → 18.6 belongs to the technical PostgreSQL image/envelope and regression boundary. Business migration history is not rewritten to represent the server patch.

The actual 18.6 refresh has now directly validated this boundary without adding an Alembic revision.

### MIG-17 — Major PostgreSQL upgrade is separate architecture/runtime boundary

Moving 18 → 19 is not automatic patch maintenance and requires compatibility/performance/extension/migration review.

### MIG-18 — `metadata.create_all()` remains forbidden as deployment authority

Inherited from CP3.

---

## 21. SEC — Database ownership/privilege constitution

### SEC-01 — CP3 role model is frozen

```text
dante_owner      NOLOGIN object/schema owner
dante_migrator   LOGIN NOINHERIT with bounded SET ROLE dante_owner
dante_runtime    LOGIN NOINHERIT runtime DML posture
```

Future business objects inherit this posture.

### SEC-02 — Runtime has least privilege

Runtime receives only required DML/schema usage/sequence/type usage. No schema CREATE, DDL, owner membership, TRUNCATE, TEMP, migration-history access or routine EXECUTE by default.

### SEC-03 — Migration/admin secrets stay outside normal backend runtime

Normal app startup MUST NOT receive admin/migrator credentials.

### SEC-04 — Migration/provisioning SQL is explicit and schema-safe

Administrative SQL SHOULD be schema-qualified where ambiguity/search-path manipulation could matter. Existing `search_path=dante,public` runtime posture does not authorize unqualified privileged maintenance code.

### SEC-05 — Routine EXECUTE is deny-by-default

New routines/functions do not automatically become runtime capability. Grants are explicit and reviewed.

### SEC-06 — SECURITY DEFINER is exceptional

A SECURITY DEFINER function MAY exist only when the privilege boundary cannot be safely expressed otherwise. It requires fixed safe search_path, least privileges, explicit ownership and security tests.

### SEC-07 — RLS activation is table/vertical-specific

RLS is not required globally. If enabled, application role/owner behavior and policy coverage are directly tested; RLS does not replace service authorization or Domain governance.

### SEC-08 — PUBLIC remains hardened

Do not restore broad PUBLIC schema/database/routine privileges that CP3 deliberately removed.

### SEC-09 — Recovery/backup identities are separate

Future pgBackRest/S3/recovery access must use bounded operational credentials and must not grant application runtime broader DB authority.

### SEC-10 — Test/provisioning isolation remains mandatory

Real PostgreSQL acceptance continues to use isolated disposable cluster/database/roles where provisioning tests would otherwise mutate ordinary LOCAL credentials/state.

---

## 22. QA — Direct persistence acceptance constitution

### QA-01 — PostgreSQL semantics require real PostgreSQL

SQLite/mocks MUST NOT qualify FK/range/locking/isolation/Alembic/role/RLS/PostGIS/pgvector PostgreSQL behavior.

### QA-02 — Exact server/extension version is recorded

Each direct evidence run records exact PostgreSQL patch and relevant extension versions.

### QA-03 — Patch refresh regression — CURRENT 18.6 PASS

The CP6 patch refresh has directly re-run the applicable CP2/CP3 technical foundation corpus on PostgreSQL 18.6 without changing business schema.

Exact evidence:

```text
Backend CI run                         32568664940
workflow event                         workflow_dispatch
executed HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c
PostgreSQL base                        postgres:18.6-trixie
base index digest                      sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS
Backend Quality                        SUCCESS
fast test lane                         32 / 32 PASS
Backend PostgreSQL                     SUCCESS
real PostgreSQL lane                   18 / 18 PASS
Backend CI Gate                        SUCCESS
current test corpus                    50 / 50 covered across mandatory lanes
```

The PostgreSQL lane directly covered Alembic fresh→head, head/base/head round-trip, no-drift check, privilege posture, runtime identity/search path, stale-connection recovery, outage/readiness recovery, commit/rollback/flush/savepoint semantics and related CP3 foundation behavior.

This must not be misreported as one single full-`pytest` 50/50 invocation; CI deliberately split the corpus into the fast and PostgreSQL lanes.

PostgreSQL 18.6 release-note-specific impact review is also complete:

```text
PASS / NO CURRENT POST-UPGRADE ACTION
```

The current boundary has no custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring an 18.6-specific action. Future activation/objects reopen only their applicable maintenance checks.

### QA-04 — Constraint proof is positive + negative

A vertical implementation must test valid rows and representative invalid rows for each material DB invariant.

### QA-05 — Reference proof includes wrong-family + dangling targets

PG-R02 is not passed by a successful happy-path FK only.

### QA-06 — History proof reconstructs past truth

Representative state changes/corrections must prove historical result does not depend on today’s current row.

### QA-07 — Missingness proof distinguishes absence/unknown/negative where material

WL-H04 must be exercised by real vertical semantics, not merely asserted in docs.

### QA-08 — Concurrency proof is multi-connection real race

Expected-state/write-skew/idempotency tests use independent real database connections/tasks and deterministic assertions.

### QA-09 — Migration proof includes fresh and upgrade path

For real business revisions:

```text
fresh DB → head
prior supported state → head
single canonical head
Alembic check/no drift
required data backfill verification
```

### QA-10 — Privilege proof uses actual runtime/migrator roles

Schema correctness under owner does not prove runtime authority boundaries.

### QA-11 — RLS/search/projection proof is activation-triggered

When activated, test WL-H12 surfaces including existence/count/rank/error/timing/source leakage, not only row contents.

### QA-12 — Destructive recovery/evolution proofs stay honestly staged

HG-09/HG-11/HG-12 and PSV-01/02/03/40 remain not-passed until real destructive recovery or real V1→V2 evolution exists.

### QA-13 — PSV-35 waits for first real representative business mapping

CP6 MUST NOT invent business tables merely to make PSV-35 green.

### QA-14 — Performance/index evidence is workload-driven

No arbitrary benchmark threshold is constitutional before representative data/query pressure exists. Explain plans/latency/cardinality/bloat become vertical/release evidence when relevant.

### QA-15 — Property-based/fuzz tests are encouraged for invariant-rich codecs/values

Hypothesis MAY be used for range boundaries, value normalization, fingerprints and constraint-adjacent pure logic, but it does not replace real PostgreSQL execution.

---

## 23. Vertical-specific decision register

The following are intentionally **not** global CP6-02 choices:

```text
exact business table names
exact business column names
exact owner-specific material-state table shape
whether a material-state address anchor is justified by real consumers
exact ReferenceAddress anchor table topology
which qualified relations require ScopedRecordRef
exact recurrence encoding/parameters
exact Place geometry/geography/SRID
exact MonetaryAmount numeric precision per specialist domain
exact capacity dimensions/units
exact lifecycle/state vocabularies
exact RLS-enabled tables/policies
exact query indexes
exact partitioning (currently none)
exact provider mapping schemas
exact outbox schema
exact PowerSync publication/schema
exact Restate workflow state
exact ContentArtifact object-flow schema
```

CP6-03 builds topology/dependency/vertical decomposition; CP6-05 designs Vertical #1 exactly.

---

## 24. Forbidden global shortcuts

```text
universal Entity/Thing table                         FORBIDDEN
universal Relationship/edge table                   FORBIDDEN
canonical EAV/property bag                          FORBIDDEN
universal event-log ontology                        FORBIDDEN
universal Fact/Version payload table                FORBIDDEN
generic kind+uuid reference without DB integrity    FORBIDDEN
provider ID promoted to NativeRef                   FORBIDDEN
MVCC/ETag/provider revision == MaterialStateRef      FORBIDDEN
absence/NULL == false globally                      FORBIDDEN
silent consequential last-write-wins                FORBIDDEN
DB-wide SERIALIZABLE by convenience                 FORBIDDEN
PostgreSQL money for MonetaryAmount                 FORBIDDEN
JSONB required-semantic escape hatch                FORBIDDEN
RLS == Authority/Consent/Visibility truth           FORBIDDEN
CASCADE as ORM/database default                      FORBIDDEN
metadata.create_all deployment                      FORBIDDEN
Alembic autogenerate as semantic authority          FORBIDDEN
fake reversible destructive migration               FORBIDDEN
speculative sharding/partitioning                    FORBIDDEN
specialist capability activation without trigger    FORBIDDEN
```

---

## 25. PG-R01..PG-R10 constitution path

| Risk | Constitution owner | Remaining direct evidence |
|---|---|---|
| PG-R01 anchor leakage | REF-03..06 | representative bounded anchor only when topology justifies it |
| PG-R02 heterogeneous integrity | REF-02..10 + CON | wrong-family/dangling real proof post-implementation |
| PG-R03 history maintainability | MAT/HIST | representative LR-01/LR-02/LR-03 business state |
| PG-R04 expected-state concurrency | MAT-09 + TX | SC-001 real race |
| PG-R05 multi-owner write skew | TX + CON | representative predicate/invariant race |
| PG-R06 Agreement/governance materiality | MAT/REL/PROV | Agreement/governance vertical proof |
| PG-R07 temporal/history semantics | HIST/TIM | representative dual-chronology/history corpus |
| PG-R08 lazy Occurrence | REF/MAT/TIM | recurrence/Occurrence vertical |
| PG-R09 disclosure/non-interference | CAP-06 + SEC + QA-11 | security/search/system proof |
| PG-R10 retention/restore | LIFE + MIG + QA-12 | destructive recovery/anti-resurrection |

No PG-R item is relabeled business-semantic direct PASS by this design document or by the 18.6 technical regression.

---

## 26. HG / SC / PSV carry-forward integrity

The complete canonical scenario/PSV ledger remains CP6-01 Part 2. CP6-02 does not duplicate/rename those IDs.

Constitution families own these major lanes:

```text
HG-01/02/03    ID/REF/REL/CON
HG-04/05       MAT/TX/IDEM
HG-06/07       MAT/HIST/PROV/CAP
HG-08          PROV/SEC/CAP/QA
HG-09          LIFE/MIG/QA — HOLD until destructive evidence
HG-10          TIM/CON
HG-11          MIG/QA — HOLD until real V1→V2
HG-12          MIG/SEC/QA — HOLD until destructive recovery
```

Selected examples retained exactly:

```text
SC-001 same-base consequential race
SC-002 idempotency-key conflicting reuse
SC-003 atomic multi-owner mutation
SC-010 correction without false rewrite
SC-011 redaction then restore older backup
SC-015 typed n-ary relation fidelity
SC-017 Search hidden-result non-interference
SC-018 FTS mixed filter/query
SC-022/023/024 recurrence temporal cases
SC-030 schema/mapping evolution with historical references
SC-031 backup/restore operational verification
SC-032 capacity/backpressure failure
```

PSV status remains as assigned by CP6-01. This constitution changes stage ownership/rules, not execution truth.

---

## 27. CP3 compatibility matrix

| CP3 contract | CP6-02 result |
|---|---|
| schema `dante` | PRESERVED |
| one SQLAlchemy Base/MetaData | PRESERVED |
| one AsyncEngine per process | PRESERVED |
| one async_sessionmaker per process | PRESERVED |
| one AsyncSession per operation/task | PRESERVED |
| `autobegin=False` | PRESERVED |
| `autoflush=True` | PRESERVED |
| `expire_on_commit=False` | PRESERVED |
| outer operation owns transaction | PRESERVED |
| adapter may flush, not commit | PRESERVED |
| default `READ COMMITTED` | PRESERVED |
| stronger isolation per invariant | MADE CONCRETE BY TX |
| no hidden retry | PRESERVED |
| one Alembic DAG/head | PRESERVED |
| reviewed autogenerate | PRESERVED / STRENGTHENED |
| owner/migrator/runtime split | PRESERVED |
| runtime DDL denied | PRESERVED |
| PostgreSQL 18.4 direct evidence | PRESERVED AS HISTORICAL EXACT EVIDENCE |
| current PostgreSQL patch | 18.6 / DIRECT REMOTE QA PASS — run 32568664940 @ ec3dc795... |

CP3 contradiction identified: **0**.

---

## 28. External benchmark disposition summary

```text
UUIDv7                                      ADOPT / BOUNDED
application-side issuance                  ADOPT
backend as online default issuer           ADOPT
future authorized offline issuance         MAY / TRIGGERED
database-only stable-ID issuance            REJECT
UUIDv7 timestamp as chronology              REJECT
homogeneous direct FK                       ADOPT
one-of-N FK for bounded union               MAY
bounded address anchor                      MAY WHEN REUSE/EVOLUTION JUSTIFIES
kind+id without DB RI                       REJECT
ON DELETE NO ACTION default                 ADOPT
CASCADE default                             REJECT
PostgreSQL ENUM everywhere                  REJECT
PostgreSQL money                            REJECT
declarative constraints first               ADOPT
PG18 temporal constraints                   ADOPT WHEN EXACT
global SERIALIZABLE                         REJECT
whole-transaction retry when SERIALIZABLE   ADOPT
RLS as Domain governance                    REJECT
RLS as defense-in-depth                     MAY
speculative indexes                         REJECT
speculative partition/sharding              REJECT
expand/backfill/cutover/contract             ADOPT
fake migration reversibility                REJECT
technology patch lifecycle                  ADOPT
```

---

## 29. Candidate Gate-02 preflight

### Constitution content

```text
TECH lifecycle                              CANDIDATE PASS
ID identity                                 CANDIDATE PASS
REF addressing                              CANDIDATE PASS
MAT material state                         CANDIDATE PASS
HIST history                                CANDIDATE PASS
TIM temporal                                CANDIDATE PASS
MISS missingness                            CANDIDATE PASS
LIFE lifecycle/retention                    CANDIDATE PASS
TYP PostgreSQL types                        CANDIDATE PASS
REL relations                               CANDIDATE PASS
CON constraints                             CANDIDATE PASS
IDX indexes                                 CANDIDATE PASS
TX transactions/concurrency                 CANDIDATE PASS
IDEM idempotency                            CANDIDATE PASS
PROV provenance                             CANDIDATE PASS
CAP capability boundaries                   CANDIDATE PASS
MIG migration/evolution                     CANDIDATE PASS
SEC ownership/privileges                    CANDIDATE PASS
QA direct-proof doctrine                    CANDIDATE PASS
```

### Required barriers

```text
all inherited decisions traceable                    CANDIDATE PASS
remaining exact choices explicitly vertical-specific CANDIDATE PASS
PG-R01..10 proof path assigned                        CANDIDATE PASS
HG/SC/PSV stage truth preserved                       CANDIDATE PASS
external benchmark completed                         CANDIDATE PASS
CP3 contradiction                                    0
Logical contradiction                                0
Physical contradiction                               0
semantic owner reclassification                      0
universal Entity/Relationship/EAV                     0
provider token == MaterialStateRef                    0
NULL-as-universal-negative                            0
silent consequential LWW                             0
implicit ORM schema authority                        0
business DDL                                          0
business migration                                    0
business SQLAlchemy mapping                           0
persistence adapter                                   0
```

### Gate-02 blocker status

```text
B-01 PostgreSQL technical target refresh 18.4 → 18.6
RESOLVED / DIRECT REMOTE QA PASS
run 32568664940 @ ec3dc795b5e044daa3a77723c94a1b4b5b92865c

B-02 PostgreSQL 18.6 release-note-specific DANTE impact review
RESOLVED / PASS / NO CURRENT POST-UPGRADE ACTION
future logical-replication activation remains trigger-bound

B-03 final post-refresh whole-Constitution independent review
OPEN / NOT YET COMPLETE

B-04 formal Gate-02 closure write
OPEN / NOT YET AUTHORIZED OR EXECUTED
```

Therefore:

```text
CP6-02
ACTIVE / CANDIDATE / PRE-CLOSURE
GATE 02 NOT PASSED
```

---

## 30. Next execution boundary

The technology-refresh and direct technical evidence boundaries are complete. The current-truth reconciliation updates current documentation to that exact evidence without rewriting historical 18.4 records.

Next:

```text
1. finish/verify current-truth reconciliation with exact Git delta and remote readback;
2. perform a fresh independent whole-Constitution review against:
   CP6-01 / WL-H / PG-R / HG / SC / PSV / Physical / CP3 /
   PostgreSQL 18.6 direct evidence / 18.6 release-note impact / external evidence;
3. repair any defect at source rather than documenting parallel truths;
4. if and only if the independent review is CLEAN, propose a separate exact Gate-02 closure write;
5. only after formal Gate 02 PASS may CP6-03 begin.
```

After Gate 02 closure, and only then:

```text
CP6-03
Concrete Relational Topology
+ Implementation Dependency DAG
+ Vertical Decomposition
```

No business table, column, migration, SQLAlchemy business mapping, persistence adapter, application use case or business API is authorized by this candidate constitution.
