# Documentation Index

This directory is the durable project memory for LifeOS. It is designed so a new human developer, ChatGPT conversation, Claude session, Codex task or other agent can resume work from the repository without reconstructing decisions from chat history.

## Start here

Read in this order for a new execution session:

1. [`../README.md`](../README.md) — repository entry point and current high-level direction;
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current global state, active workstreams and next steps;
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — mandatory cross-session bootstrap, exact Git write gate, preservation/split-document discipline, QA and tool-failure behavior;
4. [`development/operating-rules.md`](development/operating-rules.md) — authority order, where to work, branch/path ownership and coherence gates;
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — documentation/handoff protocol;
6. [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git workflow and environment policy;
7. the active [`workstreams/`](workstreams/) handoff;
8. the current product/domain/logical/architecture/ADR sources linked by that handoff.

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical: PASS WITH HARDENING / REMOTE QA PASS
WD-03: PASS
WD-05: PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

The active backend/architecture preparation handoff is [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md). It contains the unified pre-Physical roadmap, exact workstream boundaries, mandatory downstream `WL-H01..WL-H12` constraints, future requirement areas and technology-benchmark posture.

## Current semantic/model sources

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — **Accepted** current living definition of LifeOS product identity and North Star.
- [`domain/README.md`](domain/README.md) — accepted Core Domain Model / Domain Atlas entry point.
- [`domain/language-map.md`](domain/language-map.md) — accepted current Domain language/semantic map.
- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md) — integrated Whole Logical Model.
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md) — canonical Logical Model closure record.
- [`logical-model/decision-and-assumption-register-v1-part-9.md`](logical-model/decision-and-assumption-register-v1-part-9.md) — final Whole-Logical decisions, hardenings, assumptions and deferred Physical/runtime obligations.

Older product terminology does not override later accepted Domain Atlas semantics. Older architecture documents/ADRs remain evidence but may be partially qualified or superseded by later Domain/Logical decisions; the active Pre-Physical Coherence workstream is responsible for making those relationships explicit before Physical Model authorization.

## Durable product and architecture sources

- [`product/`](product/) — product scope, V1 behavior, accepted North Star and discovery evidence.
- [`domain/`](domain/) — accepted Domain Atlas and validation/checkpoint corpus.
- [`logical-model/`](logical-model/) — accepted Logical Model, representation framework, validations, benchmarks and closure records.
- [`architecture/`](architecture/) — system/technical architecture material; some pre-Domain documents are under current supersession review and must be interpreted through later Domain/Logical authority.
- [`decisions/`](decisions/) — Architecture Decision Records. Accepted historical ADR status does not automatically mean every older detail remains unqualified after later accepted decisions; explicit supersession/qualification is being hardened in the current workstream.
- [`ux/`](ux/) and [`phase-4/`](phase-4/) — UX principles, prototype documentation and Phase 4 evidence.

## Workstreams

- [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) — **active backend/architecture preparation workstream**.
- [`workstreams/today-home.md`](workstreams/today-home.md) — active Phase 4 Home/Today UX workstream.
- [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md) — preserved handoff that is currently stale/blocked pending Pre-Physical cleanup and later Physical authorization; do not execute its old Domain/persistence instructions as current truth.
- completed Domain/Logical workstream documents remain historical/canonical evidence for their closed stages.

## Development process

- [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — mandatory execution standard for new chats/agents; includes exact write gates, remote QA, canonical split counting, preservation rules and safe-stop behavior for Git/tool limits.
- [`development/operating-rules.md`](development/operating-rules.md) — where work happens, which source wins, parallel-work rules and pre/post-merge coherence checks.
- [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git workflow and DEV/UAT/PROD policy.
- [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — mandatory documentation and AI/human handoff protocol.

## Status vocabulary

Documents may use these labels:

- **Accepted** — durable decision/current baseline; do not reopen without new evidence.
- **Current** — authoritative operational state at the time of the last update.
- **In progress** — active work that may still change.
- **Draft / Proposed** — not yet accepted.
- **Planned / Ready to start** — sufficiently defined to begin but not yet implemented.
- **Study / Exploration** — useful evidence and discovery, not automatically a binding implementation decision.
- **Historical / Superseded** — preserved context that is no longer the current instruction.
- **Partially superseded / Qualified** — portions remain useful/accepted, but later sources constrain or replace specific claims.

Git history is retained. When a newer document supersedes part of an older one, prefer explicit links/status notes over deleting prior reasoning unless removal is necessary for correctness or security.

## Source-of-truth rule

For integrated project state, prefer current `main` repository documentation over conversation memory or old branches. For a specific unmerged workstream, use its branch-local handoff and explicitly linked in-progress material together with the accepted `main` baseline.

A detailed historical file does not beat a newer accepted semantic decision merely because it contains more text. Before copying a file from another branch, compare it with current `main` and preserve the newest accepted semantics.