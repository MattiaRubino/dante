# LifeOS Domain Atlas

**Status:** Active design authority for the LifeOS core domain model  
**Current workstream:** [`../workstreams/domain-model.md`](../workstreams/domain-model.md)  
**Validation standard:** [`validation-methodology-v3.md`](validation-methodology-v3.md)

## Purpose

The Domain Atlas defines the semantic kernel LifeOS must preserve before logical data modeling, PostgreSQL persistence, API contracts, backend packages, or product-specific projections are fixed.

The Atlas is intentionally stricter than ordinary product documentation.

It answers questions such as:

- what has independent semantic identity;
- what is contextual relation/capability;
- what is derived/projection only;
- what is product/UI language rather than kernel truth;
- what history must remain reconstructible;
- where Person, Actor, Account, Subject, Resource, Authority, Visibility, Agreement, Consent, Version, Reconciliation, Evidence, Actual, and other dimensions must remain separate;
- what may be safely deferred to logical/security/specialist design.

The objective is not to maximize ontology size. The objective is the **smallest model that survives reality without losing identity, history, truth, multi-actor separation, privacy, Authority, queryability, extensibility, and simple product usability**.

---

# Product compass

LifeOS is an adaptive personal operating system connecting:

```text
goals / intentions
        ↓
plans / routines / projects
        ↓
real calendar time
        ↓
realistic capacity / constraints
        ↓
observed / confirmed reality
        ↓
progress / outcomes / evidence
        ↓
adaptive future planning
```

Its defining value is not merely recording tasks or events. It is understanding the user's current situation, coordinating competing commitments, preserving history, and adapting future planning under user control.

Product principles inherited by the Domain Atlas:

- personal-first, not enterprise-collaboration-first;
- structurally multi-actor-ready without forcing collaborative UX into V1;
- modules contribute activities, constraints, observations, evidence, progress and context rather than creating semantic silos;
- external providers are optional normalized sources, not ontology authorities;
- AI produces structured proposals/reasoning under Authority/Visibility/privacy constraints rather than unchecked truth or writes;
- kernel precision should normally remain hidden behind simple user-facing language.

The accepted product identity / North Star on `main` may provide product-direction evidence, but this Domain Atlas remains authoritative for kernel terminology and semantic boundaries.

---

# Source authority

When sources conflict, use this order:

1. current main code/migrations/tests/accepted ADRs;
2. current durable product/architecture docs on main;
3. active workstream handoff for scoped unmerged work;
4. other current active-branch files;
5. historical branches/merged PRs/checkpoints;
6. chat/remembered context.

The active workstream may be newer than main **only inside its explicitly scoped unmerged work**. It cannot silently override unrelated current main truth.

---

# Operating rules

Required repository process is defined by:

- [`../development/operating-rules.md`](../development/operating-rules.md);
- [`../development/documentation-and-handoff.md`](../development/documentation-and-handoff.md);
- [`../development/branching-and-environments.md`](../development/branching-and-environments.md).

The workstream handoff is a live `save game`, not an optional summary.

Before any new Git write scope on the active Domain Model branch:

```text
state exact branch
state exact pre-scope commit
state exact path scope
wait for explicit approval
write only approved scope
QA against pre-scope
```

Historical validation/checkpoint records are preserved. Later semantic resolutions are appended as explicit downstream closures rather than silently rewriting what earlier work knew.

---

# Language governance

Canonical terminology authority:

- [`language-map.md`](language-map.md)

Language levels:

```text
DOMAIN
PRODUCT
UI
IMPLEMENTATION
```

Canonical precedence:

1. accepted Domain Atlas concept;
2. Language Map;
3. current validation/checkpoint guardrails;
4. active workstream;
5. current product behavior docs;
6. historical product docs/glossaries;
7. conversation.

A visible UI word is not evidence of a kernel primitive. A domain concept does not require a dedicated UI noun.

---

# Validation methodology

Current standard:

- [`validation-methodology-v3.md`](validation-methodology-v3.md)

Mandatory concept/family flow:

```text
A. evidence + candidate formation
B. CORE 01–13
C. Multi-Actor Compatibility 01–20
D. Cross-Concept Consistency
E. Adjacent Dependency Sweep
→ concept verdict
→ cluster integration only when candidate space is complete
```

Verdicts:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

A `PASS WITH HARDENING` is not accepted until required hardenings are incorporated and re-tested.

A `SAFE DEFERRED` item requires:

- unresolved question;
- why acceptance remains safe;
- explicit owner/stage;
- exact reopening trigger;
- exact tests to rerun.

No material dependency may remain as vague `later` or `TBD` limbo.

---

