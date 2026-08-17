# Availability & Capacity v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **Scheduling Capacity represents the time-dependent ability of a schedulable resource to accept commitments. Availability defines when that capacity may be used; reservations or claims consume, protect, or otherwise occupy capacity for accepted commitments; effective free capacity is derived from availability, reservations, compatibility rules, and applicable overrides.**

This concept family answers several related but distinct questions:

```text
Availability
When may this resource be used?

Capacity
How much / what kind of schedulable load can it sustain?

Reservation / Claim
What capacity is currently committed or protected?

Effective Free Capacity
What compatible capacity remains after rules and commitments are applied?
```

The accepted model does **not** make `Calendar Block` a separate kernel primitive by default.

`Calendar Block` remains useful product and UI language for a time-shaped construct whose primary purpose is to protect capacity, mark unavailability, hold time, or expose another capacity-only state on the calendar.

Examples include:

- focus time;
- protected recovery;
- unavailable time;
- a travel buffer;
- a tentative hold;
- a placeholder that reserves capacity without yet representing a concrete Activity or Event.

Where an Activity, Event, Occurrence, or another richer domain subject already exists, LifeOS should normally render that subject directly rather than creating a duplicate Calendar Block object merely because it occupies time.

---

## Why this concept exists

The accepted Time-cluster concepts intentionally separate temporal identity, temporal constraints, accepted placement, and actual execution:

```text
Recurrence
how a repeated pattern behaves

Occurrence
which generated expected instance exists

Temporal Constraint
where / when placement is allowed, required, bounded, or preferred

Schedule
when the subject is currently accepted to happen

Session
when actual execution happened
```

One material question remains after those distinctions:

> **Does a scheduled item consume the user's or another resource's schedulable capacity, and if so, how?**

A naive calendar model often assumes:

```text
has time on calendar
=
busy
=
capacity unavailable
```

LifeOS cannot safely make that assumption.

Examples:

```text
Birthday
all day
```

may need to be visible for the whole date without making the user unavailable for twenty-four hours.

```text
Optional webinar
15:00 -> 16:00
```

may be scheduled while still allowing compatible work.

```text
Protected focus
15:00 -> 17:00
```

may need to block competing commitments even before a concrete Activity is assigned to the protected time.

```text
Unavailable
14:00 -> 18:00
```

may mean the user simply has no schedulable capacity during that interval, not that a hidden Activity exists.

Therefore Schedule placement and capacity impact must remain separate semantics.

---

## Validation basis

Availability & Capacity v0 was reviewed against:

### Existing LifeOS documentation

- `docs/product/v1-core-domain-glossary.md`, especially the earlier `Calendar block` definition;
- `docs/product/v1-scheduling-flexibility.md`;
- `docs/product/v1-execution-status.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- the accepted Time-cluster concepts Occurrence, Schedule, Session, Temporal Constraint, and Recurrence;
- the accepted Routine and Event boundaries;
- the LifeOS temporary-mode and replanning requirements.

### Representative LifeOS scenarios

The review included:

- meetings that block attention;
- optional or passive Events that need not block attention;
- all-day informational Events;
- focus and protected-work blocks without a concrete Activity;
- hard unavailability;
- travel and preparation buffers;
- recovery periods;
- tentative holds;
- recurring working hours;
- exceptional available and unavailable periods;
- illness, travel, holiday, and disrupted-week overrides;
- overlapping compatible behavior such as walking while listening to English;
- incompatible overlaps such as driving while doing deep coding;
- imported free/busy data;
- double-booked external Events that must remain representable even when infeasible;
- future physical/resource capacity such as rooms, devices, vehicles, or equipment pools.

### External benchmark evidence

Mature calendar systems commonly separate an item's temporal placement from whether it contributes to busy/free calculations, and some expose more than a binary free/busy state.

This evidence confirms that `scheduled != busy` is a real domain problem.

However, consistent with the Domain Atlas benchmark rule:

> **External free/busy taxonomies and provider schemas are evidence only. They are not LifeOS compatibility requirements or design authorities.**

LifeOS keeps the stronger internal semantics and maps to provider models through adapters when integration is useful.

---

# 1. Core semantic model

The accepted conceptual structure is:

```text
Schedulable resource
        |
        v
     Capacity
ability to accept compatible commitments
        |
   +----+------------------+
   |                       |
   v                       v
Availability          Reservations / Claims
when capacity         what capacity is
may be used           committed/protected
   |                       |
   +-----------+-----------+
               v
      Effective Free Capacity
             derived
               |
               v
            Scheduler
               |
               v
             Schedule
```

This is a semantic relationship, not a final persistence layout.

For a proposed Schedule placement, feasibility conceptually depends on at least:

```text
Temporal Constraints satisfied?
        |
        v
Availability / Capacity present?
        |
        v
Existing capacity claims compatible?
        |
        v
