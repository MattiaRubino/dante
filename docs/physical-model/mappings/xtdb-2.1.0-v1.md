# XTDB 2.1.0 Physical Mapping v1

- Mapping ID: `PM02-XT-001`
- Candidate: XTDB
- Exact PM-01 subject: XTDB **2.1.0**, self-hosted qualification subject; PostgreSQL-wire client path where applicable
- Status: **PM-02 DESIGN COMPLETE / PM-03 NOT RUN**
- Production topology: **HOLD from PM-01**
- Selection: **NOT SELECTED**
- Purpose: idiomatic XTDB mapping of the closed LifeOS Logical Model; no executable SQL/deployment is authorized by this document.

## 1. Design thesis

Use XTDB's relational SQL surface and native bitemporality for the semantic axes where they are genuinely useful, while compensating explicitly for the absence of ordinary FK/schema constraints.

```text
owner-specific tables
+ explicit separated technical address tables
+ explicit MaterialStateRef rows
+ XTDB bitemporal history as a physical history substrate
+ ASSERT-based referential/expected-state enforcement
+ one serialized DML transaction for co-located multi-owner effects
```

Reject:

```text
one generic Entity table
one generic edge table
one universal bitemporal Fact ontology
system-time == MaterialStateRef
valid-time == every LifeOS temporal meaning
latest row == canonical truth
schema-on-write freedom == permission for semantic drift
```

## 2. Constraint reality and resulting policy

The PM-01 subject does not provide conventional SQL foreign keys and does not provide general uniqueness constraints beyond `_id` semantics.

Therefore PM-02 does **not** pretend an owner-table reference is safe merely because its column contains another row ID.

LifeOS integrity is supplied through:

```text
separated address-anchor tables
+ typed application mapping
+ transaction ASSERT predicates
+ deterministic mapping revisions
+ direct PM-03 destructive validation
```

This extra integrity machinery is mapping complexity and must count as evidence later.

## 3. LR-01 native owner mapping

Each native owner has its own XTDB table:

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

The row `_id` is the stable physical key for that concrete owner row and participates in the LifeOS NativeRef mapping.

It does not imply a generic owner table or semantic superclass.

## 4. Segregated ReferenceAddress anchor tables

Because heterogeneous FKs are not available, create four **separate technical address spaces**:

```text
native_address
scoped_address
material_state_address
external_address
```

Never combine them into one universal `typed_ref(kind,id)` root.

### `native_address`

Contains only technical address control such as:

```text
_id = NativeRef address key
owner_family
owner_row_id
mapping_revision
tombstone/address status metadata where allowed
```

Every addressable LR-01 owner row has one corresponding anchor.

### `scoped_address`

Indexes independently addressable LR-02 contextual records, retaining concrete record family + owning scope/context.

### `material_state_address`

Indexes explicit semantic material-state records and their owner/facet.

### `external_address`

Indexes provider/source-scoped external identities.

Rules:

```text
address anchor != semantic owner
address anchor contains no generic Domain property bag
Reference Contract remains the semantic eligibility authority
```

## 5. Homogeneous vs heterogeneous references

For a slot with exactly one concrete target family, store the concrete target row ID/family directly and validate target existence in consequential writes via `ASSERT` where required.

For heterogeneous slots, reference the relevant segregated address table and retain the contract-specific eligible owner/family discriminator.

Every mutation that creates a consequential reference must assert:

```text
target address exists
address space is correct
owner/record/state family is allowed by that Reference Contract
referenced target is not invalidly retired/tombstoned for that operation
```

PM-03 must prove there is no path that bypasses these checks and creates dangling/wrong-family canonical references.

## 6. LR-02 contextual/material records

Use owner-specific XTDB tables for addressable/material contextual records, for example:

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

Selective materialization still applies; do not create a row for every trivial interaction merely because XTDB can store flexible documents.

Each addressable LR-02 row has a scoped address anchor.

## 7. LR-03 relation mapping

Use **specific relation-family tables**, not a universal graph-edge table.

Examples:

```text
membership
ownership
participation
responsibility
dependency
representation
resource_allocation
capacity_claim
agreement_party_assent
```

Simple relations can be compact rows containing exact endpoints and family-specific fields.

Consequential/qualified relations receive:

