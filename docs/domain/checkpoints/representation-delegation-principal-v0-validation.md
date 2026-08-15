# Representation / Delegation / Principal v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated; documentation propagation complete; post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `b6c53ffa40ba7c1c1408f583856617a0e000f31b`

## 1. Scope

Candidate family:

```text
Representation / on-behalf-of
Delegation
Principal
technical impersonation boundary
```

Primary question:

> **When someone or something acts for another party, how can LifeOS preserve who actually acted, for whom, and on what bounded basis without turning the represented party into the Actor, fabricating their will, or collapsing the domain into IAM/security?**

Nearest accepted boundaries inspected:

- Person / Actor / Account;
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

Deliberately not designed:

- final Principal/AuthN/AuthZ schema;
- token/session/credential architecture;
- legal guardianship/POA/capacity;
- formal represented Consent/Agreement validity;
- exact Version mechanics;
- collective/Organization representation;
- final SQL/API.

---

# 2. Fresh re-score result

Candidate space was re-scored by dependency leverage, SAFE DEFERRED pressure, cross-cluster impact, multi-actor/AI pressure, implementation blocking risk, ontology cost and specialist leakage.

Ranking at selection time:

```text
1 Representation / delegation / Principal
2 Version / material equivalence
3 detailed reconciliation / source precedence
4 Proposal / request reusable identity
5 GoalCriterion / evaluation
```

Representation won narrowly because the unresolved attribution boundary already crossed Person/Actor/Account, Authority, Participation, Acknowledgement, Confirmation, Decision, Agreement, Consent, Provenance and AI. Version remained highly pressured but material-version invalidation semantics were already established; its exact mechanics remained more logical/persistence-oriented.

---

# 3. Evidence

## EV-01 — Internal LifeOS evidence

Existing accepted semantics already required:

```text
Person != Actor != Account != Principal
```

and repeatedly preserved an unresolved on-behalf-of boundary:

```text
participant/native referent
response Actor
Account/Principal used
on-behalf-of/delegation basis
```

Actor required future on-behalf-of relationships without an Actor root. Authority already treated Delegation as bounded Authority-establishment. Acknowledgement, Confirmation, Decision and Agreement/Consent required truthful assisted attribution. Provenance required material authentication/delegation context without collapsing security identity into domain agency.

**EV-01:** strong pressure; no accepted concept owned the represented-party relation.

## EV-02 — Workflow inversion

Tested:

```text
assistant schedules for manager
caregiver records for another Person
parent coordinates concerning child
external helper responds for another party
AI/service acts under bounded policy
manager acts under institutional Authority
shared-account / technical impersonation
```

Critical negative case:

```text
acting concerning X
!= acting for X
```

A child may be Subject/beneficiary without their parent expressing the child's personal will. A caregiver may merely record another Person's statement without representing that Person.

**EV-02:** actual-Actor ↔ represented-party relation recurs independently.

## EV-03 — External benchmark classifications

| Benchmark | Finding | Classification | LifeOS treatment |
|---|---|---|---|
| RFC 8693 Token Exchange | delegation preserves actor distinct from represented subject | ADAPT | preserve actual Actor + represented party; no token ontology import |
| RFC 8693 impersonation | technical rights context may mask actor/subject distinction | ANTI-PATTERN as domain truth | implementation mechanism must not erase material Actor attribution |
| HL7 FHIR Provenance `who` / `onBehalfOf` | acting agent separated from represented party | ADAPT | attribution pattern only; no healthcare ontology import |
| W3C PROV `actedOnBehalfOf` | one agent can act for another in qualified context | ADAPT | confirms relation value |
| W3C delegation wording coupling authority/responsibility | weaker separation than LifeOS | ANTI-PATTERN if copied literally | keep Authority and Responsibility separate |
| NIST SP 800-63-4 identity/security roles | real-world and security identities distinguishable | ALREADY STRONGER / boundary confirmation | reinforce existing Person/Account/Principal split |
| generic IAM Principal | request security identity | NOT APPLICABLE as domain primitive | security/logical language only |

