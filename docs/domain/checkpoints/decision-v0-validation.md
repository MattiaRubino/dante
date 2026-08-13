# Decision / Approval / Reconciliation / Effective Change v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated + post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning  
**Pre-scope validated baseline:** `e353e2756bd159b582122c4fd73b5d5d63529b30`

## Scope

This checkpoint validates the candidate family:

```text
Decision
Approval
Reconciliation
Effective canonical change
```

without presupposing that any noun must survive as a standalone primitive.

The review starts from the real problem: LifeOS must preserve materially meaningful resolution of bounded questions without collapsing proposal/response, Authority, Provenance, current state, Actual, agreement/consent, or history.

---

# 1. Evidence sequence

## EV-01 — Internal evidence

Current accepted concepts already expose the missing boundary:

- `Authority` answers who/what may legitimately make a bounded effect effective, while deferring Decision/Approval representation;
- `Actual` preserves current contextual realization while allowing conflicting assertions and deferring reconciliation/Decision mechanics;
- `Responsibility` requires reconstructible transfer/current-holder history and explicitly defers Decision/reconciliation;
- `Schedule` distinguishes proposal from current accepted placement and defers Decision/effective-change representation;
- `Provenance` explains lineage and explicitly rejects equality with Decision rationale;
- `Evidence` preserves evaluative relevance and defers Evidence-to-Decision/evaluation snapshot semantics;
- `Acknowledgement` separates taking-notice from response, Approval, Decision, effect and Actual;
- multi-actor evidence repeatedly requires proposal, acceptance, approval, canonical shared fact and Actual outcome to remain distinct.

## EV-02 — Real-world workflow inversion

Representative workflows before LifeOS mapping:

### Shared planning

Several people discuss alternatives. One option is eventually finalized. Individual preferences may remain different from the shared resolution.

### Shift swap

A worker requests a swap; the colleague accepts/declines; a manager may need to approve; only then does the effective schedule/responsibility change; actual attendance happens later.

### Conflicting reports

Several actors/providers report different actual times or outcomes. The reports remain attributable. A later reconciliation may select/correct the current contextual interpretation without erasing the original assertions.

### Reviewed material version

A proposal/version is approved. A materially changed version is not automatically covered by the earlier approval.

### AI proposal / automation

AI proposes a change. A human may reject/apply it. Separately, an already-authorized deterministic policy may legitimately apply a bounded change without fabricating a new human Decision.

## EV-03 — Targeted external benchmark

External systems/standards are benchmark evidence only.

| Benchmark | Finding | Classification |
|---|---|---|
| GitHub protected branches / pull-request reviews | approval can be required separately from merge/effect; changed content can invalidate/stale previous approval under policy | ADAPT |
| Microsoft Teams Shifts | coworker response and manager approval are distinct; schedule changes only after the applicable approval flow | ADAPT |
| W3C ActivityStreams | generic Accept/Reject actions are technically representable but do not prove one universal LifeOS Decision/Acceptance ontology | NOT APPLICABLE as kernel primitive proof |
| HL7 FHIR Provenance | lineage is target/version/process oriented and distinct from the target semantics; reinforces Provenance != Decision | ALREADY STRONGER / boundary evidence |
| OASIS XACML decision/enforcement separation | authorization decision and enforcement are separate concerns | ADAPT — separation pattern only |

LifeOS does not adopt provider nouns/state machines as ontology.

## EV-04 — Candidate minimality

Hypotheses:

```text
H0 no Decision semantics; use target state + Authority + Provenance only
H1 reusable contextual Decision semantic family
H2 universal Approval primitive
H3 universal Reconciliation primitive
H4 universal EffectiveChange object
H5 universal Decision/StateTransition mega-object for every mutation
```

Result:

```text
H0 FAIL
H1 SURVIVES
H2 FAIL as universal primitive
H3 FAIL as universal primitive
H4 FAIL as universal primitive
H5 FAIL
```

---

