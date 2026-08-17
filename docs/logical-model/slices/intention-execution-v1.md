# LifeOS Logical Model — Slice B: Intention / Execution v1

**Status:** accepted candidate baseline pending checkpoint remote QA  
**Date:** 2026-08-17  
**Slice:** B — Intention / Execution  
**Authority:** accepted Domain Atlas > Product North Star > ADR-007 > Domain→Logical readiness contract > Logical Model methodology > current external evidence

---

## 1. Purpose

Slice B defines the logical representation contract for LifeOS intention/execution semantics without collapsing the accepted Domain owners into a universal work-item, workflow, status or desired-state abstraction.

This slice covers the logical pressure around:

- Possibility;
- Goal;
- Plan;
- Activity;
- Event;
- Routine;
- Milestone;
- Proposal;
- Request;
- Decision;
- Dependency;
- relevant Conditional Policy interaction;
- material-state/version pressure required to preserve intention/execution history;
- links to later Time/Reality, Evidence/History and Multi-Actor slices.

It does **not** choose SQL tables, ORM inheritance, event sourcing, API resources, runtime workflow engines or physical indexing.

---

## 2. Core conclusion

The selected logical direction is the **Layered Typed Intention & Execution Model**.

The name describes a representation strategy only. It does not introduce a new Domain superclass named `Intention`, `Execution`, `WorkItem`, `WorkflowNode` or equivalent.

Canonical logical separation:

```text
SEMANTIC OWNER
!= MATERIAL STATE / VERSION
!= TYPED LINK / SEMANTIC ACT
!= SCHEDULE / OCCURRENCE / EXECUTION
!= ACTUAL
!= OUTCOME
!= DERIVED OPERATIONAL STATUS
```

Shared logical mechanisms may support multiple owners, but shared mechanism does not imply shared ontology or lifecycle.

---

## 3. Rejected universal hierarchy

LifeOS must not model the current kernel as:

```text
Possibility -> Goal -> Plan -> Activity -> Event -> Milestone
```

or as one generic row with:

```text
work_item
- kind
- status
- parent_id
```

Accepted Domain boundaries remain authoritative:

```text
Possibility != Goal
Goal != Plan
Plan != Activity
Activity != Event
Routine != Recurrence
Milestone != Goal / Event / Outcome / Activity
Proposal != Request != Decision
Dependency != hierarchy / containment / pure temporal order
```

Any physical/common mechanism must preserve those distinctions in reverse mapping.

---

## 4. Owner dispositions

### 4.1 Possibility

Logical role:

```text
persistent candidate future before intentional adoption
```

Disposition:

```text
LR-01 native identity-bearing logical record when persistently retained
```

Required behavior:

- may be created by user, system, AI or external evidence subject to provenance;
- may be explored/evaluated/ranked without becoming a Goal;
- may remain indefinitely unadopted;
- may be dismissed without becoming a negative preference automatically;
- may later lead to a distinct Goal;
- later Goal abandonment does not retroactively demote the historical Goal back into only a Possibility.

Canonical transition barrier:

```text
Possibility P1 retained
        ↓ later intentional adoption
Goal G1 established

P1 != G1
pre-adoption history != Goal history
```

Retyping the same logical row from Possibility to Goal is rejected.

### 4.2 Goal

Logical role:

```text
persistent intentionally adopted desired outcome / condition / change / pattern
```

Disposition:

```text
LR-01 native identity-bearing logical record
```

Required behavior:

- may exist without a prior persisted Possibility;
- may exist without a Plan;
- may be supported by zero, one or many Plans;
- one Plan may support multiple Goals;
- Goal pursuit/disposition remains distinct from Evaluation, progress, Outcome and evidence;
- Goal history is not rewritten when supporting Plans are revised/replaced.

### 4.3 Plan

Logical role:

```text
persistent revisable execution strategy / coordination structure
```

Disposition:

```text
LR-01 native identity-bearing logical record
```

Required behavior:

