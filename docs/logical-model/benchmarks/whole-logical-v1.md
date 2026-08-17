# Whole-Logical Technology / Mechanism Benchmark v1

**Status:** FINAL LOGICAL-STAGE BENCHMARK — CURRENT EVIDENCE REFRESHED  
**Date:** 2026-08-17  
**Scope:** architecture/mechanism reconsideration for integrated A+B+C+D+E+F  
**Decision class:** Logical Model evidence; concrete Physical Model selection remains stage-deferred

## 1. Purpose

The final Whole-Logical checkpoint reopens the mechanism/technology question under the complete A–F pressure rather than treating ADR-006 or an earlier preference as permanent truth.

The benchmark asks:

> Which current mechanism family gives LifeOS the best system-wide Physical Model starting point while preserving the accepted Logical Model, and which alternatives are strong enough that they must still compete later?

It does **not** ask which vendor should define LifeOS ontology.

Comparison dimensions:

```text
semantic preservation
reverse mapping
identity/reference integrity
history/correction
n-ary / typed relation support
privacy/governance
transaction/concurrency plausibility
provider integration
query/reporting ergonomics
high-volume data pressure
simple-case ceremony
operability/evolution
physical implementation freedom
```

## 2. Evidence policy

Only current primary/vendor documentation is used for technology capabilities. Product/vendor features are evidence about implementation mechanisms, not authority over Domain semantics.

Primary evidence refreshed for this checkpoint includes:

```text
PostgreSQL 18 official documentation
- transaction isolation / Serializable
- CREATE TABLE temporal WITHOUT OVERLAPS constraints
- JSON / JSONB
- row security policies

TypeDB official documentation
- entities, relations, roles, attributes
- cardinality constraints
- schema/data constraints
- transactions and isolation

Neo4j official documentation
- graph types / constraints
- relationship structure and constraints
- Cypher/current graph semantics

Kurrent official documentation
- event streams
- projections
- projection/write behavior

MongoDB official documentation
- flexible schema / schema validation
- multi-document transactions

OpenFGA official documentation
- authorization model + relationship tuples
- domain-modeling guidance
- ReBAC semantics
```

## 3. Whole pressure that materially changed the comparison

By Slice F and Whole integration, a viable physical baseline must plausibly support all of:

```text
15 independent native identity families
ScopedRecordRef + MaterialStateRef history
owner-specific dependent/material state
specific typed binary and n-ary relations
Agreement common-ground terms binding
Authority / Consent / Visibility / Representation history
provider/canonical divergence
expected-state mutation
idempotent retry
multi-owner consistency
selective disclosure
high-value historical/current queries
LR-08 projections and freshness
specialist/raw/provider payloads
```

No one capability is allowed to dominate the system-wide verdict.

---

# 4. PostgreSQL hybrid — RETAIN + HARDEN / CURRENT PREFERRED BASELINE

PostgreSQL remains the strongest current **system-wide baseline**, not necessarily the most elegant representation for every individual relation.

Current official PostgreSQL 18 capabilities relevant to LifeOS include:

```text
Serializable transaction isolation
mature relational constraints and referential modeling
range/temporal constraint support, including WITHOUT OVERLAPS
JSONB with indexing for bounded flexible/provider data
row security as a possible technical enforcement ingredient
```

Whole interpretation:

```text
relational tables/constraints
+ owner-specific or shared typed relation structures where safe
+ explicit material-state/history structures
+ JSONB only for bounded flexible/provider detail
+ derived/search/read projections
```

can preserve the current Logical Model without requiring a universal semantic root.

Important non-equivalences:

```text
WITHOUT OVERLAPS
!= universal rule that real LifeOS states cannot conflict/overcommit

RLS
!= Domain Visibility

row version / transaction ID
!= MaterialStateRef

JSONB
!= canonical property-bag escape hatch
```

### Strengths

- mature all-or-nothing transaction support for co-located owner changes;
- Serializable option for the strongest concurrency cases, with retry semantics where serialization fails;
- strong relational integrity and reporting/query ecosystem;
- temporal/range and ordinary relational representations can coexist;
- flexible provider payloads can remain bounded rather than infecting canonical semantics;
- operational maturity and broad ecosystem reduce system-wide implementation risk.

### Risks / required hardening

- generic relation tables can still become semantic `type + payload` escape hatches if unconstrained;
- current-row CRUD can destroy MaterialState semantics unless history is designed explicitly;
- RLS can be mistaken for Visibility if the architecture is careless;
- relational convenience can tempt false universal roots.

Verdict:

```text
POSTGRESQL HYBRID
RETAIN + HARDEN
CURRENT PREFERRED PHYSICAL BASELINE

NOT YET ADOPTED AS FINAL PHYSICAL MODEL
```

---

# 5. TypeDB — STRONGEST CHALLENGER / MANDATORY PHYSICAL BENCHMARK

TypeDB is the most important challenger discovered/reconsidered under Whole pressure.

Its native model explicitly supports:

```text
entities
relations
roles
attributes
n-ary relations
role/cardinality constraints
schema-level type semantics
```

These are structurally attractive for LifeOS families such as:

```text
Agreement
Membership
Responsibility
Participation
Representation
Authority
qualified multi-party relations
```

It therefore cannot be dismissed as merely a graph novelty.

### Why it is not selected at Logical stage

The system-wide question is larger than relation elegance. Whole A–F also requires:

```text
historical/material-state reconstruction
consequential concurrency
provider synchronization
reporting/analytics
high-volume observation/telemetry boundaries
operational tooling
migration/evolution confidence
selective physical specialization
```

Current TypeDB transaction documentation describes ACID transactions with isolation up to snapshot isolation. That does not prove a defect, but it means LifeOS must benchmark actual concurrency/conflict workloads rather than assume equivalent behavior to a PostgreSQL Serializable design.

Verdict:

```text
TYPEDB
STRONGEST CHALLENGER
MANDATORY PHYSICAL-MODEL BENCHMARK CHALLENGER

CURRENTLY DOES NOT PROVE
A NET SYSTEM-WIDE WIN
OVER POSTGRESQL HYBRID
```

Physical Model must therefore test it seriously. If it wins the actual workload without degrading history, concurrency, reporting, provider integration, telemetry or operability, the baseline must be replaced rather than defended by inertia.

---

# 6. Neo4j / property graph — SERIOUS SECONDARY CANDIDATE

Current Neo4j/Cypher capabilities are materially stronger than an old assumption of an unconstrained property graph would imply. Current documentation includes graph types and relationship/property constraints.

However its core relationship form remains naturally node-to-node with a relationship type/direction. Several LifeOS meanings are not merely binary traversals:

```text
n-ary Agreement common ground
party assent to one material terms state
qualified governance basis
relation state + provenance + selective disclosure
```

These can be modeled in a graph, but require additional nodes/structures whose system-wide advantage over the relational baseline must be proven.

Verdict:

```text
PRIMARY CANONICAL SOURCE OF RECORD
NOT SELECTED

GRAPH / READ / TRAVERSAL PROJECTION
SERIOUS CANDIDATE
```

Physical benchmark may still include Neo4j where traversal/read value is substantial.

---

# 7. Kurrent / universal event sourcing — REJECT AS PRIMARY ONTOLOGY

Event streams and projections are strong mechanisms for:

```text
append-only history
integration events
derived projections
replay-oriented workflows
optimistic stream concurrency
```

Kurrent documentation also makes the operational reality explicit: projections are derived machinery and can create additional writes/read models.

This is valuable for bounded history/integration use. It does not make:

```text
event type + payload
```

a better semantic owner for every LifeOS concept.

Whole requirements still need deterministic current-state queryability, specific relation ownership, material-state binding, selective governance and compact simple cases.

Verdict:

```text
UNIVERSAL EVENT SOURCING AS LIFEOS ONTOLOGY
REJECT

BOUNDED EVENT / HISTORY / OUTBOX / INTEGRATION MECHANISM
RETAIN AS PHYSICAL CANDIDATE
```

---

# 8. MongoDB / document primary — REJECT FOR CANONICAL CORE

MongoDB provides flexible documents, schema validation and multi-document transactions.

Strong bounded use cases remain:

```text
provider payloads
external/raw representations
specialist documents
low-consequence extension metadata
```

But flexible nesting does not itself solve:

```text
specific relation semantics
MaterialState binding
reverse mapping
historical applicability
n-ary common ground
selective relation/source disclosure
```

Using document flexibility as the main kernel representation would increase the risk of property-bag drift.

Verdict:

```text
MONGO / DOCUMENT PRIMARY CANONICAL CORE
REJECT

BOUNDED PROVIDER / SPECIALIST / FLEXIBLE DATA
RETAIN
```

---

# 9. Generic EAV / generic edge / meta-model — HARD REJECT

A generic model such as:

```text
object(id,type,payload)
edge(from,type,to,payload)
property(owner,key,value)
```

fails Whole reverse mapping when it becomes the canonical semantic owner/fallback.

