# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — WS1–WS5 CONVERGENCE CLOSED / WS6 NEXT  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the durable high-detail handoff for continuing World Focus without reconstructing architecture from conversation memory.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-substrate-closure-plan.md
3. world-focus-ws0-substrate-inventory.md
4. world-focus-substrate-convergence-review.md
5. world-focus-substrate-convergence-corpus.md
6. world-focus-frontend-roadmap.md
7. this handoff
8. world-focus-evidence-index.md
```

---

# 1. Current sequencing

```text
WF0 structural route/shell             FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 VFX/visual treatment             CANDIDATE

B0 production foundation               ENGINEERING CLOSED
WR0 World product reverse engineering  CLOSED
WR1 DANTE <-> user reverse engineering COMPLETE / 7 gaps found
WR2 gap closure                        CLOSED / 7 of 7
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS

World Workspace Platform               ENGINEERING CLOSED
Platform HEAD                          6c441335a75bb913af8da1eda569d8094d38a539
Platform CI                            33549465793 PASS

D0 DANTE spatial/presence              ACCEPTED
D1 quiet invoke + compact composer      CLOSED FOR SEQUENCING
D1 code HEAD                           f17291de32e6bdced20536807b32928ec1be6aea
D1 CI                                  33552437179 PASS

WS0 Substrate Inventory                CLOSED BASELINE
WS1–WS5 Convergence Loop               ANALYTICALLY CLOSED
WS6 Universal Work Primitive Closure   NEXT
WS7 Executable Non-Visual Harness      NOT STARTED
WS8 Final Falsification                NOT STARTED

Materialization M0–M7                  BLOCKED UNTIL WS8
D2–D6                                  PRESERVED / MATERIALIZATION-DEFERRED
```

The old `D2 NEXT` sequence was intentionally paused, not rejected. D2–D6 resume during Materialization M4 after substrate closure.

---

# 2. Working standard

DANTE is not a prototype that will be cleaned up later.

For every bounded task:

```text
current authority
-> exact unresolved question
-> inspect real code/evidence
-> simulate/falsify
-> targeted external research only where genuinely open
-> alternatives + explicit decision/rejects
-> architecture/state ownership
-> smallest complete implementation when implementation belongs in the phase
-> responsive/a11y/security/performance/error/race handling
-> strict automated gates
-> real-browser acceptance when UI exists
-> human/user review when actually available/required
-> truthful closure disposition
-> documentation synchronization
```

Never fabricate:

```text
CI PASS
manual visual review
backend capability
provider success semantics
AI result
canonical effect completion
```

```text
analytical convergence != executable proof
CI green != human visual review
implemented != accepted
provider acknowledgement != canonical completion
```

---

# 3. Global North Star

DANTE:

> **DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.**

Compass:

> **Understand life. Shape what comes next.**

Operating capability chain:

```text
UNDERSTAND
-> DISCOVER
-> ORCHESTRATE
-> DECIDE
-> PLAN & COORDINATE
-> ACT
-> OBSERVE
-> LEARN & ADAPT
```

Not a mandatory workflow.

Permanent constraints:

```text
life, not task/calendar/metric, is the center
time is foundational but not container of all life
planned != Actual
effort != execution != outcome != Goal progress
observed pattern != confirmed preference
correlation != causation
AI inference != confirmed fact
Proposal != Decision
no universal Life Score
no punitive streak/fill-every-minute optimization
```

---

# 4. Domain / Logical / Physical barriers

Frontend convenience cannot reinterpret canonical semantics.

Important non-collapses:

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != DANTE canonical state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
client local state != canonical accepted effect
```

Rejected canonical shortcuts:

```text
universal Entity / Thing root
universal Relationship / generic edge
universal Rule / Fact / Version root
canonical EAV/property bag
```

World must never become a DB partition, canonical owner or ACL boundary merely because the frontend has `/worlds/:worldId`.

