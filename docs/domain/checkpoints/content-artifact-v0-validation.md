# Content Artifact / Document v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — propagation candidate  
**Date:** 2026-08-16  
**Concept:** Content Artifact / Document v0  
**Workstream:** Core Domain Model v0 — Whole-Domain Repair  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Scope

This checkpoint validates whether LifeOS requires a persistent content referent distinct from physical Asset, file/blob/provider storage, Attachment use, Evidence, Provenance, Observation and Version.

The Whole-Domain audit identified Content Artifact / Document as a **REQUIRED NOW** semantic repair because V1 requires reusable notes, attachments, imported plans, source documents, meeting pre-reads/transcripts/recording references, search and content reuse without treating provider records as ontology authority.

Primary risks:

- collapsing content identity into storage identity;
- making every upload or serialized object a native entity;
- duplicating the same content for every attachment/use;
- confusing source content with Evidence or canonical structured truth;
- confusing Artifact identity with Version;
- losing historical decision/evidence basis after content edits;
- leaking private content because its parent/container is shared;
- importing a universal DMS/file/folder ontology into the kernel.

---

# 2. Candidate hypotheses

```text
H0  No persistent content identity; file/blob/link + Provenance suffice.
H1  Content Artifact = scoped native information-bearing content referent.
    Document/Note/Image/Recording/Transcript = bounded kinds/product vocabulary.
    File/blob/provider representation and Attachment use remain separate.
H2  Content Artifact = file/blob.
H3  Content Artifact = Evidence.
H4  Content Artifact = Provenance/source.
H5  Content Artifact = Version.
H6  Universal Document/File root for any LifeOS record.
H7  Every attachment/upload creates a Content Artifact.
```

Result:

```text
H1 survives.
H0/H2/H3/H4/H5/H6/H7 fail.
```

---

# 3. Existing LifeOS evidence

Current product requirements already need:

- searchable notes, attachments, imported plans and source documents;
- opening a canonical item and retaining source/history context;
- progressive search inside files/attachments;
- meeting pre-read, notes, transcript/recording reference and linked documents across occurrences;
- private notes or attached content inside otherwise shared contexts;
- AI/OCR extraction without silently turning provider text into truth.

This is not speculative DMS completeness. The missing content identity blocks truthful representation of current intended LifeOS workflows.

Result: **PASS**.

---

# 4. External benchmark — evidence only

Targeted benchmark used only to test boundaries:

- HL7 FHIR `DocumentReference` separates a document reference from the `Attachment` representation/access mechanism and permits multiple representations of the same document while distinguishing different versions;
- Google Drive separates persistent file identity from revisions;
- W3C PROV distinguishes derivation/revision/source relations rather than equating all derived content with one version chain.

Borrowed/adapted only:

```text
content identity != storage representation
identity != revision/version
revision != derivation/fork universally
lineage != content identity
```

Not imported:

- FHIR resource model;
- Drive provider schema;
- PROV-O ontology hierarchy;
- provider IDs as canonical identity;
- universal document management model.

Result: **PASS WITH HARDENING**.

---

# 5. Core Semantic Validation Gate

## CORE-01 — Real-world workflow inversion

Without a stable content referent, users and systems are forced to treat a PDF export, provider object, attachment row or copied file as the content identity. This breaks ordinary workflows where the same note/document is linked from several contexts, edited over time, exported to several formats or migrated between providers.

Content Artifact permits LifeOS to preserve the information-bearing thing while storage/use varies.

**PASS**

## CORE-02 — Deep chronology

```text
T0 User creates Note A for Event E.
   Artifact A is established.

T1 A is attached to E.
   Artifact identity != Event identity.

T2 A is exported to PDF and synced to provider object G1.
   Representation/provider object != new Artifact automatically.

T3 User materially edits A.
   Artifact A persists; material state V1 -> V2.

T4 Decision D was made using A@V1.
   Later V2 must not rewrite historical Decision basis.

T5 V2 is exported as PDF + DOCX.
   Both may represent A@V2.

T6 Provider migration G1 -> G2.
   Artifact identity survives.

T7 AI extracts `Deadline Friday` from A@V2.
   Candidate derived semantics + Provenance; not established truth.

T8 User corrects extracted deadline.
   Derived structured state changes; source Artifact remains historical source.

T9 Someone copies A and independently evolves it.
   Artifact B may become distinct where identity/lifecycle diverges.

T10 Shared Event remains visible to another Actor while private Artifact A remains hidden.

T11 Retention removes raw representation where authorised/required.
    Remaining permitted derived facts/lineage must not resurrect unauthorised raw content.
```

