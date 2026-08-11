# Multi-Actor / Collaboration Discovery

- Status: **IN PROGRESS — simulation complete; external research pending**
- Branch: `docs/multi-actor-discovery`
- Pull request: pending
- Scope: product discovery evidence for future multi-user, multi-actor and collaboration direction. This workstream does not change current V1 implementation boundaries or define collaboration architecture.

## Source-of-truth documents

- [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md) — current discovery simulation
- [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md) — earlier cross-domain discovery study used as methodological precedent
- [`../product/v1-adaptive-intelligence-and-future-social.md`](../product/v1-adaptive-intelligence-and-future-social.md) — accepted current V1/future-social boundary
- [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md) — accepted current concept meanings
- [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md) — accepted current architecture; not superseded by this study

## Last completed work

- Created a dedicated multi-actor discovery study on 2026-08-11.
- Kept persona-driven discovery as a first-class lens rather than replacing it with scenarios.
- Added detailed real-life `without LifeOS → with LifeOS` simulations across social, household, work, caregiving, specialist and complex organizational contexts.
- Added actor-by-actor needs, non-LifeOS participants, privacy boundaries, stress variations, longitudinal relationship changes, negative evidence and cross-case universality classification.
- Added the study to the `docs/product/` Discovery / evidence index.
- Deliberately excluded external competitor/academic research from the simulation to avoid biasing initial discovery.

## Current task

Validate the simulation as discovery evidence, then perform a separate external research pass that challenges and expands the findings without rewriting the simulation to match existing products.

## Next exact steps

1. Perform external research on collaboration/groupware, shared calendars, household coordination, travel/expense coordination, work hand-offs, caregiving, specialist coordination, privacy/consent and non-member participation.
2. Save that work as a separate product evidence document, provisionally `docs/product/multi-actor-collaboration-research-2026-08.md`.
3. Compare research against the simulation: confirmed findings, contradictions, missing needs, weak assumptions and additional scenarios.
4. Only after both evidence sources exist, decide whether a separate product/domain readiness review is warranted. Do not promote discovery terms directly into architecture merely because they appear in the study.

## Known open questions

- Exact reusable domain concepts for participant, role, responsibility, shared state and personal overlay remain intentionally undecided.
- Exact non-LifeOS participant experience remains intentionally undecided.
- Exact permission/authorization model remains intentionally undecided.
- Exact placement of common financial-sharing capabilities remains intentionally undecided.
- Exact boundary between structured coordination and messaging remains intentionally undecided.

## Decisions / constraints not to reopen casually

- Current V1 remains personal-first; this discovery does not silently move full collaboration into V1.
- Current accepted architecture and domain documents remain authoritative over this evidence document.
- The simulation must stay separate from later technical readiness, architecture and implementation work.
- External research must be recorded separately rather than retrofitted into the simulation as if it were originally discovered there.

## Validation

Documentation-only workstream. Validation consists of:

- branch created from current `main`;
- simulation stored under `docs/product/` beside the earlier discovery study;
- product documentation index updated;
- no accepted ADR, architecture or V1 behavior document modified by the discovery itself.
