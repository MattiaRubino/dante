# Typed Relationship Semantics v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — current Cluster-5 foundation  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

- **Concept / cluster:** Typed Relationship Semantics — first candidate in Relationships / Reasoning
- **Candidate version:** v0
- **Reviewer/workstream:** Core Domain Model v0
- **Adjacent concepts:** Goal, Plan, Activity, Event, Routine, Milestone, Occurrence, Schedule, Session, Actual, Outcome, Observation, Confirmation, Evidence, Provenance, Subject, Person, Actor, Account, Asset, Resource
- **Why this review exists:** The accepted atlas already relies on meaningful links such as `performed_by`, `recorded_by`, `confirmed_by`, `supports`, `derived_from`, `scheduled_for`, `subject_of`, and future allocation/participation/authority links. It explicitly rejects both a semantic-free `related_to` edge and a generic actor edge that replaces specific roles. This review decides the minimum semantic rule that lets such links remain precise without introducing a universal Relationship root, generic graph, or premature persistence model.

This checkpoint validates a **relationship modeling capability and decision rule**, not a universal entity, table, graph root, API resource, workflow engine, or collaboration model.

It does not validate or accept:

- Responsibility, Assignment, Claim, Hand-off, Stewardship, Contribution or Dependency;
- Participation, invitation delivery, acknowledgement, acceptance/agreement or verification;
- Authority, Visibility, consent, access-control, Principal or delegation mechanics;
- GoalCriterion, Decision, Version, AI Proposal, Resource Requirement, Allocation or Reservation;
- generic heterogeneous-reference persistence;
- SQL tables, polymorphic associations, graph storage, API contracts or UI objects.

## 2. Evidence reviewed

### Internal

- [x] accepted Domain Atlas concepts and concept specs
- [x] Cluster 1–4 checkpoints and Cross-Cluster Validation v4
- [x] Deferred Dependency Closure — Clusters 1–4 v0
- [x] Multi-Actor Readiness v1
- [x] Domain & Product Language Map
- [x] V1 product/feature-discovery and multi-actor research references already linked by the workstream
- [x] architecture/ADR constraints relevant to typed relational core and graph-like personal relations
- [x] product assumptions: personal-first UX, progressive disclosure, no enterprise workflow leakage

### External

