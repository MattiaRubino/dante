# Backend CP6-01 — Concrete Persistence Coverage Map — Part 1 / 57-of-57 Owner Ledger

- **Status:** CLOSED / GATE 01 PASS
- **Created:** 2026-08-21
- **Hardened:** 2026-08-22
- **Closed:** 2026-08-22
- **Branch:** `feature/logical-postgresql`
- **CP6 authority:** `docs/workstreams/logical-postgresql.md`
- **Canonical continuation:** `docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- **Closure record:** `docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md`
- **Purpose:** account for every one of the 57 CLOSED Logical concepts at the concrete-persistence obligation level without re-performing semantic discovery and without designing business DDL.
- **Write boundary:** documentation only. This document authorizes no business schema, migration, SQLAlchemy business mapping, persistence adapter, use case or API.

This Part 1 and Part 2 have deliberately non-overlapping primary responsibilities:

```text
PART 1
57 / 57 Domain concept owner/role coverage
+ owner-level persistence pressure
+ family/dependency inputs

PART 2
cross-cutting / non-owner contracts
+ LR-01..LR-13 physical-role coverage
+ WL-H01..WL-H12
+ PG-R01..PG-R10
+ DEFER-WL01..20
+ HG-01..HG-12
+ SC-001..SC-035 canonical scenario ledger
+ full PSV ledger
+ CP3 evidence reconciliation
```

Part 1 MUST NOT be used as an alternate source for cross-cutting risk/scenario/PSV applicability. Part 2 is the single CP6-01 cross-cutting ledger. Upstream Domain/Logical/Physical authorities outrank both.

The prior candidate/pre-hardening drafts remain only in Git history; they are not current repository authority.

---

## 1. Authority and no-reinterpretation rule

Consumed authority:

```text
CLOSED Domain Atlas / Whole-Domain
        ↓
CLOSED Whole-Logical 57 / 57
        ↓
latest Slice + Representation Framework hardenings
        ↓
WL-H01..WL-H12
        ↓
CLOSED / SELECTED / ACCEPTED Physical Model
        ↓
accepted PostgreSQL 18.4 mapping thesis
        ↓
CP1–CP5 integrated backend foundation
        ↓
CP6 durable workstream
```

CP6-01 classifies persistence consequences only. It does not change semantic ownership because SQL, ORM, table count or API convenience would be easier.

Exact Whole-Logical counters consumed:

```text
DOMAIN CONCEPTS                 57
CLASSIFIED                      57
UNCLASSIFIED                     0
LR-01 NATIVE OWNERS             15
NEW REPRESENTATION ROOT          0
GENERIC FALLBACK DEPENDENCY      0
```

Canonical non-native contextual roles remain:

```text
Actor
Subject
Resource
```

with no `ActorRef`, `SubjectRef` or `ResourceRef` wrapper identity.

---

## 2. Coverage vocabulary

### Addressability

```text
NativeRef
    only accepted LR-01 native identity owners

ScopedRecordRef
    justified stable address for LR-02 / qualified contextual records

MaterialStateRef
    stable semantic material-state address

ExternalRef
    issuer/provider-scoped external address

none
    no independent semantic address
```

### Materiality/history shorthand

```text
NONE
    no independent material state/history

CONDITIONAL
    only when consequence/history/addressability crosses the accepted threshold

MATERIAL
    exact state/history must remain reconstructible for the applicable material case

REQUIRED WHEN CONSEQUENTIAL
    material state becomes mandatory when the concept is used as consequential basis/effect
