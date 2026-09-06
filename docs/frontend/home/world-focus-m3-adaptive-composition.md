# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 CLOSED / VALIDATED — M3-1 / M3-2 / PRE-M3-3 / M3-3 / M3-4 / FINAL HOSTILE CLOSURE ALL CLOSED  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`

This is the bounded engineering authority for the completed M3 Adaptive World Composition phase. It inherits closed M0–M2 semantics and does not reopen Domain, rendering, AuthZ, DANTE runtime or backend ownership.

## 1. M3 scope

Frozen M0 assignments:

```text
M0-37 production candidate resolver from meaningful projections     M3
M0-38 Customize Draft -> Apply/Cancel, pin/hide/reorder/promote     M3
M0-39 client config revision/conflict/migration representation      M3
M0-40 durable persistence/cross-device sync/conflict authority      BACKEND
```

M3 reuses M1 application projections, M2 finite presentation vocabulary, Workspace Platform planning/packing, the finite module registry and CompositionHost failure isolation. It creates no second planner, page-per-World fork, universal ranking score, fake persistence or frontend Domain/AuthZ authority.

## 2. Permanent manual/DANTE capability law

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful product functions.

```text
MANUAL UI [M3-3] ----\
                       -> finite commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE receives no hidden mutation route. `dante-proposed` uses the same governed transaction model as manual interaction.

## 3. M3-1 — Composition Configuration Foundation — CLOSED / VALIDATED

Owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Config:

```text
schemaVersion / revision / worldId / ordered entries[]
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Commands:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Apply requires World match, revision freshness and exact base snapshot equality. Same revision with a structurally different base fails closed. No implicit merge/rebase exists.

Evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
```

## 4. M3-2 — Adaptive Candidate Resolver — CLOSED / VALIDATED

```text
validated M1 results
-> meaningful bounded opportunity
+ current M3 config
+ finite value signals
-> candidate resolver
-> WorldFocusCompositionCandidate[]
-> existing resolveWorldFocusCompositionPlan()
```

Finite signals remain:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No universal confidence/score/`aiRelevance` authority exists.

Precedence:

```text
hidden > ranking signals
pinned > adaptive budget
configured relative order > adaptive ranking
configured + null override -> opportunity.defaultProminence
configured + lead override -> lead
```

Pinned visible intent without meaningful current content remains explicit unresolved intent; no fake module is created.

Evidence:

```text
RED  c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAILURE
PASS b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
```

## 5. PRE-M3-3 safety — CLOSED / PASS

Closed gaps:

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

PRE-SCOPE:

```text
7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
```

Materialized:

```text
View -> explicit Customize
isolated route-scoped draft
lazy read of existing M1 seams
bounded meaningful opportunities
adopt / pin / unpin / hide / show / move / promote / restore
keyboard reorder independent of drag
focus + SR reorder feedback
Apply / Cancel
revision conflict / invalid-base fail closed
wide sidecar / compact allocator-owned overlay
```

No payload/reference/reasonCode/AuthZ/provider data is stored in composition config. No localStorage/server persistence exists.

Evidence:

```text
CODE/TEST 1978fe5c77c0e2661239372bf0f9bee238021faa
CI        33879774332 / run #907 PASS
77 / 77 web test files
376 / 376 web unit tests
294 modules / 851 dependencies / 0 violations
```

## 7. M3-4 Integrated Adaptive Composition — CLOSED / VALIDATED

PRE-SCOPE:

```text
688e1ab0c7a42f8d83274dedf5a2988a9388bda4
```

Normal World path:

```text
Situation / Continuity / Attention / Next / Comparison / Trajectory / Evidence-History
-> one bounded adaptive snapshot
-> meaningful opportunities
+ exact accepted M3-3 config owner
+ no invented M4/DANTE ranking signals
-> M3-2 candidate resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
-> M2 display-safe renderers
```

M3-4 proves sparse truthfulness, hidden precedence, pin budget survival without implicit reorder, promote without implicit reorder, configured user order, stable/non-user lead laws, unresolved pin without fabrication, unknown-kind local degradation, renderer failure isolation and keyboard access to the live scrollable main plane.

Integration deliberately exposed and corrected:

```text
planner prominence ordering vs configured user order
first order repair vs mixed stable/non-user lead laws
scroll-region keyboard accessibility
renderer invocation outside error boundary
```

Final evidence:

```text
CODE/TEST b10dc2bef8bab6ae863ce3c8331da6de96094a66
CI        33904052325 / run #934 PASS
79 / 79 web test files
387 / 387 web unit tests
299 modules / 891 dependencies / 0 violations
```

Detailed evidence: `world-focus-m3-4-integrated-adaptive-composition-review.md`.

## 8. M3 final hostile closure — CLOSED / PASS

PRE-SCOPE:

```text
2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
```

Final hostile test HEAD:

```text
d9c30a3c6148469b347754eab07dc2ade9be4c52
```

The final phase added no product feature and no production change. It attacks the combined projection -> opportunity -> config/customization -> resolver -> planner path.

New cross-layer pressure proves:

```text
partial content remains meaningful
empty/unavailable remains sparse
adopt/hide/pin/promote/move remain distinct inside one guarded transaction
arbitrary adopt payload/disclosure/aiRelevance does not survive config materialization
successful Apply increments once
stale revision fails with conflict
same-revision/different-base fails closed
200 deterministic hostile config/order/budget combinations remain deterministic
hidden entries never leak
visible pinned meaningful intent survives budget
selected user-owned entries preserve configured order
adaptive budget remains bounded
no duplicate plan instanceId
```

The final gate also retains prior 500-random composition and 500-width/surface-stack falsification, renderer isolation, unknown kinds, unresolved pins, responsive/a11y and frozen Timeline regression coverage.

Final evidence:

```text
Frontend CI 33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
Frontend + World Focus contracts PASS
Lint / Typecheck / Generated PASS
Production build PASS
Diff / mutation PASS
Mobile PASS
Chromium PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

Scope compare `2e69b1d... -> d9c30a3...` is linear: `ahead 2`, `behind 0`. Net change is exactly one test file; no production path changed.

Detailed evidence: `world-focus-m3-final-hostile-closure-review.md`.

## 9. Final M0 L5 disposition

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVED
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVED + validated order reconciliation
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + customization commands       M3-3 CLOSED / VALIDATED
M0-39 client revision/conflict/migration representation M3-1 + safety CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

## 10. Closure disposition

**M3 Adaptive World Composition is CLOSED / VALIDATED.**

M4 Contextual DANTE / D2–D6 is the next active phase. M4 must reuse the existing Workspace state/surface system and canonical app paths rather than creating hidden AI mutation, authorization or persistence routes.

Permanent barriers remain:

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
