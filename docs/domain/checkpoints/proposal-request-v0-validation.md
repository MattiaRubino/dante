# Proposal / Request v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — hardenings incorporated; pending post-write propagation QA  
**Validated:** 2026-08-15  
**Concept / family:** Proposal / Request v0  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Validation standard:** `../validation-methodology-v3.md`  
**Branch:** `feature/domain-model`  
**Approved pre-scope:** `6b546e744e9010dd3e93eb46a2075deda3d2b460`

---

# 0. Fresh candidate re-score

Proposal / Request was selected only after Criterion / Evaluation v0 completed final post-write QA. The remaining Relationships / Reasoning candidate space was re-scored against the then-current accepted baseline; no old ranking was inherited as authority.

Current read-only pressure ranking at selection time:

```text
1  Proposal / Request reusable semantics                  24
2  Resource Requirement / Allocation / Reservation       21
3  Trigger / conditional policy                          19
4  Verification / comprehension                          15
5  Coordination Stewardship                              13
6  Dependency                                            12
7  Contribution                                          10
8  Collective / Group / quorum                            8
9  focus / context relations                              7
```

This ranking is not a roadmap. It is invalidated for next-candidate selection by every accepted downstream milestone and must be freshly re-scored again.

Proposal / Request received the strongest pressure because already accepted semantics repeatedly require the same boundary:

```text
proposed / requested
!= delivered / seen
!= acknowledged
!= family-specific response
!= agreed / consented / decided
!= effective target state
!= Actual
```

The pressure appears across Responsibility hand-off, Participation invitations, Acknowledgement, Decision/review, Agreement/Consent, Schedule changes, Criterion changes, Representation and AI proposals/requests.

---

# 1. Scope

Primary candidate questions:

1. Does LifeOS need reusable Proposal semantics beyond family-specific proposal fields/actions?
2. Does LifeOS need reusable Request semantics beyond family-specific ask/invitation/request fields/actions?
3. Are Proposal and Request one concept, two concepts, or merely Message/Interaction vocabulary?
4. What happens between creation, delivery, view, Acknowledgement, response, Agreement/Consent/Decision and effective state?
5. How do counter-proposals, withdrawal, expiry, material changes and history behave?
6. How are actual Actor, represented party, Authority, Visibility and AI attribution preserved?
7. Can these semantics remain lightweight without universal roots/tables/workflows?

Primary adjacent accepted concepts:

- Responsibility;
- Participation;
- Acknowledgement;
- Decision;
- Agreement;
- Consent;
- Authority;
- Representation;
- Version / Material-State;
- Criterion / Evaluation;
- Schedule;
- Actual / Outcome / Provenance / Visibility.

Secondary deferred pressure:

- Trigger / conditional policy;
- Resource Requirement / Allocation / Reservation;
- Verification / comprehension;
- collective / Group / quorum;
- specialist directive/order semantics;
- messaging / notification infrastructure;
- Contract/signature/legal validity;
- retention/audit/deletion;
- logical/physical/API representation.

---

# 2. Evidence reviewed

## EV-01 — Existing LifeOS evidence

Accepted LifeOS semantics already require:

```text
handoff request != effective Responsibility transfer
invitation != Participation response != Actual Participation
Acknowledgement != acceptance / Agreement / Consent / Decision
proposed terms != Agreement
request for Consent != Consent
Proposal != Decision/effective state
proposed Criterion != adopted/applicable Criterion
AI proposal != human intention / Decision
```

The same separation recurs across otherwise independent families. Keeping every instance entirely local would duplicate targeting, material-state, actor-attribution, response-correlation, withdrawal/expiry and history semantics.

**EV-01 result: PASS.**

## EV-02 — Workflow inversion

Representative real-world workflows were reconstructed before fitting concepts:

1. Responsibility hand-off request A → B;
2. Event invitation with no response;
3. Schedule change proposal and counter-proposal;
4. Request for Consent;
5. Agreement terms proposed to multiple parties;
6. Criterion change proposed after observing data;
7. information request with no answer;
8. external/accountless recipient;
9. withdrawal before effect;
10. withdrawal after an already-effective change;
11. AI-generated proposal;
12. Request made on behalf of another party;
13. shared Proposal with different actor responses;
14. Resource/capability request without allocation/reservation.

