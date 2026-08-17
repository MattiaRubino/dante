# LifeOS Logical Model — Slice D: Evidence / Knowledge / History v1

**Status:** accepted candidate baseline pending exact remote QA  
**Date:** 2026-08-17  
**Slice:** D — Evidence / Knowledge / History  
**Authority:** accepted Domain Atlas > Product North Star > ADR-007 > Domain→Logical readiness contract > Logical Model methodology > active Slice A+B+C contract > current external evidence

---

## 1. Purpose

Slice D defines the logical representation contract for observed/asserted information, material state, lineage, attestation, evidentiary use, evaluation, reconciliation, historical reconstruction and durable cross-domain knowledge without inventing a universal `Fact`, `Claim`, `Assertion`, `Knowledge`, `Version` or event-log root.

It covers:

- Observation;
- Actual/Outcome history interaction;
- Version / Material-State;
- Provenance;
- Evidence;
- Confirmation;
- Acknowledgement;
- Criterion / Evaluation / Verification profile;
- Reconciliation / Source Precedence;
- current/historical knowledge projections;
- effective/world time versus learned/recorded/accepted chronology;
- temporal applicability of persistent, temporary, resolved, intermittent and unknown-ended information;
- provider/AI/import lineage;
- privacy/retention pressure;
- Slice-A ReferenceAddress and Slice-C historical-state obligations.

It does **not** choose SQL tables, temporal-table syntax, event sourcing, bitemporal storage, snapshot technology, search/vector infrastructure, API payloads, specialist clinical schemas, retention schedules or AuthN/AuthZ enforcement.

---

## 2. Selected logical direction

Selected representation strategy:

```text
LAYERED TYPED EPISTEMIC & HISTORY MODEL
```

This is a logical strategy, not a Domain superclass.

Canonical separation:

```text
SEMANTIC OWNER / SOURCE RECORD
!= MATERIAL STATE
!= PROVENANCE
!= ATTESTATION
!= EVIDENCE USE
!= EVALUATION
!= RECONCILIATION
!= CURRENT KNOWLEDGE PROJECTION
```

No universal canonical `Fact(subject,predicate,value)` root is accepted.

---

## 3. Observation disposition

Observation is a persistent independently meaningful observational/assertional act and therefore:

```text
Observation -> LR-01 native identity-bearing logical record
Observation -> NativeRef
```

Correction of the same observational act normally preserves Observation identity while producing another material state. A genuine re-observation normally produces another Observation identity.

```text
Observation O17 state S1 = 66.4 kg
correction
Observation O17 state S2 = 65.8 kg

O17 identity preserved
S1 != S2
```

Observation identity is not derived universally from subject + property + value + time.

High-frequency raw telemetry does not require one canonical Observation record per sensor tick. Specialist/source-native series, compressed segments, aggregates or selected Observations remain valid.

---

## 4. MaterialStateRef contract

`MaterialStateRef` is promoted from a placeholder reference category to a precise logical contract.

Conceptual meaning:

```text
MaterialStateRef
= stable reference to a materially relevant state
  of a stable semantic target
  for an applicable facet/purpose contract
```

A MaterialStateRef MUST NOT be equated automatically with:

```text
version_number
updated_at
ETag
MVCC token
provider revision
sync token
content hash
database row version
```

Required invariants:

1. target identity and material-state identity remain distinct;
2. once referenced, the MaterialStateRef does not silently retarget a later state;
3. no universal global linear sequence is required;
4. divergent/non-linear states are representable;
5. materiality is purpose/facet/consequence sensitive;
6. the physical realization may be snapshot, owner-specific revision, reconstructible state, immutable record or another later-proven mechanism;
7. a physical mechanism is acceptable only if historical semantic bindings remain lossless;
8. retention/redaction may remove sensitive payload while preserving an honest bounded historical reference/tombstone where required;
9. MaterialStateRef never creates a universal Version entity/root.

Conceptually:

```text
ReferenceAddress(target)
+
material-state anchor
+
Reference Contract / facet-purpose eligibility
```

The exact physical identifier is stage-deferred.

---

## 5. World/effective time and knowledge chronology

Slice D requires the logical model to preserve distinct temporal questions where material:

```text
WORLD / EFFECTIVE TIME
when the represented state/fact applies in the world

RECORDED / LEARNED TIME
when LifeOS received or recorded the information

ACCEPTED / CURRENT-INTERPRETATION CHRONOLOGY
when a state/interpretation became the current accepted one for its bounded context

CORRECTED / SUPERSEDED CHRONOLOGY
when that interpretation ceased to be current or was corrected
```

This is a semantic query contract, **not** a mandate to place four timestamp columns on every table or to adopt universal bitemporal storage.

The model must distinguish queries such as:

```text
What do we currently believe/apply about world time T?
What did LifeOS know at knowledge time K about T?
What interpretation was current at K?
When and why was that interpretation corrected?
```

---

## 6. Temporal applicability / durable versus temporary knowledge

A durable record existing in history does not imply that its represented state remains applicable now.

Canonical distinctions include, where the semantic owner supports them:

```text
ongoing / currently applicable
bounded episode
resolved / inactive / no-longer-applicable
end unknown
recurrent / intermittent
historical-only
```

These are **not** a universal status enum. The owning semantic family defines the valid lifecycle/status vocabulary; Slice D supplies the cross-cutting requirement that current knowledge/retrieval preserve effective applicability and historical state.

Examples of pressure:

```text
celiac condition / intolerance assertion
may be ongoing according to accepted source/state

broken-leg injury episode
has onset and later healing/resolution
history remains after current applicability ends

fever
may be a point Observation or a bounded symptom/condition episode;
a past fever is not automatically a current fact
```

Critical invariants:

```text
historical record exists
!= currently applicable

no known end
!= universally permanent

resolved
!= history deleted

old temporary state
!= retrieval should treat as current
```

Current knowledge projections MUST be able to filter/qualify by applicability rather than merely by latest storage timestamp.

---

## 7. Provenance

Disposition:

```text
Provenance -> LR-07 version/correction/lineage semantics
+ typed qualified lineage relations/segments where needed
```

Provenance explains how a target/material state came to exist or change. It does not establish truth, Authority, Evidence relevance, Confirmation or current-state precedence.

A material lineage segment may preserve, where needed:

```text
target MaterialStateRef
source ReferenceAddress / MaterialStateRef / ExternalRef
lineage role: created/imported/derived/transformed/normalized/corrected/merged/etc.
process / rule / model descriptor
Actor roles: source/observer/recorder/transformer/corrector/etc.
relevant times
```

No global PROV ontology/root is required. Provenance depth is bounded by material consequence.

AI/import pipelines must not launder source/authorship:

```text
PDF -> OCR -> AI extraction -> candidate -> user correction -> accepted state
```

must remain distinguishable from direct user authorship.

---

## 8. Evidence

Disposition:

```text
Evidence -> LR-03 typed contextual evaluative-use relation
```

Evidence links existing source information/material state to an evaluation context without duplicating source payload.

```text
source record/state
  -> Evidence use (support/contradict/qualify/input)
  -> evaluative target/context
```

Evidence may be explicit/persisted where identity/history matters, derived by rule/query where deterministic and reconstructible, or represented through a consequential evaluation snapshot.

```text
Evidence exists != target true
no Evidence != Evidence against
```

No universal evidence-strength/confidence scalar is accepted.

---

## 9. Confirmation

Disposition:

```text
Confirmation -> LR-03 typed actor-target-state attestation
```

When the attestation itself needs durable addressability/history:

```text
ScopedRecordRef(Confirmation)
```

Confirmation targets a materially relevant target state and purpose/context.

```text
Confirmation C1 -> target S1
later target S2
C1 remains about S1
```

Confirmation does not become Authority, truth, Agreement, Consent, Decision or Acknowledgement.

---

## 10. Acknowledgement

Disposition:

```text
Acknowledgement -> LR-03 typed actor-target-state common-ground attestation
```

It records explicit taking-notice of a target/material change. Delivery/read/display telemetry does not fabricate human Acknowledgement.

When durable history/addressability matters, a qualified Acknowledgement record may use ScopedRecordRef.

```text
Acknowledgement != Confirmation
!= Agreement
!= Consent
!= comprehension
!= performance
```

---

