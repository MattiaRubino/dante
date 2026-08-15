# Version / Material-Equivalence v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated; post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Approved pre-scope:** `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`

## 1. Scope

Candidate family:

```text
Version
Revision
Material state
Material equivalence
Snapshot/history
technical record version
```

Primary question:

> **How can LifeOS preserve which materially relevant state of a stable target another semantic action/evaluation actually concerned, without turning every write, provider revision or object into a universal Version entity?**

Nearest accepted boundaries inspected:

- native/contextual identity;
- Acknowledgement;
- Confirmation;
- Agreement;
- Consent;
- Decision / Approval;
- Authority;
- Responsibility;
- Participation;
- Provenance;
- Evidence;
- Actual / Observation / Outcome;
- Routine / Recurrence / Occurrence;
- Schedule;
- Milestone;
- Representation;
- AI stale-base proposals;
- Visibility / retention.

Deliberately not designed:

- one universal `versions` table;
- event sourcing;
- CRDTs;
- final effective dating schema;
- API ETag / If-Match policy;
- provider sync mapping;
- retention durations;
- exact per-family material-equivalence rules;
- source-precedence/reconciliation mechanics;
- final SQL/API.

---

# 2. Fresh candidate re-score

Candidate space was freshly re-scored after Representation v0 QA closure. Version / Material-Equivalence emerged as the highest-pressure remaining candidate because the accepted Domain Atlas already requires materially specific target binding across Ack/Confirmation/Agreement/Consent/Decision/Participation/Responsibility/Evidence/Recurrence/Schedule, and per-family deferral was beginning to duplicate the same historical applicability question.

Fresh selection did **not** assume that the previous second-place candidate must automatically run next.

---

# 3. Evidence

## EV-01 — Existing LifeOS evidence

Accepted concepts already require distinctions such as:

```text
Ack(v1) != Ack(v2 automatically)
Confirmation(v1) != Confirmation(v2 automatically)
Agreement(terms v1) != Agreement(terms v2 automatically)
Consent(scope/purpose v1) != Consent(scope/purpose v2 automatically)
Decision/Approval(proposal v1) != approval(v2 automatically)
Participation response(state v1) != response(state v2 automatically)
Responsibility hand-off response(request v1) != response(request v2 automatically)
```

Evidence/evaluation requires source/rule state binding; Routine/Recurrence needs source-policy history; Schedule needs accepted-placement history; Observation/Actual correction must not rewrite what earlier actors saw/used.

**EV-01 result:** strong cross-cutting pressure; per-family ad hoc version handling would duplicate semantics and risk incompatible history rules.

## EV-02 — Real-world workflow inversion

Tested workflows:

```text
meeting time acknowledged then materially rescheduled
Responsibility hand-off request scope changed after response
Agreement terms price changed
Consent purpose expanded
AI proposal generated against stale base
Observation corrected after confirmation/evaluation
recurring policy edited for future occurrences
provider/offline concurrent revisions
```

Observed recurring shape:

```text
stable target identity
+
materially changing states
+
semantic acts/evaluations tied to the state they actually concerned
```

**EV-02 result:** shared material-state discipline needed; universal version object not demonstrated.

## EV-03 — External benchmark classifications

| Benchmark | Finding | Classification | LifeOS treatment |
|---|---|---|---|
| HL7 FHIR `meta.versionId` | technical resource version changes on updates | ANTI-PATTERN if equated to semantic materiality | technical record version != LifeOS material-state semantics |
| HL7 FHIR resource/business version separation patterns | technical record revision and domain/business version can differ | BORROW / boundary evidence | reinforces separation |
| W3C PROV `wasRevisionOf` | revision relation preserves lineage | ADAPT | useful Provenance/history relation, not full Version ontology |
| HTTP ETag / If-Match | stale-write protection against representation state | ADAPT for future technical concurrency | ETag != domain Version |
| Git commit/snapshot history | immutable reconstructible states + parent history | ADAPT as history pattern | no Git-style DAG mandate for all LifeOS data |
| Git global commit graph | repository-wide version root | ANTI-PATTERN if imported universally | domain granularity must remain contextual |

