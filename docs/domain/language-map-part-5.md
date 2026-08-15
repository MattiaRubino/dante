<!-- LIFEOS-CANONICAL-SPLIT document="language-map.md" part="5" total="5" -->
> **Canonical document split — Part 5 of 5.** Parts 1–5 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](language-map.md) · [Part 2](language-map-part-2.md) · [Part 3](language-map-part-3.md) · [Part 4](language-map-part-4.md) · **Part 5**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
## 2. Terminology precedence
When terminology conflicts, apply this order:

1. accepted Domain Atlas concept;
2. this Language Map;
3. current validation/checkpoint guardrails;
4. active workstream handoff;
5. current product-behavior documentation;
6. historical product documents/glossaries;
7. conversation wording.

Historical terminology remains useful evidence but cannot override later accepted semantic boundaries.

---


## 3. Status classes
Terms are classified as:

```text
CANONICAL
DERIVED / PROJECTION
PRODUCT PROFILE
PRODUCT / UI TERM
PROVISIONAL / SAFE-DEFERRED
DEFERRED SPECIALIST / LOGICAL / SECURITY
HISTORICAL / REJECTED
```

These classifications are semantic, not database-table instructions.

---


## 4. Canonical Domain concepts
### Intention & Execution
| Term | Status | Current meaning |
|---|---|---|
| Goal | CANONICAL | desired condition/direction with independent identity and history |
| Plan | CANONICAL | coordinated execution strategy/path supporting one or more intentions |
| Activity | CANONICAL | actionable intention that can be performed/executed |
| Event | CANONICAL | occurrence-centred intention/fact whose temporal occurrence matters intrinsically |
| Routine | CANONICAL | persistent recurring execution/behavior policy |
| Milestone | CANONICAL | contextual meaningful checkpoint on a broader path; attainment must remain evidence/evaluation-backed |

### Time
| Term | Status | Current meaning |
|---|---|---|
| Occurrence | CANONICAL | stable expected/generated instance identity, independent from current Schedule |
| Schedule | CANONICAL | current accepted temporal assignment of a schedulable subject |
| Session | CANONICAL | bounded actual execution episode/slice |
| Temporal Constraint | CANONICAL | rule/bound governing where/when scheduling is allowed, required, bounded or preferred |
| Recurrence | CANONICAL | reusable repeating/generative temporal pattern semantics |
| Availability & Capacity | CANONICAL | schedulable-resource feasibility/ability to accept temporal commitment, distinct from Schedule |

### Observed Reality & Evidence
| Term | Status | Current meaning |
|---|---|---|
| Actual | CANONICAL | contextual established representation of how a specific expectation/intention resolved in reality |
| Outcome | CANONICAL | contextual result/disposition of a specific Actual realization |
| Observation | CANONICAL | persistent contextual measurement/perception/report/simple assertion about a Subject referent |
| Confirmation | CANONICAL | contextual attestation by a confirmer toward a materially specific target/version/purpose |
| Evidence | CANONICAL | contextual evaluative role/use of information bearing on a claim/criterion/checkpoint/Decision/evaluation |
| Provenance | CANONICAL | bounded contextual lineage explaining how a record/material state came to exist or change |

### Data / Subjects
| Term | Status | Current meaning |
|---|---|---|
| Quantity | CANONICAL VALUE SEMANTICS | scalar amount + unit semantics reusable across contexts; not a universal record/entity |
| Subject | CANONICAL CONTEXTUAL ROLE | primary aboutness/referent role over native identities; not a root entity |
| Person | CANONICAL NATIVE IDENTITY | human identity independent from Account, Actor role, Subject role, Resource role, Asset role |
| Actor | CANONICAL CONTEXTUAL ROLE/CAPABILITY | native referent/system acting semantically in context; not universal actor root |
| Account | CANONICAL IMPLEMENTATION/PLATFORM BOUNDARY | LifeOS access/platform identity, distinct from Person/Actor and future Principal |
| Asset | CANONICAL NATIVE IDENTITY FAMILY | persistent physical thing with independent identity/history where materially justified |
| Resource | CANONICAL CONTEXTUAL ROLE/CAPABILITY | referent usable/providing capability/capacity for an Activity/Event/Goal/Plan/context; not universal identity root |

