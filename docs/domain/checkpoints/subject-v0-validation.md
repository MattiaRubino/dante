# Subject v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — accepted current baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Concept/candidate: Subject
- Candidate version: v0
- Adjacent concepts: Observation, Person, Actor, Account/Principal, Asset, Resource, Provenance, Authority, Visibility, Relationship
- Why this review exists: LifeOS needs to represent who/what descriptive records are about without collapsing subject identity into account, actor, owner, source, asset, or resource semantics.

---

# 2. Evidence reviewed

## Internal

Reviewed:

- Observation v0 and its explicit `subject != observer != recorder != source != authority != viewer` boundary;
- Provenance v0 role separation;
- Multi-Actor Readiness v1;
- caregiver, parent/child, pet/plant, asset/device, room/environment, work-assessment and imported-data scenarios;
- historical `Asset/Soggetto` discovery language;
- Quantity and Register Cluster-4 conclusions.

## External benchmark evidence

| Source/pattern | Finding | Classification |
|---|---|---|
| HL7 FHIR Observation subject/focus | Subject points to native referent resources; focus/context may differ | ADAPT |
| Health/personal-data store patterns | Personal UX may make self-subject implicit while source/device stays distinct | ADAPT |
| Person/contact/account systems | Real person identity can remain distinct from account/contact/source representations | ADAPT |
| Universal wrapper/root pattern | Duplicates heterogeneous native identity merely to create one reference target | ANTI-PATTERN |

External schemas/products are evidence only. LifeOS does not inherit their taxonomies or cardinalities automatically.

---

# 3. Candidate definition

> **Subject is the contextual semantic role played by a native referent when a descriptive record primarily concerns that referent's state, property, condition, or asserted fact. Subject does not create independent identity: the referenced Person, Asset, Event, Device, Location, or other eligible referent retains its native identity. Being the Subject does not imply authorship, observation, recording, ownership, responsibility, authority, visibility, participation, or account identity.**

## Domain question answered

> Who or what is this descriptive record primarily about?

## Identity

No independent Subject identity. Subject is a contextual role/reference to native referent identity.

## Independent/contextual existence

Subject semantics exist only in relation to a record/context that is about a referent. A native Person/Asset/etc. exists independently of playing Subject role.

## Nearest boundaries

```text
Subject != Person
Subject != Actor
Subject != Account/Principal
Subject != Asset
Subject != Resource
Subject != owner/governor
Subject != observer/recorder/source/transformer
Subject != authority/visibility
Subject != generic related_to
```

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | self measurement, caregiver entry, asset telemetry, environmental reading | PASS | aboutness is required but users need not see Subject ontology |
| CORE-02 Deep chronology | Yes | unknown subject later resolved; wrong subject corrected | PASS WITH HARDENING | later resolution/correction must preserve attribution history |
| CORE-03 Reductio | Yes | remove entity, remove semantics, merge with Person/Actor/Resource/Account | PASS | entity rejected; semantic role required |
| CORE-04 Redundancy | Yes | Subject vs Person/Actor/Asset/Resource/source/context | PASS WITH HARDENING | Subject is role only; adjacent identity concepts remain distinct |
| CORE-05 Traceability | Yes | caregiver Observation about another Person later used in analysis | PASS | subject role composes without changing source/provenance |
| CORE-06 Orphan/independence | Yes | Person exists with no Subject role; Observation may temporarily have unknown Subject where valid | PASS | confirms contextual-role semantics |
| CORE-07 External benchmark | Yes | FHIR, personal-data, person/account patterns | PASS | adapt role/reference separation; reject external taxonomy authority |
| CORE-08 Anti-pattern review | Yes | universal Subject table/root, current-user default invariant | PASS | rejected explicitly |
| CORE-09 Correction/reconciliation/epistemic integrity | Yes | imported reading attributed later; wrong referent corrected | PASS WITH HARDENING | do not fabricate earlier knowledge |
| CORE-10 Scale/performance/history | Yes | many records across people/assets/locations | PASS WITH HARDENING | logical typed-reference mechanism deferred; no semantic supertable required |
| CORE-11 Simple vs power user | Yes | personal self-entry vs caregiver/asset context | PASS | UI may default contextually while kernel retains separation |
| CORE-12 Product value/complexity cost | Yes | ordinary personal capture | PASS | Subject should usually remain hidden/contextual |
| CORE-13 Implementation pressure | Yes | heterogeneous native references | PASS WITH HARDENING | final reference mechanics deferred to logical model |

## Core-gate hardenings incorporated

1. Subject is semantic role, not entity/root.
2. Native referent keeps its identity.
3. Current account holder is not a kernel-level universal Subject default.
4. Subject does not imply source/observer/recorder/owner/authority/visibility.
5. Subject does not become generic `related_to` or absorb focus/context roles.
6. Unknown/later-resolved/corrected Subject attribution preserves material history.
7. Multi-subject cardinality belongs to containing semantics, not fake composite Subject wrappers.
8. Final heterogeneous reference persistence is deferred without changing domain semantics.

