# Representation / Delegation / Principal v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — hardenings incorporated + post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `b6c53ffa40ba7c1c1408f583856617a0e000f31b`

## 1. Scope

- **Candidate family reviewed:** Representation / on-behalf-of / Delegation / Principal.
- **No candidate was pre-accepted.**
- **Primary problem:** preserve who actually acted, for whom, under which bounded basis, without collapsing semantic agency into technical identity, Authority, Responsibility, Agreement/Consent, Subject/beneficiary or impersonation.
- **Nearest accepted boundaries inspected:** Person, Actor, Account, Authority, Responsibility, Participation, Acknowledgement, Confirmation, Decision, Agreement, Consent, Provenance, Visibility, Subject.
- **Deliberately not designed here:** final AuthN/AuthZ, credentials/tokens/sessions, complete delegation policy engine, universal Organization/Group identity, specialist legal/clinical validity, final SQL/API.

Canonical product question:

> **When someone or something acts for another party, how does LifeOS preserve the actual Actor, represented party and bounded legitimacy/effect without pretending that the represented party personally acted or that technical security identity is domain truth?**

---

# 2. Product / LifeOS fit

LifeOS is personal-first but must support ordinary assistants, caregivers, parents, external helpers, services and AI without identity laundering.

The smallest useful semantic chain is:

```text
actual Actor
!= represented party
!= Subject / beneficiary
!= Account / Principal
!= Authority
!= Responsibility
```

Representation adds precision only where it matters. Ordinary self-service remains simple.

**Product conclusion:** a specific contextual on-behalf-of relation is useful; a universal Principal/Agent/Delegation ontology is not.

---

# 3. Evidence reviewed

## EV-01 — Internal evidence

Current accepted concepts repeatedly preserve attribution boundaries:

- Person is native human identity;
- Actor is contextual agency semantics;
- Account is platform/access identity;
- Principal is already deferred as technical security identity;
- Authority is bounded governance power, not Actor/Account;
- Responsibility is accountability, not Authority;
- Participation response may be submitted by an Actor different from the participant;
- Acknowledgement/Confirmation require truthful actual Actor attribution;
- Agreement/Consent explicitly require actual Actor, represented party and basis where acting on behalf of another;
- Decision requires actual decision Actor/process distinct from represented party and Authority;
- Provenance needs actual Actor/system/Account/Principal context without collapsing identities;
- multi-actor scenarios include assistants, caregivers, guardians and AI/services.

## EV-02 — Real-world workflow inversion

Representative workflows:

### Assistant schedules for another Person

```text
assistant = actual Actor
manager = represented party
meeting/event target = separate
Authority/basis = bounded scheduling permission
```

The manager did not personally click the UI.

### Caregiver records/acts for cared-for Person

Caregiver may record a statement, manage an appointment or perform a bounded action. Acting about or benefiting a Person does not necessarily mean acting on behalf of that Person's will.

### Parent/guardian

A parent may have Authority for some actions without that implying the child personally agreed/consented/acknowledged/confirmed.

### Delegated work action

Authority to approve Schedule X does not imply Authority to agree to unrelated terms, consent to data use or re-delegate.

### AI/service action

A service or AI may perform a bounded action under policy. That does not become human authorship/will merely because it is acting for the user.

## EV-03 — Targeted external benchmark

External standards are evidence only.

| Benchmark | Finding | Classification |
|---|---|---|
| RFC 8693 OAuth Token Exchange | distinguishes subject and actor/delegation/impersonation patterns | ADAPT |
| RFC 8693 impersonation semantics | represented subject may appear as acting identity for technical request | ANTI-PATTERN if copied as domain attribution truth |
| HL7 FHIR Provenance `agent.who` / `onBehalfOf` | preserves actual participating agent and represented organization/person | ADAPT |
| W3C PROV `actedOnBehalfOf` | agency relation can be represented separately | ADAPT |
| W3C PROV coupling of delegation with responsibility | useful provenance model but too broad for LifeOS Responsibility/Authority semantics | ANTI-PATTERN if copied literally |
| NIST digital identity guidance | subject/account/authenticator/authorization roles are distinct | ALREADY STRONGER / boundary confirmation |
| generic IAM Principal | useful security abstraction | NOT APPLICABLE as domain primitive |

## EV-04 — Candidate minimality

Hypotheses:

```text
H0 no Representation; infer from Authority/Provenance
H1 Representation / on-behalf-of specific relation
H2 universal Agent/Representative root
H3 universal Delegation primitive
H4 Principal as LifeOS domain identity
H5 technical impersonation as domain attribution
```

