# Quantity v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **A Quantity is reusable scalar value semantics representing an amount through a numerical magnitude together with unit semantics sufficient to interpret that amount. A Quantity has no independent subject, property, time, identity, provenance, intention, observation history, or evaluative meaning. Comparison, conversion, and arithmetic are valid only where the unit/scale semantics and the surrounding quantity-kind context make those operations semantically valid.**

Quantity answers the bounded value question:

> **What amount is represented, and under which unit semantics can that amount be interpreted?**

Examples:

```text
66.4 kg
5 km
45 min
21.6 °C
12 L
30 pages
```

Quantity is **value semantics**, not an independently persistent domain entity.

---

# 1. Why Quantity exists

LifeOS uses scalar amounts across many domains:

- Observation values;
- Goal criteria and thresholds;
- planned and actual effort;
- Temporal Constraints;
- Capacity;
- Asset specifications;
- inventory/scarcity views;
- specialist records;
- future Register aggregation/evaluation.

Without a bounded reusable Quantity abstraction, every concept would reinvent magnitude, unit, conversion, precision and comparison behavior, or LifeOS would fall into a universal untyped `number + unit_text` anti-pattern.

Quantity centralizes reusable amount semantics while leaving contextual meaning in the containing concept.

---

# 2. Quantity is value semantics, not an entity

A Quantity does not require its own stable domain identity merely because the same magnitude/unit pair appears in many places.

```text
Observation
value = Quantity(66.4 kg)

Goal criterion
threshold = Quantity(65 kg)

Asset specification
max load = Quantity(66.4 kg)
```

These are separate contexts that may use equivalent Quantity values. LifeOS does not need a shared `Quantity ID` connecting them.

Canonical rule:

> **The lifecycle, provenance, correction history, authority, privacy and identity belong to the containing record or rule, not to an independently owned Quantity object.**

Physical reuse or value normalization may later be optimized without turning Quantity into an aggregate root.

---

# 3. Numeric value does not automatically mean Quantity

Numeric representation alone is insufficient.

Examples that are not automatically Quantity:

```text
priority = 2
rank = 3
version = 4
identifier = 912
mood rating = 4/5
```

Those may represent ordinal, identifier, version, rating/scale or other semantics.

Canonical rule:

> **`number != Quantity` unless the value represents an amount whose scalar/unit semantics are materially meaningful.**

This prevents Quantity from becoming LifeOS's universal numeric wrapper.

---

# 4. Quantity versus Observation

Quantity is reusable amount/value semantics.

Observation is a contextual record of a measured, perceived, reported or derived property/state/value about a subject at an effective time/context.

```text
Quantity
66.4 kg
```

contains no claim about:

- body weight;
- a person;
- 08:00;
- who measured it;
- device/provider;
- provenance;
- confirmation;
- evidence relevance.

By contrast:

```text
Observation
property: body weight
subject: person
value: Quantity(66.4 kg)
effective time: 08:00
```

is a historical contextual assertion.

Therefore:

> **Quantity != Observation.**

Observation may use Quantity without duplicating Quantity semantics, and Quantity may appear outside Observation.

---

# 5. Quantity versus Register

Quantity is one scalar amount.

Register is expected to be a longitudinal organization/evaluation capability over records through time.

```text
Quantity
66.4 kg
```

versus:

```text
Weight Register
06 Aug -> Observation 66.8 kg
07 Aug -> Observation 66.5 kg
08 Aug -> Observation 66.4 kg
```

Quantity does not decide:

- which records belong together;
- which Subject/property the series represents;
- whether sum/average/last/min/max/trend is meaningful;
- balance semantics;
- continuity/gaps;
- privacy policy;
- source inclusion policy.

Therefore:

> **Quantity != Register and Quantity != RegisterEntry.**

Exact Register semantics remain a mandatory Data / Subjects review.

---

# 6. Property / quantity-kind context is not the unit

The unit says how an amount is represented. It does not by itself say what domain property is being measured.

```text
property: body weight
value: 66.4 kg
```

is preferable to inventing contextual units such as:

```text
66.4 kg_body_weight
```

Canonical rule:

> **Property/quantity-kind semantics remain outside the basic unit token. Unit semantics must not be overloaded to encode the full domain meaning of the measured property.**

This also means dimensional compatibility alone is not enough to conclude that two domain values are semantically interchangeable.

---

# 7. Conversion and semantic comparability

Unit conversion is valid only when the units and the surrounding quantity-kind context make the conversion meaningful.

Example:

```text
66.4 kg <-> 146.4 lb
```

can represent equivalent mass quantities.

However:

> **Unit/dimensional compatibility is necessary for many conversions but is not sufficient to establish domain-semantic equivalence.**

LifeOS must not infer that two values are comparable merely because their units reduce to the same physical dimension.

The containing Observation, criterion, specification or other domain context identifies what is actually being compared.

---

# 8. Same unit does not imply every arithmetic operation is valid

Two values using the same unit are not automatically additive, averageable, ratio-safe or otherwise algebraically interchangeable.

Examples:

```text
20 °C + 25 °C
```

is not an ordinary meaningful temperature aggregation merely because both values use °C.

Likewise:

```text
60% + 70%
```

is not automatically `130%` in an evaluation context.

Canonical rule:

> **Quantity compatibility does not grant universal aggregation semantics. Aggregation policy belongs to the containing domain/evaluation/Register context.**

Scale/ratio/percentage semantics are explicitly tracked for the post-Cluster-4 dependency closure.

---

# 9. Source representation versus normalized/display representation

LifeOS may normalize equivalent units for computation or indexing while preserving how a source actually represented the value.

Example:

```text
provider representation
5.00 km

normalized computation representation
5000 m
```

Normalization must not rewrite source history as though the provider originally sent the normalized form.

Canonical rule:

> **Normalization/display conversion changes representation, not historical source assertion. Material source representation and conversion lineage belong to the containing record's Provenance where needed.**

Precision/rounding must likewise not be silently fabricated or upgraded.

---

# 10. Actor-specific display preferences

Unit preference is presentation/context state rather than separate canonical reality.

One shared Observation can be displayed as:

```text
Actor A -> 66.4 kg
Actor B -> 146.4 lb
```

without creating two Observations or two independently owned Quantity records.

Canonical rule:

> **Actor-specific display-unit preference does not change canonical/source information and does not duplicate shared facts.**

This keeps Quantity compatible with Multi-Actor Readiness v1.

---

# 11. Custom units

LifeOS needs room for practical user/domain units such as:

```text
pages
reps
boxes
scoops
tanks
servings
```

But a label does not create a universal conversion rule.

Example:

```text
1 scoop
```

may equal 30 g only for a particular product/definition/context.

Therefore:

> **Custom unit label != globally valid conversion definition.**

A future custom UnitDefinition/value-semantics review may be justified if conversion, versioning, sharing or domain validation requires it. Quantity v0 does not pre-approve a global Unit entity/catalog beyond what implementation later proves necessary.

---

# 12. Precision and numerical semantics

Quantity should preserve decimal magnitude semantics sufficient for the domain and should not canonically depend on incidental binary floating-point artifacts.

This is a semantic constraint, not a final PostgreSQL/Python type decision.

LifeOS must be able to distinguish where relevant:

- source precision;
- stored computational precision;
- display rounding;
- conversion rounding.

A display such as `66.4 kg` must not silently claim a precision the source never supplied.

---

# 13. Money / MonetaryAmount boundary

Money is deliberately not collapsed into ordinary Quantity v0.

```text
100 EUR -> USD
```

requires time/source/policy-dependent FX semantics, unlike stable physical-unit conversion such as:

```text
1 kg -> 1000 g
```

Quantity v0 therefore records:

> **Currency-like scalar values may reuse parts of amount semantics, but LifeOS does not yet define Money/MonetaryAmount as an ordinary Quantity unit specialization.**

This boundary is a mandatory post-Cluster-4 dependency-closure item.

---

# 14. Duration / calendar-time boundary

