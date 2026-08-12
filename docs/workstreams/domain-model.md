# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Acknowledgement v0 propagated, scope QA pending**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- Pre-scope validated commit for current Acknowledgement milestone: `68b63bd233b116699719e77449db2180338b1bba`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current completed Cluster-5 reviews: **Relationship, Responsibility, Participation, Authority, Visibility, Acknowledgement**
- Generic cross-domain **Acceptance is rejected as a standalone kernel primitive**; useful positive-response semantics remain family/workflow-specific.
- Current exact task: **finish post-write QA for the Acknowledgement v0 propagation against `68b63bd...`**.
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
14. [`../domain/concepts/acknowledgement.md`](../domain/concepts/acknowledgement.md)
15. [`../domain/checkpoints/acknowledgement-v0-validation.md`](../domain/checkpoints/acknowledgement-v0-validation.md)
16. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

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
Acknowledgement v0 review       PASS WITH HARDENING — hardenings incorporated
Generic Acceptance primitive    REJECTED
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

The Acknowledgement milestone is not considered operationally complete until the current post-write QA passes.

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
```

Do not reintroduce a rejected abstraction under a new noun without explicitly reopening the relevant checkpoint with stronger evidence.

---

# 8. Current relationship/reasoning decomposition

```text
who acts?                Actor
who is accountable?      Responsibility
who is involved?         Participation
who may govern?          Authority
who may see?             Visibility
who explicitly noticed?  Acknowledgement
what actually happened?  Actual
```

Current non-collapse rules include:

```text
Actor action != Authority
Responsibility != Authority/Visibility/Acknowledgement
Participation != Authority/Visibility/Acknowledgement
Visibility != Authority/actual View/Acknowledgement
Confirmation != Authority/Acknowledgement
Acknowledgement != understanding/Confirmation/Participation response/Authority/Actual
```

Common-ground sequence where consequence requires it:

```text
proposed/sent
!= delivered/read/displayed
!= Acknowledgement
!= family-specific response / future Agreement or Consent
!= Authority / Decision / effective canonical change
!= Actual
```

---

# 9. Acknowledgement v0 — last completed semantic review

Canonical question:

> **Who explicitly took notice of this specific target/material version/change/request in this context?**

Classification:

```text
ACKNOWLEDGEMENT
CANONICAL SPECIFIC CONTEXTUAL COMMON-GROUND ATTESTATION / RELATION CAPABILITY

✅ actor-scoped
✅ target/material-version scoped
✅ optional / consequence-sensitive
✅ history-sensitive where material
✅ direct/simple or specifically qualified where justified

❌ native entity/root
❌ delivery/read/display receipt
❌ understanding/comprehension
❌ Confirmation
❌ Acceptance/Agreement/Consent
❌ Participation response
❌ Responsibility
❌ Authority/Decision/effective change
❌ Actual
```

Key hardenings:

```text
delivery/read/display telemetry != Acknowledgement
Acknowledgement(v1) != Acknowledgement(v2) after material change
silence/no response != Acknowledgement
one Actor's Acknowledgement != another/group Ack
assisted/on-behalf-of preserves actual Actor + represented party + basis
correction preserves material Provenance/history
future Visibility revocation != erased historical Acknowledgement
AI/provider inference != human Acknowledgement
```

Generic cross-domain Acceptance failed v3 minimality/redundancy tests:

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ role-specific response/operation

Schedule/AI proposal accepted/applied
→ proposal/effect-specific response/operation
```

No useful product capability is removed by rejecting the universal primitive.

---

# 10. Acknowledgement v0 evidence / validation summary

Internal evidence:

- Participation response already owns invitation `accepted`;
- Responsibility hand-off request != effective transfer;
- Confirmation already separated recognition from affirmation;
- Visibility already separated exposure from actual view/recognition;
- Authority already separated willingness from governance effect;
- Multi-Actor Readiness required common-ground state separation.

Targeted external evidence classifications:

```text
RFC 8098 displayed/read limits        ADAPT
Matrix read/private/full-read states  ADAPT
RFC 5545 attendee PARTSTAT            ALREADY STRONGER via Participation v0
Microsoft Teams Shifts acceptance → manager approval → effect  ADAPT
ActivityStreams generic Accept        NOT APPLICABLE as universal LifeOS primitive
```

Full CORE-01..13, MA-01..20, XCON-01..06 and Adjacent Dependency Sweep executed.

Current result:

```text
PASS WITH HARDENING
hardenings incorporated
REOPEN = 0
unclassified material dependencies = 0
```

Regression additions:

```text
R-ACK-01 material change read/display → Ack → material revision → new Ack
R-ACK-02 hand-off delivered → Ack → role response → approval/effect → different Actual performer
R-ACK-03 assisted acknowledgement attribution
R-ACK-04 acknowledgement under unequal power/coercion
```

---

# 11. Current Acknowledgement SAFE DEFERRED dependencies

All are non-blocking with owners/triggers in the checkpoint:

```text
Understanding / comprehension
Agreement / Consent
Decision / Approval / effective change
Principal / delegation / on-behalf-of
Version / material equivalence
read/view audit persistence
collective/group acknowledgement
retention/deletion of acknowledgement history
```

No material neighbor remains unclassified.

---

# 12. Current propagation scope

The Acknowledgement milestone intentionally propagated to:

```text
concepts/acknowledgement.md
checkpoints/acknowledgement-v0-validation.md
language-map.md
README.md
multi-actor-readiness-v1.md
concepts/confirmation.md
checkpoints/confirmation-v0-validation.md
concepts/participation.md
checkpoints/participation-v0-validation.md
concepts/responsibility.md
checkpoints/responsibility-v0-validation.md
concepts/authority.md
checkpoints/authority-v0-validation.md
concepts/visibility.md
checkpoints/visibility-v0-validation.md
concepts/schedule.md
checkpoints/deferred-dependency-closure-clusters-1-4-v0.md
this workstream handoff
```

Historical simulation/research/product-glossary files were not rewritten. Root `README.md` and `docs/PROJECT-STATUS.md` were not changed because this is branch-local incremental work, not a globally integrated project-state transition.

---

# 13. Current exact QA gate

Before this milestone becomes the new validated branch baseline, verify against pre-scope commit:

```text
68b63bd233b116699719e77449db2180338b1bba
```

Required QA:

- exactly the 18 approved paths changed;
- no other path changed;
- both new Acknowledgement files exist;
- Language Map, Domain README and this handoff agree;
- historical checkpoint amendments are explicitly downstream, not silent retroactive rewrites;
- generic Acceptance is rejected consistently;
- Participation `accepted` remains response semantics;
- Responsibility hand-off sequence preserves request/Ack/response/effect;
- Schedule `accepted` wording does not imply universal Acceptance;
- Authority/Visibility/Confirmation boundaries remain intact;
- `REOPEN = 0` and unclassified material dependencies = 0;
- `main`, prototype, root README, PROJECT-STATUS, product evidence, SQL/API/auth/backend remain untouched;
- branch remains coherent against current main baseline.

If QA fails, repair only within the already-approved scope when the fix is truly part of this milestone; otherwise stop for a new write scope.

---

# 14. Next action after QA PASS

Do **not** continue from the old roadmap order.

Re-score the remaining demonstrated candidate/dependency space by dependency leverage. Examples include:

```text
Agreement
Consent / purpose limitation
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

These are **candidate space, not a checklist of primitives**.

Do not preselect the next candidate until the current scope QA has passed.

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
