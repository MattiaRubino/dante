# Backend CP6-01 — Concrete Persistence Coverage Map

- **Status:** CP6-01 CONTENT CANDIDATE / PENDING SECOND-PASS INDEPENDENT REVIEW / GATE 01 NOT PASSED
- **Date:** 2026-08-21
- **Branch:** `feature/logical-postgresql`
- **CP6 authority:** `docs/workstreams/logical-postgresql.md`
- **Purpose:** translate the already-CLOSED Domain/Logical/Physical corpus into concrete PostgreSQL persistence obligations without re-performing semantic discovery and without designing business DDL.
- **Write boundary:** documentation only. This document authorizes no business schema, migration, SQLAlchemy mapping, persistence adapter, use case or API.

> This document is a **coverage and obligation map**, not a new Domain Model, Logical Model, Physical Model, or database schema. Where it adds a CP6 classification such as “material pressure”, “constraint pressure” or “next stage”, that classification is an implementation-planning interpretation of already-accepted semantics. It MUST NOT silently reclassify an upstream owner.

---

## 1. Authority and precedence

The consumed authority is:

```text
CLOSED Domain Atlas / Whole-Domain
        ↓
CLOSED Whole-Logical 57/57
        ↓
Whole hardenings WL-H01..WL-H12
        ↓
CLOSED / ACCEPTED Physical Model
        ↓
accepted PostgreSQL 18.4 mapping thesis
        ↓
PG-R01..PG-R10 risk register
        ↓
post-selection PSV carry-forward
        ↓
implemented CP1–CP5 backend / CP3 persistence contract
        ↓
CP6 durable workstream
```

This checkpoint MUST NOT reopen any upstream decision because of SQL, ORM, table-count, naming or implementation convenience.

### 1.1 Canonical consumed Logical facts

Whole-Logical already establishes:

```text
57 / 57 Domain concepts classified
15 / 15 LR-01 native owners
0 unclassified
0 generic fallback dependencies
0 ownerless material-state families
0 required universal roots
```

The exact accepted native set remains:

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

Canonical non-native roles remain:

```text
Actor
Subject
Resource
```

with **no ActorRef / SubjectRef / ResourceRef** wrapper identity.

### 1.2 Canonical consumed PostgreSQL mapping thesis

The accepted PostgreSQL direction is:

```text
owner-specific canonical tables/families
+ owner-specific material-state/history structures
+ specific relation tables/families
+ bounded technical address/state anchors only where genuinely required
+ separated integration/projection/technical concerns
```

Forbidden as semantic fallbacks:

```text
universal Entity / Thing
universal Relationship / Edge
canonical EAV/property bag
universal event-log ontology
universal Rule / Fact / Version / Permission root
JSONB as required-semantic escape hatch
PostgreSQL inheritance as ontology
```

Direct homogeneous FKs remain preferred. Bounded technical anchors are allowed only for genuinely heterogeneous addressing and MUST NOT acquire generic domain state.

### 1.3 CP1–CP5 implementation baseline consumed, not redesigned

Already materialized and outside CP6-01 redesign:

```text
PostgreSQL 18.4
schema = dante
SQLAlchemy 2 async
psycopg 3
Alembic
shared Base / MetaData
single migration DAG / online migrations
outer application operation owns transaction
autobegin=False
dante_owner / dante_migrator / dante_runtime separation
real-PostgreSQL test lane
```

---

## 2. Classification discipline

Every obligation in this document is assigned one of four workstream classes:

```text
INHERITED / CLOSED
    already decided upstream; consume exactly, do not debate again

CONCRETE DECISION
    genuinely global physical choice left for CP6-02 Constitution

VERTICAL-SPECIFIC
    exact business shape must wait for the relevant vertical

DIRECT-PROOF
    architecture is already decided and an actually materialized, non-speculative
    PostgreSQL artifact can be tested directly
```

A single Domain concept may carry multiple obligations with different classes. Therefore the “next-stage classification” in each entry classifies **remaining physical work**, not the already-CLOSED semantic owner.

---

## 3. Pressure vocabulary

### Material-state pressure

```text
NONE
    no independent material-state identity for this semantic family

CONDITIONAL
    only when consequence/history/addressability crosses the accepted threshold

REQUIRED
    the accepted semantics require exact materially applicable state where the
    canonical/consequential case exists
```

### History pressure

```text
NONE
LIGHTWEIGHT
MATERIAL
```

`MATERIAL` means historical reconstruction cannot truthfully be inferred from today's mutable state.

### PostgreSQL special-capability pressure

Special capabilities are **not activated by this matrix**.

```text
PostGIS   only where accepted spatial semantics/query needs justify it
FTS       derived search only
pg_trgm   bounded textual/fuzzy search only
pgvector  derived retrieval/ranking only
JSONB     LR-10/provider/raw/specialist bounded flexibility only
```

No special capability becomes canonical semantic authority.

---

## 4. Complete 57/57 Concrete Persistence Coverage Matrix

The entries below preserve the Whole-Logical disposition verbatim or in its latest superseding hardening, then add CP6 persistence-pressure classification.

### 01. Acknowledgement

- **Inherited Logical disposition:** LR-03 typed semantic act/relation; ScopedRecordRef only where independent addressability is material.
- **Concrete persistence family pressure:** typed semantic act/relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef on target state where consequence requires.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN ATTESTATION HISTORY MATTERS**.
- **Effective/world chronology pressure:** target/effect applicability when material.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted attestation chronology when material.
- **Reference Contract pressure:** strong: actor + target + exact material state/purpose.
- **Constraint / invariant pressure:** FK/eligibility/cardinality; state-binding integrity.
- **Transaction / concurrency pressure:** normally local; consequential state change uses expected-state on target, not on acknowledgement identity by default.
- **Provenance / governance pressure:** actor attribution + provenance; governance basis only when applicable.
- **Retention / redaction / tombstone pressure:** redaction/history continuity may matter for consequential attestations.
- **Query / access pressure:** current/historical acknowledgement by target state; never infer from delivery/read telemetry.
- **PostgreSQL capability pressure:** none intrinsic; search only as derived.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-05 later system proof; PSV-35 later selected-mapping smoke.
- **Dependency pressure:** Actor/ReferenceAddress/MaterialStateRef/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact qualified-record shape VERTICAL-SPECIFIC.

### 02. Activity

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef required when material state is consequential; ExternalRef conditional.
- **Material-state pressure:** **CONDITIONAL→REQUIRED AT CONSEQUENCE/HISTORY THRESHOLD**.
- **History pressure:** **MATERIAL FOR CONSEQUENTIAL INTENTION/EXECUTION HISTORY**.
- **Effective/world chronology pressure:** intended/effective applicability where material.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/corrected chronology where material.
- **Reference Contract pressure:** strong typed refs to plans/goals/schedule/resource/governance according to contracts.
- **Constraint / invariant pressure:** owner PK/FK/local lifecycle constraints; typed relation eligibility.
- **Transaction / concurrency pressure:** expected-state for consequential mutation; multi-owner transaction when coupled to Schedule/Allocation/etc.
- **Provenance / governance pressure:** authorship/provenance for consequential changes; Authority/Consent/Representation where governed.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; tombstone/history continuity.
- **Query / access pressure:** current state, historical state, schedule/actual comparison, dependencies/resources.
- **PostgreSQL capability pressure:** none intrinsic; FTS/trgm only if later text-search workload proves.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H06, WL-H07, WL-H09, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-01/02/03 later as applicable; PSV-35 later.
- **Dependency pressure:** Plan/Goal/Dependency/Schedule/Actual/Resource Requirement/Allocation/governance.
- **Remaining-work classification:** INHERITED/CLOSED family; ID/MAT/REF/TX decisions CP6-02; columns VERTICAL-SPECIFIC.

### 03. Actor

- **Inherited Logical disposition:** contextual agency role/capability; no ActorRef/native wrapper identity.
- **Concrete persistence family pressure:** contextual role over eligible ReferenceAddress targets.
- **Identity / addressability pressure:** no own address; uses address of actual actor-capable target; Principal remains separate.
- **Material-state pressure:** **NONE AS ACTOR ITSELF**.
- **History pressure:** **NONE AS WRAPPER; ACTION HISTORY BELONGS TO GOVERNED EFFECT/PROVENANCE**.
- **Effective/world chronology pressure:** action/effect time through containing record.
- **Recorded/learned/accepted chronology pressure:** recorded action/provenance chronology through containing record.
- **Reference Contract pressure:** strong role eligibility; specific actor-role relation preferred.
- **Constraint / invariant pressure:** eligibility/integrity in containing effect/relation.
- **Transaction / concurrency pressure:** inherits transaction of consequential effect.
- **Provenance / governance pressure:** critical: actual Actor must remain distinct from represented party and Principal.
- **Retention / redaction / tombstone pressure:** no Actor tombstone; underlying identity retention governs.
- **Query / access pressure:** who actually acted/recorded/requested/confirmed/etc.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R06, PG-R09.
- **PSV carry-forward:** PSV-05 later; PSV-35 later.
- **Dependency pressure:** Person/Collective/system identity, Principal, Representation, Authority, Provenance.
- **Remaining-work classification:** INHERITED/CLOSED; no wrapper implementation allowed.

### 04. Actual

- **Inherited Logical disposition:** LR-06 realization + LR-02 dependent contextual semantic record; ScopedRecordRef when addressable.
- **Concrete persistence family pressure:** dependent realization family.
- **Identity / addressability pressure:** ScopedRecordRef conditional/likely for material canonical Actual; MaterialStateRef for corrections; ExternalRef conditional source mapping.
- **Material-state pressure:** **REQUIRED FOR CANONICAL MATERIAL ACTUAL STATE/CORRECTIONS**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** world/effective realization time central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/corrected chronology central when sources conflict/correct.
- **Reference Contract pressure:** strong target expectation binding; does not exist as generic reality.
- **Constraint / invariant pressure:** FK/eligibility; unknown vs known non-realization; correction lineage.
- **Transaction / concurrency pressure:** expected-state for consequential correction; may participate in multi-owner consistency.
- **Provenance / governance pressure:** establishment basis, source/provenance, Actor/authority where applicable.
- **Retention / redaction / tombstone pressure:** redaction must preserve honest historical existence where permitted.
- **Query / access pressure:** planned-vs-actual, known non-realization vs unknown, historical corrections.
- **PostgreSQL capability pressure:** none intrinsic; high-volume raw telemetry belongs specialist/source path.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later; PSV-05 if disclosure.
- **Dependency pressure:** Activity/Event/Occurrence/Schedule/Session/Outcome/Observation/Evidence/Reconciliation.
- **Remaining-work classification:** INHERITED/CLOSED family; MAT/TIM/MISS CP6-02; exact schema VERTICAL-SPECIFIC.

### 05. Agreement

- **Inherited Logical disposition:** LR-02 n-ary contextual record + typed party assent + MaterialStateRef terms binding.
- **Concrete persistence family pressure:** qualified n-ary governance/context family.
- **Identity / addressability pressure:** ScopedRecordRef expected for material Agreement; MaterialStateRef required for terms/state; NativeRef/ScopedRecordRef for parties by contract.
- **Material-state pressure:** **REQUIRED**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** effective/applicable terms period where relevant.
- **Recorded/learned/accepted chronology pressure:** assent/acceptance/amendment chronology required.
- **Reference Contract pressure:** very strong: N parties must bind to same owned terms MaterialStateRef.
- **Constraint / invariant pressure:** n-ary cardinality, eligible party roles, exact common terms-state integrity; no pairwise approximation.
- **Transaction / concurrency pressure:** expected-state for amendment; multi-owner/assent atomicity where invariants require.
- **Provenance / governance pressure:** party Actor/Representation/Authority/Consent basis and provenance as applicable.
- **Retention / redaction / tombstone pressure:** historical terms/assent continuity; redaction cannot fabricate no agreement.
- **Query / access pressure:** current agreement, terms at T, which parties assented to exact state.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H01, WL-H02, WL-H04, WL-H05, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later; PSV-05 where disclosure.
- **Dependency pressure:** MaterialStateRef/Proposal or ContentArtifact or Agreement-owned terms state/party identities/Authority/Consent/Representation.
- **Remaining-work classification:** INHERITED/CLOSED topology thesis; exact n-ary relational design VERTICAL-SPECIFIC after CP6-02 primitives.

### 06. Asset

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE OWNERSHIP/LOCATION/STATE/HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective state where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/corrected chronology where relevant.
- **Reference Contract pressure:** typed role refs; Resource use does not create ResourceRef.
- **Constraint / invariant pressure:** PK/FK; owner-specific invariants; provider identifiers not identity.
- **Transaction / concurrency pressure:** expected-state for consequential changes; multi-owner when ownership/possession/allocation coupled.
- **Provenance / governance pressure:** provenance on identity reconciliation/material changes.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; tombstone/redaction continuity.
- **Query / access pressure:** current owner/possessor/location/material state; historical relations.
- **PostgreSQL capability pressure:** none intrinsic; trigram/FTS only workload-driven.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H08, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R10.
- **PSV carry-forward:** PSV-01/02/03/35 later.
- **Dependency pressure:** Ownership/Possession/Resource/Allocation/Observation/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; ID/MAT/REF CP6-02; exact schema VERTICAL-SPECIFIC.

### 07. Authority