placement feasible
```

The actual planner may evaluate these concerns together rather than through a literal sequential pipeline.

---

# 2. Availability

## 2.1 Definition

> **Availability is a time-dependent rule or fact describing when a schedulable resource has capacity that may be used for compatible commitments.**

Availability is about the resource, not a particular Activity/Event.

```text
Availability
User may be scheduled Mon-Fri 09:00-18:00
```

is different from:

```text
Temporal Constraint
This workout may occur only before 20:00
```

The first constrains the resource's usable capacity.

The second constrains one subject or class of subjects.

---

## 2.2 Availability is not the list of empty gaps

LifeOS should not model effective availability primarily as a giant persisted list such as:

```text
10:00-10:45 free
11:30-12:10 free
13:00-14:20 free
...
```

when those intervals are merely the result of applying rules and commitments.

A stronger source model is:

```text
Baseline Availability
Mon-Fri 09:00-18:00

Availability Override
Tuesday 09:00-13:00 unavailable

Reservation
Tuesday 15:00-16:00
```

from which LifeOS derives:

```text
Effective Free Capacity
Tuesday 13:00-15:00
Tuesday 16:00-18:00
```

Derived free intervals may later be cached or materialized for performance, but the cache is not the authoritative domain truth.

---

## 2.3 Baseline availability

Availability may express a reusable baseline such as:

```text
General personal availability
08:00 -> 23:00
```

or:

```text
Work scheduling context
Mon-Fri
09:00 -> 18:00
```

A baseline means:

> capacity may be used during these times, subject to other rules and commitments.

It does not mean:

> LifeOS should fill every available minute with work.

Preferences, Goals, priorities, recovery, workload strategy, and other planning policies remain separate.

---

## 2.4 Availability may recur

A recurring availability pattern such as:

```text
Mon-Fri 09:00-18:00
```

may reuse Recurrence semantics to describe when the availability rule applies.

This does **not** require execution Occurrences to be generated for every workday merely because the Availability rule repeats.

Conceptually:

```text
Availability Rule
        |
        v
Recurrence pattern
repeated applicability
```

not necessarily:

```text
Availability Rule
        |
        v
Occurrence
Occurrence
Occurrence
```

This follows Recurrence v0: recurrence-pattern machinery may govern repeated applicability without turning every repeated rule into an occurrence-generating source.

---

## 2.5 Availability overrides

Availability must support exceptions in both directions.

### Negative override

```text
Baseline
Saturday 10:00-15:00 available

Override
this Saturday unavailable
```

### Positive override

```text
Baseline
Saturday unavailable

Override
this Saturday 10:00-15:00 available
```

The domain must not assume that an exception only subtracts capacity.

---

## 2.6 Temporary modes and availability

Temporary Mode may alter effective availability or capacity without rewriting the user's stable baseline.

Example:

```text
Baseline
Mon-Fri 09:00-18:00

Temporary Mode
Illness

Temporary availability
Mon-Fri 11:00-14:00
```

When the temporary mode ends, the normal baseline can resume without pretending that the long-term rule had permanently changed.

This same mechanism can support:

- travel;
- exams;
- intense work;
- reduced capacity;
- holiday;
- caregiving disruption;
- recovery periods;
- other temporary circumstances.

The exact Temporary Mode domain representation remains outside this Time-cluster concept.

---

# 3. Capacity

## 3.1 Definition

> **Capacity is the time-dependent ability of a schedulable resource to accept compatible commitments.**

For personal V1, the primary schedulable resource will normally be the user.

The definition intentionally does not restrict Capacity to a person because Resource semantics may include:

- rooms;
- vehicles;
- equipment;
- devices;
- production capacity;
- shared or count-based resources.

Resource v0 now defines `Resource` as contextual planning/execution role/capability over native referents/supplies rather than a universal entity/root. See the canonical alignment amendment at the end of this document.

---

## 3.2 Capacity is not universally binary

A simple calendar often treats capacity as:

```text
FREE
or
BUSY
```

LifeOS may expose this as a useful view, but it must not become the universal ontology.

Examples expose several possible capacity behaviors:

### Exclusive capacity

```text
Deep coding
```

may consume the user's primary active attention such that another incompatible primary-attention Activity cannot overlap.

### Compatible capacity

```text
Walk
+
English listening
```

may legitimately overlap.

### Count capacity

A future resource might support:

```text
3 equivalent rooms
```

where one reservation consumes one of three slots.

### Quantitative capacity

A future physical resource could expose an amount or rate.

The Time cluster therefore fixes only this invariant:

> **Capacity is not universally binary.**

The exact quantitative/resource representation is deliberately deferred.

---

## 3.3 Capacity is not universally one percentage

LifeOS must also avoid false precision such as:

```text
user capacity = 73%
```

as a universal scheduling truth.

Human schedulability may involve different dimensions:

- primary attention;
- passive attention;
- physical effort;
- social engagement;
- mobility;
- location;
- equipment access;
- another context-specific requirement.

The fact that two Activities both consume time does not imply their compatibility can be represented by one scalar number.

LifeOS may later introduce domain-specific capacity dimensions where useful, but the kernel must not force them prematurely.

---

## 3.4 Personal V1 may use pragmatic defaults

The generic ontology should remain flexible, but the product does not need to expose a complexity matrix to every user.

A pragmatic personal-V1 default may assume that ordinary active Activities and Events consume one primary exclusive attention capacity unless their semantics/policy indicate otherwise.

Examples of alternate behavior could include:

```text
non-blocking
```

```text
passive / compatible
```

or another reviewed capability.

This is a product default, not a universal LifeOS invariant.

---

# 4. Capacity Reservation / Claim

## 4.1 Definition

> **A Capacity Reservation or Claim represents capacity that is committed, occupied, protected, or held for a purpose during an accepted temporal placement.**

Examples:

```text
Meeting
15:00-16:00
exclusive attention claim
```

```text
Protected focus
15:00-17:00
protected capacity reservation
```

```text
Tentative appointment
15:00-16:00
tentative capacity hold
```

A claim may be produced by a richer scheduled subject or may itself be the main semantics of a standalone capacity-only construct.

---

## 4.2 Schedule is not the reservation

One of the strongest Time-cluster invariants is:

> **Schedule presence does not imply capacity consumption.**

Schedule answers:

> when is this currently accepted to happen?

Capacity impact answers:

> what schedulable capacity does this placement consume or protect?

These facts may often move together operationally, but they remain semantically distinct.

---

## 4.3 Example: blocking Event

```text
Event
Client meeting

