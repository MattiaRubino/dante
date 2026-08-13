# Observation v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted current baseline  
**Date:** 2026-08-11  
**Concept:** Observation v0  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Scope

This checkpoint validates whether LifeOS requires a distinct `Observation` concept and whether that concept can remain bounded enough to avoid becoming a universal data/fact primitive.

Primary adjacent concepts:

- Actual;
- Outcome;
- Session;
- Event;
- future Evidence;
- future Confirmation;
- future Provenance;
- future Quantity;
- future Register/RegisterEntry;
- future Subject/Actor/Resource semantics.

Primary risks:

1. turning Observation into generic `data + JSON`;
2. conflating the contextual record with its Quantity/value;
3. making RegisterEntry and Observation duplicate universal records;
4. confusing observed facts with Evidence, Outcome, or confirmed truth;
5. losing effective-time/source/perspective distinctions;
6. silently reconciling conflicting actors/providers;
7. forcing one SQL row per high-frequency sensor tick.

---

# 2. Evidence reviewed

## Internal

Reviewed:

- Actual v0 + validation;
- Outcome v0 + validation;
- Activity/Event/Session accepted specs;
- feature-discovery simulation, especially Register/Quantity, sport, mood/sleep/symptoms, caregiver, assets/maintenance, investing, learning and agriculture scenarios;
- V1 data-history/privacy principles;
- Multi-Actor Readiness v1 and collaboration research;
- current Language Map;
- Methodology v3.

Key inherited requirements:

```text
observed reality may exist without prior intention
source != truth
planned != actual
passage of time != completion
private source != shareable consequence
subject != actor/account by default
history/corrections must remain explainable
```

## External benchmark

| Source/pattern | Finding | Classification |
|---|---|---|
| HL7 FHIR Observation R5 | Observation is explicitly bounded to measurements/simple assertions about a subject; separates effective time, issued time, performer, value, method, device and derived-from relationships | ADAPT |
| FHIR Observation guidance | independent observations/derived observations can retain separate identity and provenance; observation is not the universal resource for every clinical fact | BORROW/ADAPT |
| Android Health Connect Record + Metadata | data records have stable IDs, effective times plus origin/device/recording metadata and client versions; record identity is not timestamp identity | ADAPT |
| Apple HealthKit HKSample/HKQuantitySample/HKQuantity | sample record is distinct from Quantity value/unit semantics | BORROW/ADAPT |
| OpenTelemetry Logs data model | event timestamp and observed/collection timestamp are distinct | BORROW semantic time distinction |

External systems remain evidence rather than target schemas.

---

# 3. Accepted candidate definition

> **An Observation is a persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a subject at an effective time or context. It preserves what was observed or asserted without by itself establishing universal truth, authority, confirmation, Outcome, or evidentiary relevance.**

Domain question:

> **What was observed, reported, measured, or calculated about this subject, and to what time/context does that statement apply?**

Identity:

- stable identity for one observation/assertion instance;
- not a hash of subject/property/time/value;
- provider/client IDs may assist mapping but do not define LifeOS identity.

Independent existence:

- may exist without Actual, Outcome, Goal, Session, or Register;
- requires enough subject/property/context semantics to be intelligible.

Nearest boundaries:

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != Register
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| CORE-01 Workflow inversion | yes | manual weight/mood logging, imported score/odometer/sensor readings | PASS | observed facts map naturally without prior planning objects |
| CORE-02 Deep chronology | yes | observe → late import → correction → derived aggregate → historical query | PASS WITH HARDENING | effective time, ingest time, correction history remain distinct |
| CORE-03 Reductio | yes | REMOVE / MERGE / UNIVERSALIZE / INVERT / EXTREME | PASS WITH HARDENING | concept survives; universal fact/blob version rejected |
| CORE-04 Redundancy | yes | Observation vs Actual/Outcome/Quantity/Register/Evidence | PASS WITH DEFERRED RETEST | boundaries materially distinct; Quantity/Register re-test mandatory in next cluster |
| CORE-05 Traceability | yes | Observation → Evidence/Goal; Observation linked to Actual/Session/Asset | PASS | later relevance does not rewrite original observation context |
| CORE-06 Orphan/independence | yes | spontaneous weight/mood/weather/odometer observations | PASS | no planning/Actual wrapper required |
| CORE-07 External benchmark | yes | FHIR, Health Connect, HealthKit, OTel | PASS | mature systems support record/value/source/time separation |
| CORE-08 Anti-pattern review | yes | generic telemetry/fact table; JSON blob; one row per tick | PASS WITH HARDENING | explicitly prohibited as semantic invariant |
| CORE-09 Correction/reconciliation/epistemic integrity | yes | typo correction vs remeasurement; conflicting devices/actors | PASS WITH HARDENING | correction preserves identity; re-observation is new; conflicts remain distinct assertions |
| CORE-10 Scale/performance/history | yes | years of logs + high-frequency sensors | PASS WITH HARDENING | Observation semantics do not require row-per-sample persistence |
| CORE-11 Simple vs power user | yes | `Registra un dato` vs source/history detail | PASS | ontology can remain hidden/contextual |
| CORE-12 Product value/complexity cost | yes | shared record semantics across health/learning/assets/mood | PASS | reuse value is high without forcing specialist schemas into core |
| CORE-13 Implementation pressure | yes | typed values, sampled streams, derived aggregates | PASS WITH HARDENING | final value/series physical form deferred; no arbitrary JSON requirement |