Required distinctions survive only if Artifact identity, material Version and representation remain separate.

**PASS WITH HARDENING**

## CORE-03 — Adversarial reductio

### REMOVE Content Artifact

Fails current V1 reuse/search/history because storage records become accidental semantic identity or every usage duplicates content.

### MERGE with Asset

Fails because accepted Asset identity is for individually tracked non-human physical objects. Digital/information content is not physical Asset identity.

### MERGE with file/blob/provider object

Fails provider migration, alternate formats, URL/path rename, local/cloud representation and stable LifeOS identity.

### MERGE with Evidence

Fails because information may exist without being evaluatively relevant, and the same Artifact may be Evidence in one context and irrelevant in another.

### MERGE with Provenance

Fails because lineage/origin can change or expand while the content referent remains the same.

### MERGE with Observation

Fails because content can contain assertions without those assertions being accepted structured domain truth.

### MERGE with Version

Fails because several material states can belong to one Artifact and technical representations/revisions need not be material versions.

### UNIVERSAL Document/File root

Fails product simplicity and ontology discipline: ordinary structured LifeOS objects do not become documents merely because they can be rendered/exported.

### EVERY UPLOAD IS ARTIFACT

Fails transient ingestion/processing workflows and manufactures identity where no reusable content lifecycle exists.

**PASS WITH HARDENING**

## CORE-04 — Redundancy / merge-split

| Pair | Classification | Boundary |
|---|---|---|
| Content Artifact / Asset | DISTINCT | information referent vs physical object identity |
| Content Artifact / file/blob | DISTINCT | content identity vs representation/storage |
| Content Artifact / Attachment | DISTINCT | referent vs contextual use/relation |
| Content Artifact / Evidence | DISTINCT | source content vs evaluative role/use |
| Content Artifact / Provenance | DISTINCT | content referent vs lineage |
| Content Artifact / Observation | DISTINCT | information container/content vs structured assertion |
| Content Artifact / Version | DISTINCT | referent identity vs material state |
| Content Artifact / Subject | DISTINCT | referent vs contextual aboutness role |
| Document / Note / Image / Recording / Transcript | BOUNDED KINDS | no separate universal roots required |

**PASS WITH HARDENING**

## CORE-05 — Multidirectional traceability

Downward:

```text
Event/Plan/Decision -> attachment/link -> Artifact -> applicable material state -> representation
```

Upward:

```text
Artifact source -> Provenance -> derived structured fact / Evidence use / AI explanation
```

Lateral:

```text
one Artifact -> several contextual attachments/uses
```

without duplication.

**PASS**

## CORE-06 — Orphan / independence

- Artifact can exist unattached: YES.
- Artifact can exist without Evidence use: YES.
- Artifact can exist without structured extraction: YES.
- Artifact can exist while one provider representation disappears: YES, if valid continuity remains.
- file/blob can exist without Artifact identity: YES, for transient/non-reusable payloads.
- Attachment without an Artifact/content target: NO meaningful attachment semantics.

**PASS WITH HARDENING**

## CORE-07 — External cross-domain benchmark

Mature systems independently support separation among document/content identity, representation/access, revision/version and lineage. This supports the boundary while not determining LifeOS's ontology.

**PASS**

## CORE-08 — Anti-pattern test

Rejected:

- provider-first identity;
- file extension as domain type authority;
- every upload = entity;
- folder/workspace hierarchy as kernel ontology;
- hash/title/filename as universal identity equivalence;
- generated export = new content identity automatically;
- content text = canonical truth;
- shared parent = shared content automatically.

**PASS WITH HARDENING**

## CORE-09 — Correction / epistemic safety

Correction of extracted facts must not rewrite source content history. Correction of content must not silently rewrite consequential prior Decision/Evidence/Agreement basis. Presence in a document is not truth. Conflicting content or sources may remain unresolved under existing reconciliation rules.

**PASS WITH HARDENING**

## CORE-10 — Scale / history