### Relationships / Reasoning
| Term | Status | Current meaning |
|---|---|---|
| Relationship | CANONICAL CONTEXTUAL SEMANTIC FAMILY | typed/contextual semantic relation over native referents/concepts; no universal Relationship root required |
| Responsibility | CANONICAL CONTEXTUAL RELATION/CAPABILITY | accountable-for-bounded-commitment semantics; not ownership/Authority/Participation/Actor identity |
| Participation | CANONICAL CONTEXTUAL RELATION/CAPABILITY | actor involvement in shared Activity/Event/Occurrence/Session/context; actor-specific state/history preserved |
| Authority | CANONICAL CROSS-CUTTING RELATION/CAPABILITY | scoped legitimate governance/effect power for bounded target/action/context; distinct from technical authorization |
| Visibility | CANONICAL CROSS-CUTTING RELATION/CAPABILITY | bounded information-exposure semantics by recipient/scope/context; distinct from Authority and technical permission |
| Acknowledgement | CANONICAL CONTEXTUAL RELATION/CAPABILITY | explicit actor-scoped taking-notice of a specific target/material state/change/request |
| Decision | CANONICAL CONTEXTUAL REASONING FAMILY/CAPABILITY | bounded explicit resolution of a question to a specific result where the resolution itself matters; distinct from Authority/effective state/Actual |
| Agreement | CANONICAL CONTEXTUAL RELATION/CAPABILITY | multi-party mutual assent to materially same terms/version for a bounded context |
| Consent | CANONICAL CONTEXTUAL RELATION/CAPABILITY | actor-scoped bounded permission for action/use/exposure concerning a target under defined scope/purpose/context where Consent applies |
| Representation / On-Behalf-Of | CANONICAL CONTEXTUAL RELATION/CAPABILITY | actual Actor acts for a distinct represented party in a bounded action/context; preserves actual Actor, represented party and basis separately |
| Version / Material-State | CANONICAL CROSS-CUTTING CAPABILITY/DISCIPLINE | identifies/reconstructs materially relevant target state and purpose-specific material equivalence; distinct from identity, Provenance, technical revision and reconciliation |
| Reconciliation | CANONICAL CROSS-CUTTING REASONING/PROCESS CAPABILITY | handles materially competing states/assertions under a bounded context/basis while preserving Version/Provenance/Evidence/Actor/Authority; may resolve, combine, correct, defer, escalate or remain unresolved; does not own current state or objective truth |
| Source Precedence | CANONICAL BOUNDED POLICY/BASIS | contextual rule/basis that may influence Reconciliation for a specific target/facet/purpose/context/time; never a universal global source ranking |
| Conflict | DERIVED / CONTEXTUAL CONDITION | material incompatibility/competition among otherwise preserved states/assertions; may remain unresolved and is not a universal root/entity |

---


## 5. Derived / projection semantics
The following are meaningful but are usually derived from stronger source semantics rather than independent kernel identity by default.

| Term | Status | Derivation / boundary |
|---|---|---|
| Tracker / History / Progress view | DERIVED / PROJECTION | queries native records such as Observation, Actual, Outcome, Session and future domain records; not source truth |
| Busy / Free | DERIVED / PROJECTION | derived from Availability/Capacity/Schedule/participation/policy context; not universal stored truth |
| Moved earlier / later | DERIVED | Schedule revision comparison |
| Overrun / underrun | DERIVED | Schedule vs Session/Actual comparison |
| Awaiting confirmation | DERIVED WORKFLOW STATE | required Confirmation absent under applicable policy |
| Approval requirements satisfied | DERIVED / POLICY STATE | policy/Decision/Authority evaluation; not universal `approved=true` |
| Current effective availability | DERIVED | Availability/Capacity + constraints + accepted commitments + policy |
| Goal progress | DERIVED / EVALUATION | Evidence/Actual/Outcome/Milestone/criterion semantics; no automatic universal percentage |
| Conflict detected | DERIVED / CONTEXTUAL CONDITION | two or more material states/assertions are incompatible for the bounded question/facet; detection does not imply resolution |
| Current reconciled interpretation | DERIVED / OWNED STATE | result established by the affected domain concept under applicable Reconciliation/Authority/Decision/policy; not owned by Reconciliation itself |

---


## 6. Product profiles / product capabilities
These may be durable product structures/configuration without becoming native domain truth.

| Term | Status | Current meaning |
|---|---|---|
| Register | PRODUCT PROFILE / VIEW | saved longitudinal configuration/view over native records; universal Register primitive rejected |
| Calendar Block | PRODUCT / UI PROFILE | user-facing time/capacity representation; must not wrap/duplicate every temporal object |
| Life Area | PRODUCT PROFILE / CLASSIFICATION | organizational lens/classification, not current kernel primitive |
| Temporary Mode | PRODUCT CAPABILITY / PROVISIONAL | bounded temporary adaptation across planning/routine/capacity/context; not yet validated as kernel concept |
| Inbox | PRODUCT / UI | capture/review queue; not domain source identity by itself |
| Weekly Review | PRODUCT WORKFLOW | review/evaluation surface over domain records |
| Shared Plan / shared context | PRODUCT CAPABILITY | collaboration projection/workflow over accepted multi-actor-ready kernel semantics |

