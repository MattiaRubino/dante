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

# 17. External and partial participation are normal

Collaboration must assume partial adoption.

Potential participation modes include:

```text
full LifeOS user
occasional LifeOS user
bounded link/web responder
email/SMS/other external channel
assisted participant
represented non-interacting subject
external system/provider
```

This is not a commitment to implement every channel.

Canonical requirement:

> **Core coordination semantics must not depend on every actor maintaining a full LifeOS account and full LifeOS client.**

---

# 18. Assisted participation must preserve truthful attribution

If one actor helps another person interact with LifeOS, LifeOS must not silently record the helper's action as if the subject personally asserted it.

Future provenance should be able to distinguish concepts such as:

```text
subject
actor who entered/performed
actor who confirmed/approved
source/provider
```

Exact persistence belongs to Provenance/Authority review.

---

# 19. Access, participation, responsibility and history have separate lifecycles

Real relationships change:

- actors join late;
- participation ends;
- responsibility transfers;
- access is narrowed;
- access is revoked;
- temporary substitutes leave;
- relationships end;
- relationships remain operational but hostile.

Canonical rule:

> **Ending future access must not require deleting truthful historical attribution.**

Likewise:

> **Historical participation does not imply future visibility or authority.**

---

# 20. Revocation is a first-class lifecycle requirement

The evidence shows that revocation can be a safety operation, not merely a friendly membership edit.

Future design must support at least conceptually:

- review of current sharing/access;
- scoped reduction of sharing;
- immediate revocation where justified;
- removal of future AI/context/notification access;
- preservation of legitimate historical attribution;
- separation from continuing real-world obligations.

Do not assume:

```text
leave group
=
all relationship obligations disappear
```

---

# 21. High-conflict ongoing relationships are distinct

Some relationships cannot simply terminate even when trust is low.

Examples include some post-separation parenting or legally/operationally required coordination.

The system must therefore be capable of supporting bounded, auditable coordination without assuming friendship, consensus or relational closeness.

Guardrails:

- minimize unnecessary interaction;
- avoid making auditability equivalent to unlimited surveillance;
- preserve dispute/uncertainty where reality is contested;
- do not assume communication tooling reduces conflict merely because it structures messages.

---

# 22. Groups are containers, not automatic sharing domains

A family, friend group, team, club or care circle can reduce repeated setup.

But membership must not imply:

```text
access to every object
automatic participation in every Event
ownership of every shared fact
full visibility into everyone's personal LifeOS
```

Canonical rule:

> **Group membership and object-specific participation/access remain distinct semantics.**

Whether `Group`, `Household`, `Team`, `Organization` or `Workspace` deserve separate domain primitives remains deferred.

---

# 23. Resource coordination is part of multi-actor reality

People often coordinate because of resources:

- meeting room;
- car;
- shared equipment;
- operating room;
- camera;
- accommodation capacity;
- tickets;
- stock/materials;
- facilities.

The existing Availability & Capacity model is structurally compatible because it operates on schedulable resources rather than one mandatory user.

Future Resource identity belongs to the Data/Subjects cluster.

---

# 24. Session and collaborative execution

A Session can represent one logically continuous collaborative execution episode.

Example:

```text
Activity
Move sofa upstairs

Session envelope
17:00-17:30

Mattia participation
17:00-17:30

Luca participation
17:05-17:25
```

LifeOS must not infer identical actor participation duration from the Session envelope.

Conversely, simultaneous independent attempts against the same Activity may require separate Sessions.

Canonical rule:

> **Session identity follows logical execution continuity, not performer count or timestamp overlap alone.**

Actor-specific execution attribution remains deferred to Actual/Relationship work.

---

# 25. Specialist-system authority remains outside LifeOS where appropriate

The multi-actor simulations include healthcare, school, workforce, legal and operational cases as **stress tests**, not as product-scope commitments.

LifeOS should coordinate around specialist facts while preserving external authority where appropriate.

Examples:

- hospital clinical systems;
- school information systems;
- workforce/rostering systems;
- legal matter systems;
- accounting systems.

Canonical guardrail:

> **Multi-actor readiness must not turn LifeOS into every specialist system.**

---

# 26. Coordination burden is a validation dimension

A technically expressive collaboration feature can still be a product failure.

For every future collaborative capability ask:

```text
Who performs setup?
Who maintains state?
Who receives notifications?
Who must acknowledge changes?
Who monitors failures?
Who repairs exceptions?
Who receives the main benefit?
```

Canonical product requirement:

> **Evaluate coordination cost per actor, not only feature capability or organizer convenience.**

A feature that saves one organizer five clicks by giving six participants a maintenance job may be a net regression.

---

# 27. Progressive disclosure is mandatory for collaboration