The model scales by preserving one Artifact identity across many uses rather than duplicating content per container. Material-history capture is consequence-driven; technical revision history does not automatically become semantic Version history.

**PASS WITH HARDENING**

## CORE-11 — Simple / power user

Simple user: note/document behaves as one reusable thing despite exports/provider moves.  
Power user: material state, derivation, evidence basis, visibility and lineage can remain reconstructible where needed.

**PASS**

## CORE-12 — Product value / complexity

Current V1 search, notes, source documents, meeting material, attachments and AI extraction need the boundary now. One scoped referent is cheaper and clearer than multiplying attachment/document/file identities or embedding content state into every parent object.

**PASS**

## CORE-13 — Implementation pressure

The semantic result does **not** choose blob storage, object keys, MIME model, OCR pipeline, indexing, provider-sync, SQL schema or API shape. It only protects identity and history boundaries those stages must respect.

**PASS WITH HARDENING**

```text
CORE GATE
PASS WITH HARDENING
```

---

# 6. Multi-Actor Gate

```text
MA-01 Identity/account independence       PASS WITH HARDENING
MA-02 Shared fact / actor overlay         PASS WITH HARDENING
MA-03 Responsibility                     PASS
MA-04 Coordination Stewardship            PASS
MA-05 Common ground                       PASS
MA-06 Authority                           PASS WITH HARDENING
MA-07 Selective disclosure               PASS WITH HARDENING
MA-08 Inference privacy                   PASS WITH HARDENING
MA-09 Partial adoption                    PASS
MA-10 Representation/on-behalf-of        PASS
MA-11 Lifecycle/revocation               PASS WITH HARDENING
MA-12 Conflict/adversarial               PASS WITH HARDENING
MA-13 Unequal power                      PASS WITH HARDENING
MA-14 Resource/capacity                  PASS
MA-15 Burden distribution                PASS
MA-16 Progressive disclosure             PASS
MA-17 AI / automation                    PASS WITH HARDENING
MA-18 Specialist systems                 PASS WITH HARDENING
MA-19 Primitive redundancy               PASS WITH HARDENING
MA-20 Actor-scoped attribution           PASS WITH HARDENING
```

Key hardenings:

- creator/editor/contributor/owner/authority are not Artifact identity;
- shared container does not automatically expose Artifact content;
- Artifact visibility may differ from Version, Provenance and extracted structured facts;
- AI extraction remains attributable and does not silently establish truth;
- provider/system migration does not replace canonical identity automatically.

```text
MULTI-ACTOR GATE
PASS WITH HARDENING
```

---

# 7. Cross-cluster Gate

```text
XCON-01 Identity                         PASS WITH HARDENING
XCON-02 Authority                        PASS WITH HARDENING
XCON-03 current/history/material state   PASS WITH HARDENING
XCON-04 Relationships / Reasoning        PASS
XCON-05 Multi-Actor                      PASS WITH HARDENING
XCON-06 Language                         PASS WITH UPDATE
```

Key cross-cluster conclusions:

```text
Content Artifact != Asset
Content Artifact may play Subject role without becoming Subject identity
Artifact != Evidence
Artifact != Provenance
Artifact != Observation
Artifact != Version
Attachment is contextual relation/use
Visibility remains independently governed
```

No Cluster-5 relation primitive reopens.

```text
XCON GATE
PASS WITH HARDENING
```

---

# 8. Accepted hardenings ART-01..38

