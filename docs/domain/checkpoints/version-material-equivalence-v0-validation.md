# Version / Material Equivalence v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted current baseline; post-write propagation QA PASS  
**Validated:** 2026-08-13  
**Concept:** Version / Material-State v0  
**Validation standard:** `../validation-methodology-v3.md`  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`

---

# 0. Fresh candidate re-score

This review began only after Representation / On-Behalf-Of v0 completed post-write QA and the workstream required a fresh re-score with no preselected next candidate.

Remaining high-signal candidate families were compared on:

1. number of already accepted semantics that materially depend on the unresolved question;
2. risk of losing identity, history, truth, actor-specific state, Authority or privacy if deferred;
3. whether the problem is domain-semantic now or can safely remain logical/security/specialist work;
4. cross-cluster leverage;
5. product complexity cost.

Result:

```text
1  Version / material equivalence / revision applicability
2  detailed reconciliation / source precedence
3  Proposal / request reusable identity
4  GoalCriterion / evaluation
5  Resource Requirement / Allocation / Reservation
6  Trigger / conditional policy
7  Verification / comprehension
8  collective / group / quorum
9  coordination Stewardship
```

Version / Material-State ranked first because already accepted semantics repeatedly need the same answer:

> **Which state did this semantic act/evaluation actually concern, and can it still apply after change?**

The pressure is cross-cutting across Relationships / Reasoning, Observed Reality & Evidence, Time and Intention / Execution. Detailed reconciliation remains high priority but benefits from Version first because it must compare identifiable states rather than vague `latest records`.

No candidate was promoted because of vocabulary frequency alone.

---

# 1. Scope

- **Concept / family:** Version / Material-State + Material Equivalence / revision applicability.
- **Candidate version:** v0.
- **Date:** 2026-08-13.
- **Reviewer/workstream:** Core Domain Model v0 — Relationships / Reasoning.
- **Primary adjacent concepts:** Acknowledgement, Confirmation, Decision, Agreement, Consent, Authority, Participation, Responsibility, Representation, Actual, Observation, Outcome, Evidence, Provenance, Routine, Recurrence, Occurrence, Schedule, Milestone.
- **Secondary adjacent areas:** reconciliation/source precedence, GoalCriterion/evaluation, Trigger/policy, integration/provider mapping, privacy/retention, logical persistence, technical concurrency.

## Why this review exists

Multiple accepted concepts currently contain local rules equivalent to:

```text
semantic fact/action applied to material state v1
later materially changed state v2
→ historical v1 fact remains reconstructible
→ v1 semantic effect does not silently become v2 effect
```

Examples:

- Acknowledgement of a changed Schedule;
- Confirmation of an Observation state;
- Agreement on materially specific terms;
- Consent for bounded scope/purpose;
- Decision/Approval of a proposal;
- Responsibility hand-off response;
- Participation response to a materially changed occurrence/invitation;
- Evidence evaluation using historical source/rule state;
- Occurrence generated under a prior Routine/Recurrence policy.

The review tests whether a common semantic capability is justified, and if so whether it can remain smaller than a universal Version entity/root or event-sourced history model.

Primary risks:

- every technical write becoming a domain revision;
- target identity being confused with state identity;
- one global materiality flag invalidating unrelated semantics;
- provider/ETag/MVCC versions becoming domain truth;
- Version duplicating Provenance, Decision or reconciliation;
- forcing linear history despite offline/concurrent divergence;
- version-history privacy becoming a data-retention bypass;
- adding ontology/version bureaucracy to ordinary UI.

---

# 2. Evidence reviewed

## 2.1 Internal evidence

Reviewed current accepted Domain Atlas semantics and checkpoints, especially:

- Acknowledgement / generic Acceptance;
- Confirmation;
- Decision / Approval / Reconciliation boundary;
- Agreement / Consent;
- Authority;
- Participation;
- Responsibility;
- Representation / On-Behalf-Of;
- Actual / Observation / Outcome / Evidence / Provenance;
- Observed Reality & Evidence cluster checkpoint;
- Routine / Recurrence / Occurrence / Schedule;
- Time cluster checkpoint;
- Milestone;
- Intention & Execution cluster checkpoint;
- Multi-Actor Readiness v1;
- Deferred Dependency Closure — Clusters 1–4;
- Cross-Cluster Validation v4;
- current Language Map and workstream handoff.

Representative inherited rules:

```text
Ack(v1) does not silently acknowledge materially changed v2
Confirmation(v1) does not silently confirm materially changed v2
Agreement to terms v1 does not silently become Agreement to terms v2
Consent for scope/purpose v1 does not silently expand to v2
Decision approving P4 does not automatically approve materially revised P5
historical Evidence basis must remain reproducible where material
Occurrence history must preserve which policy/version governed it
correction must not falsify earlier source/assertion/evaluation history
```

The repeated requirement is semantic state binding, not merely storage history.

## 2.2 Representative LifeOS workflows

Tested:

1. Schedule change acknowledged at one time then materially rescheduled again;
2. non-material title/format correction that must not force renewed Acknowledgement;
3. Agreement price/terms amendment;
4. Consent purpose/scope expansion;
5. Participation acceptance before material Event-time change;
6. Responsibility hand-off response before scope expansion;
7. Decision approving one proposal state while later state differs;
8. Observation typo correction after earlier Confirmation/Evidence use;
9. Outcome correction by later authoritative information;
10. Routine `this and future` change preserving old Occurrence source policy;
11. concurrent/offline edits from one base state;
12. conflicting provider/user updates;
13. AI proposal prepared against a base state that changes before effect;
14. hidden private source changes while exposed projection remains equivalent;
15. Milestone redefinition crossing the identity-vs-Version boundary;
16. retention/redaction removing old payload while preserving minimum historical applicability.

## 2.3 External benchmark evidence

External sources are benchmark evidence, never LifeOS design authority.

### HL7 FHIR Resource versioning

FHIR distinguishes infrastructure/server record version (`meta.versionId`) from business-version concepts used by some artifacts. FHIR's server record version changes with resource updates, while significance/business-version behavior depends on context.

Classification:

| Finding | Classification | LifeOS use |
|---|---|---|
| technical record version and business/domain version are distinct concerns | BORROW | reinforces semantic-vs-storage separation |
| `meta.versionId` changes on server resource update | ANTI-PATTERN if generalized as LifeOS materiality | every storage update must not invalidate domain assent/state |
| version identifier need not be treated as semantic ordering/value | ADAPT | LifeOS state references need not be monotonic integers |

### W3C PROV-O

PROV-O distinguishes entity/activity/agent lineage and includes revision/derivation relationships such as `prov:wasRevisionOf`.

Classification:

| Finding | Classification | LifeOS use |
|---|---|---|
| revision lineage can be represented separately from identity/current state | ADAPT | Version may have Provenance without becoming Provenance |
| adopt complete PROV ontology as LifeOS Version model | NOT APPLICABLE | too broad and provenance-centric |

### HTTP conditional requests — RFC 9110

Entity tags and `If-Match` support conditional requests and stale-write/lost-update protection at representation/protocol level.

Classification:

| Finding | Classification | LifeOS use |
|---|---|---|
| conditional update against expected representation | ADAPT | useful future optimistic-concurrency pattern |
| ETag equals LifeOS semantic material Version | NOT APPLICABLE | protocol validator cannot decide Agreement/Consent/Ack materiality |

### Git object/history model

Git demonstrates reconstructible snapshots and parent-linked history while keeping object content and commit history distinct.

Classification:

| Finding | Classification | LifeOS use |
|---|---|---|
| reconstructible state snapshots/history | ADAPT | evidence that state references/history can be stable |
| universal Git-like commit DAG for every LifeOS domain target | ANTI-PATTERN | excessive storage/workflow model for personal-first kernel |

## 2.4 External evidence gate

```text
BORROW / ADAPT patterns found           yes
anti-patterns identified                yes
provider/standard schema copied         no
external vocabulary promoted directly   no
```

**Result: PASS.**

---

# 3. Candidate definition

> **Version / Material-State is the cross-cutting semantic capability through which LifeOS can identify and reconstruct a materially relevant state of an otherwise stable domain target, bind semantic actions, attestations, permissions, evaluations or decisions to the state they actually concerned, and determine — according to the owning semantic purpose — whether a later state remains materially equivalent for that use. Version does not define target identity, explain lineage, choose canonical state, decide reconciliation, or turn every technical write into a domain revision.**

## Domain question answered

> **Which materially relevant state of this target did this semantic act or evaluation concern, and does a later state remain equivalent for that specific purpose?**

## Identity

Version/material state does not create a second native target identity.

Conceptually:

```text
stable target identity T
  ├─ material state S1
  ├─ material state S2
  └─ divergent states S3A / S3B where reality requires
