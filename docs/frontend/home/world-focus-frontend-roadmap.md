# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`

Scope stop: production-grade frontend freeze before real backend/API/database/provider/LLM/effect integration.

## 1. Completed path

```text
World Focus route/shell
-> WF-G3 geometry freeze
-> B0 foundation
-> WR0–WR2 product/DANTE reverse engineering
-> B1 Orientation
-> B2 Continuity
-> Workspace Platform
-> D0 contextual DANTE spatial contract
-> D1 quiet invoke/composer
-> WS0–WS8 substrate closure
-> post-WS8 hygiene
-> pre-M0 red-first falsification
-> M0 materialization mapping / scope freeze
-> M1-1 production identity + reference ownership
-> M1-2 non-visual facets + WP/O2/O5/O8 seams
-> M1 final production falsification
-> canonical cursor closure
-> post-M1 safety red-first falsification
-> post-M1 read/O8 snapshot hardening
-> M2-1 shared display/presentation grammar + WP-02..04 renderers
-> WP-01 Continuity migration + 720/719/390 browser pressure
-> M2-2 shared qualifier/truthfulness grammar
-> M2-2 O2 Situation / O5 Next / O8 Evidence-History renderers
-> M2 final hostile falsification
-> bounded display-copy closure
-> M3-1 revisioned composition config + isolated customization draft
```

## 2. Evidence checkpoints

```text
Workspace Platform  HEAD 6c441335a75bb913af8da1eda569d8094d38a539  CI 33549465793 PASS
D1                  HEAD f17291de32e6bdced20536807b32928ec1be6aea  CI 33552437179 PASS
WS7                 HEAD ca89e733893959af7dcc40fd0b8c8ba08e056ba4  CI 33633635890 PASS
WS8                 HEAD 88db899391a3a41e23e76177d4896a657232b5eb  CI 33639741630 PASS
PRE-M0 fix          HEAD 7c9feab50c6e2a04a9a3b1e36c92958362dba704  CI 33664655614 PASS
M0 closure docs     HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e  CI 33668744509 PASS
M1-1 code           HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3  CI 33679425668 PASS
M1-2 code           HEAD 5e98e4b97639cd018badc23e35e7a523f2940875  CI 33738873773 PASS
M1 final code       HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9  CI 33740710290 PASS
POST-M1 safety fix  HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4  CI 33754084001 PASS
M2-1 validation     HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294  CI 33781753823 PASS
M2-2 validation     HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5  CI 33788370490 PASS
M2 final red        HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011  CI 33790674375 EXPECTED FAIL
M2 final code       HEAD e3865e0cde095acae7e3022815538f35ee0706ef  CI 33790953644 PASS
M3-1 red            HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f  CI 33850177297 EXPECTED FAIL
M3-1 validation     HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849  CI 33850441232 PASS
```

M2 final evidence remains 70/70 web test files, 332/332 web unit tests and 279 modules / 770 dependencies with zero architecture violations.

M3-1 validation adds 72/72 web test files, 344/344 web unit tests and 283 modules / 777 dependencies with zero architecture violations. Quality, production build, Chromium, frozen Timeline Firefox, Mobile Bundle and Frontend CI Gate all pass.

## 3. Materialization sequence

```text
M0 — Materialization Mapping / Scope Freeze             CLOSED
M1 — Core Non-Visual Production Materialization        CLOSED / VALIDATED
POST-M1 Safety Falsification                            CLOSED / PASS
M2 — Shared Visual Primitive Layer                      CLOSED / VALIDATED
M3 — Adaptive World Composition                         ACTIVE
  M3-1 Composition Configuration Foundation             CLOSED / VALIDATED
  M3-2 Adaptive Candidate Resolver                      NEXT
  M3-3 Manual Customize UX                              BLOCKED BY M3-2
  M3-4 Integrated Adaptive Composition                  BLOCKED BY M3-3
  M3 final hostile closure                              BLOCKED BY M3-4
M4 — Contextual DANTE                                   BLOCKED BY M3
M5 — Contrasting Complete Worlds                        BLOCKED BY M4
M6 — Integrated Product / Visual / A11y / Perf          BLOCKED BY M5
M7 — Pre-Backend Frontend Freeze                        BLOCKED BY M6
BACKEND                                                  AFTER M7 ONLY
```

## 4. Closed substrate before M3

M1 established open-ended World identity, bounded references, truthful basis/disclosure/effect/sync semantics, direct O2/O5/O8 seams and WP-01..04 application seams.

M2 established bounded display-safe reference binding, shared presentation grammar, WP renderers, O2/O5/O8 rendering, orthogonal truthfulness qualifiers and responsive/forced-colors behavior. Renderer availability remains distinct from live mounting.

M3 must consume these layers; it must not reinterpret them.

## 5. Existing composition engine — preserve, do not replace

Workspace Platform already provides:

