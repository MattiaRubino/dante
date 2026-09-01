# DANTE — World Focus Product Contract

**Status:** CURRENT PRE-BACKEND PRODUCT CONTRACT — WR0/WR1/WR2 REVERSE ENGINEERING CLOSED  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Implementation gate:** product contract saved; B1 requires product/UI revision against this contract before implementation may continue to the next mini-vertical.  
**Evidence:** `world-focus-product-reverse-engineering-stress-test.md`, `world-focus-product-reverse-engineering-stress-matrix.md`, `world-focus-dante-user-reverse-engineering-stress-test.md`, `world-focus-dante-user-gap-closure-stress-test.md`.

---

# 1. Product compass

World Focus exists for:

> **Understand this part of my life and continue from here.**

A World is:

> **a user-recognizable continuity context for a significant part of reality. World Focus projects the authoritative and derived DANTE realities relevant to that context so the user can quickly understand where things stand, recover or resume what matters, notice material change or attention needs, explore deeper evidence, and continue through decisions or actions when useful.**

A World is **not**:

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

---

# 2. World-worthiness

A context is a strong World candidate when several of these are true:

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

No canonical owner type automatically becomes a World.

Rejected automatic rules:

```text
Goal -> World
Project -> World
Person -> World
Asset -> World
Calendar -> World
Domain category -> World
```

Worlds are **curated continuity entry points**, not an exhaustive tree of everything the user owns or knows.

---

# 3. Home / World / Explore / Search boundary

## Home

Home answers cross-life questions:

```text
What matters across my life now?
What happens next?
What needs attention?
Which context should I resume?
```

Home = **cross-life compression and operation**.

## World Focus

World answers scoped continuity questions:

```text
What is happening here?
What is alive/in motion?
What should I resume?
What changed here?
What needs attention here?
What comes next here?
What is this based on?
What can I do here?
```

World = **scoped expansion, understanding and continuation**.

## Explore / detail

Explore answers depth questions:

```text
show the full itinerary
show every source record
show all versions
show complete relevant history
```

Explore = **depth**.

## Search

Search may go directly to an exact target.

Known item lookup should not be forced through a World.

World is preferable when the intent is context recovery or contextual exploration.

---

# 4. Dual role — user and DANTE

A World has two simultaneous roles.

## For the user

A low-reentry-cost surface for understanding and continuing one meaningful context.

## For DANTE

A bounded contextual coordinate that biases relevance and interaction toward that continuity context.

World context helps DANTE with:

```text
relevance prior
ambiguity/deictic resolution
continuity across interactions
retrieval starting point
source/detail context
scoped Insight
proposal target framing
returning results to the correct surface
```

World context does **not** determine:

```text
canonical truth
authorization/disclosure
all data that may be retrieved
operation permission
whether a model inference is true
```

Core thesis:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

---

# 5. Four-layer World context model

Never collapse these layers.

```text
1. World identity / purpose
2. Stable World relevance definition
3. Current World session / interaction cursor
4. Authorized purpose-scoped DANTE context
```

## 5.1 World identity / purpose

Product/presentation identity:

```text
World reference
user-recognizable name
optional concise purpose/description
theme/presentation profile
presentation lifecycle/config origin where needed
```

Name alone never proves semantics.

## 5.2 Stable World relevance definition

Answers:

> What kinds of DANTE reality are intentionally relevant to this continuity context?

May derive from bounded approved product/application configuration such as:

```text
explicit user-linked anchors
approved typed capability/query configuration
system defaults
user-approved DANTE proposals
application-derived stable configuration where allowed
```

It is not canonical membership, generic relation storage, arbitrary SQL or authorization.

A sparse World stays sparse if no justified relevance is established.

## 5.3 Current World session / interaction cursor

Transient interaction context conceptually contains:

```text
active World reference
interaction generation
current Lens/query scope when applicable
selected projection/module/source reference
current Insight/Explore reference when applicable
entry/surface context
```

It does not serialize raw DOM/React state or canonical data as truth.

## 5.4 Authorized purpose-scoped DANTE context

Built by authoritative application/Context Builder from:

```text
World identity/purpose
stable relevance definition
current interaction cursor
actual request/purpose
Principal / Actor / recipient
sensitivity/disclosure/governance
freshness/material basis
```

Only this reconstructed/minimized context is usable for the real DANTE request.

---

# 6. World Output Grammar

Worlds are **question-driven**, not widget-driven.

These are output/question families, not mandatory UI slots.

## O1 — Orientation

> What am I looking at?

## O2 — Situation

> What is currently true or materially relevant here?