When future World work needs global DB truth, consult current protected-main DB authority at that time; do not trust an old Home-branch database snapshot and do not randomly merge/rebase main into Home.

---

# 5. Home / Worlds / Explore boundary

```text
HOME
cross-life compression / orientation / operation

MONDI OVERVIEW
view/manage Worlds as a system

WORLD FOCUS
scoped expansion / understanding / continuation of one World

EXPLORE / DETAIL
specialist / evidence / history / deeper depth
```

World Focus route:

`/worlds/:worldId`

It is not a Home overlay and not a chat route disguised as a World.

---

# 6. World definition

World Focus compass:

> **Understand this part of my life and continue from here.**

A World is:

> **A user-recognizable continuity context for a significant part of reality.**

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

World-worthiness pressure:

```text
recurring re-entry
continuity/history/intent
resumability
situational understanding
meaningful change
scoped decisions/actions
deeper exploration
stable human-recognizable identity
```

Never auto-map:

```text
Goal -> World
Project -> World
Person -> World
Asset -> World
Calendar -> World
Domain category -> World
```

World is not:

```text
canonical Domain owner
folder
life-area taxonomy
dashboard ontology
universal relation/entity container
DB partition
ACL/security boundary
AI memory bucket
chat room
mandatory Goal/time-range/KPI surface
```

Worlds overlap; the same canonical reality may be projected into several Worlds without duplication.

World relevance is a contextual prior, not ownership or authorization.

---

# 7. World Output Grammar

World Focus is question-driven, not widget-driven:

```text
O1  Orientation
O2  Situation
O3  Continuity / Resume
O4  Attention / Resolution
O5  Next
O6  Change
O7  Trajectory / Comparison [when meaningful]
O8  Evidence / History
O9  Explore
O10 Act / Decide
O11 Intelligence
```

A World need not answer all eleven.

```text
available meaningful authorized reality
-> meaningful questions now
-> rank
-> restrained subset
-> deeper evidence/action on demand
```

Never fill missing answers with fake cards, fake KPI, fake progress, recent-activity filler, AI prose, prompt suggestions or dummy charts.

Crucial WS6 rule:

```text
one Output Grammar family
!= automatically one work primitive
!= automatically one module
!= automatically one renderer
```

---

# 8. WR0–WR2 closed findings

WR0 falsified several candidate World definitions and the universal first-open time Lens.

WR1 found seven gaps around:

```text
World relevance definition
visible/DANTE basis coherence
cross-World escalation
DANTE presence/proactivity
deictic interaction cursor
Home/World attention routing
LLM-independent first open
```

WR2 closed all seven without finding a structural Domain/Logical/Physical/DB/Intelligence reopen.

Four-layer context model:

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT WORLD INTERACTION CURSOR / SESSION WHEN NEEDED
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

Cursor contains bounded references/hints only, never:

```text
DOM
React tree
secrets
authorization decision
copied canonical truth
provider credentials
durable DANTE Run state
```

Future Context Builder combines actual user purpose with Principal/Actor/recipient, sensitivity/disclosure/governance and freshness/material basis.

Current World is a relevance bias, not a reasoning prison.

---

# 9. Multi-actor conclusions

Collaboration is not single-user software multiplied by N.

Keep distinct:

```text
membership != visibility != authority
assignment/execution != responsibility/stewardship
RSVP/acceptance != Actual participation
shared context != access to private overlays
sent != delivered != seen != acknowledged != accepted != acted upon
```

Partial adoption and external/non-user participants are normal.

Recurring needs include:

```text
shared resource dependency
producer/consumer dependency
simultaneity
assignment/prerequisites
selective disclosure
shared canonical facts + private overlays
handoff
acknowledgement
responsibility
external participants
authority/consent
Actual participation
provisional vs confirmed
source provenance
conflicts
temporary delegation
```

The frontend may project these distinctions; real AuthZ/Authority/Consent enforcement remains upstream.

---

# 10. WF0 / WF-G3 / VFX