## EV-04 — Candidate minimality

```text
H0 Actor + Authority + Provenance only             FAIL
H1 universal Principal/Agent domain root          FAIL
H2 generic Delegation root                        FAIL
H3 contextual Representation/on-behalf-of         SURVIVES
H4 impersonation becomes domain attribution       FAIL
H5 Provenance alone owns represented-party link   FAIL
```

Smallest surviving result:

```text
Representation / on-behalf-of
= contextual action-scoped relation/capability

Delegation
= bounded Authority-establishment/entrustment pattern

Principal
= technical security identity boundary
```

---

# 4. Candidate definition / disposition

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context. Representation preserves the actual Actor and represented party separately and, where legitimacy or effect matters, preserves the applicable Authority, delegation, policy, Consent or other basis separately.**

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

```text
Representation / on-behalf-of
✅ canonical contextual action-scoped relation/capability
✅ actual Actor preserved
✅ represented party distinct
✅ basis separately representable
❌ native entity/root
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ represented-party will by implication

Representative
✅ contextual role
❌ Person subtype/root

Delegation
✅ bounded Authority-establishment / entrustment pattern
❌ universal primitive/root
❌ blanket transfer
❌ automatic re-delegation

Principal
✅ technical authenticated/authorized security identity
❌ LifeOS domain primitive
❌ Person/Actor/Account equivalence

Technical impersonation
✅ possible future security mechanism if justified
❌ accepted domain attribution model
```

---

# 5. CORE Semantic Validation Gate

| Test | Result | Finding / hardening |
|---|---|---|
| CORE-01 Workflow inversion | PASS | representation recurs independently from Account/Authority |
| CORE-02 Deep chronology | PASS WITH HARDENING | action-time Actor, represented party, basis, expiry/revocation reconstructible |
| CORE-03 Reductio | PASS | Representation survives; Principal/Delegation/impersonation roots fail |
| CORE-04 Redundancy | PASS WITH HARDENING | Representation != Actor/Authority/Provenance/Principal/Subject |
| CORE-05 Traceability | PASS | Principal/auth context → Actor → Representation → Authority basis → effect traceable |
| CORE-06 Independence | PASS | accountless parties supported; Authority may exist without Representation |
| CORE-07 Benchmark | PASS | standards converge on actor/represented separation |
| CORE-08 Anti-pattern | PASS | shared-account truth, impersonation-as-domain, universal Agent/Delegation rejected |
| CORE-09 Correction/reconciliation | PASS WITH HARDENING | wrong/disputed/revoked basis preserves history |
| CORE-10 Scale/history | PASS WITH HARDENING | material representation chain only, not every technical hop |
| CORE-11 Simple/power user | PASS | ordinary self-use hides machinery |
| CORE-12 Product complexity | PASS WITH HARDENING | no proxy/delegation bureaucracy by default |
| CORE-13 Implementation pressure | PASS WITH HARDENING | semantics fixed without IAM/table design |

**CORE Gate:** PASS WITH HARDENING.

---

# 6. Deep chronology

```text
T0 Anna exists as Person
T1 Anna grants Luca bounded Authority to manage selected Schedule placements for Project X for seven days; no re-delegation
T2 Luca authenticates using his own Account/Principal
T3 Luca changes Anna's Schedule
   actual Actor      = Luca
   represented party = Anna
   Principal         = Luca security context
   Authority basis   = bounded delegation
   effective state   = Schedule-owned
T4 Luca requests AI proposal
   AI Actor = proposer; AI != Luca != Anna
T5 delegation revoked
T6 Luca attempts another represented action
T7 attempted effect does not become legitimate merely because earlier representation was valid
T8 historical query reconstructs actor, represented party, basis, revocation and effect separately
```