Recurring structure:

```text
semantic ask/candidate
!= communication transport
!= acknowledgement
!= response
!= effect
```

**EV-02 result: PASS.**

## EV-03 — Targeted external benchmark

External systems are evidence only and do not dictate LifeOS ontology.

### ActivityStreams 2.0 vocabulary

Relevant convergence:

- `Offer`/`Invite` are distinct semantic activities;
- later `Accept`, `Reject`, `TentativeAccept` and related activities remain distinct from the original offer/invite;
- the activity vocabulary demonstrates that proposal/invitation and response need not be one state on one object.

Classification: **ADAPT.**

LifeOS disposition:

- adopt semantic separation of candidate/request and response;
- do not import the ActivityStreams class hierarchy or generic Activity root.

Reference: W3C ActivityStreams 2.0 Vocabulary — `https://www.w3.org/TR/activitystreams-vocabulary/`.

### HL7 FHIR request pattern / ServiceRequest

Relevant convergence:

- request identity is distinct from requester, performer and target;
- status and intent are separate dimensions;
- intent differentiates proposal/plan/directive/order-like semantics;
- request lifecycle/history matters without collapsing requested action into performed action.

Classification: **ADAPT.**

LifeOS disposition:

- borrow separation of ask, actor roles, intent and execution/effect;
- do not import clinical status taxonomies, order semantics or FHIR resource hierarchy.

References:

- FHIR R5 ServiceRequest — `https://hl7.org/fhir/servicerequest.html`;
- FHIR Request pattern — `https://hl7.org/fhir/request.html`.

### HTTP request/response semantics

HTTP demonstrates a term collision rather than a domain model authority. Its `request` is protocol transport semantics.

Classification: **NOT APPLICABLE / anti-pattern if imported as domain meaning.**

LifeOS disposition:

```text
HTTP/API request != LifeOS domain Request
```

Reference: RFC 9110 — `https://www.rfc-editor.org/rfc/rfc9110.html`.

External convergence supports:

```text
candidate / ask
!= communication transport
!= response
!= performed/effective result
```

**EV-03 result: PASS WITH HARDENING.**

Hardening: never infer LifeOS Proposal/Request ontology from provider/protocol vocabulary alone.

## EV-04 — Smallest candidate

Destructive candidate comparison:

```text
H0: every family owns unrelated proposal/request semantics
FAIL
- repeated actor/recipient/target/version/history/withdrawal boundaries
- inconsistent response/effect targeting pressure

H1: universal Proposal root
FAIL
- directed asks need not put a candidate state/option forward

H2: universal Request root
FAIL
- proposals need not be asks directed toward required recipients/actions

H3: one ProposalRequest / Interaction / Message root
FAIL
- candidate semantics, directed ask semantics and transport are materially different

H4: contextual Proposal family
  + contextual Request family
  + no shared universal root/table/workflow
SURVIVES
```

**EV-04 result: PASS.**

---

# 3. Accepted candidate definitions

## Proposal

> **Proposal is the contextual semantic act/capability through which an Actor puts a materially specific candidate action, state, term set, rule, option or change forward for consideration without making that candidate effective merely by proposing it.**

Canonical question:

> **Who proposed what materially specific candidate, for whose consideration, against which target/context, and under which material proposal state?**

## Request

> **Request is the contextual directed semantic act/capability through which an Actor asks one or more recipients for a bounded action, information, response, Decision, participation, permission or change without creating the requested responsibility, participation, permission, authority, effect or actual execution merely by asking.**

Canonical question:

> **Who is asking whom for what bounded action, information, response or change, against which target/context, and under which material request state?**

## Non-collapse

```text
Proposal != Request
Proposal / Request != Message / Notification / transport
Proposal / Request != Acknowledgement
Proposal / Request != generic response
Proposal != Agreement / Decision / effective state
Request != Responsibility / Participation / Consent / Authority
requested action != Actual execution
```

---

# 4. Core Semantic Validation Gate

