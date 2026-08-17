<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-3.md" -->
> **Canonical continuation of `decision-and-assumption-register-v1.md`.** This physical file is Part 4 of the same logical register and records Slice-D Evidence / Knowledge / History decisions, rejected alternatives, assumptions and refresh triggers.

# 2026-08-17 — Slice D decisions

## DEC-D01 — Observation is native identity

```text
DECISION
Observation -> LR-01 + NativeRef.
Correction of the same observational act normally preserves Observation identity; re-observation normally creates a new Observation.

STATUS
ACCEPTED WITH HARDENING
```

Rationale: Observation can exist independently, be reused in multiple contexts/evaluations and carry material correction history.

---

## DEC-D02 — MaterialStateRef is semantic state addressability

```text
DECISION
MaterialStateRef is a stable reference to a materially relevant state of an existing semantic target under an applicable facet/purpose Reference Contract.

STATUS
ACCEPTED WITH HARDENING
```

Rejected automatic equivalences:

```text
MaterialStateRef = version_number
MaterialStateRef = updated_at
MaterialStateRef = ETag
MaterialStateRef = MVCC token
MaterialStateRef = provider revision
MaterialStateRef = hash
```

---

## DEC-D03 — no universal Version root

```text
DECISION
Material-state/version semantics remain a cross-cutting capability and do not create a universal native Version entity/root.

STATUS
ACCEPTED
```

---

## DEC-D04 — history technique remains physically open

```text
DECISION
The Logical Model does not mandate event sourcing, temporal tables, global bitemporality, immutable facts, snapshots or owner-specific revision tables universally.

STATUS
ACCEPTED
```

Different bounded physical techniques may coexist if they satisfy the same historical semantic contract.

---

## DEC-D05 — world/effective time and knowledge chronology are distinct

```text
DECISION
Where materially relevant, LifeOS must distinguish when something applied in the represented world from when LifeOS learned/recorded it, when an interpretation became current and when it was corrected/superseded.

STATUS
ACCEPTED WITH HARDENING
```

This is a semantic query requirement, not a mandatory four-column schema.

---

## DEC-D06 — current applicability is not record existence

```text
DECISION
Durable history does not imply current applicability. Current retrieval must respect the owning semantic state's effective applicability.

STATUS
ACCEPTED WITH HARDENING
```

Examples pressured before write:

```text
ongoing celiac context
bounded/resolved broken-leg episode
point or temporary fever information
unknown-ended state
intermittent/recurrent state
```

No universal cross-domain status enum is accepted.

---

## DEC-D07 — knowledge memory is LR-08 projection

```text
DECISION
Current/historical knowledge and retrieval indexes are derived LR-08 projections over canonical typed owners/material states.

STATUS
ACCEPTED
```

Rejected:

```text
canonical facts(key,value) store as LifeOS source of truth
embedding/vector record as truth
AI memory summary as canonical source
```

---

## DEC-D08 — Provenance remains typed bounded lineage

```text
DECISION
Provenance uses LR-07 plus typed qualified lineage relations/segments where material; no global PROV ontology is adopted wholesale.

STATUS
ACCEPTED
```

---

## DEC-D09 — Evidence is evaluative use

```text
DECISION
Evidence -> LR-03 contextual evaluative-use relation; source identity/payload remains with the source owner.

STATUS
ACCEPTED
```

Evidence may be explicit, derived or captured through a consequential evaluation snapshot depending on reconstructibility needs.

---

## DEC-D10 — Confirmation and Acknowledgement share infrastructure, not semantics

```text
DECISION
Confirmation and Acknowledgement may use common typed-relation/reference infrastructure but retain distinct Reference Contracts and meanings.

STATUS
ACCEPTED
```

No universal semantic Attestation root is introduced.

---

## DEC-D11 — Evaluation materialization is consequence-sensitive

```text
DECISION
Evaluation is LR-08 by default. Consequential/reproducibility-sensitive historical assessments may be LR-02 materialized snapshots with ScopedRecordRef.

STATUS
ACCEPTED WITH HARDENING
```

Persist-everything and persist-nothing are both rejected.

---

## DEC-D12 — Verification stays an Evaluation purpose/profile

```text
DECISION
No universal VerificationResult owner/root.

STATUS
ACCEPTED
```

---

## DEC-D13 — Reconciliation does not own canonical state

```text
DECISION
Reconciliation remains a reasoning/process capability; a qualified record is materialized only where rationale/history/effect needs it. Current/effective state remains owned by the affected semantic owner.

STATUS
ACCEPTED
```

Unresolved conflict remains valid.

---

## DEC-D14 — specialist condition semantics stay bounded

