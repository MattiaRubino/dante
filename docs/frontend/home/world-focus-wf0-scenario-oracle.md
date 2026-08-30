# DANTE — World Focus WF0 Scenario Oracle & Stress Matrix

**Status:** WF0 ANALYSIS COMPLETE / USER PRODUCT GATE PENDING / NO UI IMPLEMENTATION YET  
**Date:** 2026-08-30  
**Branch:** `feature/home-react`  
**Scope:** pre-backend World Focus product/architecture stress test  
**Consumes:** `world-focus-handoff.md`, `world-focus-architecture.md`, `world-focus-frontend-roadmap.md`, Home contract, Product North Star, current Domain/Logical/Physical/Database authority, discovery simulations and current frontend production-readiness contracts

---

# 1. Purpose

WF0 exists to answer one question before UI contracts harden:

> Can one World Focus platform represent materially different parts of a person's life without one bespoke page per World, without a giant generic blob, and without creating a fake `World` ontology underneath DANTE?

This document deliberately stresses **dimensions**, not an exhaustive list of future Worlds. No finite scenario set can enumerate every future use. The target is a bounded architecture with safe fallback behavior, explicit extension points and enough pressure that future cases should extend rather than force a rewrite.

WF0 does **not** authorize:

```text
new Domain concepts
new database tables
new Alembic migrations
real backend/API contracts
real provider integrations
real LLM/tool execution
Mondi Overview implementation
Home macro-geometry redesign
```

Historical product simulations are evidence only. Where their old terminology conflicts with later Domain/Logical decisions, the current accepted Domain Atlas and downstream accepted architecture remain authoritative.

---

# 2. WF0 verdict

Current World Focus architecture:

```text
PASS WITH HARDENINGS
```

The platform shape survives the stress set without requiring:

```text
if world === 'music'
if world === 'travel'
if world === 'finance'
...

one renderer per World
one persistence family per World
one generic WorldItem semantic root
arbitrary AI-generated React/HTML
raw database interpretation in the frontend
```

However, the stress test found several contracts that must be added to the implementation plan before the module system is considered production-depth:

1. bounded **World Lens** context for time/scope/filter state;
2. typed **drill-down/source traceability** from summary to underlying reality;
3. module and layout **schema/version evolution**;
4. AI Insight -> persistent widget promotion only through a **stable capability-backed configuration**;
5. explicit **cross-World reuse** with no duplication of canonical reality;
6. performance-aware **composition budgets** without prematurely freezing arbitrary numeric limits;
7. clear separation of **module semantic kind** from its approved presentation variant;
8. no default nested-scroll dashboard behavior;
9. specialist modules only when a reusable primitive materially loses meaning;
10. sensitive/high-consequence presentation metadata without moving safety authority into React.

These are WF0 hardenings, not a redesign of the Domain or current database.

---

# 3. Method

WF0 uses three pressure layers.

## Layer A — deep scenario Worlds

Five Worlds are modeled deeply because they stress substantially different kinds of reality:

```text
Musica
Viaggi
Finanza
Studio
Corpo / Benessere
```

## Layer B — secondary structural Worlds

Seven additional cases test dimensions not sufficiently covered by Layer A:

```text
Casa
Progetto condiviso / lavoro
Veicolo / Asset
Animale / cura
Fotografia
Ricerca lavoro / amministrazione
Relazioni / famiglia
```

## Layer C — adversarial system states

