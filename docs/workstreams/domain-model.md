# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch

## Purpose

Turn LifeOS product requirements into an implementation-ready domain model without prematurely designing every specialist module, collaboration feature or final SQL table.

Earlier product terminology is evidence, not automatic truth. Concepts are revalidated through scenarios, external benchmark/research, adversarial tests and cross-cluster consistency.

**Accepted means current best decision, not immutable decision.**

---

# Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/language-map.md`](../domain/language-map.md)
5. [`../domain/validation-methodology-v2.md`](../domain/validation-methodology-v2.md)
6. [`../domain/validation-methodology-v2-multi-actor-addendum.md`](../domain/validation-methodology-v2-multi-actor-addendum.md)
7. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
8. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
9. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
10. [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md)
11. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
12. accepted concept specs under [`../domain/concepts/`](../domain/concepts/)
13. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
14. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
15. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
16. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
17. accepted DB/architecture ADRs.

The old V1 glossary remains historical/product evidence. Current kernel terminology is defined by the Domain Atlas + Language Map.

---

# Operating rules

- Revalidate concepts one at a time.
- Do not inherit terminology by inertia.
- Keep external standards/products as evidence, not design authorities.
- Preserve planned/current/actual/history distinctions.
- Preserve provenance/source distinctions.
- Do not fabricate historical intention from later relevance.
- Do not create one table/entity per life topic.
- Do not collapse core semantics into arbitrary JSON or one universal graph object.
- Do not let AI inference become confirmed/canonical truth automatically.
- Preserve progressive disclosure: kernel precision must not become UI bureaucracy.
- Apply multi-actor compatibility tests to every future concept where relevant.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run cluster checkpoints and final whole-domain stress before broad persistence implementation.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Cross-Cluster Validation v2    PASS
Multi-Actor Evidence Synthesis PASS WITH HARDENING
```

No current structural reopening is required.

## Intention & Execution

Accepted concepts:

- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone.

Current boundaries:

```text
Goal      -> desired outcome/condition/pattern
Plan      -> pursuit/organization strategy
Activity  -> actionable intended work/behavior
Event     -> occurrence-centred expected happening
Routine   -> repeated behavioral/execution policy
Milestone -> meaningful contextual checkpoint
```

2026-08-11 multi-actor wording hardening:

- Goal no longer assumes one mandatory personal owner/governor in its canonical definition;
- Activity no longer assumes requester/responsible actor/performer are the same user;
- Routine no longer assumes one mandatory performer.

These hardenings preserve the original primitive boundaries.

## Time

Accepted concepts:

- Occurrence;
- Schedule;
- Session;
- Temporal Constraint;
- Recurrence;
- Availability & Capacity.

Current boundaries:

```text
Recurrence   -> how pattern repeats
Occurrence   -> which expected generated instance
Constraint   -> where/when placement allowed/required/preferred
Availability -> when resource capacity may be used
Capacity     -> compatible commitments resource can sustain
Schedule     -> accepted temporal assignment
Session      -> actual bounded execution episode
```

Critical Time invariants retained:

- Schedule != Actual;
- Schedule != Capacity;
- Constraint != Schedule;
- Recurrence != Routine;
- Occurrence identity != timestamp;
- passage of time != completion;
- Event can retain identity/history while current Schedule is absent after postponement/TBD;
- quota recurrence preserves period-frame meaning where required;
- Routine long-horizon progression tends toward Plan when strategy/stages materially change.

---

# Multi-Actor foundation — current state

Current normative reference:

- [`Multi-Actor Readiness v1`](../domain/multi-actor-readiness-v1.md)

Validation record:

- [`Multi-Actor Evidence Synthesis v0`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Earlier v0 readiness docs remain preserved as historical pre-research baseline.

## Core direction

```text
personal-first product
+
multi-actor-ready domain kernel
```

When actors genuinely coordinate around one real object:

```text
shared canonical fact
+
actor-scoped personal state
```

is preferred over per-user semantic copies.

## Non-collapse rules

```text
object identity
!= account
!= participant
!= responsibility
!= performer
!= subject
!= authority
!= visibility
```

Specific current hardenings:

```text
Goal identity       != governor / stakeholder / subject
Plan identity       != coordinator / contributor
Activity identity   != requester / assignee / performer
Event identity      != organizer / participant / response
Routine identity    != performer
Milestone identity  != stakeholder / approver
Occurrence identity != assigned actor
Schedule identity   != participant acceptance / capacity owner
Session identity    != performer count
Constraint identity != authority actor
Recurrence identity != assignment rotation
```

## Evidence-backed additions

Future domain/product work must preserve:

- responsibility richer than one assignee;
- open/claimable responsibility where valid;
- hand-off request distinct from effective accepted transfer where consequence requires it;
- assignment distinct from coordination stewardship/mental load;
- proposal/delivery/acknowledgement/agreement/authority/Actual distinctions where consequence requires them;
- external/partial/assisted participation;
- selective disclosure and private-source-derived projections;
- inference privacy, including AI explanations/tool calls;
- current access/revocation distinct from historical attribution;
- high-conflict ongoing collaboration as distinct from friendly collaboration and simple exit;
- creator/participant/visibility distinct from authority;
- AI effective authority bounded by acting principal/context/policy;
- coordination burden evaluated per actor, not only organizer benefit.

## Not pre-approved

Do not introduce by default:

- Actor/Person tables;
- Team/Organization/Household hierarchy;
- universal Group entity;
- ACL/RBAC/ABAC/ReBAC infrastructure;
- Zanzibar/OpenFGA dependency;
- generic collaboration chat;
- universal workflow/approval engine;
- Stewardship entity;
- AI multi-agent orchestration.

These require dedicated downstream review.

---

# Terminology architecture

Current canonical quick reference:

- [`Domain & Product Language Map`](../domain/language-map.md)

Four terminology layers:

```text
DOMAIN
PRODUCT
UI
IMPLEMENTATION
```

A domain concept is not required to appear as a visible UI noun, and a familiar UI noun does not automatically create a kernel type.

Important mappings:

```text
Task           -> Activity product/UI term
Project        -> Plan product profile (current direction)
Program        -> Plan product profile (current direction)
Deadline       -> latest-bound Temporal Constraint meaning
Calendar Block -> product/UI representation of temporal/capacity semantics
Occurrence     -> canonical domain concept, usually hidden in simple UI
```

Tracked but not yet canonized terms include Actor, Subject, Resource, Participant, Responsibility, Stewardship, Authority, Visibility and Principal.

---

# Current downstream review space

## Observed Reality & Evidence

Likely topics:

- Actual;
- Outcome;
- Confirmation;
- Observation;
- Evidence;
- Provenance.

Strong multi-actor watchpoints:

- Actual performer/participant attribution;
- conflicting reports;
- assisted-user provenance;
- acknowledgement vs confirmation vs Actual;
- external authority;
- evidence uncertainty.

## Data / Subjects

Likely topics:

- Register;
- Quantity;
- Asset;
- Subject;
- Person/Actor boundary;
- Resource.

Strong multi-actor watchpoints:

- Account != Person/Actor;
- Actor != Subject;
- Actor may sometimes be schedulable Resource but concepts are not synonyms;
- non-LifeOS people/subjects must remain representable.

## Relationships / Reasoning

Likely topics:

- Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal relationships;
- Evidence/Criterion relationships;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal.

Strong evidence indicates typed/directional semantics will likely be necessary; one universal semantic-free `related_to` is insufficient.

Cluster membership/naming remain provisional until concept review.

---

# Current conceptual topology

```text
Goal
↓ optional
Plan
↓ optional
Routine / Activity / Event / Milestone
↓ where recurring
Recurrence -> Occurrence