- **Inherited Logical disposition:** LR-03/LR-02 bounded governance relation/state + LR-05 basis + LR-08 effective projection.
- **Concrete persistence family pressure:** specific governance relation + policy basis + derived effective projection.
- **Identity / addressability pressure:** ScopedRecordRef conditional for material grant/state; MaterialStateRef required when action-time basis consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL BASIS**.
- **History pressure:** **MATERIAL FOR GRANTS/REVOCATIONS USED BY EFFECTS**.
- **Effective/world chronology pressure:** effective/applicability time central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revoked chronology central.
- **Reference Contract pressure:** strong target/action/scope/purpose/actor eligibility.
- **Constraint / invariant pressure:** typed scope/action constraints; grant/revocation state integrity.
- **Transaction / concurrency pressure:** expected-state on consequential change; delayed effect revalidation; multi-owner governance/effect coupling.
- **Provenance / governance pressure:** critical; must reconstruct basis separately from technical AuthZ.
- **Retention / redaction / tombstone pressure:** history/tombstone/redaction constrained by audit/privacy.
- **Query / access pressure:** effective authority now vs authority basis at effect time.
- **PostgreSQL capability pressure:** none intrinsic; derived auth projection rebuildable.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H09, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05 later; PSV-23 later durable execution; PSV-35 later.
- **Dependency pressure:** Actor/Representation/Consent/Agreement/Membership/policies/Principal projection.
- **Remaining-work classification:** INHERITED/CLOSED semantics; PROV/TX/MAT constitution CP6-02; exact grants VERTICAL-SPECIFIC.

### 08. Availability

- **Inherited Logical disposition:** LR-05 baseline/rule + LR-02 material override/fact + LR-08 effective projection.
- **Concrete persistence family pressure:** rule/spec + bounded override + derived effective projection.
- **Identity / addressability pressure:** ScopedRecordRef only for material override; MaterialStateRef where consequential historical basis needed.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL ONLY FOR CONSEQUENTIAL RULES/OVERRIDES OR RELIED-ON HISTORICAL BASIS**.
- **Effective/world chronology pressure:** effective interval/frame central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted chronology when overrides/history material.
- **Reference Contract pressure:** resource/provider target contract.
- **Constraint / invariant pressure:** range/rule constraints; do not canonicalize free-slot grid.
- **Transaction / concurrency pressure:** expected-state if editing material rule/override; concurrency with capacity claims only in specific vertical.
- **Provenance / governance pressure:** provenance for source/provider overrides; governance if shared.
- **Retention / redaction / tombstone pressure:** retention of material rule/override history as required.
- **Query / access pressure:** effective availability current/historical; explain basis.
- **PostgreSQL capability pressure:** range/GiST likely vertical-specific; PostGIS only if geo-specific availability; no intrinsic vector/JSONB.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H08, WL-H09, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/09 later; PSV-35 later.
- **Dependency pressure:** Resource/Capacity/Schedule/Temporal values/provider free-busy.
- **Remaining-work classification:** INHERITED/CLOSED family; TIM/TYP/IDX CP6-02; exact rule/override schema VERTICAL-SPECIFIC.

### 09. Capacity

- **Inherited Logical disposition:** contextual capability: LR-04/LR-05/LR-02 as applicable + LR-08 effective remaining-capacity projection.
- **Concrete persistence family pressure:** typed capability/value/rule + bounded material context + derived projection.
- **Identity / addressability pressure:** no CapacityRef; ScopedRecordRef only if bounded material record justified; MaterialStateRef if consequential.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL ONLY WHERE STATE/POLICY MATERIALLY GOVERNS CLAIMS/ALLOCATIONS**.
- **Effective/world chronology pressure:** effective time/interval where applicable.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted history where consequential.
- **Reference Contract pressure:** provider/resource context explicit.
- **Constraint / invariant pressure:** typed dimensions, nonnegative/compatibility invariants owner-specific; no universal scalar.
- **Transaction / concurrency pressure:** write-skew risk around competing claims; may require exclusion/locks/SERIALIZABLE by invariant.
- **Provenance / governance pressure:** provenance/governance when capacity basis controls consequential allocation.
- **Retention / redaction / tombstone pressure:** retention only for material bases/effects.
- **Query / access pressure:** available/free/sufficient/claimed remain distinct; historical basis for decisions.
- **PostgreSQL capability pressure:** range/index pressure likely; no intrinsic JSONB/vector.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R07.
- **PSV carry-forward:** PSV-04 later capacity/backpressure; PSV-35 later.
- **Dependency pressure:** Resource/Availability/Capacity Claim/Schedule/Allocation/Quantity.
- **Remaining-work classification:** INHERITED/CLOSED semantics; CON/TX/TYP CP6-02; dimensions VERTICAL-SPECIFIC.

### 10. Collective

- **Inherited Logical disposition:** LR-01 native identity-bearing record; identity independent from current member set.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE COLLECTIVE STATE/GOVERNANCE CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective lifecycle where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/corrected chronology.
- **Reference Contract pressure:** typed Membership/Agreement/Authority/etc.; member set not identity.
- **Constraint / invariant pressure:** PK/FK; no identity-by-membership; relation cardinality owner-specific.
- **Transaction / concurrency pressure:** expected-state for consequential state; multi-owner with governance/relations.
- **Provenance / governance pressure:** collective action must preserve agency basis; member action != collective action.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; tombstone continuity.
- **Query / access pressure:** collective current/historical identity and membership/governance separated.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R06, PG-R10.
- **PSV carry-forward:** PSV-01/02/03/35 later.
- **Dependency pressure:** Membership/Agreement/Authority/Actor/Representation.
- **Remaining-work classification:** INHERITED/CLOSED family; exact owner schema VERTICAL-SPECIFIC.

### 11. Conditional Policy

- **Inherited Logical disposition:** LR-05 typed policy/specification.
- **Concrete persistence family pressure:** owner-specific rule/specification family.
- **Identity / addressability pressure:** ScopedRecordRef/MaterialStateRef only when material independent lifecycle/history is needed.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN GOVERNING CONSEQUENTIAL EFFECTS**.
- **Effective/world chronology pressure:** effective applicability/activation basis.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/superseded chronology when material.
- **Reference Contract pressure:** typed targets/facets/effects; not Recurrence.
- **Constraint / invariant pressure:** rule structural validity and scope; no generic Rule payload.
- **Transaction / concurrency pressure:** expected-state on policy revision if consequential; effect-time revalidation.
- **Provenance / governance pressure:** provenance/authorship/Authority to establish/change policy where applicable.
- **Retention / redaction / tombstone pressure:** history of governing versions; redaction policy-specific.
- **Query / access pressure:** which policy state governed effect at T; activation != effect success.
- **PostgreSQL capability pressure:** no intrinsic special capability; JSONB forbidden for required semantics.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R06, PG-R07.
- **PSV carry-forward:** PSV-23 later for delayed effects; PSV-35 later.
- **Dependency pressure:** MaterialStateRef/Authority/Consent/target owners/Trigger basis.
- **Remaining-work classification:** INHERITED/CLOSED semantics; LR-05 constitution CP6-02; DSL/shape VERTICAL-SPECIFIC.

### 12. Confirmation

- **Inherited Logical disposition:** LR-03 typed semantic act/relation; ScopedRecordRef where addressed.
- **Concrete persistence family pressure:** typed attestation relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef on confirmed target required when consequence matters.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN ATTESTATION IS CONSEQUENTIAL/ADDRESSED**.
- **Effective/world chronology pressure:** target applicability where relevant.
- **Recorded/learned/accepted chronology pressure:** confirmation recorded/accepted chronology.
- **Reference Contract pressure:** actor + exact target state + purpose/context.
- **Constraint / invariant pressure:** eligibility/cardinality/state-binding integrity.
- **Transaction / concurrency pressure:** usually local; consequential changes governed by target expected-state.
- **Provenance / governance pressure:** actor/provenance central.
- **Retention / redaction / tombstone pressure:** retention/redaction may preserve bounded historical attestation.
- **Query / access pressure:** confirmations by exact target state; prior confirmation must not float to new state.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actor/MaterialStateRef/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact qualified shape VERTICAL-SPECIFIC.

### 13. Consent

- **Inherited Logical disposition:** LR-03 scoped relation; LR-02 + MaterialStateRef when consequential.
- **Concrete persistence family pressure:** specific governance relation + material contextual state.
- **Identity / addressability pressure:** ScopedRecordRef expected when consequential; MaterialStateRef required for exact consent state/terms/target.
- **Material-state pressure:** **REQUIRED WHEN USED AS CONSEQUENTIAL GOVERNANCE BASIS**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** effective/applicable period central.
- **Recorded/learned/accepted chronology pressure:** recorded/granted/withdrawn/revoked chronology central.
- **Reference Contract pressure:** giver/action/use/exposure/target/scope/purpose/context contract.
- **Constraint / invariant pressure:** typed scope, target state, withdrawal/supersession integrity.
- **Transaction / concurrency pressure:** expected-state for mutation; delayed effects must not use stale consent; multi-owner with governed effect.
- **Provenance / governance pressure:** critical actor/provenance/authority boundaries.
- **Retention / redaction / tombstone pressure:** withdrawal preserves truthful historical consented actions while limiting future applicability.
- **Query / access pressure:** consent applicable now and at effect time, exact state/terms.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05 later; PSV-13 offline later; PSV-23 durable execution later; PSV-35 later.
- **Dependency pressure:** Actor/Authority/Agreement/Visibility/Representation/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED semantics; PROV/MAT/TX CP6-02; exact schema VERTICAL-SPECIFIC.

### 14. Content Artifact

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional/strong for materially revised content; ExternalRef/R2 object mapping conditional.
- **Material-state pressure:** **CONDITIONAL→REQUIRED WHEN EXACT CONTENT STATE MATTERS**.
- **History pressure:** **MATERIAL FOR REVISIONS/SOURCE LINEAGE**.
- **Effective/world chronology pressure:** effective applicability less universal; content-version applicability where needed.
- **Recorded/learned/accepted chronology pressure:** recorded/imported/corrected chronology important.
- **Reference Contract pressure:** typed links to bytes/source/evidence/proposals/etc.
- **Constraint / invariant pressure:** identity continuity independent of blob/provider; content-state integrity.
- **Transaction / concurrency pressure:** expected-state for consequential revision; object-storage side effects staged/outbox later.
- **Provenance / governance pressure:** source/provenance strong; authorship may matter.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; payload/object deletion vs metadata tombstone.
- **Query / access pressure:** current/historical artifact state, source/provider, search.
- **PostgreSQL capability pressure:** FTS/trgm likely derived search pressure; pgvector only derived; JSONB only provider/LR-10; R2 bytes separate.
- **Whole hardening applicability:** WL-H03, WL-H05, WL-H07, WL-H08, WL-H09, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-06..10 later search; PSV-29..34 object/backup later; PSV-35/37 later.
- **Dependency pressure:** Provenance/Evidence/ExternalRef/R2 bytes/search projections.
- **Remaining-work classification:** INHERITED/CLOSED family; search/object integration stages later; exact business schema VERTICAL-SPECIFIC.

### 15. Contribution

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific qualified relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material attribution/history; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE ATTRIBUTION/HISTORY MATTERS**.
- **Effective/world chronology pressure:** effective realized context.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted chronology.
- **Reference Contract pressure:** actor + realized context + contribution semantics.
- **Constraint / invariant pressure:** typed endpoints/context; must not infer from Participation/assignment.
- **Transaction / concurrency pressure:** normally local; multi-owner if effect changes multiple owners.
- **Provenance / governance pressure:** actor/provenance important; governance if shared.
- **Retention / redaction / tombstone pressure:** retention/privacy of attribution where needed.
- **Query / access pressure:** who materially contributed to realized context; distinguish attendance/assignment.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later; PSV-05 if disclosure.
- **Dependency pressure:** Actor/Actual/Session/Participation/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation shape VERTICAL-SPECIFIC.

### 16. Coordination Stewardship

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific governance/coordination relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE TRANSFER/HISTORY/SCOPE CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective applicability.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/transferred chronology.
- **Reference Contract pressure:** steward + bounded coordination context.
- **Constraint / invariant pressure:** typed relation; no collapse with Responsibility/Authority.
- **Transaction / concurrency pressure:** expected-state if transferring consequential stewardship; multi-owner only if coupled effect.
- **Provenance / governance pressure:** provenance/governance where establishment/transfer matters.
- **Retention / redaction / tombstone pressure:** historical relation continuity.
- **Query / access pressure:** who bore coordination burden at T; current steward.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actor/Responsibility/Participation/Authority/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 17. Criterion

- **Inherited Logical disposition:** LR-05 rule/specification; LR-02 material record only where justified.
- **Concrete persistence family pressure:** owner-specific rule/specification family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef required when consequential Evaluation binds exact criterion state.
- **Material-state pressure:** **CONDITIONAL→REQUIRED WHEN RELIED ON CONSEQUENTIALly**.
- **History pressure:** **MATERIAL FOR REUSABLE/VERSIONED CONSEQUENTIAL CRITERIA**.
- **Effective/world chronology pressure:** effective applicability where criterion changes over time.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/superseded chronology when material.
- **Reference Contract pressure:** typed target/facet/value semantics.
- **Constraint / invariant pressure:** rule validity/type constraints; no universal Rule root.
- **Transaction / concurrency pressure:** expected-state for material criterion revision.
- **Provenance / governance pressure:** provenance/authorship when criterion established/changed.
- **Retention / redaction / tombstone pressure:** history required where past Evaluation depends on it.
- **Query / access pressure:** current criterion; criterion state used by historical Evaluation.
- **PostgreSQL capability pressure:** no intrinsic; JSONB forbidden for required semantic predicate by convenience.
- **Whole hardening applicability:** WL-H02, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07.
- **PSV carry-forward:** PSV-09 later projection basis; PSV-35 later.
- **Dependency pressure:** Evaluation/MaterialStateRef/Evidence/typed values.
- **Remaining-work classification:** INHERITED/CLOSED semantics; rule representation constitution CP6-02; exact DSL VERTICAL-SPECIFIC.

