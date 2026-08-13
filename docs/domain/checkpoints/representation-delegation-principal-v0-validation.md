# Representation / Delegation / Principal v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated; pending post-write scope QA  
**Validated:** 2026-08-13  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `b6c53ffa40ba7c1c1408f583856617a0e000f31b`

## 1. Scope

Candidate family reviewed:

```text
Representation / on-behalf-of
Delegation
Principal
technical impersonation boundary
```

No noun was pre-accepted.

Primary question:

> **When someone or something acts for another party, how can LifeOS preserve who actually acted, for whom, and on what bounded basis without turning the represented party into the Actor, fabricating their will, or collapsing the domain into IAM/security?**

Nearest accepted concepts inspected:

- Person / Actor / Account boundary;
- Authority;
- Responsibility;
- Participation;
- Acknowledgement;
- Confirmation;
- Decision;
- Agreement;
- Consent;
- Visibility;
- Provenance;
- Subject;
- Actual.

Deliberately not designed here:

- final Principal/AuthN/AuthZ schema;
- IAM/token/session architecture;
- legal guardianship/POA/capacity rules;
- formal consent/signature validity;
- exact Version mechanics;
- collective/Organization representation;
- final persistence/API.

---

# 2. Re-score result

The remaining candidate/dependency space was re-scored by:

```text
dependency leverage
existing SAFE DEFERRED pressure
cross-cluster impact
multi-actor / AI pressure
implementation-readiness blocking risk
ontology cost
specialist-system leakage risk
```

Highest candidates:

```text
1 Representation / delegation / Principal
2 Version / material equivalence
3 detailed reconciliation / source precedence
4 Proposal / request reusable identity
5 GoalCriterion / evaluation
```

Representation/delegation won narrowly over Version because the same unresolved attribution boundary already crosses Person/Actor/Account, Participation, Authority, Acknowledgement, Decision, Agreement, Consent, Provenance and AI. Version pressure is very high but current concepts already hold the semantic rule that materially changed versions do not inherit prior states; exact mechanics remain a later logical pressure.

---

# 3. Evidence reviewed

## EV-01 — Internal LifeOS evidence

Internal evidence already requires the following distinction:

```text
Person != Actor != Account != Principal
```

Actor v0 explicitly left on-behalf-of/delegation relationships deferred while requiring actual agency attribution to survive Account/access changes.

Participation v0 explicitly requires:

```text
participant/native referent
response Actor
Account/Principal used
on-behalf-of/delegation basis
```

and states that Participation itself does not solve delegation.

Authority v0 already defines Delegation narrowly as a bounded Authority-establishment/entrustment pattern and rejects a universal Authority/Permission root.

Acknowledgement, Decision and Agreement/Consent all require assisted/on-behalf-of attribution to preserve the actual Actor rather than fabricate another person's state.

Provenance requires material authentication/delegation context where relevant while keeping Principal/security identity distinct from Actor/domain identity.

**EV-01 result:** strong internal semantic pressure; no accepted concept currently owns the represented-party relation itself.

## EV-02 — Real-world workflow inversion

Representative workflows reviewed:

```text
assistant schedules for manager
caregiver records information for another person
parent coordinates an action concerning a child
external helper responds for someone
AI/service acts under bounded policy
manager acts under institutional Authority
technical shared-account / impersonation scenario
```

Critical negative case:

```text
acting concerning X
!= acting for X
```

A parent scheduling a child's appointment may act as organizer/guardian while the child is Subject/beneficiary; this does not automatically mean the parent is expressing the child's personal will.

Likewise a caregiver recording Maria's statement may simply be recorder Actor while Maria is source/Subject, with no Representation relation required.

**EV-02 result:** the actual-Actor / represented-party relation recurs independently and needs a bounded semantic owner.

## EV-03 — External benchmark evidence

External standards are behavioral evidence only.

