# Representation / On-Behalf-Of v0

**Status:** PASS WITH HARDENING — pending post-write scope QA  
**Validated:** 2026-08-13  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS must preserve who actually acted when one person, service or AI acts for another party, without collapsing identity, authentication, authority, responsibility, consent, agreement, provenance or resulting domain state.

The concept exists to answer one bounded semantic question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

Representation is deliberately narrower than legal representation, identity impersonation, delegation engines, agency law, IAM principals or generic party models.

---

# 1. Canonical definition

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context. Representation preserves the actual Actor and represented party separately and, where legitimacy or effect matters, preserves the applicable Authority, delegation, policy, Consent or other basis separately. Representation does not by itself create Authority, Responsibility, Agreement, Consent, Acknowledgement, Confirmation, authorship, truth, technical Principal identity, or an effective domain change.**

Classification:

```text
REPRESENTATION / ON-BEHALF-OF
CANONICAL CONTEXTUAL ACTION-SCOPED RELATION / CAPABILITY

not native entity/root
not universal Agent/Representative identity
not Principal
not Authority
not Responsibility
not Subject/beneficiary
not Provenance
not impersonation
```

A `Representative` is therefore a contextual role in a specific representation context, not a Person subtype or universal native identity.

---

# 2. Why this survives independently

These facts are not equivalent:

```text
who authenticated the request?
who actually acted?
for whom was the action performed?
who had Authority to make the effect legitimate?
who is responsible for the outcome?
what does the record concern?
who agreed or consented?
how did the record/effect come to exist?
```

Existing LifeOS concepts already own most of these questions:

```text
Principal / Account security context  → security/logical model
Actor                                 → actual semantic agency
Representation                        → for whom the action was performed
Authority                             → bounded governance legitimacy
Responsibility                        → accountability
Subject                               → aboutness
Agreement / Consent                   → assent / bounded permission
Provenance                            → material lineage
```

Without Representation, LifeOS is forced either to misattribute the action to the represented party or to hide the represented-party context inside generic provenance/security metadata.

---

# 3. Core non-collapse rules

```text
actual Actor != represented party
represented party != Subject/beneficiary automatically
represented party != Principal automatically
Principal != Actor
Account != Principal
Representation != Authority
Representation != Responsibility
Representation != Delegation
Representation != Provenance
Representation != Agreement
Representation != Consent
Representation != Acknowledgement
Representation != Confirmation
Representation != Decision
technical impersonation != domain attribution truth
```

A represented party may also be Subject, beneficiary, responsible Actor, Agreement party or Consent-giver in a concrete workflow, but those coincidences are contextual facts rather than ontology.

---

# 4. Representation versus Actor

Actor answers:

> Who/what performed the semantic action?

Representation answers:

> For which distinct party was that Actor acting in this bounded context?

Example:

```text
Luca uses his own Account to move Anna's Schedule item
under a bounded delegation.

actual Actor      = Luca
represented party = Anna
```

Anna does not become the actual Actor merely because the effect concerns or benefits her.

Representation does not create a second wrapper Actor identity around Luca or Anna.

---

# 5. Representation versus Subject / beneficiary

Acting concerning someone is not the same as acting for them.

Example:

```text
parent schedules child's appointment
```

The child may be:

```text
Subject
beneficiary
participant
```

without the parent necessarily expressing the child's personal will.

Likewise:

```text
caregiver records Maria's verbal statement
```

may be modeled as:

```text
caregiver = recorder Actor
Maria     = source / Subject
```

with no Representation relation at all unless the caregiver is actually acting in a representational capacity for the bounded action.

Canonical rule:

> **Do not infer Representation merely from aboutness, benefit, care, household membership, guardianship label, organizational role or proximity.**

---

# 6. Representation versus Authority

Representation records for whom an Actor acts. It does not establish whether the Actor is legitimately empowered to create the requested effect.

```text
Representation claim
!= established Authority
```

An Actor may truthfully claim to act for Anna while lacking Authority to perform the attempted operation.

Conversely, an Actor may hold Authority over a domain action without representing the affected person at all.

Example:

```text
manager decides employee shift
```

The manager may have Authority to govern the shift while not representing the employee's personal will.

Authority remains action/target/scope/context specific.

---

# 7. Delegation disposition

`Delegation` is **not** accepted as a universal cross-domain root.

Current canonical disposition:

> **Delegation is a bounded Authority-establishment / entrustment pattern for a specific action, target, scope and context.**

Therefore:

```text
delegated Authority to schedule
!= delegated Authority to consent
!= delegated Authority to agree
!= delegated Authority to disclose private data
!= delegated Responsibility
!= automatic right to re-delegate
```

Where Responsibility transfers, Responsibility/Hand-off owns that semantic change.

Where Participation response is submitted for another participant, Participation owns the response semantics while Representation preserves the response Actor versus represented participant.

Where Agreement/Consent is at stake, those concepts own the assent/permission semantics and specialist/legal validity may still remain external.

No generic `delegate everything` capability is accepted.

---

# 8. Principal / Account boundary

`Principal` remains a technical security identity concept rather than a LifeOS domain primitive.