# Evidence discipline

Preferred discovery/validation order:

1. real-world/persona/scenario first;
2. LifeOS simulation/discovery;
3. independent external benchmark research;
4. synthesis/classification without vocabulary promotion;
5. smallest candidate;
6. formal Methodology v3 validation.

Simulation discipline:

```text
context / actors
→ without LifeOS
→ needs / friction
→ with LifeOS
→ stress / failure / disagreement / refusal / silence / correction
→ improvements / limits
→ reusable capability
```

External standards/products are evidence, not design authority.

Preferred direction:

```text
LifeOS semantics
→ internal model
→ adapters / providers / standards
```

not:

```text
provider standard
→ LifeOS ontology
```

`iCalendar` is specifically not a design basis. It may provide useful evidence where adapting it does not weaken LifeOS semantics.

---

# Accepted clusters

## Cluster 1 — Intention & Execution

**Verdict:** PASS.

Accepted concepts:

- [`concepts/goal.md`](concepts/goal.md)
- [`concepts/plan.md`](concepts/plan.md)
- [`concepts/activity.md`](concepts/activity.md)
- [`concepts/event.md`](concepts/event.md)
- [`concepts/routine.md`](concepts/routine.md)
- [`concepts/milestone.md`](concepts/milestone.md)

Cluster checkpoint:

- [`checkpoints/intention-execution-v0.md`](checkpoints/intention-execution-v0.md)

---

## Cluster 2 — Time

**Verdict:** PASS.

Accepted concepts:

- [`concepts/occurrence.md`](concepts/occurrence.md)
- [`concepts/schedule.md`](concepts/schedule.md)
- [`concepts/session.md`](concepts/session.md)
- [`concepts/temporal-constraint.md`](concepts/temporal-constraint.md)
- [`concepts/recurrence.md`](concepts/recurrence.md)
- [`concepts/availability-capacity.md`](concepts/availability-capacity.md)

Cluster checkpoint:

- [`checkpoints/time-v0.md`](checkpoints/time-v0.md)

---

## Cluster 3 — Observed Reality & Evidence

**Verdict:** PASS.

Accepted concepts:

- [`concepts/actual.md`](concepts/actual.md)
- [`concepts/outcome.md`](concepts/outcome.md)
- [`concepts/observation.md`](concepts/observation.md)
- [`concepts/confirmation.md`](concepts/confirmation.md)
- [`concepts/evidence.md`](concepts/evidence.md)
- [`concepts/provenance.md`](concepts/provenance.md)

Cluster checkpoint:

- [`checkpoints/observed-reality-evidence-v0.md`](checkpoints/observed-reality-evidence-v0.md)

Canonical cluster hardenings include:

```text
reported/asserted reality != established Actual
Milestone attainment = Evidence/evaluation-backed checkpoint state
source != truth
Correction != silent rewrite
```

---

## Cluster 4 — Data / Subjects

**Verdict:** PASS WITH HARDENING.

Accepted current concepts/capabilities:

- [`concepts/quantity.md`](concepts/quantity.md)
- [`concepts/subject.md`](concepts/subject.md)
- [`concepts/person.md`](concepts/person.md)
- [`concepts/actor.md`](concepts/actor.md)
- Account boundary through Person/Actor/Account validation
- [`concepts/asset.md`](concepts/asset.md)
- [`concepts/resource.md`](concepts/resource.md)

Rejected universal roots/defaults include:

```text
Register
RegisterEntry
User
ManagedObject
Subject entity/root
Actor entity/root
Resource entity/root
```

Cluster checkpoint:

- [`checkpoints/data-subjects-v0.md`](checkpoints/data-subjects-v0.md)

Cross-cluster checkpoint:

- [`checkpoints/cross-cluster-validation-v4.md`](checkpoints/cross-cluster-validation-v4.md)

Deferred-dependency closure:

- [`checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)

---

# Active cluster — Relationships / Reasoning

**Status:** IN PROGRESS.

Current accepted candidate baselines:

- [`concepts/relationship.md`](concepts/relationship.md)
- [`concepts/responsibility.md`](concepts/responsibility.md)
- [`concepts/participation.md`](concepts/participation.md)
- [`concepts/authority.md`](concepts/authority.md)
- [`concepts/visibility.md`](concepts/visibility.md)
- [`concepts/acknowledgement.md`](concepts/acknowledgement.md)
- [`concepts/decision.md`](concepts/decision.md)
- [`concepts/agreement.md`](concepts/agreement.md)
- [`concepts/consent.md`](concepts/consent.md)
- [`concepts/representation.md`](concepts/representation.md)
- [`concepts/version.md`](concepts/version.md)
- [`concepts/reconciliation.md`](concepts/reconciliation.md)

Current validation checkpoints:

- [`checkpoints/relationship-v0-validation.md`](checkpoints/relationship-v0-validation.md)
- [`checkpoints/responsibility-v0-validation.md`](checkpoints/responsibility-v0-validation.md)
- [`checkpoints/participation-v0-validation.md`](checkpoints/participation-v0-validation.md)
- [`checkpoints/authority-v0-validation.md`](checkpoints/authority-v0-validation.md)
- [`checkpoints/visibility-v0-validation.md`](checkpoints/visibility-v0-validation.md)
- [`checkpoints/acknowledgement-v0-validation.md`](checkpoints/acknowledgement-v0-validation.md)
- [`checkpoints/decision-v0-validation.md`](checkpoints/decision-v0-validation.md)
- [`checkpoints/agreement-consent-v0-validation.md`](checkpoints/agreement-consent-v0-validation.md)
- [`checkpoints/representation-delegation-principal-v0-validation.md`](checkpoints/representation-delegation-principal-v0-validation.md)
- [`checkpoints/version-material-equivalence-v0-validation.md`](checkpoints/version-material-equivalence-v0-validation.md)
- [`checkpoints/reconciliation-source-precedence-v0-validation.md`](checkpoints/reconciliation-source-precedence-v0-validation.md)

## Current semantic decomposition

```text
Who/what acted?
→ Actor

Who is accountable for ensuring the bounded commitment is handled?
→ Responsibility

Who is involved in the shared context, and how?
→ Participation

Who/what may legitimately make a bounded governed effect effective?
→ Authority

What information may be exposed to which recipient/scope/context?
→ Visibility

Who explicitly took notice of this materially specific target/change/request?
→ Acknowledgement

What bounded question was resolved to what result?
→ Decision

Which applicable parties mutually assented to the same materially specific terms?
→ Agreement

Who explicitly permitted which bounded action/use/exposure for which target/scope/purpose/context?
→ Consent

Who actually acted for which distinct represented party in this bounded action/context?
→ Representation / On-Behalf-Of

Which materially relevant state did this semantic act/evaluation concern, and is a later state equivalent for that purpose?
→ Version / Material-State

How are materially competing states/assertions handled under the applicable bounded basis without losing their identity/history?
→ Reconciliation
```

## Reconciliation / Source Precedence v0

Current semantic verdict:

```text
RECONCILIATION / SOURCE PRECEDENCE v0
PASS WITH HARDENING

Reconciliation
✅ canonical cross-cutting reasoning/process capability
✅ may select/combine/correct/supersede/escalate/defer/remain unresolved
✅ preserves competing Version/Provenance/Evidence/Actor/Authority context
❌ universal entity/root
❌ universal truth owner
❌ current-state owner

Source Precedence
✅ bounded contextual policy/basis
❌ global source hierarchy
❌ newest-source/provider/user/organizer always wins

Conflict
✅ valid contextual/derived condition
✅ unresolved conflict is representable
❌ universal entity/root
```

The 28-path semantic propagation is complete on the active branch. Final branch-level QA is intentionally **not yet declared clean** because two separate repository tasks remain outside this approved semantic scope:

1. remove the accidental out-of-scope technical probe file through its own corrective write scope;
2. synchronize the active branch with the newer accepted `main` North Star commit through a separate write scope and re-run semantic freshness/coherence.

This distinction preserves the original Git approval boundary rather than hiding unrelated repository changes inside the Reconciliation milestone.

## Rejected universal primitives so far

```text
Acceptance / Assent
Approval
EffectiveChange / StateTransition
Delegation
Principal as domain primitive
Version root/table
Reconciliation root
Conflict root
SourcePrecedence hierarchy
```

These may still appear as UI language, bounded family semantics, policy records, specialist structures, or implementation helpers where independently justified.

---

# Cross-cutting canonical distinctions

The following must survive the logical/physical model:

```text
Person != Account
Person != Actor
Actor != Account
Actor != Principal
Subject != Actor
Subject != Resource
Asset != Resource

Activity != Event
Routine != Recurrence
Occurrence != Schedule
Schedule != Session
Schedule != Actual
Schedule != Availability / Capacity

Observation != Actual
Observation != Outcome
Observation != Evidence
Evidence != Provenance
Confirmation != Acknowledgement
Confirmation != Authority

Responsibility != Participation
Responsibility != Authority
Participation != Authority
Visibility != Authority
Acknowledgement != Agreement
Acknowledgement != Consent
Decision != Agreement
Decision != Consent
Decision != Authority
Decision != effective target state
Agreement != Consent
Consent != Visibility
Consent != technical Permission
Representation != represented-party authorship
Version != target identity
Version != Provenance
Version != reconciliation
Reconciliation != Decision universally
Reconciliation != current/effective state
Source identity != Source Precedence != Authority != truth
```

---

# Common shared-change sequence

A useful canonical sequence is:

```text
proposed / requested
!= delivered / read / displayed
!= Acknowledgement
!= family-specific response
!= Agreement / Consent where applicable
!= Approval / Decision where applicable
!= applicable Authority/effect validation
!= effective target state
!= Actual
```

Not every workflow uses every stage.

Reconciliation is orthogonal to this sequence: where materially competing states/assertions exist, it may use Evidence/Provenance/Confirmation/Authority/contextual Source Precedence and may culminate in Decision or remain unresolved. A deterministic already-authorized policy may also reconcile a bounded case without fabricating a human Decision.

---

# Multi-actor readiness

Current canonical readiness document:

- [`multi-actor-readiness-v1.md`](multi-actor-readiness-v1.md)

Important personal-first rules:

- multi-actor-ready does not mean V1 collaboration platform;
- external/accountless Persons remain representable;
- one shared fact does not imply one shared perspective;
- Visibility is independent from sharedness and Authority;
- actor-specific Participation, Acknowledgement, Agreement, Consent, Confirmation and Decision state must not be fabricated;
- Representation/on-behalf-of preserves actual Actor separately from represented party;
- conflict may remain unresolved rather than being flattened into fake consensus;
- AI may reason from authorized context but cannot create human common ground or global source precedence.

---

# Current explicit deferred owners

The following remain intentionally open, with owners/reopening triggers in checkpoints:

```text
GoalCriterion / evaluation
Proposal / Request reusable identity
Trigger / conditional policy
Verification / comprehension
Collective / Group / quorum / voting
coordination Stewardship
Resource Requirement / Allocation / Reservation
per-family material-equivalence rules
exact effective dating
native identity merge/split/deduplication
per-domain/specialist source-precedence policies
Principal/AuthN/AuthZ/enforcement
retention/audit/privacy
logical/physical/API/sync representation
```

A future candidate is selected only through a fresh re-score against the current accepted baseline. The new accepted product North Star on `main` is relevant evidence — especially the explicit distinction `Effort != Execution != Outcome != Goal Progress` — but no candidate is preselected before the active branch is cleanly synchronized and Reconciliation QA is actually closed.

---

# Regression policy

Promote genuinely new scenarios only when they expose one or more of:

- identity;
- lifecycle/history;
- multi-actor separation;
- privacy/Authority;
- contradiction/reconciliation;
- performance/scale;
- simple-user versus power-user conflict;
- specialist-system boundary.

Avoid near-duplicate regression cases.

---

# Before persistence

Do **not** jump from accepted concepts directly into SQL.

Required sequence after Relationships / Reasoning candidate space is complete:

```text
Cluster-5 integration
→ Cluster-5 multi-actor stress
→ Cluster-5 deferred-dependency closure
→ whole-domain semantic regression
→ destructive redundancy review
→ deep history/correction review
→ whole-domain multi-actor/privacy/Authority/AI review
→ simple-user regression
→ specialist-system boundary review
→ logical model
→ physical PostgreSQL
→ API contracts
→ backend implementation
```

---

# Git / QA discipline

For every approved milestone:

```text
BRANCH
PRE-SCOPE
EXACT PATH SCOPE
```

must be explicit before write.

Post-write QA checks:

- exact branch/HEAD;
- exact pre-scope compare;
- exact changed paths;
- preservation/history;
- complete Methodology v3 gates/hardenings;
- Language Map/current docs coherence;
- no unclassified dependencies;
- REOPEN count;
- no accidental prototype/SQL/API/auth/backend changes;
- branch ahead/behind current main;
- workstream final marker.

Approval is consumed only after successful write and clean QA.

---

# Current position

The active Domain Atlas branch has semantically propagated **Reconciliation / Source Precedence v0** across the exact approved 28-path milestone.

The next repository actions are deliberately separate from that semantic scope:

```text
1. verify 28 authored paths + only known probe extra
2. obtain separate approval to delete __schema_probe_do_not_create__
3. QA corrective deletion
4. obtain separate approval to sync current main
5. integrate accepted Product North Star commit
6. run semantic freshness/coherence + final Reconciliation QA
7. consume Reconciliation write approval only after that clean result
8. fresh-score remaining Relationships / Reasoning candidate space
```

Until those steps complete, do not claim the branch-level Reconciliation milestone is finally QA-clean and do not preselect the next candidate.