---


## 7. Explicitly rejected kernel defaults
The following must **not** be introduced as universal kernel primitives merely because they are convenient nouns or implementation abstractions:

```text
Universal User root
Universal Subject entity/root
Universal Actor entity/root
Universal Resource entity/root
Universal Relationship entity/root
Universal Participant/Participation root table
Universal Responsibility root table
Universal Authority entity/root
Universal Visibility/ACL root
Universal Acceptance / Assent primitive
Universal Approval primitive
Universal Reconciliation entity/root
Universal Conflict entity/root
Universal SourcePrecedence hierarchy/table
Universal EffectiveChange / StateTransition root
Universal Delegation primitive/root
Universal Principal as LifeOS domain primitive
Universal Version entity/root/table
Universal Register / RegisterEntry primitive
Universal ManagedObject root
Universal Fact / Reality / EvidenceRecord mega-object
Universal Permission object
Universal Attestation root
Universal Contract/legal-consent engine
Universal globally linear history
Universal last-write-wins / newest-source-wins / provider-always-wins / user-always-wins
```

These may exist later as implementation helpers, specialist concepts, qualified relations, policy records, projections, or domain-specific structures only when independently justified.

---


## 8. Critical non-equivalences
The following distinctions are canonical and must survive logical/persistence/API design:

```text
Person != Account
Person != Actor
Actor != Account
Actor != Principal
Subject != Actor
Subject != Account
Subject != Resource
Asset != Resource
Resource role != provider identity

Activity != Event
Routine != Recurrence
Occurrence != Schedule
Schedule != Actual
Schedule != Session
Schedule != Availability / Capacity
Temporal Constraint != Schedule

Observation != Actual
Observation != Outcome
Observation != Evidence
Evidence != Provenance
Confirmation != Evidence
Confirmation != Authority

Relationship != universal entity/root
Responsibility != Participation
Responsibility != Authority
Participation != Authority
Visibility != Authority
Acknowledgement != Confirmation
Acknowledgement != Agreement
Acknowledgement != Consent
Decision != Agreement
Decision != Consent
Decision != Authority
Decision != effective target state
Agreement != Consent
Consent != Visibility
Consent != technical Permission
Representation != Decision / Agreement / Consent / Participation / Responsibility / Authority
actual Actor != represented party by default
Principal != semantic Actor

Version != target identity
Version != Provenance
Version != Decision / Authority / reconciliation
semantic Version != technical/provider/storage revision
material equivalence != universal byte/field equality

Reconciliation != Decision universally
Reconciliation != Authority
Reconciliation != Version
Reconciliation != Provenance
Reconciliation != Evidence
Reconciliation != Actual/current state
Source identity != Source Precedence != Authority != truth
conflict detected != conflict resolved
unresolved conflict != error by definition
```

---


## 9. Common-ground / governance sequence
A useful canonical sequence for shared changes is:

```text
proposed / requested
!= delivered / read / displayed
!= Acknowledgement
!= family-specific response
!= Agreement or Consent where applicable
!= Approval / Decision where applicable
!= Authority/effect validation
!= effective target state
!= Actual
```

Not every workflow uses every stage.

A deterministic authorized process may move from policy/condition to an effective state without fabricating a human Decision, Agreement, Consent or Confirmation.

Reconciliation is orthogonal to that sequence: when materially competing states/assertions exist, Reconciliation may use Evidence, Provenance, Confirmation, Authority and contextual Source Precedence and may culminate in Decision or remain unresolved. Reconciliation never rewrites the sequence into one generic `accepted/resolved=true` state.

---


## 10. History / correction discipline
Canonical rules:

```text
current != historical
correction != silent rewrite
re-observation != correction
state change != new identity automatically
material target change != automatic carry-forward of prior Ack/Confirmation/Agreement/Consent/Decision/response
technical revision != semantic material change
```

When conflict/reconciliation occurs:

```text
competing assertions/states remain attributable
Reconciliation may establish a later current/effective interpretation
prior assertions/resolutions remain historical facts
Source Precedence must be bounded and explainable
```

Where consequence warrants it, Version/Provenance/Decision/Authority/owning concept semantics must preserve the material basis needed for reconstruction.

---


## 11. AI language boundary
AI may propose, summarize, rank, infer, detect conflict, discover candidate Evidence, suggest reconciliation, or prepare a Decision.

