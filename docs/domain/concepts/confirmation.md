# Confirmation v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **A Confirmation is a persistent contextual attestation that a specific confirmer affirms a specific version of an assertion, realization, result, observation, or other confirmable target as sufficiently accepted for a defined purpose at that time. Confirmation records the affirmation; it does not by itself prove universal truth, grant authority, replace Provenance, or change the semantic meaning of the target.**

Confirmation answers:

> **Who or what explicitly affirms this specific version of this target, for which purpose and context?**

It does not answer whether the target actually happened, whether the confirmer has authority to make it canonical for everyone, how the target was originally produced/imported, whether another actor agrees, whether a proposal was accepted, or whether a message was merely seen.

---

# 1. Why Confirmation exists

LifeOS must preserve the difference between information that exists, was imported, was inferred, was observed, was corrected, was explicitly affirmed, became canonical under authority, and what actually happened.

Without Confirmation the model tends toward a weak universal `confirmed=true` flag, or collapses human affirmation into Provenance, Actual, Outcome, acceptance, or authority.

Confirmation provides an explicit contextual attestation without becoming a universal truth mechanism.

---

# 2. Contextual and optional

Not every fact needs Confirmation.

Canonical rule:

> **Absence of Confirmation means only that no qualifying Confirmation is established for the relevant purpose; it does not mean false, rejected, incorrect, not performed, or untrusted.**

Presence of Confirmation means only that the confirmer made the recorded affirmation under the recorded context.

---

# 3. Specific target version

Confirmation targets a specific material version of a target.

```text
Observation v1
value = X
└ Confirmation A

later correction
Observation v2
value = Y
```

Confirmation A remains historical affirmation of v1 and does not silently confirm v2.

> **A materially changed target does not automatically inherit Confirmation of its previous version.**

Exact material-version equivalence remains deferred to Version/Provenance modeling.

---

# 4. Boundaries

## Confirmation versus Actual

Actual describes how an expectation was realized. Confirmation records an affirmation about a target/version.

> **Confirmation != Actual.**

## Confirmation versus Outcome

Outcome describes result/disposition. Confirmation may affirm an Outcome but does not become that result.

> **Confirmation != Outcome.**

## Confirmation versus Observation

Observation describes a measured/perceived/reported/derived fact. Confirmation expresses a stance toward a specific Observation version.

> **Confirmation != Observation.**

## Confirmation versus Provenance

Provenance explains how information came to exist or change. Confirmation is an attestation toward a target/version. Source history can stay identical while Confirmation changes independently.

> **Confirmation != Provenance.**

## Confirmation versus acknowledgement

Acknowledgement concerns receipt/recognition/common ground. Confirmation concerns affirmation of a target/assertion.

> **Acknowledgement != Confirmation.**

## Confirmation versus acceptance/agreement

Acceptance concerns willingness, participation, responsibility, proposal, or agreement semantics. It does not confirm future Actual performance.

> **Acceptance/Agreement != Confirmation.**

## Confirmation versus verification

Verification is the process/basis used to check a claim. Confirmation is the contextual attestation made toward the target.

> **Verification != Confirmation.**

## Confirmation versus authority

Authority determines who/what may establish, approve, override, or mutate canonical state. A confirmer may affirm without possessing that authority; an authoritative source may establish state without personal Confirmation.

> **Confirmation != Authority.**

---

# 5. Awaiting confirmation is derived

Do not model absence as a negative Confirmation record.

```text
policy requires qualifying Confirmation
+
no qualifying Confirmation exists
↓
needs / awaiting confirmation
```

Therefore `awaiting confirmation` is normally derived workflow state, not a Confirmation type.

Likewise imported, inferred, automatically applied, corrected, and pending review are not Confirmation types merely because older product wording grouped them together.

---

# 6. Automation and AI

A user-approved automatic policy may establish an Outcome or other state without fabricating a human Confirmation.

AI may infer, propose, surface evidence, or ask for Confirmation. AI confidence does not itself become Confirmation.

> **AI inference does not silently become Confirmation, canonical truth, or disclosure permission.**

Future bounded machine attestations remain possible but must keep identity, authority, target version and Provenance explicit.

---

# 7. Multi-actor semantics

Confirmation is actor/context scoped.

```text
confirmation by Actor A
!= confirmation by Actor B
!= universal group truth
```

Subject, confirmer, recorder, observer, performer and authority actor may differ.