The same architecture is then stressed against:

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
same canonical reality visible in multiple Worlds
sensitive/restricted information
customization while adaptive content changes
unknown future World
unknown future specialist module
reduced motion
narrow viewport
keyboard-only interaction
layout/schema migration
```

Passing WF0 means the architecture remains coherent under all three layers. It does not mean final visual design for each case is frozen.

---

# 4. Stress-dimension ledger

The scenario set intentionally covers the following dimensions.

| Dimension | Primary pressure cases |
|---|---|
| Goals / direction | Musica, Studio, Corpo, Job search |
| Plans / programs | Musica, Viaggi, Studio, Corpo |
| Activities / work | Musica, Studio, Home, Work |
| Events / schedules | Viaggi, Studio, Work, Family |
| Routines / recurrence | Studio, Corpo, Home, Pet |
| Actual / Sessions | Musica, Studio, Corpo, Work |
| Outcomes / observations | Studio, Corpo, Finance, Pet |
| Quantitative metrics | Finance, Corpo, Study, Vehicle |
| Long time series | Finance, Corpo, Vehicle |
| Categorical breakdown | Finance, Job search, Home |
| Planned vs actual | Study, Corpo, Work, Music |
| Pipelines | Music release, Job search, production/work |
| Places / spatial context | Travel, Photography, Home |
| Documents / artifacts | Travel, Music, Study, Vehicle, Admin |
| Assets | Photography, Vehicle, Home |
| People / multi-actor | Travel, Work, Family, Pet care |
| Selective disclosure | Work, Family, Travel |
| Sensitive information | Corpo/Benessere, some Family cases |
| Provider/external state | Travel, Finance, Photography, Music metrics |
| Reconciliation pressure | Finance, provider-imported facts |
| Temporary bounded context | Travel, move/household periods |
| Long-lived context | Home, Vehicle, Study, Music |
| Sparse/no metric reality | Relationships, creative ideation |
| High-volume history | Finance, Work, Vehicle, observations |
| Contextual AI exploration | all primary cases |
| User personalization | all cases |
| Specialist visualization pressure | Travel itinerary strongest; others conditional |

The important result is that no single semantic dimension is used as the organizing root of World Focus. Time, metrics, goals, people and artifacts are all possible facets, not mandatory containers.

---

# 5. Deep scenario A — Musica

## 5.1 Reality shape

A Music World may involve:

```text
Possibilities        song / album ideas
Goals                publish N tracks, finish an album, release by a date
Plans                release plan, production plan
Activities           write, edit, mix, master, artwork, distribution tasks
Sessions             real writing/mixing/mastering episodes
Milestones           lyrics locked, master approved, release submitted
Content Artifacts    lyrics, masters, stems, covers, versions
People               collaborators, producer, designer
Events               release dates, rehearsal, live events
Observations         imported performance/engagement facts
Derived state        release trajectory, time allocation, recent output
```

A product-profile pipeline can be useful, but `Release Pipeline` is not thereby a new Domain primitive.

## 5.2 What the user needs to understand on open

Likely high-value questions:

```text
What is actively moving?
What is blocked or abandoned?
What is next?
What changed recently?
How much actual effort is going where?
Which releases are approaching?
```

The World must not default to a vanity analytics dashboard. Creative continuity and resumability matter at least as much as statistics.

## 5.3 Pinned candidates

Examples:

- current release pipeline;
- selected active tracks/projects;
- weekly creative-time trend;
- upcoming release timeline;
- a chosen performance metric;
- recent artifacts/versions.

## 5.4 Adaptive candidates

Examples:

- one release becoming schedule-risky;
- a track untouched for a meaningful period;
- an imported metric materially changing;
- an upcoming milestone needing attention;
- a recent Session or artifact worth resuming.

Adaptive content must not silently reorder pinned composition.

## 5.5 AI questions and expected presentation depth

| Request | Preferred response |
|---|---|
| “Cosa è in movimento?” | concise prose + focused collection/trajectory |
| “Quale brano ho lasciato più indietro?” | Insight comparison/list with reasons |
| “Quanto tempo ho dedicato alla musica questo mese?” | Metric + trend Insight |
| “Confronta scrittura, mix e mastering.” | Comparison Insight |
| “Fammi vedere le prossime 6 settimane di release.” | Timeline/Explore |
| “Perché questa release è a rischio?” | grounded explanation + trajectory/source drill-down |
| “Cosa è cambiato rispetto alla settimana scorsa?” | change-oriented Insight |
| “Mostrami le versioni del brano X.” | artifact Collection / Explore |

## 5.6 Specialist pressure

A generic `pipeline` module appears sufficient for first implementation if it supports a typed product-profile payload. A bespoke `release-pipeline` module is **not justified yet** merely because the World is Music.

## 5.7 Failure pressure

- imported platform metrics may be stale/unavailable while the rest of the World remains usable;
- artifact version history may be large and must not be eagerly loaded;
- absence of recent Sessions must not be rendered as “no progress” without a valid progress method.

---

# 6. Deep scenario B — Viaggi

## 6.1 Reality shape

A Travel World can span:

```text
Possibility          vague future trip
Goal / Plan          accepted trip direction and plan
Places               cities, accommodation, venues
Events / Schedules   flights, trains, bookings, visits
Content Artifacts    tickets, confirmations, documents
People/Participation travellers, partial participation
Activities           check-in, packing, booking, preparation
Costs                relevant monetary observations/records
Provider state       flight/train/booking updates
Actual reality       what actually happened
```

A trip may be finite but still historically meaningful after completion.

## 6.2 What the user needs to understand on open

```text
What happens next?
What is still missing?
Has anything changed externally?
Where do I need to be and when?
Which documents/bookings matter now?
Who is involved in each segment?
What has the trip cost so far?
```

## 6.3 Pinned candidates

- itinerary;
- next transport/accommodation facts;
- preparation checklist/collection;
- budget/spending view;
- critical documents;
- participant/coordination context where relevant.

## 6.4 Adaptive candidates

- provider schedule change;
- check-in window opening;
- missing document;
- new conflict between itinerary segments;
- weather/context change only when a real integration eventually supports it;
- participation change affecting shared plans.

## 6.5 AI questions

| Request | Preferred response |
|---|---|
| “Cosa manca ancora?” | prioritized collection with source reasons |
| “Fammi vedere l'itinerario completo.” | Explore |
| “Quanto ho speso finora?” | Metric + breakdown |
| “Confronta trasporto e alloggio.” | Comparison |
| “Chi arriva dopo?” | contextual people/timeline view |
| “Quali documenti mi servono domani?” | filtered artifact collection |
| “Ci sono conflitti negli orari?” | Insight with exact schedule basis |
| “Fammi vedere le tappe sulla mappa.” | spatial/itinerary Explore if supported |

## 6.6 Specialist pressure

Travel produces the strongest evidence for a future `travel-itinerary` specialist module because the useful representation can require **time + place + transport segment + booking + participation** in one coherent visual interaction.

A generic map alone is insufficient; a generic timeline alone is also materially weaker.

Decision:

```text
travel-itinerary = specialist candidate justified for WF3/WF4 proof
not automatically part of first universal registry
```

## 6.7 Failure/privacy pressure

- provider state may lag canonical accepted state;
- not all participant travel details are necessarily shareable;
- a shared itinerary fact must not expose private reasons or unrelated calendar detail;
- large document payloads must load metadata first, bytes only on demand.

---

# 7. Deep scenario C — Finanza

## 7.1 Reality shape

WF0 uses finance as a quantitative/reconciliation stress case without inventing a specialist financial Domain model not currently accepted.

Relevant presentation pressure includes:

```text
Monetary Amounts
observed/imported transactions or records when future vertical semantics allow
period totals
balances/snapshots when semantically valid
category/group breakdowns
period comparisons
trend over time
target relationships
reconciliation/provider freshness
```

## 7.2 What the user needs to understand on open

```text
What changed?
What is the current relevant total/balance?
Where is money going?
How does this period compare?
Are there unreconciled/uncertain facts?
Can I drill from summary into the source records?
```

## 7.3 Pinned candidates

- monthly spending metric;
- spending trend;
- selected breakdown;
- target/trajectory when a real Goal semantics exists;
- a reconciliation/status module if a future vertical requires it.

## 7.4 Adaptive candidates

- unusual material change, stated cautiously;
- provider/import stale;
- unreconciled records;
- spending shift relevant to an explicit goal or World context.

No arbitrary “financial health score”.

## 7.5 AI questions

| Request | Preferred response |
|---|---|
| “Come sono andati i conti nell'ultimo mese?” | metric + comparison + breakdown Insight |
| “Solo fotografia.” | refine current Insight scope |
| “Confronta con i tre mesi precedenti.” | comparison/trend Insight |
| “Dove ho speso di più?” | breakdown with drill-down |
| “Mostrami le spese del viaggio.” | scoped collection + total |
| “Quali movimenti non sono riconciliati?” | filtered collection/Explore |
| “Fammi vedere l'andamento degli ultimi 12 mesi.” | bounded/downsampled trend |
| “Apri cosa c'è dietro questo picco.” | drill-down preserving time/category context |

## 7.6 Specialist pressure

No specialist finance widget is required for WF0. Metric/trend/comparison/breakdown/collection cover the current pressure if typed correctly.

## 7.7 Large-data pressure

Finance proves that a module must never receive every raw historical record merely to draw a chart.

Required future principle:

```text
large source history
-> application/query aggregation/downsampling
-> bounded module projection
-> source drill-down on demand
```

---

# 8. Deep scenario D — Studio

## 8.1 Reality shape

```text
Goal                 reach B2 / pass exam / finish course
Plan                 study program
Activity             exercise, chapter, assignment
Routine              recurring practice
Event                 lesson/exam
Schedule/Occurrence   accepted expected instance
Session               actual study episode
Observation           test score / measured result
Outcome               result where applicable
Content Artifact      notes, books, PDFs, exercises
Person                tutor/teacher
Derived               trajectory, planned-vs-actual
```

## 8.2 What the user needs to understand on open

```text
Where am I relative to the desired result?
What should I resume next?
What did I actually do?
Is the plan realistic?
What changed in recent assessments?
Which material is relevant now?
```

## 8.3 AI questions

| Request | Preferred response |
|---|---|
| “Come sono messo con B2?” | trajectory with evidence/method |
| “Quanto ho studiato davvero questa settimana?” | metric + planned-vs-actual |
| “Quali sessioni ho saltato?” | filtered collection |
| “Il ritmo attuale basta?” | cautious trajectory/explanation |
| “Fammi vedere i test degli ultimi tre mesi.” | trend/collection |
| “Su cosa sto andando peggio?” | comparison based on explicit assessment dimensions |
| “Cosa devo riprendere oggi?” | contextual collection / prose |
| “Apri il materiale collegato alla prossima lezione.” | artifact collection |

## 8.4 Specialist pressure

No `study-dashboard` or `learning-world` component is justified. Generic trajectory, planned-actual, timeline, collection, trend and context modules are sufficient at this stage.

---

# 9. Deep scenario E — Corpo / Benessere

## 9.1 Why this case matters

This is the safety/privacy stress case. It proves that the same composition engine can render a sensitive World without letting the UI turn DANTE into a diagnostic/medical system.

Potential relevant realities include:

```text
Goals
Plans / imported professional plans
Activities / Routines
Sessions
Observations
Outcomes where valid
Content Artifacts with source/professional authorship
Derived trends
```

## 9.2 What the user needs to understand on open

```text
What is scheduled/active?
What actually happened?
What trend is visible in confirmed observations?
Which professional/user constraint applies?
What needs attention without implying diagnosis?
```

## 9.3 AI questions

| Request | Preferred response |
|---|---|
| “Quanti allenamenti ho fatto questo mese?” | metric + collection |
| “Confronta pianificato e reale.” | planned-actual |
| “Fammi vedere il sonno delle ultime settimane.” | cautious trend |
| “Cosa è cambiato?” | factual comparison, no causal claim |
| “Apri il piano importato.” | artifact/detail with source |
| “Questa tendenza dipende da X?” | answer must preserve correlation != causation |
| “Modifica le istruzioni professionali.” | future application safety boundary; not silent mutation |
| “Diagnosticami X.” | outside intended product boundary; no visual module should make the request look clinically validated |

## 9.4 Required frontend capability

The module/Insight projection grammar must be able to carry **presentation guardrails** such as:

```text
source/provenance prominence
uncertainty/confidence when applicable
contextual safety notice requirement
professional-plan source distinction
```

The frontend displays these; it does not decide the underlying clinical/legal permission.

---

# 10. Secondary case — Casa

Pressure:

- ongoing operational reality rather than one Goal;
- maintenance, bills, recurring chores, documents, assets;
- household responsibilities and possible multiple actors;
- some modules may have no meaningful metric at all.

Result:

- collection, timeline, context, metric and pipeline-like views cover most needs;
- World Focus must remain useful without a primary Goal;
- no universal “progress of Home” concept is allowed.

---

# 11. Secondary case — Progetto condiviso / lavoro

Pressure:

- dependencies;
- responsibility/participation;
- private personal planning vs shared canonical facts;
- high item volume;
- decisions/reviews;
- selective disclosure.

Result:

- a module must use specific role labels (`Responsible`, `Participant`, etc.) rather than generic `related people` when semantics matter;
- `context` module cannot become a generic relationship graph ontology;
- derived counts/aggregates must still respect disclosure boundaries.

---

# 12. Secondary case — Veicolo / Asset

Pressure:

- identity persists for years;
- mileage/usage observations;
- costs;
- maintenance events;
- documents/expiry;
- threshold/usage-based trigger pressure.

Result:

- generic metric + trend + timeline + artifact collection + context is enough initially;
- no vehicle-specific World page required;
- large history must be summarized first, explored on demand.

---

# 13. Secondary case — Animale / cura

Pressure:

- Living Referent distinct from Person/Asset;
- recurring care routines;
- observations;
- multiple caregivers possible;
- supply/document context;
- real-world uncertainty.

Result:

- the World engine must not assume the World subject is the account owner;
- contextual `subject` semantics remain application/domain responsibility, not a new WorldItem type.

---

# 14. Secondary case — Fotografia

Pressure:

- creative projects;
- equipment Assets;
- Places;
- environmental/provider context;
- files/artifacts;
- trips/events;
- costs.

Result:

- this is a strong cross-World overlap case: the same trip/event/asset may be relevant in both `Viaggi` and `Fotografia`;
- World membership/projection must therefore not duplicate canonical identity.

---

# 15. Secondary case — Ricerca lavoro / amministrazione

Pressure:

- application pipeline;
- contacts/people;
- documents;
- deadlines/events;
- conversion statistics;
- follow-ups;
- long periods of sparse progress.

Result:

- reusable pipeline module is justified as a **product-view family**, not Domain primitive;
- metrics must not imply personal judgment or a universal performance score.

---

# 16. Secondary case — Relazioni / famiglia

Pressure:

- meaningful World with weak or inappropriate quantitative metrics;
- commitments involving people;
- privacy;
- events/history;
- subjective context.

Result:

World Focus must not require statistics, progress percentages or optimization. A valid World can be mostly:

```text
people/context
upcoming shared commitments
recent meaningful reality
artifacts/notes where semantics allow
contextual AI
```

This scenario rejects any architecture that assumes every World needs KPI cards.

---

# 17. Cross-World reality rule

One canonical DANTE reality may be relevant to several Worlds.

Example:

```text
one Event: photographic trip

