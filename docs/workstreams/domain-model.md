# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active after Clusters 1–4 validation**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current completed Cluster-5 reviews: **Relationship, Responsibility, Participation, Authority, Visibility**
- Current next review: **re-score Acceptance / Acknowledgement as one common-ground candidate area; neither is pre-accepted**

## Purpose

Turn LifeOS product requirements into an implementation-ready domain model without prematurely fixing specialist modules, collaboration infrastructure, final APIs or SQL tables.

Earlier product terminology is evidence, not automatic truth. Candidates are revalidated through real-world workflows, mature-product/standard benchmarks, adversarial reduction, history/correction tests, multi-actor stress and cross-concept consistency.

> **Accepted means current best decision, not immutable decision.**

A roadmap term is a candidate, not an object that must survive.

---

# 1. Required reading — current handoff

Read these first, in order:

1. [`../domain/README.md`](../domain/README.md)
2. [`../domain/language-map.md`](../domain/language-map.md)
3. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
4. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
5. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
6. [`../domain/checkpoints/data-subjects-v0.md`](../domain/checkpoints/data-subjects-v0.md)
7. [`../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
8. [`../domain/checkpoints/cross-cluster-validation-v4.md`](../domain/checkpoints/cross-cluster-validation-v4.md)
9. [`../domain/checkpoints/relationship-v0-validation.md`](../domain/checkpoints/relationship-v0-validation.md)
10. [`../domain/concepts/responsibility.md`](../domain/concepts/responsibility.md)
11. [`../domain/checkpoints/responsibility-v0-validation.md`](../domain/checkpoints/responsibility-v0-validation.md)
12. [`../domain/concepts/participation.md`](../domain/concepts/participation.md)
13. [`../domain/checkpoints/participation-v0-validation.md`](../domain/checkpoints/participation-v0-validation.md)
14. [`../domain/concepts/authority.md`](../domain/concepts/authority.md)
15. [`../domain/checkpoints/authority-v0-validation.md`](../domain/checkpoints/authority-v0-validation.md)
16. [`../domain/concepts/visibility.md`](../domain/concepts/visibility.md)
17. [`../domain/checkpoints/visibility-v0-validation.md`](../domain/checkpoints/visibility-v0-validation.md)
18. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect only the concept specs pressured by the immediate review.

Do **not** redo Clusters 1–4 or the five completed Cluster-5 reviews unless stronger evidence exposes a real contradiction.

---

# 2. Mandatory operating rules

- Work one candidate/family at a time.
- Use Methodology v3 for every review.
- From Relationships / Reasoning onward, run the **Adjacent Dependency Sweep before every verdict**.
- Run the whole v3 pipeline autonomously once a candidate starts; do not stop after each individual CORE/MA test merely to ask for `avanti` unless a real `REOPEN` or user decision is required.
- Mature apps, standards and specialist systems are benchmark evidence, never design authority.
- Benchmark behavior/lifecycle/failure modes, not nouns.
- Allowed concept verdicts: `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Dependency closure classes: `RESOLVED`, `SAFE DEFERRED`, `REOPEN`.
- SAFE DEFERRED requires safety reason, owner/stage, exact reopening trigger and rerun tests.
- No `TBD`, unnamed future dependency or generic `review later` for material issues.
- Candidate rejection is valid when capability survives without a distinct primitive.
- Preserve planned/current/actual/history distinctions.
- Preserve identity versus contextual-role distinctions.
- Preserve truth/Observation/Evidence/Confirmation/Provenance/Authority/Visibility distinctions.
- Do not build the domain around `users.id`.
- Do not collapse the domain into arbitrary JSON.
- Do not create a universal graph/root merely for heterogeneous references.
- Do not begin final SQL/API design until Relationships / Reasoning and whole-domain gates pass.
- Reopen earlier concepts only for an actual contradiction, not because a later concept adds detail.

## Git rule

Before **every future Git write**:

1. state exact branch + exact file scope;
2. wait for explicit user approval;
3. perform only that scope;
4. QA against the pre-scope commit;
5. treat approval as consumed after completion.

Never infer write approval from a previous scope.

---

# 3. Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING
Relationship v0 review          PASS WITH HARDENING
Responsibility v0 review        PASS WITH HARDENING
Participation v0 review         PASS WITH HARDENING
Authority v0 review             PASS WITH HARDENING
Visibility v0 review            PASS WITH HARDENING
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

---

# 4. Current accepted concept/capability set

```text
Goal
Plan
Activity
Event
Routine
Milestone
Occurrence
Schedule
Session
Temporal Constraint
Recurrence
Availability & Capacity
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
Quantity
Subject          — semantic aboutness role
Person           — native human entity
Actor            — semantic agency capability
Asset            — current scoped native physical-object entity
Resource         — semantic planning/execution role/capability
Relationship modeling discipline — cross-cutting rule, not root
Responsibility   — accountability relation family
Participation    — involvement relation family
Authority        — governance relation/capability
Visibility       — information-exposure capability
```

Accepted boundary, detailed security model deferred:

```text
Person != Account != Principal
Actor != Account/Principal
```

---

# 5. Rejected kernel roots / primitives

```text
Register
universal RegisterEntry
universal Subject entity/root
universal Actor entity/root
universal Resource entity/root
universal User root
universal ManagedObject root
universal Relationship entity/root/supertype
semantic-free related_to kernel truth
universal Responsibility entity/root
universal Assignment primitive
universal Claim primitive
universal Hand-off primitive
universal Participant entity/root
universal Participation/member/social-graph root
universal Invitation primitive
universal Attendance primitive
universal Authority entity/root
universal admin flag as domain governance
universal Permission object as domain Authority
universal Access mega-concept
universal Visibility/ACL entity/root
```

No rejected primitive should be reintroduced under a new name without explicitly reopening the relevant checkpoint.

---

# 6. Relationship modeling discipline

Normative checkpoint: `relationship-v0-validation.md`.

```text
specific meaning + semantically complete simple link
→ direct specific relation may suffice

specific meaning + material relation state/history/time/privacy/Authority/etc.
→ specific qualified relation family may be justified

universal Relationship wrapper
→ rejected
```

Hardening:

```text
qualified relation != independent entity automatically
queryability/cardinality/row-id != domain identity
orientation/symmetry/transitivity/inverse = family-specific
binary source/target not mandatory if it destroys n-ary context
```

This discipline has survived four major stresses: Responsibility, Participation, Authority and Visibility.

---

# 7. Responsibility v0

Canonical question:

> **Who is accountable for ensuring this bounded commitment is appropriately handled?**

```text
Responsibility
specific semantic relation family
simple/direct or specifically qualified when justified
NOT universal entity/root

Assignment
role-specific establishment/change operation
NOT standalone primitive

Claim
self-initiated role-acquisition operation
NOT standalone primitive

Hand-off
role-specific transfer workflow
NOT standalone primitive

Coordination Stewardship
semantically distinct
standalone primitive SAFE DEFERRED
```

Mandatory distinctions:

```text
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Resource
Responsibility != Participation
Responsibility != Authority
Responsibility != Visibility
Responsibility != ownership/custody/Stewardship
unknown holder != explicitly open/unassigned
```

Operations must name the role being changed. Hand-off request != effective transfer by default.

Authority v0 now owns governance/effect. Visibility v0 owns information exposure. Acceptance/Acknowledgement still owns willingness/common-ground questions.

---

# 8. Participation v0

Canonical questions:

> **Who is expected/intended to be involved?**

and independently:

> **Who actually participated, and how/when where material?**

```text
Participation
specific relation family
intended/response and Actual facets distinct
NOT entity/root/social graph

Participant
contextual role over native identity

Invitation
participation proposal/request

Participation response
actor-scoped intended/response state

Attendance
Event-facing Actual Participation semantics
```

Mandatory distinctions:

```text
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Participation != Session
Participation != Responsibility/Performer/Resource
Participation != Authority/Visibility
shared Actual != identical actor-specific Actual Participation
```

Provider attendance telemetry is Evidence/Provenance until applicable reconciliation establishes current truth.

---

# 9. Authority v0

Canonical question:

> **Who/what may legitimately make which bounded domain effect effective, on what target and under what scope/basis/context?**

```text
Authority
CANONICAL cross-cutting governance relation/capability
contextual + action/effect/target scoped
may be direct/derived/qualified
NOT native entity/root
```

Mandatory distinctions:

```text
Authority != Actor
Authority != Person/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility
Authority != ownership
Authority != Confirmation/Acceptance
Authority != truth
Authority != technical Permission/authorization
```

Hardening:

```text
Authority to X != Authority to Y
current Authority != historical Authority at action time
claimed Authority != established Authority
Authority unknown != explicit no-Authority/prohibition
revoked/expired != never existed
```

Delegation is a bounded Authority-establishment/entrustment pattern; it does not transfer everything and does not imply re-delegation.

AI reasoning/action ability does not create Authority. Effective AI Authority cannot silently exceed applicable scope.

---

# 10. Visibility v0

Canonical question:

> **What bounded information may this recipient/access context be exposed to?**

```text
Visibility
CANONICAL cross-cutting information-exposure capability
contextual + recipient/target/representation scoped
may be direct/derived/qualified
NOT native entity/root
NOT universal Access/ACL object
```

Mandatory distinctions:

```text
Visibility != Authority
Visibility != Account/Principal/technical read permission
Visibility != Responsibility/Participation/ownership/Subject/Resource
Visibility != Sharing/Disclosure operation
Visibility != actual View
Visibility != Acknowledgement
Visibility != Consent
Visibility != arbitrary downstream Use
```

Hardening:

```text
can see != can change
can see != can re-disclose
can see != can use for any purpose
may see != actually saw
visible endpoints != visible relationship
visible projection != visible source
current Visibility != historical Visibility
revoked Visibility != erased past disclosure/knowledge
not visible != nonexistent
no applicable grant != explicit prohibition semantically
```

Critical AI rule:

```text
AI may process authorized source
!= AI may disclose source
```

Inference/output privacy must be checked independently from input access.

---

# 11. Cross-concept closure caused by Authority + Visibility

The following old broad deferred boundaries are now semantically closed:

```text
Actor ↔ Authority/Visibility
Responsibility ↔ Authority/Visibility
Participation ↔ Authority/Visibility
Confirmation ↔ Authority/Visibility
Schedule ↔ Authority/Visibility
Actual ↔ Authority/Visibility
Subject ↔ Authority/Visibility
Resource ↔ Authority/Visibility
Asset ↔ Authority/Visibility
Provenance ↔ Authority/Visibility
```

This does **not** mean final permissions/security/persistence are designed.

Remaining detailed owners include Principal/enforcement, Consent/use purpose, Decision/reconciliation, detailed delegation, retention and logical persistence.

---

# 12. Current identity / role separation

```text
Person
= native human identity

Asset
= current scoped native physical-object identity

Subject
= contextual aboutness role

Actor
= contextual agency capability

Resource
= contextual operational eligibility/capability

Responsibility
= contextual accountability relation family

Participation
= contextual involvement relation family

Authority
= contextual governance capability

Visibility
= contextual information-exposure capability

Account
= platform/access identity boundary

Principal
= deferred authenticated/authorized security identity
```

None of these should be collapsed merely to simplify FKs.

---

# 13. Current cross-cluster invariants

Retain at least:

```text
planned != actual
passage of time != completion/Actual
Schedule != Session
Schedule != Capacity Reservation
Observation != Quantity
Evidence != source information
Provenance != truth / Authority / Visibility / Version / Audit
Confirmation != Authority / Acknowledgement / Acceptance / Verification
Subject != generic related_to
Actor != generic action edge
Resource != provider identity
Account != Person

universal Relationship root = rejected
qualified relation != entity automatically
queryability/cardinality != identity

Responsibility != requester/expected performer/actual performer
unknown Responsibility != explicitly open/unassigned
Assignment/Claim/Hand-off must name role
hand-off request != effective transfer by default

Participant != identity/root
Invitation != Acceptance/Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence

Actor action != Authority
Authority != technical authorization/truth
Visibility != Authority
Visibility != actual view
visible projection != visible source
visible endpoints != visible relationship
AI source processing != disclosure permission
```

---

# 14. Active stage — Relationships / Reasoning

**Status:** IN PROGRESS.

Completed:

```text
Relationship v0      PASS WITH HARDENING
Responsibility v0    PASS WITH HARDENING
Participation v0     PASS WITH HARDENING
Authority v0         PASS WITH HARDENING
Visibility v0        PASS WITH HARDENING
```

Every current Cluster-5 checkpoint has:

```text
REOPEN = 0
unclassified material dependencies = 0
```

Do not treat remaining candidate space as a checklist.

---

# 15. NEXT-CANDIDATE SELECTION

The next high-leverage problem is **common ground** after governance and exposure have been separated.

Current questions:

```text
who can govern?       Authority        RESOLVED
who can see?          Visibility       RESOLVED
who received/knows?   Acknowledgement  OPEN
who agrees/wants?     Acceptance       OPEN
```

Next review must start by comparing **Acceptance / Acknowledgement together**, not by assuming either deserves a standalone concept.

Test at minimum:

- message delivered vs actually received/read;
- acknowledgement vs Confirmation;
- acknowledgement vs Participation response;
- acceptance of invitation vs generic Acceptance;
- acceptance of Responsibility hand-off vs effective transfer;
- acceptance vs Authority/Approval;
- acceptance vs Agreement/Consent;
- silence vs acceptance;
- delegated/on-behalf-of acceptance;
- historical/retracted acceptance;
- common-ground state vs product notification/read receipt;
- simple personal UX vs formal high-consequence workflows.

The result may be one family, two concepts, relation-specific states, operations, or product-only semantics. Do not pre-decide.

After that, re-score again rather than following roadmap order.

---

# 16. Remaining demonstrated candidate/dependency space

Examples, not mandatory primitives:

```text
Acceptance / Acknowledgement / Agreement
Consent / use purpose
Decision / reconciliation / Approval effect
Principal / delegation / on-behalf-of
Dependency
Coordination Stewardship standalone question
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion/evaluation
Resource Requirement / Allocation / Reservation / substitution
Verification
Version
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group semantics
Personal Knowledge generic link layer
```

Each must earn its place under v3.

---

# 17. Deferred Dependency Closure registries

Clusters 1–4 normative register:

- `deferred-dependency-closure-clusters-1-4-v0.md`.

Cluster-5 current registers:

- `relationship-v0-validation.md`;
- `responsibility-v0-validation.md`;
- `participation-v0-validation.md`;
- `authority-v0-validation.md`;
- `visibility-v0-validation.md`.

Do not create a parallel unnamed watchlist. Use these checkpoints for exact owners, triggers and rerun tests.

---

# 18. Before broad persistence/backend implementation

Still mandatory after Relationships / Reasoning:

```text
Cluster-5 integration
↓
Cluster-5 multi-actor stress
↓
Cluster-5 deferred dependency closure
↓
whole-domain semantic regression
↓
destructive redundancy test
↓
deep historical reconstruction
↓
whole-domain multi-actor stress
↓
privacy / Authority / Visibility stress
↓
AI stress
↓
simple-user regression
↓
specialist-system boundary
↓
logical data model
↓
physical PostgreSQL model
↓
API contracts
↓
backend package architecture
↓
implementation / vertical slices / frontend integration
```

Do not jump directly from Cluster 5 to SQL/API stabilization.

---

# 19. Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains at `c5120ff463e027c42f4a26fc613d0917596ca738` unless a later explicitly approved scope changes it;
- no domain PR is currently required;
- backend implementation is not changed by this workstream;
- Phase-4 prototype branch is separate and must not be touched from domain-model scopes;
- repository visibility does not change write-scope rules;
- before any future Git write, state exact scope and wait for explicit approval.

## New-chat / continuation handoff

A continuing chat should:

1. read this workstream;
2. read README + Language Map + Methodology v3;
3. read Relationship/Responsibility/Participation/Authority/Visibility concept/checkpoints;
4. verify `feature/domain-model` and `main` state read-only;
5. begin Acceptance/Acknowledgement candidate formation read-only;
6. do not redo earlier reviews unless a concrete contradiction appears;
7. do not write Git until a new exact scope is explicitly approved.
