# Proposal

**Status:** ACCEPTED v0 — PASS WITH HARDENING  
**Validated:** 2026-08-15  
**Cluster:** Relationships / Reasoning  
**Validation checkpoint:** `../checkpoints/proposal-request-v0-validation.md`

## Definition

> **Proposal is the contextual semantic act/capability through which an Actor puts a materially specific candidate action, state, term set, rule, option or change forward for consideration without making that candidate effective merely by proposing it.**

Proposal answers:

> **Who proposed what materially specific candidate, for whose consideration, against which target/context, and under which material proposal state?**

Proposal is intentionally not a universal entity/root/table or a generic interaction/message abstraction. It is a reusable semantic family that may be represented directly, qualified through an owning family, or materialized when identity/history/consequence requires it.

---

## 1. Core semantics

A Proposal has, where materially applicable:

- an actual proposing Actor;
- the candidate being proposed;
- a bounded target/context/purpose;
- intended consideration recipient(s) or decision/common-ground context;
- material proposal state/version where history matters;
- temporal applicability such as creation/effective proposal window/expiry where relevant;
- optional Representation/on-behalf-of attribution;
- independent Visibility and Authority context;
- optional relationship to an earlier Proposal, Request, Decision or affected target state.

The candidate may concern:

- a Responsibility hand-off;
- Participation/invitation terms;
- a Schedule or temporal change;
- Agreement terms;
- Consent scope/purpose terms;
- a Decision option;
- a Criterion change;
- an allocation/resource choice;
- another domain-specific state or action.

Proposal does not require every such family to expose the word `Proposal` in UI or persistence.

---

## 2. Identity and history

Proposal identity matters when the proposal itself has material lifecycle/history: it may be seen, acknowledged, answered, countered, withdrawn, expire, be compared, be accepted through a family-specific operation, or later explain why a target changed.

Canonical rules:

```text
Proposal identity
!= candidate target identity
!= candidate effective state
!= Decision
!= Agreement
!= Request
```

A materially changed proposal does not silently inherit responses/acknowledgements from the prior material proposal state unless an explicit applicable policy establishes equivalence.

A genuine counter-proposal is normally a distinct Proposal because it is a new semantic act and candidate from an Actor, even when it references or derives from an earlier Proposal.

```text
Proposal P1
→ counter-Proposal P2

P2 != P1 merely because both concern the same target
```

Version/material-equivalence discipline determines whether an edit remains the same material Proposal state or becomes a materially changed state for a particular purpose; it does not manufacture agreement or effect.

---

## 3. Proposal vs Request

Proposal and Request are neighboring but distinct semantic families.

```text
Proposal
= puts a candidate forward for consideration

Request
= directs an ask toward one or more recipients for action/information/response/change
```

Examples:

```text
"How about 17:00 instead?"
→ Proposal

"Please move the meeting to 17:00."
→ Request

"Would you take over this responsibility?"
→ may contain both a Request for response/action and a proposed hand-off candidate
```

The kernel must preserve the distinction where it matters rather than force both into one `ProposalRequest` root.

---

## 4. Proposal is not communication transport

```text
Proposal != Message
Proposal != Notification
Proposal != delivery
Proposal != display/view
```

A Proposal may be communicated through a message, UI surface, notification, external system or conversation, but transport does not define the domain meaning.

A Proposal can exist before delivery. Delivery can occur without Acknowledgement. Acknowledgement can occur without Agreement or Decision.

Useful sequence:

```text
Proposal created
!= delivered/displayed
!= seen
!= Acknowledgement
!= family-specific response
!= Agreement / Consent / Decision
!= effective target state
!= Actual
```

Not every workflow uses every stage.

---

## 5. Proposal vs Acknowledgement

Acknowledgement means explicit actor-scoped taking-notice of a materially specific target/request/change.

```text
Acknowledgement of Proposal P
!= acceptance of P
!= Agreement to P
!= Decision selecting P
```

Silence does not automatically mean Acknowledgement, acceptance or rejection.

A later material Proposal change does not automatically inherit an earlier Acknowledgement.

---

## 6. Proposal vs Agreement / Consent

```text
Proposal != Agreement
Proposal != Consent
```

Agreement requires the applicable parties to mutually assent to materially same terms/version. A Proposal can exist with zero, one or many responses and may never become Agreement.

A Proposal concerning Consent does not itself grant Consent. Consent remains actor-scoped bounded permission under applicable scope/purpose/context.

```text
proposed terms
→ individual responses
→ Agreement only if its own conditions are satisfied
```

---

## 7. Proposal vs Decision / effect

```text
Proposal != Decision
Proposal != effective target state
```

A Decision may select/reject/modify a Proposal, but Proposal identity remains historical evidence of what was considered.

An applicable policy may also produce an effect without fabricating a human Decision; the affected domain concept owns the resulting effective/current state.

Example:

```text
Schedule = 14:00
A proposes 16:00
B counter-proposes 17:00
applicable resolution establishes 17:00
Schedule = 17:00
```

