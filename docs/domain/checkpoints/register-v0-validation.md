# Register Candidate v0 — Validation Checkpoint

**Status:** CANDIDATE REJECTED AS KERNEL PRIMITIVE — product need retained  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Candidate: Register / universal RegisterEntry
- Historical source: feature-discovery simulation and earlier V1 product vocabulary
- Adjacent concepts/capabilities: Observation, Quantity, Session, future domain-specific records, Goal/Evidence, Query/Aggregation, Visibility, Subject, Asset
- Why this review exists: earlier product discovery proposed a universal longitudinal `Register + RegisterEntry` structure. The current Domain Atlas must determine whether that proposal represents a distinct kernel concept or only product/query capability over native domain records.

This checkpoint intentionally preserves the rejection rationale. Historical product documentation remains evidence, but is not authoritative over the current kernel.

---

# 2. Historical candidate

The earlier proposal treated Register as a broadly reusable structure for data over time:

```text
Register
- name
- type
- subject
- unit
- aggregation
- privacy
- linked goals

RegisterEntry
- timestamp
- value(s)
- unit
- direction
- asset/location/source/note/attachments/confirmation
```

Representative uses included weight, money, mileage, mood, stock, scores, symptoms, pages, time and consumption.

The current review does **not** assume this structure is correct merely because it appeared in discovery.

---

# 3. Real need extracted from the historical proposal

The underlying product needs remain valid:

- view coherent records longitudinally;
- capture recurring data with low friction;
- show latest values and historical timelines;
- compute valid aggregates and trends;
- filter by subject/property/source/time/context;
- compare periods;
- drill back to source records;
- optionally save useful tracker/view configuration;
- connect information to Goal evaluation without duplicating source facts;
- support privacy and actor-scoped presentation.

The question is whether those needs require a new kernel object called `Register`.

---

# 4. Candidate minimality and reductio

## REMOVE Register from the kernel

Example:

```text
Observation O1 — body weight = 66.8 kg
Observation O2 — body weight = 66.5 kg
Observation O3 — body weight = 66.4 kg
```

Without a Register entity, the three Observations retain:

- identity;
- subject/focus;
- effective time;
- value semantics;
- Provenance;
- Confirmation where applicable;
- Evidence relevance where applicable;
- correction/history.

A longitudinal weight view can still query and aggregate those Observations.

**Result:** no domain truth is lost. Kernel `Register` is not required.

## REMOVE Register product capability

The product would lose useful tracker/history/trend/quick-capture experiences.

**Result:** the product capability is valuable even though the kernel primitive is not.

## UNIVERSAL RegisterEntry

Copying or wrapping every native record into a generic RegisterEntry creates duplicate identity and competes with native semantics such as Observation, Session, future transaction/movement records or specialist records.

**Result:** rejected.

## Register as source of truth

If Register owns its entries, the same source fact appearing in several views requires duplication or artificial ownership.

**Result:** rejected.

---

# 5. External benchmark evidence

The benchmark was deliberately cross-domain and used mature products/systems as evidence rather than authorities.

| System/pattern | Relevant observation | Classification |
|---|---|---|
| Apple HealthKit | Statistics and longitudinal health views are computed over native samples; valid statistics depend on the semantic quantity type | ADAPT |
| Android Health Connect | Aggregations operate over native record types/metrics and time ranges, including source-aware handling for cumulative data | ADAPT |
| Strava | Training Log/progress surfaces organize and aggregate native Activity records and permit drill-down to source activities | ADAPT |
| YNAB | Reports/search/reconciliation operate over native financial Transactions rather than a generic copied tracker-entry layer | ADAPT |

Shared pattern:

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
tracker / log / report / progress UI
```

Not:

```text
native record
        ↓ duplicate/wrap
universal RegisterEntry
        ↓