visible from:
Viaggi
Fotografia
Finanza (cost projection)
Social/Relationships if relevant
```

Required invariant:

```text
multiple projections
!= duplicated canonical Event
```

World Focus module items need stable source/open semantics. They may expose a presentation-level `inclusion reason` or equivalent explanation metadata:

```text
EXPLICIT       user intentionally pinned/included it
SEMANTIC       reached through accepted canonical relationships
CONTEXTUAL     currently surfaced as derived relevance
```

This is a frontend/product projection classification, not a new universal Domain relation.

---

# 18. Candidate World Focus information grammar

WF0 rejects both extremes:

```text
one bespoke page per World              REJECT
one fully generic arbitrary dashboard   REJECT
```

Candidate architecture:

```text
stable World Focus shell
+ finite typed module families
+ approved presentation variants
+ specialist modules only with evidence
+ user-owned stable composition
+ bounded adaptive region
+ ephemeral AI Insight layer
```

---

# 19. Candidate initial module families

These are **frontend module semantics**, not Domain concepts and not backend DTO names.

## 19.1 `metric`

Answers:

> What is the relevant value now / in this selected range?

Payload pressure:

```text
value
unit/format
scope/time basis
optional semantically valid delta
source/freshness
```

No arbitrary score.

## 19.2 `trend`

Answers:

> How has a measured/derived value changed over a defined period?

Payload pressure:

```text
time domain
bounded series
unit
aggregation meaning
optional target/range when semantically valid
source/freshness
```

Approved visual variants may include line, bars or bounded range. Variant does not change semantic kind.

## 19.3 `comparison`

Answers:

> How do explicitly comparable periods/categories/options differ?

The comparison basis must be explicit. It is not a generic ranking engine.

## 19.4 `breakdown`

Answers:

> What contributes to this total/set?

Supports source drill-down by category/group where authorized.

## 19.5 `trajectory`

Answers:

> How does current evidence relate to an explicit Goal/target/desired direction?

Must preserve the accepted progress method. Do not manufacture percentages.

## 19.6 `planned-actual`

Answers:

> What was intended versus what actually happened?

Must not collapse execution, Outcome and Goal progress.

## 19.7 `timeline`

Answers:

> What happens / happened in temporal order in this bounded context?

This is not a replacement for the full DANTE calendar/timeline product surface.

## 19.8 `collection`

Answers:

> Which relevant items belong in this bounded view?

Presentation variants may include list, compact cards or gallery-like artifact view, with typed item payload by profile. Large collections page/virtualize/drill down rather than loading fully.

## 19.9 `context`

Answers:

> Which people, places, assets, artifacts or other explicitly meaningful context matters here?

Must use specific semantic role labels where known. It must not become a generic “relations graph”.

## 19.10 `pipeline`

Answers:

> Where do items sit in an accepted product-profile workflow?

Useful for release, job applications, production/review and similar profiles. Pipeline state remains product-view semantics unless a concrete Domain owner already owns the underlying state.

---

# 20. Specialist module policy

A specialist module is justified only when:

1. several generic modules would fragment one naturally coherent interaction;
2. the combined representation has stable reusable semantics;
3. the specialist representation materially improves understanding/action;
4. it does not invent a new canonical Domain owner;
5. it can still obey common shell/state/a11y/performance contracts.

WF0 specialist candidates:

```text
travel-itinerary       JUSTIFIED CANDIDATE
release-pipeline       NOT YET REQUIRED; generic pipeline likely sufficient
training-session       NOT YET REQUIRED
asset-maintenance      NOT YET REQUIRED
relationship-map       REJECT as generic default
```

Unknown future specialist modules extend the registry; they do not modify the composition engine core.

---

# 21. Semantic kind != presentation variant

A major WF0 hardening is to avoid one module kind per chart style.

Example:

```text
trend
  -> line
  -> bars
  -> range
