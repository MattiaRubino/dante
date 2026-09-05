# DANTE — World Focus Research / Review Evidence Index

**Status:** CURRENT EVIDENCE MAP — M0 / M1 / POST-M1 SAFETY / M2 / M3 CLOSED — M4 ACTIVE / D2–D4 CLOSED / D5 NEXT  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

This index separates live sequencing authority, closure authority, falsification and supporting evidence. Older phase-time status prose is historical unless adopted by current checkpoint authority.

## 1. Read first

```text
world-focus-current-checkpoint.md
world-focus-frontend-roadmap.md
world-focus-handoff.md
world-focus-evidence-index.md
current-checkpoint.md
world-focus-d4-contextual-invocation-review.md
world-focus-d3-deterministic-conversation-adapter-review.md
world-focus-d2-adaptive-conversation-surface-review.md
world-focus-m3-final-hostile-closure-review.md
world-focus-m3-adaptive-composition.md
world-focus-m3-4-integrated-adaptive-composition-review.md
world-focus-dante-spatial-presence-review.md
world-focus-d1-dante-entry-review.md
```

Protected-main Domain/Logical/Physical authority outranks frontend convenience whenever semantic boundaries are questioned.

## 2. Evidence families

```text
E0–E25   Workspace, product, substrate, M0–M2 historical evidence
E26      M3-1 composition configuration foundation
E27      M3-2 adaptive candidate resolver
E28      PRE-M3-3 customization reachability safety
E29      M3-3 Manual Customize UX + hostile closure
E30      M3-4 Integrated Adaptive Composition
E31      M3 final cross-layer hostile closure
E32      M4 / D2 adaptive conversation surface closure
E33      M4 / D3 deterministic conversation adapter closure
E34      M4 / D4 contextual/deictic invocation closure
E35      M4 / D5 Insight presentation preflight — NEXT
```

Key anchors:

```text
Workspace Platform 6c441335a75bb913af8da1eda569d8094d38a539 / CI 33549465793 PASS
M3 final hostile   d9c30a3c6148469b347754eab07dc2ade9be4c52 / CI 33951509083 PASS
D2 final           7b787766be83096e82eab1ac116b2704fae5f202 / CI 33958677991 PASS
D3 final           59c70af6005ee87918db7fe152c043699726e78c / CI 33963858340 PASS
D4 final           e8ab022b9b00b958235ac7d09e757b45227a4356 / CI 33967719861 PASS
```

## E31 — M3 Final Cross-Layer Hostile Closure

```text
PRE-SCOPE 2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
HOSTILE   d9c30a3c6148469b347754eab07dc2ade9be4c52
CI        33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
```

Detailed review: `world-focus-m3-final-hostile-closure-review.md`.

## E32 — M4 / D2 Adaptive Conversation Surface — CLOSED / VALIDATED

```text
wide -> non-modal DANTE sidecar
compact/mobile -> route-owned DANTE focus
maximize/restore -> same conversation identity
```

Generic route presentation remains non-blocking; DANTE route-focus carries explicit `blocksWorkspaceInteraction=true`. Workspace host/allocator ownership was not duplicated.

```text
PRE-SCOPE 0a0a43ac06f93d986674f8521e521dcc05ea2c1e
CODE/TEST  7b787766be83096e82eab1ac116b2704fae5f202
CI         33958677991 / run #969 PASS
82 / 82 web test files
399 / 399 web unit tests
305 modules / 929 dependencies / 0 violations
```

Detailed review: `world-focus-d2-adaptive-conversation-surface-review.md`.

## E33 — M4 / D3 Deterministic Conversation Adapter — CLOSED / VALIDATED

D3 fills the D2 shell with deterministic typed mounted conversation behavior:

```text
D1 composer
-> same dante:conversation
-> typed World/generation/request correlation
-> deterministic local reader
-> finite validated answer | explanation or truthful technical state
```

Cancel, late completion, generation supersession, second-turn continuity and exact invoker focus return are executable. Mounted transcript remains frontend state, not durable DANTE Run state.

```text
PRE-SCOPE 57520cf0570bc2be875e7140d066e45ddd9080d5
CODE/TEST  59c70af6005ee87918db7fe152c043699726e78c
CI         33963858340 / run #1009 PASS
84 / 84 web test files
410 / 410 web unit tests
311 modules / 963 dependencies / 0 violations
```

Detailed review: `world-focus-d3-deterministic-conversation-adapter-review.md`.

