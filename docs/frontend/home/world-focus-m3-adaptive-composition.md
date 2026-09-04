# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 CLOSED / VALIDATED / M3-4 NEXT  
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

Configuration is client composition metadata only. It carries no canonical Domain payload, disclosure/AuthZ authority, provider/runtime state, renderer function/JSX or generic property bag.

Finite schema disposition:

```text
current
migration-required
unsupported
```

Current finite commands after PRE-M3-3 safety:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Origins:

```text
manual
dante-proposed
```

Apply requires revision freshness and exact base snapshot equality. Same numeric revision with a different base fails closed; no implicit merge/rebase exists.

M3-1 original evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
72 / 72 web test files
344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations
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
-> meaningful opportunity extraction
-> current M3 composition config + finite value signals
-> candidate resolver
-> WorldFocusCompositionCandidate[]
-> existing resolveWorldFocusCompositionPlan()
```

Meaningful opportunities remain sparse. Empty/unavailable results create nothing. Opportunity metadata is only:

```text
instanceId
kind
defaultProminence
footprint
```

Finite value signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No `score`, confidence or `aiRelevance` authority.

User precedence:

```text
hidden > ranking signals
pinned > adaptive budget
configured relative order > adaptive ranking
configured + null override -> preserve opportunity.defaultProminence
configured + lead override -> lead
```

Pinned visible intent without meaningful content remains explicit `unresolvedPinned`; no fake module is created.

M3-2 evidence:

```text
RED  c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAILURE
PASS b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
74 / 74 web test files
356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations
```

## 5. PRE-M3-3 Customization Reachability Safety — CLOSED / PASS

The preflight exposed three real contract gaps before visual work:

```text
A. meaningful unconfigured opportunity could not enter customization
B. merely entering config could force supporting content to primary
C. Apply checked revision but not exact base snapshot identity
```

The safety layer therefore added bounded `adopt`, corrected configured prominence semantics and hardened Apply base identity. `restore` is base-relative; adopted-only entries disappear on restore.

Evidence:

```text
PRE-SCOPE 959c9077b4726a0a89b479d23ebe0edab216018b
RED       be63d49c43c88a491439b4014668a51c8ff8ad6b / CI 33861956558 EXPECTED FAILURE
PASS      7781c6751a455767595eaf159747da833117f8b2 / CI 33862549244 PASS
5 / 5 hostile safety tests PASS
75 / 75 web test files
362 / 362 web unit tests
288 modules / 804 dependencies / 0 violations
```

## 6. M3-3 Manual Customize UX — CLOSED / VALIDATED

### 6.1 Authorized scope and red-first proof

Authorized PRE-SCOPE:

```text
7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
```

Red sequence:

```text
f1b08fc1766f801d4573f81194a6e66a147c9433  test(home): add M3-3 customization red gate
fd1d503268608df89724e216f3a5fc59f697dbef  test(home): fix M3-3 red gate lint
CI 33875210161 EXPECTED FAILURE
```

Observed valid RED:

```text
all 362 pre-existing web unit tests PASS
5 / 5 new M3-3 product tests FAIL
failure reason: actual Customize product surface/orchestration absent
contract/lint/typecheck/architecture/generated checks otherwise PASS
```

The red contract was not weakened.

### 6.2 Materialized owners

New production owners:

```text
application/world-focus-composition-customization-read.ts
ui/world-focus-composition-customization-context.tsx
ui/world-focus-composition-customization-surface.tsx
ui/world-focus-composition-customization.css
```

Bounded integrations:

```text
ui/world-focus-page.tsx
ui/world-focus-core-surfaces.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

No M3-2 resolver was mounted into normal World composition; `getCoreWorldFocusComposition()` remains the nominal live composition owner until M3-4.

### 6.3 Read/application boundary

Customize lazily reads the already-owned M1 runtime seams:

```text
Situation
Continuity
Attention
Next
Comparison
Trajectory
Evidence / History
```

One bounded aggregate read immediately reduces those validated projection results through the M3-2 opportunity extractor. Returned customization opportunity data contains only the finite opportunity metadata; reference, payload, reason code and authorization/disclosure state do not cross into the returned set.

Cancellation is propagated through one internal AbortSignal to all seven owned readers. Abort is not converted into an empty semantic result.

### 6.4 View / Customize state ownership

```text
VIEW
accepted in-memory client composition config
no draft controls
normal live World remains pre-M3-4

CUSTOMIZE
explicit invocation
one isolated draft from accepted config
configured entries + currently meaningful opportunities
finite mutation commands
review / Apply / Cancel
```

Accepted in-memory state is not durable persistence.

The surface is a finite `composition-customize` registration in the existing surface registry. It requests `sidecar`; existing Workspace allocation owns compact fallback to overlay. No second surface platform or AppShell modal path exists.

