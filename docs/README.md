# Documentation Index

This directory is the durable project memory for LifeOS. It is designed so a new human developer, ChatGPT conversation, Claude session, Codex task or other agent can resume work from the repository without reconstructing decisions from chat history.

## Start here

- [`PROJECT-STATUS.md`](PROJECT-STATUS.md) — current global state, active workstreams and next steps
- [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — mandatory cross-session bootstrap, exact Git write gate, preservation/split-document discipline, QA and tool-failure behavior
- [`development/operating-rules.md`](development/operating-rules.md) — mandatory authority order, where to work, branch/path ownership and coherence gates
- [`ROADMAP.md`](ROADMAP.md) — current delivery sequence and boundaries
- [`workstreams/`](workstreams/) — operational handoffs for active pieces of work

## Durable product and architecture sources

- [`product/`](product/) — product scope, V1 behavior, domain glossary and functional studies
- [`architecture/`](architecture/) — system architecture and implementation direction
- [`decisions/`](decisions/) — accepted Architecture Decision Records (ADRs)
- [`ux/`](ux/) — UX principles and accepted UX documentation

## Development process

- [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — mandatory execution standard for new chats/agents; includes exact write gates, remote QA, canonical split counting, preservation rules and safe-stop behavior for Git/tool limits
- [`development/operating-rules.md`](development/operating-rules.md) — where work happens, which source wins, parallel-work rules and pre/post-merge coherence checks
- [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git workflow and DEV/UAT/PROD policy
- [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — mandatory documentation and AI/human handoff protocol

## Status vocabulary

Documents may use these labels:

- **Accepted** — durable decision/current baseline; do not reopen without new evidence.
- **Current** — authoritative operational state at the time of the last update.
- **In progress** — active work that may still change.
- **Draft / Proposed** — not yet accepted.
- **Planned / Ready to start** — sufficiently defined to begin but not yet implemented.
- **Study / Exploration** — useful evidence and discovery, not automatically a binding implementation decision.
- **Historical / Superseded** — preserved context that is no longer the current instruction.

Git history is retained. When a newer document supersedes part of an older one, prefer explicit links/status notes over deleting prior reasoning unless removal is necessary for correctness or security.

## Source-of-truth rule

For project state, prefer current `main` repository documentation over conversation memory or old branches. For a specific unmerged workstream, use its branch-local handoff and explicitly linked in-progress material together with the accepted `main` baseline.

Before copying a file from another branch, compare it with current `main`; detail alone does not make an older file authoritative.