## EV-04 — Candidate minimality

Hypotheses tested:

```text
H0 no shared Version semantics; every family owns ad hoc history
H1 universal Version entity/root
H2 technical row/provider version = domain Version
H3 cross-cutting Version/material-state capability + contextual material equivalence
H4 universal event-sourcing/snapshot model
```

Result:

```text
H0 FAIL
H1 FAIL
H2 FAIL
H3 SURVIVES
H4 FAIL
```

Smallest surviving result:

```text
Version / Material-State
= cross-cutting semantic capability / discipline

Material Equivalence
= purpose/facet-specific applicability determination
```

Neither requires universal native entity identity.

---

# 4. Canonical definition

> **Version / Material-State is the cross-cutting semantic capability through which LifeOS can identify and reconstruct a materially relevant state of an otherwise stable domain target, bind semantic actions, attestations, permissions, evaluations or decisions to the state they actually concerned, and determine — according to the owning semantic purpose — whether a later state remains materially equivalent for that use. Version does not define target identity, explain lineage, choose canonical state, decide reconciliation, or turn every technical write into a domain revision.**

Canonical question:

> **Which materially relevant state of this target did this semantic act or evaluation concern, and does a later state remain equivalent for that specific purpose?**

---

# 5. Identity and independence

```text
Target identity != material state
```

A stable Event, Observation, Goal, Milestone, Agreement context or other target can change materially without automatically becoming another target identity.

But:

```text
Version cannot rescue broken identity continuity
```

If the owning concept's identity invariants fail, the correct model may be replacement/new identity rather than `v2`.

Version therefore has **semantic independence** as state/history discipline but **not native independent identity** as a universal root.

---

# 6. Deep chronology

```text
T0 Event E17 exists
T1 Schedule state S1 = 15:00
T2 Luca Acknowledges S1
T3 Participation response R1 = accepted against S1
T4 Schedule materially changes to S2 = 16:00
T5 Ack(S1) and R1 remain historical; applicability to S2 is not silently assumed
T6 Luca explicitly Acknowledges S2
T7 new Participation response R2 applies to S2
T8 event actually begins 16:12
T9 Actual = 16:12
T10 historical query asks what Luca had acknowledged/accepted before the material reschedule
```

Required reconstruction:

```text
stable Event identity
S1 / S2 material Schedule states
Ack/Participation response bindings
current accepted Schedule state
later Actual
```

No technical version number is necessary to state the semantics.

---

# 7. Concurrent divergence stress

```text
Base S1
├─ offline Actor A creates S2A
└─ provider/Actor B creates S2B
```

Required:

```text
S2A and S2B may both be historically real
arrival order != universal semantic precedence
Version preserves divergence
Reconciliation/Authority/Decision owns resolution
```

Universal last-write-wins is rejected.

---

# 8. Destructive reductio

```text
REMOVE shared Version semantics
→ FAIL: repeated ad hoc material-state rules + historical applicability ambiguity

Version = target identity
→ FAIL: ordinary revision would create false identities

Version = every database write
→ FAIL: technical noise becomes semantic history

Version = ETag/MVCC/provider revision
→ FAIL: technical concurrency/integration identifiers do not define materiality

Version = Provenance
→ FAIL: state reference != lineage

Version = Decision/Authority/Reconciliation
→ FAIL: state identification != governance/resolution

universal Version root/table
→ FAIL: granularity/identity/lifecycle not universal

cross-cutting Version/material-state capability
→ PASS WITH HARDENING
```

---

# 9. CORE Semantic Validation Gate