- may support no explicit Goal, one Goal or many Goals;
- may coordinate Activities, Milestones, Dependencies, Routines, constraints, policies and resource semantics without becoming a universal workflow graph;
- temporal horizon != Schedule occupation;
- ordinary operational edits do not automatically create a new Plan identity;
- materially different execution strategy may justify a linked replacement/continuation Plan identity;
- past Actual/history remains attached to the Plan/material state that governed it.

### 4.4 Activity

Logical role:

```text
directly executable intended work / behavior unit
```

Disposition:

```text
LR-01 native identity-bearing logical record when persistent independent identity is required
```

Required behavior:

- may exist standalone without Goal or Plan;
- may be coordinated by a Plan without being a child identity of the Plan;
- may be scheduled without becoming Event;
- Activity != Actual, Outcome, Contribution, Responsibility, Participation or Coordination Stewardship;
- completion UI must not erase planned-versus-actual distinctions.

### 4.5 Event

Logical role:

```text
occurrence-centred expected/meaningful event semantics
```

Disposition:

```text
LR-01 native identity-bearing logical record when persistent independent event identity is required
```

Required behavior:

- Event != Activity;
- Event != Schedule;
- elapsed Event/Schedule does not establish Actual automatically;
- postponement/cancellation/disposition remains distinct from concrete accepted Schedule assignment and later Actual.

Detailed Schedule/Occurrence/Session/Actual representation remains Slice C.

### 4.6 Routine

Logical role:

```text
persistent intended recurring execution / behavioral policy
```

Disposition:

```text
LR-01 native identity-bearing logical record
```

Required behavior:

- Routine != Recurrence rule;
- Routine != generated Occurrence;
- Routine != one recurring Activity row whose date is repeatedly moved forward;
- one skipped/missed occurrence does not pause/retire the Routine;
- later Slice C must preserve which Routine/material policy generated or governed each material occurrence where required.

### 4.7 Milestone

Logical role:

```text
meaningful persistent contextual checkpoint within a Goal/Plan context
```

Disposition:

```text
normally LR-02 dependent semantic record, persistently addressable where required
```

Required behavior:

- contextual persistence does not make Milestone a universal native referent superclass;
- date passage does not automatically establish attainment;
- Activity completion/Event occurrence does not automatically establish attainment;
- attainment/progress may depend on explicit criterion/evaluation/evidence semantics.

### 4.8 Proposal

Logical role:

```text
bounded proposing act/content that may be considered/responded to without being effective state
```

Disposition:

```text
LR-02 conditionally materialized semantic record
```

Materialize when independent lifecycle/reference/history matters, including async review, multi-actor response, counter-proposal, withdrawal/expiry/supersession, version binding, authority, rationale or material consequence.

Do not require a standalone Proposal record for every trivial synchronous suggestion when no independent semantic lifecycle exists.

### 4.9 Request

Logical role:

```text
bounded directed ask/solicitation for action, information, change or response
```

Disposition:

```text
LR-02 conditionally materialized semantic record
```

Request acknowledgement/response/fulfilment remain distinct from Actual or target-state mutation unless the owning semantics establish those effects.

An explicit user request may itself supply the required bounded authority/intention for the action actually requested; LifeOS must not manufacture a gratuitous approval ceremony.

### 4.10 Decision

Logical role:

```text
bounded resolution among applicable alternatives / questions
```

Disposition:

```text
LR-02 conditionally materialized semantic record
```

Required behavior:

```text
Decision != target mutation
Decision != Outcome
Decision != Approval flag
```

A Decision may produce zero, one or many effects. A rejection or decision-to-keep-current-state remains a real Decision even when no target mutation occurs.

Conversely, an effective change may occur under a previously authorized Conditional Policy without manufacturing a new Decision for every mutation.

### 4.11 Dependency

Logical role:

```text
specific directional contingency between bounded target states/results/transitions
```

Disposition:

```text
LR-03 typed association / relation record
```

Dependency is not:

```text
parent-child hierarchy
containment
pure before/after order
Schedule
Trigger
Criterion
Resource Requirement / Allocation
Actual
universal DAG edge
```

