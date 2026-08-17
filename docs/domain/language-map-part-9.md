<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-8.md" -->
> **Canonical continuation of the LifeOS Domain Language Map.** Earlier terminology remains preserved; this part promotes Conditional Policy / Trigger vocabulary after v0 validation.

# 2026-08-15 — Conditional Policy / Trigger terminology

## Canonical terms

### Conditional Policy

> Contextual rule/capability specifying a bounded downstream response when a defined activation basis becomes satisfied or occurs within its applicable scope.

Use when the semantic question is:

> **When this qualifying basis is established, what bounded response should follow?**

### Trigger

> Activation role/facet describing the occurrence or establishment of the activation basis through which an applicable Conditional Policy becomes eligible to initiate its bounded response.

Use as activation vocabulary, not as a universal standalone entity/root.

## Canonical separations

```text
Conditional Policy != Dependency
Conditional Policy != Criterion / Evaluation
Conditional Policy != Recurrence
Conditional Policy != Temporal Constraint / Schedule
Conditional Policy != Decision / Authority
Conditional Policy != Proposal / Request
Conditional Policy != Actual
Conditional Policy != Reminder / Notification

Trigger != source fact/event/state
Trigger != action/effect
Trigger != universal entity/root
```

## Preferred wording

Prefer:

```text
Conditional Policy
activation basis
policy activates
bounded response
response attempted / proposed / applied
response succeeded / failed
```

Use `Trigger` when discussing the activation role/context.

Avoid ambiguous kernel vocabulary such as:

```text
Rule
Automation
Workflow
Action
Condition
Trigger object
```

unless clearly identified as product/UI/implementation vocabulary or a separately validated specific concept.

## Related terms

```text
Dependency
prerequisite contingency

Criterion
what is evaluated

Evaluation
evaluative result/application

Recurrence
how a pattern repeats

Temporal Constraint
temporal admissibility/requirement/preference

Schedule
accepted temporal assignment

Decision
bounded resolution

Authority
legitimate governance/effect capability

Reminder / Notification
possible downstream response; primitive status not decided here
```

## State/history guardrails

```text
no data != false
no data != true
activation != response success
material policy change != automatic carry-forward
revocation != historical erasure
```

## Multi-Actor guardrails

```text
shared fact + actor-scoped policy
!= duplicate shared reality

shared policy
!= shared Agreement/Consent/Authority/Visibility

AI suggestion
!= policy adoption
```

## Rejected as current kernel roots

```text
Trigger
Condition
Action
Rule
Workflow
Automation
```

This rejection concerns universal roots from this review; specific future concepts may be reviewed independently where evidence warrants it.

Normative references:

- `concepts/conditional-policy.md`;
- `checkpoints/conditional-policy-v0-validation.md`.