| Test | Applicable | Result | Finding / hardening |
|---|---:|---|---|
| CORE-01 Workflow inversion | yes | PASS | real workflows naturally separate candidate/ask/response/effect |
| CORE-02 Deep chronology | yes | PASS WITH HARDENING | preserve material proposal/request state, response targeting, withdrawal/expiry and later effect history |
| CORE-03 Reductio | yes | PASS WITH HARDENING | universal Proposal, Request, Interaction, Message, Acceptance and Response roots fail |
| CORE-04 Redundancy | yes | PASS WITH HARDENING | Proposal/Request remain distinct from Ack/Decision/Agreement/Consent/Responsibility/Participation |
| CORE-05 Traceability | yes | PASS | proposal/request can link to target and later effect without becoming it |
| CORE-06 Orphan/independence | yes | PASS WITH HARDENING | proposal/request may exist with no response/effect; low-consequence persistence is optional |
| CORE-07 External benchmark | yes | PASS | external convergence supports separation, not imported ontology |
| CORE-08 Anti-pattern review | yes | PASS | message-root, status-machine and generic acceptance/response defaults rejected |
| CORE-09 Correction/reconciliation/history | yes | PASS WITH HARDENING | counter-proposal, material edit, withdrawal, expiry and disagreement preserve history |
| CORE-10 Scale/performance | yes | PASS WITH HARDENING | no durable row required for every conversational suggestion/ask |
| CORE-11 Simple vs power user | yes | PASS | ordinary UI can use natural verbs without exposing ontology |
| CORE-12 Product value/complexity | yes | PASS WITH HARDENING | persist only when consequence/history/coordination value warrants it |
| CORE-13 Implementation pressure | yes | PASS WITH HARDENING | targeting/queryability/version correlation required; no SQL/API/state machine chosen |

```text
CORE GATE
PASS WITH HARDENING
```

## Core hardenings incorporated

```text
PRQ-H01 Proposal != Request
PRQ-H02 Proposal/Request != Message / Notification / transport
PRQ-H03 creation != delivery != view != Acknowledgement
PRQ-H04 Acknowledgement != positive response
PRQ-H05 Proposal != Agreement
PRQ-H06 Proposal != Decision
PRQ-H07 Proposal != effective state
PRQ-H08 Request != Responsibility
PRQ-H09 Request != Participation
PRQ-H10 Request != Authority
PRQ-H11 Request for Consent != Consent
PRQ-H12 asking != granting Authority / obligation automatically
PRQ-H13 silence != acceptance / rejection
PRQ-H14 response remains family-specific; no universal Acceptance primitive
PRQ-H15 fulfillment/effect remains owned by affected domain concept
PRQ-H16 requested action != Actual execution
PRQ-H17 materially changed target/request/proposal obeys Version applicability
PRQ-H18 prior Ack/response does not automatically carry to materially changed proposal/request
PRQ-H19 genuine counter-Proposal is distinct semantic act, not silent mutation
PRQ-H20 withdrawal/expiry changes future applicability without erasing history
PRQ-H21 withdrawal after effect does not automatically undo effect
PRQ-H22 proposer/requester/recipient/responsible actor/performer/subject may differ
PRQ-H23 Representation preserves actual Actor + represented party
PRQ-H24 Account is not required
PRQ-H25 Visibility of proposal/request/content/history is independently governed
PRQ-H26 AI proposal != human intention/Decision
PRQ-H27 AI/system Request preserves actual attribution
PRQ-H28 persistence is consequence-sensitive
PRQ-H29 no universal Proposal/Request root/table/state machine
PRQ-H30 wording alone does not determine Authority/effect
```

---

# 5. Deep chronology regressions

## Schedule proposal / counter-proposal

```text
T0 Schedule = 14:00
T1 A creates Proposal P1: 16:00?
T2 B receives P1; Schedule remains 14:00
T3 B acknowledges P1; still no Agreement/Decision/effect
T4 B creates counter-Proposal P2: 17:00?
T5 applicable Agreement/Decision/Authority/policy resolves P2
T6 Schedule becomes 17:00
T7 P1, P2, responses and basis remain reconstructible where material
```

Result: **PASS WITH HARDENING.**

## Responsibility hand-off Request

```text
Responsibility = A
A Requests B to take over
B sees Request
B acknowledges Request
Responsibility remains A

applicable hand-off response/effect
+ Authority/policy
→ Responsibility = B
```