```

### Remaining-work classification

```text
INHERITED/CLOSED
CONCRETE DECISION — CP6-02
VERTICAL-SPECIFIC
DIRECT-PROOF
```

The classification refers to remaining physical work, never to reopening the already-CLOSED Logical disposition.

---

## 3. Exact 57/57 owner/role persistence ledger

| # | Concept | Inherited Logical disposition | Concrete persistence pressure | Address / material / history pressure | Remaining physical stage |
|---:|---|---|---|---|---|
| 01 | Acknowledgement | LR-03 typed semantic act/relation | specific attestation relation; qualified record only when materially addressable | Scoped conditional; exact target MaterialState when consequential; material attestation history conditional | CP6-02 REF/MAT/PROV rules + vertical relation design |
| 02 | Activity | LR-01 native owner | owner-specific canonical family | NativeRef; material state/history when consequential; provider mapping only if real | CP6-02 ID/REF/MAT/TX + vertical schema |
| 03 | Actor | contextual agency role, no wrapper identity | role over eligible acting referent | no ActorRef; effect/provenance owns chronology/history | INHERITED/CLOSED role + CP6-02 REF/PROV |
| 04 | Actual | LR-06 realization + LR-02 contextual record | specific realization family, never generic status | Scoped when addressable; material correction/history required for canonical material Actual | CP6-02 MAT/TIM/MISS + vertical |
| 05 | Agreement | LR-02 n-ary contextual record + typed assent | qualified n-ary family with common owned terms state | Scoped material record; terms/state MaterialStateRef required; material assent/amendment history | CP6-02 REL/MAT/PROV + Agreement vertical |
| 06 | Asset | LR-01 native owner | owner-specific canonical family | NativeRef; material history conditional; ExternalRef conditional | CP6-02 ID/REF/MAT + vertical |
| 07 | Authority | LR-03/LR-02 governance state + LR-05 basis + LR-08 effective projection | specific governance relation/state; separate derived effective view | Scoped/Material when consequential; grant/revocation history material | CP6-02 REL/MAT/PROV/TX + security/governance vertical |
| 08 | Availability | LR-05 rule + LR-02 material override + LR-08 effective projection | structured rule/override + derived effective state | Scoped/Material only for consequential overrides/bases; historical rule basis conditional | CP6-02 TIM/TYP/IDX/freshness + vertical |
| 09 | Capacity | LR-04/LR-05/LR-02 as applicable + LR-08 effective projection | typed capability/rule/material context; no CapacityRef | no native identity; material basis conditional; history when governing claims/allocations | CP6-02 TYP/TX + capacity vertical |
| 10 | Collective | LR-01 native owner | owner-specific canonical family independent of member set | NativeRef; material governance/state history conditional | CP6-02 ID/REF/MAT + vertical |
| 11 | Conditional Policy | LR-05 typed policy/specification | owner-specific structured rule/spec family | Scoped/Material only when governing state requires exact history | CP6-02 TYP/MAT/PROV + vertical |
| 12 | Confirmation | LR-03 typed semantic act/relation | specific attestation relation | Scoped conditional; bind exact target MaterialState when consequence matters | CP6-02 REF/MAT/PROV + vertical |
| 13 | Consent | LR-03 scoped relation + LR-02 material state when consequential | specific governance relation/state | Scoped/Material required for consequential basis; grant/withdrawal history material | CP6-02 REL/MAT/PROV/TX + governance vertical |
| 14 | Content Artifact | LR-01 native owner | canonical artifact owner; bytes remain separate bounded object concern | NativeRef; material content state/history when exact revision matters; ExternalRef conditional | CP6-02 ID/MAT/REF/CAP + content vertical |
| 15 | Contribution | LR-03 specific typed relation | qualified attribution/contribution relation | Scoped/Material conditional; history when attribution materially matters | CP6-02 REL/PROV + vertical |
| 16 | Coordination Stewardship | LR-03 specific typed relation | specific stewardship relation, separate from responsibility/authority | Scoped/Material conditional; transfer/history conditional | CP6-02 REL/PROV + vertical |
| 17 | Criterion | LR-05 rule/specification | structured criterion family | Scoped/Material when reused/versioned consequentially; historical basis retained for material Evaluation | CP6-02 TYP/MAT + vertical |
| 18 | Evaluation | LR-08 by default; LR-02 material snapshot when consequential | derived evaluation or bounded material snapshot | no native identity; Scoped/Material only for consequential reproducibility | CP6-02 freshness/MAT/PROV + vertical |
| 19 | Decision | LR-02 conditionally materialized semantic record | specific decision record when independent lifecycle/history matters | Scoped/Material conditional; decision remains distinct from effect | CP6-02 REF/MAT/PROV + vertical |
| 20 | Dependency | LR-03 directional typed contingency | specific contingency relation, no universal DAG edge | Scoped/Material conditional; exact endpoint/facet state when consequential | CP6-02 REL/REF + vertical |
| 21 | Event | LR-01 native owner | owner-specific canonical event family | NativeRef; material state/history conditional; ExternalRef conditional | CP6-02 ID/REF/MAT + vertical |
| 22 | Evidence | LR-03 evaluative-use relation | typed source→evaluation/context use relation; Evidence != truth | Scoped conditional; exact source MaterialState when required | CP6-02 REF/PROV + evaluation vertical |
| 23 | Goal | LR-01 native owner | owner-specific canonical family | NativeRef; material lifecycle/history when consequential | CP6-02 ID/MAT/TX + vertical |
| 24 | Interpersonal Relationship | LR-03 bounded Person-to-Person relation family | specific relation; no generic relationship root | Scoped/Material conditional; effective/history state when material | CP6-02 REL/MAT + relationship vertical |
| 25 | Living Referent | LR-01 native owner | owner-specific canonical family distinct from Person/Asset | NativeRef; material state/history conditional; ExternalRef conditional | CP6-02 ID/REF/MAT + vertical |
| 26 | Membership | LR-03 specific typed relation | specific member↔Collective relation; does not imply governance/participation | Scoped/Material conditional; effective membership history when material | CP6-02 REL/MAT + vertical |
| 27 | Milestone | LR-02 dependent semantic record | scoped dependent intention/attainment family | Scoped when material/addressable; Material conditional; attainment basis historical when material | CP6-02 REF/MAT + planning vertical |
| 28 | Monetary Amount | LR-04 value semantics | typed monetary value owned by containing state | no independent ref/material state; history inherited from owner | CP6-02 TYP + vertical field design |
| 29 | Observation | LR-01 native owner | owner-specific observational family | NativeRef; MaterialState required for material correction/history; ExternalRef conditional | CP6-02 ID/MAT/TIM/PROV + observation vertical |
| 30 | Occurrence | LR-01 once an individual canonical occurrence is semantically distinguished | native expected-instance family with pre-materialization locator boundary | NativeRef once distinguished; governing source/material state lineage required; material instance history when differentiated | CP6-02 ID/REF/TIM + recurrence/Occurrence vertical |
| 31 | Outcome | LR-06 result + LR-02 when materially persistent | specific result/disposition family | Scoped/Material conditional; absence remains distinct from negative result | CP6-02 MISS/MAT + vertical |
| 32 | Ownership | LR-03 specific typed relation | specific ownership relation, distinct from possession/authority | Scoped/Material conditional; effective transfer history when material | CP6-02 REL/MAT/TX + vertical |
| 33 | Participation | LR-03 specific typed relation | specific intended/accepted participation relation | Scoped/Material conditional; response/history material when needed; actual participation remains separate | CP6-02 REL/MAT + vertical |
| 34 | Person | LR-01 native owner | owner-specific canonical family separate from Account/Principal/Actor | NativeRef; material state/history conditional; ExternalRef conditional | CP6-02 ID/REF/MAT/LIFE + vertical |
| 35 | Place | LR-01 native owner | owner-specific canonical family with bounded geo capability pressure | NativeRef; material address/geometry correction history conditional; ExternalRef conditional | CP6-02 ID/MAT/CAP + Place vertical for exact PostGIS shape |
| 36 | Plan | LR-01 native owner | owner-specific canonical strategy family | NativeRef; exact material plan state/history required when later meaning depends on revision | CP6-02 ID/MAT/TX + planning vertical |
| 37 | Possession | LR-03 specific typed relation | specific custody/holding relation distinct from ownership/allocation | Scoped/Material conditional; effective transfer history when material | CP6-02 REL/MAT + vertical |
| 38 | Possibility | LR-01 once retained as canonical Possibility | native future-option family distinct from Goal | NativeRef after canonical retention; material history conditional; AI candidate before acceptance remains noncanonical | CP6-02 ID/MAT + possibility vertical |
| 39 | Proposal | LR-02 conditionally materialized semantic record | specific proposal family when review/version/history matters | Scoped/Material conditional; target exact state when consequential | CP6-02 REF/MAT/PROV + vertical |
| 40 | Provenance | LR-07 typed lineage/history semantics | bounded typed provenance/lineage; no universal graph root | exact source/target refs/material states as required; material by definition where retained | CP6-02 PROV/MAT + owner-specific vertical binding |
| 41 | Quantity | LR-04 value semantics | typed magnitude/unit value owned by containing state | no independent ref/material state; history through owner | CP6-02 TYP + vertical field design |
| 42 | Reconciliation | transient reasoning when low consequence; LR-02/LR-07 material record when resolution matters | bounded conflict/resolution/lineage record | Scoped/Material conditional→required for material resolution; competing source/state refs retained | CP6-02 MAT/PROV/TX + integration/identity vertical |
| 43 | Recurrence | LR-05 typed rule/specification | structured recurrence-family rule, not provider/RRULE ontology | Scoped/Material conditional→required when historical Occurrences depend on exact rule state | CP6-02 TYP/TIM/MAT + recurrence vertical |
| 44 | Representation | LR-03 action-scoped relation + LR-02 when consequential | specific acting-on-behalf-of governance relation | Scoped/Material when consequential; actual Actor and represented party remain distinct | CP6-02 REL/PROV/TX + governance vertical |
| 45 | Request | LR-02 conditionally materialized semantic record | specific directed request family | Scoped/Material conditional; Request != Authority/effect | CP6-02 REF/PROV/IDEM + vertical |
| 46 | Resource Allocation | LR-03 typed relation + LR-02 qualified record when material | specific allocation family distinct from capacity claim/actual use | Scoped/Material when consequential; exact requirement/schedule basis | CP6-02 REL/REF/MAT/TX + resource vertical |
| 47 | Resource Requirement | LR-05 specification + LR-02 when materially addressable | structured requirement/specification family | Scoped/Material conditional→required when Allocation/Decision depends on exact state | CP6-02 TYP/REF/MAT + resource vertical |
| 48 | Resource | contextual role/capability, no wrapper identity | heterogeneous eligible-provider role | no ResourceRef; eligible target may be Native/Scoped/value/service/pool/specialist representation | INHERITED/CLOSED role + CP6-02 Reference Contract doctrine |
| 49 | Responsibility | LR-03 specific typed relation | specific accountability relation distinct from performer/steward/authority | Scoped/Material conditional; transfer/history when material | CP6-02 REL/MAT/PROV + vertical |
| 50 | Routine | LR-01 native owner | owner-specific recurring-intention family | NativeRef; material governing state/history required when Occurrences depend on exact state | CP6-02 ID/MAT/TIM + routine/recurrence vertical |
| 51 | Schedule | LR-02 dependent semantic record + ScopedRecordRef where material/addressable | accepted-placement family distinct from Occurrence/Session/Actual/Capacity Claim | Scoped + Material for consequential placement; historical placements retained; ExternalRef conditional | CP6-02 TIM/TX/IDX/MAT + scheduling vertical |
| 52 | Session | LR-01 native owner | actual execution-episode family | NativeRef; material correction/split/merge history conditional; ExternalRef conditional | CP6-02 ID/TIM/MAT + execution vertical |
| 53 | Subject | contextual aboutness/target role, no wrapper identity | role over eligible ReferenceAddress target | no SubjectRef; history/address belongs containing record | INHERITED/CLOSED role + CP6-02 Reference Contract doctrine |
| 54 | Temporal Constraint | LR-05 typed rule/specification | structured temporal constraint family distinct from Schedule | Scoped/Material conditional when consequential/historical | CP6-02 TYP/TIM + planning/scheduling vertical |
| 55 | Verification | Evaluation purpose/profile, not independent root | uses Evaluation LR-08 or material LR-02 snapshot | no own ref family; inherits Evaluation material state/history when justified | INHERITED/CLOSED + CP6-02 freshness/MAT + evaluation vertical |
| 56 | Version | LR-07 material-state/history semantics | cross-cutting owner/facet material-state role; no universal Version root | MaterialStateRef; current binding/lineage/dual chronology as applicable | CP6-02 MAT/HIST/TIM core constitution |
| 57 | Visibility | LR-03/LR-02 scoped governance state + LR-05 basis + LR-08 effective projection | specific disclosure state/policy + derived effective surface | Scoped/Material when consequential; grant/revocation history material | CP6-02 REL/MAT/PROV/disclosure + security vertical |

### 3.1 Census result

```text
ROWS EXPECTED                      57
ROWS PRESENT                       57
DUPLICATE CONCEPTS                  0
MISSING CONCEPTS                    0
EXTRA DOMAIN CONCEPTS               0
SEMANTIC RECLASSIFICATIONS           0
```

---

## 4. Exact LR-01 native identity set

Exactly these 15 rows above carry LR-01 native identity:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Possibility
Goal
Plan
Activity
Event
Routine
Occurrence
Session
Observation
```

