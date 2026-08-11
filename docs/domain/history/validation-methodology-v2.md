# Domain Validation Methodology v2

**Status:** Current validation standard  
**Established:** 2026-08-11  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This document defines the current validation methodology for LifeOS domain modeling.

The first Domain Atlas pass established a strong concept-review cycle based on internal documentation, scenario coverage, targeted external benchmarking, boundary analysis, adversarial cases, invariants, and cluster checkpoints.

Validation Methodology v2 keeps every one of those checks and adds a second layer designed to answer a harder question:

> **Can the accepted LifeOS model describe real life as it actually unfolds, including disorder, partial information, retroactive correction, conflicting sources, spontaneous behavior, changing plans, and cross-domain effects, without forcing reality to conform to LifeOS?**

The methodology is cumulative.

Nothing in v2 removes or weakens the original Domain Atlas protocol.

Instead:

```text
original concept review
        +
cluster validation
        +
real-world inversion
        +
deep chronological simulation
        +
adversarial reduction
        +
redundancy analysis
        +
multidirectional traceability
        +
independence testing
        +
cross-domain benchmark / anti-pattern analysis
        +
scale and product-complexity testing
        =
Validation Methodology v2
```

---

# 1. Governing principles

## 1.1 LifeOS semantics first

External standards, products, APIs, schemas, data models, and architectural patterns are evidence rather than design authorities.

LifeOS may adopt, adapt, or reject external ideas.

The decision order is:

```text
LifeOS product nature
        ↓
LifeOS semantic requirements
        ↓
strongest internal model
        ↓
external pattern comparison
        ↓
adopt only if it improves LifeOS
```

Interoperability is desirable where useful, but the kernel must not be distorted merely to obtain lossless compatibility with another system.

Provider-specific compromise belongs in adapters whenever that is cleaner than weakening the domain model.

## 1.2 Real life does not have to fit LifeOS

A validation scenario must not be rewritten to make the current model look correct.

If a realistic workflow is awkward to represent, that is evidence against the model.

The validation process must therefore preserve:

- ambiguity;
- incomplete information;
- contradictory sources;
- late corrections;
- unplanned behavior;
- failed intentions;
- changing goals;
- infeasible schedules;
- temporary disruption;
- different user planning styles.

## 1.3 Representation is not sufficient

A model that can technically store a workflow may still be poor.

For each real-world case LifeOS must be evaluated on:

1. **Coverage** — can the facts be represented?
2. **Naturalness** — are they represented using their real meaning rather than workarounds?
3. **Information preservation** — are intention, source, time, history, and meaning preserved?
4. **Improvement** — can LifeOS reduce friction, memory burden, duplication, decision load, error, or search cost?
5. **Complexity cost** — is the improvement worth the additional model and UX complexity?

## 1.4 Simple use must remain simple

Kernel sophistication must not force UI sophistication.

The user should be able to express:

```text
Gym three times a week
```

without understanding:

```text
Routine
Quota Recurrence
period frame
Occurrence
Temporal Constraint
Schedule
Capacity claim
```

The internal model may preserve those distinctions where needed, while the product uses progressive disclosure.

## 1.5 Power-user depth must remain possible

The same model must allow advanced configuration when useful:

- recurring semantics;
- hard/soft constraints;
- spacing/recovery;
- availability;
- capacity compatibility;
- exceptions;
- provenance;
- revisions;
- historical comparison;
- future automation.

Simple-user usability and power-user ceiling are both validation requirements.

---

# 2. Original Domain Atlas validation retained

Every concept still requires the original review sequence:

1. inspect relevant LifeOS documentation and prior decisions;
2. inspect feature-discovery scenarios;
3. benchmark mature systems/standards where useful;
4. propose the smallest strong semantic model;
5. challenge it with the user;
6. test adversarial and edge cases;
7. check consistency with accepted concepts;
8. document invariants, rejected alternatives, and deliberate deferrals;
9. save only after the concept is coherent enough to become the current baseline.

Cluster checkpoints remain mandatory.

The following questions remain part of every checkpoint:

- Can the scenario be represented naturally?
- Does each concept have coherent identity?
- Is duplicate representation required?
- Are planned/current/actual/history dimensions preserved?
- Are relationships natural rather than forced into one universal tree?
- Is provenance preserved?
- Can valid evidence later reach relevant Goals without rewriting historical intention?
- Does the model avoid arbitrary JSON as the primary structure for core semantics?
- Does another primitive have materially distinct identity, lifecycle, invariant, or behavior?
- Can the model be queried and explained efficiently?

