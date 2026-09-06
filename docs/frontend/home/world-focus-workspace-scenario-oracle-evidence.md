# DANTE — World Focus Workspace Scenario Oracle Evidence

**Status:** RETAINED RESEARCH EVIDENCE — NOT A ROADMAP / NOT A LIVE CHECKPOINT  
**Recovered:** 2026-09-01  
**Source lineage:** the former `world-focus-wf0-scenario-oracle.md` at pre-cleanup history, plus conclusions incorporated into the current Product/Platform contracts.  
**Branch:** `feature/home-react`

This document exists to preserve a piece of research that must **not be repeated from zero in future chats**.

The original scenario oracle was mistakenly removed during documentation cleanup because its old phase/status wording was superseded. That removal was too aggressive: the old file also contained unique workspace/module stress analysis that remains useful evidence. The obsolete roadmap/status is not restored; the durable research conclusions are.

Current authority remains:

```text
world-focus-current-checkpoint.md
world-focus-handoff.md
world-focus-product-contract.md
world-focus-platform-contract.md
world-focus-structural-contract.md
world-focus-geometry-contract.md
world-focus-frontend-roadmap.md
```

This evidence may explain **why** those contracts have their current shape, but never overrides them.

---

## 1. Question already studied

The scenario work explicitly asked whether one World Focus workspace could represent materially different parts of life without:

```text
one bespoke page per World
one renderer family per World
one persistence family per World
a generic WorldItem / Thing semantic root
arbitrary AI-generated React / HTML / JavaScript
raw database interpretation in the frontend
```

The target was never a finite enumeration of all future Worlds or all future modules.

The target was:

> **a bounded workspace architecture with safe fallback behavior and explicit extension points, so unknown future Worlds and unknown future specialist surfaces extend the platform rather than force a rewrite.**

This conclusion remains valid.

---

## 2. Future uncertainty was an explicit stress dimension

The old scenario oracle intentionally included:

```text
empty World
very sparse World
very large World
long history
high-frequency observations
multiple providers
provider stale/offline
AI unavailable
partial data
late async response after World switch
same canonical reality in multiple Worlds
sensitive/restricted information
customization while adaptive content changes
unknown future World
unknown future specialist module
reduced motion
narrow viewport
keyboard-only interaction
layout/schema migration
```

Therefore:

> **“we do not yet know every future module/surface” is not a new problem. It was already an architecture input.**

Future work must consume that result instead of restarting the debate.

---

## 3. Composition was already understood as heterogeneous and dynamic

The scenarios covered materially different dimensions:

```text
goals / direction
plans / programs
activities / work
events / schedules
routines / recurrence
actual Sessions
outcomes / observations
quantitative metrics
long time series
categorical breakdown
planned vs actual
pipelines
places / spatial context
documents / artifacts
assets
people / multi-actor context
selective disclosure
provider/external state
reconciliation
temporary contexts
long-lived contexts
sparse/no-metric realities
high-volume history
contextual AI exploration
user personalization
specialist visualization pressure
```

No single dimension became the organizing root of World Focus.

Permanent consequence:

```text
time != World container
metrics != World container
goals != World container
people != World container
artifacts != World container
module kind != Domain ontology
```

The later WR0-WR2 Product Contract sharpened this into question-driven Output Grammar and stable/adaptive/ephemeral composition.

---

## 4. Stable / adaptive / ephemeral behavior was already part of the model

The earlier scenarios distinguished user-stable content from contextually useful adaptive material.

Examples from Music included stable/pinned candidates such as:

```text
current release pipeline
selected active tracks/projects
creative-time trend
upcoming release timeline
chosen performance metric
recent artifacts/versions
```

and adaptive candidates such as:

```text
release becoming schedule-risky
track untouched for a meaningful period
material provider/import change
upcoming milestone needing attention
recent Session/artifact worth resuming
```

Permanent rule retained by current contracts:

```text
stable user-owned composition remains predictable
adaptive content may surface bounded current value
adaptive content must not silently reorder/remove stable user-owned content
ephemeral Insight/query output remains temporary unless deliberately promoted
```

A hidden/removed module does not mean its source reality is false, nonexistent or forbidden to DANTE; composition, relevance and authorization remain separate.

---

## 5. Generic renderer first, specialist renderer only when semantics demand it

The study explicitly rejected one component family per World.

Examples:

### Music

A reusable typed `pipeline`-style presentation could cover release flow; a bespoke `release-pipeline` was **not justified merely because the World is Music**.

### Study

No `study-dashboard` or universal learning-specific page was justified when generic trajectory, planned-vs-actual, timeline, collection, trend and context renderers preserved meaning.

### Finance

Metric/trend/comparison/breakdown/collection primitives were sufficient for the studied pressure; no finance-specific dashboard primitive was required.

### Travel

Travel produced a legitimate specialist candidate because a useful itinerary can require time + place + transport segment + booking + participation in one coherent interaction. A generic map or generic timeline alone may materially lose meaning.

Permanent rule:

> **specialist surfaces are admitted only when a reusable primitive materially damages semantics or interaction quality.**

Unknown future specialist modules are therefore allowed as controlled extensions, not as arbitrary plugins or model-generated UI.

---

## 6. Module kind and presentation variant were already separated

The old stress work identified a required hardening:

```text
module semantic kind != approved presentation variant
```

Current contracts refine this further:

