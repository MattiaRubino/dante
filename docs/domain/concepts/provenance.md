# Provenance v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **Provenance is the persistent contextual lineage describing how a specific domain record or material version came to exist or change, including the generating, importing, deriving, transforming, correcting, or otherwise influential activities, source entities, agents/systems, and relevant times needed to understand its origin and evolution. Provenance explains lineage; it does not by itself establish truth, authority, Confirmation, Evidence relevance, or decision rationale.**

Provenance answers:

> **How did this specific record/version come to exist, and what materially influenced its current form?**

Conceptually:

```text
source entity / external record / prior version
        ↓
activity / import / derivation / transform / correction
        ↓
actor / system / provider where relevant
        ↓
current target version
```

Provenance is intentionally bounded. It preserves materially useful lineage without requiring maximal recursive capture of every technical event.

---

# 1. Why Provenance exists

LifeOS needs to explain the origin and evolution of information without collapsing that explanation into the information itself.

Without explicit Provenance semantics the model tends toward weak alternatives such as:

- one `source` string on every record;
- overwriting imported values after correction;
- pretending AI-extracted information was entered directly by the user;
- losing derivation chains for calculated/normalized values;
- treating creator/source as authority;
- using audit logs as data lineage;
- preserving current state while making historical explanation impossible.

Provenance keeps source, transformation and correction history available where materially useful.

---

# 2. Provenance versus Source

`Source` is one possible provenance dimension, not the whole concept.

```text
source = provider X
```

may be insufficient when reality is:

```text
original file
↓
provider import
↓
normalization
↓
AI extraction
↓
user correction
↓
current record
```

Therefore:

> **Source != Provenance.**

A provider ID may assist reconciliation/mapping but does not define LifeOS identity.

---

# 3. Provenance versus truth and authority

Traceability does not establish truth.

```text
official provider import
```

means LifeOS can explain that origin. It does not guarantee that the content is objectively correct in every context.

Likewise:

```text
created by Actor A
```

never implies that Actor A has authority to establish the target as canonical for everyone.

Therefore:

```text
Provenance != truth
Provenance != Authority
creator/source != authority by default
```

Authority policies may use provenance as input, but provenance does not manufacture authority.

---

# 4. Provenance versus Confirmation

Confirmation is an attestation toward a target/version. Provenance explains how the target/version came to exist.

```text
Observation v1
source: imported device record

Confirmation C1
Mattia affirms Observation v1
```

The Observation's lineage does not become `user-entered` merely because Mattia later confirmed it.

The Confirmation itself may also have its own Provenance.

Therefore:

> **Provenance != Confirmation.**

---

# 5. Provenance versus Evidence

Evidence describes evaluative relevance/use. Provenance describes origin/evolution.

The same Observation may retain identical Provenance while serving as Evidence in several unrelated evaluations.

Therefore:

> **Provenance != Evidence.**

Provenance may affect how Evidence is interpreted, but does not decide evidentiary relevance or weight.

---

# 6. Provenance versus Version

Version semantics identify materially distinct states of a target over time. Provenance explains how a specific version was produced or changed.

```text
Observation v1
66.4 kg

Observation v2
64.6 kg
```

Versioning can identify v1 and v2. Provenance can explain that v2 resulted from a user correction of imported v1 using a particular source/basis.

Therefore:

> **Version != Provenance.**

The future Version model must integrate with Provenance without replacing it.

---

# 7. Provenance versus Audit

Audit/security history and domain lineage overlap in some events but answer different questions.

```text
Audit
who accessed/changed/used the system?

Provenance
what materially produced/influenced this domain record/version?
```

Repeated reads of a record may be relevant to audit without becoming lineage of the record itself.

Therefore:

> **Audit != Provenance.**

Retention and access policy may differ between them.

---

# 8. Corrections and material history

A correction must not rewrite origin history.

Example:

```text
Observation v1
66.4 kg
source: device import

later correction
Observation v2
64.6 kg
actor: user
basis: receipt/manual check
```

Current views may use v2 while material history can still explain that v1 existed, where it came from, and why it was changed.

Canonical rule:

> **Current correctness must not be achieved by falsifying historical lineage.**

Exact version/correction persistence remains deferred to the logical model.

---

# 9. Derived and transformed information

Derived records must retain enough lineage to explain their material inputs and transformation basis.

```text
Observation A-v1 = 5 km
Observation B    = 7 km
        ↓
weekly aggregate = 12 km
```

If A is later corrected to 4.5 km, LifeOS may recompute a current value of 11.5 km without pretending the historical 12 km calculation was originally based on A-v2.

Where material, provenance should support:

- source record/version references;
- derivation/transform activity;
- rule/model/formula version where relevant;
- actor/system/provider involved;
- effective/recorded/processing times as semantically relevant.

Query aggregates that are not persisted do not require artificial standalone Provenance objects; the computation path may be reproducible from query/rule context.

---

# 10. AI and ingestion lineage

AI-mediated extraction must not launder origin.

Example:

```text
PDF
↓
OCR provider
↓
AI extraction/model
↓
structured candidate
↓
user correction
↓
accepted record
```

The accepted record must not be represented as though the user directly authored the original extracted value.

Provenance should preserve materially relevant AI/provider lineage, including model/rule/version identifiers when needed for explanation, debugging, reconciliation, safety, or audit.

AI confidence is not Provenance truth and AI provenance is not disclosure permission.

---

# 11. Multi-actor semantics

Provenance must preserve actor-role distinctions.

```text
Subject
Grandmother

Source actor
Grandmother verbal report

Recorder
Luca

Observer
may be different or absent

Transformer
LifeOS import/normalization

Confirmer
may be another actor

Authority
separate
```

