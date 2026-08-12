# Multi-Actor Readiness v1

**Status:** Current evidence-backed cross-cutting domain guardrail  
**Established:** 2026-08-11  
**Current revision:** 2026-08-12 — Acknowledgement v0 downstream hardening integrated  
**Supersedes for current work:** `multi-actor-readiness-v0.md`  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS remains **personal-first in product experience**, while its domain kernel must represent reality involving multiple independent people, external actors, shared facts, shared resources, unequal Authority, partial adoption and private personal context.

Evidence basis:

- accepted Domain Atlas baselines;
- Multi-Actor Readiness v0;
- `../product/multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `../product/multi-actor-collaboration-research-2026-08.md`;
- `checkpoints/multi-actor-evidence-synthesis-v0.md`;
- later accepted Relationship / Responsibility / Participation / Authority / Visibility / Acknowledgement reviews.

The purpose is deliberately narrower than implementing collaboration:

> **Preserve the semantic foundations required for future coordination without prematurely designing organizations, ACL infrastructure, messaging, enterprise workflow or a universal social layer.**

---

# 1. Product hypothesis

LifeOS should coordinate shared reality among independent personal systems rather than merge several people's personal operating systems into one shared account/workspace by default.

A multi-actor capability is valuable only when its coordination benefit exceeds its social, cognitive, privacy, accessibility and maintenance cost.

```text
coordination expressive enough
+
coordination not bureaucracy/surveillance
```

The kernel preserves distinctions; the product exposes only the structure justified by consequence and context.

---

# 2. Core non-collapse rule

Do not collapse these dimensions into one `user_id`, owner/member field or universal status:

```text
object identity
Person / Actor
Account / Principal
Subject / beneficiary
ownership / governance / Stewardship
Participation
Participation response
Responsibility
Assignment / Claim / Hand-off
expected performer / Actual performer
coordination Stewardship
Visibility
Authority
Acknowledgement
Provenance / source
Resource / Capacity relationship
```

These may coincide in simple personal scenarios. Coincidence is convenience, **not ontology**.

---

# 3. Shared canonical fact + actor-scoped overlay

Prefer:

```text
one shared canonical object/fact
        +
actor-scoped personal context
```

Example:

```text
Shared Event
Dinner · Saturday · 21:00 · Restaurant X

shared:
Event identity
current Schedule
place
shared lifecycle

actor scoped:
Participation response
Acknowledgement of material change
capacity impact
private constraint
reminder/note
local organization
Visibility choices
```

Avoid per-user copies unless the records genuinely represent separately governed realities/provider replicas.

---

# 4. Person / Actor / Account / Principal / Subject remain distinct

A relevant Person may exist without a LifeOS Account.

Examples include friend, colleague, child, cared-for person, patient, teacher, contractor, technician or subject in a photography job.

Likewise:

```text
caregiver acts
older adult is Subject
```

```text
parent acts
child is represented Person/Subject
```

The acting Actor, represented Person, authenticated Principal and Authority basis may differ.

Participation, Responsibility, Acknowledgement and representation must not require universal LifeOS account adoption.

---

# 5. Shared-object identity is independent from actor relations

Current invariants include:

```text
Goal identity       != governor/stakeholder/subject
Plan identity       != coordinator/contributor/responsible actor
Activity identity   != requester/responsible/performer
Event identity      != organizer/participant/response
Routine identity    != performer
Milestone identity  != approver/governor
Occurrence identity != assigned actor
Schedule identity   != participant response/Acknowledgement/capacity owner
Session identity    != performer count
Constraint identity != Authority holder
```

Actor relationships may change while object identity remains stable.

---

# 6. Participation is stateful, temporal and contextual

Participation v0 owns intended/response and Actual involvement semantics.

```text
Invitation
!= Participation response
!= Actual Participation
```

Possible product states can include invited, tentative, accepted, declined, conditional, waitlisted, removed, attended, partial, absent or unknown, but no universal enum is accepted.

```text
accepted Participation != attended
```

`accepted` here is family-specific Participation-response language, **not** a universal Acceptance primitive.

---

# 7. Common ground, response, Authority and reality are different

Current stronger decomposition after Acknowledgement v0:

```text
proposed / sent
!= delivered
!= displayed/read
!= understood
!= Acknowledgement
!= family-specific response / future Agreement or Consent
!= Authority / Decision / effective canonical change
!= acted upon
!= Actual
```

Acknowledgement is now canonical:

```text
Acknowledgement
= actor-scoped explicit taking-notice
  of a specific target/material version/change/request
