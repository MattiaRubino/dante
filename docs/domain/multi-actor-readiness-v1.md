<!-- LIFEOS-CANONICAL-SPLIT document="multi-actor-readiness-v1.md" part="1" total="3" -->
> **Canonical document split — Part 1 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: **Part 1** · [Part 2](multi-actor-readiness-v1-part-2.md) · [Part 3](multi-actor-readiness-v1-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# Multi-Actor Readiness v1

**Status:** Current evidence-backed cross-cutting domain guardrail  
**Established:** 2026-08-11  
**Supersedes for current work:** `multi-actor-readiness-v0.md`  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS remains **personal-first in product experience**, but its domain kernel must be structurally capable of representing reality involving multiple people, external actors, shared facts, shared resources, unequal authority, partial adoption and private personal context.

Version 1 is evidence-backed by:

- the accepted first two Domain Atlas clusters;
- the initial Multi-Actor Readiness v0 hardening;
- `multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `multi-actor-collaboration-research-2026-08.md`;
- adversarial/safety evidence on revocation, high-conflict relationships, guardian/minor asymmetry, assisted participation and AI-mediated privacy.

The purpose remains deliberately narrower than implementing collaboration:

> **Preserve the semantic foundations required for future collaboration without prematurely designing organizations, ACL infrastructure, chat, enterprise workflow or a universal social layer.**

---

# 1. Evidence-backed product hypothesis

The strongest supported direction is:

> **LifeOS should coordinate shared reality among independent personal systems rather than merge multiple people's personal operating systems into one shared account or workspace by default.**

A multi-actor feature is valuable only when its coordination benefit exceeds the social, cognitive, privacy, accessibility and maintenance costs it creates for the actors involved.

This yields two simultaneous requirements:

```text
coordination must be expressive enough
```

and

```text
coordination must not become bureaucracy or surveillance
```

The kernel therefore preserves distinctions; the product exposes only the amount of structure justified by consequence and context.

---

# 2. Core non-collapse rule

The domain must not collapse the following dimensions into one `user_id`, one `owner`, one `member`, or one universal status field:

```text
object identity
person / actor identity
account / authenticated principal
subject / beneficiary
ownership / governance / stewardship
participation
participation response
responsibility
assignment
performer / actual contributor
coordination stewardship
visibility / access
authority
provenance / source
capacity/resource relationship
```

These dimensions may coincide in a simple personal case. Their coincidence is convenience, **not ontology**.

Canonical rule:

> **Domain object identity must not be defined by one account or actor merely because the initial product experience is personal-first.**

---

# 3. Shared canonical fact + personal overlay

When several actors coordinate around the same real-world object, LifeOS should normally preserve one shared canonical fact and separate actor-scoped personal context.

Example:

```text
Shared Event
Dinner · Saturday · 21:00 · Restaurant X
```

Possible shared facts:

```text
Event identity
accepted shared Schedule
place
shared description
shared lifecycle/disposition
```

Possible actor-scoped context:

```text
participation response
personal capacity impact
private constraints
travel/preparation
personal reminder
private note
private Goal relation
local organizational area
visibility choices
```

Preferred pattern:

```text
Shared object
        ├── canonical/shared facts
        ├── Actor A scoped state
        ├── Actor B scoped state
        └── Actor C scoped state
```

Avoid semantic duplication such as one independent copy of the same dinner/meeting/shift for every user unless the records genuinely represent independently governed realities or provider replicas.

---

# 4. Account, person, actor and subject are not interchangeable

A relevant person may exist in LifeOS domain reality without holding a LifeOS account.

Examples:

- friend invited to dinner;
- colleague attending a meeting;
- child or cared-for person;
- patient;
- mechanic;
- teacher;
- customer;
- contractor;
- supplier;
- model/subject in a photography job.

Therefore:

> **Participation and representation must not require universal LifeOS account adoption.**

Likewise, the person performing an action may differ from the person/thing the information concerns.

Examples:

```text
caregiver acts
older adult is subject
```

```text
parent coordinates
child is subject
```

```text
technician acts
vehicle is subject
```

The exact future `Person`, `Actor`, `Account`, `Principal`, `Subject`, `Resource`, `Organization` and `Team` boundaries remain deferred to dedicated reviews.

---

# 5. Shared object identity is independent from actor relationships

Current cross-cutting invariants:

```text
Goal identity       != governor / stakeholder / subject
Plan identity       != coordinator / contributor / responsible actor
Activity identity   != requester / assignee / performer
Event identity      != organizer / participant / participant response
Routine identity    != performer
Milestone identity  != stakeholder / approver / governor
Occurrence identity != assigned actor
Schedule identity   != participant acceptance / capacity owner
Session identity    != performer count
Constraint identity != authority actor
Recurrence identity != assignment rotation
Capacity identity   != one mandatory person/account
```

Actor relationships may change while object identity remains stable.

---

# 6. Participation is stateful, temporal and context-specific

Research strongly rejects `member / not member` as a sufficient universal model.

Depending on context, useful participation semantics may include:

```text
invited
unseen
needs action
tentative
accepted
declined
conditional
waitlisted
substituted
removed
attended
partially attended
absent
unknown
```

No universal enum is accepted here.

Canonical rule:

> **Participation intention/response and actual participation must remain distinguishable where both matter.**

For Events this reinforces the existing separation:

```text
Event state
!= participant response
!= actual attendance
```

---

# 7. Proposal, common ground, authority and reality are different

The multi-actor evidence materially strengthens this state separation:

```text
proposed / sent
!= delivered
!= seen
!= understood
!= acknowledged
!= accepted / agreed
!= authoritative / canonically confirmed
!= acted upon
!= actual outcome
```

Not every dinner or casual plan needs eight visible statuses.

The distinction is semantic, with product exposure proportional to consequence.

Examples:

### Casual dinner

A simple `accepted / declined / maybe` experience may be enough.

### Shift swap

```text
worker requests
→ recipient accepts
→ authorized manager approves
→ canonical shift assignment changes
→ Actual attendance later recorded
```

### Care hand-off

Sending a request does not prove another caregiver accepted responsibility.

Canonical rule:

> **Delivery, acknowledgement, agreement, authority confirmation and Actual must not be collapsed when failure to distinguish them can change responsibility or safety.**

---

# 8. Schedule acceptance is not participant acceptance

A shared Event can have one canonical Schedule while actors hold different participation states.

```text
Meeting
Schedule: 15:00-16:00

A: accepted
B: tentative
C: declined
```

Therefore:

> **The accepted Schedule is the currently canonical temporal assignment under the relevant governing authority/context; it does not mean every participant has accepted participation.**

This remains compatible with the existing Schedule v0 semantics.

---

# 9. Responsibility is richer than one assignee

The discovery simulation and external research repeatedly expose materially different responsibility questions:

```text
Who is accountable for the outcome?
Who is expected to perform the work?
Who can claim currently open work?
Who approves it?
Who is temporarily substituting?
Who must acknowledge a hand-off?
Who remains responsible if nobody acts?
```

Canonical hardening:

> **Activity identity must not be defined by one assignee, and future responsibility semantics must be capable of representing reassignment, claim, substitution and hand-off without rewriting Activity identity/history.**

This does **not** yet justify one universal Responsibility entity or workflow engine.

---

# 10. Execution responsibility and coordination stewardship differ

External research introduces an important qualification.

A visible task can be delegated while another person continues to perform the invisible coordination work:

- anticipating that it will be needed;
- remembering deadlines/preferences;
- prompting another person;
- monitoring whether the work happened;
- resolving failure;
- repairing the surrounding plan.

Example:

```text
Activity
Book child dentist appointment

Execution responsibility
Luca

Coordination stewardship
Mattia still remembers, reminds, monitors and replans
```

The phenomenon is real and must be preserved as a validation question.

Current decision:

> **Do not equate task assignment with transfer of coordination burden.**

However, `Coordination Stewardship` is **not yet accepted as a dedicated kernel primitive**. It may later become a relationship, responsibility dimension, derived measure, or product-evaluation concept.

---

# 11. Open / claimable responsibility is legitimate

Some real situations correctly begin as:

```text
Someone eligible/willing needs to take this
```

rather than:

```text
assigned_to = X
```

Examples:

- household chore;
- caregiving help request;
- open shift;
- volunteer role;
- shared trip responsibility.

The future model must not require a mandatory assignee merely to represent a valid open responsibility state.

---

# 12. Hand-off needs acceptance where responsibility matters

A hand-off has at least a potential distinction between:

```text
transfer requested
transfer received
transfer accepted
transfer authoritative/effective
```

For low-consequence contexts the product may collapse this interaction.

For care, shift work, child pickup, important deliverables or external service work, a requested transfer must not automatically be treated as effective responsibility transfer.

---

# 13. Availability may be shared without private calendar disclosure

Canonical rule:

> **Useful coordination may expose the consequence of private context without exposing the private source.**

Example:

```text
Private Event
Therapy 18:30-19:30
```

Safe shared projection:

```text
Unavailable 18:30-19:30
```

Not automatically safe:

```text
Unavailable because of therapy
```

This applies beyond calendar data to health, finance, preferences, relationships, location and AI inference.

---

# 14. Privacy includes inference, not only direct visibility

A system can hide raw source fields and still leak sensitive meaning through:

- explanations;
- recommendations;
- availability patterns;
- notification wording;
- AI responses;
- tool/API parameters;
- status changes;
- derived rankings.

Therefore:

> **Who may see a fact and who may infer a fact are distinct privacy questions.**

And:

> **AI informational access does not imply permission to disclose the information or its private cause.**

This becomes a mandatory future AI/context-builder validation dimension.

---

# 15. Authority is contextual and must not be laundered

Item creation, participation, visibility and ownership labels do not automatically grant real-world authority.

Examples:

- dinner organizer cannot expose guests' private reasons;
- parent/guardian authority may be legitimate in one child-safety context but not unlimited across every domain;
- manager may control a work shift without access to unrelated private health reasons;
- caregiver observation is not automatically clinical truth;
- AI proposal is not authoritative because the AI has broad context.

Canonical rule:

> **Authority must be represented according to the relevant relationship/context rather than inferred from who created the object or who can see it.**

---

# 16. AI authority is bounded

Canonical rule:

> **AI effective authority must not exceed the authority of the principal/context/policy under which it acts.**

AI may:

- calculate mutual feasibility from private projections;
- propose a common Schedule;
- highlight conflicts;
- request confirmation;
- explain safe high-level reasons.

AI may not automatically:

- reveal another actor's private source context;
- convert a proposal into agreement;
- treat optimization as institutional authority;
- modify a shared fact beyond the acting principal's authority;
- infer Actual merely because an expected time passed.

---

