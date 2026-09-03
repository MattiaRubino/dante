# DANTE — World Focus Product Contract

**Status:** CURRENT PRE-BACKEND PRODUCT AUTHORITY — SEMANTICS CURRENT / HISTORICAL GATE PROSE SUPERSEDED  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This document is the current product authority for World Focus. It incorporates the WR0/WR1/WR2 reverse-engineering results and the final B1/B2 dispositions. Historical review documents are evidence only where they do not conflict with this contract.

**Sequencing note:** product semantics in this file remain authoritative. Phase-time statements in section 25 that describe the contextual DANTE spatial review as the immediate/current gate are historical. D0 and D1 are closed, D2–D6 are deferred to M4, M1 is closed, and current phase sequencing is owned by `world-focus-current-checkpoint.md`, `world-focus-m1-operational-handoff.md` and `world-focus-contract-sequencing-supersession.md`.

## 1. Product compass

World Focus exists for:

> **Understand this part of my life and continue from here.**

A World is:

> **a user-recognizable continuity context for a significant part of reality. World Focus projects the authoritative and derived DANTE realities relevant to that context so the user can understand where things stand, recover or resume what matters, notice material change or attention needs, explore deeper evidence, and continue through decisions/actions when useful.**

A World is not:

```text
life-area ontology
folder
project template
dashboard
metric collection
universal entity container
database partition
security boundary
AI memory bucket
chat room
mandatory Goal/progress surface
mandatory time range
```

## 2. World-worthiness

A context is a strong World candidate when several are true:

```text
recurring re-entry value
continuity worth recovering
resumability
situational understanding across related reality
meaningful change over time
scoped decisions/actions
history/evidence worth exploring
stable human-recognizable identity
```

No canonical owner automatically becomes a World.

Rejected automatic mappings:

```text
Goal -> World
Project -> World
Person -> World
Asset -> World
Calendar -> World
Domain category -> World
```

Worlds are curated continuity entry points, not an exhaustive tree.

## 3. Home / World / Explore / Search

```text
HOME
cross-life compression and operation
“What matters across my life now?”

WORLD FOCUS
scoped expansion, understanding and continuation
“What is happening here and how do I continue?”

EXPLORE / DETAIL
depth and evidence
“Show me everything relevant behind this.”

SEARCH
exact-target discovery/navigation where known-item lookup is the intent
```

World Focus must not become Home with a scope filter.

## 4. Dual role — user and DANTE

For the user, a World is a low-reentry-cost surface for one meaningful context.

For DANTE, a World is a bounded contextual coordinate that biases relevance/interaction toward that context.

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

World context helps DANTE with:

```text
relevance prior
deictic/ambiguity resolution
continuity across interactions
retrieval starting point
source/detail context
scoped Insight
proposal target framing
returning results to the correct surface
```

It does not determine canonical truth, authorization, disclosure or operation permission.

## 5. Four-layer World context model

Never collapse:

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT WORLD INTERACTION CURSOR / SESSION WHEN ACTUALLY NEEDED
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

### 5.1 Identity / purpose

Presentation identity such as World reference, user-recognizable name, concise purpose and bounded presentation profile.

Name alone never proves semantics.

### 5.2 Stable relevance

Answers:

> What kinds of authoritative DANTE reality are intentionally relevant to this continuity context?

May derive from typed product/application configuration, explicit anchors, system defaults, approved DANTE proposals or other bounded accepted configuration.

It is not canonical membership, arbitrary SQL, authorization or a generic relation table.

### 5.3 Interaction cursor/session

Transient context only when a real interaction requires it, e.g. selection, Explore, Insight, contextual DANTE conversation.

May conceptually hold:

```text
active World reference
interaction generation
current query/Lens if applicable
primary selected/context projection/source reference
bounded ordered supporting context references where materially needed
current Insight/Explore reference
entry/surface context
```

It does not duplicate canonical source data or serialize React/DOM state as truth.

The active World itself is currently route-owned; do not create a Session object only to mirror route state.

### 5.4 Authorized purpose-scoped DANTE context

Built by the authoritative application/Context Builder from:

```text
World identity/purpose
stable relevance
current interaction cursor
actual request/purpose
Principal / Actor / recipient
sensitivity/disclosure/governance
freshness/material basis
```

Only this minimized reconstructed context is usable by DANTE.

## 6. World Output Grammar

World Focus is question-driven, not widget-driven.

Output/question families:

```text
O1  Orientation            What am I looking at?
O2  Situation              What is currently true/relevant here?
O3  Continuity / Resume    What is in motion and where can I continue?
O4  Attention / Resolution What needs attention/decision/correction?
O5  Next                   What is coming next here?
O6  Change                 What changed?
O7  Trajectory/Comparison  Where is this going vs a meaningful baseline? [optional]
O8  Evidence / History     What is this based on / what happened before?
O9  Explore                What else can I inspect here?
O10 Act / Decide            What can I do from here?
O11 Intelligence           What can DANTE help me understand/compare/simulate/improve?
```

A World does not need all eleven.

Correct rule:

```text
meaningful available answers
-> rank by current value
-> render restrained subset
-> deeper material on demand
```

