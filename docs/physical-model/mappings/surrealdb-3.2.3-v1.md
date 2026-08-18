# SurrealDB Community 3.2.3 Physical Mapping v1

- Mapping ID: `PM02-SDB-001`
- Candidate: SurrealDB Community
- Exact PM-01 subject: SurrealDB Community **3.2.3**, single-node RocksDB qualification topology; Python SDK **2.0.0**
- Status: **PM-02 DESIGN COMPLETE / PM-03 NOT RUN**
- Selection: **NOT SELECTED**
- Purpose: idiomatic SurrealDB mapping of the closed LifeOS Logical Model; no executable SurrealQL/schema deployment is authorized by this document.

## 1. Design thesis

Use SurrealDB as a strongly constrained multimodel store, not as an excuse to collapse LifeOS into a flexible graph/document meta-model.

```text
owner-specific SCHEMAFULL tables
+ typed record IDs / typed record links
+ specific relation tables only for true binary LR-03 relations
+ normal contextual records for n-ary/material structures
+ explicit material-state records
+ technical consistency guards where snapshot isolation permits write-skew
```

Reject:

```text
one generic object table
one generic edge relation
FLEXIBLE canonical payloads
all semantics represented as graph edges
changefeed as canonical history
record ID/versionstamp == MaterialStateRef
whole-object ACL as complete Visibility model
```

## 2. Canonical table discipline

Every required semantic owner/family uses a `SCHEMAFULL` table with explicit fields/types.

Flexible nested objects are permitted only for bounded LR-09/LR-10/LR-13 data where the Logical Model already allows flexible/provider/specialist payloads.

Canonical semantic fields must not hide in arbitrary document properties.

## 3. LR-01 native owner mapping

Use one explicit SCHEMAFULL table for each native owner:

```text
person
living_referent
asset
place
content_artifact
collective
possibility
goal
plan
activity
event
routine
occurrence
session
observation
```

The table-specific record ID is the physical key for the concrete owner family.

LifeOS NativeRef therefore reconstructs as:

```text
concrete owner table/family
+ stable record ID
```

There is no universal native-object table.

## 4. LR-02 contextual/material records

Use normal SCHEMAFULL records for contextual/material semantics such as:

```text
schedule
actual
agreement
material_evaluation
material_resource_requirement
qualified_consent
qualified_authority
qualified_visibility
```

When independently addressable, the table-specific record ID carries the ScopedRecordRef mapping.

Do not turn an LR-02 contextual record into a graph edge merely because it has participants.

## 5. NativeRef and typed record links

For homogeneous reference slots, use typed record fields targeting the exact owner table.

For bounded heterogeneous Reference Contracts, use a typed record union/record-link definition limited to the accepted target tables.

Rules:

```text
target table set follows Reference Contract
record link != semantic Relationship
record ID != universal object identity
generic record type is not allowed for required canonical references unless a separate exact family discriminator/constraint makes the contract equivalent
```

Where an accepted Reference Contract includes fundamentally different address spaces (native/scoped/material/external), do not merge them simply because SurrealQL can store a generic record reference. Use separate fields/tables/address records as needed to preserve the discriminated family.

## 6. ScopedRecordRef

A concrete LR-02 record's table + record ID forms the scoped physical address. Its owning scope/context is encoded through required typed links/fields and validated as part of the table schema/operation.

For heterogeneous scoped-record references, use a bounded union of allowed scoped tables or a separate narrowly typed scoped-address record. Never introduce a universal RelationRef.

## 7. Explicit MaterialStateRef

Create explicit owner/facet-specific material-state records with stable SurrealDB record IDs.

Conceptual shape:

```text
<owner>_material_state
  record ID = material-state address
  owner typed record link
  facet/purpose
  semantic state fields
  effective/world chronology where applicable
  recorded/knowledge chronology where applicable
  mapping revision
  provenance/reconciliation links
```

Owner/current-state fields link to the accepted current state record where material.

Forbidden identities:

```text
changefeed/versionstamp != MaterialStateRef
updated timestamp        != MaterialStateRef
record revision          != MaterialStateRef
```

The explicit material-state record ID is the semantic address.

## 8. ExternalRef / provider state