The kernel may distinguish responsibility, acknowledgement, authority, provenance and privacy without exposing enterprise workflow in casual life.

Examples:

### Casual social plan

```text
Dinner Saturday?
Yes / Maybe / No
```

### Professional shift swap

```text
Request
Recipient acceptance
Manager approval
Canonical change
```

### Sensitive care

May additionally require explicit source, confirmation and hand-off evidence.

Canonical rule:

> **Consequence determines required coordination formality.**

---

# 28. Current first-two-cluster result

After discovery simulation + external research + adversarial evidence synthesis:

```text
Intention & Execution v0
PASS — no structural reopening

Time v0
PASS — no structural reopening

Multi-Actor Readiness
PASS WITH EVIDENCE-BACKED HARDENING
```

No accepted concept requires removal or merge.

No new mandatory kernel primitive is introduced by this synthesis.

The existing decompositions remain useful:

```text
Activity != assignment
Event != participation
Schedule != participant acceptance
Schedule != Capacity
Occurrence != assignment
Session != performer
Constraint != authority
```

---

# 29. Strong future review requirements

The evidence materially raises the importance of later reviews of:

```text
Actual / Outcome
Observation / Evidence / Confirmation
Provenance
Subject / Person / Actor
Resource
Relationship
Responsibility / Assignment / Hand-off
Authority
Visibility / sharing lifecycle
Decision / Version
AI Proposal / context selection
```

These are review targets, **not a pre-approved list of database tables**.

---

# 30. Explicitly deferred architecture

This readiness baseline does not select:

- Actor/Person physical model;
- organization/team/household/workspace hierarchy;
- ACL/RBAC/ABAC/ReBAC architecture;
- Zanzibar/OpenFGA or any authorization vendor/model;
- invitation protocol;
- group chat/messaging architecture;
- collaborative editor/CRDT model;
- federation;
- universal workflow engine;
- AI multi-agent orchestration;
- specialist clinical/legal/workforce administration;
- universal fairness score;
- universal audit retention.

Those choices require later evidence and implementation pressure.

---

# 31. Mandatory multi-actor validation questions

Every future concept or collaborative feature must answer the applicable subset:

1. Can relevant people exist without LifeOS accounts?
2. What is the shared canonical fact?
3. What remains actor-private/personal?
4. What dependency requires coordination?
5. Who is participant, subject, responsible actor, performer and authority?
6. Can those roles change without changing object identity?
7. Is responsibility assigned, open/claimable, delegated or substituted?
8. Did responsibility transfer actually get accepted/effectively applied?
9. Is state proposed, delivered, acknowledged, agreed, authoritative or Actual?
10. Whose capacity/resources are affected?
11. Can coordination use a derived consequence instead of private source disclosure?
12. What can another actor infer even if raw fields are hidden?
13. What authority does the creator actually have?
14. What authority does the acting AI actually have?
15. Can access/revocation change without destroying historical attribution?
16. What happens if the relationship becomes hostile or high-conflict?
17. Can essential participation work through a simpler/assisted channel?
18. If assisted, is actor/source attribution truthful?
19. Does the feature reduce total coordination burden or redistribute it unfairly?
20. Is a persistent group even necessary, or would one bounded shared item be simpler?
21. Is specialist external software the true authority?
22. Is evidence retention proportional to the coordination purpose?
23. Does the flow preserve uncertainty/conflict instead of fabricating one truth?
24. Does AI explanation leak private causes?
25. Can the simple-user experience hide unnecessary coordination machinery?

---

# 32. Reopening rule

This baseline is intentionally strong but not immutable.

Reopen it only when new evidence demonstrates at least one of:

- a current non-collapse rule is wrong;
- a missing concept has materially distinct identity/lifecycle/authority/query semantics;
- an accepted concept cannot represent a realistic multi-actor case naturally;
- later persistence/API work exposes a contradiction rather than mere implementation inconvenience;
- legal/safety requirements materially change a semantic assumption.

Do not reopen it merely because a provider or competitor uses different vocabulary.

---

# 33. Current canonical direction

```text
PERSONAL-FIRST PRODUCT
        +
MULTI-ACTOR-READY DOMAIN
        +
SHARED FACTS WITH PERSONAL OVERLAYS
        +
SELECTIVE / PURPOSE-AWARE DISCLOSURE
        +
TRUTHFUL RESPONSIBILITY / AUTHORITY / PROVENANCE
        +
PARTIAL-ADOPTION SUPPORT
        +
PROGRESSIVE DISCLOSURE
        =
CURRENT LIFEOS MULTI-ACTOR FOUNDATION
```

Full collaboration features remain future product work. Structural multi-actor readiness is now a current kernel requirement.

---

