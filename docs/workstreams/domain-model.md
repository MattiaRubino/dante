# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Representation / on-behalf-of v0 propagated, post-write QA pending**
- Active branch: `feature/domain-model`
- Upstream baseline: `main` at `c5120ff463e027c42f4a26fc613d0917596ca738`
- Pre-scope validated commit for the current Representation milestone: `b6c53ffa40ba7c1c1408f583856617a0e000f31b`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current completed QA-closed Cluster-5 reviews: **Relationship, Responsibility, Participation, Authority, Visibility, Acknowledgement, Decision, Agreement / Consent**
- Current milestone under post-write QA: **Representation / on-behalf-of v0 — PASS WITH HARDENING, hardenings incorporated, propagation complete pending diff QA**.
- Generic cross-domain **Acceptance / Assent is rejected as a standalone kernel primitive**.
- Universal **Approval**, **Reconciliation**, **EffectiveChange/state-transition**, **Contract**, and **Consent/Permission** roots remain rejected.
- Representation review additionally rejects **Principal as a LifeOS domain primitive**, **universal Delegation/Agent/Representative roots**, and **technical impersonation as domain attribution truth**.
- Current exact task: **finish post-write QA for the approved 25-path Representation v0 propagation against `b6c53ffa...`; do not re-score another candidate before QA PASS**.
- Next exact task after QA PASS: **fresh re-score of remaining Relationships / Reasoning candidate/dependency space by dependency leverage; no candidate is preselected**.

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
19. [`../domain/concepts/representation.md`](../domain/concepts/representation.md)
20. [`../domain/checkpoints/representation-delegation-principal-v0-validation.md`](../domain/checkpoints/representation-delegation-principal-v0-validation.md)
21. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect only concepts pressured by the next selected review.

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

No material `TBD`, unnamed future dependency or generic `review later` is valid.

Once a candidate review starts, execute the whole V3 autonomously. Stop only for a true REOPEN/user decision or at the Git write gate.

After a coherent review:

1. state exact branch;
2. state exact pre-scope commit;
3. state exact create/update file scope;
4. wait for explicit user approval;
5. write only approved paths;
6. QA full diff against pre-scope commit;
7. confirm no out-of-scope path changed;
8. consume approval after QA;
9. only then fresh re-score.

Canonical rule:

```text
V3 verdict in chat
!= accepted Domain Atlas baseline

accepted baseline
= completed V3
+ hardenings incorporated
+ documentation propagation
+ approved Git write
+ post-write QA PASS
```

Historical checkpoints/evidence are preserved. Later resolutions are appended as explicit downstream closures rather than retroactive rewrites.

---

# 3. Product / evidence rules

LifeOS is a **personal-first adaptive personal operating system**, not an enterprise workflow suite, IAM product, contract platform, clinical system or provider clone.

External apps, standards, APIs and specialist systems are benchmark evidence, never design authority.

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

Terminology precedence:

1. accepted concept spec;
2. Language Map;
3. current validation/checkpoint guardrails;
4. this handoff;
5. current product docs;
6. historical product docs/glossaries;
7. conversation memory.

A UI/product noun does not create a primitive. Historical checkpoints are not silently rewritten for terminology uniformity.

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
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

Representation v0 is the current milestone and remains outside the QA-closed baseline until the current post-write QA finishes.

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
universal cross-domain Acceptance / Assent root
universal Approval root
universal Reconciliation root
universal EffectiveChange / StateTransition root
Decision object for every mutation
universal Agreement / Contract root
universal Consent / Permission root
Principal as LifeOS domain primitive
universal Agent / Representative root
universal Delegation root
blanket delegation
technical impersonation as domain attribution truth
```

Do not reintroduce rejected abstractions under new names without an explicit reopening with stronger evidence.

---

# 8. Representation / on-behalf-of v0 — current milestone

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

Current classification:

```text
REPRESENTATION / ON-BEHALF-OF
CANONICAL CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY

✅ actual Actor preserved
✅ represented party distinct
✅ bounded action/context
✅ may reference applicable Authority/delegation/policy/basis
✅ history-sensitive where material

