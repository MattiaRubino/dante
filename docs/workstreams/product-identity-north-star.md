# Product Identity / North Star Workstream

**Status:** Product definition approved as the current living guideline; integration follow-up remains  
**Branch:** `docs/product-identity-north-star`  
**Base:** `feature/domain-model` at `8d761132ae446d701d68a03272bf642a86a611a2`

## Purpose

Define the current product-level answer to what LifeOS is and what principles define its identity before the Phase 4 frontend structure is rebaselined.

## Main document

- `docs/product/product-identity-and-north-star.md`

## Current interpretation

- the North Star is an Accepted Living Product Definition, not an immutable specification;
- it defines product identity, mission, broad capability boundaries and foundational principles;
- it does not define final UX, exact autonomy/proactivity behavior, notification policy, pricing, providers, release slicing, schemas or implementation mechanics;
- current accepted Domain Atlas terminology remains authoritative for kernel semantics;
- examples describe possibilities and stress cases, not mandatory modules or release commitments.

## Key accepted clarifications

- LifeOS addresses life as an interconnected system rather than centering the product on Calendar or Goals alone;
- `UNDERSTAND → DISCOVER → ORCHESTRATE → DECIDE → PLAN & COORDINATE → ACT → OBSERVE → LEARN & ADAPT` describes cooperating capabilities, not a mandatory workflow;
- Calendar, task management, Goal tracking, analytics, AI, collaboration and other product categories may all be part of LifeOS, but none individually defines it;
- whole-life Orchestration is explicit and may conclude that not everything fits or that doing less is preferable;
- Discovery is part of the direction without fixing how proactive LifeOS should be;
- `Effort != Execution != Outcome != Goal Progress` is a product-integrity rule;
- no universal Life Score, punitive streak model, universal formula for a correct life, or objective of occupying every free minute belongs to the product identity;
- LifeOS may keep rich personal context while governing its use, access and disclosure appropriately;
- external plans, professionals, tools and AI may contribute to LifeOS while source and authorship are preserved where relevant;
- a capability is not excluded merely because another product already provides it; LifeOS may provide it natively, connect to it externally, or do both when useful;
- Domain Extensions are open-ended examples rather than a predefined taxonomy;
- capability categories are guidance rather than a rigid inclusion test;
- the North Star is versionable and may evolve when evidence or product understanding changes.

## Completed

- Italian review version discussed with the user;
- user accepted it as the initial current guideline;
- repository version rewritten in English;
- North Star status changed to Accepted Living Product Definition;
- product documentation index updated accordingly.

## Remaining follow-up

1. re-check the latest `feature/domain-model` HEAD because domain work continued after this branch was created;
2. review semantic coherence against newer Domain Atlas changes if any;
3. determine whether older high-level product documents need explicit cross-links or supersession notes;
4. integrate this documentation branch through the normal repository workflow when coherent;
5. use the accepted North Star as the basis for the structural frontend rebaseline.
