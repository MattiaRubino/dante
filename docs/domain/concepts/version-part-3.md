<!-- LIFEOS-CANONICAL-CONTINUATION document="version.md" follows="version-part-2.md" -->
> **Canonical continuation of the single logical Version / Material-State v0 concept document.** Earlier Version semantics remain preserved. This continuation records Content Artifact integration only.

# 2026-08-16 — Content Artifact material-state boundary

Content Artifact / Document v0 reuses the accepted Version discipline without introducing a new versioning primitive.

Canonical separation:

```text
Content Artifact identity
!= materially relevant Artifact state

technical/provider revision
!= semantic material Version universally

alternate representation/export
!= material Version automatically
```

A materially edited Artifact may remain the same Artifact across V1, V2, V3. A PDF and DOCX may represent the same material state. Provider revision IDs, ETags, storage generations or sync revisions do not define semantic materiality.

Where a Decision, Agreement, Evidence use or another consequential context depends materially on content:

```text
basis at time T
= applicable Artifact material state at T
```

Later edits must not silently rewrite that historical basis.

A copied/derived Artifact may become a new Artifact rather than a new Version when identity/lifecycle diverges. Version does not decide Artifact identity universally; that decision belongs to the owning Content Artifact invariants.

Loss of one representation/provider does not necessarily destroy the Artifact or its material-state continuity if another valid representation/state remains.

Version v0 remains **PASS WITH HARDENING; REOPEN = 0**.

Normative reference: `../checkpoints/content-artifact-v0-validation.md`.