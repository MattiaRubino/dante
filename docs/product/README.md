# Product Documentation Index

Use [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) for the current project state and [`../ROADMAP.md`](../ROADMAP.md) for current sequencing. This directory preserves durable V1 product definitions and earlier planning context.

## Foundation

- [`vision.md`](vision.md) — product vision
- [`scope.md`](scope.md) — early scope foundation
- [`phase-3-product-definition-review.md`](phase-3-product-definition-review.md) — Phase 3 review and completeness check
- [`v1-scope.md`](v1-scope.md) — detailed V1 scope

## Canonical domain and execution behavior

- [`v1-core-domain-glossary.md`](v1-core-domain-glossary.md) — canonical meanings of core concepts
- [`v1-goal-and-program-creation.md`](v1-goal-and-program-creation.md)
- [`v1-goal-and-program-lifecycle.md`](v1-goal-and-program-lifecycle.md)
- [`v1-scheduling-flexibility.md`](v1-scheduling-flexibility.md)
- [`v1-execution-status.md`](v1-execution-status.md) — scheduling state vs execution outcome vs confirmation/provenance
- [`v1-confirmation-and-reminders.md`](v1-confirmation-and-reminders.md)
- [`v1-calendar-contexts-and-grouped-views.md`](v1-calendar-contexts-and-grouped-views.md)
- [`v1-today-experience.md`](v1-today-experience.md)

## User context and specialist boundaries

- [`v1-onboarding-and-profile.md`](v1-onboarding-and-profile.md)
- [`v1-first-run-experience.md`](v1-first-run-experience.md)
- [`v1-user-context-and-safety.md`](v1-user-context-and-safety.md)
- [`v1-health-and-wellness-boundaries.md`](v1-health-and-wellness-boundaries.md)
- [`v1-learning-context-and-ai-boundary.md`](v1-learning-context-and-ai-boundary.md)
- [`v1-work-context-and-meeting-lifecycle.md`](v1-work-context-and-meeting-lifecycle.md)
- [`v1-global-search-and-command.md`](v1-global-search-and-command.md)
- [`v1-adaptive-intelligence-and-future-social.md`](v1-adaptive-intelligence-and-future-social.md)
- [`v1-data-history-and-privacy.md`](v1-data-history-and-privacy.md)

## Discovery / evidence

- [`feature-discovery-simulation-2026-08.md`](feature-discovery-simulation-2026-08.md) — cross-domain scenario study used to discover universal primitives such as Register, Asset/Subject, Trigger, Session, Review Queue and flexible progress methods. This is product evidence; binding implementation choices are resolved through the domain/architecture documents and ADRs.
- [`multi-actor-collaboration-discovery-simulation-2026-08.md`](multi-actor-collaboration-discovery-simulation-2026-08.md) — multi-actor discovery study combining persona-driven needs with real-life `without LifeOS → with LifeOS` simulations, stress cases and longitudinal collaboration scenarios. It is discovery evidence, not a binding collaboration architecture or implementation specification.

## Historical planning note

- [`next-steps.md`](next-steps.md) — preserved early planning note. **Do not use it as the current work queue.** Current work is recorded in [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) and workstream handoffs.

## Reading rule

If two product documents appear to overlap, use the more specific V1 document for behavior, then check accepted ADR/architecture constraints and the active workstream handoff. Do not discard older docs solely because a newer navigation layer exists; Git and the repository preserve the evolution of the product definition.
