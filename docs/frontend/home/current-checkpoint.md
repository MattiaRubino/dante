# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct current state from older phase labels or chat summaries.

## 1. Branch workstreams

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

## 2. Live World Focus state

```text
WF0 route/shell                          FROZEN / USER AUTHORIZED
WF-G3 geometry                          LOCKED / USER AUTHORIZED
WF-V4 visual treatment                  CANDIDATE
B0 foundation                           ENGINEERING CLOSED
WR0–WR2                                 CLOSED
B1 Orientation                          CLOSED FOR SEQUENCING
B2 Continuity / Resume                  IMPLEMENTED / AUTOMATED PASS
Workspace Platform                      ENGINEERING CLOSED
D0 contextual DANTE spatial contract    ACCEPTED
D1 quiet invoke + compact composer       CLOSED FOR SEQUENCING
WS0–WS8                                 CLOSED
POST-WS8 HYGIENE                        CLOSED / APPLIED
PRE-M0 FALSIFICATION                    CLOSED / PASS
M0 Materialization Mapping              CLOSED
M1 Core Non-Visual Materialization      CLOSED / VALIDATED
M1-1 identity/reference ownership       CLOSED / VALIDATED
M1-2 facets + WP/O2/O5/O8 seams         CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION            CLOSED / PASS
M2 Shared Visual Primitive Layer        CLOSED / VALIDATED
M2-1 shared presentation + L1 renderers CLOSED / VALIDATED
M2-2 truthfulness + direct output        CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver         NEXT
M4–M7                                   BLOCKED BY SEQUENCE
D2–D6                                   DEFERRED TO M4
BACKEND                                 BLOCKED UNTIL M7
assistant manual visual review          NOT PERFORMED
```

## 3. Current validated evidence

```text
M0 docs closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 production identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 non-visual production materialization
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
9 / 9 hostile tests PASS; 56 / 56 web test files; 301 / 301 web unit tests

M2-1 shared visual primitive validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS
61 / 61 web test files; 312 / 312 web unit tests
262 modules / 684 dependencies / 0 architecture violations
Chromium pressure at 720 / 719 / 390 PASS
frozen Timeline Firefox PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS

M2 final hostile falsification — red discovery
HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011
CI   33790674375 EXPECTED FAILURE
hostile tests 4 / 5 PASS; web units 331 PASS / 1 FAIL
sole finding: unbounded display-binding label/supporting copy

M2 final code closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
hostile tests 5 / 5 PASS; web test files 70 / 70; web unit tests 332 / 332
279 modules / 770 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS

M3-1 red-first owner proof
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
frontend pre-production contracts PASS; Quality failed from unresolved M3-1 owner modules

M3-1 composition configuration foundation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

## 4. Closed M1/M2 substrate

M1 owns production-grade non-visual semantics and safe application seams for open-ended World identity, bounded references, freshness/validity/coverage/material state, Evidence/Provenance/Integrity, disclosure, effect/revalidation, sync/offline states, O2/O5/O8 and WP-01..04.

M2 owns presentation only: bounded display-safe bindings, shared semantic presentation grammar, WP renderers, O2/O5/O8 renderers, truthfulness qualifiers, responsive/forced-colors behavior and the real Continuity vertical. Renderer availability does not imply live mounting.

Permanent non-collapses remain in force:

```text
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend AuthZ
offline != source absent
timeout != semantic negative
partial-real != failure
reversed != compensated
Comparison != Decision
missing trajectory position != zero
AI output != accepted fact
```

## 5. M3-1 validated result

M3-1 materializes client-side composition configuration ownership without persistence or ranking:

```text
WorldFocusCompositionConfig
  schemaVersion
  revision
  worldId
  ordered entries[]

entry
  instanceId
  kind
  visibility: visible | hidden
  pinned: boolean
  prominenceOverride: lead | null
```

The constructor reconstructs allowed fields only. It does not retain canonical Domain payload, AuthZ/disclosure authority, provider truth, executable renderer code or generic property bags.

Version disposition is explicit:

```text
current
migration-required
unsupported
```

Customization uses an isolated revision-bound draft:

```text
CURRENT CONFIG
  ↓
DRAFT(baseRevision)
  ↓
pin / unpin / hide / show / move / promote / restore
  ↓
Apply OR Cancel
```

Apply is the only operation that produces revision `N+1`. A stale base returns `revision-conflict`; cross-World Apply fails closed. Cancel returns the base snapshot with no committed side effect.

### Manual + DANTE rule

Manual UI and later DANTE proposals must use the same finite command language:

```text
manual ----------\
                  -> composition draft -> review/apply -> config
DANTE proposal --/
```

`dante-proposed` commands cannot bypass Draft/Apply/revision checking. This is a permanent product constraint: canonical app capabilities must remain usable through a manual/non-AI path where they are meaningful product functions. DANTE accelerates/proposes; it does not become a hidden mutation authority.

## 6. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-m2-shared-visual-primitives.md
4. world-focus-post-m1-safety-falsification-review.md
5. world-focus-m1-core-nonvisual-materialization-review.md
6. world-focus-m1-next-subblock.md
7. world-focus-m0-materialization-mapping.md
8. world-focus-contract-sequencing-supersession.md
9. world-focus-frontend-roadmap.md
10. world-focus-handoff.md
11. world-focus-evidence-index.md
12. world-focus-substrate-closure-plan.md
13. product/platform/structure/geometry contracts as needed
```

## 7. Current gate — M3-2 next, not started

M3 is **ACTIVE**. M3-1 is **CLOSED / VALIDATED**. The next bounded block is M3-2 Adaptive Candidate Resolver.

M3-2 must consume meaningful already-authorized application projections plus current user composition configuration and produce bounded `WorldFocusCompositionCandidate[]` for the existing planner.

It must preserve:

```text
stable/pinned user intent cannot be silently overridden
sparse World remains sparse
renderer availability != mandatory mounting
no universal confidence score
AI relevance score alone cannot decide composition
candidate resolver != AuthZ
ranking != semantic truth
```

M3-2 is not started by this checkpoint and requires a fresh explicit write gate.

## 8. Explicit M3-1 stop lines

```text
NO candidate ranking/resolver yet
NO Customize UI / drag-drop yet
NO localStorage fake persistence
NO durable persistence/cross-device sync
NO new live O2/O5/O8 or WP-02..04 modules
NO DANTE runtime changes
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
```

## 9. Backend stop line

```text
frontend view model != backend DTO != Domain model != persistence row
NO World DB/Alembic
NO real business API merely for frontend completeness
NO real AuthZ/provider runtime
NO real LLM routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

## 10. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before every new write scope;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not modify Access/Auth, frozen Timeline or AppShell as collateral work;
- generated route tree is never manually edited;
- fix CI root causes rather than weaken tests;
- human visual review is recorded only when actually performed.