Result: **PASS.**

## Withdrawal after effect

```text
Request/Proposal created
→ applicable effect becomes current
→ later Proposal/Request withdrawn
```

Withdrawal does not retroactively undo the already-effective state. Reversal remains owned by the affected domain concept.

Result: **PASS WITH HARDENING.**

---

# 6. Multi-Actor Compatibility Gate

| Test | Applicable | Result | Finding / hardening |
|---|---:|---|---|
| MA-01 Identity/account independence | yes | PASS | external/accountless recipients remain representable |
| MA-02 Shared fact/actor overlay | yes | PASS WITH HARDENING | one shared Proposal/Request may have actor-scoped responses |
| MA-03 Responsibility/assignment/claim | yes | PASS WITH HARDENING | Request for hand-off != Responsibility effect |
| MA-04 Stewardship/mental load | yes | PASS WITH PRODUCT HARDENING | reminders/escalations must not create coordination burden by default |
| MA-05 Common ground/state separation | yes | PASS WITH HARDENING | Ack/response/Agreement/Consent/Decision remain distinct |
| MA-06 Authority/canonical change | yes | PASS WITH HARDENING | requester/proposer != Authority holder/effect owner automatically |
| MA-07 Selective disclosure | yes | PASS WITH HARDENING | content, recipient, response, rationale and effect visibility separate |
| MA-08 Inference privacy | yes | PASS WITH HARDENING | AI explanations cannot leak hidden proposal/request basis |
| MA-09 Partial adoption/external participant | yes | PASS | no synthetic Account required |
| MA-10 Assisted participation/Representation | yes | PASS WITH HARDENING | actual Actor + represented party preserved |
| MA-11 lifecycle/revocation | yes | PASS WITH HARDENING | withdrawal/revocation changes future applicability; history survives where policy permits |
| MA-12 conflict/adversarial relation | yes | PASS WITH HARDENING | different responses/counter-proposals may coexist |
| MA-13 unequal power | yes | PASS WITH HARDENING | request from powerful Actor != voluntary Consent; wording does not erase Authority context |
| MA-14 multi-resource/capacity | limited | PASS | Resource request != allocation/reservation/capacity truth |
| MA-15 coordination-burden distribution | yes | PASS WITH PRODUCT HARDENING | requester/recipient/reviewer/beneficiary burdens must be explicit |
| MA-16 formality/progressive disclosure | yes | PASS | low-risk asks stay lightweight; consequential workflows remain auditable |
| MA-17 AI authority/multi-party context | yes | PASS WITH HARDENING | AI proposal/request attribution and bounded Authority preserved |
| MA-18 specialist-system boundary | yes | PASS | directive/order semantics remain specialist extensions |
| MA-19 multi-actor primitive redundancy | yes | PASS | no SharedProposal/SharedRequest/GenericResponse primitive needed |
| MA-20 actor-scoped reality attribution | yes | PASS WITH HARDENING | shared target/effect does not imply identical actor response/history |

```text
MULTI-ACTOR GATE
PASS WITH HARDENING
```

## Key multi-actor guardrails

```text
one shared Proposal != one shared response
one Request to many recipients != one collective response
group membership != Agreement / Consent / obligation
request from powerful Actor != voluntary Consent
represented proposal/request != represented party authorship
AI proposal != human proposal
AI request != human request when AI is actual semantic Actor
```

---

# 7. Cross-Concept Consistency Gate

| Test | Result | Notes |
|---|---|---|
| XCON-01 Identity | PASS WITH HARDENING | Proposal/Request identity separate from target/effect and each other |
| XCON-02 Authority | PASS WITH HARDENING | asking/proposing does not create governance power/effect |
| XCON-03 planned/current/Actual/history | PASS WITH HARDENING | requested/proposed != current/effective != Actual; history preserved |
| XCON-04 Relationship | PASS | specific typed relationships; no generic Relationship root required |
| XCON-05 Multi-Actor | PASS WITH HARDENING | shared ask/candidate + actor-scoped responses/privacy survive |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Proposal and Request promoted; generic Acceptance/Response remain rejected |

