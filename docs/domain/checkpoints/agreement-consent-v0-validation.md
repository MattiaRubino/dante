# Agreement / Consent v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated; pending post-write scope QA  
**Validated:** 2026-08-13  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `0d4bb2458082f9a6d4e752d83960cea9033a05ad`

## 1. Scope

- **Candidate family reviewed:** Agreement / Consent.
- **Neither noun was pre-accepted.**
- **Primary problem:** preserve multi-party mutual assent and actor-scoped permission without collapsing common ground, Decision, Authority, Visibility, technical permission, legal validity, resulting state or Actual.
- **Nearest accepted boundaries inspected:** Acknowledgement, Decision, Authority, Visibility, Confirmation, Participation, Responsibility, Actor, Person, Account/Principal boundary, Provenance, Actual.
- **Deliberately not designed here:** Principal/authentication, detailed delegation/on-behalf-of, exact Version/material-equivalence mechanics, collective/quorum identity, legal validity/capacity, formal Contract/signature, final policy engine, retention periods, final SQL/API.

Product question:

> **How can LifeOS preserve mutual assent and bounded consent/permission without turning ordinary coordination into a contract engine or confusing assent with governance, exposure, technical authorization or real-world execution?**

---

# 2. Product / LifeOS fit

LifeOS is a personal-first adaptive operating system. It needs enough semantic precision to coordinate people safely while avoiding enterprise/legal workflow creep.

Consequential collaboration may require this chain to remain representable:

```text
proposed / requested
!= delivered/read
!= Acknowledgement
!= one Actor's family-specific response
!= Agreement
!= Consent
!= Decision / Approval
!= Authority
!= resulting effective domain state
!= Actual
```

The product must not expose all of these as mandatory UI stages for casual life.

**Product conclusion:** Agreement and Consent have independent semantic value where consequence warrants them. A generic Assent/Acceptance supertype or universal Contract/Permission engine would add more semantic and product cost than value.

---

# 3. Evidence reviewed

## EV-01 — Internal evidence

Current accepted Domain Atlas concepts already expose the missing boundary:

- `Acknowledgement` explicitly excludes Agreement and Consent;
- generic cross-domain Acceptance is already rejected, leaving positive response semantics inside their owning families;
- `Decision` explicitly excludes Agreement and Consent and separates shared resolution from individual stances;
- `Authority` separates governance power from willingness/consent and leaves Consent as a downstream privacy/common-ground dependency;
- `Visibility` explicitly separates exposure from Consent and arbitrary downstream Use/purpose;
- `Participation` proves that one actor's `accepted` response is contextual and does not create universal assent;
- multi-actor discovery/research requires proposal, acknowledgement, agreement, authority confirmation, selective sharing, withdrawal, power imbalance and Actual outcome to remain distinct;
- healthcare/care/guardian/photo/client examples require bounded permission without collapsing LifeOS into specialist record/legal systems.

**EV-01 result:** strong internal pressure for two distinct semantic questions: mutual shared terms and actor-scoped bounded permission.

## EV-02 — Real-world workflow inversion

### Shared trip / household terms

Two people may mutually agree on cost-sharing or responsibility terms while an external booking/manager/other Authority is still required before downstream state changes.

### Shift swap

Two workers can mutually agree to a proposed swap while manager Approval remains a separate Decision/Authority step and the actual shift transfer occurs later.

### Bounded sharing

A person may permit a free/busy projection for one coordination purpose without exposing raw calendar facts or authorizing unrelated downstream use.

### Photography / service relationship

Client service terms can be mutually agreed while portrait/image-use Consent remains a separate permission question.

### Care / guardian

A caregiver/helper may need bounded permission or represented action while the cared-for Person, actual Actor and Authority basis remain distinct.

### Withdrawal

Consent may be valid/current at T0, used for bounded exposure at T1 and withdrawn for future use at T2 without rewriting the historical fact that the earlier permission and exposure existed.

**EV-02 result:** Agreement and Consent each recur independently and cannot be reduced to one generic response state.

