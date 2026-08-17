<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" part="6" -->
> **Canonical continuation — Part 6.** This file continues the existing Language Map as the same logical canonical document. Parts 1–5 remain preserved historical/current payload; this continuation records the accepted Proposal / Request vocabulary and boundaries. Physical split count does not increase the logical-document count.

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 2026-08-15 — Proposal / Request language-map amendment

## Canonical terms

### Proposal

Use **Proposal** for a contextual semantic act/state in which an Actor puts forward a materially specific candidate action, state, terms, rule, option or change for consideration without making it effective merely by proposing it.

Canonical question:

> Who proposed what materially specific candidate, for whose consideration, against which target/context?

Preferred role language where useful:

- proposer;
- proposed target/candidate;
- recipient / consideration audience;
- proposed-by;
- counter-proposal for a genuinely distinct later Proposal.

Do not use Proposal as a synonym for:

- Request;
- Message/Notification;
- Acknowledgement;
- Agreement;
- Decision;
- Consent;
- effective/current state;
- Actual.

### Request

Use **Request** for a contextual directed semantic act/state in which an Actor asks one or more Actors/systems for a bounded action, information, response, Decision, participation, permission or change without itself creating the requested semantic result.

Canonical question:

> Who is asking whom for what bounded action / information / response / change, against which target/context?

Preferred role language where useful:

- requester;
- recipient / requested actor/system;
- requested action/information/response/change;
- requested-by / requested-from.

Do not use Request as a synonym for:

- Responsibility;
- Participation;
- Authority;
- Consent;
- Decision;
- effective/current state;
- Actual execution.

## Mandatory non-collapse map

```text
Proposal != Request
Proposal / Request != Message / Notification
created != delivered != displayed/viewed
viewed != Acknowledgement
Acknowledgement != positive response
Proposal != Agreement
Proposal != Decision
Proposal != effective state
Request != Responsibility
Request != Participation
Request != Authority
Request for Consent != Consent
requested action != Actual execution
silence != acceptance / rejection
```

## Response vocabulary

Do not introduce a universal `Acceptance`, `Assent` or `Response` primitive merely to make Proposal/Request look symmetrical.

Use the semantic family that actually occurred:

- Acknowledgement when notice was explicitly taken;
- Participation response when participation semantics are at issue;
- Decision when a bounded question is resolved;
- Agreement when multiple parties mutually assent to materially same terms;
- Consent when bounded permission is granted;
- Responsibility transition when accountability actually changes;
- affected-domain state when the requested/proposed change actually becomes effective.

## Version / history vocabulary

A materially changed Proposal or Request is not silently the same semantic target for prior responses merely because the UI displays it in one thread.

Use material-state-aware language where consequence requires it:

```text
proposal/request identity
+
material state/version concerned
+
actor-scoped response/acknowledgement
```

A real counter-proposal is a distinct Proposal. Withdrawal/expiry changes future applicability without erasing historical truth.

## Actor / representation vocabulary

Keep these roles independently nameable:

```text
proposer
requester
recipient
responsible Actor
participant
actual performer
Subject
represented party
Authority holder
```

They may coincide in simple personal flows but are not synonyms.

Representation preserves the actual Actor and distinct represented party. Account is not required for semantic participation in Proposal/Request flows.

## AI/system language

Prefer truthful attribution:

- `AI proposed ...` when the AI/system is the actual proposer;
- `AI requested ...` when it is the actual requesting Actor/system under applicable policy;
- `AI suggested ...` for product-language suggestion where no durable Proposal semantic act is intended.

Never phrase an AI Proposal as the user's Decision, intention, Agreement or Consent unless the user actually established that state through the applicable semantics.

## Rejected universal nouns

Do not canonize these as generic domain roots from Proposal / Request v0:

```text
ProposalRequest
Interaction
Message
Generic Acceptance
Generic Response
```

Transport/message/event-envelope terminology may exist later in infrastructure, but it is not the canonical domain meaning of Proposal or Request.

Normative references:

- `concepts/proposal.md`;
- `concepts/request.md`;
- `checkpoints/proposal-request-v0-validation.md` and canonical continuation parts.