```text
XCON GATE
PASS WITH HARDENING
```

No accepted concept is structurally reopened.

---

# 8. Adjacent Dependency Sweep

Every material neighbor is classified.

## RESOLVED

```text
Proposal ↔ Request
Proposal ↔ Acknowledgement
Proposal ↔ Agreement
Proposal ↔ Consent
Proposal ↔ Decision
Proposal ↔ Authority
Proposal ↔ Version/material state
Proposal ↔ Representation
Proposal ↔ effective state
Request ↔ delivery/view
Request ↔ Acknowledgement
Request ↔ Responsibility
Request ↔ Participation
Request ↔ Authority
Request ↔ Consent
Request ↔ Decision
Request ↔ Actual/fulfillment
Request ↔ Version/material state
Request ↔ Representation
counter-Proposal identity
withdrawal / expiry history
generic Acceptance primitive → REJECTED
generic Response root → REJECTED
ProposalRequest common root → REJECTED
```

## SAFE DEFERRED

### Trigger / conditional policy

**Why safe:** Proposal/Request can exist and be answered/effected without defining generic fact-driven automation/action semantics.  
**Owner:** Trigger/automation/policy review.  
**Reopening trigger:** ordinary Proposal/Request workflows cannot model expiry/escalation/conditional effect without embedding generic trigger logic inside Proposal/Request.  
**Tests:** CORE-03/04/09/13, MA-06/17, XCON-02/04.

### Resource Requirement / Allocation / Reservation

**Why safe:** asking for a resource/capability does not determine requirement structure, allocation, reservation or actual use.  
**Owner:** Resource planning review.  
**Reopening trigger:** common Resource workflows require Request to own candidate/allocation/reservation state.  
**Tests:** CORE-03/04/05/13, MA-14, XCON-03/04.

### Verification / comprehension

**Why safe:** checking truth/understanding remains distinct from asking/proposing/responding.  
**Owner:** Verification/Evidence review.  
**Reopening trigger:** consequential proposal/request response validity cannot be represented without folding Verification into these concepts.  
**Tests:** CORE-03/04/09, MA-05/13/18, XCON-04.

### Collective / Group / quorum

**Why safe:** one Proposal/Request may target multiple native parties while responses remain actor-scoped; no Group/quorum root is necessary yet.  
**Owner:** collective/group review.  
**Reopening trigger:** ordinary workflows require one collective responder/decision/quorum identity that cannot be reconstructed from native parties and existing Agreement/Decision semantics.  
**Tests:** CORE-04/06/12, MA-02/05/06/19/20, XCON-01/04/05.

### Specialist directive/order semantics

**Why safe:** regulated command/order semantics may extend Request/Authority without becoming universal LifeOS behavior.  
**Owner:** specialist domain/extensions.  
**Reopening trigger:** multiple ordinary non-specialist domains require a shared directive/order lifecycle not representable by Request + Authority + affected state.  
**Tests:** CORE-07/08/12/13, MA-13/18, XCON-02.

### Messaging / notification / delivery infrastructure

**Why safe:** communication transport is explicitly distinct from domain ask/candidate semantics.  
**Owner:** messaging/integration/application architecture.  
**Reopening trigger:** domain correctness requires Proposal/Request to own transport delivery/read mechanics universally.  
**Tests:** CORE-03/04/10/13, MA-07/09, XCON-04.

### Formal offer / Contract / signature / legal validity

**Why safe:** LifeOS Proposal is not a universal legal offer and Request is not a universal legal demand.  
**Owner:** specialist/legal/document integration.  
**Reopening trigger:** ordinary product semantics require legal formation/signature/capacity as core Proposal/Request identity.  
**Tests:** CORE-07/08/12, MA-13/18, XCON-02/04.

### Retention / audit / deletion

**Why safe:** historical explainability does not imply indefinite retention of all content.  
**Owner:** privacy/retention/audit.  
**Reopening trigger:** deletion/minimization makes required targeting/effect history impossible.  
**Tests:** CORE-02/09/10, MA-07/11, XCON-03/05.

### Logical / physical / API representation

