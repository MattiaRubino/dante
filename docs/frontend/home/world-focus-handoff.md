# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 + M3-2 VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff is written so a new chat/agent can continue without reconstructing the project from conversation history. Read the repository live before every write; this file defines sequence and constraints, not a substitute for fresh code inspection.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-frontend-roadmap.md
4. world-focus-handoff.md
5. world-focus-evidence-index.md
6. world-focus-m2-shared-visual-primitives.md
7. world-focus-m0-materialization-mapping.md
8. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by current checkpoint authority.

## 1. Current sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED / VALIDATED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0 / D1                                    ACCEPTED / CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M3                                         ACTIVE
M3-1 composition configuration             CLOSED / VALIDATED
M3-2 adaptive candidate resolver           CLOSED / VALIDATED
PRE-M3-3 customization reachability safety CLOSED / PASS
M3-3 Manual Customize UX                   NEXT / NOT STARTED
M3-4 integrated adaptive composition       BLOCKED BY M3-3
M3 final hostile closure                   BLOCKED BY M3-4
M4 D2–D6                                   BLOCKED BY M3
M5–M7                                      BLOCKED BY SEQUENCE
BACKEND                                    BLOCKED UNTIL M7
manual visual acceptance                   NOT PERFORMED
```

## 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

Core thesis:

> **A World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, security boundary, AI memory bucket, chat room or mandatory Goal/KPI/time surface.

## 3. Permanent semantic barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend AuthZ
offline != source absent
timeout != semantic negative
Proposal != Decision != effect
provider ACK != canonical completion
Comparison != Decision
missing trajectory position != zero
AI output != fact
client composition config != Domain state
client revision != backend persistence revision
adopt != semantic truth/AuthZ/persistence
```

## 4. Closed M1/M2 substrate

M1 owns non-visual production semantics/application seams including open-ended World identity, bounded references, truthfulness/disclosure/effect/sync dimensions, O2/O5/O8 and WP-01..04.

M2 owns bounded display-safe binding, presentation grammar, WP renderers, O2/O5/O8 rendering and truthfulness qualifiers. Renderer availability never implies mandatory live mounting.

Workspace Platform remains the planner/placement authority. Do not create a second composition engine.

## 5. M3-1 configuration + transaction

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Configuration is revisioned client composition metadata only:

```text
schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Current finite customization language after PRE-M3-3 hardening:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Origins:

```text
manual
dante-proposed
```

One canonical path:

```text
manual UI [M3-3] ----\
                       -> commands -> isolated DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

No hidden DANTE mutation route.

## 6. `adopt` and `restore` — exact semantics

M3-3 must be able to customize a currently meaningful opportunity not yet represented in config. `adopt` exists only for this reachability.

Input must be a normalized/normalizable `WorldFocusCompositionOpportunity`. The draft receives only:

```text
instanceId
kind
visibility = visible
pinned = false
prominenceOverride = null
```

Operation history retains only:

```text
source
type = adopt
instanceId
kind
```

Do not pass or retain:

```text
projection
canonical Domain payload
context reference
reasonCode
disclosure/AuthZ state
provider/runtime state
confidence / score / aiRelevance
renderer code
arbitrary property bag
```

`restore` is relative to the base snapshot:

```text
existing base entry
-> restore exact base values and base position

adopted-only entry absent from base
-> remove it from working draft
```

This is intentional and tested.

## 7. Apply / Cancel — exact semantics

Cancel:

```text
DRAFT -> baseConfig
```

No committed side effect.

Apply:

```text
World mismatch
-> fail closed

current revision != draft.baseRevision
-> revision-conflict

same revision but current snapshot != draft.baseConfig
-> invalid base snapshot / fail closed

same revision + exact base snapshot
-> working config may become revision N+1
```

Snapshot identity includes schema version, revision, World id, ordered entry count and every entry field. No implicit merge/rebase.

## 8. M3-2 candidate resolver handoff

Owners:

```text
application/world-focus-composition-opportunities.ts
application/world-focus-composition-resolver.ts
```

Path:

```text
validated M1 results
-> meaningful bounded opportunities
+ current M3 config
+ finite value signals
-> WorldFocusCompositionCandidate[]
-> existing planner
```

Meaningful mapping:

```text
Situation ready + content                -> situation
Continuity ready/partial/stale + content -> continuity
Attention ready                          -> attention:<id> per primitive
Next ready + content                     -> next
Comparison ready                         -> comparison:<id> per primitive
Trajectory ready                         -> trajectory:<id> per primitive
Evidence/History any role content        -> evidence-history
empty / unavailable                      -> nothing
```

Finite signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No confidence/AI weighted score.

User precedence:

```text
hidden > signals
pinned > adaptive budget
configured order > adaptive ranking
```

Prominence after safety hardening:

```text
configured + no explicit lead override
-> opportunity.defaultProminence

configured + lead override
-> lead
```