Result:

```text
H0 FAIL
H1 SURVIVES
H2 FAIL
H3 FAIL
H4 FAIL
H5 FAIL
```

---

# 4. Candidate definitions / classification

## Representation / on-behalf-of

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context. Representation preserves the actual Actor and represented party separately and, where legitimacy or effect matters, preserves the applicable Authority, delegation, policy, Consent or other basis separately. Representation does not by itself create Authority, Responsibility, Agreement, Consent, Acknowledgement, Confirmation, authorship, truth, technical Principal identity, or an effective domain change.**

Question:

> **Who actually acted, and for which distinct party was that action performed/asserted in this bounded context?**

Classification:

```text
CANONICAL SPECIFIC CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY
not native entity/root
not universal Agent/Representative identity
```

`Representative` is contextual role language over this relation.

## Delegation

> **Delegation is a bounded Authority-establishment/entrustment pattern for a specific governed action/effect/scope.**

```text
NOT universal cross-domain primitive/root
NOT Responsibility transfer
NOT Participation transfer
NOT Agreement/Consent transfer
NOT blanket authority
```

## Principal

```text
Principal
= authenticated/authorized security identity in technical request/security context
```

```text
Principal != Person
Principal != Account
Principal != Actor
Principal != represented party
Principal != Authority
Principal != Representation
```

Principal remains **security/logical-model language**, not a LifeOS domain primitive.

## Technical impersonation

```text
technical impersonation
!= domain attribution truth
```

Where actual semantic Actor is known, the domain keeps that Actor.

---

# 5. Core Semantic Validation Gate

| Test | Result | Finding |
|---|---|---|
| CORE-01 Workflow inversion | PASS | assistants/caregivers/guardians/services need actual Actor + represented party |
| CORE-02 Deep chronology | PASS WITH HARDENING | action-time Authority/basis must survive later revocation |
| CORE-03 Reductio | PASS | Actor/Authority/Provenance/Principal/Subject cannot replace Representation |
| CORE-04 Redundancy | PASS WITH HARDENING | Representation survives; universal Agent/Delegation/Principal roots fail |
| CORE-05 Traceability | PASS | actual Actor → represented party → basis → target/effect reconstructible |
| CORE-06 Orphan / independence | PASS WITH HARDENING | contextual relation/capability, not identity/root |
| CORE-07 External benchmark | PASS | OAuth/FHIR/PROV reinforce actor/subject/on-behalf-of separation |
| CORE-08 Anti-pattern | PASS | technical impersonation / actor-substitution rejected |
| CORE-09 Correction/reconciliation | PASS WITH HARDENING | claimed/disputed/invalid representation remains preservable |
| CORE-10 Scale/history | PASS | no wrapper row/delegation graph for ordinary self-use |
| CORE-11 Simple/power user | PASS | simple `Done by Luca for Anna` to detailed history |
| CORE-12 Product value/complexity | PASS WITH HARDENING | relation only where actor distinction materially matters |
| CORE-13 Implementation pressure | PASS WITH HARDENING | no universal principal_id/on_behalf_of_id schema pre-approved |

**Core Gate:** PASS WITH HARDENING.

---

# 6. Deep chronology

```text
T0 Anna grants bounded scheduling Authority to Luca
T1 Luca authenticates with own Account/Principal
T2 Luca changes Anna's meeting Schedule acting for Anna
T3 LifeOS records:
   actual Actor = Luca
   represented party = Anna
   basis = bounded scheduling Authority
T4 Anna later revokes that Authority
T5 Luca attempts another represented change
T6 historical query asks what was legitimate at T2 and T5
```

Required truths:

```text
T2 actual Actor remains Luca
T2 represented party remains Anna
T2 basis evaluated at action time
T4 revocation != T2 never valid
T5 attempted Representation may exist as attempted attribution
T5 effect may be rejected for no Authority
current Authority != historical action-time Authority
```

Second chronology:

```text
caregiver records Maria's statement
```

Potential roles:

```text
Maria = Subject/source Person
caregiver = recorder Actor
```

This does **not** automatically require:

```text
caregiver acted on behalf of Maria's will
```

Subject/source/beneficiary and Representation remain distinct.

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

## SAFE DEFERRED — legal/specialist representation validity

**Unresolved:** legal capacity, guardian/minor rules, clinical representation, jurisdiction/formality.  
**Why safe:** LifeOS explicitly claims no specialist universal validity.  
**Owner:** specialist/legal integration.  
**Trigger:** ordinary LifeOS Representation must itself determine regulated validity.  
**Tests:** CORE-03/08/12, MA-10/13/18, XCON-02.