```

It does **not** prove comprehension, agreement, consent, Confirmation, Authority, effect or Actual.

Generic cross-domain `Acceptance` was tested and rejected as a standalone kernel primitive. Positive response remains with the semantic family/workflow that gives it meaning.

---

# 8. Schedule acceptance is not participant response or Acknowledgement

```text
Event
current Schedule: 15:00–16:00

A Participation response: accepted
B Participation response: tentative
C Participation response: declined
```

The current accepted Schedule is the canonical/effective temporal assignment under the applicable governing context. It does not mean every participant accepted Participation.

Likewise:

```text
current Schedule/change
!= Actor Acknowledgement of that change
```

---

# 9. Responsibility is richer than one assignee

Responsibility is accountability, not one `assigned_to` field.

Distinguish:

```text
requester
responsible actor
expected performer
Actual performer
open/claimable role
substitute
hand-off recipient
approver/Authority holder
coordination Stewardship
```

Current hand-off chronology may require:

```text
transfer requested
!= delivered/read
!= Acknowledgement
!= role-specific accepted response
!= authoritative/effective transfer
!= Actual performer
```

Assignment does not automatically transfer mental load/Stewardship.

---

# 10. Coordination Stewardship / mental load

Who anticipates, remembers, prompts, monitors and repairs may differ from the Responsibility holder or performer.

This remains a mandatory validation dimension.

Standalone `Coordination Stewardship` primitive status remains SAFE DEFERRED; evidence must prove independent state/lifecycle/query value before promotion.

---

# 11. Open/claimable responsibility is legitimate

```text
someone eligible/willing needs to take this
```

is not the same as unknown holder.

The model must support open/claimable work without inventing mandatory assignee identity.

---

# 12. Availability can be shared without source disclosure

```text
PRIVATE SOURCE
Therapy 18:30–19:30

