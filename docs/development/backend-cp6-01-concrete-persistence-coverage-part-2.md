<!-- DANTE-CANONICAL-CONTINUATION document="backend-cp6-01-concrete-persistence-coverage.md" follows="backend-cp6-01-concrete-persistence-coverage.md" -->

# Backend CP6-01 — Concrete Persistence Coverage Map — Part 2 / Cross-Cutting Hardening

- **Status:** CP6-01 HARDENING CANDIDATE / FINAL INDEPENDENT REVIEW REQUIRED / GATE 01 NOT PASSED
- **Created:** 2026-08-21
- **Last hardening:** 2026-08-22
- **Branch:** `feature/logical-postgresql`
- **Part-1 authority:** `docs/development/backend-cp6-01-concrete-persistence-coverage.md`
- **CP6 authority:** `docs/workstreams/logical-postgresql.md`
- **Purpose:** close cross-cutting coverage and traceability gaps without changing the 57/57 Logical census, reopening Domain/Logical/Physical, or introducing business DDL.

This continuation is normative only for CP6-01 coverage hardening. It does not alter upstream semantic dispositions. Where this continuation refines Part 1 on cross-cutting applicability or stage ownership, this continuation is the newer CP6-01 interpretation. Upstream Domain/Logical/Physical authority remains higher than either CP6-01 document.

```text
THIS DOCUMENT
= CP6-01 coverage hardening

THIS DOCUMENT
!= Gate 01 PASS
!= CP6-02 Constitution
!= business schema
!= Physical Model redesign
```

---

## 1. Hardening method and authority reconstruction

The hardening pass was rebuilt from source authorities rather than from Part 1 alone.

Rechecked authority chain:

```text
Domain final closure
→ Whole-Logical 57/57
→ latest Slice / Representation Framework continuations
→ WL-H01..WL-H12
→ Whole decision / DEFER-WL register
→ Governed Operation / Effect Contract
→ Physical Benchmark Scenario Corpus
→ accepted PostgreSQL mapping
→ PM-03 HG semantics
→ PG-R01..PG-R10
→ PM-11 / PM-12 / PM-13 / PM-14
→ Post-Selection Validation register
→ CP3 actual technical persistence evidence
→ CP6 durable handoff
→ CP6-01 Part 1
```

No Domain owner, Logical representation, Physical selection or accepted topology is reopened by this document.

---

## 2. Coverage findings and corrected traceability

### F-01 — 57/57 Domain coverage is necessary but not sufficient

Part 1 correctly accounts for all 57 accepted Domain concepts and exactly 15 LR-01 native owners. Persistence readiness also depends on cross-cutting contracts that are intentionally **not Domain owners**.

Therefore Gate 01 requires:

```text
57 / 57 Domain concept coverage
+
cross-cutting / non-owner persistence-contract coverage
+
LR-01..LR-13 representation-role coverage
+
WL-H01..WL-H12 coverage
+
PG-R01..PG-R10 coverage
+
DEFER-WL01..20 disposition
+
HG-01..12 carry-forward
+
SC-001..SC-035 stage ownership
+
PSV full-register stage ownership
```

### F-02 — PG-R01 is anchor-family pressure

`PG-R01 technical anchor leakage` applies to every bounded technical address/state anchor actually justified, including native and any later scoped/material anchor. It is not a 15-owner-only risk.

### F-03 — PG-R02 spans the complete reference contract

Heterogeneous-reference integrity spans `NativeRef`, `ScopedRecordRef`, `MaterialStateRef`, `ExternalRef`, slot eligibility, scope and target existence.

### F-04 — WL-H06 is operation/effect-level

Idempotency applies wherever retry/replay can duplicate a material effect. It is not semantically owned by Activity, Decision, Proposal or Request merely because those are common consumers.

### F-05 — PG-R08 includes every accepted recurring source

Lazy Occurrence materialization must preserve governing source/material state whether the source is Routine, recurring Event or another explicitly accepted recurring source.

### F-06 — LR-09..LR-13 remain explicit

Provider/external, flexible metadata, unresolved/candidate, product/profile and specialist roles must not disappear merely because the 57-owner census foregrounds canonical concepts.

### F-07 — DEFER-WL01..20 are all assigned

Every Whole-Logical deferred implementation question is classified as already CLOSED, a CP6 concrete decision, vertical-specific, runtime/security-specific or capability-triggered.

### F-08 — HG / SC / PSV IDs are retained as reusable evidence contracts

Later implementation must reuse the established IDs and semantic assertions rather than recreating equivalent tests under new names.

### F-09 — CP3 direct QA is not semantic HG execution

```text
CP3 TECHNICAL PERSISTENCE FOUNDATION
DIRECT QA PASS

DANTE BUSINESS PERSISTENCE
NOT IMPLEMENTED

PHYSICAL SEMANTIC HG DIRECT PASS
not manufactured by CP3

PSV DIRECT PASS
only after the exact selected-stack subject exists and is executed
```

### F-10 — non-57 constructs stay non-57

`Account`, `Principal`, `ReferenceAddress`, governed-operation vocabulary, Capacity Claim pressure and technical persistence mechanisms may be persistence-relevant without becoming members of the Domain census.

### F-11 — SC-017 / SC-018 traceability is now canonical and singular

The canonical Physical Benchmark Scenario Corpus defines:

```text
SC-017
Search hidden-result non-interference

SC-018
FTS mixed filter/query
```

Post-closure documentation maintenance on 2026-08-22 reconciles every active Physical/CP6 carry-forward reference to that canonical meaning:

```text
PSV-06 -> SC-017 search hidden-result non-interference
PSV-07 -> SC-018 FTS mixed filter/query correctness under applicable Visibility/user/scope filtering
```

