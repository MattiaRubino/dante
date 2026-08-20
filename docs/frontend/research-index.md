# DANTE — Frontend Research / Evidence Index

**Purpose:** provide one entry point to the research and scenario evidence that should inform pre-production frontend decisions without duplicating authoritative documents already on `main`.

## 1. Current authoritative product evidence on `main`

Read these from current `main`; do not copy/fork them inside the prototype branch.

### Product identity / North Star

- `docs/product/product-identity-and-north-star.md`

Current naming note: the accepted app/product name is **DANTE**. Historical `LifeOS` naming in older evidence refers to the same lineage.

### Feature-discovery simulation

- `docs/product/feature-discovery-simulation-2026-08.md`

Use as scenario/behavior evidence for recurring personal-system needs. Do not promote old UI nouns or feature bundles automatically.

### Multi-actor discovery simulation

- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`

Use for shared-reality, authority, visibility, proposal/confirmation and collaboration stress cases.

### Multi-actor external research

- `docs/product/multi-actor-collaboration-research-2026-08.md`

This is separate external-evidence research and should remain distinct from the simulation evidence.

### Other current product specifications

Consult the relevant current files under `docs/product/` when a frontend decision touches calendar/grouped views, confirmation/reminders, data/history/privacy, adaptive intelligence, collaboration or other accepted product behavior. Current `main` specifications outrank old Phase 4 assumptions.

## 2. Frontend-specific research preserved from Phase 4

These existed only on the historical Phase 4 branch and are preserved byte-for-byte as reference evidence:

- `docs/frontend/reference/phase4/interaction-architecture-guide-v0.md`
- `docs/frontend/reference/phase4/interaction-architecture-decisions-v0.md`
- `docs/frontend/reference/phase4/frontend-architecture-requirements-v0.md`
- `docs/frontend/reference/phase4/cross-platform-interaction-rule-v0.md`

### Interaction Architecture guide

Contains the frontend research synthesis across:

- mixed-initiative interaction;
- human-AI collaboration;
- proactive assistants;
- attention/interruption management;
- situational awareness;
- prospective memory/open loops;
- personal information management;
- contextual/ambient computing;
- progressive disclosure;
- adaptive/contextual and generative UI;
- human-in-the-loop automation;
- intention/goal/planning systems;
- natural language vs direct manipulation;
- longitudinal personal systems;
- multi-actor coordination/privacy;
- contemporary product patterns and failure modes.

It also records the comparison of four architectural paradigms and the research shorthand `Stable Spine + Adaptive Contexts`. Treat that label as research shorthand, not product naming.

### Accepted-decision log

`interaction-architecture-decisions-v0.md` records which candidate principles were explicitly accepted, merged/referenced or left open during Phase 4. Use it as decision evidence, but reconcile historical wording against current `main` product/model truth.

### Frontend requirements

`frontend-architecture-requirements-v0.md` synthesizes five recurrent usage families:

- Daily / Immediate;
- Continuity;
- Capture + Retrieval;
- Disruption + Adaptation;
- Deep / Contextual.

It also identifies architecture-level capabilities such as Orientation, Time, Communication/Capture, Continuation, Action/Adaptation, Retrieval/Inspection and Resolution/Review. These are working capability labels, not automatic navigation labels.

### Cross-platform rule

`cross-platform-interaction-rule-v0.md` preserves the principle that DANTE is one semantic system expressed through multiple surfaces; Web and Mobile may differ representationally without changing semantic outcomes.

## 3. Historical timeline-behavior reference

The mature standalone temporal prototype evidence is preserved as historical regression/reference material:

- `docs/frontend/reference/phase4/frontend-master-v21.md`
- `docs/frontend/reference/phase4/today-v21.md`
- `tests/prototypes/today-v21-regression.py`

`Today v21` is a historical milestone/regression authority, **not** the current name of the Home surface.

## 4. Current visual/behavior oracle

- `docs/frontend/home/current-checkpoint.md`
- `prototypes/frontend/home/current/home.html`

The current Home artifact is approved prototype evidence. Visible labels such as `Worlds`, `Stats`, `Per te`, `Appunti` and `Review` remain working vocabulary until a deliberate naming/IA pass locks or replaces them.

## 4A. Access research / selected review evidence

On `prototype/access-system`:

- `docs/frontend/access/benchmark-2026-08-20.md`
- `docs/frontend/access/contract.md`
- `docs/frontend/access/state-model.md`
- `docs/frontend/access/current-checkpoint.md`
- `prototypes/frontend/access/archive/a3-4-approved-2026-08-20/`

The benchmark records official provider/security authorities and mature-product pattern observations used to reject the early low-fidelity Access attempts and converge on the selected A3.4 system. Provider/security documentation is authority for provider/security behavior; competitor product examples are pattern evidence only.

A3.4 is the selected pre-production review checkpoint, not production frontend code or backend-auth truth.

## 5. Evidence-use rule

When using research in design decisions:

1. state whether the point comes from current accepted product truth, Phase 4 accepted decision evidence, Phase 4 research synthesis, historical prototype behavior, or a new inference;
2. do not turn a research recommendation into an accepted product decision without explicit review;
3. do not let competitor/product examples become templates by default;
4. preserve later accepted semantic/model decisions when old research uses earlier vocabulary;
5. keep research evidence available even when its proposed UI structure is rejected.
