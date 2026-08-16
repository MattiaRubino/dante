# Contribution v0

Status: **PASS WITH HARDENING**

Contribution is a **specific contextual relation family / capability** for actor-scoped, materially meaningful actual input or work within a bounded realization, result or output context.

```text
Actor X
→ Contribution
→ bounded realization / result / output context Y
```

The core question is:

> **What materially meaningful actual input or work did this Actor contribute within this bounded realized context?**

Contribution is not a native entity/root. `Contributor` is a contextual Actor role established by an applicable Contribution relation; it is not a Person subtype, Account identity or universal role object.

## Canonical boundaries

```text
Contribution != Participation
Contribution != Responsibility
Contribution != Coordination Stewardship
Contribution != expected performer
Contribution != Actual performer universally
Contribution != Actual
Contribution != Outcome
Contribution != Provenance
Contribution != Evidence
Contribution != Confirmation
Contribution != credit / recognition / acknowledgement
Contribution != Authority
Contribution != causal blame / merit
Contribution != Goal-support evaluation semantics
```

A specific existing relation remains preferable whenever it fully answers the question. Contribution must not become a generic relationship wrapper or a synonym for “was involved”.

Examples:

```text
Who actually performed this Activity?
→ performer / Actual semantics

Who was accountable for ensuring it was handled?
→ Responsibility

Who carried the ongoing coordination burden?
→ Coordination Stewardship

Who materially contributed work/input to the realized result?
→ Contribution
```

## Actuality requirement

Contribution is grounded in **actual contribution**, not merely intention, assignment, invitation or plan.

Therefore:

```text
intended contribution != Contribution
requested contribution != Contribution
assigned work != Contribution
Participation alone != Contribution
expected performer != Contribution
```

A planned or expected contribution may be represented by its owning planning/relationship semantics. Contribution becomes applicable only when the relevant actual input/work is materially attributable in context.

## Shared reality and actor-scoped attribution

A shared Actual or Outcome may coexist with different actor-specific Contributions.

```text
shared Actual A
shared Outcome O

Actor Anna → Contribution C1
Actor Luca → Contribution C2
Actor Marco → no material Contribution
```

The shared realization/result is not duplicated per contributor, and a Contribution does not become the Outcome itself.

## Performer boundary

An Actual performer may also be a Contributor, but performance and Contribution are not universally equivalent.

A contributor may provide material input without being the final performer; conversely, a nominal performer may not capture every materially meaningful contribution to a realized output.

LifeOS must not manufacture synthetic Activities merely to make all contributions queryable.

## Provenance boundary

Provenance explains lineage of a domain record or material version. Contribution identifies materially meaningful actor input/work in the bounded realized context.

```text
record author / editor provenance
!= Contribution automatically
```

Provenance may support an assertion of Contribution, but it does not establish the semantic relation by itself.

## Evidence / Confirmation boundary

Evidence may support evaluation or assertion of Contribution. Confirmation may attest to a contextual claim. Neither is the Contribution relation itself.

```text
no Evidence != proof of no Contribution
Confirmation != Contribution
```

Conflicting contribution assertions may coexist until reconciled through applicable semantics; no universal newest-source, creator, manager or highest-confidence winner applies.

## Credit, recognition and merit

Contribution does not imply credit, recognition, reward, authorship status, ownership, merit or blame.

```text
Contribution established
!= entitled credit
!= causal responsibility
!= ownership
!= Authority
```

Those semantics require their own applicable relation/policy/specialist model where needed.

## Goal-support language

The phrase “X contributes to Goal Y” can describe evaluative support or causal relevance without meaning Actor Contribution.

Where the question is whether an Activity/Plan/etc. supports a Goal, use Criterion/Evaluation or the specific planning semantics rather than manufacturing Actor Contribution.

## History and correction

Contribution is consequence-sensitive and may require historical reconstruction when attribution mattered.

```text
current understanding != historical assertion
correction != silent overwrite
material context change != automatic carry-forward
```

A later correction may change the current understood Contribution while preserving consequential historical assertions and provenance.

## Multi-Actor semantics

Several Actors may contribute independently to the same bounded context. This does not create a Collective automatically.

A true Collective may also be the relevant Actor-capable bearer where the contribution truthfully belongs to that Collective referent; member Contributions are not inferred from Collective Contribution, and vice versa.

Contribution grants no Visibility, Authority, Responsibility, Coordination Stewardship, Consent or ownership by default.

## AI / automation

AI or system Actors may bear Contribution only where the accepted Actor model and applicable context truthfully support actor-scoped attribution. Technical participation, generation or provenance alone must not fabricate Contribution, human authorship, merit or consent.

## Non-goals

Contribution v0 does **not** establish:

- a universal `Contributor` entity/root;
- a universal `Credit` entity/root;
- a universal contribution taxonomy;
- contribution percentages or shares;
- fairness, merit or ranking scores;
- universal causal attribution/blame;
- financial-contribution semantics;
- specialist authorship, IP or publication-credit semantics;
- SQL/API/persistence shape.

Those remain separately reviewable where explicit reopen triggers are met.

## Canonical result

```text
CONTRIBUTION v0
SPECIFIC CONTEXTUAL RELATION FAMILY / CAPABILITY
PASS WITH HARDENING

Contributor
CONTEXTUAL ACTOR ROLE
NOT NATIVE ENTITY / ROOT
```

Normative validation: `../checkpoints/contribution-v0-validation.md`.