`SC-017` already covers observable leakage surfaces including contents, counts, ranking, error behavior and timing classes. Those surfaces are not duplicated under `SC-018`.

Maintenance rule:

```text
Physical Benchmark Scenario Corpus
= canonical SC identifier/name authority

PSV / acceptance / result / CP6 ledgers
MUST consume those identifiers
MUST NOT rename them locally
```

No semantic obligation was added or removed by this correction.

---

## 3. Cross-cutting / non-owner persistence ledger

| Contract / construct | Accepted role | Persistence pressure | Classification | Assigned stage | Hard barrier |
|---|---|---|---|---|---|
| ReferenceAddress | discriminated Logical address contract, not semantic owner | NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef | INHERITED/CLOSED | CP6-02 REF | no generic kind+id / universal Entity |
| Reference Contract | eligibility/scope contract for each reference slot | family/role/facet eligibility + target existence | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 REF | direct FK when homogeneous; bounded anchor only when genuinely heterogeneous |
| NativeRef | stable LR-01 address | exactly 15 native owner families | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 ID/REF | never reused; no ActorRef/SubjectRef/ResourceRef wrappers |
| ScopedRecordRef | stable address for justified LR-02/qualified contextual records | concrete scoped family; bounded heterogeneous support only if justified | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 REF | distinct from NativeRef and MaterialStateRef |
| MaterialStateRef | stable semantic material-state address | owner/facet material state | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 MAT/HIST | not xmin/xid/ETag/hash/provider revision; not equivalent to current |
| ExternalRef | issuer-scoped external address | provider + scope + external object identity | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 REF / integration vertical | provider identity/state never automatically canonical |
| Current accepted-state binding | explicit owner/facet → accepted MaterialStateRef binding | material current state | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 MAT | current != highest revision/latest inserted row |
| Correction/replacement/reconciliation lineage | typed historical lineage | material states + typed lineage | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 MAT/HIST/PROV | no silent overwrite; no universal event ontology |
| World/effective chronology | when state applies in represented reality | owner/facet-specific time/range | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 TIM/HIST | no blanket bitemporality |
| Recorded/learned/accepted chronology | when DANTE learned/recorded/accepted/corrected state | owner/facet-specific chronology | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 TIM/HIST | distinct from world chronology where material |
| Governed Operation / Effect Contract | application/technical contract for consequence | target, effect, expected state, input, purpose, governance, result axes | INHERITED/CLOSED | CP6-02 PROV/TX/IDEM + verticals | no universal Domain Operation/Command/Effect owner |
| Governed Operation Request | bounded application request | persistent only where consequence/audit/recovery requires | VERTICAL-SPECIFIC | CP6-05 / post-CP6 vertical | HTTP/UI/tool action != semantic effect |
| Execution receipt/result | bounded technical execution/result axes | persistence where recovery/audit requires | VERTICAL-SPECIFIC | post-CP6 runtime/vertical | runtime completion != Domain Actual/Outcome automatically |
| Idempotency record | retry/effect control | scope + key + material operation fingerprint + bounded result | CONCRETE DECISION | CP6-02 IDEM | idempotency != identity |
| Correlation/causation references | technical linkage | request/effect/runtime/provider/reconciliation correlation | CONCRETE DECISION + VERTICAL-SPECIFIC | CP6-02 PROV + vertical | does not replace Domain Provenance |
| Projection / Disclosure Surface Contract | recipient-context derived/disclosure contract | material source basis + projection kind + purpose + exposure boundary | INHERITED/CLOSED | CP6-02 freshness/disclosure + security/query vertical | no ProjectionRef requirement; derived != canonical |
| Provider/sync/apply state | LR-09 | external mapping/revision/apply/sync/reconciliation | INHERITED/CLOSED + VERTICAL-SPECIFIC | integration vertical | provider != canonical |
| Flexible low-consequence metadata | LR-10 | bounded JSONB or typed flexible metadata | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 CAP | required semantics cannot disappear into JSONB |
| Candidate/unresolved interpretation | LR-11 | candidate/unresolved structures when needed | INHERITED/CLOSED + VERTICAL-SPECIFIC | later vertical | confidence/newest/provider result cannot self-canonicalize |
| Product/organizational profile | LR-12 | profile structures over accepted semantics | INHERITED/CLOSED + VERTICAL-SPECIFIC | later product vertical | UI/profile grouping != kernel owner |
| Specialist extension | LR-13 | bounded specialist structures | INHERITED/CLOSED + VERTICAL-SPECIFIC | specialist vertical | no flattening into generic Observation/payload |
| Account | application/security construct outside 57 | separate account persistence if Access/security needs it | VERTICAL-SPECIFIC under inherited barrier | CP6-03/04/05 if relevant | Person != Account |
| Principal/security context | technical security identity/context outside 57 | AuthZ/provenance context | INHERITED/CLOSED boundary + VERTICAL-SPECIFIC | security vertical | Principal != Actor/Person; ALLOW != Authority |
| Actor role | contextual agency role | eligible referent address | INHERITED/CLOSED | CP6-02 REF/PROV | no ActorRef |
| Subject role | contextual aboutness role | eligible ReferenceAddress via owning contract | INHERITED/CLOSED | CP6-02 REF | no SubjectRef |
| Resource role | contextual provider/capability role | eligible native/scoped/value/service/pool/specialist representation | INHERITED/CLOSED | CP6-02 REF | no ResourceRef / NativeRef-only assumption |
| Capacity Claim pressure | accepted scheduling/capacity construct/facet, not added to 57 census | own material basis/temporal footprint where required | INHERITED/CLOSED + VERTICAL-SPECIFIC | CP6-03 DAG / capacity vertical | Schedule != Capacity Claim != Allocation != Actual use |
| Tombstone/retirement/redaction continuity | retention truth | minimal permitted address/history continuity | INHERITED/CLOSED + CONCRETE DECISION | CP6-02 LIFE | redacted/unavailable != never existed; NativeRef never reused |
| Anti-resurrection reconciliation | recovery-side enforcement | suppression/reconciliation state/mechanism | CONCRETE DECISION + DIRECT-PROOF | CP6-02 LIFE/MIG + recovery stage | no paper PASS for PSV-01/03/40 |
| Transactional outbox | selected bounded Class-A runtime mechanism | PostgreSQL technical runtime state only on real Class-A need | INHERITED/CLOSED TARGET / NOT MATERIALIZED IN CP6-01 / CAPABILITY-TRIGGERED | later async/runtime vertical | not Domain history; not universal event store |
| PowerSync/encrypted SQLite | selected noncanonical local/sync substrate | approved client projection + local staging | INHERITED/CLOSED TARGET / CAPABILITY-TRIGGERED | offline/mobile activation | local != canonical; consequential LWW forbidden |
| Search/vector indexes/caches | LR-08 derived/query state | FTS/trgm/unaccent/pgvector/rebuildable projection | INHERITED/CLOSED TARGET + VERTICAL-SPECIFIC | search/query vertical | retrieval result != canonical truth |

