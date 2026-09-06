# DANTE — World Product Reverse Engineering Mega Stress Test

**Status:** PRODUCT REVERSE-ENGINEERING GATE ACTIVE — B1 USER ACCEPTANCE BLOCKED  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope:** determine what a `World` is as a product surface, what job it must perform, what it must be able to produce, and which implications follow for World Focus before B1 is accepted or B2 begins.  
**Implementation rule:** no new World Focus UI/product vertical is authorized while this gate is active. Existing B0 remains closed. Existing B1 code remains evidence and may be retained, changed, hidden or partially reused after this gate.

---

# 0. Why this gate exists

B0 correctly established the production foundation. B1 then implemented a visible World Context + temporal Lens vertical and passed automated gates.

During user acceptance, a fundamental product question surfaced immediately:

> Why would I want to choose 7 / 30 / 90 days when I open a World?

That question reveals a problem upstream of the control itself.

The issue is not primarily whether the Lens implementation is technically correct. It is whether World Focus had first been reverse-engineered deeply enough as a **product job** before selecting the first visible product capability.

The existing WF0 scenario oracle stress-tested whether one architecture could technically represent heterogeneous Worlds. That remains useful and largely valid. This new gate asks a different and earlier product question:

> **What is a World for the user, why does the user return to it, and what should DANTE help them understand or continue when they open it?**

Until that question survives adversarial scenarios, visible World controls, module order and default composition remain provisional.

---

# 1. Authorities and constraints consumed

## 1.1 Product North Star

Current accepted Product Identity states that DANTE is a personal operating system that maintains structured, updateable understanding of a person's situation, connects parts of life, identifies opportunities/problems, helps compare alternatives, orchestrates demands, builds realistic paths, observes actual reality and adapts what comes next.

Durable consequences:

```text
life != tasks
life != calendar
life != metrics
life != goals alone
planned != actual
effort != execution != outcome != Goal progress
observed pattern != confirmed preference
AI inference != confirmed fact
simple situations may remain simple
time is foundational but is not the container of life
```

A song is not its next Session. A vehicle is not its next maintenance Event. A learning path is not Tuesday's lesson.

## 1.2 Home contract

The current Home contract gives the strongest existing product definition of `Mondi`:

> **Significant realities the user wants readily recoverable, resumable or explorable over time.**

Home itself is the recurring cross-life orientation/operation surface combining current situation, conversational access, temporal reality, contextual information and direct action.

Therefore World Focus must not merely duplicate Home with a scope filter.

## 1.3 Domain / Logical / Physical barriers

The Domain Atlas is closed for the accepted kernel and explicitly rejects deriving ontology from product/UI labels.

Current barriers include:

```text
product/UI terminology != automatic ontology
specific truthful semantics > generic catch-all abstraction
native identity != contextual role
planned/intended != Actual
Observation != Actual
Authority != Visibility
provider identity != canonical DANTE identity
```

The Logical Model preserves specific owners and qualified projections rather than a universal semantic root.

Consequently:

```text
World != Domain owner
World != universal Entity
World != universal relation container
World != automatic Life Area primitive
World != database partition key
World != security boundary by itself
```

World Focus must consume bounded projections over authoritative realities.

## 1.4 Existing WF0 scenario oracle

WF0 already established that one World Focus platform can survive Music, Travel, Finance, Study, Body/Wellbeing, Home, Vehicle, Photography, work/shared projects, people, sparse realities, large history, stale providers, multi-actor privacy and unknown future Worlds without requiring one bespoke page per World.

This review does not discard that architecture result. It re-examines **what the page should be trying to accomplish before module architecture decides how to render it**.

---

# 2. Research method

The gate uses five layers.

## Layer A — source reconstruction

Re-read DANTE authorities to derive product intent without importing dashboard assumptions.

## Layer B — external pattern comparison

Inspect current mature products for transferable interaction/product patterns, not for ontology copying.

Products reviewed in this pass include:

```text
Linear
Notion Dashboard
TripIt
Apple Health
YNAB Reflect
Home Assistant
Strava Training Log
Airtable Interfaces
Microsoft Loop
Todoist
```

## Layer C — definition falsification

Create candidate definitions of `World`, then try to break them with counterexamples.

## Layer D — contrasting World stress

Run materially different Worlds and states through a common set of questions.

## Layer E — architecture/product propagation