# 2026-08-12 — Acknowledgement / generic Acceptance downstream hardening

Acknowledgement v0 turns one previously provisional common-ground distinction into a canonical boundary without selecting messaging/read-receipt infrastructure.

Current canonical decomposition:

```text
delivery/read/display evidence
!= Acknowledgement

Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request

Acknowledgement
!= understanding
!= Confirmation
!= Participation response
!= Responsibility
!= Authority / Decision / effective change
!= Actual
```

Generic cross-domain `Acceptance` is rejected as a standalone primitive. Existing `accepted` wording in this readiness document is interpreted through the owning family/workflow:

```text
participant accepted
→ Participation response

hand-off recipient accepted
→ Responsibility-specific response/operation

proposal accepted/applied
→ proposal/effect-specific response/operation
```

This also strengthens several existing readiness questions without changing their original intent:

- section 7 common-ground separation now has a canonical `Acknowledgement` owner;
- section 12 hand-off can distinguish request/receipt/Acknowledgement/role-specific response/effect;
- section 18 assisted participation must preserve who actually acknowledged versus the represented Person;
- section 26 coordination-burden review must ask whether explicit Acknowledgement is justified by consequence;
- section 27 progressive disclosure may expose `Got it` without forcing formal workflow everywhere;
- section 31 questions 8–9 must treat generic `accepted` as family-specific response rather than one universal kernel status.

Agreement, Consent, Decision, Principal/delegation, Version, collective semantics and read/view audit persistence remain independently reviewable. This amendment introduces no collaboration infrastructure and requires no reopening of the evidence-backed readiness baseline.

---

# 2026-08-13 — Decision / Approval / Reconciliation downstream hardening

Decision v0 closes another multi-actor separation that this readiness baseline intentionally left provisional.

Current canonical resolution chain where consequence requires it:

```text
proposal / request
!= delivered/read
!= Acknowledgement
!= family-specific response / future Agreement or Consent
!= Approval / Decision
!= effective target state
!= Actual
```

Canonical Decision boundary:

```text
Decision
= bounded contextual resolution to a specific result
  for a defined target/material version/context

Decision != Authority
Decision != effective target state
Decision != Actual/truth
Decision != Provenance/rationale
Decision != Evidence
Decision != Agreement/Consent
```

Multi-actor hardenings:

- one Actor's position/Approval does not automatically become the shared Decision;
- a shared Decision does not imply every Actor agreed or consented;
- an authoritative manager/guardian/specialist Decision must not be laundered into another person's Agreement/Consent;
- Approval is scoped Decision/review-result semantics whose effect depends on applicable Authority/policy;
- Decision result Visibility can differ from rationale/Evidence/Provenance Visibility;
- assisted/on-behalf-of flows must preserve the actual decision Actor/process, represented party and applicable basis;
- reversed/superseded Decisions remain historical facts where material;
- AI recommendation/proposal is not a human Decision;
- AI/system Decision semantics require explicit bounded policy/Authority and truthful attribution;
- low-consequence collaboration must not be inflated into mandatory approval/Decision bureaucracy.

Reconciliation remains a process/pattern, not a universal primitive. It may culminate in a Decision or remain unresolved. The affected domain concept owns any effective state change; no universal `EffectiveChange` root is introduced.

Agreement/Consent, Principal/delegation, Version/material equivalence, collective Decision formation, proposal identity, detailed reconciliation policy and evaluation semantics remain independently reviewable. No prior multi-actor readiness invariant is reopened.

---

# 2026-08-13 — Agreement / Consent downstream hardening

Agreement / Consent v0 closes mutual-assent and bounded-permission boundaries while preserving the existing multi-actor foundation.

Canonical separation:

```text
Acknowledgement
= explicit taking-notice

Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure under scope/purpose/context

Decision
= bounded resolution

Authority
= legitimate governance power

Visibility
= bounded exposure capability
```

Multi-actor hardenings:

- one Actor's positive response does not establish multi-party Agreement;
- a shared Decision does not manufacture Agreement or Consent;
- Agreement does not create Authority, Responsibility or automatic Visibility;
- Consent may be a bounded policy basis/constraint without becoming Authority or Visibility;
- Consent scope/purpose must not silently expand;
- withdrawal changes future applicability without erasing prior legitimate disclosure/use history;
- household/group/relationship membership does not imply Consent;
- helper/caregiver/representative action must preserve actual Actor, represented party and basis rather than silently becoming the represented Person's personal assent/Consent;
- unequal-power acknowledgement/compliance must not be relabeled voluntary/legal Consent automatically;
- AI may request/surface applicable Consent but cannot infer, fabricate or enlarge human Agreement/Consent from behavior, access or probability;
- legal/clinical validity and formal Contract/signature lifecycle remain specialist boundaries;
- ordinary low-risk collaboration must not become mandatory Agreement/Consent ceremony.