SAFE PROJECTION
Unavailable 18:30–19:30
```

Useful coordination may expose a consequence without exposing the private reason/source.

This principle extends beyond calendar data to health, finance, relationships, location and AI inference.

---

# 13. Privacy includes inference

Hiding raw fields is insufficient if explanations, recommendations, rankings, notification wording, derived availability, AI responses or tool arguments expose the private cause.

> **AI/system knowledge does not create disclosure permission.**

Visibility(source) and Visibility(output/derived projection) are evaluated independently.

---

# 14. Authority is contextual and cannot be laundered

Creation, Participation, Visibility, Responsibility, ownership, Confirmation or Acknowledgement do not automatically grant domain Authority.

Examples:

- organizer cannot disclose every participant's private reason;
- manager may govern a work shift without seeing unrelated health data;
- caregiver observation is not automatically clinical truth;
- AI proposal is not authoritative because the AI has broad context.

```text
Actor action != Authority
Acknowledgement != Authority
family-specific response != Authority
```

---

# 15. AI Authority is bounded

> **AI effective Authority <= applicable acting Principal/context/policy Authority.**

AI may calculate, propose, highlight, request Confirmation/Acknowledgement, or explain safe high-level consequences.

AI must not silently:

- reveal another actor's private source;
- convert proposal into response/agreement;
- fabricate human Acknowledgement;
- treat optimization as institutional Authority;
- modify shared state beyond applicable Authority;
- infer Actual because expected time passed.

---

# 16. External and partial participation are ordinary

Potential interaction modes include:

```text
full LifeOS user
occasional user
bounded web/link responder
external communication channel
assisted participant
represented non-interacting Person
external specialist/provider system
```

This is semantic readiness, not a commitment to implement every channel.

---

# 17. Assisted/on-behalf-of interaction must preserve attribution

Where one actor helps another, distinguish where material:

```text
Subject / represented Person
actual acting Actor
asserted/acknowledged/confirmed by
Account / Principal used
Authority/on-behalf-of basis
performer
Provenance
```

A helper pressing `Acknowledge` must not silently become a personal Acknowledgement by the represented person.

---

# 18. Relationship lifecycle / revocation

Participation, Responsibility, Visibility, Authority and historical attribution have distinct lifecycles.

Real relationships may join, narrow, substitute, revoke, end or become hostile.

> **Ending future access must not delete truthful historical attribution.**

Likewise historical participation or Acknowledgement does not imply future Visibility/Authority.

---

# 19. High-conflict ongoing relationships

Some relationships cannot simply terminate even when trust is low.

Design must support bounded coordination without assuming consensus/friendship, avoid converting auditability into surveillance, preserve dispute/uncertainty, and minimize unnecessary interaction.

A forced Acknowledgement still means only recorded taking-notice; it must not be represented as Agreement/Consent.

---

# 20. Unequal power / guardian / caregiver

Authority can be asymmetric and context-bounded.

Do not infer unlimited access or erase subject autonomy because one actor is manager/guardian/caregiver/teacher/specialist.

Acknowledgement, Agreement, Consent and Authority remain separate questions, especially under power imbalance.

---

# 21. Groups are not automatic sharing/authority domains

Membership in family/team/club/care-circle does not imply:

```text
access to every object
automatic Participation
shared Responsibility
Authority over every member
Acknowledgement by every member
```

Group/Household/Team/Organization primitives remain deferred until independent identity/lifecycle value is proven.

---

# 22. Multi-resource / Capacity

People coordinate around rooms, vehicles, equipment, facilities, tickets, accommodation, stock and services.

One shared scheduled object must be able to create independent Capacity/Reservation pressure without duplicating the object.

Resource booking/capacity does not establish Participation, Responsibility or Acknowledgement.

---

# 23. Collaborative Session / Actual attribution

A shared Session envelope does not imply identical actor participation intervals.

```text
Session 17:00–17:30
Actor A participation 17:00–17:30
Actor B participation 17:05–17:25
```

Shared Actual and actor-specific Actual Participation remain independently attributable.

---

# 24. Specialist-system boundary

Healthcare, workforce, education, legal, finance and other high-risk scenarios are stress tests, not a mandate to rebuild specialist administration.

LifeOS should coordinate around specialist facts while preserving external Authority/source-of-record boundaries where appropriate.

---

# 25. Coordination burden is a validation dimension

For every collaborative capability ask:

```text
Who sets it up?
Who maintains state?
Who receives notifications?
Who must acknowledge/respond?
Who monitors failure?
Who repairs exceptions?
Who receives the primary benefit?
```

Evaluate total work and its distribution, not organizer efficiency alone.

Acknowledgement must therefore be **consequence-sensitive**, not a universal requirement.

---

# 26. Progressive disclosure is mandatory

Same semantic foundations can support different product formality:

```text
Dinner
Yes / Maybe / No
```

```text
Material schedule change
Got it
```

```text
Professional hand-off
Request
Acknowledgement
role-specific response
Approval/effect where required
```

Kernel precision must not force enterprise workflow into casual life.

---

# 27. Current accepted multi-actor decomposition

```text
who acts?                Actor
who is accountable?      Responsibility
who is involved?         Participation
who may govern?          Authority
who may see?             Visibility
who explicitly noticed?  Acknowledgement
what actually happened?  Actual
```

Open semantic areas such as Agreement, Consent, Decision, Principal/delegation, Version and collective semantics remain candidates/dependencies rather than assumed primitives.

---

# 28. Explicitly rejected/premature collaboration abstractions

Current evidence does not justify merely from multi-actor needs:

```text
universal User/Actor/Participant root
universal Relationship/social graph
universal Responsibility workflow
universal Acceptance/Assent root
universal acknowledgement/read-receipt state machine
universal Permission/ACL domain root
universal approval engine
organization/team hierarchy
chat/messaging architecture
Zanzibar/OpenFGA dependency
universal audit log visible to collaborators
AI multi-agent orchestration
universal fairness score
```

Each future capability must earn its place independently.

---

# 29. Mandatory multi-actor validation questions

Every future concept/feature must answer applicable questions:

1. Can relevant Persons exist without LifeOS Accounts?
2. What is the shared canonical fact?
3. What remains actor-private?
4. Which dependency requires coordination?
5. Who is Subject, Actor, participant, responsible actor, performer and Authority holder?
6. Can those roles change without changing object identity?
7. Is Responsibility assigned, open/claimable, delegated or substituted?
8. Did a transfer request get delivered/read, explicitly acknowledged, positively responded to and effectively applied as separate stages where consequence requires it?
9. Is state proposed, delivered/read, acknowledged, family-response/agreement, authoritative/effective, or Actual?
10. Whose Capacity/Resources are affected?
11. Can coordination share a derived consequence instead of private source?
12. What can another actor infer despite hidden raw fields?
13. What Authority does the creator actually have?
14. What Authority does acting AI actually have?
15. Can Visibility/revocation change without destroying historical attribution?
16. What happens under conflict/refusal/silence/hostility?
17. Can essential participation work through external/assisted channels?
18. If assisted, is actor/source/on-behalf-of attribution truthful?
19. Does the feature reduce total coordination burden or shift it unfairly?
20. Is persistent Group identity truly needed?
21. Is specialist external software the real Authority/source of record?
22. Is evidence/Acknowledgement retention proportional to purpose?
23. Does the flow preserve unknown/conflict instead of fabricating truth?
24. Does AI explanation leak private causes?
25. Can simple users avoid unnecessary coordination machinery?

---

# 30. Current readiness result

```text
PERSONAL-FIRST PRODUCT
        +
