# Multi-Actor / Collaboration Discovery

- Status: **IN PROGRESS — simulation and deep external research complete; synthesis/readiness pending**
- Branch: `docs/multi-actor-discovery`
- Pull request: #6
- Scope: product discovery evidence for future multi-user, multi-actor and collaboration direction. This workstream does not change current V1 implementation boundaries or define collaboration architecture.

## Source-of-truth documents

- [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md) — completed multi-actor discovery simulation
- [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md) — completed broad external deep-research pass
- [`../product/multi-actor-collaboration-research-stress-domains-2026-08.md`](../product/multi-actor-collaboration-research-stress-domains-2026-08.md) — targeted stress-domain research on adversarial exits, minors, accessibility/low digital literacy and AI multi-party privacy
- [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md) — earlier cross-domain discovery study used as methodological precedent
- [`../product/v1-adaptive-intelligence-and-future-social.md`](../product/v1-adaptive-intelligence-and-future-social.md) — accepted current V1/future-social boundary
- [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md) — accepted current concept meanings
- [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md) — accepted current architecture; not superseded by this study

## Last completed work

- Created a dedicated multi-actor discovery simulation on 2026-08-11.
- Kept persona-driven discovery as a first-class lens rather than replacing it with scenarios.
- Added detailed real-life `without LifeOS → with LifeOS` simulations across social, household, work, caregiving, specialist and complex organizational contexts.
- Added actor-by-actor needs, non-LifeOS participants, privacy boundaries, stress variations, longitudinal relationship changes, negative evidence and cross-case universality classification.
- Performed a broad independent external research pass across foundational CSCW/groupware, coordination theory, common ground/awareness, shared calendars, household/family coordination and mental load, shift scheduling/fairness, caregiving/healthcare, education, shared expenses, external participants, GDPR/privacy-by-design, authorization patterns and current products.
- Compared the broad research against the simulation and recorded strongly confirmed findings, qualifications, missing needs, risk register, confidence levels and a five-layer research framing: shared reality, dependency, actor relationship, personal interpretation and coordination evidence.
- Performed four additional stress-domain research passes covering adversarial relationship exits and emergency revocation, children/adolescent agency and guardian power, accessibility/older adults/low digital literacy, and AI-mediated multi-party privacy/leakage.
- Added all evidence documents to the `docs/product/` Discovery / evidence index.
- Kept simulation, external research and accepted V1/architecture documents separate.
- Draft PR #6 remains the review container for this workstream.

## Current task

Review simulation + broad deep research + stress-domain research together and decide whether the evidence base is sufficient to begin a separate synthesis / multi-actor readiness pass. Do not promote research vocabulary directly into the domain model before that synthesis.

## Next exact steps

1. Perform an evidence synthesis that compares all multi-actor findings by recurrence, confidence, domain breadth and contradiction.
2. Produce a compact candidate set of product invariants and unresolved design tensions without yet choosing physical architecture.
3. Run a separate Multi-Actor Readiness Pass against existing core concepts only if the synthesis supports it.
4. Keep architecture/authorization implementation decisions separate and ADR-driven when/if they later become necessary.

## Major research additions beyond the simulation

External evidence strengthened four areas that the simulation underweighted:

- **coordination-cost fairness:** a feature can benefit the organizer while shifting maintenance work onto other participants;
- **common ground:** message delivery is not the same as shared operational understanding;
- **invisible coordination labor:** assignment can transfer execution without transferring anticipation, reminding, monitoring and repair work;
- **social/authority realism:** fairness, consent, guardian power, professional authority and the ability to refuse differ by relationship.

Targeted stress research further added:

- emergency/global review and revocation for unsafe relationship exits;
- evolving child/adolescent autonomy rather than one static parental-control assumption;
- modality degradation and assisted participation for low-digital-literacy/accessibility cases;
- cross-participant AI leakage and privacy-preserving explanation as first-order multi-party AI risks.

## Known open questions

- Exact reusable domain concepts for participant, role, responsibility, shared state, personal overlay and coordination evidence remain intentionally undecided.
- Exact non-LifeOS participant experience remains intentionally undecided.
- Exact permission/authorization model remains intentionally undecided.
- Exact placement of common financial-sharing capabilities remains intentionally undecided.
- Exact boundary between structured coordination and messaging remains intentionally undecided.
- Whether coordination stewardship / mental load becomes a visible product concept or only a design/evaluation property remains undecided.
- Exact child/guardian semantics require later jurisdictional/legal review where relevant.
- Exact AI multi-party architecture (single orchestrator, isolated user agents, deterministic abstractions or another design) remains intentionally undecided.

## Decisions / constraints not to reopen casually

- Current V1 remains personal-first; this discovery/research does not silently move full collaboration into V1.
- Current accepted architecture and domain documents remain authoritative over evidence documents.
- The simulation remains separate from external research so the original findings are not retrofitted to competitor/literature patterns.
- External research is evidence, not a direct implementation specification.
- Do not select Zanzibar/OpenFGA-like authorization, organization models, AI orchestration or specialist subsystem designs merely because they appear as feasibility/reference evidence.
- Multi-user product value must be evaluated against the coordination, cognitive, privacy and maintenance burden it creates for every actor, not only feature completeness.

## Validation

Documentation-only workstream. Validation consists of:

- branch created from current `main`;
- simulation and research stored under `docs/product/` beside the earlier discovery study;
- product documentation index updated;
- no accepted ADR, architecture or V1 behavior document modified by the evidence work;
- draft PR #6 open against `main`;
- research sources separated from binding project decisions and recorded inside the research documents.