Generic cross-domain Acceptance/Assent remains rejected; universal Contract and universal Consent/Permission roots are not introduced.

---

# 2026-08-13 — Representation / on-behalf-of downstream hardening

Representation v0 closes the assisted/delegated action attribution boundary without turning LifeOS into IAM, legal-representation software or a universal delegation engine.

Current canonical decomposition:

```text
actual Actor
= who/what actually acts semantically

represented party
= distinct party for whom the Actor acts in a bounded action/context

Representation / on-behalf-of
= action-scoped relation connecting those two

Principal
= technical security/request identity

Authority / delegation basis
= whether the represented action may legitimately produce its bounded effect
```

Mandatory multi-actor hardenings:

```text
actual Actor != represented party
actual Actor != Principal by definition
Representation != Authority
Representation != Responsibility
Representation != Subject/beneficiary
Representation != Provenance
```

Assisted/caregiver/assistant/manager/AI flows must preserve truthful attribution:

- a helper acting for another Person does not become that Person;
- Authority concerning a child/employee/cared-for Person does not automatically manufacture that Person's personal Acknowledgement, Agreement, Consent, Confirmation or Decision;
- representation is action-specific: Authority to schedule does not imply Authority to consent, agree, disclose, acknowledge, decide or re-delegate;
- re-delegation is not implied;
- expiry/revocation narrows future authority while preserving truthful action-time history;
- a representative may be accountless; no synthetic Account is required;
- a visible represented effect does not imply visibility of private representation/delegation basis/history;
- claimed representation may be disputed and must not become established Authority merely because the actor asserted it;
- AI/service action under bounded policy remains attributed to the AI/service Actor where material and is never laundered into human authorship or will;
- technical impersonation/shared credentials may be implementation mechanisms but must not rewrite domain attribution where the material actual Actor is known.

Product guardrail:

> **Representation detail is consequence-sensitive. Ordinary self-use should not expose proxy/delegation machinery merely because the kernel can represent it.**

Principal/AuthN/AuthZ implementation, action-specific policy mechanics, legal capacity/power-of-attorney, multi-hop delegation, Version/material scope, collective representation, Verification of basis and retention/audit remain independently SAFE DEFERRED.

No prior Multi-Actor Readiness invariant is reopened.

---

# 2026-08-13 — Version / material-equivalence downstream hardening

Version v0 closes the cross-cutting material-state ambiguity that already appeared throughout multi-actor coordination without turning collaboration state into a universal workflow/version engine.

Canonical separation:

```text
shared/native object identity
!= material state of that object
!= actor-scoped semantic state
!= provider/storage revision

Version
= reference to the materially relevant state for the purpose/facet that currently matters
```

Mandatory multi-actor hardenings:

- a shared object's material revision does not silently carry every participant response, Acknowledgement, Confirmation, Agreement, Consent or Decision to the new state;
- actor-scoped states remain bound to the material target state they actually concerned;
- one actor/provider's newer technical revision does not automatically become shared canonical truth;
- non-linear/offline divergent states may coexist until applicable reconciliation/Authority/Decision establishes or constructs current state;
- Version itself never selects the winning actor/provider state and never creates Authority;
- a visible derived projection may remain materially equivalent for the recipient even when a hidden private source changes, so projection Version != private source Version automatically;
- selective disclosure of current state does not imply access to all historical Versions, source payloads, conflicting branches, delegation basis or private rationale;
- revocation/relationship change may alter future access without erasing materially required historical state attribution;
- AI proposals/effects must preserve the material base state where stale application could overwrite newer actor/domain intent; after material divergence they require re-evaluation rather than silent application;
- represented/on-behalf-of actions bind to the materially relevant target/scope state without turning Version into Representation or Authority;
- provider ETags, sync revisions, storage row versions and hashes may support concurrency/lineage but are not semantic Version by themselves;
- historical reconstructibility does not justify indefinite retention of sensitive payloads.

Product guardrail:

> **Version semantics should normally remain invisible unless the user needs to understand a meaningful change, conflict, stale proposal, prior assent, correction, or historical basis.**

The readiness baseline still does not pre-approve universal Version tables, event sourcing, CRDT/collaborative-editor architecture, provider-specific sequence semantics, one global material-equivalence function, or a generic collaboration workflow state machine.

Detailed reconciliation/source precedence, Proposal/request identity, GoalCriterion/evaluation, Trigger/automation, Principal/AuthN/AuthZ, collective/group/quorum semantics, Verification/comprehension, retention/audit and physical persistence remain independently reviewable.

No prior Multi-Actor Readiness invariant is reopened.