## Core hardenings

1. Observation is bounded to measurement/simple-assertion semantics, not all domain facts.
2. Stable identity is independent from current field values and timestamps.
3. Effective time/context remains distinct from recorded/ingested/source-issued time.
4. Correction of one observational act differs from a new measurement.
5. Quantity is reusable value/unit semantics, not the observation record.
6. Register is longitudinal organization/analysis, not universal Observation identity.
7. Missing Observation, explicit negative Observation, and failed/unavailable measurement differ.
8. Subjective reports remain valid observations without becoming universal objective truth.
9. Derived/aggregate observations require traceability; query aggregates need not be persisted.
10. High-frequency sensor storage does not imply one relational Observation row per tick.

---

# 5. Reductio detail

## REMOVE

Without Observation, simple measured/asserted reality must be scattered across Actual, Outcome, Goal, Asset, Register, and specialist modules.

**Result:** REMOVE fails.

## MERGE WITH ACTUAL

Counterexample:

```text
weight = 66.4 kg
```

has no prior expectation to reconcile.

**Result:** MERGE fails.

## MERGE WITH OUTCOME

Counterexample:

```text
exam score = 78/100
Outcome = passed
```

fact and result remain distinct.

**Result:** MERGE fails.

## MERGE WITH QUANTITY

`66.4 kg` has value/unit semantics but no observation identity, subject, effective context, source perspective, or correction history.

Quantity is also reused outside observation.

**Result:** MERGE fails.

## MERGE WITH REGISTER

A Register organizes records longitudinally. An Observation may exist outside a Register; a Register may organize transactions/movements/specialist entries that are not Observations.

**Result:** MERGE fails provisionally; mandatory re-test in Data/Subjects cluster.

## MERGE WITH EVIDENCE

An Observation need never be used for evaluation.

**Result:** MERGE fails.

## MAKE UNIVERSAL

Flattening transactions, documents, Activities, Events, relationships, and Decisions into Observation loses richer semantics.

**Result:** UNIVERSALIZE fails.

## INVERT

Assuming no Observation means false/zero/absent destroys epistemic integrity.

**Result:** INVERT fails.

## EXTREME

High-frequency telemetry shows why logical observation semantics must be independent from row-per-sample physical storage.

**Result:** bounded model survives.

---

# 6. Multi-Actor Compatibility Gate

