# ADR-007: Domain-Model-Informed Persistence Boundaries

- Status: Accepted
- Date: 2026-08-16
- Supersedes: only the semantic-authority implications of earlier generic-model language in ADR-006 and related architecture documents; PostgreSQL, hybrid persistence, provider abstraction and progressive implementation remain valid where compatible with the final Domain Atlas.

## Context

ADR-006 and the August 10 architecture documents were intentionally written before the final LifeOS Domain Atlas existed. They established useful technical direction: PostgreSQL as the primary source of truth, a hybrid typed/flexible persistence approach, provider adapters, version/audit history, and the ability to support open-ended personal domains without one table per imaginable subject.

Subsequent Domain Validation Methodology v3 work materially refined the semantic model. The accepted Domain Atlas now rejects several assumptions that a generic persistence layer could accidentally reintroduce, including:

- a universal semantic `Relationship`/`Relation` root;
- semantic-free `related_to` canonical truth;
- universal `Register` semantics;
- provider or storage objects as canonical LifeOS identity;
- creating native domain primitives because of query frequency, cardinality, UI grouping or storage convenience;
- treating product profiles such as Project/Program as independent kernel primitives merely because they have product identity;
- using arbitrary generic properties/relations as canonical fallback when AI interpretation is semantically unresolved.

The semantic model must therefore govern persistence design, not the reverse.

## Decision

### 1. Domain Atlas is authoritative for semantic meaning

When legacy architecture examples conflict with later accepted Domain Atlas definitions or validation checkpoints, the later Domain Atlas decision controls semantic interpretation.

```text
accepted Domain Atlas / validation checkpoint
        >
legacy generic-model semantic assumption
```

This ADR does not erase the earlier history. It constrains how that history may be implemented.

### 2. Technical generic mechanisms are allowed, semantic generic roots are not implied

A logical/physical implementation may use shared technical mechanisms where useful, including:

- common identity/reference registries;
- typed discriminators;
- shared history/version infrastructure;
- typed edge/reference tables;
- JSONB or metadata for genuinely flexible/provider-specific properties;
- search/index projections;
- provider sync/reconciliation tables.

But:

```text
technical registry != universal semantic Entity/Thing root
technical edge row != universal semantic Relationship
shared table != shared ontology parent
object_type discriminator != proof of domain superclass
```

The database may generalize representation without generalizing domain meaning.

### 3. Specific semantic owner takes precedence over generic edge

When LifeOS knows the meaning, persistence/API representation must preserve the specific accepted semantic family.

Examples include:

```text
Participation
Responsibility
Coordination Stewardship
Authority
Visibility
Agreement
Consent
Representation
Membership
Contribution
Ownership
Possession
Interpersonal Relationship
Dependency
Resource Allocation
```

A physical shared relation table may store several such typed families if that design survives logical-model validation, but an untyped or semantically weak `related_to` record must not replace them.

### 4. Generic relation/property is not a canonical AI fallback

If input cannot be expressed precisely with the accepted semantic vocabulary, AI or ingestion logic may retain source material and create a proposal/candidate with Provenance and uncertainty, or leave the interpretation unresolved.

It must not silently establish:

```text
generic canonical Relation
arbitrary canonical property
new ontology type
```

Merely persisting uncertainty as `related_to` would manufacture truth the semantic model has explicitly rejected.

### 5. JSONB is an extension mechanism, not semantic debt storage

JSONB/provider metadata may represent:

- provider-specific fields;
- low-consequence flexible descriptive properties;
- adapter payload remnants needed for reconciliation;
- specialist or optional metadata whose semantics are not part of the general kernel.

It must not become an escape hatch for required but unclassified kernel semantics.

If repeated concrete LifeOS workflows demonstrate a missing semantic owner, the normal evidence → simulation → V3 review process applies.

### 6. Product object identity does not automatically create domain-native identity

Product concepts and UX containers may have application identifiers without becoming native semantic referents.

Examples historically discussed as product profiles/organization include Project, Program, Calendar/Life Area, Inbox Item, Module, Template, Review Queue and similar constructs.

Their product identity may be useful operationally. That alone does not override their semantic classification.

### 7. Provider identity remains external evidence

Provider IDs, URLs, file IDs, place IDs, calendar IDs and analogous external identifiers remain integration/reconciliation evidence unless an accepted owner explicitly defines otherwise.

```text
provider object != LifeOS canonical identity automatically
```

### 8. Persistence pressure cannot justify ontology changes by convenience

The following are insufficient, by themselves, to create or merge a semantic primitive:

```text
foreign-key convenience
query frequency
index convenience
cardinality
UI grouping
serialization shape
one-table implementation preference
provider schema
AI output schema
```

If logical implementation pressure reveals that no representation can preserve accepted invariants, that is valid evidence for a targeted semantic reopen. The implementation must demonstrate the contradiction; convenience alone is not enough.

## Required logical-model invariants

The next logical-model stage must prove that its representation can preserve at least the following distinctions:

```text
Person != Account != Actor
Goal != Plan != Activity != Event
Routine != Occurrence
Occurrence != Schedule
Schedule != Session
Session != Actual
Actual != Observation != Outcome
Confirmation != Evidence != Provenance
Asset != Resource
Place != Asset
Content Artifact != file/blob/provider representation
Quantity != MonetaryAmount
Responsibility != Participation != Coordination Stewardship
Authority != Visibility
Agreement != Consent
Ownership != Possession
Collective != current member set
current != historical
correction != silent overwrite
provider state != canonical LifeOS state automatically
```

The list is illustrative, not a substitute for the full Domain Atlas.

## What remains valid from ADR-006

Unless contradicted by this ADR or later reviewed decisions, the following direction remains valid:

- PostgreSQL as primary source of truth;
- shared schema across users/workspaces;
- typed relational structures for stable/high-value semantics;
- JSONB/metadata for genuinely flexible/provider-specific data;
- provider adapters and reconciliation;
- auditable version/history support;
- no per-user/per-domain database/table proliferation;
- AI cannot invent physical schema;
- specialized infrastructure only when justified by real workload.

## Consequences

- The logical model must be designed from accepted semantics rather than from old candidate table lists.
- A generic technical relation/reference mechanism is permissible only if every canonical semantic use remains typed, validated and queryable without semantic collapse.
- Unsupported semantic interpretations remain unresolved/proposed rather than becoming generic canonical facts.
- Architecture documentation predating the final Domain Atlas is historical context, not independent ontology authority.
- SQL, migrations, API resources and backend implementation remain separately gated after logical-model validation.
