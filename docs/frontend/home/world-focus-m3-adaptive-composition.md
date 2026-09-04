# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 CUSTOMIZATION SAFETY CLOSED / PASS / M3-3 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`

This is the bounded engineering authority for M3. It inherits closed M0–M2 semantics and does not reopen Domain, rendering, AuthZ, DANTE runtime or backend ownership.

## 1. M3 scope

Frozen M0 assignments:

```text
M0-37 production candidate resolver from meaningful projections     M3
M0-38 Customize Draft -> Apply/Cancel, pin/hide/reorder/promote     M3
M0-39 client config revision/conflict/migration representation      M3
M0-40 durable persistence/cross-device sync/conflict authority      BACKEND
```

M3 must reuse:

```text
M1 application projections
M2 finite renderer/presentation vocabulary
Workspace Platform composition planner
finite module registry
CompositionHost placement/failure isolation
```

M3 must not create a second planner, page-per-World renderer fork, universal ranking score, fake persistence or frontend Domain/AuthZ authority.

## 2. Permanent product rule — manual and DANTE share canonical paths

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful product functions.

```text
MANUAL UI [M3-3] ----\
                       -> finite commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE receives no hidden mutation route. A `dante-proposed` operation uses the same draft, review, Apply and revision guards as manual interaction.

## 3. M3-1 — Composition Configuration Foundation — CLOSED / VALIDATED

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Config snapshot:

```text
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

Configuration is client composition metadata only. It contains no canonical Domain payload, disclosure/AuthZ authority, provider/runtime state, renderer function/JSX or arbitrary property bag.

Schema disposition remains explicit:

```text
current
migration-required
unsupported
```

Original M3-1 transaction:

```text
CURRENT revision N
  -> DRAFT(baseRevision=N)
  -> pin / unpin / hide / show / move / promote / restore
  -> Apply | Cancel
```

Original M3-1 evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
72 / 72 web test files
344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations
```

## 4. M3-2 — Adaptive Candidate Resolver — CLOSED / VALIDATED

Production owners:

```text
application/world-focus-composition-opportunities.ts
application/world-focus-composition-resolver.ts
```

M3-2 remains pre-planner and pre-renderer:

```text
validated M1 results
  -> meaningful opportunity extraction
  -> current M3 composition config + finite value signals
  -> candidate resolver
  -> WorldFocusCompositionCandidate[]
  -> existing resolveWorldFocusCompositionPlan()
```

It does not mount UI and does not modify `world-focus-core-composition.tsx`.

### 4.1 Meaningful opportunity extraction

```text
Situation ready + non-empty               -> situation
Continuity ready/partial/stale + content  -> continuity
Continuity empty/unavailable              -> no opportunity
Attention ready                           -> attention:<primitive.instanceId> per item
Next ready + non-empty                    -> next
Comparison ready                          -> comparison:<primitive.instanceId> per item
Trajectory ready                          -> trajectory:<primitive.instanceId> per item
Evidence/History ready + any role content -> evidence-history
```

Sparse Worlds stay sparse. Renderer availability never creates content.

Opportunity metadata is intentionally narrow:

```text
instanceId
kind
defaultProminence
footprint
```

No projection, context reference, reason code, canonical payload, disclosure/AuthZ state or executable renderer crosses the boundary. Opportunity set is bounded and duplicate instance ids fail closed. Unknown future World/module kinds remain representable.

### 4.2 Finite value signals

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

There is no `score`, `confidence` or `aiRelevance` authority.

For **unconfigured** opportunities:

```text
FOREGROUND
material-consequence OR immediacy OR current-intent
-> minimum lead

ACTIVE
resumability OR meaningful-change
-> minimum primary

ORDINARY
no asserted value signal
-> opportunity default prominence
```

Signal absence is not interpreted as a semantic negative.

### 4.3 User configuration precedence

```text
hidden user config > ranking signals
pinned user config > adaptive budget
configured relative order > adaptive ranking
explicit promote -> lead override only
```

Pinned visible intent without currently meaningful content remains explicit `unresolvedPinned` with `meaningful-projection-unavailable`; no fake module is created.

### 4.4 M3-2 original evidence

```text
RED  c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAILURE
PASS b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
74 / 74 web test files
356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