The failure is not that shared technical storage is forbidden. The failure is losing enforceable owner semantics and relying on strings/payload convention to reconstruct them.

OpenFGA is a useful negative benchmark here: despite being relation-oriented authorization infrastructure, its current best-practice guidance explicitly emphasizes modeling the domain rather than building an excessively generic meta-model.

Verdict:

```text
GENERIC EAV / GENERIC EDGE / META-MODEL
HARD REJECT FOR CANONICAL LIFEOS MEANING
```

---

# 10. Authorization technologies — projection/enforcement only

OpenFGA/Zanzibar-style ReBAC, Cedar/ABAC, OPA/Rego, capabilities or a custom/hybrid engine remain runtime candidates.

Whole rule remains:

```text
LifeOS Authority / Consent / Visibility / Agreement / Membership / Representation
-> bounded technical projection
-> Principal + action/resource/context or equivalent
-> runtime allow/deny
```

The reverse identity is forbidden:

```text
ALLOW != Authority
DENY != established absence of Authority
Principal != Actor
AuthZ tuple/policy store != canonical Domain ontology
```

No authorization engine is selected by this benchmark.

---

# 11. Technology reconsideration scorecard

| Candidate | Semantic preservation | History/concurrency | Relation fit | Provider/reporting/ops | Whole verdict |
|---|---|---|---|---|---|
| PostgreSQL hybrid | strong if owner typing enforced | strong baseline; explicit history design required | good/hybrid | strongest current system-wide baseline | RETAIN + HARDEN |
| TypeDB | strong typed relation semantics | must benchmark Whole workload/concurrency | excellent for many F families | system-wide superiority unproven | MANDATORY CHALLENGER |
| Neo4j | strong graph traversal semantics | viable but n-ary/material patterns need added structures | strong binary graph fit | strong secondary/read candidate | SERIOUS SECONDARY |
| event-store primary | owner meaning can degrade to event vocabulary | excellent history mechanism, projection costs | indirect | bounded mechanism valuable | REJECT PRIMARY ONTOLOGY |
| Mongo/document primary | flexible but weaker semantic pressure by default | transactions available, history still explicit | indirect | excellent bounded payload/document use | REJECT CANONICAL CORE |
| generic EAV/meta-model | poor reverse mapping | weak semantic guarantees | superficially flexible | high semantic drift risk | HARD REJECT |

## 12. Whole verdict

```text
TECHNOLOGY / MECHANISM RECONSIDERATION
PASS

CURRENT PREFERRED BASELINE
PostgreSQL hybrid
RETAIN + HARDEN

MANDATORY PHYSICAL CHALLENGER
TypeDB

SERIOUS SECONDARY
Neo4j / graph projection

BOUNDED MECHANISMS
Event streams / document stores / specialist stores

HARD REJECT
Generic semantic-free meta-model
```

This benchmark satisfies Logical Model mechanism-reconsideration pressure only. Physical Model must run its own concrete workload/schema/query benchmark before technology adoption.

## 13. Primary sources refreshed

- PostgreSQL 18 — Transaction Isolation: `https://www.postgresql.org/docs/18/transaction-iso.html`
- PostgreSQL 18 — CREATE TABLE / temporal constraints: `https://www.postgresql.org/docs/18/sql-createtable.html`
- PostgreSQL 18 — JSON Types: `https://www.postgresql.org/docs/18/datatype-json.html`
- PostgreSQL 18 — Row Security Policies: `https://www.postgresql.org/docs/18/ddl-rowsecurity.html`
- TypeDB — Entities / Relations / Attributes: `https://typedb.com/docs/typeql-reference/definitions/`
- TypeDB — Constraints: `https://typedb.com/docs/typeql-reference/constraints/`
- TypeDB — Transactions: `https://typedb.com/docs/maintenance-operation/operation/transactions/`
- Neo4j — Constraints: `https://neo4j.com/docs/cypher-manual/current/constraints/`
- Neo4j — Graph types / values: `https://neo4j.com/docs/cypher-manual/current/values-and-types/property-structural-constructed/`
- Kurrent — Projections: `https://docs.kurrent.io/server/current/features/projections/`
- MongoDB — Schema Validation: `https://www.mongodb.com/docs/manual/core/schema-validation/`
- MongoDB — Transactions: `https://www.mongodb.com/docs/manual/core/transactions/`
- OpenFGA — Modeling / design principles: `https://openfga.dev/docs/modeling/design-patterns`

If a later Physical benchmark finds a material change in these capabilities, evidence must be refreshed rather than preserving this verdict by inertia.