### 18. Evaluation

- **Inherited Logical disposition:** LR-08 by default; LR-02 historical snapshot where consequential.
- **Concrete persistence family pressure:** derived projection/process-result; bounded material snapshot when consequential.
- **Identity / addressability pressure:** no native address; ScopedRecordRef for materialized consequential evaluation; MaterialStateRefs for inputs/rules.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL SNAPSHOT**.
- **History pressure:** **MATERIAL ONLY WHEN HISTORICAL CONSEQUENCE/REPRODUCIBILITY REQUIRES**.
- **Effective/world chronology pressure:** world/effective target window/context.
- **Recorded/learned/accepted chronology pressure:** recorded/computed/accepted chronology for snapshot.
- **Reference Contract pressure:** must bind target/criterion/evidence source states when material.
- **Constraint / invariant pressure:** input-state eligibility; result typing; snapshot integrity.
- **Transaction / concurrency pressure:** consequential use requires freshness revalidation or bound snapshot; may race with source updates.
- **Provenance / governance pressure:** evaluator/model/provenance where material; governance/visibility as applicable.
- **Retention / redaction / tombstone pressure:** retention of consequential snapshots/input basis only as policy requires.
- **Query / access pressure:** recompute current vs reproduce historical evaluation.
- **PostgreSQL capability pressure:** pgvector/FTS only as derived inputs depending vertical; JSONB bounded computation metadata only.
- **Whole hardening applicability:** WL-H03, WL-H05, WL-H09, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/08/09/35/37 later as capabilities activate.
- **Dependency pressure:** Criterion/Evidence/MaterialStateRef/Provenance/target owner.
- **Remaining-work classification:** INHERITED/CLOSED semantics; projection freshness constitution CP6-02; material snapshot VERTICAL-SPECIFIC.

### 19. Decision

- **Inherited Logical disposition:** LR-02 conditionally materialized semantic record.
- **Concrete persistence family pressure:** dependent semantic-act family.
- **Identity / addressability pressure:** ScopedRecordRef when materialized; MaterialStateRef for target state/decision state where consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED WHEN INDEPENDENT LIFECYCLE/HISTORY/CONSEQUENCE MATTERS**.
- **History pressure:** **MATERIAL WHERE MATERIALIZED/CONSEQUENTIAL**.
- **Effective/world chronology pressure:** decision applicability/effect context where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/superseded chronology.
- **Reference Contract pressure:** alternatives/question/target exact state contract.
- **Constraint / invariant pressure:** state-binding; decision != effect; no generic approval flag.
- **Transaction / concurrency pressure:** expected-state for target effect; multi-owner if decision triggers coupled effects.
- **Provenance / governance pressure:** actor/authority/rationale/provenance important.
- **Retention / redaction / tombstone pressure:** retention/history of decision even if no target mutation.
- **Query / access pressure:** decisions with/without effect; exact target version decided.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H06, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later; PSV-43 solver later.
- **Dependency pressure:** Proposal/Request/MaterialStateRef/Authority/Actor/Effect owners.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact materialization VERTICAL-SPECIFIC.

### 20. Dependency

- **Inherited Logical disposition:** LR-03 directional typed contingency.
- **Concrete persistence family pressure:** specific typed contingency relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when history/addressability; MaterialStateRef at endpoints/facets when consequence state-specific.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE DEFINITION/HISTORY GOVERNS EXECUTION**.
- **Effective/world chronology pressure:** effective applicability where dependency changes.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted chronology where material.
- **Reference Contract pressure:** strong endpoint + facet/state/result/transition condition contract.
- **Constraint / invariant pressure:** direction/eligibility; no universal DAG/cycle prohibition; derived blocked/satisfied not canonical.
- **Transaction / concurrency pressure:** expected-state if consequential dependency change; may affect eligibility under concurrent prerequisite changes.
- **Provenance / governance pressure:** provenance/governance if established/shared consequentially.
- **Retention / redaction / tombstone pressure:** history where past execution depended on exact dependency state.
- **Query / access pressure:** current derived blocked/eligible and historical applicable dependency.
- **PostgreSQL capability pressure:** recursive CTE potentially vertical-specific; no graph server required.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07.
- **PSV carry-forward:** PSV-09/35 later.
- **Dependency pressure:** ReferenceAddress/MaterialStateRef/Plan/Activity/Milestone.
- **Remaining-work classification:** INHERITED/CLOSED semantics; relation/facet doctrine CP6-02; exact schema VERTICAL-SPECIFIC.

### 21. Event

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef often conditional for calendar/provider.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL FOR CONSEQUENTIAL EVENT STATE/DISPOSITION**.
- **Effective/world chronology pressure:** expected event applicability + schedule distinct.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/corrected chronology.
- **Reference Contract pressure:** typed Schedule/Occurrence/Participation/etc.; Event != Schedule.
- **Constraint / invariant pressure:** owner lifecycle constraints; provider state separate.
- **Transaction / concurrency pressure:** expected-state for consequential changes; multi-owner with schedule/participation/governance.
- **Provenance / governance pressure:** provenance/actor/governance where shared/consequential.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; cancellation != deletion; history continuity.
- **Query / access pressure:** event identity, current schedule, actual occurrence, participants.
- **PostgreSQL capability pressure:** FTS/trgm workload-driven; no intrinsic vector/JSONB.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later; offline/provider PSV later if activated.
- **Dependency pressure:** Schedule/Occurrence/Session/Actual/Participation/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; exact schema VERTICAL-SPECIFIC.

### 22. Evidence

- **Inherited Logical disposition:** LR-03 evaluative-use relationship; source MaterialStateRef where required.
- **Concrete persistence family pressure:** typed evaluative-use relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; source MaterialStateRef required when exact source state matters.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL EVALUATION**.
- **History pressure:** **MATERIAL WHERE EXPLICIT EVIDENCE USE/HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** source/target effective context where material.
- **Recorded/learned/accepted chronology pressure:** recorded/use chronology where material.
- **Reference Contract pressure:** source state + evaluative target/context + role (support/contradict/qualify/input).
- **Constraint / invariant pressure:** typed source/target eligibility; no Evidence=truth.
- **Transaction / concurrency pressure:** normally local; consequential evaluation freshness/input-binding.
- **Provenance / governance pressure:** source/provenance central; visibility especially important.
- **Retention / redaction / tombstone pressure:** redaction may preserve bounded historical use without payload.
- **Query / access pressure:** all contexts where source used; historical evaluation basis.
- **PostgreSQL capability pressure:** search/vector may find candidates but do not establish Evidence; derived only.
- **Whole hardening applicability:** WL-H03, WL-H04, WL-H09, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05..10 later as search/disclosure active; PSV-35.
- **Dependency pressure:** MaterialStateRef/Observation/ContentArtifact/Evaluation/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 23. Goal

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef material for consequential goal state/history.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR MATERIAL LIFECYCLE/STATE**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** effective pursuit/applicability where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology.
- **Reference Contract pressure:** typed links to Possibility/Plan/Evaluation etc.
- **Constraint / invariant pressure:** owner-specific lifecycle; no universal status; identity not retyped from Possibility.
- **Transaction / concurrency pressure:** expected-state for consequential changes; multi-owner with plan/relations when atomic.
- **Provenance / governance pressure:** authorship/provenance; governance if shared.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; retirement/abandonment preserves history.
- **Query / access pressure:** goal current state, prior states, plans, progress/evaluation.
- **PostgreSQL capability pressure:** FTS/trgm maybe workload-driven; vector only derived recommendation/search.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later.
- **Dependency pressure:** Possibility/Plan/Evaluation/Dependency/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED family; exact columns/lifecycle VERTICAL-SPECIFIC.

### 24. Interpersonal Relationship

- **Inherited Logical disposition:** LR-03 bounded Person-to-Person relation family.
- **Concrete persistence family pressure:** specific typed relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material state/history; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL IF HISTORY/CONTEXT CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective applicability where relation changes.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/corrected chronology.
- **Reference Contract pressure:** Person endpoints, relationship-kind-specific inverse/symmetry rules.
- **Constraint / invariant pressure:** typed endpoints; no universal symmetry/transitivity.
- **Transaction / concurrency pressure:** expected-state for consequential relation changes; normally local.
- **Provenance / governance pressure:** provenance; must not imply Authority/Visibility/Consent.
- **Retention / redaction / tombstone pressure:** privacy/redaction highly relevant; historical truth where retained.
- **Query / access pressure:** relationship current/history without deriving governance.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05 later; PSV-35.
- **Dependency pressure:** Person/Visibility/Authority/Consent/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 25. Living Referent

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef conditional (chip/provider/etc.).
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE IDENTITY/STATE/CARE/HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective state where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/corrected chronology.
- **Reference Contract pressure:** typed subject/resource/care relations; != Person/Asset.
- **Constraint / invariant pressure:** owner-specific identity/invariants; aliases/provider IDs not identity.
- **Transaction / concurrency pressure:** expected-state for consequential updates; multi-owner relations as needed.
- **Provenance / governance pressure:** provenance on reconciliation/material state.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; tombstone/redaction continuity.
- **Query / access pressure:** same referent across changed caregiver/location/name; history.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H08, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R10.
- **PSV carry-forward:** PSV-01/02/03/35 later.
- **Dependency pressure:** Reconciliation/Observation/Subject/Resource/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; exact schema VERTICAL-SPECIFIC.

### 26. Membership

- **Inherited Logical disposition:** LR-03 specific typed relation; no automatic governance consequence.
- **Concrete persistence family pressure:** specific typed relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material relation state/history; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE SCOPE/HISTORY/GOVERNANCE CONSEQUENCE**.
- **Effective/world chronology pressure:** effective membership period central when material.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/transferred/revoked chronology.
- **Reference Contract pressure:** member + Collective exact roles; provider security groups only evidence/projection.
- **Constraint / invariant pressure:** typed endpoints/cardinality; no implication to Participation/Authority/etc.
- **Transaction / concurrency pressure:** expected-state for material relation change; multi-owner if coupled governance effect.
- **Provenance / governance pressure:** provenance; governance basis for establishment where needed.
- **Retention / redaction / tombstone pressure:** historical membership may be sensitive; tombstone/redaction as policy.
- **Query / access pressure:** who was member at T; do not infer collective action/authority.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/35 later.
- **Dependency pressure:** Collective/Person or eligible member identities/Authority/Visibility.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 27. Milestone

- **Inherited Logical disposition:** LR-02 dependent semantic record.
- **Concrete persistence family pressure:** dependent contextual intention family.
- **Identity / addressability pressure:** ScopedRecordRef where material/addressable; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN ATTAINMENT CRITERIA/HISTORY MATTERS**.
- **Effective/world chronology pressure:** target/effective date only where semantically defined.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology where material.
- **Reference Contract pressure:** scoped to Goal/Plan context; Criterion/Evaluation state may establish attainment.
- **Constraint / invariant pressure:** scope/cardinality; date passage must not imply attainment.
- **Transaction / concurrency pressure:** expected-state for consequential updates; normally scoped transaction.
- **Provenance / governance pressure:** provenance/governance where shared/consequential.
- **Retention / redaction / tombstone pressure:** history of definition/attainment basis if material.
- **Query / access pressure:** pending/attained on evaluative basis; historical definitions.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Goal/Plan/Criterion/Evaluation/Dependency.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact scoped record VERTICAL-SPECIFIC.

### 28. Monetary Amount

- **Inherited Logical disposition:** LR-04 value semantics.
- **Concrete persistence family pressure:** typed monetary value family embedded/owner-bound.
- **Identity / addressability pressure:** no independent NativeRef; state address via containing owner/material state.
- **Material-state pressure:** **NONE INDEPENDENTLY; INHERITED THROUGH OWNER**.
- **History pressure:** **INHERITED THROUGH CONTAINING OWNER**.
- **Effective/world chronology pressure:** effective time relevant to FX basis, not amount identity universally.
- **Recorded/learned/accepted chronology pressure:** recorded/source chronology via containing owner/provenance.
- **Reference Contract pressure:** currency + amount semantics distinct from Quantity.
- **Constraint / invariant pressure:** precision/currency validity; avoid float; exact CP6-02 type doctrine.
- **Transaction / concurrency pressure:** none independently.
- **Provenance / governance pressure:** provenance for FX conversion/source if derived.
- **Retention / redaction / tombstone pressure:** via containing owner.
- **Query / access pressure:** exact source amount vs converted derived amount.
- **PostgreSQL capability pressure:** none intrinsic; no JSONB required.
- **Whole hardening applicability:** WL-H04.
- **PostgreSQL risk applicability:** PG-R03 only through containing history.
- **PSV carry-forward:** PSV-35 later through representative corpus.
- **Dependency pressure:** Containing owner/FX basis/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED value semantics; SQL numeric/currency doctrine CP6-02.