```text
scoped address when independently addressable
material-state binding/history where required
scope/purpose/context
provenance
governance/visibility basis
```

## 8. N-ary Agreement

Represent Agreement as one contextual record plus explicit party-assent rows.

```text
agreement row
  scoped identity
  current agreement material-state binding

agreement_party_assent rows
  agreement reference
  party ReferenceAddress
  role
  exact terms MaterialStateRef
  assent material state/provenance where required
```

All material party assent for one accepted Agreement terms state must bind to the same terms MaterialStateRef.

Do not model common assent as N pairwise edges.

## 9. Explicit MaterialStateRef

XTDB's bitemporal versions are extremely useful history evidence, but they do not automatically identify a LifeOS materially meaningful semantic state.

Create explicit material-state rows with stable `_id` values in owner/state-family tables and an entry in `material_state_address`.

Conceptual payload:

```text
_id = MaterialStateRef
owner reference
facet/purpose
semantic state fields
recorded/accepted metadata
provenance/reconciliation links
mapping revision
```

Forbidden equivalences:

```text
XTDB transaction token != MaterialStateRef
SYSTEM_TIME coordinate  != MaterialStateRef
VALID_TIME coordinate   != MaterialStateRef
row version             != MaterialStateRef
```

A single explicit material state may itself have XTDB system-time history if its record is corrected operationally, but the semantic address remains stable according to the accepted correction policy.

## 10. Bitemporal use

Use XTDB's native two temporal axes carefully.

### System time

System time is useful evidence for:

```text
when a database version became recorded/committed/visible
knowledge chronology pressure
correction chronology
technical reconstruction
```

It is not automatically the moment LifeOS semantically learned/accepted a fact when workflow/import timing differs. Explicit semantic timestamps remain where necessary.

### Valid time

Use valid time where the row truthfully represents world/effective applicability of that specific semantic state.

Do **not** use valid time to absorb:

```text
Schedule vs Actual distinction
Recurrence semantics
Occurrence identity
provider revision state
Visibility applicability when its owner semantics differ
arbitrary UI validity
```

### Semantic chronology fields

When the native temporal axes are insufficient to recover accepted meaning, preserve explicit fields for:

```text
observed_at
learned_at
accepted_at
source effective interval
correction/reconciliation chronology
```

The exact set remains owner-specific.

## 11. Current state

XTDB's default current query view is useful but not the full LifeOS definition of “current”.

For materially stateful owners/facets, canonical current accepted state is an explicit owner/current-state binding or owner current record field referring to the active `MaterialStateRef`.

```text
current knowledge/acceptance
!= world/effective applicability
```

Queries must qualify which axis they mean.

## 12. Unknown / negative semantics

No row remains unknown unless an explicit owner-specific negative state exists.

Do not let temporal absence, expired valid-time, missing provider state or no Actual row become false/cancelled/non-realization by convention.

## 13. ExternalRef / provider state

Use `external_address` plus provider-specific integration tables carrying:

```text
provider/source
realm/tenant/account/integration instance where required
provider object kind
opaque external ID
provider revision/version
provider payload/state
apply/sync state
reconciliation state
canonical mapping target
```

Provider revisions remain LR-09 state and never become MaterialStateRef automatically.

## 14. Temporal value semantics

XTDB's temporal SQL types do not eliminate the need to preserve the original semantic form.

Store distinct owner-bound shapes for applicable:

```text
date-only
floating local wall-clock
named-zone wall-clock + zone ID
accepted historical resolution basis
absolute instant
range/interval
duration
precision/granularity/frame
```

Do not resolve every future intention to one UTC instant as canonical meaning.

## 15. Recurrence

Use explicit recurrence-family tables/structured rows with family discriminator and family-specific parameters:

```text
calendar/wall-clock
elapsed interval
quota per period
completion-relative
anchor-stream-relative
cyclic positional
```

XTDB valid time is not recurrence.

## 16. Lazy Occurrence

Before persistent differentiation:

```text
governing source ReferenceAddress
+ governing MaterialStateRef
+ recurrence family
+ semantic coordinate when available
= bounded locator
```

Do not create every future occurrence row to exploit XTDB history.

When an instance becomes semantically distinguished, create an `occurrence` row with stable `_id`/NativeRef and retain the governing locator lineage.