## O3 — Continuity / Resume

> What is in motion and where can I continue?

## O4 — Attention / Resolution

> What needs attention, confirmation, correction or decision?

## O5 — Next

> What is coming next here?

## O6 — Change

> What changed since the relevant reference point?

## O7 — Trajectory / Comparison

> Where is this going relative to a meaningful baseline, plan or outcome?

Optional only when semantics justify it.

## O8 — Evidence / History

> What is this based on and what happened before?

## O9 — Explore

> What else can I inspect inside this context?

## O10 — Act / Decide

> What can I do from here?

## O11 — Intelligence

> What can DANTE help me understand, compare, simulate or improve here?

A World does not need all eleven.

Correct rule:

```text
meaningful available answers
-> rank by current value
-> render restrained subset
-> deeper material on demand
```

Never fill missing grammar with invented cards, KPIs or AI prose.

---

# 7. First-open contract

Core first-open value must be available without an LLM.

Required architecture:

```text
bounded authorized application projections
-> question/output classification
-> initial composition resolver
-> first screen
```

DANTE may explain/summarize/refine afterward, but does not own whether the World is understandable.

The first screen should prioritize depending on context:

```text
orientation
situation
continuity/resume
attention
next
change
optional trajectory
```

History and depth usually remain summary-first -> Explore.

Sparse Worlds remain sparse.

Completed Worlds may prioritize history/outcomes/artifacts rather than next actions.

Dormant Worlds do not manufacture urgency or guilt.

---

# 8. Ranking and composition

Do not start from the registry catalogue.

Potential ranking inputs:

```text
stable/pinned user importance
material consequence
immediacy/time sensitivity
resumability value
meaningful change
explicit current user intent/selection
confidence/provenance quality
```

Novelty is at most a weak tie-breaker.

Hard reject:

```text
AI relevance score alone decides page composition
```

Stable user-owned composition remains stable.

Adaptive content may temporarily surface a high-value answer but cannot silently rearrange/remove user stable content.

---

# 9. DANTE presence inside a World

A World is not required to display a permanent chat box.

Product presentation depths:

```text
P0 QUIET
- no AI output required

P1 INVOKE
- user explicitly asks DANTE

P2 CONTEXTUAL ENTRY
- small meaningful question/action entry when useful

P3 INSIGHT
- bounded evidence-backed interpretation

P4 PROPOSAL
- specific suggested change/scenario

P5 ACTION / RECEIPT
- governed operation/result state
```

These are presentation depths, not new Domain/autonomy concepts.

Proactivity requires real material value. No random “insight” slot exists merely to make the product appear intelligent.

---

# 10. DANTE result semantics visible to the user

Never collapse everything into `AI response`.

Keep distinct:

```text
SOURCE-BACKED FACT / PROJECTION
DANTE ANSWER / EXPLANATION
DANTE INSIGHT / DERIVED INTERPRETATION
CANDIDATE / UNRESOLVED INTERPRETATION
SCENARIO / RECOMMENDATION
PROPOSAL
GOVERNED EFFECT / RECEIPT
```

Required permanent boundaries:

```text
AI output != accepted fact
AI proposal != Decision
Decision != effect
request accepted != effect completed
provider acknowledgement != canonical completion
```

---

# 11. Deictic interaction / context cursor

Inside a World, the user should be able to say:

```text
“questa”
“perché?”
“continua da qui”
“confronta con prima”
“aprimi la fonte”
“spostalo”
```

without restating the context.

The current interaction cursor provides bounded references/hints; the authoritative application reconstructs usable context.

A DANTE run remains bound to the initiating World/cursor generation.

Switching World must not cause a late result to attach to the new context.

Durable runtime work must not depend on React mount lifetime.

---

# 12. Coherent basis / freshness

Visible projections and contextual DANTE answers need compatible basis semantics.

Important projections/results retain where applicable:

```text
request/projection generation
basis/material state reference
as-of/freshness
provider/source freshness
```

DANTE may reuse a compatible visible basis or re-read/revalidate.

If a material refresh changes the state, the answer/result must truthfully reflect the new basis rather than pretend the old visible state is still current.

Provider unavailable/timeout never becomes a false semantic negative.

---

# 13. Cross-World DANTE orchestration

A World is a default relevance bias, not an AI silo.

Default:

```text
start from the current World
minimize unrelated retrieval
```

Expand only when:

```text
the user's actual purpose materially requires it
AND
the additional context is authorized/relevant
```

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
World question = whole-life retrieval permission
```

When broader context materially changes the conclusion, the user-facing result should make the meaningful broader basis understandable.

---

# 14. Home ↔ World attention altitude

The same underlying matter may appear at different information altitude.

Example:

```text
Home
“Release at risk”

