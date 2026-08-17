<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-3.md" -->
> **Canonical continuation of `representation-framework-v1.md`.** This physical file is Part 4 of the same logical document and appends Slice-D Evidence / Knowledge / History representation contracts.

# 2026-08-17 — Slice D representation hardening

## 27. Observation as native identity

Observation satisfies native identity pressure independently of persistence convenience:

```text
Observation -> LR-01
Observation -> NativeRef
```

Correction of the same observational act preserves target identity by default while material state changes. Re-observation is normally a new Observation.

```text
Observation identity != subject + property + time + value tuple
```

High-volume sampled data does not require one LR-01 Observation object per raw sample; specialist/source-native representation may retain raw series while selected contextual observations remain canonical where appropriate.

---

## 28. MaterialStateRef contract

`MaterialStateRef` means a stable semantic reference to one materially relevant state of an existing target under an applicable Reference Contract/facet-purpose context.

It is **not** a new Domain owner and is never inferred merely from:

```text
row version
updated_at
ETag
MVCC token
provider revision
sync token
hash
```

Required properties:

```text
stable target association
stable addressed material state
no silent retargeting
purpose/facet-sensitive material equivalence
support for divergent/non-linear states
lossless historical semantic binding
```

Physical realization remains open.

---

## 29. Epistemic/history representation roles

Slice D uses the existing LR taxonomy as follows:

```text
Observation                 LR-01
Actual                      LR-02 + LR-06
Outcome                     LR-02 / LR-06 where materially persistent
Provenance                  LR-07 + typed lineage relations
Evidence use                LR-03
Confirmation                LR-03 (+ ScopedRecordRef where addressed)
Acknowledgement             LR-03 (+ ScopedRecordRef where addressed)
Criterion                   LR-05 (+ LR-02 material record where justified)
Evaluation                  LR-08 by default; LR-02 snapshot where consequential
Verification                profile/purpose of Evaluation
qualified Reconciliation    LR-02 / LR-07 where materially recorded
Knowledge/retrieval view    LR-08
```

No additional generic `Fact`, `Claim`, `Assertion`, `Attestation`, `Version` or `Knowledge` LR root is introduced.

---

## 30. Typed history versus universal history engine

A common history/query contract does not require one physical mechanism for every owner.

Valid future implementation ingredients may include:

```text
owner-specific revision records
immutable facts/events
snapshots
system-versioned/temporal tables
append-only ledgers
specialist history stores
materialized current-state projections
```

Selection is deferred to Physical Model evidence. Whatever combination is chosen must satisfy the same material-state and historical reconstruction contract.

---

## 31. Effective/world time versus knowledge chronology

Where material, representations must distinguish:

```text
effective/world time
recorded/learned time
accepted/current-interpretation chronology
corrected/superseded chronology
```

This distinction is conceptual. It does not impose universal four-column bitemporality.

Current-state indexes/projections may precompute answers but must remain reconstructible from canonical owners/history.

---

## 32. Applicability of remembered state

Cross-domain knowledge/retrieval must not treat every historical source record as currently applicable.

Representation must permit the semantic owner/material state to expose or derive applicability such as:

```text
currently applicable
bounded episode
resolved/no-longer-applicable
end unknown
recurrent/intermittent
historical-only
```

These labels are explanatory categories, **not** a universal canonical status enum.

```text
record existence != current applicability
unknown end != permanent
resolved != deleted
```

A point Observation carries its own effective context and does not become a continuing condition automatically.

---

## 33. Knowledge projection

Current/historical knowledge and retrieval indexes are:

```text
LR-08 derived projections
```

They may denormalize:

```text
subject/referent
semantic topic
current applicability
explicit vs observed vs inferred vs specialist-sourced
source/provenance pointers
visibility classification/projection eligibility
search/vector features
```

but MUST retain reversible links to canonical typed owners/material states.

```text
knowledge row != canonical Fact
embedding != truth
AI summary != source record
```

---

## 34. Evidence representation

Evidence is an evaluative-use relationship, not a copy or intrinsic flag.

```text
ReferenceAddress(source)
+ source MaterialStateRef where required
+ evaluation target/context
+ direction/qualification where meaningful
```

May be:

- explicit/persisted;
- derived by deterministic rule/query;
- represented as part of a consequential evaluation snapshot.

Do not require one Evidence record per transient query/source use.

---

## 35. Provenance representation

Provenance may use typed qualified lineage segments/relations rather than one global graph root.

Potential dimensions include:

```text
target state
source state/provider
lineage role
process/model/rule
Actor role
relevant chronology
```

Technical audit/read telemetry remains separate unless it materially produced/influenced target state.

---

## 36. Attestation representation

Confirmation and Acknowledgement may share technical relation infrastructure while retaining different Reference Contracts and semantics.

```text
shared technical mechanism
!= shared semantic Attestation superclass
```

A target material-state change does not silently move prior attestation to the new state.

---

## 37. Evaluation materialization

```text
transient/recomputable Evaluation -> LR-08
consequential historical Evaluation -> LR-02 snapshot
```

Materialized assessment identity is justified by historical consequence, not by every calculation tick.

A historical evaluation snapshot must bind to/reconstruct the target/rule/source material states actually used.

---

## 38. Reconciliation representation

Reconciliation may remain transient reasoning when low consequence. Where history/rationale/effect matters it may be represented by a qualified LR-02/LR-07 record.

The affected semantic owner retains current-state ownership.

```text
reconciliation record != canonical Fact
winner source != universal source priority
```

---

## 39. Simple-case compactness

Examples that must remain compact:

```text
manual weight entry
simple personal note-like assertion mapped to appropriate owner
one explicit Confirmation
one current preference/interested-state projection
```

No user-facing version graph, Evidence graph, reconciliation object or provenance tree is mandatory in ordinary low-consequence use.

Kernel precision remains compatible with hidden/default infrastructure and progressive disclosure.

---

## 40. Physical-stage obligations

Physical candidates must prove:

1. MaterialStateRef can be resolved/reconstructed efficiently;
2. current state does not require full lifetime replay in application memory;
3. owner-specific referential integrity is retained;
4. history divergence/correction can be represented;
5. world/effective and knowledge chronology queries survive;
6. cross-domain retrieval can use current applicability safely;
7. high-volume telemetry/evaluation does not explode canonical rows;
8. retention/redaction does not falsify historical bindings;
9. provider revisions remain external/technical until semantic mapping proves materiality;
10. no generic Fact/Version/Event root is required to achieve performance.