## EV-03 — Targeted external benchmark

External evidence pressures behavior/lifecycle/failure modes only; it does not dictate LifeOS ontology.

| Benchmark | Finding | Classification | LifeOS interpretation |
|---|---|---|---|
| HL7 FHIR Consent | permission can be scoped by actor/action/purpose/time/data context | ADAPT | reinforces bounded target/action/purpose/lifecycle semantics; do not copy healthcare ontology wholesale |
| European Commission / EDPB consent guidance | in GDPR contexts consent validity depends on specific/informed/affirmative/free choice and withdrawal; power imbalance matters | ADAPT — boundary evidence only | reinforces explicitness, purpose scope, withdrawal and unequal-power caution; does not make LifeOS a legal-validity engine |
| HL7 FHIR Contract | formal/legal agreement has rich terms/signers/status/legally enforceable lifecycle | ANTI-PATTERN if copied into kernel | demonstrates specialist boundary and why generic LifeOS Agreement must stay narrower |
| W3C ActivityStreams Accept | generic Accept actions can target arbitrary objects | NOT APPLICABLE as primitive proof | technical genericity does not establish stable shared LifeOS identity/lifecycle/effect |

## EV-04 — Candidate minimality

Hypotheses tested:

```text
H0 no Agreement/Consent semantics
H1 one generic Assent/Acceptance supertype
H2 Agreement survives independently
H3 Consent survives independently
H4 Agreement = Consent
H5 formal Contract/Terms primitive in kernel
```

Result:

```text
H0 FAIL
H1 FAIL
H2 SURVIVES
H3 SURVIVES
H4 FAIL
H5 FAIL
```

Smallest surviving result:

```text
Agreement
= contextual multi-party mutual assent to the same materially specific terms/version

Consent
= contextual actor-scoped permission for bounded action/use/exposure concerning a defined target/scope/purpose/context
```

Both are relation/capability semantics, not universal native roots.

---

# 4. Candidate definitions / identity / independence

## Agreement

Canonical definition:

> **Agreement is the contextual multi-party mutual-assent relation/capability through which a defined set of parties have explicitly assented to the same materially specific terms/version for a bounded context. Agreement records that shared assent and commitment to those terms; it does not by itself prove legal enforceability, create Authority, guarantee compliance, replace Decision, or replace the Responsibilities, Schedules, Visibility or other domain states its terms may establish or influence.**

Domain question:

> **Which parties mutually assented to which materially specific terms, in which bounded context?**

Identity/classification:

```text
specific contextual multi-party mutual-assent relation/capability
not native entity/root
not generic Acceptance
not Decision
not Authority
not Responsibility
not Consent
not legal Contract
not proof of compliance/Actual
```

Independence examples:

```text
workers mutually agree to swap
manager Approval still pending
→ Agreement exists without effective state change
```

```text
manager decides a disputed shift outcome
worker disagrees
→ Decision exists without Agreement
```

## Consent

Canonical definition:

> **Consent is the contextual actor-scoped permission relation/declaration through which an eligible consent-giver explicitly permits a bounded action, exposure, use, processing or interaction concerning a defined target/subject for a defined scope, purpose and context where Consent is an applicable basis. Consent records that permission state; it does not by itself prove legal validity, create Authority or Visibility, execute the permitted action, or prove compliance with its scope.**

Domain question:

> **Who explicitly permitted what bounded action/use/exposure concerning what target, for which scope/purpose/context?**

Identity/classification:

```text
specific contextual actor-scoped permission relation/capability
not universal Permission
not technical authorization
not Visibility
not Authority
not Agreement
not Decision
not legal-validity proof
not proof action occurred
```

Independence examples:

```text
Consent granted
no disclosure occurs
→ Consent exists without Visibility/disclosure event
```

```text
Visibility exists under another legitimate basis
→ does not prove Consent existed
```

---