**Why safe:** semantic identity/boundaries are fixed without choosing tables, cardinalities or generic endpoints.  
**Owner:** logical/physical/API modeling.  
**Reopening trigger:** no implementation can preserve targeting, version, history, privacy and performance without changing semantics.  
**Tests:** CORE-10/13, XCON-01/03/05.

```text
REOPEN                         0
unclassified material items    0
```

---

# 9. Adversarial scenario log

| Scenario | Stress | Result |
|---|---|---|
| invitation sent + silence | Request vs Participation | PASS — no Participation fabricated |
| Consent requested + seen | Request vs Consent | PASS — no Consent fabricated |
| hand-off requested + Ack | Request vs Responsibility | PASS — no transfer fabricated |
| Proposal accepted by only one required party | Proposal vs Agreement | PASS — no Agreement fabricated |
| AI proposes new Goal Criterion | AI vs human intention | PASS WITH HARDENING — no automatic adoption |
| manager writes “please do this” | wording vs Authority | PASS WITH HARDENING — wording does not define governance |
| counter-proposal | identity/history | PASS — distinct Proposal linked to predecessor |
| Request withdrawn after action already happened | withdrawal vs effect | PASS — no retroactive erasure |
| Resource requested | Request vs allocation | PASS — no Allocation/Reservation fabricated |
| information requested but never received | Request vs Evidence | PASS — no information/Evidence fabricated |
| external recipient without Account | partial adoption | PASS |
| one shared Proposal, different responses | actor-scoped state | PASS WITH HARDENING |
| represented Request | attribution | PASS WITH HARDENING — actual Actor preserved |

---

# 10. Reopening / dependency register

| Finding | Class | Closure | Current treatment |
|---|---|---|---|
| Proposal vs Request | STRUCTURAL | RESOLVED | distinct contextual families, no common root |
| proposal/request vs response/effect | STRUCTURAL | RESOLVED | response family-specific; affected concept owns effect |
| Ack vs positive response | STRUCTURAL | RESOLVED | Acknowledgement remains taking-notice only |
| material edit/history | HARDENING | RESOLVED | Version/material applicability + counter-Proposal identity |
| withdrawal/expiry | HARDENING | RESOLVED | future applicability changes; history/effect not erased |
| Authority wording/power | HARDENING | RESOLVED | Authority independent from ask/candidate wording |
| AI attribution | HARDENING | RESOLVED | actual AI/system Actor preserved where material |
| Trigger automation | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| resource planning | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| Verification | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| collective/quorum | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| messaging transport | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| legal/specialist offer/order | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |
| retention/logical/API | DEFERRED DEPENDENCY | SAFE DEFERRED | separate owner/trigger/tests |

---

# 11. Verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

```text
PROPOSAL / REQUEST v0
PASS WITH HARDENING

Proposal
✅ canonical contextual semantic family/capability
✅ materially targetable/version-aware where consequence requires
❌ universal root/table/workflow

Request
✅ canonical contextual directed semantic family/capability
✅ reusable across bounded asks
❌ Responsibility
❌ Participation
❌ Authority
❌ Consent
❌ effect
❌ universal root/table/workflow

ProposalRequest common root
❌ REJECTED

Generic Acceptance
❌ REJECTED

Generic Response root
❌ REJECTED

REOPEN        0
UNCLASSIFIED  0
```

All mandatory hardenings are incorporated into `../concepts/proposal.md` and `../concepts/request.md` before acceptance.

Relationships / Reasoning candidate space remains open. This verdict does not authorize Cluster-5 integration and does not preselect the next candidate.

---

# 12. Regression corpus additions

```text
R-PRQ-01 invitation + silence → no Participation
R-PRQ-02 Consent Request + seen → no Consent
R-PRQ-03 Responsibility hand-off Request + Ack → no transfer
R-PRQ-04 one-party assent to Proposal → no multi-party Agreement
R-PRQ-05 AI Criterion Proposal → no human adoption
R-PRQ-06 high-authority Actor uses polite wording → Authority independent
R-PRQ-07 counter-Proposal → distinct Proposal/history
R-PRQ-08 Request withdrawal after Actual effect → no rollback
R-PRQ-09 Resource Request → no Allocation/Reservation
R-PRQ-10 information Request without answer → no Evidence
R-PRQ-11 represented Proposal/Request → actual Actor preserved
R-PRQ-12 one shared Proposal/Request + different actor responses
```