| Benchmark | Finding | Classification | LifeOS treatment |
|---|---|---|---|
| RFC 8693 OAuth 2.0 Token Exchange | delegation can preserve actor distinct from represented subject; impersonation is a different mechanism | ADAPT | preserve actual Actor + represented party; do not import token schema into domain |
| RFC 8693 impersonation semantics | technical rights context may intentionally make actor indistinguishable from subject | ANTI-PATTERN as domain truth | security mechanism must not erase materially known semantic Actor |
| HL7 FHIR R5 Provenance agent `who` / `onBehalfOf` | separates acting agent from entity represented by that agent | ADAPT | useful attribution pattern; no healthcare ontology import |
| W3C PROV `actedOnBehalfOf` / Delegation | models one agent acting on behalf of another with qualified context | ADAPT | confirms relation value; keep Authority/Responsibility separately stronger in LifeOS |
| W3C PROV Delegation authority/responsibility wording | combines notions LifeOS has separated | ANTI-PATTERN if copied literally | do not merge Representation with Authority/Responsibility |
| NIST SP 800-63-4 digital identity roles | subscriber/account/authenticator/security roles remain distinguishable | ALREADY STRONGER / boundary confirmation | reinforces Person/Account/Principal separation without importing security vocabulary |
| generic IAM `Principal` | security identity used for authentication/authorization | NOT APPLICABLE as domain primitive | retain as security/logical concept |

**EV-03 result:** external evidence converges on attribution separation and does not justify a universal Agent/Principal/Delegation root.

## EV-04 — Candidate minimality

Hypotheses:

```text
H0 Actor + Authority + Provenance only; no Representation semantics
H1 universal Principal/Agent domain root
H2 generic Delegation root
H3 contextual Representation/on-behalf-of relation + existing Actor/Authority/Provenance
H4 technical impersonation becomes domain attribution
H5 Provenance alone owns represented-party semantics
```

Result:

```text
H0 FAIL
H1 FAIL
H2 FAIL
H3 SURVIVES
H4 FAIL
H5 FAIL
```

Smallest surviving result:

```text
Representation / on-behalf-of
= contextual action-scoped relation/capability
  preserving actual Actor + distinct represented party

Delegation
= bounded Authority-establishment / entrustment pattern
  not universal root

Principal
= technical security identity boundary
  not LifeOS domain primitive
```

---

# 4. Candidate definition / identity / boundaries

Canonical Representation definition:

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context. Representation preserves the actual Actor and represented party separately and, where legitimacy or effect matters, preserves the applicable Authority, delegation, policy, Consent or other basis separately. Representation does not by itself create Authority, Responsibility, Agreement, Consent, Acknowledgement, Confirmation, authorship, truth, technical Principal identity, or an effective domain change.**

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

Classification:

```text
REPRESENTATION / ON-BEHALF-OF
CANONICAL CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY

Representative = contextual role
not native entity/root
not Principal
not Authority
not Responsibility
not Subject/beneficiary
not Provenance
not impersonation
```

Delegation disposition:

```text
bounded Authority-establishment / entrustment pattern
not universal cross-domain primitive/root
not blanket transfer
not automatic re-delegation
```

Principal disposition:

```text
technical authenticated/authorized security identity
not LifeOS domain primitive
not Person
not Actor
not Account equivalence
not represented party
not Authority
```

---