# 2. Candidate definition and boundaries

Canonical Decision definition:

> **Decision is the contextual resolution semantics through which a bounded decision question is explicitly determined to a specific result for a defined target, materially relevant version and context by an Actor or applicable decision process. Where the resolution itself is materially relevant, it must remain historically reconstructible together with its result, decision-maker/process and, where justified, alternatives, rationale and basis. Decision does not by itself create Authority, prove truth, guarantee downstream effect, replace the resulting domain state, establish Actual, or replace Provenance.**

Canonical question:

> **What bounded question was resolved to what result, by whom/what, about which target/version/context?**

Classification:

```text
Decision
= canonical contextual resolution semantic family/capability

not:
- universal entity/root
- every user choice
- every mutation
- Authority
- Approval super-object
- Reconciliation process
- state transition
- Provenance
- Actual
- Acknowledgement/Confirmation/Acceptance/Agreement/Consent
```

Approval:

> **Scoped Decision/review result concerning a bounded proposal/action/material version, whose governance significance depends on applicable Authority/policy.**

Reconciliation:

> **Process/pattern for comparing/resolving competing, duplicate, inconsistent or revised representations; it may culminate in a Decision but is not universally a Decision.**

Effective canonical change:

> **The resulting state transition owned by the affected domain concept; not a universal root/object.**

---

# 3. Deep chronology

```text
T0  Schedule = Monday 18:00
T1  Anna proposes Tuesday 19:00 — proposal v1
T2  Luca receives/sees it
T3  Luca Acknowledges v1
T4  Luca gives positive family-specific response
T5  Marco has applicable Authority and approves v1
T6  Decision D1: v1 approved
T7  effect is not yet active / effective time is future
T8  proposal materially changes to Tuesday 20:00 — v2
    D1 does not silently apply to v2
T9  Decision D2: v2 approved
T10 Schedule becomes Tuesday 20:00
T11 meeting actually starts 20:18
T12 Actual = 20:18
```

Required reconstruction:

```text
proposal v1 → D1 → superseded
proposal v2 → D2 → effective Schedule → later Actual
```

Canonical sequence:

```text
proposed
!= delivered/read
!= Acknowledgement
!= family-specific response
!= Approval/Decision
!= effective domain state
!= Actual
```

Decision time, effect time and Actual time are distinct.

---

# 4. Destructive reductio

```text
REMOVE Decision
→ FAIL
```

Target state + Authority + Provenance cannot always answer which bounded question was explicitly resolved, particularly when the result is reject/retain-current/defer.

```text
Decision = state change
→ FAIL
```

A Decision may retain current state; authorized policy may change state without a new explicit Decision.

```text
Decision = Authority
→ FAIL
```

Legitimacy to govern and actual resolution are distinct.

```text
Decision = Provenance
→ FAIL
```

Lineage and resolution/rationale are distinct.

```text
Decision = Confirmation
→ FAIL
```

Attestation and resolution are distinct.

```text
Decision = Acknowledgement / Acceptance
→ FAIL
```

Taking notice / workflow response and resolution are distinct.

```text
Universal Approval root
→ FAIL
```

Approval meaning remains review/Decision semantics plus policy/Authority.

```text
Universal Reconciliation root
→ FAIL
```

Reconciliation may be deterministic, human, partial, unresolved, merge/select/correct/split and does not share one independent lifecycle universally.

```text
Universal EffectiveChange root
→ FAIL
```

The changed concept already owns the resulting state.

```text
Every mutation = Decision
→ FAIL
```

Creates history volume, UI/process burden and false semantic importance.

---

# 5. CORE Semantic Validation Gate

