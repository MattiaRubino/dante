# Interpersonal Relationship v0

**Status:** accepted semantic baseline — PASS WITH HARDENING; repository closure pending post-write QA  
**Cluster:** Relationships / Reasoning  
**Scope:** persistent Person-to-Person interpersonal context required by current LifeOS product needs

---

## 1. Definition

> **Interpersonal Relationship is the bounded contextual Person-to-Person relation through which LifeOS retains materially useful interpersonal context between two persistent Persons, independently from Participation, Collective Membership, Responsibility, Coordination Stewardship, Authority, Visibility, Agreement, Consent, Representation, Contribution or any particular Activity/Event.**

Canonical question:

> **What materially useful interpersonal relation does Person A have to Person B in this bounded context?**

Examples include user-established context such as:

```text
Maria is Mattia's mother
Luca is Mattia's friend
Anna is Mattia's partner
Marco is Mattia's colleague
```

The relation exists because the interpersonal context itself has durable product value across commitments, search, reminders, history and future collaboration. It is not merely a label attached to one Activity/Event.

---

## 2. Classification

```text
Interpersonal Relationship
= SPECIFIC CONTEXTUAL PERSON↔PERSON RELATION FAMILY

Relationship kind
= BOUNDED / EXTENSIBLE VOCABULARY

Person
= existing native human identity

new native referent
= NO

universal Relationship/social-graph root
= NO
```

An interpersonal relation may be represented directly where semantics are complete or through a specifically qualified relation where material state/history/context requires it. Storage row identity, M:N cardinality, graph traversal and query frequency do not create ontology.

---

## 3. Why current LifeOS needs it

Current product requirements explicitly include person-related commitments without requiring account-to-account collaboration. LifeOS also needs to answer person-scoped questions and preserve context such as family member, friend, colleague, caregiver or client without requiring those people to have Accounts.

Without this relation family, ordinary requests such as:

```text
remind me to call my mother
which commitments to Marco are still open?
buy this for my partner
show items involving my colleague Luca
```

must either depend on fragile free text, misuse Participation/Membership, or fabricate a generic semantic-free Relationship graph. None is acceptable.

---

## 4. Relationship kind

A `relationship kind` carries the specific interpersonal meaning where it is useful. Example vocabulary may include:

```text
parent / child
partner
friend
colleague
manager / report
caregiver / cared-for
client / adviser
teacher / student
other bounded product vocabulary
```

This list is **not** a fixed universal taxonomy and does not authorize one primitive/entity per label.

Canonical rules:

```text
relationship kind
!= native identity
!= universal social role hierarchy
!= Authority role
!= Responsibility role
!= Membership role
```

Vocabulary should remain minimal, extensible and evidence-driven. New kinds are added only when current LifeOS product behavior needs the distinction.

---

## 5. Specific relation semantics over generic graph semantics

Interpersonal Relationship does not reopen the rejected universal `Relationship` entity/root.

```text
specific truthful Person↔Person interpersonal relation
> generic related_to edge
```

Do not normalize semantically stronger relations into this family when the stronger relation fully answers the question:

```text
who is responsible?
→ Responsibility

who participated?
→ Participation

who belongs to this Collective?
→ Membership

who may govern?
→ Authority

who may see?
→ Visibility

who acted for whom?
→ Representation
```

Interpersonal Relationship answers persistent interpersonal context, not those other questions.

---

## 6. Core non-collapse boundaries

```text
Interpersonal Relationship != Person identity
Interpersonal Relationship != Actor
Interpersonal Relationship != Account
Interpersonal Relationship != Collective
Interpersonal Relationship != Membership
Interpersonal Relationship != Participation
Interpersonal Relationship != Responsibility
Interpersonal Relationship != Coordination Stewardship
Interpersonal Relationship != Authority
Interpersonal Relationship != Visibility
Interpersonal Relationship != Agreement
Interpersonal Relationship != Consent
Interpersonal Relationship != Representation
Interpersonal Relationship != Contribution
Interpersonal Relationship != Subject/aboutness
Interpersonal Relationship != Ownership/Possession
Interpersonal Relationship != generic Personal Knowledge edge
```

Therefore:

```text
Maria is my mother
!= Maria may see my data
!= Maria has Authority over me
!= Maria is responsible for my commitments
!= Maria has Consent for another purpose
!= Maria participates in a specific Event
```

Likewise:

```text
Marco is my manager
```

does not itself establish a bounded LifeOS Authority relation for a specific governed action/state.

---

## 7. Direction, inverse, symmetry and transitivity

No universal orientation rule is imposed across all kinds.

Some kinds are naturally directional and may have a specific inverse:

```text
parent_of(A,B)
↔ child_of(B,A)
```

Some may be intentionally actor-scoped or perspective-sensitive:

```text
A records B as friend
!= B necessarily records A as friend
```

No universal symmetry, inverse inference or transitivity is accepted.

```text
friend(A,B)
friend(B,C)
!= friend(A,C)
```

Inverse/symmetry rules belong to the specific relationship kind where materially justified.

---

## 8. Current, historical and material-state semantics

Interpersonal context can change without changing Person identity.

```text
current relationship != historical relationship
correction != silent overwrite
Account lifecycle != interpersonal relationship lifecycle
```

Example:

```text
T0 Anna is Person
T1 partner relation Mattia↔Anna established
T2 relationship later ends
T3 Anna participates in a later Event
```

