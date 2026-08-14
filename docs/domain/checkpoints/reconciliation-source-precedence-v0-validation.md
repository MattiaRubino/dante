# Reconciliation / Source Precedence v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — hardenings incorporated; post-write QA PASS  
**Validated:** 2026-08-13  
**Concept:** Reconciliation / Source Precedence v0  
**Validation standard:** `../validation-methodology-v3.md`  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `f2c28d0f4fe6ec6afe1b5934ec4279422a09605a`

---

# 0. Fresh candidate re-score

This review began only after Version / Material Equivalence v0 completed post-write QA. The workstream explicitly required a fresh re-score with no preselected candidate.

Candidates were compared using dependency leverage, amount of SAFE DEFERRED debt that could be closed, pressure from already accepted concepts, risk to logical-model readiness, cross-cluster impact, product value, ontology cost, specialist leakage and implementation prematurity.

Result:

```text
1  Detailed Reconciliation / Source Precedence       24
2  GoalCriterion / evaluation                        22
3  Proposal / request reusable identity              21
4  Trigger / conditional policy                      16
5  Resource Requirement / Allocation / Reservation  16
6  Verification / comprehension                      14
7  Dependency                                        14
8  Coordination Stewardship                          10
9  Contribution                                      10
10 collective / group / quorum                        5
```

Reconciliation ranked first because Version solved `which materially relevant states exist?` while intentionally leaving open `how should materially competing states/assertions be handled?`. That unresolved pressure already crosses Actual, Observation, Outcome, Confirmation, Evidence, Provenance, Authority, Decision, Schedule, providers, offline/sync and AI stale-base behavior.

No candidate was promoted because of roadmap vocabulary or external schema terminology.

---

# 1. Scope

Candidate family:

```text
Reconciliation
Conflict condition
Source Precedence
source-of-record policy
current/effective-state establishment under conflict
```

Primary question:

> **Which materially competing states or assertions concern this bounded target/question, what applicable resolution basis exists, and what — if anything — becomes the current/effective interpretation without rewriting history?**

Nearest accepted boundaries:

- Version;
- Provenance;
- Evidence;
- Actual;
- Observation;
- Outcome;
- Confirmation;
- Authority;
- Decision;
- Schedule;
- Representation;
- Agreement / Consent;
- Visibility.

Deliberately not designed:

- CRDT/OT;
- generic sync/merge engine;
- final source-priority tables;
- native Person/Asset identity merge/split;
- final provider mappings;
- collective/quorum rules;
- final Trigger/policy engine;
- security enforcement;
- retention/audit architecture;
- SQL/API.

---

# 2. Evidence

## EV-01 — Internal LifeOS evidence

Accepted semantics already require:

```text
Version preserves competing/divergent states but does not choose current state
Provenance preserves origin but does not choose winner
Evidence may conflict
Actual may have competing assertions
Observation conflicts must not be silently averaged/overwritten
Authority legitimizes bounded effect but is not objective truth
Decision is one possible bounded resolution
Schedule/provider conflicts must not use universal last-write-wins
AI stale-base proposals must be re-evaluated after material divergence
```

This demonstrates a repeated cross-domain process problem not owned by any single accepted concept.

**EV-01: PASS.**

## EV-02 — Workflow inversion

Representative workflows tested:

```text
user correction vs newer provider state
two credible sensors disagree
provider and current Schedule diverge
specialist source-of-record vs personal annotation
offline edits from one common base
same-facet concurrent conflict
independent-facet concurrent changes
AI proposal based on stale state
later Authority revocation after historical resolution
shared visible result with private competing source
collective disagreement followed by authoritative Decision
malicious/high-frequency provider updates
resolution producing a new material Version with multiple predecessors
```

Without an explicit reconciliation discipline these flows degenerate into recency, source identity, implicit Authority or ad-hoc family logic.

**EV-02: PASS.**

## EV-03 — External benchmark

Primary external benchmark evidence used during read-only validation:

| Benchmark | Finding | Classification | LifeOS treatment |
|---|---|---|---|
| RFC 9110 conditional requests / `If-Match` | detect stale base and prevent lost update | ADAPT | detection/concurrency support only; not semantic winner rule |
| HL7 FHIR version-aware updates | reject stale/concurrent update with explicit conflict/precondition behavior | ADAPT | reinforces conflict detection vs semantic resolution |
| Git three-way merge/conflicts | preserve competing states/base and allow unresolved conflict | ADAPT | history/conflict pattern; no universal Git ontology |
| Kubernetes Server-Side Apply conflict detection | field ownership + explicit resolution paths | ADAPT | explicit conflict/policy lesson only |
| Kubernetes field ownership as universal LifeOS governance | technical manager/ownership would leak into domain truth | ANTI-PATTERN | do not copy |
| W3C PROV source/revision lineage | lineage can explain state origins | NOT APPLICABLE as reconciliation rule | Provenance remains separate |