| Test | Result | Finding / hardening |
|---|---|---|
| CORE-01 Workflow inversion | PASS | real workflows require stable identity + material state binding |
| CORE-02 Deep chronology | PASS WITH HARDENING | current/history/action bindings remain distinct |
| CORE-03 Reductio | PASS | shared capability survives; universal root/technical version/event sourcing fail |
| CORE-04 Redundancy | PASS WITH HARDENING | Version distinct from identity/Provenance/Decision/Reconciliation |
| CORE-05 Traceability | PASS | semantic action → material state → later state/history reconstructible |
| CORE-06 Independence | PASS WITH HARDENING | contextual/cross-cutting capability, not native entity |
| CORE-07 Benchmark | PASS | standards reinforce technical/domain version distinction |
| CORE-08 Anti-pattern | PASS | every-write versioning, LWW, provider-version equality rejected |
| CORE-09 Correction/reconciliation | PASS WITH HARDENING | divergence/correction history preserved; Version does not decide winner |
| CORE-10 Scale/history | PASS WITH HARDENING | no mandatory snapshot/event per write |
| CORE-11 Simple/power user | PASS | ordinary UI hides version mechanics |
| CORE-12 Product complexity | PASS WITH HARDENING | state precision only where consequence warrants it |
| CORE-13 Implementation pressure | PASS WITH HARDENING | semantics fixed without one persistence strategy |

**CORE Gate:** PASS WITH HARDENING.

---

# 10. Mandatory hardenings

1. Version is cross-cutting semantic capability/discipline, not universal entity/root.
2. Target identity != material state.
3. Version cannot preserve identity after owning identity invariants fail.
4. Not every write/update is material.
5. Technical row version != domain Version.
6. Provider revision != native LifeOS Version automatically.
7. ETag/MVCC/optimistic-lock token != semantic Version.
8. Hash/content equality != universal material equivalence.
9. Materiality is purpose/family/facet-specific where needed.
10. Irrelevant facet changes must not invalidate unrelated semantic actions.
11. Semantic acts/evaluations bind to material state where consequence requires it.
12. Material change does not inherit prior Ack/Confirmation/Agreement/Consent/Decision/family-specific response by default.
13. Non-material equivalence may preserve applicability without fabricating a new human action.
14. Current != historical state.
15. Version != Provenance.
16. Version != Decision/Approval/Authority.
17. Version != reconciliation/source precedence.
18. History need not be globally linear.
19. Version IDs need not encode semantic/chronological ordering.
20. Owning domain + applicable governance owns current/effective state.
21. Projection materiality may differ from hidden source materiality.
22. Material evaluation history may require source/rule state binding.
23. AI proposals/actions preserve material base state where consequence requires it.
24. stale-base action must re-evaluate after material divergence.
25. history Visibility independently governed.
26. historical integrity does not require indefinite sensitive-payload retention.
27. physical snapshot/delta/event-sourcing strategy remains open.
28. persistence/formality consequence-sensitive.

---

# 11. Multi-Actor Compatibility Gate