Temporal Constraints
Availability / Capacity
existing commitments
        ↓
feasibility evaluation
        ↕
Schedule
        ↓
Session where executable episode exists
        ↓
Actual / Outcome / Evidence   (future review)
```

This is not a mandatory parent/child chain and not a persistence schema.

Multi-actor relationships cut across this topology rather than forming a second duplicate domain model.

---

# Reopen watchlist

Explicit future boundary tests:

- Milestone vs Outcome vs GoalCriterion;
- Plan vs Routine under complex progression;
- Session vs broader Actual;
- Event participation vs personal commitment/delegation;
- Actual participant/performer attribution;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Person vs Actor vs Subject vs Account/Principal;
- Resource vs Actor;
- Authority vs Visibility vs governance;
- completion-relative Recurrence vs Trigger/relative Constraint;
- typed/directional Relationship vocabulary;
- confirmation/acknowledgement depth by consequence;
- AI Context Builder inference/disclosure boundaries.

These are watch items, not current failures.

---

# Before broad persistence/backend implementation

The full Domain Atlas must eventually establish:

- conceptual model;
- entity/value-object/relationship boundaries;
- identity/invariants;
- actor/context/authority model;
- lifecycle/state distinctions;
- structural + semantic relationship map;
- provenance/confirmation rules;
- AI authority/proposal boundaries;
- logical data model;
- physical PostgreSQL model;
- API contracts;
- backend package boundaries;
- final whole-domain stress result.

Only after the domain is coherent should the first production vertical slice be locked to persistence.

---

# Current task / sequencing

**Do not automatically start the Observed Reality & Evidence cluster.**

Current state:

```text
first two clusters validated
multi-actor evidence synthesized
canonical terminology architecture established
next cluster not yet selected
```

Continue user-led architecture/product questions and additional tests, or explicitly select the next Domain Atlas cluster when ready.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- multi-actor discovery/research from PR #6 is already merged into the domain branch through merge commit `08595f9526e08db53d9b446b8a7a76cd46adcd55`;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream.

Do not duplicate the multi-actor evidence documents or create a parallel terminology tree. Continue from the current Domain Atlas + Language Map + v1 readiness baseline.