External convergence supports:

```text
detect divergence
→ preserve competing material states
→ retain source/base/context
→ apply explicit bounded resolution basis when valid
→ otherwise remain unresolved
```

No external noun is promoted automatically.

**EV-03: PASS.**

## EV-04 — Smallest candidate

Hypotheses:

```text
H0 Version + Decision + Authority + Provenance only             FAIL
H1 universal Reconciliation entity/root                         FAIL
H2 global SourcePrecedence rank                                 FAIL
H3 conflict entity/root                                          FAIL
H4 contextual Reconciliation reasoning/process capability       SURVIVES
H5 technical merge/sync owns domain reconciliation              FAIL
```

Smallest surviving result:

```text
Reconciliation
= cross-cutting contextual reasoning/process capability

Conflict
= contextual/derived condition

Source Precedence
= bounded contextual policy/basis when justified
```

**EV-04: PASS.**

---

# 3. Candidate definition / disposition

> **Reconciliation is the contextual cross-cutting reasoning/process capability through which LifeOS handles materially competing states, assertions or interpretations concerning the same bounded target, question or facet while preserving their identity, Version, Provenance, Evidence, Actor and Authority context. Reconciliation applies an explicit bounded resolution basis where one exists and may select, combine, correct, supersede, escalate, defer or intentionally retain conflict unresolved. Reconciliation does not itself establish objective truth, own the resulting domain state, or create universal source precedence.**

Canonical question:

> **Which materially competing states or assertions concern this bounded target/question, what applicable resolution basis exists, and what — if anything — becomes the current/effective interpretation without rewriting history?**

Disposition:

```text
Reconciliation                        CANONICAL cross-cutting process/capability
Conflict                              contextual/derived condition
Source Precedence                     contextual bounded policy/basis
universal Reconciliation root         REJECTED
universal Conflict root               REJECTED
universal SourcePrecedence rank       REJECTED
last-write-wins                       REJECTED as canonical policy
newest-source-wins                    REJECTED
provider-always-wins                  REJECTED
user-always-wins                      REJECTED
technical merge = domain truth        REJECTED
```

---

# 4. CORE Semantic Validation Gate

## CORE-01 — Real-world workflow inversion

People and systems already reconcile competing versions and assertions in everyday reality: comparing records, asking which source governs, correcting prior entries, choosing between conflicting provider/user states, combining compatible edits and sometimes leaving uncertainty unresolved.

LifeOS improves the workflow only if it preserves conflict and basis rather than silently forcing one current value.

**Result: PASS.**

## CORE-02 — Deep chronological simulation

Integrated chronology:

```text
T0 target state S1
T1 provider creates S2P from S1
T2 user offline creates S2U from S1
T3 LifeOS receives both
T4 conflict detected
T5 Provenance/Version/Actor/source context reconstructed
T6 applicable bounded policy checked
T7 policy insufficient → conflict remains unresolved
T8 later specialist Evidence arrives
T9 authorized Decision/process establishes S3
T10 S3 becomes current in owning domain concept
T11 later stronger information produces correction S4
T12 historical query reconstructs S2P, S2U, unresolved period, S3 basis and later S4
```

Required distinctions:

```text
conflict detection time != resolution time
current state != competing historical state
source time != receive time
Authority at action time != current Authority
resolution basis != objective truth
resolved != history erased
```

**Result: PASS WITH HARDENING.**

## CORE-03 — Adversarial reductio

```text
REMOVE Reconciliation discipline
→ FAIL: conflict handling becomes ad hoc/LWW/source-rank leakage.

MERGE Reconciliation + Version
→ FAIL: Version identifies divergence but cannot decide/handle it.

MERGE Reconciliation + Provenance
→ FAIL: lineage does not establish precedence or result.

MERGE Reconciliation + Evidence
→ FAIL: Evidence may conflict and need reconciliation itself.

MERGE Reconciliation + Authority
→ FAIL: Authority legitimizes effect but is not universal truth/source precedence.

MERGE Reconciliation + Decision
→ FAIL: some valid reconciliation is deterministic or unresolved; no human Decision required.

MAKE universal Reconciliation entity/root
→ FAIL: low-consequence conflict/correction becomes workflow bureaucracy.

MAKE global source priority
→ FAIL: source authority varies by facet/purpose/context/time.

MAKE last-write-wins canonical
→ FAIL: recency is not truth/Authority and destroys offline/provider conflict semantics.

contextual process/capability
→ SURVIVES.
```

