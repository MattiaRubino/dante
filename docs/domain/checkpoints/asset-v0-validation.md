# Asset v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — accepted current baseline, mandatory terminology-neutral re-review before final Cluster-4 closure  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Candidate: Asset
- Candidate version: v0
- Adjacent concepts: Subject, Person, Actor, Resource, Observation, Provenance, Place/Location/Property, Document/Artifact, FinancialAccount, inventory/stock, ownership/stewardship/Authority
- Why this review exists: the old discovery grouped many unrelated `Asset/Soggetto` examples together; current modeling must determine whether Asset has a real identity/lifecycle boundary or is merely a convenient generic container.

Special caution recorded during acceptance:

> The term `Asset` itself may bias analysis toward CMMS/inventory conventions. The current result is accepted as the best present baseline but must be re-tested before final Cluster-4 closure using a terminology-neutral comparison of how mature products model managed/tracked things.

---

# 2. Evidence reviewed

## Internal

Reviewed:

- historical `Asset/Soggetto` discovery language;
- Subject v0 and native-referent role semantics;
- Person v0 and Person/Actor/Account boundary;
- Observation v0;
- Availability & Capacity v0;
- Provenance v0;
- multi-actor readiness scenarios;
- car, camera, laptop, equipment, home/property, pet/plant, document, account, inventory and shared-object scenarios.

## External benchmark evidence

External products were evidence only, not design authority.

| Product/system family | Useful lesson | Classification |
|---|---|---|
| CMMS / maintenance systems | individual equipment identity, lifecycle, location, maintenance history | ADAPT |
| IT asset/inventory systems | individually tagged assets often differ from components, accessories, consumables and stock | ADAPT |
| smart-home/device registries | physical device identity can differ from functional entities/state and location/area | ADAPT |
| model/catalog systems | product/model definition differs from physical instance identity | ADAPT |
| provider/integration identity | external identifiers help reconciliation but may not safely define canonical identity | ADAPT |
| universal managed-object root | collapses people, living things, documents, accounts, services and property semantics | ANTI-PATTERN |

Because these benchmark families themselves frequently use `asset`, `device`, `inventory` or similar domain terms, a broader terminology-neutral benchmark remains mandatory.

---

# 3. Candidate definition

> **An Asset is a persistent native representation of an individually tracked non-human physical object whose distinct identity and management history materially matter within LifeOS. Asset identity is independent of ownership, possession, location, current operational state, Subject role, Resource role, current Account context, and external/provider identifiers.**

Classification: **CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE**.

This is not a universal root for managed things.

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | car/camera/laptop/equipment tracked before any maintenance or schedule | PASS | Asset can exist independently of action/workflow |
| CORE-02 Deep chronology | Yes | acquire → repair → lend → sell → retain history | PASS WITH HARDENING | lifecycle changes do not automatically replace identity |
| CORE-03 Reductio | Yes | remove Asset; merge with Subject/Resource/ownership; universal managed-object root | PASS WITH HARDENING | bounded Asset survives; terminology-neutral re-test required |
| CORE-04 Redundancy | Yes | Person, Subject, Resource, inventory, document, financial account | PASS WITH HARDENING | Asset kept narrow; adjacent concepts not absorbed |
| CORE-05 Traceability | Yes | Observation/repair/document history attached to one object | PASS | native records relate to Asset without universal history wrapper |
| CORE-06 Orphan/independence | Yes | stored/retired camera not currently Resource/Subject | PASS | independent native identity demonstrated |
| CORE-07 External benchmark | Yes | CMMS, IT asset, inventory, smart-home/device patterns | PASS WITH HARDENING | useful evidence, but possible terminology bias explicitly retained |
| CORE-08 Anti-pattern review | Yes | every physical item as Asset; every managed thing as Asset | PASS | both rejected |
| CORE-09 Correction/reconciliation/epistemic integrity | Yes | duplicate provider device; wrong serial/object match | PASS WITH HARDENING | no silent merge; history preserved |
| CORE-10 Scale/performance/history | Yes | many physical items, stock, integrations | PASS WITH HARDENING | do not create per-unit Assets for fungible stock |
| CORE-11 Simple vs power user | Yes | user sees `My car`, `Camera`, not ontology | PASS | generic Asset noun need not surface |
| CORE-12 Product value/complexity cost | Yes | shared identity/lifecycle across durable physical categories | PASS WITH HARDENING | survives currently, but boundary must be re-tested cross-domain |
| CORE-13 Implementation pressure | Yes | models, serials, ownership, maintenance, location | PASS WITH HARDENING | no final table hierarchy/type schema pre-approved |

