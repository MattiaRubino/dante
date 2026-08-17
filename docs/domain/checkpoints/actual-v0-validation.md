# Actual v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted current baseline  
**Date:** 2026-08-11  
**Concept:** Actual v0  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Scope

This checkpoint validates whether LifeOS requires a distinct `Actual` concept and, if so, how narrowly it must be defined.

Primary adjacent concepts:

- Activity;
- Event;
- Occurrence;
- Schedule;
- Session;
- future Outcome;
- future Observation;
- future Evidence;
- future Confirmation;
- future Provenance;
- future Participation/Relationship.

Primary risk:

> turning `Actual` into a universal reality mega-object or duplicating semantics already owned by Session, Observation, Outcome, Evidence, or Provenance.

---

# 2. Evidence reviewed

## Internal evidence

Reviewed:

- accepted Activity v0;
- accepted Event v0;
- accepted Occurrence v0;
- accepted Schedule v0;
- accepted Session v0;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-confirmation-and-reminders.md`;
- feature-discovery scenarios;
- Multi-Actor Readiness v1;
- multi-actor discovery simulation and research;
- current Language Map;
- Methodology v3.

Key inherited invariants:

```text
planned != actual
Schedule != actual timing
passage of time != completion
Session != broader outcome
source/provenance != truth
later relevance != original intention
```

## External benchmark evidence

| Source/pattern | Finding | Classification |
|---|---|---|
| HL7 FHIR Procedure + Observation + Provenance | performed action/occurrence, observations, and provenance are separable concerns | ADAPT |
| Android Health Connect exercise-session model | central executed session coexists with separate measurement records | ADAPT |
| Health Connect planned vs executed exercise records | planned and executed representations remain distinguishable | ADAPT |
| FHIR Task | one workflow resource spans intended through completion states | ANTI-PATTERN for LifeOS core |

External systems were treated as evidence rather than target schemas.

---

# 3. Accepted candidate definition

> **An Actual is a persistent contextual realization record representing whether and how a specific intended or expected domain subject was realized in reality. It preserves the realized truth of that expectation without replacing the Sessions, Observations, Outcomes, participation records, Confirmations, or Provenance that describe particular facets of what happened or how LifeOS knows it.**

Domain question:

> **How did this specific intention or expectation resolve in reality?**

Identity:

- contextual to a specific expected/intended subject;
- stable across ordinary correction of realization details;
- not derived solely from timestamps or provider identity.

Independent existence:

- Actual requires expectation/intention context;
- spontaneous reality may exist through Session/Observation/etc. without Actual.

Nearest boundaries:

```text
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
```

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| CORE-01 Workflow inversion | yes | task/event/routine execution and retrospective capture | PASS | Actual naturally reconciles expectation with reality without changing original intent |
| CORE-02 Deep chronology | yes | plan → execution → late import → correction → historical query | PASS WITH HARDENING | correction must preserve assertion/source history |
| CORE-03 Reductio | yes | REMOVE / MERGE / SPLIT / UNIVERSALIZE / INVERT / EXTREME | PASS WITH HARDENING | REMOVE and merges fail; universal Actual mega-object rejected |
| CORE-04 Redundancy | yes | Actual vs Session/Outcome/Observation | PASS | distinct domain question and lifecycle role survive pairwise tests |
| CORE-05 Traceability | yes | expectation → Actual → facts/evaluation and retrospective reality | PASS | Actual supports downward reconciliation without fabricating upward intention |
| CORE-06 Orphan/independence | yes | weight record, spontaneous debugging | PASS WITH HARDENING | reality may exist without Actual; Actual is contextual rather than universal |
| CORE-07 External benchmark | yes | FHIR / Health Connect | PASS | separation patterns support bounded realization concept |
| CORE-08 Anti-pattern review | yes | universal event log; overloaded workflow object | PASS | reject generic reality container and intention/execution collapse |
| CORE-09 Correction/reconciliation/epistemic integrity | yes | conflicting imported/user times | PASS WITH HARDENING | current accepted Actual may change while provenance/assertion history remains |
| CORE-10 Scale/performance/history | yes | long activity history, large imports | PASS | no need for Actual per measurement/session; avoids unnecessary duplication |
| CORE-11 Simple vs power user | yes | ordinary completion UI vs detailed history | PASS | Actual can remain hidden/advanced in UI |
| CORE-12 Product value/complexity cost | yes | unknown vs confirmed non-execution; event occurrence reconciliation | PASS | semantic benefit exceeds hidden-model cost |
| CORE-13 Implementation pressure | yes | temptation to duplicate timestamps/results on Actual | PASS WITH HARDENING | persistence must reference/compose facts rather than duplicate them |

## Core-gate hardenings

1. `Actual` is explicitly contextual, not universal reality.
2. Absence of Actual is not a negative outcome.
3. Known non-realization is a valid realized state and differs from unknown.
4. Actual does not duplicate Session timing/Observation measurements/Outcome semantics.
5. Correction preserves relevant source/assertion history.
6. Provider identity does not define Actual identity.

---

# 5. Adversarial Reductio Detail

## REMOVE

Without Actual, LifeOS must either:

- mutate expected objects into reality;
- overload Session;
- overload Outcome;
- use Observation for complex occurrence realization;
- duplicate reconciliation logic per subject type.

**Result:** REMOVE fails.

## MERGE WITH SESSION

Counterexample:

```text
Event meeting occurred 10:08-11:23
```

The Event has realized occurrence but does not require performed-work Session semantics.

Also one Activity may use several Sessions but one broader realization context.

**Result:** MERGE fails.

## MERGE WITH OUTCOME

Counterexample:

```text
Actual: meeting occurred
Outcome: no decision reached
```

Occurrence and result differ.

**Result:** MERGE fails.

## MERGE WITH OBSERVATION

Measurements/simple assertions may exist independently and may contextualize one Actual.

**Result:** MERGE fails.

## MAKE UNIVERSAL

Forcing Actual around every measurement, transaction, spontaneous Session, or imported fact creates meaningless wrappers and generic-object drift.

**Result:** UNIVERSALIZE fails.

## INVERT

Assumption:

```text
no Actual => not done
```

breaks unknown/unconfirmed reality and contradicts existing LifeOS rules.

**Result:** INVERT fails.

## EXTREME

Large imports and years of measurement history do not require Actual wrappers unless specific expectations are reconciled.

**Result:** bounded model scales semantically better.

---

# 6. Multi-Actor Compatibility Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| MA-01 Identity/account independence | yes | shared event with external participants | PASS | Actual identity is not account identity |
| MA-02 Shared fact/actor overlay | yes | one meeting + individual attendance | PASS WITH HARDENING | shared Actual must coexist with actor-scoped participation reality |
| MA-03 Responsibility/assignment/claim | yes | expected performer differs from actual performer | PASS | performer relation does not redefine Activity/Actual identity |
| MA-04 Stewardship/mental load | limited | coordinator records another actor's execution | PASS | coordination burden remains separate future relation/product concern |
| MA-05 Common ground/state separation | yes | message says task done vs actual confirmed execution | PASS | assertion/acknowledgement does not itself establish Actual |
| MA-06 Authority/canonical change | yes | conflicting actor/provider claims | PASS WITH HARDENING | Actual needs contextual authority/reconciliation without owning full authority model |
| MA-07 Selective disclosure | yes | private appointment produces busy projection | PASS | private Actual may yield safe derived projection |
| MA-08 Inference privacy | yes | AI uses private Actual to coordinate | PASS | computation does not grant disclosure permission |
| MA-09 Partial adoption/external participant | yes | meeting attendee without LifeOS | PASS | actor participation can be represented without account dependency |
| MA-10 Assisted participation/provenance | yes | caregiver records medication | PASS WITH HARDENING | subject, performer, recorder, confirmer must remain distinguishable |
| MA-11 Relationship lifecycle/revocation | limited | former participant retains historical attribution | PASS | current access and historical Actual attribution remain separable |
| MA-12 Conflict/adversarial relationship | yes | actors disagree on whether task completed | PASS WITH HARDENING | conflicting assertions must not be flattened prematurely |
| MA-13 Unequal power | yes | caregiver/manager/clinician contexts | PASS | role/authority context remains external to Actual identity |
| MA-14 Multi-resource/capacity | limited | realized meeting uses room and people | PASS | Actual does not become resource-reservation record |
| MA-15 Coordination-burden distribution | limited | repeated confirmation requests | PASS | product policy must avoid forcing every actor to confirm low-value reality |
| MA-16 Formality/progressive disclosure | yes | casual event vs regulated hand-off | PASS | same semantics may expose different confirmation detail by consequence |
| MA-17 AI authority/multi-party context | yes | AI infers likely completion | PASS WITH HARDENING | AI inference cannot silently establish/disclose canonical Actual |
| MA-18 Specialist-system boundary | yes | healthcare/workforce authoritative systems | PASS | LifeOS may reconcile around external facts without replacing specialist authority |
| MA-19 Multi-actor primitive redundancy | yes | shared Actual + actor participation | PASS | no new generic SharedActual/ActorActual primitive justified now |
| MA-20 Actor-scoped reality attribution | yes | partial attendance; collaborative Session | PASS WITH HARDENING | shared realization and individual participation facts must remain separable |

## Multi-actor hardenings

1. Shared Actual does not imply identical actor participation.
2. Actual performer may differ from expected performer/responsible actor.
3. Subject, recorder, confirmer, and performer may differ.
4. Conflicting assertions do not become one fact merely because they concern one expectation.
5. AI/system reasoning over private Actual does not imply disclosure rights.
6. No LifeOS Account is required for every represented participant.

---

# 7. Cross-Concept Consistency Gate

| Test ID | Applicable | Result | Notes |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS | does not redefine Activity/Event/Occurrence/Session identity |
| XCON-02 Ownership/authority compatibility | yes | PASS | authority remains distinct and deferred |
| XCON-03 Planned/current/actual/history compatibility | yes | PASS | strengthens existing separation |
| XCON-04 Relationship compatibility | yes | PASS | replacement/participation/conflict remain future typed relationships |
| XCON-05 Multi-actor readiness compatibility | yes | PASS | shared fact + actor overlay remains intact |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE | Actual promoted from DEFERRED to CANONICAL after acceptance |

---

# 8. Hardest scenario log

| Scenario | Stress | Result | Model change |
|---|---|---|---|
| scheduled medication, no response | unknown vs non-execution | PASS after hardening | absence of Actual cannot mean missed |
| user confirms medication skipped | known negative realization | PASS | Actual can represent non-realization |
| meeting occurred, participants differ | shared vs actor-specific reality | PASS after hardening | actor participation separate |
| three work Sessions complete one Activity | cardinality | PASS | Actual not Session-per-slice |
| spontaneous debugging | orphan reality | PASS | Session can exist without Actual/intention |
| imported measurement | mega-object pressure | PASS | Observation may exist independently |
| conflicting provider/user timestamps | correction/provenance | PASS after hardening | preserve assertion history |
| caregiver records action for another subject | assisted provenance | PASS after hardening | subject/performer/recorder separate |
| AI predicts completion | epistemic integrity | PASS after hardening | inference does not establish Actual |
| replacement transport method | history rewrite | PASS | original expectation preserved |

---

# 9. Reopening / dependency register

| Finding | Severity | Current treatment | Reopening trigger |
|---|---|---|---|
| Actual vs Outcome exact boundary | DEFERRED DEPENDENCY | separate concepts provisionally validated | Outcome v0 review |
| Actual vs Observation exact boundary | DEFERRED DEPENDENCY | measurements/facts remain separate | Observation v0 review |
| current accepted truth vs competing assertion storage | DEFERRED DEPENDENCY | provenance/authority requirement recorded | Provenance/Confirmation review |
| actor-scoped participation representation | DEFERRED DEPENDENCY | semantic separation fixed | Relationship/Participation review |
| physical Actual cardinality | DEFERRED DEPENDENCY | no SQL decision | logical data model |
| risk of generic reality mega-object | STRUCTURAL | explicitly prohibited | any proposal broadening Actual beyond realization context |

---

# 10. Concept verdict

**PASS WITH HARDENING**

The concept survives removal, merge, split, universalization, chronological, reconciliation, multi-actor, privacy, authority, and implementation-pressure tests.

The hardenings are already incorporated into `concepts/actual.md`.

No structural reopening of accepted Intention/Execution or Time concepts is required.

Mandatory future re-tests:

- Actual vs Outcome;
- Actual vs Observation;
- Actual vs Confirmation/Provenance;
- collaborative Actual/Session attribution;
- Reality/Evidence cluster checkpoint;
- whole-domain multi-actor gate;
- logical/persistence pressure gate.

---

# 11. Regression corpus additions

| Scenario | New boundary | Reuse trigger |
|---|---|---|
| scheduled item with no evidence after time passes | unknown != non-execution | every outcome/confirmation model |
| shared event occurred but participant attendance differs | shared Actual != actor reality | Event/Participation/Actual models |
| caregiver records execution for another subject | subject != performer != recorder | Observation/Provenance/Authority models |
| conflicting actor/provider reports | assertion != accepted Actual | Provenance/Confirmation/Version models |
| spontaneous Session without prior intent | reality != fabricated intention | every bottom-up capture model |

---

# 12. Documentation propagation

Completed in the Actual v0 acceptance pass:

- concept specification created;
- validation checkpoint created;
- Language Map promoted Actual to CANONICAL;
- Domain Atlas README updated;
- workstream handoff updated;
- reopening triggers recorded;
- Methodology v3 remains the mandatory standard.

---

# 13. Downstream closure — Decision v0 (2026-08-13)

Decision v0 resolves the later semantic part of Actual's reconciliation dependency without changing the historical Actual v0 test result.

Current closure:

```text
competing assertion/report
!= Decision
!= current Actual