# 5. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence / scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| CORE-01 Real-World Workflow Inversion | yes | trip terms, shift swap, care, bounded sharing, photo use | PASS | mutual terms and scoped permission recur independently |
| CORE-02 Deep Chronological Simulation | yes | terms v1→v2; Consent grant→use→withdrawal | PASS WITH HARDENING | bind Agreement/Consent to material terms/scope/version and preserve history |
| CORE-03 Adversarial Reductio | yes | remove/merge/Assent/Contract/Permission | PASS | Agreement and Consent survive; generic Assent and specialist roots fail |
| CORE-04 Semantic Redundancy / Merge-Split | yes | Agreement vs Decision; Consent vs Visibility/Authority; Agreement vs Consent | PASS WITH HARDENING | both DISTINCT and non-collapsible |
| CORE-05 Multidirectional Traceability | yes | proposal→assent/Consent→Decision/policy→effect→Actual | PASS | chronology remains reconstructible |
| CORE-06 Orphan / Independence | yes | Agreement before effect; Consent before use | PASS WITH HARDENING | both can exist independently but need no native identity root |
| CORE-07 External Cross-Domain Benchmark | yes | FHIR Consent/Contract, EDPB, ActivityStreams | PASS | external evidence reinforces scope/lifecycle and specialist boundaries |
| CORE-08 External Anti-Pattern Review | yes | `agreed=true`, `consented=true`, generic Assent/Contract/Permission engines | PASS | universal workflow/root abstractions rejected |
| CORE-09 Correction / Reconciliation / Epistemic Integrity | yes | changed terms/scope, disputed assent, withdrawal | PASS WITH HARDENING | material changes never silently inherit prior assent/Consent |
| CORE-10 Scale / Performance / History | yes | long-lived relationships, many casual interactions | PASS WITH HARDENING | materialize only where consequence/history justify |
| CORE-11 Simple User / Power User | yes | casual agree/share vs formal care/client workflows | PASS | progressive disclosure preserves kernel precision without enterprise UI |
| CORE-12 Product Value / Complexity Cost | yes | coordination benefit vs ceremony burden | PASS WITH HARDENING | no mandatory Agreement/Consent workflow for ordinary low-risk interactions |
| CORE-13 Implementation Pressure Without Premature Schema | yes | query parties/terms/consent scope/history | PASS | semantics fixed without universal tables/polymorphic target API |

**CORE Gate:** PASS WITH HARDENING.

---

# 6. Deep chronology stress

```text
T0 Anna + Luca plan Trip A
T1 terms v1: cost split 50/50 + bounded free/busy use for trip coordination
T2 Anna Acknowledges v1
T3 Anna grants Consent C-A-v1 for bounded free/busy use/purpose Trip A
T4 Luca grants corresponding bounded Consent C-L-v1
T5 Anna + Luca both assent to materially same cost terms v1
T6 Agreement A1 exists for those terms
T7 organizer Decision selects apartment X
T8 applicable Authority/policy makes booking/effective shared state change
T9 proposal v2 adds unrelated full-history AI training purpose
T10 existing Consent v1 does not cover v2 purpose
T11 Anna refuses expanded permission
T12 Agreement A1 on trip/cost terms remains historically/currently independent from expanded Consent
T13 Anna later withdraws original future free/busy Consent
T14 future LifeOS-mediated use/exposure changes; prior disclosure/history remains
T15 trip Actual later differs from plan
```

Required reconstruction:

- which terms/version each party assented to;
- whether a shared Agreement existed and when;
- which Consent scope/purpose each actor granted;
- which Consent was refused/withdrawn;
- which Decision occurred;
- which Authority/policy made downstream state effective;
- what was actually disclosed/used/performed;
- what Actual later occurred.

Canonical sequence:

```text
proposed
!= Acknowledged
!= individual family response
!= Agreement
!= Consent
!= Decision/Approval
!= Authority
!= effective state
!= Actual
```

---

# 7. Destructive reductio

