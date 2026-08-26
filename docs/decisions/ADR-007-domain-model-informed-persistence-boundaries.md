# ADR-007: Domain-Model-Informed Persistence Boundaries

- Status: **Accepted semantic guardrail / Physical posture superseded by later selection**
- Date: 2026-08-16
- Qualified: 2026-08-17
- Current semantic authority: accepted Domain Atlas + closed Logical Model
- Current Physical replacement authority: closed Physical Model + ADR-010 + closed CP6-02 PostgreSQL Persistence Constitution

## Context

Earlier architecture material predated the final Domain Atlas and risked allowing generic persistence mechanisms to redefine LifeOS semantics.

Subsequent Domain Validation Methodology v3 and Whole-Logical work confirmed that persistence must preserve accepted semantic ownership rather than manufacture universal roots for convenience.

## Decision

### 1. Domain and Logical semantics govern persistence

When implementation pressure conflicts with accepted Domain/Logical meaning, the accepted semantic model controls unless a separate explicit reopen demonstrates a genuine contradiction.

```text
accepted Domain Atlas + closed Logical Model
        >
legacy generic-model assumption
        >
provider/storage/API convenience
```

### 2. Representation is not ontology

Technical implementation may use shared mechanisms such as:

- common reference/identity registries;
- typed discriminators;
- shared history/version infrastructure;
- typed edge/reference structures;
- JSON/provider metadata;
- search/index projections;
- provider sync/reconciliation structures.

But:

```text
technical registry != universal semantic Entity/Thing root
technical edge row != universal semantic Relationship
shared table != shared ontology parent
discriminator != proof of domain superclass
```

### 3. Specific semantics beat generic fallback

Where LifeOS knows the accepted meaning, persistence/API representation must preserve the specific semantic owner/relation/governance family.

A semantically weak `related_to` or arbitrary property must not replace accepted semantics merely because it is easier to store.

### 4. Uncertainty remains uncertainty

If input cannot be represented precisely with accepted semantics, AI/ingestion may retain source material and unresolved/candidate state with provenance.

It must not silently establish:

```text
generic canonical Relationship
arbitrary canonical property
new ontology owner
```

### 5. Flexible metadata is bounded

JSON/provider metadata may represent provider-specific fields, low-consequence flexible descriptive properties, reconciliation payload remnants, specialist/optional metadata and implementation projections where semantics permit.

It must not hide a required but unclassified kernel semantic owner/material state.

### 6. Product/runtime identity does not imply Domain-native identity

Product containers, profiles, UI objects, technical runtime objects, provider objects and storage objects may have identifiers without thereby becoming native semantic referents.

### 7. Provider identity remains external representation

Provider IDs, URLs, file IDs, place IDs, calendar IDs and analogous identifiers remain integration/reconciliation representation unless accepted semantics explicitly establish otherwise.

```text
provider object != canonical LifeOS identity automatically
provider state != canonical LifeOS truth automatically
```

### 8. Persistence pressure cannot justify ontology changes by convenience

The following are insufficient by themselves to create/merge semantic primitives:

```text
foreign-key convenience
query frequency
index convenience
cardinality
UI grouping
serialization shape
one-table preference
provider schema
AI output schema
```

If no implementation can preserve an accepted invariant, that is valid evidence for a targeted reopen. Convenience is not.

## Logical-model hardening now carried forward

The closed Logical Model expands this ADR's original guardrails with `WL-H01..WL-H12`, including:

- justified material Agreement terms;
- governed operation/effect contract;
- bounded projection/disclosure surfaces;
- absence/unknown not collapsing to false;
- expected-state consequential writes;
- idempotency distinct from identity;
- truthful multi-owner consistency;
- canonical/provider-state separation;
- derived-state freshness/material basis;
- retention/redaction/tombstone integrity;
- reconstructible consequential AuthZ provenance;
- non-interference/inference-leakage protection.

These Logical contracts are now the stronger downstream authority.

## Historical pre-selection Physical qualification

When this ADR was qualified on 2026-08-17, the Physical benchmark had not yet closed. The then-current posture was:

```text
PostgreSQL hybrid
PREFERRED PHYSICAL BASELINE — not yet final selection at that checkpoint

TypeDB
MANDATORY PHYSICAL BENCHMARK CHALLENGER at that checkpoint

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE at that checkpoint

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

That block is retained as historical selection-process rationale only.

## Current Physical truth

The later Physical Model completed the benchmark and closed the persistence architecture:

```text
PostgreSQL 18 major family
CLOSED / SELECTED / ACCEPTED
sole canonical persistence + material-history authority

Physical exact phase-time patch
18.4 / HISTORICAL

current repository-controlled patch
18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS
```

The old PostgreSQL-vs-TypeDB/Neo4j selection contest is therefore not an open current decision. Reopening canonical persistence requires materially changed requirements/evidence and an explicit architecture gate.

The detailed physical persistence doctrine is now governed by ADR-010 and the closed CP6-02 Constitution.

## Consequences

- Physical/database implementation starts from the closed Domain + Logical + Physical models, not old candidate table lists.
- Shared technical representations are allowed only where semantic boundaries remain explicit and reconstructible.
- Unsupported interpretation remains unresolved/proposed rather than becoming generic canonical truth.
- Current PostgreSQL schema/mapping choices remain separately gated inside CP6 even though the canonical database family is selected.
- A genuine semantic contradiction triggers a targeted reopen; implementation convenience does not.

## Historical relation to ADR-006

This ADR originally superseded the semantic-authority implications of ADR-006. ADR-006 is explicitly superseded as canonical semantic/data-model architecture. This ADR remains current for its semantic guardrails; only its old pre-selection Physical posture is historical.