| Test ID | Applicable | Result | Finding / hardening |
|---|---:|---|---|
| CORE-01 Real-world workflow inversion | yes | PASS | bounded resolution recurs across social/work/reconciliation/review flows |
| CORE-02 Deep chronological simulation | yes | PASS WITH HARDENING | Decision/version/effect/Actual times and applicability must stay distinct |
| CORE-03 Destructive reductio | yes | PASS | Decision survives; universal Approval/Reconciliation/EffectiveChange do not |
| CORE-04 Redundancy / merge-split | yes | PASS WITH HARDENING | Decision remains distinct from Authority/Provenance/state/Ack/response |
| CORE-05 Multidirectional traceability | yes | PASS | proposal/Evidence → Decision → target effect → Actual reconstructible |
| CORE-06 Orphan / independence | yes | PASS | Decision may exist without target mutation; mutation may exist without new Decision |
| CORE-07 External benchmark | yes | PASS | mature systems reinforce review/version/effect separation |
| CORE-08 Anti-pattern | yes | PASS | rejects last-write-wins, universal `approved=true`, generic transition root |
| CORE-09 Correction/reconciliation | yes | PASS WITH HARDENING | supersession/reversal/material revision preserve history |
| CORE-10 Scale/performance/history | yes | PASS | no Decision record required for every trivial edit |
| CORE-11 Simple/power user | yes | PASS | ordinary UX can use Apply/Keep/Approve without ontology jargon |
| CORE-12 Product value/complexity | yes | PASS WITH HARDENING | Decision appears only where resolution itself matters |
| CORE-13 Implementation pressure | yes | PASS | semantics fixed without one polymorphic Decision table/API |

**CORE Gate: PASS WITH HARDENING.**

---

# 6. Mandatory hardenings — incorporated

1. Decision is bounded/contextual.
2. No Decision != reject != retain-current != defer != unresolved.
3. Consequential Decision binds to the materially relevant question/target/version.
4. Material target/version change does not inherit prior Decision/Approval automatically.
5. Decision != Authority.
6. Decision != effective domain change.
7. Decision != Actual/objective truth.
8. Decision != Acknowledgement/Confirmation/family-specific Acceptance/Agreement/Consent.
9. Decision may cause zero, one or multiple effects.
10. Effective change may occur without a new explicit Decision under an already-authorized bounded policy/process.
11. Decision time != effect time != Actual realization time.
12. Superseded/reversed Decisions remain historically reconstructible where material.
13. One Actor's Approval/Decision != collective Decision automatically.
14. Aggregate `approved` may be derived from policy requirements.
15. Decision result Visibility != rationale Visibility != supporting Evidence/Provenance Visibility.
16. AI proposal/recommendation != Decision.
17. AI/system Decision semantics require explicit bounded policy/Authority and must never fabricate a human Decision.
18. Deterministic reconciliation != human Decision automatically.
19. The affected domain concept owns its effective state transition.
20. Ordinary low-consequence edits do not require durable Decision records where the resolution itself has no independent product/domain value.

---

# 7. Multi-Actor Compatibility Gate