## WF0

**FROZEN / USER AUTHORIZED**

```text
APP SHELL / GLOBAL TOPBAR
└ route outlet
   └ /worlds/:worldId
      └ WORLD FOCUS SHELL
         ├ visual frame
         ├ rectangular workspace
         └ shell controls
```

Global Topbar is outside World ownership.

Future route-owned overlays may cover the World but do not resize/re-own Global Topbar or frozen workspace geometry.

## WF-G3

**LOCKED / USER AUTHORIZED**

Reference geometry remains:

```text
center 50/50
outer ellipse rx 52.25%, ry 90%
origin rx 50%, ry 87%
inner rx 47.75%, ry 84%
standard inline inset clamp(136px, 14vw, 224px)
compact inline inset clamp(76px, 18vw, 112px)
standard block inset clamp(32px, 5vh, 64px)
compact block inset 20px
compact <=720px
```

Rule:

> the visual skin must fit the geometry; the geometry does not chase the visual skin.

## WF-V4

VFX remains candidate and degrades before interaction/performance quality.

---

# 11. B0 reusable foundation

B0 established:

```text
model -> application -> ui -> route
strict typed frontend vocabulary
runtime validation seam
latest-only async commit protection
AbortSignal/cancellation
safe HTTPS external URL parsing
route error boundary
local renderer boundary
persistent rectangular workspace
container-query foundation
User Timing/open-to-usable instrumentation
a11y/focus/reduced-motion foundations
ornamental WebGL degradation
explicit dependency non-adoptions
backend/provider/LLM stop line
```

No generic repository/data-port abstraction was invented without a real read intent.

---

# 12. B1 Orientation

B1 originally carried a universal time Lens.

WR0 showed it was product-wrong across materially different Worlds.

Retained:

```text
World identity/orientation
route-owned active World
entry/exit lifecycle
loading/error/unavailable
responsive/a11y shell behavior
```

Removed fully:

```text
universal visible time Lens
Lens fixture capability
?time= route contract
Lens model/tests
Lens-only Session scaffolding
```

Lesson:

> When product semantics reject a capability, remove hidden infrastructure unless another real vertical independently earns it.

---

# 13. B2 Continuity / Resume

Question:

> **What is actually in motion and where can I continue?**

Permanent semantics:

```text
RECENT != RESUMABLE
LAST VIEWED != LAST MEANINGFUL CHECKPOINT
OPEN != IN MOTION
UNFINISHED != IMPORTANT
AI-GUESSED RELEVANCE != CONTINUITY FACT
```

First-open continuity requires recognizable thread identity + meaningful current/unfinished state + meaningful checkpoint.

No fake Resume action exists without a real continuation destination.

A previous premature implementation added an ungrounded Body `Mobility Reset` item and fake DANTE conversation surface; commit `aa495e38304ae26a4635e9c843cabbe1cb954f6e` reverted both.

Durable lesson:

> plausible != authorized/grounded.

B2 is implemented/automated PASS; integrated polish remains M6.

---

# 14. Workspace/module uncertainty research

Broad unknown-module research is already done.

Accepted:

```text
one shared World workspace platform
not page-per-World
finite approved module/surface registries
controlled specialist extension
no arbitrary model-generated executable UI
stable/adaptive/ephemeral distinct
AI cannot silently rewrite stable composition
DANTE can request Insight/Explore/deeper-surface intents
typed source drill-down on demand
large data bounded/aggregated before React
same canonical reality reused across Worlds
future persisted stable config needs revision/version/migration/concurrency
```

Specialist renderer only when generic primitives materially damage semantics/interaction.

Travel remains a possible specialist candidate only when integrated time/place/transport/booking/participation interaction earns it.

---

# 15. Existing executable Workspace Platform

Engineering closure:

```text
HEAD 6c441335a75bb913af8da1eda569d8094d38a539
CI   33549465793 PASS
```

Mechanics:

```text
stable/adaptive/ephemeral
origin system-default/user/dante-proposed/application-derived
lead/primary/supporting
wide/standard/compact
12-unit logical composition planner
finite module registry
finite surface registry
transient workspace reducer
singular bounded selection/context reference today
interaction generation
open/replace/promote/close surfaces
Escape ownership
blocking-tail barrier
expectedGeneration stale-intent guard
mainAllocation full/split
topLayer none/overlay/focus
interaction interactive/inert
sidecar/overlay/focus/dormant/external slots
ResizeObserver allocation
nested world-focus-main container ownership
wide sidecar real-width allocation
narrow sidecar workspace-local overlay degradation
modal/full-focus inert behavior
local failure isolation
```

Stress evidence:

```text
500 deterministic composition scenarios
500 deterministic allocation/surface-stack scenarios
```

Important limitation:

The current executable interaction cursor is singular. WS1–WS5 found that real comparison/deictic cases require future bounded primary + supporting refs. Do not claim this is already implemented.

The platform owns allocation inside the rectangular workspace; route-owned full-width DANTE materialization remains future D2/M4 work.

---

# 16. D0 / D1

## D0 — ACCEPTED

External product research synthesized:

> **AI availability is persistent; AI footprint is not.**

Accepted ladder:

```text
P0 quiet World + small invoke
P1 compact transient non-modal composer
ongoing + wide -> internal sidecar
ongoing + constrained/mobile -> route-owned focus overlay below Topbar
wide deep work -> explicit maximize
restore -> same logical conversation
explicit contextual use -> bounded context reference
```

Rejected universal models:

```text
always-open chatbot column
support-widget-only model
focus-overlay-only model
Home AI copied into World
fixed pane at every width
mobile conversation trapped in narrow World workspace
AI prose first-open
random prompt suggestions
```

## D1 — CLOSED FOR SEQUENCING

```text
HEAD f17291de32e6bdced20536807b32928ec1be6aea
CI   33552437179 PASS
```

Implemented:

```text
quiet invoke
>=44px target
no auto-open
registered dante-composer
peek + popover + user origin
non-modal semantics
World remains interactive
textarea focus
close/Escape focus restoration
truthful unavailable/pre-backend failure
draft preservation
no fake assistant/model/tool/effect
IT/EN
390px containment
axe wide/compact
```

Critical:

```text
global invoke -> contextReference: null
```

Current selection is not silently inherited.

D1 exposed and fixed a generic popover pointer interaction bug. Manual assistant visual review was not performed; user delegated sequencing closure on strong automated/browser evidence. Do not rewrite that history.

---

# 17. WS0 — Substrate Inventory

WS0 closed the truthful baseline:

```text
composition/workspace/surface mechanics = substantially executable
real application/work-semantic breadth  = partial
broad work-pattern knowledge            = research-evidenced
universal work primitive vocabulary     = not closed
whole-corpus executable oracle          = missing
```

Authority:

`world-focus-ws0-substrate-inventory.md`

---

# 18. WS1–WS5 Convergence Loop — CLOSED AS ONE MACRO-BLOCK

Authorities:

```text
world-focus-substrate-convergence-corpus.md
world-focus-substrate-convergence-review.md
```

The user explicitly required WS1–WS5 to be one indivisible block to avoid endless phase-by-phase churn.

Execution shape:

```text
simulation corpus
+ without/with DANTE stress
+ adversarial/edge stress
+ targeted reverse engineering
+ gap closure
-> repeat until converged
```

Evidence:

```text
44 primary scenarios
16 adversarial cross-product mutations
first confirmation discovers CG-32 revocation/disclosure gap
44 primary scenarios re-evaluated after hardening
20 additional alien confirmation cases
32 concern/closure records
final new material classes = 0
```

This is analytical closure, not executable WS7 proof.

---

# 19. Main convergence result — layered substrate

Do not turn all recurring needs into one work-primitive taxonomy.

