# Content Artifact v0

**Status:** PASS WITH HARDENING — accepted current baseline  
**Date:** 2026-08-16  
**Workstream:** Core Domain Model v0 — Whole-Domain Repair  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Definition

A **Content Artifact** is the persistent native representation of a materially reusable information-bearing content item whose identity matters across LifeOS contexts independently from any one storage file/blob, provider identifier, attachment use, Provenance role, Evidence use, or material version/representation.

It answers:

> Which persistent content item is this, when the information itself must be found, linked, versioned, cited, shared or reused as one continuing thing?

Classification:

```text
Content Artifact
= SCOPED NATIVE INFORMATION-CONTENT REFERENT
```

Content Artifact is a native referent only where reusable content identity materially matters. It is not a universal wrapper for every serialized, rendered, uploaded or transient payload in LifeOS.

---

# 2. Bounded vocabulary

The following are bounded kinds / product vocabulary over Content Artifact where useful:

```text
Document
Note
Image
Recording
Transcript
```

They are not separate universal kernel roots merely because products expose them as nouns.

`Attachment` is contextual use/relation vocabulary: an Artifact may be attached to an Event, Activity, Plan, Decision or another relevant context while preserving its own identity.

---

# 3. Identity boundaries

Canonical non-collapse rules:

```text
Content Artifact != Asset
Content Artifact != file/blob/storage object
Content Artifact != provider file ID / URL / path
Content Artifact != Attachment
Content Artifact != Evidence
Content Artifact != Provenance
Content Artifact != Observation
Content Artifact != Version
```

A single Artifact material state may have several technical representations or exports. Conversely, a copied or derived representation may become a distinct Artifact when its materially relevant lifecycle/identity diverges.

No universal same-Artifact rule is established from filename, title, hash, URL, provider ID or storage location alone.

---

# 4. Version and representation

Content Artifact identity and material Version are separate:

```text
Artifact identity
!= materially relevant Artifact state

technical revision
!= material Version universally

new representation / export
!= new Artifact automatically
!= new Version automatically
```

A materially edited note can remain the same Artifact with a later material state. A PDF and DOCX can represent the same material state. A provider migration, path rename or storage move does not replace Artifact identity automatically.

Where a Decision, Evidence use, Agreement or another consequential context depends materially on content, the then-applicable Artifact material state must remain reconstructible according to the accepted Version/history discipline.

---

# 5. Evidence, Provenance and structured truth

An Artifact may be used as Evidence without becoming Evidence identity.

An Artifact may be a source/input in Provenance without becoming Provenance.

Content may contain assertions, but presence in content is not itself canonical truth:

```text
text inside Artifact
!= Observation automatically

AI/OCR/provider extraction
!= established canonical fact automatically
```

Extracted or derived semantics must retain attribution/Provenance and remain subject to the owning concept's epistemic, correction and conflict rules.

---

# 6. Attachment and reuse

The same Artifact may simultaneously be:

```text
attached to Event E
linked from Plan P
used as Evidence for Criterion C
used as source for AI extraction
linked from Decision D
returned by Global Search
```

without manufacturing separate content identities per usage.

Attachment to another referent does not merge identities.

---

# 7. Multi-actor and visibility

Content Artifact identity is independent from authorship, Contribution, Ownership, Authority and Visibility.

Container visibility does not imply Artifact visibility:

```text
Visibility(container)
!= Visibility(Content Artifact)

Visibility(Artifact)
!= Visibility(all Artifact versions)
!= Visibility(Provenance)
!= Visibility(extracted structured facts)
```

This permits private notes inside otherwise shared contexts without duplicating the shared Event/Plan/other referent.

Digital/IP/copyright ownership is not established by Content Artifact v0.

---

# 8. Correction, derivation and deletion

Current state and historical state remain distinct. Correction must not silently overwrite materially consequential prior content states.

Independent copy/fork can create a distinct Artifact where continuity no longer truthfully describes the content lifecycle. Derivation history remains reconstructible where consequential.

Retention/deletion of raw representations or content must not manufacture false historical truth or allow retained Provenance to reconstruct content that is no longer authorised to remain accessible.

---

# 9. Anti-overmodeling boundary

Content Artifact identity is **not required** merely because data can be rendered or serialized.

Therefore ordinary structured LifeOS referents do not become Content Artifacts just because they can be exported, and transient uploads used only for one processing step need not create Artifact identity.

Not accepted by this semantic review:

- universal `Document` / `File` / `Content` superclass;
- universal folder/workspace/document-management hierarchy;
- one Artifact per upload automatically;
- blob-store, MIME, OCR, indexing or provider-sync persistence model;
- SQL/API/storage shape;
- specialist legal-document, credential, eDiscovery or regulated-retention ontology.

---

# 10. Canonical hardenings

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

Normative validation: `../checkpoints/content-artifact-v0-validation.md`.