Census barrier:

```text
DOMAIN CONCEPTS                     57 / 57
LR-01 NATIVE OWNERS                 15 / 15
ADDITIONAL DOMAIN OWNERS FROM CP6         0
```

---

## 4. LR-01..LR-13 complete physical-role coverage

| LR | Logical role | PostgreSQL pressure | Addressability | Canonicality | Non-collapse barrier | Next stage |
|---|---|---|---|---|---|---|
| LR-01 | native identity-bearing record | owner-specific canonical family | NativeRef | canonical | exactly 15 native owners | CP6-02 ID/REF + vertical |
| LR-02 | dependent/material contextual record | owner-specific contextual/qualified family | ScopedRecordRef when justified; MaterialStateRef where material | canonical when accepted/material | no native-identity inflation | CP6-02 REF/MAT + vertical |
| LR-03 | specific typed association/relation | dedicated relation family / qualified contextual record when consequential | endpoint refs + conditional Scoped/Material refs | canonical relation state | no universal edge | CP6-02 REL + vertical |
| LR-04 | value semantics | typed columns/composites/dependent values | no independent identity by default | canonical within owner state | Quantity != Monetary Amount; no scalar bag | CP6-02 TYP + vertical |
| LR-05 | rule/policy/specification | structured owner-specific rule/spec families | Scoped/Material refs when justified | canonical rule/spec where accepted | no universal Rule(type,payload) | CP6-02 TYP/REL/MAT + vertical |
| LR-06 | realization/result | specific Actual/Outcome/etc family | Scoped/Material refs as required | canonical when established | no generic result/status root | vertical after CP6-02 |
| LR-07 | version/correction/lineage/history | material-state + typed lineage/provenance | MaterialStateRef; scoped refs for qualified records | canonical history | no universal Version/Event ontology | CP6-02 MAT/HIST/PROV |
| LR-08 | derived/effective projection | view/materialized/cache/read state | source/material basis; identity not automatic | noncanonical by default | cache != truth | CP6-02 CAP/freshness + query vertical |
| LR-09 | provider/external state/mapping | integration structures | ExternalRef + canonical/scoped mapping | noncanonical provider state | provider revision/state != canonical | integration vertical |
| LR-10 | flexible low-consequence metadata | bounded JSONB/typed metadata | owned by containing record | canonical only as bounded metadata | no required semantics in JSONB | CP6-02 CAP + vertical |
| LR-11 | unresolved/candidate interpretation | candidate/unresolved structures | bounded refs/bases | noncanonical until accepted | no automatic promotion | later vertical |
| LR-12 | product/organizational profile | profile structures | underlying owner refs | profile/non-kernel | product vocabulary != owner root | product vertical |
| LR-13 | specialist extension | specialist schema/records | specialist-specific | canonical only within accepted specialist boundary | no generic core flattening | specialist vertical |

```text
LR FAMILIES ACCOUNTED  13 / 13
UNCLASSIFIED LR FAMILY       0
GENERIC FALLBACK REQUIRED    0
```

---

## 5. WL-H01..WL-H12 applicability map

| WL-H | Contract | True pressure surface | Stage | Barrier |
|---|---|---|---|---|
| WL-H01 | Agreement terms bind justified owned MaterialStateRef | Agreement/material terms | CP6-02 MAT/REL + Agreement vertical | no TermsRef/unowned terms_id |
| WL-H02 | Governed Operation / Effect Contract | every consequential effect | CP6-02 PROV/TX/IDEM + verticals | operation vocabulary not Domain owner |
| WL-H03 | Projection / Disclosure Surface | derived/search/disclosure surfaces | CP6-02 freshness/disclosure + security/query | no universal ProjectionRef |
| WL-H04 | absence != false | whole model | CP6-02 MISS + every vertical | NULL/row absence not universal negative |
| WL-H05 | expected-state | stale-write-sensitive consequential mutation | CP6-02 TX + real race proof | storage token != MaterialStateRef |
| WL-H06 | idempotency != identity | retryable/replayable material effect | CP6-02 IDEM + real retry proof | same key + different op conflicts |
| WL-H07 | multi-owner consistency | invariant-spanning effect | CP6-02 TX + vertical proof | no hidden partial success |
| WL-H08 | canonical != provider sync/apply | all LR-09 integration | CP6-02 boundary + integration vertical | provider does not overwrite canonical automatically |
| WL-H09 | LR-08 freshness | consequential use of derived/cached/search/vector/solver/effective state | CP6-02 CAP/freshness + vertical | stale derived state cannot authorize consequence |
| WL-H10 | retention/redaction/tombstone | address/history/downstream copies | CP6-02 LIFE + destructive proof later | redacted != never existed; NativeRef non-reuse |
| WL-H11 | consequential AuthZ provenance | governed consequential effect | CP6-02 PROV + security/effect vertical | Actor/represented party/Principal/governance/technical decision distinct |
| WL-H12 | non-interference | every recipient-observable surface | CP6-02 disclosure + system security proof | no leakage by existence/count/rank/error/timing/etc. |