```text
L0 higher authorities
   Domain / Logical / Physical / AuthZ

L1 work-semantic projections
   WS6 closes the finite vocabulary

L2 evidence / basis envelope
   source / provenance / basis / freshness / coverage / unresolved

L3 coordination / disclosure envelope
   participant state / responsibility / acknowledgement / private overlay

L4 interaction / cursor state
   World / generation / primary ref / bounded supporting refs / surface

L5 composition configuration
   stable/adaptive/ephemeral + personal/shared explicit configuration

L6 operation / effect presentation grammar
   proposal / confirmation / pending / ambiguity / reconciliation / receipt

L7 renderer / specialist extension
   finite code-shipped catalog + truthful fallback

L8 platform / user policies
   scale / offline / sync / a11y / notifications / performance / responsive
```

DANTE consumes, but does not own, these layers.

---

# 20. WS1–WS5 hardenings that must survive WS6

## 20.1 Evidence/basis

Important outputs may need source/evidence refs, material/basis ref, as-of/freshness, coverage/missingness and conflict/unresolved semantics.

Resource lifecycle status does not replace evidence basis.

## 20.2 Attention

```text
read/clear/dismiss/snooze/ack
!= underlying matter resolved
```

## 20.3 Decision preparation

Alternatives/constraints/trade-offs/evidence can be reusable work semantics without being the Domain Decision itself.

## 20.4 Resource/capacity

Keep requirement, availability, candidate, request/reservation/allocation intent, acceptance/binding and Actual use distinct.

## 20.5 Coordination/disclosure

Keep participant response, responsibility, assignment, acknowledgement, acceptance, Actual participation and private/shared information boundaries distinct.

## 20.6 Configuration/pinning

```text
personal favorite/shortcut
!= pinned/stable composition
!= saved typed query/view
!= shared config
!= source data
```

Persistent/shared configuration later needs ownership/audience + revision/version/migration/concurrency.

## 20.7 Effect presentation

Proposal/confirmation/request/pending/external ACK/ambiguity/reconciliation/completion cannot collapse.

## 20.8 Specialist fallback

Generic fallback is valid only when semantics and required interaction remain truthful. Missing essential specialist capability degrades safely rather than lying.

## 20.9 Conflicting claims

Keep incompatible claims/evidence unresolved if necessary. No LWW/provider-wins/AI-wins.

## 20.10 Multiple explicit interaction refs

Future cursor direction:

```text
primaryReference
+ bounded ordered supportingReferences
```

Primary owns deictic “this”. Supporting refs do not widen authorization and do not become payload bags.

## 20.11 Revocation/disclosure invalidation

This was the material gap that forced the loop restart.

```text
previous authorization
!= perpetual authorization
mounted/cached ref
!= continued eligibility
```

Authoritative app/context layer revalidates; revoked reference/result becomes unusable/redacted. Workspace generation is not AuthZ version.

---

# 21. Explicit non-universalizations

Do not resurrect:

```text
TemporaryMode universal lifecycle
offline/sync work primitive
universal World Lens/filter
large-data semantic primitive
a11y/low-attention semantic object
WorldItem
Thing
Widget
Fact root
generic Relationship/Edge
universal Register root
```

Real problems remain handled by the correct layer rather than deleted.

---

# 22. WS6 — CURRENT NEXT GATE

Question:

> **What is the smallest finite work-semantic vocabulary that expresses the converged corpus without duplicating Domain semantics or creating a generic escape hatch?**

Candidate pressure clusters, not final decisions:

```text
attention / unresolved work
choice / decision preparation
measurement / series
movement / balance / reconciliation
dependency / requirement
execution/session projection
pipeline/stage
capture/review
```

Every candidate must be classified as:

```text
universal work primitive
composition of smaller primitives
existing Domain projection pattern
interaction/configuration pattern
specialist extension
rejected universalization
```

WS6 should use deletion/merge pressure aggressively: if a candidate can be removed or composed without material loss across the corpus, do not keep it as a primitive.

