# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 7

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md` — sections 1–30
- **Part 2:** `dante-postgresql-database-part-2.md` — section 31
- **Part 3:** `dante-postgresql-database-part-3.md` — section 32
- **Part 4:** `dante-postgresql-database-part-4.md` — section 33
- **Part 5:** `dante-postgresql-database-part-5.md` — section 34
- **Part 6:** `dante-postgresql-database-part-6.md` — section 35
- **Continuation numbering:** section 36 onward
- **Continuation anchor:** `168c0adad72b9afd8d99f020f947b437080f59bb`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of Parts 1–6. It does not replace, summarize or supersede any prior part as a whole.

```text
dante-postgresql-database.md
PART 1 / sections 1–30
+

dante-postgresql-database-part-2.md
PART 2 / section 31
+

dante-postgresql-database-part-3.md
PART 3 / section 32
+

dante-postgresql-database-part-4.md
PART 4 / section 33
+

dante-postgresql-database-part-5.md
PART 5 / section 34
+

dante-postgresql-database-part-6.md
PART 6 / section 35
+

dante-postgresql-database-part-7.md
PART 7 / section 36 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

Readers, reviewers, final object-inventory work, Database Dictionary reconciliation, migration planning, SQLAlchemy mapping review, generated-reference checks, direct PostgreSQL proof planning and Gate-03 review MUST consume all active parts.

The preservation, no-summary, explicit-supersession and whole-database cumulative-audit rules established in earlier parts remain fully applicable.

---

## 36. Consolidation checkpoint I — Provider / Idempotency / Outbox / Derived baseline disposition

### 36.1 Scope

This checkpoint closes four remaining global CP6-03 disposition items:

```text
DB-U17  provider / integration object shapes
DB-U18  idempotency persistence timing
DB-U19  transactional outbox timing
DB-U20  derived / search / vector persisted structures
```

The checkpoint is intentionally grouped because all four are capability- or consumer-triggered technical persistence concerns that must remain separate from canonical DANTE semantic ownership.

They are not grouped because they share one table, one lifecycle or one technical abstraction.

They do not.

### 36.2 Authority consumed

The decision is derived from the complete accumulated authority, including:

```text
closed Domain Atlas and concept specifications
closed Whole-Logical 57/57 model
LR-01..LR-13 representation framework
WL-H01..WL-H12
Governed Operation / Effect Contract
Projection / Disclosure Surface Contract
CP6-01 Part 1 owner coverage
CP6-01 Part 2 cross-cutting persistence ledger
accepted PostgreSQL Physical mapping
PG-R01..PG-R10
CP6-02 Persistence Constitution
ADR-010
Parts 1–6 of this database reference
current backend source tree
current backend dependency graph
current Alembic head / CP3 technical baseline
```

No product vertical, provider integration, material idempotent operation, Class-A asynchronous publication flow, search consumer or vector consumer exists in the current backend implementation.

### 36.3 Current runtime/materialization reality

The real backend currently contains only the technical application/persistence foundation:

```text
dante/bootstrap

dante/platform/config

dante/platform/database
```

There is no current product capability module that establishes one of the four triggers closed in this checkpoint.

The current backend dependency graph contains the accepted FastAPI/Pydantic/SQLAlchemy/psycopg/Alembic foundation and no concrete provider client, message-bus worker, search service or embedding runtime that creates an implementation-bound schema requirement.

The current Alembic baseline intentionally creates no DANTE business schema.

Therefore this checkpoint may not infer a consumer from selected technology alone.

---

### 36.4 Four different trigger classes

The four items close under different future triggers:

```text
DB-U17
→ first concrete provider/integration contract

DB-U18
→ first persistent material operation requiring retry/replay reservation semantics

DB-U19
→ first real Class-A asynchronous external/publication effect

DB-U20
→ first query/search/vector consumer proving persisted derived-state need
```

Closing all four at zero baseline DDL does not merge those triggers.

A future activation of one does not activate the others automatically.

---

# DB-U17 — provider / integration

### 36.5 LR-09 remains authoritative

Provider/external state remains LR-09.

The physical thesis remains:

```text
provider identifiers
provider revisions
provider payload/state
provider sync/apply state
provider receipts
provider reconciliation state

!=

canonical DANTE identity/state
```

Provider state may propose, inform, synchronize or reconcile canonical state, but cannot silently become current canonical truth.

### 36.6 ExternalRef remains distinct

The reference-family boundary remains:

```text
ExternalRef
!= NativeRef
!= ScopedRecordRef
!= MaterialStateRef
```

A provider identifier does not become a DANTE native identity because it is stable, unique or widely used by the provider.

### 36.7 ExternalRef is issuer-scoped

