# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Decision v0 propagated, post-write QA PASS**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- Pre-scope validated commit for the completed Decision milestone: `e353e2756bd159b582122c4fd73b5d5d63529b30`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current completed Cluster-5 semantic reviews: **Relationship, Responsibility, Participation, Authority, Visibility, Acknowledgement, Decision**
- Generic cross-domain **Acceptance is rejected as a standalone kernel primitive**; useful positive-response semantics remain family/workflow-specific.
- Universal **Approval**, **Reconciliation**, and **EffectiveChange/state-transition** roots are rejected; Approval remains scoped Decision/review semantics, Reconciliation a process/pattern, and effective state belongs to the affected domain concept.
- Current exact task: **re-score the remaining Relationships / Reasoning candidate/dependency space by dependency leverage; do not preselect the next concept from roadmap vocabulary**.
- Next exact task after re-score: **select the highest-leverage demonstrated candidate/family and execute one complete Methodology v3 cycle through documentation propagation analysis, then stop before Git write**.

## Purpose

Turn LifeOS product requirements into the smallest implementation-ready semantic model that survives real workflows without prematurely fixing specialist modules, collaboration infrastructure, final APIs or SQL tables.

Earlier product terminology is evidence, not automatic truth. Candidates are revalidated through real-world workflow inversion, discovery simulations, targeted mature-product/standard benchmarks, adversarial reduction, history/correction tests, multi-actor stress, cross-concept consistency and explicit dependency closure.

> **Accepted means current best decision, not immutable decision.**

A roadmap/product term is a candidate, not an object that must survive.

---

# 1. Required reading — current handoff

Read in this order:

1. [`../domain/README.md`](../domain/README.md)
2. [`../domain/language-map.md`](../domain/language-map.md)
3. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
4. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
5. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
6. [`../domain/checkpoints/data-subjects-v0.md`](../domain/checkpoints/data-subjects-v0.md)
7. [`../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
8. [`../domain/checkpoints/cross-cluster-validation-v4.md`](../domain/checkpoints/cross-cluster-validation-v4.md)
9. [`../domain/checkpoints/relationship-v0-validation.md`](../domain/checkpoints/relationship-v0-validation.md)
10. [`../domain/concepts/responsibility.md`](../domain/concepts/responsibility.md) + validation
11. [`../domain/concepts/participation.md`](../domain/concepts/participation.md) + validation
12. [`../domain/concepts/authority.md`](../domain/concepts/authority.md) + validation
13. [`../domain/concepts/visibility.md`](../domain/concepts/visibility.md) + validation
14. [`../domain/concepts/acknowledgement.md`](../domain/concepts/acknowledgement.md) + validation
15. [`../domain/concepts/decision.md`](../domain/concepts/decision.md)
16. [`../domain/checkpoints/decision-v0-validation.md`](../domain/checkpoints/decision-v0-validation.md)
17. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect only concept specs pressured by the next selected review.

Do **not** redo Clusters 1–4 or completed Cluster-5 reviews unless stronger evidence exposes an actual contradiction.

---

# 2. Mandatory operating procedure

One candidate/family at a time.

For every review execute, in order:

```text
candidate selection / re-score
↓
problem + evidence formation before nouns
↓
EV-01 internal evidence
EV-02 real-world workflow inversion
EV-03 targeted external benchmark
      BORROW / ADAPT / ALREADY STRONGER /
      ANTI-PATTERN / NOT APPLICABLE
EV-04 smallest candidate
↓
identity / independence / boundaries / deliberate deferrals
↓
CORE-01..13
↓
MA-01..20
↓
XCON-01..06
↓
Adjacent Dependency Sweep
RESOLVED / SAFE DEFERRED / REOPEN
↓
adversarial log
reopening/dependency register
regression corpus additions
↓
verdict
↓
documentation propagation analysis
↓
STOP BEFORE GIT WRITE
```

A SAFE DEFERRED item must include:

- unresolved question;
- why current acceptance is safe;
- owner/stage;
- exact reopening trigger;
- exact tests/boundaries to rerun.

No `TBD`, unnamed future dependency or generic `review later` is valid for a material issue.

Once a candidate review starts, execute the whole v3 pipeline autonomously. Do not stop after each CORE/MA test merely for `avanti`; stop only for a true REOPEN/user decision or at the Git write gate.

After a coherent review:

1. state exact branch;
2. state exact pre-scope commit;
3. state exact create/update file scope with propagation reason;
4. wait for explicit user approval;
5. write only approved paths;
6. QA the full diff against the pre-scope commit;
7. confirm no out-of-scope path changed;
8. treat approval as consumed;
9. only then re-score the next candidate.

Canonical rule:

```text
V3 verdict in chat
!= accepted Domain Atlas baseline

accepted baseline
= completed v3
+ hardenings incorporated
+ documentation propagation
+ approved Git write
+ post-write QA PASS
```

---

# 3. Product / evidence rules

LifeOS is a **personal-first adaptive personal operating system**, not a universal enterprise/specialist workflow suite.

External apps, standards, APIs and specialist systems are **benchmark evidence, never design authority**.

Preferred direction:

```text
LifeOS semantics
↓
strong internal model
↓
optional adapters/mappings
↓
external providers/standards
```

Benchmark behavior, lifecycle, correction/history, failure modes, privacy, Authority, sync and product cost — not nouns.

A mature product feature is not proof of correct ontology. A technical security model being feasible is not proof LifeOS should adopt it. A provider enum/status does not become a kernel invariant merely through interoperability pressure.

---

# 4. Language / documentation rules

`docs/domain/language-map.md` is the canonical quick terminology map:

```text
DOMAIN LANGUAGE
↓
PRODUCT LANGUAGE
↓
UI LANGUAGE
↓
IMPLEMENTATION LANGUAGE
```

A UI/product noun does not create a primitive.

Terminology precedence:

1. accepted concept spec;
2. Language Map;
3. validation/checkpoint guardrails;
4. this workstream handoff;
5. current product docs;
6. historical product docs/glossaries;
7. conversation memory.

Historical checkpoints/evidence are not silently rewritten for vocabulary uniformity. Later resolutions close earlier deferrals through explicit downstream amendments/current docs.

The old product glossary remains product/historical evidence; Domain Atlas semantics take precedence where they differ.

---

# 5. Current validated baseline

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
Acknowledgement v0 review       PASS WITH HARDENING — hardenings incorporated + post-write QA PASS
Generic Acceptance primitive    REJECTED
Decision v0 review              PASS WITH HARDENING — hardenings incorporated + post-write QA PASS
Universal Approval primitive    REJECTED
Universal Reconciliation root   REJECTED
Universal EffectiveChange root  REJECTED
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

Decision v0 is operationally complete and is part of the current validated branch baseline.

---

# 6. Current accepted concept/capability set

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
Person           — native human identity
Actor            — semantic agency capability
Asset            — scoped native physical-object identity
Resource         — semantic planning/execution role/capability
Relationship modeling discipline — cross-cutting rule, not root
Responsibility   — accountability relation family
Participation    — involvement relation family
Authority        — governance relation/capability
Visibility       — information-exposure capability
Acknowledgement  — explicit-taking-notice common-ground attestation/relation capability
Decision         — contextual bounded-resolution semantic family/capability
```

Accepted security/access boundary, detailed model deferred:

```text
Person != Account != Principal
Actor != Account/Principal
```

---

# 7. Current rejected kernel abstractions

Includes:

```text
universal Register/RegisterEntry
universal Subject/Actor/Resource/User/ManagedObject roots
universal Relationship root / semantic-free related_to
universal Responsibility/Assignment/Claim/Hand-off roots
universal Participant/Participation/Invitation/Attendance roots
universal Authority/admin/Permission root
universal Access/Visibility ACL root
universal delivery/read/Acknowledgement state machine
universal cross-domain Acceptance / Assent root
one generic accepted=true status across workflows
universal Approval root
universal Reconciliation root
universal EffectiveChange / StateTransition root
one universal approved=true status
Decision object for every mutation
```

Do not reintroduce a rejected abstraction under a new noun without explicitly reopening the relevant checkpoint with stronger evidence.

---

# 8. Current relationship/reasoning decomposition

```text
who acts?                   Actor
who is accountable?         Responsibility
who is involved?            Participation
who may govern?             Authority
who may see?                Visibility
who explicitly noticed?     Acknowledgement
what bounded question was resolved? Decision
what state is now effective? affected domain concept
what actually happened?     Actual
```

Current non-collapse rules include:

```text
Actor action != Authority
Responsibility != Authority/Visibility/Acknowledgement/Decision
Participation != Authority/Visibility/Acknowledgement/Decision
Visibility != Authority/actual View/Acknowledgement
Confirmation != Authority/Acknowledgement/Decision
Acknowledgement != understanding/Confirmation/Participation response/Authority/Decision/Actual
Decision != Authority/effective target state/Actual/Provenance/Evidence/Agreement/Consent
```

Common-ground/governance sequence where consequence requires it:

```text
proposed/sent
!= delivered/read/displayed
!= Acknowledgement
!= family-specific response / future Agreement or Consent
!= Approval / Decision
!= effective target state
!= Actual
```

---

# 9. Acknowledgement v0 — last common-ground milestone

Canonical question:

> **Who explicitly took notice of this specific target/material version/change/request in this context?**

Current result:

```text
PASS WITH HARDENING
hardenings incorporated
post-write QA PASS
REOPEN = 0
unclassified material dependencies = 0
```

Generic cross-domain Acceptance remains rejected. See `concepts/acknowledgement.md` and `checkpoints/acknowledgement-v0-validation.md` for the full normative baseline.

---

# 10. Decision v0 — completed milestone

Canonical question:

> **What bounded question was resolved to what result, by whom/what, about which target/version/context?**

Classification:

```text
DECISION
CANONICAL CONTEXTUAL BOUNDED-RESOLUTION SEMANTIC FAMILY / CAPABILITY

✅ bounded question/result/context
✅ target/material-version sensitive
✅ Actor/process attributable
✅ historically reconstructible where material

❌ universal entity/root
❌ every mutation
❌ Authority
❌ effective target state
❌ Actual/truth
❌ Provenance/rationale
❌ Evidence/evaluation
❌ Acknowledgement/Confirmation/Acceptance/Agreement/Consent
```

Key hardenings:

```text
Decision(v1) != Decision(v2) after material change by default
Decision time != effect time != Actual time
Decision may cause zero/one/multiple effects
state change may occur without a new explicit human Decision under bounded authorized policy
superseded/reversed Decision != never decided
one Actor's Approval/Decision != collective Decision automatically
Decision result Visibility != rationale/Evidence/Provenance Visibility
AI proposal/recommendation != Decision
```

Related disposition:

```text
Approval
→ scoped Decision/review-result semantics
→ no universal primitive

Reconciliation
→ process/pattern
→ may culminate in Decision or remain unresolved
→ no universal primitive

Effective canonical change
→ owned by affected domain concept
→ no universal root/object
```

Full CORE-01..13, MA-01..20, XCON-01..06 and Adjacent Dependency Sweep executed.

Current result:

```text
PASS WITH HARDENING
hardenings incorporated
post-write QA PASS
REOPEN = 0
unclassified material dependencies = 0
```

Regression additions:

```text
R-DEC-01 material version change invalidates inherited approval by default
R-DEC-02 shift swap response → Approval/Decision → effective transfer → later Actual
R-DEC-03 conflicting assertions → reconciliation → explicit Decision → corrected current Actual with history preserved
R-DEC-04 reject/retain-current Decision without target mutation
R-DEC-05 bounded authorized deterministic effect without fabricated human Decision
R-DEC-06 shared Decision + different actor stances + selective rationale/Evidence Visibility
```

---

# 11. Current Decision SAFE DEFERRED dependencies

All remain non-blocking with owners/triggers/tests in the Decision checkpoint:

```text
Agreement / Consent
Version / material-equivalence mechanics
Principal / delegation / on-behalf-of
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Collective Decision / quorum / voting
GoalCriterion / evaluation
exact persistence/cardinality/API representation
specialist approval/signature/legal workflows
```

No material neighbor remains unclassified.

---

# 12. Completed Decision propagation scope

The Decision milestone propagated to exactly:

```text
concepts/decision.md
checkpoints/decision-v0-validation.md
language-map.md
README.md
this workstream handoff
multi-actor-readiness-v1.md
concepts/authority.md
checkpoints/authority-v0-validation.md
concepts/actual.md
checkpoints/actual-v0-validation.md
concepts/responsibility.md
checkpoints/responsibility-v0-validation.md
concepts/provenance.md
checkpoints/provenance-v0-validation.md
concepts/evidence.md
checkpoints/evidence-v0-validation.md
concepts/schedule.md
checkpoints/time-v0.md
concepts/confirmation.md
checkpoints/confirmation-v0-validation.md
concepts/acknowledgement.md
checkpoints/acknowledgement-v0-validation.md
checkpoints/deferred-dependency-closure-clusters-1-4-v0.md
```

Historical discovery/research/product-glossary files, Cross-Cluster v4, root `README.md`, `docs/PROJECT-STATUS.md`, prototype, SQL/API/auth/backend were intentionally left untouched.

---

# 13. Decision post-write QA — PASS

Validated against pre-scope commit:

```text
e353e2756bd159b582122c4fd73b5d5d63529b30
```

QA result:

```text
approved paths changed               23 / 23
out-of-scope paths                    0
new Decision files                    2 / 2
structural REOPEN                     0
unclassified material dependencies   0
current main baseline                 c5120ff463e027c42f4a26fc613d0917596ca738
branch behind current main            0
```

Validated conditions:

- Language Map, Domain README, Multi-Actor Readiness and workstream agree;
- historical concept/checkpoint material is preserved with explicit downstream Decision closures rather than silent historical rewrites;
- Approval remains scoped Decision/review semantics and is not Authority/effect/root;
- Reconciliation remains a process/pattern, not a universal root;
- effective state remains owned by the affected domain concept;
- Authority, Actual, Responsibility, Provenance, Evidence, Schedule, Confirmation and Acknowledgement boundaries remain intact;
- Agreement/Consent, Version, Principal/delegation, proposal identity, collective Decision, evaluation and detailed reconciliation remain classified SAFE DEFERRED with executable owners/triggers/tests;
- generic Acceptance remains rejected;
- no universal Approval/Reconciliation/EffectiveChange root was introduced;
- main, prototype, root README, PROJECT-STATUS, product evidence, SQL/API/auth/backend were not touched by this milestone.

The Decision write approval is consumed after this QA PASS.

---

# 14. Current next action

Do **not** continue from the old roadmap order.

Re-score the remaining demonstrated candidate/dependency space by dependency leverage. Examples now include:

```text
Agreement
Consent / purpose limitation
Principal / delegation / on-behalf-of
Version / material equivalence
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Dependency
Coordination Stewardship standalone question
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion/evaluation
Resource Requirement / Allocation / Reservation / substitution
Verification
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/collective-Decision semantics
Personal Knowledge generic link layer
```

These are **candidate space, not a checklist of primitives**.

Selection must use dependency leverage, existing SAFE DEFERRED pressure, product value, cross-cluster impact, implementation-readiness blocking risk and ontology/specialist-system cost.

After selecting one candidate/family, execute one full v3 cycle autonomously and stop at the next Git write gate.

---

# 15. Before broad implementation

Still mandatory:

```text
finish Relationships / Reasoning candidate reviews
↓
Cluster-5 integration
↓
Cluster-5 multi-actor stress
↓
Cluster-5 deferred-dependency closure
↓
whole-domain semantic regression
↓
destructive redundancy regression
↓
deep history/correction regression
↓
whole-domain multi-actor/privacy/Authority/AI stress
↓
simple-user regression
↓
specialist-system boundary
↓
logical data model
↓
physical PostgreSQL
↓
API contracts
↓
backend packages / implementation
```

No final SQL/API jump from the current semantic stage.

---

# 16. Git / handoff discipline

`main` remains the only integrated source of truth. This branch is newer only inside its scoped unmerged Domain Model work.

For every future write:

```text
state branch + exact files + pre-scope SHA
↓
explicit user approval
↓
write only approved scope
↓
QA against pre-scope SHA
↓
approval consumed
```

Do not place critical project state only in chat. Update this handoff after each meaningful validated milestone.
