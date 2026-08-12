# Relationship v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — canonical modeling capability / semantic rule; universal Relationship primitive rejected  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

This review asks a deliberately prior question before validating Responsibility, Participation, Authority, Dependency, Allocation, or other relation-rich candidates:

> **Does LifeOS need a universal domain concept/entity called `Relationship`, or should meaningful connections remain specific domain semantics with qualification only where the connection itself materially needs state/history/lifecycle?**

The review does **not** assume that a roadmap noun must survive. It evaluates four competing shapes:

1. universal `Relationship` entity/root;
2. only ad-hoc specific links with no common discipline;
3. a common semantic modeling rule without a universal root;
4. the same domain rule plus a separately bounded future Personal Knowledge link layer.

This checkpoint validates the modeling discipline. It does not accept Responsibility, Participation, Dependency, Authority, Visibility, Resource Allocation, GoalCriterion, Decision, Version, delegation, or a generic Personal Knowledge graph.

---

# 2. Evidence and candidate formation

## 2.1 Existing LifeOS pressure

Clusters 1–4 already require multiple kinds of meaningful connection:

```text
Observation -> Subject
Actor-specific roles -> performed_by / recorded_by / confirmed_by / proposed_by
Evidence source -> evaluative target
Provenance source/activity/actor -> material target/version
Activity -> future Responsibility / expected performer
Session/Actual -> future Participation / actual performer
Resource Requirement -> candidate / Allocation / Reservation / actual use
Confirmation -> target version
Asset -> future ownership/custody/stewardship/location relations
```

Those boundaries were intentionally left distinct. The current review must not flatten them merely because they can all be drawn as graph edges.

## 2.2 Real-world workflow inversion

Representative workflows were reconstructed without assuming LifeOS objects first.

### Simple aboutness

```text
Anna records Maria's temperature.
```

The material information is the Observation, its Subject, recorder/source, time and value. A standalone `Relationship` object adds no independent domain truth to the ordinary Subject association.

### Dependency

```text
Book hotel
before
Leave for trip
```

A simple dependency may be expressible directly. If reason, lag, waiver, validity or material history later matter, that pressure belongs to a specific Dependency semantic family rather than proving a universal Relationship lifecycle.

### Responsibility / hand-off

```text
Luca is responsible
-> asks Anna to take over
-> Anna has not accepted
-> Anna accepts
-> Marco actually performs
```

The connection can acquire state/history independent from Activity and Person identity. This demonstrates pressure for a qualified Responsibility/hand-off family, not for an untyped universal relation.

### Event participation

```text
invited
-> tentative
-> accepted
-> declined
-> actually attended
```

Event identity and Person identity remain stable while contextual participation state changes.

### Resource planning

```text
Requirement
-> candidates
-> Allocation
-> Reservation / Capacity Claim
-> Actual use
```

These are not one generic Activity-Resource relationship whose `type` merely changes over time.

### Evidence use

The same Observation can support one Criterion, contradict another, and be irrelevant to a third. Existing Evidence semantics already represent contextual evaluative use and must not be demoted into a semantic-free generic edge.

### Personal Knowledge

Low-consequence user-defined links such as `reminds me of`, `inspired by`, or `met at` may benefit from a flexible knowledge-link layer in the future. That possible layer must not automatically establish Responsibility, Authority, Actual, Evidence, Participation or allocation semantics.

## 2.3 External benchmark interpretation

External patterns were treated as evidence, not ontology authority:

| Source / pattern | Finding | LifeOS treatment |
|---|---|---|
| W3C PROV-O / qualified relations | Simple binary relations can be qualified when the relation needs additional contextual details. | **ADAPT** — useful pattern, provenance-specific standard not adopted as LifeOS root ontology. |
| Microsoft Graph attendee/response state | Event identity is distinct from per-attendee response state. | **ADAPT** — supports relation-specific contextual state. |
| FHIR Task roles | Requester, owner/responsible party and performers are distinguished instead of collapsed into one actor link. | **ADAPT** — specialist workflow semantics remain specialist evidence. |
| Jira issue links | Generic typed links work inside a bounded and comparatively uniform issue domain. | **BOUNDED EVIDENCE** — does not justify a whole-LifeOS Relationship root. |
| Notion Relation property | Flexible references are valuable for user-defined knowledge/database linking. | **ADAPT LATER** — evidence for a possible separate Personal Knowledge layer, not operational kernel truth. |
| ActivityStreams Relationship object | Explicit relationship objects can be valuable for a bounded social-relationship problem. | **BOUNDED EVIDENCE** — a specialized family is not a universal edge model. |