Count:

```text
EXPECTED  15
PRESENT   15
EXTRA      0
MISSING    0
```

Important hardenings:

- `Occurrence` gains LR-01 NativeRef only once an individual canonical occurrence is semantically distinguished; lazy derivation before materialization does not invent identity.
- `Actor`, `Subject`, `Resource` remain contextual roles.
- `Person != Account != Principal != Actor`.
- `Living Referent != Person != Asset`.
- `Possibility != Goal`.

---

## 5. Aggregate persistence-family pressure

The 57 rows produce these reusable physical pressure families; these are **not** table counts.

### 5.1 Native canonical owners

```text
15 LR-01 owner-specific canonical families
```

The accepted PostgreSQL mapping already rejects a common semantic parent Entity row.

### 5.2 Dependent/material contextual records

Representative pressure includes:

```text
Actual
Agreement
Milestone
Proposal
Request
Decision
Schedule
Outcome
material Evaluation
material Reconciliation
material Criterion
material Resource Requirement
material Availability/Capacity context
qualified governance/relation records
```

Stable contextual addressability uses `ScopedRecordRef` only when justified; it never inflates LR-02 into LR-01.

### 5.3 Specific typed relations

Representative families include:

```text
Acknowledgement
Confirmation
Evidence
Dependency
Interpersonal Relationship
Membership
Participation
Responsibility
Coordination Stewardship
Contribution
Ownership
Possession
Resource Allocation
Authority
Consent
Visibility
Representation
Agreement party assent
```

