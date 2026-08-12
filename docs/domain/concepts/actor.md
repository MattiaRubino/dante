# Actor v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **Actor is the contextual semantic role/capability of a native referent or system when agency for an action, assertion, transformation, proposal, confirmation, participation, or other meaningful behavior is attributed to it. Actor does not create independent identity and does not by itself imply responsibility, authority, ownership, Account identity, Principal identity, participation, or any specific action role.**

Actor answers the bounded semantic question:

> **What native referent or system is acting in this context?**

Actor is a **canonical semantic agency role/capability**, not an independent entity, universal root, or mandatory persistence superclass.

Typical shapes:

```text
Person Anna
    ↓ recorder role / Actor semantics
Observation O7
```

```text
Automation X
    ↓ generated-by / Actor semantics
Reminder proposal
```

```text
AI Agent Y
    ↓ proposed-by / Actor semantics
Plan revision proposal
```

---

# 1. Why Actor semantics exist

LifeOS needs to attribute meaningful agency without assuming that every actor is a Person or Account.

Possible actors include, where the containing semantics permit:

- Person;
- organization-like referent;
- external provider/system;
- device/automation with meaningful agency attribution;
- AI agent;
- integration/service.

Without Actor semantics, LifeOS would be pushed toward weak alternatives:

1. use Account/User as the identity of every action;
2. treat every action source as a Person;
3. create a universal `Actor` entity that wraps native identities;
4. conflate who acted with who was responsible or authorized;
5. lose accurate provenance when software/automation acts on behalf of a human or service.

The agency semantic is real; a duplicate Actor identity is not.

---

# 2. Actor is a role/capability, not identity

If Person Anna records a measurement, Anna retains Person identity.

```text
Person Anna
recorded Observation O7
```

Rejected shape:

```text
Actor A99
    ↓ wraps
Person Anna
```

Likewise an AI/service should retain whatever native/system identity is appropriate rather than being copied into a parallel Actor object solely to be referenced.

Canonical rule:

> **Actor attribution references the native referent/system identity appropriate to the context; it does not manufacture a second Actor identity.**

The final logical typed-reference mechanism is deferred.

---

# 3. Actor versus Person

Person is native human identity.

Actor is contextual agency.

```text
Person != Actor
Person may play Actor role
Actor need not be Person
```

Examples:

- a child may be represented as Person/Subject without acting in a workflow;
- a deceased Person remains a Person but has no current agency;
- a software service may be an Actor without being a Person.

Agency does not define human identity.

---

# 4. Actor versus Account

Account represents LifeOS access/membership/authentication lifecycle.

Actor represents who/what acted semantically.

Example:

```text
Person Anna
Actor role: recorder

Account A1
authenticates request

Observation
subject = Person Maria
```

The Person/Actor attribution and Account/authentication context may coincide in simple self-use, but they answer different questions.

Canonical boundaries:

```text
Actor != Account
Account != action performer by definition
Account closure != loss of historical Actor attribution
```

A system action may also occur under a service/security Principal rather than a human Account.

---

# 5. Actor versus Principal

Principal is a deferred security/authority concept answering approximately:

> Under which security identity was this action authenticated/authorized?

Actor answers:

> Who/what is semantically attributed as acting?

These may differ.

Example:

```text
AI agent
Actor

service identity
Principal

human Person
on-behalf-of / delegated authority context
```

Therefore:

```text
Actor != Principal
```

Exact Principal/delegation/authorization semantics belong to later Authority/security review.

---

# 6. Actor versus Subject

Subject concerns aboutness; Actor concerns agency.

```text
Person Maria
Subject of Observation

Person Anna
Actor/recorder of Observation
```

A single Person may be both in a self-report, but the roles remain separate.

```text
Subject != Actor
```

This boundary prevents `current user` or `creator` from becoming accidental subject identity.

---

# 7. Actor versus specific action roles

Actor is not a replacement for precise relations such as:

```text
performer
recorder
observer
confirmer
requester
proposer
transformer
participant
responsible actor
approver
governor
```

When the exact role matters, LifeOS should preserve it.

Actor is the shared agency semantic that allows those relations to reference eligible native agents without creating an inheritance root.

Canonical rule:

> **Use the most specific meaningful action role; do not replace typed relations with a generic `actor` edge merely because all participants exhibit agency.**