```

is preferable to:

```text
lineWidget
barWidget
rangeWidget
```

when all three answer the same semantic question.

Conversely, `trajectory` must not be folded into `trend` merely because both can draw a line. Their semantics and valid actions differ.

Rule:

```text
semantic question chooses module kind
approved visual grammar chooses presentation variant
```

---

# 22. World Lens hardening

Several scenarios require a shared exploratory scope without forcing every module into one global filter.

Introduce a frontend-level bounded concept such as `WorldLens` during WF2/WF3.

Potential responsibilities:

```text
selected time range
selected sub-scope/category
temporary user filter
current exploration context
```

Rules:

- lens is presentation/query context, not Domain state;
- modules explicitly declare whether/how they participate;
- a pinned module may intentionally keep a fixed saved scope;
- changing the lens is ephemeral unless user explicitly saves new widget configuration;
- route/deep-link representation may preserve a useful lens later, but URL state is not semantic truth.

This supports natural interactions such as:

```text
“ultimo mese”
-> “solo fotografia”
-> “confronta con i tre mesi precedenti”
```

without rebuilding the page or mutating persistent layout.

---

# 23. Drill-down/source traceability hardening

Every summary module that compresses underlying reality must have a defined route to deeper inspection when that data is legitimately inspectable.

Examples:

```text
finance bar “Fotografia €220”
-> underlying scoped records for that category/time range