---

# 13. Documentation propagation scope

Approved pre-scope:

```text
6b546e744e9010dd3e93eb46a2075deda3d2b460
```

Approved exact scope:

## CREATE — 3

```text
docs/domain/concepts/proposal.md
docs/domain/concepts/request.md
docs/domain/checkpoints/proposal-request-v0-validation.md
```

## UPDATE — 27

```text
docs/domain/concepts/responsibility.md
docs/domain/checkpoints/responsibility-v0-validation.md
docs/domain/concepts/participation.md
docs/domain/checkpoints/participation-v0-validation.md
docs/domain/concepts/acknowledgement.md
docs/domain/checkpoints/acknowledgement-v0-validation.md
docs/domain/concepts/decision.md
docs/domain/checkpoints/decision-v0-validation.md
docs/domain/concepts/agreement.md
docs/domain/concepts/consent.md
docs/domain/checkpoints/agreement-consent-v0-validation.md
docs/domain/concepts/authority.md
docs/domain/checkpoints/authority-v0-validation.md
docs/domain/concepts/representation.md
docs/domain/checkpoints/representation-delegation-principal-v0-validation.md
docs/domain/concepts/criterion-evaluation.md
docs/domain/checkpoints/criterion-evaluation-v0-validation.md
docs/domain/concepts/version.md
docs/domain/checkpoints/version-material-equivalence-v0-validation.md
docs/domain/concepts/schedule.md
docs/domain/checkpoints/time-v0.md
docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md
docs/domain/checkpoints/cross-cluster-validation-v4.md
docs/domain/multi-actor-readiness-v1-part-3.md
docs/domain/language-map-part-5.md
docs/domain/README-part-3.md
docs/workstreams/domain-model-part-2.md
```

## DELETE — 0

Propagation discipline:

> Historical checkpoints remain evidence. Existing reasoning, rejected alternatives, scenarios, prior SAFE DEFERRED classifications and earlier QA records are preserved; later Proposal / Request amendments state downstream resolution without pretending the dependency was already closed at the earlier validation time.

Explicitly out of scope:

```text
main
main synchronization
backend
SQL / migrations
API
auth / Principal implementation
prototype / frontend
logical / physical model
Trigger / conditional policy
Resource Requirement / Allocation / Reservation
Verification / comprehension
collective / Group / quorum
generic Response primitive
generic Acceptance primitive
messaging / notification infrastructure
formal Contract / legal-offer engine
specialist order/directive model
next candidate selection
historical-record deletion/rewrite
docs/domain/concepts/relationship.md
```

---

# 14. Post-write QA requirements

Proposal / Request v0 is semantically accepted but propagation is not QA-closed until the exact approved scope is written and remotely verified against the pre-scope.

Required path QA:

```text
branch = feature/domain-model
pre-scope = 6b546e744e9010dd3e93eb46a2075deda3d2b460
exact changed paths = 30 / 30
CREATE = 3 / 3
UPDATE = 27 / 27
DELETE = 0
out-of-scope paths = 0
```

Required semantic/document QA:

- Proposal and Request concepts complete;
- EV-01..04 present;
- CORE-01..13 complete;
- MA-01..20 complete;
- XCON-01..06 complete;
- Adjacent Dependency Sweep complete;
- every SAFE DEFERRED item has owner + exact reopening trigger + tests;
- adversarial/reopening/regression sections complete;
- hardenings incorporated;
- `REOPEN = 0`;
- unclassified material dependencies = 0;
- Proposal != Request preserved;
- generic Acceptance/Response roots remain rejected;
- Responsibility/Participation/Consent/Authority/effective-state ownership preserved;
- Version/history/Representation/Visibility/AI boundaries preserved;
- historical checkpoint content preserved with downstream amendments;
- Language Map/README/Multi-Actor/workstream current state coherent;
- no `docs/domain/concepts/relationship.md` created;
- no next candidate preselected;
- `main`, backend, SQL/API/auth and prototype untouched.

Only after those checks pass may this checkpoint be marked `post-write propagation QA PASS` through a separately truthful closure if the marker itself requires a later write.
