# ADR-005: Replaceable AI Gateway

- Status: **Accepted / current with Logical-model qualification**
- Date: 2026-08-02
- Updated: 2026-08-17

## Decision

Isolate AI interactions behind a replaceable/provider-neutral gateway and keep all AI access subordinate to LifeOS domain/governance services.

LifeOS may support multiple AI interaction paths:

1. mock provider for development/testing;
2. structured manual/import-export workflows;
3. paid API providers for integrated AI features;
4. external assistants connected through provider-neutral tool/action adapters when supported.

AI receives context through a bounded Context Builder rather than unrestricted database access. It may request additional relevant state through tools and must return structured proposals/candidates or governed-effect requests for persistent consequence.

LifeOS owns persistent canonical state and material history. AI conversation memory is not authoritative.

## Rationale

LifeOS needs AI-assisted interpretation, planning/replanning and explanation without making the core product dependent on one provider, one subscription model or unbounded model usage.

Many operations are deterministic and should remain normal services. AI is most valuable for ambiguity, natural-language interpretation, explanation and cross-domain reasoning.

Provider-neutral internal contracts allow LifeOS-integrated AI and future external assistants to share governance/validation rules while remaining replaceable at the protocol/provider boundary.

## Current consequences

- AI output uses structured bounded contracts.
- AI never writes SQL directly and never invents/modifies physical schema.
- AI uncertainty remains proposal/candidate/source-backed unresolved state rather than silently becoming generic canonical property/relation truth.
- Persistent effect must pass applicable domain validation, authorization/governance, expected-state/conflict checks, consequence rules and confirmation policy.
- Important AI-derived state retains provenance/material basis where required.
- Context is selected progressively; the entire user history is not sent by default.
- Routine calculations, aggregation, deterministic constraints and straightforward state transitions remain deterministic where appropriate.
- Automatic AI usage should be event-gated/aggregated where useful rather than firing on every low-level input.
- External assistants may submit governed proposals/actions only through LifeOS-controlled contracts.
- Provider protocols such as MCP/A2A/future tool protocols are adapters, not LifeOS ontology.

## Logical-model qualification

The closed Logical Model supersedes older generic semantic-candidate assumptions.

AI may not use a universal Entity/Relationship/property meta-model as canonical fallback. When meaning cannot be established precisely, the correct state is unresolved/candidate/source-backed rather than fabricated generic truth.

For consequential operations, a UI action, HTTP route or external tool action string is not itself the canonical semantic operation. Later API/runtime design must preserve the governed operation/effect contract (`WL-H02`) and related expected-state, provider-state, freshness, provenance and disclosure hardenings.

## Context categories to preserve

Later AI/runtime work must keep distinct:

- canonical state;
- material history;
- retrieved context;
- derived context;
- live external context;
- candidate/unresolved state;
- transient LLM working context.

The exact runtime/cache/retrieval/tool implementation is deferred to later Pre-Physical/Physical/backend work.
