# DANTE — World Focus WS0 Substrate Inventory

**Status:** HISTORICAL WS0 BASELINE — CLOSED / SEQUENCING SUPERSEDED  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`  
**Baseline branch HEAD before WS0 documentation:** `cee9a50f2c0abc52bb1c10a9250ee1527b0fc16d`

> **Authority note (2026-09-02):** this file preserves the WS0 baseline exactly as it existed before WS1–WS5. Any `WS1 NEXT`, `WS1–WS6 pressure`, or later-gate wording below is phase-time evidence only. Current sequencing is owned by `world-focus-current-checkpoint.md`; final WS1–WS5 closure authority is `world-focus-substrate-final-convergence-proof.md`. Do not execute old next-gate text from this baseline.

This is the executable/research/contract inventory required by **WS0 — Substrate Inventory**.

Its purpose is not to declare the World substrate universally complete. It establishes exactly what exists today and what WS1–WS5 must attempt to falsify.

Classification vocabulary:

```text
IMPLEMENTED              code exists on branch
CONTRACT-ONLY            accepted current contract; executable support may be incomplete
STRESS-EVIDENCED         durable research/simulation exists; not necessarily executable
PRESSURE-NEEDED          must be tested by WS1-WS5 before universal closure
MATERIALIZATION-DEFERRED intentionally delayed until after WS8
BACKEND-DEFERRED         requires later real application/API/provider/DB/runtime integration
REJECTED                 explicitly not part of the target architecture
```

A row may carry several classifications because, for example, a mechanism can be implemented but still need broader product falsification.

---

## 1. High-level disposition

The current branch already has a strong **workspace mechanics substrate** and a narrower set of **real product/application verticals**.

The most important WS0 conclusion is:

```text
composition / workspace / surface mechanics = substantially executable
real reusable World work semantics          = only partially materialized
broad World/work coverage                   = heavily research-evidenced
universal primitive closure                 = not yet performed
non-visual whole-corpus oracle              = not yet built
```

Therefore:

```text
World Workspace Platform ENGINEERING CLOSED
```

remains a truthful bounded statement, while:

```text
World Substrate UNIVERSALLY CLOSED
```

is **not** yet claimed.

---

## 2. Product / semantic substrate

| Area | Current state | WS0 evidence / meaning | Next pressure |
| --- | --- | --- | --- |
| World definition | CONTRACT-ONLY + STRESS-EVIDENCED | World = user-recognizable continuity context; shared coordinate system, not source of truth | keep as invariant; only reopen if a real scenario falsifies it |
| World-worthiness | CONTRACT-ONLY + STRESS-EVIDENCED | recurring re-entry, continuity, resumability, situational understanding, meaningful change, scoped action/history | pressure borderline/overlapping Worlds |
| Home / World / Explore boundary | CONTRACT-ONLY + STRESS-EVIDENCED | cross-life compression vs scoped continuation vs deeper specialist/evidence depth | pressure cross-surface routing and escalation |
| Output Grammar | CONTRACT-ONLY + STRESS-EVIDENCED + PRESSURE-NEEDED | Orientation, Situation, Continuity, Attention, Next, Change, optional Trajectory, Evidence, Explore, Act/Decide, Intelligence | determine reusable work primitives beneath these answer families |
| Sparse/negative-space rule | CONTRACT-ONLY + STRESS-EVIDENCED | no fake cards/KPIs/AI filler | verify across corpus |
| same reality in multiple Worlds | CONTRACT-ONLY + STRESS-EVIDENCED + PRESSURE-NEEDED | projection reuse without canonical duplication | executable cross-World scenarios needed |
| World relevance vs authorization | CONTRACT-ONLY + STRESS-EVIDENCED | relevance is contextual prior, not access control | multi-actor/selective-disclosure pressure |

Permanent rejects retained:

```text
World as canonical Domain owner
World as DB partition
World as ACL/security boundary
World as AI memory bucket
World as universal Goal/Project/Person/Asset mapping
World as generic dashboard ontology
universal WorldItem / Thing / Entity / Relationship semantic root
```

---

## 3. Core platform vocabulary — executable

### 3.1 Resource/status vocabulary

**Classification:** IMPLEMENTED + PRESSURE-NEEDED

`apps/web/src/features/world-focus/model/world-focus-platform.ts`

Implemented resource states:

```text
loading
ready
empty
partial
stale
error
unavailable
```

Also implemented:

```text
composition stability: stable / adaptive / ephemeral
composition origin: system-default / user / dante-proposed / application-derived
interaction depth: peek / insight / explore
presentation: inline / popover / sidecar / modal / full-screen / route
feature availability: available / disabled / unavailable
versioned payload seam
safe absolute HTTPS external URL parsing
```

This is useful platform vocabulary, not yet proof that every future work primitive has the right semantic state model.

WS1–WS5 must pressure whether additional **work-semantic** distinctions are required without bloating this platform vocabulary.

---

## 4. Dynamic composition substrate — executable

### 4.1 Composition ownership and candidate planning

**Classification:** IMPLEMENTED + STRESS-EVIDENCED + PRESSURE-NEEDED

Primary files:

```text
apps/web/src/features/world-focus/model/world-focus-composition.ts
apps/web/src/features/world-focus/model/world-focus-composition-plan.ts
apps/web/src/features/world-focus/model/world-focus-composition.test.ts
apps/web/src/features/world-focus/model/world-focus-composition-plan.test.ts
```

Implemented concepts include:

```text
stable / adaptive / ephemeral
system-default / user / dante-proposed / application-derived
lead / primary / supporting
wide / standard / compact
logical 12-unit plan
stable relative-order preservation
adaptive/ephemeral budgets
explicit omission reasons
bounded row planning
```

The planner intentionally does not know `worldId` or canonical Domain semantics.

Existing stress evidence records 500 deterministic composition scenarios.

What is **not** proven by this:

```text
that the final universal work primitive vocabulary is known
that every Output Grammar answer maps cleanly to current module kinds
that dense real Worlds never require another composition invariant
that multi-actor/privacy conditions are fully represented in composition inputs
```

Those remain WS1–WS6 pressure.

---

## 5. Finite module extension substrate — executable

**Classification:** IMPLEMENTED + STRESS-EVIDENCED + PRESSURE-NEEDED

Primary files:

```text
apps/web/src/features/world-focus/ui/world-focus-module-registry.ts
apps/web/src/features/world-focus/ui/world-focus-module-registry.test.ts
apps/web/src/features/world-focus/ui/world-focus-composition-host.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-host.test.tsx
apps/web/src/features/world-focus/ui/world-focus-core-composition.tsx
```

Accepted behavior:

```text
finite code-shipped module registry
unknown kinds fail locally
no remote/model-generated executable UI
shared workspace platform rather than page-per-World component tree
specialist renderer allowed only when reusable primitives materially lose meaning/interaction
```

What remains open for WS1–WS6 is **which universal work primitives deserve shared renderers** and which cases truthfully require specialist capability.

The extension mechanism exists; the final primitive catalog does not.

---

## 6. Transient workspace interaction state — executable

**Classification:** IMPLEMENTED + STRESS-EVIDENCED + PRESSURE-NEEDED

Primary files:

```text
apps/web/src/features/world-focus/model/world-focus-workspace.ts
apps/web/src/features/world-focus/model/world-focus-workspace.test.ts
```

Implemented state:

```text
worldId
generation
bounded selection reference
surface stack
```

Implemented bounded context reference:

```text
kind
key
```

Implemented surface descriptor:

```text
instanceId
kind
depth
presentation
origin
boundGeneration
contextReference
dismissible
```

Implemented intents:

```text
select-context
clear-context
open-surface
replace-surface
promote-surface
close-surface
close-top-surface
```

Important proven invariants:

```text
expectedGeneration may turn stale presentation intent into deterministic no-op
blocking modal/full-screen creates a blocking tail
weaker surfaces cannot be appended above a blocker
lower surfaces cannot be mutated while blocker owns interaction
cursor exposes bounded refs, not raw payload/DOM/authorization/provider state
```

The code explicitly states that workspace state does not own:

```text
canonical World truth
authorization
provider state
durable DANTE Run lifetime
```

WS1–WS5 must pressure whether real work requires additional **non-canonical transient interaction primitives** beyond selection + surfaces, without turning the workspace reducer into a business-state store.

---

## 7. Physical workspace allocation — executable

**Classification:** IMPLEMENTED + STRESS-EVIDENCED + PRESSURE-NEEDED

Primary files:

```text
apps/web/src/features/world-focus/model/world-focus-workspace-allocation.ts
apps/web/src/features/world-focus/model/world-focus-workspace-allocation.test.ts
apps/web/src/features/world-focus/ui/world-focus-workspace-allocation-context.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace-allocation.test.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace-host.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace-host.test.tsx
```

Implemented orthogonal axes:

```text
mainAllocation: full / split
topLayer: none / overlay / focus
mainInteraction: interactive / inert
surface slot: sidecar / overlay / focus / dormant / external
```

Default allocation policy currently implements:

```text
minimum split workspace: 900
minimum useful main:      520
minimum sidecar:          300
maximum sidecar:          420
preferred sidecar:        36%
split gap:                16
```

Important implemented behavior:

```text
wide sidecar consumes real canvas width
narrow sidecar degrades inside workspace allocation to overlay
modal/full-screen can make main inert
underlying visible sidecar can be inert under blocker
malformed stacks are defensively normalized
dormant placement is explicit
route presentation maps to external slot
```

Existing stress evidence records 500 deterministic allocation/surface-stack scenarios.

Important limitation exposed before this WS program:

- the generic workspace allocator owns the **rectangular World workspace**;
- route-owned deeper surface presentation is represented as `external`, but D2 route-level materialization is not implemented;
- therefore current allocation code must not be mistaken for complete mobile/route-owned DANTE conversation materialization.

That specific D2 work remains MATERIALIZATION-DEFERRED until WS8.

---

## 8. Surface registry and mounted surface layer — executable

**Classification:** IMPLEMENTED + PRESSURE-NEEDED

Primary files:

```text
apps/web/src/features/world-focus/ui/world-focus-surface-registry.ts
apps/web/src/features/world-focus/ui/world-focus-surface-registry.test.tsx
apps/web/src/features/world-focus/ui/world-focus-surface-layer.tsx
apps/web/src/features/world-focus/ui/world-focus-surface-layer.test.tsx
apps/web/src/features/world-focus/ui/world-focus-core-surfaces.tsx
```

Implemented rules include:

```text
finite local code-shipped renderer registration
unknown future kind fails locally rather than executing remote UI
active/dormant allocation filtering
workspace-local surface rendering
interaction/inert propagation
local surface failure isolation
```

D1 also exposed and fixed a real generic non-modal popover issue:

```text
popover allocation wrapper -> pointer-transparent
actual panel               -> pointer-interactive
main World                 -> remains interactive
```

This is strong mechanical substrate evidence. It is not yet a universal answer to every future work primitive or route-level specialist surface.

---

## 9. Frozen World route/shell geometry — executable + contractually frozen

**Classification:** IMPLEMENTED + CONTRACT-ONLY for ownership invariants

Primary areas:

```text
apps/web/src/features/world-focus/ui/world-focus-page.tsx
apps/web/src/features/world-focus/ui/world-focus-page.test.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace.tsx
apps/web/src/features/world-focus/ui/world-focus-visual-frame.tsx
apps/web/src/features/world-focus/model/world-focus-geometry.ts
apps/web/src/features/world-focus/model/world-focus-geometry.test.ts
```

Current frozen macro ownership remains:

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

WF-G3 geometry remains locked. WS1–WS8 may pressure substrate behavior **inside/above this ownership model** but must not casually move the shell or redefine Global Topbar ownership.

Visual VFX remains candidate rather than human-frozen final design.

---

## 10. Application/read substrate — narrower than workspace mechanics

This is one of the most important WS0 findings.

### 10.1 Foundation application utilities

**Classification:** IMPLEMENTED

Primary files:

```text
apps/web/src/features/world-focus/application/world-focus-foundation.ts
apps/web/src/features/world-focus/application/world-focus-foundation.test.ts
```

Existing B0 evidence records:

```text
runtime validation seam
latest-only async commit protection
AbortSignal / cancellation foundation
safe external link parsing
error isolation foundations
User Timing/open-to-usable seam
```

### 10.2 Continuity / Resume vertical

**Classification:** IMPLEMENTED + STRESS-EVIDENCED

Primary files:

```text
apps/web/src/features/world-focus/model/world-focus-continuity.ts
apps/web/src/features/world-focus/application/world-focus-continuity.ts
apps/web/src/features/world-focus/application/world-focus-continuity-runtime.ts
apps/web/src/features/world-focus/application/world-focus-continuity-fixture-adapter.ts
apps/web/src/features/world-focus/application/world-focus-continuity.test.ts
apps/web/src/features/world-focus/ui/world-focus-continuity.tsx
apps/web/src/features/world-focus/ui/world-focus-continuity.test.tsx
```

B2 semantics already established:

```text
recent != resumable
last viewed != meaningful checkpoint
open != in motion
unfinished != important
AI-guessed relevance != continuity fact
```

The deterministic fixture adapter remains explicitly pre-backend.

### 10.3 Missing breadth

Outside foundation + Continuity, the current `application/` directory does **not** yet contain production materialization for the full Output Grammar or a universal work primitive layer.

This is not a defect to patch inside WS0. It is the main reason the program now performs WS1–WS8 before further visible materialization.

---

## 11. DANTE substrate — partly executable, partly accepted future work

### 11.1 D0 spatial/presence contract

**Classification:** CONTRACT-ONLY + STRESS-EVIDENCED

Accepted principle:

> AI availability is persistent; AI footprint is not.

Accepted ladder:

```text
quiet invoke
compact non-modal composer
wide ongoing conversation -> sidecar
constrained/mobile -> route-owned focus overlay
explicit maximize/restore
explicit contextual/deictic binding later
```

### 11.2 D1 quiet invoke + compact composer

**Classification:** IMPLEMENTED

Primary files:

```text
apps/web/src/features/world-focus/ui/world-focus-dante-entry.tsx
apps/web/src/features/world-focus/ui/world-focus-dante-entry.css
apps/web/src/features/world-focus/ui/world-focus-dante-entry.test.tsx
```

D1 closure evidence:

```text
validated code HEAD f17291de32e6bdced20536807b32928ec1be6aea
Frontend CI        33552437179 PASS
```

Key current semantics:

```text
no auto-open
non-modal composer
World remains interactive
focus restoration
truthful unavailable/pre-backend failure
draft preserved
no fake assistant response
no fake model/tool/effect
contextReference: null for global quiet invoke
```

### 11.3 D2–D6

**Classification:** MATERIALIZATION-DEFERRED

Previously sequenced work remains valid but is paused until WS8:

```text
D2 adaptive ongoing conversation surface
D3 deterministic pre-backend conversation adapter
D4 explicit contextual/deictic invocation
D5 Insight presentation integration
D6 Proposal / confirmation / receipt presentation
```

WS1–WS6 may refine what substrate references/primitives these surfaces consume. They must not prematurely implement the surfaces.

### 11.4 Real intelligence/runtime

**Classification:** BACKEND-DEFERRED

Not implemented here:

```text
real model call
streaming
conversation backend
canonical chat persistence
Context Builder runtime
tool execution
governed effects
provider runtime
```

---

## 12. Context / DANTE authorization model

**Classification:** CONTRACT-ONLY + STRESS-EVIDENCED + PRESSURE-NEEDED

Current four-layer contract:

```text
1. World identity / purpose
2. stable World relevance definition
3. current bounded interaction cursor when needed
4. authorized purpose-scoped DANTE context
```

Current executable frontend cursor covers bounded references and generation, but the future Context Builder is not implemented in this branch.

WS2/WS3 must pressure:

```text
same visible basis vs DANTE basis
cross-World expansion
selective disclosure
sensitivity
recipient/actor differences
stale provider data
unknown vs false
explicit vs implicit context binding
```

Any finding that implies `surface visible == authorized for model context` is rejected.

---

## 13. Multi-actor / collaboration substrate

**Classification:** STRESS-EVIDENCED + PRESSURE-NEEDED + BACKEND-DEFERRED for real enforcement

Existing research already established that collaboration is not `single-user × N`.

Permanent semantic distinctions include:

```text
membership != visibility != authority
assignment/execution != stewardship/responsibility
RSVP/acceptance != Actual participation
sent != seen != understood != acknowledged != accepted != acted upon
shared context != access to private overlays
provider acknowledgement != canonical completion
```

The current World workspace mechanics do not yet constitute a complete multi-actor work primitive system.

WS1–WS6 must determine which collaboration concepts are universal work primitives, which belong to Domain/application projections, and which are backend/AuthZ concerns that must remain outside frontend substrate ownership.

---

## 14. Temporal / recurrence / actual / evidence semantics

**Classification:** CONTRACT-ONLY + STRESS-EVIDENCED + PRESSURE-NEEDED

Higher-order semantic constraints already exist:

```text
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
planned/intended != Actual
Evidence != Provenance
absence != false
```

World Focus previously falsified a universal first-open time Lens.

Therefore WS1–WS6 must not create a generic timeline/time-range primitive by default. Any temporal work primitive must be earned by scenarios and preserve the existing semantic distinctions.

---

## 15. Persistence / customization / stable configuration

**Classification:** STRESS-EVIDENCED + BACKEND-DEFERRED + MATERIALIZATION-DEFERRED

Existing research says future persisted stable composition/configuration needs explicit:

```text
schema/version evolution
migration semantics
concurrency semantics
no silent last-write-wins assumption
```

Existing composition origin/stability vocabulary is executable, but there is no claim that user customization persistence is implemented.

A future flow such as:

```text
View -> Customize Draft -> Apply / Cancel
```

remains post-primitive materialization work.

DANTE may propose configuration changes; it must not silently apply them.

---

## 16. Error / stale / race / unavailable behavior

**Classification:** IMPLEMENTED in several mechanics + PRESSURE-NEEDED across full corpus

Already executable in bounded areas:

```text
resource status vocabulary
latest-only read protection
AbortSignal foundation
expectedGeneration stale surface intent protection
route error boundary
local renderer/surface failure boundary
feature unavailable/disabled vocabulary
```

Still to pressure across scenarios:

```text
multi-source partial data
mixed freshness
late result after World switch
late result after context-generation change
specialist surface failure
AI/provider unavailable while deterministic World remains useful
configuration version mismatch
```

---

## 17. Accessibility / focus / responsive substrate

**Classification:** IMPLEMENTED in current surfaces + PRESSURE-NEEDED for future primitive set

Existing evidence includes:

```text
container-query foundation
actual ResizeObserver allocation
keyboard/Escape behavior
focus restoration for D1
non-modal vs modal interaction distinctions
inert handling
reduced-motion foundation
390px containment tests
no horizontal overflow checks
axe checks in current D1 paths
```

This does not automatically prove future primitives. WS3 and post-WS8 materialization must keep these as invariant classes.

---

## 18. Performance / scale substrate

**Classification:** STRESS-EVIDENCED + PARTLY IMPLEMENTED + PRESSURE-NEEDED

Existing principles:

```text
large data bounded/aggregated before React
modules adapt to actual allocated main width
VFX degrades before interaction/performance
User Timing seam exists
finite registries, not runtime executable plugins
```

WS1/WS3 must include:

```text
large history
high-frequency records
dense answer sets
20+ potential outputs
multiple source pressure
```

The expected solution is usually ranking/bounding/aggregation, not rendering all raw records.

---

## 19. Specialist extension / unknown future World

**Classification:** IMPLEMENTED extension seam + STRESS-EVIDENCED + PRESSURE-NEEDED

Already accepted:

```text
one shared World workspace platform
finite approved module/surface registries
controlled specialist extension
no arbitrary AI executable UI
specialist renderer only when generic primitive materially damages semantics/UX
```

Travel remains an example of a potential specialist experience only if integrated time/place/transport/booking/participation interaction proves generic primitives insufficient.

`worldId == travel` alone is not justification for page branching.

WS1–WS8 must explicitly retain an unknown future World and unknown specialist-capability case.

---

## 20. Test / evidence inventory

Current durable engineering evidence includes at least:

```text
B0 production foundation tests/review
B1 product disposition
B2 continuity application/UI tests
500 deterministic composition scenarios
500 deterministic allocation/surface-stack scenarios
module registry tests
surface registry tests
workspace reducer tests
workspace host/allocation tests
surface layer tests
World page tests
D1 component tests
D1 Chromium real-browser acceptance
D1 axe wide/compact
frozen Timeline Firefox/mobile regressions
Frontend CI closure evidence
```

Current research evidence includes:

```text
World product reverse engineering
World product stress matrix
DANTE <-> user reverse engineering
DANTE/user gap closure
workspace/module scenario oracle
workspace dynamic composition/allocation review
DANTE spatial/presence review
multi-actor collaboration research in wider project authority
```

Important distinction:

```text
many strong bounded tests
!=
one executable whole-corpus substrate oracle
```

That missing whole-corpus executable layer is the explicit purpose of WS7.

---

## 21. Capability matrix — concise baseline

| Capability | Executable today | Durable evidence | Universal closure now? | Program disposition |
| --- | --- | --- | --- | --- |
| World identity/orientation | yes | yes | bounded | preserve |
| Continuity/Resume | yes | yes | one real output family only | corpus pressure |
| dynamic composition mechanics | yes | yes | mechanics closed, work semantics not | preserve + pressure |
| stable/adaptive/ephemeral | yes | yes | mechanics closed | pressure against corpus |
| finite module registry | yes | yes | extension mechanism closed | primitive catalog open |
| finite surface registry | yes | yes | extension mechanism closed | primitive/surface usage open |
| transient cursor/selection | yes | yes | bounded mechanics closed | contextual work pressure |
| surface stack / blocking | yes | yes | bounded mechanics closed | adversarial pressure |
| responsive allocation | yes | yes | workspace-local mechanics closed | route/specialist pressure |
| route/external surface slot | representation yes | yes | route materialization no | materialization-deferred |
| deterministic read adapter pattern | yes | B2 | not broad | primitive/read pressure |
| Situation | not generally | research | no | WS1-WS6 |
| Attention/Resolution | not generally | research | no | WS1-WS6 |
| Next | not generally | research | no | WS1-WS6 |
| Change | not generally | research | no | WS1-WS6 |
| Trajectory/Comparison | not generally | research | no | WS1-WS6 |
| Evidence/History | not generally | research | no | WS1-WS6 |
| Explore | surface semantics partly | research | no | WS1-WS6 then materialize |
| Act/Decide | no real effects | research/contracts | no | primitives now; effects backend-deferred |
| Intelligence | D1 entry only | strong research | no | WS2 then M4/backend |
| multi-actor coordination | no universal executable primitive | strong research | no | WS1-WS6 |
| stable customization persistence | no | research | no | post-WS8/backend |
| whole-corpus nonvisual oracle | no | scenario evidence only | no | WS7 |

---

## 22. WS1 primary falsification targets

WS1 must not start from a blank page. It should deliberately attack the following uncertainty clusters discovered by this inventory.

### P1 — Work primitive completeness

Can materially different user jobs be expressed without inventing one-off page semantics?

### P2 — Output Grammar to primitive relationship

Are the eleven answer families enough as product grammar while requiring a smaller/different reusable work primitive vocabulary underneath?

Do not assume one answer family = one module = one primitive.

### P3 — Read / evidence / freshness model

Can generic substrate support fresh/partial/stale/unavailable/multi-source evidence without becoming a generic data platform or losing source truth?

### P4 — Continuation / state / transition

What non-canonical work state is truly reusable beyond the existing Continuity vertical?

### P5 — Choice / proposal / decision / action preparation

What frontend work primitive is needed before the later governed-effect backend seam while preserving:

```text
suggestion != Proposal
Proposal != Decision
Decision != effect
```

### P6 — Multi-actor coordination

What must be expressible universally for responsibility, handoff, acknowledgement, participation and selective disclosure without duplicating Domain/AuthZ semantics?

### P7 — DANTE optionality

Does every scenario remain meaningfully operable without DANTE, and can DANTE enhance the same substrate through bounded references rather than bespoke AI-only objects?

### P8 — Unknown specialist capability

Can an unknown future specialist surface be integrated through the finite extension model without page-per-World branching or arbitrary executable UI?

### P9 — Scale / density

Does the composition hypothesis survive zero, 1–2, 4–8, 12 and 20+ possible answers plus large histories?

### P10 — Failure / race / responsive class completeness

Do current generation, allocation, blocking, inert, error and cancellation mechanics cover the materially distinct failures surfaced by the corpus?

---

## 23. Things WS1 must NOT rediscover from zero

Already closed unless falsified by new evidence:

```text
What is a World?
Should every Goal/Project/Person/Asset be a World?
Should each World get its own page architecture?
Can AI generate arbitrary UI?
Should every World have a universal time Lens?
Is recent equal to resumable?
Should global DANTE silently inherit selected context?
Should DANTE be permanently open?
Can mobile ongoing DANTE be trapped in the narrow World rectangle?
```

WS1 uses these as constraints, not fresh debate prompts.

---

## 24. WS0 closure decision

WS0 is **COMPLETE as an inventory baseline**.

It does not close the substrate.

The branch now has enough durable truth to enter WS1 with a falsifiable hypothesis:

> DANTE already has a credible finite workspace/composition/surface substrate, but the universal **work primitive** layer and its cross-scenario executable proof are not yet closed.

Therefore the next gate is:

```text
WS1 — Simulation Corpus
```

No WS1 simulation has been executed in this document.