The Proposal objects/states do not become the Schedule itself.

---

## 8. Withdrawal and expiry

Withdrawal or expiry changes future applicability of a Proposal; it does not erase truthful history.

```text
withdraw Proposal
!= erase that it was proposed
```

If an affected state already became effective through applicable Agreement/Decision/Authority/policy, later withdrawal of the Proposal does not automatically undo that state.

```text
Proposal led to effective state
→ later Proposal withdrawal
→ no automatic rollback
```

Any rollback/change must be represented through the owning domain semantics.

---

## 9. Authority

Proposal and Authority are independent.

```text
may propose
!= may make effective

proposal creator
!= Authority holder automatically
```

A high-authority Actor may issue something phrased politely as a proposal, but wording alone does not determine governance effect. Conversely, proposing an option does not create Authority.

LifeOS must preserve the actual Authority/policy context separately from the Proposal.

---

## 10. Representation / on-behalf-of

A Proposal made on behalf of another party preserves:

```text
actual proposing Actor
+
represented party
+
Representation basis/context
```

It must not rewrite the represented party as the actual proposer where that would be false.

Representation does not by itself create Authority, Agreement, Consent or Decision.

---

## 11. Multi-actor semantics

One shared Proposal may have different actor-scoped responses.

```text
one Proposal
!= one shared response
!= group Agreement
```

Group membership, Participation, Responsibility or relationship membership does not imply assent to a Proposal.

Different Actors may:

- not receive it;
- see it but not acknowledge it;
- acknowledge it without responding positively;
- reject it;
- counter-propose;
- agree under the relevant family;
- lack Authority to make the resulting state effective.

These differences must remain representable without duplicating the shared Proposal as one object per user.

---

## 12. Visibility / privacy

Proposal Visibility is independent from:

- candidate target Visibility;
- response Visibility;
- Decision rationale Visibility;
- underlying Evidence Visibility;
- Representation/delegation basis Visibility;
- resulting effective-state Visibility.

A bounded result may be visible without exposing private proposal rationale or source context.

AI-generated explanations must not leak hidden proposal context merely because the AI had authorized access to it.

---

## 13. AI boundary

AI may:

- generate candidate proposals;
- compare proposals;
- summarize trade-offs;
- suggest counter-proposals;
- prepare a proposal for human review;
- submit a Proposal where applicable Authority/policy permits and attribution remains truthful.

AI may not silently manufacture:

```text
human Proposal authorship
human Agreement
human Consent
human Decision
human Acknowledgement
Authority
```

Canonical rule:

> **AI proposal != human intention or human proposal unless the human actually performs the applicable semantic act.**

---

## 14. Persistence / scale guardrail

Proposal semantics do not require:

- a universal `proposals` root/table;
- one row for every conversational suggestion;
- a universal proposal state machine;
- event sourcing;
- mandatory immutable snapshots for every edit;
- one generic proposal graph spanning every specialist domain.

Materialization is consequence-sensitive.

Persist/identify Proposal state when needed for history, review, response targeting, version binding, auditability, privacy/governance or later explanation. Low-consequence transient suggestions may remain contextual/derived.

---

## 15. Rejected alternatives

Rejected as universal kernel defaults:

```text
ProposalRequest common root
Interaction root
Message as domain Proposal
Proposal = Decision
Proposal = Agreement
Proposal = effective state
Proposal = generic workflow item
one universal proposal lifecycle/status enum
AI-generated candidate = human Proposal
latest Proposal automatically wins
```

---

## 16. Adjacent dependencies

Resolved at semantic boundary:

- Proposal vs Request;
- Proposal vs Acknowledgement;
- Proposal vs Agreement;
- Proposal vs Consent;
- Proposal vs Decision;
- Proposal vs Authority;
- Proposal vs Version/material state;
- Proposal vs Representation;
- Proposal vs effective state;
- counter-Proposal identity;
- withdrawal/expiry history.

Still independently SAFE DEFERRED:

- Trigger / conditional policy;
- Resource Requirement / Allocation / Reservation;
- Verification / comprehension;
- collective / Group / quorum mechanics;
- specialist governed directive/order semantics;
- messaging / notification / delivery infrastructure;
- formal offer / Contract / signature / legal validity;
- retention/audit/deletion policy;
- logical / physical / API representation.

---

## 17. Canonical invariants

```text
Proposal != Request
Proposal != Message / Notification
Proposal != Acknowledgement
Proposal != Agreement
Proposal != Consent
Proposal != Decision
Proposal != Authority
Proposal != effective target state
Proposal != Actual
counter-Proposal != silent mutation
withdrawal != historical deletion
withdrawal after effect != automatic rollback
one Proposal != one shared response
AI proposal != human intention
```

Proposal v0 remains reopenable only if stronger workflow, specialist, multi-actor, history, privacy or implementation evidence proves these boundaries structurally insufficient.
