# Security / Privacy / Retention / Recovery Requirements

- Status: **CURRENT — Phase 5 accepted requirement package**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical/security mechanism selection: **DEFERRED**

## Purpose

Define the security, privacy, retention, deletion/redaction and security-aware backup/recovery properties that later Physical/runtime/API/backend designs must preserve.

This package defines architectural requirements, not legal advice and not implementation selection. Exact legal bases, statutory retention periods, data residency obligations, processor arrangements and final policy language remain subject to qualified legal/security review where required.

## Accepted upstream boundaries

LifeOS already requires:

- user control and understandable disclosure;
- purpose-aware data use;
- bounded AI/provider context;
- provenance and historical truth;
- separation of canonical state from provider/cache/index state;
- retention/redaction/tombstone integrity through `WL-H10`;
- selective disclosure/non-interference through `WL-H03` and `WL-H12`;
- specialist/sensitive domains to retain stronger boundaries rather than being flattened into generic personal-data handling.

Historical reconstructibility MUST NOT be interpreted as permission for indefinite retention of every sensitive payload.

## Normative requirements

### SEC-01 — Purpose and handling class are explicit enough to enforce

Data processing and disclosure MUST have enough explicit purpose/context/sensitivity classification to apply appropriate controls.

The system MUST NOT rely on one global `personal = true` flag as the only privacy/security model.

Where a precise legal/data-class taxonomy is not yet accepted, the architecture MUST preserve the ability to introduce stronger per-category controls without redesigning canonical semantics.

### SEC-02 — Data minimization applies across collection, storage, disclosure, AI and providers

LifeOS MUST collect, retain, expose and send to AI/providers only the data reasonably necessary for the applicable purpose and accepted feature behavior.

A technically available field MUST NOT automatically be included in:

- AI context;
- logs/traces;
- provider payloads;
- search/vector indexes;
- analytics;
- exports;
- support/admin views;
- shared projections.

### SEC-03 — Confidentiality, integrity and availability are risk/consequence sensitive

Controls MUST protect confidentiality, integrity and availability according to the sensitivity and consequence of the data/effect.

The design MUST support stronger controls for higher-risk categories without requiring those categories to be converted into a separate universal ontology.

### SEC-04 — Credentials, secrets and cryptographic material are not canonical Domain data

Secrets, provider credentials, signing/encryption keys, authentication factors and equivalent security material MUST be isolated from ordinary canonical Domain payloads and MUST NOT be hard-coded in source, documentation, test fixtures or logs.

Access, rotation and storage mechanisms are implementation-deferred, but secure separation is mandatory.

### SEC-05 — Observability is privacy-minimized

Logs, metrics, traces, error payloads and diagnostic events MUST minimize sensitive/personal data and MUST NOT become an uncontrolled parallel history store.

Where identifiers/correlation are required for diagnosis, exposure and retention MUST be bounded to operational purpose.

### SEC-06 — Retention is category/purpose/consequence sensitive

LifeOS MUST NOT assume one global indefinite retention rule.

Retention policy MUST be capable of varying by applicable data category, purpose, user action, legal requirement, specialist boundary and historical/audit necessity.

Exact durations remain open until responsibly decided.

### SEC-07 — Deletion/redaction/anonymization must preserve truthful semantics

Deletion, anonymization or redaction MUST NOT fabricate a false historical statement.

Where policy permits/needs minimal continuity, the system MAY preserve bounded non-sensitive tombstone/reference/provenance continuity sufficient to distinguish:

```text
redacted / unavailable
!= never existed
```

This MUST NOT be used as a pretext to retain sensitive payload unnecessarily.

### SEC-08 — Native identity is never recycled

A removed/redacted referent MUST NOT cause its NativeRef to be reassigned to a different referent.

Identity non-reuse remains mandatory even when payload retention is minimized.

### SEC-09 — Deletion/correction propagation is explicit across derived and external state

When canonical data is deleted, corrected, redacted or access-restricted, the architecture MUST define how applicable downstream copies/projections are handled, including as relevant:

- caches;
- search indexes;
- vector/retrieval indexes;
- analytics/derived projections;
- device-local copies;
- synchronized provider copies;
- backup/restore lineage.

If immediate propagation is impossible, the state MUST expose the pending/unresolved propagation or reconciliation truthfully rather than pretending completion.

### SEC-10 — Backup/restore must not silently resurrect forbidden state

Restore/recovery processes MUST preserve currently applicable deletion, redaction, retention and disclosure requirements.

A restore MUST NOT silently reintroduce data that policy requires to remain deleted/redacted or make previously restricted data newly visible merely because an older backup contains it.

The design MUST support a truthful strategy for reconciling restored historical media with later deletion/redaction state.

### SEC-11 — User data access/export/correction/deletion remain supportable