```text
REMOVE Agreement
→ FAIL: cannot represent that applicable parties mutually assented to the same terms/version

Agreement = Decision
→ FAIL: authoritative resolution can exist without mutual assent; mutual assent can exist before any effect/Decision

Agreement = Responsibility
→ FAIL: terms may create/influence accountability but are not the resulting Responsibility state

Agreement = Consent
→ FAIL: mutual terms != unilateral actor-scoped permission

Agreement = legal Contract
→ FAIL: imports specialist legal lifecycle/enforceability into ordinary LifeOS

REMOVE Consent
→ FAIL: Visibility/Authority cannot represent actor-owned bounded permission/purpose/withdrawal without semantic distortion

Consent = Visibility
→ FAIL: permission can exist before exposure; exposure may have another applicable basis

Consent = Authority
→ FAIL: permission does not manufacture general governance power

Consent = technical Permission
→ FAIL: domain consent != request enforcement

Consent = Decision
→ FAIL: permission != bounded resolution

Generic Assent/Acceptance root
→ FAIL: Ack, response, Agreement, Consent, Confirmation and Decision differ materially in target/effect/lifecycle/Authority implication
```

---

# 8. Mandatory hardenings — incorporated

## Agreement

1. Agreement requires materially same terms/version among the applicable required party set.
2. One party's assent != Agreement for everyone.
3. Silence/no response != Agreement.
4. Agreement(v1) does not silently carry to materially changed v2.
5. Agreement != Acknowledgement.
6. Agreement != generic/family-specific response automatically.
7. Agreement != Decision.
8. Agreement != Authority.
9. Agreement != Responsibility/resulting state.
10. Agreement != Consent.
11. Agreement != legal Contract/enforceability proof.
12. Agreement != compliance/Actual.
13. Agreement does not grant blanket Visibility/re-disclosure rights.
14. On-behalf-of assent preserves actual actor/represented party/basis where material.
15. AI inference does not fabricate human Agreement.
16. Agreement persistence/workflow is consequence-sensitive.

## Consent

1. Consent is explicit actor-scoped permission; silence/behavior/inference do not establish it by themselves.
2. Consent is bounded by action/use/exposure and target.
3. Purpose/context is material where it changes what was permitted.
4. Consent for purpose A does not silently cover purpose B.
5. Material target/scope/version changes do not inherit prior Consent automatically.
6. Consent != Visibility.
7. Consent != Authority.
8. Consent != technical authorization/Permission.
9. Consent != Agreement.
10. Consent != Decision.
11. Consent != Acknowledgement/Confirmation/family response.
12. Consent does not prove the permitted action/use occurred.
13. Withdrawal/revocation changes future applicability without rewriting history.
14. No current Consent != explicit refusal by default.
15. Membership/relationship/Participation does not imply Consent.
16. On-behalf-of Consent preserves actor/represented party/basis.
17. AI may not infer/fabricate/enlarge human Consent.
18. LifeOS Consent does not prove legal validity/capacity.
19. Consent history has independent Visibility/privacy requirements.
20. Consent/purpose enforcement remains downstream policy/security work.

---

