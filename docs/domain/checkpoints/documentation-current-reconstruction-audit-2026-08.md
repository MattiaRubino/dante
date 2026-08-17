# Current Documentation Reconstruction Audit — 2026-08

**Status:** Local reconstruction candidate validated; Git write not yet performed  
**Branch:** `feature/domain-model`  
**Pre-write HEAD:** `0e2f4b621e640421e2d5c9c0dc80fb20ff79b4a0`  
**Current main observed during audit:** `2739e96955974d1273e704905ace03f9ac478e05`

## Purpose

This audit records the preservation-first reconstruction of six current Domain Atlas documents/concepts whose earlier histories contained destructive compaction or incomplete restoration. It exists to make the reconstruction reproducible and to prevent a later editor, chat, or model from treating context-window/tool limits as a reason to discard accepted reasoning.

No Git write is represented by this file until its exact scope is separately approved and written.

## Preservation rule used

The reconstruction deliberately does **not** use `summary + reference` or `current + secondary companion` document classes.

For each logical document:

```text
verified full pre-compaction healthy baseline
+
downstream current sections that contain newer/material text
+
explicit correction of stale operational markers only
=
one reconstructed logical document
```

If the resulting logical document is long, it is split only physically:

```text
part 1
part 2
part 3
...
```

All parts have equal canonical authority and explicit navigation. They are not summaries, references, appendices of lower authority, or separate concepts. Removing the generated split navigation preambles and concatenating the payloads in order must reproduce the reconstructed unsplit document exactly.

## Verified source blobs

The following local source files were rechecked with `git hash-object` before reconstruction and matched the expected Git blob SHAs exactly:

- `/docs/domain/language-map.md	healthy	1e234392b212c7a414952948eef2605a7db2fde6	342ccfa5eebef88d2096464a68f37fe588774449`
- `/docs/domain/language-map.md	current	feature/domain-model	662d8558f7925378bae93d6c958ad78b3b602da6`
- `/docs/domain/README.md	healthy	8084a4ab3defe025017fc2fcb8d4235a808bb9fa	6064b9bd11435aeeebdf1725d832233ca79824a6`
- `/docs/domain/README.md	current	feature/domain-model	8ff1fa1411193208d34aa1ff375fa9cca633f75b`
- `/docs/workstreams/domain-model.md	healthy	840651cc14c1f7bb0a0adf3396692b8f55deca94	9af85b948b4791dd67035f710d7bca4ff08f57ae`
- `/docs/workstreams/domain-model.md	current	feature/domain-model	bc788c6fed2cd5e340e5bf7327ef537ad1d06c4c`
- `/docs/domain/multi-actor-readiness-v1.md	healthy	a9ca753c07d35c65177d5c42361d1b1bd48f32bd	97606d0b3480fd8e352386f1cb66909ddf206d0d`
- `/docs/domain/multi-actor-readiness-v1.md	current	feature/domain-model	bb6838d85724e687a67376fcf79c663942159007`
- `/docs/domain/concepts/responsibility.md	healthy	cb6d7f3353882f0fd1d9ff39acfe072d5981538b	a5d033fdd48f3323ebc065bc88b1636cf6012b50`
- `/docs/domain/concepts/responsibility.md	current	feature/domain-model	6c551224df242603122db95fbd2fab43832f6c57`
- `/docs/domain/concepts/participation.md	healthy	61d06c4ad695fa40f0668af15f74b8e746ec2fa1	562fec6b849d027bdf2ef9495e370dd009081243`
- `/docs/domain/concepts/participation.md	current	feature/domain-model	9b68452c67e1d91941d151f6e2c6343fa15762b5`

## Reconstruction accounting

- `README.md`: healthy 996 lines; current 654 lines; reconstructed 1651 lines; included current sections 17; skipped only sections whose non-heading blocks were already present verbatim: 0.
- `language-map.md`: healthy 2189 lines; current 671 lines; reconstructed 2865 lines; included current sections 20; skipped only sections whose non-heading blocks were already present verbatim: 0.
- `domain-model.md`: healthy 781 lines; current 438 lines; reconstructed 1233 lines; included current sections 13; skipped only sections whose non-heading blocks were already present verbatim: 0.
- `multi-actor-readiness-v1.md`: healthy 1141 lines; current 367 lines; reconstructed 1515 lines; included current sections 18; skipped only sections whose non-heading blocks were already present verbatim: 0.
- `responsibility.md`: healthy 1033 lines; current 1031 lines; reconstructed 1401 lines; included current sections 14; skipped only sections whose non-heading blocks were already present verbatim: 22.
- `participation.md`: healthy 1102 lines; current 1045 lines; reconstructed 1604 lines; included current sections 18; skipped only sections whose non-heading blocks were already present verbatim: 18.

