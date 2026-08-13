# Representation / On-Behalf-Of v0

**Status:** Current accepted baseline — PASS WITH HARDENING; hardenings incorporated; post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `b6c53ffa40ba7c1c1408f583856617a0e000f31b`

## Canonical definition

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context. Representation preserves the actual Actor and represented party separately and, where legitimacy or effect matters, preserves the applicable Authority, delegation, policy, Consent or other basis separately. Representation does not by itself create Authority, Responsibility, Agreement, Consent, Acknowledgement, Confirmation, authorship, truth, technical Principal identity, or an effective domain change.**

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

Classification:

```text
REPRESENTATION / ON-BEHALF-OF
CANONICAL CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY

✅ actual Actor preserved
✅ represented party preserved separately
✅ bounded action / target / context
✅ applicable Authority / delegation / policy / Consent / other basis remains separate
✅ history-sensitive where material
✅ direct/simple or specifically qualified when lifecycle/history/basis matters

❌ native entity/root
❌ universal Agent/Representative identity
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ impersonation
❌ represented-party will by implication
```

`Representative` is contextual role language over a Representation relation. It is not a Person subtype or universal party identity.

---

# 1. Why Representation exists

LifeOS already separates:

```text
Person != Actor != Account != Principal
Actor != Authority
Actor != Responsibility
Actor != Subject
```

Those distinctions still leave a material question:

```text
Who actually acted?
```

is not the same as:

```text
For whom was this bounded action performed/asserted?
```

Representative workflows include assistants, caregivers, parents/guardians, external helpers, services and AI operating under bounded policy. Without Representation, implementations are pushed toward false shortcuts such as recording the represented party as the Actor, using Account/Principal as domain attribution, or overloading Authority/Provenance.

Canonical rule:

> **Representation owns the bounded actual-Actor ↔ represented-party relation without manufacturing a new identity root.**

---

# 2. Actual Actor and represented party

Where representation is material:

```text
actual Actor != represented party
```

`Luca acted for Anna` must not become `Anna acted`.

The represented party may be an eligible native referent; Representation never creates a wrapper identity.

---

# 3. Representation versus Subject / beneficiary

```text
acting about X
acting for the benefit of X
acting for X
```

are not automatically equivalent.

Examples:

```text
parent schedules child's appointment
```

may be:

```text
parent = actual Actor
child = Subject / beneficiary
```

without asserting that the parent expressed the child's personal will.

Likewise a caregiver recording another Person's statement may be recorder Actor while the Person is source/Subject, with no Representation relation required.

```text
Representation != Subject/beneficiary
```

---

# 4. Representation versus Authority

Representation is attribution, not legitimacy.

```text
Actor claims to act for X
!= Actor has Authority to produce the effect for X
```

Where legitimacy matters, preserve the applicable Authority/delegation/policy/Consent/other basis separately.

```text
Representation != Authority
claimed Representation != established Authority
```

This preserves disputed, expired, revoked, exceeded-scope and hostile cases.

---

# 5. Delegation disposition

`Delegation` is **not** a universal cross-domain primitive/root.

Current canonical meaning:

> **Delegation is a bounded Authority-establishment / entrustment pattern for a specific governed action/effect/scope.**

Therefore:

```text
delegation of Authority X
!= transfer of Responsibility
!= transfer of Participation
!= transfer of Agreement/Consent
!= blanket authority to act
```

Responsibility Hand-off remains Responsibility-specific. Participation operations remain Participation-specific. Agreement/Consent remain separate semantic families.

```text
re-delegation is not implied
```

---

# 6. Principal / Account boundary

```text
Person
= native human identity

Account
= platform/access identity boundary

Principal
= authenticated/authorized security identity in a technical request/security context

Actor
= semantic agency attribution

Representation
= action-scoped on-behalf-of relation

Authority
= legitimacy/governance capability for bounded effect
```

Canonical separation:

```text
Account != Principal
Principal != Actor
Principal != represented party
Principal != Authority
Principal != Representation
```

`Principal` remains security/logical-model language and is **not a LifeOS domain primitive**.

A represented Person requires no synthetic Account.

---

# 7. Technical impersonation

Security infrastructure may later support impersonation/token exchange/session switching.

Canonical rule:

```text
technical impersonation
!= domain attribution truth
```

Where the material actual Actor is known, authentication mechanics must not rewrite history as if the represented party personally acted.

---

# 8. Responsibility and Participation

```text
Representation != Responsibility
Delegation of Authority != Responsibility transfer
```

A response Actor may also differ from the participant whose Participation state is being changed.

```text
participant/native referent
!= actual response Actor
```

Representation owns the on-behalf-of relation; Participation owns the response/involvement semantics.

---

# 9. Acknowledgement / Confirmation

A representative may perform a bounded acknowledgement or confirmation action where the workflow permits represented effect, but LifeOS preserves the actual Actor.

```text
representative Acknowledgement
!= represented party personally acknowledged

representative Confirmation
!= represented party personally confirmed
```