### 29. Observation

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native observational owner family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef required for correction of same observation; ExternalRef conditional.
- **Material-state pressure:** **REQUIRED FOR MATERIAL CORRECTION/HISTORY**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** observed/effective time central.
- **Recorded/learned/accepted chronology pressure:** recorded/learned/accepted/corrected chronology central.
- **Reference Contract pressure:** Subject Reference Contract strong; source/provider separate.
- **Constraint / invariant pressure:** owner identity not derived from subject+property+time+value; typed observation shape.
- **Transaction / concurrency pressure:** expected-state for correction; concurrent correction conflict where consequential.
- **Provenance / governance pressure:** observer/recorder/source/provenance critical.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; payload redaction/history continuity as policy.
- **Query / access pressure:** observation state at T, corrections, source, subject; point != ongoing condition.
- **PostgreSQL capability pressure:** high-volume telemetry may use specialist representation; vector/FTS only derived.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H08, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later; search PSV if activated.
- **Dependency pressure:** Subject/Provenance/Evidence/Reconciliation/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; MAT/TIM/PROV CP6-02; observation schema VERTICAL-SPECIFIC.

### 30. Occurrence

- **Inherited Logical disposition:** LR-01 native identity once one canonical individual Occurrence is semantically distinguished; lazy/non-row derivation allowed before that.
- **Concrete persistence family pressure:** native expected-instance family with lazy derivation boundary.
- **Identity / addressability pressure:** NativeRef once distinguished; pre-materialization bounded locator is NOT ReferenceAddress; MaterialStateRef to governing source state required where historical meaning depends.
- **Material-state pressure:** **REQUIRED ONCE MATERIAL/DISTINGUISHED HISTORY EXISTS**.
- **History pressure:** **MATERIAL FOR DISTINGUISHED/EXCEPTION/SCHEDULED/ACTUAL INSTANCES**.
- **Effective/world chronology pressure:** expected instance temporal semantics central.
- **Recorded/learned/accepted chronology pressure:** materialization/recorded/corrected chronology where applicable.
- **Reference Contract pressure:** source + governing MaterialStateRef + recurrence-family generation context.
- **Constraint / invariant pressure:** identity continuity across reschedule/provider churn; no fake ordinals for unordered quota.
- **Transaction / concurrency pressure:** concurrency around materialization/idempotent establishment must avoid duplicate semantic instance; exact mechanism CP6-02/vertical.
- **Provenance / governance pressure:** source/provenance/provider mapping where relevant.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; tombstone for material historical occurrence where permitted.
- **Query / access pressure:** which occurrence after move; source state that generated it; virtual vs material.
- **PostgreSQL capability pressure:** range/time index likely; no generic JSONB; recurrence-family indexing vertical-specific.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H08, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R07, PG-R08, PG-R10.
- **PSV carry-forward:** PSV-35 later; offline/provider PSV later if activated.
- **Dependency pressure:** Routine/Event/Recurrence/MaterialStateRef/Schedule/Actual/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED semantic boundary; locator/key/materialization exact design VERTICAL-SPECIFIC after ID/REF constitution.

### 31. Outcome

- **Inherited Logical disposition:** LR-06 result; LR-02 when materially persistent/addressable.
- **Concrete persistence family pressure:** dependent contextual result family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef conditional for corrections.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN PERSISTENT/CONSEQUENTIAL**.
- **Effective/world chronology pressure:** result applicability/effective time context-specific.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/corrected chronology where material.
- **Reference Contract pressure:** bound to specific Actual realization; no universal enum.
- **Constraint / invariant pressure:** typed result semantics; absence != negative outcome.
- **Transaction / concurrency pressure:** expected-state for consequential correction.
- **Provenance / governance pressure:** provenance/evidence establishment where needed.
- **Retention / redaction / tombstone pressure:** historical result continuity/redaction as policy.
- **Query / access pressure:** result for exact Actual; distinguish no outcome/partial/etc.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actual/Evidence/Observation/Provenance.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact result shape VERTICAL-SPECIFIC.

### 32. Ownership

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific typed relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material/history; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE TRANSFER/HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective ownership period central when material.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/transferred chronology.
- **Reference Contract pressure:** owner + owned target; distinct from Possession/Authority.
- **Constraint / invariant pressure:** typed endpoints; transfer/non-overlap rules owner-specific not universal.
- **Transaction / concurrency pressure:** expected-state for transfer; multi-owner asset/relation consistency may require transaction.
- **Provenance / governance pressure:** provenance/authority for transfer where applicable.
- **Retention / redaction / tombstone pressure:** historical ownership may be retained/redacted per policy.
- **Query / access pressure:** who owned at T vs possessed at T.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Person/Collective/Asset or eligible targets/Possession/Authority.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 33. Participation

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific typed relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when response/history/scope material; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE INVITATION/RESPONSE/HISTORY MATTERS**.
- **Effective/world chronology pressure:** effective intended participation period/context.
- **Recorded/learned/accepted chronology pressure:** recorded/invited/responded chronology.
- **Reference Contract pressure:** participant + Event/Activity/etc.; invited/accepted/intended/actual distinct.
- **Constraint / invariant pressure:** typed states/cardinality; no inference of Actual participation.
- **Transaction / concurrency pressure:** expected-state for response changes; multi-owner only when coupled effect.
- **Provenance / governance pressure:** actor/provenance; governance if shared.
- **Retention / redaction / tombstone pressure:** privacy/history as policy.
- **Query / access pressure:** invited/accepted/intended vs actual participation.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/35 later.
- **Dependency pressure:** Person/Collective/Event/Activity/Actual/Contribution.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 34. Person

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef conditional; Account/Principal remain separate.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL FOR CONSEQUENTIAL PERSON-OWNED STATE/HISTORY**.
- **Effective/world chronology pressure:** effective state context-specific.
- **Recorded/learned/accepted chronology pressure:** recorded/learned/corrected chronology where material.
- **Reference Contract pressure:** broad typed role/subject/governance refs; no Person=Account/Actor.
- **Constraint / invariant pressure:** PK/FK; identity reconciliation; aliases/contact/provider IDs not identity.
- **Transaction / concurrency pressure:** expected-state for consequential changes; multi-owner with Account mappings/relations as needed.
- **Provenance / governance pressure:** authorship/identity reconciliation/governance highly relevant.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; privacy/redaction/tombstone critical.
- **Query / access pressure:** same person across accounts/providers/roles; historical reconciliation.
- **PostgreSQL capability pressure:** FTS/trgm for name search only if justified; vector only derived; JSONB only LR-10.
- **Whole hardening applicability:** WL-H03, WL-H04, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-01/02/03/05/35 later.
- **Dependency pressure:** Account/Principal mappings, Actor/Subject/Resource roles, Reconciliation, governance relations.
- **Remaining-work classification:** INHERITED/CLOSED family; ID/REF/MAT/LIFE CP6-02; exact person schema VERTICAL-SPECIFIC.

### 35. Place

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family with spatial pressure.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional; ExternalRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE PLACE DEFINITION/ADDRESS/GEOMETRY CORRECTIONS MATTER**.
- **Effective/world chronology pressure:** effective validity of address/geometry where material.
- **Recorded/learned/accepted chronology pressure:** recorded/corrected chronology where material.
- **Reference Contract pressure:** typed refs; coordinates/address/provider IDs not identity.
- **Constraint / invariant pressure:** identity continuity independent of coordinate correction; spatial validity owner-specific.
- **Transaction / concurrency pressure:** expected-state for consequential corrections.
- **Provenance / governance pressure:** provenance of geocoding/provider correction where material.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; redaction/location privacy can be critical.
- **Query / access pressure:** same Place across address/coordinate correction; spatial queries later.
- **PostgreSQL capability pressure:** PostGIS genuine pressure; exact geometry/geography/index only VERTICAL-SPECIFIC; trigram optional for address search.
- **Whole hardening applicability:** WL-H03, WL-H04, WL-H05, WL-H08, WL-H10, WL-H12.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05 later; PSV-36 when accepted geo cases exist; PSV-35 later.
- **Dependency pressure:** ExternalRef/Provenance/Resource role/Visibility.
- **Remaining-work classification:** INHERITED/CLOSED family; CAP/IDX doctrine CP6-02; geo shape VERTICAL-SPECIFIC.

### 36. Plan

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native owner canonical family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef strongly required for materially governed strategy; ExternalRef conditional.
- **Material-state pressure:** **REQUIRED FOR MATERIALLY APPLICABLE PLAN REVISIONS**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** effective strategy applicability/horizon where material.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/replaced chronology.
- **Reference Contract pressure:** typed Goal/Activity/Milestone/Dependency/Policy refs.
- **Constraint / invariant pressure:** identity vs revision/replacement must remain explicit; no universal workflow hierarchy.
- **Transaction / concurrency pressure:** expected-state for revision; multi-owner changes with coordinated structures where atomic.
- **Provenance / governance pressure:** provenance/governance for shared/consequential plan changes.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; replaced plan history retained.
- **Query / access pressure:** which plan/material state governed occurrence/actual at T.
- **PostgreSQL capability pressure:** none intrinsic; graph traversal via SQL/CTE, no graph DB needed.
- **Whole hardening applicability:** WL-H02, WL-H05, WL-H07, WL-H09, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later.
- **Dependency pressure:** Goal/Activity/Milestone/Dependency/Occurrence/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED family; MAT/TX CP6-02; exact plan schema VERTICAL-SPECIFIC.

### 37. Possession

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific typed relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional when material/history; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE CUSTODY HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective possession period.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/transferred chronology.
- **Reference Contract pressure:** holder + target; distinct from Ownership/Allocation.
- **Constraint / invariant pressure:** typed endpoints; temporal overlap rules domain-specific.
- **Transaction / concurrency pressure:** expected-state for transfer; transaction if coupled with other invariant.
- **Provenance / governance pressure:** provenance where possession established/transferred.
- **Retention / redaction / tombstone pressure:** history as policy.
- **Query / access pressure:** who possessed at T vs owned/allocated.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H10.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Asset/Ownership/Resource Allocation/Actor.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 38. Possibility

- **Inherited Logical disposition:** LR-01 once retained as canonical Possibility.
- **Concrete persistence family pressure:** native candidate-future owner family.
- **Identity / addressability pressure:** NativeRef required once canonical retained; MaterialStateRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE EVALUATION/POSTURE/HISTORY CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective relevance context-specific.
- **Recorded/learned/accepted chronology pressure:** recorded/retained/dismissed/adopted chronology.
- **Reference Contract pressure:** typed adoption/origin lineage to Goal; AI candidate not canonical automatically.
- **Constraint / invariant pressure:** identity must not retype into Goal; dismissal not negative preference automatically.
- **Transaction / concurrency pressure:** expected-state for consequential updates/adoption if coupled.
- **Provenance / governance pressure:** source/AI/user provenance central.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; history retained per policy.
- **Query / access pressure:** retained never adopted; provenance; adoption lineage.
- **PostgreSQL capability pressure:** vector/ranking only derived discovery; not canonical; FTS optional.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35/37 later if vector used.
- **Dependency pressure:** Goal/Evaluation/Provenance/AI candidate state.
- **Remaining-work classification:** INHERITED/CLOSED family; exact schema VERTICAL-SPECIFIC.

### 39. Proposal

- **Inherited Logical disposition:** LR-02 conditionally materialized semantic record.
- **Concrete persistence family pressure:** dependent semantic-act family.
- **Identity / addressability pressure:** ScopedRecordRef when materialized; MaterialStateRef for proposal content/target state when consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED WHEN INDEPENDENT REVIEW/VERSION/HISTORY MATTERS**.
- **History pressure:** **MATERIAL WHERE MATERIALIZED**.
- **Effective/world chronology pressure:** effective/expiry/applicability if relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/proposed/withdrawn/superseded chronology.
- **Reference Contract pressure:** proposer + target MaterialStateRef + scope/context.
- **Constraint / invariant pressure:** state-binding; proposal != decision/effect.
- **Transaction / concurrency pressure:** expected-state for target-dependent acceptance; multi-owner if effect atomic.
- **Provenance / governance pressure:** actor/provenance/authority context.
- **Retention / redaction / tombstone pressure:** history of withdrawn/superseded proposals where material.
- **Query / access pressure:** what was proposed against which target state; responses.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H06, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actor/Decision/Request/MaterialStateRef/Authority.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact materialization VERTICAL-SPECIFIC.

### 40. Provenance

- **Inherited Logical disposition:** LR-07 typed lineage/history semantics.
- **Concrete persistence family pressure:** typed lineage/provenance family, bounded not universal graph root.
- **Identity / addressability pressure:** addresses target MaterialStateRef and source ReferenceAddress/MaterialStateRef/ExternalRef as needed; own ScopedRecordRef only if qualified record needs addressability.
- **Material-state pressure:** **REQUIRED FOR CONSEQUENTIAL LINEAGE WHERE SPECIFIED**.
- **History pressure:** **MATERIAL BY DEFINITION WHEN RETAINED**.
- **Effective/world chronology pressure:** source/effect times where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/process/correction chronology central.
- **Reference Contract pressure:** typed lineage roles and exact source/target state contracts.
- **Constraint / invariant pressure:** no provenance=truth/evidence/authority; target/source ref integrity.
- **Transaction / concurrency pressure:** written atomically with consequential effect where needed; must not be detached from commit result.
- **Provenance / governance pressure:** core purpose; actor/process/model/source/basis.
- **Retention / redaction / tombstone pressure:** retention/minimization critical; redaction may preserve bounded lineage.
- **Query / access pressure:** how state came to exist/change; source chain; correction history.
- **PostgreSQL capability pressure:** JSONB only bounded low-consequence computation/provider metadata; graph traversal via relational queries.
- **Whole hardening applicability:** WL-H02, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/35/37 later; logging/privacy PSV-45.
- **Dependency pressure:** MaterialStateRef/ExternalRef/Actor/Reconciliation/Evidence.
- **Remaining-work classification:** INHERITED/CLOSED semantics; PROV constitution CP6-02; owner-specific details VERTICAL-SPECIFIC.