Unordered equivalent quota slots receive no arbitrary early ordinal.

## 17. Schedule / Session / Actual / Outcome

Maintain separate tables/owners:

```text
occurrence
schedule
session
actual
outcome representation where material
```

Schedule revisions are historical accepted placements. Actual never overwrites Schedule. Session retains stable identity through ordinary time correction. No Actual remains unknown.

## 18. Expected-state mutation with ASSERT

A consequential XTDB DML transaction is designed as a non-interactive sequence whose preconditions are expressed in the transaction itself.

Conceptual sequence:

```text
ASSERT current owner/facet material_state_ref == expected MaterialStateRef
ASSERT all ReferenceAddress targets exist and are contract-eligible
ASSERT applicable invariant predicates / guard state
INSERT/UPDATE new material state
UPDATE current owner binding
UPDATE all co-located affected relations/owners
INSERT bounded provenance/idempotency state where required
```

If an `ASSERT` fails, the transaction must fail rather than partially commit.

This is a core PM-03 proof obligation.

## 19. Non-interactive transaction consequence

XTDB's write transactions are submitted as DML statement lists rather than an arbitrary client read/branch/write dialogue.

Therefore every governed mutation must be designed so that:

```text
semantic precondition can be stated as SQL/ASSERT
required derived values can be computed inside the submitted DML/query expressions
all intended writes are known/constructible before submission
```

If a use case fundamentally requires iterative client interaction inside one transaction, the mapping must use a different bounded pattern rather than pretending XTDB provides that transaction API.

PM-03 must inspect representative governed operations for ergonomic/semantic viability.

## 20. Multi-owner consistency

For one XTDB database, place all co-located changes in one DML transaction with the full invariant assertion set.

XTDB serializes writes through its transaction log, so PM-02 does not introduce a synthetic per-invariant locking table merely to imitate PostgreSQL.

Still, serial write order does not excuse incomplete invariant checks. Every transaction must assert the relevant semantic preconditions against the state visible in that transaction.

Do not split one invariant across separate XTDB databases: serializability guarantees are not assumed across databases.

External/provider side effects remain staged/reconciled.

## 21. Idempotency

Use a bounded technical idempotency table keyed by operation scope/key and material operation fingerprint.

The transaction first asserts compatible key reuse and then establishes/replays the recorded result semantics.

Idempotency identity is not semantic owner identity.

## 22. Derived/projection state

Prefer SQL queries over current/history tables where sufficient.

If a materialized projection is justified, store it in a separate projection table with:

```text
projection kind
source/bounded source set
source MaterialStateRefs/material basis
source XTDB tx token/snapshot token where useful for technical freshness
created/refreshed time
expiry/freshness contract
purpose/context
```

Important:

```text
snapshot/tx token != MaterialStateRef
```

The token may prove database visibility/freshness only.

## 23. Change visibility / read-your-write coordination

XTDB transaction tokens may be used by clients to await/query after a submitted transaction so later reads observe the required database state.

This is runtime consistency metadata, not Domain history or semantic Version identity.

## 24. Retention / deletion / erase

Distinguish ordinary temporal deletion from irreversible history erasure.

### Normal semantic deletion/retirement

Use normal current-state/tombstone semantics so prior history remains reconstructible where policy permits.

### Privacy/legal erase

XTDB `ERASE`-class behavior removes historical versions and is appropriate only when policy truly requires removal of that payload/history.

Where permitted/required to retain non-sensitive continuity, keep a separate minimal address/tombstone record whose retained fields do not contain the erased sensitive payload.

Do not call ERASE on a canonical owner and then pretend required historical reference continuity still exists if no legal minimal anchor remains.

PM-07 must test anti-resurrection after backup/restore for whatever deployment topology is eventually frozen.

## 25. Dynamic schema discipline

XTDB allows gradual/dynamic table shape. LifeOS treats that as a physical capability, not semantic permission.

Every canonical row carries or is governed by a mapping revision contract.

Writer/readers must validate:

```text
required fields for semantic family
field types/shape
Reference Contract eligibility
owner-specific state invariants
mapping revision compatibility
```

No canonical producer may add arbitrary fields as hidden ontology.

