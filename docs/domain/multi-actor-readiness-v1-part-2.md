<!-- LIFEOS-CANONICAL-SPLIT document="multi-actor-readiness-v1.md" part="2" total="3" -->
> **Canonical document split — Part 2 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](multi-actor-readiness-v1.md) · **Part 2** · [Part 3](multi-actor-readiness-v1-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
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