Determine what the surviving definition implies for:

```text
Home vs World boundary
World Focus default composition
World Lens
modules
Adaptive
DANTE/AI
projection contracts
future backend seams
B1 disposition
next mini-vertical order
```

---

# 3. External reverse engineering — what mature products teach us

These products are references for product mechanics only. None is a semantic template for DANTE.

## 3.1 Linear — scoped continuity, status and catch-up

Current Project Overview combines summary/description, resources/documents, milestones and progress. Linear also keeps structured project updates and a chronological update history showing material property changes.

Transferable lesson:

```text
opening a meaningful context should help the user re-orient,
see current state,
understand progress/change,
and continue from there
```

Important rejection:

Linear is project/work software. DANTE must not assume every World has a project lifecycle, completion percentage or issue graph.

## 3.2 TripIt — finite context whose useful output changes with phase

TripIt organizes a trip around the itinerary and contextually relevant facts. Near execution, alerts, check-in, gates, delays, disruption and leave-now timing become prominent.

Transferable lesson:

```text
the useful default view changes with lifecycle/current situation
```

A trip months away, tomorrow and already completed should not expose the same first-screen emphasis.

Important rejection:

World Focus cannot be a Travel-specific itinerary application.

## 3.3 Apple Health — selective highlights before raw history

Health Summary surfaces selected Highlights and Trends. The user drills into a specific graph/category for detail.

Transferable lesson:

```text
surface materially useful interpretation first;
put temporal exploration inside the evidence/detail context when appropriate
```

Important rejection:

DANTE must not infer health significance beyond authorised evidence or copy a health-metric ontology into all Worlds.

## 3.4 YNAB Reflect — analysis is a mode, not the entire product context

YNAB's `Reflect` area contains spending trends and breakdown analysis, with date/category/account filtering and drill-down toward individual transactions.

Transferable lesson:

```text
time/category filters are natural when the user's active job is analysis
```

They do not need to dominate every high-level context before an analytical question exists.

## 3.5 Home Assistant — at-a-glance situation plus direct action

Home Assistant's dashboard is explicitly an at-a-glance view of what is happening now, with immediate controls.

Transferable lesson:

```text
for operational contexts, current state + meaningful control can outrank history
```

Important rejection:

DANTE realities are not all controllable devices and should not become a grid of status cards.

## 3.6 Strava — time filters belong to a specific history/progress surface

Training Log is a dedicated historical/progress view with calendar navigation and filters for sport/measure/tag.

Transferable lesson:

```text
filter grammar can be local to the representation that needs it
```

A World need not expose a universal time Lens merely because one module later needs historical analysis.

## 3.7 Microsoft Loop — recoverable workspace continuity

Loop workspaces group the content and context important to an ongoing project so people can catch up and track what is happening.

Transferable lesson:

```text
a useful workspace preserves continuity and reduces re-entry cost
```

Important rejection:

DANTE World is not a free-form collaborative document canvas.

## 3.8 Notion / Airtable — useful counterexamples

Notion Dashboard and Airtable Dashboard provide stable widget-based summary/control surfaces with filtering and drill-down.

Transferable lesson:

```text
bounded high-level summaries + drill-down are useful
```

Counterexample lesson:

```text
World Focus must not become a user-built BI/dashboard system by default
```

DANTE's product value is not widget composition itself.

---

# 4. Candidate definitions of World — falsification

## Candidate A

> A World is a life area.

**REJECT.**

Fails on:

- one finite Japan trip;
- one car;
- one album/release context;
- one important relationship;
- a temporary move;
- a cross-area project;
- user-created scopes that do not map cleanly to Work/Health/Finance/etc.

Also risks promoting UI taxonomy into Domain semantics.

## Candidate B

> A World is a dashboard for one category of data.

**REJECT.**

Fails on:

- qualitative relationships;
- creative continuity;
- sparse Worlds;
- next-action/resumption value;
- non-metric assets;
- travel disruption;
- user decisions and DANTE interaction.

## Candidate C

> A World is a container of related DANTE entities.

**REJECT.**

Too storage-shaped. Encourages generic relationship/container semantics and duplicates canonical ownership.

A reality may appear in several Worlds without being copied into them.

## Candidate D

> A World is one persistent object such as a project, asset or person.

**REJECT as universal definition.**

A World may be centered on one object, but Music/Finance/Family can span many owners. Conversely, not every Goal, Person, Asset or Project deserves a full World surface.

