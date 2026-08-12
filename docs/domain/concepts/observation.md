# Observation v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Current revision:** 2026-08-12 — Quantity finalized, Register kernel candidate rejected, Subject role finalized  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **An Observation is a persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context. It preserves what was observed or asserted without by itself establishing universal truth, authority, confirmation, Outcome, or evidentiary relevance.**

Observation answers the descriptive reality question:

> **What was observed, reported, measured, or calculated about this subject, and to what time/context does that statement apply?**

Typical forms include:

```text
body weight = 66.4 kg
pain = 4/10
mood = low
room temperature = 21.6 °C
exam score = 78/100
vehicle odometer = 84,220 km
inventory count = 12 units
symptom present = false
```

An Observation may be objective, subjective, manually reported, device-recorded, externally imported, or explicitly derived. Those origins affect Provenance, confidence, authority, reconciliation, and privacy; they do not create separate Observation domain types by themselves.

---

# 1. Why Observation exists

LifeOS needs a reusable way to preserve reality that is neither planned intention nor execution result.

Examples:

```text
Weight
66.4 kg
```

```text
Mood
2 / 5
```

```text
Exam score
78 / 100
```

```text
Vehicle odometer
84,220 km
```

```text
Caregiver report
pain = severe
```

These facts may matter to Goals, routines, decisions, triggers, analytics, assets, health/wellness, finance, learning, maintenance, or later AI reasoning without having been planned in advance.

Without Observation, LifeOS would be pushed toward weak alternatives:

1. store measurements directly on unrelated domain objects;
2. turn Actual into a universal reality container;
3. treat every measured value as an Outcome;
4. make a universal tracker/RegisterEntry the semantic record for all facts;
5. equate raw Quantity values with historical observations;
6. store every specialist fact as opaque JSON;
7. use Evidence as both source fact and evaluation relationship.

Observation provides the bounded record for simple observed/asserted facts while leaving domain-specific events, transactions, outputs, relationships, and conclusions in their proper concepts.

---

# 2. Observation is not a universal fact/blob

Observation is intentionally broad enough to support measurements and simple assertions across life domains, but not broad enough to become a generic database row for everything.

Canonical guardrail:

> **If a real-world fact already has materially richer identity, lifecycle, authority, transaction, execution, or relationship semantics, preserve that concept instead of flattening it into Observation.**

Examples that should not become generic Observations merely because they contain data:

```text
Activity
Event
Session
transaction
inventory movement
file/document
relationship
Goal
Plan
Decision
```

Observation may describe facts about those things, but it does not replace them.

Therefore:

> **Observation is a measurement/simple-assertion concept, not LifeOS's universal event store or semantic fact table.**

---

# 3. Observation versus Actual

Actual reconciles a specific expectation/intention with reality.

Observation can exist with or without any prior expectation.

Example:

```text
Observation
weight = 66.4 kg
```

requires no Goal, Activity, Occurrence, Schedule, Session, or Actual.

When an expectation exists, Observations may describe its realized reality:

```text
Activity
Run 5 km

Actual
run was performed

Observation
distance = 3.8 km

Outcome
partially completed
```

The distance remains an Observation rather than a duplicated Actual field.

Therefore:

> **Observation != Actual.**

---

# 4. Observation versus Outcome

Observation describes a measured/asserted fact.

Outcome describes the contextual result/disposition of an Actual realization.

Example:

```text
Event
Exam

Actual
exam occurred

Observation
score = 78 / 100

Outcome
passed
```

A policy may derive the Outcome from one or more Observations, but the source measurement and semantic result remain distinguishable.

If an external source directly reports `passed`, LifeOS may map that assertion directly into Outcome with Provenance when appropriate; Observation is not a mandatory intermediate wrapper.

Therefore:

> **Observation != Outcome.**

---

# 5. Observation versus Quantity

Quantity is accepted reusable scalar value semantics:

```text
66.4 kg
12 km
45 min
```

Observation is a contextual record using such a value:

```text
Observation
property: body weight
value: Quantity(66.4 kg)
subject: Person P17
subject-effective time: 08:00
```

Quantity can also appear outside Observation:

- Goal criteria;
- Temporal Constraints;
- Capacity;
- inventory thresholds;
- planned effort;
- specifications;
- derived calculations.