## 11. Criterion / Evaluation / Verification

### Criterion

Primary disposition:

```text
Criterion -> LR-05 rule/policy definition
```

A Criterion with independent material lifecycle/reuse/history may require a dependent semantic record and MaterialStateRef without becoming a universal native root.

### Evaluation

Default disposition:

```text
Evaluation -> LR-08 derived projection/process-result
```

Where consequence/reproducibility requires historical identity:

```text
materialized Evaluation -> LR-02 contextual semantic record
                           + ScopedRecordRef where addressed
```

A consequential Evaluation must bind/reconstruct:

```text
target MaterialStateRef
Criterion MaterialStateRef or equivalent rule state
Evidence/source material states actually used
window/context/purpose
evaluator/policy where material
assessment result
```

Current reevaluation may differ from historical Evaluation without rewriting the earlier basis.

### Verification

Verification remains a purpose/profile of Criterion/Evaluation semantics. No universal `VerificationResult` root is introduced.

---

## 12. Reconciliation

Reconciliation remains a cross-cutting reasoning/process capability, not a universal entity/root.

Where the resolution process itself has material historical consequence, a qualified reconciliation record may use:

```text
LR-02 / LR-07
ScopedRecordRef where addressed
```

and preserve bounded target/facet, competing states/assertions, resolution basis, relevant Evidence/Authority/Decision and resulting effect link.

The current/effective state remains owned by the affected semantic owner.

```text
Reconciliation != truth
Reconciliation != current-state owner
Reconciliation != Authority
Reconciliation != Version
```

Unresolved conflict is valid.

---

## 13. Current knowledge / memory projection

LifeOS durable memory is represented through **derived knowledge/retrieval projections**, not through a universal canonical fact store.

Disposition:

```text
Current/Historical Knowledge Projection -> LR-08
```

A projection may index/denormalize information such as:

```text
explicitly declared
observed
specialist-sourced
AI-inferred
historical
currently applicable
resolved/no-longer-applicable
unresolved/conflicting
```

but it MUST retain a reversible path to the canonical typed source/material-state/provenance basis.

```text
knowledge projection != source of truth
vector/search index != source of truth
AI memory summary != canonical fact
```

Cross-domain retrieval must consider semantic relevance, current applicability, Visibility and source/epistemic nature rather than merely recency.

Example pressure:

```text
"I like photography"
explicit declaration != AI inference

"I am celiac"
self-report != specialist diagnosis automatically

old fever
historical != currently applicable

healed fracture
historical condition remains but current activity planning must not treat it as active by default
```

---

## 14. Provider / external identity and specialist boundaries

Provider record/revision/source identifiers remain ExternalRef/provenance/concurrency inputs. They do not become LifeOS MaterialStateRef or native Observation identity automatically.

Specialist domains may preserve richer clinical/financial/legal/scientific condition/evidence/validity models through LR-13 extensions or authoritative external systems. LifeOS does not universalize those specialist lifecycles.

---

## 15. Privacy, Visibility, retention and deletion

Current target Visibility does not imply Visibility of:

- historical material states;
- Evidence;
- Provenance;
- Confirmation/Acknowledgement history;
- reconciliation conflict/rationale;
- private identity/source linkages.

Private source information may support an authorized shareable consequence without source disclosure.

Historical reconstructibility is not a backdoor indefinite archive. Deletion/redaction/anonymization may preserve minimal honest historical references where required while removing sensitive payload.

---

## 16. Candidate comparison

### Candidate A — Universal Fact / Claim graph

**Verdict:** REJECTED AS UNIVERSAL KERNEL.

Useful for bounded assertion/search/knowledge projections; rejected as canonical ontology because it recreates generic Entity/Relation/property escape hatches and flattens richer owner identity/lifecycle.

### Candidate B — Universal event-sourced / bitemporal ledger

**Verdict:** REJECTED AS UNIVERSAL LOGICAL REQUIREMENT.

Powerful possible physical technique, but event/transaction history does not define materiality, Evidence relevance, current accepted interpretation or semantic owner.

### Candidate C — fully owner-specific history/provenance/evidence per owner

**Verdict:** STRONG PHYSICAL INGREDIENT; not selected as complete logical baseline.

