# Conditional Policy v0

**Status:** Current accepted baseline — propagation pending final QA  
**Accepted:** 2026-08-15  
**Meaning of accepted:** best current semantic decision; reopenable with stronger evidence  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **A Conditional Policy is a contextual rule/capability that specifies a bounded downstream response when a defined activation basis becomes satisfied or occurs within its applicable scope, while leaving the source condition, applicable Authority, and resulting target state/effect to their owning semantics.**

A Conditional Policy answers:

> **When this qualifying basis is established in this scope, what bounded response is intended to be initiated, proposed, requested, or applied?**

Conceptual shape:

```text
qualifying event / state / evaluation / time
                    ↓
          activation basis satisfied
                    ↓
            Conditional Policy
                    ↓
       bounded downstream response
```

The three layers remain distinct:

```text
activation basis
!= Conditional Policy
!= resulting operation/effect
```

## Trigger semantics

`Trigger` is accepted as activation vocabulary/role inside conditional-response semantics.

> **Trigger describes the occurrence or establishment of the activation basis through which an applicable Conditional Policy becomes eligible to initiate its bounded response.**

`Trigger` does not survive as a universal independent entity/root.

```text
Trigger
✅ canonical activation vocabulary / role
❌ universal standalone root/entity
```

A Trigger does not own the source fact, event, Observation, Evaluation, time relation, or downstream action. Those retain their owning semantics.

## Canonical boundaries

```text
Conditional Policy != Dependency
Conditional Policy != Criterion / Evaluation
Conditional Policy != Recurrence
Conditional Policy != Temporal Constraint
Conditional Policy != Schedule
Conditional Policy != Decision
Conditional Policy != Authority
Conditional Policy != Proposal / Request
Conditional Policy != Actual
Conditional Policy != Reminder / Notification
Conditional Policy != generic Workflow / Automation

Trigger != source condition/fact/event
Trigger != downstream action/effect
Trigger != standalone universal primitive
```

### Conditional Policy versus Dependency

Dependency describes contingency:

```text
B may proceed / be satisfied only if prerequisite A-state holds
```

Conditional Policy describes conditional response:

```text
when qualifying A-state is established
→ initiate/propose/apply bounded response X
```

Therefore:

> **Dependency satisfaction does not cause action by itself.**

A Dependency may be one input to a Conditional Policy, but the two semantics remain separate.

### Conditional Policy versus Criterion / Evaluation

Criterion specifies what is evaluated. Evaluation applies a Criterion to Evidence/context and produces an evaluative result.

Example:

```text
Criterion
balance < €500

Evaluation
true

Conditional Policy
if the applicable Evaluation is true
→ notify / propose / request / act within scope
```

The Criterion and Evaluation do not become the Conditional Policy.

### Conditional Policy versus Recurrence

Recurrence owns repeated temporal/generative structure.

```text
Every Monday
3 expected practices per week
30 days after qualifying completion
```

may be Recurrence semantics.

```text
if account balance < €500
→ notify

if temperature > 30°C
→ suggest lighter training

when vehicle usage reaches 10,000 km
→ propose maintenance
```

are conditional-response semantics.

A recurring policy may itself be repeatedly applicable, but repeated applicability does not collapse Conditional Policy into Recurrence.

### Conditional Policy versus Time

Time can supply activation basis without becoming policy semantics.

```text
at 18:00
when scheduled window ends
24h before Schedule start
```

may participate in activation.

But:

```text
Temporal Constraint
= temporal admissibility/requirement/preference

Schedule
= accepted temporal assignment

Conditional Policy
= what bounded response should occur when its basis is established
```

These remain separate.

### Conditional Policy versus Decision and Authority

A policy can be defined, applicable, and activated without manufacturing Authority.

```text
policy exists
!= policy may legitimately act

policy activates
!= resulting effect is authoritative/effective
```

A policy may initiate a Proposal, Request, Decision workflow, or already-authorized bounded operation depending on applicable governance. The affected concept owns effective state.

> **Conditional Policy never grants itself Authority.**

### Conditional Policy versus Actual

Policy expresses intended conditional response, not reality.

```text
policy activated
→ response attempted
→ response failed
```

The activation remains historical. Failure does not erase it and does not fabricate successful Actual.

Likewise a source state later corrected does not permit silent deletion of consequential action history.

## Absence and unknown state

Absence/non-response may participate in an activation basis only when the applicable policy explicitly defines it that way.

```text
no data != false
no data != true
unknown != negative fact
```

Example:

```text
scheduled window ended
AND item remains unresolved under applicable semantics
→ include in end-of-day review
```

is valid if explicitly defined.

But failure to receive a provider event must not silently fabricate the source condition.

## Transition, persistent-state, and repeated-observation semantics

Conditional-response correctness often depends on distinguishing:

```text
when value crosses below threshold
vs
while value remains below threshold
vs
every new qualifying Observation below threshold
```

Conditional Policy v0 requires that this distinction remain expressible where consequential, without yet selecting a DSL or physical representation.

Repeated import/Observation of the same underlying event does not automatically establish a new semantic activation.

## Activation and response history

Where consequence warrants it, LifeOS must be able to reconstruct:

```text
which policy/material state applied
what activation basis was established
when it became applicable
what response was initiated/proposed/applied
whether that response succeeded/failed/remained pending
what later correction or policy change occurred
```

Material policy change does not silently inherit prior activation, approval, or applicability.

Pause/revocation/end of applicability affects future behavior but does not erase historical activations/effects.

## Conflict and precedence

Competing Conditional Policies may coexist or conflict.

No universal winner is accepted:

```text
latest wins
most specific always wins
user wins
manager wins
provider wins
AI wins
highest numeric priority wins
```

Resolution depends on applicable domain semantics, Authority, Decision/Reconciliation, and policy context.

Conflict detection does not itself choose a winner.

## Loops and cycles

Conditional policies can form loops:

```text
Policy A response changes state X
state X activates Policy B
Policy B response changes state Y
state Y activates Policy A
```

LifeOS must be able to represent and diagnose this as a real condition. Conditional Policy v0 does not impose universal acyclicity.

Loop prevention, recursion limits, idempotency, retry, debounce, deduplication, and runtime execution safeguards are later reasoning/runtime concerns.

## Multi-Actor semantics

One shared fact/object may support actor-scoped Conditional Policies without duplicating reality.

```text
shared Event
Dinner 20:00

Actor A policy
remind me 30 min before

Actor B policy
no reminder
```

The Event remains one shared Event.

Likewise:

```text
shared Conditional Policy
!= every Actor agrees with it
!= every Actor may alter it
!= every Actor may see every private activation basis/rationale
```

A private basis may yield an authorized bounded public/shared result without disclosing the private reason.

Example:

```text
private suitability/recovery input
→ policy evaluation/activation
→ shared result: unavailable for assignment
```

The shared result does not automatically disclose the private evidence.

## Actor and authorship separation

The following may all differ:

```text
source Actor
recorder/importer
policy author
policy adopter/approver
Actor whose private state forms part of the basis
affected Actor
action recipient
actual executing service/Actor
```

Technical execution must not rewrite human authorship or will.

AI may suggest, rank, simulate, or evaluate a Conditional Policy, but:

```text
AI suggestion != adopted Policy
AI Evaluation != human Decision
AI access != disclosure Authority
AI execution != human authorship
AI inference != source fact
```

## Progressive formality

A simple case may remain lightweight:

```text
If still unresolved at 18:00 → put in daily review
```

A consequential case may require explicit scope, material version, Authority context, history, Provenance and privacy.

This does not justify a universal workflow entity/root.

## Accepted hardenings — CP-01..30

```text
CP-01  Conditional Policy is a specific conditional-response family, not a generic Rule root.
CP-02  Trigger is an activation role/facet, not a universal standalone entity/root.
CP-03  The source event/state/fact retains its owning concept identity.
CP-04  The downstream operation/effect retains its owning semantics.
CP-05  Conditional Policy does not create Authority.
CP-06  Policy applicability/effectiveness must be reconstructible where materially consequential.
CP-07  Dependency satisfaction does not cause action without applicable Conditional Policy semantics.
CP-08  Conditional Policy != Dependency.
CP-09  Conditional Policy != Criterion / Evaluation.
CP-10  Conditional Policy != Recurrence.
CP-11  Conditional Policy != Temporal Constraint / Schedule.
CP-12  Conditional Policy != Decision.
CP-13  Conditional Policy != Proposal / Request.
CP-14  Conditional Policy != Actual.
CP-15  Reminder/notification is a possible response, not the Policy or Trigger itself.
CP-16  Absence/non-response is a condition only when explicitly part of the applicable policy.
CP-17  No data != condition false; no data != condition true.
CP-18  Consequential repeat behavior must distinguish transition/event, persistent-state, and repeated-observation semantics where needed.
CP-19  Repeated observation/import of the same underlying event does not automatically create a new semantic activation.
CP-20  Policy activation != downstream response success.
CP-21  Failed response does not erase the activation that initiated it.
CP-22  Material Policy change does not silently inherit prior activation/approval/applicability.
CP-23  Pause/revocation/end of applicability does not erase history.
CP-24  Competing policies may remain unresolved; no universal LWW/newest/highest-priority winner.
CP-25  Policy loops/cycles are representable failure conditions; no universal acyclic assumption.
CP-26  Private activation basis may yield an authorized bounded effect without forcing disclosure of private rationale/evidence.
CP-27  Source Actor, recorder, policy author, approving Actor, affected Actor and action recipient may all differ.
CP-28  AI may propose/evaluate a Policy but does not manufacture adoption, Authority or human intent.
CP-29  Simple inline conditional configuration is allowed; qualified policy state/history only where consequential.
CP-30  No SQL/API DSL/event-bus/workflow-engine representation is accepted by semantic review.
```

## Rejected abstractions

```text
universal Trigger entity/root
universal Condition entity/root from this review
universal Action entity/root from this review
generic Rule root
generic Workflow root
generic Automation root
event-bus schema as ontology
cron expression as ontology
provider automation schema as ontology
```

## Safe-deferred questions

Still deferred with separate ownership:

- AND/OR/NOT/threshold/temporal condition-expression composition;
- transition/edge versus persistent-state versus repeated-observation logical representation;
- idempotency/dedup/retry/debounce runtime mechanics;
- compensation/rollback workflows;
- domain-specific conflict/precedence policy;
- loop/cycle detection algorithms and runtime safeguards;
- Reminder / Notification primitive status;
- exact policy/activation-history materialization and retention;
- external event/provider adapters;
- logical/physical/API representation.

These do not reopen Conditional Policy v0 unless their exact reopen conditions are met in the validation checkpoint.

## Current verdict

```text
CONDITIONAL POLICY v0
+ TRIGGER ACTIVATION SEMANTICS

PASS WITH HARDENING

Conditional Policy
✅ canonical specific contextual conditional-response family/capability

Trigger
✅ canonical activation role/vocabulary
❌ standalone universal root/entity

Generic Rule / Workflow / Automation root
❌ rejected

REOPEN       0
UNCLASSIFIED 0
```

Final repository closure remains conditional on approved propagation and remote post-write QA.