---

## 6. PG-R01..PG-R10 applicability / stage map

| PG-R | Risk | True pressure surface | Assigned stage | Gate rule |
|---|---|---|---|---|
| PG-R01 | technical anchor leakage | every justified native/scoped/material technical anchor | CP6-02 REF + later representative proof | address metadata only; no generic Domain state/lifecycle |
| PG-R02 | heterogeneous reference integrity | ReferenceAddress + Reference Contract across Native/Scoped/Material/External | CP6-02 REF + real wrong-family/dangling proof post-CP6 | enforce eligibility/existence; direct FK when homogeneous |
| PG-R03 | history maintainability | representative LR-01/LR-02/LR-03 material-history families | CP6-02 MAT/HIST + vertical proof | no universal state/history escape hatch |
| PG-R04 | expected-state concurrency | stale-write-sensitive consequential mutations | CP6-02 TX + SC-001-style real race post-CP6 | no silent LWW |
| PG-R05 | multi-owner write skew | predicate/invariant-spanning writes | CP6-02 TX + invariant-specific proof | READ COMMITTED not automatically sufficient |
| PG-R06 | Agreement/governance materiality | Agreement + material Consent/Authority/Visibility/Representation bases | CP6-02 REL/MAT/PROV + governance vertical | common terms state and change history reconstructible |
| PG-R07 | temporal/history semantics | material history needing world/effective + recorded/learned axes | CP6-02 TIM/HIST + history proof | no universal bitemporal Fact root |
| PG-R08 | lazy Occurrence | Occurrence + Recurrence + Routine + recurring Event/other accepted source | CP6-02 ID/REF/TIM + recurrence vertical | locator→NativeRef preserves identity/source lineage |
| PG-R09 | selective disclosure/non-interference | shared canonical state + recipient-specific query/projection/security surfaces | CP6-02 disclosure + system/security proof | FK/error/count/rank/timing/source leakage included |
| PG-R10 | retention/restore | addresses/history/tombstones/restore reconciliation | CP6-02 LIFE/MIG + destructive proof later | no paper anti-resurrection PASS |

Potential bounded address infrastructure remains conceptually separate:

```text
native address anchor
scoped address anchor only if genuinely required
material-state address/control anchor
external address structures
```

CP6-02 must justify exact topology. CP6-01 does **not** pre-decide that every conceptual anchor becomes a table.

---

## 7. Whole DEFER-WL01..20 disposition matrix

| Deferred | Question | Current disposition | Owner/stage | CP6 interpretation |
|---|---|---|---|---|
| DEFER-WL01 | concrete PostgreSQL schema/table/key strategy | Physical thesis closed; reusable details remain | CP6-02 + CP6-03/05 | exact global rules and vertical design only |
| DEFER-WL02 | TypeDB benchmark schema/query | CLOSED / historical | Physical Model | PostgreSQL selected; no reopen |
| DEFER-WL03 | Neo4j graph/read projection | CLOSED for initial target | capability-triggered explicit reopen only | no hidden graph dependency |
| DEFER-WL04 | owner-specific vs shared typed-relation physical structures | thesis partially closed | CP6-02 REL + vertical | specific relation semantics fixed; physical reusable pattern now |
| DEFER-WL05 | MaterialStateRef storage/index/version | OPEN concrete global | CP6-02 MAT/HIST/IDX | core constitution item |
| DEFER-WL06 | expected-state token/API mechanics | split | CP6-02 TX; API later | semantic expected state closed; physical enforcement now |
| DEFER-WL07 | idempotency store/lifetime/replay | OPEN concrete global | CP6-02 IDEM | operation-level technical contract |
| DEFER-WL08 | transaction/atomicity/staging boundaries | CP3 outer transaction closed; invariant mechanics open | CP6-02 TX + vertical | READ COMMITTED inherited; escalation invariant-specific |
| DEFER-WL09 | provider outbox/inbox/sync/reconciliation mechanics | canonical/provider separation CLOSED; PostgreSQL Class-A outbox selected; provider-specific inbox/sync/reconciliation shape remains open | integration/runtime vertical | do not imply every provider mechanism is already selected or materialized |
| DEFER-WL10 | LR-08 materialization/freshness | global noncanonical boundary closed | CP6-02 CAP/freshness + query vertical | exact caches/materializations query-driven |
| DEFER-WL11 | retention/redaction/tombstone physical representation | OPEN global doctrine + direct proof later | CP6-02 LIFE + recovery/release | HG-09/PSV-01 remain unpassed |
| DEFER-WL12 | AuthN Principal/session/device persistence | OPEN vertical/security | Access/security vertical | not Domain owner |
| DEFER-WL13 | AuthZ engine/vendor/policy language | later security/runtime | security stage | AuthZ != Authority/Consent |
| DEFER-WL14 | canonical→AuthZ projection/cache consistency | later security/runtime | security/system proof | WL-H11/12 carry-forward |
| DEFER-WL15 | disclosure/RLS/application/sidecar enforcement split | later security design; DB boundary doctrine in CP6 | CP6-02 + security vertical | RLS may be ingredient, not semantic authority |
| DEFER-WL16 | API routes/DTO/serialization | out of CP6 persistence | post-CP6 API | no table design by route convenience |
| DEFER-WL17 | bounded event-stream/outbox/audit use | Class-A PG outbox selected; exact use later | runtime/integration vertical | no universal event ontology |
| DEFER-WL18 | specialist document/telemetry stores | telemetry target/boundary selected; raw ContentArtifact bytes target selected; specialist persistence remains bounded and vertical-specific | specialist/runtime | do not imply a universal specialist store is selected |
| DEFER-WL19 | indexes/constraints/partition/performance | global doctrine open; exact structures workload-specific | CP6-02 CON/IDX + vertical | no blanket 57-owner predesign |
| DEFER-WL20 | migrations/rollout | CP3 Alembic governance closed; business evolution doctrine open | CP6-02 MIG + later V1→V2 proof | PSV-02 remains direct proof |

