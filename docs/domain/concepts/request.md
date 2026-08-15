# Request

**Status:** ACCEPTED v0 — PASS WITH HARDENING  
**Validated:** 2026-08-15  
**Cluster:** Relationships / Reasoning  
**Validation checkpoint:** `../checkpoints/proposal-request-v0-validation.md`

## Definition

> **Request is the contextual directed semantic act/capability through which an Actor asks one or more recipients for a bounded action, information, response, Decision, participation, permission or change without creating the requested responsibility, participation, permission, authority, effect or actual execution merely by asking.**

Request answers:

> **Who is asking whom for what bounded action, information, response or change, against which target/context, and under which material request state?**

Request is a reusable semantic family, not a universal entity/root/table, transport message or generic workflow state machine.

---

## 1. Core semantics

A Request has, where materially applicable:

- an actual requesting Actor;
- one or more intended recipients;
- a bounded requested action/information/response/change;
- a target/context/purpose;
- material request state/version where consequence/history matters;
- temporal applicability such as due/expiry/withdrawal where relevant;
- optional Representation/on-behalf-of attribution;
- independent Visibility and Authority context;
- optional relationship to Proposal, Responsibility, Participation, Decision, Consent, Criterion, Resource planning or another owning family.

A Request can exist even if:

- the recipient has no LifeOS Account;
- delivery has not yet occurred;
- nobody acknowledges it;
- it is rejected or ignored;
- the requested action never occurs;
- the requester lacks Authority to make the requested outcome mandatory/effective;
- the request later expires or is withdrawn.

---

## 2. Request vs Proposal

```text
Request
= directs an ask to recipient(s)

Proposal
= puts a materially specific candidate forward for consideration
```

A single real-world interaction may contain both semantics.

Example:

```text
"Would you take over this task?"

Request:
please respond / take action

Proposal:
candidate Responsibility hand-off A → B
```

The system must not force both into a universal `ProposalRequest` root where their differences matter.

---

## 3. Request vs communication transport

```text
Request != Message
Request != Notification
Request != HTTP/API request
Request != delivery
Request != view
```

A domain Request may be carried by message, notification, UI, external integration or conversation. Transport describes how it moved; Request describes what was semantically asked.

Useful sequence:

```text
Request created
!= delivered/displayed
!= seen
!= Acknowledgement
!= family-specific response
!= requested effect
!= Actual execution
```

Not every workflow requires every stage.

---

## 4. Request vs Acknowledgement

Acknowledgement means explicit taking-notice of the materially specific Request/target.

```text
Acknowledgement of Request
!= positive response
!= fulfillment
!= Agreement
!= Consent
!= Decision
```

Silence does not automatically mean acknowledgement, rejection or acceptance.

A response to a materially changed Request must not silently rely on Acknowledgement of an older materially different state.

---

## 5. Request vs Responsibility

```text
Request to take Responsibility
!= Responsibility transfer
```

Example:

```text
Responsibility = A
A requests B to take over
B sees request
B acknowledges request
Responsibility still = A
```

Only the applicable family-specific transfer/claim/Decision/Authority/policy semantics may establish the new Responsibility state.

Request may ask for a hand-off; it does not own the resulting Responsibility.

---

## 6. Request vs Participation

```text
Invitation / participation Request
!= Participation response
!= Actual Participation
```

A recipient can be invited/requested to participate without accepting, appearing or becoming a participant.

The Participation concept owns actual involvement and family-specific participation response/state.

---

## 7. Request vs Consent

```text
Request for Consent
!= Consent
```

Viewing, acknowledging or failing to reject a Request for Consent does not create Consent.

Consent remains actor-scoped bounded permission under defined scope/purpose/context where Consent is an applicable basis.

A high-pressure or high-authority context must not relabel compliance/silence as voluntary Consent automatically.

---

## 8. Request vs Authority

```text
Request != Authority
requester != Authority holder automatically
recipient != obligated merely because requested
```

A Request may be issued in a context where Authority independently makes compliance required, optional, reviewable or governed. The wording `please` does not determine Authority.

Conversely, a person may request something they have no Authority to require.

Authority/effect must therefore remain separately modeled.

---

## 9. Request vs Decision

A Request may ask for a Decision or be one input to a Decision.

```text
Request != Decision
```

A Decision resolving the Request does not erase the Request identity/history when that history is material.

A deterministic authorized policy may produce a bounded effect without fabricating a human Decision.

---

## 10. Request vs Actual / fulfillment

```text
requested action
!= Actual execution
```

A Request can be outstanding, declined, impossible, fulfilled partially, fulfilled by a different Actor where permitted, superseded or withdrawn.

Fulfillment/effect remains owned by the affected domain semantics:

- Responsibility owns accountability state;
- Participation owns involvement state;
- Schedule owns accepted temporal assignment;
- Consent owns bounded permission;
- Decision owns bounded resolution;
- Actual/Session/Outcome describe what happened;
- Resource allocation/reservation semantics remain separately reviewable.

Request does not become a universal `fulfilled=true` truth layer.

---