Future security design may need to answer:

```text
which authenticated/authorized Principal made the request?
```

while the domain independently answers:

```text
who actually acted semantically?
for whom did they act?
what Authority/basis applied?
```

Canonical rules:

```text
Person != Account != Principal
Actor != Account/Principal
Principal != represented party
Principal != Authority
Principal authentication != semantic Representation
```

A represented Person requires no synthetic Account.

---

# 9. Technical impersonation boundary

A future security mechanism may permit technical impersonation, delegated tokens, service accounts or session switching.

Those mechanisms do not define domain attribution truth.

```text
request technically executes as B
```

does not justify recording:

```text
B actually performed the semantic action
```

when LifeOS materially knows that A performed the action for B.

Canonical rule:

> **Security-layer impersonation must not erase materially relevant actual-Actor attribution.**

---

# 10. Representation versus Responsibility

Acting for someone does not make the representative responsible for the underlying commitment, nor does Responsibility imply Representation.

Example:

```text
assistant submits manager's approved travel booking
```

Possible facts:

```text
assistant = actual booking Actor
manager   = represented party
manager   = Responsibility holder
```

or a different workflow may assign Responsibility to the assistant while no Representation exists.

Therefore:

```text
Representation != Responsibility
Delegation of Authority != Responsibility transfer
```

---

# 11. Representation versus Acknowledgement / Confirmation / Agreement / Consent / Decision

Representation preserves attribution; it does not fabricate the represented party's mental, common-ground or permission state.

Canonical rules:

```text
representative clicked Acknowledge
!= represented Person personally Acknowledged by default

representative affirmed a fact
!= represented Person personally Confirmed by default

representative assented to terms
!= represented Person's Agreement by default

representative permitted use
!= represented Person's Consent by default

representative made a Decision
!= represented Person personally made the Decision by default
```

A representative action may have effect for the represented party when applicable Authority/policy/specialist rules allow it. That still does not rewrite the identity of the actual Actor.

For Agreement/Consent especially, LifeOS records its domain semantics without claiming that a representation basis is legally sufficient in every jurisdiction/context.

---

# 12. Representation versus Provenance

Provenance may record that a record/effect came from an action performed by a representative under a particular source, process or security context.

That lineage does not make Representation redundant.

```text
Provenance
= how the target/action/result came to exist or change

Representation
= actual Actor acted for a distinct represented party
```

A Representation relation may itself have Provenance.

Do not hide represented-party semantics inside arbitrary provenance metadata when the distinction materially affects history, Authority or interpretation.

---

# 13. Action-specific scope and delegability

Representation and delegation are bounded by the semantic action family.

The following implication is rejected:

```text
Actor may do one thing for Anna
→ Actor may do every thing for Anna
```

