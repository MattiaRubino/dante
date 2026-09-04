# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 CLOSED / VALIDATED / M3-4 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Historical `NEXT`/`ACTIVE` prose is evidence only unless adopted here. Fresh live code inspection is still required before every new write scope.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-frontend-roadmap.md
4. world-focus-handoff.md
5. world-focus-evidence-index.md
6. current-checkpoint.md
7. world-focus-m2-shared-visual-primitives.md
8. world-focus-post-m1-safety-falsification-review.md
9. world-focus-m1-core-nonvisual-materialization-review.md
10. world-focus-m0-materialization-mapping.md
11. world-focus-contract-sequencing-supersession.md
12. product/platform/structure/geometry contracts as needed
```

# 2. Live sequence

```text
WF0                                      FROZEN / USER AUTHORIZED
WF-G3                                    LOCKED / USER AUTHORIZED
WF-V4                                    CANDIDATE
B0                                       ENGINEERING CLOSED
WR0–WR2                                  CLOSED
B1                                       CLOSED FOR SEQUENCING
B2                                       IMPLEMENTED / AUTOMATED PASS
Workspace Platform                       ENGINEERING CLOSED
D0                                       ACCEPTED
D1                                       CLOSED FOR SEQUENCING
WS0–WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0                                       CLOSED
M1                                       CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2                                       CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver         CLOSED / VALIDATED
PRE-M3-3 customization reachability safety CLOSED / PASS
M3-3 Manual Customize UX                 CLOSED / VALIDATED
M3-4 integrated adaptive composition     NEXT / NOT STARTED
M3 final falsification                   BLOCKED BY M3-4
M4 Contextual DANTE / D2–D6             BLOCKED BY M3
M5 complete contrasting Worlds          BLOCKED BY M4
M6 integrated product/visual/a11y/perf   BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
BACKEND                                  BLOCKED UNTIL M7
assistant manual visual review           NOT PERFORMED
```

# 3. Permanent product / semantic law

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World is a shared coordinate system between user and DANTE, not a shared source of truth.

Permanent non-collapses:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
AI output != accepted fact
Possibility != Goal != Proposal != Decision
planned != actual
Actual != Observation != Outcome
Proposal != Decision != effect
provider ACK != canonical completion
cancel != reverse != compensation
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
adopt != semantic truth != authorization != persistence
```

# 4. Existing engine ownership — preserve

Workspace Platform remains the only composition/placement engine and already owns:

```text
stable / adaptive / ephemeral
system-default / user / dante-proposed / application-derived
lead / primary / supporting
wide / standard / compact
12-unit deterministic packing
adaptive / ephemeral budgets
stable relative-order preservation
finite module registry
surface stack and deterministic allocation
local renderer failure isolation
```

M1 owns non-visual semantic/application substrate. M2 owns display-safe bindings, truthfulness qualifiers and finite accessible presentation vocabulary. M3 feeds these existing owners; it does not create a second planner or redefine Domain/AuthZ/persistence authority.

# 5. M3-1 / PRE-M3-3 transaction retained

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Configuration remains client composition metadata only:

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

Canonical command language:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Origins:

```text
manual
dante-proposed
```

Single transaction path:

```text
CURRENT CONFIG
  -> begin customization
  -> isolated DRAFT
  -> finite commands
  -> REVIEW
  -> Apply | Cancel
```

`adopt` accepts only an already-known meaningful opportunity and creates composition metadata only: visible, unpinned, `prominenceOverride = null`. It never imports canonical payload, references, disclosure/AuthZ state, provider state, confidence/score/AI relevance or renderer code.

`restore` is base-snapshot relative:

```text
base entry existed -> restore exact base values + base position
adopted-only entry absent from base -> remove from draft
```

Apply remains fail-closed:

```text
revision mismatch -> revision-conflict
same revision + different base snapshot -> invalid base / FAIL CLOSED
same revision + exact base snapshot -> revision N+1
```

No implicit merge/rebase exists.

# 6. M3-2 result retained

M3-2 remains a pre-planner/pre-renderer boundary:

```text
validated meaningful M1 results
  -> bounded opportunities
  + current composition config
  + finite explicit value signals
  -> WorldFocusCompositionCandidate[]
  -> existing planner
```

Opportunity metadata remains only:

```text
instanceId
kind
defaultProminence
footprint
```

Sparse remains sparse. Renderer presence never creates an opportunity. Configuration precedence remains:

```text
hidden > signals
pinned > adaptive budget
configured relative order > adaptive ranking
configured + null override -> preserve opportunity.defaultProminence
configured + lead override -> lead
```

Pinned intent without a meaningful current projection remains explicit unresolved intent, never fabricated content.

# 7. M3-3 Manual Customize UX — CLOSED / VALIDATED

Authorized M3-3 PRE-SCOPE:

```text
7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
```

M3-3 materialized a manual/non-AI customization experience over the canonical M3-1 transaction rather than creating a UI-only state model.

Production ownership added:

```text
application/world-focus-composition-customization-read.ts
ui/world-focus-composition-customization-context.tsx
ui/world-focus-composition-customization-surface.tsx
ui/world-focus-composition-customization.css
```

Bounded existing owners updated:

```text
ui/world-focus-page.tsx
ui/world-focus-core-surfaces.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

Behavior now proven:

```text
View mode != Customize mode
explicit Customize invocation
accepted config unchanged while editing
single isolated route-scoped draft
lazy aggregate read of existing M1 Situation / Continuity / Attention / Next /
  Comparison / Trajectory / Evidence-History readers