# 5. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence / scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| CORE-01 Real-World Workflow Inversion | yes | assistant/manager, caregiver, parent/child, AI/service, external helper | PASS | representation recurs independently from Account/Authority |
| CORE-02 Deep Chronological Simulation | yes | grant → represented action → revocation → later attempt | PASS WITH HARDENING | preserve action-time Actor, represented party, basis and later revocation/history |
| CORE-03 Adversarial Reductio | yes | remove Representation; merge into Principal/Authority/Provenance; universal Delegation | PASS | Representation survives; universal roots fail |
| CORE-04 Semantic Redundancy / Merge-Split | yes | Representation vs Actor/Authority/Provenance/Principal/Subject | PASS WITH HARDENING | distinct questions and lifecycles |
| CORE-05 Multidirectional Traceability | yes | Principal/auth context → Actor → Representation → Authority basis → effect | PASS | consequential chain reconstructible |
| CORE-06 Orphan / Independence | yes | accountless party; Authority without Representation; invalid representation claim | PASS | Representation independent and no Account requirement |
| CORE-07 External Cross-Domain Benchmark | yes | RFC 8693, FHIR, PROV, NIST | PASS | behavior converges on actor/represented distinction |
| CORE-08 External Anti-Pattern Review | yes | shared-account truth, impersonation-as-domain, universal Agent/Delegation | PASS | anti-patterns explicitly rejected |
| CORE-09 Correction / Reconciliation / Epistemic Integrity | yes | wrong representative, disputed basis, revoked authority | PASS WITH HARDENING | claims/basis may be disputed; history preserved |
| CORE-10 Scale / Performance / History | yes | high-volume service actions, delegation chains | PASS WITH HARDENING | preserve material representation chain, not every technical hop |
| CORE-11 Simple User / Power User | yes | ordinary self-use vs care/admin/high-consequence flows | PASS | representation normally hidden in simple UI |
| CORE-12 Product Value / Complexity Cost | yes | proxy/delegation setup burden | PASS WITH HARDENING | no representation bureaucracy for ordinary direct self-actions |
| CORE-13 Implementation Pressure Without Premature Schema | yes | AuthN/AuthZ, typed actors, chain/basis/history | PASS WITH HARDENING | semantic boundary fixed without IAM or table design |

**CORE Gate:** PASS WITH HARDENING.

---

# 6. Deep chronology stress

```text
T0 Anna exists as Person.

T1 Anna establishes bounded delegated Authority to Luca:
   action: manage selected Schedule placements
   scope: Project X
   period: 7 days
   re-delegation: not granted

T2 Luca authenticates using his own Account/Principal context.

T3 Luca changes Anna's Schedule under that delegation.

   actual Actor      = Luca
   represented party = Anna
   Principal         = Luca security context
   Authority basis   = bounded delegation
   effective state   = owned by Schedule

T4 Luca asks AI to propose an improved slot.
   AI Actor = proposer.
   AI != Anna.
   AI != Luca.

T5 delegation is revoked.

T6 Luca attempts another represented Schedule action.
   representation claim/action may remain attributable;
   applicable Authority no longer exists.

T7 attempted change does not become legitimate/effective merely because Luca previously represented Anna.

T8 historical query reconstructs actor, represented party, action-time basis, revocation and resulting effects separately.
```

Required chronology:

```text
current Authority != historical action-time Authority
past valid representation != standing future Authority
revoked basis != never existed
representation claim != legitimate effect
```

---

# 7. Destructive reductio

```text
REMOVE Representation
→ FAIL: either actual Actor or represented-party context is lost.

Representation = Actor
→ FAIL: Actor answers who acted, not for whom.

Representation = Subject/beneficiary
→ FAIL: acting concerning someone != acting for them.

Representation = Authority
→ FAIL: representation can be claimed/recorded without legitimate Authority; Authority can exist without representation.

Representation = Responsibility
→ FAIL: acting for someone != accountability.

Representation = Provenance
→ FAIL: lineage does not own the represented-party semantic relation.

Representation = Principal
→ FAIL: authenticated request identity != domain Actor/represented party.

Universal Delegation root
→ FAIL: Authority, Responsibility, Participation, Agreement/Consent and other role changes have different semantics.

Technical impersonation = domain attribution
→ FAIL: erases material actual Actor.
```

---

# 8. Mandatory hardenings — incorporated