Any future ExternalRef contract must preserve enough scope to make the external identifier meaningful.

Potential required axes include:

```text
provider / issuer
integration instance
realm
tenant
account/workspace
provider object family/type
opaque external object identifier
provider revision/version where material
```

The exact axes are provider-contract-specific.

### 36.8 No generic provider root

CP6 baseline MUST NOT introduce a universal semantic/provider root such as:

```text
dante.provider
dante.external_ref
dante.external_object
dante.integration_object
dante.provider_entity
```

merely to pre-allocate an integration abstraction.

A later integration may introduce bounded shared technical support only when more than one concrete provider contract proves that sharing preserves integrity rather than erasing issuer scope.

### 36.9 No generic provider mapping table

The baseline MUST NOT introduce a table equivalent to:

```text
provider_code
external_id
target_kind
target_uuid
payload jsonb
```

Such a table would recreate the rejected generic kind+id semantic/reference pattern and would not prove target eligibility.

### 36.10 Future mapping must be bounded

A future integration mapping must specify exactly which DANTE target families are eligible.

Examples of valid future implementation shapes may include:

```text
provider-specific mapping to one concrete native family
provider-specific mapping to one concrete scoped family
bounded heterogeneous mapping through accepted address infrastructure
candidate/reconciliation mapping that remains explicitly noncanonical
```

The concrete provider contract chooses the shape.

### 36.11 Provider payload boundary

Provider raw payload MAY use bounded JSONB when retention/debug/reconciliation requires preserving provider-native data.

That permission does not allow required canonical DANTE semantics to disappear into provider payload JSONB.

```text
provider payload JSONB
!= canonical semantic owner state
```

### 36.12 Provider revision boundary

Provider revision/version tokens may be retained when required for synchronization, conditional provider writes or reconciliation.

They MUST NOT be treated as:

```text
MaterialStateRef
canonical chronology
current accepted DANTE state
```

### 36.13 Provider success/failure boundary

A provider response such as:

```text
200 OK
accepted by provider
queued by provider
provider revision advanced
```

MUST NOT by itself establish canonical DANTE acceptance.

Canonical acceptance follows the relevant governed DANTE operation/effect contract.

### 36.14 Ambiguous external result

Loss of a provider response does not prove provider failure.

Future external-effect integrations must be able to represent/reconcile ambiguity without fabricating a canonical negative result.

### 36.15 Sync/apply state

Future sync/apply state is technical integration state.

It may need statuses such as pending/applied/failed/ambiguous for a concrete provider contract, but CP6 does not create one global status vocabulary.

### 36.16 Reconciliation remains separate

Provider reconciliation may result in:

```text
candidate match
accepted mapping
rejected mapping
manual resolution
canonical material-state change
```

where the concrete contract allows those outcomes.

The provider mapping itself does not become the reconciliation semantic result.

### 36.17 DB-U17 final disposition

```text
DB-U17
CLOSED

CP6-04 BASELINE PROVIDER / INTEGRATION BUSINESS OBJECTS
0
```

No generic provider, ExternalRef registry, provider mapping, sync/apply or provider payload table is authorized by the CP6 baseline.

### 36.18 DB-U17 future materialization trigger

The first concrete provider/integration contract MUST close, as applicable:

```text
provider / issuer identity
realm / tenant / account / integration-instance scope
provider object type/family
opaque external identifier semantics
provider revision/version semantics
payload retention/redaction
exact DANTE target Reference Contract
candidate vs accepted mapping semantics
sync/apply state
provider-side conditional/idempotency behavior
ambiguous-result handling
reconciliation path
canonical acceptance boundary
chronology
retention
indexes
ACL
proof matrix
```

Only then may provider-specific DDL be introduced.

---

# DB-U18 — idempotency persistence

### 36.19 Idempotency doctrine is already closed

DB-U18 is not open because the idempotency mechanism is conceptually undefined.

CP6-02 already closes the reusable doctrine.

The remaining question was whether a baseline persistent table is justified before a real material operation exists.

The answer is no.

### 36.20 Reservation identity

For a future persistent idempotency reservation:

```text
reservation identity
=
operation_scope
+
idempotency_key
```

The material-operation fingerprint remains a separate immutable field.

### 36.21 Fingerprint is not uniqueness identity

The future schema MUST NOT use:

```text
UNIQUE(operation_scope, idempotency_key, fingerprint)
```

as the reservation identity because that would allow one key to reserve multiple materially different operations.

Instead:

```text
UNIQUE(operation_scope, idempotency_key)
```

with immutable fingerprint comparison is the reusable contract.

### 36.22 Same key + same operation

A retry using the same reservation identity and materially equivalent normalized operation may:

```text
wait for the winning execution
replay an established bounded result
return the already established canonical result/reference
```

according to the concrete operation contract.

### 36.23 Same key + different operation

A retry using the same reservation identity but a different material-operation fingerprint MUST conflict/reject.

The reservation MUST NOT be rebound.

### 36.24 Concurrent duplicates

Concurrent duplicate requests for one reservation identity MUST serialize so that at most one material execution wins.

The exact locking/insert-on-conflict strategy is selected when a real table exists.

### 36.25 Validation before reservation

Pure syntactic, authentication, authorization or precondition rejection MAY occur before a persistent reservation is created if no material execution has started.

Once the concrete operation reserves/starts execution, the fingerprint cannot mutate.

### 36.26 Operation scope cannot be invented globally

CP6 baseline does not yet know the exact operation families that need persistent idempotency.

Therefore it cannot truthfully define:

```text
operation_scope vocabulary
scope cardinality
scope key composition
```

A generic `operation_scope text` without a bounded operation contract would be a placeholder, not a completed schema decision.

### 36.27 Key representation remains operation-contract-specific

CP6 does not globally freeze:

```text
key maximum length
key encoding
case sensitivity
caller namespace
transport header name
```

unless/until the real operation boundary requires them.

### 36.28 Fingerprint representation remains versioned

A future material operation must define deterministic normalization and fingerprint versioning.

Raw sensitive request payload MUST NOT be duplicated merely to obtain a hash.

### 36.29 Result binding remains bounded

The future idempotency row may need to retain enough result information to replay or identify the established effect.

That does not authorize a generic JSON result payload.

The concrete operation must decide whether the bounded result is, for example:

```text
new NativeRef
new ScopedRecordRef
new MaterialStateRef
technical execution receipt
provider receipt
response status/body subset
another typed result
```

### 36.30 Retention horizon is operation-specific

There is no universal 24-hour or fixed retention rule.

The idempotency reservation lives for the concrete operation's retry/reconciliation/policy horizon.

### 36.31 Idempotency is not identity

The following remain forbidden collapses:

```text
idempotency key = NativeRef
idempotency key = Request identity
idempotency row = Domain Operation
idempotency row = Decision
idempotency row = Provenance root
idempotency key = authorization token
```

### 36.32 DB-local canonical effect coordination

When a future material operation's whole effect is canonical PostgreSQL state, the reusable invariant is:

```text
reservation/claim
+
canonical effect
+
retained result binding

→ coordinated by the same outer PostgreSQL transaction
  or an equally strong DB-local atomic mechanism
```

A committed canonical effect must not coexist with reservation state falsely indicating no execution occurred.

### 36.33 External effect coordination

When the material operation includes an external effect that cannot share the PostgreSQL transaction, the applicable durable-coordination pieces may include:

```text
DANTE idempotency reservation
canonical pending/staged state where semantically required
transactional outbox for a real Class-A publication/effect
provider idempotency where available
provider receipt/outcome tracking
reconciliation for ambiguous outcome
```

Not every external operation requires every item.

### 36.34 No baseline operation exists

The current backend has no concrete product material operation whose retry can currently duplicate a business/canonical effect.

Therefore CP6 cannot currently close:

```text
operation_scope
fingerprint normalization
bounded result binding
retention horizon
caller scope
exact transaction ownership
```

for a real row.

### 36.35 DB-U18 final disposition

```text
DB-U18
CLOSED

CP6-04 BASELINE IDEMPOTENCY OBJECTS
0
```

No generic `dante.idempotency`, request-deduplication or operation-execution table is authorized in the baseline.

### 36.36 DB-U18 future materialization trigger

The first persistent material operation requiring retry/replay control MUST close:

```text
exact operation family/scope
idempotency key contract
scope+key uniqueness
normalized fingerprint algorithm/version
same-operation equivalence
bounded result binding
reservation/execution states if required
concurrency behavior
transaction coordination
retention/expiry
security/caller scoping
indexes
ACL
real PostgreSQL race/replay tests
```

Then the operation-specific or bounded shared technical idempotency structure may be introduced.

---

# DB-U19 — transactional outbox

### 36.37 Outbox remains Class-A only

The transactional outbox remains a selected technical runtime mechanism for a real Class-A requirement:

```text
canonical PostgreSQL commit
+
durable asynchronous publication / external dispatch
```

It is not a default companion table for every canonical mutation.

### 36.38 Outbox is not Domain history

Outbox rows are technical delivery/runtime state.

They MUST NOT become:

```text
universal Domain event ontology
canonical historical truth source
replacement for owner/material history
replacement for Provenance
replacement for Outcome
```

### 36.39 No generic integration-event root

CP6 baseline MUST NOT create a generic semantic table such as:

```text
dante.domain_event
dante.integration_event
dante.event_store
dante.message_event
```

simply because a future outbox may need an envelope.

### 36.40 No current Class-A flow

The current backend implements no product workflow that requires durable asynchronous publication or provider dispatch after a canonical commit.

Therefore no outbox row shape can currently be tied to a real destination/effect contract.

### 36.41 Future outbox identity

A future outbox implementation must define a bounded technical message/effect identity suitable for claiming, retry and deduplication.

That identity does not become NativeRef or Domain identity.

### 36.42 Future source basis

An outbox item must preserve enough basis to establish what canonical committed effect requires dispatch.

Depending on the real operation this may be:

```text
operation/effect identity
new MaterialStateRef
concrete owner/reference
bounded payload generated from committed state
another typed technical basis
```

No universal source tuple is invented today.

### 36.43 Future destination contract

The concrete Class-A consumer must define:

```text
destination/provider/transport
envelope/payload
routing
ordering requirement if any
delivery acknowledgment semantics
```

before DDL is created.

### 36.44 Retry and claim semantics

A real outbox must define worker claiming/concurrency and retry semantics.

Potential PostgreSQL tools may include row locks and `SKIP LOCKED`, but CP6 does not prescribe them before the worker model exists.

### 36.45 Delivery ambiguity

Transport timeout does not prove delivery failure.

The real Class-A contract must distinguish retry-safe, provider-idempotent and ambiguous outcomes and provide reconciliation where necessary.

### 36.46 Dead-letter/poison handling is not automatic

A dead-letter state/table is introduced only if the concrete runtime needs durable operator intervention or bounded poison-message handling.

No ceremonial dead-letter table is created in the baseline.

### 36.47 Retention is runtime-contract-specific

Outbox delivery history retention depends on operational recovery/audit requirements.

It is not canonical history retention by default.

### 36.48 DB-U19 final disposition

```text
DB-U19
CLOSED

CP6-04 BASELINE TRANSACTIONAL OUTBOX OBJECTS
0
```

### 36.49 DB-U19 future materialization trigger

The first real Class-A asynchronous effect MUST close:

```text
message/effect technical identity
producing canonical operation/effect basis
destination/provider/transport
payload/envelope
transactional insert point
claiming/concurrency
dispatch lifecycle
retry/backoff
provider idempotency
receipt/ack semantics
ambiguous result/reconciliation
operator/dead-letter behavior if required
retention
indexes
ACL
worker transaction contract
direct PostgreSQL concurrency/recovery proof
```

Only then is outbox DDL authorized.

---

# DB-U20 — derived / search / vector persisted structures

### 36.50 LR-08 remains noncanonical by default

Derived/search/projection state remains LR-08.

The baseline invariant remains:

```text
derived result
!= canonical truth

search ranking
!= canonical truth

vector nearest-neighbor result
!= canonical truth

cache freshness
!= source currentness unless explicitly proven
```

### 36.51 Ordinary views remain allowed

DB-U20 closure does NOT remove ordinary PostgreSQL views already justified elsewhere in the blueprint for cheap deterministic current-state access.

Examples include owner/current-binding views derived from canonical structures where their contract has already been closed.

Those are part of the final object inventory if previously accepted.

### 36.52 DB-U20 scope

DB-U20 governs new persisted/materialized LR-08 structures whose existence depends on a concrete query/search/vector consumer, including potential:

```text
materialized views
projection/cache tables
persisted search documents
persisted tsvector surfaces
trigram-specific query indexes
embedding tables
vector indexes
semantic-search caches
expensive derived read models
```

### 36.53 Cheap derivation prefers views

Where a result is cheap and deterministic from canonical state, an ordinary view is preferred over a materialized cache solely for convenience.

### 36.54 Materialization requires measured need

A materialized view/cache/projection requires demonstrated cost, latency, fan-out or query complexity value.

No table is created because a cache might improve performance later.

### 36.55 Materialized derived state must preserve basis

A consequential materialized projection must retain or reconstruct the material source basis needed to understand freshness and correctness.

Applicable basis may include:

```text
projection kind
bounded source set
source MaterialStateRefs/material basis
creation/refresh time
freshness/expiry semantics
purpose/context
security/disclosure scope
```

The exact profile is consumer-specific.

### 36.56 FTS capability remains dormant

PostgreSQL full-text search, `pg_trgm` and `unaccent` remain accepted capabilities.

Selection does not authorize a search schema or index without a real query contract.

### 36.57 Future FTS contract

Before persisted FTS/search structures are introduced, the consumer must close as applicable:

```text
source owner/facet fields
language/text-search configuration
tokenization
normalization/unaccent behavior
ranking
prefix/fuzzy/trigram behavior
filters
Visibility/disclosure non-interference
update/refresh strategy
freshness
index method
query latency/selectivity need
```

### 36.58 Search leakage remains a hard barrier

Search must preserve WL-H12 / disclosure non-interference.

Hidden information must not leak through:

```text
result existence
counts
rank order
error behavior
relation existence
snippets
facets
query timing class beyond accepted bounds
```

A future search structure must be designed and tested with that boundary.

### 36.59 pgvector capability remains dormant

pgvector remains an accepted PostgreSQL capability.

Its installation/availability does not imply a DANTE vector table or vector index.

### 36.60 Future vector contract

A concrete vector consumer must close at minimum:

```text
source family/facet
exact source MaterialStateRef/material basis
model/provider identity
model version
embedding dimension
normalization semantics
distance metric
index method
freshness/staleness
rebuild strategy
redaction/deletion propagation
Visibility/security scope
query contract
recall/latency target
```

before any persisted embedding/index becomes canonical database structure.

### 36.61 Embedding is not canonical meaning

A vector embedding is a derived representation produced by a specific model/version.

It MUST NOT become:

```text
canonical Content Artifact meaning
Observation truth
Evidence truth
Goal state
Outcome
identity
```

### 36.62 Model changes do not rewrite source history

A future embedding refresh due to model/version change creates/refreshed derived state.

It does not rewrite the canonical source MaterialState merely because the numeric vector changes.

### 36.63 Bounded JSON/search metadata

Search/vector implementation metadata may use bounded technical metadata where required, but required model/source/freshness/security semantics must remain explicit enough for reconstruction and proof.

### 36.64 No speculative query indexes

DB-U20 does not authorize:

```text
GIN on every text column
trigram on every display string
HNSW/IVFFlat without a vector consumer
materialized views for possible dashboards
```

Index creation is closed later through DB-U15 against the final actual object/query graph.

### 36.65 DB-U20 final disposition

```text
DB-U20
CLOSED

NEW CP6-04 BASELINE PERSISTED LR-08
SEARCH / VECTOR / CACHE OBJECTS
0
```

Already accepted deterministic ordinary/current-state views remain unaffected and continue into final inventory where applicable.

### 36.66 DB-U20 future materialization trigger

The first consumer demonstrating persisted derived-state need MUST close:

```text
consumer/query contract
source/material basis
canonical-vs-derived boundary
freshness/rebuild
security/disclosure
retention/redaction propagation
failure/recovery
index need
mapping/ownership
ACL
proof matrix
```

before DDL is introduced.

---

# Cross-cutting hardening

### 36.67 Selection does not imply activation

The selected technical stack may include available capability without requiring business schema.

Examples:

```text
pgvector available
!= vector table required

PostGIS available
!= geometry column required on every Place

PostgreSQL FTS available
!= search document table required

outbox selected as Class-A mechanism
!= outbox table required today
```

### 36.68 Provider + idempotency do not collapse

Provider idempotency tokens are provider-scoped technical facilities.

They do not replace a DANTE idempotency reservation when DANTE itself must prevent duplicate canonical effects.

Conversely, a DANTE reservation does not prove an external effect occurred exactly once.

### 36.69 Idempotency + outbox do not collapse

Idempotency controls repeated operation requests/effects.

Outbox controls durable post-commit asynchronous dispatch.

```text
idempotency
!= outbox
```

A future Class-A operation may require both, one, or neither depending on its exact effect topology.

### 36.70 Outbox + provider state do not collapse

An outbox dispatch attempt and a provider's accepted/applied state are distinct.

The outbox is not the provider reconciliation record.

### 36.71 Derived state + provider state do not collapse

Provider state is LR-09 external state.

Derived/search/vector state is LR-08 projection/query state.

A provider-returned embedding or search index payload does not collapse those representation roles.

### 36.72 No generic technical object registry

This checkpoint MUST NOT be used to create one generic technical table carrying:

```text
kind
key
status
payload
created_at
updated_at
```

for provider, idempotency, outbox and projections.

Their triggers, identity, lifecycle and semantics are different.

### 36.73 No new native owner

None of the following becomes LR-01:

```text
Provider
ExternalRef
Idempotency Reservation
Outbox Message
Projection
Search Document
Embedding
```

The native owner census remains exactly 15.

### 36.74 No baseline ScopedRecordRef inflation

No new ScopedRecordRef family is created merely to make any of these technical records uniformly addressable.

Future concrete technical records use the identity needed for their technical contract and only become scoped semantic records if upstream semantics genuinely justify that role.

### 36.75 MaterialStateRef boundary

Provider revisions, idempotency fingerprints, outbox message versions, search refresh versions and embedding model versions are not MaterialStateRef.