Schedule
15:00-16:00

Capacity impact
blocks primary attention
```

---

## 4.4 Example: non-blocking Event

```text
Event
Optional webinar

Schedule
15:00-16:00

Capacity impact
non-blocking / compatible
```

The Event remains scheduled and visible.

The scheduler may still place compatible work during the same interval.

---

## 4.5 Example: all-day information

```text
Event
Birthday

Schedule
all day
```

This does not automatically imply:

```text
capacity unavailable for 24 hours
```

All-day placement and full-day capacity consumption remain independent semantics.

---

# 5. Event participation does not determine capacity automatically

Event identity, participation state, attendance, and capacity impact remain separate.

Example:

```text
Event
Meeting 15:00-16:00

Participant response
declined
```

LifeOS may keep the Event visible for context/history while treating the user's capacity as free.

Conversely:

```text
Event
Company livestream

Participant response
accepted
```

could still be configured as non-blocking or compatible if the user intends to listen passively.

Therefore:

> **accepted/declined attendance state is not itself a universal capacity rule.**

---

# 6. Calendar Block

## 6.1 Product meaning remains useful

The previous LifeOS glossary used `Calendar Block` for something that reserves or protects time without necessarily representing a concrete outcome.

That user-facing meaning remains valuable.

Examples:

- focus time;
- unavailable time;
- travel buffer;
- recovery;
- preparation;
- placeholder;
- tentative hold.

The domain review changes the kernel classification, not the usefulness of the product concept.

---

## 6.2 Calendar Block is not a kernel primitive by default

The accepted direction is:

> **Calendar Block is product/UI language for a time-shaped capacity construct, usually a standalone Capacity Reservation or Availability override when no richer domain subject already provides the semantics.**

Therefore LifeOS should avoid:

```text
Event
Meeting

+

CalendarBlock
clone of Meeting's time
```

or:

```text
Activity
Write report

+

CalendarBlock
clone of Activity's scheduled placement
```

The calendar should normally render the existing domain subject directly.

---

## 6.3 Standalone protected focus

```text
Capacity-only construct
Protected focus

Schedule
15:00-17:00

Capacity behavior
protected / blocking
```

The UI may show this as a Calendar Block.

No fake Activity needs to be invented if there is no concrete work identity yet.

---

## 6.4 Unavailability block

A visually identical calendar rectangle may have different semantics:

```text
Availability Override
14:00-18:00
unavailable
```

rather than:

```text
Capacity Reservation
14:00-18:00
protected for a purpose
```

The UI may present both as calendar blocks, but the kernel should preserve the distinction.

---

# 7. Availability versus Temporal Constraint

Availability acts primarily on a schedulable resource.

Temporal Constraint acts primarily on a subject or class of subjects.

Example:

```text
Temporal Constraint
No workouts after 20:00
```

means:

> this class of work cannot validly be placed after 20:00.

It does not mean:

> the user has zero capacity after 20:00 for everything.

The user might still schedule:

- a movie;
- coding;
- a social Event;
- another compatible Activity.

By contrast:

```text
Availability
unavailable after 20:00
```

means that the governed schedulable capacity itself is unavailable.

---

# 8. Availability versus preference

```text
Prefer studying in the morning
```

is not an Availability rule.

It is more naturally a soft Temporal Constraint / scheduling preference.

Availability answers:

> can capacity be used here?

Preference answers:

> would this placement be better here?

Capacity Reservation answers:

> is capacity already committed/protected here?

Schedule answers:

> when did we accept this subject to happen?

These questions must remain distinguishable.

---

# 9. Hard unavailability and real-world inconsistencies

LifeOS must be able to represent states that are currently infeasible or contradictory.

Example:

```text
Availability
unavailable 15:00-17:00

