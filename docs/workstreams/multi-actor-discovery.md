# Multi-Actor / Collaboration Discovery

- Status: **COMPLETE — simulation + unified deep research + QC integrated into `main` via PR #6**
- Historical work branch: `docs/multi-actor-discovery`
- Merge pull request: #6
- Merge commit: `a53ee804b57746043216c96aabb787fbb3ed116e`
- Scope: completed product discovery evidence for future multi-user, multi-actor and collaboration direction. This workstream does not change current V1 implementation boundaries or define collaboration architecture.

## Canonical source-of-truth documents now on `main`

- [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md) — completed multi-actor discovery simulation
- [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md) — single consolidated and quality-checked external Deep Research document
- [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md) — earlier cross-domain discovery study used as methodological precedent
- [`../product/v1-adaptive-intelligence-and-future-social.md`](../product/v1-adaptive-intelligence-and-future-social.md) — accepted current V1/future-social boundary
- [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md) — accepted current concept meanings
- [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md) — accepted current architecture; not superseded by this evidence

## Completed work

- Created a dedicated multi-actor discovery simulation using both persona-driven and scenario-driven lenses.
- Simulated real-life `without LifeOS → with LifeOS` behavior across social, household, work, caregiving, specialist and complex organizational contexts.
- Added actor-by-actor needs, non-LifeOS participants, privacy boundaries, stress variations, longitudinal relationship changes, negative evidence and cross-case universality classification.
- Performed a broad external Deep Research pass across CSCW/groupware, coordination theory, common ground/awareness, calendars/privacy, household/family coordination and mental load, scheduling/fairness, caregiving/healthcare, education, shared expenses, external participation, privacy-by-design, authorization feasibility and current products.
- Deepened high-risk areas: adversarial exits and technology-facilitated abuse, ongoing high-conflict collaboration, child/adolescent agency and guardian power, accessibility/older adults/low digital literacy, and AI-mediated multi-party privacy/leakage.
- Consolidated all external multi-actor research into **one** canonical research document.
- Performed semantic and bibliographic QC: removed duplicated themes, preserved genuine trade-offs, corrected source identifiers/links, strengthened source support for safety claims, and added post-separation co-parenting as the last materially distinct research family.
- Recorded a consolidated risk register, validation questions, confidence classification, negative evidence and five-layer analytical framing: shared reality, dependency, actor relationship, personal interpretation and coordination evidence.
- Updated the product Discovery / evidence index and global project status.
- Merged the completed evidence work into `main` through PR #6 on 2026-08-11.

## QC outcome

No external evidence overturns the central simulation hypothesis. The research strengthens it while preserving several real product tensions:

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
- **ongoing high-conflict coordination:** some relationships remain operational despite distrust and require bounded, low-friction, auditable coordination;
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

- Current V1 remains personal-first; this evidence does not silently move full collaboration into V1.
- Current accepted architecture and domain documents remain authoritative over evidence documents.
- The simulation remains separate from external research because they are independent evidence methods.
- All external multi-actor research for this workstream lives in the single `multi-actor-collaboration-research-2026-08.md` document.
- External research is evidence, not implementation specification.
- Do not select Zanzibar/OpenFGA-like authorization, organization models, AI orchestration or specialist subsystems merely because they appear as feasibility/reference evidence.
- Multi-user value must be evaluated against coordination, cognitive, privacy, accessibility and maintenance burden for every affected actor.

## Future work — separate workstream only if deliberately started

The evidence-acquisition phase is closed. Do **not** continue adding generic research families without a concrete gap.

If the project later chooses to act on this evidence, start a separate evidence-synthesis / Multi-Actor Readiness workstream that:

1. compares findings by recurrence, confidence, domain breadth and tension;
2. derives a small candidate set of product invariants without choosing physical architecture;
3. tests existing core concepts for dangerous single-user assumptions;
4. promotes changes into product/domain/ADR documents only through normal project governance.

## Final validation

- PR #6 merged successfully into `main` on 2026-08-11.
- Merge commit: `a53ee804b57746043216c96aabb787fbb3ed116e`.
- The simulation and consolidated research are present on `main` under `docs/product/`.
- `docs/product/README.md` indexes both evidence documents.
- The redundant standalone stress-research file is not present in the merged final structure.
- No accepted ADR, architecture or V1 behavior document was modified by the evidence work.
- No workflow runs/checks were configured for the documentation-only merge.
- This handoff is closed; `main` is authoritative for the integrated evidence.