AI must not silently manufacture:

```text
human Acknowledgement
human Confirmation
human Agreement
human Consent
human Decision
Authority
objective truth
universal source precedence
current state merely from confidence
```

A bounded system/AI process may produce an effect only under explicit applicable policy/Authority and truthful attribution.

---


## 12. Provider / interoperability language boundary
External provider nouns and identifiers are integration evidence, not LifeOS ontology authority.

Canonical direction:

```text
LifeOS semantics
→ internal model
→ provider/standard adapter
```

not:

```text
provider/standard schema
→ LifeOS ontology
```

Examples:

```text
provider event ID != Event identity
provider person/contact ID != Person identity
provider revision != semantic Version automatically
ETag/MVCC != semantic Version
provider role/title != Authority automatically
provider source != truth automatically
```

---


## 13. Deferred specialist / logical / security terms
The following remain deliberately outside the current canonical kernel unless/until separately validated:

```text
GoalCriterion / evaluation model
Trigger / conditional policy
Verification / comprehension
Proposal / Request reusable identity
Collective Actor / Group / quorum / voting
Organization identity
Place / Location / Property identity
Document / Artifact identity
FinancialAccount / service/subscription identity
living-entity identity
Principal/AuthN/AuthZ details
Credential
Audit/security history
retention/anonymization classes
Resource Requirement
Allocation
Reservation / Capacity Claim
inventory/supply/consumption
per-family material-equivalence rules
exact effective dating
native identity merge/split/deduplication
per-domain/specialist source-precedence policies
physical reconciliation/sync/CRDT strategy
```

These are explicit future owners/dependencies, not silent omissions.

---


## 14. UI wording rules
UI may use ordinary language even when the kernel is more precise.

Examples:

```text
UI: Accept
```

may map to:

- Participation response;
- Responsibility hand-off response;
- proposal/effect application;
- Agreement assent;
- another family-specific operation.

It does **not** justify a universal Acceptance entity.

```text
UI: Confirm
```

may map to Confirmation, Acknowledgement, review, or another bounded action depending on context; labels must not collapse semantics.

```text
UI: Resolve conflict / Use this version
```

may invoke Reconciliation or a bounded Decision/effect but does not create a universal Reconciliation/Conflict object.

Simple user-facing language should remain natural while advanced/history views may expose source, version, actor, authority and reconciliation basis where authorized.

---


## 15. Product terminology guardrails
Product documentation may keep historical/useful nouns such as:

```text
Register
Tracker
Calendar Block
Owner
Assigned
Shared
Accepted
Confirmed
Resolved
```

but must not silently promote them into domain primitives.

Where old product docs conflict with the current Domain Atlas, update only current durable docs that have become misleading. Preserve historical evidence/checkpoints so the project remains reconstructible.

---


## 16. Persistence guardrails derived from language
The Language Map does not dictate tables, but it prohibits semantic shortcuts such as:

```text
persons.id = accounts.id
actor_id = user_id everywhere
subject_id points only to users
resource_id implies native Resource root
visibility_acl = source of domain Visibility truth without review
permission row = domain Authority
accepted boolean = Agreement/Consent/Decision/Participation interchangeably
latest row wins = canonical Reconciliation
updated_at/ETag = semantic Version
provider source rank = universal Source Precedence
```

Logical modeling must preserve the accepted distinctions first, then choose the smallest queryable persistence structure that survives them.

---


## 17. Reopening rule
A canonical term may be reopened only when stronger semantic evidence shows one of the following:

- identity/history cannot be preserved;
- ordinary workflows become unnatural or impossible;
- a neighboring concept fully absorbs it without information loss;
- multi-actor/privacy/Authority boundaries fail;
- implementation pressure reveals a genuine semantic contradiction rather than mere schema inconvenience;
- specialist-system evidence proves the current abstraction is structurally insufficient.

Vocabulary preference, provider naming, UI convenience, or table-count reduction is not enough.

---


## 18. Current Relationships / Reasoning position
Current accepted Cluster-5 candidate baselines:

```text
Relationship
Responsibility
Participation
Authority
Visibility
Acknowledgement
Decision
Agreement
Consent
Representation / On-Behalf-Of
Version / Material-State
Reconciliation / Source Precedence
```

Still not justified as universal primitives:

```text
Acceptance / Assent
Approval
EffectiveChange / StateTransition
Delegation
Principal
Version root/table
Reconciliation root
Conflict root
SourcePrecedence hierarchy
```

Cluster 5 remains open until the remaining candidate/dependency space is freshly re-scored and later integrated/stressed as a cluster.

