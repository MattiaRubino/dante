# DANTE — Frontend Prototype Workspace

This directory documents the pre-production frontend workstream on `prototype/frontend`.

It is used to validate product surfaces, interaction behavior, information hierarchy, naming, overlay grammar, visual language, responsive/cross-platform behavior and coded UX prototypes before production frontend implementation.

It is not the production application codebase.

## Current starting point

Primary surface: **Home**.

- workstream: `docs/workstreams/frontend.md`
- research/evidence index: `docs/frontend/research-index.md`
- current Home checkpoint: `docs/frontend/home/current-checkpoint.md`
- exact complete Home oracle: `prototypes/frontend/home/current/home.html`
- modular Home work source: `prototypes/frontend/home/work/`

Oracle identity:

```text
size     748625 bytes
SHA-256  986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob fd9788212fbbd1ee40e53271cc39cedd9275b341
```

## A2 modularization

The complete standalone oracle is deliberately retained.

`prototypes/frontend/home/work/` is the maintainable copy-on-write source used for subsequent Home prototype work. Untouched CSS/JS/template modules remain exact pointers to the immutable oracle; a module is materialized only when it needs editing.

Its deterministic `build.py` reconstructs the standalone oracle byte-for-byte before any later visual/behavioral change is introduced.

Current A2 build result:

```text
generated size     748625 bytes
generated SHA-256  986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
oracle match       PASS
```

This separation means future prototype changes can be isolated to named modules while still producing a single standalone HTML for user review and checkpointing, without duplicating the whole prototype across dozens of files.

`docs/frontend/reference/phase4/` preserves useful branch-only Phase 4 research, decisions and behavior references. Historical wording there is evidence from that phase and does not override newer accepted `main` truth.