Elapsed-duration amounts may use Quantity-like semantics:

```text
45 min
12 h elapsed
```

But calendar-relative constructs must not be reduced automatically:

```text
1 calendar month != universally 30 days
```

The accepted Time cluster already preserves calendar/wall-clock/elapsed distinctions.

Canonical guardrail:

> **Quantity must not collapse calendar-relative temporal semantics into fixed elapsed-unit arithmetic.**

The exact Duration/value boundary is deferred to dependency closure/logical modeling unless a later concept makes it structural.

---

# 15. Range / threshold / comparator boundary

A Quantity represents one scalar amount, not a comparison rule or interval.

```text
65-67 kg
```

is better understood as a range using Quantity endpoints.

```text
weight >= 65 kg
```

contains comparator/criterion semantics around a Quantity threshold.

Therefore:

```text
Quantity != Range
Quantity != Threshold rule
Quantity != comparator / criterion
```

Final Range/criterion representation remains deferred.

---

# 16. Composite values

Composite measurements should not be forced into one universal Quantity.

Examples:

```text
blood pressure
120 mmHg systolic
80 mmHg diastolic
```

```text
exercise structure
3 sets x 10 reps x 20 kg
```

These structures may contain several Quantity/scalar values with different property roles.

Canonical rule:

> **Multiple scalar components with distinct semantic roles remain a composite structure; Quantity does not absorb the structure merely because each component is numeric.**

---

# 17. Multi-actor, privacy and authority

Quantity itself normally has no actor ownership, authority or visibility lifecycle independent from its container.

Canonical guardrails:

```text
Quantity identity != Actor
Quantity display preference != canonical value mutation
Quantity visibility normally follows containing record/context
custom unit label by Actor A != automatically same definition for Actor B
```

AI may perform deterministic conversions when unit/context compatibility is established, but must not invent custom conversion definitions, assume semantic comparability from dimensions alone, or disclose a private containing record merely because the numerical conversion is harmless.

---

# 18. Scale and persistence pressure

Quantity semantics must not require one database row per scalar value.

Ten years of measurements, high-frequency imports and large registers would make independent Quantity entities wasteful and misleading.

Possible future physical forms include:

- embedded value object columns;
- typed structures;
- domain-specific optimized storage;
- normalized unit codes/value columns;
- specialist high-frequency storage.

Quantity v0 does not choose the physical representation.

---

# 19. External benchmark interpretation

External standards are benchmark evidence, not LifeOS design authorities.

Useful patterns:

- **UCUM** demonstrates computable unit semantics, dimensional compatibility and the need to distinguish unit representation from domain-property meaning.
- **HL7 FHIR Quantity** demonstrates a reusable measured-amount datatype with magnitude and unit/code semantics rather than an independent business entity.
- **HL7 FHIR Range** reinforces that interval semantics can be composed from Quantity endpoints instead of bloating Quantity itself.
- **HL7 FHIR Money** is useful anti-collapse evidence that currency amounts can justify semantics distinct from ordinary physical-unit conversion.

LifeOS adopts the bounded lessons, not the healthcare resource model.

---

# 20. Current invariants

1. Quantity is canonical reusable value semantics, not an independent domain entity.
2. `number != Quantity` by default.
3. Quantity represents a scalar amount through magnitude + unit semantics sufficient for interpretation.
4. Quantity has no independent Subject, property, effective time, Provenance, Confirmation, Evidence, ownership or history.
5. `Quantity != Observation`.
6. `Quantity != Register` and `Quantity != RegisterEntry`.
7. Property/quantity-kind context is not encoded by overloading the unit token.
8. Unit/dimensional compatibility alone does not establish domain-semantic equivalence.
9. Same/compatible unit does not grant universal aggregation/arithmetic permission.
10. Source representation and actor/display representation may differ without changing the underlying fact.
11. Unit preference does not duplicate canonical data.
12. Custom unit label does not establish a globally valid conversion rule.
13. Normalization does not rewrite historical source representation.
14. Precision/rounding semantics must not be silently fabricated.
15. Money/MonetaryAmount is not pre-collapsed into ordinary Quantity.
16. Calendar-relative time is not pre-collapsed into elapsed Quantity arithmetic.
17. `Quantity != Range / Threshold / comparator / criterion`.
18. Composite numeric structures are not forced into one Quantity.
19. AI may convert validated compatible values but must not invent semantic or custom conversion rules.
20. Quantity semantics do not imply a standalone SQL table or one persisted record per scalar value.

