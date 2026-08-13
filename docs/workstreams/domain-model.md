# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active; Reconciliation / Source Precedence v0 propagation complete; final QA pending**
- Active branch: `feature/domain-model`
- Current upstream `main`: `2739e96955974d1273e704905ace03f9ac478e05`
- Current branch pre-this-scope HEAD: `c06eab35b46fd043c1438cdd5a2d97885195650a`
- Reconciliation pre-scope baseline: `f2c28d0f4fe6ec6afe1b5934ec4279422a09605a`
- PR: none
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Accidental probe cleanup: **QA PASS** at `c06eab35b46fd043c1438cdd5a2d97885195650a`
- Reconciliation v0: **PASS WITH HARDENING — hardenings incorporated; 28-path propagation now complete; final diff/semantic QA pending**
- Current exact task: **run Reconciliation post-write QA against `f2c28d0...`, verify exactly 28 approved paths, no extras, preservation/coherence, V3 completeness, current-doc markers and main freshness**
- `main` contains one newer product-direction/North-Star commit. Its semantic impact was reviewed read-only and did not reopen Reconciliation; branch synchronization remains a separate Git scope.
- After Reconciliation QA PASS: **consume Reconciliation write approval, then resolve the separate main-sync gate before starting the next candidate review**.

## Purpose

Turn LifeOS product requirements into the smallest implementation-ready semantic model that survives real workflows without prematurely fixing specialist modules, collaboration/IAM infrastructure, final APIs or SQL tables.

Earlier product terminology and current product-direction documents are evidence inputs, not automatic ontology truth.

> **Accepted means current best decision, not immutable decision.**

---

# 1. Required reading

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

# 2. Mandatory operating procedure

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

# 3. Current validated baseline

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
Reconciliation v0               PASS WITH HARDENING — FINAL QA PENDING

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

# 4. Current Relationships / Reasoning decomposition

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

# 5. Reconciliation / Source Precedence v0

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

# 6. Reconciliation V3 result

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

# 7. Reconciliation propagation scope

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

# 8. Reconciliation SAFE DEFERRED debt

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

# 9. Product / North-Star evidence rule

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

Branch synchronization to that `main` commit is intentionally a separate Git scope.

---

# 10. Current exact next steps

```text
1. complete Reconciliation post-write QA against f2c28d0...
2. verify exactly 28 approved paths, no extras
3. verify concept/checkpoint V3 + hardenings + ADS
4. verify current docs coherent
5. verify historical checkpoints preserved
6. verify probe absent
7. compare against current main
8. if QA PASS, consume Reconciliation write approval
9. STOP before main synchronization
10. present separate main-sync scope
```

No next Relationships / Reasoning candidate may begin before the Reconciliation gate and main-freshness gate are closed.

---

# 11. Before broad implementation

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

# 12. Git / handoff discipline

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