Imported Event
Schedule 15:30-16:30
```

The imported Event remains a real fact.

LifeOS should not silently delete it or rewrite availability merely to keep the plan mathematically clean.

The system may derive:

```text
capacity conflict
```

and surface a resolution workflow.

This follows the same rule used for hard Temporal Constraints:

> **planning invalidity does not make real data unrepresentable.**

---

# 10. Compatibility, overlap, and conflict

## 10.1 Timestamp overlap is not enough

The naive rule:

```text
interval A overlaps interval B
=> conflict
```

is too strong for LifeOS.

Example:

```text
Walk
17:00-18:00

English listening
17:00-18:00
```

may be compatible.

Example:

```text
Driving
17:00-18:00

Deep coding
17:30-18:30
```

is normally incompatible.

Therefore:

> **capacity compatibility, not timestamp overlap alone, determines the semantic scheduling conflict.**

---

## 10.2 Overlap must remain representable

Even obviously incompatible commitments may exist in imported or user-entered data.

```text
Meeting A
15:00-16:00

Meeting B
15:30-16:30
```

LifeOS must be able to store both and derive:

```text
capacity overcommitment / conflict
```

A universal database rule such as:

```text
no overlapping schedules allowed
```

would be incorrect for the general model.

---

## 10.3 Overlap in Actual history

Session v0 already allows overlapping actual Sessions where real behavior was compatible or where the imported history says both occurred.

Capacity v0 explains why planned overlaps also cannot be globally prohibited.

Analytics must therefore distinguish concepts such as:

```text
category-specific time
```

from:

```text
unique wall-clock coverage
```

rather than blindly summing every overlapping duration.

---

# 11. Effective Free Capacity

## 11.1 Derived view

Effective Free Capacity is derived from the current effective state.

Conceptually:

```text
baseline capacity
+ positive availability overrides
- unavailable intervals
- incompatible committed reservations
+/- context-specific capacity modifiers
=
effective remaining compatible capacity
```

The actual computation may be more sophisticated than arithmetic because compatibility need not be scalar.

---

## 11.2 Effective free capacity is contextual

The question:

> Am I free at 18:00?

may be incomplete.

A stronger query is:

> Do I have enough compatible capacity at 18:00 for **this candidate commitment**?

Example:

```text
18:00-19:00
Walking already scheduled
```

The user may still have capacity for English listening but not for another physically incompatible Activity.

Therefore a simple free/busy projection may be useful for UI, but it is a lossy view over richer semantics.

---

# 12. Temporary reduction of capacity

Not every temporary limitation needs to be expressed solely as unavailable time.

A Temporary Mode may conceptually reduce the class or amount of commitments the user should accept.

Example:

```text
Temporary Mode
Illness
```

could lead to:

- shorter usable windows;
- fewer demanding Activities;
- reduced scheduling density;
- protection of critical items only;
- recovery Reservations;
- broader replanning.

The exact quantitative energy model is intentionally deferred.

LifeOS must avoid pretending that complex human state can always be captured as a precise capacity percentage.

---

# 13. Travel buffer example

A travel-related requirement illustrates the separation among concepts.

```text
Event
Flight
```

may imply a rule:

```text
Temporal Constraint
arrive at airport at least 2 hours before departure
```

The planner may use that rule to create/propose a concrete protected interval:

```text
Capacity Reservation
Airport / travel buffer

Schedule
06:00-08:00
```

The rule and the resulting reservation are different facts.

The UI may show the concrete reservation as a Calendar Block.

---

# 14. Recovery example

```text
Routine
Strength training

Temporal Constraint
minimum 48h between relevant sessions
```

This does not require a forty-eight-hour Calendar Block.

However the user may additionally create:

```text
Capacity Reservation
Protected recovery
Sunday morning
```

One is a relationship constraint.

The other is an explicit reservation of capacity.

---

# 15. Tentative holds

A useful capacity model should allow commitments that are not all equally firm.

Example:

```text
Possible appointment
Tuesday 15:00-16:00
```

The user may want to protect the interval provisionally while still distinguishing it from a confirmed commitment.

The current model therefore allows the semantic possibility of:

```text
firm reservation
```

versus:

```text
tentative hold
```

without prematurely freezing the final enum/state machine.

Firmness, authority, and lifecycle details remain for persistence/lifecycle design.

---

# 16. External free/busy data

External providers may supply free/busy information or status taxonomies.

LifeOS should represent imported information with provenance such as:

```text
Imported capacity evidence
source: provider X
interval: 10:00-11:00
provider meaning: busy
```

A local policy may then decide how to interpret it, for example:

```text
treat as hard local reservation
```

or:

```text
treat as tentative
```

or:

```text
require reconciliation
```

Provider semantics must not silently become universal LifeOS semantics.

The external-adapter layer is responsible for controlled mapping/degradation when LifeOS capacity semantics are richer than a provider's free/busy model.

---

# 17. Provenance and history

Availability rules, overrides, and material reservations may affect scheduling decisions and therefore can require history/provenance.

Example:

```text
Baseline Availability
09:00-18:00
```

later becomes:

```text
10:00-19:00
```

Past schedules should remain explainable under the availability/capacity assumptions that applied when relevant.

Similarly:

```text
Provider busy interval
15:00-16:00
```

later corrected or removed should not necessarily make it appear that LifeOS never saw the earlier information if that information influenced decisions.

The exact history/version structure is deferred to the Version/Provenance model.

---

# 18. Schedule revisions and capacity claims

When a blocking scheduled subject moves:

```text
Event
Meeting