# 9. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Result | Finding / hardening |
|---|---:|---|---|
| MA-01 Identity / Account Independence | yes | PASS | parties/consent-givers need not have LifeOS Accounts |
| MA-02 Shared Canonical Fact / Actor Overlay | yes | PASS WITH HARDENING | shared Agreement can coexist with actor-scoped assent/Consent states |
| MA-03 Responsibility / Assignment / Claim | yes | PASS WITH HARDENING | Agreement terms may influence Responsibility but do not become Responsibility |
| MA-04 Coordination Stewardship / Mental Load | yes | PASS | assent/Consent do not silently transfer stewardship/mental load |
| MA-05 Common Ground / State Separation | yes | PASS WITH HARDENING | Ack, response, Agreement, Consent, Decision/effect remain separate |
| MA-06 Authority / Canonical Change | yes | PASS WITH HARDENING | Agreement/Consent may be basis/precondition; neither manufactures Authority |
| MA-07 Selective Disclosure | yes | PASS WITH HARDENING | Consent directly pressures scope/purpose while Visibility remains resulting exposure capability |
| MA-08 Inference Privacy | yes | PASS WITH HARDENING | derived/AI outputs must not exceed consent/use boundary or expose private causes |
| MA-09 Partial Adoption / External Participant | yes | PASS | external parties can assent/consent without Account creation |
| MA-10 Assisted Participation / Assertion Provenance | yes | PASS WITH HARDENING | helper/representative cannot silently impersonate consent-giver/party |
| MA-11 Lifecycle / Revocation | yes | PASS WITH HARDENING | amendment/termination/withdrawal preserve history |
| MA-12 Conflict / Adversarial Relationship | yes | PASS WITH HARDENING | disputed assent/Consent may remain unresolved pending reconciliation |
| MA-13 Unequal Power / Guardian / Caregiver | yes | PASS WITH HARDENING | forced acknowledgement/click must not be relabeled valid voluntary Consent/Agreement |
| MA-14 Multi-Resource / Capacity | limited | PASS | terms/Consent may govern Resource use but do not establish Capacity/availability truth |
| MA-15 Coordination-Burden Distribution | yes | PASS WITH HARDENING | no universal ceremony for casual interactions |
| MA-16 Formality / Progressive Disclosure | yes | PASS | simple agree/share actions to richer version/history detail by consequence |
| MA-17 AI Authority / Multi-Party Context | yes | PASS WITH HARDENING | AI suggestion != assent/Consent; access != permission to disclose |
| MA-18 Specialist-System Boundary | yes | PASS WITH HARDENING | regulated consent/contracts remain externally authoritative/specialist where needed |
| MA-19 Multi-Actor Primitive Redundancy | yes | PASS | Agreement and Consent survive separately; generic Assent root fails |
| MA-20 Actor-Scoped Reality Attribution | yes | PASS WITH HARDENING | shared Agreement does not rewrite each actor's individual state or Actual |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 10. Cross-Concept Consistency Gate

| Test ID | Result | Closure |
|---|---|---|
| XCON-01 Identity | PASS | neither concept creates Person/Actor/Account identity |
| XCON-02 Ownership / Authority | PASS WITH HARDENING | assent/permission != governance power; technical enforcement separate |
| XCON-03 Planned / current / Actual / history | PASS WITH HARDENING | terms/Consent history remains separate from resulting state/Actual |
| XCON-04 Relationships | PASS | specific direct/derived or qualified relation-family modeling fits Relationship v0 |
| XCON-05 Multi-actor | PASS WITH HARDENING | Agreement is shared mutual state; Consent remains actor-scoped |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Agreement/Consent canonical meanings and product/UI mappings must be recorded |

**Structural reopening of prior accepted concepts:** 0.

---

# 11. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Agreement ↔ Acknowledgement | taking notice != mutual assent |
| Consent ↔ Acknowledgement | taking notice != permission |
| Agreement ↔ family-specific positive response | one actor response != shared Agreement |
| Agreement ↔ Decision | mutual assent != bounded resolution |
| Consent ↔ Decision | permission != resolution |
| Agreement ↔ Authority | mutual assent != governance power |
| Consent ↔ Authority | permission != governance power |
| Consent ↔ Visibility | permission/basis != resulting exposure capability |
| Consent ↔ arbitrary downstream Use | scope/purpose semantic boundary fixed; enforcement deferred |
| Agreement ↔ Responsibility | terms may influence/create accountability; Agreement is not Responsibility state |
| Agreement ↔ Consent | shared mutual terms != actor-scoped permission |
| generic Assent / Acceptance root | REJECTED |
| universal Contract primitive | REJECTED |

## SAFE DEFERRED — Principal / delegation / representation

**Unresolved:** who may assent/consent on behalf of whom and under which Principal/delegation/Authority basis.  
**Why safe:** actual Actor, represented party and applicable basis are now required to remain distinct.  
**Owner:** Principal/delegation/security review.  
**Reopening trigger:** on-behalf-of Agreement/Consent cannot preserve attribution without collapsing Person/Actor/Account/Principal/Authority.  
**Tests to rerun:** CORE-02, CORE-06, CORE-09, CORE-13, MA-01, MA-06, MA-10, MA-11, MA-13, MA-17, XCON-01, XCON-02.

