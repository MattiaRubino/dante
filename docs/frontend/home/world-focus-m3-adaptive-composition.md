# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 CLOSED / VALIDATED / M3-4 CLOSED / VALIDATED / M3 FINAL HOSTILE CLOSURE NEXT  
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

M3 reuses M1 application projections, M2 finite presentation vocabulary, Workspace Platform planning/packing, the finite module registry and CompositionHost failure isolation. It must not create a second planner, page-per-World fork, universal ranking score, fake persistence or frontend Domain/AuthZ authority.

## 2. Permanent product rule — manual and DANTE share canonical paths

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful product functions.

```text
MANUAL UI [M3-3] ----\
                       -> finite commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE receives no hidden mutation route. `dante-proposed` remains the same governed transaction model as manual interaction.

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
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Finite commands:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Configuration is client composition metadata only. Apply requires revision freshness and exact base snapshot equality. Same numeric revision with a different base fails closed; no implicit merge/rebase exists.

Evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
```

## 4. M3-2 — Adaptive Candidate Resolver — CLOSED / VALIDATED

Owners:

```text
application/world-focus-composition-opportunities.ts
application/world-focus-composition-resolver.ts
```

Boundary:

```text
validated M1 results
-> meaningful bounded opportunity
+ current M3 config
+ finite value signals
-> candidate resolver
-> WorldFocusCompositionCandidate[]
-> existing resolveWorldFocusCompositionPlan()
```

Finite value signals remain:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No universal score/confidence/`aiRelevance` authority exists.

User precedence remains:

```text
hidden > ranking signals
pinned > adaptive budget
configured relative order > adaptive ranking
configured + null override -> preserve opportunity.defaultProminence
configured + lead override -> lead
```

Pinned visible intent without meaningful content remains explicit `unresolvedPinned`; no fake module is created.

Evidence:

```text
RED  c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAILURE
PASS b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
```

## 5. PRE-M3-3 safety — CLOSED / PASS

The preflight exposed and closed three contract gaps:

```text
meaningful unconfigured opportunity needed explicit adopt
configured supporting content must not become primary merely by entering config
same-revision different-base Apply must fail closed
```

Evidence:

```text
PRE-SCOPE 959c9077b4726a0a89b479d23ebe0edab216018b
RED       be63d49c43c88a491439b4014668a51c8ff8ad6b / CI 33861956558 EXPECTED FAILURE
PASS      7781c6751a455767595eaf159747da833117f8b2 / CI 33862549244 PASS
```

## 6. M3-3 Manual Customize UX — CLOSED / VALIDATED

Authorized PRE-SCOPE:

```text
7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
```

M3-3 materialized the explicit non-AI customization route over the canonical transaction:

```text
View
-> explicit Customize
-> isolated draft
-> adopt meaningful opportunities
-> pin/unpin/hide/show/move/promote/restore
-> review
-> Apply | Cancel
```

The route-scoped owner keeps accepted config and transaction state in memory. The customization read consumes the seven existing M1 runtime seams and reduces them immediately to bounded opportunity metadata. No payload/reference/reasonCode/AuthZ/provider state leaks into config metadata.

Reorder is keyboard-operable without drag, deterministic, preserves moved-row focus and announces position. Wide uses the existing sidecar allocation; compact degrades through the existing Workspace allocator to overlay.

Final M3-3 evidence:

```text
CODE/TEST HEAD 1978fe5c77c0e2661239372bf0f9bee238021faa
CI             33879774332 / run #907 PASS
77 / 77 web test files
376 / 376 web unit tests
294 modules / 851 dependencies / 0 violations
```

## 7. M3-4 Integrated Adaptive Composition — CLOSED / VALIDATED

Authorized PRE-SCOPE:

```text
688e1ab0c7a42f8d83274dedf5a2988a9388bda4
```

Normal live World composition now uses the validated pipeline:

```text
Situation / Continuity / Attention / Next / Comparison / Trajectory / Evidence-History
-> one bounded adaptive snapshot
-> M3-2 meaningful opportunities
+ exact accepted M3-3 config owner
+ no invented M4/DANTE ranking signals
-> M3-2 candidate resolver
-> existing Workspace planner
-> finite module registry
-> WorldFocusCompositionHost
-> M2 display-safe renderers
```

New production owners:

```text
application/world-focus-adaptive-composition.ts
ui/presentation/world-focus-pre-backend-display-bindings.ts
ui/world-focus-adaptive-composition.tsx
```

The same snapshot supplies the opportunity path and display-safe renderer bindings. Normal composition therefore does not create a second M1 read or state store when accepted config changes.

M3-4 proves:

```text
sparse remains sparse
hidden remains hidden
pin survives adaptive budget without becoming reorder
promote changes prominence without becoming reorder
configured user relative order remains user-owned
configured supporting remains supporting unless promoted
stable relative order remains stable
non-user dynamic lead policy remains intact
unresolved pin does not fabricate content
unknown future kind degrades locally as unsupported
registered renderer throw degrades locally as error
healthy sibling module survives renderer failure
scrollable active main plane is keyboard reachable
accepted config remains client metadata, not persistence
```

### 7.1 Cross-layer planner defect discovered and corrected

Integration proved that M3-2 configured order could be lost when the existing planner re-ranked adaptive entries by prominence. A first slot-replacement fix was deliberately falsified because it could disturb mixed stable/non-user lead ordering.

The final planner resolves a deterministic partial order while leaving membership, budgets and 12-unit packing unchanged:

```text
user move order
stable relative order
non-user dynamic lead precedence
stable before non-user dynamic non-lead
existing policy order as deterministic tie-break
```

### 7.2 Browser accessibility defect discovered and corrected

With multiple live modules, the main plane became genuinely scrollable. Axe reported that the region was not keyboard focusable. Active main plane is now focusable; inert allocation remains non-focusable. No axe rule was disabled.

### 7.3 Renderer isolation RED and fix

```text
RED HEAD d2af7a47df8562439487fb4ab4298bff4653f098
CI       33903884239 / run #933 EXPECTED FAILURE
386 pre-existing tests PASS
1 new test FAIL: registered renderer throw escaped before boundary

FIX HEAD b10dc2bef8bab6ae863ce3c8331da6de96094a66
CI       33904052325 / run #934 PASS
```

Renderer execution now occurs inside the existing `WorldFocusRenderBoundary`; unsupported kind and runtime renderer error remain distinct states.

### 7.4 Final M3-4 evidence

```text
CODE/TEST HEAD                       b10dc2bef8bab6ae863ce3c8331da6de96094a66
Frontend CI                          33904052325 / run #934 PASS
Frontend pre-production contracts    PASS
World Focus pre-production contracts PASS
Web test files                       79 / 79 PASS
Web unit tests                       387 / 387 PASS
Architecture                         299 modules / 891 dependencies / 0 violations
Lint / Typecheck / Generated         PASS
Production build                     PASS
Diff / repository mutation           PASS
Mobile Bundle                        PASS
Chromium                             PASS
frozen Timeline Firefox              PASS
Frontend CI Gate                     PASS
```

Detailed closure: `world-focus-m3-4-integrated-adaptive-composition-review.md`.

### 7.5 Scope audit

Compare `688e1ab... -> b10dc2b...` is linear: ahead 8 / behind 0. Changed non-doc paths are confined to World Focus M3-4 application/UI/test/E2E and the directly-falsified planner/workspace corrections. No Timeline implementation, AppShell, Access/Auth, route tree, backend/API/DB/Alembic/AuthZ/provider/LLM or persistence path changed.

## 8. Current M0 L5 disposition

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE + M3-4 order reconciliation
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + customization commands       M3-3 CLOSED / VALIDATED
M0-39 client revision/conflict/migration representation M3-1 + safety CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

## 9. M3 final hostile closure — NEXT / NOT STARTED

M3 is still ACTIVE. The next phase must falsify the combined M3 layer without adding feature scope.

Required pressure includes:

```text
conflicting configuration
stale / partial / empty / unavailable M1 inputs
sparse and dense Worlds
many-candidate budget pressure
adopted / hidden / pinned / promoted combinations
mixed user/stable/application-derived order laws
unresolved pins
unknown kinds
renderer failures
responsive / keyboard / a11y pressure
accepted-config transaction integrity
```

Only after this phase passes may M3 be marked CLOSED and M4 Contextual DANTE / D2–D6 become NEXT.

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

Human visual acceptance remains **NOT PERFORMED**. Automated browser green does not substitute for it.