Current `blocked`, `satisfied`, `eligible` or similar operational views are normally derived from the Dependency plus relevant target/prerequisite state, not independent canonical truth fields.

Cycles may be represented and diagnosed; no universal DAG invariant is imposed.

---

## 5. Material state and version contract

Slice B requires a distinction between continuing owner identity and materially applicable state/revision.

```text
owner identity
!= material state / version
```

The exact Version storage mechanism remains Slice D, but Slice B requires the later mechanism to support at least:

- reconstruction of material Goal/Plan/Activity/Routine/Proposal/Request/Decision state where relevant;
- explicit supersession/correction/revision history;
- effective applicability boundaries where later execution depends on a prior state;
- addressability of the reviewed/approved target state when material;
- no silent overwrite of consequential past intention/strategy.

### 5.1 Plan revision versus replacement

```text
minor/ordinary operational edit
!= automatic new Plan identity

materially different execution strategy
may justify linked replacement / continuation Plan
```

No mechanical field-count threshold is introduced.

A replacement preserves predecessor history and does not rewrite past Actual or previous Plan semantics.

### 5.2 Version-bound proposal/decision

Where the content under review can materially change:

```text
Proposal P1 -> target material state V3
Decision D1 -> resolves P1 / V3
later V4 materially differs
D1 does not automatically approve V4
```

Material-equivalence rules determine whether a prior Decision remains applicable. Exact Version mechanics remain Slice D.

---

## 6. Lifecycle discipline

LifeOS must not define one universal lifecycle enum across intention/execution owners.

Rejected universal form:

```text
DRAFT | ACTIVE | PAUSED | DONE | CANCELLED
```

Instead, each owner preserves its own material lifecycle/disposition dimensions.

Examples:

```text
Goal pursuit/disposition
!= Evaluation / progress / Outcome

Plan operational disposition
!= material Plan content/version

Activity intended execution state
!= Actual
!= Outcome

Event disposition
!= Schedule
!= Actual occurrence

Routine lifecycle
!= individual occurrence disposition
!= adherence

Possibility posture
!= Goal adoption
!= preference

Proposal / Request applicability/response
!= Decision
!= effect

Decision resolution
!= target effect

Dependency definition/history
!= current blocked/satisfied projection
```

Product/UI may expose a simplified status projection when useful. That projection is not a universal canonical semantic field.

---

## 7. Definition / instance / execution separation

Slice B adopts the structural principle:

```text
definition / policy / strategy
!= material revision
!= generated or expected instance
!= execution
!= Actual
```

This applies especially to Plan, Routine and Conditional Policy pressure.

A later execution/Occurrence may need to retain which material Plan/Routine/Policy state governed it. Slice C owns occurrence/execution shape; Slice D owns version/history mechanics.

---

## 8. AI and user-authority boundary

Canonical rules:

```text
AI-discovered candidate != user Goal
AI-ranked candidate != adoption
AI-generated Plan details != established user preference/fact automatically
AI Proposal != Decision
```

However:

```text
explicit user request
may itself authorize the bounded requested action
```

LifeOS must not force redundant approval records merely because AI participated.

Material autonomous actions still require the applicable Authority/Consent/Policy semantics from later governance/runtime layers.

---

## 9. High-value logical queries

The accepted representation must support at least:

1. which Possibilities were retained but never adopted as Goals?
2. which Goal arose from a prior Possibility, without rewriting pre-adoption history?
3. which Plans currently support a Goal, and which Plans supported it at time T?
4. what Plan materially governed a period/occurrence at time T?
5. which Plan replaced/continued another without changing Goal identity?
6. which Activities are standalone versus coordinated by a Plan?
7. which Events/Routines/Activities are currently expected without claiming they actually happened?
8. which Proposal/Request/Decision concerned which material target state/version?
9. what was proposed, what was decided and what effect actually followed?
10. which Decisions produced no target change?
11. which effective changes came from an authorized policy rather than a fresh explicit Decision?
12. which Dependencies currently block/permit a target, derived from present prerequisite state?
13. what Dependency was applicable historically when execution diverged from plan?
14. which Milestones are pending/attained and on what evaluative basis?
15. can a simple standalone Activity remain compact without Goal/Plan/Proposal scaffolding?