### 41. Quantity

- **Inherited Logical disposition:** LR-04 value semantics.
- **Concrete persistence family pressure:** typed scalar/unit value family embedded/owner-bound.
- **Identity / addressability pressure:** no independent reference; containing owner/material state carries address.
- **Material-state pressure:** **NONE INDEPENDENTLY**.
- **History pressure:** **INHERITED THROUGH OWNER**.
- **Effective/world chronology pressure:** effective time via containing state if needed.
- **Recorded/learned/accepted chronology pressure:** source/recorded chronology via owner/provenance.
- **Reference Contract pressure:** unit/magnitude semantics; not Observation.
- **Constraint / invariant pressure:** numeric precision/unit validity/conversion rules.
- **Transaction / concurrency pressure:** none independently.
- **Provenance / governance pressure:** source/provenance if observed/derived.
- **Retention / redaction / tombstone pressure:** via containing owner.
- **Query / access pressure:** exact value, source unit, normalized derived value without fabricated precision.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04.
- **PostgreSQL risk applicability:** PG-R03 only through containing history.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Containing owner/Observation/Resource Requirement/Capacity.
- **Remaining-work classification:** INHERITED/CLOSED value semantics; SQL type/unit doctrine CP6-02.

### 42. Reconciliation

- **Inherited Logical disposition:** transient reasoning when low consequence; LR-02/LR-07 qualified material record where history/rationale/effect matters.
- **Concrete persistence family pressure:** bounded reasoning/lineage record when material.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRefs/ExternalRefs of competing and resolved states required where material.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR MATERIAL RESOLUTION**.
- **History pressure:** **MATERIAL WHEN RESOLUTION CHANGES ACCEPTED INTERPRETATION OR IDENTITY**.
- **Effective/world chronology pressure:** effective resolution impact where relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revoked/corrected chronology central.
- **Reference Contract pressure:** bounded target/facet + competing source/state refs.
- **Constraint / invariant pressure:** unresolved conflict valid; no newest/provider/confidence winner.
- **Transaction / concurrency pressure:** expected-state for applying resolution; may span multiple owners atomically.
- **Provenance / governance pressure:** resolution basis/evidence/actor/authority/provenance central.
- **Retention / redaction / tombstone pressure:** history needed for reversal/correction; privacy/minimization.
- **Query / access pressure:** why current interpretation won; unresolved conflicts; reverse mistaken merge.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** MaterialStateRef/ExternalRef/Evidence/Provenance/Decision/Authority.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact record shape VERTICAL-SPECIFIC.

### 43. Recurrence

- **Inherited Logical disposition:** LR-05 typed rule/specification.
- **Concrete persistence family pressure:** owner-specific recurrence rule family.
- **Identity / addressability pressure:** ScopedRecordRef/MaterialStateRef conditional when independent history/addressability; governing state must be bindable.
- **Material-state pressure:** **CONDITIONAL→REQUIRED WHEN HISTORICAL OCCURRENCES DEPEND ON EXACT RULE STATE**.
- **History pressure:** **MATERIAL WHEN GOVERNING GENERATED INSTANCES/HISTORY**.
- **Effective/world chronology pressure:** calendar/wall-clock/elapsed/quota/etc. applicability central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology where material.
- **Reference Contract pressure:** source owner + family-specific parameters/frame.
- **Constraint / invariant pressure:** family discriminator + structured params; no provider/RRULE kernel limitation.
- **Transaction / concurrency pressure:** expected-state for revision if consequential; occurrence materialization may race.
- **Provenance / governance pressure:** provenance on rule creation/change where needed.
- **Retention / redaction / tombstone pressure:** retain governing historical state for material occurrences.
- **Query / access pressure:** derive future instances, reconstruct rule state that generated historical occurrence.
- **PostgreSQL capability pressure:** range/time indexes likely; no one JSONB recurrence payload if required semantics; exact DSL vertical-specific.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07, PG-R08, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Routine/Event/Occurrence/MaterialStateRef/temporal values.
- **Remaining-work classification:** INHERITED/CLOSED semantics; type/range doctrine CP6-02; recurrence representation VERTICAL-SPECIFIC.

### 44. Representation

- **Inherited Logical disposition:** LR-03 action-scoped relation; LR-02 when consequential/material.
- **Concrete persistence family pressure:** specific action-scoped governance relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef for action target/governance basis when consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL ON-BEHALF-OF EFFECT**.
- **History pressure:** **MATERIAL WHEN CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effect-time applicability central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revoked chronology of delegation/basis as applicable.
- **Reference Contract pressure:** actual Actor + represented party + bounded action + target/basis.
- **Constraint / invariant pressure:** must preserve actor != represented party; typed scope.
- **Transaction / concurrency pressure:** effect-time revalidation; expected-state and multi-owner transaction as applicable.
- **Provenance / governance pressure:** critical: Authority/delegation/Consent/Principal context separate.
- **Retention / redaction / tombstone pressure:** history/privacy of representation basis.
- **Query / access pressure:** who acted for whom under what basis at T.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H05, WL-H07, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/23/35 later.
- **Dependency pressure:** Actor/Person/Collective/Principal/Authority/Consent/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED semantics; PROV/TX CP6-02; exact relation VERTICAL-SPECIFIC.

### 45. Request

- **Inherited Logical disposition:** LR-02 conditionally materialized semantic record.
- **Concrete persistence family pressure:** dependent directed-act family.
- **Identity / addressability pressure:** ScopedRecordRef when materialized; MaterialStateRef for target state where consequential.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN ASYNC/HISTORY/GOVERNANCE/CONSEQUENCE**.
- **Effective/world chronology pressure:** request applicability/expiry if relevant.
- **Recorded/learned/accepted chronology pressure:** recorded/requested/acknowledged/fulfilled chronology distinct from Actual.
- **Reference Contract pressure:** requester + target/action/context; Request != Authority.
- **Constraint / invariant pressure:** typed lifecycle; acknowledgement/fulfilment distinct from effect.
- **Transaction / concurrency pressure:** expected-state for requested target effect; no implicit Authority.
- **Provenance / governance pressure:** actor/provenance; authority/consent basis only separately.
- **Retention / redaction / tombstone pressure:** history where material.
- **Query / access pressure:** what was requested, response, effect or no effect.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H06, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actor/Decision/Acknowledgement/Authority/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact materialization VERTICAL-SPECIFIC.

### 46. Resource Allocation

- **Inherited Logical disposition:** LR-03 typed relation; LR-02 + ScopedRecordRef where material lifecycle/history requires.
- **Concrete persistence family pressure:** specific qualified allocation relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRefs to Requirement/Schedule/basis where consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL ALLOCATION BASIS**.
- **History pressure:** **MATERIAL WHERE ALLOCATION/REALLOCATION GOVERNS EFFECTS**.
- **Effective/world chronology pressure:** effective allocation period/context.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/reallocated chronology.
- **Reference Contract pressure:** Requirement + provider/resource target + quantities/context; allocation != claim/actual.
- **Constraint / invariant pressure:** typed target eligibility, quantities, no automatic carry-forward after material Requirement change.
- **Transaction / concurrency pressure:** write skew possible with capacity/claims; expected-state + transaction/SERIALIZABLE depending invariant.
- **Provenance / governance pressure:** decision/authority/provenance when consequential.
- **Retention / redaction / tombstone pressure:** historical reallocation basis preserved.
- **Query / access pressure:** allocated vs candidate/claimed/actual; historical basis.
- **PostgreSQL capability pressure:** range/index pressure likely; solver outputs derived only.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H09, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-04/35 later; PSV-41..44 solver later when activated.
- **Dependency pressure:** Resource Requirement/Resource/Capacity/Capacity Claim/Schedule/Decision.
- **Remaining-work classification:** INHERITED/CLOSED semantics; TX/REF/MAT CP6-02; exact allocation schema VERTICAL-SPECIFIC.

### 47. Resource Requirement

- **Inherited Logical disposition:** LR-05 specification; LR-02 + ScopedRecordRef where materially addressable.
- **Concrete persistence family pressure:** owner-specific requirement/specification family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef required when consequential Allocation/Decision depends on exact requirement state.
- **Material-state pressure:** **CONDITIONAL→REQUIRED AT CONSEQUENCE THRESHOLD**.
- **History pressure:** **MATERIAL WHEN VERSION BINDING/EXPLANATION/GOVERNANCE MATTERS**.
- **Effective/world chronology pressure:** effective requirement applicability.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology where material.
- **Reference Contract pressure:** provider/resource-role eligibility + quantity/capability/location/time constraints.
- **Constraint / invariant pressure:** typed structured specification; no universal Rule payload.
- **Transaction / concurrency pressure:** expected-state for consequential revision; allocation effect must bind exact state.
- **Provenance / governance pressure:** provenance/authorship/governance as needed.
- **Retention / redaction / tombstone pressure:** history required when explaining past allocation/claim.
- **Query / access pressure:** requirement state considered for candidate/allocation; current vs historical.
- **PostgreSQL capability pressure:** PostGIS possible for location criteria; range/time indexes possible; JSONB no required semantics.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07.
- **PSV carry-forward:** PSV-09/35 later; solver PSV later.
- **Dependency pressure:** Resource/Quantity/Temporal Constraint/Availability/Allocation.
- **Remaining-work classification:** INHERITED/CLOSED semantics; rule/value doctrine CP6-02; exact shape VERTICAL-SPECIFIC.

### 48. Resource

- **Inherited Logical disposition:** contextual role/capability over eligible providers; no ResourceRef/native wrapper identity.
- **Concrete persistence family pressure:** contextual role over heterogeneous eligible representations.
- **Identity / addressability pressure:** no own address; target may be NativeRef, ScopedRecordRef, bounded value/service/pool/supply/specialist representation under contract.
- **Material-state pressure:** **NONE AS ROLE ITSELF**.
- **History pressure:** **NONE AS WRAPPER**.
- **Effective/world chronology pressure:** through containing Requirement/Allocation/Claim.
- **Recorded/learned/accepted chronology pressure:** through containing records.
- **Reference Contract pressure:** very strong heterogeneous eligibility contract; no NativeRef-only assumption.
- **Constraint / invariant pressure:** must reject ineligible target representation/family; no synthetic native identity.
- **Transaction / concurrency pressure:** inherits operation transaction.
- **Provenance / governance pressure:** provenance/governance through allocation/effect.
- **Retention / redaction / tombstone pressure:** underlying target retention governs.
- **Query / access pressure:** which targets can satisfy requirement without identity inflation.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H09.
- **PostgreSQL risk applicability:** PG-R02, PG-R05.
- **PSV carry-forward:** PSV-35 later; solver PSV later.
- **Dependency pressure:** Resource Requirement/Allocation/Capacity/specialist providers/ReferenceAddress.
- **Remaining-work classification:** INHERITED/CLOSED; REF constitution CP6-02 must support truthful heterogeneous role targets.

### 49. Responsibility

- **Inherited Logical disposition:** LR-03 specific typed relation.
- **Concrete persistence family pressure:** specific accountability relation family.
- **Identity / addressability pressure:** ScopedRecordRef conditional; MaterialStateRef conditional when transfer/history material.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHERE SCOPE/TRANSFER/GOVERNANCE CONSEQUENTIAL**.
- **Effective/world chronology pressure:** effective responsibility period.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/transferred chronology.
- **Reference Contract pressure:** responsible party + bounded commitment/context.
- **Constraint / invariant pressure:** must not collapse with performer/steward/authority/participation.
- **Transaction / concurrency pressure:** expected-state for transfer; multi-owner if coupled effect.
- **Provenance / governance pressure:** provenance/governance for establishment/transfer.
- **Retention / redaction / tombstone pressure:** history where material.
- **Query / access pressure:** who was responsible at T, independent of actual performer.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Actor/Coordination Stewardship/Participation/Authority/Activity.
- **Remaining-work classification:** INHERITED/CLOSED semantics; exact relation VERTICAL-SPECIFIC.

### 50. Routine

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native recurring-intention owner family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef required for materially governing routine state; ExternalRef conditional.
- **Material-state pressure:** **REQUIRED WHEN OCCURRENCES DEPEND ON EXACT ROUTINE STATE**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** effective routine/policy period.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised/retired chronology.
- **Reference Contract pressure:** typed Recurrence/Occurrence/Plan/etc.; Routine != Recurrence.
- **Constraint / invariant pressure:** owner lifecycle distinct from occurrence state; recurrence state binding.
- **Transaction / concurrency pressure:** expected-state for consequential revision; multi-owner when coupled with recurrence/material state.
- **Provenance / governance pressure:** provenance/governance if shared/consequential.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; retired routine history retained.
- **Query / access pressure:** which routine state generated occurrence; skipped occurrence != routine paused.
- **PostgreSQL capability pressure:** range/time index possible; no intrinsic JSONB/vector.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R08, PG-R10.
- **PSV carry-forward:** PSV-02/35 later.
- **Dependency pressure:** Recurrence/Occurrence/Schedule/Actual/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED family; MAT/TIM CP6-02; exact routine schema VERTICAL-SPECIFIC.