## Candidate E

> A World is a user-recognizable continuity context around a significant reality, used to reduce the cost of re-orienting, resuming, understanding change/attention, exploring evidence and acting within that scope.

**SURVIVES INITIAL FALSIFICATION.**

It supports:

- broad contexts such as Music;
- finite contexts such as Japan Trip;
- object-centered contexts such as Car;
- person/relationship contexts;
- quantitative contexts such as Finance;
- sparse contexts;
- completed/historical contexts;
- the same canonical fact appearing in multiple projections.

It also remains a product/presentation concept rather than a Domain owner.

---

# 5. Provisional World definition

The current strongest definition is:

> **A World is a user-recognizable continuity context for a significant part of reality. World Focus projects the authoritative and derived DANTE realities relevant to that context so the user can quickly understand where things stand, recover or resume what matters, notice material change or attention needs, explore deeper evidence, and continue through decisions or actions when useful.**

Short internal product compass:

> **Understand this part of my life and continue from here.**

This line from the existing World Focus direction remains strong and now has a more precise product interpretation.

The definition intentionally does **not** say:

```text
area
folder
project
dashboard
metric collection
query
filter
AI chat
Domain aggregate
```

---

# 6. World-worthiness test

This is a product heuristic, not Domain validation and not an automatic classifier.

A candidate context becomes a strong World candidate when several of the following are true:

## W1 — recurring re-entry value

The user benefits from returning to the context repeatedly rather than opening one item once.

## W2 — continuity

There is meaningful state/history/intent worth recovering between visits.

## W3 — resumability

The user can reasonably ask “where was I?” or “what should I pick back up?”

## W4 — situational understanding

Several facts/owners/capabilities become more useful when understood together in this context.

A World can still be object-centered; it does not require many canonical entity types.

## W5 — meaningful change

Changes in the context may matter enough to surface later.

## W6 — scoped decisions/actions

The context can generate decisions, planning, coordination or action that benefits from preserved local context.

## W7 — deeper exploration

The user may want to drill from summary into history, evidence, artifacts, people, plans or specialist views.

## W8 — identity for the user

The context has a stable human meaning the user can recognize and name.

### Weak World candidates

Examples that may remain ordinary objects/views instead:

```text
one simple appointment
one trivial task
one isolated receipt
one temporary search result
one number with no continuity
one document the user only opens once
```

A weak candidate can later become World-worthy if its lifecycle/context grows.

---

# 7. World vs adjacent product surfaces

## 7.1 Home

Home answers cross-life questions:

```text
What matters across my life now?
What happens next?
What needs my attention?
What should I capture/resolve?
Which significant contexts should I resume?
```

Home optimizes **global orientation and operation**.

## 7.2 World Focus

World answers scoped continuity questions:

```text
What is the situation in this context?
What is alive/in motion?
What should I resume?
What changed here?
What needs attention here?
What comes next here?
What evidence/context do I need?
What can I decide/do here?
```

World Focus optimizes **context recovery + scoped understanding + continuation**.

## 7.3 Explore / detail surface

Explore answers depth questions:

```text
show me the complete itinerary
show me all transactions behind this spike
show me all versions of this song
show me this person's relevant history
```

Explore optimizes **depth**, not first-screen orientation.

## 7.4 Specialist surface

A specialist surface exists only when generic projections materially lose meaning, e.g. a rich travel itinerary or a future domain-specific editor.

It must remain connected to the same canonical reality rather than becoming a parallel product silo.

## 7.5 DANTE conversational/intelligence surface

DANTE is a contextual interaction layer over the same World/session reality.

It may answer, explain, compare, simulate or propose. It does not define the World by itself and AI unavailability must not destroy the World's core usefulness.

---

# 8. World Output Grammar — question families, not fixed UI sections

The most important result of this stress test is that a World should be **question-driven**.

The following are output families. They are not mandatory slots, fixed module positions or new Domain concepts.

## O1 — ORIENTATION

Question:

> What am I looking at and what is the relevant context right now?

Possible outputs:

- title/context identity;
- phase/mode where meaningful;
- concise situation framing;
- relevant scope qualifiers.

## O2 — SITUATION

Question:

> What is currently true or materially relevant here?

Possible outputs:

- current state;
- current balance/status;
- active trip segment;
- current program phase;
- current asset condition;
- recent confirmed observations.