## SAFE DEFERRED — Version / material terms/scope

**Unresolved:** exact material-equivalence/version representation.  
**Why safe:** material terms/scope/version applicability is already mandatory semantically.  
**Owner:** Version + logical model.  
**Reopening trigger:** system cannot determine whether prior assent/Consent remains applicable after change.  
**Tests to rerun:** CORE-02, CORE-09, CORE-10, CORE-13, MA-11, MA-12, XCON-03.

## SAFE DEFERRED — Consent validity / capacity / legal basis

**Unresolved:** age, capacity, coercion, jurisdiction, legal sufficiency and specialist validity.  
**Why safe:** LifeOS explicitly records scoped permission semantics without claiming legal validity.  
**Owner:** specialist/legal/product policy.  
**Reopening trigger:** a product flow requires LifeOS itself to establish legally/clinically authoritative consent validity.  
**Tests to rerun:** CORE-03, CORE-04, CORE-09, CORE-12, MA-06, MA-10, MA-13, MA-18, XCON-02.

## SAFE DEFERRED — Purpose/use enforcement

**Unresolved:** technical policy representation and enforcement.  
**Why safe:** Consent scope/purpose and Visibility/use boundaries are semantically fixed independently.  
**Owner:** privacy/policy/security/logical model.  
**Reopening trigger:** enforcement requires Consent to collapse into Visibility, Authority or technical Permission.  
**Tests to rerun:** CORE-04, CORE-10, CORE-13, MA-06, MA-07, MA-08, MA-17, XCON-02, XCON-04.

## SAFE DEFERRED — Collective/group party identity

**Unresolved:** collective Actor, quorum, represented group and required-party membership.  
**Why safe:** Agreement requires an applicable party set without inventing a universal Group identity.  
**Owner:** collective/group semantics.  
**Reopening trigger:** ordinary workflows require collective identity/quorum that cannot be represented using native parties/roles.  
**Tests to rerun:** CORE-04, CORE-06, CORE-12, MA-01, MA-02, MA-05, MA-13, MA-19, MA-20, XCON-01, XCON-04, XCON-05.

## SAFE DEFERRED — Formal signature / Contract

**Unresolved:** signatures, witnesses, legal terms, enforceability and formal contract lifecycle.  
**Why safe:** generic LifeOS Agreement explicitly claims none of those specialist guarantees.  
**Owner:** specialist/document/legal integration.  
**Reopening trigger:** ordinary LifeOS Agreement must own formal legal validity/lifecycle to remain correct.  
**Tests to rerun:** CORE-03, CORE-04, CORE-08, CORE-12, CORE-13, MA-13, MA-18, MA-19, XCON-04.

## SAFE DEFERRED — Proposal / request reusable identity

**Unresolved:** whether proposed terms/consent request require one cross-family proposal primitive.  
**Why safe:** Agreement/Consent can target materially specific terms/proposal without universalizing Proposal.  
**Owner:** proposal/reasoning review.  
**Reopening trigger:** history cannot bind assent/Consent to the exact proposal/version.  
**Tests to rerun:** CORE-02, CORE-03, CORE-04, CORE-06, CORE-13, MA-05, MA-19, XCON-03, XCON-04.

## SAFE DEFERRED — Retention / deletion

**Unresolved:** duration/anonymization/deletion of Agreement/Consent history and source payloads.  
**Why safe:** historical attribution does not imply indefinite payload retention.  
**Owner:** privacy/retention.  
**Reopening trigger:** privacy/deletion rules conflict with required historical reconstruction.  
**Tests to rerun:** CORE-02, CORE-09, MA-07, MA-11, MA-13, XCON-03.

```text
REOPEN                         0
unclassified material items    0
```

---

# 12. Hardest adversarial scenario log

