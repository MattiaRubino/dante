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

Contains the frontend research synthesis across mixed-initiative interaction, human-AI collaboration, proactive assistants, attention/interruption management, situational awareness, prospective memory/open loops, personal information management, contextual/ambient computing, progressive disclosure, adaptive/contextual and generative UI, human-in-the-loop automation, intention/goal/planning systems, natural language vs direct manipulation, longitudinal personal systems, multi-actor coordination/privacy and contemporary product patterns/failure modes.

It also records the comparison of four architectural paradigms and the research shorthand `Stable Spine + Adaptive Contexts`. Treat that label as research shorthand, not product naming.

### Accepted-decision log

`interaction-architecture-decisions-v0.md` records which candidate principles were explicitly accepted, merged/referenced or left open during Phase 4. Use it as decision evidence, but reconcile historical wording against current `main` product/model truth.

### Frontend requirements

`frontend-architecture-requirements-v0.md` synthesizes five recurrent usage families: Daily / Immediate, Continuity, Capture + Retrieval, Disruption + Adaptation and Deep / Contextual. It also identifies architecture-level capabilities such as Orientation, Time, Communication/Capture, Continuation, Action/Adaptation, Retrieval/Inspection and Resolution/Review. These are working capability labels, not automatic navigation labels.

### Cross-platform rule

`cross-platform-interaction-rule-v0.md` preserves the principle that DANTE is one semantic system expressed through multiple surfaces; Web and Mobile may differ representationally without changing semantic outcomes.

## 3. Historical timeline-behavior reference

- `docs/frontend/reference/phase4/frontend-master-v21.md`
- `docs/frontend/reference/phase4/today-v21.md`
- `tests/prototypes/today-v21-regression.py`

`Today v21` is a historical milestone/regression authority, **not** the current name of the Home surface.

## 4. Current Home visual/behavior oracle

- `docs/frontend/home/current-checkpoint.md`
- `prototypes/frontend/home/current/home.html`

The current Home artifact is approved prototype evidence. Visible labels such as `Worlds`, `Stats`, `Per te`, `Appunti` and `Review` remain working vocabulary until a deliberate naming/IA pass locks or replaces them.

## 4A. Access desktop research / selected evidence

On `prototype/access-system`:

- `docs/frontend/access/benchmark-2026-08-20.md`
- `docs/frontend/access/contract.md`
- `docs/frontend/access/state-model.md`
- `docs/frontend/access/current-checkpoint.md`
- `prototypes/frontend/access/archive/a3-4-approved-2026-08-20/`

The benchmark records official provider/security authorities and mature-product pattern observations used to converge on the selected A3.4 desktop system. Provider/security documentation is authority for provider/security behavior; competitor product examples are pattern evidence only.

## 4B. Access Mobile / PRG-0 research and assurance evidence

Current mobile/cross-platform authority set:

- `docs/frontend/access/mobile-ui-registry.md`
- `docs/frontend/access/mobile-technical-contract.md`
- `docs/frontend/access/mobile-research-matrix.md`
- `docs/frontend/access/mobile-production-readiness.md`
- `docs/frontend/access/mobile-qa.md`
- `prototypes/frontend/access/archive/mobile-m1-2-approved-2026-08-20/`

The mobile research matrix distinguishes platform/standards authority from mature-product pattern evidence. PRG-0 adds explicit assurance targets and threat/account/session consequences so later backend/native implementation can execute against known requirements rather than reverse-engineering them from screens.

Primary authority families used by PRG-0 include:

- IETF RFC 8252 and RFC 9700;
- OWASP MASVS v2 / MASTG / MAS Testing Profiles;
- OWASP ASVS 5.0.0;
- NIST SP 800-63B;
- Android Credential Manager / Identity / App Links / insets / back / Play Integrity / Network Security Configuration;
- Apple Authentication Services / AutoFill content types / Universal Links / LocalAuthentication / App Attest / ATS.

Important current-standard note: MASVS v2 no longer defines the old formal L1/L2 verification levels; testing depth is expressed through MAS Testing Profiles. DANTE therefore targets relevant MASVS controls plus L2-profile testing where applicable instead of claiming a nonexistent modern `MASVS L2` certification.

Access PRG-0 is a **production-ready specification**, not proof that the yet-unimplemented native app/backend has passed those standards. Real MAS/ASVS/native verification remains a release gate.

## 5. Evidence-use rule

When using research in design decisions:

1. state whether the point comes from current accepted product truth, Phase 4 accepted decision evidence, Phase 4 research synthesis, historical prototype behavior, standards/platform authority or a new inference;
2. do not turn a research recommendation into an accepted product decision without explicit review;
3. do not let competitor/product examples become templates by default;
4. preserve later accepted semantic/model decisions when old research uses earlier vocabulary;
5. keep research evidence available even when its proposed UI structure is rejected;
6. do not label a prototype as standards-compliant when the relevant requirement can only be verified against production/native/backend implementation.