## O3 — CONTINUITY / RESUME

Question:

> What is in motion, and where can I continue?

Possible outputs:

- active tracks/projects;
- last meaningful artifact/session;
- unfinished preparation;
- active learning thread;
- ongoing responsibility;
- current pipeline stage.

## O4 — ATTENTION / RESOLUTION

Question:

> What needs my attention, confirmation, correction or decision?

Possible outputs:

- conflict;
- overdue review;
- provider discrepancy;
- missing document;
- blocked dependency;
- ambiguous import;
- user confirmation.

Not every World must have attention items.

## O5 — NEXT

Question:

> What is coming next in this context?

Possible outputs:

- next transport segment;
- upcoming release milestone;
- next lesson/exam;
- maintenance deadline;
- promised follow-up;
- next meaningful action.

## O6 — CHANGE

Question:

> What changed since the last relevant reference point?

Possible outputs:

- changed schedule;
- new artifact/version;
- updated assessment;
- meaningful spending shift;
- new accepted decision;
- changed participant;
- provider freshness/disruption.

Change is not equivalent to notification volume.

## O7 — TRAJECTORY / COMPARISON

Question:

> Where is this going relative to a meaningful baseline, plan or outcome?

Optional. Only when semantics justify it.

Possible outputs:

- Goal trajectory;
- planned vs actual;
- spending comparison;
- assessment trend;
- release risk;
- workload direction.

Must never invent a percentage, score or causal explanation merely to fill a slot.

## O8 — EVIDENCE / HISTORY

Question:

> What is this based on, and what happened before?

Possible outputs:

- Sessions;
- Observations;
- source records;
- documents;
- versions;
- provenance/freshness;
- decision history.

Usually summary-first with drill-down rather than raw data dump.

## O9 — EXPLORE

Question:

> What else can I inspect within this context?

This is navigation into deeper bounded views, not a requirement to show everything on the first screen.

## O10 — ACT / DECIDE

Question:

> What can I do from here?

Possible outputs:

- resume;
- create within valid contextual flow;
- approve/reject;
- reschedule;
- reconcile;
- open source;
- start a Session;
- invoke a capability;
- compare alternatives.

Authority remains explicit.

## O11 — INTELLIGENCE

Question:

> What can DANTE help me understand, compare or improve here?

Possible outputs:

- grounded explanation;
- contextual questions;
- bounded insight;
- scenario comparison;
- proposal.

AI output remains distinguishable from canonical fact, Decision and accepted Effect.

---

# 9. Key rule: Output Grammar is sparse and state-dependent

A World does not need one instance of O1..O11.

Correct behavior:

```text
available meaningful answers
        ↓
rank by current value
        ↓
render a restrained subset
        ↓
deeper information on demand
```

Wrong behavior:

```text
11 output slots
-> fill every slot
-> invent metrics/empty cards/placeholders
```

This preserves the Product North Star rule that simple situations remain simple.

---

# 10. Deep stress scenarios

Each case is evaluated by the **first-open value test**:

> If the user opens this World after not looking at it for a while, what are the highest-value things DANTE should help them understand or continue before they manually query/filter anything?

## S1 — Music / creative continuity

Reality:

```text
ideas
songs/releases
Goals
Plans
Activities
Sessions
artifacts/versions
collaborators
release dates
imported performance observations
```

First-open winners:

```text
CONTINUITY   active songs/releases and where each stopped
RESUME       most meaningful recent Session/artifact
NEXT         upcoming milestone/release
ATTENTION    blocked/stale/at-risk item if evidence exists
CHANGE       new version/result/material change
TRAJECTORY   only for valid release/Goal semantics
INTELLIGENCE contextual questions and grounded insight
```

Loser as first-screen global control:

```text
7d / 30d / 90d / 1y
```

Time becomes useful inside specific questions such as creative-time trend, recent Sessions or performance comparison.

**Verdict:** creative continuity World passes strongly.

## S2 — Travel / finite journey

Phases:

```text
idea
planning
booked/upcoming
in progress
completed/historical
```

First-open winners change by phase.

Planning:

```text
what is decided
what is missing
bookings/documents
open decisions
```

Near departure:

```text
next segment
check-in/document readiness
changes/disruptions
where/when
```

During trip:

```text
next location/segment
live disruption
booking facts
local context
```