## SAFE DEFERRED — represented Agreement / Consent validity

**Unresolved:** when representative assent/permission can count for another party.  
**Why safe:** actual Actor + represented party + action-specific basis stay explicit.  
**Owner:** Agreement/Consent + Authority/policy + specialist validity.  
**Trigger:** represented assent/permission cannot remain separate from personal Agreement/Consent.  
**Tests:** CORE-04/09, MA-05/06/10/13/17, XCON-02/04.

## SAFE DEFERRED — Version / material scope

**Unresolved:** exact material-version/scope persistence and carry-forward rules.  
**Why safe:** action/target/scope is mandatory semantically.  
**Owner:** Version + logical model.  
**Trigger:** system cannot determine whether Representation/Authority still applies after material change.  
**Tests:** CORE-02/09/10/13, MA-11/12, XCON-03.

## SAFE DEFERRED — multi-hop delegation / chain persistence

**Unresolved:** chain normalization, cycles, depth, revocation propagation.  
**Why safe:** re-delegation is not implied.  
**Owner:** security/logical model.  
**Trigger:** valid multi-hop use cases cannot preserve bounded attribution/Authority.  
**Tests:** CORE-02/09/10/13, MA-06/10/11/17, XCON-02/03.

## SAFE DEFERRED — Verification of representation basis

**Unresolved:** whether/how claimed mandates/delegations are verified.  
**Why safe:** claimed Representation != established Authority already fixed.  
**Owner:** Verification/Evidence/Authority review.  
**Trigger:** ordinary represented actions need a reusable verification state/process.  
**Tests:** CORE-04/09, MA-06/12/18, XCON-02.

## SAFE DEFERRED — Organization / group / collective representation

**Unresolved:** representing organizations/groups/collective Actors and their representatives.  
**Why safe:** current workflows work with native parties without universal Group identity.  
**Owner:** collective/Organization review.  
**Trigger:** ordinary workflows require persistent represented collective identity not decomposable to current referents.  
**Tests:** CORE-04/06, MA-01/02/05/13/19/20, XCON-01/04/05.

## SAFE DEFERRED — retention / audit / privacy

**Unresolved:** detailed retention/anonymization and security-audit storage.  
**Why safe:** historical attribution does not imply retaining all sensitive credentials/basis forever.  
**Owner:** privacy/retention/audit/security.  
**Trigger:** retention rules conflict with required action-time attribution.  
**Tests:** CORE-02/09/10, MA-07/08/11/13, XCON-03.

## SAFE DEFERRED — AI/service delegation chain

**Unresolved:** reusable AI/service principal, tool chain, sub-agent delegation and policy propagation.  
**Why safe:** current actual Actor/service + represented party + Authority boundary is sufficient semantically.  
**Owner:** AI/application/security architecture.  
**Trigger:** AI/tool chains cannot preserve actual semantic Actor and bounded Authority without generic Agent/Delegation root.  
**Tests:** CORE-02/04/10/13, MA-06/08/10/17, XCON-01/02/04.

## SAFE DEFERRED — exact persistence/cardinality/API

**Unresolved:** direct relation vs qualified record, typed references, cardinality, indexing.  
**Why safe:** semantic family and identity boundaries fixed.  
**Owner:** logical/persistence model.  
**Trigger:** semantic requirements cannot be represented without universal Agent/Principal/Relationship root.  
**Tests:** CORE-06/10/13, MA-01/10/19, XCON-01/04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 12. Hardest adversarial scenarios

| Scenario | Stress | Required result |
|---|---|---|
| assistant schedules for manager | actual Actor vs represented party | preserve both + bounded basis |
| caregiver records Person statement | source/Subject vs on-behalf-of | do not invent Representation unless actually acting for party |
| parent acts for child | unequal power | Authority may exist; child's will/Consent not fabricated |
| Actor claims mandate but has none | claim vs legitimacy | Representation claim may exist; effect not authoritative |
| delegation expires after valid action | historical Authority | past action remains reconstructible |
| B tries to re-delegate to C | transitivity | not allowed unless explicit basis |
| shared Account used by assistant | technical identity | do not rewrite semantic Actor if known |
| technical impersonation token | security mechanism | does not become domain actor truth |
| representative accepts Agreement terms | assent | represented party Agreement only under applicable action-specific basis; actual Actor retained |
| representative grants Consent | permission | does not silently become represented Person's personal Consent |
| representative makes Decision | decision attribution | actual decision Actor/process retained |
| AI acts under bounded policy | machine agency | AI/service remains actual Actor, not human author |
| visible result with private delegation basis | privacy | result Visibility != Representation/basis Visibility |