## 11. Withdrawal / expiry / supersession

Withdrawal or expiry changes future applicability of a Request; it does not erase history.

```text
withdraw Request
!= delete historical ask
```

If the requested action/effect already occurred legitimately:

```text
later withdrawal
!= automatic undo
```

Any reversal must be represented through the affected domain concept.

A materially changed Request must preserve Version/material-state applicability where earlier responses/acknowledgements/history matter.

---

## 12. Representation / on-behalf-of

A Request made on behalf of another party preserves:

```text
actual requesting Actor
+
represented party
+
Representation basis/context
```

The represented party must not silently replace the actual Actor as author where that would be false.

Representation does not automatically create Authority or the represented party's personal Acknowledgement, Consent, Agreement or Decision.

---

## 13. Multi-actor semantics

One Request may target one or several recipients while responses remain actor-scoped.

```text
one Request
!= one shared response
```

Recipients may independently:

- never receive it;
- see it;
- acknowledge it;
- decline;
- ask for clarification;
- counter-propose;
- fulfill different parts;
- lack Authority/capability;
- have private constraints not visible to the requester.

Group membership, relationship membership or shared context does not imply receipt, assent, obligation or fulfillment.

External/accountless recipients remain representable without synthetic Accounts.

---

## 14. Visibility / privacy

Request Visibility is independent from:

- target Visibility;
- recipient list Visibility;
- response Visibility;
- reason/constraint Visibility;
- requested information Visibility;
- Representation/delegation basis Visibility;
- resulting effective-state Visibility.

A requester may receive a bounded response/result without receiving private supporting context.

AI explanation must not leak private reasons merely because it had authorized context access.

---

## 15. AI boundary

AI may:

- draft a Request;
- suggest whom to ask;
- send/issue a Request under explicit applicable policy/Authority and truthful attribution;
- summarize responses;
- identify missing responses;
- prepare follow-up Requests.

AI may not fabricate:

```text
human Request authorship
human Acknowledgement
human Agreement
human Consent
human Decision
Authority
fulfillment
```

If an AI/system is the actual semantic requester, attribution must remain to that Actor where material rather than being laundered into human intent.

---

## 16. Request for information / Evidence

Requesting information does not fabricate the information or Evidence.

```text
information requested
!= information received
!= Observation / Evidence
```

A later response may produce information that becomes Evidence in an evaluation context, but Request does not own the truth/value of that information.

---

## 17. Resource planning boundary

```text
Request for a Resource/capability
!= Resource Requirement universally
!= Allocation
!= Reservation / Capacity Claim
!= Actual use
```

Some domain-specific Resource requests may later map to Resource Requirement/Allocation/Reservation semantics. Those concepts remain separately reviewable and are not absorbed into generic Request.

---

## 18. Persistence / scale guardrail

Request semantics do not require:

- a universal `requests` root/table;
- one durable record for every conversational ask;
- one generic request status enum;
- one cross-domain workflow engine;
- indefinite retention;
- one response object for all families.

Materialization is consequence-sensitive.

Persist/identify a Request when needed for targeting, history, deadlines, response correlation, governance, privacy, explanation, version binding or consequential fulfillment. Low-consequence transient asks may remain contextual.

---

## 19. Rejected alternatives

Rejected as universal kernel defaults:

```text
ProposalRequest common root
Interaction / Message root
Request = Responsibility
Request = Participation
Request = Authority
Request for Consent = Consent
Request = Decision
Request = Actual action
silence = acceptance
seen = acceptance
one universal Response root
one universal request state machine
HTTP/API request semantics as domain Request
```

---

## 20. Adjacent dependencies

Resolved at semantic boundary:

- Request vs Proposal;
- Request vs delivery/view;
- Request vs Acknowledgement;
- Request vs Responsibility;
- Request vs Participation;
- Request vs Authority;
- Request vs Consent;
- Request vs Decision;
- Request vs Actual/fulfillment;
- Request vs Version/material state;
- Request vs Representation;
- withdrawal/expiry/history;
- generic Acceptance root — rejected;
- generic Response root — rejected.

Still independently SAFE DEFERRED:

- Trigger / conditional policy;
- Resource Requirement / Allocation / Reservation;
- Verification / comprehension;
- collective / Group / quorum mechanics;
- specialist governed directive/order semantics;
- messaging / notification / delivery infrastructure;
- formal Contract/legal offer/signature validity;
- retention/audit/deletion;
- logical / physical / API representation.

---

## 21. Canonical invariants

```text
Request != Proposal
Request != Message / Notification / HTTP request
Request created != delivered != seen != acknowledged
Acknowledgement != positive response
Request != Responsibility
Request != Participation
Request != Authority
Request for Consent != Consent
Request != Decision
Request != Actual execution
silence != acceptance / rejection
withdrawal != historical deletion
withdrawal after fulfillment != automatic undo
one Request != one shared response
AI/system Request preserves actual attribution
```

Request v0 remains reopenable only if stronger workflow, specialist, multi-actor, history, privacy or implementation evidence proves these boundaries structurally insufficient.