study trajectory point
-> contributing assessments/sessions/evidence

music release risk
-> exact schedule/milestone/activity basis
```

Do not encode drill-down as arbitrary URLs supplied by remote/AI payloads.

Use typed semantic intents, conceptually:

```text
OPEN_SOURCE
OPEN_DETAIL
OPEN_SCOPED_COLLECTION
EXPAND_MODULE
```

with the active lens/source context preserved.

This satisfies the product requirement that statistics and insights remain explorable to their basis.

---

# 24. AI Insight grammar

AI-generated visual answers are not arbitrary UI.

Pipeline:

```text
user request
-> contextual conversational interpretation
-> approved capability + typed parameters
-> application/query execution
-> validated InsightProjection
-> registered visual renderer
```

The pre-backend phase simulates the result with deterministic fixtures.

Allowed presentation depth:

```text
PROSE
PEEK
INSIGHT
EXPLORE
```

One request may combine concise prose with one visual surface.

Avoid nested modal chains. A Peek can promote into Insight/Explore rather than opening another independent modal over itself.

---

# 25. Insight -> widget promotion hardening

This is a critical decision.

A one-off AI answer may be pinned only if its meaning can be represented as a stable approved capability configuration.

Correct future shape:

```text
Insight result
+ promotable capability identity
+ validated bounded parameters
+ presentation profile
-> user accepts “Mantieni qui”
-> stable module configuration
```

Forbidden shape:

```text
save raw generated HTML
save raw SQL
save arbitrary JavaScript
save LLM prompt as the only executable query contract
save current result values as if they were the ongoing source
```

The original user request/prompt may be retained as provenance/label/history later if useful, but it cannot be the sole durable execution semantics.

---

# 26. Personalization ownership

Retain the three accepted classes.

## PINNED

Stable and user-owned. DANTE does not silently move/remove it.

## ADAPTIVE

Bounded contextual region. DANTE/application logic may change its content as reality changes.

## EPHEMERAL

Temporary AI/exploration surface. No persistence until explicit promotion.

WF0 additionally requires that adaptive content **cannot repack pinned geometry unpredictably**. Its layout region/slots must be bounded.

---

# 27. Composition budget and anti-sprawl rule

World Focus must remain an application surface, not an infinite dashboard builder.

Do **not** freeze an arbitrary product maximum during WF0. Instead WF3/WF7 must profile at least:

```text
4 modules
8 modules
12 modules
20 modules stress case
```

and choose a deliberate top-level composition budget based on:

- comprehension;
- layout quality;
- keyboard/touch cost;
- payload pressure;
- JS/render cost;
- mobile/narrow behavior.

Potential overflow should move into deeper views/collections rather than making the World Focus infinitely dense.

External product review supports this direction: mature dashboard products often deliberately constrain visible composition and separate everyday viewing from layout editing. DANTE should adopt the principle, not copy another product's exact numeric limit.

---

# 28. Scroll/layout rule

Default rule:

```text
page scroll owns normal World Focus vertical flow
```

Avoid many independent scrolling widgets.

A module that needs large internal browsing should usually:

```text
show bounded summary
-> open Explore/detail
```

Internal virtualization/scroll is acceptable only when the module interaction genuinely requires it (e.g. a large dedicated collection in Explore).

This protects accessibility, trackpad/touch behavior and performance.

---

# 29. Module/version evolution hardening

Each durable module kind/configuration must be versionable.

Conceptual identity:

```text
module kind
module contract/schema version
module instance identity
presentation profile
source/capability configuration
```

Layout must also have its own schema version.

Future rule:

```text
old saved layout/config
-> explicit migration or supported compatibility
-> never silent breakage
```

If a module/capability becomes unavailable, render a truthful recoverable state; do not silently delete the user's pinned composition.

---

# 30. Data-volume pressure

WF0 fixture pressure for later implementation:

```text
EMPTY_WORLD
SPARSE_WORLD                1–2 meaningful modules
NORMAL_WORLD                4–8 modules
DENSE_WORLD                 12 modules
OVERFLOW_STRESS_WORLD       20 modules