After trip:

```text
history/artifacts/cost summary/actual record
```

Global historical Lens is weak. Trip-relative or itinerary scope is stronger.

**Verdict:** lifecycle-sensitive World; validates dynamic composition and specialist itinerary candidate.

## S3 — Finance / long-lived quantitative

First-open winners:

```text
SITUATION    current relevant balance/commitment state when semantically valid
CHANGE       material movement or spending shift
ATTENTION    unreconciled/stale/provider issue
NEXT         upcoming obligations where available
TRAJECTORY   explicit savings/Goal relationship only when real
EVIDENCE     drill to records
```

Analytical period is valuable but should usually be attached to the analytical surface:

```text
spending trend -> 30d / 90d / 1y
cashflow compare -> selected period
```

**Verdict:** quantitative World does not require a global Lens to be understandable.

## S4 — Study / Goal + Plan + actual execution

First-open winners:

```text
TRAJECTORY   where am I relative to desired result, if measurable
CONTINUITY   what topic/program is active
RESUME       last/next useful material or Session
NEXT         lesson/exam/milestone
ATTENTION    missed Sessions/plan risk only when grounded
CHANGE       assessment change
```

Time filters belong in history/trend questions, not necessarily the page header.

**Verdict:** World survives without dashboard-first design.

## S5 — Body / wellbeing / sensitive observations

First-open winners:

```text
SITUATION    confirmed relevant observations/context
NEXT         accepted plan/routine/event
CHANGE       cautiously stated trend
ATTENTION    only authorized and non-diagnostic
EVIDENCE     strong provenance/source visibility
```

Hard rejects:

```text
health score
causal claim from correlation
hidden sensitive disclosure
AI diagnosis framing
```

**Verdict:** proves output grammar must be disclosure/safety-aware before React.

## S6 — Relationships / qualitative continuity

Possible realities:

```text
People
commitments/promises
shared Events
notes/context
important dates
decisions
history
```

First-open winners:

```text
CONTINUITY   relevant relationship context
NEXT         next shared commitment/event
RESUME       promise/follow-up worth remembering
CHANGE       meaningful shared change where valid
EVIDENCE     prior decision/context on demand
```

Hard rejects:

```text
interaction count as relationship quality
relationship score
streaks
forced time Lens
```

**Verdict:** critical proof that World is not a metrics dashboard.

## S7 — Vehicle / Asset-centered World

First-open winners:

```text
SITUATION    current known asset state
NEXT         maintenance/document deadline
ATTENTION    fault/expiry/reconciliation issue
CHANGE       recent service/cost/condition update
EVIDENCE     maintenance/cost/document history
ACT          record service, open document, plan maintenance
```

A single Asset can justify a World when it has enough ongoing operational continuity.

**Verdict:** disproves “World must be broad life area”.

## S8 — Shared work/project

First-open winners:

```text
SITUATION    accepted shared status
CONTINUITY   current workstream
ATTENTION    blocked dependency/review
NEXT         milestone/handoff
CHANGE       participant/decision/scope change
EVIDENCE     decision/update history
```

Privacy rule:

shared canonical fact does not expose another actor's private plan or reason.

**Verdict:** World must support role/disclosure-specific projection.

## S9 — Care / pet / dependent living referent

First-open winners:

```text
SITUATION    confirmed care context
NEXT         feeding/appointment/medication-like schedule where applicable
ATTENTION    missing confirmation/supply issue
CHANGE       observation/condition change without diagnostic overreach
EVIDENCE     source and actor who reported it
```

**Verdict:** subject != user; actor != subject; absence != false.

## S10 — Photography / opportunity-driven hobby

First-open winners may include:

```text
CONTINUITY   current shoots/projects/edit backlog
NEXT         planned outing/delivery
ATTENTION    backup/delivery/equipment issue
DISCOVERY via DANTE  weather/astronomy/event opportunity when integrations justify it
```

A discovered opportunity remains a possibility, not an accepted commitment.

**Verdict:** validates Discover as adaptive/intelligence output rather than permanent dashboard slot.

## S11 — Unknown future World

Assume a user creates a meaningful continuity context not known by current fixture categories.

Expected behavior:

```text
show identity/context
show only projections whose semantics are known
no invented KPI
no fake Goal
no forced time filter
unknown module fails locally
DANTE remains bounded by available capability/evidence
```