Examples:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private source
!= Authority to re-delegate
```

The exact delegability rules remain policy/specialist dependent. The domain invariant is that scope cannot be silently broadened.

---

# 14. Lifecycle and history

Representation may be bounded by time, context, action scope or a delegation/Authority basis.

A material history may need to reconstruct:

```text
T0 representation/delegation established
T1 Actor acts for represented party
T2 effect becomes effective
T3 representation/delegation expires or is revoked
T4 later action attempted
```

Canonical rules:

```text
revoked/expired basis != never existed
current Representation/Authority != historical action-time basis
past valid representation != standing future authority
```

If a representation claim is later disputed or corrected, LifeOS preserves materially relevant attribution/provenance rather than silently rewriting history.

---

# 15. Conflict and epistemic integrity

The following states may differ:

```text
Actor claims to represent B
source/provider says Actor represented B
B disputes representation
Authority evidence is incomplete
current policy cannot establish legitimacy
```

LifeOS may preserve an unresolved representation claim or disputed basis where reality cannot yet be established.

Do not infer:

```text
record exists
→ representation was valid
```

or:

```text
effect occurred
→ representative had legitimate Authority
```

Actual occurrence, Attribution and Authority remain separable.

---

# 16. Multi-hop delegation / re-delegation

A chain such as:

```text
Anna → Luca → Service X
```

must not be assumed valid merely because Anna delegated something to Luca.

Canonical rule:

> **Re-delegation is not implied.**

Where a multi-hop chain is legitimate, later security/logical design must preserve the materially relevant chain, scope reductions and action-time basis without requiring one universal Delegation graph/root.

---

# 17. AI / software representation

AI or software may be the actual Actor when material semantic agency exists.

Example:

```text
AI proposes a Schedule change under a user's bounded policy.
```

Canonical rules:

```text
AI Actor != human Actor
AI proposal != human Decision
AI access != Authority to disclose
AI acting under policy != unlimited representation
AI action != human Agreement/Consent/Acknowledgement/Confirmation
```

If an AI/service actually executes a bounded action for a user under valid policy, the AI/service Actor, represented party and applicable Authority/policy basis remain separately attributable where material.

Do not launder AI/service behavior into human authorship.

---

# 18. Visibility / privacy

The existence of Representation does not mean every actor may see its basis or full chain.

Possible separation:

```text
shared resulting Schedule change          visible
actual representative identity            restricted
private delegation/guardian basis         more restricted
supporting Evidence                        separately governed
```

Canonical rule:

> **Result Visibility, Representation Visibility, delegation/Authority-basis Visibility and Evidence/Provenance Visibility may differ.**

Representation itself may reveal sensitive relationships or capacity/legal context and must remain subject to contextual Visibility/retention rules.

---

# 19. Specialist boundaries

LifeOS does not determine universal legal capacity, power-of-attorney validity, guardianship law, clinical consent authority, corporate agency law or regulated authorization.

External specialist systems/documents may remain authoritative sources for those questions.

LifeOS needs only enough semantic structure to preserve:

```text
actual Actor
represented party
bounded action/context
claimed/established applicable basis where material
source/Provenance
resulting effect separately
```

without asserting more legal validity than the evidence supports.

---

# 20. Product / UI implications

Ordinary self-use should expose no representation machinery.

Simple assisted workflows may show natural language such as:

```text
Added by Luca for Anna
Responded by Sara on behalf of Marco
Scheduled by assistant
```

High-consequence views may expose:

```text
acting person/service
represented party
scope
basis
validity period
revocation/history
source/evidence
```

Kernel precision must not produce enterprise proxy-management UI everywhere.

---

# 21. Core invariants

1. Actual semantic Actor is preserved where material.
2. Actual Actor != represented party.
3. Represented party != Subject/beneficiary automatically.
4. Representation != Authority.
5. Claiming representation != established right to act.
6. Representation != Delegation.
7. Delegation is action/target/scope/context bounded.
8. Delegated Authority for X does not imply Authority for Y.
9. Delegated Authority != Responsibility transfer.
10. Re-delegation is not implied.
11. Representative action does not automatically become represented party's Acknowledgement.
12. Representative action does not automatically become represented party's Confirmation.
13. Representative assent does not automatically become represented party's Agreement.
14. Representative permission does not automatically become represented party's Consent.
15. Representative Decision/action preserves actual decision/action Actor.
16. Principal != Actor.
17. Account != Principal.
18. Represented Person requires no Account.
19. Technical impersonation does not rewrite domain attribution truth.
20. Revoked/expired basis does not erase historical representation.
21. Disputed representation may remain unresolved.
22. AI/service action must not be laundered into human authorship or will.
23. Result Visibility does not imply Visibility of representation/delegation basis.
24. Persistence/formality is consequence-sensitive.

---

# 22. Rejected alternatives

Rejected:

- `Principal` as a LifeOS domain root;
- universal `Agent` / `Representative` entity hierarchy;
- generic Delegation root for every transferred role/permission;
- blanket `acts_for` relationship implying all actions;
- `user_id` / authenticated Principal as semantic Actor truth;
- technical impersonation as domain attribution;
- household/member/guardian label as blanket representation;
- acting for someone = Subject/beneficiary;
- acting for someone = Authority;
- acting for someone = Responsibility;
- acting for someone = represented person's Agreement/Consent/Acknowledgement/Confirmation/Decision;
- automatic re-delegation;
- one universal delegation graph/table pre-approved by semantics.

---

# 23. Deliberately deferred questions

- exact Principal/AuthN/AuthZ/security identity model;
- technical impersonation/token-exchange/session mechanics;
- exact action-specific delegation policy representation;
- legal capacity/guardian/power-of-attorney validity;
- whether a representative may create legally/clinically valid Agreement/Consent in a concrete specialist domain;
- material Version/scope-equivalence mechanics;
- multi-hop delegation-chain persistence;
- Verification of representation/delegation basis;
- Organization/group/collective representation;
- retention/audit/anonymization;
- AI/service native identity and delegation mechanics;
- exact logical/physical typed-reference representation.

All are SAFE DEFERRED only while the invariants above remain representable without identity/Authority collapse.

---

# 24. Persistence / API pressure without physical commitment

Future logical design must be able to represent, where material:

```text
actual Actor
represented party
specific action/role
bounded target/context
relevant time
Account/Principal authentication context if needed
Authority/delegation/policy/Consent basis if applicable
source/Provenance
revocation/expiry/history
resulting target state separately
```

This concept does **not** pre-approve:

```text
representations table
principals table as domain ontology
delegations table for every role
polymorphic party root
universal actor_id
universal on_behalf_of FK
universal authorization graph
```

Physical representation is deferred until whole-domain semantic and multi-actor gates are complete.

---

# 25. Reopening triggers

Reopen Representation v0 if later evidence proves that:

1. actual Actor + represented party can be represented losslessly by an already accepted concept with lower semantic cost;
2. Representation cannot remain distinct from Authority in real workflows;
3. specialist legal/clinical representation requires a stronger universal semantic boundary for ordinary LifeOS use;
4. logical persistence cannot preserve action-scoped history without introducing an identity/lifecycle contradiction rather than an implementation inconvenience;
5. AI/service delegation requires a materially different semantic model;
6. collective/organization representation demonstrates that the current party/action relation is structurally insufficient.

Until then, Representation/on-behalf-of is the current accepted semantic candidate pending full propagation and post-write QA.