---

# 3. Real-World Workflow Inversion Test

## 3.1 Purpose

Instead of asking:

> What could this person do with LifeOS?

start with:

> What does this person actually do without LifeOS?

The test reconstructs current behavior before mapping anything into the LifeOS model.

## 3.2 Procedure

For each selected scenario:

```text
real-world goal/problem
        ↓
existing tools / memory / paper / messages / specialist apps
        ↓
actual sequence of actions and decisions
        ↓
information created or lost
        ↓
friction / failure modes
        ↓
LifeOS semantic mapping
        ↓
coverage test
        ↓
improvement test
        ↓
complexity-cost test
```

## 3.3 Required questions

- What happens if the user never opens LifeOS?
- Which information currently lives only in memory?
- Which information is duplicated across systems?
- Which decision depends on searching old messages/files?
- Which state is derived manually?
- Which mistake is common because tools are disconnected?
- Can LifeOS represent the workflow without inventing fake entities?
- Can LifeOS remove meaningful friction?
- Does LifeOS preserve specialist software as the authoritative specialist tool where appropriate?
- Is an integration useful, optional, or unnecessary?

## 3.4 Failure signals

The model fails or needs revision when:

- the real workflow requires artificial LifeOS-only steps;
- users must create duplicate objects to preserve meaning;
- historical facts must be rewritten to match the model;
- a simple real-world case requires excessive mandatory modeling;
- LifeOS adds complexity without producing a meaningful benefit.

---

# 4. Deep Chronological Simulation

## 4.1 Purpose

Static scenario descriptions often hide lifecycle problems.

A model can look correct at one instant while failing after several revisions.

Deep chronological simulation therefore tests the model as a sequence of events over days, weeks, or months.

## 4.2 Standard progression

A deep simulation should include several of the following:

```text
Day 1   intention created
Day 2   Schedule accepted
Day 3   external change arrives
Day 4   execution differs from plan
Day 5   correction imported late
Week 2  recurring policy changes
Week 3  exception occurs
Month 2 user asks historical question
```

## 4.3 Mandatory disturbances

Where meaningful, inject:

- reschedule;
- postponement with no new date;
- cancellation;
- partial execution;
- skipped expected execution;
- spontaneous execution;
- imported data;
- provider disagreement;
- user correction;
- source-policy revision;
- temporary disruption;
- overlapping commitments;
- timezone/travel change;
- retroactive semantic relevance.

## 4.4 Historical queries

Every deep simulation should eventually ask questions such as:

- What did we expect at that time?
- What was the current Schedule then?
- Which rule generated this expectation?
- Which constraints applied?
- Why was this placement selected?
- What actually happened?
- What was learned later?
- Which value was corrected and why?
- Did later relevance rewrite original intention?

If these cannot be answered without reconstructing guesswork, the model is not history-safe.

---

# 5. Adversarial Reductio Test

For each concept perform deliberate destructive alternatives.

## 5.1 REMOVE

Ask:

> What becomes impossible or unnatural if the concept is removed?

A primitive that cannot justify its existence under this test may be redundant.

## 5.2 MERGE

Ask:

> Can this concept be merged with its nearest neighbor without losing identity, lifecycle, history, behavior, authority, or query semantics?

If yes, separate primitives may be unnecessary.

## 5.3 SPLIT

Ask:

> Does splitting the concept produce materially different invariants, or only additional terminology?

Avoid fragmentation where specialization/product language is sufficient.

## 5.4 MAKE UNIVERSAL

Apply the concept to every possible adjacent object.

Examples:

```text
every Activity gets an Occurrence
```

or:

```text
every Schedule becomes blocking Capacity
```

If the universal version introduces meaningless wrappers or false assumptions, preserve optional composition.

## 5.5 INVERT

Reverse a central rule.

Examples:

```text
time passing means completion
```

```text
Actual rewrites Schedule
```

```text
all overlap is conflict
```

The resulting contradictions help justify invariants.

## 5.6 EXTREME

Stress the concept at scale and over long history:

- ten years;
- hundreds of thousands of records;
- recurring open-ended series;
- large import batches;
- many revisions;
- offline edits;
- multiple providers.

Semantic correctness must not depend on tiny data volumes.

---

# 6. Semantic Redundancy / Merge-Split Test

For every suspicious concept pair A/B, answer:

1. Do they have different identity?
2. Can A change without B changing?
3. Can B change without A changing?
4. Do they have different lifecycle?
5. Do they have different authority or provenance semantics?
6. Do they answer different user/domain questions?
7. Are their historical queries different?
8. Can A exist without B?
9. Can B exist without A?
10. Are there realistic cases requiring one and not the other?
11. Would merging them create overloaded status/state?
12. Would splitting them further produce real behavior or only labels?

Classification:

- **DISTINCT** — both primitives justified;
- **SOFT BOUNDARY** — distinct semantics but requires ongoing stress testing;
- **SPECIALIZATION/UI LANGUAGE** — one kernel concept with contextual presentation;
- **REDUNDANT CANDIDATE** — likely merge/remove;
- **DEFERRED** — cannot decide until an adjacent cluster exists.

---

# 7. Multidirectional Semantic Traceability

LifeOS is not a universal parent/child tree.

Validation therefore runs in three directions.

## 7.1 Downward composition

Start from intention/strategy and trace toward reality.

Example:

```text
Goal
  ↓
Plan
  ↓
Routine
  ↓
Recurrence
  ↓
Occurrence
  ↓
Constraint / Availability / Capacity
  ↓
Schedule
  ↓
Session
  ↓
Actual / Evidence
```

No link in this example is universally mandatory.

The test asks whether the composition works naturally when those concepts are present.

## 7.2 Upward reconstruction

Start from reality or imported facts and trace possible context upward.

Example:

```text
spontaneous Session
  ↑
possible execution context
  ↑
possible Activity / Occurrence
  ↑
possible Routine / Plan
  ↑
possible Goal relevance
```

The central invariant is:

> **later-discovered meaning must not fabricate historical intention.**

## 7.3 Lateral propagation

One fact may affect multiple domains simultaneously.

Example:

```text
Dinner with friends
 ├─ supports social Goal
 ├─ may conflict with nutrition Goal
 ├─ consumes time/capacity
 ├─ may replace planned workout
 ├─ may generate spending data
 └─ may produce photos/notes
```

The test verifies that one real-world fact does not require duplicated source objects merely to participate in multiple contexts.

---

# 8. Orphan / Independence Test

For each concept ask:

> Can this concept exist without adjacent concepts and still retain semantic meaning?

Then distinguish:

- independent identity;
- contextual identity;
- capability/value semantics;
- derived projection.

Examples from the current baseline:

```text
Goal       may exist without Plan
Plan       may exist without explicit Goal
Activity   may exist without Goal/Schedule
Event      may exist without Goal/Plan
Routine    may exist without Goal
Session    may exist spontaneously
```

while concepts such as:

```text
Occurrence
Schedule
Recurrence
Temporal Constraint
Milestone
Availability
```

require some governing/source/context semantics even if the exact physical reference is deferred.

A dependency is acceptable only when semantic, not merely because the first database design made it convenient.

---

# 9. External Cross-Domain Benchmark

## 9.1 Purpose

Benchmarking must not be limited to products marketed as personal productivity systems.

LifeOS should inspect systems that solve individual hard problems well.

Useful classes include:

- calendar/scheduling systems;
- project/work management;
- health-data platforms;
- accounting/ledger systems;
- home automation;
- CRMs;
- flexible database/note tools;
- version-control systems;
- operating-system scheduling/resource systems;
- distributed/offline systems;
- search/index/materialized-view systems;
- specialist domain software where a LifeOS integration boundary matters.

## 9.2 Dimensions to benchmark

For each external system or pattern evaluate:

- domain separation;
- identity;
- lifecycle;
- history/correction;
- provenance;
- derived versus persisted state;
- extensibility;
- queryability;
- performance;
- scale;
- offline/sync;
- automation boundaries;
- progressive disclosure;
- simple-user experience;
- power-user ceiling;
- provider lock-in risk.

## 9.3 Classification

Every benchmark finding should be classified as one of:

- **BORROW** — strong pattern fits LifeOS directly;
- **ADAPT** — useful idea but LifeOS needs different semantics;
- **ALREADY STRONGER** — LifeOS intentionally preserves richer semantics;
- **ANTI-PATTERN** — avoid the external system's tradeoff;
- **NOT APPLICABLE** — valid elsewhere but inappropriate for LifeOS.

---

# 10. External Anti-Pattern Review

Popularity does not make a pattern correct for LifeOS.

Explicitly test external designs for risks such as:

- one universal generic object;
- arbitrary custom-field sprawl;
- opaque JSON as the primary model;
- status explosion;
- provider identity becoming internal identity;
- start/end fields duplicated across domain entities;
- calendar presence treated as truth/busy state;
- recurrence implemented by mutating one item forward forever;
- automatic overwrite of history;
- automation spaghetti where trigger/condition/effect are indistinguishable;
- destructive derived-state persistence;
- forced hierarchy;
- inability to represent contradictory reality;
- excessive configuration for simple users.

A benchmark should record both what to learn and what to avoid.

---

# 11. Scale / performance / history stress

Conceptual validation must anticipate implementation pressure without prematurely choosing SQL.

For each cluster ask:

- Does correctness require eager persistence of infinite/large future state?
- Can derived projections be recomputed or cached?
- Are high-value queries structurally expressible?
- Does history grow append-only in places where overwrite would be dangerous?
- Can current-state queries remain fast through projections/indexes later?
- Would one concept require scanning an entire ten-year history for every common action?
- Does offline reconciliation require stable identity?
- Can provider mappings remain separate from LifeOS identity?

Performance optimization may denormalize future physical storage, but denormalization must not redefine semantic truth.

---

# 12. Simple-user versus power-user test

For each major feature evaluate two experiences.

## Simple user

Can the user perform the common action with minimal decisions?

Examples:

```text
Buy milk tomorrow
Gym three times a week
Dentist Friday at 15:00
```

The user should not need to understand internal primitives.

## Power user

Can the same system expose additional precision when intentionally requested?

Examples:

```text
3x/week with 48h recovery
prefer evenings
never after 21:00
protect travel buffer
show historical recurrence revisions
```

A design fails when either:

- simple users must configure the kernel;
- power users hit an artificial ceiling that requires another disconnected system.

---

# 13. Cluster result taxonomy

A validation round must classify findings explicitly.

## PASS

No material structural issue remains before the next workstream step.

## PASS WITH HARDENING

The concept/cluster architecture remains valid, but definitions/invariants need strengthening before canonical checkpoint save.

## REOPEN

An accepted concept's identity, boundary, lifecycle, or invariant is materially incorrect or incomplete.

## NEW PRIMITIVE CANDIDATE

A recurring gap has materially distinct identity/lifecycle/behavior and cannot be represented cleanly by accepted concepts.

## DEPENDENCY, NOT FAILURE

The scenario correctly reaches the boundary of a future cluster (for example Resource, Actual, Evidence, Trigger, Relationship, Provenance) without invalidating the current cluster.

## UX / PRODUCT ISSUE

The kernel is correct but exposing it directly would create unnecessary user complexity.

---

# 14. Current v2 validation set

The first full application of this methodology validates the following accepted concepts together:

## Intention & Execution

- Goal v0;
- Plan v0;
- Activity v0;
- Event v0;
- Routine v0;
- Milestone v0.

## Time

- Occurrence v0;
- Schedule v0;
- Session v0;
- Temporal Constraint v0;
- Recurrence v0;
- Availability & Capacity v0.

The detailed result is recorded separately in the cross-cluster validation record and Time checkpoint.

---

# 15. Mandatory reuse for future clusters

Validation Methodology v2 is not a one-time test.

Every future cluster should inherit these methods where applicable.

A new cluster may add domain-specific tests, but should not silently drop:

- existing scenario/boundary validation;
- real-world workflow inversion;
- deep chronological simulation;
- adversarial reductio;
- redundancy/merge-split analysis;
- downward/upward/lateral traceability;
- orphan/independence checks;
- cross-domain benchmarking;
- anti-pattern review;
- scale/history stress;
- simple-user/power-user validation;
- final cross-cluster consistency testing.

The goal is not to produce the largest ontology.

It is to produce the smallest model that remains semantically accurate, history-safe, understandable, extensible, queryable, scalable, and useful when confronted with real life rather than idealized workflows.