**Result: PASS WITH HARDENING.**

## CORE-04 — Semantic redundancy / merge-split

| Pair | Classification | Reason |
|---|---|---|
| Reconciliation / Version | DISTINCT | competing state identity vs handling/resolution |
| Reconciliation / Provenance | DISTINCT | lineage vs result process |
| Reconciliation / Evidence | DISTINCT | evaluative support vs resolution process |
| Reconciliation / Authority | DISTINCT | legitimacy vs conflict handling |
| Reconciliation / Decision | DISTINCT | Decision may be one path/result; not every reconciliation is Decision |
| Reconciliation / Actual | DISTINCT | process vs current contextual realization |
| Source Precedence / source identity | DISTINCT | bounded policy vs origin identity |
| Conflict / Reconciliation | condition vs process | conflict may exist unresolved |
| Reconciliation / technical merge | DISTINCT | semantic vs transport/storage operation |

**Result: PASS WITH HARDENING.**

## CORE-05 — Multidirectional traceability

Downward:

```text
competing states/assertions
→ resolution basis
→ Reconciliation
→ Decision/policy where applicable
→ owning current/effective state
```

Upward:

```text
current/effective state
→ resolution history/basis
→ competing Versions/assertions
→ Provenance/Evidence/Actors
```

Lateral:

```text
one conflict set
→ different authorized projections/decisions without duplicating source facts
```

**Result: PASS.**

## CORE-06 — Orphan / independence

Valid:

- conflict remains unresolved;
- low-risk deterministic reconciliation without persistent object;
- current state with no historical conflict;
- Decision unrelated to any reconciliation;
- Version history with no conflict.

Invalid universalization:

- requiring a Reconciliation object for every correction/update;
- forcing every conflict to resolve.

**Result: PASS WITH HARDENING.**

## CORE-07 — External cross-domain benchmark

External systems distinguish conflict detection/concurrency/history from semantic resolution and commonly preserve unresolved conflict or require explicit policy/action.

**Result: PASS.**

## CORE-08 — External anti-pattern review

Rejected:

```text
last-write-wins
newest-source-wins
provider-always-wins
user-always-wins
creator/manager always wins
field manager = domain Authority
ETag/MVCC/technical merge = semantic winner
source identity = truth
```

**Result: PASS.**

## CORE-09 — Correction / epistemic integrity

A resolution must not rewrite what sources/assertions originally said.

Example:

```text
A asserted X
B asserted Y
resolution at T2 chooses Y for bounded context
```

Historical truth remains:

```text
A asserted X
B asserted Y
T2 basis/result selected Y
```

not:

```text
A always asserted Y
```

A later reversal/correction must preserve the prior result and basis.

**Result: PASS WITH HARDENING.**

## CORE-10 — Scale / performance / history

The semantics do not require:

- persistent conflict row for every concurrent write;
- storing every technical revision;
- retaining every rejected sensitive payload forever;
- running expensive universal source ranking;
- materializing all reconciliations as workflow instances.

Persistence depth is consequence-sensitive.

**Result: PASS WITH HARDENING.**

## CORE-11 — Simple user / power user

Simple UI:

```text
This changed somewhere else
Keep mine
Use updated value
Both changes can be kept
Needs review
```

Power/high-consequence UI may expose material diff, source/basis, conflict history, Authority, Decision and predecessors.

**Result: PASS.**

## CORE-12 — Product value / complexity cost

Value:

- prevents silent data loss;
- supports offline/provider conflict;
- improves AI safety;
- preserves epistemic integrity;
- prevents source/Authority laundering;
- provides explainability.

Cost is acceptable only if ordinary low-risk cases stay largely invisible and deterministic where safe.

**Result: PASS WITH HARDENING.**

## CORE-13 — Implementation pressure without premature schema

Future implementation must answer:

- what states/assertions conflict?;
- which target/facet/question do they concern?;
- what Version/Provenance/Actor/source context applies?;
- what bounded policy/Authority basis was used?;
- was conflict resolved, deferred or unresolved?;
- did a Decision occur?;
- what state became current in the owning concept?;
- did resolution create a new Version and predecessors?;
- what conflict/rationale/source history may a viewer see?;
- how do technical merge/concurrency and semantic resolution remain separate?

No final table/API/state machine is required now.