| Source/pattern | Finding | Classification |
|---|---|---|
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Direct binary assertions are useful when their meaning is complete; qualified relations exist to carry details not expressible on the simple link. | ADAPT |
| [W3C PROV Data Model](https://www.w3.org/TR/prov-dm/) | Delegation, derivation, association and attribution distinguish several directions and roles rather than using one generic edge. The standard is provenance-specific and cannot become the LifeOS root ontology. | ADAPT |
| [Microsoft Graph attendee](https://learn.microsoft.com/en-us/graph/api/resources/attendee?view=graph-rest-1.0) | Event identity and per-attendee invitation response are separate; attendee type and response are contextual rather than Event-wide facts. | ALREADY STRONGER |
| [FHIR Task](https://build.fhir.org/task-definitions.html) | Focus, requester, owner/performer and restrictions are distinct workflow roles. Its specialist workflow resource is not a LifeOS universal task/relation model. | ADAPT |
| [Asana task model](https://developers.asana.com/reference/tasks) | Dependencies are explicit directional task links, but assignee, completion, approval and workflow state are compressed into an application-specific Task model. | ANTI-PATTERN |
| [RFC 5545](https://www.rfc-editor.org/info/rfc5545/) / calendar exceptions | Series-instance relationships and exception identity remain directional and historically stable; calendar interoperability identifiers are not LifeOS universal relation identity. | ALREADY STRONGER |
| [FHIR Provenance](https://fhir.hl7.org/fhir/provenance.html) | A record/version can have multiple provenance records and provenance is distinct from audit. The target relation is contextual and version-aware. | ALREADY STRONGER |
| Generic graph/Node identity patterns | A technical global node interface helps refetch/caching but does not establish shared domain identity or relation semantics. | ANTI-PATTERN |

## 3. Candidate definition

> **Typed Relationship Semantics is the LifeOS modeling capability by which two or more existing domain referents are connected through an explicit, directional, domain-meaningful relation whose verb and invariants answer a specific domain question. A direct typed relation is sufficient when the link has no independently material lifecycle, role/state, authority, provenance, privacy, temporal, cardinality, or query semantics. When the link itself materially needs one or more of those properties, LifeOS may model a qualified relation specific to that semantic family. This does not create a universal Relationship entity/root, semantic-free `related_to` graph, or generic relation table.**

### Domain question answered

> What is the smallest semantically truthful way to express a meaningful connection between already-established LifeOS concepts without collapsing distinct meanings into an untyped edge or inventing a generic graph object?

### Identity

- A direct typed relation does **not** automatically have independent identity.
- A qualified relation may have independent identity only when its own lifecycle/history/authority/provenance/query semantics require it.
- Independent identity belongs to the specific future relation family — for example a future Participation, Assignment, Allocation, Authority grant, Evidence use or Version relation — not to a universal `Relationship` wrapper.
- A relation's technical database row, foreign-key pair or graph edge ID is not, by itself, evidence of domain identity.

### Independent/contextual existence

| Form | Existence rule |
|---|---|
| Direct typed relation | Contextual assertion between existing referents; normally exists only as part of those concepts' semantics. |
| Qualified relation | May exist as a contextual domain record when its own changes, history, authority, state, timing or query behavior matter. |
| Universal Relationship | Rejected as a current kernel root because no common independent identity/lifecycle has been demonstrated across all relation families. |

### Core decision rule

```text
specific domain verb + complete semantics
→ direct typed relation

link needs material temporal state, roles, provenance, authority,
privacy, lifecycle, cardinality constraints, or standalone querying/history
→ candidate qualified relation in its own semantic family

link has no demonstrated semantic distinction
→ no new kernel relation; keep it as product/UI organization, query result,
note, label, or await concrete evidence
```

### Nearest boundaries

```text
Typed Relationship Semantics != universal Relationship entity/root
Typed Relationship Semantics != semantic-free related_to
Typed Relationship Semantics != Subject
Typed Relationship Semantics != Actor
Typed Relationship Semantics != Resource
Typed Relationship Semantics != Provenance
Typed Relationship Semantics != Evidence
Typed Relationship Semantics != Authority
Typed Relationship Semantics != Visibility
Typed Relationship Semantics != Account/Principal
Typed Relationship Semantics != generic polymorphic persistence mechanism
```

### Deliberate deferrals

Responsibility, Participation, Authority, Visibility, Dependency, GoalCriterion, Decision, Version, delegation, Resource Requirement/Allocation/Reservation, focus/context and heterogeneous persistence remain separately owned candidates. This checkpoint defines no relation verb, states or cardinality for them.

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | Household task, shared meeting, caregiver record, camera booking, imported measurement, goal evidence and asset transfer each need different verbs/roles; a generic link makes “who/why/what changed?” unanswerable. | PASS | Direct typed relations express the simple cases; higher-consequence relation records remain candidate-specific. |
| CORE-02 Deep chronology | Yes | Anna records Maria's temperature; later the observation's subject is corrected. A camera is planned then substituted. A recurring meeting instance moves. | PASS WITH HARDENING | Relation history must not be overwritten when material. A change in a qualified relation may require its own historical record; a direct relation must not pretend old semantics were always current. |
| CORE-03 Reductio | Yes | Remove typed verbs; merge every link into `related_to`; split every link into a standalone object; make all links universal; invert direction. | PASS | Removal loses meaning/query safety; universalization creates an empty graph; universal reification creates overhead; inversion proves direction must be explicit per verb. |
| CORE-04 Redundancy | Yes | Compare Subject, Actor roles, Resource role, Evidence, Provenance and direct links such as `performed_by`/ `derived_from`. | PASS WITH HARDENING | Subject/Actor/Resource remain bounded roles, not substitutes for generic links. Evidence and Provenance remain relation-capabilities in their own contexts, not universal relation types. |
| CORE-05 Traceability | Yes | Goal → Plan → Activity; Session → Actual; Observation → Evidence use; imported source → transformed Observation. | PASS | Downward, upward and lateral traces can be expressed without duplicate source objects or fake historical intention. |
| CORE-06 Orphan/independence | Yes | A direct `scheduled_for` link has no reason to exist independently; an asserted Participation or Allocation may need history/state even if endpoints remain. | PASS | Relation identity is conditional, not assumed. |
| CORE-07 External benchmark | Yes | PROV qualified relations, calendar series/instances, event attendee responses, FHIR workflow roles. | PASS | External evidence supports a direct-versus-qualified distinction, while LifeOS remains narrower and personal-first. |
| CORE-08 Anti-pattern review | Yes | Property graph with generic labels; generic join table; universal Node/ManagedObject; storing every relation as unbounded JSON; app-specific Task super-object. | PASS | All are rejected for kernel truth. Technical implementation may later use varied mechanisms only if it preserves semantic distinctions. |
| CORE-09 Correction/reconciliation/epistemic integrity | Yes | Later correction changes a subject association or imported source mapping; later evidence becomes relevant to a different Milestone. | PASS WITH HARDENING | Later relevance must not fabricate an earlier relation; relation provenance/versioning is required only where material. |
| CORE-10 Scale/performance/history | Yes | Ten-year activity graph, high-volume observation provenance, many recurring exceptions, numerous personal associations. | PASS | Do not materialize every possible transitive/derived relationship; query/index choices remain physical-model work. |
| CORE-11 Simple vs power user | Yes | “Done by Anna”, “Camera used”, “Based on this measurement” versus audits, corrections and multi-party records. | PASS | Direct language can expose verbs while qualified details stay progressive/advanced. |
| CORE-12 Product value/complexity cost | Yes | Casual personal links should not require a relation form; safety-critical hand-off cannot be a silent field overwrite. | PASS | Qualification is consequence-driven, not default UX burden. |
| CORE-13 Implementation pressure | Yes | Need integrity, directionality, history and efficient queries, but no final table/API decision is yet justified. | PASS | The candidate constrains later persistence without selecting it. |

## Core-gate hardenings incorporated

1. **Explicit direction and verb rule:** no generic `related_to` for a material domain relation; direction is part of the meaning.
2. **Qualified-relation threshold:** reify/identify only when the link itself has material lifecycle, temporal, state, role, authority, provenance, privacy, cardinality or query semantics.
3. **No technical leakage:** foreign-key shape, graph edge ID, polymorphic association, JSON object or API link never decides domain identity.
4. **Historical relation integrity:** material changes to a relation must preserve enough history/provenance to avoid rewriting the past.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | External doctor is an Event participant without Account; Anna changes login but remains recorder in historical provenance. | PASS | Endpoint identity must remain independent from Account. |
| MA-02 Shared fact/actor overlay | Yes | One shared Event with separate invite responses/reminders/private notes. | PASS | Shared relation/context must not produce per-account copies of the Event. |
| MA-03 Responsibility/assignment/claim | Yes | Shared grocery task starts open, Luca claims it, Anna remains fallback, then hand-off is requested. | DEFERRED DEPENDENCY | Demonstrates qualified-relation pressure but does not accept Responsibility or Assignment. |
| MA-04 Stewardship/mental load | Yes | Parent remembers a deadline while another person performs it. | DEFERRED DEPENDENCY | Coordination burden is not inferred from a typed link; ownership remains future Responsibility/Stewardship review. |
| MA-05 Common ground/state separation | Yes | Invitation sent, delivered, seen, accepted and attended differ. | PASS WITH HARDENING | A direct participant link cannot silently represent all these states. Qualified Participation/Acknowledgement candidates are required if a workflow needs them. |
| MA-06 Authority/canonical change | Yes | Caregiver reports a fact; clinician/external authority determines canonical care decision. | PASS WITH HARDENING | Relation type does not manufacture Authority; authority basis remains a separate candidate. |
| MA-07 Selective disclosure | Yes | Share “unavailable” without medical cause or hidden participant linkage. | PASS | Relation existence/detail/endpoint visibility can be separately controlled later; no disclosure is implied by a relation. |
| MA-08 Inference privacy | Yes | AI links a private Observation to a recommendation. | PASS | AI-derived relation/proposal cannot disclose or establish the relation as canonical automatically. |
| MA-09 Partial adoption/external participant | Yes | A non-LifeOS family member participates by phone/email. | PASS | A relation endpoint need not have Account or app adoption. |
| MA-10 Assisted participation/provenance | Yes | Anna enters Maria's measurement; Maria is Subject, Anna recorder, source device distinct. | PASS | Specific relation roles preserve truthful attribution. |
| MA-11 Relationship lifecycle/revocation | Yes | A former partner loses future access but historical event participation remains. | PASS WITH HARDENING | Current access/relation status and historical attribution must not collapse. |
| MA-12 Conflict/adversarial relationship | Yes | Two actors contest who accepted a hand-off or whether a dependency was cleared. | DEFERRED DEPENDENCY | Relationship semantics allow the distinction, but conflict resolution/Authority is not decided here. |
| MA-13 Unequal power | Yes | Guardian, caregiver and clinician relationships vary by context and scope. | DEFERRED DEPENDENCY | No typed relation name becomes blanket authority or visibility. |
| MA-14 Multi-resource/capacity | Yes | Camera/room/person can be candidates; selection and capacity claim are separate. | PASS | Resource-role relation does not become allocation/reservation. |
| MA-15 Coordination-burden distribution | Yes | Household coordination should not be hidden in assignee relation. | DEFERRED DEPENDENCY | Future stewardship/responsibility review owns the distinct burden semantics. |
| MA-16 Formality/progressive disclosure | Yes | Dinner RSVP versus care hand-off. | PASS | Same direct vocabulary may be adequate in low consequence; qualified records can carry formality when concrete workflows demand it. |
| MA-17 AI authority/multi-party context | Yes | AI proposes a resource match or hand-off based on private context. | PASS | Proposal/action authority stays bounded by acting Principal/context/policy; exact Principal model deferred. |
| MA-18 Specialist-system boundary | Yes | Medical authority, workforce shift transfer and legal consent may be externally authoritative. | PASS | LifeOS coordinates and records relevant relations; it does not rebuild specialist administration. |
| MA-19 Multi-actor primitive redundancy | Yes | Test universal Relation, Participant, Team, User, Actor wrappers. | PASS | No generic collaboration root is justified. |
| MA-20 Actor-scoped reality attribution | Yes | Shared Session with differing attendance intervals and actual performers. | DEFERRED DEPENDENCY | Requires future Participation/Actual relation semantics; current Actual/Session identity remains valid. |

## Multi-actor hardenings incorporated

1. **A typed link is not consent, acceptance, participation, responsibility, authority, ownership, visibility or execution by default.**
2. **A direct relation must not absorb actor-scoped state.** When per-actor response, interval, consequence, permissions or history matter, a future qualified relation is required.
3. **Historical attribution and current access have different lifecycles.**
4. **External/non-account endpoints are legitimate where the underlying concept permits them.**

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS | Does not introduce a universal identity/root; preserves native Person/Asset and existing concept identities. |
| XCON-02 Ownership/authority compatibility | Yes | PASS WITH HARDENING | Relation verbs never imply authority, ownership, visibility or canonical-change rights unless a future typed relation explicitly proves and models that semantic. |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS | Direct and qualified relation rule preserves planned allocation vs actual use, Schedule vs Session/Actual, and historical corrections. |
| XCON-04 Relationship compatibility | Yes | PASS | Confirms specific role/verb precedence and rejects `related_to` as a semantic escape hatch. |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS WITH HARDENING | Future Participation/Responsibility/Authority must qualify links where actor-scoped state matters. |
| XCON-06 Language-map compatibility | Yes | PASS | No new product/UI noun is required. “Done by”, “Based on”, “For”, “Used”, “Available to” remain contextual UI language. |

---

# 7. Adjacent Dependency Sweep

| Dependency / boundary | Why it matters | Closure class | Current resolution / why safe to defer | Owner / future concept or stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|---|
| Typed direct relation ↔ universal Relationship root | A generic root could duplicate all endpoints and erase family-specific semantics. | RESOLVED | Universal root rejected; direct/qualified rule is sufficient at current scope. | This checkpoint | A concrete cross-domain relation family proves shared independent lifecycle/authority/history not expressible through specific qualified relations. | CORE-03, CORE-04, MA-19, XCON-01, XCON-04 |
| Typed direct relation ↔ generic `related_to` | Generic link loses direction, verb and invariants. | RESOLVED | Material relations require an explicit meaningful verb/direction. | This checkpoint | A legitimate material relation cannot be named/typed without false specificity, yet has more than UI/query meaning. | CORE-01, CORE-03, CORE-04, XCON-04 |
| Direct relation ↔ qualified relation | Over-qualification creates enterprise/graph overhead; under-qualification loses history/state/authority. | RESOLVED | Qualification threshold incorporated as core hardening. | This checkpoint; future relation families apply it | A relation with only a direct link cannot preserve material temporal/state/role/authority/provenance/privacy/query semantics, or qualified records repeatedly add no independent truth. | CORE-02, CORE-04, CORE-06, CORE-09, CORE-12, MA-05, MA-11 |
| Activity ↔ Responsibility / Assignment / Claim / Hand-off / Stewardship | Assignment and transfer can change while Activity identity persists. | SAFE DEFERRED | Current direct/qualified rule safely identifies the pressure without deciding relation types/states. | Relationships / Reasoning — Responsibility | Concrete workflows cannot represent open/claimable/reassigned/accepted hand-off without changing Activity identity or misrepresenting performer. | CORE-02, CORE-03, MA-03, MA-04, MA-11, MA-15, XCON-04 |
| Session/Actual ↔ Participation | Shared occurrence and actor-specific attendance/execution differ. | SAFE DEFERRED | Current Actual/Session boundary survives; future participation may qualify the relation. | Relationships / Reasoning — Participation | Different participation intervals/roles/consequences cannot be represented without creating competing Session/Actual identities. | CORE-03, MA-02, MA-05, MA-09, MA-20, XCON-03, XCON-05 |
| Confirmation ↔ Acknowledgement / Acceptance / Verification | Direct relation to a target cannot collapse receipt, willingness, attestation and checking. | SAFE DEFERRED | Confirmation remains bounded and distinct; this checkpoint supplies the qualification rule. | Relationships / Reasoning — Participation / Authority / acknowledgement review | Ordinary collaboration workflow requires one relation to carry incompatible states or destroys material history. | CORE-03, CORE-04, MA-03, MA-05, MA-11, XCON-04 |
| Authority ↔ Visibility / ownership / actor action | Relation labels often incorrectly imply permission/authority. | SAFE DEFERRED | Explicit non-inference hardening preserves current model. | Relationships / Reasoning — Authority / Visibility | A canonical change/disclosure decision cannot be represented without treating a direct relation as authority/visibility. | MA-06, MA-07, MA-08, MA-11, MA-13, MA-17, XCON-02, XCON-05 |
| Provenance ↔ relation history / Version / Audit | Material relation correction must not rewrite origin, while not every link needs audit history. | SAFE DEFERRED | Qualification threshold identifies material relation history; Version/Audit mechanics remain deferred. | Relationships / Reasoning — Version/Decision; logical/security design | Material relation correction cannot preserve what was asserted/effective without redefining Provenance or creating universal audit. | CORE-02, CORE-09, MA-10, MA-11, XCON-03 |
| Evidence ↔ Criterion / Decision | Evidence is evaluative use, possibly a qualified relation, not source copy or decision. | SAFE DEFERRED | Existing Evidence boundary survives; typed/qualified rule provides future representation pressure only. | Relationships / Reasoning — GoalCriterion/Evidence/Decision | Evaluation cannot retain direction, scope, context and competing evidence without changing Evidence semantics. | CORE-03, CORE-04, CORE-05, CORE-09, MA-06, XCON-04 |
| Resource Requirement ↔ candidate / Allocation / Reservation / actual use | These are links at different planning/reality stages. | SAFE DEFERRED | Direct/qualified rule does not merge stages; Resource remains role not identity. | Relationships / Reasoning — resource planning semantics | One stage cannot be represented without falsely asserting another or requiring a Resource root. | CORE-02, CORE-04, MA-14, XCON-03, XCON-04 |
| Subject ↔ focus/context | Subject is primary aboutness, not all contextual links. | SAFE DEFERRED | A future focus/context relation may be typed/qualified; Subject boundary remains intact. | Relationships / Reasoning — focus/context | Ordinary descriptive records cannot distinguish primary subject from material context/focus. | CORE-04, CORE-05, XCON-04 |
| Account/Principal/delegation/on-behalf-of | Actor, authenticated identity and authority chain may differ. | SAFE DEFERRED | Existing separation holds; this checkpoint does not invent a generic delegation edge. | Relationships / Reasoning — Authority/delegation; logical security design | Delegated human/AI/service action cannot preserve attribution and authority chain through specific future relation semantics. | MA-01, MA-06, MA-10, MA-11, MA-13, MA-17, XCON-02 |
| Heterogeneous relation persistence | A later physical model needs integrity/queryability without forcing a universal node root. | SAFE DEFERRED | Semantic rule is independent of storage; physical mechanism is deferred. | Logical data model | No persistence approach can preserve required endpoints, history and integrity without a materially different semantic abstraction. | CORE-10, CORE-13, XCON-01, XCON-04 |
| AI proposal/inference relation | AI can propose links without establishing identity, allocation, authority or disclosure. | SAFE DEFERRED | Non-inference rules hold; proposal semantics remain a future candidate. | Relationships / Reasoning — AI Proposal / Authority | An AI workflow needs a relation to become canonical without explicit authority/decision semantics. | MA-06, MA-07, MA-08, MA-17, XCON-02, XCON-05 |

---

# 8. Adversarial scenario log

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|
| “Anna is related to Buy milk” | Semantic-free generic edge | Fails: no answer to whether she created, performs, is responsible, observes, has access or is subject. | No; reject generic link. |
| Activity assigned to Luca, actually completed by Anna | Assignment versus performer/Actual | Direct assignment cannot represent execution truth. | Future Responsibility/Participation, not this checkpoint. |
| Meeting invitation accepted but participant absent | Response versus Actual participation | One attendee relation cannot represent both safely. | Future Participation relation if product needs it. |
| Caregiver records patient measurement | Subject, recorder, account, provenance | Specific roles preserve attribution; generic actor/subject link fails. | No. |
| Camera A17 allocated then A18 actually used | Requirement/candidate/allocation/actual use | Single “uses resource” relation destroys plan/history. | Future allocation/actual-use semantics. |
| Child-safety hand-off requested but not accepted | Request, acceptance, effective responsibility | Direct relation cannot silently transfer responsibility. | Future Responsibility/Authority review. |
| Former partner loses access to shared history | Revocation versus historical participation | Current relation history must remain distinguishable from future visibility. | Future Visibility/revocation policy. |
| AI infers that two external contacts are the same Person | Proposed reconciliation versus established identity | Inference cannot write canonical relation automatically. | Future AI Proposal/Authority/Decision. |

---

# 9. Reopening / dependency register

| Finding | Severity | Closure class | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|
| Need for a universal Relationship root | STRUCTURAL | RESOLVED | Rejected; no shared independent semantics demonstrated. | This checkpoint | Specific relation families cannot express demonstrated cross-domain lifecycle/history/authority without a universal root. |
| Direct relation may need contextual state/history | HARDENING | RESOLVED | Qualification threshold incorporated. | This checkpoint | Threshold repeatedly fails realistic workflows. |
| Responsibility/assignment/hand-off | DEFERRED DEPENDENCY | SAFE DEFERRED | Separate future candidate. | Relationships / Reasoning | Activity history cannot survive valid transfers. |
| Participation and actor-scoped Actual | DEFERRED DEPENDENCY | SAFE DEFERRED | Separate future candidate. | Relationships / Reasoning | Shared reality requires competing Actual/Session identity. |
| Authority/Visibility/delegation | DEFERRED DEPENDENCY | SAFE DEFERRED | Separate future candidates/security stage. | Relationships / Reasoning | Relation labels must carry authority/disclosure to model ordinary cases. |
| Relation version/history/persistence | DEFERRED DEPENDENCY | SAFE DEFERRED | Version/logical model later. | Relationships / Reasoning / logical model | Material corrections cannot be reconstructed. |

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Rationale

The candidate survives as a minimal **capability and modeling rule**, not as a new universal domain entity. It protects the accepted atlas against both failure modes:

1. semantic loss through `related_to`, generic actor/resource links, field overwrites or untyped graph edges;
2. unnecessary complexity through a universal Relationship root or automatic reification of every link.

The rule is compatible with the first four clusters and gives future candidates a precise test: determine whether their link is a direct typed relation or a separately justified qualified relation. It does not decide the semantics of those future relation families.

## Hardenings incorporated before acceptance

- material domain relations require explicit, directional, meaningful verbs;
- specific roles remain stronger than generic actor relations;
- direct relation is the default only while the link has no material independent semantics;
- qualified relation is justified only by demonstrated lifecycle/history/state/role/authority/provenance/privacy/cardinality/query need;
- relation existence and relation details do not imply visibility, consent, ownership, responsibility, participation, authority or actual execution;
- material relation correction must preserve historical integrity;
- technical representation never determines semantic identity.

## Dependency-sweep summary

- **RESOLVED:** universal Relationship root; semantic-free `related_to`; direct-versus-qualified decision rule.
- **SAFE DEFERRED:** Responsibility, Participation, Authority/Visibility, acknowledgement/acceptance/verification, Version/Decision/Audit, Evidence/Criterion, resource planning stages, focus/context, delegation, heterogeneous persistence, AI proposal.
- **REOPEN:** none.

## Mandatory future re-tests

- Re-run the direct-versus-qualified threshold in every future candidate that creates a material link.
- Re-run relevant relationship history/provenance tests when Version or Decision is reviewed.
- Re-run multi-actor tests MA-03, MA-05, MA-06, MA-07, MA-11, MA-13, MA-17 and MA-20 in Responsibility, Participation, Authority and Visibility reviews.
- Re-run XCON-04 whenever a candidate proposes a generic relation/root or persistence abstraction.

---

# 11. Cluster-only integration section

Not applicable: this checkpoint validates one candidate, not the complete Cluster 5.

---

# 12. Regression corpus additions

| Scenario | New boundary covered | Reuse trigger |
|---|---|---|
| Open grocery responsibility → claim → accepted hand-off → actual performer differs | direct link versus qualified Responsibility/Participation | Responsibility or Participation review |
| Shared meeting → invitation response → attendance intervals → revocation | Event identity versus actor-scoped relationship state | Participation / Visibility review |
| Caregiver records observation about another person | Subject/Actor/Account/Provenance role separation | Authority / assisted participation review |
| Planned camera A17 → substituted A18 → actual use | Resource planning stages and history | Requirement / Allocation review |
| AI proposes identity/resource link from private context | proposal versus canonical link/disclosure | AI Proposal / Authority review |

---

# 13. Documentation propagation

- [x] candidate checkpoint created
- [ ] language map update — no canonical UI/product term changed
- [ ] cluster checkpoint update — Cluster 5 not complete
- [ ] workstream handoff update — no stage transition
- [x] Adjacent Dependency Sweep completed
- [x] every material deferral has owner + reopening trigger
- [x] no unclassified dependency limbo remains for this candidate
- [x] no old canonical wording changed