old Schedule
15:00-16:00

new Schedule
16:00-17:00
```

its effective capacity claim should normally follow the accepted Schedule.

This operational dependency does not collapse the concepts.

The model remains:

```text
subject
   |
   +-> Schedule placement
   |
   +-> capacity impact / claim semantics
```

rather than:

```text
Schedule == reservation
```

This matters because another subject may be scheduled but non-blocking.

---

# 19. Reservation identity is deliberately not over-specified

The Time cluster establishes reservation semantics but does not require every blocking scheduled item to create a separate first-class `CapacityReservation` aggregate.

For an ordinary Event or Activity, capacity impact may later be physically represented as:

- a relation/capability attached to Schedule;
- a compact claim record;
- another normalized structure.

By contrast, a standalone construct whose primary meaning is itself to protect capacity may justify persistent identity, for example:

```text
Protected focus block
```

The physical distinction is intentionally deferred.

> **First-class semantic capability does not imply one mandatory table/entity shape.**

---

# 20. Capacity-only subject

A standalone protected block needs persistent user meaning even when no Activity/Event exists.

Conceptually:

```text
Capacity-only subject
Protected focus

Schedule
15:00-17:00

Capacity behavior
blocking / protected
```

The UI may call this a `Calendar Block`.

The kernel does not need to pretend that the user had a concrete Activity if the only intention was to protect time.

The exact persistence shape and whether a general `CapacityReservation` identity represents this subject remain deferred.

---

# 21. Context/location does not automatically consume capacity

A contextual fact such as:

```text
Working from office
```

```text
Working from home
```

```text
Travelling
```

may influence scheduling preferences, Temporal Constraints, or available resources without itself implying:

```text
busy
```

Therefore contextual state and location must not be collapsed into capacity consumption.

This is now compatible with Resource v0: Place/Location may later play Resource role where relevant, without context/location state itself becoming a capacity claim.

---

# 22. Capacity versus Actual utilization

Capacity describes what could be accepted/committed.

Actual utilization describes what really happened.

Example:

```text
Schedule
Focus work 15:00-17:00

Capacity Reservation
15:00-17:00 exclusive attention

Actual Session
15:20-16:10
```

Derived analytics may later compare:

- scheduled load;
- protected capacity;
- effective free capacity;
- actual utilization;
- unused reserved time;
- overcommitment;
- actual concurrency.

These are not one value.

Resource v0 adds the related guardrail that **allocated/reserved Resource != actually used Resource**.

---

# 23. Capacity versus effort

Capacity must not be confused with estimated effort.

```text
Activity estimated effort
3h
```

is not a statement that the user has three hours of capacity now.

Likewise:

```text
Schedule duration
2h
```

is not actual effort.

And:

```text
Capacity available
2h
```

is not a promise that two hours of useful work will be completed.

The Time cluster preserves all three dimensions separately.

---

# 24. Capacity-aware scheduler semantics

A future planner should reason about feasibility rather than merely empty rectangles.

For a candidate placement it should be able to evaluate:

1. does the subject's Temporal Constraint allow the placement?
2. what Resource Requirement(s), if any, must be satisfied?
3. which native referents/supplies are eligible Resource candidates?
4. is the relevant schedulable Resource available?
5. what capacity does the subject claim?
6. are existing claims compatible?
7. does a hard or protected reservation forbid displacement?
8. does movement/allocation authority permit changing existing placements/resources?
9. if infeasible, which conflict or assumption caused infeasibility?

The planner must not silently solve conflicts by deleting user intent, violating hard constraints, or pretending a Resource was selected before it actually was.

---

# 25. AI authority

AI may propose changes such as:

```text
Move study to 18:00 because free compatible capacity exists there
```

or:

```text
Protect 90 minutes tomorrow morning for focus work
```

or:

```text
Use Camera A17; it satisfies the requirement and is available
```

but proposal/acceptance rules remain consistent with Schedule v0, Resource v0 and the broader LifeOS authority model.

A proposed reservation/allocation does not become canonical merely because the AI generated it unless an approved automatic policy authorizes that action.

Imported external busy data likewise does not automatically override explicit user truth without the applicable integration/reconciliation policy.

---

# 26. Representative scenarios

## Scenario A — ordinary blocking meeting

```text
Event
Client meeting

Schedule
15:00-16:00

Capacity claim
exclusive primary attention
```

Result:

- Event remains the domain subject;
- no duplicate Calendar Block;
- the interval normally reduces compatible free capacity.

---

## Scenario B — optional webinar

```text
Event
Optional webinar

