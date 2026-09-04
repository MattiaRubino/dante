# DANTE — World Focus Frontend Roadmap

**Status:** CURRENT WORKING ROADMAP — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 CUSTOMIZATION SAFETY CLOSED / PASS / M3-3 NEXT  
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
-> PRE-M3-3 customization reachability/snapshot safety hardening
```

## 2. Key evidence

```text
M0 closure          6ea74f630cb35af65d58e7ae873882d6d975411e / CI 33668744509 PASS
M1 final            7369c51e7ba04f8913728a0770f700c728c3b9f9 / CI 33740710290 PASS
POST-M1 safety      ecc2128b62395f82eab9ee7ff239355b4ca81ee4 / CI 33754084001 PASS
M2 final            e3865e0cde095acae7e3022815538f35ee0706ef / CI 33790953644 PASS
M3-1 validation     49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
M3-2 validation     b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
PRE-M3-3 red        be63d49c43c88a491439b4014668a51c8ff8ad6b / CI 33861956558 EXPECTED FAIL
PRE-M3-3 validation 7781c6751a455767595eaf159747da833117f8b2 / CI 33862549244 PASS
```

Current validation baseline:

```text
PRE-M3-3 hostile tests 5 / 5 PASS
75 / 75 web test files
362 / 362 web unit tests
288 modules / 804 dependencies / 0 architecture violations
Quality PASS
Production build PASS
Mobile Bundle PASS
Chromium PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

## 3. Materialization sequence

```text
M0 — Materialization Mapping / Scope Freeze                 CLOSED
M1 — Core Non-Visual Production Materialization            CLOSED / VALIDATED
POST-M1 Safety Falsification                                CLOSED / PASS
M2 — Shared Visual Primitive Layer                          CLOSED / VALIDATED
M3 — Adaptive World Composition                             ACTIVE
  M3-1 Composition Configuration Foundation                 CLOSED / VALIDATED
  M3-2 Adaptive Candidate Resolver                          CLOSED / VALIDATED
  PRE-M3-3 Customization Reachability Safety                CLOSED / PASS
  M3-3 Manual Customize UX                                  NEXT / NOT STARTED
  M3-4 Integrated Adaptive Composition                      BLOCKED BY M3-3
  M3 final hostile closure                                  BLOCKED BY M3-4
M4 — Contextual DANTE / D2–D6                              BLOCKED BY M3
M5 — Contrasting Complete Worlds                            BLOCKED BY M4
M6 — Integrated Product / Visual / A11y / Perf              BLOCKED BY M5
M7 — Pre-Backend Frontend Freeze                            BLOCKED BY M6
BACKEND                                                      AFTER M7 ONLY
```

## 4. Closed substrate before M3-3

M1 provides validated non-visual semantics/application seams. M2 provides bounded accessible presentation and finite renderer vocabulary. Workspace Platform provides deterministic planning, registry, surface stack and local failure isolation.

M3-1 + PRE-M3-3 now provide a customization transaction that is actually reachable from meaningful adaptive opportunities:

```text
CURRENT CONFIG
-> DRAFT
-> adopt / pin / unpin / hide / show / move / promote / restore
-> REVIEW
-> Apply | Cancel
```

`adopt` adds only composition metadata for a known opportunity. It never imports Domain payload, references, AuthZ/disclosure state, AI relevance, provider state or renderer code.

Apply is guarded by both revision and exact base snapshot identity. Same revision is not enough if the draft base no longer equals current.

M3-2 remains the candidate-resolution boundary and does not mount live content.

## 5. Current composition precedence

Meaningful opportunities remain sparse and bounded.

```text
hidden > adaptive ranking
pinned > adaptive budget
configured relative order > adaptive ranking
```

Prominence semantics are now exact:

```text
unconfigured opportunity
-> finite value bands may elevate it

configured + no lead override
-> preserve opportunity.defaultProminence

configured + lead override
-> lead

pin
-> changes stability/ownership only, not prominence
```

Pinned config with no currently meaningful projection remains `unresolvedPinned`, not a fabricated module.

## 6. M3-3 — Manual Customize UX — detailed execution roadmap

M3-3 is the next implementation phase. Its purpose is to expose the validated composition capability manually and professionally before DANTE automation is allowed to use it.

### M3-3A — Interaction/ownership preflight and write gate

Before writes:

```text
fresh branch HEAD
inspect current World page/context/workspace/surface owners
inspect current composition config/customization/opportunity/resolver contracts
inspect responsive pressure and D0/D1 surface rules
inspect current i18n and presentation primitives
choose exact M3-3 production/test paths
state CREATE / UPDATE / DELETE
state PRE-SCOPE
state explicit out-of-scope
```

Do not assume the old UI tree. Re-read it live.

The gate must decide where Customize lives without violating existing ownership:

```text
wide desktop
-> existing wide sidecar/workspace surface if semantically appropriate

compact/tablet/mobile
-> existing route-owned focus surface/overlay semantics

never
-> AppShell-owned modal hack
-> geometry rewrite
-> page-per-World fork
```

### M3-3B — Red-first product interaction contract

Write hostile/component tests before production for the high-risk behaviors:

```text
View mode != Customize mode
entering Customize does not mutate current config
meaningful unconfigured opportunity can be adopted
adopt defaults visible/unpinned/null override
no arbitrary payload/reference/reasonCode retained/displayed
pin/unpin/hide/show mutate draft only
reorder is deterministic
promote creates lead override only
restore existing returns exact base state/order
restore adopted-only removes it
Cancel returns exact base snapshot
Apply increments revision exactly once
stale revision produces conflict treatment
same revision/different base produces fail-closed treatment
```