### 51. Schedule

- **Inherited Logical disposition:** LR-02 dependent semantic record + ScopedRecordRef where materialized/addressable.
- **Concrete persistence family pressure:** dependent accepted-placement family.
- **Identity / addressability pressure:** ScopedRecordRef for material placements; MaterialStateRef required for accepted placement history when consequential; ExternalRef conditional provider mapping.
- **Material-state pressure:** **REQUIRED FOR CONSEQUENTIAL ACCEPTED PLACEMENT**.
- **History pressure:** **MATERIAL**.
- **Effective/world chronology pressure:** accepted temporal assignment/effective placement central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology central.
- **Reference Contract pressure:** schedulable subject + typed temporal values; Schedule != Capacity Claim/Actual.
- **Constraint / invariant pressure:** range/temporal validity, cardinality, no synthetic unscheduled row.
- **Transaction / concurrency pressure:** expected-state for revision; conflict constraints/locks by resource invariant; multi-owner when coupled claims/participants.
- **Provenance / governance pressure:** provenance/governance for shared/consequential schedule changes.
- **Retention / redaction / tombstone pressure:** prior placements retained; redaction/provider tombstone where applicable.
- **Query / access pressure:** current accepted placement and placement at T; compare Actual.
- **PostgreSQL capability pressure:** range/multirange/GiST likely; exact indexes vertical-specific; no JSONB semantics.
- **Whole hardening applicability:** WL-H02, WL-H04, WL-H05, WL-H07, WL-H08, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later; provider/offline PSV when active.
- **Dependency pressure:** Activity/Event/Occurrence/Temporal values/Capacity Claim/Actual/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; TIM/TX/IDX CP6-02; exact placement schema VERTICAL-SPECIFIC.

### 52. Session

- **Inherited Logical disposition:** LR-01 native identity-bearing record.
- **Concrete persistence family pressure:** native actual-execution episode family.
- **Identity / addressability pressure:** NativeRef required; MaterialStateRef conditional for correction/split/merge state; ExternalRef conditional.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL FOR CORRECTIONS/SPLIT/MERGE/EPISODE HISTORY**.
- **Effective/world chronology pressure:** actual execution interval central.
- **Recorded/learned/accepted chronology pressure:** recorded/corrected/reconciled chronology.
- **Reference Contract pressure:** typed links to Activity/Occurrence/Actual; spontaneous allowed.
- **Constraint / invariant pressure:** identity != timestamps/provider; overlap not globally invalid.
- **Transaction / concurrency pressure:** expected-state for correction; split/merge may require multi-row atomicity.
- **Provenance / governance pressure:** source/provenance for capture/correction.
- **Retention / redaction / tombstone pressure:** NativeRef non-reuse; historical episode continuity.
- **Query / access pressure:** active/paused/elapsed, overlaps, correction lineage.
- **PostgreSQL capability pressure:** range/time indexing likely; exact pause segments vertical-specific.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H07, WL-H08, WL-H10.
- **PostgreSQL risk applicability:** PG-R01, PG-R02, PG-R03, PG-R04, PG-R05, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-02/35 later.
- **Dependency pressure:** Activity/Occurrence/Actual/Observation/ExternalRef.
- **Remaining-work classification:** INHERITED/CLOSED family; exact segment/schema VERTICAL-SPECIFIC.

### 53. Subject

- **Inherited Logical disposition:** contextual role/capability; no SubjectRef/native wrapper identity.
- **Concrete persistence family pressure:** contextual aboutness/target role.
- **Identity / addressability pressure:** no own address; uses eligible target ReferenceAddress under containing contract.
- **Material-state pressure:** **NONE**.
- **History pressure:** **NONE AS WRAPPER**.
- **Effective/world chronology pressure:** through containing Observation/Evidence/etc.
- **Recorded/learned/accepted chronology pressure:** through containing records.
- **Reference Contract pressure:** strong target eligibility and semantic role contract.
- **Constraint / invariant pressure:** reject ineligible target family; no wrapper identity.
- **Transaction / concurrency pressure:** inherits containing operation.
- **Provenance / governance pressure:** visibility/provenance through containing record.
- **Retention / redaction / tombstone pressure:** underlying target retention governs.
- **Query / access pressure:** what record is about without equating target with Subject identity.
- **PostgreSQL capability pressure:** none intrinsic.
- **Whole hardening applicability:** WL-H03, WL-H04, WL-H12.
- **PostgreSQL risk applicability:** PG-R02, PG-R09.
- **PSV carry-forward:** PSV-05/35 later.
- **Dependency pressure:** Observation/Evidence/ReferenceAddress/Visibility.
- **Remaining-work classification:** INHERITED/CLOSED; no SubjectRef.

### 54. Temporal Constraint

- **Inherited Logical disposition:** LR-05 typed rule/specification.
- **Concrete persistence family pressure:** owner-specific temporal rule/spec family.
- **Identity / addressability pressure:** ScopedRecordRef/MaterialStateRef conditional when material history/reuse.
- **Material-state pressure:** **CONDITIONAL**.
- **History pressure:** **MATERIAL WHEN CONSEQUENTIAL PLANNING BASIS**.
- **Effective/world chronology pressure:** effective temporal applicability central.
- **Recorded/learned/accepted chronology pressure:** recorded/accepted/revised chronology when material.
- **Reference Contract pressure:** target/facet + typed temporal semantics.
- **Constraint / invariant pressure:** range/relationship semantics; hard/soft typed; must not become Schedule.
- **Transaction / concurrency pressure:** expected-state for consequential revision; concurrency only in containing planning operation.
- **Provenance / governance pressure:** provenance/authorship/governance when established/shared.
- **Retention / redaction / tombstone pressure:** history when relied upon by past planning/effects.
- **Query / access pressure:** applicable constraints and whether Actual violated them.
- **PostgreSQL capability pressure:** range/multirange/GiST likely vertical-specific.
- **Whole hardening applicability:** WL-H04, WL-H05, WL-H09, WL-H10.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07.
- **PSV carry-forward:** PSV-35 later.
- **Dependency pressure:** Temporal values/Schedule/Activity/Plan/Actual.
- **Remaining-work classification:** INHERITED/CLOSED semantics; TYP/TIM constitution CP6-02; exact schema VERTICAL-SPECIFIC.

### 55. Verification

- **Inherited Logical disposition:** purpose/profile of Evaluation; LR-08 or LR-02 via applicable Evaluation representation.
- **Concrete persistence family pressure:** evaluation profile, not independent root.
- **Identity / addressability pressure:** no own reference family; inherits Evaluation addressing/material state when material.
- **Material-state pressure:** **INHERITED FROM EVALUATION**.
- **History pressure:** **INHERITED FROM EVALUATION**.
- **Effective/world chronology pressure:** target/evaluation window as applicable.
- **Recorded/learned/accepted chronology pressure:** evaluation recorded chronology.
- **Reference Contract pressure:** Criterion/Evidence/target state contract.
- **Constraint / invariant pressure:** no universal VerificationResult root; constraints through Evaluation.
- **Transaction / concurrency pressure:** freshness/expected-state inherited from consequential Evaluation use.
- **Provenance / governance pressure:** provenance/governance inherited from Evaluation.
- **Retention / redaction / tombstone pressure:** retention inherited from material Evaluation snapshot.
- **Query / access pressure:** verification result and basis via Evaluation.
- **PostgreSQL capability pressure:** same as Evaluation; derived only.
- **Whole hardening applicability:** WL-H03, WL-H05, WL-H09, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R07, PG-R09.
- **PSV carry-forward:** PSV-05/09/35 later.
- **Dependency pressure:** Evaluation/Criterion/Evidence/MaterialStateRef.
- **Remaining-work classification:** INHERITED/CLOSED; no independent persistence family.

### 56. Version

- **Inherited Logical disposition:** LR-07 material-state/history semantics; no universal Version root.
- **Concrete persistence family pressure:** cross-cutting owner-specific material-state/history role.
- **Identity / addressability pressure:** MaterialStateRef is the address contract; no universal VersionRef root beyond MaterialStateRef semantics.
- **Material-state pressure:** **REQUIRED WHERE MATERIAL STATE EXISTS**.
- **History pressure:** **MATERIAL BY DEFINITION FOR REPRESENTED MATERIAL VERSIONS**.
- **Effective/world chronology pressure:** effective/world chronology where owner requires.
- **Recorded/learned/accepted chronology pressure:** recorded/learned/accepted/corrected chronology where owner requires.
- **Reference Contract pressure:** owner/facet-specific; must never float from owner.
- **Constraint / invariant pressure:** stable state identity, immutability/lineage/current-binding invariants.
- **Transaction / concurrency pressure:** central to expected-state; new state + current binding atomic.
- **Provenance / governance pressure:** provenance/correction/reconciliation links central.
- **Retention / redaction / tombstone pressure:** retention/redaction/tombstone must preserve honest continuity where permitted.
- **Query / access pressure:** current state, state at T, what was known at K, lineage.
- **PostgreSQL capability pressure:** range/index pressure owner-specific; no universal JSONB state blob.
- **Whole hardening applicability:** WL-H01, WL-H04, WL-H05, WL-H07, WL-H09, WL-H10, WL-H11.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R10.
- **PSV carry-forward:** PSV-01/02/03/09/35 later.
- **Dependency pressure:** all material owners/Provenance/Reconciliation.
- **Remaining-work classification:** INHERITED/CLOSED semantics; MAT/HIST/TIM constitution is core CP6-02 CONCRETE DECISION.

### 57. Visibility

- **Inherited Logical disposition:** LR-03/LR-02 scoped governance state + LR-05 policy basis + LR-08 effective disclosure projection.
- **Concrete persistence family pressure:** specific disclosure relation/state + policy + derived effective projection.
- **Identity / addressability pressure:** ScopedRecordRef conditional for material grants/state; MaterialStateRef required when exact historical basis consequential.
- **Material-state pressure:** **CONDITIONAL→REQUIRED FOR CONSEQUENTIAL DISCLOSURE**.
- **History pressure:** **MATERIAL FOR GRANTS/REVOCATIONS/HISTORY USED BY DISCLOSURE/EFFECTS**.
- **Effective/world chronology pressure:** effective visibility/applicability central.
- **Recorded/learned/accepted chronology pressure:** recorded/granted/revoked/corrected chronology central.
- **Reference Contract pressure:** recipient/source/projection/relation/facet purpose context; endpoint visibility != relation visibility.
- **Constraint / invariant pressure:** typed scope/surface constraints; no object-wide ACL simplification.
- **Transaction / concurrency pressure:** expected-state for changes; consequence requires fresh basis; multi-owner effect when disclosure generated/stored.
- **Provenance / governance pressure:** actor/authority/consent/provenance critical; technical AuthZ separate.
- **Retention / redaction / tombstone pressure:** privacy/redaction central; visibility history itself sensitive.
- **Query / access pressure:** effective visibility by surface; safe projection without private source disclosure.
- **PostgreSQL capability pressure:** query/RLS/application policy later; no separate authority; search must filter before leakage.
- **Whole hardening applicability:** WL-H02, WL-H03, WL-H04, WL-H05, WL-H07, WL-H09, WL-H10, WL-H11, WL-H12.
- **PostgreSQL risk applicability:** PG-R03, PG-R04, PG-R05, PG-R06, PG-R07, PG-R09, PG-R10.
- **PSV carry-forward:** PSV-05/06/07/08/09/10/35 later; offline PSV-13 later.
- **Dependency pressure:** Authority/Consent/Agreement/Representation/MaterialStateRef/Principal projection.
- **Remaining-work classification:** INHERITED/CLOSED semantics; security/disclosure enforcement later; PROV/MAT/TX constitution CP6-02.

---

## 5. Aggregate concrete persistence-family map

This is an implementation-family map, **not** a table list.

### 5.1 Native canonical owner families

Exactly 15 semantic owner families require stable native identity:

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

Physical implication already inherited from the accepted PostgreSQL mapping:

```text
each native owner
→ owner-specific canonical table/family
→ no required common semantic parent row
→ direct FK when a Reference Contract is homogeneous
→ bounded native-address infrastructure only for genuine heterogeneous addressing
```

### 5.2 Dependent/material contextual families

Current Whole pressure includes, conditionally or inherently:

```text
Actual
Agreement
Milestone
Proposal
Request
Decision
Schedule
Outcome
material Criterion
material Evaluation
material Reconciliation
material Resource Requirement
material Availability override
material Capacity state
qualified Resource Allocation
qualified Membership
qualified Interpersonal Relationship
qualified Participation
qualified Responsibility
qualified Coordination Stewardship
qualified Contribution
qualified Ownership
qualified Possession
qualified Authority
qualified Consent
qualified Visibility
qualified Representation
qualified Acknowledgement / Confirmation / Evidence / Dependency where independent state/history matters
```

Rule:

```text
stable contextual addressability
!= native identity
```

Use `ScopedRecordRef` only when the concrete record requires stable address/history.

### 5.3 Specific typed relation families

