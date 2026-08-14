<!-- LIFEOS-CANONICAL-SPLIT document="domain-model.md" part="2" total="2" -->
> **Canonical document split — Part 2 of 2.** Parts 1–2 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](domain-model.md) · **Part 2**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# ACTIVE STAGE — Relationships / Reasoning

The stage is in progress.

Completed reviews:

```text
Relationship v0
PASS WITH HARDENING

Responsibility v0
PASS WITH HARDENING

Participation v0
PASS WITH HARDENING
```

**Do not treat the remaining candidate space as a checklist.** It currently includes:

```text
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Principal / delegation / on-behalf-of
Decision / reconciliation
Dependency
Stewardship standalone primitive question
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation relationship
Resource Requirement / Allocation / substitution
Verification
Version
AI Proposal
focus/context relations
Trigger / conditional policy
collective/group semantics
```

## NEXT-CANDIDATE SELECTION

Do not continue merely because a roadmap item is next in the old list. Re-score dependency leverage after Participation v0.

Current strongest pressure area is **common-ground / governance semantics**:

```text
Authority
Visibility
Acceptance / Acknowledgement
Delegation / on-behalf-of
Decision / reconciliation
```

Why this area now has high leverage:

- Responsibility role changes depend on policy/Authority/Acceptance without absorbing them;
- Participation invitation/response and on-behalf-of cases expose the same boundary;
- Confirmation already requires separation from Acceptance/Acknowledgement/Authority;
- Actual reconciliation and conflicting assertions depend on who may establish/override current truth;
- Visibility and relation visibility are repeatedly distinct across Subject, Resource, Responsibility and Participation;
- AI must not launder information access into disclosure or action Authority;
- Account/Principal semantics remain intentionally separate.

This is an **area to score**, not a pre-accepted list of primitives. Candidate formation must determine whether Authority and Visibility should be reviewed together or separately, whether Acceptance/Acknowledgement are distinct concepts/operations/states, and which dependencies must precede the others.

## Mandatory method

For every candidate/family:

```text
Evidence + candidate
→ Core Gate
→ Multi-Actor Gate
→ Cross-Concept Gate
→ Adjacent Dependency Sweep
→ verdict
```

No concept verdict may be saved with an unclassified material adjacent dependency.

---

# Required Cluster-5 pressure

Relationships / Reasoning must explicitly pressure:

- specific relation semantics vs one generic `related_to`;
- direct vs qualified relation threshold;
- symmetric/asymmetric/n-ary relation semantics where relevant;
- Responsibility vs expected/actual performer vs Resource eligibility vs Participation;
- open/claimable responsibility;
- hand-off request vs Acceptance vs effective responsibility change;
- stewardship/coordination burden vs execution responsibility;
- Participation response vs Actual Participation;
- Invitation vs Acceptance/Acknowledgement;
- Authority vs Visibility;
- Confirmation vs Acknowledgement / Acceptance / Verification;
- canonical-change Authority vs asserted reality / Confirmation / Provenance;
- Account/Principal/delegation/on-behalf-of;
- shared fact vs actor-scoped overlay;
- selective disclosure and inference privacy;
- Evidence/Criterion/Decision semantics;
- Provenance vs Version/Decision/Audit;
- Milestone attainment evaluation;
- Resource Requirement/Allocation/Reservation/history;
- Subject focus/context relations;
- AI proposal/action/authority boundaries;
- historical attribution after Account/relationship changes;
- deletion/revocation/retention implications.

---

# Before broad persistence/backend implementation

Still required after Relationships / Reasoning:

```text
whole-domain semantic regression
↓
whole-domain destructive redundancy test
↓
deep historical reconstruction
↓
whole-domain multi-actor stress
↓
privacy / authority stress
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

Do not jump directly from the current Cluster-5 work to SQL/API stabilization.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains at the integrated repository baseline and was not changed by the current semantic-review scopes;
- no PR for the domain branch yet;
- backend implementation was not changed here;
- Phase-4 prototype branch was not changed here;
- repository visibility does not change write-scope rules;
- before **any future Git write**, state the exact intended file/branch scope and wait for explicit user approval.

## New-chat / continuation handoff

A continuing or fresh chat should begin by reading this workstream plus:

1. `data-subjects-v0.md`;
2. `deferred-dependency-closure-clusters-1-4-v0.md`;
3. `cross-cluster-validation-v4.md`;
4. `relationship-v0-validation.md`;
5. `responsibility.md`;
6. `responsibility-v0-validation.md`;
7. `participation.md`;
8. `participation-v0-validation.md`.

Then inspect README + Language Map + Methodology v3 and the concept specs pressured by the next review.

Do **not** redo Clusters 1–4, Relationship v0, Responsibility v0 or Participation v0 from scratch unless stronger evidence exposes a real contradiction. Re-select the next Relationships / Reasoning candidate by dependency leverage, with common-ground/governance semantics now the strongest pressure area rather than a pre-accepted next primitive.

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.


- Status: **IN PROGRESS — Relationships / Reasoning active; Reconciliation / Source Precedence v0 post-write QA PASS**
- Active branch: `feature/domain-model`
- Current upstream `main`: `2739e96955974d1273e704905ace03f9ac478e05`
- Current branch pre-reconstruction HEAD: `0e2f4b621e640421e2d5c9c0dc80fb20ff79b4a0`
- Reconciliation pre-scope baseline: `f2c28d0f4fe6ec6afe1b5934ec4279422a09605a`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Accidental probe cleanup: **QA PASS** at `c06eab35b46fd043c1438cdd5a2d97885195650a`
- Reconciliation v0: **PASS WITH HARDENING — hardenings incorporated; 28-path propagation complete; final post-write QA PASS**
- Current exact task: **fresh re-score the remaining Relationships / Reasoning candidate space; do not preselect the next candidate**
- `main` contains one newer product-direction/North-Star commit. Its semantic impact was reviewed read-only and did not reopen Reconciliation. Synchronization remains a separate future Git scope and does not block completion of the current cluster.
- Current continuation rule: **finish Relationships / Reasoning candidate reviews and required Cluster-5 validation first; do not present or perform a `main` sync gate now**.

## Purpose

Turn LifeOS product requirements into the smallest implementation-ready semantic model that survives real workflows without prematurely fixing specialist modules, collaboration/IAM infrastructure, final APIs or SQL tables.

Earlier product terminology and current product-direction documents are evidence inputs, not automatic ontology truth.

> **Accepted means current best decision, not immutable decision.**

---


## 1. Required reading
Read in order:

1. `docs/domain/README.md`
2. `docs/domain/language-map.md`
3. `docs/domain/validation-methodology-v3.md`
4. `docs/domain/validation-execution-template-v3.md`
5. `docs/domain/multi-actor-readiness-v1.md`
6. `docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`
7. `docs/domain/checkpoints/cross-cluster-validation-v4.md`
8. Relationship / Responsibility / Participation / Authority / Visibility concepts + checkpoints
9. Acknowledgement concept + checkpoint
10. Decision concept + checkpoint
11. Agreement / Consent concepts + joint checkpoint
12. Representation concept + checkpoint
13. Version concept + checkpoint
14. Reconciliation concept + checkpoint
15. `docs/domain/checkpoints/multi-actor-evidence-synthesis-v0.md`

Then inspect only concepts pressured by the newly selected review.

Do not redo QA-closed concepts unless stronger evidence exposes an actual contradiction.

---


## 2. Mandatory operating procedure
One candidate/family at a time.

```text
fresh candidate selection / re-score
↓
problem + evidence formation
↓
EV-01 internal evidence
EV-02 workflow inversion
EV-03 external benchmark classification
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
regression additions
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

No material `TBD` or generic `review later` is valid.

After a coherent read-only review:

```text
state branch
+ exact pre-scope SHA
+ exact file scope
↓
explicit approval
↓
write only approved scope
↓
QA against pre-scope
↓
approval consumed only after QA PASS
↓
fresh re-score only then
```

---


## 3. Current validated baseline
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
Decision v0                     PASS WITH HARDENING — QA PASS
Agreement / Consent v0          PASS WITH HARDENING — QA PASS
Representation v0               PASS WITH HARDENING — QA PASS
Version v0                      PASS WITH HARDENING — QA PASS
Reconciliation v0               PASS WITH HARDENING — QA PASS

Generic Acceptance / Assent     REJECTED
Universal Approval              REJECTED
Universal EffectiveChange       REJECTED
Universal Contract              REJECTED
Universal Consent/Permission    REJECTED
Principal domain primitive      REJECTED
Universal Agent/Representative  REJECTED
Universal Delegation            REJECTED
Impersonation-as-domain-truth    REJECTED
Universal Version root/table    REJECTED
Universal Reconciliation root   REJECTED
Universal Conflict root         REJECTED
Universal SourcePrecedence rank REJECTED
Universal LWW/newest-wins       REJECTED
```

---


## 4. Current Relationships / Reasoning decomposition
```text
who acts?
→ Actor

who is accountable?
→ Responsibility

who is involved?
→ Participation

who may legitimately govern/effect?
→ Authority

what may be exposed?
→ Visibility

who explicitly took notice?
→ Acknowledgement

what bounded question was resolved?
→ Decision

which parties mutually assented?
→ Agreement

who permitted bounded action/use/exposure?
→ Consent

who actually acted for which distinct party?
→ Representation / on-behalf-of

which material target state matters?
→ Version / material equivalence

how are materially competing states/assertions handled?
→ Reconciliation / Source Precedence discipline

what state becomes effective/current?
→ affected domain concept

what actually happened?
→ Actual

how did the record/state arise?
→ Provenance
```

---


## 5. Reconciliation / Source Precedence v0
Canonical question:

> **Which materially competing states/assertions concern this bounded target/question, what applicable resolution basis exists, and what — if anything — becomes current/effective without rewriting history?**

Current classification:

```text
Reconciliation
= CANONICAL cross-cutting reasoning/process capability

Conflict
= contextual/derived condition
!= universal root