## 5. PRE-M3-3 Customization Reachability Safety — CLOSED / PASS

### 5.1 Why this gate was required

A read-only M3-3 preflight against live M3-1/M3-2 discovered three contract defects that would have made a professional Customize UX dishonest or semantically wrong:

```text
A. Unconfigured meaningful opportunity was unreachable
   M3-1 commands targeted existing config entries only.
   A new adaptive opportunity could not be pinned/hidden/moved/promoted by the manual UI.

B. Config presence accidentally changed prominence
   M3-2 mapped every configured non-lead opportunity to primary.
   A supporting Comparison/Trajectory became primary merely because it entered config.

C. Apply proved revision number but not base snapshot identity
   A same-revision draft whose base content differed from current could still Apply.
```

The correct response was to harden the model/application seam before building UI, not patch around it in components.

### 5.2 Red-first proof

Authorized PRE-SCOPE:

```text
959c9077b4726a0a89b479d23ebe0edab216018b
```

Red test-only commit:

```text
HEAD be63d49c43c88a491439b4014668a51c8ff8ad6b
CI   33861956558 EXPECTED FAILURE
```

`world-focus-pre-m3-3-customization-safety.test.ts` was added before production changes. The five hostile obligations all failed while every pre-existing web test stayed green:

```text
new hostile safety tests 0 / 5 PASS
pre-existing web tests   356 / 356 PASS
```

The five red obligations were:

```text
1. meaningful unconfigured opportunity must be able to enter customization
2. configured + no promote must preserve opportunity default prominence
3. same revision + different base snapshot must not Apply
4. adopt must not retain arbitrary payload/AI/disclosure data
5. duplicate / blank / malformed adopt target must fail closed
```

The hostile test was not weakened after red.

### 5.3 `adopt` — bounded reachability, not new truth

The finite command language is now:

```text
adopt
pin
unpin
hide
show
move
promote
restore
```

`adopt` accepts a known `WorldFocusCompositionOpportunity`. It is normalized through the existing opportunity constructor, then only composition metadata enters the draft:

```text
instanceId
kind
visibility = visible
pinned = false
prominenceOverride = null
```

The recorded operation retains only:

```text
source
type = adopt
instanceId
kind
```

Explicit exclusions:

```text
adopt != semantic truth
adopt != canonical payload ownership
adopt != AuthZ/disclosure proof
adopt != renderer availability proof
adopt != persistence
adopt != AI relevance
adopt != score/confidence
```

Arbitrary extra fields are stripped by normalization. Duplicate instance ids fail closed. Blank/malformed opportunity metadata fails through existing finite validators.

### 5.4 `restore` semantics

`restore` is defined relative to the snapshot at draft start:

```text
base entry existed
-> restore exact base entry + base position

entry was adopted during this draft and absent in base
-> remove entry from working draft
```

This prevents `restore` from creating accidental pseudo-persistence for newly adopted opportunities.

### 5.5 Correct configured prominence semantics

After hardening:

```text
configured + prominenceOverride = null
-> opportunity.defaultProminence

configured + prominenceOverride = lead
-> lead
```

Consequences:

```text
Comparison supporting + adopt/config + no Promote = supporting
Trajectory supporting + pin + no Promote           = supporting
pin changes stability/ownership, not prominence
config presence is not evidence of primary importance
```

Finite value bands continue to rank/elevate **unconfigured** adaptive opportunities only.

### 5.6 Apply snapshot identity guard

Apply semantics are now:

```text
current World != draft World
-> fail closed

current revision != draft.baseRevision
-> revision-conflict

same revision
but draft.baseConfig != current snapshot structurally
-> invalid base snapshot / fail closed

same revision
+ exact base snapshot identity
+ base/working revisions equal baseRevision
-> Apply may produce revision N+1
```

Structural equality covers schemaVersion, revision, World id, entry count/order and every entry field. No implicit merge exists.

### 5.7 Green validation

Production closure:

```text
HEAD 7781c6751a455767595eaf159747da833117f8b2
CI   33862549244 PASS
```

Observed:

```text
Frontend pre-production contracts PASS
Lint                              PASS
Typecheck                         PASS
Architecture                      PASS
Generated-source drift            PASS
hostile safety tests              5 / 5 PASS
Web test files                    75 / 75 PASS
Web unit tests                    362 / 362 PASS
Architecture graph                288 modules / 804 dependencies / 0 violations
Production build                  PASS
Diff check                        PASS
Repository mutation check         PASS
Mobile Bundle                     PASS
Web E2E / Chromium                PASS
frozen Timeline Firefox           PASS
Frontend CI Gate                  PASS
```

No Customize UI, live candidate mounting or backend work was introduced by this gate.

## 6. Current M0 L5 disposition

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + customization commands       MODEL + PRE-M3-3 SAFETY CLOSED; UI M3-3 NEXT
M0-39 client revision/conflict/migration representation M3-1 + PRE-M3-3 SAFETY CLOSED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

## 7. M3-3 Manual Customize UX — NEXT / NOT STARTED

M3-3 must now materialize the manual experience over validated state transitions; it must not invent a parallel UI-only state model.

### 7.1 Product contract

```text
VIEW MODE
  current accepted composition
  no draft mutation controls

CUSTOMIZE MODE
  explicit entry
  isolated draft created from current config
  meaningful opportunities available for adoption/customization
  changes visible as draft state
  Apply / Cancel are explicit terminal actions
```

For an opportunity absent from config:

```text
meaningful opportunity
-> adopt
-> optional pin/hide/move/promote
```

Never synthesize config entries from arbitrary UI data.

### 7.2 Interaction requirements

```text
pin / unpin
hide / show
move/reorder
promote / restore
dirty/changed-state communication
review before Apply where composition impact warrants it
revision-conflict treatment
invalid-state treatment
keyboard reorder path independent of drag
touch-accessible actions
focus entry and focus return
screen-reader names/state announcements
responsive geometry
```

Drag/drop is optional enhancement, not the state model. If introduced, parity is required across pointer, touch, keyboard and assistive technologies. Evaluate React Aria only if the concrete interaction complexity earns the dependency; do not add it pre-emptively.

### 7.3 Spatial guidance

Respect existing World surface ownership:

```text
wide desktop
-> use existing wide sidecar / workspace surface patterns when appropriate
-> do not modalize the whole World without need

compact / tablet / mobile
-> use existing route-owned focus surface/overlay semantics
-> no bespoke viewport hack
```

Do not alter frozen WF0/WF-G3 geometry or AppShell ownership.

### 7.4 Test/acceptance obligations

At minimum:

```text
View/Customize separation
entering Customize leaves current config unchanged
unconfigured meaningful opportunity adopts through canonical command
adopt defaults visible/unpinned/null override
pin/unpin draft-only
hide/show draft-only
keyboard reorder deterministic
pointer/touch reorder if drag exists
promote -> lead override only
restore existing -> exact base state/order
restore adopted-only -> absence
Cancel -> exact base snapshot
Apply -> revision N+1 exactly once
revision-conflict UX
same-revision wrong-base invalid-state UX
sparse World remains sparse
unresolved pinned intent remains honest
no reference/reasonCode/payload leak
no live M3-4 candidate mounting
focus management
forced-colors
reduced-motion when motion exists
no horizontal document overflow
pressure widths 1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 / 721 / 720 / 719 / 390
```

Automated green does not equal human visual acceptance; that remains explicitly recorded only when actually performed.

## 8. M3-4 and later

M3-4, only after M3-3, integrates:

```text
validated application projections
-> M3-2 meaningful opportunities/resolver
+ accepted M3 config
-> existing planner
-> finite registry
-> CompositionHost
```

M3-4 must preserve sparse output, user precedence and local renderer failure isolation.

M3 final hostile closure follows M3-4.

M4 resumes D2–D6 contextual DANTE only after M3 closes. M5 proves contrasting complete Worlds. M6 performs integrated product/visual/a11y/performance review. M7 freezes frontend/backend seams. Real backend/API/DB/provider integration begins only after M7.

## 9. Stop line

```text
M3-3 Manual Customize UX                 NEXT
M3-4 Integrated Adaptive Composition     BLOCKED BY M3-3
M3 final hostile closure                 BLOCKED BY M3-4
M4 D2–D6 contextual DANTE                BLOCKED BY M3
M5–M7                                    BLOCKED BY SEQUENCE
BACKEND                                  BLOCKED UNTIL M7
```

A fresh explicit bounded write gate is required before M3-3 production writes.