| Test ID | Applicable | Result | Finding / hardening |
|---|---:|---|---|
| MA-01 Identity / Account Independence | yes | PASS | external/accountless approver/decision-maker may exist |
| MA-02 Shared Fact / Actor Overlay | yes | PASS WITH HARDENING | shared Decision != every actor's personal stance |
| MA-03 Responsibility / Assignment / Claim | yes | PASS WITH HARDENING | Decision may authorize/resolve transfer but is not Responsibility |
| MA-04 Stewardship / Mental Load | yes | PASS | Decision does not transfer coordination burden automatically |
| MA-05 Common Ground / State Separation | yes | PASS WITH HARDENING | Ack/response/Decision/effect remain distinct |
| MA-06 Authority / Canonical Change | yes | PASS WITH HARDENING | Decision does not manufacture Authority |
| MA-07 Selective Disclosure | yes | PASS WITH HARDENING | result/rationale/Evidence visibility may differ |
| MA-08 Inference Privacy | yes | PASS WITH HARDENING | private basis cannot leak through explanations |
| MA-09 Partial Adoption / External Participant | yes | PASS | external reviewer/approver requires no synthetic Account |
| MA-10 Assisted Participation / Provenance | yes | PASS WITH HARDENING | helper/recorder != decision-maker/represented party |
| MA-11 Lifecycle / Revocation | yes | PASS WITH HARDENING | reversed/superseded Decisions remain history |
| MA-12 Conflict / Adversarial | yes | PASS WITH HARDENING | competing Decisions/assertions may remain unresolved pending governance/reconciliation |
| MA-13 Unequal Power / Guardian / Caregiver | yes | PASS WITH HARDENING | authoritative Decision != represented person's Agreement/Consent |
| MA-14 Multi-Resource / Capacity | yes | PASS | allocation Decision != feasibility/capacity truth |
| MA-15 Coordination Burden | yes | PASS WITH HARDENING | no mandatory approvals/Decision objects for casual life |
| MA-16 Progressive Formality | yes | PASS | simple choose/apply to formal decision history by consequence |
| MA-17 AI Authority / Multi-Party | yes | PASS WITH HARDENING | AI recommendation != human Decision; bounded system Decision only under policy/Authority |
| MA-18 Specialist Boundary | yes | PASS | external authoritative systems may remain sources of record |
| MA-19 Primitive Redundancy | yes | PASS | Decision survives; universal Approval/Reconciliation/EffectiveChange do not |
| MA-20 Actor-Scoped Reality Attribution | yes | PASS WITH HARDENING | shared Decision does not rewrite individual stance or Actual |

**Multi-Actor Gate: PASS WITH HARDENING.**

---

# 8. Cross-Concept Consistency Gate

| Test ID | Result | Closure |
|---|---|---|
| XCON-01 Identity | PASS | no Person/Actor/Account identity collision |
| XCON-02 Ownership / Authority | PASS WITH HARDENING | Authority legitimizes bounded governance effect; Decision remains resolution |
| XCON-03 Planned/current/Actual/history | PASS WITH HARDENING | proposal, Decision, effective state, Actual and history remain separate |
| XCON-04 Relationship | PASS | material Decision may use qualified contextual structure without universal root |
| XCON-05 Multi-actor | PASS WITH HARDENING | shared resolution != unanimous stance/agreement |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Decide/Approve/Keep/Reject/Apply require precise mapping |

**Structural reopening of prior accepted concepts: 0.**

---

# 9. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Decision ↔ Authority | resolution != governance capability |
| Decision ↔ Acknowledgement | taking-notice != resolution |
| Decision ↔ Confirmation | attestation != resolution |
| Decision ↔ family-specific Acceptance | workflow response != Decision by default |
| Decision ↔ Responsibility | resolving transfer != accountability state itself |
| Decision ↔ Schedule | resolving proposal != current temporal state |
| Decision ↔ Actual | contextual resolution != realized truth |
| Decision ↔ Provenance | resolution/rationale != lineage |
| Decision ↔ Evidence | evaluation input/use != resolution |
| Approval ↔ Decision | Approval retained as scoped Decision/review result |
| Reconciliation ↔ Decision | process/pattern may culminate in Decision; not universal equality |
| Effective change ↔ Decision | changed concept owns resulting state |

## SAFE DEFERRED — Agreement / Consent

**Unresolved:** independent mutual-assent/commitment and voluntary bounded permission semantics.  
**Why safe:** Decision can remain resolution without absorbing mutuality, voluntariness, purpose or withdrawal.  
**Owner:** Agreement / Consent review.  
**Reopening trigger:** Decision begins absorbing mutual assent, purpose-scoped permission or withdrawal semantics.  
**Tests to rerun:** CORE-03, CORE-04, CORE-09, MA-05, MA-06, MA-07, MA-13, MA-19, MA-20, XCON-02, XCON-04, XCON-05.

## SAFE DEFERRED — Version / material-equivalence mechanics