**Result: PASS WITH HARDENING.**

## CORE Gate

```text
CORE-01 PASS
CORE-02 PASS WITH HARDENING
CORE-03 PASS WITH HARDENING
CORE-04 PASS WITH HARDENING
CORE-05 PASS
CORE-06 PASS WITH HARDENING
CORE-07 PASS
CORE-08 PASS
CORE-09 PASS WITH HARDENING
CORE-10 PASS WITH HARDENING
CORE-11 PASS
CORE-12 PASS WITH HARDENING
CORE-13 PASS WITH HARDENING

CORE GATE
PASS WITH HARDENING
```

---

# 5. Mandatory hardenings — incorporated and retested

```text
REC-01  conflict detection != conflict resolution
REC-02  unresolved conflict is valid
REC-03  competing material states/assertions remain reconstructible
REC-04  no universal source priority
REC-05  newer != truer / more authoritative
REC-06  source identity != Authority != truth
REC-07  source precedence is target/facet/purpose/context/time scoped
REC-08  Version identifies competing states; it does not reconcile them
REC-09  Provenance explains origin; it does not choose a winner
REC-10  Evidence may support/contradict without determining the result
REC-11  Authority legitimizes bounded effect; it does not manufacture objective truth
REC-12  Decision is one possible resolution path, not mandatory for every reconciliation
REC-13  deterministic authorized reconciliation may occur without fabricated human Decision
REC-14  effective/current state remains owned by the affected domain concept
REC-15  reconciliation output may create a new material Version with preserved predecessors
REC-16  non-conflicting changes may be combined when semantically safe
REC-17  last-write-wins is never the universal canonical rule
REC-18  user-always-wins is rejected
REC-19  provider-always-wins is rejected
REC-20  specialist source-of-record precedence is bounded to actual authoritative context
REC-21  Actor stances/Ack/Agreement/Consent remain separate from result
REC-22  conflict/source/basis Visibility is independently governed
REC-23  AI may detect/explain/propose but cannot silently exceed policy/Authority
REC-24  technical merge/CRDT/ETag/MVCC != domain Reconciliation
REC-25  correction/reversal preserves prior resolution/assertion history
REC-26  low-consequence deterministic reconciliation should normally remain product-invisible
REC-27  native identity merge/split is not owned by this family
REC-28  persistence/formality is consequence-sensitive
```

Retest after incorporation produced no REOPEN.

---

# 6. Multi-Actor Compatibility Gate

## MA-01 — Identity / Account independence

Competing sources/Actors may be accountless people, devices, providers or external systems.

**PASS.**

## MA-02 — Shared canonical fact / Actor-scoped overlay

A shared target may have multiple Actor-specific assertions/stances against different Versions without duplicating the target.

**PASS WITH HARDENING.**

## MA-03 — Responsibility / assignment / hand-off

Role-state conflict may require reconciliation while Responsibility remains independently owned. Reconciliation does not become Assignment/Hand-off.

**PASS.**

## MA-04 — Stewardship / mental load

Routine conflict handling must not force one coordinator to manually review every technical divergence. Consequence-sensitive automation and product filtering are required.

**PASS WITH HARDENING.**

## MA-05 — Common ground / state separation

A reconciled shared result does not manufacture Acknowledgement, Agreement, Consent or identical participant stance.

**PASS.**

## MA-06 — Authority / canonical change

Resolution effect must respect applicable Authority/policy. Authority still does not equal objective truth or universal source precedence.

**PASS WITH HARDENING.**

## MA-07 — Selective disclosure

The result may be shared while conflict sources/rationale/history remain private.

**PASS WITH HARDENING.**

## MA-08 — Inference privacy

AI explanations and derived projections must not reveal hidden competing sources or private resolution basis.

**PASS WITH HARDENING.**

## MA-09 — Partial adoption / external participant

External/provider sources participate in reconciliation without synthetic LifeOS Account identity.

**PASS.**

## MA-10 — Assisted participation / on-behalf-of

Actual resolver Actor, represented party, source and Authority basis remain distinct.

**PASS WITH HARDENING.**

## MA-11 — Lifecycle / revocation

Authority/source-policy revocation affects future applicability without erasing historical valid resolution.

**PASS.**

## MA-12 — Conflict / adversarial relationship

This is the core case: disagreement may persist unresolved and must not be erased by recency or power unless bounded Authority/policy legitimately establishes the affected state.

**PASS WITH HARDENING.**

## MA-13 — Unequal power

An authoritative result is not renamed Agreement/Consent or the weaker party's stance. Source precedence must not become a hidden power hierarchy.