| Test | Result | Finding |
|---|---|---|
| MA-01 Identity/account independence | PASS | material states remain target-bound; no Account identity assumption |
| MA-02 Shared fact / actor overlay | PASS WITH HARDENING | one shared target can have common material states + actor-scoped semantic bindings |
| MA-03 Responsibility | PASS WITH HARDENING | response/history binds to request state without becoming Responsibility |
| MA-04 Stewardship | PASS | versioning does not create coordination burden ownership |
| MA-05 Common ground | PASS WITH HARDENING | Ack/Agreement/Consent/response applicability explicitly state-bound |
| MA-06 Authority | PASS WITH HARDENING | Version does not create Authority/canonical-state selection |
| MA-07 Selective disclosure | PASS WITH HARDENING | history/state visibility may differ from current projection |
| MA-08 Inference privacy | PASS WITH HARDENING | hidden source changes need not leak through exposed projection version |
| MA-09 Partial adoption | PASS | provider/external revisions map without native identity collapse |
| MA-10 Assisted attribution | PASS | represented action preserves Actor/party separately from target state |
| MA-11 Lifecycle/revocation | PASS WITH HARDENING | old applicable states remain history after later revocation/change |
| MA-12 Conflict/adversarial | PASS WITH HARDENING | divergent states may coexist unresolved |
| MA-13 Unequal power | PASS | Version does not manufacture assent/Consent/Authority |
| MA-14 Resource/capacity | PASS — limited | Version applies without redefining Resource/Capacity identity |
| MA-15 Coordination burden | PASS | no universal review/version ceremony |
| MA-16 Progressive formality | PASS | simple changed/updated UI to rich version history |
| MA-17 AI | PASS WITH HARDENING | stale-base protection + no implicit carry-forward |
| MA-18 Specialist boundary | PASS WITH HARDENING | specialist revision IDs remain adapter evidence, not ontology |
| MA-19 Primitive redundancy | PASS | universal Version root unnecessary |
| MA-20 Actor-scoped attribution | PASS | state history does not overwrite who acted/experienced what |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 12. Cross-Concept Consistency Gate

| Test | Result | Closure |
|---|---|---|
| XCON-01 Identity | PASS WITH HARDENING | Version state distinct from target identity; identity replacement guard added |
| XCON-02 Authority | PASS | Version never decides governance/current state |
| XCON-03 current/history/Actual | PASS WITH HARDENING | current, historical material states and later Actual remain separable |
| XCON-04 Relationships | PASS WITH HARDENING | qualified material-state binding allowed without universal root |
| XCON-05 Multi-actor | PASS WITH HARDENING | actor-scoped Ack/response/Consent can bind same shared target states |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Version/revision/update/current language normalized |

**Structural reopening of prior accepted concepts:** 0.

---

# 13. Adjacent Dependency Sweep

## RESOLVED

```text
Version ↔ target identity
Version ↔ technical revision
Version ↔ provider revision
Version ↔ ETag/MVCC
material equivalence ↔ hash/content equality
Version ↔ Provenance
Version ↔ Decision / Approval
Version ↔ Authority
Version ↔ reconciliation
Acknowledgement / Confirmation target binding
Agreement / Consent applicability
Participation / Responsibility response applicability
Evidence historical source/rule-state binding
Routine / Recurrence / Occurrence policy history
Schedule revision history
Milestone Version vs identity replacement
Representation material action/scope binding
```

## SAFE DEFERRED — per-family material-equivalence rules

**Unresolved:** exact differences that require renewed Ack/response/Agreement/Consent/Decision for each family.  
**Why safe:** Version v0 fixes purpose-specific materiality and prohibits global equality shortcuts.  
**Owner:** owning concept/product policy + logical model.  
**Trigger:** a family cannot determine applicability after change without changing Version semantics.  
**Tests:** CORE-02/04/09/13, MA-05/06/11/12/17, XCON-03/04.

## SAFE DEFERRED — branch/merge/source-precedence mechanics

**Unresolved:** merge/select/correct/split behavior for concurrent states.  
**Why safe:** Version preserves divergence without deciding winner.  
**Owner:** reconciliation + logical model.  
**Trigger:** offline/provider conflicts cannot be reconstructed without Version becoming reconciliation.  
**Tests:** CORE-02/09/10/13, MA-06/11/12/17/18, XCON-02/03.

## SAFE DEFERRED — exact effective dating

**Unresolved:** state validity/effect interval representation.  
**Why safe:** action-time/current/history separation is canonical.  
**Owner:** Time + logical model.  
**Trigger:** system cannot determine which state governed action/evaluation at time T.  
**Tests:** CORE-02/09/13, MA-11, XCON-03.

## SAFE DEFERRED — provider version mapping