The exact Relationship model is deferred.

---

# 8. Actor versus responsibility

Doing something and being responsible for it are not identical.

Examples:

```text
manager responsible
employee performs
```

```text
caregiver responsible for follow-up
nurse records measurement
```

```text
automation executes
human remains accountable
```

Therefore:

```text
Actor != Responsible actor
Actor != accountability
Actor != stewardship
```

Responsibility/Assignment/Hand-off/Stewardship will be modeled later.

---

# 9. Actor versus authority

Agency does not imply permission or canonical authority.

```text
Person X edits record
```

does not itself prove:

```text
X was authorized
X's assertion becomes canonical
X may override another actor
```

Likewise:

```text
AI proposes change
```

does not grant the AI Authority to establish it.

Canonical rule:

> **An Actor can act without thereby becoming authoritative; authorization and canonical-change authority remain separate semantics.**

---

# 10. Actor versus source/provenance

An Actor may appear in Provenance as creator, recorder, transformer, importer, generator, or corrector.

But:

```text
Actor != Provenance
Actor != Source
```

Provenance describes materially relevant lineage. Actor semantics identify an agentic referent participating in that lineage/action.

A provider may be a source without being modeled as the semantic Actor for every downstream transformation.

---

# 11. Human-on-behalf-of and delegated action

LifeOS must remain capable of representing cases such as:

```text
assistant acts for manager
caregiver acts for older adult
AI acts under user-approved automation
service acts under delegated integration permission
```

Do not flatten these into one `created_by` identifier.

Conceptually distinguish:

- semantic Actor;
- Account/Principal that authenticated the operation;
- Person/organization on whose behalf the action occurred, where relevant;
- Authority/delegation basis;
- responsibility/accountability.

Exact on-behalf-of/delegation relationships are deferred, but Actor v0 must not prevent them.

---

# 12. System, automation, device, and AI agency

Not every technical process deserves Actor semantics.

Actor should be used when agency attribution is meaningful to domain history, authority, responsibility, user understanding, or provenance.

Examples that may justify Actor semantics:

- AI proposes a schedule change;
- automation sends a reminder;
- integration imports and transforms external data;
- service submits an externally authoritative update.

Examples that may remain implementation detail:

- database trigger updates timestamp;
- cache refresh;
- internal serialization step.

Canonical guardrail:

> **Technical execution alone does not automatically elevate every process into a domain Actor.**

The containing workflow/provenance policy determines materiality.

---

# 13. External/non-account actors

An Actor does not require a LifeOS Account.

Examples:

- external Person who performs an Activity;
- clinician/teacher/vendor named in imported history;
- external organization/provider;
- automation or integration.

Historical reality should not require synthetic Accounts merely to record agency.

---

# 14. Historical attribution

Actor attribution should remain explainable after access relationships change.

Example:

```text
2027 Anna records Observation
2029 Anna's Account changes
2030 Account disabled
```

Where retention/privacy policy permits, historical records should still identify Person Anna as recorder/Actor rather than degrading automatically to an Account tombstone.

Current access != historical attribution.

---

# 15. Multi-actor implications

Actor semantics support shared reality without forcing one user-centric model.

Canonical examples:

```text
shared Activity
Person A = responsible actor
Person B = performer
Person C = requester
```

or:

```text
Observation about Person D
Person E = observer
Person F = recorder
AI G = transformer
```

These roles may coexist without creating duplicate domain objects or per-user copies.

Actor itself must not become a semantic-free universal relation replacing the typed roles.

---

# 16. Privacy and selective disclosure

Knowing who acted can itself be sensitive.

Therefore:

- visibility of a target does not imply visibility of all Actor/provenance details;
- historical attribution may be retained while selectively hidden in product views;
- AI/context builders must respect visibility before surfacing actor identity;
- on-behalf-of/delegation details may require tighter disclosure than the resulting shared fact;
- current Account access does not determine all historical visibility.

Exact policy remains future work.

---

# 17. AI boundary

AI can itself be an Actor when its agency is materially relevant.

AI may:

- propose actions;
- transform data;
- summarize or derive candidates;
- execute user-authorized automations where product semantics permit.

AI must not:

- impersonate a human Actor;
- attribute a human action to itself or vice versa;
- convert its proposal into human Confirmation/Acceptance;
- infer Authority from its ability to act;
- hide the human/service delegation chain when material.

