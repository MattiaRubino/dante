# Product Documentation Index

Use [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) for the current project state and [`../ROADMAP.md`](../ROADMAP.md) for current sequencing. This directory preserves durable V1 product definitions and earlier planning context.

For current **Domain Atlas / kernel terminology**, use [`../domain/README.md`](../domain/README.md) and [`../domain/language-map.md`](../domain/language-map.md). Product documents in this directory remain authoritative for accepted V1 product behavior where they have not been explicitly superseded, but older product terminology does not override a later accepted Domain Atlas definition.

## Foundation

- [`vision.md`](vision.md) — product vision
- [`scope.md`](scope.md) — early scope foundation
- [`phase-3-product-definition-review.md`](phase-3-product-definition-review.md) — Phase 3 review and completeness check
- [`v1-scope.md`](v1-scope.md) — detailed V1 scope

## V1 product concepts and execution behavior

- [`v1-core-domain-glossary.md`](v1-core-domain-glossary.md) — preserved V1 product glossary; use the Domain Atlas / Language Map for current kernel terminology where later reviews differ
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

- [`feature-discovery-simulation-2026-08.md`](feature-discovery-simulation-2026-08.md) — cross-domain scenario study used to discover reusable concepts such as Register, Asset/Subject, Trigger, Session, Review Queue and flexible progress methods. This is product evidence; binding implementation choices are resolved through domain/architecture documents and ADRs.
- [`multi-actor-collaboration-discovery-simulation-2026-08.md`](multi-actor-collaboration-discovery-simulation-2026-08.md) — multi-actor discovery study combining persona-driven needs with real-life `without LifeOS → with LifeOS` simulations, stress cases and longitudinal collaboration scenarios. It is discovery evidence, not a binding collaboration architecture or implementation specification.
- [`multi-actor-collaboration-research-2026-08.md`](multi-actor-collaboration-research-2026-08.md) — consolidated and quality-checked external research spanning foundational CSCW/groupware, coordination/common-ground theory, calendar/privacy, family and mental load, work/shift fairness, caregiving/healthcare, education, shared expenses, external participants, privacy-by-design, authorization evidence, adversarial and high-conflict relationships, minors/guardian power, accessibility/low digital literacy and multi-party AI privacy. It includes source audit, contradictions/trade-offs, risk register, confidence classification and negative evidence; it remains product evidence rather than binding architecture.

## Historical planning note

- [`next-steps.md`](next-steps.md) — preserved early planning note. **Do not use it as the current work queue.** Current work is recorded in [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) and workstream handoffs.

## Reading rule

When product documents overlap, use the more specific accepted V1 document for product behavior, then check accepted ADR/architecture constraints and the active workstream handoff. When terminology itself conflicts with an accepted Domain Atlas concept, the Domain Atlas concept specification and [`../domain/language-map.md`](../domain/language-map.md) take precedence. Preserve older documents and Git history rather than silently rewriting their historical context.