The red run must fail because M3-3 UI/application orchestration is missing, not because tests are malformed.

### M3-3C — View/Edit separation

Nominal World view remains calm. Customize controls do not permanently turn the page into an admin/dashboard surface.

Required state distinction:

```text
VIEW
accepted current composition
no draft mutation controls

CUSTOMIZE
explicit mode indicator
draft state
pending changes
Apply / Cancel
```

Entering Customize creates one isolated draft from current config. Leaving through Cancel discards draft changes. No localStorage fake persistence.

### M3-3D — Opportunity reachability and editable list model

The Customize surface must reconcile:

```text
current configured entries
+
currently meaningful opportunities
+
unresolved pinned intent where applicable
```

A meaningful opportunity absent from config is not directly patched into config by UI code:

```text
opportunity
-> adopt command
-> config entry exists in draft
-> later pin/hide/move/promote commands may target it
```

The UI must not manufacture entries for unavailable/non-meaningful modules.

### M3-3E — Manual controls

Expose the finite semantics directly:

```text
pin / unpin
hide / show
move/reorder
promote / restore
```

Copy and icons must not imply stronger semantics than the model:

```text
pin != fact
hide != delete
promote != semantic importance truth
restore != backend reset
```

Restore is relative to draft-start base; for adopted-only entries it means removal from the draft.

### M3-3F — Reorder accessibility

Keyboard-accessible reorder is mandatory independently of drag.

Acceptable baseline:

```text
Move up / Move down or equivalent explicit reorder action
focus preserved on moved item
screen-reader announcement of new position
bounded deterministic ordering
```

If drag/drop is added:

```text
mouse parity
touch parity
keyboard parity
screen-reader equivalent
no drag-only discoverability
no custom fragile pointer math if an established accessible primitive is warranted
```

React Aria/Spectrum may be evaluated here, but only if dependency cost is justified by actual interaction complexity. No automatic dependency addition.

### M3-3G — Apply / Cancel / conflict UX

Apply calls the canonical application operation only.

UI must distinguish:

```text
clean draft
-> Apply disabled or clearly no-op by product decision

dirty valid draft
-> Apply available

revision-conflict
-> current changed since draft start
-> no implicit merge
-> provide truthful recover/reload/re-enter flow

invalid same-revision base snapshot
-> fail closed
-> do not silently apply/rebase
```

Cancel must restore accepted view without side effect.

### M3-3H — Responsive/surface behavior

Pressure widths:

```text
1856
1600
1366
1200
1024
901
900
760
721
720
719
390
```

At every boundary verify:

```text
no horizontal document overflow
controls remain reachable
Apply/Cancel remain reachable
reorder remains usable
focus is not lost across layout changes
semantics do not change merely because layout changes
```

### M3-3I — Accessibility and platform quality

Required:

```text
semantic headings/list structure
named controls
visible focus
keyboard complete path
focus return on exit
screen-reader state/position communication
touch targets
forced-colors support
reduced-motion support where motion exists
no color-only state communication
```

### M3-3J — Full validation and closure

Run targeted tests then full Frontend CI:

```text
pre-production contracts
format
lint
typecheck
architecture
generated drift
all units
production build
repository diff/mutation check
Mobile Bundle
Chromium E2E
frozen Timeline Firefox
Frontend CI Gate
```

Before closing M3-3, exact compare PRE-SCOPE -> final HEAD must contain only authorized files. Update the six live authority docs only after production is fully green.

Do not claim human visual acceptance unless a real human review was actually performed.

## 7. M3-4 — Integrated Adaptive Composition

Only after M3-3 closes, integrate the live path:

```text
validated application projections
-> meaningful opportunities
+ accepted composition config
+ finite value signals
-> M3-2 candidate resolver
-> existing planner
-> finite registry
-> CompositionHost
```

M3-4 must prove:

```text
sparse remains sparse
hidden remains hidden
pin survives adaptive budget
configured order remains user-owned
configured supporting stays supporting unless promoted
unresolved pin does not create fake content
unknown future Worlds remain viable
renderer failure remains local
no fake persistence
```

M3-4 is where normal World composition becomes adaptive. M3-3 must not pull this forward.

## 8. M3 final hostile closure

After M3-4, attack the combined M3 layer with adversarial cases rather than adding new features. Pressure likely includes conflicting config, stale signals, sparse worlds, many candidates, adopted/hidden/pinned combinations, unknown future kinds, responsive composition and failure isolation.

## 9. M4–M7

M4 resumes D2–D6 contextual DANTE. DANTE proposals reuse governed app paths and do not replace manual capability.

M5 proves contrasting complete Worlds over the same engine rather than page-specific forks.

M6 performs integrated product/visual review plus accessibility/performance pressure. Automated green is not human visual acceptance.

M7 freezes frontend/backend seams before real vertical integration.

After M7, real verticals may connect:

```text
UI -> application -> Access/Auth/AuthZ -> API -> Domain -> PostgreSQL
```

under backend authority.

## 10. Permanent barriers

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
adopt != semantic truth/AuthZ/persistence
```

## 11. Immediate continuation

> **M3-3 Manual Customize UX is NEXT and not started. Start with a fresh read-only preflight and bounded write gate. Do not start M3-4, M4/DANTE or backend work automatically.**