Never fill missing grammar with invented cards/KPIs/AI prose.

## 7. First-open contract

Core first-open value must not require an LLM completion.

```text
bounded authorized application projections
-> output/question classification
-> initial composition resolver
-> user-visible first screen
```

DANTE may explain, summarize, compare, propose or act afterward.

Sparse Worlds remain sparse. Dormant Worlds do not manufacture urgency. Completed contexts may emphasize history/outcomes/artifacts rather than fake next actions.

## 8. Dynamic composition

Potential ranking inputs include:

```text
stable/pinned user importance
material consequence
immediacy/time sensitivity
resumability value
meaningful change
explicit current user intent/selection
validated material-basis / evidence / provenance quality where the owning projection explicitly defines it
```

There is **no universal confidence score**. Evidence, provenance, integrity/attestation, freshness, coverage/conflict and validity are separate dimensions and must not be collapsed into a generic confidence number for ranking.

Hard reject:

```text
AI relevance score alone decides page composition
universal confidence score silently decides page composition
```

Stable user-owned content remains predictable. Adaptive content is bounded. Ephemeral content stays temporary unless deliberately promoted through accepted configuration semantics.

## 9. Module / renderer meaning

A module is a controlled renderer for a validated projection, not a product ontology.

```text
ModuleKind != Domain owner
ModuleKind != World question
ModuleConfig != canonical source data
ModuleProjection != canonical source data
```

Finite registered renderers are allowed. Arbitrary remote JSX/HTML/JavaScript or model-generated executable UI is forbidden.

Specialist renderers are justified only when generic rendering would materially damage semantics/UX.

## 10. DANTE presence semantics

World Focus is useful without AI, but DANTE is native to the experience.

WR2 established presentation depths:

```text
P0 QUIET
no AI output required

P1 INVOKE
user explicitly asks DANTE

P2 CONTEXTUAL ENTRY
small meaningful contextual question/action entry when useful

P3 INSIGHT
bounded evidence-backed interpretation

P4 PROPOSAL
specific suggested change/scenario

P5 ACTION / RECEIPT
governed operation/result state
```

These are semantic/product depths, not a fixed geometry.

No AI slot generates content merely because it exists.

## 11. DANTE result distinctions

Do not collapse everything into `AI response`.

Keep distinguishable:

```text
SOURCE-BACKED FACT / PROJECTION
DANTE ANSWER / EXPLANATION
DANTE INSIGHT / DERIVED INTERPRETATION
CANDIDATE / UNRESOLVED INTERPRETATION
SCENARIO / RECOMMENDATION
PROPOSAL
GOVERNED EFFECT / RECEIPT
```

Permanent boundaries:

```text
AI output != accepted fact
AI proposal != Decision
Decision != effect
request accepted != effect completed
provider acknowledgement != canonical completion
```

## 12. Deictic interaction

Inside a World the user should eventually be able to say:

```text
“questa”
“perché?”
“continua da qui”
“confronta con prima”
“aprimi la fonte”
“spostalo”
```

without restating identity.

The frontend passes bounded references/hints; authoritative context is reconstructed.

A DANTE run stays bound to its initiating World/cursor generation. Switching World must not attach a late result to the new context.

## 13. Coherent basis / freshness

Visible projections and contextual DANTE results need compatible basis semantics.

Important values retain as applicable:

```text
request/projection generation
basis/material state reference
as-of/freshness
provider/source freshness
```

DANTE may reuse a compatible visible basis or re-read/revalidate.

If refreshed reality materially changes, the result must make that new basis truthful rather than answer as if the old visible state remained current.

Provider unavailable/timeout never becomes a semantic negative.

## 14. Cross-World orchestration

A World is the default relevance bias, not a reasoning prison.

Start local; expand only when the actual user purpose materially requires authorized broader context.

Examples:

```text
Travel -> Finance for affordability
Music -> Work/Calendar/Capacity for release feasibility
Study -> Work/Capacity for plan realism
Vehicle -> Finance for repair trade-off
```

Hard rejects:

```text
activeWorldId = ACL
World question = permission for whole-life retrieval
```

When broader context materially changes the conclusion, expose enough of that broader basis for the user to understand why.

## 15. Home ↔ World attention altitude

The same underlying matter may appear at different altitude:

```text
Home
compressed cross-life signal

World
scoped explanation/context/options/action
```

Presentation dismissal/snooze does not silently become semantic resolution.

## 16. Lens disposition

The old B1 universal visible temporal Lens was rejected and **removed completely**.

Current rule:

Show a World-level Lens only when multiple prominent projections genuinely share the same dimension/semantics and changing it has obvious value.

Otherwise scope belongs to module-local control, Insight, Explore, contextual query or transient session state.

No Lens/session infrastructure is kept merely “for later”. Reintroduce it only when a real vertical proves the need.

## 17. Same reality / multiple Worlds

Correct:

```text
one canonical reality
+ multiple bounded World projections/configurations
```

World relevance never transfers canonical ownership.

Removing a World/module never deletes source reality.

## 18. Multi-actor / privacy

