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

Authority v0 now closes this boundary canonically: Confirmation is an attestation; Authority is scoped governance/effect power. A Confirmation may be one input to an authoritative decision, but does not manufacture Authority.

## Confirmation versus Visibility

Visibility controls bounded information exposure; Confirmation records an affirmation.

```text
Confirmation != Visibility
```

A target may be visible without its Confirmation history being visible, and a Confirmation may exist even when the recipient cannot inspect the private target/source. Visibility of a Confirmation does not grant Authority or make the attested target true.

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

Authority v0 and Visibility v0 harden this further:

```text
AI can request/propose Confirmation
!= AI has Authority to enact the target
!= AI may disclose private source/Confirmation context
```

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

Visibility v0 additionally means target visibility does not imply visibility of all Confirmation/actor/history details.

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
18. Visibility of a target does not imply visibility of its Confirmation history.
19. Visibility of a Confirmation does not imply visibility of every private source or grant re-disclosure Authority.

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
- Confirmation = Visibility;
- universal Attestation root at this stage.

The generic Attestation abstraction is premature because acknowledgement, acceptance, approval, verification and Confirmation have different targets, effects, lifecycles and authority implications.

---

# 14. Deliberately deferred questions

- exact persistence shape: entity/relation/value semantics;
- generic target-reference mechanics;
- material-version equivalence rules;
- retraction/supersession lifecycle;
- machine attestations/trusted automated verification;
- Agreement/Consent semantics;
- Decision/Approval/effective-change semantics;
- Verification process/basis semantics;
- conflict reconciliation;
- specialist signature semantics;
- retention requirements for sensitive/high-consequence Confirmations.

Authority, Visibility and Acknowledgement boundaries are now canonical; detailed enforcement/persistence remains later logical/security work.

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
- Authority/Visibility/Acknowledgement separation;
- conflicting Confirmations;
- offline/sync reconciliation.

This does not yet imply a universal `confirmations` table or generic polymorphic foreign key.

---

# 16. Reopening triggers

Reopen Confirmation v0 if later Evidence/Provenance/Authority/Version work demonstrates that Confirmation is fully redundant, a materially stronger attestation abstraction emerges, specialist verification semantics require a different universal boundary, or persistence pressure exposes unacceptable generic-target coupling.

Absent such evidence, Confirmation remains the current accepted baseline.

---

# 17. Downstream closure — Acknowledgement v0 (2026-08-12)

The later common-ground review has now closed the previously deferred Acknowledgement boundary.

Current canonical result:

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change

Acknowledgement != Confirmation
```

This does not change the historical Confirmation v0 verdict; it resolves a neighbor that was intentionally deferred at the time.

Additional current rules:

```text
delivery/read/display telemetry != Acknowledgement
Acknowledgement != understanding
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority/Decision/effective change
Acknowledgement != Actual
```

Generic cross-domain `Acceptance` was tested in the same review and rejected as a standalone kernel primitive. Positive `accepted` semantics remain owned by the relevant family/workflow, including Participation response and Responsibility-specific hand-off response.

The earlier `Acknowledgement/common-ground model` and generic `Acceptance` entries in this document's deferred list are therefore **closed downstream**. Agreement, Consent, Decision, Version, Verification and specialist semantics remain separately owned dependencies.

Normative downstream references:

- `acknowledgement.md`;
- `../checkpoints/acknowledgement-v0-validation.md`.

---

# 2026-08-13 — Decision / Approval closure amendment

Decision v0 closes the previously deferred Decision/Approval semantic boundary without changing Confirmation.

Canonical separation:

```text
Confirmation
= contextual attestation toward a specific target/version/purpose

Decision
= bounded contextual resolution of a question to a specific result