| Scenario | Stress | Required result |
|---|---|---|
| message delivered; nobody responds | silence | no Agreement; no Consent |
| one of four parties accepts terms | partial assent | no fabricated four-party Agreement |
| A assents v1, B assents materially different v2 | version mismatch | no Agreement until material terms align |
| manager makes legitimate Decision over worker objection | Decision vs Agreement | Decision may exist; Agreement does not |
| workers mutually agree to swap; manager approval required | Agreement vs effect | Agreement may exist; effective transfer still pending |
| household/family membership | relationship inference | does not establish permanent Consent |
| employee forced to click `I agree` | unequal power | LifeOS must not automatically claim voluntary/legal Consent |
| free/busy Consent for trip planning | purpose scope | does not cover unrelated AI training/analytics |
| Consent withdrawn after prior disclosure | history | future permission changes; historical disclosure remains |
| caregiver/helper acts for older adult | representation | actual Actor/represented party/basis preserved |
| service Agreement + portrait use | Agreement vs Consent | one does not manufacture the other |
| AI predicts user would probably agree | AI inference | no human Agreement/Consent |
| imported legal Contract | specialist boundary | may provide Evidence/Provenance; does not redefine kernel Agreement |

---

# 13. Reopening / dependency register

| Finding | Severity | Treatment | Reopening trigger |
|---|---|---|---|
| multi-party mutual terms have independent value | STRUCTURAL | canonical Agreement relation/capability | stronger existing semantic proves complete redundancy |
| actor-scoped bounded permission has independent value | STRUCTURAL | canonical Consent relation/capability | stronger existing semantic preserves purpose/scope/withdrawal without loss |
| generic Assent/Acceptance root | STRUCTURAL | rejected | shared independent identity/lifecycle emerges across Ack/Agreement/Consent/Decision families |
| Agreement = Decision | STRUCTURAL | rejected | only reopen if mutuality becomes inseparable from resolution semantics |
| Agreement = Consent | STRUCTURAL | rejected | only reopen if mutual terms and permission lifecycles converge materially |
| Consent = Visibility/Authority | STRUCTURAL | rejected | only reopen if permission cannot remain a basis/constraint rather than exposure/governance itself |
| material terms/version binding | HARDENING | invariant now; mechanics deferred | applicability cannot be determined after change |
| Consent scope/purpose | HARDENING | invariant now; enforcement deferred | policy cannot enforce without semantic collapse |
| historical withdrawal/amendment | HARDENING | preserve history | retention/privacy model conflicts with reconstruction |
| legal validity/capacity | DEFERRED DEPENDENCY | SAFE DEFERRED | LifeOS must certify regulated validity itself |
| on-behalf-of | DEFERRED DEPENDENCY | SAFE DEFERRED | attribution fails under Principal/delegation model |
| collective/group identity | DEFERRED DEPENDENCY | SAFE DEFERRED | ordinary workflows require collective party/quorum identity |
| formal Contract/signature | SPECIALIST DEPENDENCY | SAFE DEFERRED | generic Agreement becomes insufficient for ordinary product scope |
| Agreement/Consent overload | PRODUCT / UX | consequence-sensitive guardrail | casual coordination becomes ceremony/bureaucracy |

---

# 14. Regression corpus additions

| ID | Scenario | Boundary |
|---|---|---|
| R-AGR-01 | all required parties assent v1 → material terms v2 → old Agreement not inherited | Agreement + Version/history |
| R-AGR-02 | mutual shift-swap Agreement → external manager Approval still required → effective transfer later | Agreement + Decision/Authority/effect |
| R-AGR-03 | partial party assent | no fabricated group Agreement |
| R-CON-01 | Consent free/busy for trip → new AI-training purpose | Consent purpose limitation |
| R-CON-02 | Consent grant → disclosure/use → later withdrawal | lifecycle + historical preservation |
| R-CON-03 | guardian/caregiver/helper acts on behalf of another | actor attribution + Principal/delegation |
| R-AGR-CON-01 | service Agreement + separate image/data-use Consent | Agreement != Consent |
| R-CON-04 | power-imbalanced acknowledgement/accept click | response/Ack != valid Consent automatically |

---

# 15. Concept-family verdict

