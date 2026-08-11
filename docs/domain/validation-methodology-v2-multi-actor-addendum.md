# Validation Methodology v2 — Multi-Actor Addendum

**Status:** Mandatory extension to current validation standard  
**Established:** 2026-08-11  
**Applies to:** all Domain Atlas concept reviews, cluster checkpoints, and final domain validation

## Purpose

Validation Methodology v2 remains fully in force.

This addendum adds one mandatory cross-cutting test because LifeOS is now explicitly required to remain personal-first in UX while being multi-actor-ready in its domain kernel.

Nothing in this addendum requires full collaboration features to be implemented now.

It prevents new concepts from silently embedding single-user assumptions that would later force structural redesign.

---

# Multi-Actor / Collaboration Compatibility Test

Every new or reopened Domain Atlas concept must be tested against the following questions where relevant.

## Identity

- Does concept identity accidentally depend on one user/account?
- Can the relevant actor change without forcing a new domain object?
- Can one shared real-world object exist without being duplicated per user?
- Can a non-LifeOS actor participate in the represented reality?

## Roles and relationships

- Who owns/stewards the object?
- Who participates?
- Who is responsible?
- Who is assigned?
- Who actually performs?
- Who or what is the subject/beneficiary?
- Which of those relations are genuinely distinct?

The test must not assume that one Actor occupies all roles.

## Shared versus actor-scoped state

- Which state is canonical/shared?
- Which state belongs to one actor's relationship with the shared object?
- Can one actor's state change without silently changing the shared object?
- Can several actors hold conflicting but valid actor-scoped states simultaneously?

Examples include accepted/tentative/declined participation, personal reminders, private notes, individual capacity claims, and actor-specific execution attribution.

## Authority

- Who may create, revise, cancel, assign, approve, or override the object/rule?
- Is authority distinct from visibility and participation?
- What happens when actors disagree or concurrently change related state?
- Would an AI acting for one actor gain more authority than that actor actually has?

## Privacy / visibility

- Can private source data affect a shared decision without requiring source disclosure?
- Can the system expose a safe derived projection such as free/busy, eligibility, or aggregate state?
- Does the design accidentally make all actor-scoped state visible because the parent object is shared?

## Capacity and temporal effects

- Whose capacity is consumed or protected?
- Can one shared Schedule produce several independent resource claims?
- Can a participant decline without deleting the shared Event/Schedule?
- Can actor/resource availability be evaluated independently?

## Reality and provenance

- Who produced or asserted a fact?
- Who was actually present or performed execution?
- Can actor-specific Actual history differ from the shared episode/event history?
- Can correction authority differ from source/provenance?

## Account independence

- Does the model require every Actor to be a registered LifeOS account?
- Can external people, organizations, providers, teams, patients, clients, contractors, or other relevant identities exist before/onboarding?

If a concept requires `Account == Actor == Owner == Participant` to work, it fails this test unless that equality is a deliberate domain invariant for that specific concept.

---

# Required scenario ladder

Concept reviews do not need to simulate every collaboration feature, but each relevant cluster must include representative cases across increasing complexity.

```text
Level 0  personal / one actor
Level 1  social / friends
Level 2  household / shared chores/resources
Level 3  work meeting / assignment
Level 4  team Goal/Plan / responsibility
Level 5  caregiving / actor differs from subject
Level 6  specialist professional workflow
Level 7  multi-role / multi-resource operation
Level 8  external or non-LifeOS actors/providers
```

Examples may include:

- dinner or concert with friends;
- shared trip planning;
- household chore rotation;
- meeting with organizer/required/optional participants;
- Activity reassignment;
- shift swap;
- caregiver and assisted person;
- medical appointment;
- surgical team plus room/equipment;
- external contractor/provider participant.

The exact examples should vary with the concept under review.

---

# Mandatory reductio variants

For relevant concepts add these destructive tests to the existing Adversarial Reductio method.

## SINGLE OWNER UNIVERSALIZATION

Assume every object has exactly one user who is simultaneously owner, subject, assignee, performer, authority, and viewer.

If realistic cases break, those roles must remain separable.

## PER-USER DUPLICATION

Duplicate one shared real-world object for each participant.

Check whether this creates:

- competing canonical truth;
- duplicated Schedule/history;
- reconciliation problems;
- provider-sync ambiguity;
- inconsistent lifecycle.

If so, prefer shared identity plus actor-scoped state.

## PARTICIPANT-STATE COLLAPSE

Put participant response/attendance directly on the shared object.

If one participant can differ from another, actor-scoped state is required.

## ASSIGNMENT-AS-IDENTITY

Change assignee/responsible actor.

If the underlying intended work remains the same, assignment cannot define object identity.

## VISIBILITY-EQUALS-AUTHORITY

Assume anyone who can see an object can modify it.

If realistic cases fail, visibility and authority must remain distinct.

## PRIVATE-SOURCE-DISCLOSURE

Require source facts to be visible whenever their derived projection is used.

If free/busy, recommendation, eligibility, or aggregate reasoning can work without source disclosure, privacy-safe projection must remain possible.

---

# Classification

Use the following result classes during concept/cluster review:

- **MULTI-ACTOR PASS** — semantics already neutral and composable.
- **PASS WITH HARDENING** — concept remains valid but single-user wording/invariants must be generalized.
- **DEFERRED RELATIONSHIP DETAIL** — concept is sound, but actor/authority/visibility relationship shape belongs to later clusters.
- **STRUCTURAL REOPENING** — identity/lifecycle cannot support realistic multi-actor behavior without changing the concept.
- **NEW PRIMITIVE CANDIDATE** — repeated multi-actor semantics reveal materially distinct identity/lifecycle/invariants not covered by existing concepts.

A concept must not be failed merely because ACL/UI/invitations have not yet been designed.

The test is semantic readiness, not feature completeness.

---

# Product complexity rule

The existence of multi-actor semantics must not force personal users to configure collaboration structures.

Simple personal case:

```text
Buy milk tomorrow
```

must remain simple.

The kernel may internally support richer relationships without requiring UI such as:

```text
owner
participant
assignee
performer
authority
visibility
```

unless those distinctions are actually relevant.

This extends Validation Methodology v2's progressive-disclosure requirement.

---

# AI-specific rule

For any AI-assisted operation involving shared or actor-scoped state, validate:

1. whose context the AI is using;
2. which private facts the AI is allowed to read;
3. which derived facts it may disclose;
4. which objects it may modify;
5. whether the change needs another actor's approval;
6. whether a proposal is being confused with accepted canonical state.

Canonical requirement:

> **AI effective authority cannot exceed the acting principal's authority plus explicit approved policy.**

---

# Relationship to future Collaboration Discovery Simulation

This addendum is intentionally conservative.

A dedicated Collaboration Discovery Simulation will later provide deeper evidence across social, household, work, caregiving, specialist, organizational, and external-participant scenarios.

That simulation may:

- confirm these guardrails;
- refine terminology;
- expose new relationship/authority concepts;
- reopen an accepted concept;
- justify a new primitive.

Until then, all Domain Atlas work must treat this addendum and `multi-actor-readiness-v0.md` as the minimum collaboration-readiness baseline.