Conflicting Confirmations are legitimate records and must not be flattened automatically. Future Provenance/Authority/Version rules determine reconciliation and current canonical interpretation by context.

Current access or participation does not erase historical Confirmation attribution.

---

# 8. Purpose scope

A Confirmation sufficient for one purpose is not automatically sufficient for every other domain, actor, legal, professional, or specialist context.

Purpose/context therefore belongs to the semantic meaning of Confirmation.

---

# 9. Identity and cardinality

Conceptual identity is independent from account coincidence, target timestamps alone, provider ID, or UI action ID.

A confirmable target may have `0..N` Confirmations. Exact persistence/cardinality remains deferred to the logical model.

---

# 10. UI implications

Confirmation is primarily a domain concept. UI should usually expose action-oriented language such as:

- Confirm;
- Looks correct;
- Yes, this happened;
- Review and confirm;
- Needs confirmation.

Low-risk interaction may be one tap. High-consequence workflows may expose source, target version, confirmer role, authority basis and audit history through progressive disclosure.

---

# 11. External benchmark interpretation

External evidence supports separation without dictating LifeOS schema:

- RFC 5545 attendee participation states show acceptance/tentative/decline are participation semantics, not Actual occurrence proof;
- ActivityStreams models Accept/Reject as actions toward objects rather than object truth itself;
- HL7 FHIR Provenance separates source/agent/process history from the target resource;
- FHIR VerificationResult provides evidence that verification can remain distinct from the verified resource;
- W3C PROV reinforces separation of provenance from content truth.

External standards remain benchmark evidence, not design authority.

---

# 12. Invariants

1. Confirmation is contextual and optional.
2. Confirmation targets a specific target/version/context.
3. No Confirmation does not mean false, rejected, incorrect, or not performed.
4. Confirmation does not prove universal truth.
5. Confirmation does not create Authority.
6. Confirmation does not replace Provenance.
7. Confirmation does not replace Actual, Outcome or Observation.
8. Material target correction does not silently inherit previous Confirmation.
9. `Awaiting confirmation` is derived workflow state when policy requires Confirmation and none qualifies.
10. Imported/inferred/automatic/corrected are not universal Confirmation types.
11. Human Confirmation must not be fabricated from automation or AI inference.
12. Confirmation by one actor does not imply Confirmation by another.
13. Subject, confirmer, recorder, observer, performer and authority actor may differ.
14. Conflicting Confirmations must be representable.
15. Confirmation may be retracted/superseded without deleting material history.
16. Purpose/context may limit where a Confirmation is sufficient.
17. UI simplicity must not collapse high-consequence semantics in the kernel.

---

# 13. Rejected alternatives

Rejected:

- universal `confirmed` boolean;
- merge with Provenance;
- merge with Actual;
- merge with Outcome;
- merge with Observation;
- Confirmation = Acceptance/Acknowledgement;
- Confirmation = Authority;
- universal Attestation root at this stage.

The generic Attestation abstraction is premature because acknowledgement, acceptance, approval, verification and Confirmation have different targets, effects, lifecycles and authority implications.

---

# 14. Deliberately deferred questions

- exact persistence shape: entity/relation/value semantics;
- generic target-reference mechanics;
- material-version equivalence rules;
- retraction/supersession lifecycle;
- machine attestations/trusted automated verification;
- Authority and canonical-state mutation;
- Acknowledgement/common-ground model;
- Acceptance/Agreement/Participation semantics;
- Verification process/basis semantics;
- conflict reconciliation;
- specialist signature semantics;
- retention requirements for sensitive/high-consequence Confirmations.

---

# 15. Persistence/API implications without physical commitment

The logical model must eventually support, directly or through equivalent semantics:

- stable Confirmation identity where history/sync requires it;
- confirmer/acting actor without requiring every represented actor to have an account;
- target + material target version/reference;
- purpose/context;
- relevant times;
- superseded/retracted history where needed;
- Provenance of the Confirmation itself;
- Authority/Visibility separation;
- conflicting Confirmations;
- offline/sync reconciliation.

This does not yet imply a universal `confirmations` table or generic polymorphic foreign key.

---

# 16. Reopening triggers

Reopen Confirmation v0 if later Evidence/Provenance/Authority/Version work demonstrates that Confirmation is fully redundant, a materially stronger attestation abstraction emerges, specialist verification semantics require a different universal boundary, or persistence pressure exposes unacceptable generic-target coupling.

Absent such evidence, Confirmation remains the current accepted baseline.