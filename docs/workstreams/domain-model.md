# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch

## Purpose

Turn LifeOS product requirements into an implementation-ready domain model without prematurely fixing specialist modules, collaboration infrastructure, API shapes or final SQL tables.

Earlier product terminology is evidence, not automatic truth. Candidates are revalidated through real-world workflows, mature-product/standard benchmarks, adversarial reduction, history/correction tests, explicit multi-actor stress and cross-concept consistency.

**Accepted means current best decision, not immutable decision.**

A roadmap concept is a candidate to validate, not an object that must survive. Rejection is correct when the capability can be preserved more cleanly without an additional kernel primitive.

---

# Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/language-map.md`](../domain/language-map.md)
5. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
6. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
7. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
8. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
9. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
10. [`../domain/checkpoints/observed-reality-evidence-v0.md`](../domain/checkpoints/observed-reality-evidence-v0.md)
11. [`../domain/checkpoints/cross-cluster-validation-v3.md`](../domain/checkpoints/cross-cluster-validation-v3.md)
12. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
13. [`../domain/concepts/actual.md`](../domain/concepts/actual.md)
14. [`../domain/concepts/outcome.md`](../domain/concepts/outcome.md)
15. [`../domain/concepts/observation.md`](../domain/concepts/observation.md)
16. [`../domain/concepts/confirmation.md`](../domain/concepts/confirmation.md)
17. [`../domain/concepts/evidence.md`](../domain/concepts/evidence.md)
18. [`../domain/concepts/provenance.md`](../domain/concepts/provenance.md)
19. [`../domain/concepts/quantity.md`](../domain/concepts/quantity.md)
20. [`../domain/checkpoints/quantity-v0-validation.md`](../domain/checkpoints/quantity-v0-validation.md)
21. [`../domain/checkpoints/register-v0-validation.md`](../domain/checkpoints/register-v0-validation.md)
22. [`../domain/concepts/subject.md`](../domain/concepts/subject.md)
23. [`../domain/checkpoints/subject-v0-validation.md`](../domain/checkpoints/subject-v0-validation.md)
24. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
25. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
26. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)
27. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
28. accepted architecture/DB ADRs.

Validation Methodology v2 and its multi-actor addendum are historical audit sources only. v3 is the mandatory active standard.

---

# Operating rules

- Revalidate candidates one at a time, then run cluster-level integration.
- Use Methodology v3 for every concept/cluster checkpoint.
- Treat mature apps, specialist systems, standards and APIs as evidence, never as automatic design authority.
- Benchmark broadly when another domain has likely learned hard product/semantic lessons already.
- Record test IDs, evidence, result, hardening/dependency and justified `N/A`.
- Allowed concept/cluster verdicts: `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Dependency closure classes are `RESOLVED`, `SAFE DEFERRED`, `REOPEN`; they are not additional concept verdicts.
- Candidate rejection is valid when no distinct identity/lifecycle/authority/invariant/query behavior justifies the primitive.
- Preserve useful product capability even when a historical kernel candidate is rejected.
- Preserve planned/current/actual/history distinctions.
- Preserve source/provenance/confirmation/evidence/authority distinctions.
- Do not fabricate historical intention or earlier knowledge from later relevance/resolution.
- Do not create one table/entity per life topic.
- Do not collapse semantics into arbitrary JSON or one universal graph/reality/fact/subject object.
- Do not let AI inference become confirmed/canonical truth or established identity automatically.
- Preserve progressive disclosure.
- Run the dedicated Multi-Actor Compatibility Gate after the Core Semantic Gate.
- New primitives require materially distinct identity/lifecycle/authority/invariants/query behavior.
- Run Cluster Integration + Cluster Multi-Actor Stress before declaring a cluster complete.
- Do not leave material neighboring questions as generic `TBD`/`review later`; every applicable closure point must classify them.
- A `SAFE DEFERRED` item must identify why it is non-blocking, its owner/future stage, exact reopening trigger and tests to rerun.
- Re-run prior clusters together when a new cluster resolves old deferred boundaries.
- Finish Data / Subjects, then perform the dedicated clusters 1–4 deferred-dependency closure and Cross-Cluster Validation v4 before Relationships / Reasoning.
- From Relationships / Reasoning onward, run the Adjacent Dependency Sweep before every concept verdict.
- Run final whole-domain regression, multi-actor and persistence/API pressure before broad implementation is treated as stable.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Cross-Cluster Validation v3     PASS
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

Actual v0                       ACCEPTED
Outcome v0                      ACCEPTED
Observation v0                  ACCEPTED
Confirmation v0                 ACCEPTED
Evidence v0                     ACCEPTED
Provenance v0                   ACCEPTED
Quantity v0                     PASS WITH HARDENING / ACCEPTED
Subject v0                      PASS WITH HARDENING / ACCEPTED SEMANTIC ROLE
Register kernel candidate       REJECTED
Universal RegisterEntry         REJECTED
Universal Subject entity/root   REJECTED
```

