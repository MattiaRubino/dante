# Multi-Actor / Collaboration Discovery

- Status: **EVIDENCE COMPLETE — simulation + unified deep research + QC complete; awaiting PR review/merge**
- Branch: `docs/multi-actor-discovery`
- Pull request: #6 — ready for review
- Scope: product discovery evidence for future multi-user, multi-actor and collaboration direction. This workstream does not change current V1 implementation boundaries or define collaboration architecture.

## Source-of-truth documents

- [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md) — completed multi-actor discovery simulation
- [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md) — single consolidated and quality-checked external deep-research document
- [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md) — earlier cross-domain discovery study used as methodological precedent
- [`../product/v1-adaptive-intelligence-and-future-social.md`](../product/v1-adaptive-intelligence-and-future-social.md) — accepted current V1/future-social boundary
- [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md) — accepted current concept meanings
- [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md) — accepted current architecture; not superseded by this evidence

## Completed work

- Created a dedicated multi-actor discovery simulation on 2026-08-11.
- Preserved persona-driven discovery as a first-class lens and added progressive real-life multi-actor scenarios.
- Simulated `without LifeOS → with LifeOS` behavior across social, household, work, caregiving, specialist and complex organizational contexts.
- Added actor-by-actor needs, non-LifeOS participants, privacy boundaries, stress variations, longitudinal relationship changes, negative evidence and cross-case universality classification.
- Performed a broad external research pass across CSCW/groupware, coordination theory, common ground/awareness, calendars/privacy, household/family coordination and mental load, scheduling/fairness, caregiving/healthcare, education, shared expenses, external participation, privacy-by-design, authorization feasibility and current products.
- Deepened high-risk areas: adversarial exits and technology-facilitated abuse, ongoing high-conflict collaboration, child/adolescent agency and guardian power, accessibility/older adults/low digital literacy, and AI-mediated multi-party privacy/leakage.
- Consolidated the broad research and stress-domain research into **one** canonical research document rather than maintaining overlapping research files.
- Performed a semantic and bibliographic QC pass: removed duplicated research themes, preserved genuine trade-offs, corrected several emerging-source identifiers/links, added source support for smart-home/IPV claims, and added ongoing high-conflict co-parenting as the last materially distinct research family.
- Recorded a consolidated risk register, validation questions, evidence-confidence classification, negative evidence and a five-layer analytical framing: shared reality, dependency, actor relationship, personal interpretation and coordination evidence.
- Updated the `docs/product/` Discovery / evidence index.
- Kept simulation, research and accepted V1/architecture documents separate.
- PR #6 is the ready-for-review container for the completed evidence work.

## QC outcome

No external evidence overturns the central simulation hypothesis. The research strengthens it but introduces important tensions that must remain visible:

- more structure can reduce ambiguity while increasing coordination bureaucracy;
- more awareness can improve coordination while enabling surveillance;
- more transparency can improve explanation while violating privacy/minimization;
- more automation can reduce visible work while increasing supervision and mental load;
- auditability can support difficult collaboration while also amplifying conflict;
- equal participation can support agency but is not universally appropriate where bounded legitimate authority exists;
- revocation can be safety-critical while real-world legal/parental/financial obligations may remain.

These are deliberate product tensions, not documentation contradictions.

## Main research additions beyond the simulation

External evidence materially strengthened:

- **coordination-cost fairness:** a feature can benefit an organizer while shifting maintenance work onto other actors;
- **common ground:** message delivery is not the same as shared operational understanding;
- **invisible coordination labor:** assignment can transfer execution without transferring anticipation, reminding, monitoring and repair;
- **social/authority realism:** fairness, consent, guardian power, professional authority and ability to refuse differ by relationship;
- **relationship safety:** reduced sharing, scoped revocation and emergency revocation are real lifecycle states;
- **ongoing high-conflict coordination:** some relationships remain operational despite distrust and require bounded, low-friction, auditable coordination without pretending cooperation is friendly;
- **accessibility spectrum:** necessary actors may participate through simplified/assisted modalities rather than a full LifeOS client;
- **multi-party AI privacy:** cross-participant leakage and privacy-preserving explanation are distinct future AI risks.

## Known open questions intentionally left for later work

- Exact reusable domain concepts for participant, role, responsibility, shared state, personal overlay and coordination evidence.
- Exact non-LifeOS participant experience and supported modalities.
- Exact permission/authorization model and whether specialized authorization infrastructure is ever justified.
- Exact placement of shared-expense capabilities.
- Exact boundary between structured coordination and messaging.
- Whether coordination stewardship/mental load becomes a visible product concept or only a design/evaluation property.
- Exact child/guardian semantics, which require later jurisdictional/legal review where relevant.
- Exact AI multi-party architecture.
- Exact conflict-resolution semantics for shared facts when authoritative sources and participant reports disagree.

## Decisions / constraints not to reopen casually

- Current V1 remains personal-first; this evidence work does not silently move full collaboration into V1.
- Current accepted architecture and domain documents remain authoritative over evidence documents.
- The simulation remains separate from external research so the original findings are not retrofitted to literature/competitor patterns.
- All external multi-actor research for this workstream now lives in the single `multi-actor-collaboration-research-2026-08.md` document.
- External research is evidence, not implementation specification.
- Do not select Zanzibar/OpenFGA-like authorization, organization models, AI orchestration or specialist subsystems merely because they appear as feasibility/reference evidence.
- Multi-user value must be evaluated against coordination, cognitive, privacy, accessibility and maintenance burden for every affected actor.

## Next step — separate workstream only if/when deliberately started

The evidence-acquisition phase is complete. Do **not** continue adding generic research families without a concrete gap.

If the project later chooses to act on this evidence, start a separate evidence-synthesis / Multi-Actor Readiness workstream that:

1. compares findings by recurrence, confidence, domain breadth and tension;
2. derives a small candidate set of product invariants without choosing physical architecture;
3. tests existing core concepts for dangerous single-user assumptions;
4. promotes changes into product/domain/ADR documents only through normal project governance.

## Validation

Documentation-only workstream. Final validation includes:

- work remained on the dedicated branch based on accepted `main`;
- simulation and one consolidated external research document are stored under `docs/product/`;
- product documentation index reflects the consolidated structure;
- the redundant standalone stress-research file was removed only after its useful evidence was integrated;
- no accepted ADR, architecture or V1 behavior document was modified by the evidence work;
- source corrections and research limitations are documented inside the consolidated research;
- PR #6 is the single review container for the completed work.