The architecture MUST preserve the ability to support accepted user controls around accessing, exporting, correcting and deleting their data without requiring direct database access or bypassing semantic/provenance rules.

The exact product/legal workflow remains later work, but the Physical Model MUST NOT make these capabilities structurally impossible.

### SEC-12 — AI/provider context is purpose-bounded and disclosure-aware

Context Builder and integration/provider layers MUST apply purpose-aware minimization and applicable Visibility/disclosure boundaries before data is exposed externally or to AI.

Private source material MAY support an authorized shareable consequence without exposing the private source itself.

AI/provider access MUST NOT be treated as internal full-database privilege by default.

### SEC-13 — Sensitive/specialist categories support stronger controls

The architecture MUST permit stronger isolation, authorization, retention, audit, context-minimization and disclosure behavior for sensitive/specialist categories such as health-adjacent, financial, legal or other high-consequence information when product/legal requirements demand it.

Generic flexible metadata MUST NOT be used to bypass those stronger requirements.

### SEC-14 — Security/recovery controls are testable

Security, retention, deletion propagation and recovery controls MUST be testable through repeatable validation rather than existing only as documentation.

Later implementation MUST include tests appropriate to the accepted mechanisms and risk classes.

### SEC-15 — Backup/recovery access is privileged, governed and auditable

Backup creation, restoration, recovery tooling and access to backup payloads MUST be treated as privileged security operations.

Where consequence requires, actual operator/service identity, purpose, authorization and resulting recovery action MUST be auditable.

### SEC-16 — Provider/export copies do not become uncontrolled shadow truth

Exports, provider mirrors and integration payloads MUST retain enough source/provenance/state information to distinguish them from current canonical LifeOS state.

Security/privacy controls MUST account for the fact that external copies may have different deletion/retention capabilities and must expose limitations truthfully.

### SEC-17 — Security failure must fail safely without falsifying semantic state

Where a security/privacy control cannot establish safe disclosure/effect, the runtime MAY deny or degrade the operation according to policy.

That technical safety outcome MUST NOT rewrite unknown/unresolved semantic state into a false canonical negative.

## Security/privacy recovery vs operational recovery

This document owns the **security/privacy correctness of recovery**, including:

```text
backup-data protection
backup/restore authorization
restore audit
retention/redaction/deletion correctness through restore
prevention of unauthorized data resurrection
confidentiality/integrity of recovery data
```

`nonfunctional-multidevice-recovery.md` separately owns operational RPO/RTO, availability/degraded behavior and restore-time objectives.

## Open parameters / decisions

The following require later explicit resolution before dependent implementation is accepted:

```text
SEC-OPEN-01 final data/sensitivity classification catalogue
SEC-OPEN-02 exact retention schedule per accepted category/purpose
SEC-OPEN-03 legal basis / notice / consent treatment per regulated processing purpose
SEC-OPEN-04 data residency/localization requirements if applicable
SEC-OPEN-05 processor/subprocessor governance and contractual requirements
SEC-OPEN-06 DPIA or equivalent risk-assessment triggers where applicable
SEC-OPEN-07 final admin/support access policy
SEC-OPEN-08 incident/breach-response operating requirements
SEC-OPEN-09 backup retention/media lifecycle policy
SEC-OPEN-10 irreversible deletion vs cryptographic-erasure requirements by storage class
```

These are not to be guessed during Physical selection.

## Deferred mechanisms — not selected by Phase 5

No mechanism is selected here for:

```text
encryption algorithm/provider
KMS/HSM/secret-store product
field/column/application/database encryption split
backup technology
immutable backup product
DLP product
SIEM/log platform
anonymization/tokenization technology
data-residency provider
privacy policy engine
specific redaction/tombstone physical representation
specific deletion propagation queue/workflow
```

Later mechanisms must satisfy this package rather than redefining it.

## Downstream acceptance / benchmark pressure

Physical/runtime candidates MUST be pressure-tested for at least:

1. selective disclosure without source leakage;
2. redaction/deletion while preserving permitted historical integrity;
3. deletion propagation to caches/indexes/derived state;
4. restore from an older backup after a later deletion/redaction event;
5. backup access/audit isolation;
6. high-sensitivity payload isolation/minimization;
7. AI/provider context minimization;
8. history/provenance reconstruction without turning retention into indefinite sensitive archive;
9. schema/data evolution without resurrecting or overexposing deprecated sensitive fields.

## Traceability

Primary downstream Logical pressure:

```text
WL-H03 bounded projection/disclosure
WL-H08 canonical != provider state
WL-H10 retention/redaction/tombstone integrity
WL-H11 consequential security/AuthZ provenance where applicable
WL-H12 non-interference/inference leakage
```

This package does not authorize security implementation, select Physical persistence or provide final legal advice.