**PASS WITH HARDENING.**

## MA-14 — Resource / capacity

Future resource allocation conflicts can reuse the discipline without becoming Reconciliation semantics themselves.

**PASS.**

## MA-15 — Coordination burden

Auto-resolution is justified only where consequence/risk/policy permit. High-consequence ambiguity may require explicit review.

**PASS WITH HARDENING.**

## MA-16 — Formality / progressive disclosure

Casual use can hide Reconciliation; advanced/shared/specialist contexts may expose it.

**PASS.**

## MA-17 — AI Authority

AI may recommend/detect but cannot silently exceed Authority or convert confidence into canonical source precedence.

**PASS WITH HARDENING.**

## MA-18 — Specialist boundary

Specialist source-of-record policy may legitimately dominate a bounded facet without making the external system universally authoritative.

**PASS WITH HARDENING.**

## MA-19 — Primitive redundancy

No separate `SharedReconciliation`, `ProviderConflict`, `UserConflict` or actor-specific conflict primitive is justified.

**PASS.**

## MA-20 — Actor-scoped reality attribution

Shared current result does not rewrite which Actor/source asserted which competing state.

**PASS WITH HARDENING.**

## Multi-Actor Gate

```text
MA-01 PASS
MA-02 PASS WITH HARDENING
MA-03 PASS
MA-04 PASS WITH HARDENING
MA-05 PASS
MA-06 PASS WITH HARDENING
MA-07 PASS WITH HARDENING
MA-08 PASS WITH HARDENING
MA-09 PASS
MA-10 PASS WITH HARDENING
MA-11 PASS
MA-12 PASS WITH HARDENING
MA-13 PASS WITH HARDENING
MA-14 PASS
MA-15 PASS WITH HARDENING
MA-16 PASS
MA-17 PASS WITH HARDENING
MA-18 PASS WITH HARDENING
MA-19 PASS
MA-20 PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
```

---

# 7. Cross-Concept Consistency Gate

| Test | Applicable | Result | Closure |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS WITH HARDENING | reconciliation handles competing states of a coherent target; native identity merge/split stays separate |
| XCON-02 Ownership/Authority compatibility | yes | PASS WITH HARDENING | applicable Authority legitimizes effect but is not objective truth/source rank |
| XCON-03 Planned/current/Actual/history | yes | PASS WITH HARDENING | candidate/current/resolved/Actual/historical states remain distinguishable |
| XCON-04 Relationship compatibility | yes | PASS | no universal Relationship/Reconciliation root required |
| XCON-05 Multi-actor readiness | yes | PASS WITH HARDENING | shared result + Actor-specific assertions/stances coexist |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE REQUIRED | Reconciliation discipline canonical; Source Precedence remains bounded policy language |

```text
XCON GATE
PASS WITH HARDENING
```

Structural reopening of prior accepted concepts: **0**.

---

# 8. Adjacent Dependency Sweep

## RESOLVED

```text
Actual ↔ competing assertions ↔ Reconciliation
Version ↔ divergent states ↔ Reconciliation
Decision ↔ Reconciliation
Authority ↔ Reconciliation
Provenance ↔ Source Precedence
Evidence ↔ Reconciliation
Confirmation conflict ↔ Reconciliation
Observation conflict/correction ↔ Reconciliation
Outcome correction ↔ Reconciliation
Schedule/provider conflict ↔ Reconciliation
offline/concurrent divergence ↔ domain reconciliation
technical merge/concurrency ↔ domain reconciliation
AI stale-base conflict ↔ Reconciliation
universal last-write-wins                         REJECTED
universal newest-source-wins                      REJECTED
universal provider/user source hierarchy          REJECTED
```

## SAFE DEFERRED — exact per-domain/source precedence policies

**Unresolved:** exact bounded precedence rules for each family/provider/facet.  
**Why safe:** Reconciliation requires contextual policy and rejects universal ranking.  
**Owner:** owning domain/product policy.  
**Trigger:** a concrete family cannot determine bounded precedence without changing Reconciliation semantics.  
**Tests:** CORE-02/04/09/13; MA-06/11/12/18; XCON-02/03/04.

## SAFE DEFERRED — GoalCriterion / evaluation

**Unresolved:** explicit criterion/evaluation identity and historical rule applicability.  
**Why safe:** conflicting Evidence can remain preserved/reconciled without defining GoalCriterion now.  
**Owner:** GoalCriterion/evaluation review.  
**Trigger:** Goal/Milestone evaluation cannot reconcile conflicting Evidence without stronger criterion identity/lifecycle.  
**Tests:** CORE-03/04/05/09/13; MA-06/19; XCON-03/04.