| Test ID | Applicable | Evidence/scenario | Result | Finding / hardening |
|---|---:|---|---|---|
| MA-01 Identity/account independence | yes | external caregiver/device/provider | PASS | Observation does not depend on LifeOS account identity |
| MA-02 Shared fact/actor overlay | yes | shared context + private observations | PASS WITH HARDENING | related shared object does not force observation visibility/sharedness |
| MA-03 Responsibility/assignment/claim | limited | caregiver/technician records observation | PASS | responsibility for task is separate from observer/recorder |
| MA-04 Stewardship/mental load | limited | caregiver repeatedly monitors readings | PASS | burden may exist but is not Observation identity |
| MA-05 Common ground/state separation | yes | one actor reports a value, another disputes it | PASS WITH HARDENING | reported != acknowledged/confirmed/canonical truth |
| MA-06 Authority/canonical change | yes | manager vs worker report; clinician vs user report | PASS WITH HARDENING | observation source does not automatically establish universal authority |
| MA-07 Selective disclosure | yes | private health/mood observation | PASS | derived projection may be shared without raw observation |
| MA-08 Inference privacy | yes | AI derives schedule/capacity from private observation | PASS | inference/explanation cannot leak private cause |
| MA-09 Partial adoption/external participant | yes | non-LifeOS subject/observer/provider | PASS | external actors/sources remain representable |
| MA-10 Assisted participation/provenance | yes | caregiver records older adult temperature | PASS WITH HARDENING | subject/observer/recorder/device/source remain separable |
| MA-11 Relationship lifecycle/revocation | yes | former caregiver loses access | PASS | historical attribution may remain while current access changes |
| MA-12 Conflict/adversarial relationship | yes | conflicting subjective reports or sensors | PASS WITH HARDENING | preserve separate observations; no silent averaging/overwrite |
| MA-13 Unequal power | yes | manager rating worker; caregiver/clinician contexts | PASS WITH HARDENING | power/role does not turn perspective into universal fact automatically |
| MA-14 Multi-resource/capacity | limited | device/asset observations | PASS | resource context does not redefine Observation identity |
| MA-15 Coordination-burden distribution | limited | repeated confirmation prompts | PASS | low-value observations should not impose universal confirmation burden |
| MA-16 Formality/progressive disclosure | yes | casual mood log vs regulated measurement | PASS | same core semantics can expose different metadata depth |
| MA-17 AI authority/multi-party context | yes | AI-generated anomaly/inference | PASS WITH HARDENING | AI inference is proposal/candidate unless policy establishes otherwise |
| MA-18 Specialist-system boundary | yes | clinical/financial/sensor authoritative sources | PASS | LifeOS can preserve imported observations without replacing specialist authority |
| MA-19 Multi-actor primitive redundancy | yes | subject/observer/source roles | PASS | no separate SharedObservation/UserObservation primitive justified |
| MA-20 Actor-scoped reality attribution | yes | two observers report different values | PASS WITH HARDENING | distinct perspective/source observations may coexist around one context |

## Multi-actor hardenings

1. `subject != observer != recorder != source != authority != viewer`.
2. Shared domain context does not imply shared Observation visibility.
3. Conflicting perspectives remain distinct observations until contextual reconciliation.
4. Manager/creator/device/provider status does not automatically establish universal truth.
5. Assisted capture preserves whose subject and whose assertion are represented.
6. AI computation over private observations does not create disclosure permission.

---

# 7. Cross-Concept Consistency Gate

| Test ID | Applicable | Result | Notes |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS | does not redefine Actual/Outcome/Session/Event identity |
| XCON-02 Ownership/authority compatibility | yes | PASS | authority remains separate/deferred |
| XCON-03 Planned/current/actual/history compatibility | yes | PASS | observation can arise bottom-up and preserve effective/correction history |
| XCON-04 Relationship compatibility | yes | PASS | context/derived-from/evidence links remain future typed relationships |
| XCON-05 Multi-actor readiness compatibility | yes | PASS | subject/source/perspective remain independent |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE | Observation promoted from DEFERRED to CANONICAL after acceptance |

---

# 8. Hardest scenario log

| Scenario | Stress | Result | Model change |
|---|---|---|---|
| 08:00 measurement entered at 18:00 | temporal semantics | PASS after hardening | effective != recorded time |
| 76.4 typo corrected to 66.4 | correction identity | PASS | same Observation + correction history |
| new measurement ten minutes later | identity boundary | PASS | new Observation |
| no symptom entry vs explicit `false` | unknown/negative | PASS after hardening | missing != observed-negative |
| sensor failed | data absence | PASS | distinct from negative/missing observation |
| two sensors disagree | source conflict | PASS after hardening | preserve both assertions |
| two people rate same meeting differently | subjective multi-actor reality | PASS after hardening | perspective-specific observations coexist |
| caregiver records another person's temperature | assisted provenance | PASS after hardening | subject/observer/recorder separate |
| BMI derived from height/weight | derivation | PASS | source facts preserved/traceable |
| daily average queried from raw history | derived persistence | PASS | query aggregate not automatically persisted |
| 1 Hz sensor stream for years | scale pressure | PASS after hardening | physical series representation allowed |
| one weight record visible in dashboard + Goal + Register | duplication pressure | PASS | one source Observation, multiple projections/uses |