Required:

```text
current Authority != historical action-time Authority
past valid Representation != standing future Authority
revoked basis != never existed
Representation claim != legitimate/effective effect
```

---

# 7. Destructive reductio

```text
REMOVE Representation               FAIL
Representation = Actor               FAIL
Representation = Subject             FAIL
Representation = Authority           FAIL
Representation = Responsibility      FAIL
Representation = Provenance          FAIL
Representation = Principal           FAIL
universal Delegation root            FAIL
impersonation = domain attribution    FAIL
specific Representation relation     PASS WITH HARDENING
```

---

# 8. Mandatory hardenings — incorporated

1. preserve actual semantic Actor where material;
2. actual Actor != represented party;
3. represented party != Subject/beneficiary automatically;
4. Representation != Authority;
5. claim of representation != established right;
6. Representation != Delegation;
7. delegation bounded by action/target/scope/context;
8. Authority to X != Authority to Y;
9. delegation of Authority != transfer of Responsibility;
10. re-delegation not implied;
11. representative action != represented-party Acknowledgement automatically;
12. representative action != represented-party Confirmation automatically;
13. representative assent != represented-party Agreement automatically;
14. representative permission != represented-party Consent automatically;
15. represented Decision preserves actual decision Actor/process;
16. Principal != Actor;
17. Account != Principal;
18. represented Person needs no synthetic Account;
19. technical impersonation does not rewrite material domain attribution;
20. revoked/expired basis != never existed;
21. disputed representation may remain unresolved;
22. AI/service action is not human authorship/will;
23. result Visibility != Representation/basis Visibility;
24. persistence/formality consequence-sensitive;
25. LifeOS relation does not prove specialist legal/clinical validity.

---

# 9. Multi-Actor Compatibility Gate

| Test | Result | Finding |
|---|---|---|
| MA-01 Identity/account independence | PASS | representatives/represented parties may be accountless |
| MA-02 Shared fact / overlay | PASS WITH HARDENING | shared effect + separate representation attribution coexist |
| MA-03 Responsibility | PASS WITH HARDENING | representation/delegated Authority does not transfer Responsibility |
| MA-04 Stewardship | PASS | no stewardship transfer inference |
| MA-05 Common ground | PASS WITH HARDENING | represented action != represented person's Ack/Agreement/Consent |
| MA-06 Authority | PASS WITH HARDENING | Representation never manufactures Authority |
| MA-07 Selective disclosure | PASS WITH HARDENING | representative may receive minimum necessary projection; basis may be private |
| MA-08 Inference privacy | PASS WITH HARDENING | representation relationship itself may be sensitive |
| MA-09 Partial adoption | PASS | accountless external representative supported |
| MA-10 Assisted attribution | PASS WITH HARDENING | helper/representative cannot impersonate represented party |
| MA-11 Lifecycle/revocation | PASS WITH HARDENING | expiry/revocation affects future, preserves history |
| MA-12 Conflict | PASS WITH HARDENING | alleged representation/basis may remain disputed |
| MA-13 Unequal power | PASS WITH HARDENING | Authority concerning someone != their personal will/Consent |
| MA-14 Resource/capacity | PASS — limited | Representation changes neither Resource nor Capacity truth |
| MA-15 Burden | PASS | no mandatory proxy machinery |
| MA-16 Progressive formality | PASS | simple labels to rich history by consequence |
| MA-17 AI | PASS WITH HARDENING | AI can act under policy but cannot fabricate human will |
| MA-18 Specialist boundary | PASS WITH HARDENING | legal/clinical representative validity may remain external |
| MA-19 Primitive redundancy | PASS | universal Principal/Agent/Delegation roots unnecessary |
| MA-20 Actor-scoped attribution | PASS WITH HARDENING | actual Actor stays distinct |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 10. Cross-Concept Consistency Gate

