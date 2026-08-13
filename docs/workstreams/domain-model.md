# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Agreement / Consent v0 propagated, post-write QA pending**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- Pre-scope validated commit for the current Agreement / Consent milestone: `0d4bb2458082f9a6d4e752d83960cea9033a05ad`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current completed QA-closed Cluster-5 semantic reviews: **Relationship, Responsibility, Participation, Authority, Visibility, Acknowledgement, Decision**
- Current milestone under post-write QA: **Agreement / Consent v0 — PASS WITH HARDENING, hardenings incorporated, propagation complete pending diff QA**.
- Generic cross-domain **Acceptance / Assent is rejected as a standalone kernel primitive**; useful response/mutual-assent/permission semantics remain family-specific.
- Universal **Approval**, **Reconciliation**, **EffectiveChange/state-transition**, **Contract**, and **Consent/Permission** roots are rejected; scoped useful semantics remain in Decision, affected target state, Agreement, Consent, specialist integration and policy/enforcement boundaries.
- Current exact task: **finish post-write QA for the approved 18-path Agreement / Consent v0 propagation against `0d4bb245...`; do not re-score another candidate before QA PASS**.
- Next exact task after QA PASS: **re-score the remaining Relationships / Reasoning candidate/dependency space by dependency leverage; do not preselect a next concept from roadmap vocabulary**.

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
15. [`../domain/concepts/decision.md`](../domain/concepts/decision.md) + validation
16. [`../domain/concepts/agreement.md`](../domain/concepts/agreement.md)
17. [`../domain/concepts/consent.md`](../domain/concepts/consent.md)
18. [`../domain/checkpoints/agreement-consent-v0-validation.md`](../domain/checkpoints/agreement-consent-v0-validation.md)
19. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

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
Agreement / Consent v0 review   PASS WITH HARDENING — hardenings incorporated; post-write QA pending
Generic Assent root             REJECTED
Universal Contract root         REJECTED
Universal Consent/Permission root REJECTED
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

Agreement / Consent v0 is **not yet** the validated branch baseline until this milestone's post-write QA passes against `0d4bb245...`.

---

# 6. Current accepted / candidate concept-capability set

QA-closed current baseline:

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

Current Agreement / Consent candidate milestone pending QA:

```text
Agreement        — contextual multi-party mutual-assent relation/capability
Consent          — contextual actor-scoped bounded-permission relation/capability
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
universal Agreement / Contract root
universal Consent / Permission root
membership = Consent
Agreement = Decision
Consent = Visibility / Authority / technical permission
```

Do not reintroduce a rejected abstraction under a new noun without explicitly reopening the relevant checkpoint with stronger evidence.

---

# 8. Current relationship/reasoning decomposition

```text
who acts?                                  Actor
who is accountable?                       Responsibility
who is involved?                          Participation
who may govern?                           Authority
who may see?                              Visibility
who explicitly noticed?                   Acknowledgement
what bounded question was resolved?       Decision
which parties mutually assented to terms? Agreement
who permitted bounded use/action/exposure? Consent
what state is now effective?              affected domain concept
what actually happened?                   Actual
```

Current non-collapse rules include:

```text
Actor action != Authority
Responsibility != Authority/Visibility/Acknowledgement/Decision
Participation != Authority/Visibility/Acknowledgement/Decision
Visibility != Authority/actual View/Acknowledgement/Consent
Confirmation != Authority/Acknowledgement/Decision/Agreement/Consent
Acknowledgement != understanding/Confirmation/Participation response/Agreement/Consent/Authority/Decision/Actual
Decision != Authority/effective target state/Actual/Provenance/Evidence/Agreement/Consent
Agreement != one Actor's response/Decision/Authority/Responsibility/Consent/Contract/Actual
Consent != Visibility/Authority/technical Permission/Agreement/Decision/Actual
```

Consequence-sensitive sequence:

```text
proposed/sent
!= delivered/read/displayed
!= Acknowledgement
!= family-specific response
!= Agreement
!= Consent
!= Approval / Decision
!= Authority / effective target state
!= Actual
```

This is not a mandatory product workflow; simple UX may collapse irrelevant stages without destroying kernel semantics.

---

# 9. Acknowledgement v0 — QA-closed common-ground milestone

Canonical question:

> **Who explicitly took notice of this specific target/material version/change/request in this context?**

```text
PASS WITH HARDENING
hardenings incorporated
post-write QA PASS
REOPEN = 0
unclassified material dependencies = 0
```

Generic cross-domain Acceptance remains rejected.

---

# 10. Decision v0 — QA-closed milestone

Canonical question:

> **What bounded question was resolved to what result, by whom/what, about which target/version/context?**

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

```text
PASS WITH HARDENING
hardenings incorporated
post-write QA PASS
REOPEN = 0
unclassified material dependencies = 0
```

---

# 11. Agreement / Consent v0 — current milestone

## Agreement

Canonical question:

> **Which parties mutually assented to which materially specific terms, in which bounded context?**

```text
AGREEMENT
SPECIFIC CONTEXTUAL MULTI-PARTY MUTUAL-ASSENT RELATION / CAPABILITY

✅ applicable party set
✅ materially same terms/version
✅ history-sensitive where material
✅ direct/derived or qualified where justified

❌ native entity/root
❌ generic Acceptance/Assent
❌ Decision
❌ Authority
❌ Responsibility/resulting state
❌ Consent
❌ legal Contract/enforceability proof
❌ compliance/Actual proof
```

Key hardenings:

```text
one party assent != Agreement for everyone
silence/no response != Agreement
Agreement(v1) != materially changed terms v2 by default
current no Agreement != never agreed historically
Agreement grants no blanket Visibility/re-disclosure rights
AI inference != human Agreement
```

## Consent

Canonical question:

> **Who explicitly permitted what bounded action/use/exposure concerning what target, for which scope/purpose/context?**

```text
CONSENT
SPECIFIC CONTEXTUAL ACTOR-SCOPED BOUNDED-PERMISSION RELATION / CAPABILITY

✅ target/action/use/exposure scoped
✅ purpose/context sensitive where material
✅ lifecycle/history sensitive
✅ may be one policy basis/constraint

❌ universal Permission
❌ technical authorization
❌ Visibility
❌ Authority
❌ Agreement
❌ Decision
❌ legal-validity/capacity proof
❌ proof permitted action occurred
```

Key hardenings:

```text
silence/behavior/membership != Consent
Consent to X != Consent to Y
purpose A != materially different purpose B
material scope/version v1 != v2 by default
withdrawal changes future applicability != erases historical grant/use/disclosure
helper action != represented person's Consent automatically
AI source access/inference != human Consent or enlarged scope
```

Family verdict:

```text
PASS WITH HARDENING
hardenings incorporated
REOPEN = 0
unclassified material dependencies = 0
post-write QA pending
```

Rejected in this review:

```text
generic Assent / Acceptance supertype
universal Contract root
universal Consent / Permission root
Agreement = Decision
Agreement = Consent
Consent = Visibility / Authority / technical Permission
```

Regression additions:

```text
R-AGR-01 terms v1 → material v2 → prior Agreement not inherited
R-AGR-02 mutual shift-swap Agreement → manager Approval/effect still required
R-AGR-03 partial party assent → no fabricated full Agreement
R-CON-01 free/busy trip Consent → unrelated AI-training purpose not covered
R-CON-02 grant → use/disclosure → withdrawal → future changes, history preserved
R-CON-03 helper/guardian/caregiver on-behalf-of attribution preserved
R-AGR-CON-01 service Agreement != image/data-use Consent
R-CON-04 power-imbalanced Ack/accept click != valid Consent automatically
```

---

# 12. Agreement / Consent SAFE DEFERRED dependencies