---

# 3. Candidate result

## 3.1 Rejected universal primitive

```text
UNIVERSAL Relationship ENTITY / ROOT
REJECTED

semantic-free related_to as kernel truth
REJECTED
```

No shared independent identity or lifecycle has been demonstrated across Subject, Evidence, Responsibility, Participation, Dependency, Authority, allocation, ownership, provenance and other relation families.

A generic structure such as:

```text
Relationship
- id
- type
- source
- target
- metadata
```

can represent almost anything technically, but would move domain meaning into `type + metadata`, weaken invariants, and recreate the generic-graph anti-pattern already rejected by the architecture.

## 3.2 Accepted modeling capability

> **A meaningful LifeOS connection uses the most specific domain semantics that truthfully answer the relationship question. A simple connection does not acquire independent identity merely because it is stored, queried, traversed, many-to-many, or high-cardinality. When the connection itself has materially relevant state, lifecycle, history, temporal scope, actor-scoped state, authority, provenance, privacy, or domain invariants, LifeOS may represent it through a qualified relation specific to that semantic family. This does not imply a universal `Relationship` entity/root, semantic-free `related_to`, generic graph edge, or universal relation table.**

Canonical decision shape:

```text
specific meaning + semantically complete simple connection
-> direct typed/specific relation

specific meaning + materially rich connection
-> domain-specific qualified relation / relation record

flexible user-defined knowledge association
-> separate future Personal Knowledge review/layer

no demonstrated domain meaning
-> do not invent kernel relation
```

---

# 4. Core Semantic Validation Gate

| Test ID | Evidence / destructive pressure | Result | Finding / hardening |
|---|---|---|---|
| CORE-01 Workflow inversion | aboutness, dependency, hand-off, attendance, resource planning, Evidence use, knowledge links | PASS | A universal wrapper adds overhead in simple cases and flattens meaning in rich cases. |
| CORE-02 Deep chronology | create, change, transfer, revoke, correct, restore, later historical query | PASS WITH HARDENING | Material relation history belongs to the specific semantic family; no universal lifecycle emerged. |
| CORE-03 Reductio | REMOVE / MERGE / SPLIT / MAKE UNIVERSAL / INVERT / EXTREME | PASS | Removing relation semantics fails; universal root fails; making every relation an entity fails; only direct fields forever also fails. |
| CORE-04 Redundancy / merge-split | Subject, Actor, Resource, Evidence, Confirmation, Provenance and future rich families | PASS WITH HARDENING | Existing rich concepts remain distinct; qualified structure does not automatically imply entity identity. |
| CORE-05 Traceability | intention -> execution, reality -> evaluation, lateral use | PASS | Specific semantic links preserve traceability without source duplication. |
| CORE-06 Orphan / independence | simple association vs relation state/history | PASS | Universal Relationship has no demonstrated independent existence; specific qualified families may. |
| CORE-07 Cross-domain benchmark | PROV, Graph attendee, FHIR, Jira, Notion, ActivityStreams | PASS | Different systems support different bounded relation shapes; none justifies one LifeOS root. |
| CORE-08 Anti-pattern review | generic graph, universal join table, JSON metadata semantics, node-root pressure | PASS | Reject semantic-free graph/root as kernel truth. |
| CORE-09 Correction / epistemic integrity | wrong Subject, inferred link, corrected allocation, revoked relationship | PASS WITH HARDENING | Corrections/inferences must not silently rewrite historical relationship truth. |
| CORE-10 Scale / history | long personal graph, high-volume provenance/evidence, recurring relations | PASS | Do not eagerly materialize universal graph closure/transitivity. Physical indexes remain later work. |
| CORE-11 Simple vs power user | simple `Done by Anna` vs rich audit/state | PASS | Kernel precision need not expose a Relationship object in ordinary UI. |
| CORE-12 Product value / complexity | low-consequence link vs formal hand-off | PASS | Qualification is consequence/semantics driven, not default UX burden. |
| CORE-13 Implementation pressure | FK, many-to-many, graph traversal, SQL row ID | PASS | Technical storage/query needs do not create domain identity. |

