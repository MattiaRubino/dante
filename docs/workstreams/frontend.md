# Workstream — Frontend Prototype

- Status: **IN PROGRESS**
- Product: **DANTE**; historical `LifeOS` references belong to the same product lineage
- Branch: `prototype/frontend`
- Work type: pre-production frontend / coded UX prototype / interaction and visual validation
- Production frontend implementation: **NOT STARTED in this workstream**
- Current primary surface: **Home**
- Retained complete A2 baseline: `prototypes/frontend/home/current/home.html`
- Current modular Home work source: `prototypes/frontend/home/work/`
- Current Home contract: `docs/frontend/home/contract.md`
- Current UI registry: `docs/frontend/ui-registry.md`
- Terminology registry: `docs/frontend/terminology.md`
- Research/evidence index: `docs/frontend/research-index.md`

## Purpose

This is the shared pre-production frontend workspace. It supersedes `prototype/phase-4-today-home` as the active prototype continuation branch and allows Home, Logger and later surfaces to evolve without forcing them into one monolithic standalone HTML artifact.

This branch is not the production frontend implementation. Production framework/runtime selection and application architecture remain a later explicit engineering scope.

## Mandatory frontend documentation invariant

**This rule is permanent for this workstream and applies to every frontend change from B1 onward.**

A frontend write is not complete merely because the HTML renders. Every user-visible surface, control, interaction, state, label, visual token and removal must remain discoverable without reverse-engineering the implementation.

For every frontend change, update the applicable authorities in the same bounded write:

1. `docs/frontend/ui-registry.md` — what exists now, its stable technical ID, status and current behavior;
2. surface contract, e.g. `docs/frontend/home/contract.md` — what the surface contains, what it must not contain, states, actions, dependencies and non-regression rules;
3. `docs/frontend/terminology.md` — product terms, technical IDs, naming status, replacements and deprecated/rejected names;
4. localization resources / `docs/frontend/localization.md` — user-facing copy and locale keys when wording is introduced or changed;
5. design tokens / `docs/frontend/design-tokens.md` — semantic visual tokens when colors, spacing, radii, shadows or typography are introduced or changed;
6. `docs/frontend/change-log.md` — append-only history classified as `ADDED`, `CHANGED`, `REMOVED`, `DEPRECATED`, `RENAMED`, `BEHAVIOR_CHANGED` or `VISUAL_ONLY`;
7. the current checkpoint / QA record when the accepted artifact or behavior changes.

### Required guarantees

- Every durable UI concept gets a stable **English technical ID**; visible labels may change without changing that ID.
- Product labels are not implementation identifiers.
- New/touched user-facing copy must be represented in localization resources; inline prototype copy may remain only as a transitional fallback and must be traceable to the locale key.
- New/touched visual values must use semantic tokens rather than adding arbitrary raw colors/radii/shadows/spacing.
- Removed or superseded UI is recorded, not erased from history.
- A new chat must be able to determine current Home functionality by reading the workstream + registry + contract + current checkpoint, without inferring behavior from screenshots or 700k of HTML.
- A local fix must state what is intentionally unchanged.
- Prototype-only or mock controls must be explicitly marked as such; presence must never imply implemented backend semantics.
- Documentation and implementation must move in the same bounded scope. If they diverge, the scope is not closed.

## Frontend bootstrap order

For any new chat/agent continuing frontend work, read in this order:

1. mandatory repository bootstrap from current `main`;
2. `docs/workstreams/frontend.md`;
3. `docs/frontend/README.md`;
4. `docs/frontend/ui-registry.md`;
5. current surface contract, beginning with `docs/frontend/home/contract.md`;
6. `docs/frontend/terminology.md`;
7. `docs/frontend/localization.md`;
8. `docs/frontend/design-tokens.md`;
9. current checkpoint / QA record;
10. research/evidence index when making semantic/UX decisions;
11. implementation only after the authorities above are understood.

## Source precedence

1. current `main` Product/North Star, accepted Domain/Logical/Physical semantics and repository rules;
2. this workstream handoff and mandatory invariant;
3. frontend registry + current surface contract;
4. terminology/localization/design-token authorities;
5. current checkpoint;
6. modular work source and deterministic build output;
7. retained complete baseline/oracle;
8. migrated Phase 4 reference material when behavior/research history is material;
9. historical Git/PR evidence.

Current `main` truth outranks historical Phase 4 terminology when they conflict.

## Retained complete A2 baseline

```text
path
prototypes/frontend/home/current/home.html

size
748625 bytes

SHA-256
986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df

Git blob
fd9788212fbbd1ee40e53271cc39cedd9275b341
```

This complete file is deliberately retained as the immutable pre-B1 baseline.

## Current accepted Home build — B1 Context Rail v1

B1 is stored as a deterministic accepted override on top of the retained A2 baseline.

```text
build command
cd prototypes/frontend/home/work
python build.py

accepted output size
760281 bytes

accepted output SHA-256
a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

Accepted behavior:

- the old `Appunti` + side `Review` cards are superseded by one integrated right contextual rail;
- the rail contains `Capture` (`user -> DANTE`) and `Resolution` (`DANTE -> user`) functions;
- both remain visible together; the rejected ambiguous focus/expand interaction is not part of the accepted state;
- the rail stretches with the timeline column instead of stopping early and leaving an arbitrary empty lower block;
- timeline expansion still yields the rail's horizontal space;
- deep/complex resolution is intentionally deferred to the future overlay/sheet grammar.

## Constraints carried forward

- one persistent semantic reality, multiple projections/surfaces;
- time is primary but not sovereign;
- current situation is broader than the timeline;
- persistent UI serves recurring user needs rather than exposing ontology;
- natural language and GUI operate on the same semantic reality;
- GUI remains first-class;
- adaptive/contextual UI uses a controlled interaction grammar;
- unresolved state is separate from attention delivery;
- hidden knowledge remains inspectable/correctable when materially used;
- attention priority and action authority remain separate;
- Mobile/Web may differ in representation while preserving semantic outcomes;
- prototype nouns are not canonized merely because they appear in the current artifact.

## Historical Phase 4 handling

`prototype/phase-4-today-home` and PR #2 are historical/superseded evidence. Selected branch-only research/decision/reference material is preserved under `docs/frontend/reference/phase4/`. Product research already integrated into `main` is not duplicated and is indexed from `docs/frontend/research-index.md`.

## Immediate roadmap

1. **B1 Context Rail** — accepted, documentation/operational hardening in progress;
2. audit and register the rest of the current Home surface;
3. **B2 central stage** — define actual purpose/content of current `Worlds` / `Stats`;
4. naming pass;
5. overlay grammar and real popup/sheet/dialog cases;
6. complete Home functional review;
7. final product identity treatment / skin;
8. Home QA and final pre-production checkpoint;
9. Logger and later surfaces.

## Scope boundary

Do not silently start production frontend implementation, choose production framework/runtime, invent backend contracts from prototype convenience, alter accepted semantic models, or promote historical UI vocabulary into final Information Architecture without explicit review.