**Unresolved:** exact material-version and equivalence representation.  
**Why safe:** version binding is already mandatory semantically.  
**Owner:** Version + logical model.  
**Reopening trigger:** Decision/Approval cannot safely bind to the reviewed state or determine applicability after revision.  
**Tests to rerun:** CORE-02, CORE-09, CORE-10, CORE-13, MA-11, MA-12, XCON-03.

## SAFE DEFERRED — Principal / delegation / on-behalf-of

**Unresolved:** authenticated Principal, represented party and delegated decision Authority mechanics.  
**Why safe:** actual decision Actor/process and Authority already remain separate.  
**Owner:** Principal/delegation/security review.  
**Reopening trigger:** delegated Decision attribution cannot be represented without collapsing Person/Actor/Account/Principal.  
**Tests to rerun:** CORE-06, CORE-09, CORE-13, MA-01, MA-06, MA-10, MA-11, MA-13, MA-17, XCON-01, XCON-02.

## SAFE DEFERRED — Proposal / request representation

**Unresolved:** whether proposals need reusable independent identity across families.  
**Why safe:** current families can own proposal semantics while Decision binds to the materially relevant target/version.  
**Owner:** proposal/reasoning logical review.  
**Reopening trigger:** cross-family proposal history becomes duplicated or Decision cannot target the exact proposal/version without a stronger abstraction.  
**Tests to rerun:** CORE-03, CORE-04, CORE-06, CORE-13, MA-05, MA-19, XCON-04.

## SAFE DEFERRED — Detailed reconciliation policy

**Unresolved:** source precedence, merge/select/correct/split rules and policy evaluation.  
**Why safe:** Reconciliation process boundary is fixed without a universal policy engine.  
**Owner:** reasoning/policy + logical model.  
**Reopening trigger:** current truth/effective state cannot be established or reconstructed without giving Reconciliation universal independent identity.  
**Tests to rerun:** CORE-02, CORE-04, CORE-09, CORE-13, MA-06, MA-12, MA-18, XCON-03.

## SAFE DEFERRED — Collective Decision / quorum / voting

**Unresolved:** persistent collective decision-formation semantics.  
**Why safe:** shared Decision can currently remain distinct from individual Actor stances.  
**Owner:** collective/group semantics.  
**Reopening trigger:** ordinary LifeOS workflows require a persistent collective Actor/quorum/voting identity to establish Decision.  
**Tests to rerun:** CORE-04, CORE-06, CORE-12, MA-02, MA-05, MA-06, MA-13, MA-19, MA-20, XCON-01, XCON-04, XCON-05.

## SAFE DEFERRED — GoalCriterion / evaluation

**Unresolved:** when evaluation/attainment is derived state versus explicit Decision.  
**Why safe:** Decision != Evidence/evaluation is fixed.  
**Owner:** GoalCriterion / evaluation review.  
**Reopening trigger:** Goal/Milestone attainment cannot be established without making Decision the evaluation engine.  
**Tests to rerun:** CORE-03, CORE-04, CORE-05, CORE-09, MA-06, MA-19, XCON-03, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 10. Hardest adversarial scenario log

| Scenario | Stress | Result |
|---|---|---|
| proposal rejected / current state retained | Decision without mutation | meaningful Decision survives |
| already-authorized deterministic policy changes state | mutation without new human Decision | no fabricated human Decision |
| proposal v1 approved then materially revised to v2 | Version | prior approval does not silently carry |
| shift swap colleague accepts but manager approval required | response vs Approval/Authority/effect | stages remain distinct |
| conflicting Actual assertions | reconciliation | assertions preserved; explicit resolution may create Decision |
| manager decides while employee disagrees | unequal power | Decision != Agreement/Consent |
| one committee member approves | collective inference | not automatically collective Decision |
| AI recommends option X | AI | recommendation != Decision |
| AI applies bounded pre-authorized policy | system Decision/effect | attribution/policy/Authority required; not human Decision |
| Decision result shared but rationale relies on private health fact | selective disclosure | result may be visible while rationale/Evidence remains private |
| later reversal | history | reversed != never decided |
| creator/source changes target without Authority | governance | write/provenance does not automatically establish legitimate Decision/effect |