A derived/provider row may reference MaterialStateRef as source basis where needed.

### 36.76 Current-state boundary

No provider, outbox or derived row becomes current canonical state merely by being newest, successful or completed.

Explicit canonical current bindings remain owned by the accepted semantic owner/facet structures.

### 36.77 Chronology boundary

Technical timestamps such as:

```text
reserved_at
dispatched_at
provider_received_at
refreshed_at
embedded_at
```

may become valid fields in future concrete technical profiles.

They do not substitute for world/effective or accepted canonical chronology.

### 36.78 Security boundary

Future technical tables must follow least privilege and exact object-level ACL closure when introduced.

No generic provider/search/outbox object is added to DB-U21 now because no such object exists in the CP6 baseline inventory.

### 36.79 Index boundary

No speculative indexes are added from this checkpoint.

DB-U15 receives only real final baseline objects.

Future capability-triggered objects receive their indexes in the same schema-evolution change that introduces the concrete consumer.

### 36.80 SQLAlchemy boundary

CP6-04 baseline creates no SQLAlchemy mapping for a non-materialized provider/idempotency/outbox/search/vector object.

Future technical mappings remain technical and must not become polymorphic semantic superclasses.

### 36.81 Alembic boundary

CP6-04 baseline migration DAG contains no migration step solely for DB-U17/18/19/20 objects.

Future activation is ordinary reviewed schema evolution with the same documentation/dictionary/test discipline.

### 36.82 Database Dictionary boundary

The baseline Database Dictionary MUST NOT advertise nonexistent tables, views or indexes for these four capabilities.

Their non-materialization/future-trigger rationale remains in the human-readable architecture/reference until a real object exists.

### 36.83 Generated documentation boundary

Generated/introspection reference will include only actually materialized PostgreSQL objects.

Capability availability is not rendered as a fake business object.

### 36.84 Direct proof boundary

CP6-05 cannot truthfully run provider/idempotency/outbox/search/vector business-semantic tests against nonexistent concrete consumers.

Future activation inherits the applicable staged proof obligations and must add concrete direct tests.

---

# Future proof obligations by trigger

### 36.85 Provider direct-proof minimum

A future provider integration should directly prove, as applicable:

```text
issuer-scoped ExternalRef uniqueness
wrong provider/realm does not alias identity
eligible DANTE target enforcement
provider revision != MaterialStateRef
provider success does not bypass canonical acceptance
ambiguous result preserved/reconciled
provider payload cannot become generic canonical state
redaction/retention behavior
ACL isolation
```

### 36.86 Idempotency direct-proof minimum

A future persistent idempotency implementation should directly prove:

```text
same scope+key+same operation -> one material effect
same scope+key+different operation -> conflict
concurrent duplicates -> one winner
fingerprint immutable
canonical rollback -> reservation/result does not lie
reservation rollback -> no committed canonical effect mismatch
replay returns bounded established result
expiry obeys operation retention policy
```

### 36.87 Outbox direct-proof minimum

A future outbox implementation should directly prove:

```text
canonical commit + required outbox row atomic
canonical rollback -> no dispatchable outbox item
concurrent workers do not double-claim unsafely
retry after worker crash is safe
ambiguous provider outcome does not become false failure
successful dispatch lifecycle is reconstructible
retention does not delete still-needed recovery state
outbox payload cannot become Domain history authority
```

### 36.88 Search direct-proof minimum

A future search implementation should directly prove:

```text
canonical source updates reflected per freshness contract
hidden rows do not leak through results/counts/ranking/errors
search index absence does not alter canonical truth
rebuild produces semantically equivalent derived state
redaction/deletion propagates under contract
```

### 36.89 Vector direct-proof minimum

A future vector implementation should directly prove:

```text
embedding bound to correct source/material basis
model/version/dimension consistent
stale embedding handling explicit
rebuild after model change does not rewrite source truth
redaction/deletion propagation
security scope respected
vector nearest-neighbor result treated as derived retrieval only
```

---

# Whole-database cumulative audit

### 36.90 Audit questions

The cumulative review asks whether closing these four items at zero baseline DDL would accidentally remove or contradict an already accepted concrete database obligation.

The answer is no after repair/hardening.

### 36.91 Provider findings

Rejected/closed findings:

```text
generic Provider root                         REJECTED
generic ExternalRef registry                  REJECTED
generic provider mapping kind+uuid            REJECTED
provider payload JSONB as canonical shortcut  REJECTED
provider newest revision = current            REJECTED
provider success = canonical acceptance       REJECTED
```

### 36.92 Idempotency findings

Rejected/closed findings:

```text
generic idempotency table before real operation        REJECTED
(scope,key,fingerprint) reservation uniqueness         REJECTED
unbounded operation_scope text as completed contract   REJECTED
universal retention horizon                            REJECTED
idempotency key = Request/semantic identity             REJECTED
generic result JSON payload                            REJECTED
```

### 36.93 Outbox findings

Rejected/closed findings:

```text
outbox pre-materialized for future use      REJECTED
outbox = Domain history                     REJECTED
generic integration-event ontology          REJECTED
automatic dead-letter table                 REJECTED
one universal dispatch lifecycle            REJECTED
```

### 36.94 Derived/search/vector findings

Rejected/closed findings:

```text
materialized projection without consumer    REJECTED
FTS indexes without query contract           REJECTED
generic vector/embedding table               REJECTED
embedding without source/model basis         REJECTED
cache = canonical truth                      REJECTED
search/vector result = canonical truth       REJECTED
DB-U20 deleting already accepted views       REJECTED
```

### 36.95 Non-collapse regression

```text
provider != canonical                         PASS
ExternalRef != NativeRef                       PASS
provider revision != MaterialStateRef          PASS

idempotency != semantic identity               PASS
idempotency != Request                         PASS

outbox != Domain history                       PASS
outbox != Provenance                           PASS

LR-08 derived != canonical                     PASS
search result != canonical                     PASS
vector result != canonical                     PASS
cache freshness != source truth                PASS

selection != activation                        PASS
```

### 36.96 Census regression

```text
DOMAIN CONCEPTS
57 / 57
PASS

LR-01 NATIVE OWNERS
15 / 15
PASS

NEW NATIVE OWNER FROM CHECKPOINT I
0
```

### 36.97 Generic-fallback regression

```text
generic provider root               0
generic ExternalRef root            0
generic technical event root        0
generic idempotency semantic root   0
generic projection root             0
generic vector root                 0
semantic JSON fallback              0
```

### 36.98 Existing baseline objects remain intact

This checkpoint does not remove already accepted concrete database structures elsewhere in Parts 1–6.

In particular it does not invalidate:

```text
native/scoped/material address-control topology
owner-specific canonical tables
owner-specific material-state/history tables
current accepted-state bindings
specific relation families
accepted Schedule/Actual/Session/Recurrence structures
accepted deterministic current-state views
```

### 36.99 Current-state view clarification

The phrase:

```text
NO NEW PERSISTED LR-08 SEARCH/VECTOR/CACHE OBJECTS
```

must not be misread as:

```text
NO VIEWS IN THE BASELINE
```

Ordinary views that are already justified as deterministic access surfaces remain candidates for the final object inventory.

### 36.100 Capability-installation clarification

This checkpoint also does not remove selected PostgreSQL capabilities from the technical platform envelope.

It distinguishes:

```text
capability available / extension selected
```

from:

```text
business schema object justified
```

### 36.101 SQLAlchemy/Alembic inventory consequence

For the four closed DB-U items, baseline inventory contribution is:

```text
new tables                0
new materialized views    0
new search indexes        0
new vector indexes        0
new SQLAlchemy mappings   0
new business migrations   0
new baseline ACL entries  0
```

except already accepted ordinary views/objects from other closed sections remain unaffected.

### 36.102 DB-U15 consequence

DB-U15 must evaluate only the final actual baseline object/query graph.

It does not create indexes for dormant provider, outbox, search or vector objects.

### 36.103 DB-U21 consequence

DB-U21's final ACL matrix covers actual baseline objects only.

Future capability-triggered objects receive exact privileges in their introducing migration.

### 36.104 DB-U08 consequence

DB-U08 does not need to reserve names for absent provider/idempotency/outbox/search/vector objects.

Future names are frozen when those concrete object families are actually introduced.

---

# Final dispositions

### 36.105 DB-U17 closure

```text
DB-U17
PROVIDER / INTEGRATION OBJECT SHAPES

CLOSED

FINAL CP6 BASELINE DISPOSITION
NO GENERIC PROVIDER / INTEGRATION DDL

FUTURE TRIGGER
FIRST CONCRETE PROVIDER / INTEGRATION CONTRACT
```

### 36.106 DB-U18 closure

```text
DB-U18
IDEMPOTENCY PERSISTENCE TIMING

CLOSED

FINAL CP6 BASELINE DISPOSITION
NO GENERIC IDEMPOTENCY DDL

REUSABLE IDEM DOCTRINE
PRESERVED

FUTURE TRIGGER
FIRST PERSISTENT MATERIAL OPERATION
REQUIRING RESERVATION / REPLAY SEMANTICS
```

### 36.107 DB-U19 closure