Approval
= scoped Decision/review result whose governance significance depends on Authority/policy
```

Therefore:

```text
Confirmation != Decision
Confirmation != Approval
```

A Confirmation may be used as Evidence/input in a Decision, but affirming that a target is accurately stated does not choose among alternatives or approve a governed effect. Conversely, a Decision/Approval does not imply that the decision-maker confirmed every underlying fact as universally true.

Material target/version changes do not silently inherit either Confirmation or Decision/Approval. Their applicability/lifecycles remain distinct even when one UI action creates more than one semantic consequence in a particular workflow.

Conflicting Confirmations may remain representable while a Decision/reconciliation process establishes a bounded current interpretation under applicable Authority. That resolution does not erase the Confirmation history.

Downstream closure:

```text
Confirmation ↔ Decision  RESOLVED
Confirmation ↔ Approval  RESOLVED
```

Agreement/Consent, Version/material equivalence, Verification, detailed reconciliation, specialist signature semantics and persistence remain independently deferred.

**Confirmation v0 verdict is unchanged. REOPEN = 0.**

---

# 2026-08-13 — Agreement / Consent downstream closure

Agreement / Consent v0 resolves the remaining mutual-assent/permission boundary without changing Confirmation semantics.

```text
Confirmation
= contextual affirmation of a target/version for a purpose/context

Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure under defined scope/purpose/context
```

Therefore:

```text
Confirmation != Agreement
Confirmation != Consent
```

A confirmer may affirm that terms or facts are accurately stated while refusing those terms or withholding Consent. Conversely, a party may agree to terms or grant Consent without personally confirming every supporting fact as universally true.

The historical `Agreement/Consent semantics` deferral is now downstream-closed at the semantic-boundary level. Version/material equivalence, Verification, specialist signatures/legal validity, Principal/delegation and retention remain separately owned.

**Confirmation v0 verdict remains unchanged. REOPEN = 0.**

---

# 2026-08-13 — Representation / on-behalf-of downstream closure

Representation v0 closes Confirmation's acting-confirmer / represented-party boundary without changing Confirmation semantics.

Current canonical separation:

```text
Confirmation
= contextual affirmation performed by the actual confirmer Actor

Representation / on-behalf-of
= that actual Actor acted for a distinct represented party in the bounded confirmation context

Principal
= technical request identity

Authority / delegation basis
= whether the represented confirmation action is legitimate/effective for the represented party where applicable
```

Therefore:

```text
actual confirmer Actor != represented party by default
Representation != Confirmation
Principal != semantic confirmer
```

A representative may submit a Confirmation with effect for another party where applicable Authority/policy permits it. LifeOS still preserves the actual confirmer Actor, represented party and basis; it does not rewrite the record as if the represented party personally made the affirmation.

Representation does not establish the truth of the confirmed target, and a valid representation basis does not create Confirmation unless an actual confirmation action occurs.

Exact Principal/AuthN/AuthZ mechanics, legal/specialist representation validity, Version/material equivalence, Verification, specialist signatures and retention remain independently SAFE DEFERRED.

No Confirmation invariant failed. **Confirmation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `representation.md`;
- `../checkpoints/representation-delegation-principal-v0-validation.md`.

---

# 2026-08-13 — Version / Material-State downstream closure

Version / Material-State v0 resolves Confirmation's previously deferred material-version-equivalence semantics.

Confirmation remains bound to the materially relevant target state it actually affirmed:

```text
Confirmation C1 -> target state S1
materially changed target state S2
→ C1 remains historical affirmation of S1
→ C1 does not silently confirm S2
```

Materiality is purpose/facet scoped. A technical storage revision, provider sequence/ETag change, metadata-only correction or byte/hash difference does not by itself invalidate Confirmation. Reuse of the same target identity likewise does not prove carry-forward after a material change.

A later state that is materially equivalent for the Confirmation purpose may preserve applicability without fabricating a new attestation.

Canonical downstream separation:

```text
Version != Confirmation
Version != Provenance
Version != Authority / Decision / reconciliation
technical revision != semantic Confirmation target state
```

Version identifies/reconstructs the state to which Confirmation applied; Provenance explains how that state arose; Authority/Decision/reconciliation may govern which interpretation becomes current without rewriting the Confirmation history.

Remaining SAFE DEFERRED concerns include exact retraction/supersession persistence, Verification process/basis, specialist signature/legal validity, exact Principal/AuthN/AuthZ enforcement and retention policy.

No Confirmation invariant failed. **Confirmation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

---

# 2026-08-13 — Reconciliation / Source Precedence downstream closure

Reconciliation v0 closes Confirmation's historical conflict-reconciliation dependency without changing Confirmation semantics.

Canonical separation:

```text
Confirmation
= actor/context-scoped attestation toward a materially specific target state

Reconciliation
= contextual process/capability for handling materially competing states/assertions
```

Conflicting Confirmations remain legitimate attributed records. Reconciliation may consider Confirmation together with Version, Provenance, Evidence, Authority and applicable bounded policy, but it does not transform one confirmer's stance into another's, fabricate consensus, or make source recency equivalent to truth.

A bounded reconciliation result may establish or correct the owning target's current interpretation, while every material Confirmation remains bound to the state/purpose it actually affirmed. Later resolution or reversal does not rewrite historical Confirmation attribution.

Source Precedence is contextual and cannot be inferred from `confirmed`, provider identity, actor identity, recency, Account status or technical access. Visibility of conflict, confirmation history and resolution basis remains independently governed.

No Confirmation invariant failed. **Confirmation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `reconciliation.md`;
- `../checkpoints/reconciliation-source-precedence-v0-validation.md`.