1. Preserve the actual semantic Actor where material.
2. Actual Actor != represented party.
3. Represented party != Subject/beneficiary automatically.
4. Representation != Authority.
5. `I act for X` != established right to act for X.
6. Representation != Delegation.
7. Delegation is bounded by action/target/scope/context.
8. Authority to do X for B != Authority to do Y for B.
9. Delegation of Authority != transfer of Responsibility.
10. Re-delegation is not implied.
11. Representative action != represented person's Acknowledgement automatically.
12. Representative action != represented person's Confirmation automatically.
13. Representative assent != represented person's Agreement automatically.
14. Representative permission != represented person's Consent automatically.
15. Representative Decision/action preserves the actual decision/action Actor.
16. Principal != semantic Actor.
17. Account != Principal.
18. Represented Person requires no synthetic Account.
19. Technical impersonation must not rewrite material domain attribution truth.
20. Revoked/expired representation basis != never existed.
21. Disputed/alleged representation may remain unresolved.
22. AI/service actions must not be laundered into human authorship, assent or will.
23. Result Visibility != Representation/basis/Evidence Visibility.
24. Representation persistence/formality is consequence-sensitive.
25. Legal/clinical validity of representation is not proven merely by a LifeOS relation.

---

# 9. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Result | Finding / hardening |
|---|---:|---|---|
| MA-01 Identity / Account Independence | yes | PASS | represented parties and representatives may be accountless |
| MA-02 Shared Canonical Fact / Actor Overlay | yes | PASS WITH HARDENING | shared effect coexists with actor/represented attribution |
| MA-03 Responsibility / Assignment / Claim | yes | PASS WITH HARDENING | acting/delegated Authority does not transfer Responsibility |
| MA-04 Coordination Stewardship / Mental Load | yes | PASS | Representation does not prove Stewardship transfer |
| MA-05 Common Ground / State Separation | yes | PASS WITH HARDENING | represented action != represented person's Ack/Agreement/Consent |
| MA-06 Authority / Canonical Change | yes | PASS WITH HARDENING | Representation never manufactures Authority |
| MA-07 Selective Disclosure | yes | PASS WITH HARDENING | representative may receive only minimum necessary projection; basis may remain private |
| MA-08 Inference Privacy | yes | PASS WITH HARDENING | representation relationship itself may reveal sensitive facts |
| MA-09 Partial Adoption / External Participant | yes | PASS | external representative supported without Account |
| MA-10 Assisted Participation / Assertion Provenance | yes | PASS WITH HARDENING | core justification: helper/recorder/representative must not impersonate represented person |
| MA-11 Lifecycle / Revocation | yes | PASS WITH HARDENING | expiry/revocation changes future applicability while preserving history |
| MA-12 Conflict / Adversarial Relationship | yes | PASS WITH HARDENING | alleged representation/basis may remain disputed |
| MA-13 Unequal Power / Guardian / Caregiver | yes | PASS WITH HARDENING | Authority concerning someone does not fabricate their personal will/Consent |
| MA-14 Multi-Resource / Capacity | limited | PASS | Representation changes neither Resource nor Capacity truth |
| MA-15 Coordination-Burden Distribution | yes | PASS | no mandatory proxy machinery for ordinary use |
| MA-16 Formality / Progressive Disclosure | yes | PASS | simple assisted labels to richer history only when consequence warrants |
| MA-17 AI Authority / Multi-Party Context | yes | PASS WITH HARDENING | AI may act under bounded policy but cannot fabricate human action/will |
| MA-18 Specialist-System Boundary | yes | PASS WITH HARDENING | legal/clinical/organizational representative authority may remain externally authoritative |
| MA-19 Multi-Actor Primitive Redundancy | yes | PASS | universal Principal/Agent/Delegation roots unnecessary |
| MA-20 Actor-Scoped Reality Attribution | yes | PASS WITH HARDENING | actual Actor stays distinct even when effect is for another party |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 10. Cross-Concept Consistency Gate

