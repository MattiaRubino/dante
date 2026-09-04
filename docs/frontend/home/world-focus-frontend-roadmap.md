# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / M3-3 NEXT  
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
-> pre-M0 falsification
-> M0 materialization mapping
-> M1 non-visual production materialization
-> post-M1 safety falsification
-> M2 shared visual primitive layer
-> M2 final hostile closure
-> M3-1 revisioned composition config + isolated customization draft
-> M3-2 meaningful-opportunity + adaptive candidate resolver
```

## 2. Key evidence

```text
M0 closure          6ea74f630cb35af65d58e7ae873882d6d975411e / CI 33668744509 PASS
M1 final            7369c51e7ba04f8913728a0770f700c728c3b9f9 / CI 33740710290 PASS
POST-M1 safety      ecc2128b62395f82eab9ee7ff239355b4ca81ee4 / CI 33754084001 PASS
M2 final            e3865e0cde095acae7e3022815538f35ee0706ef / CI 33790953644 PASS
M3-1 red            b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAIL
M3-1 validation     49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
M3-2 red            c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAIL
M3-2 validation     b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
```

Current M3-2 validation:

```text
74 / 74 web test files
356 / 356 web unit tests
287 modules / 797 dependencies / 0 architecture violations
Quality PASS
Production build PASS
Mobile Bundle PASS
Chromium PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

## 3. Materialization sequence

```text
M0 — Materialization Mapping / Scope Freeze              CLOSED
M1 — Core Non-Visual Production Materialization         CLOSED / VALIDATED
POST-M1 Safety Falsification                             CLOSED / PASS
M2 — Shared Visual Primitive Layer                       CLOSED / VALIDATED
M3 — Adaptive World Composition                          ACTIVE
  M3-1 Composition Configuration Foundation              CLOSED / VALIDATED
  M3-2 Adaptive Candidate Resolver                       CLOSED / VALIDATED
  M3-3 Manual Customize UX                               NEXT
  M3-4 Integrated Adaptive Composition                   BLOCKED BY M3-3
  M3 final hostile closure                               BLOCKED BY M3-4
M4 — Contextual DANTE                                    BLOCKED BY M3
M5 — Contrasting Complete Worlds                         BLOCKED BY M4
M6 — Integrated Product / Visual / A11y / Perf           BLOCKED BY M5
M7 — Pre-Backend Frontend Freeze                         BLOCKED BY M6
BACKEND                                                   AFTER M7 ONLY
```

## 4. Closed substrate before M3-3

M1 provides validated non-visual semantics/application seams. M2 provides bounded, accessible presentation and renderer vocabulary. Workspace Platform already provides the deterministic planner, finite registry, surface stack and local failure isolation.

M3-1 adds client composition configuration/revision ownership and the finite customization command transaction.

M3-2 adds the production candidate-resolution boundary without mounting anything live.

## 5. M3-1 configuration/draft model

```text
WorldFocusCompositionConfig
  schemaVersion
  revision
  worldId
  ordered entries[]

entry
  instanceId
  kind
  visibility
  pinned
  prominenceOverride
```

Commands:

```text
pin / unpin / hide / show / move / promote / restore
```

Manual UI and future DANTE proposals share these commands and the same Draft -> Review/Apply -> Config path. DANTE cannot bypass revision guards.

## 6. M3-2 meaningful opportunities

Opportunity extraction consumes only validated M1 results:

```text
Situation ready + content                -> situation
Continuity ready/partial/stale + content -> continuity
Attention ready                          -> one opportunity per primitive
Next ready + content                     -> next
Comparison ready                         -> one opportunity per primitive
Trajectory ready                         -> one opportunity per primitive
Evidence/History with any role content   -> evidence-history
empty / unavailable                      -> no opportunity
```

Sparse Worlds stay sparse. Opportunity metadata carries only composition-safe fields and is bounded to 16.

## 7. M3-2 ranking/config precedence

Finite signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No weighted AI score, confidence score or universal relevance number exists.

Deterministic bands:

```text
foreground -> lead minimum
active     -> primary minimum
ordinary   -> opportunity default
```

Config precedence:

```text
hidden > ranking
pinned > adaptive budget
configured relative order > adaptive ranking
promote -> lead presentation override only
```

Pinned user intent with no meaningful projection remains explicit unresolved intent rather than a fabricated module.

## 8. M3-3 intent — next

M3-3 must build the **manual** Customize UX over the already-validated command/draft engine.

Required product capabilities:

```text
explicit enter/exit Customize mode
clear distinction current vs draft
pin / unpin
hide / show
reorder
promote / restore
review changed state
Apply / Cancel
revision-conflict handling
keyboard-first reorder path
touch-usable controls
responsive layout
focus management / screen-reader semantics
```

Drag-and-drop may supplement these controls, but cannot be the canonical state model or only accessible interaction.

M3-3 does not mount resolved candidate modules in the normal World; that remains M3-4.

## 9. M3-4 intent

Integrate:

```text
validated application projections
-> M3-2 opportunities/resolver
+ accepted M3-1 config
-> existing planner
-> finite registry
-> CompositionHost
```

The integration must preserve sparse output, pinned user intent, local failure isolation and no fake persistence.

## 10. M4–M7

M4 resumes D2–D6 contextual DANTE. DANTE proposals reuse governed app paths and do not replace manual capability.

M5 proves contrasting complete Worlds over the same engine.

M6 performs integrated human product/visual review plus accessibility and performance pressure. Automated green does not equal human visual acceptance.

M7 freezes frontend/backend seams before real vertical integration.

After M7, real verticals may connect UI -> application -> Access/Auth/AuthZ -> API -> Domain -> PostgreSQL under backend authority.

## 11. Permanent barriers

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
AI output != fact
Proposal != Decision != effect
Evidence != Provenance
absence/unknown != false
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
renderer availability != mandatory mounting
```

## 12. Immediate continuation

> **M3-3 Manual Customize UX is NEXT but unstarted. Begin only from a fresh bounded gate. Do not start M3-4, M4 DANTE or backend work automatically.**