```text
AGREEMENT / CONSENT FAMILY
PASS WITH HARDENING
```

Accepted candidate result pending post-write QA:

```text
Agreement
✅ specific contextual multi-party mutual-assent relation/capability
✅ materially same terms/version
✅ explicit applicable party set
✅ history-sensitive where material
✅ direct/derived or qualified where justified
❌ native entity/root
❌ generic Acceptance/Assent
❌ Decision/Authority/Responsibility
❌ Consent
❌ legal Contract
❌ compliance/Actual proof

Consent
✅ specific contextual actor-scoped permission relation/capability
✅ bounded target/action/use/exposure
✅ purpose/context-sensitive where material
✅ lifecycle/history-sensitive
✅ may be one policy basis/constraint
❌ universal Permission
❌ technical authorization
❌ Visibility/Authority
❌ Agreement/Decision
❌ legal-validity proof
❌ proof permitted action occurred

Generic Assent / Acceptance supertype
❌ REJECTED

Universal Contract / legal-consent engine
❌ REJECTED
```

All mandatory hardenings are incorporated in `../concepts/agreement.md`, `../concepts/consent.md` and this checkpoint.

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 16. Mandatory future re-tests

Retest at the recorded triggers when these owners mature:

- Principal / delegation / representation;
- Version / material equivalence;
- collective/group/quorum semantics;
- legal/specialist consent validity/capacity;
- formal Contract/signature integration;
- Proposal/request identity;
- privacy/purpose/use policy enforcement;
- retention/deletion;
- whole-domain multi-actor/privacy/AI regression;
- persistence/API pressure gate.

Do not reopen by vocabulary alone.

---

# 17. Cluster integration

Not applicable yet: Cluster 5 remains open and must continue candidate re-scoring after this milestone is fully propagated and post-write QA passes.

---

# 18. Documentation propagation

Approved write scope for this milestone:

### CREATE

- [x] `../concepts/agreement.md`
- [x] `../concepts/consent.md`
- [x] this checkpoint

### UPDATE — current canonical state

- [ ] `../language-map.md`
- [ ] `../README.md`
- [ ] `../../workstreams/domain-model.md`
- [ ] `../multi-actor-readiness-v1.md`

### UPDATE — downstream closures

- [ ] `../concepts/acknowledgement.md`
- [ ] `acknowledgement-v0-validation.md`
- [ ] `../concepts/decision.md`
- [ ] `decision-v0-validation.md`
- [ ] `../concepts/visibility.md`
- [ ] `visibility-v0-validation.md`
- [ ] `../concepts/authority.md`
- [ ] `authority-v0-validation.md`
- [ ] `../concepts/confirmation.md`
- [ ] `confirmation-v0-validation.md`
- [ ] `deferred-dependency-closure-clusters-1-4-v0.md`

Historical discovery/research/product-glossary/Cross-Cluster documents are intentionally not rewritten for terminology uniformity.

Root `README.md`, `docs/PROJECT-STATUS.md`, prototype, SQL/API/auth/backend are outside scope.

---

# 19. Git QA gate

The milestone becomes an accepted Domain Atlas baseline only after full diff QA against:

```text
0d4bb2458082f9a6d4e752d83960cea9033a05ad
```

Required checks:

- exactly the approved 18 paths changed;
- no out-of-scope path changed;
- all documentation-propagation checkboxes above are complete;
- Language Map, Domain README, Multi-Actor Readiness and workstream agree;
- historical checkpoint material remains preserved with explicit downstream closure rather than silent rewrite;
- Agreement != Decision/Authority/Responsibility/Consent/Contract/Actual;
- Consent != Visibility/Authority/technical Permission/Agreement/Decision;
- generic Assent/Acceptance remains rejected;
- Participation `accepted` remains family-specific response semantics;
- purpose/scope, withdrawal/history and unequal-power hardenings remain visible;
- `REOPEN = 0`, unclassified material dependencies = 0;
- no main/prototype/SQL/API/auth/backend/global-status changes.

Do not re-score/select the next candidate until this QA passes.