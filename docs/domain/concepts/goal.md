# Goal v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Multi-actor wording hardening:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Goal is a persistent representation of an outcome, condition, change, or behavioral pattern intentionally adopted as desired within a LifeOS context: something to reach, produce, improve, reduce, maintain, avoid, or sustain over time. A Goal defines what is wanted, not the work plan, scheduling, ownership/governance relationship, or evidence used to pursue or evaluate it.**

A Goal can therefore represent both an end result and a desired pattern sustained over time.

The personal-first V1 case usually has one user governing the Goal, but that product default is not part of Goal identity. A later shared/team/care context may have multiple stakeholders or governors without requiring a different Goal primitive.

Examples:

- reach spoken English B2;
- pass an exam;
- rebuild a personal website by a target date;
- publish an album;
- save €20,000;
- reduce debt below a threshold;
- maintain weight within a range;
- train at least three times per week;
- study at least eight hours per week;
- keep a category of spending below a monthly ceiling;
- improve sleep quality;
- build a more satisfying social life;
- organize a shared trip;
- reach a team delivery outcome where a shared Goal is later justified.

## Why this definition

Earlier formulations that described a Goal only as a future state were too narrow. LifeOS must also represent process and behavioral goals such as frequency, duration, accumulation, reduction, or sustained maintenance.

The LifeOS feature-discovery simulation identified goal outcomes including binary completion, reach/reduce/accumulate, maintenance ranges, frequency, time invested, milestones, trends, external results, and hybrid outcomes. The domain model must cover all of those without creating a different Goal entity for each form.

The multi-actor discovery and evidence synthesis later exposed a second weakness in the original wording: defining Goal as only what `the user` wants accidentally fused desired-state identity with one personal owner/governor. That is correct as a common V1 product case but too narrow as a kernel invariant.

The definition therefore keeps the semantic core — an intentionally desired state/pattern — while separating Goal identity from ownership, governance, stakeholder, subject, contributor and account identity.

The definition also deliberately allows concrete outcomes such as `rebuild the personal website`. A finite deliverable is not automatically excluded from being a Goal.

## Core semantic separation

A Goal answers:

> **What is intentionally desired to become true, remain true, or repeatedly be true in this context?**

It does not by itself answer:

- how the result will be pursued;
- which Activities must be performed;
- who owns/governs/contributes to it;
- when operational work occupies calendar time;
- what evidence proves or measures progress.

Conceptually:

```text
Goal       -> what is wanted
Plan       -> how it may be pursued/organized
Activity   -> what action is intended
Schedule   -> when concrete execution is planned
Actual     -> what actually happened
Evidence   -> what supports an evaluation
```

`Project` and `Program` remain product/profile candidates around Plan semantics unless a later review demonstrates materially distinct kernel identity/lifecycle/invariants.

## Goal versus Plan / Project / Program

A Goal expresses the desired condition/result. A Plan expresses how a purpose is pursued or coordinated.

```text
Goal
Rebuild website by 30 September

Plan
Design -> implementation -> deployment
```

The previous V1 glossary treated `Goal`, `Project`, and `Program` as necessarily distinct kernel nouns. Current Domain Atlas direction does not.

A product may still present:

```text
Project: Website Redesign
Program: 12-week Training
```

while their strategy/coordination semantics are represented by Plan unless later evidence justifies separate primitives.

Do not create a duplicate Project/Goal solely because a finite desired outcome requires coordinated work.

## Goal versus Routine

A behavioral Goal and a Routine can look similar but express different semantics.

```text
Goal
Train at least 3 times per week

Routine
Gym Monday / Wednesday / Friday
```

The Goal defines the desired condition. The Routine is an operational repeated policy intended to help produce it.

The Routine can be replaced while preserving the Goal. The Goal can also be satisfied through execution outside the Routine.

Therefore:

> **Goal != Routine.**

## Goal versus Activity

An Activity is actionable intended work/behavior. A Goal expresses the desired result or behavioral condition.

`Go to the gym` may be an Activity when it means a concrete action. `Train at least three times per week` may be a Goal when it expresses a desired behavioral pattern.

Natural-language wording alone does not determine the concept; domain intent does.

Therefore:

> **Goal != Activity.**

## Goal versus Temporal Constraint

A Goal represents a desired state/pattern. A Temporal Constraint restricts or prefers temporal placement/duration/relationships.

```text
Goal
Keep restaurant spending <= €500/month

Temporal Constraint
Never schedule meetings after 18:00
```

Therefore:

> **Goal != Temporal Constraint.**

## Goal versus Life Area / Value

`Family is important to me` is not necessarily a Goal. It may represent a value or organizational context.

`Spend at least two evenings per week with my family` can be a Goal because it states a desired condition/pattern.

Therefore:

> **Goal != Life Area / Value.**

The exact Life Area / Value model remains a separate review topic.

## Criteria are separate from Goal identity

The Goal expresses what is wanted. Evaluation criteria express how LifeOS can determine or assess whether the desired result/pattern is being reached or sustained.

A Goal may have zero or more criteria.

Examples:

```text
Goal
Become more physically active

Criteria
- >= 3 training sessions/week
- >= 150 active minutes/week
- optional monthly self-assessment
```

```text
Goal
Rebuild personal website

Criteria
- new site published
- mobile responsive
- portfolio updated
- old site replaced
```

```text
Goal
Maintain body weight

Criterion
65 kg <= measured weight <= 67 kg
```

This avoids forcing every Goal into a universal `target_value` or `progress_percentage` field.

## Required evaluation expressiveness

The future criterion/evaluation model must be capable of representing, where useful:

- boolean/binary outcome;
- threshold at or above a value;
- threshold at or below a value;
- target value;
- acceptable range;
- accumulation;
- frequency within a period;
- duration within a period;
- milestone/checkpoint;
- trend/directional change;
- external result;
- manual/qualitative assessment;
- composite criteria.

These are semantic requirements, not a decision to implement one enum value or table per form.

## Evidence and progress sources

A criterion may eventually be evaluated from one or multiple evidence sources, including:

- explicit authorized declaration;
- Activity Actual/execution history;
- Session duration;
- Routine Occurrences/Actuals;
- Register/measurement history;
- Observation;
- Milestone;
- external integration/import;
- derived formula;
- manual/qualitative assessment.

The Goal must not depend directly on one specialist module to remain reusable across life domains.

Valid Evidence may later become relevant even when it was not originally produced for the Goal. That discovered relevance must not rewrite historical intention.

## Progress is derived, not universal state

LifeOS must not assume every Goal has a canonical stored percentage.

For some Goals a percentage is meaningful and can be derived. For others it creates false precision.

Examples:

- saving €20,000 can support a useful ratio;
- maintaining weight in a range is evaluated over time rather than linearly toward 100%;
- training three times each week can succeed/fail by period;
- a more satisfying social life may rely partly on qualitative assessment.

Therefore:

> **A progress percentage is an optional derived presentation, not an invariant property of Goal.**

## Temporal semantics

A Goal may have temporal information such as:

- effective/start date;
- target date;
- target window;
- evaluation period;
- open-ended horizon;
- review date.

A Goal having temporal targets does not mean it directly occupies operational calendar capacity.

```text
Goal
Rebuild website by 30 September
```

may expose the target in timeline/calendar surfaces, while concrete work is represented separately:

```text
Activity
Work on homepage

Schedule
Saturday 09:00-13:00
```

A target date/window and a review date are also semantically distinct from a hard Temporal Constraint unless explicitly modeled that way.

## Terminal and sustained semantics

LifeOS must support both terminal and continuously/repeatedly evaluated Goals.

```text
Save €20,000 by December
```

can reach a terminal achievement.

```text
Maintain weight between 65 and 67 kg
```

is normally evaluated over time.

```text
Maintain weight between 65 and 67 kg for six months
```

uses maintenance semantics with a bounded duration.

Therefore `maintain` must not be equated with `open-ended`.

## Identity and continuity

A Goal has persistent identity independent of the strategy used to pursue it and independent of ordinary changes in participant/contributor relationships.

Changing from one study/training/financial/execution strategy to another may preserve Goal identity when the intended desired state remains materially the same.

Likewise, ordinary changes in who contributes or coordinates do not automatically replace the Goal.

A materially changed desired result/meaning may require versioning or replacement. Exact version/replacement rules remain deferred.

## Governance, stakeholders and subject

Goal identity is distinct from all of:

```text
governor / owner / steward
stakeholder
contributor
subject / beneficiary
creator
account/principal
```

The personal-first case may be:

```text
Governor: user
Subject: user
Goal: Reach spoken English B2
```

but LifeOS must also remain capable of later representing shapes such as:

```text
Governor/context: household or multiple authorized actors
Goal: Organize shared Japan trip
Stakeholders: several participants
```

or:

```text
Governor: caregiver/authorized context
Subject: cared-for person
Goal: maintain an agreed non-clinical daily-living condition
```

or:

```text
Governor: user
Subject: car
Goal: reduce average fuel consumption below X
```

Exact Actor/Person/Subject/Authority/Group models remain deferred. This section establishes only the non-collapse rule.

## Authority and provenance

For a personal Goal under the user's authority, explicit user declaration may establish achievement where no stronger domain-specific rule applies.

Shared, professional, care or externally governed Goals may later require different authority semantics.

LifeOS must preserve how an evaluation/change was established, for example:

- authorized explicit declaration;
- imported external fact;
- derived measurement;
- automatically applied approved rule;
- provisional inference;
- AI proposal awaiting authority.

Provenance must not be confused with truth/authority. AI inference is not automatically canonical Goal state.

## AI boundary

AI may propose:

- a Goal;
- wording refinements;
- criteria;
- horizons/target dates;
- Plans/execution strategies;
- possible interpretations of progress;
- possible shared/stakeholder relationships.

AI does not gain Goal governance authority merely because it has context.

Canonical changes follow the authority/policy of the actor/context under which AI acts.

## Multi-actor evidence hardening

The completed multi-actor simulation/research confirms:

```text
Goal identity != one mandatory personal owner
Goal identity != participant/contributor set
Goal identity != subject
creator != authority by default
```

One genuinely shared desired state should not require per-user duplicate Goals solely to fit a single-owner schema.

This does not mean every apparently similar personal objective should be merged into one shared Goal. Independent intentions remain independent when actors genuinely hold separately governed desired states.

## Current invariants

1. `Goal != Activity`.
2. `Goal != Routine`.
3. `Goal != Schedule`.
4. `Goal != Temporal Constraint`.
5. `Goal != Life Area / Value`.
6. `Goal != Plan`.
7. A Goal may exist without a detailed execution Plan.
8. A Goal may have zero or more evaluation criteria.
9. A Goal may be quantitative, qualitative, or hybrid.
10. A Goal may be bounded or open-ended.
11. A Goal may express terminal achievement or sustained/repeated evaluation.
12. A Goal may have a target date/window without directly occupying operational calendar time.
13. A Goal may be supported by multiple execution structures.
14. One execution structure may contribute to multiple Goals.
15. Goal progress may be supported by multiple evidence sources.
16. Progress is not necessarily a percentage and percentage is not universal canonical state.
17. Goal identity survives ordinary strategy changes when the desired state remains materially the same.
18. Goal identity is independent from one mandatory owner/governor/account.
19. Goal governance, stakeholder, contributor and subject relationships remain conceptually separable.
20. Historical structural/meaningful changes must not silently rewrite past meaning.
21. Valid later Evidence may become relevant without rewriting original intention.
22. An authorized declaration may establish Goal evaluation when applicable; exact authority depends on context/domain and provenance is preserved.
23. AI proposals do not directly establish canonical Goal state or authority.
24. A genuinely shared Goal must not require semantic duplication solely because multiple actors are involved.
25. Independent personal intentions must not be merged merely because their wording/outcome resembles a shared Goal.

## Stress-test coverage

The current model has been checked against broad personal and multi-actor scenario families including:

- study, exams, language learning and research;
- software/professional work and deadlines;
- shifts and field work;
- farming, inventory, production, home/vehicle maintenance;
- medication, sport, sleep, symptoms and caregiving;
- job search, travel, freelancing and savings;
- creative production, photography and writing;
- unemployment, moving, animals/plants and disrupted weeks;
- shared trips/social planning;
- household coordination;
- team/shared outcomes;
- caregiver/subject separation;
- external participants and professional contexts.

Representative Goal shapes include:

| Case | Current representation |
|---|---|
| Reach spoken English B2 | Goal + assessment/manual criteria |
| Pass an exam | Goal + target + external/binary result |
| Rebuild a website | Goal + target + criteria + optional Plan |
| Reach target weight | numeric criterion |
| Maintain 65-67 kg | range criterion evaluated over time |
| Train 3 times/week | frequency criterion |
| Study 8 hours/week | duration criterion |
| Save €20,000 | accumulation criterion |
| Keep spending <= €500/month | upper-bound criterion |
| Improve sleep | metric/trend/qualitative criteria |
| Improve social life | qualitative/manual criteria |
| Publish 3 songs/month | frequency/outcome criterion |
| Find a job | external-result criterion |
| Improve a car metric | Goal with Asset/Subject context |
| Shared trip outcome | one Goal where genuinely shared governance is later supported |
| Change execution strategy | same Goal with preserved history |

No reviewed case requires changing the fundamental Goal primitive.

## Deliberately deferred questions

- exact Goal lifecycle/state machine;
- version/replacement persistence;
- GoalCriterion model;
- exact Goal ownership/governance cardinalities;
- Actor/Person/Account/Principal/Subject model;
- shared Goal approval/governance lifecycle;
- relationship vocabulary (`supports`, `depends_on`, `conflicts_with`, etc.);
- Life Area / Value semantics;
- exact Asset/Subject model;
- exact progress/evaluation implementation;
- API/SQL representation.

## Decision note

Goal v0 remains the accepted desired-state primitive.

The 2026-08-11 hardening changes **who/what may govern or be subject to a Goal**, not Goal's core semantic identity. The previous personal-first wording is therefore superseded without introducing a new Goal type.