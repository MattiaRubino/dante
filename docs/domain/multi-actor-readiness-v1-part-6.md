<!-- LIFEOS-CANONICAL-CONTINUATION document="multi-actor-readiness-v1.md" follows="multi-actor-readiness-v1-part-5.md" -->
> **Canonical continuation of Multi-Actor Readiness v1.** Earlier multi-actor findings remain unchanged; this part records Conditional Policy / Trigger integration only.

# 2026-08-15 — Conditional Policy / Trigger multi-actor hardening

Conditional Policy v0 adds reusable conditional-response semantics without changing the accepted shared-reality / actor-overlay model.

## Shared fact + actor-scoped policy

```text
shared Event / Activity / Plan / other canonical fact
+
Actor-specific Conditional Policy
```

is preferred to duplicating the shared fact per Actor.

Example:

```text
shared Event
Dinner 20:00

Actor A policy
30 min before → remind A

Actor B policy
no reminder
```

The Event remains one shared Event.

## Shared policy does not imply shared assent or control

```text
shared Conditional Policy
!= every Actor agrees with it
!= every Actor may edit/revoke it
!= every Actor may see all private basis/evidence
!= every Actor has Authority over resulting effects
```

Agreement, Consent, Acknowledgement, Authority and Visibility remain separately owned.

## Private activation basis

A private fact/Observation/Evaluation may support a bounded result without disclosing its private rationale.

```text
private recovery/suitability basis
→ policy yields unavailable result
→ shared coordination sees bounded result
```

The result and its private evidence can have different Visibility scopes.

AI access to private inputs does not grant disclosure Authority.

## Actor/party attribution

The following may all differ:

```text
source Actor
recorder/importer
policy author
policy adopter/approver
represented party
Actor whose state contributes to basis
affected Actor
action recipient
actual executor/service
```

Representation/on-behalf-of semantics must preserve actual Actor and represented party separately.

## Responsibility and Stewardship

Conditional Policy can initiate fallback after a Responsibility response, but:

```text
activation != Responsibility transfer
Conditional Policy != Coordination Stewardship
```

Who bears ongoing coordination/mental load remains separately owned.

## AI / automation

```text
AI proposal != policy adoption
AI evaluation != human Decision
AI execution != human authorship
policy execution != new Authority
```

Automation may operate only inside separately applicable Authority/autonomy boundaries.

## History / revocation

Consequential policy history preserves material policy state, activation, response and attribution even after access loss, revocation or later correction.

## Current result

```text
MULTI-ACTOR READINESS v1
Conditional Policy integration  PASS WITH HARDENING
REOPEN                          0
UNCLASSIFIED                    0
```

Normative references:

- `concepts/conditional-policy.md`;
- `checkpoints/conditional-policy-v0-validation.md`.