---

# 21. Rejected alternatives

## Universal numeric wrapper

Rejected because identifiers, ordinal values, ratings, versions and domain scores do not automatically share amount/unit semantics.

## Quantity as persistent entity

Rejected because it creates meaningless identity/history and severe row explosion while the real lifecycle belongs to the containing concept.

## Quantity as Observation

Rejected because Quantity may be used in criteria, constraints, capacity and specifications without being an observed historical fact.

## Put property inside the unit

Rejected because it conflates measurement/property semantics with unit semantics and damages interoperability/conversion.

## Same dimension means same semantic value

Rejected because dimensional compatibility is weaker than domain meaning.

## Every currency is an ordinary unit

Rejected pending dedicated MonetaryAmount boundary review because FX conversion is contextual and time/source dependent.

## Every duration/calendar period is ordinary Quantity

Rejected because accepted Time semantics distinguish elapsed duration from calendar-relative/wall-clock meaning.

---

# 22. Dependency register for transition cluster

Data / Subjects predates the fully mandatory Adjacent Dependency Sweep. The following obligations are therefore recorded now and must be classified during the post-Cluster-4 Deferred Dependency Closure unless a later Cluster 4 concept resolves them earlier.

| Boundary | Current treatment | Closure expectation / trigger |
|---|---|---|
| Quantity vs Register aggregation semantics | open but non-blocking | Re-test during Register review; must be RESOLVED or REOPEN before Cluster 4 closure |
| Quantity vs Money / MonetaryAmount | SAFE-DEFER candidate, not yet final | Post-Cluster-4 dependency closure; reopen if finance workflows cannot remain correct without distinct value semantics |
| Quantity vs ratings/scales | SAFE-DEFER candidate | Revisit with Register/Observation data-shape review |
| Quantity vs ratio/percentage/count | SAFE-DEFER candidate | Revisit with Register/GoalCriterion semantics |
| Quantity vs custom UnitDefinition | SAFE-DEFER candidate | Reopen if custom conversion/version/sharing requires independent semantics |
| Quantity vs elapsed Duration/calendar-relative time | SAFE-DEFER candidate | Re-test against Time cluster during dependency closure |
| Quantity vs Range/Threshold/comparator | SAFE-DEFER candidate | Re-test with GoalCriterion/Temporal Constraint/Range needs |
| Quantity vs final numeric/decimal persistence | SAFE-DEFER candidate | Logical/physical persistence pressure gate |

These labels are transition-stage candidates, not a substitute for the mandatory closure pass.

---

# 23. Reopening triggers

Reopen Quantity v0 if later evidence shows that:

- scalar amount identity/lifecycle must exist independently from every containing record;
- unit/property separation makes ordinary workflows unnatural or lossy;
- Money, ratings or temporal values prove that the canonical Quantity definition is too broad rather than simply adjacent;
- custom-unit requirements force material identity/version/authority semantics into the basic Quantity itself;
- Register cannot aggregate/query quantities without contradicting Quantity's bounded value semantics;
- physical implementation cannot preserve precision/conversion/source representation without changing the semantic model.

---

# 24. Decision note

Quantity v0 is accepted as **canonical value semantics** for reusable scalar amounts.

The accepted model deliberately avoids:

- independent Quantity identity;
- universal numeric wrapping;
- property encoded into unit labels;
- semantic equivalence inferred from physical dimensions alone;
- universal aggregation rules;
- currency/calendar semantics silently absorbed into ordinary unit conversion;
- premature SQL/API commitment.

The next Data / Subjects concept should re-test this boundary through Register rather than treating the historical idea of a universal Register/Entry model as already accepted.