Applicable Authority/policy may determine effect; Representation itself does not manufacture it.

---

# 10. Agreement / Consent

Agreement requires mutual assent to materially same terms/version. Consent is actor-scoped bounded permission.

Representative action does not automatically become represented-party Agreement or Consent.

```text
Authority to schedule for Anna
!= Authority to agree for Anna
!= Authority to consent for Anna
```

Represented Agreement/Consent may have valid effect only under an applicable action-specific basis/policy/specialist rule. LifeOS preserves actual Actor, represented party, scope/version/purpose and basis while avoiding claims of universal legal validity.

---

# 11. Decision

A representative may make/participate in a Decision for another party only where applicable Authority/process permits it.

Preserve separately:

```text
actual decision Actor/process
represented party
Authority/delegation basis
Decision result
resulting target state
```

A represented Decision does not mean the represented party personally deliberated, agreed, consented, acknowledged or confirmed.

---

# 12. Provenance

Representation is not Provenance, but materially relevant representation should be traceable through Provenance/history.

Possible material lineage:

```text
actual Actor
represented party
Account/Principal context
Authority/delegation/policy basis
target/material version
time
correction/revocation context
```

```text
Representation != Provenance
Representation may have Provenance
```

---

# 13. Chronology / lifecycle

Representative chronology must preserve action-time truth:

```text
T1 bounded delegation granted
T2 actual Actor authenticates
T3 represented action occurs
T4 resulting domain concept owns effect
T5 delegation revoked
T6 later represented attempt occurs
```

Required rules:

```text
current Authority != historical action-time Authority
past valid Representation != standing future Authority
revoked/expired basis != never existed
attempted Representation != legitimate/effective result automatically
```

Historical queries must reconstruct who acted, for whom, under which basis, whether the basis applied then, and what effect became effective.

---

# 14. Dispute / correction

A party may dispute that an Actor was authorized to act for them.

LifeOS may need to preserve:

```text
claimed Representation
Evidence / Provenance
claimed or established Authority basis
Decision/reconciliation if later resolved
unresolved conflict if not resolved
```

No universal last-write-wins rule is accepted.

Misattribution may be corrected without erasing material history.

---

# 15. Re-delegation / chains

Representation is not transitively delegable.

```text
A authorizes B
```

does not imply:

```text
B may authorize C
```

Multi-hop delegation requires explicit applicable basis. Exact chain persistence remains security/logical-model work.

---

# 16. AI / service boundary

AI/software may be actual Actors where agency is domain-material.

AI/service may act under bounded policy/Authority, but must not:

- be recorded as the represented human;
- fabricate human Acknowledgement/Confirmation/Agreement/Consent/Decision;
- infer or enlarge delegation scope;
- assume re-delegation;
- hide a materially relevant representation chain.

```text
AI/service agency != human authorship/will
```

---

# 17. Visibility / privacy

Representation/delegation can itself be sensitive.

```text
visible result
!= visible Representation relation
!= visible Authority/delegation basis
!= visible Principal/authentication details
```

A representative may receive only a safe projection rather than all private source context.

---

# 18. Product simplicity

Representation precision belongs in the kernel but should be exposed only where consequence warrants it.

Possible natural UI:

```text
Done by Luca for Anna
Responded by caregiver
Managed by assistant
```

High-consequence history may expose actor, represented party, action/scope, basis, time and revocation status.

Ordinary self-use must not become proxy/delegation bureaucracy.

---

# 19. External benchmark disposition

Benchmark findings used by the V3 review:

```text
RFC 8693 delegation actor/subject separation        ADAPT
RFC 8693 impersonation as domain attribution        ANTI-PATTERN
FHIR Provenance who/onBehalfOf                       ADAPT
W3C PROV actedOnBehalfOf                             ADAPT
W3C authority/responsibility coupling                ANTI-PATTERN if copied literally
NIST digital-identity role separation                ALREADY STRONGER / boundary confirmation
generic IAM Principal as domain primitive            NOT APPLICABLE
```

External standards are evidence, not ontology authority.

---

# 20. Canonical invariants

1. Representation is contextual action-scoped semantics, not identity/root.
2. Actual Actor and represented party remain distinct.
3. Representation != Actor identity.
4. Representation != Subject/beneficiary.
5. Representation != Authority.
6. Claimed Representation != established legitimacy.
7. Representation != Responsibility.
8. Representation != Principal/Account.
9. Representation != Provenance.
10. Technical impersonation does not replace truthful domain attribution.
11. Delegation is bounded Authority-establishment/entrustment, not universal primitive.
12. Authority to X does not imply Authority to Y.
13. Delegation of Authority does not transfer Responsibility automatically.
14. Re-delegation is not implied.
15. Representative action does not fabricate represented-party Acknowledgement.
16. Representative action does not fabricate represented-party Confirmation.
17. Representative action does not fabricate represented-party Agreement.
18. Representative action does not fabricate represented-party Consent.
19. Representative Decision preserves actual decision Actor/process.
20. Revocation/expiry changes future applicability without deleting history.
21. Disputed Representation may remain unresolved.
22. AI/service action does not become human authorship/will.
23. Representation/basis Visibility is independent from result Visibility.
24. Representation persistence/formality is consequence-sensitive.
25. A LifeOS Representation relation does not prove legal/clinical capacity or validity.