| Test ID | Result | Closure |
|---|---|---|
| XCON-01 Identity | PASS WITH HARDENING | Person/Actor/Account/Principal/represented party remain distinct |
| XCON-02 Authority | PASS WITH HARDENING | Representation does not establish governance legitimacy |
| XCON-03 Planned / current / Actual / history | PASS WITH HARDENING | action-time representation/basis remains reconstructible after revocation |
| XCON-04 Relationships | PASS | specific contextual direct/qualified relation fits Relationship v0 discipline |
| XCON-05 Multi-actor | PASS WITH HARDENING | actor/represented party/subject/participant remain independently attributable |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Representation/on-behalf-of must become canonical; Principal remains security language |

**Structural reopening of prior accepted concepts:** 0.

---

# 11. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Representation ↔ Actor | actual Actor != represented party |
| Representation ↔ Subject/beneficiary | acting for != aboutness/benefit |
| Representation ↔ Authority | representation != governance legitimacy |
| Representation ↔ Responsibility | acting for != accountability |
| Representation ↔ Participation response | response Actor may differ from participant |
| Representation ↔ Acknowledgement | representative action != represented Actor's Ack by default |
| Representation ↔ Confirmation | representative action != represented Actor's Confirmation by default |
| Representation ↔ Decision | represented effect != identity of decision Actor |
| Representation ↔ Agreement | representative assent does not automatically create represented party's Agreement |
| Representation ↔ Consent | representative permission does not automatically create represented party's Consent |
| Representation ↔ Provenance | represented-party relation != lineage |
| generic Delegation primitive | REJECTED; bounded Authority-establishment pattern retained |
| Principal as domain primitive | REJECTED; security identity boundary retained |
| impersonation as domain attribution | REJECTED |

## SAFE DEFERRED — exact Principal / AuthN / AuthZ model

**Unresolved:** authentication identities, service principals, credentials, session/token semantics, enforcement.  
**Why safe:** Person/Actor/Account/Principal/Authority/Representation semantic split is fixed independently.  
**Owner:** security + logical model.  
**Reopening trigger:** security implementation cannot preserve semantic Actor/represented-party/Authority attribution without changing the domain boundary.  
**Tests:** CORE-04, CORE-05, CORE-10, CORE-13, MA-01, MA-06, MA-10, MA-17, XCON-01, XCON-02.

## SAFE DEFERRED — technical impersonation mechanics

**Unresolved:** whether any product/admin flow needs impersonation/token exchange/session switching.  
**Why safe:** current semantic rule already requires material actual Actor attribution.  
**Owner:** security/operations.  
**Reopening trigger:** a required technical mechanism makes actual actor attribution impossible or misleading.  
**Tests:** CORE-02, CORE-05, CORE-08, CORE-09, MA-10, MA-11, MA-17, XCON-01.

## SAFE DEFERRED — action-specific delegability

**Unresolved:** which semantic actions may be delegated and under what policy.  
**Why safe:** no blanket delegation is assumed; each family retains its own semantics.  
**Owner:** Authority/policy + owning semantic family.  
**Reopening trigger:** a concrete family cannot determine represented action effect without a stronger shared Delegation primitive.  
**Tests:** CORE-03, CORE-04, CORE-06, CORE-13, MA-03, MA-05, MA-06, MA-13, XCON-02, XCON-04.

## SAFE DEFERRED — legal representative / capacity

**Unresolved:** guardianship, power of attorney, age/capacity, jurisdiction, clinical/legal validity.  
**Why safe:** LifeOS preserves actor/represented-party/basis semantics without certifying regulated validity.  
**Owner:** specialist/legal/product policy.  
**Reopening trigger:** ordinary LifeOS product must itself determine legally authoritative representation validity.  
**Tests:** CORE-03, CORE-04, CORE-09, CORE-12, MA-06, MA-10, MA-13, MA-18, XCON-02.

## SAFE DEFERRED — represented Agreement / Consent validity

**Unresolved:** when a representative may create legally/clinically effective assent or consent for another party.  
**Why safe:** actual Actor + represented party + basis remain preserved and generic legal validity is not claimed.  
**Owner:** Agreement/Consent + specialist policy.  
**Reopening trigger:** product needs to treat represented assent/permission as authoritative without an external/specialist validity rule.  
**Tests:** CORE-03, CORE-04, CORE-09, MA-05, MA-06, MA-10, MA-13, MA-18, XCON-02, XCON-05.

