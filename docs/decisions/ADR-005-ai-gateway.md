# ADR-005: Replaceable AI Gateway

- Status: Accepted
- Date: 2026-08-02
- Updated: 2026-08-10

## Decision

Isolate AI interactions behind a replaceable gateway and keep all AI access subordinate to LifeOS domain services.

LifeOS may support multiple AI interaction paths:

1. mock provider for development/testing;
2. structured manual/import-export workflows;
3. paid API providers for integrated AI features;
4. external assistants connected through a provider-neutral Tool API / MCP-compatible surface when their platform allows it.

AI receives context through a Context Builder rather than direct unrestricted database access. It may request additional relevant state through tools and must return structured semantic candidates/proposals for persistent changes.

LifeOS owns persistent memory and user state. AI conversation memory is not authoritative.

## Rationale

The application must support AI-assisted creation, interpretation and recalibration without making the core product dependent on one provider, one consumer subscription or continuous high-cost model usage.

Many LifeOS operations are deterministic and should stay in normal domain services. AI is most valuable for natural-language interpretation, ambiguous cross-domain reasoning, complex planning/replanning and conversation.

The same domain/tool contracts should serve both LifeOS-integrated AI and future external assistants so provider changes do not require separate product logic.

## Consequences

- AI output follows structured schemas/semantic contracts.
- AI never writes SQL directly and never creates/modifies physical database schema.
- AI may propose new entities, relationships, memories, preferences or plan changes only within the supported LifeOS semantic model.
- The backend validates authorization, versions, duplicates, entity/relation types, constraints, consequences and confirmation policy before persistence.
- Important AI-inferred facts/relations retain provenance and lifecycle/status where relevant.
- Context is selected progressively; the entire user history is not sent to a model by default.
- Routine calculations, aggregation, conflict detection and straightforward state transitions remain deterministic where practical.
- Automatic AI usage should be event-gated/aggregated so every incoming sensor or user event does not trigger a model call.
- External assistants with write-capable tool support may submit validated proposals/actions through LifeOS APIs.
- When an external assistant is read-only, it may still generate a portable proposal that the user opens/imports into LifeOS for validation and confirmation.
- A future OpenAI, Anthropic, Google or other provider can be added without changing core client/domain workflows.

Detailed interaction with the personal data model is defined in [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md).
