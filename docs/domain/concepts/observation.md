# Observation v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
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
4. make RegisterEntry the universal semantic record for all facts;
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

Quantity is value semantics:

```text
66.4 kg
12 km
45 min
€18.50
```

Observation is a contextual record using such a value:

```text
Observation
property: body weight
value: 66.4 kg
subject: person
subject-effective time: 08:00
```

Quantity can also appear outside Observation:

- Goal criteria;
- Temporal Constraints;
- Capacity;
- inventory thresholds;
- prices;
- budgets;
- planned effort;
- derived calculations.

Therefore:

> **Quantity != Observation.**

The final Quantity value-object/unit model belongs to the Data/Subjects cluster.

---

# 6. Observation versus Register

The feature-discovery simulation identified Register as a longitudinal organization/analysis capability for data such as weight, money, pages, mileage, mood, stock, scores, symptoms, and consumption.

Observation and Register answer different questions:

```text
Observation
What fact was observed/asserted?

Register
Which longitudinal collection/view/policy organizes records over time?
```

A Register may contain or surface Observations, but it may also organize other semantic records such as transactions, movements, specialist entries, or snapshots.

Likewise an Observation may exist without any explicit user-visible Register.

Canonical guardrail:

> **Do not duplicate one Observation merely because it is surfaced in more than one Register, dashboard, Goal evaluation, or specialist view.**

Therefore:

> **Observation != Register and Observation != universal RegisterEntry.**

Exact Register/RegisterEntry persistence remains deferred to the Data/Subjects cluster.

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

Those concerns belong to future Confirmation, Provenance, Authority, Visibility, and reconciliation semantics.

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

The exact data-absence/status vocabulary is deferred to Confirmation/Provenance and specialist modeling rather than becoming one universal enum immediately.

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
Asset
car

Observation
odometer = 84,220 km
```

Therefore:

> **context relation != Observation identity.**

One Observation may later become relevant to multiple Goals or analyses without duplication.

---

# 19. Multi-actor semantics

Observation must remain structurally multi-actor-ready.

Potential dimensions include:

```text
subject
observer
recorder
source/provider/device
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

Canonical guardrail:

> **Observation subject != observer != recorder != source != authority != viewer.**

Exact Actor/Subject/Authority/Visibility relationships remain deferred to their dedicated clusters.

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

without sharing the underlying symptom/measurement.

Canonical rule:

> **The ability to compute from an Observation does not imply permission to disclose the Observation or explain a result using its private cause.**

---

# 22. AI boundary

AI may:

- summarize Observations;
- detect possible trends;
- propose relationships;
- identify anomalies;
- propose derived values;
- suggest that an Observation may be relevant to a Goal;
- surface conflicting sources.

AI must not silently:

- invent Observations that were never observed/asserted;
- change an Observation's source/subject;
- turn uncertain inference into confirmed fact;
- discard conflicting observations;
- disclose private observations to another actor;
- make itself authority over specialist facts merely because it computed them.

Canonical rule:

> **AI inference may create a proposal/inference candidate; it does not automatically create authoritative observed truth.**

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

Users should not need to understand the noun `Observation` for ordinary capture.

Power-user/detail surfaces may expose:

- source;
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
subject = person
effective = 08:00
recorded = 18:00
```

Passes because effective and recorded times remain distinct.

## Subjective self-report

```text
Observation
mood = 2/5
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

## Register view

```text
Weight Register
- O1
- O2
- O3
```

The Register organizes observations; it does not redefine their identity.

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

Without Observation, measurement/assertion semantics scatter across Actual, Outcome, Register, Goal, Asset, and specialist modules.

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

## MERGE WITH REGISTER

Register is longitudinal organization/analysis; Observation is one semantic observed assertion. Each can exist without the other.

**Result:** MERGE fails.

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

1. **Observation records a measurement/property/state/rating/simple assertion about a subject in an effective context.**
2. **Observation is not a universal fact/event/blob primitive.**
3. **Observation may exist without prior intention, Actual, Outcome, Goal, or Register.**
4. **Observation != Actual != Outcome.**
5. **Observation != Evidence; Evidence is contextual evaluation use.**
6. **Observation != Quantity; Quantity is reusable value/unit semantics.**
7. **Observation != Register; Register is longitudinal organization/analysis.**
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
18. **Subject != observer != recorder != source != authority != viewer.**
19. **Private Observation can support an authorized derived projection without source disclosure.**
20. **AI inference does not automatically create authoritative Observation.**

---

# 27. Persistence and API implications — deliberately not physical design

Future logical modeling should be capable of representing, where applicable:

- stable Observation identity;
- observed property/type;
- subject/focus semantics;
- effective instant/period/context;
- typed value semantics, potentially using Quantity or categorical/text/boolean/range forms;
- method/device/source/provenance references;
- correction/supersession history;
- derived-from relationships;
- context links such as Actual/Session/Event/Asset;
- privacy/authority metadata through future cross-cutting models.

Do not infer from this concept that LifeOS requires:

- one SQL table for every Observation subtype;
- one generic JSON value blob for all observations;
- one row per sensor tick;
- a universal `observations` table containing every domain fact;
- provider IDs as canonical identity;
- automatic persistence of every derived aggregate.

High-volume telemetry, financial transactions, documents, and other specialist records may require different physical structures while still contributing Observations/derived views where semantically appropriate.

---

# 28. Deliberately deferred questions

The following remain open for later review:

- exact Quantity/unit/type model;
- Register/RegisterEntry identity and whether some product Register entries directly reference Observations or specialist records;
- Subject/Actor/Person/Asset boundaries;
- typed value/component representation;
- data-quality/measurement-quality vocabulary;
- Confirmation/epistemic states;
- Provenance/assertion/source model;
- Authority/Visibility/access semantics;
- high-volume sampled-series physical model;
- Version/correction persistence;
- exact treatment of probabilistic inference versus derived Observation;
- Evidence relationship/evaluation semantics;
- specialist medical/financial/scientific observation profiles.

These are dependencies, not reasons to weaken the current Observation boundary.

---

# 29. Reopening triggers

Reopen Observation v0 if later evidence shows that:

1. Register/Quantity can absorb Observation without losing identity, effective time, source/perspective, correction, conflict, or independent existence;
2. Actual/Outcome can naturally represent spontaneous observed facts without semantic overload;
3. Evidence requires source-fact identity to be modeled differently;
4. Subject/Provenance design proves the current Observation boundary redundant;
5. high-volume implementation pressure requires a different semantic rather than merely different physical storage;
6. ordinary product capture cannot remain simple without exposing Observation ontology;
7. multi-actor conflicting assertions cannot be preserved naturally under the accepted model.

Until such evidence appears, Observation remains the current accepted bounded measurement/simple-assertion concept.