First-three-cluster regression result remains:

```text
18 accepted concepts retained before Cluster 4
0 structural reopenings
0 concept removals
0 justified concept merges
0 mandatory new primitives
```

The two existing cross-cluster hardenings remain:

1. reported/asserted reality != established Actual;
2. Milestone attainment is Evidence/evaluation-backed and must not duplicate underlying reality.

---

# Multi-Actor foundation

Normative reference:

- [`Multi-Actor Readiness v1`](../domain/multi-actor-readiness-v1.md)

Core direction:

```text
personal-first product
+
multi-actor-ready domain kernel
```

When actors coordinate around one real object:

```text
shared canonical fact
+
actor-scoped personal state
```

is preferred over per-user semantic duplication.

Current non-collapse rules now include:

```text
native referent/object identity
!= account
!= participant
!= responsibility
!= performer
!= Subject role
!= authority
!= visibility
```

Subject v0 further establishes:

```text
Subject role
!= Person identity
!= Actor role
!= Account/Principal
!= Resource role
!= source/observer/recorder
```

No Actor/Team/Organization/ACL/Stewardship primitive is pre-approved.

---

# Terminology architecture

Canonical quick reference:

- [`Domain & Product Language Map`](../domain/language-map.md)

Important mappings:

```text
Task           -> Activity product/UI term
Project        -> Plan product profile
Program        -> Plan product profile
Deadline       -> latest-bound Temporal Constraint
Calendar Block -> product/UI temporal/capacity representation
Occurrence     -> canonical, usually hidden
Actual         -> canonical contextual realization
Outcome        -> canonical contextual result/disposition
Observation    -> canonical measurement/simple assertion
Confirmation   -> canonical contextual attestation
Evidence       -> canonical contextual evaluative role/relationship
Provenance     -> canonical bounded contextual lineage capability
Quantity       -> canonical reusable scalar amount value semantics
Subject        -> canonical contextual aboutness role over native identity; not entity
Register       -> possible product/UI label for longitudinal capability, not kernel primitive
Tracker/History/Progress -> product/query views over native records
```

---

# Closed cluster — Observed Reality & Evidence

**Status:** PASS — current validated cluster baseline.

## Actual v0