Therefore:

> **Quantity != Observation.**

Quantity v0 is canonical value semantics. Money/MonetaryAmount, rating/scale, ratio/percentage, custom-unit, calendar-duration, range and comparator boundaries remain separate dependency questions rather than being silently absorbed into Quantity.

---

# 6. Observation versus longitudinal tracking / historical Register candidate

The feature-discovery simulation identified a useful product need for longitudinal tracking of weight, money, pages, mileage, mood, stock, scores, symptoms, consumption and other records. It proposed `Register + RegisterEntry` as a universal structure.

The Data / Subjects review rejected both **Register as a kernel primitive** and **universal RegisterEntry**.

The validated architecture is:

```text
native semantic records
Observation / Session / future justified domain records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
tracker / history / progress / report UI
```

An Observation may be surfaced in zero, one, or many longitudinal product views without changing identity or being copied into a second semantic record.

Likewise a longitudinal view may combine records whose native semantics are not Observation, provided each source record retains its own identity and rules.

Canonical guardrails:

> **Do not duplicate one Observation merely because it is surfaced in more than one tracker, dashboard, Goal evaluation, report, or specialist view.**

> **No universal RegisterEntry is required between a native record and longitudinal UI.**

A saved tracker/view configuration may exist later as product/application configuration, but persisted configuration does not become an independent source of domain truth merely because it has an application identifier.

Therefore:

```text
Observation != tracker/view configuration
Observation != universal RegisterEntry
longitudinal view != source of truth
```

See `checkpoints/register-v0-validation.md` for the rejected-candidate rationale.

---

# 7. Observation versus Evidence

Evidence is contextual use of information in an evaluation.

An Observation may exist for years without being Evidence for any Goal or criterion.

Later:

```text
Observation
walked 10.4 km

Criterion
weekly distance >= 30 km

Evidence relation/evaluation
uses this Observation
```

The same Observation may support one criterion, conflict with another, or be irrelevant elsewhere.

Therefore:

> **Observation != Evidence.**

Evidence is a role/relationship in evaluation, not a synonym for every observed fact.

---

# 8. Observation versus Confirmation and Provenance

An Observation records what was measured, perceived, reported, asserted, or derived.

It does not by itself answer:

- who supplied the information;
- who actually observed it;
- which device/provider generated it;
- whether the value was reviewed;
- whether an authorized actor accepted it;
- which assertion is currently preferred when sources conflict;
- how confident LifeOS should be;
- who may see it.

Those concerns belong to Confirmation, Provenance and future Authority, Visibility, and reconciliation semantics.

Example:

```text
Observation A
weight = 66.4 kg
source = smart scale

Observation B
weight = 65.9 kg
source = manual entry
```

LifeOS must not merge them silently merely because they concern the same property and similar time.

Therefore:

```text
Observation != Confirmation
Observation != Provenance
source != truth
authority != source by default
```

---

# 9. Observation identity

Observation requires stable LifeOS identity.

Identity is **not** derived from:

```text
subject + property + timestamp + value
```

because two devices, two people, or two providers may make distinct observations with identical apparent values and times.

Example:

```text
Observation O1
08:00
weight = 66.4 kg
smart scale

Observation O2
08:00
weight = 66.4 kg
manual entry
```

These may later be reconciled or recognized as duplicates, but they are not automatically the same assertion.

Canonical rule:

> **Observation identity represents one observation/assertion instance, not a hash of its current fields.**

Provider IDs and client IDs may assist reconciliation but do not become LifeOS identity.

---

# 10. Correction versus new observation

A correction to the same observational act normally preserves Observation identity.

Example:

```text
manual Observation O17
weight = 76.4 kg
```

User corrects a typo:

```text
Observation O17
weight = 66.4 kg
```

Current accepted value changes while relevant history/Provenance should preserve the original assertion and correction.

A new measurement is different:

```text
08:00
66.4 kg

08:10
66.2 kg
```

Those are separate Observations even if they concern the same subject/property.

Therefore:

> **correction of one observation != new observation, while re-observation/re-measurement normally creates a new observation.**

Exact version/correction persistence belongs to Provenance/Version and physical-model review.

---

# 11. Effective time versus recorded/imported time

LifeOS must distinguish when the observed fact applied from when LifeOS received or stored it.

Example:

```text
measurement effective time
08:00

manual entry into LifeOS
18:00
```

The Observation remains about 08:00.

Conceptually distinguish:

- **effective time/context** — when the observed value/finding applies;
- **recorded/ingested time** — when LifeOS received/stored it;
- **issued/source-available time** — when an external source made the assertion available, where relevant;
- **correction time** — when a later change was applied.

Not every Observation needs every timestamp.

Canonical rule:

> **recorded_at must not silently replace effective_time.**

If effective time is imprecise, preserve that uncertainty rather than inventing false precision.

---

# 12. Instant, interval, and aggregate Observations

Observation may describe an instant or a period depending on what the value means.

Examples:

```text
08:00
weight = 66.4 kg
```

```text
00:00-24:00
steps = 11,240
```

```text
training Session interval
average heart rate = 155 bpm
```

An interval aggregate remains an Observation if the asserted fact is the aggregate over that interval.

However:

> **A chart/query aggregate does not automatically need to be persisted as a new Observation.**

Persisted derived/aggregate Observations are justified when they have independent source/provenance/reconciliation value, are imported as such, or must be historically stable/explainable.

Otherwise they may remain derived projections.

---

# 13. Derived Observations

Some observations are explicitly calculated from other facts.

Example:

```text
Observation
height = 1.78 m

Observation
weight = 66.4 kg

Derived Observation
BMI = 20.96
```

A derived Observation must retain enough relationship/Provenance to explain its basis when that matters.

Canonical rules:

- deterministic/declared derivation does not erase source Observations;
- a derived value is not automatically authoritative merely because software computed it;
- changed source values may require recomputation while historical derivation remains explainable;
- AI inference is not silently promoted to confirmed Observation merely because a model generated it.

A probabilistic AI hypothesis may be represented later as an inference/proposal with confidence and Provenance rather than being forced into canonical Observation.

---

# 14. Subjective Observations are valid observations

Observation is not limited to instrument measurements.

Examples:

```text
pain = 4/10
mood = low
fatigue = high
perceived difficulty = 8/10
```

These are legitimate reports about a subject when their subjective nature, source, scale, and context are preserved.

Canonical guardrail:

> **Subjective does not mean invalid, and subjective does not mean universally objective.**

Two people may produce different valid Observations about the same shared context.

Example:

```text
Mattia
meeting usefulness = 4/5

Luca
meeting usefulness = 2/5
```

LifeOS must not average or overwrite those perspectives merely to manufacture one canonical fact.

---

# 15. Negative observation versus missing observation

The absence of an Observation is not equivalent to a negative value.

Example:

```text
no symptom Observation
```

means only that LifeOS lacks that Observation.

This is different from:

```text
Observation
symptom present = false
```

which is an explicit observed/reported negative.

And both differ from:

```text
measurement attempted
result unavailable / sensor failed
```

which is a capture-quality/data-absence condition.

Canonical rule:

> **unknown, observed-negative, and failed/unavailable measurement must remain distinguishable where the domain cares.**

The exact data-absence/status vocabulary is deferred to specialist modeling and future epistemic rules rather than becoming one universal enum immediately.

---

# 16. High-frequency and sampled data

LifeOS must not define semantic correctness in a way that requires one relational Observation row per raw sensor tick.

Examples include:

- continuous heart-rate streams;
- GPS traces;
- accelerometer data;
- temperature telemetry;
- power consumption sampling.

Conceptually such data may be represented by:

- source-native series/sampled records;
- specialist storage;
- compressed segments;
- imported aggregates;
- selected persistent Observations;
- derived projections.

Canonical guardrail:

> **Observation semantics do not mandate one physical row per sample.**

The logical/physical data model will decide which observations deserve individual identity and which high-volume streams use specialist representation.

---

# 17. Multi-component observations

Some real-world measurements are meaningful as one observation with inseparable components.

Example:

```text
blood pressure
systolic = 120 mmHg
diastolic = 80 mmHg
```

Other values are independently interpretable and should normally remain separate observations linked by context.

The kernel must not decide this through arbitrary JSON nesting.

Canonical direction:

> **Use one Observation with components only when the components genuinely share one observational act/context and are not meaningfully independent records; otherwise use separate Observations with explicit relationships/context.**

The final typed-value/component model remains deferred.