---

# 11. Reopening / dependency register

| Finding | Severity | Current treatment | Reopening trigger |
|---|---|---|---|
| bounded resolution has independent value | STRUCTURAL | canonical Decision family | stronger model proves complete redundancy |
| every mutation = Decision | ANTI-PATTERN | rejected | only reopen if history/query semantics require durable resolution for all mutations |
| Approval has scoped meaning | HARDENING | Decision/review semantics | independent cross-domain identity/lifecycle appears |
| Reconciliation is broader/different than Decision | STRUCTURAL | process/pattern | universal independent lifecycle becomes necessary |
| target owns effective state | STRUCTURAL | canonical rule | target concepts cannot preserve effective transitions without generic root |
| material-version binding | HARDENING | invariant now; mechanics deferred | applicability cannot be determined after edit |
| delegated/on-behalf-of Decision | DEFERRED DEPENDENCY | SAFE DEFERRED | attribution/Authority collapse appears |
| Agreement / Consent | DEFERRED DEPENDENCY | SAFE DEFERRED | Decision starts absorbing assent/permission |
| collective Decision formation | DEFERRED DEPENDENCY | SAFE DEFERRED | common workflows require quorum/voting/collective identity |
| Decision overuse | PRODUCT / UX | consequence-sensitive persistence/UI | casual user coordination becomes workflow bureaucracy |

---

# 12. Regression corpus additions

| ID | Scenario | Boundary |
|---|---|---|
| R-DEC-01 | proposal v1 approved → material v2 → prior approval not inherited | Decision + Version/history |
| R-DEC-02 | shift swap request → coworker response → manager Approval/Decision → effective Responsibility/Schedule → later Actual | response + Authority + effect + Actual |
| R-DEC-03 | conflicting Actual assertions → reconciliation → explicit Decision → corrected current Actual → assertions preserved | Decision + Actual + Provenance |
| R-DEC-04 | reject / retain-current resolution | Decision without mutation |
| R-DEC-05 | already-authorized deterministic policy → effective change | effect without fabricated human Decision |
| R-DEC-06 | shared Decision + different actor stances + private rationale/Evidence | multi-actor + privacy |

---

# 13. Concept-family verdict

```text
DECISION / APPROVAL / RECONCILIATION / EFFECTIVE-CHANGE FAMILY
PASS WITH HARDENING
```

Accepted current result:

```text
Decision
✅ canonical contextual bounded resolution semantic family/capability
❌ universal entity/root
❌ every mutation
❌ Authority/Provenance/Actual

Approval
✅ scoped Decision/review result
❌ universal primitive/root
❌ Authority/effective change

Reconciliation
✅ process/pattern
✅ may culminate in Decision
✅ may remain unresolved
❌ universal primitive/root

Effective canonical change
✅ real transition owned by affected domain concept
❌ universal EffectiveChange object/root
```

Hardenings are incorporated in `concepts/decision.md` and this checkpoint.

```text
REOPEN = 0
unclassified material dependencies = 0
```

---

# 14. Documentation propagation — approved scope

The approved Decision v0 milestone propagation was:

### CREATE

- `docs/domain/concepts/decision.md`
- `docs/domain/checkpoints/decision-v0-validation.md`

### UPDATE — current canonical state

- `docs/domain/language-map.md`
- `docs/domain/README.md`
- `docs/workstreams/domain-model.md`
- `docs/domain/multi-actor-readiness-v1.md`

### UPDATE — downstream closure / accepted concept compatibility