Core Gate verdict: **PASS WITH HARDENING**.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | shared/company/rented object | PASS | Asset identity does not depend on Account |
| MA-02 Shared canonical fact / actor overlay | Yes | one car shared by two people | PASS | one Asset identity; actor-scoped notes/state may differ |
| MA-03 Responsibility/assignment/claim | Yes | maintenance responsible actor differs from owner | PASS | Responsibility not absorbed |
| MA-04 Stewardship/mental load | Yes | one actor monitors maintenance, another owns/uses | PASS | stewardship separate |
| MA-05 Common ground/state separation | Yes | actors disagree on condition | PASS | observations/perspectives need not collapse |
| MA-06 Authority/canonical change | Yes | owner/holder/importer not automatically authority | PASS WITH HARDENING | Asset identity does not grant Authority |
| MA-07 Selective disclosure | Yes | location/serial/value/private notes | PASS WITH HARDENING | related data visibility separate |
| MA-08 Inference privacy | Yes | AI/provider identity matching | PASS WITH HARDENING | matching does not create disclosure permission |
| MA-09 Partial adoption/external participant | Yes | rental/company owner outside LifeOS | PASS | no Account required |
| MA-10 Assisted participation/provenance | Limited | another actor records/maintains Asset | PASS | actor/source roles preserved |
| MA-11 Relationship lifecycle/revocation | Yes | sale/transfer/revoked viewer | PASS | current access != historical Asset identity |
| MA-12 Conflict/adversarial relationship | Yes | disputed ownership/condition | PASS | Asset identity can remain while relations/assertions conflict |
| MA-13 Unequal power | Limited | employer device/caregiver property contexts | PASS | ownership/control does not automatically imply all visibility |
| MA-14 Multi-resource/capacity | Yes | same Asset may be Resource | PASS WITH HARDENING | Resource boundary next mandatory review |
| MA-15 Coordination-burden distribution | Yes | maintenance burden differs from use | PASS | not inferred from Asset identity |
| MA-16 Formality/progressive disclosure | Yes | simple personal object vs managed equipment | PASS | kernel can remain hidden |
| MA-17 AI authority/multi-party context | Yes | AI suggests duplicate/maintenance | PASS WITH HARDENING | AI does not establish ownership/Authority/identity silently |
| MA-18 Specialist-system boundary | Yes | CMMS/device/inventory adapters | PASS WITH HARDENING | adapt identity patterns without importing taxonomy |
| MA-19 Multi-actor primitive redundancy | Yes | universal managed-object entity | PASS WITH HARDENING | current bounded entity survives, broader root rejected |
| MA-20 Actor-scoped reality attribution | Yes | actor-specific notes/condition assertions about shared Asset | PASS | Asset identity does not create one shared perspective |

Multi-Actor Gate verdict: **PASS WITH HARDENING**.

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS WITH HARDENING | native object identity distinct from roles/relations |
| XCON-02 Ownership/authority compatibility | Yes | PASS | ownership/Authority not identity |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS | lifecycle/history survives ownership/use/state changes |
| XCON-04 Relationship compatibility | Yes | PASS WITH HARDENING | ownership/custody/location/Resource remain separate typed relations/roles |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS | one shared Asset identity + actor-scoped overlays |
| XCON-06 Language-map compatibility | Yes | PASS WITH HARDENING | product wording may be Car/Gear/Device; generic Asset term not mandatory UI |

Cross-Concept Gate verdict: **PASS WITH HARDENING**.

---

# 7. Adversarial reductio

## REMOVE Asset

Would force repeated durable-object identity/lifecycle semantics across Vehicle/Camera/Laptop/Tool/etc. or flatten objects into weak generic structures.

**Result:** FAIL under current evidence.

## Asset = Subject

Aboutness is contextual and applies to non-Assets.

**Result:** FAIL.

## Asset = Resource

Capacity/use and identity/history differ.

**Result:** FAIL.

## Asset = owned thing

Rented, borrowed, company-owned and shared objects fail.

**Result:** FAIL.

## Asset = every physical thing

Fungible stock/consumables produce meaningless per-item identity.

**Result:** FAIL.

## Asset = every managed thing

Person, living things, documents, accounts, services, property/place and financial semantics become one dumping ground.

**Result:** FAIL.

## Asset = durable individually tracked non-human physical object

Survives present scenarios with bounded reuse.

**Result:** PASS WITH HARDENING, subject to mandatory terminology-neutral re-review.

---

# 8. Adjacent Dependency Sweep

