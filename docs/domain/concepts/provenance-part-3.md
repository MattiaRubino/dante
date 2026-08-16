<!-- LIFEOS-CANONICAL-CONTINUATION document="provenance.md" follows="provenance-part-2.md" -->
> **Canonical continuation of the single logical Provenance v0 concept document.** Earlier Provenance semantics remain preserved. This continuation records Content Artifact integration only.

# 2026-08-16 — Content Artifact boundary

Content Artifact / Document v0 confirms that persistent information-content identity and lineage remain distinct.

```text
Content Artifact != Provenance
```

An Artifact may be a source/input/output in Provenance while retaining independent identity. Provenance may record material derivation, transformation, extraction, import or provider lineage without becoming the Artifact itself.

Canonical examples:

```text
OCR result
→ derived from Artifact A@V2

structured Observation candidate
→ derived from Artifact A@V2

Artifact B
→ derived/copy basis from Artifact A
```

Derivation does not universally imply a later Version of the same Artifact. A copy/fork may become a distinct Artifact where identity/lifecycle diverges.

Provider migration/path change does not replace Artifact identity automatically; Provenance may record that lineage if materially relevant.

Retention/deletion constraints must prevent lineage metadata from becoming a backdoor reconstruction of content no longer authorised to remain accessible.

No universal provenance winner, provider identity or document-lineage root is introduced.

Provenance v0 remains **PASS WITH HARDENING; REOPEN = 0**.

Normative reference: `../checkpoints/content-artifact-v0-validation.md`.