Decision
= explicit bounded resolution when materially relevant

Actual
= current established contextual realization
```

A Decision may select/correct the current interpretation under applicable Authority/policy, while earlier assertions and their Provenance remain reconstructible. A Decision does not create objective reality and does not replace Actual.

Reconciliation remains a process/pattern and may be deterministic or remain unresolved; it is not a universal entity. An already-authorized deterministic reconciliation may change current Actual without fabricating a new human Decision. A Decision may also reject a proposed correction and leave Actual unchanged.

The affected Actual owns its effective state transition. No universal `EffectiveChange` root is required.

Downstream classification:

```text
Actual ↔ Decision             RESOLVED
Actual ↔ Reconciliation       RESOLVED at semantic boundary
Decision ↔ objective truth    RESOLVED — not equal
```

Version/material-equivalence mechanics, detailed reconciliation/source-precedence policy, Principal/enforcement and physical Actual representation remain independently deferred.

**Actual v0 remains PASS WITH HARDENING. REOPEN = 0.**

Normative downstream references:

- `../concepts/decision.md`;
- `decision-v0-validation.md`.

---

# 14. Downstream closure — Version / material-equivalence v0 (2026-08-13)

Version v0 resolves the checkpoint's historical `Version / material-equivalence` dependency without changing the original Actual validation result.

Current closure:

```text
Actual identity
!= materially relevant Actual state
!= technical/provider record revision