**Unresolved:** mapping remote provider revisions/sync tokens to LifeOS states.  
**Why safe:** provider IDs explicitly do not define LifeOS materiality.  
**Owner:** integration + Provenance.  
**Trigger:** sync cannot avoid false duplicate/overwrite without changing native Version semantics.  
**Tests:** CORE-02/09/10/13, MA-09/12/18, XCON-01/03.

## SAFE DEFERRED — retention/deletion/tombstone/redaction

**Unresolved:** how much historic payload/state to retain.  
**Why safe:** reconstructibility does not mandate payload retention.  
**Owner:** privacy/retention/logical model.  
**Trigger:** required applicability/history cannot coexist with minimization/deletion.  
**Tests:** CORE-02/09/10, MA-07/08/11/13, XCON-03.

## SAFE DEFERRED — versioned evaluation/rule snapshots

**Unresolved:** persisted rule/source snapshots for evaluation.  
**Why safe:** material source/rule state binding required only where historical reproducibility matters.  
**Owner:** GoalCriterion / Trigger / evaluation reasoning.  
**Trigger:** evaluation history cannot be explained without stronger universal rule-Version primitive.  
**Tests:** CORE-02/04/09/10/13, MA-17/18, XCON-03/04.

## SAFE DEFERRED — identity replacement threshold

**Unresolved:** exact edit-vs-replacement rules for each owning concept.  
**Why safe:** Version explicitly defers continuity to owning identity invariants.  
**Owner:** each native/contextual concept.  
**Trigger:** ordinary workflows cannot decide revision-vs-replacement locally without shared stronger identity-transition semantics.  
**Tests:** CORE-03/04/06/09, XCON-01/03/04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 14. Adversarial log

| Scenario | Required result |
|---|---|
| database metadata update only | no automatic semantic material Version |
| Schedule 15:00→16:00 after Ack | prior Ack historical; renewed applicability decided by Ack/Schedule purpose |
| title typo after Ack | may remain equivalent for time-Ack purpose |
| Agreement price 100→120 | material terms change; prior Agreement not inherited |
| Consent trip free/busy→AI-training full history | material scope/purpose expansion; prior Consent not inherited |
| Responsibility duties expand after positive response | old response not silently applied |
| corrected Observation after Confirmation | old Confirmation remains bound to earlier material state |
| AI proposal against stale base | preserve base; re-evaluate before effect |
| private source change, public projection unchanged | source Version may change; exposed projection may remain materially equivalent |
| provider revision with no semantic change | provider version != LifeOS material state |
| offline concurrent S2A/S2B | preserve both; no LWW semantic rule |
| Milestone B1→C1 | owning identity may require replacement, not v2 |
| old Occurrence after Recurrence policy change | remains explainable under old governing policy |
| deletion/minimization | preserve required reference/history without assuming full payload retention |

---

# 15. Reopening / dependency register

| Finding | Severity | Treatment |
|---|---|---|
| stable identity + materially changing state | STRUCTURAL | canonical Version/material-state capability |
| Version = technical revision | STRUCTURAL | rejected |
| universal Version entity/root | STRUCTURAL | rejected |
| materiality contextual | HARDENING | canonical invariant |
| history may diverge | HARDENING | no universal linear/LWW rule |
| material-state binding | HARDENING | canonical invariant |
| identity replacement guard | HARDENING | owning concept decides continuity |
| reconciliation mechanics | DEFERRED | SAFE DEFERRED |
| effective dating | DEFERRED | SAFE DEFERRED |
| provider mapping | DEFERRED | SAFE DEFERRED |
| retention/redaction | DEFERRED | SAFE DEFERRED |
| evaluation rule snapshots | DEFERRED | SAFE DEFERRED |
| product complexity | UX | consequence-sensitive |

---

# 16. Regression corpus additions