## SAFE DEFERRED — Version / material scope

**Unresolved:** exact material-version identity for delegated scope/basis/actions.  
**Why safe:** action/time/scope binding is mandatory semantically.  
**Owner:** Version + logical model.  
**Reopening trigger:** system cannot determine whether a representation/delegation basis applies after material change.  
**Tests:** CORE-02, CORE-05, CORE-09, CORE-10, CORE-13, MA-11, MA-12, XCON-03.

## SAFE DEFERRED — multi-hop delegation chain

**Unresolved:** persistence and validation of legitimate re-delegation chains.  
**Why safe:** re-delegation is explicitly not implied.  
**Owner:** Authority/security/logical model.  
**Reopening trigger:** ordinary workflows require material multi-hop delegation that cannot be represented without a stronger independent lifecycle.  
**Tests:** CORE-02, CORE-04, CORE-05, CORE-10, CORE-13, MA-06, MA-11, MA-12, XCON-02, XCON-03.

## SAFE DEFERRED — Verification of representation basis

**Unresolved:** how claimed delegation/representation basis is checked/established.  
**Why safe:** claim != Authority/verified basis is already canonical.  
**Owner:** Verification/Evidence/Authority.  
**Reopening trigger:** consequential workflows cannot distinguish claimed from established representation without merging Representation into Verification/Authority.  
**Tests:** CORE-04, CORE-05, CORE-09, MA-06, MA-12, MA-18, XCON-02, XCON-04.

## SAFE DEFERRED — Organization / collective representation

**Unresolved:** native Organization/group identity and representation of collectives.  
**Why safe:** current relation can target a native party without inventing universal Organization/Party roots.  
**Owner:** collective/native-identity review.  
**Reopening trigger:** common workflows require collective represented identity/quorum incompatible with current relation semantics.  
**Tests:** CORE-04, CORE-06, CORE-12, MA-02, MA-05, MA-13, MA-19, MA-20, XCON-01, XCON-04, XCON-05.

## SAFE DEFERRED — retention / audit / privacy

**Unresolved:** retention classes, anonymization, technical audit and visibility of representation chains.  
**Why safe:** historical attribution does not imply retaining all sensitive basis payloads forever.  
**Owner:** privacy/retention/security/logical model.  
**Reopening trigger:** deletion/audit rules conflict with required material actor/representation reconstruction.  
**Tests:** CORE-02, CORE-09, CORE-10, MA-07, MA-08, MA-11, MA-13, XCON-03.

## SAFE DEFERRED — AI/service delegation chain

**Unresolved:** service/AI native identity, technical Principal and chained policy mechanics.  
**Why safe:** AI Actor/represented party/Authority ceilings are fixed now.  
**Owner:** AI + Principal/security + logical model.  
**Reopening trigger:** autonomous execution cannot preserve actual AI/service Actor and bounded human policy without identity/Authority collapse.  
**Tests:** CORE-04, CORE-05, CORE-13, MA-06, MA-08, MA-10, MA-17, XCON-01, XCON-02.

```text
REOPEN                         0
unclassified material items    0
```

---

# 12. Adversarial scenario log

| Scenario | Stress | Required result |
|---|---|---|
| assistant validly schedules for manager | ordinary representation | actual Actor assistant; manager represented; bounded Authority separate |
| same assistant acts after delegation revoked | lifecycle | action/claim attributable; effect not legitimate automatically |
| parent coordinates child's appointment | Subject vs representation | child may be Subject/beneficiary; child's personal will not fabricated |
| caregiver transcribes verbal statement | recorder/source | no Representation required unless actually acting for the person |
| AI proposes for user | AI attribution | AI actual proposer; no human Decision/Agreement fabricated |
| AI attempts Consent for user | delegability | no represented Consent without applicable action-specific basis/policy |
| shared Account / technical impersonation | security ambiguity | known material actual Actor preserved separately |
| representative re-delegates without permission | chain | downstream Authority not established |
| accountless external representative | adoption | no synthetic Account required |
| represented party disputes authorization | epistemic conflict | claim/evidence/basis/history preserved; may remain unresolved |
| representative may change Schedule but not see private health cause | privacy | Authority != Visibility |
| manager controls shift over employee objection | unequal power | manager Authority != representation of employee's personal will |
| household membership | false inference | no automatic Representation/delegated Authority |