---

# 18. Observation and Session/Event context

An Observation may occur during or relate to a Session, Event, Actual, Asset, location, or other context without becoming that context.

Examples:

```text
Session
run

Observation
average HR = 155 bpm
```

```text
Event
exam

Observation
score = 78/100
```

```text
Car

Observation
subject = Car
odometer = 84,220 km
```

Therefore:

> **context relation != Observation identity.**

One Observation may later become relevant to multiple Goals or analyses without duplication.

---

# 19. Subject role and multi-actor semantics

Subject v0 is now canonical as a **semantic role/reference capability**, not an entity or universal root.

For Observation:

> **Subject identifies the native referent whose state/property/condition/asserted fact the Observation primarily concerns. The referenced Person, Asset, Event, Device, Location, or other eligible referent retains native identity.**

Potential dimensions remain:

```text
subject
observer
recorder
source/provider/device
transformer
confirmer/reviewer
authority
viewer
```

These dimensions may coincide in personal use but must not be collapsed universally.

Example:

```text
subject
older adult

observer
caregiver

recorder
caregiver

device
thermometer
```

The record must not imply that the older adult personally entered or asserted the value.

Canonical guardrails:

```text
Subject != Person/Actor/Account identity
Subject != observer
Subject != recorder
Subject != source/provider/device
Subject != transformer
Subject != authority
Subject != viewer
```

A Person or Asset may play Subject role while retaining native identity. Current account holder is not the universal kernel-level Subject default. Unknown or later-corrected subject attribution must preserve material attribution history.

Exact Person/Actor/Account, Asset, Resource, Authority, Visibility, focus/context and generic relationship mechanics remain scheduled adjacent reviews; they do not reopen the basic Subject-role boundary by themselves.

See `concepts/subject.md` and `checkpoints/subject-v0-validation.md`.

---

# 20. Conflicting observations

Conflicting observations are valid reality to preserve.

Example:

```text
Observation A
room temperature = 21.1 °C
sensor A

Observation B
room temperature = 22.0 °C
sensor B
```

or:

```text
Employee self-report
workload = manageable

Manager report
workload = excessive
```

LifeOS must not silently:

- average conflicting values;
- discard one source;
- select the newest source as universal truth;
- give creator/manager/device automatic authority;
- rewrite prior records after reconciliation.

A future reconciliation/Confirmation/Provenance layer may determine which assertion is preferred for a particular purpose while preserving the competing observations.

---

# 21. Privacy and selective disclosure

Observation can contain highly sensitive data.

Examples:

- symptoms;
- mood;
- health measurements;
- financial values;
- work performance ratings;
- location-derived measurements.

A shared Goal/Event/Plan does not automatically make related Observations shared.

Subject association itself may be sensitive: knowing that a hidden record concerns Person X can disclose information even if the value remains hidden.

Private Observations may support authorized derived projections:

```text
private Observation/context
        ↓
authorized computation
        ↓
shareable consequence
```

Example:

```text
private health context
        ↓
capacity reduced today
```

without sharing the underlying symptom/measurement or unnecessary subject detail.

Canonical rule:

> **The ability to compute from an Observation or resolve its Subject does not imply permission to disclose the Observation, Subject association, or private cause.**

---

# 22. AI boundary

AI may:

- summarize Observations;
- detect possible trends;
- propose relationships;
- identify anomalies;
- propose derived values;
- suggest that an Observation may be relevant to a Goal;
- surface conflicting sources;
- propose Subject resolution/matching when imported context is ambiguous.

AI must not silently:

- invent Observations that were never observed/asserted;
- change an Observation's source/Subject;
- replace unknown Subject with the current account holder;
- turn probabilistic Subject matching into established identity without appropriate policy/authority;
- turn uncertain inference into confirmed fact;
- discard conflicting observations;
- disclose private observations or Subject associations to another actor;
- make itself authority over specialist facts merely because it computed them.

Canonical rule:

> **AI inference may create a proposal/inference candidate; it does not automatically create authoritative observed truth or established Subject identity.**

---

# 23. Simple UI versus kernel semantics

Observation should usually appear through natural domain language.

Examples:

```text
Weight
66.4 kg
```

```text
Mood
Low
```

```text
Odometer
84,220 km
```

```text
Exam
78 / 100
```