Schedule
15:00-16:00

Capacity impact
non-blocking / compatible
```

Result:

- remains visible;
- does not automatically make the user busy for all purposes.

---

## Scenario C — all-day birthday

```text
Event
Birthday

Schedule
all day
```

Result:

- all-day semantics preserved;
- no automatic 24-hour capacity reservation.

---

## Scenario D — focus protection without work identity

```text
Protected focus
15:00-17:00
```

Result:

- standalone capacity reservation/subject;
- UI may present Calendar Block;
- no fake Activity required.

---

## Scenario E — unavailability

```text
Availability Override
14:00-18:00
unavailable
```

Result:

- governed resource has no relevant capacity there;
- not represented as a hidden Activity.

---

## Scenario F — special available Saturday

```text
Baseline
Saturday unavailable

Override
Saturday 10:00-15:00 available
```

Result:

- positive exception increases effective availability.

---

## Scenario G — recurring working hours

```text
Availability Rule
09:00-18:00

Recurrence
Mon-Fri
```

Result:

- repeated applicability;
- does not generate meaningless Activity/Occurrence objects.

---

## Scenario H — illness mode

```text
Normal Availability
09:00-18:00

Temporary Mode
Illness

Temporary effective capacity
reduced
```

Result:

- normal baseline not rewritten;
- future planning may be reduced/replanned.

---

## Scenario I — two overlapping incompatible meetings

```text
Meeting A
15:00-16:00

Meeting B
15:30-16:30
```

Result:

- both facts remain representable;
- derived capacity conflict;
- resolution required rather than silent deletion.

---

## Scenario J — compatible overlap

```text
Walk
17:00-18:00

English listening
17:00-18:00
```

Result:

- overlap can be valid if capacity/compatibility semantics allow it;
- total unique wall-clock time is one hour, not automatically two.

---

## Scenario K — declined Event remains visible

```text
Event
Meeting 15:00-16:00

Response
declined
```

Result:

- Event may remain in history/calendar;
- user capacity can be free.

---

## Scenario L — imported provider busy interval

```text
External source
busy 10:00-11:00
```

Result:

- imported capacity/availability evidence with provenance;
- adapter/policy determines LifeOS interpretation;
- provider taxonomy is not kernel authority.

---

## Scenario M — travel buffer

```text
Flight Event
08:00

Temporal Constraint
arrive >= 2h before

Capacity Reservation
06:00-08:00 travel/airport
```

Result:

- rule and reservation remain separate;
- concrete reservation may be rendered as Calendar Block.

---

## Scenario N — recovery rule and recovery block

```text
Temporal Constraint
48h minimum recovery
```

may coexist with:

```text
Capacity Reservation
Protected Sunday morning recovery
```

Result:

- no conceptual duplication.

---

## Scenario O — capacity greater than one

Future example:

```text
Resource pool
3 equivalent slots