## E34 — M4 / D4 Contextual / Deictic Invocation — CLOSED / VALIDATED

### E34.1 RED proof

```text
PRE-SCOPE c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
FIRST RED d017b17aec4b690a26781a88a17a372b0d670411
VALID RED 1cbcc27bf19c91e195dd1f0f4a5c57915facb432
RED CI    33966295853 / run #1030 EXPECTED FAILURE
```

The valid RED passed contracts/lint/typecheck/architecture/generated/Mobile and reached unit execution with exactly two intended failures: missing explicit request `contextReferences: null` and missing live Continuity contextual action. Existing D1 no-implicit-selection behavior remained green.

### E34.2 Bounded implementation

```text
Continuity -> continue
Attention  -> why
Comparison -> compare
Evidence   -> open-source
```

Only finite `WorldFocusContextReferenceSet` coordinates cross into the D3 request. Global DANTE invoke remains context-free. Arbitrary DOM/component/source payload is not serialized.

Contextual composer state is bound to World + Workspace generation. Stale-before-submit preserves the draft and fails closed. Valid follow-ups reuse the exact explicit reference set; a later generation change supersedes the contextual session and blocks stale follow-up context.

Only Evidence receives the source-opening action; Provenance, Integrity and History remain separate roles.

### E34.3 Hostile closure

```text
CODE/TEST e8ab022b9b00b958235ac7d09e757b45227a4356
CI        33967719861 / run #1038 PASS
87 / 87 web test files
422 / 422 web unit tests
317 modules / 1021 dependencies / 0 architecture violations
Frontend + World Focus contracts PASS
Lint / Typecheck / Generated / Build / Diff / Mutation PASS
Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

Real browser coverage uses `/worlds/music` Continuity at 1600 and 390. It proves seeded contextual composer, existing D3 conversation handoff, existing D2 sidecar/route focus, >=44px contextual target, no compact overflow, exact contextual invoker focus return and automated axe checks.

### E34.4 Scope compare

```text
base        c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
head        e8ab022b9b00b958235ac7d09e757b45227a4356
status      ahead
commits     9
behind      0
merge-base  == base
net paths   19 code/test/i18n
```

No Workspace reducer/allocator, AppShell, Timeline, Access/Auth, generated route tree, backend/API/DB/Alembic/provider/LLM/persistence path changed.

Detailed review: `world-focus-d4-contextual-invocation-review.md`.

## E35 — M4 / D5 Insight Presentation Preflight — NEXT

D5 has no implementation authority yet. Fresh read-only preflight must inspect the closed D4 contextual request/session boundary, closed D3 conversation/result owners, current finite World surface/rendering grammar and any existing semantic/basis/evidence owners capable of supporting an Insight without inventing truth.

Required barriers:

```text
conversation message != Insight
assistant prose != validated Insight
Insight != canonical World/Domain truth
Insight != Proposal != Decision != effect
context reference != authorization
reference exists != payload available/disclosable/fresh
```

D5 must not pull D6 Proposal/Decision/effect semantics or real backend/provider/LLM integration forward.

## 3. Current layered result

```text
L0 Higher Authorities
L1 Work-Semantic Projections — M1
L2 Evidence/Basis
L3 Coordination/Disclosure
L4 Interaction/Reference
L5 Composition — M3 CLOSED / VALIDATED
L6 Operation/Effect presentation
L7 Renderer/Specialist Extension
L8 Platform/User Policy

M2 presentation boundary CLOSED
M3 Adaptive Composition CLOSED / VALIDATED
M4 Contextual DANTE ACTIVE
D2 Adaptive Conversation Surface CLOSED / VALIDATED
D3 Deterministic Conversation Adapter CLOSED / VALIDATED
D4 Contextual/Deictic Invocation CLOSED / VALIDATED
D5 Insight Presentation NEXT / NOT STARTED
```

## 4. Current evidence gate

> **M1 — CLOSED / VALIDATED**

> **POST-M1 SAFETY — CLOSED / PASS**

> **M2 — CLOSED / VALIDATED**

> **M3 — CLOSED / VALIDATED**

> **M3 FINAL HOSTILE CLOSURE — CLOSED / PASS**

> **D2 — CLOSED / VALIDATED**

> **D3 — CLOSED / VALIDATED**

> **D4 — CLOSED / VALIDATED**

> **M4 — ACTIVE / D5 READ-ONLY PREFLIGHT NEXT**

> **M5–M7 and backend remain blocked by sequence.**

Human/manual visual acceptance remains **NOT PERFORMED**.