SMALL_COLLECTION            10 items
MEDIUM_COLLECTION           200 items
LARGE_SOURCE_COLLECTION     10,000+ source items represented by bounded projection

SHORT_SERIES                30 points
YEAR_SERIES                 365 source points
LARGE_SERIES                10,000+ source points represented by aggregation/downsampling

ARTIFACT_HEAVY              1,000 metadata records, content bytes on demand
MULTI_ACTOR                 20+ participants/context refs without rendering every detail eagerly
```

The module projection must remain bounded even when source history is large.

Exact byte/point caps are intentionally deferred to measured WF7 performance budgets.

---

# 31. Async/race pressure

Mandatory pre-backend scenario:

```text
open Musica
request modules/insight
switch quickly to Viaggi
Musica response resolves late
```

Invariant:

```text
late Musica completion MUST NOT overwrite Viaggi state
```

The same applies to:

- module lazy-load completion;
- AI/Insight scenario completion;
- layout/customization async operations;
- route exit/unmount.

Use request identity/abort/cancellation or equivalent deterministic ownership.

---

# 32. Provider/staleness pressure

A World can remain usable when one provider-backed module is stale or unavailable.

Example:

```text
Musica canonical plans/activities      READY
streaming-platform metrics             STALE/UNAVAILABLE
```

Page behavior:

```text
World Focus remains READY/PARTIAL
provider module degrades locally
freshness/source shown where relevant
```

No provider failure may rewrite canonical DANTE state automatically.

---

# 33. AI-unavailable pressure

Invariant:

```text
AI unavailable
!= World Focus unavailable
```

Structured GUI remains fully inspectable. AI composer/Insight capability reports truthful unavailable state without blanking pinned/adaptive content.

---

# 34. Privacy/disclosure pressure

Multi-actor and sensitive scenarios expose a critical rule:

```text
frontend hiding != authorization
```

The future backend/application projection must already be disclosure-safe before payload reaches the component.

The frontend must not assume it is safe to show:

- hidden-source explanation text;
- exact counts that reveal concealed records;
- private reasons behind availability;
- sensitive values because a generic module can render them.

A “restricted” placeholder itself can leak existence. Therefore the authoritative projection decides whether absence, unavailable, redacted summary or nothing at all is safe.

---

# 35. Safety/high-consequence presentation pressure

For health/wellness and future consequential capabilities, the presentation layer must support explicit metadata such as:

```text
requires contextual notice
source prominence
confidence/uncertainty
professional-source marker
high-consequence confirmation handoff
```

But React must not infer risk from labels like `health` or `medicine`.

Risk/safety semantics are decided by application/backend capability contracts when the vertical exists.

---

# 36. Unknown future World test

Counterexample:

```text
World = “Orto”
```

Potential content:

- recurring activities;
- observations;
- quantities;
- weather/provider data;
- assets/tools;
- places;
- costs;
- photos/artifacts.

Result:

The core registry can still render useful metric, trend, timeline, collection and context modules without a dedicated `OrtoPage`.

If a future crop-cycle interaction proves special, it becomes a specialist module rather than a new World engine.

PASS.

---

# 37. Unknown qualitative World test

Counterexample:

```text
World = “Amicizie”
```

Potential meaningful content may contain almost no numerical telemetry.

Result:

A valid World Focus can be composed from context, upcoming events/commitments, recent reality and AI exploration.

No mandatory metric/progress slot exists.

PASS.

---

# 38. External product-pattern review — non-authoritative evidence

WF0 reviewed current patterns from large/mature products only as UI/system evidence. They do not override DANTE contracts.

Useful principles observed:

## Notion dashboard views

- stable View mode separated from Edit mode;
- constrained widget composition rather than unlimited free-form dashboard behavior;
- performance guidance explicitly favors filtered summaries and drill-down instead of huge unfiltered views.

DANTE adoption:

```text
consume mode != customize mode
bounded composition
summary -> deeper inspection
```

Do not copy Notion's database-centric semantics.

## Apple Smart Stack / widgets

- adaptive relevance can coexist with explicitly pinned widgets;
- pinned items preserve stable user ownership.

DANTE adoption:

```text
PINNED != ADAPTIVE
```

## Linear Peek

- quick inspection can preserve the current context and keyboard flow.

DANTE adoption:

```text
PEEK as temporary inspection depth
not every detail requires route replacement/full page
```

## Airtable dashboard interfaces

- high-level summary supports drill-down to underlying records;
- filters can affect multiple visual elements without changing the underlying source data.

DANTE adoption:

```text
WorldLens
source-preserving drill-down
```

## Grafana dashboards

- panels separate query/data processing from visual presentation;
- drill-down can preserve time range/filter context.

DANTE adoption:

```text
typed projection boundary
lens context propagation
bounded summaries -> detail
```

## Home Assistant sections

- constrained sections/grids improve layout stability;
- automatic dense placement trades compactness against user control.

DANTE adoption:

```text
stable deterministic placement
adaptive content must not arbitrarily repack pinned user layout
```

---

# 39. Rejected generalizations

WF0 explicitly rejects:

```text
World = Domain entity
World = life-area taxonomy
World = folder
World = generic database
WorldItem universal entity
one full custom React page per World
one generic blob widget with hundreds of optional fields
arbitrary JSON-to-UI renderer
LLM-generated JSX/HTML/JavaScript
LLM-generated SQL as durable widget definition
one request per widget by default
loading all World source history on open
one chart component used for semantically different questions
mandatory KPI/statistics region for every World
mandatory Goal/progress for every World
unbounded adaptive AI rearrangement
nested modal stack
many independent scroll panes
saving Insight values as canonical truth
```

---

# 40. WF0 hardening ledger

The following must carry into WF1–WF8.

```text
WF0-H01  WorldProjection remains noncanonical.
WF0-H02  World Lens is bounded presentation/query context.
WF0-H03  Summaries support typed source drill-down where legitimate.
WF0-H04  Module semantic kind is separate from presentation variant.
WF0-H05  Module and layout contracts are versionable.
WF0-H06  Insight promotion requires stable capability-backed config.
WF0-H07  Same canonical reality may appear in multiple Worlds without duplication.
WF0-H08  PINNED / ADAPTIVE / EPHEMERAL ownership remains explicit.
WF0-H09  Adaptive content cannot unpredictably repack pinned geometry.
WF0-H10  Specialist modules extend registry; they do not fork World Focus.
WF0-H11  Large source datasets are reduced to bounded projections.
WF0-H12  Page-level normal scroll preferred over widget-scroll proliferation.
WF0-H13  Provider/AI/module failures isolate locally when possible.
WF0-H14  Late async completion cannot overwrite the active World.
WF0-H15  Safety/disclosure semantics are supplied by authoritative capability/projection layers, not guessed in React.
WF0-H16  Unknown future Worlds must degrade to useful core modules before specialist work is required.
```

---

# 41. Candidate default page grammar — not pixel layout

WF0 does not freeze exact visual geometry, but the information ownership should follow:

```text
WORLD FOCUS SHELL
  identity / navigation / ambient theme

