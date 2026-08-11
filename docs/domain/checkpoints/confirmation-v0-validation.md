# Confirmation v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted current baseline  
**Date:** 2026-08-11  
**Concept:** Confirmation v0  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Scope

This checkpoint validates whether LifeOS requires a distinct `Confirmation` concept and whether that concept can remain narrower than generic acknowledgement, acceptance, authority, verification, Provenance, or truth.

Primary adjacent concepts:

- Actual;
- Outcome;
- Observation;
- future Evidence;
- future Provenance;
- future Authority/Relationship/Participation;
- future Version/Decision semantics.

Primary risks:

1. one ambiguous `confirmed=true` flag;
2. treating Confirmation as universal truth;
3. collapsing acknowledgement/acceptance/authority into one concept;
4. losing target-version specificity after correction;
5. fabricating human Confirmation from imports, automation or AI inference.

---

# 2. Evidence reviewed

## Internal evidence

Reviewed:

- accepted Actual v0;
- accepted Outcome v0;
- accepted Observation v0;
- `docs/product/v1-execution-status.md`;
- `docs/product/v1-confirmation-and-reminders.md`;
- Multi-Actor Readiness v1;
- multi-actor discovery simulation and Deep Research;
- Validation Methodology v3;
- current Language Map.

Inherited invariants:

```text
passage of time != completion
Actual != Outcome
Observation != universal truth
source != authority
acceptance != Actual participation
AI inference != canonical truth
```

## External benchmark evidence

| Source/pattern | Finding | Classification |
|---|---|---|
| RFC 5545 participant status | acceptance/tentative/decline are participation states, not proof of Actual occurrence | ADAPT |
| ActivityStreams Accept/Reject | acceptance is an action toward an object, not the object truth itself | ADAPT |
| HL7 FHIR Provenance | source/agent/process history remains separate from target content | ADAPT |
| FHIR VerificationResult | verification can be modeled separately from the verified target | ADAPT, not copied |
| W3C PROV | provenance does not itself establish content truth | ADAPT |

External standards remain evidence rather than target schemas.

---

# 3. Accepted candidate definition

> **A Confirmation is a persistent contextual attestation that a specific confirmer affirms a specific version of an assertion, realization, result, observation, or other confirmable target as sufficiently accepted for a defined purpose at that time. Confirmation records the affirmation; it does not by itself prove universal truth, grant authority, replace Provenance, or change the semantic meaning of the target.**

Domain question:

> **Who or what explicitly affirms this specific version of this target, for which purpose and context?**