The ended partner state remains historical where materially relevant; later Participation does not recreate it.

A materially changed relationship state does not silently inherit prior consequences, Visibility, Authority, Consent, Responsibility or Participation because those remain separate semantics.

---

## 9. Assertion, evidence, conflict and correction

A contact/provider import, message history or AI inference may provide Evidence/Provenance for a proposed interpersonal relation but does not silently establish it.

```text
provider label `mother`
→ Evidence/Provenance
→ not automatically canonical truth

AI infers `close friend`
→ inference/proposal
→ not automatically established relation
```

Competing assertions may remain unresolved. LifeOS does not use universal newest-source, provider, creator, manager, contact owner or AI-confidence precedence.

Material correction preserves consequential prior attribution/history rather than rewriting the past.

---

## 10. Identity and Account independence

Both endpoints are Persons. Neither requires a LifeOS Account.

```text
Person A has Account
Person B has no Account
Interpersonal Relationship(A,B)
→ valid
```

Later Account creation, provider linking, account closure or login-provider replacement does not itself create, transfer or erase the interpersonal relation.

---

## 11. Collective boundary

A Person-to-Person interpersonal relation does not manufacture Collective identity.

```text
several friends
!= Collective automatically

family relationship between two Persons
!= Family Collective automatically
```

A true Family/Household/Team Collective may separately exist when its plurality has persistent irreducible identity/state/history/agency. Membership in that Collective remains a separate specific relation.

---

## 12. Privacy and inference safety

Interpersonal context can itself be sensitive.

Visibility of:

```text
Person existence
relationship existence
relationship kind
relationship history
supporting Evidence/Provenance
```

may differ.

A relation does not create disclosure rights. Derived answers must not leak a private relationship kind or hidden Evidence merely because the user can see a related commitment.

---

## 13. AI and automation

AI may:

- resolve natural-language references using already authorized established relations;
- suggest a relation from Evidence;
- detect possible duplicates/conflicts;
- explain a result using only visible basis.

AI must not:

- silently establish a human interpersonal relation;
- infer Authority, Consent, Visibility, Responsibility or Participation from a relationship label;
- universalize culturally or legally variable labels;
- fabricate reciprocity or transitivity.

---

## 14. Progressive formality

Ordinary UI should remain light:

```text
Maria · Mother
Luca · Friend
Anna · Partner
Marco · Colleague
```

The kernel may preserve more context/history only when materially useful. Casual personal context must not become a CRM/social-network bureaucracy.

---

## 15. Stage-deferred implementation matters

The semantic boundary is complete without selecting:

```text
SQL shape
junction-table shape
indexes
API resources
contact/provider sync mechanics
exact kind vocabulary storage
retention/anonymisation mechanics
technical authorization enforcement
```

These are later-stage implementation questions. They are not semantic `SAFE DEFERRED` debt and do not block Relationships / Reasoning closure.

---

## 16. Canonical hardenings

```text
IPR-01  Interpersonal Relationship is a specific Person↔Person contextual relation family.
IPR-02  It creates no native referent/root.
IPR-03  Relationship kind is bounded/extensible vocabulary, not a universal ontology.
IPR-04  Do not create one primitive/entity per kinship/social label.
IPR-05  Interpersonal Relationship != universal Relationship/social graph.
IPR-06  Interpersonal Relationship != Collective.
IPR-07  Interpersonal Relationship != Membership.
IPR-08  Interpersonal Relationship != Participation.
IPR-09  Interpersonal Relationship != Responsibility.
IPR-10  Interpersonal Relationship != Coordination Stewardship.
IPR-11  Interpersonal Relationship != Authority.
IPR-12  Interpersonal Relationship != Visibility.
IPR-13  Interpersonal Relationship != Agreement or Consent.
IPR-14  Interpersonal Relationship != Representation.
IPR-15  Interpersonal Relationship != Contribution.
IPR-16  Relationship labels do not grant rights, duties or disclosure.
IPR-17  Account identity is not required at either endpoint.
IPR-18  Account lifecycle does not determine relationship lifecycle.
IPR-19  No universal symmetry is accepted.
IPR-20  No universal transitivity is accepted.
IPR-21  Inverse semantics belong to the specific kind where justified.
IPR-22  Actor/perspective-scoped relations need not imply reciprocity.
IPR-23  Provider/contact metadata remains Evidence/Provenance until established.
IPR-24  AI inference/proposal does not silently establish human relationship truth.
IPR-25  Conflict may remain unresolved; no universal source-precedence winner.
IPR-26  Current relationship != historical relationship.
IPR-27  Material correction preserves consequential history.
IPR-28  Several interpersonal relations do not automatically create a Collective.
IPR-29  Prefer a stronger specific relation family where it fully answers the domain question.
IPR-30  Persistence/query/cardinality pressure never creates a universal relationship root.
```

---

## 17. Semantic verdict

```text
INTERPERSONAL RELATIONSHIP v0
PASS WITH HARDENING

CURRENT LIFEOS NEED        YES
NEW NATIVE REFERENT        NO
NEW SPECIFIC RELATION      YES
SEMANTIC SAFE DEFERRED      0
REOPEN                      0
UNCLASSIFIED                0
```

Repository `CLOSED` status is intentionally not claimed here. It requires the approved propagation and remote post-write QA recorded in the validation continuation.