| Test | Result | Closure |
|---|---|---|
| XCON-01 Identity | PASS WITH HARDENING | Person/Actor/Account/Principal/represented party distinct |
| XCON-02 Authority | PASS WITH HARDENING | Representation != legitimacy |
| XCON-03 Current/history | PASS WITH HARDENING | action-time basis survives revocation |
| XCON-04 Relationships | PASS | specific direct/qualified relation discipline fits |
| XCON-05 Multi-actor | PASS WITH HARDENING | actor/represented/subject/participant independently attributable |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED → completed | canonical mappings propagated |

**Structural reopening of prior accepted concepts:** 0.

---

# 11. Adjacent Dependency Sweep

## RESOLVED

```text
Representation ↔ Actor
Representation ↔ Subject/beneficiary
Representation ↔ Authority
Representation ↔ Responsibility
Representation ↔ Participation response
Representation ↔ Acknowledgement
Representation ↔ Confirmation
Representation ↔ Decision
Representation ↔ Agreement
Representation ↔ Consent
Representation ↔ Provenance
Principal as domain primitive                 REJECTED
universal Delegation primitive                REJECTED
impersonation as domain attribution           REJECTED
```

## SAFE DEFERRED — exact Principal / AuthN / AuthZ model

**Unresolved:** security identities, service principals, credentials, sessions/tokens, enforcement.  
**Why safe:** semantic identity/agency/Authority/Representation split is fixed independently.  
**Owner:** security + logical model.  
**Trigger:** implementation cannot preserve Actor/represented-party/Authority attribution without changing domain semantics.  
**Tests:** CORE-04/05/10/13, MA-01/06/10/17, XCON-01/02.

## SAFE DEFERRED — technical impersonation mechanics

**Unresolved:** whether product/admin flows need impersonation/token exchange/session switching.  
**Why safe:** material actual Actor must already be preserved.  
**Owner:** security/operations.  
**Trigger:** required mechanism makes actual-actor attribution impossible or misleading.  
**Tests:** CORE-02/05/08/09, MA-10/11/17, XCON-01.

## SAFE DEFERRED — action-specific delegability

**Unresolved:** which semantic actions may be delegated and under what policy.  
**Why safe:** no blanket delegation; each family owns effect semantics.  
**Owner:** Authority/policy + owning family.  
**Trigger:** concrete family cannot apply represented effect without generic Delegation primitive.  
**Tests:** CORE-03/04/06/13, MA-03/05/06/13, XCON-02/04.

## SAFE DEFERRED — legal representative / capacity

**Unresolved:** guardianship, POA, age/capacity, jurisdiction, regulated validity.  
**Why safe:** LifeOS records attribution/basis without certifying legal validity.  
**Owner:** specialist/legal/product policy.  
**Trigger:** ordinary LifeOS must itself establish legally authoritative representation.  
**Tests:** CORE-03/04/09/12, MA-06/10/13/18, XCON-02.

## SAFE DEFERRED — represented Agreement / Consent validity

**Unresolved:** when a representative action legally/clinically establishes another party's assent/Consent.  
**Why safe:** actual Actor + represented party + basis preserved; universal validity not claimed.  
**Owner:** Agreement/Consent + specialist policy.  
**Trigger:** product must treat represented assent/permission as authoritative without external/specialist rule.  
**Tests:** CORE-03/04/09, MA-05/06/10/13/18, XCON-02/05.

## SAFE DEFERRED — Version / material scope

**Unresolved:** material-version identity for delegation/representation applicability.  
**Why safe:** action/time/scope binding canonical now.  
**Owner:** Version + logical model.  
**Trigger:** applicability after material change cannot be determined.  
**Tests:** CORE-02/05/09/10/13, MA-11/12, XCON-03.

## SAFE DEFERRED — multi-hop delegation