```text
stable / adaptive / ephemeral stability
system-default / user / dante-proposed / application-derived origin
lead / primary / supporting prominence
wide / standard / compact footprint
12-unit deterministic packing
adaptive / ephemeral budgets
stable relative-order preservation
finite module registry
local render-failure isolation
```

`WorldFocusCompositionHost` receives an already-resolved plan and owns placement only. Ranking, canonical truth and authorization stay outside it.

M3 therefore fills missing L5 ownership rather than introducing another composition engine.

## 6. M3-1 — closed materialized result

M3-1 satisfies the configuration/revision foundation needed before adaptive ranking or Customize UI.

Client snapshot:

```text
schemaVersion
revision
worldId
ordered entries[]
```

Entry metadata is deliberately narrow:

```text
instanceId
kind
visibility: visible | hidden
pinned: boolean
prominenceOverride: lead | null
```

It contains no canonical Domain payload, AuthZ/disclosure authority, provider truth, executable renderer or arbitrary property bag.

Schema disposition:

```text
current
migration-required
unsupported
```

No fake automatic migration and no persistence are introduced.

Customization transaction:

```text
CURRENT revision N
       ↓
DRAFT(baseRevision=N)
       ↓
pin / unpin / hide / show / move / promote / restore
       ↓
Apply | Cancel
```

Apply creates revision `N+1` only when the base revision is still current. Stale Apply returns explicit `revision-conflict`; cross-World Apply fails closed; no implicit merge occurs.

## 7. Manual + DANTE product rule

M3-1 establishes the canonical customization command language for both manual UI and future DANTE proposals:

```text
manual UI [M3-3] ----\
                       -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE cannot obtain a private mutation path or skip Apply/revision conflict semantics.

Permanent rule:

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful application functions.

This keeps DANTE an intelligence/acceleration layer over the product rather than the mandatory remote control for it.

## 8. M0 L5 disposition state

```text
M0-35 stability/origin semantics                         DONE / existing
M0-36 prominence/footprint/grid planner                  DONE / existing
M0-37 production candidate resolver                      M3-2 NEXT
M0-38 Draft/Apply/Cancel + pin/hide/reorder/promote     MODEL FOUNDATION M3-1; UI M3-3
M0-39 client config revision/conflict/migration         DONE / M3-1
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

M3-1 does not falsely close the visual/manual Customize interaction surface.

## 9. M3-2 intent

M3-2 must materialize the production candidate resolver from meaningful already-authorized application projections.

Conceptual path:

```text
meaningful available projections
+ current user composition config
+ bounded product ranking inputs
        ↓
M3-2 resolver
        ↓
WorldFocusCompositionCandidate[]
        ↓
existing resolveWorldFocusCompositionPlan()
        ↓
existing CompositionHost
```

Allowed product signals may include, only where the owning projection provides them truthfully:

```text
stable/pinned user importance
material consequence
immediacy/time sensitivity
resumability
meaningful change
explicit current user intent/selection
validated basis/evidence dimensions without collapsing them
```

Hard rejects:

```text
AI relevance score alone decides page composition
universal confidence score
renderer exists -> renderer must mount
missing Output Grammar -> fabricate content
adaptive logic silently removes/reorders stable pinned user intent
candidate resolver becomes AuthZ
```

Sparse Worlds remain sparse.

## 10. M3-3 / M3-4 intent

M3-3 will materialize the actual manual Customize UX over the M3-1 command language, including accessible keyboard/touch controls for pin/hide/reorder/promote and explicit Apply/Cancel/conflict treatment. Drag/drop is an interaction option, not the canonical state model.

M3-4 will integrate resolver + user config + planner + registered renderers into the live World while retaining deterministic fallback and no fake persistence.

## 11. M4–M7 intent

M4: preserve D0/D1 and resume D2–D6 contextual DANTE. DANTE proposals reuse governed application paths; they do not bypass manual/canonical state transitions.

M5: contrasting complete Worlds over the same engine, including unknown-future World and specialist rendering only where earned.

M6: integrated visual/a11y/performance review; automated green != human visual acceptance.

M7: pre-backend frontend freeze/handoff.

After M7, real vertical integration may connect UI → application → Access/Auth/AuthZ → API → Domain → PostgreSQL according to backend authority, rather than turning frontend config into DB truth.

## 12. Permanent barriers

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
AI output != fact
Proposal != Decision != effect
provider ACK != canonical completion
absence/unknown != false
Evidence != Provenance
Authority != Visibility
timeout != semantic negative
retired reference != automatic replacement
Comparison != Decision
missing trajectory position != zero
no universal Entity/Thing/Fact/Relationship/property bag
client composition config != canonical Domain state
client revision != backend persistence revision
```

## 13. Sequencing supersession

Historical product/platform `NEXT` prose is superseded for sequencing by the current checkpoint. Semantic invariants remain authoritative. D2–D6 remain M4; backend remains blocked until M7.

## 14. Immediate continuation

> **M3-2 Adaptive Candidate Resolver is NEXT but unstarted. Begin only from a fresh bounded gate; do not start M3-3, M4 DANTE or backend integration automatically.**