---

# 13. Reopening / dependency register

| Finding | Severity | Treatment | Reopening trigger |
|---|---|---|---|
| actual Actor vs represented party has independent value | STRUCTURAL | canonical Representation relation/capability | stronger accepted concept proves lossless redundancy |
| Representation = Authority | STRUCTURAL | rejected | real workflows make for-whom and legitimacy inseparable |
| Representation = Principal | STRUCTURAL | rejected | security identity becomes unavoidable domain identity |
| Representation = Subject/beneficiary | STRUCTURAL | rejected | aboutness/benefit and representation converge materially |
| generic Delegation root | STRUCTURAL | rejected | one shared independent lifecycle becomes necessary across semantic families |
| universal Principal/Agent root | STRUCTURAL | rejected | one native domain identity becomes necessary without duplication |
| impersonation as domain attribution | STRUCTURAL | rejected | security mechanism cannot preserve actual semantic Actor |
| action-specific scope/delegability | HARDENING | canonical invariant | family cannot apply effect without generic blanket Delegation |
| revocation/history | HARDENING | canonical invariant | action-time basis cannot be reconstructed |
| represented-person will fabrication | HARDENING | prohibited | specialist rule explicitly establishes equivalent effect |
| Principal/auth enforcement | DEFERRED DEPENDENCY | SAFE DEFERRED | implementation changes semantic boundary |
| legal capacity/representation | SPECIALIST DEPENDENCY | SAFE DEFERRED | LifeOS must certify regulated validity itself |
| multi-hop/redelegation persistence | DEFERRED DEPENDENCY | SAFE DEFERRED | common workflow needs stronger chain model |
| Version/material scope | DEFERRED DEPENDENCY | SAFE DEFERRED | applicability after change cannot be determined |
| workflow complexity | PRODUCT/UX | consequence-sensitive | ordinary personal flows require explicit proxy bureaucracy |

---

# 14. Regression corpus additions

| ID | Scenario | Boundary |
|---|---|---|
| R-REP-01 | valid bounded representation → revocation → later attempted action | lifecycle + action-time Authority |
| R-REP-02 | represented Person != actual Actor != Account != Principal != Authority basis | identity/security separation |
| R-REP-03 | guardian/parent Authority concerning child != child's personal Agreement/Consent/will | unequal power |
| R-REP-04 | helper records another Person's statement without automatically representing them | recorder/source/Subject separation |
| R-REP-05 | AI/service operates under bounded policy; AI Actor preserved; no human authorship/Decision | AI attribution |
| R-REP-06 | delegated Actor attempts unauthorized re-delegation | delegation scope |
| R-REP-07 | technical impersonation/shared credential with known actual Actor | security vs domain attribution |
| R-REP-08 | shared effect visible while representation/delegation basis remains restricted | selective Visibility |

---

# 15. Concept-family verdict

```text
REPRESENTATION / DELEGATION / PRINCIPAL FAMILY
PASS WITH HARDENING
```

Current disposition pending post-write QA:

```text
Representation / On-Behalf-Of
✅ canonical contextual action-scoped relation/capability
✅ actual Actor preserved
✅ represented party preserved separately
✅ action/context scoped
✅ history-sensitive where material
✅ applicable Authority/delegation/policy basis separately representable
❌ native entity/root
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ represented person's will by implication

Representative
✅ contextual role
❌ native Person subtype/root

Delegation
✅ bounded Authority-establishment / entrustment pattern
❌ universal primitive/root
❌ blanket transfer
❌ automatic re-delegation

Principal
✅ technical security identity boundary
❌ LifeOS domain primitive
❌ Person/Actor/Account equivalence

Technical impersonation
✅ possible future security mechanism if justified
❌ accepted domain attribution model
```

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 16. Mandatory future re-tests