Core Gate verdict: **PASS WITH HARDENING**, with hardenings incorporated in `concepts/subject.md`.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | caregiver records about non-account person | PASS | Subject identity references native referent, not account |
| MA-02 Shared fact/actor overlay | Yes | shared record about one Person with private actor overlays | PASS | Subject does not duplicate shared fact per user |
| MA-03 Responsibility/assignment/claim | Limited | Subject may differ from responsible/performing actor | PASS | roles remain separate |
| MA-04 Stewardship/mental load | Limited | caregiver manages data about another person | PASS | Subject does not imply stewardship |
| MA-05 Common ground/state separation | Limited | record about Person X may be asserted by Person Y | PASS | aboutness != assertion/acceptance |
| MA-06 Authority/canonical change | Yes | manager/caregiver records about another | PASS | Subject has no authority semantics |
| MA-07 Selective disclosure | Yes | private Observation about Person X | PASS WITH HARDENING | subject association itself may be sensitive |
| MA-08 Inference privacy | Yes | AI knows subject mapping | PASS WITH HARDENING | resolution knowledge does not create disclosure permission |
| MA-09 Partial adoption/external participant | Yes | non-LifeOS person is Subject | PASS | ordinary supported case |
| MA-10 Assisted participation/provenance | Yes | helper records another person's measurement | PASS | subject, recorder, observer remain distinct |
| MA-11 Relationship lifecycle/revocation | Limited | account/user relationship changes but historical Subject remains | PASS | current access != historical aboutness |
| MA-12 Conflict/adversarial relationship | Yes | manager/employee conflicting assessments | PASS | Subject does not imply authority over truth |
| MA-13 Unequal power | Yes | guardian/caregiver/manager contexts | PASS WITH HARDENING | power does not broaden visibility automatically |
| MA-14 Multi-resource/capacity | Yes | car is both Subject of odometer and Resource for trip | PASS | roles remain independent |
| MA-15 Coordination-burden distribution | Limited | caregiver workflows | PASS | Subject does not assign burden |
| MA-16 Formality/progressive disclosure | Yes | self-entry vs care/work context | PASS | kernel role can remain hidden in simple UI |
| MA-17 AI authority/multi-party context | Yes | AI proposes subject match | PASS WITH HARDENING | proposal does not establish identity/authority automatically |
| MA-18 Specialist-system boundary | Yes | patient/device/location subject patterns | PASS | LifeOS coordinates without rebuilding external identity taxonomies |
| MA-19 Multi-actor primitive redundancy | Yes | universal Subject entity vs role/reference | PASS | entity redundant; role sufficient |
| MA-20 Actor-scoped reality attribution | Yes | shared Observation about one Subject entered by another actor | PASS | subject remains distinct from assertion/participation roles |

Multi-Actor Gate verdict: **PASS WITH HARDENING**, with privacy/authority/AI hardenings incorporated.

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS | Subject creates no duplicate native identity |
| XCON-02 Ownership/authority compatibility | Yes | PASS | no ownership/authority implied |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS | later subject resolution does not rewrite earlier knowledge |
| XCON-04 Relationship compatibility | Yes | PASS WITH HARDENING | Subject is bounded role, not universal relationship catch-all |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS | actor/account independence preserved |
| XCON-06 Language-map compatibility | Yes | PASS | kernel role can remain hidden/contextual in UI |

Cross-Concept Gate verdict: **PASS WITH HARDENING**.

---

# 7. Adjacent Dependency Sweep

| Dependency / boundary | Why it matters | Closure class | Current resolution / why safe to defer | Owner / future concept or stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|---|
| Subject vs observer/recorder/source/transformer | Prevents provenance/role collapse | RESOLVED | Aboutness and origin/action roles are distinct | current Subject/Provenance | future Relationship model tries to collapse them | CORE-04, XCON-04 |
| Subject entity vs semantic role | Avoid duplicate identity/root | RESOLVED | role needed; entity rejected | current Subject | native identity model cannot support role without duplicate truth | CORE-03, CORE-06, XCON-01 |
| Subject vs current Account | Multi-actor/external correctness | RESOLVED | account does not define subject | current Subject | future identity model ties native referent to account | MA-01, MA-09, XCON-01 |
| Subject vs Person/Actor | Human identity and agency | SAFE DEFERRED | role semantics do not require final Person/Actor shape | immediate Person/Actor review | Person/Actor cannot express passive/non-account subject + actor separation | CORE-04, MA-01, MA-09, MA-10, XCON-01 |
| Subject vs Asset | non-person managed objects | SAFE DEFERRED | Asset eligibility does not define aboutness | Asset review | Asset becomes universal managed-object identity conflicting with Subject role | CORE-04, CORE-06, XCON-01 |
| Subject vs Resource | scheduling/capacity role | SAFE DEFERRED | aboutness and capacity are independently meaningful | Resource review | Resource claims to subsume every eligible Subject | CORE-04, MA-14, XCON-01 |
| Subject vs Account/Principal/Authority/Visibility | rights and acting identity | SAFE DEFERRED | Subject explicitly owns none of these semantics | Person/Actor then Relationships | later access model requires Subject itself to own rights/authority | MA-06, MA-07, MA-08, MA-13, MA-17, XCON-02 |
| Subject vs focus/context/typed Relationship | avoids generic related_to | SAFE DEFERRED | bounded primary-aboutness is sufficient now | Relationships / Reasoning | ordinary scenarios cannot distinguish subject from context without semantic change | CORE-04, CORE-05, XCON-04 |