## SAFE DEFERRED — Proposal / request reusable identity

**Unresolved:** cross-family reusable proposal/request identity.  
**Why safe:** Version can bind competing material proposal/request states now.  
**Owner:** Proposal/reasoning review.  
**Trigger:** cross-family conflict/review history duplicates or cannot target proposals precisely.  
**Tests:** CORE-02/03/04/06/13; MA-05/19; XCON-03/04.

## SAFE DEFERRED — Trigger / conditional policy

**Unresolved:** reusable condition/policy rule identity/execution.  
**Why safe:** deterministic reconciliation may apply explicit bounded policy without defining the generic policy engine here.  
**Owner:** Trigger/automation/policy review.  
**Trigger:** resolution rules require generic Trigger semantics inside Reconciliation.  
**Tests:** CORE-03/04/13; MA-06/17; XCON-03/04.

## SAFE DEFERRED — technical CRDT/OT/merge algorithms

**Unresolved:** operational collaborative/offline merge mechanics.  
**Why safe:** technical merge and semantic resolution are explicitly distinct.  
**Owner:** logical/sync implementation.  
**Trigger:** implementation cannot preserve domain conflict/Authority/materiality without changing Reconciliation semantics.  
**Tests:** CORE-08/10/13; MA-12/17; XCON-03.

## SAFE DEFERRED — native-entity duplicate merge/split

**Unresolved:** whether two Person/Asset/native identities refer to the same real entity.  
**Why safe:** current family only handles competing states/assertions of a coherent target identity.  
**Owner:** native identity reconciliation review.  
**Trigger:** ordinary conflict resolution requires deciding whether two native identities are one entity.  
**Tests:** CORE-03/04/06/09; MA-01/12; XCON-01/04.

## SAFE DEFERRED — specialist source-of-record mappings

**Unresolved:** exact provider/system authoritative scope maps.  
**Why safe:** bounded source-of-record semantics are allowed without hard-coded universal hierarchy.  
**Owner:** integration/specialist policy.  
**Trigger:** concrete integration cannot express authoritative scope without universal source precedence.  
**Tests:** CORE-07/08/09/13; MA-09/18; XCON-02/03.

## SAFE DEFERRED — collective/quorum resolution

**Unresolved:** collective Actor/quorum/voting formation of shared resolution.  
**Why safe:** shared result remains separate from individual stance.  
**Owner:** collective/group semantics.  
**Trigger:** ordinary collective resolutions require quorum/voting identity that cannot remain outside Reconciliation.  
**Tests:** CORE-04/06/12; MA-02/05/06/13/19/20; XCON-01/04/05.

## SAFE DEFERRED — Principal/AuthN/AuthZ enforcement

**Unresolved:** technical request identity and enforcement of resolver Authority/policy.  
**Why safe:** Actor/Authority/Representation/result remain semantically independent.  
**Owner:** security/logical model.  
**Trigger:** enforcement cannot preserve actual resolver Actor/basis/result without domain/security collapse.  
**Tests:** CORE-05/13; MA-06/10/17; XCON-01/02.

## SAFE DEFERRED — retention/audit

**Unresolved:** deletion/redaction/audit retention of competing states and resolution basis.  
**Why safe:** material history need not retain every sensitive payload forever.  
**Owner:** privacy/retention/security.  
**Trigger:** deletion/audit requirements make required conflict reconstruction impossible.  
**Tests:** CORE-02/09/10; MA-07/08/11/13; XCON-03.

## SAFE DEFERRED — physical representation/API

**Unresolved:** table/cardinality/state machine/API shape.  
**Why safe:** semantic queries/boundaries are fixed without implementation commitment.  
**Owner:** logical/physical model + API stage.  
**Trigger:** no strategy preserves conflict, basis, history and current result naturally.  
**Tests:** CORE-10/13; MA-07/12/17; XCON-01/03/04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 9. Adversarial log