STABLE COMPOSITION
  user-owned pinned modules

BOUNDED ADAPTIVE REGION
  current relevant DANTE projections

CONTEXTUAL DANTE AI
  active World context + optional selected module/lens context

INSIGHT LAYER
  ephemeral Peek / Insight / Explore
```

The page must feel like:

> “Understand this part of my life and continue from here.”

not:

> “Here are twelve unrelated KPI cards.”

---

# 42. WF0 fixture specification for later implementation

WF2/WF3 deterministic fixtures should include at minimum:

```text
world-music-normal
world-travel-normal
world-finance-normal
world-study-normal
world-wellness-sensitive
world-home-no-primary-goal
world-relationships-qualitative
world-crosslink-photography-travel
world-empty
world-sparse
world-dense
world-overflow-stress
world-provider-stale
world-module-error
world-ai-unavailable
world-race-switch
world-reduced-motion
```

For primary Worlds, fixtures must include enough data to drive the AI questions listed above through deterministic `runScenarioInsight` behavior without pretending a real LLM exists.

---

# 43. WF0 exit-gate assessment

## Same platform across contrasting Worlds

```text
PASS
```

## No page branch per World required

```text
PASS
```

## No giant generic semantic blob required

```text
PASS — provided module families remain discriminated and typed
```

## Unknown future World fallback

```text
PASS
```

## Specialist extension path

```text
PASS — travel itinerary is a valid first candidate
```

## AI visual answer path

```text
PASS — capability -> typed Insight -> registered renderer
```

## AI result promotion path

```text
PASS WITH WF0-H06
```

## Large-data path

```text
PASS WITH bounded projection/downsampling/paging hardening
```

## Sensitive/multi-actor path

```text
PASS architecturally; authoritative backend disclosure/safety remains future vertical responsibility
```

## Product feel gate

```text
PENDING USER REVIEW
```

WF0 analysis is complete. It becomes **WF0 CLOSED** only after the user accepts the product grammar/hardenings sufficiently to proceed to WF1.

---

# 44. Exact next step after user gate

If WF0 receives product PASS:

```text
WF1
Route / shell / immersive entry transition foundation
```

WF1 must start with an empty/minimal composition canvas. Do **not** implement the full module registry during the transition work.

The first visible proof should establish:

```text
Home centered World
-> open World Focus
-> shared immersive transition
-> correct route/history/back
-> correct return to Home state
-> one parameterized WorldThemeProfile
-> reduced-motion equivalent
-> no Home geometry regression
```

Only after that shell/entry ownership is frozen does WF2/WF3 materialize the application contracts and module engine.