```text
DECISION
Health/clinical condition lifecycle models may influence/apply through LR-13 or specialist source-of-record integration but are not universalized into a LifeOS Condition/Status root.

STATUS
ACCEPTED
```

The shared kernel requirement is history/applicability integrity, not clinical ontology replication.

---

## DEC-D15 — mechanism reconsideration

```text
CANDIDATES REOPENED
Universal Fact/Claim graph
Universal event-sourced/bitemporal ledger
Fully owner-specific history
Global PROV-like lineage graph
Layered Typed Epistemic & History

SELECTED
Layered Typed Epistemic & History

ReferenceAddress
RETAIN + HARDEN

MaterialStateRef
HARDEN
```

No architecture receives incumbency privilege.

---

# Rejected alternatives register

## ALT-D01 — Universal Fact / Claim graph

Rejected as universal kernel because it flattens rich owner identity/lifecycle and recreates generic semantic property/relation escape hatches.

May remain useful for bounded knowledge projections/adapters/assertion families.

## ALT-D02 — Universal event-sourced/bitemporal ledger

Rejected as universal Logical Model requirement because storage/transaction history does not define semantic materiality, Evidence relevance, current accepted interpretation or owner identity.

Remains a serious Physical Model candidate/ingredient.

## ALT-D03 — Fully owner-specific independent history stacks

Rejected as complete Logical Model baseline due duplicated state-binding/provenance/evaluation mechanisms and weak cross-domain coherence.

Retained as strong physical ingredient.

## ALT-D04 — Global PROV-like graph

Rejected as complete Logical Model because lineage ontology does not own attestation/evaluation/reconciliation/current knowledge and generic Entity/Activity/Agent roots would conflict with LifeOS semantic boundaries.

## ALT-D05 — Canonical facts(key,value) memory store

Rejected because current retrieval would erase explicit/observed/inferred/source/applicability/history distinctions and invite latest-value semantics.

## ALT-D06 — universal applicability/status enum

Rejected because `active/resolved/intermittent/...` semantics vary by owner/specialist context. Shared requirement is applicability/history queryability, not one vocabulary.

---

# Assumption register

## ASM-D01 — Material state can be represented without universal physical mechanism

```text
ASSUMPTION
Different owner classes may use different physical history techniques while preserving one logical MaterialStateRef contract.

EVIDENCE
Domain Version semantics + broad database/history benchmark.

STABILITY
medium-high

IF FALSE
Physical Model may need a stronger shared history substrate.

REFRESH
Physical Model candidate comparison; Whole-Logical closure.
```

## ASM-D02 — Current knowledge projection can remain derived/rebuildable

```text
ASSUMPTION
Fast personal-memory/retrieval can be implemented as LR-08 projections without becoming canonical truth.

EVIDENCE
read-model/search/index patterns; Product Reality scenarios.

STABILITY
high at logical level

IF FALSE
reopen projection ownership only after proving canonical-source queryability impossible.

REFRESH
Physical Model/search/reasoning design.
```

## ASM-D03 — Owner-specific applicability is sufficient

```text
ASSUMPTION
LifeOS does not currently require a universal Condition/Applicability Domain owner; owner-specific state plus common temporal/history contract is sufficient.

EVIDENCE
celiac/fracture/fever pressure + FHIR specialist benchmark + Domain anti-universal-root rules.

STABILITY
medium

IF FALSE
reopen only if multiple non-specialist owners require independent persistent applicability semantics that cannot be composed.

REFRESH
Slice E/F; Whole-Logical; specialist-profile design.
```

## ASM-D04 — consequential evaluations are a minority

```text
ASSUMPTION
Most rolling/dashboard evaluations can remain derived while a bounded subset needs historical materialization.

EVIDENCE
Domain Criterion/Evaluation semantics and scale pressure.

STABILITY
medium-high

IF FALSE
Physical Model may materialize more assessments without changing semantic owner classification.

REFRESH
analytics/reasoning workloads.
```

## ASM-D05 — retention can preserve honest historical references without every old payload

```text
ASSUMPTION
Privacy/deletion policies can remove/redact some historical content while preserving enough metadata/reference to avoid falsifying consequential history.

EVIDENCE
Domain Provenance/Version privacy boundaries.

STABILITY
medium; legally/product dependent

IF FALSE
specialist/legal retention rules may require profile-specific treatment, not kernel history weakening.

REFRESH
privacy/retention/security workstream.
```

---

# Deferred physical decisions

```text
exact PostgreSQL history mapping
MaterialStateRef token/ID format
temporal/bitemporal/event sourcing use
current projection/index technology
vector/search architecture
history partitioning/indexes
source redaction/tombstone representation
specialist clinical condition profile
cryptographic credential/signature engine
```

None is pre-approved by Slice D.