So configuring/adopting a supporting module never silently makes it primary. Pin changes stability/ownership only.

Pinned visible config with no meaningful projection becomes `unresolvedPinned`, never an empty fake candidate.

## 9. PRE-M3-3 safety evidence

Original authorized PRE-SCOPE:

```text
959c9077b4726a0a89b479d23ebe0edab216018b
```

Red-first:

```text
HEAD be63d49c43c88a491439b4014668a51c8ff8ad6b
CI   33861956558 EXPECTED FAILURE
```

The new hostile file failed 5/5 expected cases while all 356 pre-existing web tests passed. Findings:

```text
1. unconfigured meaningful opportunities could not enter customization
2. configured supporting opportunity was forced to primary
3. same-revision different-base draft could Apply
4. adopt needed payload-stripping proof
5. adopt needed duplicate/blank/malformed fail-closed proof
```

Green closure:

```text
HEAD 7781c6751a455767595eaf159747da833117f8b2
CI   33862549244 PASS
5 / 5 hostile safety tests PASS
75 / 75 web test files
362 / 362 web unit tests
288 modules / 804 dependencies / 0 violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Gate PASS
```

The hostile safety file was not weakened.

There are two harmless connector side-effect commits in history that created then removed an empty `__dummy__` file. Final project tree is clean and final compare from the authorized PRE-SCOPE must not contain that file. Do not rewrite history to remove them; no force/rebase is authorized.

## 10. M3-3 — what the next chat must do

M3-3 is **manual Customize UX only**. It is not M3-4 live adaptive composition.

### First action: read-only preflight

Fresh-check branch HEAD and inspect live files before proposing any write:

```text
world-focus page/context/workspace/surface ownership
current module registry / CompositionHost
composition config + customization transaction
opportunity + resolver contracts
current Continuity/live core composition
current CSS/tokens/i18n
D0/D1 surface rules
responsive pressure tests
```

Do not assume file contents from this handoff.

### Then propose an exact bounded gate

State:

```text
branch
PRE-SCOPE exact SHA
CREATE
UPDATE
DELETE
purpose
red-first tests
explicit out-of-scope
```

The user expects this discipline.

### Product target

Build a polished explicit mode transition:

```text
VIEW
accepted composition
quiet nominal surface

CUSTOMIZE
isolated draft
configured entries + meaningful available opportunities
manual controls
changed-state visibility
Apply / Cancel
```

For an opportunity absent from config:

```text
opportunity -> adopt -> later commands
```

Never direct-patch config from arbitrary UI data.

### Required manual capabilities

```text
pin / unpin
hide / show
reorder
promote / restore
Apply / Cancel
revision conflict handling
invalid draft handling
```

Semantics must remain honest:

```text
hide != delete
pin != semantic truth
promote != semantic importance fact
restore != server reset
```

### Reorder quality bar

Keyboard path is mandatory and independent of drag. Preserve focus on the moved item and expose position/state to assistive technology.

Drag/drop is optional. If implemented, require pointer/touch/keyboard/screen-reader parity. Do not hand-roll fragile drag math just to create visual polish. Evaluate React Aria only if the actual M3-3 interaction justifies the dependency.

### Spatial behavior

Respect existing World surface architecture:

```text
wide
-> use existing wide sidecar/workspace surface patterns if appropriate

compact/mobile
-> use existing route-owned focus surface/overlay behavior
```

Do not modify WF0/WF-G3 or AppShell as collateral.

### Test obligations

Before closure pressure at minimum:

```text
View != Customize
enter does not mutate current
adopt unconfigured meaningful opportunity
adopt metadata defaults
no payload/reference/reasonCode leakage
pin/unpin draft only
hide/show draft only
reorder keyboard path
pointer/touch parity if drag exists
promote -> lead only
restore existing -> base state/order
restore adopted-only -> remove
Cancel -> exact base
Apply -> revision +1 once
stale revision -> conflict
same revision/wrong base -> fail-closed UX
sparse World remains sparse
unresolved pin honest
focus entry/return
screen reader labels/states
forced-colors
reduced-motion
no horizontal overflow
1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 / 721 / 720 / 719 / 390
```

Run full Frontend CI. Only after full green update authority docs and compare exact PRE-SCOPE -> final HEAD.

## 11. Explicit M3-3 out-of-scope

```text
NO M3-4 live candidate integration
NO localStorage fake durable persistence
NO server/cross-device persistence
NO DANTE D2–D6
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
NO generated route-tree edits
```

## 12. After M3-3

```text
M3-4 live adaptive composition
-> M3 final hostile closure
-> M4 D2–D6 contextual DANTE
-> M5 contrasting complete Worlds
-> M6 integrated product/visual/a11y/perf review
-> M7 pre-backend freeze
-> backend vertical integration
```

Human visual acceptance remains **NOT PERFORMED** until actually done.