---

# 13. Reopening / dependency register

| Finding | Severity | Closure | Current treatment | Reopening trigger |
|---|---|---|---|---|
| actual Actor vs represented party | STRUCTURAL | RESOLVED | canonical Representation | stronger model proves full redundancy |
| Representation vs Authority | STRUCTURAL | RESOLVED | independent | ordinary workflows cannot preserve legitimacy separately |
| Principal domain primitive | STRUCTURAL | RESOLVED | rejected | domain semantics require security identity as native root |
| universal Delegation primitive | STRUCTURAL | RESOLVED | rejected | shared independent lifecycle/identity emerges across action families |
| technical impersonation | HARDENING | RESOLVED | security mechanism != attribution | implementation makes attribution impossible |
| re-delegation | HARDENING | RESOLVED | not implied | ordinary workflows require universal transitivity |
| represented Agreement/Consent | HARDENING | SAFE DEFERRED | preserve Actor/party/basis; validity later | action-specific basis cannot remain separate |
| Version/material scope | DEFERRED DEPENDENCY | SAFE DEFERRED | bounded scope required now | carry-forward cannot be determined |
| collective representation | DEFERRED DEPENDENCY | SAFE DEFERRED | no Group root | ordinary workflows require collective identity |
| retention/audit | DEFERRED DEPENDENCY | SAFE DEFERRED | history + minimization coexist semantically | retention destroys attribution correctness |
| AI/service delegation chains | DEFERRED DEPENDENCY | SAFE DEFERRED | actual Actor/service remains attributable | tool chains require new primitive |

---

# 14. Regression corpus additions

| ID | Scenario | Boundary |
|---|---|---|
| R-REP-01 | assistant uses own Account to schedule for manager | Account/Principal vs Actor/represented party/Authority |
| R-REP-02 | caregiver records a cared-for Person's report | Subject/source/recorder vs Representation |
| R-REP-03 | delegated Authority expires after valid represented action | action-time Authority/history |
| R-REP-04 | Actor attempts re-delegation without basis | delegation transitivity |
| R-REP-05 | representative responds/acknowledges/decides for another | actual Actor vs represented semantic action |
| R-REP-06 | representative attempts Agreement/Consent | represented will vs Authority/specialist validity |
| R-REP-07 | AI/service acts under bounded policy | machine Actor vs human authorship/Authority |
| R-REP-08 | result visible while delegation basis private | selective disclosure |
| R-REP-09 | technical impersonation/session switch | security identity vs domain attribution |

---

# 15. Concept-family verdict

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

# 20. Downstream closure — Version / Material-State v0 (2026-08-13)

Version / Material-State v0 resolves the historical `Version / material scope` SAFE DEFERRED item without reopening Representation.

A represented action remains bound to the material action/target/scope state actually acted against:

```text
R1:
actual Actor = Luca
represented party = Anna
target/action/scope state = S1

later material change -> S2
→ R1 remains historical attribution for S1
→ R1 is not silently rewritten as action against S2
```

The applicable Authority/delegation/policy basis may itself change materially over time. Version preserves/reconstructs the basis state used at action time; Authority/policy determines legitimacy/effect; Provenance explains how the basis/target state arose.

Materiality is action/scope specific. Technical storage/provider revisions, ETags/MVCC tokens, hashes or target-ID reuse do not by themselves determine represented-action applicability.

Downstream classification:

```text
Representation ↔ Version/material state           RESOLVED
Version ↔ Authority/Delegation/Principal           RESOLVED — not equal
Version ↔ Provenance                               RESOLVED — state vs lineage
Version ↔ Decision/Reconciliation                  RESOLVED — not equal
```

Still SAFE DEFERRED:

- exact Principal/AuthN/AuthZ model;
- technical impersonation mechanics;
- action-specific delegability/policy;
- legal/specialist representation validity;
- represented Agreement/Consent legal validity;
- multi-hop delegation persistence;
- Verification of representation basis;
- Organization/group/collective representation;
- retention/audit/privacy;
- AI/service delegation chains;
- exact persistence/cardinality/API.

AI/service represented actions inherit the stale-base guard: where consequence requires it, the system must preserve the material target/scope/Authority state it reasoned/acted against and re-evaluate if that state materially diverges before effect.

No Representation hardening failed. **Representation remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.