---

# 9. Reopening / dependency register

| Finding | Severity | Current treatment | Reopening trigger |
|---|---|---|---|
| Observation vs Quantity exact value model | DEFERRED DEPENDENCY | semantic boundary accepted | Quantity review |
| Observation vs Register/RegisterEntry physical/logical boundary | DEFERRED DEPENDENCY | register organizes/references records, not universal observation | Register review |
| Subject/observer/recorder typing | DEFERRED DEPENDENCY | semantic non-collapse fixed | Data/Subjects + Relationships review |
| epistemic/confirmation states | DEFERRED DEPENDENCY | source assertion != confirmed truth | Confirmation review |
| source/correction/derived-from history | DEFERRED DEPENDENCY | provenance requirement fixed | Provenance/Version review |
| high-volume sampled-series persistence | DEFERRED DEPENDENCY | no row-per-tick semantic invariant | logical/physical model |
| generic fact/blob creep | STRUCTURAL | explicitly prohibited | any proposal making Observation universal domain row |
| AI-derived observation authority | HARDENING | inference remains proposal/candidate unless policy allows | AI/Confirmation review |

---

# 10. Concept verdict

**PASS WITH HARDENING**

Observation survives removal, merge, universalization, chronology, correction, scale, multi-actor, privacy, authority, subjective-report and implementation-pressure tests.

The hardenings are incorporated in `concepts/observation.md`.

No structural reopening of Actual, Outcome, Intention/Execution, or Time is required.

Mandatory future re-tests:

- Observation vs Quantity;
- Observation vs Register/RegisterEntry;
- Observation vs Evidence;
- Observation vs Confirmation/Provenance;
- Subject/observer/recorder/source semantics;
- high-volume persistence pressure;
- Reality/Evidence cluster checkpoint;
- final whole-domain multi-actor gate.

---

# 11. Regression corpus additions

| Scenario | Boundary | Reuse trigger |
|---|---|---|
| measurement effective at 08:00, entered at 18:00 | effective != recorded time | Observation/Provenance/import models |
| typo correction vs new remeasurement | correction identity | Version/Provenance models |
| missing value vs explicit negative vs sensor failure | epistemic/data-absence integrity | Confirmation/specialist models |
| conflicting sensors | assertion conflict | Provenance/reconciliation models |
| two actors report different subjective values | perspective-specific reality | multi-actor/evaluation models |
| caregiver records another person's observation | subject != observer != recorder | Subject/Actor/Provenance models |
| high-frequency sensor stream | semantic vs physical representation | logical/physical model |
| one observation used by multiple Register/Goal/UI projections | source object != projection duplication | Register/Evidence/query models |

---

# 12. Documentation propagation

Acceptance pass scope:

- concept specification created;
- validation checkpoint created;
- Language Map promotes Observation to CANONICAL;
- Domain Atlas README records Observation acceptance and next review;
- workstream handoff records Observation acceptance and next review;
- Quantity/Register/Confirmation/Provenance reopening triggers remain explicit;
- no persistence schema is fixed.

---

# 13. Downstream closure — Version / material-equivalence v0 (2026-08-13)

Version v0 resolves the checkpoint's historical `source / correction / derived-from history` Version dependency without changing the original Observation validation result.

Current closure:

```text
Observation identity
!= material state of that Observation
!= provider/storage revision
```

A typo correction may preserve one Observation identity while changing its material state. A remeasurement remains a separate Observation identity. Historical Confirmations, Evidence evaluations, Decisions and derivations remain bound to the material state actually used and are not silently rewritten by later correction.

Distinct conflicting observations from different sensors/actors/providers remain separate assertion identities rather than Versions of one record solely because Subject/property/time overlap. Reconciliation owns duplicate/conflict resolution; Version owns only state reference/history within a given identity.

Material equivalence is purpose/facet scoped. Technical client versions, hashes, ETags and storage revisions may assist concurrency or lineage but do not define semantic materiality automatically. Historical reconstruction also does not require indefinite retention of all sensitive source payloads.

Downstream classification:

```text
Observation ↔ Version/correction persistence   RESOLVED
Version ↔ observation identity                 RESOLVED — distinct
```

Detailed reconciliation/source precedence, typed values/series, retention and physical persistence remain independently owned.

No original Observation hardening failed. **Observation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.