# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / PRE-M3-3 CUSTOMIZATION SAFETY CLOSED / PASS / M3-3 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Historical `NEXT`/`ACTIVE` prose remains evidence only unless adopted here. Do not infer current sequencing from old review files.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-frontend-roadmap.md
4. world-focus-handoff.md
5. world-focus-evidence-index.md
6. world-focus-m2-shared-visual-primitives.md
7. world-focus-post-m1-safety-falsification-review.md
8. world-focus-m1-core-nonvisual-materialization-review.md
9. world-focus-m0-materialization-mapping.md
10. world-focus-contract-sequencing-supersession.md
11. product/platform/structure/geometry contracts as needed
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
M3-3 Manual Customize UX                 NEXT / NOT STARTED
M3-4 integrated adaptive composition     BLOCKED BY M3-3
M3 final falsification                   BLOCKED BY M3-4
M4 Contextual DANTE / D2–D6             BLOCKED BY M3
M5 complete contrasting Worlds          BLOCKED BY M4
M6 integrated product/visual/a11y/perf   BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
BACKEND                                  BLOCKED UNTIL M7
assistant manual visual review           NOT PERFORMED
```

# 3. Evidence anchors

```text
M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2 final hostile closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
70 / 70 web test files; 332 / 332 web unit tests
279 modules / 770 dependencies / 0 violations

M3-1 validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations

M3-2 validated code
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
74 / 74 web test files; 356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations

PRE-M3-3 red-first safety proof
PRE-SCOPE 959c9077b4726a0a89b479d23ebe0edab216018b
HEAD      be63d49c43c88a491439b4014668a51c8ff8ad6b
CI        33861956558 EXPECTED FAILURE
new hostile safety tests 0 / 5 PASS
all 356 pre-existing web unit tests PASS

PRE-M3-3 safety closure
HEAD 7781c6751a455767595eaf159747da833117f8b2
CI   33862549244 PASS
hostile safety tests 5 / 5 PASS
75 / 75 web test files; 362 / 362 web unit tests
288 modules / 804 dependencies / 0 violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

The red safety test was not weakened between red and green.

# 4. Closed semantic/presentation substrate retained

M1 owns validated non-visual semantics and application seams. M2 owns bounded display/presentation and finite renderer vocabulary. Workspace Platform remains the only planner/packing/placement owner.

Permanent non-collapses:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
timeout != semantic negative
offline != source absent
provider ACK != canonical completion
Proposal != Decision != effect
Comparison != Decision
missing trajectory position != zero
AI output != fact
client composition config != canonical Domain state
client revision != backend persistence revision
```

# 5. Existing composition engine — preserve

Workspace Platform already owns:

```text
stable / adaptive / ephemeral
system-default / user / dante-proposed / application-derived
lead / primary / supporting
wide / standard / compact
12-unit deterministic packing
adaptive / ephemeral budgets
stable relative-order preservation
finite module registry
local renderer failure isolation
```

M3 feeds this engine. M3 must not create a second planner.

# 6. M3-1 + customization reachability contract

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Configuration:

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

Current finite command language:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Finite origins:

```text
manual
dante-proposed
```

Manual and future DANTE proposals use the **same** transaction path:

```text
CURRENT CONFIG
  -> begin customization
  -> isolated DRAFT
  -> finite commands
  -> REVIEW
  -> Apply | Cancel
```

`adopt` exists because M3-3 must be able to customize a meaningful adaptive opportunity that is not already present in config. It accepts only an already-known `WorldFocusCompositionOpportunity`, normalizes it through the existing constructor, and creates:

```text
instanceId
kind
visibility = visible
pinned = false
prominenceOverride = null
```

It never imports projection data, canonical payload, references, disclosure/AuthZ state, confidence, `aiRelevance`, provider data or renderer code. Operation history retains only `source/type/instanceId/kind`.

`restore` is base-snapshot semantics:

```text
entry existed in base
-> restore exact base state + base position

entry was adopted and absent from base
-> remove it from working draft
```

`hide != delete`; `pin != semantic truth`; `promote != semantic truth`.

# 7. Apply semantics after PRE-M3-3 hardening

Apply now proves both revision freshness and base identity:

```text
current.revision != draft.baseRevision
-> revision-conflict { baseRevision, currentRevision }