```text
ART-01  Content Artifact is a scoped native information-content referent.
ART-02  Document/Note/Image/Recording/Transcript are bounded kinds/product vocabulary, not separate universal roots.
ART-03  Content Artifact != Asset.
ART-04  Content Artifact != file/blob/storage object.
ART-05  Provider file ID / URL / path != canonical Artifact identity.
ART-06  Attachment is contextual use/relation, not native identity/root.
ART-07  Content Artifact != Evidence.
ART-08  Artifact may be used as Evidence without becoming Evidence identity.
ART-09  Content Artifact != Provenance.
ART-10  Artifact may be a provenance source/input while retaining independent identity.
ART-11  Content Artifact != Observation or other structured domain fact.
ART-12  Content may contain assertions; presence in content != canonical truth.
ART-13  AI/OCR/provider extraction produces attributable candidate/derived semantics, not silent canonical truth.
ART-14  Content Artifact != Version.
ART-15  Material Version may change while Artifact identity persists.
ART-16  Technical revision != material Version universally.
ART-17  Alternate formats/representations may express the same Artifact material state.
ART-18  Independent fork/copy may become a distinct Artifact where lifecycle/identity diverges.
ART-19  Derivation/fork history must remain reconstructible where consequential.
ART-20  No universal same-Artifact rule based solely on filename/hash/title/provider ID.
ART-21  Same hash does not universally prove same Artifact; different hash does not universally prove different Artifact.
ART-22  Provider migration/path rename/storage move != Artifact replacement automatically.
ART-23  Correction/current state != silent historical overwrite.
ART-24  Decision/Evidence/Agreement/etc. depending materially on content must be able to retain the applicable Artifact material state.
ART-25  Attachment to Event/Activity/Plan/etc. does not merge identities.
ART-26  Shared container Visibility != Artifact Visibility.
ART-27  Artifact Visibility != visibility of every Version/Provenance/extracted fact.
ART-28  Content Artifact may play Subject role without becoming Subject identity.
ART-29  Authorship/Contribution/Ownership/Authority are independent semantics.
ART-30  Digital/IP/copyright ownership is not established by this review.
ART-31  Retention/deletion of representation/content must not manufacture false historical truth or allow Provenance to reconstruct content that is no longer authorised.
ART-32  Ordinary structured LifeOS objects do not become Content Artifacts merely because they can be serialized/rendered/exported.
ART-33  Legal Contract/credential/official-record semantics are not replaced by Content Artifact.
ART-34  Content Artifact identity exists only where reusable content identity/history/search/linking materially matters.
ART-35  Transient upload/payload used only for one processing step need not create Artifact identity.
ART-36  Loss of one representation/provider does not necessarily destroy Artifact identity when another valid representation/state remains.
ART-37  No universal folder/workspace/document-management hierarchy is accepted.
ART-38  No blob store/MIME schema/OCR/index/storage/SQL/API/provider-sync model is accepted by this semantic review.
```

All hardenings were incorporated before verdict.

---

# 9. ADS — dependency classification

```text
enterprise Document Management System
→ NOT REQUIRED BY CURRENT LIFEOS KERNEL

universal Document/File/Content superclass
→ REJECTED / OVERMODELED

universal folder/workspace hierarchy
→ REJECTED

every-upload-is-an-Artifact
→ REJECTED

IP/copyright ownership
→ NOT REQUIRED BY CURRENT LIFEOS KERNEL

legal document validity / signature / enforceability
→ specialist semantics / OUT OF KERNEL

credential/passport/legal-record semantics
→ specialist domain where required

regulated records retention / eDiscovery
→ specialist implementation/compliance domain

file/blob representation
→ STAGE-DEFERRED logical/physical representation

MIME/storage/object-store design
→ STAGE-DEFERRED

OCR / transcription / indexing
→ implementation capability

provider sync / conflict algorithms
→ integration stage

content search indexing
→ implementation stage

SQL/API
→ STAGE-DEFERRED
```

These stage/specialist items are not semantic candidate debt and do not authorize automatic future ontology expansion.

```text
SEMANTIC SAFE DEFERRED  0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

---

# 10. Verdict

```text
CONTENT ARTIFACT / DOCUMENT v0

PASS WITH HARDENING

Content Artifact
SCOPED NATIVE INFORMATION-CONTENT REFERENT

Document / Note / Image / Recording / Transcript
BOUNDED KINDS / PRODUCT VOCABULARY
NO SEPARATE UNIVERSAL ROOTS

Attachment
CONTEXTUAL USE / RELATION
NO NATIVE ENTITY/ROOT

File / blob / provider object / URL
REPRESENTATION / ACCESS / STORAGE SEMANTICS
NOT CANONICAL ARTIFACT IDENTITY

Version
MATERIAL-STATE CAPABILITY
NOT ARTIFACT IDENTITY

Evidence
CONTEXTUAL EVALUATIVE ROLE/USE
NOT ARTIFACT IDENTITY

Provenance
BOUNDED LINEAGE
NOT ARTIFACT IDENTITY

NEW NATIVE REFERENT
YES — Content Artifact

REOPEN       0
UNCLASSIFIED 0
```

Repository closure remains conditional on exact propagation and remote post-write QA.