**Verdict:** generic platform must degrade sparsely, not guess semantics.

---

# 11. Adversarial state matrix

## A1 — Empty new World

Expected:

- orientation remains useful;
- explain that the context has no projected material yet without pretending failure;
- offer appropriate contextual creation/import/explore path only if semantics exist;
- no placeholder metrics/modules.

## A2 — Sparse World with one meaningful reality

Expected:

- one strong item may be enough;
- do not fabricate dashboard density;
- allow direct resume/explore.

## A3 — Dormant World

No recent activity does not mean failure or lack of value.

Expected:

- preserve continuity/history;
- optionally surface “last meaningful state”;
- no guilt framing;
- DANTE may ask whether it still matters only when justified.

## A4 — Completed finite World

Example: completed trip or finished move.

Expected:

- historical orientation;
- actual outcome/history/artifacts;
- no fake “next action” requirement;
- archive/removal is user/configuration semantics, not automatic deletion.

## A5 — World with no Goal

Expected:

- fully valid;
- no trajectory/progress module invented;
- continuity, state, history or exploration may be enough.

## A6 — World with no action required

Expected:

- still valid as persistent context;
- no artificial task generation;
- “nothing needs attention” may be represented quietly rather than as a card.

## A7 — Provider stale/offline

Expected:

- canonical/local accepted reality remains usable;
- affected provider projection identifies stale/unavailable state;
- unrelated World content remains available;
- provider failure never rewrites canonical truth.

## A8 — AI unavailable

Expected:

- World remains understandable and operable;
- only Intelligence surfaces degrade;
- no blank page or broken core navigation.

## A9 — Conflicting evidence

Expected:

- uncertainty/conflict represented explicitly;
- Resolution may surface if user action materially helps;
- no silent selection of preferred source.

## A10 — Massive history

Expected:

- bounded summaries/aggregation first;
- metadata before heavy bytes;
- drill-down on demand;
- no “load entire World history”.

## A11 — High-frequency observations

Expected:

- downsample/aggregate for first view;
- preserve access to evidence;
- avoid per-record module payload.

## A12 — Same reality appears in multiple Worlds

Expected:

- one canonical owner/state;
- multiple projections/configurations;
- no duplicated fact or diverging truth.

## A13 — Multi-actor selective disclosure

Expected:

- projection is already disclosure-safe before rendering;
- private overlays remain private;
- UI hiding is never authorization.

## A14 — Temporary life mode

Expected:

- current temporary context may change ranking/next/attention;
- normal configuration/history is not silently overwritten;
- restoration/review policy remains explicit.

## A15 — 20 potential modules

Expected:

- World does not render all available module kinds;
- initial composition answers the highest-value questions;
- summary -> Explore for depth;
- user-pinned stable content remains stable;
- adaptive content is bounded.

---

# 12. Archetype model — structural pressure, not taxonomy

The scenarios suggest useful **presentation pressure archetypes**. These are not World types stored as ontology.

```text
A. CONTINUITY / CREATIVE
   Music, writing, long project

B. FINITE JOURNEY
   Trip, move, event preparation

C. QUANTITATIVE LONG-LIVED
   Finance, selected health/training histories

D. GOAL / PROGRAM
   Study, training, certification

E. ASSET / RESOURCE
   Vehicle, home, equipment

F. PEOPLE / RELATIONSHIP
   Family, relationship, care

G. SHARED / MULTI-ACTOR
   project, household, trip, group

H. SPARSE / QUALITATIVE
   ideation, relationship, emerging interest
```

A World may exert several pressures simultaneously.

The archetypes exist only to ensure composition/interaction survives different shapes.

---

# 13. First-screen priority model

World Focus should not begin from `available widgets`.

Provisional resolver logic:

```text
1. identify current World/session context
2. gather disclosure-safe bounded candidate projections
3. map candidates to Output Grammar questions
4. suppress unsupported/empty/artificial answers
5. preserve stable user-owned composition
6. rank adaptive answers by material current value
7. render a restrained first screen
8. provide drill-down / Explore for depth
```

This explains why the same module family can appear in different positions or not appear at all without creating one page per World.

---

# 14. World Lens verdict

## 14.1 Architectural verdict

The B1 Lens model remains useful as a bounded session/query concept.

Useful future examples:

```text
Finance spending trend -> 90d
Music creative Sessions -> 30d
Study assessments -> 3 months
Body observation trend -> selected range
Explore history -> exact custom range
```