## 26. Schema/mapping evolution

Because multiple row shapes can coexist, migration strategy explicitly controls transition:

1. add new mapping revision/read compatibility;
2. write new shape for new states;
3. backfill/rewrite historical/current rows only where semantics remain identical;
4. retain explicit version/mapping metadata needed to interpret old rows;
5. verify address anchors and MaterialStateRefs;
6. verify bitemporal history has not been rewritten to imply the new interpretation existed earlier;
7. retire old readers only after evidence.

“Schema is flexible” is not a migration plan.

## 27. Selective disclosure

Shared canonical tables remain one reality. Recipient projections filter at query/runtime level and may use bounded materialized projections.

PM-03/later enforcement must pressure:

```text
hidden row/relationship existence
history visibility
bitemporal query leakage
counts/rankings/errors
provider/source disclosure
stale projection basis
```

No per-recipient canonical duplication.

## 28. Governed-effect provenance

Persist/reconstruct bounded consequential-effect basis:

```text
operation family
semantic target/facet
expected MaterialStateRef
actual Actor
represented party
Principal/security context reference
governance basis MaterialStateRefs
purpose/context
idempotency/correlation metadata
resulting canonical MaterialStateRef/effect
provider/runtime result separately
XTDB transaction token as technical evidence only
```

Do not create a universal Command/Event ontology.

## 29. Query strategy

Exploit XTDB where it is structurally distinctive:

```text
ordinary SQL joins over owner-specific tables
native valid/system-time historical queries
current queries without replay
state history/correction analysis
explicit address-anchor joins for heterogeneous references
```

Do not route every query through bitemporal clauses merely because they exist.

## 30. Candidate-native strengths deliberately used

```text
native bitemporal rows
SQL current/history querying
serialized write transaction processing
ASSERT-based in-transaction preconditions
immutable historical versions under normal temporal updates
```

These strengths are hypotheses to validate, not automatic hard-gate PASS.

## 31. PM-03 proof obligations / known risks

### XT-R01 — referential integrity without FK

Prove all consequential reference-creation paths assert target existence/address space/eligible family and no dangling canonical references can be produced.

### XT-R02 — uniqueness/cardinality without ordinary constraints

Prove owner/relation cardinalities and uniqueness obligations survive concurrent mutation using `_id` design + ASSERT + serialized writes.

### XT-R03 — address anchors are not ontology

Prove the four separated address spaces contain only technical addressability and cannot become generic semantic property stores.

### XT-R04 — MaterialStateRef distinction

Prove semantic material-state identity remains explicit and is not silently replaced by system-time, valid-time or transaction tokens.

### XT-R05 — bitemporal semantic alignment

Prove representative world/effective and knowledge/correction histories use native axes only where truthful, with explicit semantic chronology where needed.

### XT-R06 — non-interactive governed mutations

Prove representative complex WL-H02 operations can express all preconditions/effects in one submitted DML transaction without semantic weakening.

### XT-R07 — multi-owner consistency

Prove concurrent submitted operations see serialized invariant truth and one failed ASSERT leaves no partial canonical effect.

### XT-R08 — dynamic schema containment

Prove malformed/old/new shapes cannot silently become canonical valid state and V1->V2 migration retains historical meaning.

### XT-R09 — lazy Occurrence

Prove locator -> persisted Occurrence identity with no premature quota-slot identity.

### XT-R10 — erase/tombstone integrity

Prove policy-specific deletion can erase sensitive payload while retaining only the permitted minimal historical/address continuity.

### XT-R11 — current-state practicality

Prove current views for high-value owner/state queries do not require expensive lifetime-history logic by default.

### XT-R12 — topology boundary

Production topology remains HOLD and is not scored from this mapping. PM-07/operations cannot claim HA/recovery properties until exact topology is frozen/executed.

## 32. PM-02 result

```text
MAPPING ID
PM02-XT-001

SUBJECT
XTDB 2.1.0 / self-hosted qualification subject

DESIGN
COMPLETE

PRODUCTION TOPOLOGY
HOLD

HG-01..HG-12
NOT RUN

BENCHMARK
NOT STARTED

CURRENT DISPOSITION
ADMITTED / NOT SELECTED
```

No hard-gate PASS, performance or selection claim is made.