```

A state may require durable/reconstructible identity/reference where another semantic fact depends on it. That does not imply one universal `Version` aggregate root.

## Independent/contextual existence

- a domain target may exist with no explicit persisted Version object;
- low-consequence changes may be represented without durable material-state identity if history/applicability is unaffected;
- Version/state semantics become material when history, semantic binding, correction, concurrent divergence, evaluation reproducibility or other consequence requires them.

## Nearest boundaries

```text
Version != target identity
Version != Provenance
Version != Decision / Approval
Version != Authority
Version != reconciliation/source precedence
Version != provider revision
Version != ETag / MVCC token
Version != content hash
material equivalence != universal object equality
```

## Deliberate deferrals

- exact physical version representation;
- branch/merge algorithms;
- per-family material-equivalence rules;
- source-precedence/reconciliation policy;
- technical optimistic-concurrency mechanism;
- effective-dating schema;
- provider mapping implementation;
- retention/tombstone/redaction classes;
- GoalCriterion/Trigger rule snapshots;
- native identity replacement thresholds beyond current owning-concept invariants.

---

# 4. Core Semantic Validation Gate

## CORE-01 — Workflow inversion

Without LifeOS, people commonly act against a specific version of reality even if they do not call it a version:

- `I agreed to the price you sent yesterday`;
- `I saw the 15:00 change, not the later 16:00 one`;
- `I approved that draft, not this revision`;
- `I consented to sharing free/busy for this trip, not the expanded purpose`;
- `that evaluation was based on the old measurement/rule`.

A system that stores only current values destroys this context.

LifeOS improvement:

- preserve what state mattered;
- distinguish harmless from material change by semantic purpose;
- preserve history without making every edit user-visible bureaucracy.

**Result: PASS.**

## CORE-02 — Deep chronology

Integrated chronology:

```text
T0 Schedule state S1 = 15:00
T1 Luca acknowledges S1
T2 title capitalization correction → technical revision only for Ack purpose
T3 Schedule state S2 = 16:00 → material for Ack
T4 Luca acknowledges S2