All remain non-blocking with owner/trigger/tests in the Agreement/Consent checkpoint:

```text
Principal / delegation / representation
Version / material-equivalence mechanics
Consent validity / capacity / legal basis
Purpose/use technical policy enforcement
Collective/group/quorum party identity
Formal signature / Contract lifecycle
Proposal / request reusable identity
Retention / deletion
Verification / comprehension remains separately owned from earlier common-ground work
```

No material neighbor remains unclassified.

---

# 13. Current Agreement / Consent propagation scope

The approved milestone intentionally propagates to exactly:

```text
concepts/agreement.md
concepts/consent.md
checkpoints/agreement-consent-v0-validation.md
language-map.md
README.md
this workstream handoff
multi-actor-readiness-v1.md
concepts/acknowledgement.md
checkpoints/acknowledgement-v0-validation.md
concepts/decision.md
checkpoints/decision-v0-validation.md
concepts/visibility.md
checkpoints/visibility-v0-validation.md
concepts/authority.md
checkpoints/authority-v0-validation.md
concepts/confirmation.md
checkpoints/confirmation-v0-validation.md
checkpoints/deferred-dependency-closure-clusters-1-4-v0.md
```

Historical discovery/research/product-glossary files, Participation, Responsibility, Relationship, Provenance, Actual, Schedule, Time checkpoint, Multi-Actor Evidence Synthesis, Cross-Cluster v4, root `README.md`, `docs/PROJECT-STATUS.md`, prototype, SQL/API/auth/backend are intentionally out of scope.

---

# 14. Current Agreement / Consent QA gate

Before Agreement / Consent v0 becomes the next validated branch baseline, verify against:

```text
0d4bb2458082f9a6d4e752d83960cea9033a05ad
```

Required QA:

- exactly the approved 18 unique paths changed;
- exactly 3 new files and 15 modified files;
- no out-of-scope path changed;
- Agreement/Consent checkpoint contains complete V3 and complete propagation checklist;
- Language Map, Domain README, Multi-Actor Readiness and workstream agree;
- historical checkpoints preserve original state plus explicit downstream closure;
- Agreement != Decision/Authority/Responsibility/Consent/Contract/Actual;
- Consent != Visibility/Authority/technical Permission/Agreement/Decision;
- generic Acceptance/Assent remains rejected;
- Participation `accepted` remains family-specific response semantics;
- purpose/scope, withdrawal/history, unequal-power and on-behalf-of hardenings remain visible;
- `REOPEN = 0`, unclassified material dependencies = 0;
- main/prototype/SQL/API/auth/backend/global-status/product evidence remain untouched;
- branch remains behind main by 0.

Do not re-score another candidate until this gate passes.

---

# 15. Decision post-write QA — historical completed milestone

Decision v0 was validated against:

```text
e353e2756bd159b582122c4fd73b5d5d63529b30
```

Result:

```text
approved paths changed               23 / 23
out-of-scope paths                    0
new Decision files                    2 / 2
structural REOPEN                     0
unclassified material dependencies   0
main                                  c5120ff463e027c42f4a26fc613d0917596ca738
branch behind main                    0
```

The Decision write approval was consumed after that QA PASS.

---

# 16. Next action after current QA

Do **not** continue from old roadmap order.

After Agreement / Consent post-write QA PASS, re-score the remaining demonstrated candidate/dependency space by dependency leverage.

Candidate/dependency space includes, among others:

```text
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
Verification / comprehension
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/quorum semantics
Consent validity / purpose-use enforcement
formal Contract/signature specialist boundary
retention/deletion
Personal Knowledge generic link layer
```

These are **candidate/dependency space, not a checklist of primitives**.

Selection must use dependency leverage, existing SAFE DEFERRED pressure, product value, cross-cluster impact, implementation-readiness blocking risk and ontology/specialist-system cost.

---

# 17. Before broad implementation

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

# 18. Git / handoff discipline

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