```text
+ Registra un dato
```

Users should not need to understand the nouns `Observation` or `Subject` for ordinary capture.

Personal product context may safely default the visible subject to `me` when context establishes it, while caregiver/asset flows may expose a natural Person/Asset label.

Power-user/detail surfaces may expose:

- source;
- Subject/referent;
- effective time;
- recorded time;
- device/method;
- corrections;
- confidence/confirmation;
- related raw/derived observations;
- history.

Therefore Observation has mostly **CONTEXTUAL / HIDDEN / ADVANCED** UI exposure.

---

# 24. Validation examples

## Personal measurement

```text
Observation
weight = 66.4 kg
subject = Person(self)
effective = 08:00
recorded = 18:00
```

Passes because effective and recorded times remain distinct and the product may hide the Subject role.

## Caregiver measurement

```text
Observation
subject = Person Maria
temperature = 38.2 °C
observer/recorder = caregiver Anna
```

Passes because Subject and recorder/account roles remain distinct.

## Subjective self-report

```text
Observation
mood = 2/5
subject = Person(self)
source = self-report
```

Passes without pretending the rating is an objective universal state.

## Derived metric

```text
height + weight Observations
        ↓
derived BMI Observation
```

Passes if derivation remains traceable.

## Two conflicting sensors

```text
21.1 °C
22.0 °C
```

Both remain observations until reconciliation policy says otherwise.

## Longitudinal product view

```text
Weight history / tracker
- Observation O1
- Observation O2
- Observation O3
```

The product view queries/surfaces the Observations. It does not own, duplicate, or redefine their identity and no universal RegisterEntry is created.

## Goal evidence

```text
Observation
walked 10.4 km
        ↓
Evidence use
weekly-distance criterion
```

Later evidence use does not rewrite original observation purpose.

---

# 25. Adversarial reductio summary

## REMOVE

Without Observation, measurement/assertion semantics scatter across Actual, Outcome, Goal, Asset, trackers, and specialist modules.

**Result:** REMOVE fails.

## MERGE WITH ACTUAL

Spontaneous measurements have no expectation to reconcile.

**Result:** MERGE fails.

## MERGE WITH OUTCOME

Score/measurement and semantic result/disposition can differ.

**Result:** MERGE fails.

## MERGE WITH QUANTITY

Quantity lacks subject/time/source/identity context and is reused outside Observation.

**Result:** MERGE fails.

## MERGE WITH HISTORICAL REGISTER CANDIDATE

The Register candidate was rejected as a kernel primitive. Longitudinal product views can organize/query Observation and other native records without absorbing or replacing their identity.

**Result:** no merge target is justified; universal RegisterEntry remains rejected.

## REMOVE SUBJECT ENTITY

Subject v0 confirms no independent Subject entity is needed; Observation references the native referent playing Subject role.

**Result:** PASS — entity removal does not weaken Observation.

## REMOVE SUBJECT SEMANTICS

Observation loses the ability to state who/what the assertion is about without overloading account/source/owner.

**Result:** FAIL — Subject role is required.

## MERGE WITH EVIDENCE

Observed fact may never be used in evaluation.

**Result:** MERGE fails.

## MAKE UNIVERSAL

Treating every file, transaction, event, decision, relationship, or domain object as Observation destroys richer semantics.

**Result:** UNIVERSALIZE fails.

## INVERT

Assuming missing Observation means negative/zero/false destroys unknown-state integrity.

**Result:** INVERT fails.

## EXTREME

Raw high-frequency sensor streams show why semantic Observation must not imply one SQL row per tick.

**Result:** bounded concept survives when physical representation remains flexible.

---

# 26. Core invariants