## 4.1 Hardenings incorporated

### Orientation, not forced direction

Relation orientation semantics must be explicit, but not every relation is inherently directional.

```text
parent_of     asymmetric
sibling_of    symmetric
```

A technical `source_id / target_id` representation must not manufacture semantic direction.

### Qualified relation != entity automatically

A relation may require structured state/history/context without automatically deserving independently meaningful domain identity.

```text
needs structure != proves entity identity
```

Independent identity still requires separate justification through lifecycle, referenceability, history, authority, invariants or other material semantics.

### Queryability/cardinality != domain identity

```text
frequently queried
many-to-many
millions of rows
requires database row id
```

are implementation pressures, not sufficient evidence for a domain primitive.

### Binary representation is not universal

Some rich relations may be naturally contextual/n-ary. Future Allocation, delegation, participation or evidence semantics must not be decomposed into arbitrary binary edges if doing so loses the semantic context.

### No universal symmetry/transitivity/inverse propagation

Symmetry, inverse semantics, transitivity and reasoning/propagation belong to the specific relation family.

```text
friend_of(A,B) + friend_of(B,C)
!= friend_of(A,C)
```

A specific future Dependency relation may support different reasoning rules. Those rules must never be inherited from `Relationship` generally.

---

# 5. Multi-Actor Compatibility Gate

| Test area | Result | Key conclusion |
|---|---|---|
| MA-01 Identity/account independence | PASS | relation endpoints do not require Account coincidence |
| MA-02 Shared canonical fact / overlays | PASS | one shared object can coexist with actor-scoped relation state |
| MA-03 Responsibility / assignment / claim | PASS WITH DEFERRED FAMILY | demonstrates specific qualified-family pressure |
| MA-04 Stewardship / mental load | PASS WITH DEFERRED FAMILY | coordination burden must not be inferred from assignment |
| MA-05 Common-ground states | PASS WITH DEFERRED FAMILY | sent/seen/acknowledged/accepted/Actual remain separable |
| MA-06 Authority / canonical change | PASS WITH HARDENING | relation existence/type does not manufacture Authority |
| MA-07 Selective disclosure | PASS WITH HARDENING | endpoint, relation existence, relation details and derived consequence may have different visibility |
| MA-08 Inference privacy | PASS WITH HARDENING | inferred relation does not become disclosure permission or canonical truth |
| MA-09 Partial adoption | PASS | non-LifeOS endpoints remain ordinary where native semantics permit |
| MA-10 Assisted participation | PASS | actor/subject/recorder/authority relations stay specific |
| MA-11 Lifecycle / revocation | PASS WITH HARDENING | current relationship/access and historical attribution are distinct |
| MA-12 Conflict/adversarial | PASS WITH HARDENING | conflicting relation assertions may coexist until authority/decision resolves them |
| MA-13 Unequal power | PASS | social/legal role labels do not automatically expand Authority or Visibility |
| MA-14 Multi-resource/capacity | PASS | Requirement/eligibility/allocation/reservation remain distinct |
| MA-15 Coordination burden | PASS | relation model does not assume assignee owns all mental load |
| MA-16 Progressive formality | PASS | casual UI and formal relation records can share semantic boundaries without same UX |
| MA-17 AI authority | PASS WITH HARDENING | AI may propose/infer relations but not silently establish Authority/identity/allocation |
| MA-18 Specialist boundary | PASS | LifeOS does not replace authoritative external relationship systems |
| MA-19 Primitive redundancy | PASS | universal Relationship root adds no independent semantic identity |
| MA-20 Actor-scoped reality | PASS | Participation/actual-performer semantics can remain specific without duplicating shared Actual/Session |