- `docs/domain/concepts/authority.md`
- `docs/domain/checkpoints/authority-v0-validation.md`
- `docs/domain/concepts/actual.md`
- `docs/domain/checkpoints/actual-v0-validation.md`
- `docs/domain/concepts/responsibility.md`
- `docs/domain/checkpoints/responsibility-v0-validation.md`
- `docs/domain/concepts/provenance.md`
- `docs/domain/checkpoints/provenance-v0-validation.md`
- `docs/domain/concepts/evidence.md`
- `docs/domain/checkpoints/evidence-v0-validation.md`
- `docs/domain/concepts/schedule.md`
- `docs/domain/checkpoints/time-v0.md`
- `docs/domain/concepts/confirmation.md`
- `docs/domain/checkpoints/confirmation-v0-validation.md`
- `docs/domain/concepts/acknowledgement.md`
- `docs/domain/checkpoints/acknowledgement-v0-validation.md`
- `docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`

Historical product discovery/research, old product glossary, cross-cluster v4, root README and PROJECT-STATUS were intentionally not rewritten.

---

# 15. Post-write QA — PASS

Validated against:

```text
e353e2756bd159b582122c4fd73b5d5d63529b30
```

QA result at Decision milestone closure:

```text
approved paths changed               23 / 23
out-of-scope paths                    0
new Decision files                    2 / 2
structural REOPEN                     0
unclassified material dependencies   0
main unchanged
branch behind main                    0
```

Authority/Actual/Responsibility/Provenance/Evidence/Schedule/Confirmation/Acknowledgement boundaries remained intact; generic Approval/Reconciliation/EffectiveChange roots remained rejected; historical material was preserved through downstream amendments rather than silent rewrite.

---

# 16. Downstream closure — Agreement / Consent v0 (2026-08-13)

Agreement / Consent v0 resolves the Decision checkpoint's historical `Agreement / Consent` SAFE DEFERRED item without reopening Decision.

Current canonical separation:

```text
Decision
= bounded contextual resolution to a specific result

Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure under defined scope/purpose/context
```

Therefore:

```text
Decision ↔ Agreement  RESOLVED
Decision ↔ Consent    RESOLVED
```

The prior adversarial case `manager decides while employee disagrees` remains a regression guardrail: valid Decision does not fabricate Agreement/Consent. Conversely, mutual Agreement may exist before an Authority-dependent effect, and Consent may constrain future action/use without becoming the Decision.

The historical Agreement/Consent dependency is now closed downstream. Remaining SAFE DEFERRED Decision dependencies are Version/material equivalence, Principal/delegation, Proposal identity, detailed reconciliation/source precedence, collective Decision/quorum/voting, GoalCriterion/evaluation, exact persistence/API, and specialist approval/signature/legal workflows.

No Decision hardening failed; **Decision remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/agreement.md`;
- `../concepts/consent.md`;
- `agreement-consent-v0-validation.md`.

---

# 17. Downstream closure — Representation / on-behalf-of v0 (2026-08-13)

Representation v0 resolves the checkpoint's historical `Principal / delegation / on-behalf-of` dependency without reopening Decision.

Canonical separation:

```text
actual decision Actor/process
= who/what actually performed the bounded resolution

Representation / on-behalf-of
= actual decision Actor/process acted for a distinct represented party in that bounded context

Authority / delegation basis
= whether the Decision/effect is legitimate for the represented context

Principal
= technical authenticated/authorized request identity
```

Therefore:

```text
actual decision Actor != represented party by default
Representation != Decision
Representation != Authority
Principal != Decision Actor
```

A represented Decision can govern another party's context only when the applicable Authority/process permits it. Even then, the represented party is not rewritten as the historical decision-maker and the action does not imply their personal Agreement, Consent, Acknowledgement or Confirmation.

AI/service Decision processes preserve the same attribution rule: when they actually perform the bounded process under valid policy, they remain the attributable Actor/process rather than being laundered into a human Decision.

Downstream classification:

```text
Decision ↔ Representation/on-behalf-of   RESOLVED
Principal as domain primitive            REJECTED
universal Delegation primitive           REJECTED
```

Exact Principal/AuthN/AuthZ enforcement, action-specific delegability, Version/material equivalence, Proposal identity, detailed reconciliation/source precedence, collective Decision, GoalCriterion/evaluation and specialist approval/signature/legal validity remain SAFE DEFERRED.

No Decision hardening failed. **Decision remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/representation.md`;
- `representation-delegation-principal-v0-validation.md`.

