# Goal v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Goal is a persistent representation of an outcome, condition, change, or behavioral pattern that the user intentionally wants to reach, produce, improve, reduce, maintain, avoid, or sustain over time. A Goal defines what is wanted, not the work plan, scheduling, or evidence used to pursue or evaluate it.**

A Goal can therefore represent both an end result and a desired pattern sustained over time.

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
- build a more satisfying social life.

## Why this definition

Earlier formulations that described a Goal only as a future state were too narrow. LifeOS must also represent process and behavioral goals such as frequency, duration, accumulation, reduction, or sustained maintenance.

The existing LifeOS feature-discovery simulation already identified goal outcomes including binary completion, reach/reduce/accumulate, maintenance ranges, frequency, time invested, milestones, trends, external results, and hybrid outcomes. The domain model must cover all of those without creating a different Goal entity for each form.

The definition also deliberately allows concrete outcomes such as `rebuild the personal website`. A finite deliverable is not automatically excluded from being a Goal.

## Core semantic separation

A Goal answers:

> **What does the user want to become true, remain true, or repeatedly be true?**

It does not by itself answer:

- how the result will be pursued;
- which activities must be performed;
- when operational work occupies calendar time;
- what evidence proves or measures progress.

Conceptually:

```text
Goal          -> what is wanted
Plan/Program  -> how it may be pursued
Activity      -> what is done
Schedule      -> when concrete execution is planned
Actual        -> what actually happened
Evidence      -> what supports an evaluation
```

The exact status of `Program` and especially `Project` remains subject to separate domain review.

## Goal versus Project

The previous canonical glossary treated `Goal` and `Project` as necessarily distinct. This is now explicitly **open for revalidation**.

Example:

```text
Goal: Rebuild my personal website by 30 September
```

is semantically valid. It should not require a duplicate `Project: Rebuild my personal website` merely because the result involves coordinated finite work.

Current rule:

> Do not introduce `Project` as an independent domain primitive until separate review demonstrates materially distinct identity, lifecycle, invariants, or behavior that cannot be represented cleanly through Goal plus execution structures.

This does not decide that Project must disappear. It removes the assumption that it must exist.

## Goal versus Routine

A behavioral Goal and a Routine can look similar but express different semantics.

```text
Goal
Train at least 3 times per week

Routine
Gym Monday / Wednesday / Friday
```

The Goal defines the desired condition. The Routine is an operational pattern intended to help produce it.

The Routine can be replaced while preserving the Goal. The Goal can also be satisfied through actions that do not follow the Routine exactly.

Therefore:

> **Goal != Routine.**

## Goal versus Activity

An Activity is executable work or action. A Goal expresses the desired result or behavioral condition.

`Go to the gym` may be an Activity when it means a concrete action. `Train at least three times per week` may be a Goal when it expresses a desired behavioral pattern.

Natural-language wording alone does not determine the entity; user intent and domain semantics do.

Therefore:

> **Goal != Activity.**

## Goal versus Constraint

A Goal describes something the user wants to achieve or sustain.

A Constraint restricts planning or execution.

Examples:

```text
Goal:
Keep restaurant spending <= €500/month

Constraint:
Never schedule meetings after 18:00
```

The first is a state to evaluate. The second constrains what the planner may do.

Therefore:

> **Goal != Constraint.**

## Goal versus Life Area / Value

`Family is important to me` is not necessarily a Goal. It may represent a value or organisational life area.

`Spend at least two evenings per week with my family` can be a Goal because it states a condition the user wants to sustain.

Therefore:

> **Goal != Life Area / Value.**

The exact Life Area / World / Value model remains a separate review topic.

## Criteria are separate from the Goal

The Goal expresses what the user wants. Evaluation criteria express how LifeOS can determine or assess whether the desired result or pattern is being reached or sustained.

A Goal may have zero or more criteria.

Examples:

```text
Goal
Become more physically active

Criteria
- >= 3 training sessions / week
- >= 150 active minutes / week
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

The future criterion model must be capable of representing at least:

- boolean / binary outcome;
- threshold at or above a value;
- threshold at or below a value;
- target value;
- acceptable range;
- accumulation;
- frequency within a period;
- duration within a period;
- milestone or checkpoint;
- trend or directional change;
- external result;
- manual / qualitative assessment;
- composite criteria.

These are required semantics, not a decision to implement one database enum per item.

## Evidence and progress sources

A criterion may eventually be evaluated from one or multiple evidence sources, for example:

- explicit user declaration;
- Activity Actual / execution history;
- real Session duration;
- Routine occurrences;
- Register / measurement history;
- Observation;
- Milestone;
- external integration/import;
- derived formula;
- manual assessment.

The Goal must not depend directly on any one specialist module in order to remain reusable across life domains.

## Progress is derived, not universal state

LifeOS must not assume that every Goal has a canonical stored percentage.

For some Goals a percentage is meaningful and can be derived. For others it would be false precision.

Examples:

- saving €20,000 can support a useful numerical progress ratio;
- maintaining weight in a range is evaluated over time rather than progressing linearly toward 100%;
- training three times each week may be satisfied in one period and not another;
- a more satisfying social life may depend partly on qualitative assessment.

Therefore:

> **A progress percentage is an optional derived presentation, not an invariant property of Goal.**

Progress evaluation may use metrics, criteria, evidence, formulas, or user assessment according to the Goal.

## Temporal semantics

A Goal may have temporal information such as:

- effective/start date;
- target date;
- target window;
- evaluation period;
- open-ended horizon;
- review date.

A Goal having a date does not mean it directly occupies calendar time.

Example:

```text
Goal
Rebuild website by 30 September
```

may expose the target date in timeline/calendar surfaces, while concrete work such as:

```text
Work on homepage — Saturday 09:00-13:00
```

is a separately schedulable execution item linked to the Goal.

Therefore:

> **A Goal may be time-bounded without itself being an operational time block.**

A review date is also semantically distinct from a target/deadline date.

## Terminal and sustained semantics

LifeOS must support both Goals that can reach a terminal achievement and Goals that are evaluated continuously or repeatedly.

Examples:

```text
Save €20,000 by December
```

can reach a terminal state.

```text
Maintain weight between 65 and 67 kg
```

is normally evaluated over time.

```text
Maintain weight between 65 and 67 kg for six months
```

uses maintenance semantics but still has a bounded end condition.

Therefore `maintain` must not be equated with `open-ended`, and the implementation should not prematurely encode an overly simple `ATTAIN/MAINTAIN` enum before the criterion and lifecycle models are reviewed.

## Identity and continuity

A Goal has persistent identity independent of the strategy used to pursue it.

If the user changes from one study plan, workout strategy, financial method, or project structure to another while pursuing the same intended result, the Goal may remain the same Goal.

This allows LifeOS to preserve the history of attempted strategies without falsely representing each strategy change as a new intention.

A materially changed desired result or criterion may require versioning or possibly a new Goal; the exact versioning boundary will be decided in the history/versioning review.

## Ownership and subject

The owner of a Goal and the subject of the Goal are conceptually distinct.

The user may own a Goal whose subject is:

- the user themself;
- another person they care for;
- an animal or plant;
- an asset such as a vehicle or home;
- another managed subject supported by the future Asset/Subject model.

Examples:

```text
Owner: user
Subject: car
Goal: reduce average fuel consumption below X
```

```text
Owner: user
Subject: plant
Goal: maintain healthy condition
```

This distinction does not imply multi-user collaboration or permissions in V1. It prevents the Goal model from assuming that every tracked desired state is directly about the owning user.

## User authority and provenance

For the user's own Goals, an explicit user declaration that the Goal has been achieved remains authoritative unless a specific domain rule requires otherwise.

LifeOS may also track how an evaluation was established, for example:

- user-confirmed;
- imported from an external system;
- derived from measurements;
- automatically applied by a user-approved rule;
- inferred provisionally and awaiting confirmation.

Provenance must not be confused with truth status. AI inference is not automatically canonical fact.

## AI boundary

AI may propose:

- a new Goal;
- wording refinements;
- possible criteria;
- possible horizon or target dates;
- possible plans or execution strategies;
- possible interpretations of progress.

AI does not bypass domain validation or directly establish canonical Goal state merely by generating a proposal.

Material changes follow LifeOS user-control and provenance rules.

## Current invariants

1. `Goal != Activity`.
2. `Goal != Routine`.
3. `Goal != Schedule`.
4. `Goal != Constraint`.
5. `Goal != Life Area / Value`.
6. A Goal may exist without a detailed execution plan.
7. A Goal may have zero or more evaluation criteria.
8. A Goal may be quantitative, qualitative, or hybrid.
9. A Goal may be bounded or open-ended.
10. A Goal may express terminal achievement or sustained/repeated evaluation.
11. A Goal may have a target date/window without directly occupying operational calendar time.
12. A Goal may be supported by multiple execution structures.
13. One execution structure may contribute to multiple Goals.
14. Goal progress may be supported by multiple evidence sources.
15. Progress is not necessarily a percentage and a percentage is not universally canonical state.
16. A Goal retains identity across ordinary strategy changes.
17. Goal ownership is distinct from its optional subject.
18. Historical structural changes must not silently rewrite past meaning.
19. User-declared achievement is authoritative for the user's own progress subject to explicit domain-specific rules, with provenance preserved.
20. AI proposals do not directly establish canonical Goal state.

## Stress-test coverage

The current model was checked against the existing LifeOS feature-discovery simulation, including scenarios involving:

- study, exams, language learning, research;
- software/professional work and hard deadlines;
- shift work and field work;
- farming, inventory, production, home and vehicle maintenance;
- medication, sport, sleep, symptoms and caregiving;
- job search, travel, freelancing and savings;
- creative production, photography and writing;
- unemployment, moving house, animals/plants, attention difficulties and disrupted weeks.

Representative Goal cases that fit without special-case entity types include:

| Case | Current representation |
|---|---|
| Reach spoken English B2 | Goal + assessment/manual criteria |
| Pass an exam | Goal + target date + external/binary result |
| Rebuild a website | Goal + target window + completion criteria |
| Reach a target weight | numeric criterion |
| Maintain 65-67 kg | range criterion evaluated over time |
| Train 3 times/week | frequency criterion |
| Study 8 hours/week | duration criterion |
| Save €20,000 | accumulation criterion |
| Keep spending <= €500/month | upper-bound criterion |
| Improve sleep | metric/trend and/or qualitative criteria |
| Improve social life | qualitative/manual criteria |
| Publish 3 songs/month | frequency/outcome criterion |
| Find a job | external-result criterion |
| Improve a car metric | Goal with Asset as subject |
| Maintain a plant's condition | Goal with Subject/Asset |
| Change strategy mid-way | same Goal with preserved history |

No case in the reviewed simulation currently requires changing the fundamental Goal definition.

## Deliberately deferred questions

The following are not decided by Goal v0 and must be reviewed separately:

- whether `Project` exists as an independent domain entity;
- exact `Program` semantics;
- exact lifecycle state machine for Goal;
- whether and how Goal versions are represented physically;
- criterion entity/value-object boundaries and persistence;
- relationship model for `supports`, `contributes_to`, decomposition, and multi-goal execution;
- Life Area / World / Value semantics;
- generic Asset / Subject model;
- exact progress-policy implementation;
- API and SQL representation.

## Decision note

Goal v0 is intentionally broader than the previous glossary definition and supersedes it **for the active Domain Model workstream only** while the broader documentation set is being revalidated.

The older glossary remains preserved as source material until changes are propagated deliberately after related concepts have been reviewed.