Canonical multi-actor non-inferences:

```text
relation != Authority
relation != Visibility
relation != ownership
relation != Responsibility
relation != participation state
relation != consent
relation != Account identity
AI inferred relation != established relation
```

---

# 6. Cross-Concept Consistency Gate

| Test | Result | Finding |
|---|---|---|
| XCON-01 Identity | PASS | no Person/Asset/Account/Subject/Actor/Resource identity collapse |
| XCON-02 Ownership / Authority | PASS WITH HARDENING | relationship labels cannot be permission shortcuts |
| XCON-03 Planned/current/actual/history | PASS | Requirement/allocation/actual use and expected/actual performer remain separable |
| XCON-04 Relationship consistency | PASS | specific direct/qualified relations compose with current concepts without generic root |
| XCON-05 Multi-actor | PASS WITH HARDENING | actor-scoped relation state and privacy remain possible |
| XCON-06 Language map | PASS | no mandatory user-facing noun `Relationship` is introduced |

No accepted Cluster 1–4 concept requires structural reopening.

---

# 7. Adjacent Dependency Sweep

| Dependency / boundary | Closure | Why current result is safe | Owner / future stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|
| universal Relationship entity/root | RESOLVED — REJECTED | no shared independent identity/lifecycle demonstrated | this checkpoint | multiple concrete relation families cannot preserve demonstrated common lifecycle/authority/history without one shared domain identity | CORE-03, CORE-04, CORE-06, MA-19, XCON-01, XCON-04 |
| semantic-free `related_to` kernel edge | RESOLVED — REJECTED | material domain links require truthful specific meaning | this checkpoint | a material relation cannot be represented specifically without false semantics yet has more than note/query/knowledge-link meaning | CORE-01, CORE-03, CORE-04, XCON-04 |
| direct vs qualified relation discipline | RESOLVED | qualification threshold survives current scenarios | each future relation-family review | repeated realistic workflows show the rule either loses material history/state or causes systematic over-modeling | CORE-02, CORE-03, CORE-04, CORE-12, CORE-13 |
| Responsibility / Assignment / Claim / Hand-off / Stewardship | SAFE DEFERRED | Activity identity is already independent of responsibility/performer | Relationships / Reasoning — next review family | claim/transfer/acceptance cannot be modeled while preserving one Activity identity and expected-vs-actual performer | CORE-02, CORE-03, MA-03, MA-04, MA-11, MA-15, XCON-04 |
| Participation | SAFE DEFERRED | Session/Actual identity is already independent from participant state | Relationships / Reasoning | actor-specific invitation/attendance intervals require competing Session/Actual identities | CORE-03, MA-02, MA-05, MA-09, MA-20, XCON-03, XCON-05 |
| Dependency | SAFE DEFERRED | direct-vs-qualified rule preserves room for dependency-specific semantics | Relationships / Reasoning | real dependencies require semantics incompatible with either direct link or specific qualified Dependency family | CORE-02, CORE-03, CORE-04, XCON-04 |
| Authority / Visibility | SAFE DEFERRED | explicit non-inference protects current model | Relationships / Reasoning | ordinary canonical change or disclosure requires treating generic relation existence/type as permission | MA-06, MA-07, MA-08, MA-11, MA-13, MA-17, XCON-02, XCON-05 |
| Acknowledgement / Acceptance / Agreement / Verification | SAFE DEFERRED | Confirmation already excludes these semantics | Relationships / Reasoning | collaboration workflows cannot separate these states without changing Confirmation | CORE-03, CORE-04, MA-03, MA-05, MA-11, XCON-04 |
| Evidence ↔ Criterion / Decision | SAFE DEFERRED | Evidence remains contextual evaluative use with its own boundary | Relationships / Reasoning | evaluation cannot preserve direction/context/competing evidence without changing Evidence semantics | CORE-03, CORE-04, CORE-05, CORE-09, MA-06, XCON-04 |
| Resource Requirement / Allocation / Reservation | SAFE DEFERRED | Resource v0 already separates need/provider/planned/actual stages | Relationships / planner | one stage cannot be represented without falsely asserting another | CORE-02, CORE-04, MA-14, XCON-03, XCON-04 |
| Subject ↔ focus/context | SAFE DEFERRED | primary aboutness remains distinct from contextual association | Relationships / Reasoning | ordinary descriptive records cannot distinguish primary Subject from material focus/context | CORE-04, CORE-05, XCON-04 |
| delegation / on-behalf-of | SAFE DEFERRED | Actor, Account and Principal boundaries remain distinct | Authority / Principal review | delegated human/AI/service action cannot preserve attribution + authority chain through specific semantics | MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02 |
| Version / material relation history | SAFE DEFERRED | specific relation families can later own material revisions | Version / Decision | material relationship correction cannot be reconstructed without universal version semantics that change current model | CORE-02, CORE-09, XCON-03, XCON-04 |
| generic Personal Knowledge links | SAFE DEFERRED | no current kernel workflow depends on them; operational non-inference boundary is explicit | future Personal Knowledge review | knowledge organization cannot remain useful without using the same authoritative relation structures as operational kernel semantics | CORE-03, CORE-04, CORE-11, CORE-12, MA-07, MA-08 |
| heterogeneous relation persistence | SAFE DEFERRED | semantic rule is storage-independent | logical data model | no physical model can preserve typed endpoints/integrity/history without introducing a materially different domain abstraction | CORE-10, CORE-13, XCON-01, XCON-04 |