| Dependency / boundary | Closure class | Current resolution / why safe | Owner / future stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|
| Asset vs Subject | RESOLVED | native identity vs aboutness role | current Asset/Subject | later Asset scope requires Subject wrapper/root | CORE-04, XCON-01 |
| Asset vs Person | RESOLVED | Person human identity; Asset current non-human physical scope | current Asset/Person | stronger native identity abstraction makes boundary artificial | CORE-03, CORE-04, XCON-01 |
| Asset vs fungible stock | RESOLVED conceptually | per-instance Asset only when identity materially matters | current Asset | real workflows need universal per-unit identity or current split fails | CORE-03, CORE-10, CORE-12 |
| Asset vs ownership identity | RESOLVED at identity level | ownership does not define Asset | current Asset | ownership becomes inseparable from object identity in ordinary workflows | CORE-04, XCON-02 |
| Asset vs Resource | SAFE DEFERRED | identity/history and capacity/use are distinct today | immediate Resource review | Resource makes Asset redundant/conflicting or cannot compose cleanly | CORE-03, CORE-04, MA-14, XCON-01, XCON-04 |
| terminology-neutral managed-referent model | SAFE DEFERRED — MANDATORY REVISIT | present physical/durable scope passes, but benchmark may be naming-biased | Cluster-4 integration + dependency closure | broader abstraction explains workflows with fewer exceptions/no semantic loss | CORE-03, CORE-04, CORE-06, CORE-07, CORE-08, CORE-12, CORE-13, MA-18, MA-19, XCON-01, XCON-04, CL-03, CL-04, CL-05, CL-06 |
| Asset vs Place/Location/Property | SAFE DEFERRED | movable-object identity works without final property ontology | future Place/Property review | home/property workflows require shared identity abstraction | CORE-04, XCON-01, XCON-04 |
| Asset vs living entities | SAFE DEFERRED | stable identity can exist outside Asset; no need to force pet/plant in | future concrete workflow review | recurring workflows reveal stronger shared identity model | CORE-03, CORE-04, CORE-06, XCON-01 |
| Asset vs Document/Artifact/FinancialAccount/service | SAFE DEFERRED | materially distinct semantics | future specialist reviews | repeated common identity/lifecycle semantics make exclusions artificial | CORE-03, CORE-04, CORE-12, XCON-01 |
| Asset model/type/profile | SAFE DEFERRED | instance identity can stand alone | logical model/specialist profiles | model/type required to preserve identity/history correctly | CORE-04, CORE-10, CORE-13 |
| Asset merge/split/reconciliation | SAFE DEFERRED | invariant fixed; mechanics open | logical model + Provenance/Version/Decision | imports/integrations cannot preserve identity/history | CORE-02, CORE-09, XCON-01, XCON-03 |

No current structural blocker. The terminology-neutral revisit is mandatory, not optional.

---

# 9. Representative scenarios

## Personal camera

```text
Asset A17 = Sony A7 IV body
serial/provider IDs = identity evidence
Observation = shutter count
Resource role = used for photo shoot
owner/holder = separate relations
```

**PASS**.

## Company laptop

```text
Asset = laptop
owner = company
holder = Person Mattia
maintenance responsibility = IT
```

**PASS** — ownership/holder/responsibility do not define identity.

## Shared car

One physical car with two owners, one current driver, actor-specific notes, shared maintenance facts and private location history.

**PASS WITH HARDENING** — one Asset; Visibility remains separate.

## 100 batteries

No reason to create 100 Asset identities if only stock quantity matters.

**PASS** — physical thing != Asset automatically.

## Pet

Dog has stable identity/history, but current Asset definition excludes living subjects.

**PASS WITH DEFERRED DEPENDENCY** — not evidence that dog must be Asset; revisit only if stronger cross-domain identity abstraction emerges.

## Home/property

Physical property may also be Place/Location and Resource.

**PASS WITH DEFERRED DEPENDENCY** — not enough evidence to collapse those concepts now.

## Duplicate provider representation

Two integrations appear to represent same device.

**PASS WITH HARDENING** — propose reconciliation; no silent identity merge.

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Accepted current baseline

```text
ASSET
CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE

scope:
individually tracked
non-human physical object
identity/history materially matter

not:
universal managed-object root
Person
Subject role
Resource role
ownership relation
financial asset
Document / FinancialAccount / service catch-all
fungible-stock unit by default
living entity by default
```

## Hardenings incorporated

1. physical thing != Asset automatically;
2. managed thing != Asset automatically;
3. individual identity must materially matter;
4. Asset != Subject / Person / Resource;
5. ownership/possession/stewardship do not define identity;
6. provider/serial identifiers are reconciliation evidence, not automatic identity;
7. lifecycle changes do not automatically replace identity;
8. no universal Asset status/history wrapper/table hierarchy pre-approved;
9. adjacent property/living/document/account/service boundaries remain explicit;
10. **mandatory terminology-neutral re-review before final Cluster-4 closure**.

---

# 11. Mandatory future re-tests

1. Resource review — immediate.
2. Data / Subjects cluster integration — destructive redundancy + reconstruction.
3. Terminology-neutral managed/tracked-referent benchmark across personal/inventory/smart-home/property/document/finance/living/service products.
4. Deferred Dependency Closure clusters 1–4.
5. Place/Location/Property if introduced.
6. Relationships/Authority for ownership, possession, custody, stewardship and Visibility.
7. logical model for Asset type/model/profile and identity reconciliation.
8. Cross-Cluster Validation v4.

---

# 12. Documentation propagation

Before closing:

- [x] Asset concept created;
- [x] Subject wording aligned;
- [x] Language Map updated;
- [x] Domain README updated;
- [x] workstream handoff updated;
- [x] terminology-neutral mandatory revisit recorded;
- [x] no universal managed-object root or all-things Asset model pre-approved.