```text
Actual = how a specific intention/expectation was established as realized
```

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
reported/asserted reality != established Actual
```

## Outcome v0

```text
Outcome = contextual result/disposition of an Actual realization
```

## Observation v0

> A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a Subject referent at an effective time or context.

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != universal RegisterEntry
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Longitudinal tracker/history/report views query native Observations and other native records without duplicating them into a universal entry layer.

Subject now references the native referent playing the aboutness role; Observation does not own a separate Subject entity.

## Confirmation v0

> A persistent contextual attestation that a specific confirmer affirms a specific version of a confirmable target as sufficiently accepted for a defined purpose at that time.

## Evidence v0

> Evidence is the contextual evaluative role played by information when that information materially bears on a specific claim, criterion, checkpoint, decision or other evaluation target.

## Provenance v0

> Provenance is bounded contextual lineage describing how a specific domain record/material version came to exist or change, including materially relevant source entities, activities, actors/systems/providers and times.

Cluster checkpoint:

- [`Observed Reality & Evidence Cluster v0`](../domain/checkpoints/observed-reality-evidence-v0.md)

Cross-cluster checkpoint:

- [`Cross-Cluster Validation v3`](../domain/checkpoints/cross-cluster-validation-v3.md)

---

# ACTIVE TASK — Data / Subjects

The first three clusters are validated together. **Data / Subjects is the active domain cluster.**

Do not jump to SQL/API design yet.

## Candidate status

```text
Quantity       ACCEPTED — canonical value semantics
Register       REJECTED as kernel primitive
RegisterEntry  REJECTED as universal semantic record
Subject        ACCEPTED — canonical semantic role; entity/root rejected
Person / Actor ACTIVE NEXT BOUNDARY REVIEW
Asset          PENDING CANDIDATE
Resource       PENDING CANDIDATE
```

None of the pending candidates is guaranteed to survive.

## Accepted concept — Quantity v0

> A Quantity is reusable scalar value semantics representing an amount through a numerical magnitude together with unit semantics sufficient to interpret that amount. It has no independent subject, property, time, identity, provenance, intention, observation history, or evaluative meaning.

Critical boundaries:

```text
Quantity != entity
number != Quantity by default
Quantity != Observation
property / quantity kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range / Threshold / comparator / criterion
```

Checkpoint:

- [`Quantity v0 Validation`](../domain/checkpoints/quantity-v0-validation.md) — **PASS WITH HARDENING**.

## Rejected candidate — Register

Historical discovery proposed a universal `Register + RegisterEntry` structure.

Current validation rejects that kernel design while preserving:

```text
native semantic records
        ↓
query / filtering / grouping
        ↓
valid aggregation / trend / comparison
        ↓
Register / Tracker / History / Progress product UI
```

Rules:

- no universal RegisterEntry;
- no Register source-of-truth container;
- one native record may appear in several views without duplication;
- view deletion/filter changes do not modify source facts/history;
- aggregation validity comes from source metric/record/evaluation semantics;
- quick capture creates the native semantic record;
- saved tracker configuration is product/application configuration unless future evidence proves distinct domain truth;
- `Transaction`, `Movement`, `Snapshot`, or similar concepts are not pre-approved by examples from the old Register proposal.

Checkpoint:

- [`Register Candidate v0 Validation`](../domain/checkpoints/register-v0-validation.md) — **KERNEL CANDIDATE REJECTED / PRODUCT NEED RETAINED**.

## Accepted semantic role — Subject v0

> Subject is the contextual semantic role played by a native referent when a descriptive record primarily concerns that referent's state, property, condition, or asserted fact.

Accepted shape:

```text
Person / future Asset / Device / Location / other native referent
        ↑
     Subject role
        │
Observation / descriptive record
```

Rejected shape:

```text
Subject entity/root
    ↓ wraps