No universal `relationship(from,type,to,payload)` canonical fallback is admitted.

### 5.4 Rule/policy/specification pressure

```text
Conditional Policy
Criterion
Recurrence
Resource Requirement
Temporal Constraint
Availability rules
bounded Authority/Visibility policy bases
Capacity compatibility/policy
```

Reusable expression machinery may be technical infrastructure later, but it may not become a universal semantic `Rule` root.

### 5.5 Value pressure

```text
Quantity
Monetary Amount
typed temporal values
typed capacity dimensions where numeric
```

Value semantics inherit identity/history from the containing semantic owner/state.

### 5.6 History/material truth

Cross-cutting material truth requires, where applicable:

```text
MaterialStateRef
owner/facet-specific material state
explicit current accepted-state binding
typed correction/replacement/reconciliation lineage
world/effective chronology
recorded/learned/accepted/corrected chronology
```

No universal Fact/Version/Event ontology is introduced.

### 5.7 Provider and derived pressure

```text
LR-09 provider/external state
!= canonical

LR-08 projection/search/effective state
!= canonical

LR-11 candidate/unresolved state
!= accepted canonical state
```

Part 2 owns the complete physical-role/cross-cutting ledger for LR-01..LR-13.

---

## 6. Dependency-pressure inputs for CP6-03

