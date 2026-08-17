# ADR-006: Hybrid Personal Data and Semantic Relationship Model

- Status: **Superseded as canonical semantic/data-model architecture**
- Date: 2026-08-10
- Superseded for current execution: 2026-08-17
- Current authority: accepted Domain Atlas + closed Logical Model + future separately authorized Physical Model

## Original context

LifeOS needed to represent broad, user-specific personal data while retaining strong consistency for planning, history, permissions and cross-domain behavior. The original design therefore proposed PostgreSQL with a hybrid typed/flexible/graph-like model rather than either a rigid table-per-domain approach or an unstructured document store.

## Original decision

The original architecture proposed:

1. typed relational structures for stable concepts;
2. metadata/JSONB for genuinely flexible or provider-specific properties;
3. a graph-like relationship layer for personal/emergent/uncertain links;
4. provenance/status for inferred or observed facts/relationships;
5. version/audit/event history;
6. shared schema rather than per-user/per-domain databases.

It also proposed beginning new domains with a generic model and progressively formalizing repeated/high-value concepts.

## Why this ADR is superseded

Subsequent Domain Validation Methodology v3 and Whole-Logical work established a materially more precise semantic architecture.

The following implications of this ADR are no longer current:

- a universal or generic semantic relationship layer as canonical fallback;
- generic-model-first semantics for unknown domains;
- promotion to first-class semantic ownership based mainly on repeated usage/query pressure;
- AI persisting uncertainty through generic canonical entities/relations/properties;
- PostgreSQL being final merely because the hybrid model was originally framed around it.

The accepted architecture now requires:

```text
technical shared representation != universal semantic owner
technical edge/reference != universal semantic Relationship
flexible metadata != semantic-debt storage
AI uncertainty != fabricated generic canonical truth
query/storage convenience != ontology authority
```

## Knowledge retained from the original ADR

Several technical principles remain valid and are carried by current architecture/Logical sources:

- avoid per-user/per-domain schema proliferation;
- preserve strong typed/invariant-bearing semantics where required;
- allow bounded metadata/JSON/provider-specific extension where semantics permit;
- preserve provenance and reconciliation for external/inferred data;
- preserve material history/correction/version semantics;
- provider abstraction remains separate from canonical LifeOS meaning;
- AI cannot invent physical schema;
- specialized infrastructure requires demonstrated benefit rather than fashion-driven adoption.

These retained principles no longer imply the old generic semantic model.

## Current replacement

Current semantic authority:

- [`../domain/README.md`](../domain/README.md)
- [`../domain/language-map.md`](../domain/language-map.md)
- [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md)
- [`../logical-model/decision-and-assumption-register-v1-part-9.md`](../logical-model/decision-and-assumption-register-v1-part-9.md)

Current architecture summary:

- [`../architecture/README.md`](../architecture/README.md)
- [`../architecture/system-overview.md`](../architecture/system-overview.md)
- [`../architecture/technical-decisions.md`](../architecture/technical-decisions.md)

## Physical boundary

This supersession does not select a Physical database or schema.

PostgreSQL hybrid remains the current preferred Physical baseline, TypeDB is a mandatory challenger, and bounded graph/event/document mechanisms remain candidates. Generic EAV/generic-edge/universal meta-model design remains rejected for the canonical kernel.