```text
DEFER-WL ASSIGNED      20 / 20
DEFERRED ITEM LOST           0
PHYSICAL REOPEN CREATED      0
```

---

## 8. HG-01..HG-12 carry-forward matrix

Result-layer invariant:

```text
STATIC PASS-CONDITIONAL != DIRECT PASS
HOLD != REJECT
CP3 TECHNICAL QA != SEMANTIC HG EXECUTION
```

| HG | Gate | PostgreSQL static disposition | Direct truth | Stage |
|---|---|---|---|---|
| HG-01 | semantic ownership | PASS-CONDITIONAL | semantic direct PASS not established | CP6-01/02 + representative post-CP6 corpus |
| HG-02 | reference-family integrity | PASS-CONDITIONAL | wrong-family/dangling proof required | CP6-02 REF + vertical |
| HG-03 | typed/n-ary relation fidelity | PASS-CONDITIONAL | representative direct proof required | CP6-02 REL + vertical |
| HG-04 | expected-state concurrency | PASS-CONDITIONAL | SC-001 direct race required | CP6-02 TX + business proof |
| HG-05 | multi-owner consistency | PASS-CONDITIONAL | SC-003/write-skew proof required | CP6-02 TX + vertical |
| HG-06 | history/correction/reconciliation | PASS-CONDITIONAL | representative SC-010/013/014 proof required | CP6-02 MAT/HIST + vertical |
| HG-07 | state-layer separation | PASS-CONDITIONAL | provider/projection/system proof later | CP6-02 boundary + vertical |
| HG-08 | governance/selective disclosure | PASS-CONDITIONAL | WL-H12/security proof later | CP6-02 + security vertical |
| HG-09 | retention/redaction/tombstone/restore | HOLD | destructive anti-resurrection not run | CP6-02 LIFE + recovery/release |
| HG-10 | temporal/recurrence/timezone | PASS-CONDITIONAL | SC-022..025/lazy Occurrence proof later | CP6-02 TIM + temporal vertical |
| HG-11 | schema/data evolution | HOLD | actual V1→V2 not run | CP6-02 MIG + post-vertical PSV-02 |
| HG-12 | recoverability/evidence quality | HOLD | destructive restore/recovery not run | release/recovery PSV-03/40 |

```text
POSTGRESQL STATIC
PASS-CONDITIONAL  9
HOLD              3
REJECT            0

EXECUTION HOLDS
HG-09
HG-11
HG-12
```

---

## 9. Canonical Physical Scenario Corpus stage ledger

The canonical scenario names below are copied from `docs/architecture/physical-benchmark-scenario-corpus.md`. CP6 ledgers do not rename them.