### 6.5 Manual behavior proven

```text
adopt meaningful unconfigured opportunity
pin / unpin
hide / show
move up / move down
promote -> lead override only
restore existing -> exact base state/order
restore adopted-only -> remove from draft
```

Reorder is keyboard-operable without drag, deterministic, retains focus on the moved row and announces the resulting position through an assistive-technology status path.

Cancel:

```text
accepted config unchanged
revision unchanged
surface closes
World remains open
focus returns to exact invoker
```

Apply:

```text
calls applyWorldFocusCompositionDraft only
apply protected from duplicate concurrent activation
success -> accepted revision N + 1 exactly once
revision-conflict -> surface remains truthful, no merge/rebase
invalid state -> fail closed, no accepted mutation
```

### 6.6 Root-cause corrections during implementation

The implementation sequence deliberately let CI expose defects instead of weakening tests:

```text
a1e6709e375cdeab984e9625a326ae5fcdc4e919
CI 33876283735
-> TypeScript exposed post-await AbortSignal narrowing in aggregate read

c2f2f3e875c73a3ec54938c206f2fad873f5bc21
CI 33876436413
-> type/architecture passed; 365 tests passed; 2 focus-return tests failed

168d3c9565914c8fcc47a578c0750b030d42223f
CI 33876915226 FULL PASS
-> deterministic invoker focus restoration
```

Hardening-only commits:

```text
0dd816fe03fc45c5fe1799a5cd41e75c59c726ee  hostile M3-3 falsification
93effa1278b4a3d33c289f6467ee35551d0324b0  test lint correction only
1978fe5c77c0e2661239372bf0f9bee238021faa  exactOptional typing correction only
```

The latter corrections changed test harness correctness, not production semantics or assertions.

### 6.7 Final hostile closure evidence

```text
CODE/TEST HEAD                      1978fe5c77c0e2661239372bf0f9bee238021faa
Frontend CI                         33879774332 / run #907 PASS
Web test files                      77 / 77 PASS
Web unit tests                      376 / 376 PASS
Architecture                        294 modules / 851 dependencies / 0 violations
Frontend pre-production contracts   PASS
Lint                                PASS
Typecheck                           PASS
Generated-source drift              PASS
Production build                    PASS
Diff check                          PASS
Repository mutation check           PASS
Mobile Bundle                       PASS
Chromium                            PASS
frozen Timeline Firefox             PASS
Frontend CI Gate                    PASS
```

Browser hardening proves:

```text
wide sidecar behavior
compact overlay behavior
pressure widths 1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 /
  721 / 720 / 719 / 390
no horizontal document overflow
compact terminal target pressure
axe checks at wide and compact pressure
forced-colors operability
```

No motion-specific Customize behavior was added, so reduced-motion does not need a bespoke interaction branch.

Human visual acceptance remains **NOT PERFORMED**; automated green does not substitute for it.

### 6.8 Scope audit

PRE-SCOPE -> code/test hardening HEAD is linear and contains only the authorized M3-3 production/test/i18n/CSS paths. No Timeline, AppShell, Access/Auth, route tree, backend/API/DB/Alembic/AuthZ/provider/LLM or M3-4 integration path changed.

## 7. Current M0 L5 disposition

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + customization commands       M3-3 CLOSED / VALIDATED
M0-39 client revision/conflict/migration representation M3-1 + safety CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

## 8. M3-4 Integrated Adaptive Composition — NEXT / NOT STARTED

M3-4 is now the next engineering phase. It may integrate the already-validated layers:

```text
validated application projections
-> M3-2 meaningful opportunities
+ accepted M3 composition config
+ finite explicit value signals
-> M3-2 candidate resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
```

Required invariants:

```text
sparse remains sparse
hidden remains hidden
pinned user intent survives adaptive budget
configured relative order remains user-owned
configured supporting remains supporting unless explicitly promoted
unresolved pin does not fabricate content
unknown future World/module kinds remain viable
renderer failure remains local
no fake persistence
no frontend canonical-truth/AuthZ ownership
```

M3-4 requires a fresh live read-only preflight and a new exact bounded write gate. Do not infer its file scope from M3-3.

## 9. M3 final hostile closure and later sequence

```text
M3-4 integrated adaptive composition     NEXT / NOT STARTED
M3 final hostile closure                 BLOCKED BY M3-4
M4 Contextual DANTE / D2–D6             BLOCKED BY M3
M5 contrasting complete Worlds          BLOCKED BY M4
M6 integrated product/visual/a11y/perf  BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
BACKEND                                  AFTER M7 ONLY
```

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

## 11. Stop line

Do not start M3-4, M4/DANTE or backend work automatically from this closure. M3-4 starts only after a new bounded gate is explicitly authorized.