Register source of truth
```

LifeOS is not required to copy any of these systems. The value of the benchmark is that several mature domains independently reinforce the same separation between source records and longitudinal presentation/analysis.

---

# 6. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | weight, mood, fitness, finance, mileage, inventory | PASS | longitudinal UX is useful; native records remain the source of truth |
| CORE-02 Deep chronology | Yes | years of measurements, corrections, source changes, saved views | PASS | changing/deleting a tracker view must not rewrite source history |
| CORE-03 Reductio | Yes | remove Register, remove product capability, universalize RegisterEntry | PASS | kernel candidate is unnecessary; product capability remains useful |
| CORE-04 Redundancy | Yes | Register vs Observation/native records/query/view | PASS | no independent domain truth/lifecycle justifies kernel primitive |
| CORE-05 Traceability | Yes | source record -> trend -> Goal evidence -> drill-down | PASS | preserve source identity; aggregation/projection remains traceable |
| CORE-06 Orphan/independence | Yes | Observation without saved Register; dynamic query without saved view | PASS | native records and longitudinal views can exist independently |
| CORE-07 External benchmark | Yes | HealthKit, Health Connect, Strava, YNAB | PASS | mature patterns reinforce native-record + query/aggregation separation |
| CORE-08 Anti-pattern review | Yes | universal Entry, one unit/aggregation field, copied data | PASS | rejected explicitly |
| CORE-09 Correction/reconciliation | Yes | corrected Observation/Transaction-like record | PASS | source record owns correction/provenance, not view/container |
| CORE-10 Scale/performance/history | Yes | ten-year history/high-frequency data | PASS | no duplicated entry layer required; materialization remains implementation concern |
| CORE-11 Simple vs power user | Yes | metric page vs configurable tracker | PASS | product can expose progressively richer views without kernel noun |
| CORE-12 Product value/complexity cost | Yes | quick capture/trends/reports | PASS | value is strong at product layer, weak as kernel primitive |
| CORE-13 Implementation pressure | Yes | querying, indexes, cached aggregates, saved filters | PASS | implementation may persist configuration/materializations without changing domain truth |

Core conclusion: **the need passes; the kernel primitive does not.**

---

# 7. Register versus Observation

Observation answers:

> What was measured, perceived, reported, asserted or derived about a subject/context?

A longitudinal product view answers:

> Which existing records should be shown/analyzed together over time, and how should they be presented?

Example:

```text
Observation O1
body weight = 66.4 kg
```

may appear in:

- a Weight history screen;
- a health dashboard;
- a Goal evaluation;
- an AI trend summary;
- another authorized view.

It remains one Observation.

Canonical result:

> **Observation != Register; no universal RegisterEntry is required between Observation and longitudinal UI.**

---

# 8. Register versus Quantity and aggregation

Quantity provides scalar amount/unit semantics. It does not define which longitudinal operation is meaningful.

Examples:

```text
20 °C + 25 °C
```

is not automatically a meaningful 45 °C aggregate.

Likewise identical units do not establish whether `sum`, `average`, `last`, `delta`, `min/max`, `balance`, or another operation is semantically valid.

Canonical result:

> **Aggregation validity belongs to the semantic source metric/record/evaluation context, not to a universal Register field and not to Quantity alone.**

Therefore the historical idea of one generic `Register.aggregation` or `Register.unit` kernel model is rejected.

---

# 9. Quick capture

A tracker-like UI may provide optimized capture defaults.

Example:

```text
Weight screen
+ 66.4 kg
```

creates the appropriate native record:

```text
Observation
property = body weight
value = Quantity(66.4 kg)
```

It does not create a generic RegisterEntry whose semantic meaning must later be decoded.

Future financial/inventory/specialist capture must likewise create the native semantic record justified by that domain; this checkpoint does not pre-approve generic `Transaction`, `Movement`, or `Snapshot` primitives.

---

# 10. Saved views/configuration

LifeOS may later persist a named tracker or saved longitudinal view such as:

```text
Morning Weight
- subject = me
- property = body weight
- optional source/time filters
- preferred visualization
- capture defaults
```

Such configuration may have an application identifier/lifecycle for product behavior, sync or customization.

That fact alone does not elevate it to a Domain Atlas primitive comparable to Activity, Observation or Asset.

Canonical rule:

> **Persisted product configuration does not automatically imply independent domain truth.**

Dynamic longitudinal views may also exist without any saved configuration.

---

# 11. Multi-Actor Compatibility Gate

The rejected-kernel direction improves multi-actor separation.

- one shared native fact may appear in different actor-scoped views without duplication;
- actor-specific filters, preferred units, chart settings or dashboard placement do not mutate canonical source records;
- a shared view does not automatically grant visibility to every source record;
- private source information may contribute to an authorized aggregate/projection without raw disclosure where policy allows;
- deleting an actor's saved tracker configuration does not delete shared/native history;
- AI may query authorized source records and explain allowed aggregates without creating new ownership over the data.

Result: **PASS** for product capability over native records; no multi-actor justification appears for a universal Register entity.

---

# 12. Cross-Concept Consistency Gate

| Test ID | Result | Notes |
|---|---|---|
| XCON-01 Identity compatibility | PASS | native record identity remains authoritative |
| XCON-02 Ownership/authority compatibility | PASS | view ownership/configuration does not imply authority over source facts |
| XCON-03 Planned/current/actual/history compatibility | PASS | views do not rewrite underlying history |
| XCON-04 Relationship compatibility | PASS | one source record can surface in many contexts without duplicate facts |
| XCON-05 Multi-actor readiness compatibility | PASS | actor-scoped presentation remains separate from shared/native truth |
| XCON-06 Language-map compatibility | PASS WITH UPDATE | Register should move from deferred kernel candidate to product/UI capability term |

---

# 13. Reopening / dependency register

| Finding | Severity | Closure class | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|
| Universal RegisterEntry | STRUCTURAL | RESOLVED | rejected; native records retain identity | Domain Atlas | reopen only if an ordinary workflow cannot be represented without a generic entry identity |
| Register as kernel source-of-truth container | STRUCTURAL | RESOLVED | rejected | Domain Atlas | reopen only if later evidence reveals independent domain truth/lifecycle not reducible to native records + configuration |
| Longitudinal query/aggregation | PRODUCT-UX / implementation | SAFE DEFERRED | required capability, exact query/materialization model not fixed | Logical/physical model + product design | persistence/query design phase |
| Saved tracker/view configuration | PRODUCT-UX | SAFE DEFERRED | optional product behavior | Product + logical model | when saved views/custom trackers are implemented |
| Subject-scoped longitudinal filtering | DEFERRED DEPENDENCY | SAFE DEFERRED | requires Subject review | Subject | immediately during Subject validation |
| Visibility/privacy of aggregate vs source | DEFERRED DEPENDENCY | SAFE DEFERRED | current privacy invariants retained | Authority/Visibility | Visibility/Authority review and Cross-Cluster v4 |
| Goal/Evidence relation to longitudinal aggregates | DEFERRED DEPENDENCY | SAFE DEFERRED | use source Evidence/derived projection rules for now | GoalCriterion/Relationships | GoalCriterion/Evidence relationship review |
| Financial/inventory native record types | DEFERRED DEPENDENCY | SAFE DEFERRED | no generic primitive pre-approved | future workflow evidence | only if a concrete workflow proves distinct identity/lifecycle semantics |
| Materialized aggregate/history | implementation | SAFE DEFERRED | derived unless independently asserted/imported/history-stable | logical/physical model | persistence/API pressure test |

No item remains as unnamed `review later` debt.

---

# 14. Final verdict

```text
Historical candidate: Register as kernel primitive
VERDICT: REJECTED