| Scenario | Required result |
|---|---|
| newer provider state conflicts with prior user correction | recency alone does not win |
| two credible sources disagree | preserve both; unresolved is valid |
| specialist system is bounded source of record | precedence only within governed facet/context |
| offline edits touch independent facets | combine only if semantically non-conflicting |
| offline edits change same material facet | explicit conflict; no silent LWW |
| manager establishes governed Schedule over objection | current governed state may differ from personal stance; no fabricated Agreement |
| AI gives source A higher probability | recommendation/Evidence only; no silent winner |
| valid resolution at T1, Authority later revoked | historical T1 resolution remains reconstructible |
| source attribution later corrected | correction without rewriting historical assertion chain |
| group disagrees, authorized process decides | Decision/result != Agreement |
| malicious provider sends many newer updates | update count/recency does not establish precedence |
| current result shareable, source conflict private | selective disclosure preserved |
| no sufficient basis | conflict remains unresolved |
| merge creates new synthesis | new material Version with predecessors/Provenance preserved |
| same bytes, different authoritative context | content/hash equality does not decide precedence |
| technical CRDT merge succeeds but domain policy conflicts | technical success does not establish semantic result |

---

# 10. Reopening / dependency register

| Finding | Severity | Closure | Treatment |
|---|---|---|---|
| conflict detection vs resolution | STRUCTURAL | RESOLVED | canonical non-collapse |
| unresolved conflict | STRUCTURAL | RESOLVED | valid state |
| universal source rank | STRUCTURAL | REJECTED | bounded contextual precedence only |
| LWW/newest-wins | STRUCTURAL | REJECTED | no canonical recency policy |
| Reconciliation = Version | STRUCTURAL | REJECTED | state identity vs handling |
| Reconciliation = Provenance | STRUCTURAL | REJECTED | lineage vs handling |
| Reconciliation = Decision | STRUCTURAL | REJECTED | Decision optional path |
| Reconciliation = Authority | STRUCTURAL | REJECTED | legitimacy vs truth/process |
| effective state owner | HARDENING | RESOLVED | affected concept owns state |
| source precedence scope | HARDENING | RESOLVED | target/facet/purpose/context/time |
| historical assertion preservation | HARDENING | RESOLVED | no retroactive rewrite |
| AI resolution | HARDENING | RESOLVED | bounded proposal/action only |
| technical merge separation | HARDENING | RESOLVED | implementation != semantic truth |
| native identity merge/split | DEFERRED | SAFE DEFERRED | separate identity review |
| per-family precedence rules | DEFERRED | SAFE DEFERRED | owning policies |
| provider source-of-record mapping | DEFERRED | SAFE DEFERRED | integration/specialist |
| collective/quorum resolution | DEFERRED | SAFE DEFERRED | collective review |
| retention/audit | DEFERRED | SAFE DEFERRED | privacy/security |
| physical model/API | DEFERRED | SAFE DEFERRED | later gates |

---

# 11. Regression corpus additions

```text
R-REC-01 user correction vs newer provider state
R-REC-02 two credible sources contradict with no sufficient winner
R-REC-03 concurrent offline changes on independent facets
R-REC-04 concurrent same-facet conflict retained unresolved
R-REC-05 bounded specialist source-of-record precedence
R-REC-06 deterministic authorized policy resolves without fabricated human Decision
R-REC-07 AI stale-base proposal after divergent target change
R-REC-08 historical resolution remains after Authority revocation
R-REC-09 shared reconciled projection with private conflict/source
R-REC-10 collective disagreement + authoritative Decision without fabricated Agreement
R-REC-11 malicious/high-frequency provider cannot win by update count/recency
R-REC-12 reconciliation creates new material Version retaining multiple predecessors
R-REC-13 technical merge succeeds while semantic policy still conflicts
R-REC-14 source attribution corrected without rewriting original assertion
```

---

# 12. Verdict

```text
RECONCILIATION / SOURCE PRECEDENCE v0
PASS WITH HARDENING

Reconciliation discipline               CANONICAL
Conflict                                CONTEXTUAL / DERIVED CONDITION
Source Precedence                       BOUNDED CONTEXTUAL POLICY/BASIS
Universal Reconciliation root           REJECTED
Universal Conflict root                 REJECTED
Universal SourcePrecedence hierarchy    REJECTED
Last-write-wins canonical policy        REJECTED

CORE                                    PASS WITH HARDENING
MA                                      PASS WITH HARDENING
XCON                                    PASS WITH HARDENING
REOPEN                                  0
unclassified material dependencies      0
```

No prior accepted concept requires structural reopening.

The hardenings are incorporated and retested read-only. The approved propagation is complete and final post-write QA passes; acceptance is canonical on the active branch.

---

# 13. Cluster integration

**N/A — Relationships / Reasoning remains open.**

After this milestone is QA-closed, perform a fresh re-score of the remaining demonstrated candidate/dependency space. Do not preselect GoalCriterion, Proposal or any other remaining candidate merely because of the current ranking.

Cluster-5 integration, dedicated multi-actor stress and deferred-dependency closure occur only after remaining candidate reviews are complete.

