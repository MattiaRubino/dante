# Workstream — Frontend Prototype

- Status: **IN PROGRESS**
- Product: **DANTE**; historical `LifeOS` references belong to the same product lineage
- Branch: `prototype/frontend`
- Work type: pre-production frontend / coded UX prototype / interaction and visual validation
- Production frontend implementation: **NOT STARTED in this workstream**
- Current primary surface: **Home**
- Current exact Home oracle: `prototypes/frontend/home/current/home.html`
- Current Home checkpoint: `docs/frontend/home/current-checkpoint.md`
- Research/evidence index: `docs/frontend/research-index.md`

## Purpose

This is the shared pre-production frontend workspace. It supersedes `prototype/phase-4-today-home` as the active prototype continuation branch and allows Home, Logger and later surfaces to evolve without forcing them into one monolithic standalone HTML artifact.

This branch is not the production frontend implementation. Production framework/runtime selection and application architecture remain a later explicit engineering scope.

## Source precedence

1. current `main` Product/North Star, accepted Domain/Logical/Physical semantics and repository rules;
2. this workstream handoff;
3. `docs/frontend/README.md`;
4. `docs/frontend/research-index.md` and the authoritative sources it points to;
5. surface-specific current checkpoint, beginning with `docs/frontend/home/current-checkpoint.md`;
6. exact current surface artifact;
7. migrated Phase 4 reference material under `docs/frontend/reference/phase4/` when behavior/research history is material;
8. historical Git/PR evidence.

Current `main` truth outranks historical Phase 4 terminology when they conflict.

## Current Home oracle

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

The artifact is migrated by reusing the exact corrected Phase 4 Git blob. This migration does not authorize visual or behavioral changes.

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

`prototype/phase-4-today-home` and PR #2 become historical evidence after A1. Selected branch-only research/decision/reference material is preserved under `docs/frontend/reference/phase4/`. Product research already integrated into `main` is not duplicated and is indexed from `docs/frontend/research-index.md`.

## Immediate next scope

**A2 — mechanically modularize the current Home prototype without changing visual output or behavior.**

The immutable current oracle remains available while a maintainable `work/` source is derived. A2 requires its own exact PRE-SCOPE/write gate and validation.

After A2, Home work proceeds through: side surfaces → central stage purpose/content → naming → overlay grammar → functional review → brand/skin → QA/final pre-production checkpoint → Logger and other surfaces.

## Scope boundary

Do not silently start production frontend implementation, choose production framework/runtime, invent backend contracts from prototype convenience, alter accepted semantic models, change the immutable Home oracle during structural maintenance, or promote historical UI vocabulary into final Information Architecture without explicit review.