Person / Asset / Device / ...
```

Core rules:

```text
Subject != Person
Subject != Actor
Subject != Account/Principal
Subject != Asset
Subject != Resource
Subject != observer/recorder/source/transformer
Subject != authority/visibility/owner
Subject != generic related_to
```

Additional hardenings:

- current Account is not universal Subject default;
- non-LifeOS people and non-person referents may be Subject;
- unknown/later-resolved/corrected subject attribution preserves material history;
- subject association itself may be sensitive;
- AI may propose Subject resolution but does not establish identity/authority automatically;
- no universal `subjects` table/root is pre-approved.

Checkpoint:

- [`Subject v0 Validation`](../domain/checkpoints/subject-v0-validation.md) — **PASS WITH HARDENING**.

## ACTIVE NEXT REVIEW — Person / Actor / Account boundary

This review must not begin from `users.id` or assume a fixed inheritance tree.

Primary questions:

```text
Person = native human identity?
Actor = entity, capability, role, or category of possible agents?
Person can exist without Account? — must survive
Account = login/credential container, product identity, or principal?
Can one Person have several Accounts/credentials?
Can Account represent service/system without Person?
Can several Persons/actors ever operate through one account/context?
Actor vs Person vs Organization/service/device agent
Person vs contact/profile/provider duplicates and reconciliation
Subject role over Person vs Actor role over same Person
participant/responsible/performer roles vs Actor identity
Principal belongs here or later with Authority?
historical attribution when account is revoked/deleted/changed
assisted participation and low-digital/non-account people
AI/service acting identity without authority laundering
```

Mandatory scenarios:

- personal self-use where Person/Actor/Account coincide;
- contact/person represented without account;
- caregiver enters/acts for another Person;
- external participant never joins LifeOS;
- same Person changes email/account provider;
- multiple credentials/accounts linked to one Person;
- service/bot/device performs a system action;
- account is disabled/revoked but historical attribution survives;
- guardian/caregiver unequal authority;
- AI acts on behalf of a principal but does not become authority itself.

External benchmarks should include mature identity/contact/collaboration systems, but their resource taxonomy is evidence only.

## Mandatory inherited re-tests

```text
Observation vs Quantity — RESOLVED by Quantity v0
Observation vs Register/RegisterEntry — RESOLVED by Register rejection
Quantity vs Register aggregation — RESOLVED at kernel level
Subject vs observer/recorder/source/transformer — RESOLVED by Subject v0
Subject entity vs semantic role — RESOLVED by Subject v0
Subject vs current Account — basic boundary RESOLVED
Person vs Actor vs Subject vs Account/Principal — ACTIVE
sampled-series physical representation — SAFE implementation dependency
Availability/Capacity vs Resource
Provenance source/actor roles vs Person/Actor/Account
Subject vs Asset/Resource — mandatory later in this cluster
```

The Person / Actor / Account review is read-only until Methodology v3 passes and a separately stated Git write scope is explicitly approved.

---

# TRANSITION GATE — after Data / Subjects

Before Relationships / Reasoning begins, execute:

```text
Data / Subjects cluster integration
        ↓
Data / Subjects multi-actor stress
        ↓
cluster verdict
        ↓
DEFERRED DEPENDENCY CLOSURE — clusters 1–4
        ↓
RESOLVED / SAFE DEFERRED / REOPEN for every material open boundary
        ↓
Cross-Cluster Validation v4 — clusters 1–4
        ↓ only after PASS
Relationships / Reasoning
```

The dependency closure must revisit inherited issues from the first three clusters as well as Cluster 4 findings. Nothing material may remain as unowned limbo.

---

# Later Relationships / Reasoning review space

Likely topics:

- Relationship;
- Dependency;
- Responsibility / Assignment / Hand-off;
- Contribution;
- Goal relationships;
- Evidence/Criterion relationships;
- Participation;
- Authority / Visibility;
- Decision;
- Version;
- AI Proposal;
- Principal if the identity/authority review shows it belongs here rather than in Data / Subjects.

Mandatory inherited re-tests:

- Evidence vs typed Relationship semantics;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version / Decision / Audit;
- Confirmation vs Authority / Acknowledgement / Acceptance;
- competing assertions and canonical decision/reconciliation policy;
- collaborative Session/Actual attribution;
- Subject vs focus/context/Visibility;
- Person/Actor historical attribution after account revocation.

From this cluster onward, the Adjacent Dependency Sweep is mandatory before each concept verdict.

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
Actual realization context
        ├─ Outcome where result/disposition matters
        └─ Observation(s)
             ├─ may use Quantity value semantics
             └─ references native referent playing Subject role

Confirmation
= contextual affirmation of specific target/version/purpose

Evidence
= contextual evaluative use of existing information

Provenance
= bounded lineage explaining how records/material versions came to exist/change

Quantity
= reusable scalar amount value semantics also usable outside Observation

Subject
= contextual role over native referent identity

Longitudinal product views
= queries/projections over native records, not a separate truth layer
```

This is not a mandatory parent/child chain and not a persistence schema.