---

# 14. Documentation propagation — approved scope

Pre-scope:

```text
f2c28d0f4fe6ec6afe1b5934ec4279422a09605a
```

Approved unique paths: **28**.

## CREATE

1. `docs/domain/concepts/reconciliation.md`
2. `docs/domain/checkpoints/reconciliation-source-precedence-v0-validation.md`

## UPDATE — current canonical state

3. `docs/domain/language-map.md`
4. `docs/domain/README.md`
5. `docs/domain/multi-actor-readiness-v1.md`
6. `docs/workstreams/domain-model.md`

## UPDATE — downstream semantic closures

7. `docs/domain/concepts/actual.md`
8. `docs/domain/checkpoints/actual-v0-validation.md`
9. `docs/domain/concepts/observation.md`
10. `docs/domain/checkpoints/observation-v0-validation.md`
11. `docs/domain/concepts/outcome.md`
12. `docs/domain/checkpoints/outcome-v0-validation.md`
13. `docs/domain/concepts/evidence.md`
14. `docs/domain/checkpoints/evidence-v0-validation.md`
15. `docs/domain/concepts/provenance.md`
16. `docs/domain/checkpoints/provenance-v0-validation.md`
17. `docs/domain/checkpoints/observed-reality-evidence-v0.md`
18. `docs/domain/concepts/confirmation.md`
19. `docs/domain/checkpoints/confirmation-v0-validation.md`
20. `docs/domain/concepts/authority.md`
21. `docs/domain/checkpoints/authority-v0-validation.md`
22. `docs/domain/concepts/decision.md`
23. `docs/domain/checkpoints/decision-v0-validation.md`
24. `docs/domain/concepts/version.md`
25. `docs/domain/checkpoints/version-material-equivalence-v0-validation.md`
26. `docs/domain/concepts/schedule.md`
27. `docs/domain/checkpoints/time-v0.md`
28. `docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`

Intentionally out of scope:

```text
root README
PROJECT-STATUS
product v1 core glossary
historical research/discovery evidence
Cross-Cluster v4 historical checkpoint
main
prototype
SQL/API/backend/auth/security implementation
CRDT/sync implementation
all future candidate concepts
```

Propagation rule:

> Historical concept/checkpoint material remains reconstructible. Downstream Reconciliation closures are appended/amended explicitly; they do not retroactively falsify what earlier checkpoints knew at their validation time.

---

# 15. Post-write QA requirements

Final post-write QA verified:

```text
branch = feature/domain-model
exact final HEAD
compare f2c28d0... → final HEAD
exactly 28 approved paths
2 CREATE + 26 UPDATE
0 out-of-scope paths
concept + checkpoint complete
CORE 01–13 complete
MA 01–20 complete
XCON 01–06 complete
ADS complete
all REC hardenings present
REOPEN = 0
unclassified = 0
unresolved conflict explicit
no universal source rank
no LWW/newest/provider/user universal rule
Version/Provenance/Evidence/Authority/Decision boundaries intact
effective/current state remains owned by affected concept
AI boundary explicit
Visibility/privacy boundary explicit
technical merge/CRDT remains implementation-only
historical checkpoints preserved
workstream current
root README / PROJECT-STATUS / product glossary / main / prototype / SQL/API/backend/auth untouched
compare to main: divergence recorded; synchronization is separately gated and is not a blocker for continued Cluster-5 semantic review
```

Approval is consumed only after final clean QA.

---

# 16. Final post-write QA closure — 2026-08-14

The original Reconciliation semantic milestone is closed against its approved pre-scope `f2c28d0f4fe6ec6afe1b5934ec4279422a09605a` with exactly the approved 28-path propagation (`2 CREATE + 26 UPDATE`) and no semantic out-of-scope path. The later preservation-first documentation reconstruction was reviewed for semantic neutrality: it preserved the Reconciliation invariants, SAFE DEFERRED ownership, regression corpus and rejected universal defaults.

Current closure:

```text
Reconciliation / Source Precedence v0   PASS WITH HARDENING — POST-WRITE QA PASS
CORE                                    PASS WITH HARDENING
MA                                      PASS WITH HARDENING
XCON                                    PASS WITH HARDENING
ADS                                     COMPLETE
REC-01..28                              PRESENT
REOPEN                                  0
unclassified                            0
```

The active branch may remain diverged from `main` while Relationships / Reasoning is completed. Upstream synchronization is a separate future scope and is not required to begin the next fresh candidate re-score. No next candidate is preselected.