---

# 21. Rejected alternatives

Rejected:

```text
universal Principal domain root
universal Agent/Representative root
universal Delegation root
represented party substituted as actual Actor
Account = Actor
Principal = Actor
Representation = Authority
Representation = Responsibility
Representation = Subject/beneficiary
Representation = Provenance
technical impersonation as domain truth
blanket delegability
implicit re-delegation
Representation as legal-validity proof
AI inference as representation/Authority basis
```

---

# 22. SAFE DEFERRED dependencies

Still independently owned:

```text
exact Principal/AuthN/AuthZ/enforcement
technical impersonation mechanics
action-specific delegability/policy
legal/specialist representation capacity
represented Agreement/Consent legal validity
Version/material scope
multi-hop delegation persistence
Verification of representation basis
Organization/group/collective representation
retention/audit/privacy
AI/service delegation chain
exact persistence/cardinality/API representation
```

Every material item has owner, reopening trigger and test set in `../checkpoints/representation-delegation-principal-v0-validation.md`.

```text
REOPEN                         0
unclassified material items    0
```

---

# 23. Persistence/API implications — no physical commitment

Future logical modeling must support, where material:

- actual Actor/native identity;
- represented party/native identity;
- bounded action/target/context;
- material scope/version/time;
- applicable Authority/delegation/policy/Consent/other basis;
- Account/Principal context separately where material;
- history/revocation/correction;
- Provenance/Evidence/dispute;
- independent Visibility/retention.

This does **not** pre-approve:

```text
one representatives table
one universal principal_id domain FK
universal on_behalf_of_id on every record
universal delegation graph
policy-engine schema
Party/Agent superclass
generic polymorphic target JSON
final AuthN/AuthZ implementation
```

---

# 24. Reopening triggers

Reopen Representation v0 only if later evidence shows that:

1. Actor + Authority + Provenance can represent the relation losslessly with lower complexity;
2. represented-party relation gains independent stable identity/lifecycle requiring a different family;
3. specialist representation workflows expose a structural contradiction;
4. collective/Organization identity materially changes represented-party semantics;
5. Principal/AuthN/AuthZ implementation proves the accepted separation contradictory rather than merely inconvenient;
6. Version/material-scope mechanics cannot preserve action-specific history;
7. whole-domain regression exposes real redundancy with another accepted concept.

Vocabulary difference alone is never sufficient.

---

# 25. Validation / QA result

Normative validation:

- `../checkpoints/representation-delegation-principal-v0-validation.md`

Post-write QA against:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

resulted in:

```text
approved unique paths changed          25 / 25
new files                                2 / 2
modified files                          23 / 23
out-of-scope paths                       0
structural REOPEN                        0
unclassified material dependencies      0
branch behind main                       0
```

Representation / on-behalf-of v0 is therefore part of the current accepted Domain Atlas branch baseline.

---

# 26. Downstream closure — Version / Material-State v0 (2026-08-13)

Version / Material-State v0 resolves Representation's former `Version / material scope` SAFE DEFERRED dependency without changing Representation semantics.

A represented action remains attributable to the material action/target/scope state the actual Actor acted against:

```text
Representation R1
actual Actor = Luca
represented party = Anna
action/target/scope state = S1

later material target/scope change -> S2
→ R1 remains historical attribution for S1
→ R1 is not silently rewritten as action against S2
```

A materially changed Authority/delegation/policy basis may also affect whether a later represented action is legitimate, while the historical action and basis state remain reconstructible. Version identifies/reconstructs those states; Authority/policy decides legitimacy/effect; Provenance explains lineage.

Materiality is action/scope specific. Technical storage/provider revisions, ETags/MVCC tokens, hashes or same target ID do not determine whether a represented action/basis remains applicable.

Canonical separation:

```text
Version != Representation
Version != Authority / Delegation / Principal
Version != Provenance / Decision / reconciliation
same represented party/target identity != automatic scope carry-forward
```

AI/service represented actions follow the same stale-base rule: where material, the system must preserve the state it acted against and re-evaluate before effect if target, scope or Authority/policy basis materially diverges.

Remaining SAFE DEFERRED Representation dependencies include exact Principal/AuthN/AuthZ enforcement, action-specific delegability/policy, legal/specialist capacity/validity, represented Agreement/Consent legal validity, multi-hop delegation persistence, Verification of basis, collective/Organization representation, retention/audit/privacy, AI/service delegation chain and exact persistence/API representation.

No Representation hardening failed. **Representation remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.