```text
R-VER-01 technical metadata revision after Ack -> no automatic renewed Ack
R-VER-02 material Schedule revision after Ack -> prior Ack does not silently carry
R-VER-03 Agreement material terms amendment -> prior Agreement historical only
R-VER-04 Consent purpose expansion -> prior Consent not inherited
R-VER-05 corrected Observation after Confirmation/Evaluation -> historical bindings preserved
R-VER-06 concurrent offline/provider revisions -> divergence preserved; no LWW
R-VER-07 stale-base AI proposal -> re-evaluate before effect
R-VER-08 private source revision + materially equivalent exposed projection
R-VER-09 Recurrence policy revision + old/future Occurrence history
R-VER-10 Milestone material redefinition crosses identity boundary -> replacement candidate, not automatic v2
```

---

# 17. Verdict

```text
VERSION / MATERIAL-EQUIVALENCE FAMILY
PASS WITH HARDENING

Version / Material-State
✅ CANONICAL cross-cutting semantic capability/discipline
✅ materially relevant state binding
✅ historical reconstructibility
✅ concurrent/divergent-state compatible
✅ consequence-sensitive
❌ universal entity/root
❌ target identity
❌ technical revision token
❌ Provenance/Decision/Authority/Reconciliation

Material Equivalence
✅ contextual / purpose/facet-specific applicability concept
❌ universal object equality flag

REOPEN                               0
unclassified material dependencies   0
```

No prior accepted concept required structural reopening.

---

# 18. Mandatory future re-tests

Retest when these owners mature:

- per-family material-equivalence policy;
- reconciliation/source precedence;
- effective dating;
- provider synchronization/version mapping;
- retention/deletion/redaction;
- GoalCriterion/Trigger/evaluation snapshots;
- native identity replacement rules;
- final logical/physical/API model;
- whole-domain history/privacy/AI/multi-actor regression.

---

# 19. Cluster integration

Not applicable yet. Relationships / Reasoning remains open.

No next candidate is selected by this checkpoint. After this milestone reaches QA closure, perform a fresh candidate re-score of the remaining unresolved candidate/dependency space.

---

# 20. Documentation propagation — approved scope

### CREATE

- `../concepts/version.md`
- this checkpoint

### UPDATE — current canonical state

- `../language-map.md`
- `../README.md`
- `../../workstreams/domain-model.md`
- `../multi-actor-readiness-v1.md`

### UPDATE — downstream state-binding closures

- `../concepts/acknowledgement.md`
- `acknowledgement-v0-validation.md`
- `../concepts/confirmation.md`
- `confirmation-v0-validation.md`
- `../concepts/agreement.md`
- `../concepts/consent.md`
- `agreement-consent-v0-validation.md`
- `../concepts/decision.md`
- `decision-v0-validation.md`
- `../concepts/responsibility.md`
- `responsibility-v0-validation.md`
- `../concepts/participation.md`
- `participation-v0-validation.md`
- `../concepts/representation.md`
- `representation-delegation-principal-v0-validation.md`
- `../concepts/provenance.md`
- `provenance-v0-validation.md`
- `../concepts/evidence.md`
- `evidence-v0-validation.md`
- `../concepts/actual.md`
- `actual-v0-validation.md`
- `../concepts/observation.md`
- `observation-v0-validation.md`
- `../concepts/outcome.md`
- `outcome-v0-validation.md`
- `../concepts/schedule.md`
- `time-v0.md`
- `../concepts/recurrence.md`
- `../concepts/routine.md`
- `recurrence-v0-validation.md`
- `../concepts/milestone.md`
- `intention-execution-v0.md`
- `deferred-dependency-closure-clusters-1-4-v0.md`

Intentionally out of scope:

```text
Authority concept/checkpoint
Visibility concept/checkpoint
Person/Actor concepts
Resource/Asset/Capacity
Goal
Relationship concept (nonexistent by design)
Cross-Cluster Validation v4
product research/simulations/glossary
root README
PROJECT-STATUS
main
prototype
backend / SQL / API / auth
```

Propagation discipline:

> Historical checkpoints are append-only evidence. Original decision-time deferrals remain preserved in place; downstream Version resolution is added as an explicit closure instead of rewriting what was known then.

