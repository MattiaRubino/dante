# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Representation / on-behalf-of v0 post-write QA PASS**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- Completed Representation pre-scope baseline: `b6c53ffa40ba7c1c1408f583856617a0e000f31b`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current QA-closed Cluster-5 reviews: **Relationship, Responsibility, Participation, Authority, Visibility, Acknowledgement, Decision, Agreement / Consent, Representation / on-behalf-of**
- Generic cross-domain **Acceptance / Assent remains rejected**.
- Universal **Approval, Reconciliation, EffectiveChange, Contract, Consent/Permission, Principal, Agent/Representative and Delegation roots remain rejected**.
- Current exact task: **fresh re-score of the remaining Relationships / Reasoning candidate/dependency space by dependency leverage; no next candidate is preselected**.
- After re-score: **select one highest-leverage candidate/family, execute one full Methodology v3 cycle through propagation analysis, then stop before Git write**.

## Purpose

Turn LifeOS product requirements into the smallest implementation-ready semantic model that survives real workflows without prematurely fixing specialist modules, collaboration/IAM infrastructure, final APIs or SQL tables.

Earlier product terminology is evidence, not automatic truth.

> **Accepted means current best decision, not immutable decision.**

---

# 1. Required reading — current handoff

Read in order:

1. [`../domain/README.md`](../domain/README.md)
2. [`../domain/language-map.md`](../domain/language-map.md)
3. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
4. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
5. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
6. [`../domain/checkpoints/data-subjects-v0.md`](../domain/checkpoints/data-subjects-v0.md)
7. [`../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
8. [`../domain/checkpoints/cross-cluster-validation-v4.md`](../domain/checkpoints/cross-cluster-validation-v4.md)
9. [`../domain/checkpoints/relationship-v0-validation.md`](../domain/checkpoints/relationship-v0-validation.md)
10. Responsibility concept + checkpoint
11. Participation concept + checkpoint
12. Authority concept + checkpoint
13. Visibility concept + checkpoint
14. Acknowledgement concept + checkpoint
15. Decision concept + checkpoint
16. Agreement + Consent concepts + joint checkpoint
17. [`../domain/concepts/representation.md`](../domain/concepts/representation.md)
18. [`../domain/checkpoints/representation-delegation-principal-v0-validation.md`](../domain/checkpoints/representation-delegation-principal-v0-validation.md)
19. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect only concepts pressured by the newly selected review.

Do not redo Clusters 1–4 or QA-closed Cluster-5 reviews unless stronger evidence exposes an actual contradiction.

---

# 2. Mandatory operating procedure

One candidate/family at a time.

```text
fresh candidate selection / re-score
↓
problem + evidence formation before nouns
↓
EV-01 internal evidence
EV-02 workflow inversion
EV-03 external benchmark
      BORROW / ADAPT / ALREADY STRONGER /
      ANTI-PATTERN / NOT APPLICABLE
EV-04 smallest candidate
↓
identity / independence / boundaries / deferrals
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

A SAFE DEFERRED item requires:

- unresolved question;
- why current acceptance is safe;
- owner/stage;
- exact reopening trigger;
- exact tests/boundaries to rerun.

No material `TBD`/generic `review later` is valid.

Once a candidate review begins, execute the whole V3 autonomously. Stop only for a real REOPEN/user decision or at the Git write gate.

After a coherent read-only review:

1. state branch;
2. state exact pre-scope SHA;
3. state exact create/update path scope;
4. wait for explicit approval;
5. write only approved paths;
6. QA full diff against pre-scope;
7. confirm no out-of-scope path;
8. consume approval after QA PASS;
9. only then fresh re-score.

Canonical rule:

```text
V3 verdict in chat
!= accepted Domain Atlas baseline

accepted baseline
= complete V3
+ hardenings incorporated
+ propagation
+ approved write
+ post-write QA PASS
```

Historical checkpoints remain reconstructible; later resolutions use explicit downstream amendments.

---

# 3. Product / evidence rules

LifeOS is a **personal-first adaptive personal operating system**, not an enterprise workflow suite, IAM product, contract platform, clinical system or provider clone.

External systems are benchmark evidence, never design authority.

Preferred direction:

```text
LifeOS semantics
↓
strong internal model
↓
optional adapters
↓
external systems
```

Benchmark behavior, lifecycle, history/correction, failure modes, privacy, Authority, sync and product cost — not nouns.

---

# 4. Language / documentation rules

Canonical quick terminology source: `docs/domain/language-map.md`.

Precedence:

1. accepted concept spec;
2. Language Map;
3. current checkpoint guardrails;
4. this handoff;
5. current product docs;
6. historical product docs/glossaries;
7. conversation memory.

A UI/product noun does not create a primitive. Historical checkpoint material is not silently rewritten for vocabulary uniformity.

---

# 5. Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

Relationship v0                 PASS WITH HARDENING
Responsibility v0               PASS WITH HARDENING
Participation v0                PASS WITH HARDENING
Authority v0                    PASS WITH HARDENING
Visibility v0                   PASS WITH HARDENING
Acknowledgement v0              PASS WITH HARDENING — QA PASS
Generic Acceptance / Assent     REJECTED
Decision v0                     PASS WITH HARDENING — QA PASS
Universal Approval              REJECTED
Universal Reconciliation        REJECTED
Universal EffectiveChange       REJECTED
Agreement / Consent v0          PASS WITH HARDENING — QA PASS
Universal Contract              REJECTED
Universal Consent/Permission    REJECTED
Representation v0               PASS WITH HARDENING — QA PASS
Principal domain primitive      REJECTED
Universal Agent/Representative  REJECTED
Universal Delegation            REJECTED
Impersonation-as-domain-truth    REJECTED

Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

---

# 6. Current concept/capability decomposition

```text
who acts?                                  Actor
who is accountable?                       Responsibility
who is involved?                          Participation
who may govern?                           Authority
what may be exposed?                      Visibility
who explicitly noticed?                   Acknowledgement
what bounded question was resolved?       Decision
which parties mutually assented?          Agreement
who permitted bounded use/action?         Consent
who actually acted for which party?       Representation / on-behalf-of
what state is now effective?              affected domain concept
what actually happened?                   Actual
how did it arise/change?                   Provenance
```

Security identity remains separate:

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
universal Participant/Invitation/Attendance roots
universal Authority/admin/Permission root
universal Access/Visibility ACL root
universal delivery/read/Acknowledgement state machine
universal cross-domain Acceptance/Assent root
universal Approval root
universal Reconciliation root
universal EffectiveChange/StateTransition root
Decision object for every mutation
universal Agreement/Contract root
universal Consent/Permission root
Principal as LifeOS domain primitive
universal Agent/Representative root
universal Delegation root
blanket delegation
technical impersonation as domain attribution truth
```

Do not reintroduce a rejected abstraction without explicit reopening and stronger evidence.

---

# 8. Representation / on-behalf-of v0 — completed milestone

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

```text
Representation / on-behalf-of
CANONICAL CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY

✅ actual Actor preserved
✅ represented party distinct
✅ action/context scoped
✅ Authority/delegation/policy/basis separable
✅ history-sensitive where material

❌ native entity/root
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ represented-person will by implication
```

`Representative` is contextual role language, not identity.

### Delegation

```text
bounded Authority-establishment / entrustment pattern
```

No universal root, blanket transfer or automatic re-delegation.

### Principal

```text
technical authenticated/authorized request identity
```

Security/logical-model only; not a domain primitive.

### Impersonation

Possible technical mechanism only:

```text
technical impersonation != domain attribution truth
```

---

# 9. Representation hardenings

```text
actual Actor != represented party
represented party != Subject/beneficiary automatically
Representation != Authority
Representation claim != established Authority
Representation != Responsibility
Representation != Provenance
Principal != Actor
Account != Principal
represented Person requires no synthetic Account
re-delegation not implied
revoked/expired basis != never existed
AI/service action != human action/will
```

Action-specific scope:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

Representative action does not fabricate represented-party Acknowledgement, Confirmation, Agreement, Consent or Decision. Any represented effect requires an applicable action-specific basis while truthful Actor attribution remains intact.

---

# 10. Representation V3 / external evidence

Selection came from a fresh dependency-leverage re-score, narrowly ahead of Version/material equivalence.

Benchmark classifications:

```text
RFC 8693 delegation actor/subject separation        ADAPT
RFC 8693 impersonation as domain truth              ANTI-PATTERN
FHIR Provenance who/onBehalfOf                       ADAPT
W3C PROV actedOnBehalfOf                             ADAPT
W3C Authority/Responsibility coupling                ANTI-PATTERN if copied literally
NIST security-identity separation                    ALREADY STRONGER / confirmation
IAM Principal as domain primitive                    NOT APPLICABLE
```

V3 result:

```text
CORE-01..13    PASS / PASS WITH HARDENING
MA-01..20      PASS / PASS WITH HARDENING
XCON-01..06    PASS / PASS WITH HARDENING
ADS            complete
REOPEN         0
unclassified   0
```

---

# 11. Representation SAFE DEFERRED dependencies

All are non-blocking with owner/trigger/tests in the Representation checkpoint:

```text
exact Principal/AuthN/AuthZ/enforcement
technical impersonation mechanics
action-specific delegability/policy
legal/specialist representation capacity
represented Agreement/Consent legal validity
Version/material scope
multi-hop delegation persistence
Verification of representation basis
Organization/group/collective representation
retention/audit/privacy
AI/service delegation chain
exact persistence/cardinality/API representation
```

---

# 12. Representation regression additions

```text
R-REP-01 valid bounded Representation → revocation → later attempt
R-REP-02 represented Person != actual Actor != Account != Principal != Authority basis
R-REP-03 guardian/parent Authority concerning child != child's personal Agreement/Consent/will
R-REP-04 helper records statement without automatic Representation
R-REP-05 AI/service policy → AI Actor preserved; no human authorship/Decision
R-REP-06 unauthorized re-delegation
R-REP-07 technical impersonation/shared credential → actual Actor preserved
R-REP-08 shared represented effect + private representation/delegation basis
```

---

# 13. Representation propagation scope — completed

Pre-scope:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Approved unique paths: **25**.

### CREATE

```text
docs/domain/concepts/representation.md
docs/domain/checkpoints/representation-delegation-principal-v0-validation.md
```

### UPDATE — current state

```text
docs/domain/language-map.md
docs/domain/README.md
docs/workstreams/domain-model.md
docs/domain/multi-actor-readiness-v1.md
```

### UPDATE — downstream closures

```text
docs/domain/concepts/person.md
docs/domain/concepts/actor.md
docs/domain/checkpoints/person-actor-account-v0-validation.md
docs/domain/concepts/authority.md
docs/domain/checkpoints/authority-v0-validation.md
docs/domain/concepts/participation.md
docs/domain/checkpoints/participation-v0-validation.md
docs/domain/concepts/acknowledgement.md
docs/domain/checkpoints/acknowledgement-v0-validation.md
docs/domain/concepts/confirmation.md
docs/domain/checkpoints/confirmation-v0-validation.md
docs/domain/concepts/decision.md
docs/domain/checkpoints/decision-v0-validation.md
docs/domain/concepts/agreement.md
docs/domain/concepts/consent.md
docs/domain/checkpoints/agreement-consent-v0-validation.md
docs/domain/concepts/provenance.md
docs/domain/checkpoints/provenance-v0-validation.md
docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md
```

Intentionally untouched:

```text
Visibility concept/checkpoint
Responsibility concept/checkpoint
Actual
Schedule/Time
Resource
Cross-Cluster v4
product discovery/research/simulations
old product glossary
root README
PROJECT-STATUS
main
prototype
SQL/API/auth/backend implementation
Version concept
```

---

# 14. Representation post-write QA — PASS

Validated against `b6c53ffa40ba7c1c1408f583856617a0e000f31b`.

```text
approved unique paths changed          25 / 25
new files                                2 / 2
modified files                          23 / 23
out-of-scope paths                       0
structural REOPEN                        0
unclassified material dependencies      0
main                                    c5120ff463e027c42f4a26fc613d0917596ca738
branch behind main                       0
```

Validated:

- full V3 coverage;
- hardenings incorporated;
- every SAFE DEFERRED item has owner/trigger/test set;
- actual Actor != represented party;
- Person/Actor/Account/Principal split intact;
- Representation != Authority/Responsibility/Subject/Provenance;
- representative action does not fabricate Ack/Confirmation/Agreement/Consent/Decision;
- Delegation remains bounded Authority semantics;
- Principal remains security-only;
- technical impersonation is not domain truth;
- historical checkpoints retain original material plus downstream amendments;
- Clusters 1–4 checkpoint preserves historical content and adds Representation appendix;
- no out-of-scope implementation/global/product-evidence changes;
- branch behind main = 0.

The Representation write approval is **consumed**.

---

# 15. Previous QA-closed milestones

```text
Acknowledgement v0    PASS WITH HARDENING — QA PASS
Decision v0           PASS WITH HARDENING — QA PASS
Agreement/Consent v0  PASS WITH HARDENING — QA PASS
Representation v0     PASS WITH HARDENING — QA PASS
```

Associated rejected universal abstractions remain rejected.

---

# 16. Current next action

Run a **fresh re-score** of the remaining demonstrated candidate/dependency space.

Examples:

```text
Version / material equivalence
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Dependency
Coordination Stewardship
Contribution
GoalCriterion / evaluation
Evidence ↔ Criterion/evaluation
Resource Requirement / Allocation / Reservation / substitution
Verification / comprehension
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/quorum semantics
Principal/AuthN/AuthZ implementation boundary
legal/specialist representation capacity
retention/audit
Personal Knowledge generic link layer
```

No candidate is preselected. Version ranked second before Representation but must compete again against the updated dependency graph.

After selection:

```text
one full V3 cycle
↓
propagation analysis
↓
STOP BEFORE NEXT GIT WRITE
```

---

# 17. Before broad implementation

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
backend implementation
```

No final SQL/API jump from the current semantic stage.

---

# 18. Git / handoff discipline

`main` remains integrated source of truth. `feature/domain-model` is newer only inside its unmerged Domain Model scope.

For every future write:

```text
state branch + exact files + pre-scope SHA
↓
explicit approval
↓
write only approved scope
↓
QA against pre-scope SHA
↓
approval consumed
```

Do not place critical project state only in chat. Update this handoff after every validated milestone.