Use explicit SCHEMAFULL external/provider records carrying provider-specific scope:

```text
provider/source
realm/tenant/account/integration instance where required
provider object kind
opaque external ID
provider revision/version
provider payload/state
apply/sync status
reconciliation status
canonical mapping target
```

Provider payload may use bounded flexible nested fields if the integration contract genuinely requires opaque/provider-specific structure.

ExternalRef is separate from native/scoped/material record identity even if all are implemented through SurrealDB records.

## 9. Binary simple LR-03 relations

Use either:

```text
specific typed record link fields
or
specific `TYPE RELATION` tables with typed `in`/`out` endpoints
```

only when the accepted semantic family is genuinely binary and the relation representation preserves its meaning.

Examples may include bounded simple Membership/Ownership relation forms when their exact accepted profile is binary and no material history/context forces qualification.

Every relation table is named/typed for the semantic family. No generic `edge(type,payload)` fallback.

## 10. Qualified relation escalation

When history, scope, provenance, visibility, governance or independent addressability matters, use a normal contextual SCHEMAFULL record or qualified relation record carrying the required state explicitly.

Do not rely on a lightweight binary edge whose existence cannot reconstruct the historical/governance basis.

## 11. N-ary Agreement — do not force graph binary edges

SurrealDB graph relations are binary `in`/`out` structures. Material Agreement is n-ary/common-ground semantics, so use a normal contextual `agreement` record plus explicit party-assent records/links.

Conceptual mapping:

```text
agreement
  scoped record identity
  current agreement material-state link
  terms MaterialStateRef

agreement_party_assent
  agreement link
  party ReferenceAddress
  party role
  exact terms MaterialStateRef
  assent material-state/provenance where required
```

All party assent for one accepted terms state points to the same material terms state.

Do not replace this with a star/pairwise graph and infer common assent.

## 12. Consent / Authority / Visibility / Representation

Keep as specific semantic tables/records/relations.

### Consent

Consequential records carry giver, target/use/action/exposure, purpose/context, material target/terms state, applicability and withdrawal/revocation history.

### Authority

Explicit Authority is a canonical relation/material state. Effective Authority may be a derived projection.

### Visibility

Visibility may independently govern record facet, relation existence, source/evidence and derived projection. Do not treat a record-level permission field as the entire semantic model.

### Representation

Preserve actual Actor, represented party and legitimacy/Authority basis separately.

Technical authentication/access state remains runtime state.

## 13. History strategy

Do not use SurrealDB changefeeds as the authoritative long-term material history because changefeed retention is operational/bounded and its records are synchronization/change evidence, not LifeOS semantic material-state identity.

Canonical history uses explicit material-state records plus typed lineage/provenance.

Changefeeds may later support:

```text
cache/index invalidation
sync/integration
outbox-like propagation
observability
```

without becoming canonical truth.

## 14. Current vs historical state

Stable owner record + explicit current-state link provides fast current access.

Historical material states remain separately queryable.

Do not infer semantic current state from newest record/changefeed event alone.

Where applicable preserve separate world/effective and knowledge/recording axes as explicit fields/state structures.

## 15. Unknown / negative semantics

Missing record/relation/state is not a universal false value.

Examples:

```text
no Actual record != known non-realization
no Membership row != proven non-member
no visible edge != nonexistent edge
no provider record != canonical negative fact
```

Explicit negative/refusal/cancelled/revoked semantics remain owner-specific records/fields.

## 16. Temporal representation

SurrealDB datetime values are used only for actual instant semantics.

Preserve separate structures for applicable:

```text
date-only
floating local wall-clock
named-zone wall-clock + zone ID
accepted historical resolution basis
absolute instant
interval/range
duration
precision/granularity/frame
```

A nested SCHEMAFULL object may group the components, but the semantic form is explicit and not a generic arbitrary JSON object.

## 17. Recurrence

Use explicit Recurrence SCHEMAFULL family/type records with semantic-family discriminator and family-specific typed fields:

```text
calendar / wall-clock
elapsed interval
quota per period
completion-relative
anchor-stream-relative
cyclic positional
```

Graph traversal and datetime functions do not replace recurrence semantics.

## 18. Lazy Occurrence

Before persistent differentiation, maintain the bounded logical locator:

```text
governing source ReferenceAddress
governing MaterialStateRef
recurrence family
semantic coordinate when available
```

Do not create future graph nodes/records for every derivable Occurrence.

Once semantically differentiated/addressable, create an `occurrence` record with stable NativeRef and retain locator/source lineage.

Unordered quota slots remain without artificial ordinal identity until one becomes individually distinguished.

## 19. Schedule / Session / Actual / Outcome

Keep distinct tables/record families:

```text
occurrence
schedule
session
actual
outcome representation where material
```

Actual remains dependent contextual identity, not native root. Schedule revisions remain reconstructible. Session ordinary corrections retain Session identity. Absence remains unknown.

## 20. Expected-state consequential mutation

Every stale-write-sensitive operation carries an expected MaterialStateRef.

Conceptual transaction:

```text
1. read/match owner + current material-state record
2. require current state record == expected MaterialStateRef
3. require all target Reference Contracts/invariants
4. establish replacement material state
5. update current state links and all co-located affected records
6. mutate consistency guard if invariant set is write-skew-sensitive
7. store bounded provenance/idempotency state
8. commit
```

A non-match conflicts/retries/reconciles; no silent overwrite.

## 21. Snapshot isolation hardening

The PM-01 subject provides snapshot isolation with write-write conflict detection; PM-02 does not assume it prevents write-skew over disjoint records.

For multi-owner/predicate invariants susceptible to write-skew, introduce a narrowly scoped technical `consistency_guard` SCHEMAFULL table.

Conceptual record:

```text
consistency_guard
  scope key / record ID
  guard revision/nonce
  optional invariant-family discriminator
```

Every consequential transaction within the same invariant boundary mutates that same guard record, creating a write-write contention point.

Rules:

```text
guard != Domain Transaction
guard != canonical Resource/Relationship
not one global guard
scope = narrowest actual invariant set
```

PM-03 must prove this pattern using concurrent tests/design analysis; it is not accepted merely by documentation.

## 22. Multi-owner consistency

Use one SurrealDB transaction for co-located changes.

Layered enforcement:

```text
SCHEMAFULL field/type constraints
unique indexes where exact semantics require uniqueness
conditional expected-state updates
shared consistency-guard mutation for write-skew-sensitive invariant sets
```

External/provider effects remain staged/partial/reconciled when not transactionally atomic.

## 23. Idempotency

Use a bounded technical idempotency table keyed by operation scope + key + material operation fingerprint/result reference.

Idempotency does not create a universal Command entity or replace Request/Decision identity.

## 24. Derived/projection state

Use computed/derived query fields only for cheap semantics whose source can be resolved truthfully.

Materialized projections are explicit projection records with:

```text
projection kind
source/bounded source set
source MaterialStateRefs/material basis
created/refreshed time
freshness/expiry
purpose/context
```

Do not let a materialized graph/search projection become canonical state by reuse.

## 25. Search/vector boundary

SurrealDB's multimodel/query capabilities may support some bounded search/vector workloads later, but PM-02 does not move PM-08 specialist decisions into the primary mapping.

If vector/search data is stored in the same engine:

```text
embedding/index row != Evidence
similarity != Relationship
search miss != canonical nonexistence
projection/filtering must respect Visibility
```

## 26. Selective disclosure

One shared canonical record remains one shared reality.

Recipient-specific queries/projections enforce allowed exposure at field/facet/relation/source level.

PM-03/later security pressure must test:

```text
hidden relation existence through traversal
counts/rankings
edge/node presence
error behavior
source/evidence leakage
projection freshness after access change
```

No per-recipient canonical copies.

## 27. Retention / deletion / graph-edge behavior

Use explicit semantic tombstone/history records rather than relying on automatic relation cleanup to represent consequential historical truth.

For simple non-historical edges, normal relation deletion semantics may be sufficient.

For consequential relation/history:

```text
qualified contextual record/material state remains independently reconstructible
references bind stable owner/tombstone addresses where policy permits
payload can be redacted/deleted according to retention class
```

NativeRef/table record identity is never reused for another referent.

Changefeed retention is not a substitute for historical retention.

## 28. Provider / projection / runtime boundaries

Keep explicit tables or namespaces/conventions for:

```text
canonical owners/material state
provider/external state
rebuildable projections
runtime/job/cache state
technical security state
```

Co-location in one SurrealDB instance does not imply semantic equivalence.

## 29. Governed-effect provenance

Consequential effects retain/reconstruct bounded evidence for applicable:

```text
operation family
target semantic owner/facet
expected MaterialStateRef
actual Actor
represented party
Principal/security context reference
governance basis MaterialStateRefs
purpose/context
idempotency/correlation/causation
resulting canonical state/effect
provider/runtime result separately
```

This is bounded provenance/technical evidence, not a universal semantic Operation root.

## 30. Schema evolution

The canonical mapping is `SCHEMAFULL`; migration is explicit.

Process:

1. version LifeOS mapping;
2. define additive fields/tables/indexes under reviewed change;
3. backfill/migrate current/material state explicitly;
4. preserve record IDs/NativeRef/ScopedRecordRef/MaterialStateRef;
5. preserve old history interpretation rather than retroactively applying new semantics;
6. validate relation endpoint/table constraints;
7. validate tombstone/redaction behavior;
8. remove obsolete fields only after compatibility/rollback evidence.

Do not switch canonical tables to FLEXIBLE to avoid migration work.

## 31. Query strategy

Use SurrealDB candidate-native strengths selectively:

```text
direct typed record links for bounded homogeneous/polymorphic references
specific binary relation traversals
normal record queries for contextual/n-ary objects
material-state joins/links for history
computed projections for cheap derived reads
```

Do not graphify values/specifications/history merely for traversal convenience.

## 32. Candidate-native strengths deliberately used

```text
SCHEMAFULL typed tables
record IDs and typed record links
specific graph relation tables
multimodel document+relation querying
transactional multi-record mutations
```

These are design hypotheses, not hard-gate or performance PASS.

## 33. PM-03 proof obligations / known risks

### SDB-R01 — no document/meta-model escape hatch

Prove all required canonical semantics stay in SCHEMAFULL typed fields/tables and FLEXIBLE/generic objects remain bounded to permitted LR-09/LR-10/LR-13 use.

### SDB-R02 — no generic graph ontology

Prove only specific LR-03 binary families use edge tables and contextual/n-ary/material relations remain explicit owner records.

### SDB-R03 — ReferenceAddress discrimination

Prove typed record unions/links cannot collapse native/scoped/material/external address spaces or accept invalid target families.

### SDB-R04 — MaterialStateRef distinction

Prove explicit material-state IDs remain separate from record/update/changefeed/version metadata.

### SDB-R05 — expected-state/write-skew

Prove conditional current-state check + narrow consistency guard prevents representative concurrent stale/predicate anomalies under actual snapshot isolation.

### SDB-R06 — n-ary Agreement

Prove common terms MaterialStateRef and N party assent bindings remain one common-ground structure, not inferred pairwise graph state.

### SDB-R07 — temporal/history

Prove explicit material history and world/knowledge chronology remain queryable without relying on bounded changefeed history.

### SDB-R08 — lazy Occurrence

Prove derivation locator -> persisted Occurrence record preserves semantic identity without eager graph-node creation.

### SDB-R09 — deletion/tombstone

Prove record/relation deletion behavior cannot silently erase required consequential history and sensitive payload can still be removed according to policy.

### SDB-R10 — selective disclosure

Prove graph traversal, count/ranking and record-link queries can enforce WL-H12 without relation/source leakage.

### SDB-R11 — mapping evolution

Prove SCHEMAFULL V1->V2 migration retains identity/material-state/history semantics and does not require generic flexible fallback.

### SDB-R12 — topology/edition sensitivity

Do not award HA/distributed operation properties from Enterprise features to the Community single-node qualification subject.

## 34. PM-02 result

```text
MAPPING ID
PM02-SDB-001

SUBJECT
SurrealDB Community 3.2.3 / single-node RocksDB qualification topology / Python SDK 2.0.0

DESIGN
COMPLETE

HG-01..HG-12
NOT RUN

BENCHMARK
NOT STARTED

CURRENT DISPOSITION
ADMIT-CONDITIONAL / NOT SELECTED
```

No hard-gate PASS, performance or selection claim is made.