---

# 18. Downstream closure — Version / Material-State v0 (2026-08-13)

Version / Material-State v0 resolves the checkpoint's historical `Version / material-equivalence mechanics` SAFE DEFERRED dependency without reopening Decision.

The original V3 rule now has an explicit shared state model:

```text
Decision D1 / Approval A1 -> materially reviewed state S1
later materially changed state S2
→ S1 remains reconstructible
→ D1/A1 remain historical decisions about S1
→ D1/A1 do not silently apply to S2
```

Materiality is purpose/facet scoped and cannot be inferred from a database update, provider revision, ETag/MVCC token, content hash or same target ID. A materially equivalent later state may remain covered where the owning policy explicitly supports that equivalence.

Version also strengthens the existing Reconciliation boundary:

```text
state S1
├─ divergent S2A
└─ divergent S2B

Version/material-state
= preserve/reconstruct the divergence

Reconciliation / Decision / Authority
= determine select/merge/correct/retain-unresolved behavior where applicable
```

No universal last-write-wins or globally linear history is accepted.

Downstream classification:

```text
Decision/Approval ↔ Version/material state       RESOLVED
Version ↔ Reconciliation                         RESOLVED — not equal
Version ↔ Authority                              RESOLVED — not equal
Version ↔ Provenance                             RESOLVED — state vs lineage
technical/provider revision ↔ material Version   RESOLVED — not equal
```

Remaining SAFE DEFERRED Decision dependencies:

- proposal/request reusable identity;
- detailed reconciliation/source-precedence policy;
- collective Decision/quorum/voting;
- GoalCriterion/evaluation;
- exact persistence/cardinality/API;
- specialist approval/signature/legal workflows.

AI/system decision proposals/actions must retain their material base state where consequence requires it. If the target materially changes before effect, blind stale application is prohibited; applicability must be re-evaluated under the owning policy/Authority.

Mandatory regression reuse:

- `R-DEC-01` proposal v1 approval → material v2;
- `R-VER-06` concurrent divergent edits;
- `R-VER-07` stale-base AI proposal.

No Decision hardening failed. **Decision remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.

---

# 19. Downstream closure — Reconciliation / Source Precedence v0 (2026-08-13)

Reconciliation v0 resolves the checkpoint's historical detailed reconciliation/source-precedence dependency without reopening Decision.

Current separation:

```text
Reconciliation
= process/capability for handling materially competing states/assertions

Decision
= explicit bounded resolution to a specific result where the resolution itself is material
```

A Reconciliation may culminate in a Decision, but unresolved conflict and deterministic already-authorized reconciliation remain valid without fabricating a human Decision. Many Decisions also have no preceding conflict/reconciliation.

Evidence, Provenance, Authority and contextual Source Precedence may inform the basis while remaining distinct. Source identity/recency does not become Decision; Decision does not create Authority or objective truth.

If reconciliation leads to an effective change, the affected domain concept owns current state. Version/Provenance preserve materially relevant predecessor/basis history, and later reversal/correction does not rewrite the prior Decision.

Decision-result Visibility remains distinct from conflict, rationale, Evidence, Provenance and source Visibility.

Downstream classification:

```text
Decision ↔ Reconciliation        RESOLVED
Decision ↔ Source Precedence     RESOLVED — basis, not identity
Decision ↔ effective state       RESOLVED — not owner
```

Remaining SAFE DEFERRED dependencies include Proposal/request reusable identity, collective/quorum/voting semantics, GoalCriterion/evaluation, Trigger/policy mechanics, exact persistence/API and specialist approval/signature/legal validity.

No Decision hardening failed. **Decision remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/reconciliation.md`;
- `reconciliation-source-precedence-v0-validation.md`.