No current dependency is a structural blocker.

---

# 8. Adversarial scenario log

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|
| Self-entered weight | account/person/subject coincidence | PASS | keep coincidence contextual, not invariant |
| Caregiver records grandmother temperature | subject vs recorder/observer/account | PASS | role separation required |
| Car odometer + trip booking | same object Subject and Resource | PASS | independent roles required |
| Unknown imported reading later matched | chronology/epistemic integrity | PASS WITH HARDENING | preserve prior unknown attribution |
| Wrong Person attribution corrected | correction/history | PASS WITH HARDENING | correction must retain history |
| Employee assessment by manager | authority/privacy/conflict | PASS | Subject does not grant truth/visibility |
| AI guesses record belongs to Person X | inference/authority | PASS WITH HARDENING | proposal != established identity |
| Group/environment observation | multiple/collective subject pressure | PASS WITH HARDENING | no fake composite wrapper; cardinality contextual |

---

# 9. Reopening / dependency register

| Finding | Severity | Closure class | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|
| Person/Actor native identity boundary | DEFERRED DEPENDENCY | SAFE DEFERRED | next review | Person/Actor | passive/non-account Subject cannot coexist with actor model |
| Asset eligibility as Subject | DEFERRED DEPENDENCY | SAFE DEFERRED | retain role boundary | Asset | Asset proposed as universal root |
| Resource eligibility as Subject | DEFERRED DEPENDENCY | SAFE DEFERRED | retain role boundary | Resource | Resource proposed to subsume aboutness |
| focus/context semantics | DEFERRED DEPENDENCY | SAFE DEFERRED | Subject kept narrowly primary-aboutness | Relationships | ordinary workflows require materially different boundary |
| heterogeneous reference persistence | DEFERRED DEPENDENCY | SAFE DEFERRED | semantic role accepted, physical mechanism open | logical data model | persistence pressure shows current semantics impossible/unacceptably costly |
| subject association privacy | HARDENING | RESOLVED | explicit non-disclosure invariant | Subject + future Visibility | future policy contradicts separation |

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Rationale

LifeOS materially needs the **Subject semantic role** to express aboutness independently from account, actor, source, ownership and authority. The candidate does **not** justify an independent Subject entity, universal root, or wrapper identity. The accepted baseline is therefore a canonical semantic role/reference capability over native referent identities.

## Hardenings incorporated before acceptance

- no Subject entity/root/table implied;
- current account != universal subject;
- Subject != actor/source/observer/recorder/owner/authority/visibility;
- unknown/later-corrected attribution preserves history;
- focus/context not absorbed into generic Subject;
- privacy and AI-resolution boundaries explicit;
- multi-subject cardinality left to containing semantics/logical model.

## Dependency-sweep summary

- RESOLVED: basic Subject-role identity, subject vs provenance roles, subject vs current account.
- SAFE DEFERRED: Person/Actor, Asset, Resource, Principal/Authority/Visibility, focus/context, heterogeneous reference persistence.
- REOPEN: none.

## Mandatory future re-tests

1. Person / Actor / Account boundary review.
2. Asset review.
3. Resource review with Availability/Capacity.
4. Relationships / Reasoning for focus/context/Authority/Visibility.
5. Logical data-model pressure for heterogeneous references.
6. Cross-Cluster Validation v4.

---

# 11. Regression corpus additions

| Scenario | New boundary covered | Reuse trigger |
|---|---|---|
| caregiver records another person's measurement | subject/account/recorder independence | Person/Actor, Authority, Visibility |
| native object simultaneously Subject and Resource | contextual role composition | Resource/Asset |
| unknown imported subject resolved later | attribution chronology | Provenance/Version/logical model |
| subject association itself reveals sensitive context | inference privacy | Visibility/AI |

---

# 12. Documentation propagation

Before closing:

- [x] concept document created;
- [x] Observation wording updated;
- [x] Language Map updated;
- [x] Domain README updated;
- [x] workstream handoff updated;
- [x] deferrals/reopening triggers recorded;
- [x] no universal Subject entity/table pre-approved.