| SC | Canonical name | Stage | Direct status |
|---|---|---|---|
| SC-001 | Same-base consequential race | CP6-02 doctrine; direct business proof post-CP6 | NOT RUN / NOT PASS |
| SC-002 | Idempotency-key conflicting reuse | CP6-02 doctrine; direct retry/effect proof post-CP6 | NOT RUN / NOT PASS |
| SC-003 | Atomic multi-owner mutation | CP6-02 doctrine; direct invariant proof post-CP6 | NOT RUN / NOT PASS |
| SC-004 | Distributed/provider partial outcome | integration/provider/runtime | NOT RUN / NOT PASS |
| SC-005 | Provider effect may have occurred before timeout | integration/provider/runtime | NOT RUN / NOT PASS |
| SC-006 | Duplicate/out-of-order callback | integration/provider/runtime | NOT RUN / NOT PASS |
| SC-007 | Revoked governance during delayed execution | governed-effect/security/runtime | NOT RUN / NOT PASS |
| SC-008 | Stale LR-08 consequential basis | governed-effect/security/runtime | NOT RUN / NOT PASS |
| SC-009 | Web/mobile offline divergence | PowerSync/offline activation | NOT RUN / NOT PASS |
| SC-010 | Correction without false rewrite | CP6-02 doctrine; direct history proof post-CP6 | NOT RUN / NOT PASS |
| SC-011 | Redaction then restore older backup | CP6-02 LIFE/MIG; recovery destructive proof | NOT RUN / NOT PASS |
| SC-012 | Native identity non-reuse | CP6-02 doctrine; direct lifecycle proof post-CP6 | NOT RUN / NOT PASS |
| SC-013 | Deep-history current-state query | representative history/performance stage | NOT RUN / NOT PASS |
| SC-014 | Historical reconstruction | CP6-02 doctrine; direct history proof post-CP6 | NOT RUN / NOT PASS |
| SC-015 | Typed n-ary relation fidelity | CP6-02 doctrine; direct relation proof post-CP6 | NOT RUN / NOT PASS |
| SC-016 | Selective disclosure without source leakage | CP6-02 disclosure; security/system proof | NOT RUN / NOT PASS |
| SC-017 | Search hidden-result non-interference | CP6-02 disclosure; search/security proof | NOT RUN / NOT PASS |
| SC-018 | FTS mixed filter/query | search/FTS activation | NOT RUN / NOT PASS |
| SC-019 | Vector recall after security/scope filter | pgvector/search activation | NOT RUN / NOT PASS |
| SC-020 | Search/index stale source | search/projection activation | NOT RUN / NOT PASS |
| SC-021 | Search/index deletion propagation | search/projection activation | NOT RUN / NOT PASS |
| SC-022 | Recurrence across DST spring gap | CP6-02 TIM; recurrence vertical | NOT RUN / NOT PASS |
| SC-023 | Recurrence across DST fall fold | CP6-02 TIM; recurrence vertical | NOT RUN / NOT PASS |
| SC-024 | Individual recurrence override | CP6-02 TIM; recurrence vertical | NOT RUN / NOT PASS |
| SC-025 | Provider calendar sync-token invalidation/rebaseline | integration/provider | NOT RUN / NOT PASS |
| SC-026 | Solver candidate from stale snapshot | OR-Tools activation | NOT RUN / NOT PASS |
| SC-027 | Solver UNKNOWN vs INFEASIBLE | OR-Tools activation | NOT RUN / NOT PASS |
| SC-028 | Crash between canonical commit and external publication/effect | integration/runtime | NOT RUN / NOT PASS |
| SC-029 | Durable in-flight execution across version change | Restate/Class-B activation | NOT RUN / NOT PASS |
| SC-030 | Schema/mapping evolution with historical references | CP6-02 MIG; actual V1→V2 post-vertical | NOT RUN / NOT PASS |
| SC-031 | Backup/restore operational verification | recovery/release | NOT RUN / NOT PASS |
| SC-032 | Capacity/backpressure failure | capacity/runtime/release | NOT RUN / NOT PASS |
| SC-033 | Older client/effect contract version | governed-effect/API/runtime | NOT RUN / NOT PASS |
| SC-034 | Provider/derived/search state unavailable | provider/derived/system boundary | NOT RUN / NOT PASS |
| SC-035 | Graph projection divergence/rebuild | DORMANT capability-triggered only if separate graph projection is later accepted | NOT RUN / NOT PASS |

`SC-035` remains preserved but inactive because no separate graph server/projection is selected in the initial target.

---

## 10. Full Post-Selection Validation stage ledger

No PSV is PASS merely because the architecture is selected or CP3 materialized technical PostgreSQL infrastructure.