Historical candidate: universal RegisterEntry
VERDICT: REJECTED

Longitudinal querying/tracking/analysis product need
VERDICT: VALIDATED

Optional saved tracker/view configuration
VERDICT: PRODUCT / APPLICATION CONCERN, exact shape deferred
```

This is not a failure of the Domain Atlas. Candidate rejection is a successful validation result when the required capability survives more cleanly without an additional primitive.

---

# 15. Regression obligations

Future cluster/whole-domain tests must preserve:

1. source records remain canonical when shown in multiple longitudinal views;
2. deleting/changing a view does not delete/change source history;
3. no universal RegisterEntry layer is introduced for convenience;
4. aggregate/trend values remain derived unless a separate asserted/imported fact justifies persistence;
5. aggregation validity follows source metric/record semantics rather than same-unit coincidence;
6. drill-down/traceability to source information remains possible where authorization allows;
7. actor-scoped presentation does not duplicate shared facts;
8. product terminology such as Register/Tracker/Progress/History does not create a kernel type by naming alone.

---

# 16. Next review

Proceed to `Subject` in the Data / Subjects cluster.

Subject must be tested independently rather than assumed necessary merely because Observation currently uses the word `subject`. The review must determine whether Subject is a true identity/semantic role, a relationship role over heterogeneous entities, or an unnecessary universal wrapper.