---

## 10. Falsification summary

Rejected mutations include:

```text
Possibility retyped into Goal
universal status enum
universal parent_id hierarchy
Plan collapsed into Activity
Activity collapsed into Event
recurring Activity identity moved forward forever
Proposal acceptance mutates Proposal into target
Request fulfilled implies Actual
Decision disappears into target transition
every mutation creates Decision
approval survives material target-state change
replacement strategy overwrites old Plan
Milestone attained by date passage alone
Dependency represented as hierarchy/order
canonical stored blocked=true
mandatory record for every tiny Proposal/Request/Decision
never materialize Proposal/Request/Decision
universal full event replay required for current state
provider lifecycle becomes canonical owner lifecycle
AI candidate becomes canonical Goal/Plan automatically
```

No mutation exposed a Domain-level contradiction in the selected candidate.

---

## 11. Candidate comparison

### Candidate A — universal WorkItem / IntentItem

**Verdict:** logically rejected.

Reason: false superclass, generic lifecycle, retyping pressure, hierarchy ambiguity and generic metadata/status escape hatch.

### Candidate B — completely owner-specific representation

**Verdict:** viable strong alternative.

Reason retained: strongest local semantic/FK specificity.

Why not selected as full logical baseline: repeats shared addressability/history/material-state mechanics unnecessarily. May remain a Physical Model ingredient.

### Candidate C — Layered Typed Intention & Execution Model

**Verdict:** preferred logical candidate.

Shape:

```text
typed semantic owner
+ owner-specific material state/version
+ typed links / semantic acts
+ selective materialization
+ history / lineage
+ derived projections
```

### Candidate D — universal command/event-sourced model

**Verdict:** rejected as logical requirement.

Event sourcing may still be a later physical technique in bounded areas; it is not LifeOS semantic ontology.

### Candidate E — universal desired spec/current status

**Verdict:** rejected universally.

LifeOS adopts the useful principle `intended != actual`, not a universal controller metamodel.

---

## 12. Cross-slice dependencies

### Slice A — Identity / Reference

Slice B reuses Slice-A NativeRef/Reference Contracts without creating a universal Entity/Thing root.

Persistent addressability of a dependent semantic record does not by itself promote it to native Domain identity.

### Slice C — Time / Reality

Must preserve:

```text
Routine != Recurrence != Occurrence
Activity/Event expected state != Schedule != Session != Actual
```

### Slice D — Evidence / Knowledge / History

Must supply exact material Version/history/provenance mechanics required by this slice.

### Slice E — Resources / Values / Capacity

Resource/Requirement/Allocation pressure may affect Plan/Activity feasibility without becoming intention/execution identity.

### Slice F — Relationships / Multi-Actor / Governance

Must preserve Proposal/Request/Decision actor roles, Authority, Responsibility, Participation, Visibility and selective disclosure without retyping the Slice-B owners.

---

## 13. Physical deferrals

The following remain intentionally deferred:

```text
exact PostgreSQL table split
single-table vs per-owner vs hybrid physical persistence
exact Version table/history mechanism
event-sourcing usage, if any
native key type/generation
ORM mapping
API resource/envelope shape
query/index strategy
runtime workflow/orchestration engine
runtime authorization enforcement
exact Occurrence/Schedule/Session/Actual persistence
```

Deferral is safe only if the later physical design preserves this logical contract.

---

## 14. Slice-B acceptance contract

Slice B may be declared active only after:

```text
canonical slice document written
validation checkpoint written
external benchmark record written
traceability ledger updated
decision/assumption register updated
test corpus updated
representation framework updated
workstream updated
exact remote compare/readback passes
main remains unchanged
```

Until that QA succeeds, this document records the accepted candidate but not final remote closure.