| PSV | Obligation | Stage | Current direct status |
|---|---|---|---|
| PSV-01 | SC-011 old-backup anti-resurrection | CP6-02 LIFE + recovery destructive proof | NOT DIRECTLY PASSED |
| PSV-02 | SC-030 actual DANTE V1→V2 mapping/schema evolution | CP6-02 MIG + actual post-vertical evolution | NOT DIRECTLY PASSED |
| PSV-03 | SC-031 destructive restore + semantic verification | recovery/release | NOT DIRECTLY PASSED |
| PSV-04 | SC-032 capacity/backpressure truthful degradation | capacity/runtime/release | NOT DIRECTLY PASSED |
| PSV-05 | WL-H12 system-level non-interference | CP6-02 doctrine + security/system proof | NOT DIRECTLY PASSED |
| PSV-06 | SC-017 search hidden-result non-interference | search/security activation | NOT DIRECTLY PASSED |
| PSV-07 | SC-018 FTS mixed filter/query correctness under applicable Visibility/user/scope filtering | FTS/search activation | NOT DIRECTLY PASSED |
| PSV-08 | SC-019 vector recall/relevance after real Visibility/user/scope filtering | pgvector/search activation | NOT DIRECTLY PASSED |
| PSV-09 | SC-020 projection freshness/material-basis behavior | projection/search activation | NOT DIRECTLY PASSED |
| PSV-10 | SC-021 deletion/redaction propagation | projection/search activation | NOT DIRECTLY PASSED |
| PSV-11 | two-device divergence from common material base | PowerSync/offline | NOT DIRECTLY PASSED |
| PSV-12 | offline mutation after remote canonical change | PowerSync/offline | NOT DIRECTLY PASSED |
| PSV-13 | Authority/Consent/Visibility change while client offline | PowerSync/security | NOT DIRECTLY PASSED |
| PSV-14 | local encrypted-database validation and key-storage posture | mobile/offline | NOT DIRECTLY PASSED |
| PSV-15 | device deletion/redaction purge/invalidation | PowerSync/mobile | NOT DIRECTLY PASSED |
| PSV-16 | PowerSync source half-open/stalled replication scenario | PowerSync | NOT DIRECTLY PASSED |
| PSV-17 | independent replication/checkpoint-lag monitoring | PowerSync | NOT DIRECTLY PASSED |
| PSV-18 | controlled restart/reconnect + client reconciliation | PowerSync | NOT DIRECTLY PASSED |
| PSV-19 | broad publication regression: approved sync projections only | PowerSync | NOT DIRECTLY PASSED |
| PSV-20 | consequential LWW rejection | PowerSync/offline | NOT DIRECTLY PASSED |
| PSV-21 | crash between canonical commit and external side effect | async/runtime | NOT DIRECTLY PASSED |
| PSV-22 | provider applied effect but response lost/ambiguous | integration/runtime | NOT DIRECTLY PASSED |
| PSV-23 | human wait followed by target/governance change | Restate/Class-B | NOT DIRECTLY PASSED |
| PSV-24 | duplicate/replay idempotency | CP6-02 IDEM + real retry/runtime/vertical proof | NOT DIRECTLY PASSED |
| PSV-25 | cancellation/timeout truthfulness | runtime/integration | NOT DIRECTLY PASSED |
| PSV-26 | in-flight workflow version/deployment evolution | Restate/Class-B | NOT DIRECTLY PASSED |
| PSV-27 | runtime-journal privacy minimization | Restate/Class-B | NOT DIRECTLY PASSED |
| PSV-28 | recovery/reconciliation after runtime outage | Restate/Class-B | NOT DIRECTLY PASSED |
| PSV-28A | deployment-mode review: self-hosted vs Cloud EU privacy/operability/cost posture | Restate activation | NOT DIRECTLY PASSED |
| PSV-28B | Python path must not assume TypeScript-only client-side journal encryption | Restate Python activation | NOT DIRECTLY PASSED |
| PSV-29 | ContentArtifact metadata commit vs object upload partial failure | R2/ContentArtifact activation | NOT DIRECTLY PASSED |
| PSV-30 | R2 deletion/redaction propagation | R2 activation | NOT DIRECTLY PASSED |
| PSV-31 | R2 primary object loss → S3 object restore | object recovery | NOT DIRECTLY PASSED |
| PSV-32 | DB restore + object backup reconciliation | recovery | NOT DIRECTLY PASSED |
| PSV-33 | no unauthorized public/private-cache exposure | object/security | NOT DIRECTLY PASSED |
| PSV-34 | backup access/audit and finite retention controls | production recovery | NOT DIRECTLY PASSED |
| PSV-35 | PostgreSQL selected mapping end-to-end smoke corpus | first real representative business mapping after CP6 | NOT DIRECTLY PASSED |
| PSV-36 | PostGIS query/index correctness for accepted geo cases | geo activation | NOT DIRECTLY PASSED |
| PSV-37 | pgvector model/source/freshness provenance | vector/retrieval activation | NOT DIRECTLY PASSED |
| PSV-38 | PgBouncer pool-mode compatibility by connection class | PgBouncer activation | NOT DIRECTLY PASSED |
| PSV-39 | PowerSync logical replication bypasses incompatible transaction pooling | PowerSync + PgBouncer activation | NOT DIRECTLY PASSED |
| PSV-40 | pgBackRest archive/restore/PITR rehearsal | recovery/production | NOT DIRECTLY PASSED |
| PSV-41 | deterministic OR-Tools corpus | solver activation | NOT DIRECTLY PASSED |
| PSV-42 | UNKNOWN != INFEASIBLE behavior | solver activation | NOT DIRECTLY PASSED |
| PSV-43 | candidate result cannot bypass Decision/governance | solver activation | NOT DIRECTLY PASSED |
| PSV-44 | timeout/capacity degradation | solver/runtime | NOT DIRECTLY PASSED |
| PSV-45 | no sensitive payload logging by default | implementation/release observability | NOT DIRECTLY PASSED |
| PSV-46 | required backlog/lag/failure signals observable | activated runtime/release | NOT DIRECTLY PASSED |
| PSV-47 | telemetry outage does not mutate semantic truth | observability/release | NOT DIRECTLY PASSED |

```text
PSV-01..PSV-47   PRESENT
PSV-28A          PRESENT
PSV-28B          PRESENT
PSV ID LOST      0
FALSE PSV PASS   0
```

### PSV-35 boundary

`PSV-35` cannot be satisfied by inventing generic business tables in CP6 merely to create a green smoke test.

```text
CP6
foundation rules + Vertical #1 exact design
+ direct proof only for real existing foundation subjects

POST-CP6 VERTICAL #1 IMPLEMENTATION
first representative business mapping
→ genuine PSV-35 evidence becomes possible
```

---

## 11. CP3 direct-evidence reconciliation

CP3 directly established technical substrate including:

```text
PostgreSQL 18.4 real acceptance container
schema dante
SQLAlchemy 2 async
psycopg 3
Alembic
single migration DAG
fresh DB → repository head
single Alembic head
alembic check / no DANTE drift
owner / migrator / runtime separation
runtime DDL/privilege denial
transaction commit
whole-transaction rollback
flush != commit
SAVEPOINT behavior
pool_pre_ping recovery
DB outage readiness behavior
```

CP3 also freezes:

```text
default isolation = READ COMMITTED
stronger locking/isolation = concrete-invariant decision
no hidden transaction retry
outer application operation owns commit/rollback
adapter may flush; adapter does not implicitly commit
```

CP3 does **not** directly prove business semantics such as:

```text
heterogeneous Reference Contract eligibility
a real MaterialState current-binding pattern
SC-001 business race
SC-003 multi-owner invariant race
SC-010 correction lineage
SC-015 n-ary Agreement/governance fidelity
SC-017 search non-interference
SC-018 FTS mixed filter/query
SC-022..024 recurrence semantics
SC-030 actual business V1→V2
SC-011/031 anti-resurrection/recovery
WL-H12 business-surface non-interference
```

---

## 12. Canonical / provider / derived / security / recovery ownership recheck