2 simultaneous reservations
```

Result:

- still has remaining capacity;
- binary free/busy cannot be the universal kernel model;
- the pool/quantity implementation remains deferred without requiring a universal Resource entity.

---

# 27. Adversarial boundary tests

## 27.1 Calendar item with no capacity effect

A scheduled informational item can remain scheduled without becoming a reservation.

Pass.

## 27.2 Reservation with no Activity/Event

Protected focus can reserve capacity without inventing work identity.

Pass.

## 27.3 Availability window and subject preference share same geometry

```text
18:00-20:00
```

can mean resource availability or preferred study window depending on semantics.

Geometry alone does not determine concept.

Pass.

## 27.4 Hard unavailability conflicts with imported Event

Both facts remain representable; conflict is derived.

Pass.

## 27.5 Overlap does not always equal conflict

Compatibility-based capacity supports simultaneous walking/listening.

Pass.

## 27.6 Capacity is not energy score

Model does not require one fake human percentage.

Pass.

## 27.7 Recurring Availability does not create execution Occurrences

Recurrence applies to the rule without changing its parent semantics.

Pass.

## 27.8 Temporary disruption does not rewrite normal weekly availability

Temporary Mode / overrides preserve baseline history.

Pass.

## 27.9 External provider disagreement

Imported provider busy data can coexist with local user interpretation/provenance.

Pass.

## 27.10 Resource model now defined

Resource v0 defines Resource as contextual planning/execution role/capability over native referents/supplies, not an entity/root. Availability/Capacity attaches to schedulable Resource-role cases without requiring wrapper identity.

Pass with hardening around Requirement/Allocation/Reservation and heterogeneous references.

---

# 28. Invariants

The current accepted invariants are:

1. **Schedule != Capacity Reservation / Claim.**
2. Schedule presence does not automatically imply busy or occupied capacity.
3. **Availability != Schedule.**
4. **Availability != Temporal Constraint**, even though both may limit planning feasibility.
5. **Availability != preference.**
6. **Capacity != Actual utilization.**
7. **Calendar Block is not a separate kernel primitive by default.**
8. Calendar Block remains valid product/UI language for time-shaped capacity-only constructs.
9. A scheduled Activity/Event/Occurrence must not require a duplicate Calendar Block solely to appear on the calendar or consume capacity.
10. Availability describes when a schedulable resource has capacity that may be used.
11. Capacity describes ability to accept compatible commitments and is not universally binary.
12. Capacity is not universally a single scalar, percentage, or energy score.
13. Capacity Reservation/Claim expresses capacity committed, occupied, protected, or held.
14. Effective Free Capacity is derived from effective Availability, claims/reservations, compatibility semantics, and applicable overrides.
15. Effective free intervals need not be canonical persisted truth merely because they can be computed.
16. Baseline Availability may recur without generating execution Occurrences.
17. Availability overrides may both subtract and add exceptional capacity.
18. Temporary modes may temporarily alter Availability/Capacity without rewriting the stable baseline.
19. A scheduled subject may be blocking, non-blocking, tentative, shared/compatible, or later use richer capacity semantics without changing subject identity.
20. Event invitation/participation/attendance state does not universally determine capacity impact.
21. All-day/date-based Schedule placement does not automatically imply full-day capacity consumption.
22. Hard unavailability applies to the governed resource/capacity; subject-specific timing limits normally belong to Temporal Constraint.
23. Capacity compatibility, not timestamp overlap alone, determines the semantic scheduling conflict.
24. Overlap is not universally invalid.
25. Overcommitted/conflicting states must remain representable and explainable.
26. LifeOS must not silently delete, rewrite, or ignore real commitments merely to make the planning state feasible.
27. Capacity may support exclusive, count-based, quantitative, or compatibility-based behavior in future without forcing one universal representation now.
28. Personal V1 may use pragmatic defaults without elevating those defaults into universal kernel invariants.
29. External free/busy is imported evidence/provenance and not automatically unquestionable LifeOS truth.
30. Provider-specific busy/free/tentative taxonomies remain adapter concerns when they do not match LifeOS semantics.
31. Context/location state does not automatically consume capacity.
32. Capacity and estimated effort remain distinct.
33. Capacity and scheduled duration remain distinct.
34. Capacity and Actual Session duration remain distinct.
35. Standalone protected capacity may have meaningful identity even when no Activity/Event exists.
36. The Time cluster does not require every ordinary blocking Schedule to create a separate first-class Reservation aggregate.
37. Reservation/claim physical persistence is deferred until logical persistence and Relationship/Allocation review.
38. Changes to Availability/Capacity that materially affected planning may require history/provenance rather than silent overwrite.
39. AI-generated reservations/availability/resource allocations remain proposals unless accepted by user authority or an explicitly authorized automatic policy.
40. **Resource is a contextual planning/execution role/capability, not an entity/root.**
41. **Availability/Capacity does not manufacture Resource identity.**
42. **A schedulable Resource is a Resource-role case whose time-dependent capacity matters; not every Resource requires calendar semantics.**
43. **Resource Requirement != candidate != Allocation != Reservation/Claim != actual use.**
44. Exact physical `Capacity`, `Availability`, `Reservation`, Resource-role reference, pool and compatibility structures remain deliberately deferred.

---

# 29. Alternatives considered

## Alternative A — Every scheduled item is busy

Rejected.

Fails on:

- birthdays/all-day information;
- optional webinars;
- passive compatible activities;
- declined Events retained for context;
- provider/imported informational items.

---

## Alternative B — Calendar Block as universal wrapper

```text
Activity/Event
    +