Canonical rule:

> **AI agency must remain attributable without laundering human authorship, authority, or responsibility.**

---

# 18. Simple UI versus kernel semantics

Users should normally see specific natural roles:

```text
Done by Anna
Recorded by Marco
Imported from Garmin
Suggested by LifeOS AI
Confirmed by Luca
```

rather than a generic `Actor` noun.

Actor is primarily hidden/cross-cutting semantics enabling consistent identity references across those roles.

---

# 19. External benchmark synthesis

External patterns are evidence only.

Useful lessons include:

- provenance models distinguish agents from activities/entities and allow people, organizations, or software agents;
- identity/security systems distinguish authenticated principals from real-world persons and service/application identities;
- mature systems frequently need on-behalf-of/delegated execution semantics.

LifeOS adapts the separation of **agency, human identity, credentials, and authority** without inheriting external taxonomies wholesale.

---

# 20. Adversarial reductio summary

## REMOVE Actor semantics

Agency becomes scattered into Person/Account/User/source fields and cannot represent software/external actors coherently.

**Result:** FAIL.

## MAKE Actor a universal entity/root

Person/system/native identities are duplicated only to create a common reference target.

**Result:** FAIL.

## MERGE Actor with Person

Software/service actors and passive humans break the model.

**Result:** FAIL.

## MERGE Actor with Account

External actors, service actions and historical identity continuity break.

**Result:** FAIL.

## MERGE Actor with Principal

Semantic agency and authentication/authorization identity become indistinguishable.

**Result:** FAIL.

## MERGE Actor with Responsibility/Authority

Performance and permission/accountability collapse.

**Result:** FAIL.

## Actor as agency role over native identity

Preserves meaningful action attribution while allowing typed roles and separate authority/security semantics.

**Result:** PASS.

---

# 21. Core invariants

1. **Actor is contextual semantic agency, not an independent entity/root.**
2. **Actor attribution references a native referent/system identity; no parallel Actor identity is created.**
3. **Actor != Person, though a Person may play Actor role.**
4. **Actor != Account/Principal/User.**
5. **Actor != Subject.**
6. **Actor != Responsibility/Stewardship/Authority/Ownership.**
7. **Actor does not replace specific roles such as performer, recorder, observer, confirmer or proposer.**
8. **No Account is required to preserve agency attribution.**
9. **Current access != historical Actor attribution.**
10. **AI/software may be Actors when domain-material agency exists, but technical processes are not automatically domain Actors.**
11. **AI Actor attribution does not create human Confirmation, authority or responsibility.**
12. **Visibility of a target does not imply visibility of all Actor/delegation details.**

---

# 22. Persistence/API implications — deliberately not physical design

Future logical modeling must support, where relevant:

- typed action-role references to native Person/system/etc. identities;
- Account/Principal/authentication context separately from Actor identity;
- on-behalf-of/delegation relationships;
- historical actor attribution;
- provenance references to material agents;
- actor-scoped privacy/visibility.

Do not infer from Actor v0 that LifeOS requires:

- one `actors` table;
- one universal `actor_id` field on every record;
- universal inheritance from Actor;
- every automation/process becoming a domain Actor;
- Actor = Person or Account;
- final Principal/authorization schema now.

---

# 23. Deliberately deferred questions

- native Organization/system/service/AI identity shapes;
- Principal/authenticated security identity;
- delegated/on-behalf-of authority;
- Participation/Responsibility/Performer/Assignment/Stewardship;
- Authority/Visibility/consent;
- precise actor-role relationship representation;
- Account/auth-provider linkage;
- deletion/retention/anonymization;
- logical typed-reference mechanism.

These are dependencies, not reasons to create a universal Actor entity.

---

# 24. Reopening triggers

Reopen Actor v0 if later evidence shows that:

1. agency cannot be represented through typed contextual roles without a distinct Actor identity;
2. a future Organization/system identity model requires a shared native entity that materially changes Actor semantics;
3. Responsibility/Authority modeling proves Actor is redundant or incorrectly bounded;
4. logical persistence pressure requires a different semantic model rather than merely a different typed-reference mechanism;
5. delegated AI/service action cannot preserve attribution and authority boundaries under this role-based model.

Until then, Actor remains the current accepted semantic agency role/capability.