T5 Agreement terms A1: EUR 100 / 24h cancellation
T6 non-material formatting clarification
T7 price becomes EUR 120 → material terms state A2

T8 Consent C1: free/busy / Trip A
T9 private source note changes but projection unchanged
T10 purpose expands to unrelated AI training → material Consent-scope state C2

T11 Decision D1 approves proposal P4
T12 proposal materially revised to P5

T13 offline actor edits from P4 while provider/user state P5 exists
T14 AI prepared patch against P5
T15 target becomes P6 before AI effect

T16 historical query asks what each actor saw/assented/confirmed/approved and what was effective then
```

Required distinctions survive if Version is purpose-sensitive and non-linear where necessary.

Hardening:

- semantic state time, recorded time, action time and effect time must not be collapsed;
- state history may branch;
- applicability is not inherited solely by same target ID.

**Result: PASS WITH HARDENING.**

## CORE-03 — Reductio

### REMOVE Version/material-state discipline

Fails because each family either invents its own state identity or silently binds to latest/current values.

### MERGE Version with target identity

Fails because ordinary correction/reschedule can preserve target identity.

### MERGE Version with Provenance

Fails because lineage may explain how S2 arose without deciding which state an Agreement/Ack referred to.

### MERGE Version with Decision/reconciliation

Fails because divergent states can exist before any resolution, and a state can be referenced without selecting a winner.

### UNIVERSALIZE every write

Fails product semantics: capitalization/metadata/storage changes would spuriously invalidate unrelated Acknowledgement/Agreement/Consent/etc.

### UNIVERSAL linear sequence

Fails concurrent/offline/provider divergence.

### UNIVERSAL content/hash equivalence

Fails because identical bytes can sit under materially different Authority/purpose/context, while different bytes can be semantically equivalent for a bounded purpose.

Minimal candidate survives.

**Result: PASS WITH HARDENING.**

## CORE-04 — Redundancy / merge-split pair test

| Pair | Classification | Reason |
|---|---|---|
| Version / target identity | DISTINCT | state change can preserve identity |
| Version / Provenance | DISTINCT | state reference vs lineage |
| Version / Decision | DISTINCT | referenced state vs resolution |
| Version / Authority | DISTINCT | state vs governance capability |
| Version / reconciliation | DISTINCT | divergence/reference vs conflict resolution |
| Version / technical concurrency token | DISTINCT | semantic applicability vs storage/protocol freshness |
| material equivalence / content equality | DISTINCT | purpose-sensitive semantics vs bytes/fields |
| per-family target binding / common Version discipline | COMMON CAPABILITY | repeated same invariant without creating generic Assent/Response concepts |

No universal Version entity/root is justified.

**Result: PASS WITH HARDENING.**

## CORE-05 — Multidirectional traceability

Downward:

```text
target
→ material state
→ Ack/Confirmation/Agreement/Consent/Decision/response/evaluation
```

Upward:

```text
historical semantic action
→ exact/reconstructible material target state
→ target identity
```

Lateral:

```text
one target state
→ several independently visible semantic relations
```

without copying target data into every relation.

**Result: PASS.**

## CORE-06 — Orphan / independence

- target without explicit persisted Version object: valid;
- material state with no Ack/Decision/etc.: valid where history/revision matters;
- semantic action requiring target-state specificity without state binding: invalid where consequence would be lost;
- Version without a target identity/context: not meaningful as universal standalone domain identity.

Version is therefore a **cross-cutting state-reference capability**, not a universal independent root.

**Result: PASS WITH HARDENING.**

## CORE-07 — External benchmark

FHIR, PROV, HTTP concurrency and Git history all reinforce separation of technical revision, business/domain semantics, lineage, identity and concurrency.

LifeOS adopts the lessons, not their schemas.

**Result: PASS.**

## CORE-08 — Anti-pattern review

Rejected:

- `updated_at` as semantic Version;
- one monotonic version integer on every domain row;
- provider revision as native LifeOS identity;
- ETag as Agreement/Ack materiality;
- hash equality as semantic applicability;
- global `material_changed` flag;
- universal last-write-wins;
- event sourcing by default;
- version every field/write forever;
- one polymorphic Version root/table before logical review.

**Result: PASS.**

## CORE-09 — Correction / reconciliation / epistemic integrity

Stress:

```text
Observation O-v1 used by Evaluation E1
later corrected to O-v2
```

Current evaluation may use O-v2; E1 must not be rewritten as if it did.

Stress:

```text
provider state P2
user state U2
both from P1
```

Neither is erased merely because the other arrived later.

Stress:

```text
same textual content
but materially different Consent purpose/basis
```

content equality cannot decide applicability.

Version can preserve divergence and historical binding while leaving winner/merge to reconciliation/Authority/Decision.

**Result: PASS WITH HARDENING.**

## CORE-10 — Scale / performance / history

Ten-year personal history must not require:

- snapshot every unchanged technical write;
- Version object for every sensor tick;
- historical duplication into every Ack/Evidence relation;
- infinite future Routine versions/Occurrences;
- full private payload retention forever.

Valid implementation strategies may include direct state references, effective-dated history, snapshots, deltas, provider references, specialist storage or reconstructible derivation depending on consequence.

Semantic correctness does not choose one.

**Result: PASS WITH HARDENING.**

## CORE-11 — Simple user / power user

Simple UI can show:

```text
Changed from 15:00 to 16:00
Updated after you responded
Review changes
```

without exposing `Version v7`.

Power/high-consequence UI may show state history, actor action binding, material diff, provenance and conflicts.

**Result: PASS.**

## CORE-12 — Product value / complexity cost

Value:

- prevents stale assent/permission/approval laundering;
- preserves explanation/history;
- supports safer AI and offline/provider reconciliation;
- reduces duplicated per-family revision logic.

Cost becomes unacceptable if ordinary edits require manual version management or every write becomes a semantic revision.

Hardening:

> persistence/formality is consequence-sensitive and usually hidden.

**Result: PASS WITH HARDENING.**

## CORE-13 — Implementation pressure without premature schema

Future implementation must be able to answer:

- what state did this Actor acknowledge?;
- did this Agreement apply before or after the amendment?;
- did the approved proposal materially change before effect?;
- which source/rule state supported historical evaluation?;
- which Routine policy generated this Occurrence?;
- did an AI patch use a stale base?;
- did two offline/provider states diverge from the same base?;
- what can this viewer see of current/history/provenance?;
- can old payload be redacted while preserving minimum history?

No final table/API decision is required now.

**Result: PASS WITH HARDENING.**

## Core Gate result

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

# 5. Multi-Actor Compatibility Gate

## MA-01 — Identity / Account independence

Target/state identity is not Account identity. External Persons/providers can act against material states without synthetic Accounts.

**PASS.**

## MA-02 — Shared fact / actor overlay

One shared target can have different actor-scoped semantic actions against different historical states:

```text
Anna Ack S1
Luca Ack S2
```

No per-actor duplicate target is needed.

**PASS WITH HARDENING.**

## MA-03 — Responsibility / assignment / claim / hand-off

A hand-off response to request state H1 does not automatically apply to materially broadened H2.

Version does not become Responsibility or generic Acceptance.

**PASS WITH HARDENING.**

## MA-04 — Stewardship / mental load

Version must not force coordinators to manually monitor every irrelevant technical change. Product should surface only material changes where consequence warrants.

**PASS.**

## MA-05 — Common ground / state separation

Acknowledgement, Participation response, Agreement and other common-ground semantics can refer to different material states without being collapsed.

**PASS WITH HARDENING.**

## MA-06 — Authority / canonical change

Authority may determine who can make a state/effect effective; Version merely identifies state/history.

A newer state is not canonical merely because it is newer.

**PASS WITH HARDENING.**

## MA-07 — Selective disclosure

Current target Visibility does not imply visibility of historical versions, actors, rationale or private source payloads.

**PASS WITH HARDENING.**

## MA-08 — Inference privacy

A safe projection may remain materially equivalent while hidden private source state changes. Explanations must not reveal the hidden changed source.

**PASS WITH HARDENING.**

## MA-09 — Partial adoption / external participant

Provider/external revision IDs can be retained as mapping/provenance without requiring LifeOS Account or becoming native Version identity.

**PASS.**

## MA-10 — Assisted participation / provenance

Represented/on-behalf-of action must bind the actual Actor to the state they acted against while preserving represented party and basis separately.

**PASS WITH HARDENING.**

## MA-11 — Relationship lifecycle / revocation

Later amendment/revocation changes future applicability without erasing legitimate historical state/action.

```text
current no Consent/Authority/etc.
!= never existed
```

**PASS WITH HARDENING.**

## MA-12 — Conflict / adversarial relationship

Different actors/providers may create divergent states. Version preserves conflict without universal LWW or forced consensus.

**PASS WITH HARDENING.**

## MA-13 — Unequal power

Version cannot upgrade weak/coerced acknowledgement/acceptance into valid Agreement/Consent simply because it binds to the correct state. Validity remains owned by specialist/policy semantics.

**PASS WITH HARDENING.**

## MA-14 — Multi-resource / capacity

Future resource requirement/allocation/reservation may have revisions; Version must not absorb those planning semantics. State discipline remains reusable.

**PASS WITH HARDENING.**

## MA-15 — Coordination-burden distribution

Do not require every actor to reconfirm every technical change for organizer convenience. Renewed action depends on materiality/consequence.

**PASS.**

## MA-16 — Formality / progressive disclosure

Casual personal use can hide versions entirely. Shared/high-consequence flows may expose changes/state history.

**PASS.**

## MA-17 — AI authority / multi-party context

AI proposal/action may become stale if target materially changes between reasoning and effect.

Required:

```text
base state preserved where material
material divergence detected/re-evaluated
no fabricated human carry-forward
```

**PASS WITH HARDENING.**

## MA-18 — Specialist-system boundary

Specialist systems may remain authoritative for their own version/record semantics. LifeOS maps rather than cloning provider identity/history.

**PASS.**

## MA-19 — Multi-actor primitive redundancy

No `SharedVersion`, `ConsentVersion`, `AgreementVersion`, `ActorVersion`, `ParticipantVersion` or other generic duplicate primitive is justified.

**PASS.**

## MA-20 — Actor-scoped reality attribution

Revision of shared target state must not rewrite actor-specific Participation, Ack, Confirmation, Agreement/Consent, performer or other historical attribution.

**PASS WITH HARDENING.**

## Multi-Actor Gate result

```text
MA-01 PASS
MA-02 PASS WITH HARDENING
MA-03 PASS WITH HARDENING
MA-04 PASS
MA-05 PASS WITH HARDENING
MA-06 PASS WITH HARDENING
MA-07 PASS WITH HARDENING
MA-08 PASS WITH HARDENING
MA-09 PASS
MA-10 PASS WITH HARDENING
MA-11 PASS WITH HARDENING
MA-12 PASS WITH HARDENING
MA-13 PASS WITH HARDENING
MA-14 PASS WITH HARDENING
MA-15 PASS
MA-16 PASS
MA-17 PASS WITH HARDENING
MA-18 PASS
MA-19 PASS
MA-20 PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
```

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable | Result | Notes |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS WITH HARDENING | stable target identity remains separate from material-state continuity; identity replacement remains owning-concept decision |
| XCON-02 Ownership/Authority compatibility | yes | PASS WITH HARDENING | Version identifies state; Authority/Decision/policy selects legitimate effect/current interpretation |
| XCON-03 Planned/current/Actual/history compatibility | yes | PASS WITH HARDENING | original, historical, current, effective and Actual states are not collapsed |
| XCON-04 Relationship compatibility | yes | PASS | state binding can be direct/derived/qualified without universal Relationship/Version root |
| XCON-05 Multi-actor readiness compatibility | yes | PASS | one shared target supports actor-scoped actions against different historical states |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE REQUIRED | Version/Material-State becomes canonical cross-cutting vocabulary; technical/provider versions remain implementation/integration terms |

```text
XCON GATE
PASS WITH HARDENING
```

No accepted concept requires structural reopening.

---

# 7. Adjacent Dependency Sweep

| Dependency / boundary | Why it matters | Closure | Current resolution / why safe | Owner / stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|---|
| target identity ↔ Version | revision must not fabricate/reuse identity incorrectly | RESOLVED | Version applies only while owning identity invariants survive | every owning concept | ordinary revision-vs-replacement cannot be decided locally | CORE-03/04/06/09, XCON-01/03/04 |
| semantic Version ↔ technical record revision | every write must not invalidate assent/ack | RESOLVED | explicitly distinct | logical/persistence | implementation requires semantic equality with every storage write | CORE-03/08/10/13 |
| provider revision ↔ LifeOS state | sync IDs can change independently | RESOLVED | provider ID is mapping/provenance input | integration | provider sync cannot avoid false identity/overwrite | CORE-02/09/13, MA-09/12/18 |
| Version ↔ ETag/MVCC | concurrency token useful but weaker | RESOLVED | technical freshness != semantic materiality | API/persistence | stale-write prevention requires collapsing domain semantics | CORE-08/13 |
| material equivalence ↔ hash/content equality | same/different bytes do not decide purpose | RESOLVED | materiality purpose/facet scoped | owning family | semantic applicability cannot be decided without global byte equality | CORE-03/04/09 |
| Version ↔ Provenance | lineage and state reference must stay separate | RESOLVED | Version may have Provenance | Provenance/logical | lineage cannot identify material states without semantic collapse | CORE-04/05/09, XCON-04 |
| Version ↔ Decision/Approval | approved state must remain identifiable | RESOLVED | Decision binds state; Version does not resolve | Decision | Decision must own state identity itself | CORE-04, MA-06, XCON-02 |
| Version ↔ Authority | applicable policy/basis can change | RESOLVED | Authority governs effect, Version identifies state | Authority/security | historical Authority cannot be reconstructed without Version becoming Authority | CORE-02/04, MA-06/11 |
| Version ↔ reconciliation/source precedence | divergent states need resolution later | RESOLVED semantic boundary | Version preserves divergence; reconciliation selects/merges/keeps unresolved | reconciliation/logical | divergence cannot coexist without Version owning merge/winner | CORE-02/09/13, MA-12/18 |
| Ack / Confirmation target binding | prior action must not float to latest | RESOLVED | material-state binding + purpose-specific equivalence | Ack/Confirmation | persistence cannot reconstruct target state | CORE-02/09/13, MA-05/11 |
| Agreement / Consent applicability | material amendment invalidates carry-forward | RESOLVED | state-bound terms/scope/purpose | Agreement/Consent/policy | applicability cannot be determined after amendment | CORE-02/09, MA-05/13 |
| Participation response | accepted response may target old Event state | RESOLVED | response binds materially relevant participation/request state | Participation | response history cannot distinguish changed invitation/occurrence | CORE-02/09, MA-05/11 |
| Responsibility hand-off response | role transfer response may target old scope | RESOLVED | response binds hand-off/request state | Responsibility | scope change cannot invalidate/reuse response correctly | CORE-02/09, MA-03/11 |
| Representation action state | representative may act against stale state | RESOLVED | actual Actor + represented party + target state remain distinct | Representation | attribution cannot identify acted-against state | CORE-02/09, MA-10/17 |
| Actual/Observation/Outcome correction | current correction must not rewrite earlier state | RESOLVED | same target may have material states; current selection separate | reality/reconciliation | correction requires new target identity for ordinary cases | CORE-02/09, XCON-01/03 |
| Evidence evaluation history | old conclusion must retain old basis | RESOLVED | material source/rule states may be bound/reconstructed | GoalCriterion/evaluation | historical result cannot be reproduced without universal snapshot root | CORE-02/09/10/13 |
| Routine/Recurrence/Occurrence history | past instances must retain governing policy | RESOLVED | Occurrence may bind/reconstruct source policy state | Time/logical | past occurrence source semantics cannot be reconstructed | CORE-02/09/13, XCON-03 |
| Schedule revision | semantic consumers need old/current placement | RESOLVED | Schedule owns placement history; Version provides state discipline | Schedule/logical | Ack/Decision cannot bind correct schedule state | CORE-02/09, XCON-03 |
| Milestone redefinition | some changes are replacement, not revision | RESOLVED with identity guard | owning Milestone identity decides continuity | Milestone | common identity-transition primitive becomes necessary | CORE-03/04/06/09 |
| per-family material-equivalence rules | materiality differs by purpose | SAFE DEFERRED | global flag rejected; owning semantics already define consequence | owning concept/product policy | a family cannot decide carry-forward without changing Version semantics | CORE-02/04/09/13, MA-05/06/11/17 |
| branch/merge algorithm | concurrent states need operational handling | SAFE DEFERRED | divergence can remain unresolved; Version need not merge | reconciliation/logical | concurrency cannot be represented without universal LWW/merge inside Version | CORE-02/09/10/13, MA-12/18 |
| exact effective dating | must know which state governed time T | SAFE DEFERRED | historical/action-time distinction fixed | Time/logical | action-time state cannot be reconstructed | CORE-02/09/13, MA-11, XCON-03 |
| provider mapping | external histories differ | SAFE DEFERRED | native/provider identity separation fixed | integration/Provenance | provider mapping creates duplicate/overwrite ambiguity | CORE-09/13, MA-09/18 |
| retention/redaction | history vs privacy tension | SAFE DEFERRED | history does not mandate full payload retention | privacy/retention | deletion makes required applicability impossible | CORE-02/09/10, MA-07/08/11/13 |
| versioned evaluation/rule snapshots | historical reasoning may need rules | SAFE DEFERRED | only consequential evaluations need material basis | GoalCriterion/Trigger/evaluation | current rules rewrite historical conclusions | CORE-02/09/10/13 |

```text
RESOLVED material boundaries       19
SAFE DEFERRED material boundaries   6
REOPEN                              0
unclassified material items         0
```

---

# 8. Adversarial scenario log

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|
| database update changes only technical metadata | storage vs material state | PASS | technical revision explicitly separated |
| title capitalization corrected after Schedule Ack | purpose-specific materiality | PASS | no renewed Ack required by domain solely for irrelevant change |
| Schedule 15:00 -> 16:00 after Ack | target-state binding | PASS | old Ack retained; renewed Ack policy may apply |
| Agreement formatting clarification | non-material carry-forward | PASS | material equivalence can preserve applicability |
| Agreement price EUR100 -> EUR120 | material terms | PASS | old Agreement not inherited |
| Consent purpose expands to unrelated use | scope/purpose | PASS | old Consent not inherited |
| Participation accepted then Event materially moved | family response | PASS | response binds prior state; owning policy decides renewed stance |
| Responsibility hand-off scope expands after response | role-transfer history | PASS | prior response does not silently cover new scope |
| hidden source changes, safe projection same | projection/source privacy | PASS WITH HARDENING | projection materiality independent; explanation cannot leak source |
| provider/user concurrent edits | branching/conflict | PASS WITH HARDENING | divergence preserved; no universal LWW |
| same content but Authority/basis materially changed | content equality | PASS | hash cannot decide semantic equivalence |
| provider increments revision counter | integration boundary | PASS | provider revision not semantic by default |
| AI patch prepared against stale base | AI safety | PASS WITH HARDENING | preserve/re-evaluate base state before effect |
| Routine `this and future` policy change | Time history | PASS | prior Occurrences remain tied to prior policy state |
| Milestone B1 -> C1 | identity continuity | PASS WITH HARDENING | likely replacement/new identity; Version cannot hide semantic replacement |
| old sensitive payload deleted | retention/history | PASS WITH HARDENING | minimal history may remain without full payload |

No scenario requires a universal Version entity/root.

---

# 9. Reopening / dependency register

| Finding | Severity | Closure | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|
| target continuity vs new identity | HARDENING | RESOLVED | owning-concept identity guard | whole-domain/logical | common transition semantics becomes unavoidable |
| technical revision vs semantic state | STRUCTURAL | RESOLVED | explicit non-equivalence invariant | logical/API | implementation cannot preserve distinction |
| purpose-specific materiality | HARDENING | SAFE DEFERRED | owning family determines relevance/carry-forward | each family/product policy | family applicability cannot be implemented without changing common concept |
| concurrent divergent states | DEFERRED DEPENDENCY | SAFE DEFERRED | preserve branches/conflict; no LWW | reconciliation/logical | state divergence cannot remain reconstructible |
| source precedence / merge | DEFERRED DEPENDENCY | SAFE DEFERRED | separate from Version | reconciliation | Version must decide winner to remain coherent |
| effective dating | DEFERRED DEPENDENCY | SAFE DEFERRED | semantics fixed, storage open | Time/logical | historical action-time state cannot be known |
| provider version mapping | DEFERRED DEPENDENCY | SAFE DEFERRED | external/native IDs distinct | integration/Provenance | provider sync corrupts identity/history |
| retention/redaction | DEFERRED DEPENDENCY | SAFE DEFERRED | no full-payload retention mandate | privacy/retention | history requirement conflicts with deletion/minimization |
| AI stale-base change | HARDENING | RESOLVED | base state + re-evaluation required where material | AI/application/logical | AI cannot avoid stale semantic writes without broader primitive |
| universal Version root pressure | STRUCTURAL | RESOLVED | explicitly rejected | logical/persistence | only reopen with evidence of common independent lifecycle/identity |

```text
REOPEN 0
```

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Rationale

The candidate survives removal, merge, universalization, history, correction, privacy, multi-actor, AI, provider, concurrency and implementation-pressure tests.

The common capability is necessary because many accepted semantic families already depend on target-state specificity. A universal Version entity/root is unnecessary and harmful. The smallest surviving model is a cross-cutting semantic state-reference/material-equivalence discipline whose physical representation remains consequence-sensitive.

## Hardenings incorporated before acceptance

All mandatory hardenings are incorporated into `../concepts/version.md`:

```text
VER-01 target identity != target Version
VER-02 not every persistence change is a material revision
VER-03 technical record version != semantic Version
VER-04 provider version != LifeOS material Version automatically
VER-05 content/hash equality != material equivalence
VER-06 materiality is purpose/family/facet scoped
VER-07 irrelevant facet change does not invalidate unrelated semantics
VER-08 semantic actions/evaluations bind to the state they actually concerned
VER-09 material change does not inherit prior semantic state by default
VER-10 non-material equivalence may preserve applicability
VER-11 same target ID does not prove semantic carry-forward
VER-12 current state != historical state
VER-13 Version != Provenance
VER-14 Version != Decision / Authority / reconciliation
VER-15 history need not be globally linear
VER-16 version identifiers need not carry ordering meaning
VER-17 current/effective-state selection remains owned by domain + Authority/Decision/policy
VER-18 projection Version != hidden source Version
VER-19 historical evaluation may bind source/rule states
VER-20 AI proposal/action retains material base state where needed
VER-21 stale-base AI/system action requires re-evaluation after material divergence
VER-22 ETag/MVCC is implementation support, not domain truth
VER-23 version history does not justify indefinite sensitive payload retention
VER-24 snapshots/deltas/event sourcing/effective dating remain physical choices
VER-25 identity-breaking redefinition may require replacement, not new Version
VER-26 no universal versions table/polymorphic Version root is pre-approved
```

## Dependency-sweep summary

```text
RESOLVED      19
SAFE DEFERRED  6
REOPEN          0
unclassified    0
```

## Mandatory future re-tests

- detailed reconciliation / source precedence;
- GoalCriterion / evaluation rule history;
- Trigger / conditional policy rule revisions;
- logical data model;
- persistence/API pressure;
- offline/sync/provider reconciliation;
- privacy/retention/tombstone behavior;
- whole-domain semantic regression;
- whole-domain multi-actor regression;
- AI stale-base write/effect policy.

The approved 42-path documentation propagation and post-write QA completed successfully; this verdict is the accepted current branch baseline.

---

# 11. Cluster-only integration section

**N/A — justified.**

Relationships / Reasoning remains an open candidate space. Version v0 completion does not authorize a synthetic cluster verdict before the remaining candidate space is freshly re-scored.

Required next stage after successful post-write QA:

```text
fresh Relationships / Reasoning candidate re-score
→ one next candidate/family only
→ full V3
```

No next candidate is preselected by this checkpoint.

---

# 12. Regression corpus additions

| ID | Scenario | New boundary covered | Reuse trigger |
|---|---|---|---|
| R-VER-01 | technical metadata revision after semantic Ack | technical vs material Version | any persistence/API versioning proposal |
| R-VER-02 | material Schedule revision invalidates prior Ack applicability | target-state binding | Acknowledgement/common-ground flows |
| R-VER-03 | Agreement terms v1/v2 mismatch | mutual assent versioning | Agreement/amendment flows |
| R-VER-04 | Consent purpose expansion | scoped permission applicability | privacy/Consent/use flows |
| R-VER-05 | Participation/Responsibility response against materially changed request | family-specific response state | shared coordination/hand-off |
| R-VER-06 | offline divergent edits from one base | non-linear history | sync/reconciliation/logical model |
| R-VER-07 | AI proposal stale before application | base-state AI safety | AI write/effect workflows |
| R-VER-08 | private source changes while exposed projection remains equivalent | source/projection materiality + privacy | Visibility/AI context builder |
| R-VER-09 | Recurrence `this and future` revision with old Occurrences | source-policy history | Time/recurrence persistence |
| R-VER-10 | Milestone semantic redefinition | Version vs identity replacement | lifecycle/identity review |
| R-VER-11 | provider/ETag revision differs from LifeOS materiality | integration/concurrency boundary | provider/API adapters |
| R-VER-12 | historical Evidence evaluation tied to old source/rule state | reasoning reproducibility | GoalCriterion/evaluation |
| R-VER-13 | sensitive old payload deleted but minimal state reference retained | history vs retention | privacy/logical model |

These scenarios are materially non-duplicate of prior regression cases because they specifically test semantic state binding/material equivalence rather than generic correction/history alone.

---

# 13. Documentation propagation

Approved Git scope from pre-scope commit `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`:

## CREATE

1. `docs/domain/concepts/version.md`
2. `docs/domain/checkpoints/version-material-equivalence-v0-validation.md`

## UPDATE — current canonical navigation/state

3. `docs/domain/language-map.md`
4. `docs/domain/README.md`
5. `docs/domain/multi-actor-readiness-v1.md`
6. `docs/workstreams/domain-model.md`

## UPDATE — Relationships / Reasoning consumers

7. `docs/domain/concepts/acknowledgement.md`
8. `docs/domain/checkpoints/acknowledgement-v0-validation.md`
9. `docs/domain/concepts/confirmation.md`
10. `docs/domain/checkpoints/confirmation-v0-validation.md`
11. `docs/domain/concepts/decision.md`
12. `docs/domain/checkpoints/decision-v0-validation.md`
13. `docs/domain/concepts/agreement.md`
14. `docs/domain/concepts/consent.md`
15. `docs/domain/checkpoints/agreement-consent-v0-validation.md`
16. `docs/domain/concepts/authority.md`
17. `docs/domain/checkpoints/authority-v0-validation.md`
18. `docs/domain/concepts/participation.md`
19. `docs/domain/checkpoints/participation-v0-validation.md`
20. `docs/domain/concepts/responsibility.md`
21. `docs/domain/checkpoints/responsibility-v0-validation.md`
22. `docs/domain/concepts/representation.md`
23. `docs/domain/checkpoints/representation-delegation-principal-v0-validation.md`

## UPDATE — Observed Reality / Evidence consumers

24. `docs/domain/concepts/actual.md`
25. `docs/domain/checkpoints/actual-v0-validation.md`
26. `docs/domain/concepts/observation.md`
27. `docs/domain/checkpoints/observation-v0-validation.md`
28. `docs/domain/concepts/outcome.md`
29. `docs/domain/checkpoints/outcome-v0-validation.md`
30. `docs/domain/concepts/evidence.md`
31. `docs/domain/checkpoints/evidence-v0-validation.md`
32. `docs/domain/concepts/provenance.md`
33. `docs/domain/checkpoints/provenance-v0-validation.md`
34. `docs/domain/checkpoints/observed-reality-evidence-v0.md`

## UPDATE — Time / Intention history consumers

35. `docs/domain/concepts/routine.md`
36. `docs/domain/concepts/occurrence.md`
37. `docs/domain/concepts/recurrence.md`
38. `docs/domain/concepts/schedule.md`
39. `docs/domain/checkpoints/time-v0.md`
40. `docs/domain/concepts/milestone.md`
41. `docs/domain/checkpoints/intention-execution-v0.md`

## UPDATE — historical dependency closure

42. `docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`

Propagation rule:

> Existing concept/checkpoint content is preserved. Historical validation checkpoints receive explicit downstream closure amendments rather than silent rewriting of what their original review knew at the time.

Explicitly out of scope:

```text
root README.md
PROJECT-STATUS
product v1 core glossary
feature-discovery historical evidence
multi-actor discovery/research historical evidence
Cross-Cluster v4 unless later whole-domain work requires it
main
prototype
SQL
API
backend
auth/security implementation
```

## Post-write QA requirements

Before Version v0 becomes canonical accepted baseline, verify:

- branch = `feature/domain-model`;
- exact final HEAD;
- diff against pre-scope `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`;
- exactly 42 approved paths, no extras;
- 2 new + 40 modified;
- concept/checkpoint complete;
- CORE 01–13 present;
- MA 01–20 present;
- XCON 01–06 present;
- ADS complete;
- external classifications present;
- all VER hardenings incorporated;
- no universal Version root/table/event-sourcing mandate;
- technical/provider/ETag version separated;
- purpose-specific materiality explicit;
- non-linear/offline conflict allowed;
- AI stale-base rule explicit;
- source/projection privacy explicit;
- Version-vs-identity guard explicit;
- downstream closure amendments present;
- historical checkpoints remain historically reconstructible;
- old product glossary untouched;
- workstream current;
- `main`, prototype, SQL/API/backend/auth untouched;
- compare to `main`: branch behind = 0.

## Post-write QA result — PASS

Validated against pre-scope `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`.

```text
branch                           feature/domain-model
approved unique paths changed   42 / 42
new files                        2 / 2
modified files                  40 / 40
out-of-scope paths               0
preservation                     PASS
CORE / MA / XCON / ADS           COMPLETE
RESOLVED                         19
SAFE DEFERRED                    6
REOPEN                           0
unclassified                     0
branch behind main               0
```

Historical checkpoints remain reconstructible; old product glossary, root README, PROJECT-STATUS, main, prototype, SQL/API/backend/auth remain untouched by this scope.

Version v0 is the current accepted Domain Atlas baseline.