**Unresolved:** persistence/validation of legitimate re-delegation chains.  
**Why safe:** re-delegation explicitly not implied.  
**Owner:** Authority/security/logical model.  
**Trigger:** ordinary workflows require stronger chain identity/lifecycle.  
**Tests:** CORE-02/04/05/10/13, MA-06/11/12, XCON-02/03.

## SAFE DEFERRED — Verification of representation basis

**Unresolved:** how claimed basis becomes established.  
**Why safe:** claim != Authority/verified basis already canonical.  
**Owner:** Verification/Evidence/Authority.  
**Trigger:** consequential workflows cannot distinguish claim from established basis without semantic collapse.  
**Tests:** CORE-04/05/09, MA-06/12/18, XCON-02/04.

## SAFE DEFERRED — Organization / collective representation

**Unresolved:** native Organization/group identity and collective representation.  
**Why safe:** no universal Party/Group identity required now.  
**Owner:** collective/native-identity review.  
**Trigger:** common workflows require collective represented identity/quorum incompatible with current relation.  
**Tests:** CORE-04/06/12, MA-02/05/13/19/20, XCON-01/04/05.

## SAFE DEFERRED — retention / audit / privacy

**Unresolved:** retention, anonymization, technical audit, visibility of representation chains.  
**Why safe:** historical attribution != retain every sensitive payload forever.  
**Owner:** privacy/retention/security/logical model.  
**Trigger:** deletion/audit rules conflict with required material reconstruction.  
**Tests:** CORE-02/09/10, MA-07/08/11/13, XCON-03.

## SAFE DEFERRED — AI/service delegation chain

**Unresolved:** service/AI native identity, Principal and chained-policy mechanics.  
**Why safe:** AI Actor/represented party/Authority ceilings fixed now.  
**Owner:** AI + Principal/security + logical model.  
**Trigger:** autonomous execution cannot preserve actual AI/service Actor and bounded human policy without collapse.  
**Tests:** CORE-04/05/13, MA-06/08/10/17, XCON-01/02.

```text
REOPEN                         0
unclassified material items    0
```

---

# 12. Adversarial log

| Scenario | Required result |
|---|---|
| assistant validly schedules for manager | assistant actual Actor; manager represented; Authority separate |
| assistant acts after revocation | attempt attributable; effect not legitimate automatically |
| parent coordinates child's appointment | child may be Subject; personal will not fabricated |
| caregiver transcribes statement | recorder/source separation; no automatic Representation |
| AI proposes for user | AI actual proposer; no human Decision fabricated |
| AI attempts Consent for user | no represented Consent absent applicable action-specific basis |
| shared Account / impersonation | known actual Actor preserved |
| unauthorized re-delegation | downstream Authority not established |
| accountless representative | supported without synthetic Account |
| represented party disputes basis | claim/Evidence/basis/history preserved; conflict may remain unresolved |
| representative can schedule but not see private health cause | Authority != Visibility |
| manager controls shift over objection | Authority != representation of worker's personal will |
| household membership | no automatic Representation/Delegation |

---

# 13. Reopening / dependency register

| Finding | Severity | Treatment |
|---|---|---|
| actual Actor vs represented party | STRUCTURAL | canonical Representation capability |
| Representation = Authority | STRUCTURAL | rejected |
| Representation = Principal | STRUCTURAL | rejected |
| Representation = Subject | STRUCTURAL | rejected |
| generic Delegation root | STRUCTURAL | rejected |
| universal Principal/Agent root | STRUCTURAL | rejected |
| impersonation as domain truth | STRUCTURAL | rejected |
| action-specific scope | HARDENING | canonical invariant |
| revocation/history | HARDENING | canonical invariant |
| represented-person will fabrication | HARDENING | prohibited |
| Principal/auth enforcement | DEFERRED | SAFE DEFERRED |
| legal capacity/representation | SPECIALIST | SAFE DEFERRED |
| multi-hop delegation | DEFERRED | SAFE DEFERRED |
| Version/material scope | DEFERRED | SAFE DEFERRED |
| product complexity | UX | consequence-sensitive |