| State class | Physical authority/mechanism | Canonical? | CP6-01 rule |
|---|---|---:|---|
| accepted DANTE current truth | PostgreSQL | YES | owner-specific |
| material history | PostgreSQL | YES | explicit material-state/history |
| semantic relations | PostgreSQL | YES | specific typed relations |
| provider/external state | integration structures | NO | LR-09 separate |
| lexical/vector/query projection | PostgreSQL query/index capabilities | NO | LR-08 / rebuildable |
| local/offline copy | SQLite/PowerSync when activated | NO | downstream only |
| bounded Class-A async | PG outbox/worker when real need exists | NO | runtime only |
| durable Class-B runtime | Restate when activated | NO | runtime only |
| raw object bytes | R2 when activated | bytes only | ContentArtifact authority remains PostgreSQL |
| recovery copies | pgBackRest/S3 when activated | NO | recovery only |
| solver output | OR-Tools | NO | candidate only |
| telemetry | OTel/Alloy/Grafana/pg_stat_statements | NO | operational only |
| Principal/AuthZ runtime | security system | NO Domain governance identity | technical context/evidence only |

Canonical persistence authorities remain exactly **1 — PostgreSQL**.

---

## 13. PostgreSQL capability pressure

### PostGIS

Selected capability, not universal default. Exact geometry/geography/index design waits for an accepted geo use case. `PSV-36` remains direct proof.

### Native FTS / pg_trgm / unaccent

Derived/query capability only. Exact indexed document/ranking/query design follows real query needs and `WL-H12`. `SC-018`/`PSV-07` are the canonical FTS correctness carry-forward.

### pgvector

Derived retrieval only. Model/source/freshness/security-filter provenance remains explicit. `PSV-37` waits for a real retrieval path.

### JSONB

Allowed only for bounded cases such as:

```text
LR-10 flexible low-consequence metadata
provider/raw payload
specialist extension detail
bounded technical computation/provenance metadata
```

Required semantics remain explicit.

```text
DOMAIN CONCEPT REQUIRING JSONB AS CANONICAL SEMANTIC ESCAPE HATCH
0
```

### PgBouncer / PowerSync / Restate / outbox / recovery

Selected target capabilities do not generate speculative CP6-01 tables. Their materialization and direct proof remain real-trigger-bound.

---

## 14. Gate-01 preflight after hardening

```text
57 / 57 Domain concepts accounted                      CANDIDATE PASS
15 / 15 LR-01 native owners                            CANDIDATE PASS
LR-01..LR-13 representation roles                      CANDIDATE PASS
cross-cutting/non-owner contracts                      CANDIDATE PASS
ReferenceAddress family separation                     CANDIDATE PASS
material/history/chronology pressure                    CANDIDATE PASS
canonical/provider/derived/security boundaries          CANDIDATE PASS
dependency pressure                                    CANDIDATE PASS
WL-H01..WL-H12 applicability                           CANDIDATE PASS
PG-R01..PG-R10 applicability/stage                     CANDIDATE PASS
DEFER-WL01..20 disposition                             CANDIDATE PASS
HG-01..HG-12 carry-forward                             CANDIDATE PASS
SC-001..SC-035 exact canonical names/stages            CANDIDATE PASS
PSV-01..47 + PSV-28A/B stage ownership                 CANDIDATE PASS
SC-017/SC-018 traceability                              REPAIRED / FINAL RECHECK REQUIRED
CP3 technical-vs-semantic evidence distinction          CANDIDATE PASS

semantic owner reclassification                         0
additional Domain owner                                  0
generic semantic fallback                               0
generic Rule/Fact/Version root                           0
unexplained canonical JSONB fallback                    0
unclassified persistence family                         0
unexecuted HG/SC/PSV relabeled PASS                     0
speculative business table                               0
business migration                                       0
business SQLAlchemy mapping                              0
persistence adapter                                      0
Physical Model redesign/reopen                           0
```

---

## 15. Mandatory final independent control

Gate 01 may become PASS only after a fresh post-write/readback control checks:

```text
A  Domain final closure / no new owner
B  Whole-Logical exact 57/57 census
C  exact 15 LR-01 native set
D  latest Slice/Representation hardenings
E  WL-H01..12
F  LR-01..LR-13
G  DEFER-WL01..20
H  Governed Operation / Effect Contract
I  ReferenceAddress + Reference Contract
J  accepted PostgreSQL mapping
K  PG-R01..10
L  HG-01..12
M  canonical SC-001..SC-035 names/assertions
N  PM-11/12/13/14 selected/accepted truth
O  full PSV register and exact SC bindings
P  CP3 actual technical evidence
Q  CP6 durable handoff
R  CP6-01 Part 1 + this Part 2
S  exact Git PRE-SCOPE → HEAD delta
```

Specific failure questions:

```text
Does any CP6 text create a Domain owner not in the 57?
Does any non-owner construct silently become semantic identity?
Does any cross-cutting contract disappear behind the 57 rows?
Does any CLOSED Physical decision get reopened?
Does any SC identifier have more than one active meaning?
Does any unexecuted HG/SC/PSV become PASS?
Does any selected capability become required before a real trigger?
Does technical evidence get overstated as business-semantic evidence?
Does PostgreSQL convenience weaken a Logical invariant?
Does any business DDL/table/column/index leak into CP6-01?
```

Any unsafe answer means:

```text
GATE 01
HOLD
```

Only a clean final control may authorize a separate closure record stating:

```text
CP6-01
GATE 01 PASS
```

---

## 16. Resume point

```text
POST-WRITE REMOTE READBACK
        ↓
FINAL INDEPENDENT CONTROL A→S
        ↓
if defect → bounded repair
        ↓
if clean → Gate 01 closure write gate
        ↓
only after Gate 01 closure
CP6-02 PostgreSQL Persistence Constitution
```

No business DDL, business migration, SQLAlchemy business mapping, persistence adapter, application use case or business API is authorized by this continuation.