CalendarBlock
```

for every temporal placement.

Rejected.

Creates duplicate identity and duplicated timing/history without adding domain meaning.

---

## Alternative C — Calendar Block as independent peer primitive for every protected/unavailable case

Not preferred as the kernel baseline.

The user-facing concept is valuable, but its cases decompose more cleanly into:

- Capacity Reservation/Claim;
- Availability override;
- a richer existing Activity/Event/Occurrence where applicable.

---

## Alternative D — Availability as stored free gaps

Rejected as canonical domain truth.

Free gaps are normally derived from rules/overrides/reservations and would require constant destructive recomputation.

---

## Alternative E — Capacity as one percentage

Rejected.

Produces false precision and cannot model compatibility, exclusive attention, passive behavior, or future count/resource capacity.

---

## Alternative F — No overlap ever

Rejected.

Real history can be inconsistent, imported commitments can double-book, and some simultaneous Activities are genuinely compatible.

---

## Alternative G — Provider free/busy model as LifeOS kernel

Rejected.

Violates the Domain Atlas external-benchmark/interoperability rule and would constrain LifeOS to external schema limitations without product justification.

---

## Alternative H — Resource as universal entity/root

Rejected by Resource v0.

People, Assets, Places, services and supplies retain native semantics; Resource is the contextual operational role under which they may satisfy execution requirements.

A universal Resource wrapper would duplicate identity and encourage generic `resource_id` relationships that erase Requirement/Performer/Responsibility/Allocation semantics.

---

# 30. Deliberately deferred questions

Availability & Capacity v0 intentionally does **not** decide:

- final Resource Requirement representation;
- final Allocation/selection model;
- exact Account/Authority rights for allocating shared Resources;
- whether personal attention needs an explicit capacity profile record;
- the final capacity-dimension vocabulary;
- a quantitative compatibility model;
- the exact product defaults for blocking/non-blocking Activities and Events;
- exact reservation firmness states;
- exact reservation lifecycle;
- exact identity rules for standalone reservations;
- whether ordinary capacity claims are embedded, related, or persisted as separate rows;
- exact Availability revision/version tables;
- exact Temporary Mode structure;
- exact imported-provider reconciliation workflow;
- exact scheduler optimization algorithm;
- exact conflict severity taxonomy;
- exact Calendar UI rendering language;
- exact pool/count/supply representation;
- exact database range/index strategy;
- exact API payloads.

These decisions should be made only after the Data / Subjects cluster integration, Relationships / Reasoning review and logical persistence pressure provide enough context.

---

# 31. Implications for future persistence

Without fixing the schema, the future model must be capable of representing at least:

- baseline Availability rules;
- recurrent applicability where needed;
- positive/negative Availability overrides;
- capacity-impact semantics for scheduled subjects;
- standalone protected/tentative reservations;
- provenance/source;
- history/version context where material;
- references to native referents/supplies playing Resource role rather than requiring a universal Resource entity;
- Resource Requirements independently from concrete allocations;
- derived free-capacity queries;
- conflicts/overcommitment without destructive normalization;
- external provider mappings without provider semantics becoming canonical.

The persistence model should not force:

```text
one CalendarBlock row per scheduled object
```

or:

```text
one FREE/BUSY boolean as universal capacity truth
```

or:

```text
persist every computed free interval as canonical state
```

or:

```text
one universal resources table / resource_id wrapper
```

---

# 32. Implications for APIs

Future APIs should be able to distinguish operations such as:

```text
set/update baseline availability
```

```text
create availability override
```

```text
protect/reserve capacity
```

```text
define/query a Resource Requirement
```

```text
find Resource candidates
```

```text
allocate/select a candidate
```

```text
schedule a subject
```

```text
set/change capacity impact
```

```text
query effective capacity for a candidate
```

```text
query simple free/busy projection
```

```text
surface capacity conflict
```

These operations must not be collapsed into one ambiguous `calendar block` or `resource` endpoint merely because they may interact in the same scheduler.

---

# 33. Cross-concept consistency

Availability & Capacity v0 is consistent with the accepted model:

```text
Goal
what is wanted

Plan
how it is pursued

Activity
what action is intended

Event
what occurrence-centred thing is expected

Routine
what recurring behavioral policy exists

Recurrence
how repeated temporal/generative structure behaves

Occurrence
which expected generated instance exists

Temporal Constraint
where/when a subject may/must/preferably occur

Resource
what native referent/supply may satisfy an execution requirement in context

Availability / Capacity
whether the schedulable Resource can accept the commitment

Schedule
when the commitment is currently accepted

Session
which actual execution episode happened

Actual
broader truth about what happened

Evidence
what supports evaluation
```

No previous accepted Time primitive needs reopening solely because Resource v0 now closes the earlier deferred boundary.

The strongest combined cross-concept rule is:

> **appears in time != scheduled commitment != Resource requirement satisfied != Resource allocated != capacity consumed != resource unavailable != actual execution.**

These states may correlate, but LifeOS preserves their separate semantics.

---

# 34. Acceptance summary

Availability & Capacity v0 retains the following accepted direction:

```text
Availability
when schedulable capacity may be used

Capacity
ability to accept compatible commitments

Reservation / Claim
capacity committed/protected

Effective Free Capacity
derived state

Calendar Block
product/UI representation for capacity-only temporal constructs,
not a mandatory kernel primitive
```

Resource v0 now closes the earlier abstract-resource dependency:

```text
native referent / service / pool / supply
        ↓ contextual Resource role
may satisfy execution requirement
        ↓ when time-dependent capacity matters
Availability + Capacity
```

No universal Resource entity/root is introduced.

---

# 35. Resource v0 alignment — 2026-08-12

This section is a canonical amendment to the original Time-cluster text and **supersedes earlier forward-looking statements in this document that said the Resource model or Resource identity still belonged to a later review**.

Resource v0 is now accepted as:

> **a contextual planning/execution role/capability over native referents, services, pools, supplies or other eligible providers; not an independent universal entity/root.**

Therefore:

```text
Person may play Resource role
Asset may play Resource role
future Place may play Resource role
service/pool/supply may play Resource role where semantics justify it

Resource role != native identity
Resource != Requirement
Resource != Allocation
Resource != Reservation / Capacity Claim
Resource != actual use / consumption
```

For this Time-cluster concept, `schedulable resource` now means:

> a native referent/supply playing Resource role in a context where time-dependent Availability/Capacity matters.

This amendment does **not** reopen the accepted Time cluster. It closes an inherited deferred boundary and schedules regression during Data / Subjects cluster integration, the deferred-dependency closure, and Cross-Cluster Validation v4.