current.revision == draft.baseRevision
AND current snapshot structurally equals draft.baseConfig
AND working/base revisions equal baseRevision
-> Apply allowed -> config revision N+1

same numeric revision but base snapshot differs
-> invalid draft base snapshot / FAIL CLOSED
```

Snapshot equality covers schema version, revision, World id, entry count/order and every entry field (`instanceId/kind/visibility/pinned/prominenceOverride`). No implicit merge exists.

# 8. M3-2 result retained + corrected precedence

M3-2 owns:

```text
validated meaningful M1 results
  -> bounded opportunities
  + current composition config
  + finite explicit value signals
  -> WorldFocusCompositionCandidate[]
  -> existing planner
```

Meaningful opportunities remain sparse. Empty/unavailable results do not create modules. Opportunity metadata carries only:

```text
instanceId
kind
defaultProminence
footprint
```

Finite ranking signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No universal confidence, AI relevance or weighted score.

Precedence:

```text
hidden > signals
pinned > adaptive budget
configured relative order > adaptive ranking
```

Corrected prominence rule:

```text
configured + prominenceOverride = null
-> preserve opportunity.defaultProminence

configured + prominenceOverride = lead
-> lead
```

Config presence alone never means primary. Pin affects stability/ownership; it does not imply importance. Signals rank/elevate only unconfigured opportunities. Pinned visible intent without a meaningful projection remains explicit `unresolvedPinned`, never fabricated content.

# 9. Why PRE-M3-3 existed

The M3-3 preflight found three real contract defects before visual work:

```text
1. M3-1 could mutate only entries already present in config.
   -> a new meaningful adaptive opportunity could not enter Customize.

2. M3-2 treated any configured non-lead entry as primary.
   -> merely materializing/adopting a supporting Comparison/Trajectory changed its prominence.

3. Apply checked revision but not exact base snapshot identity.
   -> a draft from a different same-revision snapshot could be applied.
```

The hostile test also required adopt to reject/strip arbitrary payload and reject duplicate/blank/malformed targets. All five hostile cases now pass.

# 10. M0 M3 disposition state

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + customization commands       MODEL/SAFETY CLOSED; UI M3-3 NEXT
M0-39 client revision/conflict/migration representation M3-1 + safety CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

# 11. Current gate — M3-3 Manual Customize UX

M3-3 is next but unstarted. It must create the actual manual product experience over the validated transaction model.

Mandatory behavior:

```text
View mode and Customize mode are distinct
enter Customize explicitly
construct a real isolated draft
show currently configured entries and meaningful available opportunities
unconfigured meaningful opportunity -> adopt before later mutations
pin/unpin
hide/show
reorder
promote/restore
indicate changed/dirty state without fake persistence
Apply only through applyWorldFocusCompositionDraft
Cancel returns base snapshot
revision-conflict and invalid-state UX
focus entry/return
keyboard operability
touch operability
screen-reader semantics
responsive geometry
```

Reorder must have a keyboard-accessible non-drag path. Drag/drop may be layered later only with equivalent mouse/touch/keyboard/screen-reader behavior. Do not add React Aria automatically; evaluate it during M3-3 only if the actual interaction earns it.

# 12. M3-3 testing obligations

At minimum pressure:

```text
entering Customize does not mutate current config
unconfigured opportunity is adoptable
adopted entry has visible/unpinned/null override defaults
pin/unpin/hide/show are draft-only
move is deterministic and keyboard-operable
promote only creates lead override
restore existing -> base state/order
restore adopted-only -> removes from draft
Cancel -> exact base snapshot
Apply -> revision +1 exactly once
stale revision -> revision-conflict
same revision/different base -> fail-closed UX path
manual and dante-proposed state model remains one canonical command language
raw reference/reasonCode/payload never becomes UI copy
sparse World remains sparse
unresolved pin does not become fake content
720 / 719 / 390 and desktop pressure
no horizontal overflow
forced-colors and reduced-motion behavior
```

M3-3 does **not** mount the M3-2 candidate resolver into normal live World composition. That is M3-4.

# 13. Stop lines

```text
NO M3-4 live integration
NO fake localStorage persistence
NO durable server persistence/cross-device sync
NO DANTE D2–D6 before M4
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral changes
NO generated route-tree edits
```

A fresh bounded write gate is required before M3-3 production writes.