---


## 19. Current Reconciliation / Source Precedence v0 amendment
Reconciliation v0 is the current semantic baseline for conflict/source-precedence reasoning on `feature/domain-model`.

Current invariant set:

```text
material competition may remain unresolved
newer != truer
source identity != Authority != truth
Source Precedence is bounded by target/facet/purpose/context/time
Reconciliation may select/combine/correct/supersede/escalate/defer/remain unresolved
Decision may result but is not mandatory
current/effective state remains owned by the affected concept
Version preserves material states/divergence
Provenance preserves lineage
Evidence informs but does not select by itself
Visibility of conflict/source/basis remains independent
AI confidence/access does not create precedence or Authority
```

This amendment does not introduce a global reconciliation engine or physical schema. Per-domain precedence policies, native identity merge/split, GoalCriterion/evaluation, Trigger/policy mechanics, Principal/enforcement, retention/audit and logical/physical/API/sync representation remain explicitly deferred.

**Propagation status:** semantic 28-path Reconciliation scope is complete on the active branch and final post-write QA is PASS. The accidental technical probe was already removed and QA-closed. Synchronization with the newer accepted `main` baseline remains a separately gated future scope and is not a prerequisite for continuing Relationships / Reasoning.

---

# 2026-08-14 — Repository-state correction

The preservation-first current-document reconstruction is complete and QA-closed on `feature/domain-model`. The accidental technical probe was already removed and QA-closed before reconstruction, and the historical-preservation audit remains intact. Reconciliation semantic propagation and final branch-level QA are complete. The current operating decision is to finish Relationships / Reasoning and the required Cluster-5 validations before any separately gated synchronization with `main`.

`Relationship v0` remains a checkpoint-backed typed/specific relationship modeling discipline. `docs/domain/concepts/relationship.md` does not exist by design and must not be recreated merely to satisfy navigation symmetry.

---

# 2026-08-15 — Criterion / Evaluation v0 language-map amendment

Criterion / Evaluation v0 supersedes the earlier `GoalCriterion / evaluation model` deferral in section 13 at the semantic level. The historical line remains preserved above because this split document is append-only/current-state preserving; this amendment is authoritative where the two conflict.

## Current canonical vocabulary

| Term | Status | Current meaning |
|---|---|---|
| Criterion | CANONICAL CONTEXTUAL EVALUATIVE SPECIFICATION/CAPABILITY | defines the condition, rule, threshold, pattern, checkpoint, assessment or combination relevant to evaluating a bounded target for a defined purpose/context |
| GoalCriterion | CANONICAL SCOPED USE / NOT SEPARATE ROOT | Criterion applied/scoped to a Goal; not a separate universal primitive/entity/root |
| Evaluation | CANONICAL CONTEXTUAL REASONING / PROCESS-RESULT SEMANTICS | applies the applicable Criterion state to relevant Evidence under material target/rule/context/time; may be reconstructed or materialized where consequence requires, but is not a universal entity/root/workflow |
| Goal Progress | DERIVED / EVALUATION PROJECTION | projection derived from applicable Evaluation semantics; not universal stored percentage/status |

## Canonical non-equivalences

```text
Goal != Criterion
Milestone != Criterion
Criterion != Evidence
Evaluation != Evidence
Evaluation != Actual
Evaluation != Outcome
Evaluation != Decision
Evaluation != Confirmation
Evaluation != Reconciliation
Goal Progress != universal stored percentage/status
```

## Current evaluation guardrails

```text
missing Evidence != failed Criterion
unknown / insufficient Evidence is valid
multiple Criteria != universal AND / average / score
Criterion change v1 -> v2 != retroactive rewrite of v1 Evaluation
historical Evaluation may require material target + Criterion + Evidence/source basis + context reconstruction
private Evidence may support shareable bounded Evaluation without source disclosure
AI proposal/calculation != Criterion adoption / Agreement / Decision / Authority / Evidence / certainty
```

The following universal defaults are rejected:

```text
Universal GoalCriterion entity/root
Universal Evaluation entity/root/workflow
Universal target_value field
Universal progress_percentage
Universal score/confidence model
Universal evaluation DSL
```

Section 18 current accepted Cluster-5 baselines is extended downstream to include:

```text
Criterion / Evaluation
```

No next Cluster-5 candidate is selected by this language-map amendment. Trigger/conditional policy, reusable comparator/Range/Threshold representation, criterion-combination representation, Verification/comprehension, specialist evaluation/adjudication, Evaluation retention/materialization, Proposal/Request and the other explicitly deferred owners remain subject to fresh candidate re-score or their designated later stages.