Maximum local specificity but duplicates state-binding/history/lineage/evaluation mechanisms and weakens cross-domain memory/query coherence.

### Candidate D — global W3C-PROV-like lineage graph as backbone

**Verdict:** REJECTED AS COMPLETE LOGICAL MODEL.

Excellent provenance evidence; does not own attestation/evaluation/reconciliation/current knowledge and introduces ontology shapes that LifeOS does not adopt wholesale.

### Candidate E — Layered Typed Epistemic & History Model

**Verdict:** SELECTED CANDIDATE.

Preserves typed owners, explicit material-state binding, lineage, attestation, Evidence use, evaluation, reconciliation and fast derived knowledge projections without a universal Fact/Version/Event root.

---

## 17. High-value queries

The logical model must support at least:

1. current material state of target X;
2. material state of X at historical time T;
3. what LifeOS currently accepts/applies about world time T;
4. what LifeOS knew/accepted at knowledge time K about T;
5. exact target state confirmed/acknowledged/decided/evaluated;
6. provenance path that produced current state;
7. exact source/material states used by historical Evaluation E;
8. why current reevaluation differs from historical evaluation;
9. unresolved conflicting Observations/assertions/states;
10. bounded basis that established current interpretation;
11. all evaluation contexts in which one source was used as Evidence;
12. safe result without disclosure of private Evidence/Provenance;
13. PDF/OCR/AI/correction lineage;
14. whether provider revision actually produced material semantic change;
15. current knowledge projection with explicit/observed/inferred/historical/unresolved/applicability distinctions;
16. historical reference after source redaction/deletion;
17. high-volume telemetry use without one Observation/Evidence row per sample/use;
18. applicability of prior Confirmation/Acknowledgement after target state change;
19. reconciliation reversal/correction history;
20. verification-purpose assessment without universal VerificationResult;
21. current interpretation under divergent states;
22. current state query without replaying lifetime history;
23. whether a remembered condition/state is still applicable now;
24. onset/resolution/history of a bounded temporary condition without deleting the history;
25. distinguish ongoing persistent state from unknown-ended or intermittent state.

---

## 18. Physical deferrals

```text
PostgreSQL current/history table mapping
system-versioned/bitemporal strategy
event sourcing usage
snapshot vs revision record strategy
MaterialStateRef physical ID/token
exact owner-history cardinalities
history indexing/partitioning
knowledge/search/vector projection technology
high-frequency telemetry storage
retention schedules/anonymization
specialist condition/status schemas
cryptographic signatures/credential engine
API serialization
AuthN/AuthZ enforcement
```

None may weaken this logical contract.

---

## 19. Cross-slice obligations

Slice A:

```text
ReferenceAddress remains representation-only
MaterialStateRef is now a precise state-address contract
Observation adds a justified LR-01 owner; no generic FactRef is introduced
```

Slice B:

```text
historical Goal/Plan/Activity/Decision semantics may bind to exact material states
knowledge projection must not invent intention
```

Slice C:

```text
world/effective temporal meaning remains distinct from knowledge chronology
Schedule/Session/Actual history becomes reconstructible without collapsing layers
temporal applicability uses typed time semantics without a universal status enum
```

Slice E must preserve value/resource/capacity history and current applicability where material.

Slice F must preserve Visibility/Authority/actor-scoped epistemic semantics without duplicating shared reality.

---

## 20. Current verdict

```text
SLICE D — EVIDENCE / KNOWLEDGE / HISTORY

SELECTED CANDIDATE
Layered Typed Epistemic & History Model

LOCAL VERDICT
PASS WITH HARDENING

Observation
LR-01 / NativeRef

MaterialStateRef
PRECISE LOGICAL CONTRACT ESTABLISHED

ReferenceAddress
REOPENED UNDER LM-WF-21
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED      0
NEW DOMAIN OWNER REQUIRED   0
LOGICAL STRUCTURAL BLOCKER  0

WD-03
LOGICAL MECHANISM SUBSTANTIVELY ESTABLISHED
FINAL DISCHARGE DEFERRED TO CUMULATIVE/FULL LOGICAL REGRESSION

REMOTE ACTIVATION
PENDING CHECKPOINT QA
```