Source Precedence
= contextual bounded policy/basis when justified
!= universal source ranking
```

Core non-collapse:

```text
Reconciliation != Decision
Reconciliation != Authority
Reconciliation != Actual
Reconciliation != Version
Reconciliation != Provenance
Reconciliation != Evidence
Reconciliation != technical merge/sync
```

Mandatory hardenings include:

- conflict detection != conflict resolution;
- unresolved conflict is valid;
- newer/more frequent/more recent does not automatically win;
- source identity/Provenance/recency do not create Authority or truth;
- Source Precedence is bounded to target/facet/purpose/context/time;
- no universal source ranking;
- effective/current state remains owned by the affected concept;
- deterministic authorized resolution need not fabricate a human Decision;
- historical competing states/assertions remain reconstructible;
- result Visibility does not imply source/conflict/rationale Visibility;
- AI may detect/compare/propose but cannot silently invent canonical precedence;
- specialist source-of-record precedence remains context-bounded;
- CRDT/merge/ETag/MVCC/sync mechanics remain implementation concerns.

---


## 6. Reconciliation V3 result
```text
CORE-01..13     PASS / PASS WITH HARDENING
MA-01..20       PASS / PASS WITH HARDENING
XCON-01..06     PASS / PASS WITH HARDENING
ADS             complete
REOPEN          0
unclassified    0
```

Regression additions cover:

- user correction vs newer provider state;
- credible conflicting sources with no sufficient winner;
- independent concurrent changes;
- same-facet unresolved conflict;
- bounded specialist source-of-record;
- deterministic authorized resolution without fabricated human Decision;
- stale-base AI proposal after material divergence;
- historical resolution under later-revoked Authority;
- shared result with private competing source;
- authoritative Decision without fabricated Agreement;
- high-frequency source unable to win by recency/count;
- reconciliation creating a new material Version with predecessor history.

---


## 7. Reconciliation propagation scope
Approved pre-scope:

```text
f2c28d0f4fe6ec6afe1b5934ec4279422a09605a
```

Approved scope:

```text
28 unique paths
2 CREATE
26 UPDATE
```

Current propagation includes:

- Reconciliation concept + V3 checkpoint;
- current Language Map / Domain README / Multi-Actor Readiness / this handoff;
- Actual / Observation / Outcome;
- Evidence / Provenance / Confirmation;
- Authority / Decision / Version;
- Schedule / Time;
- integrated Observed Reality & Evidence checkpoint;
- historical Clusters 1–4 deferred-closure amendment.

The accidental `__schema_probe_do_not_create__` file was outside the Reconciliation semantic scope and has been removed in a separately approved cleanup commit.

---


## 8. Reconciliation SAFE DEFERRED debt
Still independently owned:

```text
per-domain/source precedence policies
GoalCriterion / evaluation
Proposal / request reusable identity
Trigger / conditional policy
technical merge / CRDT / sync algorithms
native-identity duplicate merge/split
specialist source-of-record mappings
collective/quorum resolution
Principal/AuthN/AuthZ enforcement
retention/audit of competing historical payloads
physical representation/cardinality/API
```

Each remains subject to its owner/reopening triggers in the Reconciliation checkpoint.

---


## 9. Product / North-Star evidence rule
The current `main` includes a newer LifeOS product-direction/North-Star document.

It is treated as product evidence, not Domain Atlas authority.

Read-only review found it consistent with the current semantic direction, including:

```text
history is not silently rewritten
plan != reality
external/source authorship remains attributable
user Authority remains bounded
conflict is coordinated rather than hidden
Effort != Execution != Outcome != Goal Progress
```

The last distinction materially increases future pressure on GoalCriterion/evaluation, but does not reopen Reconciliation.

Branch synchronization to that `main` commit remains a separately gated future Git scope and is not a prerequisite for completing Relationships / Reasoning.

---


## 10. Current exact next steps
```text
1. fresh-score the remaining Relationships / Reasoning candidate space against the full accepted baseline
2. select the next candidate by dependency leverage, with no preselection
3. execute the complete Methodology v3 cycle
4. stop at the next Git write gate
5. repeat until the Relationships / Reasoning candidate space is complete
6. run Cluster-5 integration
7. run Cluster-5 multi-actor stress
8. run Cluster-5 deferred-dependency closure
9. keep `main` synchronization as a separate later scope; do not block steps 1–8 on it
```

Reconciliation is QA-closed. No next candidate is preselected.

---


## 11. Before broad implementation
```text
finish remaining Relationships / Reasoning candidate reviews
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


## 12. Git / handoff discipline
`main` is the integrated source of truth. `feature/domain-model` may be newer only inside its scoped unmerged Domain Model work.

For every write:

```text
branch + pre-scope + exact paths
↓
explicit approval
↓
write only approved scope
↓
QA against pre-scope
↓
approval consumed only after clean QA
```

Do not keep critical project state only in chat.

---

# 2026-08-14 — Repository-state correction

The preservation-first reconstruction is complete and QA-closed on `feature/domain-model`. The accidental technical probe was already removed and QA-closed before reconstruction, and the historical-preservation audit remains intact. Reconciliation semantic propagation and final post-write QA are complete. The current operating decision is to finish Relationships / Reasoning plus the required Cluster-5 integration/stress/dependency closure before any separately gated synchronization with `main`.

`Relationship v0` remains a checkpoint-backed typed/specific relationship modeling discipline. `docs/domain/concepts/relationship.md` does not exist by design and must not be recreated merely to satisfy navigation symmetry.
