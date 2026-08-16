<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-16.md" -->
> **Canonical continuation of the single logical Domain Language Map.** Earlier language mappings remain preserved; this continuation records Content Artifact / Document terminology only.

# 2026-08-16 — Content Artifact / Document language

Canonical domain term:

```text
Content Artifact
```

Meaning:

> scoped native information-content referent whose reusable identity materially matters across LifeOS contexts independently from one storage representation/provider/use.

Preferred bounded product/kind vocabulary where truthful:

```text
Document
Note
Image
Recording
Transcript
```

These terms do not imply separate universal kernel roots.

Canonical distinctions:

```text
Content Artifact != Asset
Content Artifact != file/blob
Content Artifact != Attachment
Content Artifact != Evidence
Content Artifact != Provenance
Content Artifact != Observation
Content Artifact != Version
```

`Attachment` means contextual attachment/link use, not the content's native identity.

`file`, `blob`, `provider object`, `URL`, `path`, `MIME type` belong to representation/access/storage vocabulary unless a later implementation stage defines a more specific technical contract.

Use `material state` / `Version` for consequential semantic content state, not provider revision IDs by default.

Use `derived from` / Provenance for lineage. Do not call an independently evolving copy merely a `version` unless identity continuity is actually established.

Do not use `document` as a universal synonym for every serializable LifeOS object.

Normative reference: `checkpoints/content-artifact-v0-validation.md`.