1. **Observation records a measurement/property/state/rating/simple assertion about a Subject referent in an effective context.**
2. **Observation is not a universal fact/event/blob primitive.**
3. **Observation may exist without prior intention, Actual, Outcome, Goal, or saved longitudinal view.**
4. **Observation != Actual != Outcome.**
5. **Observation != Evidence; Evidence is contextual evaluation use.**
6. **Observation != Quantity; Quantity is reusable scalar amount value semantics.**
7. **Observation may appear in zero or many tracker/history/report views without duplication; no universal RegisterEntry is required.**
8. **Observation != Confirmation/Provenance.**
9. **Observation identity != subject + type + time + value.**
10. **Correction of the same observational act normally preserves identity; re-observation normally creates a new Observation.**
11. **Effective time/context != recorded/ingested time.**
12. **Missing Observation != observed negative != failed/unavailable measurement.**
13. **Subjective Observations are valid when perspective/source/context are preserved.**
14. **Conflicting observations may coexist and must not be silently averaged/overwritten.**
15. **Derived Observation does not erase its source facts and is not automatically authoritative.**
16. **Chart/query aggregates do not automatically become persisted Observations.**
17. **Observation semantics do not mandate one physical row per raw sensor sample.**
18. **Subject is a semantic role over native referent identity, not a Subject entity/root.**
19. **Subject != observer != recorder != source != transformer != authority != viewer.**
20. **Current Account is not the universal kernel-level Subject default.**
21. **Unknown/later-corrected Subject attribution preserves material history.**
22. **Private Observation can support an authorized derived projection without source or Subject disclosure.**
23. **AI inference does not automatically create authoritative Observation or established Subject identity.**

---

# 27. Persistence and API implications — deliberately not physical design

Future logical modeling should be capable of representing, where applicable:

- stable Observation identity;
- observed property/type;
- one or more Subject-role references to eligible native referents where the Observation profile allows;
- unresolved/unknown Subject where semantically valid;
- effective instant/period/context;
- typed value semantics, potentially using Quantity or categorical/text/boolean/range forms;
- method/device/source/provenance references;
- correction/supersession history including materially relevant Subject-attribution corrections;
- derived-from relationships;
- context links such as Actual/Session/Event/Asset;
- privacy/authority metadata through future cross-cutting models.

Do not infer from this concept that LifeOS requires:

- one SQL table for every Observation subtype;
- one generic JSON value blob for all observations;
- one row per sensor tick;
- a universal `observations` table containing every domain fact;
- a universal `subjects` wrapper table/root;
- a universal `register_entries` table wrapping longitudinal records;
- provider IDs as canonical identity;
- automatic persistence of every derived aggregate.

High-volume telemetry, financial transactions, documents, and other specialist records may require different physical structures while still contributing Observations/derived views where semantically appropriate.

Final heterogeneous Subject-reference mechanics depend on Person/Actor/Asset/Resource/Relationships review plus logical data-model pressure.

---

# 28. Deliberately deferred questions

The following remain open for later review:

- Person / Actor / Account native identity boundaries;
- Asset eligibility and identity;
- Resource semantics and overlap with Subject-role eligibility;
- focus/context/typed Relationship semantics beyond primary Subject aboutness;
- typed categorical/rating/range/component representation;
- data-quality/measurement-quality vocabulary;
- Authority/Visibility/access semantics;
- high-volume sampled-series physical model;
- Version/correction persistence;
- exact treatment of probabilistic inference versus derived Observation;
- Evidence relationship/evaluation semantics;
- longitudinal query/materialization and optional saved-view configuration;
- specialist medical/financial/scientific observation profiles.

Resolved since the original Observation v0 acceptance:

- Quantity is canonical reusable scalar value semantics;
- Register as a kernel primitive is rejected;
- universal RegisterEntry is rejected;
- Subject is canonical semantic role/reference capability and independent Subject entity/root is rejected.

These remaining dependencies are not reasons to weaken the current Observation boundary.

---

# 29. Reopening triggers

Reopen Observation v0 if later evidence shows that:

1. another accepted semantic record can absorb Observation without losing identity, effective time, source/perspective, correction, conflict, Subject aboutness, or independent existence;
2. Actual/Outcome can naturally represent spontaneous observed facts without semantic overload;
3. Evidence requires source-fact identity to be modeled differently;
4. Person/Actor/Asset/Resource/Relationship design proves the current Subject-role or Observation boundary redundant;
5. high-volume implementation pressure requires a different semantic rather than merely different physical storage;
6. ordinary product capture cannot remain simple without exposing Observation/Subject ontology;
7. multi-actor conflicting assertions or subject-attribution corrections cannot be preserved naturally under the accepted model.

A future product decision to call a screen `Register`, `Tracker`, `History`, `Progress`, or similar is not a reopening trigger by itself.

Until stronger evidence appears, Observation remains the current accepted bounded measurement/simple-assertion concept.