The Physical Model must continue to preserve specific semantic owners for:

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
party assent within Agreement
```

and other future accepted typed relations.

No canonical:

```text
relationship(from_ref, relation_type, to_ref, payload)
```

may become the semantic fallback.

### 5.4 Rule / policy / specification families

LR-05 pressure includes:

```text
Conditional Policy
Criterion
Recurrence
Resource Requirement
Temporal Constraint
Availability baseline/rule
Authority policy/basis where applicable
Visibility policy/basis where applicable
Capacity compatibility/policy semantics
```

Shared predicate/expression machinery remains a possible technical primitive, but:

```text
shared rule machinery
!= universal Rule owner
```

### 5.5 Value families

Current reusable value pressure includes:

```text
Quantity
Monetary Amount
typed temporal values
typed capacity dimensions where numeric
```

The containing semantic owner owns context, history and provenance.

### 5.6 Material truth / history families

Cross-cutting material truth requires:

```text
MaterialStateRef
owner/facet-specific material state
explicit current accepted-state binding where required
typed correction/replacement/reconciliation lineage
world/effective chronology where material
recorded/learned/accepted/corrected chronology where material
```

No universal Version/Fact/Event owner is introduced.

### 5.7 Provider / external families

Provider/source state remains separate:

```text
ExternalRef
provider payload/state
provider revision
sync/apply state
reconciliation state
canonical DANTE state
```

These may coexist and disagree without implicit overwrite.

### 5.8 Derived/projection families

Current LR-08 pressure includes:

```text
Evaluation by default
Verification via Evaluation
Candidate Set
Effective Availability
Effective remaining Capacity
Effective Authority
Effective Visibility
current/historical knowledge/retrieval
recipient-specific disclosure surfaces
other bounded progress/feasibility projections
```

They are rebuildable/derived unless a consequential historical snapshot is explicitly justified.

---

## 6. Dependency-pressure graph inputs

CP6-01 does **not** freeze the final implementation DAG. It records the dependency pressures CP6-03 must resolve.

### Foundation dependency group F1 — Identity / addressing

```text
ID policy
NativeRef concrete addressing
direct homogeneous FK doctrine
heterogeneous native-address eligibility
ScopedRecordRef concrete addressing
MaterialStateRef concrete addressing
ExternalRef issuer-scoped addressing
Reference Contract enforcement
```

Consumers include essentially every native owner plus all qualified contextual/relation families.

### F2 — Material truth / history

```text
material-state identity
current accepted-state binding
owner/facet state
immutability/correction/replacement
lineage
world/effective chronology
recorded/learned/accepted chronology
```

Strong consumers:

```text
Version
Provenance
Reconciliation
Observation
Plan
Routine
Occurrence
Schedule
Actual
Agreement
Consent
Authority
Visibility
Evaluation
Criterion
Resource Requirement
Resource Allocation
Capacity Claim pressure
```

### F3 — Consequential mutation / concurrency

```text
expected-state
idempotency
transaction ownership
lock / isolation escalation
multi-owner atomicity
external-effect staging boundary
```

Strong consumers:

```text
material owner revisions
Agreement amendment/assent
Consent/Authority/Visibility change
Schedule revision
Resource Allocation / capacity claims
identity reconciliation
governed effects
```

### F4 — Governance / provenance

```text
actual Actor
represented party
Principal/security context reference
Authority / Consent / Visibility / Agreement basis
purpose/context
effect/result
correlation/causation
provider/runtime outcome kept separate
```

Consumers include all consequential governed effects and historical governance reconstruction.

### F5 — Missing / unknown / redaction

```text
absence
explicit negative
unknown/unresolved
not applicable
redacted/unavailable
retired
tombstone continuity
non-reuse
```

This is Whole-wide and cannot be left to individual ORM defaults.

### F6 — Typed temporal semantics

```text
date-only
floating local
named-zone wall-clock
absolute instant
range/interval
duration
precision/frame
accepted historical resolution basis
```

Primary consumers:

```text
Recurrence
Occurrence
Schedule
Session
Actual
Temporal Constraint
Availability
Capacity/Claim
historical applicability
```

### F7 — Derived/search/disclosure boundary

```text
LR-08 freshness
source MaterialState basis
recipient-scoped exposure
search/vector filtering
projection/source non-equivalence
```

Primary consumers:

```text
Evaluation
Candidate Set
Availability/Capacity projections
Authority/Visibility projections
knowledge/retrieval
Content Artifact search
Possibility/recommendation surfaces
```

---

## 7. Closed-vs-open concrete decision register

### 7.1 INHERITED / CLOSED — do not reopen in CP6

```text
PostgreSQL 18.4 is sole canonical/material-history authority
schema dante
owner-specific typed relational/hybrid mapping
15 native owner families
no universal Entity / Thing
no universal Relationship / Edge
no canonical EAV/property bag
no universal event-log ontology
no universal Rule / Fact / Version / Permission root
NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef remain distinct
direct FK preferred for homogeneous references
bounded technical anchors only for genuine heterogeneous addressing
current state != historical material state
canonical != provider != projection != security-runtime state
MaterialStateRef != xmin/xid/updated_at/hash/ETag/provider revision
specific relations remain semantically specific
Agreement is n-ary and terms-state-bound
Occurrence may remain lazy before physical materialization
Schedule != Session != Actual != Outcome
absence != false
expected-state required where stale consequential write is unsafe
idempotency != identity
multi-owner invariants require truthful atomic/staged handling
provider failure does not silently rewrite canonical state
LR-08 cache != canonical truth
NativeRef never reused
technical AuthZ != Domain Authority/Consent
selective disclosure includes indirect inference surfaces
SQLAlchemy 2 / psycopg 3 / Alembic / shared MetaData
outer operation owns transaction
runtime role does not own DDL
```

### 7.2 CONCRETE DECISION — CP6-02 Constitution

The following are truly open global decisions:

```text
ID
    physical identifier policy
    generation locus
    sortability/offline implications
    external exposure doctrine

REF
    exact bounded anchor topology
    eligibility enforcement pattern
    dangling-reference prevention
    scoped/material address physical shape

MAT/HIST
    material-state anchor/current-binding topology
    owner-specific state-row doctrine
    immutability/correction/replacement mechanics
    materiality escalation rules

TIM
    reusable PostgreSQL temporal type doctrine
    historical resolution-basis rule
    dual chronology trigger

MISS
    NULL / row absence / explicit unknown / explicit negative /
    N/A / redacted / unavailable / retired doctrine

TYP
    ENUM vs text+CHECK vs lookup/reference table
    DOMAIN/composite/range/array decision rules

REL
    direct vs qualified vs n-ary reusable relational patterns
    when relation gets ScopedRecordRef/MaterialStateRef

PROV
    bounded consequential provenance pattern

LIFE
    retirement / tombstone / redaction / anti-resurrection metadata rules

CON/TX
    constraint placement doctrine
    DEFERRABLE / EXCLUDE / locking / SERIALIZABLE taxonomy
    retry/conflict semantics

IDX
    FK/composite/partial/INCLUDE/GiST/GIN/index-evidence doctrine

CAP
    allowed activation boundaries for PostGIS/FTS/pg_trgm/pgvector/JSONB

MIG
    business migration/evolution constitution
    expand/migrate/contract / downgrade-vs-forward-fix
    data-migration evidence / continuity rules

QA
    non-speculative direct-proof doctrine