---

# 21. Post-write QA requirements

Required compare:

```text
base
1008aeb0367de4ae73a8e8d41a76aee9e0493f34

head
feature/domain-model after Version propagation
```

Required QA:

```text
exact approved path scope
2 CREATE
40 UPDATE
0 DELETE
0 extra paths
```

Semantic preservation checks:

- `docs/domain/concepts/relationship.md` remains absent;
- no universal Version entity/root introduced;
- no ETag/MVCC/provider revision promoted to domain identity;
- material-equivalence remains purpose/facet-specific;
- no universal LWW/linear-history rule introduced;
- Version does not become Provenance, Decision, Authority or Reconciliation;
- every modified historical checkpoint preserves its original decision/deferral state with additive downstream closure;
- current Language Map/README/workstream/multi-actor docs agree;
- REOPEN remains 0;
- unclassified material dependencies remain 0;
- no next candidate preselected;
- main remains untouched and current with branch merge-base requirements;
- prototype/backend/SQL/API/auth remain untouched.

Only after these checks pass may Version v0 be marked post-write QA PASS.

---

# 22. Post-write QA — PASS

The approved Version / Material-State v0 scope was written and then compared against the exact pre-scope baseline:

```text
base
1008aeb0367de4ae73a8e8d41a76aee9e0493f34

head
9530b64c62f09c11359c99b46aebdbed39a778c8
```

Git compare result:

```text
status      ahead
ahead_by    42
behind_by   0
commits     42
files       42

CREATE       2 / 2
UPDATE      40 / 40
DELETE       0
extra paths  0
```

Preservation QA:

- exact approved 42-path scope and no other paths;
- `docs/domain/concepts/relationship.md` remains absent;
- no universal Version entity/root/table was introduced;
- no technical ETag/MVCC/provider revision/hash was promoted to semantic Version identity;
- material-equivalence remains purpose/family/facet specific;
- no universal last-write-wins or globally linear semantic history rule was introduced;
- target identity remains distinct from material target state;
- Version remains distinct from Provenance, Decision, Authority and Reconciliation;
- historical concept/checkpoint material remains intact with append-only downstream closure;
- Acknowledgement / Confirmation / Agreement / Consent / Participation / Responsibility / Representation state bindings remain specific and historically reconstructible;
- Evidence and evaluation history preserve source/rule material-state requirements without universal snapshot persistence;
- Routine / Recurrence / Occurrence / Schedule / Milestone history remains coherent;
- Multi-Actor Readiness, Language Map, README and workstream agree on current Version semantics;
- `main` remained unchanged during this scope;
- no prototype/backend/SQL/API/auth or global PROJECT-STATUS changes;
- no next Relationships / Reasoning candidate was preselected;
- `REOPEN = 0`;
- unclassified material dependencies = 0.

The Version / Material-State v0 write approval is therefore consumed and this checkpoint is now **post-write QA PASS**.

The next valid semantic action is a **fresh candidate re-score** over the remaining Relationships / Reasoning candidate/dependency space.

---

# 23. Downstream closure — Reconciliation / Source Precedence v0 (2026-08-13)

Reconciliation v0 resolves the checkpoint's historical `branch/merge/source-precedence mechanics` SAFE DEFERRED dependency at the semantic-boundary level without reopening Version.

Current canonical separation:

```text
Version / Material-State
= identify/reconstruct materially relevant states and divergence

Reconciliation
= contextual process/capability for handling materially competing states/assertions

Source Precedence
= bounded contextual policy/basis where justified
```

Version preserves concurrent/divergent states such as `S2A` and `S2B`; it does not pick a winner by arrival time, provider revision, source identity or technical token. Reconciliation may select, combine, correct, supersede, escalate, defer or keep the conflict unresolved under applicable bounded policy/Authority.