```text
ModuleKind != Domain owner
ModuleKind != World question
renderer != canonical owner
```

A validated projection selects a finite approved renderer. Presentation depth/layout can vary without turning visual variants into ontology.

No remote executable plugin system and no LLM-generated JSX/HTML/JS are authorized.

---

## 7. DANTE was already expected to open deeper contextual material

The scenarios included user requests such as:

```text
“Fammi vedere le prossime 6 settimane di release.”
“Perché questa release è a rischio?”
“Mostrami le versioni del brano X.”
“Fammi vedere l'itinerario completo.”
“Fammi vedere le tappe sulla mappa.”
“Apri cosa c'è dietro questo picco.”
“Apri il materiale collegato alla prossima lezione.”
```

Expected presentation depths already distinguished:

```text
concise contextual response
Insight
comparison
collection
trajectory
source drill-down
Explore
specialist surface where justified
```

WR1/WR2 later formalized the deictic cursor and DANTE presentation depths P0-P5.

Therefore the current implementation problem is **not** to rediscover whether DANTE may contextualize/open deeper surfaces. It may.

What remains to materialize is the controlled workspace mechanism that presents those known semantic intents safely and responsively.

---

## 8. AI Insight -> persistent content was already constrained

The scenario work rejected silent persistence of AI-generated UI.

Durable rule:

```text
AI Insight / ephemeral result
    != automatically persistent widget/module
```

Promotion into stable composition requires an accepted, capability-backed configuration path. In current terminology, DANTE may propose stable configuration; user/product policy decides acceptance.

This protects:

```text
user ownership
predictability
versioning/migration
future concurrency semantics
no silent AI layout mutation
```

---

## 9. Source drill-down and large-data behavior were already studied

A summary/visual must preserve typed traceability toward underlying reality where meaningful.

Examples:

```text
finance aggregate/downsample -> bounded chart projection -> source records on demand
artifact metadata first -> bytes/history only on demand
high-volume history -> bounded projection, not full payload to every widget
provider state -> truthful freshness/stale/unavailable semantics
```

Permanent rule:

```text
no request-per-widget architecture
no all-life-data load
no every-raw-record-to-React pattern
```

Deeper source material is fetched/opened only when the interaction requires it.

---

## 10. Cross-World reuse was already a core constraint

The same canonical reality may participate in several World projections without duplication.

Examples studied include travel reality appearing in Travel, Photography and Finance.

Permanent consequence:

```text
one canonical reality
+ several bounded World projections/configurations
```

A World/module/surface is presentation/context, not canonical ownership.

DANTE may broaden context only through the purpose-scoped authorization/disclosure path established later by WR2.

---

## 11. Schema/version and evolution were already identified

The original work explicitly identified future pressure from:

```text
module schema evolution
layout/config evolution
unknown future modules
unknown future Worlds
migration across presentation versions
```

This does **not** authorize speculative persistence today.

It means any stable future module/layout configuration must eventually support version/revision/migration/concurrency semantics rather than assuming permanent ad-hoc JSON or silent last-write-wins.

---

## 12. Composition/performance budgets were already part of the design pressure

The study did not freeze arbitrary card counts as universal product law.

It required performance-aware bounded composition so sparse, normal and dense Worlds can share one platform.

Later roadmap pressure retained cases such as:

```text
empty
1-2 useful answers
4-8
12
20 potential answers/modules
large history
stale/partial/provider unavailable
AI unavailable
```

If the platform needs a bespoke page branch per World to survive those cases, the platform has failed.

---

## 13. What is already decided and must not be re-researched from zero

```text
World workspace must tolerate unknown future Worlds
World workspace must tolerate unknown future specialist surfaces
no page-per-World architecture
no generic Thing/WorldItem ontology
no arbitrary AI-generated executable UI
finite registered renderer/surface families
specialist renderer only when generic primitives lose meaning
stable vs adaptive vs ephemeral are distinct
AI cannot silently mutate stable composition
DANTE can drive contextual Insight/Explore/deeper-surface intents
source drill-down is typed and on demand
large data is aggregated/bounded before UI
same canonical reality can appear in multiple Worlds
future stable config needs version/evolution semantics
composition must survive sparse and dense Worlds
AI/provider failure stays local
```

These are inputs to implementation, not open discovery questions.

---

## 14. What is still legitimately open

The current contracts intentionally leave concrete presentation decisions open where they were never frozen:

```text
exact World DANTE quiet footprint
composer location
conversation expansion geometry
which semantic depth uses inline vs sidecar vs overlay/full-workspace
surface coexistence/exclusivity rules
focus/back/Escape behavior across simultaneous surfaces
responsive/mobile mapping of those surfaces
exact workspace orchestration state model required to implement them
which future specialist surface kinds become justified by real verticals
```

These are implementation/product interaction decisions inside the already-studied architecture, not reasons to restart the full World/module research.

---

## 15. Continuation rule

When continuing World Focus:

1. consume current Product/Platform contracts;
2. use this file only as recovered research evidence for workspace/module uncertainty;
3. do **not** repeat the old “what if future modules are unknown?” analysis;
4. materialize the smallest production-grade workspace orchestration proven necessary by the accepted semantics;
5. pressure it with contrasting Worlds and unknown/specialist-surface cases already identified;
6. keep backend/API/DB/provider/LLM execution deferred until the final backend vertical.