Retest at recorded triggers for:

- Principal/AuthN/AuthZ logical/security model;
- technical impersonation/session/token mechanics;
- Version/material-equivalence mechanics;
- Agreement/Consent represented-party legal/capacity semantics;
- Verification of representation/delegation basis;
- collective/Organization representation;
- multi-hop re-delegation;
- retention/audit/privacy;
- AI/service identity and delegation;
- whole-domain multi-actor/privacy/Authority/AI stress;
- persistence/API pressure gate.

Do not reopen by vocabulary alone.

---

# 17. Cluster integration

Not applicable yet. Relationships / Reasoning remains open.

A fresh candidate re-score is required only after this milestone reaches post-write QA PASS.

---

# 18. Documentation propagation

Approved scope for this milestone:

### CREATE

- [x] `../concepts/representation.md`
- [x] this checkpoint

### UPDATE — current canonical state

- [ ] `../language-map.md`
- [ ] `../README.md`
- [ ] `../../workstreams/domain-model.md`
- [ ] `../multi-actor-readiness-v1.md`

### UPDATE — downstream semantic closures

- [ ] `../concepts/person.md`
- [ ] `../concepts/actor.md`
- [ ] `person-actor-account-v0-validation.md`
- [ ] `../concepts/authority.md`
- [ ] `authority-v0-validation.md`
- [ ] `../concepts/participation.md`
- [ ] `participation-v0-validation.md`
- [ ] `../concepts/acknowledgement.md`
- [ ] `acknowledgement-v0-validation.md`
- [ ] `../concepts/confirmation.md`
- [ ] `confirmation-v0-validation.md`
- [ ] `../concepts/decision.md`
- [ ] `decision-v0-validation.md`
- [ ] `../concepts/agreement.md`
- [ ] `../concepts/consent.md`
- [ ] `agreement-consent-v0-validation.md`
- [ ] `../concepts/provenance.md`
- [ ] `provenance-v0-validation.md`
- [ ] `deferred-dependency-closure-clusters-1-4-v0.md`

Intentionally out of scope:

- Visibility concept/checkpoint;
- Responsibility concept/checkpoint;
- Actual;
- Schedule / Time;
- Resource;
- Cross-Cluster v4;
- product research/simulations;
- historical product glossary;
- root `README.md`;
- `docs/PROJECT-STATUS.md`;
- main;
- prototype;
- SQL/API/auth implementation/backend;
- Version concept.

Historical checkpoints must be preserved and closed by explicit downstream amendment rather than silently rewritten.

---

# 19. Git QA gate

This family becomes an accepted Domain Atlas baseline only after full diff QA against:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Required checks:

- exactly 25 approved unique paths changed;
- exactly 2 new files + 23 modified files;
- no out-of-scope path changed;
- full V3 sections remain present;
- all hardenings are incorporated in current specs;
- every SAFE DEFERRED item retains owner, exact trigger and test set;
- `REOPEN = 0` and unclassified material dependencies = 0;
- Language Map, Domain README, Multi-Actor Readiness and workstream agree;
- Person/Actor/Account/Principal separation remains intact;
- Representation != Authority/Responsibility/Subject/Provenance;
- representative action does not fabricate Acknowledgement/Confirmation/Agreement/Consent/Decision;
- Delegation remains bounded Authority-establishment semantics, not universal root;
- Principal remains security-only, not domain primitive;
- technical impersonation does not become domain attribution truth;
- historic checkpoints preserve their original content plus downstream closure;
- no main/prototype/SQL/API/auth/backend/root README/PROJECT-STATUS/product-evidence changes;
- branch remains behind main by 0.

Do not re-score/select the next candidate until this QA passes.