The finite parser, URL restoration and `scopeKey` can remain valuable infrastructure.

## 14.2 Product/UI verdict

A **global visible temporal Lens is not justified as the first universal World control**.

Reason:

- time is not the organizing root of World;
- many first-open questions are current/next/resume/change rather than historical filtering;
- several Worlds have no natural global time semantics;
- individual projections can use different temporal semantics simultaneously;
- a future-facing release/itinerary module and a past-facing trend may coexist;
- the user's acceptance question demonstrated poor discoverable value before content exists.

## 14.3 Revised rule

A visible World-level Lens should appear only if:

```text
multiple prominent current projections
share the same temporal/context dimension
with the same semantics
AND changing that scope creates obvious user value
```

Otherwise scope belongs to:

```text
module-local control
Insight/Explore interaction
contextual query
or invisible session state
```

## 14.4 B1 implication

Do not delete the Lens infrastructure yet.

Do not freeze the current visible segmented-control/header treatment.

B1 visual/product acceptance remains blocked until World composition is re-derived from this product model.

---

# 15. Module system implications

Modules should be treated as **answer renderers**, not as the product ontology.

Example:

```text
Question: What changed?
Possible renderer: comparison / trend / collection / prose

Question: What is next?
Possible renderer: timeline / collection / context

Question: What should I resume?
Possible renderer: artifact / collection / pipeline / context
```

Therefore:

```text
module kind != World meaning
module kind != output question
module kind != canonical source owner
```

A module can answer several question families depending on its projection semantics.

---

# 16. Adaptive implications

Adaptive content should not mean “AI rearranges dashboard widgets”.

Its job is closer to:

> surface a temporarily high-value answer that the stable composition would otherwise not prioritize.

Strong adaptive candidates:

```text
material change
new risk/blocker
time-sensitive next step
important resumable context
provider discrepancy
discovered opportunity
```

Weak candidates:

```text
random metric
novelty for novelty's sake
reordering stable user content
unexplained score
```

Adaptive remains bounded, dismissible/snoozable where meaningful and subordinate to user-owned stable composition.

---

# 17. DANTE Intelligence implications

World-contextual DANTE should inherit:

```text
World identity
current session context
currently viewed projection/selection
relevant provenance/freshness
user-authorized capabilities
```

Good contextual prompts derive naturally from Output Grammar:

```text
What changed?
What should I resume?
What is blocked?
Why is this at risk?
What comes next?
Compare these alternatives.
Show me the evidence.
What would happen if I move this?
```

This is stronger than a generic blank chat box because the World already establishes meaningful scope.

---

# 18. Projection/data implications for later B2

B2 should not begin by defining a generic `WorldData` blob.

The projection boundary must support bounded answer-oriented candidate data while preserving source truth.

Required later properties include:

```text
projection identity
World/session scope identity
status
question/use intent where useful
module/render kind
bounded payload
freshness/provenance
source drill-down intent
available semantic actions
sensitivity/disclosure metadata when applicable
```

Do not duplicate canonical reality into World records.

Large-history cases require aggregation/downsampling at the application/query boundary rather than raw-history delivery to each module.

---

# 19. Future backend requirements — no backend implementation now

This gate does not design endpoint paths or tables.

It does establish needs the final backend vertical must satisfy:

1. projection requests scoped by a World presentation/context identity without making `world_id` canonical ownership;
2. intent-specific application ports rather than universal repository APIs;
3. disclosure-safe projection before frontend render;
4. provenance/freshness and source drill-down;
5. deterministic stale-result protection across World/session/Lens changes;
6. aggregation/downsampling for large histories;
7. same canonical reality reusable across multiple Worlds;
8. provider state separate from canonical accepted state;
9. DANTE intelligence consumes the same governed application capabilities rather than direct database/provider access;
10. durable actions retain EffectIntent -> Permit -> Attempt -> Receipt/Reconciliation semantics from the Intelligence architecture.

---

# 20. Hard failure modes this gate rejects

```text
WORLD = dashboard
WORLD = folder
WORLD = life-area ontology
WORLD = one Domain aggregate
WORLD = universal entity container
WORLD = filtered database view only
WORLD = AI chat room
WORLD = mandatory Goal/progress surface
WORLD = mandatory time range
WORLD = mandatory metrics
WORLD = fixed 8-card template
WORLD = everything related to a scope loaded at once
WORLD = duplicated canonical data
WORLD = front-end authorization boundary
```

