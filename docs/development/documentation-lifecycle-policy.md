# DANTE Documentation Lifecycle Policy

- **Status:** CURRENT / NORMATIVE
- **Applies to:** repository documentation lifecycle, branch handoffs, historical material, split-document compaction
- **Introduced:** 2026-08-26

## 1. Goal

DANTE documentation must make the current project understandable without forcing a reader, AI agent or developer to reconstruct obsolete operational chronology.

The working tree should contain current authority, durable reference material and evidence that still has continuing value. Git remains the complete recoverable history.

The governing rule is:

```text
current truth stays current
valuable evidence stays identifiable
branch-operational chatter does not leak into main
knowledge is never discarded silently
```

## 2. Documentation classes

Every documentation artifact belongs to one of these classes.

### CURRENT / AUTHORITATIVE

Current product, architecture, database, engineering or project-state truth.

These documents must describe the present directly. They must not require reading a chronological chain of obsolete amendments to reconstruct current meaning.

### REFERENCE / CONTRACT

Durable normative material such as accepted architecture contracts, constitutions, ADR-backed doctrine, database reference and other long-lived constraints.

### EVIDENCE / VALIDATION

Audits, checkpoints, research, acceptance records and validation results that explain or prove why current decisions were accepted.

Historical evidence must be labelled as historical/evidentiary and must never override newer current truth.

### BRANCH-OPERATIONAL HANDOFF

Temporary save-game material used only while a branch/workstream is active.

This includes live handoffs, session handoffs, resume notes and context-transfer files created because a chat, tool session or agent context may end.

### BRANCH HISTORY / CLOSURE RECORD

One consolidated final narrative for a completed branch/workstream when retaining a human-readable branch history has continuing value beyond Git/PR history.

### PURE HISTORY / DUPLICATE

Material whose only remaining purpose is chronology already recoverable from Git and which contains no unique current truth, durable rationale, requirement or evidence worth retaining in-tree.

## 3. Main-branch rule for handoffs

Protected `main` must not contain active or temporary branch-operational handoffs.

Forbidden on merged `main` as current repository artifacts:

```text
live-handoff-*
session-handoff-*
resume-handoff-*
chat-transfer-*
other equivalent temporary save-game files
```

During an active branch, temporary handoffs are allowed when they materially improve continuity. They remain branch-local operational artifacts.

Before merge, the branch performs a handoff consolidation gate:

```text
all temporary branch handoffs
        ↓
knowledge-coverage review
        ↓
current truth propagated to current docs
rationale propagated to ADR/reference where required
evidence propagated to durable validation/evidence records where required
        ↓
optional ONE branch history / closure record
        ↓
temporary handoffs removed
```

A branch must not merge a pile of live/session handoffs into `main` merely because they were useful during execution.

## 4. One consolidated branch-history rule

When a completed branch has enough continuing historical value to justify an in-tree narrative, retain at most one consolidated branch history/closure document for that branch/workstream.

The record should summarize navigation and chronology while preserving references to the durable artifacts and Git/PR evidence. It is not a substitute for current documentation.

Recommended content:

```text
branch/workstream identity
scope and purpose
starting/main anchor where relevant
major milestones and material decisions
important repairs or failed paths worth remembering
final accepted implementation/closure state
validation and CI evidence
merged PR / merge commit when applicable
where current truth now lives
```

Do not duplicate full current specifications inside the branch-history document.

If the branch history has no continuing value beyond normal Git/PR history, retain no additional history document.

## 5. Archive policy

`docs/archive/` is optional historical visibility, not a second source of truth and not a dumping ground.

Archive only historical material that remains useful to inspect directly in the working tree but is no longer current authority.

Every archived artifact is:

```text
NON-AUTHORITATIVE
HISTORICAL / EVIDENCE ONLY
```

Do not create backup copies of current files in `docs/archive/` before editing them. The pre-change Git commit already provides the exact immutable backup.

Do not archive pure duplicates merely to avoid deleting them. If Git history is sufficient and knowledge coverage passes, remove the obsolete working-tree file.

## 6. Knowledge-coverage gate before move, merge or deletion

Before a stale, split or temporary document is removed, moved, compacted or replaced, every meaningful statement must receive a disposition:

```text
current truth        → current source
normative rule       → reference/contract/ADR as appropriate
rationale            → ADR/reference where continuing value exists
evidence             → evidence/checkpoint/branch history if worth retaining
future requirement   → roadmap/requirement owner
superseded history   → Git history
true duplicate       → discard
```

Required gate:

```text
unclassified meaningful content = 0
valid requirement lost           = 0
current truth represented        = PASS
continuing rationale retained    = PASS
continuing evidence retained     = PASS
references/navigation repaired   = PASS
```

No cleanup operation may trade clarity for silent knowledge loss.

## 7. Frozen/read-only split documents may be compacted

A document that is closed/frozen and expected to be read-only may be recomposed from multiple physical parts into fewer files or one file when doing so improves navigation and tooling.

Compaction is allowed only when the logical payload is preserved losslessly except for content deliberately classified as obsolete, duplicate or no longer useful under the knowledge-coverage gate.

The default compaction contract is:

```text
all still-valid substantive information preserved
all still-useful rationale preserved
all still-useful evidence references preserved
requirements preserved
invariants preserved
accepted decisions preserved
explicit supersession preserved where still needed
```

Compaction must NOT silently:

```text
summarize away detail
paraphrase away requirements
remove inconvenient rationale
collapse distinct invariants
rewrite historical evidence as if it were current execution
invent new semantics
```

Whitespace, navigation wrappers, obsolete status banners, duplicated prose and superseded operational routing may be removed when coverage proves they carry no remaining unique meaning.

## 8. Split by subject, not by chronology, for long-lived current reference

A size/tool-limit split is acceptable when one logical payload is too large for safe transport or editing.

For long-lived current/reference documents, semantic/topic partitions are preferred over endless chronological continuations whenever the document is being deliberately reorganized.

Prefer:

```text
reference/
  identity-and-addressing.md
  state-and-history.md
  integrity.md
  security.md
```

over:

```text
reference-part-17.md
reference-part-18.md
reference-part-19.md
```

when the latter parts merely represent successive amendments rather than an intentional stable partition.

Existing split documents are not automatically defective. Their purpose must be classified before reorganization.

## 9. Current specifications must not become append-only diaries

A current specification must present current truth directly.

Do not preserve a chain such as:

```text
old state
→ amendment
→ amendment
→ correction
→ final correction
```

as the required reading path for understanding the present.

When safe, rewrite the current specification to the final accepted state and retain only the historical rationale/evidence that still deserves a durable home.

## 10. Merge gate for documentation lifecycle

Before a documentation-heavy branch merges to `main`, verify:

- no temporary live/session handoffs remain;
- at most one justified consolidated branch history exists for the workstream;
- current docs contain current truth directly;
- archived material is clearly non-authoritative;
- removed/compacted docs passed knowledge coverage;
- frozen split compaction was lossless for retained substantive information;
- internal links/navigation were repaired;
- Git/PR history remains sufficient for chronology intentionally removed from the tree.