```text
shared World context != access to every actor's private context
World relevance != Visibility
UI hiding != authorization
```

Projection/context must be disclosure-safe before React/DANTE presentation.

## 19. Lifecycle

World lifecycle is product/presentation state, not Domain ontology.

Possible concepts:

```text
emerging
active
dormant
completed-context
archived/unpinned
```

Names are not frozen.

```text
dormant != failed
completed != needs fake next action
archived != delete canonical reality
```

## 20. AI/provider unavailable

AI unavailable:

```text
World remains understandable and operable
DANTE-only surfaces degrade locally
```

Provider unavailable:

```text
accepted canonical reality remains usable
provider projection reports truthful stale/unavailable state
unrelated World content remains available
```

## 21. Consequential actions

World context may target an operation but never authorizes it.

Existing governed operation/effect architecture remains authoritative:

```text
caller intent
-> target/effect interpretation
-> expected state/freshness
-> governance/autonomy/confirmation
-> execution
-> canonical/provider/runtime result axes
-> reconciliation where needed
```

Navigating away from React is not semantic effect cancellation.

## 22. Unknown future Worlds

Unknown World behavior must be sparse and safe.

```text
show identity
show only justified projections
no fake KPI
no fake Goal
no forced Lens
DANTE may propose linking/configuration
DANTE does not silently establish truth/membership
```

## 23. B1 final disposition

```text
World Orientation                    KEEP
route-owned active World             KEEP
entry/exit lifecycle                 KEEP
loading/error/unavailable            KEEP
responsive/a11y foundation           KEEP
visible global time Lens             REMOVED
Lens fixture capability              REMOVED
URL time contract                    REMOVED
Lens model/tests                     REMOVED
Lens-only Session snapshot           REMOVED
user structural/function gate        ACCEPTED
micro visual polish                  DEFERRED to integrated composition review
sequencing gate                      CLOSED
```

## 24. B2 Continuity / Resume disposition

B2 implements the first real question-driven projection:

> **What is in motion and where can I continue?**

Permanent semantic rule:

```text
recent != resumable
last opened != meaningful checkpoint
unfinished != important
AI thinks important != continuity fact
```

Implemented engineering includes intent-specific boundary validation, deterministic local adapter, bounded results, truthful resource states, race/cancellation protection, local failure isolation, responsive/a11y behavior and no fake Resume CTA.

Automated gates passed.

**Integrated user visual acceptance is deferred**, not failed: the user correctly identified that DANTE's real spatial footprint must be established before more content is judged/composed against the workspace. B2 remains valid capability/evidence and will be re-reviewed inside the real post-DANTE composition.

## 25. Historical product gate — World contextual DANTE spatial/presence model

This section records the product problem that was the immediate gate at the WR/B2 stage. It is retained as phase-time evidence; it is **not the current sequencing authority**.

The problem space was:

```text
persistent vs transient presence
quiet footprint
invocation/composer placement
long-conversation expansion
sidecar/dock/overlay/full-surface alternatives
when DANTE consumes layout space
minimum content area
content reflow during expansion
selection/deictic context interaction
conversation vs Insight
conversation vs Explore
Proposal/confirmation/receipt presentation
World switch/run binding
desktop/laptop/tablet/mobile
focus/keyboard/SR/touch/reduced motion
AI unavailable/degraded state
pre-backend shell now vs real runtime later
```

Critical rule:

```text
Home AI surface != World contextual DANTE surface
```

The accepted outcome is now carried by D0/D1: quiet invoke, compact composer, wide sidecar where viable, constrained/mobile route-owned focus overlay, explicit maximize/restore, and bounded contextual/deictic invocation. D2–D6 remain intentionally deferred to M4.

The historical rule against copying Home geometry/components remains binding. No later phase may reinterpret DANTE as a decorative chatbot or silently widen context/authorization.

## 26. Product invariants

```text
World != canonical Domain owner
World != folder
World != life-area taxonomy
World != universal relation container
World relevance != ownership
World relevance != authorization
World composition != DANTE context universe
World session != canonical state
World != AI memory
World != reasoning prison

AI output != fact
AI proposal != Decision
Tool call != authorization
Provider state != canonical state
Planned != actual
Effort != execution != outcome != Goal progress
Observation != causation
Observed pattern != confirmed preference
Absence != false
UI hiding != authorization
```

## 27. Reverse-engineering closure evidence

```text
WR0
World product definition / Output Grammar / archetypes / Lens falsification

WR0 matrix
World-worthiness / overlap / lifecycle / proliferation / density

WR1
World role for DANTE and user
-> 7 material gaps found

WR2
G1..G7 closure + adversarial rerun
-> 7/7 closed
-> no new structural gap
```

Final structural scan at WR closure:

```text
NEW DOMAIN GAP                 0
NEW LOGICAL GAP                0
NEW PHYSICAL/DB GAP            0
NEW INTELLIGENCE ARCH GAP      0
NEW WORLD PRODUCT STRUCTURAL   0
```

That closure remains valid. Later D0/D1, WS0–WS8, M0 and M1 materialized and hardened the accepted semantics without changing the World product definition above. Live sequencing is not owned by this historical closure section.