WS6 is non-visual and must not start D2/UI materialization.

---

# 23. WS7 / WS8

## WS7

Build deterministic non-visual executable oracle over WS6 contracts.

Must exercise primitive applicability, absence/unresolved state, evidence basis, composition, primary/supporting refs, revocation seam, surface intent/blocking, responsive allocation, DANTE context-ref eligibility, late-result rejection, cross-World reuse and specialist fallback.

## WS8

Run full hostile corpus against executable substrate.

No ceremonial PASS. Any material gap returns to earliest necessary phase.

---

# 24. Materialization M0–M7

Only after WS8:

```text
M0 Materialization Mapping / Scope Freeze
M1 Core Non-Visual Production Materialization
M2 Shared Visual Primitive Layer
M3 Adaptive World Composition Materialization
M4 Contextual DANTE Materialization
M5 Contrasting Complete Worlds
M6 Integrated Product / Visual / Accessibility Review
M7 Pre-Backend Frontend Freeze / Handoff
```

M4 preserves D0/D1 and resumes:

```text
D2 adaptive ongoing conversation surface
D3 deterministic pre-backend conversation adapter
D4 explicit contextual/deictic invocation
D5 Insight
D6 Proposal/confirmation/receipt
```

M6 subsumes old D7 integrated review.

---

# 25. Backend / Intelligence stop line

Before explicit backend vertical:

```text
NO real World business API
NO World persistence/Alembic
NO provider runtime
NO model routing/streaming
NO canonical chat persistence
NO durable Run/Task backend
NO real tool/effect execution
NO fake success
NO provider acknowledgement treated as canonical completion
```

AI/context/runtime representation remains distinct from canonical truth.

No second canonical AI memory.

---

# 26. Operational repository rules

Authority order:

```text
1 protected-main executable/current accepted docs
2 durable main docs
3 active bounded unmerged branch record for its own scope
4 other current branch sources
5 historical evidence/Git
6 conversation
```

`NEW CHAT != NEW BRANCH`.

For each remote write:

```text
BRANCH
PRE-SCOPE exact SHA
CREATE exact paths
UPDATE exact paths
DELETE exact paths
PURPOSE
EXPLICITLY OUT OF SCOPE
```

Immediately before first write refetch active branch. If HEAD differs, stop/inspect/re-gate.

No merge/rebase/force/history rewrite/main mutation without explicit authorization.

No guessed status. Documentation is implementation.

Do not weaken TypeScript/lint/a11y/E2E gates.

---

# 27. Current branch/global DB caution

Home is a bounded frontend branch and may not contain latest protected-main PostgreSQL state.

Do not randomly merge/rebase main into Home.

If WS6 requires current global semantic/DB truth, read protected main at that time.

Before final integration, Home must reconcile against then-current main and branch-up-to-date policy.

---

# 28. Documentation reading rule

Current authority/evidence order:

```text
world-focus-current-checkpoint.md
world-focus-substrate-closure-plan.md
world-focus-ws0-substrate-inventory.md
world-focus-substrate-convergence-review.md
world-focus-substrate-convergence-corpus.md
world-focus-frontend-roadmap.md
world-focus-handoff.md
world-focus-product-contract.md
world-focus-platform-contract.md
world-focus-structural-contract.md
world-focus-geometry-contract.md
world-focus-delivery-methodology.md
world-focus-evidence-index.md
```

Old research status lines are historical unless explicitly marked current disposition.

---

# 29. Immediate instruction to next chat

Do not restart broad World simulations.

Do not implement D2.

Do not build beautiful cards/renderers yet.

Do not turn old discovery nouns into primitives automatically.

Resume at:

> **WS6 — Universal Work Primitive Closure. Use the converged 44-scenario corpus + 32 concern decisions, aggressively merge/delete candidate primitives, and stop only when the finite vocabulary has no generic escape hatch or semantic overlap.**