The section-selection rule is conservative: a downstream current H1 section is included in full whenever any non-heading content block in that section is not already present verbatim in the healthy baseline. This preserves heading/list/example context instead of extracting isolated sentences.

## Intentional current-state corrections

Only stale operational/navigation statements were corrected rather than preserved as active current instructions:

1. `docs/domain/README.md`: the stale link to `docs/domain/concepts/relationship.md` is replaced with the authoritative `checkpoints/relationship-v0-validation.md` target because the concept file does not exist by design.
2. `docs/domain/README.md`: obsolete instructions to remove the already-deleted technical probe are replaced with the current state: probe cleanup is complete; current-document reconstruction and the separately gated `main` synchronization remain.
3. `docs/domain/language-map.md`: obsolete wording that final QA still waits on probe removal is updated to record probe cleanup and historical-preservation completion.
4. `docs/workstreams/domain-model.md`: stale pre-scope/current-task markers are updated from the earlier cleanup checkpoint to the actual pre-reconstruction HEAD and current reconstruction gate.

The superseded text remains reconstructible from Git history and the exact current-source blobs listed above; the current document does not keep obsolete instructions active merely for byte preservation.

## Physical split result

- `README.md` → 3 physical parts; reconstructed unsplit 1651 lines; payload parts: 556, 548, 547
- `domain-model.md` → 2 physical parts; reconstructed unsplit 1233 lines; payload parts: 606, 627
- `language-map.md` → 5 physical parts; reconstructed unsplit 2865 lines; payload parts: 588, 564, 567, 609, 537
- `multi-actor-readiness-v1.md` → 3 physical parts; reconstructed unsplit 1515 lines; payload parts: 499, 500, 516
- `participation.md` → 3 physical parts; reconstructed unsplit 1604 lines; payload parts: 526, 546, 532
- `responsibility.md` → 3 physical parts; reconstructed unsplit 1401 lines; payload parts: 457, 484, 460

Each part begins with a machine-readable `LIFEOS-CANONICAL-SPLIT` marker, a plain statement that all parts form one authoritative document, navigation to every sibling part, and a `LIFEOS-CANONICAL-PAYLOAD` marker separating generated navigation from canonical payload.

## QA contract and result

Local QA after reconstruction and split:

```text
12 / 12 source blobs              exact SHA PASS
6 / 6 healthy baselines           preserved as exact byte prefix PASS
current downstream block account  PASS
changed current sections          preserved with structural context PASS
physical split round-trip         exact for all 6 logical documents PASS
split navigation                  PASS
Markdown fence balance            PASS
old summary/reference design      absent PASS
Relationship fake concept link    absent PASS
probe current-state correction    PASS
semantic closure assertions       PASS
placeholders                       none introduced
```

The comprehensive automated run completed with **147 PASS / 0 FAIL** before this audit file was added. A final candidate-scope QA must be rerun after adding this audit and again after any Git write.

## Relationship special case

`Relationship v0` is intentionally not represented by `docs/domain/concepts/relationship.md`.

Its authoritative current modeling result is the checkpoint-backed typed/specific relationship discipline in:

- `docs/domain/checkpoints/relationship-v0-validation.md`

The reconstruction must not invent the missing concept file merely for index symmetry.

## Repository-state boundary

This reconstruction does not synchronize `main`, does not close final Reconciliation branch QA, and does not select the next Relationships / Reasoning candidate.

Required sequence remains:

```text
current-document reconstruction write + post-write QA
↓
separate main-sync approval/write
↓
semantic freshness/coherence review
↓
final Reconciliation QA
↓
fresh candidate re-score
```

## Out of scope

No changes are intended to:

- `main`;
- backend implementation;
- SQL/migrations;
- API contracts;
- authentication/authorization implementation;
- prototype/UI branches;
- unrelated concepts/checkpoints;
- historical full-record preservation files already committed;
- Reconciliation concept/checkpoint content itself.
