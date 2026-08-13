# Multi-Actor Readiness v1

**Status:** Current cross-cutting domain guardrail  
**Established:** 2026-08-11  
**Current revision:** 2026-08-13 — Reconciliation / Source Precedence v0 incorporated  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS is personal-first in product experience while the domain kernel remains structurally capable of representing multiple independent actors, shared facts, actor-scoped context, partial adoption, selective disclosure, bounded Authority, represented action, material-state divergence and unresolved conflict.

This document is the current operational guardrail. Historical evidence remains in the dedicated discovery, research and validation checkpoints.

> **Coordinate shared reality without merging independent actors into one identity, one truth, one privacy boundary or one universal workflow.**

---

# 1. Core non-collapse baseline

```text
Person != Account != Principal
Actor != Account / Principal
actual Actor != represented party
Subject != Actor
Participation != Responsibility
Authority != Visibility
Authority != truth
Visibility != Consent
Acknowledgement != Agreement / Consent
Decision != Agreement / Consent
Version != current-state selection
Provenance != source precedence
Reconciliation != Decision / Authority / Actual / Version
```

Coincidence in simple personal flows is convenience, not ontology.

---

# 2. Shared fact + actor-scoped state

A shared real-world object should normally remain one shared object while actor-specific context stays separate.

Actor-scoped state may include:

- Participation response;
- private constraints/preferences;
- private notes/reminders;
- actor-specific Acknowledgement;
- individual Agreement/Consent state;
- private Visibility choices;
- competing assertions or stances.

> **A shared current result does not imply every actor saw, asserted, accepted, agreed, consented or decided the same thing.**

---

# 3. Account independence / partial adoption

Relevant Persons and Actors can exist without LifeOS Accounts.

Core semantics must support full users, occasional users, external responders, represented parties and external systems without fabricating Accounts merely for domain representation.

---

# 4. Participation and Responsibility

```text
Invitation / proposal
!= Participation response
!= Actual Participation
```

```text
Responsibility
!= actual performer
!= Participation
!= Authority
```

Activity identity must survive reassignment, claim, substitution and hand-off where the Activity itself remains the same.

Open/claimable Responsibility is legitimate. A transfer request is not automatically an effective transfer.

Coordination burden may remain with a different actor than execution Responsibility. `Coordination Stewardship` remains a review target, not an accepted standalone primitive.

---

# 5. Common-ground separation

Where consequence requires precision:

```text
proposed / sent
!= delivered / displayed
!= seen
!= Acknowledgement
!= family-specific response
!= Agreement / Consent
!= Approval / Decision
!= effective target state
!= Actual
```

Ordinary UI may collapse low-consequence steps, but the kernel must not lose the semantic distinction.

---

# 6. Authority and represented action

Authority is contextual and bounded.

```text
Authority != Actor / Account / Principal
Authority != Responsibility / Participation
Authority != Visibility
Authority != Agreement / Consent
Authority != Decision
Authority != truth
```

Representation preserves the actual Actor and the distinct represented party.

```text
Authority to action X
!= Authority to action Y
```

Represented action does not fabricate the represented party's personal Acknowledgement, Confirmation, Agreement, Consent or Decision.

Re-delegation is not implied.

---

# 7. Visibility and inference privacy

```text
can see != can change
can see != can re-disclose
can see != use for every purpose
may see != actually saw
visible result != visible source
visible current state != visible full history
```

Useful coordination may expose a bounded consequence while private source context remains hidden.

AI explanations and derived outputs must be reviewed for inference leakage, not only direct field exposure.

---

# 8. Version / material state

```text
shared/native identity
!= material state
!= actor-scoped semantic state
!= provider/storage revision
```

Rules:

- semantic acts remain bound to the material state they actually concerned;
- materiality is purpose/facet specific;
- provider/storage revisions are not semantic Version by default;
- divergent/offline states may coexist;
- projection Version and source Version may differ;
- stale-base AI/system effects require re-evaluation when material divergence matters;
- history does not imply indefinite retention of sensitive payloads.

Version identifies competing states; it does not choose the winner.

---

# 9. Reconciliation / Source Precedence

Reconciliation v0 provides the current conflict-handling discipline.

```text
Version
= identifies materially competing states

Provenance
= explains origin/evolution

Evidence
= may support or contradict interpretations

Authority
= determines legitimate bounded effect

Decision
= one possible bounded resolution path

Reconciliation
= handles materially competing states/assertions under an applicable bounded basis
```

Mandatory rules:

1. conflict detection != conflict resolution;
2. unresolved conflict is valid reality;
3. newer/more recent/more frequent input does not automatically win;
4. source identity, Provenance and recency do not create Authority or truth;
5. Source Precedence, when justified, is target/facet/purpose/context/time scoped;
6. there is no global source ranking;
7. a shared current result does not erase actor-specific assertions or historical competing Versions;
8. compatible independent changes may be combined where semantics permit;
9. material same-facet conflicts require explicit handling or remain unresolved;
10. deterministic resolution may occur without fabricating a human Decision only under explicit bounded policy and applicable Authority;
11. represented Reconciliation preserves actual Actor, represented party and basis;
12. result Visibility does not automatically expose private competing sources, rationale or Provenance;
13. AI may detect, compare and propose, but may not silently invent precedence or canonical truth;
14. specialist source-of-record precedence remains bounded to its actual context;
15. technical merge/sync/concurrency mechanics do not become domain Reconciliation semantics.

Rejected universal rules:

```text
last-write-wins
newest-source-wins
provider-always-wins
user-always-wins
AI-confidence-wins
universal Reconciliation root
universal Conflict root
universal SourcePrecedence hierarchy
```

---

# 10. Lifecycle / revocation / disagreement

Participation, Responsibility, Visibility, Authority, Representation and Consent have separate lifecycles.

- ending future access does not erase truthful historical attribution;
- historical participation does not imply future Visibility or Authority;
- revocation changes future capability without rewriting past valid action;
- disagreement may remain explicitly unresolved;
- auditability must not become unlimited surveillance.

---

# 11. Groups and Resource coordination

Group membership must not imply access, Participation, Agreement, Consent or governance over every object.

`Group`, `Household`, `Team`, `Organization` and `Workspace` remain separately reviewable.

Resource/Capacity truth remains separate from Participation, Responsibility, Schedule and Authority. Requirement/allocation/reservation/substitution remain future review targets.

---

# 12. AI guardrails

```text
AI proposal != human Decision
AI inference != human Agreement / Consent / Acknowledgement
AI capability != Authority
AI confidence != source precedence
AI source access != disclosure permission
```

AI may detect conflict, compare Evidence, summarize changes, propose options and request missing human action.

AI may not exceed bounded Authority, fabricate human state, apply stale-base effects after material divergence without re-evaluation, or convert uncertainty into false certainty.

---

# 13. Product simplicity / coordination burden

Kernel precision must not force enterprise workflow into ordinary UI.

For every collaborative capability ask:

```text
Who sets it up?
Who maintains it?
Who gets notified?
Who must review/acknowledge?
Who monitors failure?
Who repairs exceptions?
Who receives the benefit?
```

Expose collaboration/reconciliation machinery only when consequence, uncertainty, trust or user choice justifies it.

---

# 14. Mandatory validation questions

Every future multi-actor concept/feature must answer the applicable subset:

1. Can relevant actors exist without Accounts?
2. What is the shared canonical fact/object?
3. What remains actor-private?
4. Who is Actor, Subject, participant, responsible party, performer and Authority holder?
5. Can those roles change without changing object identity?
6. What actor-scoped state exists separately from shared state?
7. Did a proposed hand-off actually become effective?
8. Which material Version did each semantic act concern?
9. What may be exposed versus inferred?
10. Who actually acted if the action was on behalf of another party?
11. What happens when actors/providers disagree?
12. Is there a valid bounded source-precedence policy or must conflict remain unresolved?
13. Does a shared result preserve individual assertions/states?
14. Is an external specialist system authoritative for this bounded facet?
15. Does AI have sufficient Authority and safe disclosure scope?
16. Can revocation change future capability without deleting truthful history?
17. Is retention proportional to purpose?
18. Does the feature reduce total coordination burden?
19. Can low-consequence UX hide unnecessary machinery?
20. Does any implementation convenience accidentally create a universal root/ranking/workflow?

---

# 15. Explicitly deferred architecture

This readiness baseline does not select:

- final Person/Actor/Account/Principal physical model;
- organization/team/household hierarchy;
- ACL/RBAC/ABAC/ReBAC architecture or vendor;
- universal workflow/collaboration graph;
- CRDT/OT/merge implementation;
- universal source ranking;
- messaging/federation architecture;
- AI multi-agent orchestration;
- universal audit retention;
- final SQL/API representation.

---

# 16. Current canonical direction

```text
PERSONAL-FIRST PRODUCT
+
MULTI-ACTOR-READY DOMAIN
+
SHARED FACTS WITH ACTOR-SCOPED OVERLAYS
+
SELECTIVE / PURPOSE-AWARE DISCLOSURE
+
TRUTHFUL ACTOR / REPRESENTATION / AUTHORITY / PROVENANCE
+
VERSION-AWARE HISTORY
+
CONFLICT-PRESERVING RECONCILIATION
+
PARTIAL-ADOPTION SUPPORT
+
PROGRESSIVE DISCLOSURE
=
CURRENT LIFEOS MULTI-ACTOR FOUNDATION
```

No prior accepted concept is reopened by this revision.

---

# 17. Reopening rule

Reopen only when stronger evidence shows that a current non-collapse rule is wrong, an accepted concept cannot naturally represent realistic multi-actor behavior, a missing concept has materially independent semantics, or later logical/API/privacy/safety pressure exposes an actual semantic contradiction.

Provider/framework vocabulary alone is never sufficient.
