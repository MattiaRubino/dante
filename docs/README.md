# Documentation Index

This directory is the durable project memory for LifeOS. It is designed so a new human developer, ChatGPT conversation, Claude session, Codex task or other agent can resume work from the repository without reconstructing decisions from chat history.

## Start here

- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current global state, active workstreams and next steps
- [`ROADMAP.md`](ROADMAP.md) — current delivery sequence and boundaries
- [`workstreams/`](workstreams/) — operational handoffs for active pieces of work

## Durable product and architecture sources

- [`product/`](product/) — product scope, V1 behavior, domain glossary and functional studies
- [`architecture/`](architecture/) — system architecture and implementation direction
- [`decisions/`](decisions/) — accepted Architecture Decision Records (ADRs)
- [`ux/`](ux/) — UX principles and accepted UX documentation

## Development process

- [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git workflow and DEV/UAT/PROD policy
- [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — mandatory documentation and AI/human handoff protocol

## Status vocabulary

Documents may use these labels:

- **Accepted** — durable decision/current baseline; do not reopen without new evidence.
- **Current** — authoritative operational state at the time of the last update.
- **In progress** — active work that may still change.
- **Planned / Ready to start** — sufficiently defined to begin but not yet implemented.
- **Study / Exploration** — useful evidence and discovery, not automatically a binding implementation decision.
- **Historical** — preserved context that is no longer the current instruction.

Git history is retained. When a newer document supersedes part of an older one, prefer explicit links/status notes over deleting prior reasoning unless removal is necessary for correctness or security.

## Source-of-truth rule

For project state, prefer repository documentation over conversation memory. For a specific workstream, the workstream handoff plus its linked accepted ADRs/product/architecture documents are authoritative.