MULTI-ACTOR-READY DOMAIN
        +
SHARED FACTS WITH ACTOR-SCOPED OVERLAYS
        +
SELECTIVE / PURPOSE-AWARE DISCLOSURE
        +
TRUTHFUL RESPONSIBILITY / AUTHORITY / PROVENANCE
        +
EXPLICIT COMMON-GROUND SEPARATION
        +
PARTIAL-ADOPTION SUPPORT
        +
PROGRESSIVE DISCLOSURE
        =
CURRENT LIFEOS MULTI-ACTOR FOUNDATION
```

Structural multi-actor readiness is a current kernel requirement. Full collaboration implementation remains future product work.

---

# 31. Reopening rule

Reopen this readiness baseline only when new evidence demonstrates a current non-collapse rule is wrong, a missing concept has materially distinct identity/lifecycle/Authority/query semantics, an accepted concept cannot naturally represent a realistic multi-actor case, later persistence/API work exposes a semantic contradiction, or safety/legal evidence materially changes an assumption.

Do not reopen it merely because a provider/competitor uses different vocabulary.

---

# 32. Downstream hardening — Acknowledgement v0 (2026-08-12)

Acknowledgement v0 converts one previously provisional common-ground distinction into a canonical boundary without selecting messaging/read-receipt infrastructure.

Current hardening:

```text
delivery/read/display evidence
!= Acknowledgement

Acknowledgement
= explicit actor-scoped taking-notice
  of a specific target/material version/change/request

Acknowledgement
!= understanding
!= Confirmation
!= Participation response
!= Responsibility
!= Authority/Decision/effective change
!= Actual
```

Generic cross-domain `Acceptance` is rejected as a standalone primitive. Existing `accepted` wording in this readiness document must be interpreted through the owning family/workflow:

```text
participant accepted
→ Participation response

hand-off recipient accepted
→ Responsibility-specific response/operation

proposal accepted/applied
→ proposal/effect-specific response/operation
```

Agreement, Consent and Decision remain independently reviewable and are not collapsed into `Acceptance`.

This downstream hardening preserves the original evidence-based readiness findings while making the common-ground vocabulary consistent with the current Domain Atlas.