Also rejected:

```text
fill empty space because the workspace looks sparse
invent KPI because a module family exists
show a time filter before it changes anything meaningful
force a 'next action' when nothing requires action
mark inactivity as failure
turn relationships into engagement analytics
turn body/wellbeing into diagnostic scoring
let provider outage erase accepted state
let AI absence erase the World
```

---

# 21. Revised product-development order

Current state:

```text
B0 Foundation
CLOSED

B1 Context / Session / Lens
IMPLEMENTED
AUTOMATED PASS
PRODUCT ACCEPTANCE BLOCKED BY THIS GATE
```

Do **not** begin old B2 directly.

First close:

```text
WR0 — World Product Reverse Engineering
  definition
  World-worthiness heuristic
  Home / World / Explore boundary
  Output Grammar
  archetype pressure
  Lens verdict
  first-screen resolver principles
  user product acceptance
```

Then revise the next mini-vertical sequence from product value outward.

Likely direction after WR0 acceptance:

```text
1. first real World answer vertical
   probably CONTINUITY / RESUME or NEXT/ATTENTION

2. bounded deterministic projection adapter required by that answer

3. real module renderer required by that answer

4. composition behavior proven by contrasting Worlds

5. only then broader module families / Adaptive / Insight / Customize
```

This reverses the earlier risk of building infrastructure in advance of an actual user question.

---

# 22. Candidate next verticals after this gate

The stress set suggests three strong first candidates.

## Candidate 1 — Continuity / Resume

Why strong:

- central to the current Home definition of Worlds;
- useful in Music, Study, projects, relationships, assets and many sparse cases;
- makes World value immediately understandable;
- does not require metrics or AI;
- naturally tests recent state, artifacts, Sessions, plans and user ownership.

Risk:

must not reduce everything to “recent activity”. Resume needs semantic relevance, not just latest timestamp.

## Candidate 2 — Next / Attention

Why strong:

- high operational value;
- strong in Travel, Study, vehicle, work, care;
- naturally connects to Home without duplicating it.

Risk:

needs a very clear distinction between global Home attention and scoped World attention.

## Candidate 3 — Situation / Change

Why strong:

- demonstrates DANTE's value as understanding rather than task list;
- works across quantitative and qualitative Worlds;
- supports later Adaptive and DANTE Insight.

Risk:

requires careful projection semantics and reference basis for “change”.

No candidate is frozen until user product acceptance of this reverse-engineering result.

---

# 23. Stress-test verdict

## Definition

**PASS WITH PRODUCT HARDENING.**

A coherent World concept exists without creating a new Domain owner or dashboard ontology.

## Current architecture

**HOLDS.**

The existing shell, workspace, projection/module separation, stable/adaptive composition and contextual DANTE direction remain viable.

## Current B1 infrastructure

**PARTIALLY VALID / KEEP PROVISIONALLY.**

Session scope, finite validation, URL restoration and stale-request identity are useful foundations.

## Current B1 visible temporal Lens

**NOT ACCEPTED AS A UNIVERSAL FIRST-SCREEN WORLD CONTROL.**

It must be hidden, contextualized or reintroduced only where multiple meaningful projections share its semantics.

## Product direction

**WORLD FOCUS SHOULD BE QUESTION-DRIVEN.**

Core compass:

> **Understand this part of my life and continue from here.**

Operationally this means:

```text
orientation
+ situation
+ continuity/resume
+ attention
+ next
+ change
+ optional trajectory
+ evidence/explore
+ action
+ contextual intelligence
```

rendered sparsely according to what is genuinely meaningful.

---

# 24. User acceptance gate

Before resuming implementation, the user should explicitly accept or revise:

1. the provisional World definition;
2. the `Understand this part of my life and continue from here` compass;
3. the distinction Home = cross-life orientation vs World = scoped continuity;
4. the World Output Grammar as question families, not fixed UI sections;
5. the rule that sparse Worlds remain sparse;
6. the rule that a World does not require Goals, metrics, actions or a time Lens;
7. the Lens demotion from universal first-screen control;
8. the likely next vertical should answer a real World question end-to-end rather than add another generic platform layer.

Only after this acceptance should B1 be revised and the next mini-vertical be selected.
