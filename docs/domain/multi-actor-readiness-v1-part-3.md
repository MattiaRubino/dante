<!-- LIFEOS-CANONICAL-SPLIT document="multi-actor-readiness-v1.md" part="3" total="3" -->
> **Canonical document split — Part 3 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](multi-actor-readiness-v1.md) · [Part 2](multi-actor-readiness-v1-part-2.md) · **Part 3**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
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

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.


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


## 1. Core non-collapse baseline
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


## 2. Shared fact + actor-scoped state
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


## 3. Account independence / partial adoption
Relevant Persons and Actors can exist without LifeOS Accounts.

Core semantics must support full users, occasional users, external responders, represented parties and external systems without fabricating Accounts merely for domain representation.

---


## 4. Participation and Responsibility
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


## 5. Common-ground separation
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


## 6. Authority and represented action
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


## 7. Visibility and inference privacy
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


## 8. Version / material state
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


## 9. Reconciliation / Source Precedence
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


## 10. Lifecycle / revocation / disagreement
Participation, Responsibility, Visibility, Authority, Representation and Consent have separate lifecycles.

- ending future access does not erase truthful historical attribution;
- historical participation does not imply future Visibility or Authority;
- revocation changes future capability without rewriting past valid action;
- disagreement may remain explicitly unresolved;
- auditability must not become unlimited surveillance.

---


## 11. Groups and Resource coordination
Group membership must not imply access, Participation, Agreement, Consent or governance over every object.

`Group`, `Household`, `Team`, `Organization` and `Workspace` remain separately reviewable.

Resource/Capacity truth remains separate from Participation, Responsibility, Schedule and Authority. Requirement/allocation/reservation/substitution remain future review targets.

---


## 12. AI guardrails
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


## 13. Product simplicity / coordination burden
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


## 14. Mandatory validation questions
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


## 15. Explicitly deferred architecture
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


## 16. Current canonical direction
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


## 17. Reopening rule
Reopen only when stronger evidence shows that a current non-collapse rule is wrong, an accepted concept cannot naturally represent realistic multi-actor behavior, a missing concept has materially independent semantics, or later logical/API/privacy/safety pressure exposes an actual semantic contradiction.

Provider/framework vocabulary alone is never sufficient.