---

# 14. Regression corpus additions

```text
R-REP-01 valid bounded Representation → revocation → later attempted action
R-REP-02 represented Person != actual Actor != Account != Principal != Authority basis
R-REP-03 guardian/parent Authority concerning child != child's personal Agreement/Consent/will
R-REP-04 helper records another Person statement without automatic Representation
R-REP-05 AI/service under bounded policy → AI Actor preserved; no human authorship/Decision
R-REP-06 delegated Actor attempts unauthorized re-delegation
R-REP-07 technical impersonation/shared credential → material actual Actor preserved
R-REP-08 shared represented effect + private representation/delegation basis
```

---

# 15. Verdict

```text
REPRESENTATION / DELEGATION / PRINCIPAL FAMILY
PASS WITH HARDENING

Representation / on-behalf-of       CANONICAL
Representative contextual role      CANONICAL ROLE LANGUAGE
universal Delegation root            REJECTED
Principal domain primitive           REJECTED
technical impersonation as domain    REJECTED

REOPEN                               0
unclassified material dependencies   0
```

No prior accepted concept requires structural reopening.

---

# 16. Mandatory future re-tests

Retest when these owners mature:

- Principal/AuthN/AuthZ security/logical model;
- technical impersonation/session/token mechanics;
- Version/material equivalence;
- represented Agreement/Consent capacity/validity;
- Verification of representation basis;
- collective/Organization representation;
- multi-hop re-delegation;
- retention/audit/privacy;
- AI/service identity/delegation;
- whole-domain multi-actor/privacy/Authority/AI regression;
- persistence/API pressure gate.

---

# 17. Cluster integration

Not applicable yet. Relationships / Reasoning remains open.

After this QA-closed milestone, perform a **fresh candidate re-score**. Do not preselect Version merely because it ranked second in the previous re-score.

---

# 18. Documentation propagation — complete

### CREATE

- [x] `../concepts/representation.md`
- [x] this checkpoint

### UPDATE — current canonical state

- [x] `../language-map.md`
- [x] `../README.md`
- [x] `../../workstreams/domain-model.md`
- [x] `../multi-actor-readiness-v1.md`

### UPDATE — downstream closures

- [x] `../concepts/person.md`
- [x] `../concepts/actor.md`
- [x] `person-actor-account-v0-validation.md`
- [x] `../concepts/authority.md`
- [x] `authority-v0-validation.md`
- [x] `../concepts/participation.md`
- [x] `participation-v0-validation.md`
- [x] `../concepts/acknowledgement.md`
- [x] `acknowledgement-v0-validation.md`
- [x] `../concepts/confirmation.md`
- [x] `confirmation-v0-validation.md`
- [x] `../concepts/decision.md`
- [x] `decision-v0-validation.md`
- [x] `../concepts/agreement.md`
- [x] `../concepts/consent.md`
- [x] `agreement-consent-v0-validation.md`
- [x] `../concepts/provenance.md`
- [x] `provenance-v0-validation.md`
- [x] `deferred-dependency-closure-clusters-1-4-v0.md`

Intentionally out of scope:

```text
Visibility concept/checkpoint
Responsibility concept/checkpoint
Actual
Schedule / Time
Resource
Cross-Cluster v4
product research/simulations
historical product glossary
root README
PROJECT-STATUS
main
prototype
SQL/API/auth implementation/backend
Version concept
```

Historical checkpoints retain their original decision material with explicit downstream Representation amendments. The Clusters 1–4 closure retains its pre-scope content and appends a Representation resolution appendix.

---

# 19. Post-write Git QA — PASS

Validated against:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Result:

```text
approved unique paths changed          25 / 25
new files                                2 / 2
modified files                          23 / 23
out-of-scope paths                       0
structural REOPEN                        0
unclassified material dependencies      0
main baseline                           c5120ff463e027c42f4a26fc613d0917596ca738
branch behind main                       0
```