aggregate read immediately reduces projections to bounded opportunity metadata
no payload/reference/reasonCode/AuthZ leakage into customization opportunity output
meaningful unconfigured opportunity -> explicit adopt
pin / unpin / hide / show / move / promote / restore mutate draft only
move is deterministic and has a non-drag keyboard-operable path
focus remains on the moved item and screen reader receives useful position state
promote creates only prominenceOverride = lead
restore existing -> exact base state/order
restore adopted-only -> removes from draft
Cancel -> exact accepted/base state, no revision bump, focus returns to invoker
Apply -> canonical application operation exactly once, revision N -> N+1
revision-conflict -> no merge/rebase
invalid/same-revision wrong-base path -> fail closed
sparse World remains sparse
no localStorage/backend/fake persistence
normal live composition remains pre-M3-4 core composition
```

The finite customization surface is registered in the existing surface registry and requested as a sidecar. Existing Workspace allocation owns compact degradation to overlay; no AppShell modal hack or new surface platform was introduced.

# 8. M3-3 red-first / correction / closure evidence

Valid RED sequence:

```text
RED test commit      f1b08fc1766f801d4573f81194a6e66a147c9433
RED lint-fix commit  fd1d503268608df89724e216f3a5fc59f697dbef
CI                   33875210161 EXPECTED FAILURE
pre-existing web     362 / 362 PASS
new M3-3 tests       0 / 5 PASS
failure cause        Customize product behavior absent
```

The red contract was not weakened.

Production/hardening sequence intentionally exposed and fixed root causes:

```text
a1e6709e375cdeab984e9625a326ae5fcdc4e919
  initial M3-3 shell; CI 33876283735 exposed AbortSignal TypeScript issue

c2f2f3e875c73a3ec54938c206f2fad873f5bc21
  preserved internal cancellation semantics; CI 33876436413 then exposed
  two real focus-return failures while 365 tests passed

168d3c9565914c8fcc47a578c0750b030d42223f
  deterministic invoker focus restoration; CI 33876915226 FULL PASS

0dd816fe03fc45c5fe1799a5cd41e75c59c726ee
93effa1278b4a3d33c289f6467ee35551d0324b0
1978fe5c77c0e2661239372bf0f9bee238021faa
  hostile hardening tests + test-harness lint/typing fixes only
```

Final M3-3 hardening evidence:

```text
CODE/TEST HEAD                     1978fe5c77c0e2661239372bf0f9bee238021faa
Frontend CI                        33879774332 / run #907 PASS
Web test files                     77 / 77 PASS
Web unit tests                     376 / 376 PASS
Architecture                       294 modules / 851 dependencies / 0 violations
Frontend pre-production contracts  PASS
Lint                               PASS
Typecheck                          PASS
Generated-source drift             PASS
Production build                   PASS
Diff check                         PASS
Repository mutation check          PASS
Mobile Bundle                      PASS
Chromium                           PASS
frozen Timeline Firefox            PASS
Frontend CI Gate                   PASS
```

Browser hardening includes wide sidecar, compact overlay, all pressure widths `1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 / 721 / 720 / 719 / 390`, no horizontal overflow, compact terminal-target pressure, axe checks and forced-colors operability.

Automated green is not human visual acceptance. Human visual acceptance remains **NOT PERFORMED**.

# 9. Final M3-3 scope audit

Compare from authorized PRE-SCOPE through code/test hardening HEAD is linear (`ahead`, no behind) and contains only authorized M3-3 paths:

```text
apps/web/e2e/world-focus-composition-customization.spec.ts
apps/web/src/features/world-focus/application/world-focus-composition-customization-read.ts
apps/web/src/features/world-focus/application/world-focus-composition-customization-read.test.ts
apps/web/src/features/world-focus/ui/world-focus-composition-customization-context.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-customization-surface.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-customization.css
apps/web/src/features/world-focus/ui/world-focus-composition-customization.test.tsx
apps/web/src/features/world-focus/ui/world-focus-core-surfaces.tsx
apps/web/src/features/world-focus/ui/world-focus-page.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

No Timeline, AppShell, Access/Auth, generated route-tree, backend/API/DB/Alembic/AuthZ/provider/LLM or M3-4 production path changed.

# 10. Current gate — M3-4 Integrated Adaptive Composition

M3-4 is **NEXT / NOT STARTED**. It is the first phase allowed to replace the nominal fixed core-composition feed with the already-built meaningful-opportunity/config/resolver path.

Expected integrated direction:

```text
validated M1 projection results
-> M3-2 meaningful opportunities
+ accepted M3 composition config
+ finite value signals
-> M3-2 candidate resolver
-> existing Workspace planner
-> finite module registry
-> CompositionHost
```

M3-4 must preserve:

```text
sparse remains sparse
hidden remains hidden
pin survives adaptive budget
configured relative order remains user-owned
configured supporting remains supporting unless explicitly promoted
unresolved pin does not fabricate content
unknown future World/module kinds remain representable
renderer failure remains local
no fake persistence
no frontend AuthZ/canonical-truth invention
```

Before M3-4 writes, perform a fresh read-only preflight and propose a new bounded gate with exact branch HEAD / PRE-SCOPE / CREATE / UPDATE / DELETE / tests / out-of-scope. M3-4 must not be started implicitly by M3-3 closure.

# 11. Stop lines

```text
NO M3 final closure before M3-4
NO M4 / D2–D6 before M3 closes
NO fake localStorage persistence
NO durable server/cross-device persistence yet
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral changes
NO generated route-tree edits
NO claim of human visual acceptance from CI
```