No universal LWW, globally linear semantic history, provider-always-wins or user-always-wins hierarchy is accepted. Technical concurrency/sync mechanisms remain implementation aids, not domain Reconciliation.

Where reconciliation yields a new material state, Version may preserve multiple predecessor states while Provenance captures material lineage. The affected domain concept still owns the resulting current/effective state under applicable Authority/Decision/policy.

History/source/conflict Visibility remains independent. AI may detect divergence or propose a merge but cannot silently erase competing state or exceed Authority/policy.

Downstream classification:

```text
Version ↔ Reconciliation          RESOLVED
Version ↔ Source Precedence       RESOLVED — not owner
Version ↔ technical concurrency   RESOLVED — distinct
```

Remaining SAFE DEFERRED items retain their existing owner/trigger/test contracts: per-family material equivalence, exact effective dating, provider mapping, retention/redaction, versioned evaluation/rule snapshots and identity-replacement thresholds.

No Version hardening failed. **Version remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/reconciliation.md`;
- `reconciliation-source-precedence-v0-validation.md`.

---

# 24. Downstream closure — Criterion / Evaluation v0 (2026-08-15)

Criterion / Evaluation v0 resolves the checkpoint's historical `versioned evaluation / rule snapshots` SAFE DEFERRED dependency without reopening Version.

Where consequence requires historical reproducibility, Evaluation binds to or reconstructs:

```text
material target state
+ materially applicable Criterion state
+ relevant Evidence/source material states or reconstructible basis
+ applicable evaluation time/window/context
```

Later Criterion revisions, corrected Evidence, target changes or reconciliation can change a later/current Evaluation without retroactively rewriting the material state basis of the earlier one.

Version still does **not** determine whether the Criterion is applicable, whether Evidence is sufficient/admissible, what the assessment is, or which conflicting source wins. Those remain Criterion/Evaluation and applicable Reconciliation/Authority/policy semantics.

The closure remains consequence-sensitive: a transient derived Evaluation need not create a durable universal Version/snapshot record for every source/rule input. Direct bindings, qualified state references, reconstructible rule/source-set bases and selectively materialized snapshots remain implementation choices.

Downstream classification:

```text
Version ↔ Criterion material state      RESOLVED
Version ↔ Evaluation historical basis   RESOLVED
universal rule-Version primitive         REJECTED
universal Evaluation snapshot            REJECTED
```

The prior regression cases for source/rule revision, stale-base AI evaluation and corrected Observation remain active. Retention/materialization strategy and exact physical/API representation remain downstream.

No Version hardening failed. **Version remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/criterion-evaluation.md`;
- `criterion-evaluation-v0-validation.md`.

---

# 25. Downstream closure — Proposal / Request v0 (2026-08-15)

Proposal / Request v0 resolves the reusable candidate/ask identity boundary that Version must preserve without becoming that identity itself.

```text
Proposal / Request
= attributable semantic act with a materially specific candidate/ask

Version / Material-State
= which materially relevant state that act concerned
```

Therefore:

```text
Version != Proposal
Version != Request
Proposal/Request != target Version
```

A materially different counter-Proposal is a distinct Proposal rather than a silent mutation inheriting prior response/Decision. A materially changed Request likewise does not silently preserve prior Acknowledgement, response, Agreement, Consent or Decision. Technical provider/storage revisions do not decide whether the candidate/ask changed materially.

Version preserves/reconstructs the relevant proposal/request state and history; Decision/Authority/policy and affected domain concepts still own response, legitimacy and effective result.

Withdrawal/expiry affects future Proposal/Request applicability without erasing historical state binding or undoing an already-established downstream effect automatically.

Downstream classification:

```text
Version ↔ Proposal / Request      RESOLVED
technical revision = Proposal     REJECTED
Version owns proposal response    REJECTED
```

No Version hardening failed. **Version remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/proposal.md`;
- `../concepts/request.md`;
- `proposal-request-v0-validation.md`.