Version
= purpose/facet-scoped reference to the materially relevant Actual state
```

A Confirmation, Decision, Evidence evaluation or reconciliation result that concerned Actual state v1 remains attributable to v1. A material correction to v2 does not silently rewrite the historical evaluation or make it applicable to v2 by default. Non-material equivalence may preserve applicability only when the relevant purpose/facet is unchanged.

Conflicting/offline assertions may diverge from one prior state and remain historically valid as competing branches. Version preserves those state references but does not choose current truth; current Actual selection still belongs to the applicable reconciliation/Authority/Decision policy.

Provider revision IDs, ETags, hashes and storage row versions may support concurrency or lineage but do not define semantic Actual materiality automatically. Historical references also do not require retaining every sensitive source payload indefinitely.

Downstream classification:

```text
Actual ↔ Version/material equivalence   RESOLVED
Version ↔ current truth selection       RESOLVED — not owner
```

Detailed reconciliation/source precedence, Principal/enforcement, retention and physical representation remain separately owned.

No original Actual hardening failed. **Actual remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.

---

# 15. Downstream closure — Reconciliation / Source Precedence v0 (2026-08-13)

Reconciliation v0 resolves the checkpoint's historical detailed reconciliation/source-precedence dependency without changing the original Actual validation result.

Current closure:

```text
competing assertions / material states
!= Reconciliation process
!= current Actual

Reconciliation
= contextual process/capability that preserves and handles material competition under a bounded basis

Actual
= current established contextual realization owned by Actual semantics
```

Reconciliation may preserve conflict unresolved, apply bounded source-of-record policy, use Evidence/Provenance, culminate in Decision, or deterministically establish/correct current Actual under already-authorized policy. It does not fabricate human Decision and does not use universal last-write-wins, provider-always-wins or user-always-wins.

Source identity, Provenance, Authority and truth remain distinct. A newer source does not become current Actual by recency alone. Where reconciliation yields a new material Actual state, Version preserves the relevant predecessor/state binding and Provenance preserves the materially relevant basis/lineage.

Earlier assertions remain historical facts even after current Actual changes. Conflict/source/basis Visibility remains independently governed.

Downstream classification:

```text
Actual ↔ detailed Reconciliation        RESOLVED
Actual ↔ Source Precedence              RESOLVED — bounded policy only
Reconciliation ↔ Actual                 RESOLVED — process vs owned current state
```

Per-domain precedence rules, Principal/enforcement, native identity deduplication, retention and physical representation remain separately owned.

No original Actual hardening failed. **Actual remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/reconciliation.md`;
- `reconciliation-source-precedence-v0-validation.md`.