```text
DB-U19
TRANSACTIONAL OUTBOX TIMING

CLOSED

FINAL CP6 BASELINE DISPOSITION
NO TRANSACTIONAL OUTBOX DDL

FUTURE TRIGGER
FIRST REAL CLASS-A ASYNCHRONOUS
EXTERNAL / PUBLICATION EFFECT
```

### 36.108 DB-U20 closure

```text
DB-U20
DERIVED / SEARCH / VECTOR PERSISTED STRUCTURES

CLOSED

FINAL CP6 BASELINE DISPOSITION
NO NEW PERSISTED LR-08 SEARCH / VECTOR / CACHE OBJECTS

ALREADY ACCEPTED ORDINARY/CURRENT-STATE VIEWS
UNAFFECTED

FUTURE TRIGGER
REAL QUERY / SEARCH / VECTOR CONSUMER
PROVING MATERIALIZATION OR INDEX NEED
```

### 36.109 Global unresolved register after Checkpoint I

Before this checkpoint:

```text
GLOBAL DB-U OPEN
7

DB-U08
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21
```

After this checkpoint:

```text
GLOBAL DB-U OPEN
3

DB-U08
DB-U15
DB-U21
```

### 36.110 Local unresolved register

```text
LOCAL EXACT OPEN
0
```

No local semantic blocker is reopened by this checkpoint.

### 36.111 Unclassified register

```text
UNCLASSIFIED NEW ITEMS
0
```

### 36.112 Whole accumulated database audit result

```text
WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER HARDENING

C DEFECTS AFTER REPAIR
0
```

This is a design/audit result only. It is not direct PostgreSQL execution evidence.

### 36.113 Gate 03 remains not earned

Despite reducing global DB-U items to three, Gate 03 remains closed because the final implementation-deterministic inventory has not yet been frozen.

Still required:

```text
DB-U08 final PostgreSQL object naming
DB-U15 final structural/query index matrix
DB-U21 final exact object privilege matrix

final actual object inventory
final column/type/nullability/default catalog
final PK/FK/UNIQUE/CHECK/EXCLUDE/trigger catalog
final Reference Contract integrity catalog
final migration dependency DAG
final SQLAlchemy mapping plan
Database Dictionary initialization/freeze
final direct PostgreSQL proof plan
whole-database final reconciliation
```

Therefore:

```text
CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

### 36.114 Next CP6-03 boundary — final inventory freeze

The next block changes the nature of CP6-03 work.

The question is no longer primarily:

```text
Does another semantic/capability family need baseline persistence?
```

After Checkpoint I the unresolved question becomes:

```text
What exact PostgreSQL objects from the accumulated blueprint
will CP6-04 create,
under what final names,
with what exact indexes,
and with what exact PostgreSQL privileges?
```

The remaining three DB-U items are therefore coupled to the final object inventory:

```text
DB-U08
→ exact deterministic PostgreSQL names for every real object

DB-U15
→ exact structural/query indexes for every real object

DB-U21
→ exact owner/migrator/runtime/PUBLIC privilege matrix
  for every real object
```

### 36.115 Practical-vs-materialization boundary

The next block is still CP6-03 design.

It will enumerate and freeze what must be created, but MUST NOT yet execute business DDL.

The real database creation boundary remains:

```text
CP6-03 FINAL FREEZE + GATE 03 PASS
        ↓
EXPLICIT USER-APPROVED MATERIALIZATION GATE
        ↓
CP6-04
REAL ALEMBIC / SQLALCHEMY / POSTGRESQL MATERIALIZATION
```

No transition into CP6-04 is implied by completing Checkpoint I.

### 36.116 Checkpoint I final state

```text
CONSOLIDATION CHECKPOINT I
PROVIDER / IDEMPOTENCY / OUTBOX / DERIVED

PASS AFTER HARDENING

DB-U17
CLOSED

DB-U18
CLOSED

DB-U19
CLOSED

DB-U20
CLOSED

PROVIDER / INTEGRATION BASELINE DDL
NONE

IDEMPOTENCY BASELINE DDL
NONE

TRANSACTIONAL OUTBOX BASELINE DDL
NONE

NEW PERSISTED SEARCH / VECTOR / CACHE BASELINE OBJECTS
NONE

ALREADY ACCEPTED ORDINARY/CURRENT-STATE VIEWS
UNAFFECTED

LOCAL EXACT OPEN
0

GLOBAL DB-U OPEN
3

GLOBAL DB-U OPEN SET
DB-U08
DB-U15
DB-U21

UNCLASSIFIED NEW ITEMS
0

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER HARDENING

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

Part 7 remains CP6-03 design authority. It creates no business DDL, Alembic business migration, SQLAlchemy business mapping, provider integration, idempotency implementation, outbox worker, search index or vector persistence object.