❌ native entity/root
❌ universal Agent/Representative identity
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ represented person's will by implication
```

`Representative` is a contextual role, not native identity.

### Delegation

```text
bounded Authority-establishment / entrustment pattern
```

```text
❌ universal primitive/root
❌ blanket transfer
❌ Responsibility transfer by implication
❌ automatic re-delegation
```

### Principal

```text
technical authenticated/authorized request identity
security/logical model boundary
```

```text
Principal != Person
Principal != Actor
Principal != represented party
Principal != Authority
Principal != Representation
```

Principal as a LifeOS domain primitive is rejected.

### Technical impersonation

Potential implementation mechanism only.

```text
technical impersonation
!= domain attribution truth
```

The materially known actual Actor must not be overwritten.

---

# 9. Representation hardenings

Mandatory current rules:

```text
actual Actor != represented party
represented party != Subject/beneficiary automatically
Representation != Authority
claim of Representation != established Authority
Representation != Delegation
Representation != Responsibility
Representation != Provenance
Principal != semantic Actor
represented Person requires no synthetic Account
re-delegation not implied
revoked/expired basis != never existed
technical impersonation != authorship truth
AI/service action != human action
```

Action-specific delegability is mandatory:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

A representative action does not manufacture represented-party Acknowledgement, Confirmation, Agreement, Consent or Decision. Those represented effects are valid only where an applicable action-specific Authority/policy/specialist basis permits them, while the actual Actor remains attributable.

---

# 10. Representation evidence / V3 result

The read-only V3 selected Representation after a fresh dependency-leverage re-score, narrowly ahead of Version/material equivalence.

Internal pressure came from Person/Actor/Account, Participation response Actor, Authority, Acknowledgement, Confirmation, Decision, Agreement/Consent, Provenance and AI/service attribution.

External evidence classifications:

```text
RFC 8693 delegation actor/subject separation     ADAPT
RFC 8693 impersonation as domain truth           ANTI-PATTERN
FHIR Provenance who/onBehalfOf                    ADAPT
W3C PROV actedOnBehalfOf                          ADAPT
W3C delegation authority/responsibility coupling ANTI-PATTERN if copied literally
NIST SP 800-63-4 security-identity separation    ALREADY STRONGER / boundary confirmation
generic IAM Principal as domain primitive        NOT APPLICABLE
```

V3 gates:

```text
CORE-01..13   PASS / PASS WITH HARDENING
MA-01..20     PASS / PASS WITH HARDENING
XCON-01..06   PASS / PASS WITH HARDENING
ADS           complete
REOPEN        0
unclassified  0
```

---

# 11. Representation SAFE DEFERRED dependencies

All remain non-blocking with owner/trigger/tests in the Representation checkpoint:

```text
exact Principal/AuthN/AuthZ/enforcement
technical impersonation mechanics
action-specific delegability/policy
legal/specialist representation capacity
represented Agreement/Consent legal validity
Version/material scope
multi-hop delegation-chain persistence
Verification of representation basis
Organization/group/collective representation
retention/audit/privacy
AI/service delegation chain
exact persistence/cardinality/API representation
```

No material neighboring dependency is unclassified.

---

# 12. Representation regression additions

```text
R-REP-01 valid bounded Representation → revocation → later attempted action
R-REP-02 represented Person != actual Actor != Account != Principal != Authority basis
R-REP-03 guardian/parent Authority concerning child != child's personal Agreement/Consent/will
R-REP-04 helper records another Person statement without automatic Representation
R-REP-05 AI/service bounded policy → AI Actor preserved; no human authorship/Decision
R-REP-06 delegated Actor attempts unauthorized re-delegation
R-REP-07 technical impersonation/shared credential → material actual Actor preserved
R-REP-08 shared represented effect + private representation/delegation basis
```

---

# 13. Current approved Representation write scope

Pre-scope baseline:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Approved exact scope — **25 unique paths**:

### CREATE

```text
docs/domain/concepts/representation.md
docs/domain/checkpoints/representation-delegation-principal-v0-validation.md
```

### UPDATE — current canonical state

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

Out of scope:

```text
Visibility
Responsibility
Actual
Schedule / Time
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

# 14. Current QA gate — pending

The milestone is not accepted until full diff QA against:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Required checks:

```text
approved unique paths changed              25 / 25
new files                                    2 / 2
modified files                              23 / 23
out-of-scope paths                           0
structural REOPEN                            0
unclassified material dependencies          0
branch behind current main                   0
```

Semantic QA must confirm:

- full Representation V3 checkpoint: CORE-01..13, MA-01..20, XCON-01..06, ADS, adversarial log, regressions;
- actual Actor and represented party remain separate;
- Person/Actor/Account/Principal boundaries remain intact;
- Representation != Authority/Responsibility/Subject/Provenance;
- Delegation remains bounded Authority pattern, not root;
- Principal remains security-only;
- technical impersonation does not define domain attribution;
- representative action does not fabricate human Acknowledgement/Confirmation/Agreement/Consent/Decision;
- historical checkpoints are preserved with downstream appendices, especially Clusters 1–4;
- no main/prototype/root README/PROJECT-STATUS/product evidence/SQL/API/auth/backend changes.

Do not re-score another candidate until this QA passes.

---

# 15. Previous QA-closed milestones

## Acknowledgement v0

```text
PASS WITH HARDENING
post-write QA PASS
Generic Acceptance primitive REJECTED
```

## Decision v0

```text
PASS WITH HARDENING
post-write QA PASS
Approval scoped
Reconciliation process/pattern
Universal EffectiveChange rejected
```

## Agreement / Consent v0

```text
PASS WITH HARDENING
post-write QA PASS
Generic Assent rejected
Universal Contract rejected
Universal Consent/Permission root rejected
```

These remain part of the validated branch baseline.

---

# 16. Current next action

**Current:** finish Representation post-write QA only.

If QA passes:

```text
consume Representation write approval
↓
set final branch HEAD as new baseline
↓
fresh re-score remaining candidate/dependency space
↓
select one highest-leverage demonstrated candidate/family
↓
execute one complete V3 cycle
↓
propagation analysis
↓
STOP BEFORE NEXT GIT WRITE
```

No candidate is preselected. Version/material equivalence had the next-highest pressure in the prior re-score but must compete again after Representation becomes canonical.

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

`main` remains the integrated source of truth. This branch is newer only inside scoped unmerged Domain Model work.

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
