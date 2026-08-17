<!-- LIFEOS-CANONICAL-SPLIT document="README.md" part="3" total="3" -->
> **Canonical document split — Part 3 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](README.md) · [Part 2](README-part-2.md) · **Part 3**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
## Language governance
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


## Validation methodology
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


## Evidence discipline
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


## Accepted clusters
### Cluster 1 — Intention & Execution
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

### Cluster 2 — Time
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

### Cluster 3 — Observed Reality & Evidence
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

### Cluster 4 — Data / Subjects
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


## Active cluster — Relationships / Reasoning
**Status:** IN PROGRESS.

Current accepted candidate baselines:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md)
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

### Current semantic decomposition
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

### Reconciliation / Source Precedence v0
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

The 28-path semantic propagation is complete on the active branch. The accidental out-of-scope technical probe was already removed through its own approved corrective scope. Final branch-level Reconciliation post-write QA is complete; synchronization with `main` remains a separately gated future scope and does not block continued Cluster-5 semantic review.

### Rejected universal primitives so far
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


## Cross-cutting canonical distinctions
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


## Common shared-change sequence
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


## Multi-actor readiness
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


## Current explicit deferred owners
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

A future candidate is selected only through a fresh re-score against the current accepted baseline. The newer Product North Star on `main` has already been reviewed read-only as relevant product evidence — including `Effort != Execution != Outcome != Goal Progress` — but no candidate is preselected and branch synchronization is not a prerequisite for continuing the current Cluster-5 semantic work.

---


## Regression policy
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


## Before persistence
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


## Git / QA discipline
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


## Current position
The active Domain Atlas branch has semantically propagated **Reconciliation / Source Precedence v0** across the exact approved 28-path milestone and the final post-write QA is complete.

Current sequence:

```text
1. preservation-first current-document reconstruction — COMPLETE
2. probe absence + preservation audit — VERIFIED
3. Reconciliation 28-path propagation + post-write QA — PASS
4. fresh-score remaining Relationships / Reasoning candidate space
5. validate the selected candidate with full Methodology v3
6. continue until Relationships / Reasoning candidate space is complete
7. Cluster-5 integration / multi-actor stress / deferred-dependency closure
8. upstream `main` synchronization remains a separate future scope; it is not a prerequisite for the steps above
```

Do not preselect the next candidate before the fresh re-score.

---

# 2026-08-14 — Repository-state correction

The preservation-first reconstruction was completed from pre-write HEAD `0e2f4b621e640421e2d5c9c0dc80fb20ff79b4a0` and QA-closed on the active `feature/domain-model` branch. The accidental technical probe was already removed and QA-closed before that reconstruction. The historical-preservation audit remains intact. Reconciliation semantic propagation and final post-write QA are complete. The current operating decision is to finish Relationships / Reasoning and the required cluster validations before any separately gated synchronization with `main`.

`Relationship v0` remains a checkpoint-backed typed/specific relationship modeling discipline. `docs/domain/concepts/relationship.md` does not exist by design and must not be recreated merely to satisfy navigation symmetry.

---

# 2026-08-15 — Criterion / Evaluation v0 current-state amendment

Criterion / Evaluation v0 is now part of the accepted Relationships / Reasoning semantic baseline.

Normative concept and validation checkpoint:

- [`concepts/criterion-evaluation.md`](concepts/criterion-evaluation.md)
- [`checkpoints/criterion-evaluation-v0-validation.md`](checkpoints/criterion-evaluation-v0-validation.md)

Current semantic verdict:

```text
CRITERION / EVALUATION v0
PASS WITH HARDENING

Criterion
✅ canonical contextual evaluative specification/capability

GoalCriterion
✅ Criterion applied/scoped to a Goal
❌ separate universal primitive/root

Evaluation
✅ contextual reasoning/process-result semantics
✅ may be reconstructed/materialized where consequence requires
❌ universal entity/root/workflow

Goal Progress
✅ derived/evaluative projection
❌ universal stored percentage/status

REOPEN       0
unclassified 0
```

The current Cluster-5 decomposition is extended with:

```text
Under which applicable rule should this bounded target be evaluated,
using which relevant Evidence and material states,
and what assessment follows for this evaluation context?
→ Criterion / Evaluation
```

Canonical cross-cutting additions:

```text
Goal != Criterion
Milestone != Criterion
Criterion != Evidence
Evaluation != Evidence / Actual / Outcome / Decision / Confirmation / Reconciliation
missing Evidence != failed Criterion
multiple Criteria != universal AND / average / score
later Criterion state != retroactive rewrite of historical Evaluation
Goal Progress = derived projection, not universal stored percentage
```

The older `GoalCriterion / evaluation` entry under explicit deferred owners is superseded at the semantic level by this amendment. Remaining explicit deferred space includes:

```text
Proposal / Request reusable identity
Trigger / conditional policy
Verification / comprehension
Collective / Group / quorum / voting
coordination Stewardship
Resource Requirement / Allocation / Reservation
reusable comparator / Range / Threshold value representation
criterion-combination / composite-expression representation
specialist evaluation / adjudication models
Evaluation retention / materialization strategy
per-family material-equivalence rules
exact effective dating
native identity merge/split/deduplication
per-domain/specialist source-precedence policies
Principal/AuthN/AuthZ/enforcement
retention/audit/privacy
logical/physical/API/sync representation
```

Current sequence after Criterion / Evaluation propagation QA:

```text
1. preservation-first current-document reconstruction — COMPLETE
2. probe absence + preservation audit — VERIFIED
3. Reconciliation propagation + post-write QA — PASS
4. Criterion / Evaluation v0 semantic validation — PASS WITH HARDENING
5. Criterion / Evaluation current-state propagation — completed by the approved corrective scope; QA required before milestone closure
6. fresh-score remaining Relationships / Reasoning candidate space
7. validate one selected candidate with full Methodology v3
8. continue until candidate space is complete
9. Cluster-5 integration / dedicated multi-actor stress / deferred-dependency closure
10. upstream `main` synchronization remains separately gated and is not a prerequisite
```

No next candidate is preselected by this amendment. `docs/domain/concepts/relationship.md` remains absent by design.