---

# Reopen / deferred-dependency watchlist

The post-Cluster-4 closure pass must turn every still-material item into `RESOLVED`, `SAFE DEFERRED`, or `REOPEN`.

Active/current items:

- Person vs Actor vs Subject vs Account/Principal — ACTIVE;
- Person identity vs contact/profile/provider representation;
- historical actor attribution after account change/revocation;
- service/system/device acting identity;
- Subject vs Asset;
- Subject vs Resource;
- Subject vs focus/context/typed Relationship;
- Subject association privacy vs Visibility;
- heterogeneous Subject-reference persistence;
- Availability/Capacity vs Resource;
- Actual establishment under Authority/Decision/reconciliation semantics;
- Confirmation vs Authority/Acknowledgement/Acceptance/Version;
- Evidence vs GoalCriterion/Relationship/Decision/Version;
- Milestone attainment vs Evidence/GoalCriterion/Decision;
- Provenance vs Version/Decision/Audit/Authority;
- provenance retention/privacy/deletion;
- contextual competing assertions under Authority rules;
- collaborative Session vs actor-scoped Actual participation;
- Responsibility vs Assignment vs Hand-off vs Stewardship;
- Resource vs Actor;
- Authority vs Visibility/governance;
- AI Context Builder inference/disclosure boundaries;
- Recurrence vs Trigger;
- Quantity vs Money/MonetaryAmount;
- Quantity vs ratings/scales/ratio/percentage/count semantics;
- Quantity vs custom unit-definition semantics;
- Quantity vs elapsed duration/calendar-relative time;
- Quantity vs Range/Threshold/comparator semantics;
- Quantity decimal/unit physical representation;
- longitudinal query/materialization/saved-view implementation;
- aggregate visibility vs source-record visibility;
- future transaction/movement/snapshot semantics only when concrete workflow evidence requires them.

Resolved:

- Observation vs Register/RegisterEntry;
- Register as kernel primitive;
- universal RegisterEntry;
- Quantity vs generic Register aggregation at kernel level;
- Subject entity vs semantic role;
- Subject vs observer/recorder/source/transformer;
- Subject vs current Account at the basic identity boundary.

These are executable obligations, not generic `later` notes.

---

# Before broad persistence/backend implementation

The full Domain Atlas must eventually establish:

- conceptual model;
- entity/value-object/semantic-role/relationship boundaries;
- identity/invariants;
- actor/context/authority model;
- lifecycle/state distinctions;
- relationship map;
- provenance/confirmation/evidence rules;
- AI authority/proposal boundaries;
- logical data model;
- physical PostgreSQL model;
- API contracts;
- backend package boundaries;
- final whole-domain stress result.

Only after the domain is coherent should production persistence be treated as stable.

---

# Current task / sequencing

```text
Intention & Execution v0 accepted
↓
Time v0 accepted
↓
Observed Reality & Evidence v0 accepted
↓
Cross-Cluster Validation v3 PASS
↓
Data / Subjects — ACTIVE
  Quantity v0 accepted
  Register candidate rejected
  Subject v0 accepted as semantic role
  Person / Actor / Account boundary review now
↓
Asset candidate
↓
Resource candidate
↓
Data / Subjects cluster integration + multi-actor stress
↓
Deferred Dependency Closure — clusters 1–4
↓
Cross-Cluster Validation v4
↓ only after PASS
Relationships / Reasoning
↓
final whole-domain gates
↓
logical/physical persistence and API stabilization
```

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains the integrated repository source of truth for merged work;
- no PR for the domain branch yet;
- backend implementation not changed here;
- Phase 4 prototype branch not changed by this workstream;
- repository visibility does not change the branch/write-scope operating rules.

Continue from Methodology v3 + Execution Template v3 + Language Map + accepted Quantity v0 + Register rejection checkpoint + accepted Subject v0 + the three validated cluster checkpoints. The active next candidate is the `Person / Actor / Account` boundary in read-only mode. Do not create a parallel validation standard, terminology tree or collaboration ontology.