Nearest boundaries:

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
```

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| CORE-01 Workflow inversion | yes | user review, imported result, corrected record, shared hand-off | PASS | explicit affirmation is a real workflow need independent of source/result semantics |
| CORE-02 Deep chronology | yes | assertion → confirmation → correction → re-confirm/retract → later audit | PASS WITH HARDENING | Confirmation must bind to material target version and preserve history |
| CORE-03 Reductio | yes | REMOVE / MERGE / UNIVERSALIZE / INVERT / EXTREME | PASS WITH HARDENING | universal boolean and generic attestation root rejected |
| CORE-04 Redundancy | yes | vs Actual/Outcome/Observation/Provenance/Acceptance/Authority | PASS | each neighbor answers a different domain question |
| CORE-05 Traceability | yes | imported/observed fact → Confirmation → later evaluation | PASS | affirmation can be traced without rewriting origin or reality |
| CORE-06 Orphan/independence | yes | authoritative record usable without personal Confirmation | PASS | Confirmation is optional/contextual |
| CORE-07 External benchmark | yes | RFC 5545, ActivityStreams, FHIR, PROV | PASS | external patterns support semantic separation |
| CORE-08 Anti-pattern review | yes | `confirmed=true`, status explosion, provenance collapse | PASS | reject boolean/global status semantics |
| CORE-09 Correction/reconciliation/epistemic integrity | yes | confirmed v1 later corrected to v2 | PASS WITH HARDENING | previous Confirmation cannot silently confirm changed target |
| CORE-10 Scale/performance/history | yes | many low-risk observations/imports | PASS | Confirmation is not required for every fact |
| CORE-11 Simple vs power user | yes | one-tap personal confirm vs auditable high-consequence review | PASS | progressive disclosure preserves both modes |
| CORE-12 Product value/complexity cost | yes | review queue / unresolved high-value results | PASS | explicit Confirmation reduces ambiguity where consequence warrants it |
| CORE-13 Implementation pressure | yes | cross-target confirmation temptation | PASS WITH HARDENING | do not pre-commit to generic polymorphic table; preserve semantic target-version requirement |

## Core hardenings

1. Confirmation is contextual/optional, not universal.
2. No Confirmation is not negative truth.
3. Confirmation binds to a specific material target version.
4. `awaiting confirmation` is derived workflow state.
5. imported/inferred/automatic/corrected are not Confirmation types.
6. automation/AI must not fabricate human Confirmation.
7. purpose/context may bound where Confirmation is sufficient.

---

# 5. Adversarial Reductio

## REMOVE

Without Confirmation, explicit affirmation must be hidden inside Provenance, object state or audit text, losing queryable confirmer/version/purpose semantics.

**Result:** REMOVE fails.

## MERGE WITH PROVENANCE

Source history can remain unchanged while Confirmation changes independently.

**Result:** MERGE fails.

## MERGE WITH ACTUAL

Affirmation does not cause reality.

**Result:** MERGE fails.

## MERGE WITH OUTCOME

Result/disposition and epistemic affirmation can change independently.

**Result:** MERGE fails.

## MERGE WITH OBSERVATION

An Observation exists independently of whether someone affirms it.

**Result:** MERGE fails.

## MERGE WITH ACCEPTANCE / ACKNOWLEDGEMENT

Receipt/common-ground and willingness/commitment are not factual affirmation.

**Result:** MERGE fails.

## MERGE WITH AUTHORITY

A confirmer may lack canonical authority and an authoritative source may not need personal Confirmation.

**Result:** MERGE fails.

## MAKE UNIVERSAL

Requiring Confirmation for every imported/observed/ordinary fact creates product bureaucracy and semantic noise.

**Result:** UNIVERSALIZE fails.

## UNIVERSAL ATTESTATION ROOT

A generic Attestation root over acknowledgement, acceptance, approval, verification and Confirmation hides materially different effects/lifecycles.

**Result:** premature abstraction rejected.

---

# 6. Multi-Actor Compatibility Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| MA-01 Identity/account independence | yes | confirmer without LifeOS account | PASS | confirmer identity cannot require `users.id` equivalence |
| MA-02 Shared fact/actor overlay | yes | one shared target with actor-specific confirmations | PASS | one actor's Confirmation does not duplicate shared target |
| MA-03 Responsibility/assignment | limited | hand-off workflow | PASS | acceptance/responsibility transfer remain separate |
| MA-04 Stewardship/mental load | limited | repeated review requests | PASS | product should not force low-value confirmations on every participant |
| MA-05 Common ground/state separation | yes | sent/seen/acknowledged/accepted/confirmed/Actual | PASS WITH HARDENING | stages remain separable where consequence warrants |
| MA-06 Authority/canonical change | yes | actor confirms but lacks shared authority | PASS WITH HARDENING | Confirmation != canonical authority |
| MA-07 Selective disclosure | yes | private confirmer/context | PASS | shared consequence need not expose private source details |
| MA-08 Inference privacy | yes | AI uses private confirmation status | PASS | AI access does not create disclosure permission |
| MA-09 Partial adoption/external participant | yes | external actor confirms via bounded interaction | PASS | no mandatory account for represented confirmer |
| MA-10 Assisted participation/provenance | yes | helper records/affirms for another subject | PASS WITH HARDENING | subject, confirmer and recorder remain distinct |
| MA-11 Relationship lifecycle/revocation | yes | access ends after historical confirmation | PASS | historical attribution remains distinct from current access |
| MA-12 Conflict/adversarial relationship | yes | actors provide conflicting confirmations | PASS WITH HARDENING | conflicting Confirmations remain representable |
| MA-13 Unequal power | yes | manager/caregiver/guardian contexts | PASS | Confirmation does not automatically expand authority |
| MA-14 Multi-resource/capacity | no | not a capacity concept | N/A | no resource-capacity semantics owned by Confirmation |
| MA-15 Coordination burden | yes | confirmation-heavy group workflow | PASS WITH HARDENING | require Confirmation only where product value justifies burden |
| MA-16 Formality/progressive disclosure | yes | casual vs high-consequence review | PASS | kernel supports formality without forcing UI bureaucracy |
| MA-17 AI authority/multi-party context | yes | AI infers likely truth | PASS WITH HARDENING | inference cannot silently become Confirmation |
| MA-18 Specialist-system boundary | yes | externally authoritative records | PASS | LifeOS may accept external authority without fabricating personal Confirmation |
| MA-19 Multi-actor primitive redundancy | yes | one target + N confirmations | PASS | no SharedConfirmation/ActorConfirmation subtype needed |
| MA-20 Actor-scoped reality attribution | yes | actor confirms own participation vs group Actual | PASS WITH HARDENING | confirmer scope must not broaden target attribution |

---

# 7. Cross-Concept Consistency Gate

| Test ID | Applicable | Result | Notes |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS | does not redefine Actual/Outcome/Observation identity |
| XCON-02 Ownership/authority compatibility | yes | PASS WITH HARDENING | Confirmation explicitly separated from Authority |
| XCON-03 Planned/current/actual/history compatibility | yes | PASS | confirmation history survives correction/supersession |
| XCON-04 Relationship compatibility | yes | PASS | confirmer/target/purpose relationships remain compatible with future typed model |
| XCON-05 Multi-actor readiness compatibility | yes | PASS | actor-scoped Confirmation + shared fact model preserved |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE | Confirmation promoted from DEFERRED to CANONICAL after acceptance |

---

# 8. Hardest scenario log

| Scenario | Stress | Result | Model change |
|---|---|---|---|
| confirmed target later corrected | version inheritance | PASS after hardening | Confirmation binds to material target version |
| imported authoritative result | personal confirmation optionality | PASS | canonical use can exist without human Confirmation |
| group actor confirms own participation | scope | PASS | actor Confirmation does not establish others' reality |
| conflicting actor confirmations | disagreement | PASS after hardening | no flattening/overwrite |
| automatic rule establishes result | false human attribution | PASS | automation provenance != human Confirmation |
| AI predicts likely completion | epistemic integrity | PASS | inference != Confirmation |
| acknowledgement of schedule change | common-ground boundary | PASS | acknowledgement != Confirmation |
| recipient accepts responsibility | commitment boundary | PASS | acceptance != Confirmation |
| confirmer loses access later | lifecycle | PASS | historical attribution survives access revocation |

---

# 9. Reopening / dependency register

| Finding | Severity | Current treatment | Reopening trigger |
|---|---|---|---|
| Confirmation vs Provenance persistence boundary | DEFERRED DEPENDENCY | semantic distinction fixed | Provenance v0 + logical model |
| material version equivalence | DEFERRED DEPENDENCY | bind to specific material version | Version model |
| Acknowledgement/Common Ground | DEFERRED DEPENDENCY | kept separate | Relationship/communication review |
| Acceptance/Agreement/Approval | DEFERRED DEPENDENCY | kept separate | Participation/Authority/Decision review |
| machine attestation | DEFERRED DEPENDENCY | no fabricated human confirmation | AI/Authority/Provenance review |
| generic target storage | STRUCTURAL WATCH | no physical decision | logical/persistence pressure gate |
| generic Attestation root | STRUCTURAL WATCH | rejected for now | reopen only with evidence of shared lifecycle/behavior |

---

# 10. Concept verdict

**PASS WITH HARDENING**

Confirmation survives removal, merge, universalization, chronology, version correction, multi-actor conflict, authority, AI, privacy and product-burden tests.

No structural reopening of Actual, Outcome, Observation, Time or Intention/Execution concepts is required.

Mandatory future re-tests:

- Confirmation vs Provenance;
- Confirmation vs Evidence usage;
- Confirmation + Authority/Version interaction;
- Reality/Evidence cluster checkpoint;
- whole-domain multi-actor gate;
- persistence/API pressure gate.

---

# 11. Regression corpus additions

| Scenario | New boundary | Reuse trigger |
|---|---|---|
| confirmation of v1 followed by corrected v2 | confirmation != floating boolean | Version/Provenance models |
| authoritative import without personal confirmation | confirmation optionality | Provenance/Authority/Evidence |
| actor confirms own state only | actor-scoped affirmation | Participation/Actual/Outcome |
| conflicting confirmations | conflict preservation | Provenance/Authority/Decision |
| automation produces result | automation != human confirmation | AI/Policy/Provenance |
| acknowledgement/acceptance without factual confirmation | common-ground/commitment boundaries | collaboration modeling |

---

# 12. Documentation propagation

Acceptance requires:

- concept specification;
- this validation checkpoint;
- Language Map promotion;
- Domain Atlas README update;
- workstream handoff update;
- reopening triggers retained for Evidence/Provenance/Authority/Version work.