Semantic QA confirmed:

- full CORE-01..13, MA-01..20, XCON-01..06 and ADS coverage;
- hardenings incorporated;
- every SAFE DEFERRED item has unresolved question, why safe, owner, exact trigger and tests;
- actual Actor != represented party;
- Person/Actor/Account/Principal boundaries intact;
- Representation != Authority/Responsibility/Subject/Provenance;
- representative action does not fabricate represented-party Acknowledgement/Confirmation/Agreement/Consent/Decision;
- Delegation remains bounded Authority semantics, not universal root;
- Principal remains security-only;
- technical impersonation does not become domain attribution truth;
- historical checkpoints remain reconstructible through downstream amendments;
- no main/prototype/root README/PROJECT-STATUS/product-evidence/SQL/API/auth/backend changes;
- branch remains behind main by 0.

The Representation write approval is consumed after this QA PASS.

---

# 20. Downstream closure — Version / material-equivalence v0 (2026-08-13)

Version v0 resolves the checkpoint's historical `Version / material scope` SAFE DEFERRED dependency without reopening Representation.

Canonical separation:

```text
Representation identity/context
= actual Actor acted for a distinct represented party in a bounded action/context

material target/action state
= the state the represented action actually concerned

Version
= purpose/facet-scoped reference to that material state
```

A represented or delegated action must bind to the materially relevant target/scope state where stale applicability would matter. A later material change to target, terms, delegation scope, policy or action context does not silently make the earlier represented action/Authority basis applicable to the new state.

Version does not create Representation, Delegation or Authority. It preserves which state was acted on; action-specific policy/Authority still determines whether the represented action was legitimate/effective. Current and historical Representation attribution, together with action-time Authority, remain reconstructible after later revision, expiry or revocation.

Principal/session/token/provider revisions are technical security/integration state and do not become semantic Version of the represented party or domain action automatically. Likewise a changed hash/ETag/storage revision is not proof that Representation semantics materially changed.

Non-linear/offline history may preserve competing material target or scope states until reconciliation. Version does not choose the winning state and does not launder an invalid stale action into a valid represented action.

Downstream classification:

```text
Representation ↔ Version/material scope   RESOLVED
Version ↔ Representation/Authority        RESOLVED — distinct
```

Still independently SAFE DEFERRED are exact Principal/AuthN/AuthZ mechanics, technical impersonation, action-specific delegability, legal/specialist capacity, represented Agreement/Consent validity, multi-hop delegation, Verification of representation basis, Organization/collective representation, retention/audit/privacy, AI/service delegation chain and physical persistence.

No Representation hardening failed. **Representation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.

---

# 21. Downstream closure — Proposal / Request v0 (2026-08-15)

Proposal / Request v0 resolves how represented proposal/request acts are attributed without reopening Representation.

Canonical separation:

```text
actual proposer/requester Actor
!= represented party by default

Representation
= bounded on-behalf-of relation for the act

Authority / delegation / policy / Consent / specialist basis
= legitimacy/effect basis where required
```

A represented Proposal/Request remains the actual Actor's semantic action. The represented party is not rewritten as proposer/requester and does not acquire fabricated personal intention, Acknowledgement, Agreement, Consent or Decision.

A claim to issue a request for someone can remain attributable even where the applicable Authority/basis is disputed or invalid; attribution does not make the requested effect legitimate. AI/service requests preserve the same actual-Actor rule.

Material changes to action/target/scope remain Version-sensitive and cannot silently enlarge the represented basis.

Downstream classification:

```text
Representation ↔ Proposal / Request      RESOLVED
represented party = actual proposer      REJECTED by default
represented party = actual requester     REJECTED by default
```

No Representation hardening failed. **Representation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/proposal.md`;
- `../concepts/request.md`;
- `proposal-request-v0-validation.md`.