This is not yet the final Implementation Dependency DAG. It records reusable prerequisites that CP6-03 must order.

```text
F1  physical identity + ReferenceAddress / Reference Contract
F2  material-state identity + current accepted binding + history lineage
F3  expected-state + idempotency + transaction/concurrency doctrine
F4  consequential provenance/governance linkage
F5  absence/unknown/negative/redacted/tombstone semantics
F6  typed temporal/recurrence representation doctrine
F7  derived/search/disclosure freshness and noncanonical boundaries
F8  migration/evolution continuity doctrine
```

High-leverage consumers:

```text
Agreement       needs F1/F2/F3/F4/F5
Observation     needs F1/F2/F4/F6
Plan/Routine    need F1/F2/F3/F6
Occurrence      needs F1/F2/F3/F6
Schedule        needs F1/F2/F3/F5/F6
Authority/
Consent/
Visibility      need F1/F2/F3/F4/F5/F7
Resource /
Allocation      need F1/F2/F3/F5/F6
provider paths  need F1/F2/F3/F4/F5 plus LR-09 separation
```

The exact vertical decomposition and final DAG belong only to CP6-03.

---

## 7. What Part 1 intentionally does not duplicate

To prevent two competing truths, Part 1 does **not** maintain separate detailed ledgers for:

```text
WL-H01..WL-H12 applicability
PG-R01..PG-R10 applicability
DEFER-WL01..20 disposition
HG-01..HG-12 carry-forward
SC-001..SC-035 names/stages
PSV-01..47 + PSV-28A/B stages
CP3 technical-vs-semantic evidence reconciliation
cross-cutting/non-owner constructs
LR-01..LR-13 physical-role matrix
```

Those are all owned by the canonical continuation:

`docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md`

This is deliberate normalization, not missing documentation.

---

## 8. CP6-02 concrete-decision handoff

The 57/57 ledger confirms that the genuinely global unresolved PostgreSQL questions are foundation questions rather than new semantic discovery.

CP6-02 must close reusable doctrine for at least:

```text
ID       physical identifier policy / generation / exposure
REF      concrete direct-FK vs bounded-anchor topology and integrity
MAT      MaterialState/current-binding/lineage topology
HIST/TIM materiality threshold + world/effective vs recorded/learned chronology
MISS     NULL / absence / unknown / negative / N/A / redacted / unavailable
TYP      PostgreSQL type / ENUM / CHECK / lookup / domain / range doctrine
REL      direct / qualified / n-ary relational patterns
PROV     consequential provenance pattern
LIFE     retirement / tombstone / redaction / anti-resurrection mechanics
CON      constraint-placement doctrine
TX       locking/isolation/retry/conflict taxonomy
IDEM     idempotency scope/fingerprint/replay/conflict doctrine
IDX      indexing doctrine tied to actual query evidence
CAP      PostGIS/FTS/pg_trgm/pgvector/JSONB activation rules
MIG      business migration/evolution constitution
SEC      future business objects under existing owner/migrator/runtime contract
QA       non-speculative direct-proof doctrine
```

Exact business tables/columns/indexes remain vertical-specific and are not designed here.

---

## 9. Gate-01 closure result

The final independent Part 1 + Part 2 + source-authority review is complete and the separately authorized closure record has been produced.

```text
57 / 57 Domain concepts accounted                  PASS
15 / 15 LR-01 native owners                        PASS
Actor / Subject / Resource wrapper identity        0
owner-level addressability pressure                PASS
owner-level material/history pressure              PASS
owner-level remaining-stage classification         PASS
aggregate physical-family pressure                 PASS
dependency-pressure inputs                         PASS

new Domain owner                                   0
generic Entity/Thing requirement                   0
generic Relationship requirement                  0
generic Rule/Fact/Version root                     0
canonical EAV/property-bag requirement             0
required-semantic JSONB escape hatch               0
business table/column/index design                 0
business migration                                 0
business SQLAlchemy mapping                        0
persistence adapter                                0
Physical Model reopen                              0
```

Formal checkpoint state:

```text
CP6-01
CLOSED / GATE 01 PASS
```

The closure record is authoritative for the gate evidence and repository write boundary.

---

## 10. Resume point

```text
CP6-01
CLOSED / GATE 01 PASS
        ↓
CP6-02 PostgreSQL Persistence Constitution
NEXT / NOT STARTED
```

CP6-02 may now begin under its own design/write gates. No business DDL, migration, SQLAlchemy business mapping, persistence adapter, application use case or business API is authorized by CP6-01 closure.