Music World
why, what changed, blocker, source, options
```

Home = compressed cross-life signal.

World = scoped expansion/explanation/action.

Presentation dismissal/snooze must not silently become semantic resolution unless the owning application contract says so.

---

# 15. Lens contract after reverse engineering

World Lens remains a useful bounded session/query mechanism.

But a global visible temporal Lens is **not** a universal first-screen control.

Show a World-level Lens only when:

```text
multiple prominent current projections
share the same dimension
with the same semantics
AND changing it has obvious user value
```

Otherwise scope belongs to:

```text
module-local control
Insight
Explore
contextual query
invisible session state
```

The B1 finite parser, URL restoration, `scopeKey` and race foundations may be retained.

The current B1 visible segmented time control is not product-frozen.

---

# 16. Same reality / multiple Worlds

One canonical reality may appear in several Worlds.

Example:

```text
Iceland trip
-> Travel
-> Photography
-> Finance
-> Family
```

Correct:

```text
one canonical reality
+ multiple bounded projections/configurations
```

World relevance never transfers canonical ownership.

Removing a World/module never deletes source reality.

---

# 17. Multi-actor/privacy

Shared World context does not imply shared access to every actor's private context.

```text
shared fact != private overlay
World relevance != Visibility
UI hiding != authorization
```

Projection must be disclosure-safe before React/DANTE presentation.

The Context Builder remains recipient/purpose/sensitivity-aware.

---

# 18. World lifecycle

World lifecycle is product/presentation state, not Domain ontology.

A World may be conceptually:

```text
emerging
active
dormant
completed-context
archived/unpinned
```

Names are not frozen.

Rules:

```text
dormant != failed
completed != needs a fake next action
archived != delete canonical reality
```

---

# 19. AI unavailable / provider failure

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

Neither failure rewrites canonical truth.

---

# 20. Consequential actions

World context may help target an operation but never authorizes it.

The existing governed operation/effect architecture remains authoritative:

```text
caller intent
-> target/effect interpretation
-> expected state/freshness
-> governance/autonomy/confirmation
-> execution
-> canonical/provider/runtime result axes
-> reconciliation where needed
```

Navigating away or cancelling a React surface is not semantic effect cancellation.

---

# 21. Unknown future Worlds

Unknown World behavior must be sparse and safe.

A name/label does not justify ontology inference.

Expected:

```text
show identity
show only known justified projections
no fake KPI
no fake Goal
no forced Lens
DANTE may propose context linking/configuration
DANTE does not silently establish truth or membership
```

---

# 22. Product invariants

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

---

# 23. B1 disposition

Current B1 implementation:

```text
engineering implementation      PASS
automated frontend gates        PASS
session/race foundations        KEEP PROVISIONALLY
finite Lens parsing             KEEP PROVISIONALLY
URL restoration                 KEEP PROVISIONALLY
scopeKey                        KEEP PROVISIONALLY
visible global time Lens        REVISE / likely hide or contextualize
B1 product acceptance           NOT CLOSED
```

B1 must be revised against this contract before freeze.

---

# 24. Next mini-vertical direction after B1 revision

Do not resume the old infrastructure-first sequence.

The next real vertical should answer one concrete World question end-to-end.

Strongest current candidate:

```text
CONTINUITY / RESUME
```

because it directly proves the core World promise:

> **I return to this part of my life, understand what is alive, and continue.**

The mini-vertical must include the necessary deterministic projection/application seam, real renderer/UI, interaction, responsive/a11y/performance/error/race behavior and future backend contract together.

Backend/API/DB/provider/real-LLM integration remains deferred to the final backend vertical as already agreed.

---

# 25. Reverse-engineering closure evidence

Stress sequence:

```text
WR0
World product definition / Output Grammar / archetypes / Lens falsification

WR0 matrix
borderline World-worthiness / overlap / lifecycle / proliferation / density

WR1
World role for DANTE and user / AI/context/action simulations
-> 7 material gaps found

WR2
G1..G7 closure + adversarial rerun
-> 7/7 closed
-> no new structural gap
```

Final scan:

```text
NEW DOMAIN GAP                 0
NEW LOGICAL GAP                0
NEW PHYSICAL/DB GAP            0
NEW INTELLIGENCE ARCH GAP      0
NEW WORLD PRODUCT STRUCTURAL   0
```

This contract is therefore the current product authority for resuming World Focus pre-backend implementation, subject to normal user visual/functional acceptance of each subsequent mini-vertical.