```

### 7.3 VERTICAL-SPECIFIC — intentionally not decided by CP6-01/02 globally

Examples:

```text
exact business table names
exact columns per owner
owner-specific lifecycle fields
specific indexes tied to proven queries
Place geometry/geography shape
Recurrence DSL and family-specific storage
Occurrence locator/key algorithm
Schedule placement cardinality/schema
Session pause/resume segment representation
specific Capacity dimensions
provider-specific integration schemas
specific RLS/AuthZ enforcement
specialist finance/inventory/clinical schemas
```

### 7.4 DIRECT-PROOF — only where a real non-speculative artifact already exists

CP6 may directly prove only materialized foundation behavior such as:

```text
current CP3 transaction ownership semantics
current migration authority/drift contract
current owner/migrator/runtime privilege separation
current real-PostgreSQL harness
current extension envelope
existing schema / version-table posture
```

It MUST NOT manufacture generic address/history/business tables merely to turn a paper obligation into a PASS.

---

## 8. WL-H01..WL-H12 applicability map

### WL-H01

- **Inherited contract:** Agreement terms require an owned MaterialStateRef; no ownerless TermsRef/root.
- **Direct concept pressure identified in this matrix:** Agreement, Version.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H02

- **Inherited contract:** Consequential governed effects preserve semantic target/effect/governance/expected-state/idempotency contract.
- **Direct concept pressure identified in this matrix:** Activity, Actor, Agreement, Authority, Conditional Policy, Consent, Criterion, Decision, Event, Goal, Plan, Proposal, Provenance, Representation, Request, Resource Allocation, Resource Requirement, Resource, Routine, Schedule, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H03

- **Inherited contract:** Projection/disclosure surface remains distinct from source and does not require ProjectionRef.
- **Direct concept pressure identified in this matrix:** Content Artifact, Evaluation, Person, Place, Subject, Verification, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H04

- **Inherited contract:** Absence is not false/negative/non-realization.
- **Direct concept pressure identified in this matrix:** Acknowledgement, Activity, Actual, Agreement, Asset, Authority, Availability, Capacity, Collective, Conditional Policy, Confirmation, Consent, Contribution, Coordination Stewardship, Decision, Dependency, Event, Evidence, Goal, Interpersonal Relationship, Living Referent, Membership, Milestone, Monetary Amount, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Possession, Possibility, Proposal, Quantity, Reconciliation, Recurrence, Request, Resource Allocation, Resource Requirement, Resource, Responsibility, Routine, Schedule, Subject, Temporal Constraint, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H05

- **Inherited contract:** Stale-write-sensitive consequence requires expected-state semantics.
- **Direct concept pressure identified in this matrix:** Acknowledgement, Activity, Actual, Agreement, Asset, Authority, Availability, Capacity, Collective, Conditional Policy, Confirmation, Consent, Content Artifact, Coordination Stewardship, Criterion, Evaluation, Decision, Dependency, Event, Goal, Interpersonal Relationship, Living Referent, Membership, Milestone, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Resource Requirement, Responsibility, Routine, Schedule, Session, Temporal Constraint, Verification, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H06

- **Inherited contract:** Idempotency is technical retry identity, not Domain identity.
- **Direct concept pressure identified in this matrix:** Activity, Decision, Proposal, Request.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H07

- **Inherited contract:** Multi-owner consequential invariants require truthful atomicity or explicit staged/partial handling.
- **Direct concept pressure identified in this matrix:** Activity, Actual, Agreement, Asset, Authority, Capacity, Collective, Conditional Policy, Consent, Content Artifact, Contribution, Decision, Event, Goal, Living Referent, Membership, Ownership, Person, Plan, Possession, Provenance, Reconciliation, Recurrence, Representation, Resource Allocation, Routine, Schedule, Session, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H08

- **Inherited contract:** Canonical state remains separate from provider sync/apply state.
- **Direct concept pressure identified in this matrix:** Actual, Asset, Availability, Content Artifact, Event, Living Referent, Observation, Occurrence, Person, Place, Reconciliation, Provenance, Schedule, Session.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H09

- **Inherited contract:** LR-08 freshness/material basis must be revalidated or bound for consequential use.
- **Direct concept pressure identified in this matrix:** Activity, Authority, Availability, Capacity, Criterion, Evaluation, Dependency, Evidence, Goal, Milestone, Possibility, Resource Allocation, Resource Requirement, Resource, Temporal Constraint, Verification, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H10

- **Inherited contract:** Retention/redaction/tombstone must preserve honest historical existence and non-reuse.
- **Direct concept pressure identified in this matrix:** Acknowledgement, Activity, Actual, Agreement, Asset, Authority, Availability, Capacity, Collective, Conditional Policy, Confirmation, Consent, Content Artifact, Contribution, Coordination Stewardship, Criterion, Evaluation, Decision, Dependency, Event, Evidence, Goal, Interpersonal Relationship, Living Referent, Membership, Milestone, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Resource Requirement, Responsibility, Routine, Schedule, Session, Temporal Constraint, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H11

- **Inherited contract:** Consequential AuthZ provenance preserves Actor/represented party/Principal/governance basis/effect distinctions.
- **Direct concept pressure identified in this matrix:** Acknowledgement, Activity, Actor, Agreement, Authority, Conditional Policy, Confirmation, Consent, Contribution, Decision, Event, Membership, Observation, Ownership, Person, Plan, Proposal, Provenance, Reconciliation, Representation, Request, Resource Allocation, Responsibility, Schedule, Version, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

### WL-H12

- **Inherited contract:** Selective disclosure includes indirect inference channels and projection/source separation.
- **Direct concept pressure identified in this matrix:** Actor, Authority, Availability, Consent, Content Artifact, Evaluation, Evidence, Interpersonal Relationship, Membership, Participation, Person, Place, Provenance, Representation, Subject, Verification, Visibility.
- **Gate-01 disposition:** `ACCOUNTED / NOT REOPENED`.
- **Proof stage:** Constitution in CP6-02 where global mechanics are needed; direct execution only when non-speculative; otherwise vertical/release carry-forward.

---

## 9. PG-R01..PG-R10 applicability and stage map

### PG-R01 — technical anchor leakage

- **Pressure consumers:** Activity, Asset, Collective, Content Artifact, Event, Goal, Living Referent, Observation, Occurrence, Person, Place, Plan, Possibility, Routine, Session.
- **Assigned stage:** FOUNDATION RULE CLOSED IN CP6 + later representative implementation proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R02 — heterogeneous reference integrity

- **Pressure consumers:** Activity, Actor, Agreement, Asset, Collective, Content Artifact, Contribution, Dependency, Evidence, Event, Goal, Interpersonal Relationship, Living Referent, Membership, Observation, Occurrence, Ownership, Participation, Person, Place, Plan, Possession, Provenance, Reconciliation, Representation, Resource Allocation, Resource, Responsibility, Routine, Subject.
- **Assigned stage:** CP6-02 REF constitution + Vertical #1/later vertical direct proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R03 — owner-specific material-history maintainability

- **Pressure consumers:** Acknowledgement, Activity, Actual, Agreement, Asset, Authority, Availability, Capacity, Collective, Conditional Policy, Confirmation, Consent, Content Artifact, Contribution, Coordination Stewardship, Criterion, Evaluation, Decision, Dependency, Event, Evidence, Goal, Interpersonal Relationship, Living Referent, Membership, Milestone, Monetary Amount, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Quantity, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Resource Requirement, Responsibility, Routine, Schedule, Session, Temporal Constraint, Verification, Version, Visibility.
- **Assigned stage:** CP6-02 MAT/HIST constitution + representative vertical direct proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R04 — expected-state concurrency

- **Pressure consumers:** Activity, Actual, Agreement, Asset, Authority, Availability, Capacity, Collective, Conditional Policy, Consent, Content Artifact, Coordination Stewardship, Criterion, Evaluation, Decision, Dependency, Event, Goal, Interpersonal Relationship, Living Referent, Membership, Milestone, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Resource Requirement, Responsibility, Routine, Schedule, Session, Temporal Constraint, Verification, Version, Visibility.
- **Assigned stage:** CP6-02 TX constitution + real business concurrency proof post-CP6.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R05 — multi-owner write skew

- **Pressure consumers:** Activity, Actual, Agreement, Asset, Authority, Capacity, Collective, Consent, Contribution, Decision, Dependency, Event, Goal, Living Referent, Membership, Ownership, Person, Plan, Possession, Provenance, Reconciliation, Representation, Resource Allocation, Resource, Routine, Schedule, Session, Version, Visibility.
- **Assigned stage:** CP6-02 TX taxonomy + invariant-specific vertical concurrency proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R06 — Agreement/governance materiality

- **Pressure consumers:** Acknowledgement, Agreement, Authority, Collective, Conditional Policy, Confirmation, Consent, Coordination Stewardship, Decision, Membership, Proposal, Provenance, Representation, Request, Responsibility, Version, Visibility.
- **Assigned stage:** CP6-02 relation/material/governance doctrine + Agreement/governance vertical proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R07 — temporal/history semantics

- **Pressure consumers:** Acknowledgement, Activity, Actual, Agreement, Authority, Availability, Capacity, Confirmation, Consent, Content Artifact, Contribution, Coordination Stewardship, Criterion, Evaluation, Decision, Dependency, Event, Evidence, Goal, Interpersonal Relationship, Membership, Milestone, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Resource Requirement, Responsibility, Routine, Schedule, Session, Temporal Constraint, Verification, Version, Visibility.
- **Assigned stage:** CP6-02 HIST/TIM constitution + representative vertical history queries.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R08 — lazy Occurrence identity/materialization

- **Pressure consumers:** Occurrence, Recurrence, Routine.
- **Assigned stage:** rule carried into CP6; exact locator/materialization proof belongs recurrence/Occurrence vertical.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R09 — selective disclosure/non-interference

- **Pressure consumers:** Actor, Authority, Availability, Consent, Content Artifact, Evaluation, Evidence, Interpersonal Relationship, Membership, Participation, Person, Place, Provenance, Representation, Subject, Verification, Visibility.
- **Assigned stage:** CP6 disclosure doctrine + system/vertical security proof; not fully provable with no business surface.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

### PG-R10 — retention/restore anti-resurrection

- **Pressure consumers:** Acknowledgement, Activity, Actual, Agreement, Asset, Authority, Availability, Collective, Confirmation, Consent, Content Artifact, Contribution, Coordination Stewardship, Evaluation, Decision, Event, Evidence, Goal, Interpersonal Relationship, Living Referent, Membership, Observation, Occurrence, Outcome, Ownership, Participation, Person, Place, Plan, Possession, Possibility, Proposal, Provenance, Reconciliation, Recurrence, Representation, Request, Resource Allocation, Responsibility, Routine, Schedule, Session, Version, Visibility.
- **Assigned stage:** CP6 lifecycle/tombstone doctrine; destructive restore/anti-resurrection remains release/recovery proof.
- **CP6-01 status:** `MAPPED / NOT CLAIMED PASS`.

---

## 10. PSV applicability / stage map

The complete PSV register remains authoritative. CP6-01 does not relabel any unexecuted item as PASS.

### 10.1 Primary correctness/recovery

| PSV | Obligation | CP6 applicability | Assigned stage |
|---|---|---|---|
| PSV-01 | old-backup anti-resurrection | Foundation doctrine relevant; destructive proof unavailable without recovery scenario | CP6-02 LIFE rule; release/recovery direct proof |
| PSV-02 | actual DANTE V1 → V2 mapping/schema evolution | Migration constitution relevant; real business evolution does not yet exist | CP6-02 MIG rule; post-vertical real V1→V2 proof |
| PSV-03 | destructive restore + semantic verification | Recovery contract relevant; no CP6 business state to fabricate | release/recovery direct proof |
| PSV-04 | capacity/backpressure truthful degradation | Capacity semantics represented in coverage; runtime pressure not CP6 foundation-only | Capacity/runtime vertical or release |
| PSV-05 | WL-H12 system-level non-interference | Foundation disclosure doctrine relevant; full system proof requires real surfaces | CP6-02 doctrine; vertical/security/system proof |
| PSV-35 | selected PostgreSQL mapping end-to-end smoke corpus | CP6 coverage/constitution prepares it; no speculative business schema | representative post-CP6 vertical implementation proof |

### 10.2 Search/vector/projection PSV-06..10

Current applicability:

```text
CP6-01: MAP ONLY
CP6-02: establish canonical-vs-derived, freshness, filtering, deletion doctrines
direct PASS: only after actual search/vector/projection capability exists
```

Primary future consumers include Content Artifact search, Possibility/recommendation, Evaluation/knowledge retrieval, Candidate Set and Visibility-filtered projections.

### 10.3 Offline/PowerSync PSV-11..20

```text
CURRENT CP6-01
NOT ACTIVE FOR DIRECT PROOF

carry forward because PowerSync remains bounded companion, not current canonical business implementation
```

No offline obligation is dropped.

### 10.4 Durable execution/Restate PSV-21..28B

```text
CURRENT CP6-01
NOT ACTIVE FOR DIRECT PROOF

WL-H07/WL-H08/WL-H11 semantics are mapped,
but Restate remains later bounded execution capability.
```

### 10.5 Object storage / backup PSV-29..34

Content Artifact creates future pressure, but no CP6 business object-storage workflow is implemented. Preserve to object-storage/recovery stage.

### 10.6 PostgreSQL / extensions / pooling PSV-36..40

```text
PSV-36 PostGIS
    activate only after a real accepted Place/geo query corpus exists

PSV-37 pgvector provenance
    activate only after an actual vector projection exists

PSV-38 PgBouncer compatibility
PSV-39 PowerSync bypass of incompatible transaction pooling
    activation tied to those bounded capabilities

PSV-40 pgBackRest archive/restore/PITR
    recovery stage
```

### 10.7 Solver PSV-41..44

Resource Requirement/Allocation/Capacity coverage preserves solver boundaries, but OR-Tools direct proof waits until the solver capability is activated.

### 10.8 Observability/privacy PSV-45..47

Remain cross-cutting implementation/release obligations. CP6-02 provenance/logging doctrine must avoid creating a contradictory foundation, but no unexecuted item becomes PASS.

---

## 11. PostgreSQL special-capability coverage summary

### PostGIS

Current semantic pressure:

```text
Place
Resource Requirement location constraints
possible Schedule/Availability/location feasibility
```

CP6-01 verdict:

```text
CAPABILITY PRESSURE PRESENT
NO GEOMETRY/GEOGRAPHY SHAPE SELECTED
NO INDEX SELECTED
PSV-36 REMAINS FUTURE DIRECT PROOF
```

### FTS / pg_trgm

Potential derived query pressure includes:

```text
Content Artifact textual search
Person/Place human-facing lookup where product query proves it
Goal/Possibility/Activity text lookup where a vertical proves need
```

No canonical search field or index is authorized by this document.

### pgvector

Potential bounded derived retrieval/ranking pressure:

```text
knowledge/retrieval
Content Artifact semantic retrieval
Possibility/recommendation
Evaluation/candidate discovery
```

It remains LR-08/projection infrastructure and never canonical truth.

### JSONB

Allowed pressure remains restricted to:

```text
LR-10 low-consequence flexible metadata
provider/raw payloads
bounded specialist-extension detail
bounded computation/provenance metadata where semantics do not disappear into it
```

CP6-01 found **zero** concept requiring JSONB as its canonical semantic representation.

---

## 12. Canonical/provider/derived boundary coverage

### Canonical

Owned by typed semantic families and their applicable material-state history.

### Provider/external

```text
ExternalRef
provider payload
provider revision
sync/apply state
provider tombstone
```

do not overwrite canonical truth automatically.

### Derived

```text
Evaluation by default
Verification via Evaluation
Candidate Set
Effective Availability
Effective Capacity
Effective Authority
Effective Visibility
knowledge/retrieval
recipient projection
search/vector indexes
```

do not become canonical merely because cached/materialized.

### Unresolved/candidate

Unresolved provider mapping, AI inference and conflicting interpretation remain representable without forced canonical target.

### Security/runtime

Principal/session/AuthZ allow/deny remain downstream security context/evidence, not Domain Authority/Actor identity.

Gate-01 boundary result:

```text
CANONICAL / PROVIDER / DERIVED CLASSIFICATION PRESSURE
ACCOUNTED

SILENT LAYER COLLAPSE
0 identified in candidate map
```

---

## 13. Gate-01 candidate audit

This document is **not yet Gate 01 PASS**.

Current candidate audit:

```text
57 / 57 concepts accounted                         CANDIDATE PASS
15 / 15 LR-01 families accounted                   CANDIDATE PASS
reference pressure classified                      CANDIDATE PASS
materiality/history pressure classified            CANDIDATE PASS
canonical/provider/derived boundaries classified   CANDIDATE PASS
dependency pressure classified                     CANDIDATE PASS
WL-H01..12 applicability complete                  CANDIDATE PASS
PG-R01..10 applicability complete                  CANDIDATE PASS
PSV applicability/stage complete                   CANDIDATE PASS

semantic owner reclassification                    0 identified
generic semantic fallback                          0 identified
unexplained JSONB fallback                          0 identified
unclassified persistence family                    0 identified
accidental upstream architecture reopen             0 identified
```

These are **candidate findings only** until the independent second-pass review below is completed.

---

## 14. Mandatory second-pass review before Gate 01

Before Gate 01 can be called PASS, perform a fresh review that does **not** merely reread this document for internal consistency.

The reviewer/pass must re-derive from source authorities:

```text
A. Whole-Logical exact 57-owner census
B. canonical Slice A–F superseding hardenings
C. Representation Framework Whole hardening
D. accepted PostgreSQL mapping
E. PG-R01..PG-R10
F. PM-03 / Physical carry-forward where relevant
G. complete PSV register
H. CP6 durable gate requirements
I. current branch delta
```

Required reconciliation checks:

```text
1. every Whole-Logical concept appears exactly once in the 57-entry map
2. no additional concept was silently promoted to owner
3. all 15 native owners exactly match Whole-Logical
4. Actor/Subject/Resource still have no wrapper identity
5. latest superseding hardenings win over earlier slice wording
6. ReferenceAddress variants remain non-collapsed
7. MaterialStateRef is not confused with MVCC/revision/token
8. no relation family became generic
9. no LR-05 family became generic Rule
10. no LR-08 projection became canonical
11. no provider state became canonical
12. all WL-H01..12 have concrete consumers/stage
13. all PG-R01..10 have stage ownership
14. every PSV item is either applicable now, explicitly later, or inactive-capability-bound
15. no unexecuted PSV is labeled PASS
16. no speculative table/primitive is introduced
17. no exact business DDL leaks into CP6-01
18. exact PRE-SCOPE → HEAD delta contains only the authorized CP6-01 file
```

If any mismatch appears:

```text
DO NOT PATCH SILENTLY
classify source conflict / CP6 inference error
repair under explicit bounded write
repeat remote readback
repeat second-pass review
```

Only after this independent pass may a separate closure/gate record or authorized status update state:

```text
CP6-01
GATE 01 PASS
```

---

## 15. Resume point

If this candidate artifact is remotely written and exact-delta QA passes, the next action is **not CP6-02 yet**.

Next:

```text
SECOND-PASS INDEPENDENT CP6-01 REVIEW
        ↓
repair if required
        ↓
GATE 01 decision
        ↓
only then CP6-02 PostgreSQL Persistence Constitution
```

No business DDL/migration/mapping/adapter is authorized anywhere in that sequence.