Do not rewrite this as though the recorder personally observed the event or the subject personally entered the record.

External/non-LifeOS people and providers may participate in provenance without requiring LifeOS accounts.

Canonical guardrail:

```text
subject
!= source actor
!= observer
!= recorder
!= transformer
!= confirmer
!= authority
```

where those roles differ in reality.

---

# 12. Visibility and privacy

Target visibility and Provenance visibility are independent questions.

A shared derived consequence may be visible while private source lineage remains hidden.

Example:

```text
shared
Sara unavailable 14:00–16:00

not automatically shared
medical source reason
provider/clinic
private supporting record
```

Therefore:

> **Target visibility does not imply full Provenance visibility.**

Likewise, access to a provenance fragment does not grant access to all upstream private source payloads.

AI/tool explanations must respect the same boundary.

---

# 13. Retention, deletion and minimization

Historical traceability does not justify retaining every sensitive source payload forever.

Deletion/retention policy may preserve a minimal historical fact such as:

```text
record existed
was corrected/deleted at time X
by actor/process Y
```

without preserving a deleted sensitive payload when policy/law/product semantics require removal or anonymization.

Canonical rule:

> **Provenance history is subject to privacy, retention, deletion, minimization and legal requirements; it is not a backdoor archive.**

---

# 14. Bounded depth

Provenance may itself have Provenance conceptually, but LifeOS does not require infinite recursive capture.

Capture depth should be sufficient to preserve material lineage for the relevant product/domain consequence.

Low-risk manual record:

```text
entered by user at T
```

may be enough.

High-consequence imported/derived/corrected record may require a richer chain.

> **Material lineage, not maximal lineage, is the default objective.**

---

# 15. Identity and cardinality

Provenance semantics may attach to records, material versions, Confirmations, derived outputs, Decisions, relationships, or other future domain objects where lineage matters.

A target may require zero, one, or several provenance facts/segments depending on how it was produced and revised.

The exact persistence shape is deliberately deferred. This concept does not pre-approve:

- one universal `provenance` table;
- one generic graph for all history;
- one polymorphic foreign key strategy;
- one row for every technical processing event.

---

# 16. UI implications

Most users should not see ontology language.

Typical UI:

- Source: Garmin;
- Imported from…;
- Entered by…;
- Corrected by…;
- Derived from…;
- Why does LifeOS show this?;
- View history / source details.

Progressive disclosure should expose richer lineage only when useful.

---

# 17. External benchmark interpretation

External systems support the separation without dictating LifeOS schema:

- W3C PROV distinguishes entities, activities, agents, generation, derivation, revision and primary-source lineage;
- HL7 FHIR Provenance models creation/revision/import/transformation lineage around target resources and versions;
- FHIR distinguishes Provenance from AuditEvent semantics;
- specialist standards demonstrate that provenance may itself have provenance and that privacy can require selective disclosure/segmentation.

LifeOS borrows the semantic lesson, not the complete ontology.

---

# 18. Invariants

1. Provenance explains material origin/evolution, not universal truth.
2. Source is a Provenance dimension, not the whole concept.
3. Provenance does not create Authority.
4. Provenance != Confirmation.
5. Provenance != Evidence.
6. Provenance != Version.
7. Provenance != Audit.
8. Provider IDs do not define LifeOS identity.
9. Corrections preserve materially relevant prior lineage.
10. Derived/transformed records retain material source/transformation traceability.
11. AI/import pipelines must not launder authorship/source.
12. Subject/source/observer/recorder/transformer/confirmer/authority roles remain distinguishable.
13. External/non-account actors may exist in Provenance.
14. Target visibility does not imply full Provenance visibility.
15. Provenance access does not imply access to all upstream private payloads.
16. Retention/history does not justify indefinite storage of deleted sensitive payloads.
17. Provenance depth is bounded by material need, not maximal recursion.
18. Provenance semantics do not pre-approve one physical provenance table/graph.

---

# 19. Rejected alternatives

Rejected:

- one `source` string as full provenance model;
- Provenance = truth;
- Provenance = Authority;
- merge with Confirmation;
- merge with Evidence;
- merge with Version;
- merge with Audit log;
- provider ID as domain identity;
- destructive correction overwrite;
- record-everything-forever lineage;
- wholesale adoption of W3C PROV/FHIR physical ontology.

---

# 20. Deliberately deferred questions

- exact logical/physical representation;
- generic versus typed provenance relationships;
- Version/material-version mechanics;
- Decision rationale versus lineage;
- Authority and source-precedence policy;
- signature/verification specialist semantics;
- retention classes and anonymization;
- offline/sync conflict provenance;
- provider reconciliation identifiers;
- how much transformation/model metadata must be persisted by consequence level;
- provenance of dynamic semantic relationships and AI proposals.

---

# 21. Persistence/API implications without physical commitment

The future model must be able to reconstruct material lineage where required, including combinations of:

- target identity/material version;
- source entity/record/provider;
- source version/external identifier where useful;
- generating/importing/deriving/transforming/correcting activity;
- actor/system/provider role;
- relevant timestamps;
- previous/derived-from relationships;
- rule/model/formula version where material;
- correction/reconciliation reason where appropriate;
- selective visibility/retention rules.

This is a semantic capability requirement, not a final table design.

---

# 22. Reopening triggers

Reopen Provenance v0 if later Version/Decision/Audit/Authority work proves this boundary redundant, if persistence pressure demonstrates that material lineage cannot be represented without unacceptable generic coupling, or if specialist interoperability/safety requirements require a stronger universal provenance distinction.

Absent such evidence, Provenance remains the current accepted baseline.