Dependency sweep result:

```text
RESOLVED: universal root; semantic-free related_to; direct-vs-qualified discipline
SAFE DEFERRED: specific relation families / Personal Knowledge / persistence
REOPEN: none
UNCLASSIFIED: none
```

---

# 8. Concept / capability verdict

```text
RELATIONSHIP AS UNIVERSAL DOMAIN PRIMITIVE
REJECTED

RELATIONSHIP AS UNIVERSAL ENTITY / ROOT / SUPERTYPE
REJECTED

SEMANTIC-FREE related_to AS KERNEL TRUTH
REJECTED

TYPED / SPECIFIC RELATIONSHIP MODELING DISCIPLINE
ACCEPTED BASELINE
```

**Verdict:** **PASS WITH HARDENING**  
**Classification:** canonical cross-cutting modeling capability / semantic rule, not an independent domain entity.

No `docs/domain/concepts/relationship.md` is created because validation did not establish a standalone domain concept with independent identity/lifecycle. This checkpoint is the authoritative decision record.

---

# 9. Mandatory future re-tests

1. Every future material relation family must rerun the direct-vs-qualified threshold.
2. Specific family semantics must explicitly define applicable orientation, symmetry, inverse and transitivity rules rather than inheriting them globally.
3. Responsibility/Assignment/Claim/Hand-off/Stewardship is the next high-leverage review family because it stresses relation state, transfer, acceptance, coordination burden and expected-vs-actual performer semantics.
4. Authority/Visibility reviews must re-test that relation existence/type never becomes implicit permission/disclosure.
5. Personal Knowledge review must preserve the boundary between flexible user-defined association and operational/evidentiary/authority semantics.
6. Logical persistence must preserve typed relation semantics without forcing a universal node/edge root merely for implementation convenience.

---

# 10. Documentation propagation

- [x] validation checkpoint created
- [x] universal Relationship primitive/root rejection recorded
- [x] canonical direct-vs-qualified modeling discipline recorded
- [x] Language Map aligned
- [x] Domain README aligned
- [x] workstream handoff aligned
- [x] Adjacent Dependency Sweep completed
- [x] every material deferral has owner + exact reopening trigger + rerun tests
- [x] no structural reopening of Clusters 1–4
- [x] next review family identified without pre-accepting its internal concepts
