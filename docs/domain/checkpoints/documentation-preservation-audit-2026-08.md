# Documentation Preservation Audit — 2026-08

**Status:** Historical preservation repair record  
**Date:** 2026-08-14  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope commit:** `706327868cc323b4631a2f5ecb7478990a2836c3`

## 1. Purpose

This audit records a documentation-preservation defect discovered while reviewing the Domain Atlas history.

The semantic direction of the affected milestones was generally retained, but several later propagation commits compacted earlier validation records or current-state references too aggressively. In those cases, verdicts and many final boundaries survived while detailed validation procedure, adversarial reasoning, regression criteria, explicit dependency rationale, examples, or post-write QA criteria were removed from the live file.

That is not acceptable for the Domain Atlas audit model.

Canonical preservation rule:

> **When useful documentation becomes too large for a safe single-file workflow, split it into explicitly linked authoritative companions. Never compress away semantic, evidentiary, procedural, or historical information because of transport, tooling, context-window, or document-size constraints.**

This repair is preservation-only. It does not reopen any accepted concept, change any verdict, or make an older snapshot current semantic authority.

---

## 2. Authority rule for preserved records

The files under `docs/domain/history/validation/*-full-record.md` created by this repair are **historical preservation records**.

They are exact Git-blob copies of the identified healthy historical snapshots. Exact copying is deliberate: evidentiary fidelity is stronger than rewriting the historical text merely to add a modern banner.

Therefore:

```text
historical preservation record
!= current semantic authority by itself
```

Current truth must be reconstructed as:

```text
preserved historical validation record
+
explicit later downstream amendments / closures
+
current accepted concept and checkpoint state
```

A dependency shown as open or deferred in a preserved historical record may have been resolved later. The historical wording must not be interpreted as silently reopening a downstream-closed dependency.

The preservation records must remain immutable evidence. If commentary, indexing, or current-status explanation is needed, add it outside the preserved blob rather than editing the historical record in place.

---

## 3. Recovered validation records

| Record | Healthy source ref | Healthy source blob | Compaction / loss point | Recovery classification |
|---|---|---|---|---|
| Responsibility v0 validation | `68b63bd233b116699719e77449db2180338b1bba` | `328f1330d46196750595041f3c3a4227cd2ac952` | `a29d406c28d9ce85dd64b7c1c263b1e767f201de` — common-ground closure | **LOSSY COMPACTION — PRESERVE FULL RECORD** |
| Participation v0 validation | `68b63bd233b116699719e77449db2180338b1bba` | `7429ede311e473b9f6a5c8a6c743569be424e7ad` | `f09559e117a164cf474804a5839ce34ba675ae39` — common-ground closure | **LOSSY COMPACTION — PRESERVE FULL RECORD** |
| Visibility v0 validation | `68b63bd233b116699719e77449db2180338b1bba` | `4b91dda673c110c36a6e88090f298a58c1a26dc8` | `b330d09c6a29a58b8d32099e5ae93352d431f8b4` — Acknowledgement closure | **LOSSY COMPACTION — PRESERVE FULL RECORD** |
| Confirmation v0 validation | `68b63bd233b116699719e77449db2180338b1bba` | `92496f3c5c41117e64e91cd14190e74e19d87866` | `466d4615c33e92c9c9baf867eeae928551e196fd` — common-ground closure | **LOSSY COMPACTION — PRESERVE FULL RECORD** |
| Decision v0 validation | `7b3ba3833d7cecc695fd5462c70412dbe2eed909` | `757edd5dc5a5250685b5b1f41c3baf65e9f9e058` | `233e06d52316a7dac64d928738ffca43c01f9d3e` — Agreement/Consent closure | **HISTORICAL QA CRITERIA REMOVED — PRESERVE PRE-COMPACTION RECORD** |
| Deferred Dependency Closure — Clusters 1–4 v0 | `68b63bd233b116699719e77449db2180338b1bba` | `83109eb050139d1401f6d5211d96b9e50926f10b` | `01e5414d9920f3ea27e7fc2b2d09929fe9928063` — common-ground closure | **LOSSY COMPACTION — PRESERVE FULL RECORD** |

### Why these source refs are safe preservation points

- Responsibility and Participation had already completed their original propagation; their completion commits changed propagation checkboxes rather than deleting the validation body.
- Authority/Visibility work had already occurred by `68b63bd...`; the six selected records were still reconstructible at the required level before the Acknowledgement/common-ground compactions.
- Decision uses the direct parent of the identified lossy Agreement/Consent checkpoint rewrite, not a broader earlier milestone. This preserves the exact original post-write QA gate that was later replaced by a result summary.

---

## 4. What was considered a preservation defect

A later document is not defective merely because it is shorter.

The audit classified a rewrite as lossy only when information with independent audit value disappeared and was not demonstrably preserved elsewhere at equal fidelity, including one or more of:

- individual CORE / multi-actor / cross-concept validation reasoning;
- reductio or adversarial scenarios;
- explicit hardening rationale;
- dependency owner, safety reason, reopening trigger, or rerun tests;
- historical chronology needed to understand why a verdict was reached;
- exact post-write QA criteria used to gate a milestone;
- materially distinct examples or non-collapse guardrails;
- evidence needed to reconstruct the accepted reasoning path.

By contrast, moving detail out of a current concept into an intact checkpoint is **not** information loss. That pattern is acceptable and is the preferred long-document strategy.

---

## 5. Known non-defects / false positives

The audit also identified cases where deletions were legitimate current-state cleanup because the removed detail remained preserved in a normative checkpoint.

Examples include:

- Authority concept cleanup after dependencies were resolved while the original validation checkpoint retained owner/reopen/test detail;
- Confirmation concept downstream updates that added or replaced resolved-neighbor boundaries without deleting the underlying validation record;
- Responsibility and Participation original propagation-completion commits that only flipped required-propagation checkboxes.

The repair must not restore superseded wording into current semantic authority merely because that wording once existed.

---

## 6. Current-state documents requiring a separate split repair

The historical preservation scope does **not** repair the current-state navigation/guardrail files. They require a second bounded scope because the correct result is a structured split, not a rollback.

Confirmed pressure areas:

```text
docs/domain/language-map.md
docs/domain/README.md
docs/domain/multi-actor-readiness-v1.md
docs/workstreams/domain-model.md
```

Known audit anchors include:

- Language Map: major compaction already visible in `8084a4ab3defe025017fc2fcb8d4235a808bb9fa`;
- Domain README: major compaction already visible in `840651cc14c1f7bb0a0adf3396692b8f55deca94`;
- Workstream: significant current-handoff compaction visible in `68b63bd233b116699719e77449db2180338b1bba`;
- Multi-Actor Readiness: later milestone compactions culminate in the Reconciliation propagation at pre-scope HEAD `706327868cc323b4631a2f5ecb7478990a2836c3`.

The follow-up repair must reconstruct current truth forward, preserving every still-valid later hardening from Authority/Visibility through Acknowledgement, Decision, Agreement/Consent, Representation, Version, and Reconciliation.

It must **not** revert those later semantic advances.

---

## 7. Required split pattern going forward

Use this default when a canonical document becomes too large to maintain safely:

```text
small current/index document
        ↓ explicit links
normative concept / checkpoint documents
        ↓ when needed
full validation / evidence / regression / history companions
```

Rules:

1. the current/index file may summarize but must link to the authoritative detailed material;
2. summary text must not become the only surviving copy of validation evidence;
3. historical validation records are append-only or preserved as immutable snapshots;
4. downstream closures are explicit amendments, not silent rewrites of the historical test outcome;
5. current-state documents may be reorganized, but only after a preservation check proves that unique valid content still exists somewhere authoritative;
6. transport/context limits are implementation constraints, not reasons to destroy domain knowledge;
7. no split may create two contradictory current authorities — ownership and precedence must remain explicit.

---

## 8. Scope executed by this preservation repair

Approved scope from pre-scope `706327868cc323b4631a2f5ecb7478990a2836c3`:

### CREATE ONLY

```text
docs/domain/history/validation/responsibility-v0-validation-full-record.md
docs/domain/history/validation/participation-v0-validation-full-record.md
docs/domain/history/validation/visibility-v0-validation-full-record.md
docs/domain/history/validation/confirmation-v0-validation-full-record.md
docs/domain/history/validation/decision-v0-validation-full-record.md
docs/domain/history/validation/deferred-dependency-closure-clusters-1-4-v0-full-record.md
docs/domain/checkpoints/documentation-preservation-audit-2026-08.md
```

No existing file is intentionally changed by this scope.

---

## 9. QA contract

Post-write QA must verify:

```text
changed paths                     = exactly 7
added paths                       = exactly 7
modified paths                    = 0
deleted paths                     = 0
out-of-scope paths                = 0
```

For each of the six historical companions:

- destination blob SHA must equal the healthy source blob SHA listed in Section 3;
- therefore content is byte-identical to the healthy historical source;
- no later downstream file is replaced or rolled back;
- no verdict is changed;
- no dependency is reopened merely by preservation.

The branch ref must advance by a normal fast-forward commit whose parent is exactly the approved pre-scope commit. No force update, history rewrite, reset, or main-branch write is permitted.

---

## 10. Status after this repair

This preservation scope restores durable access to the identified full historical records.

It does **not** declare the broader documentation repair complete. The next documentation scope must repair/split the current README, Language Map, Multi-Actor guardrail, and workstream handoff using the preserved evidence plus all later valid semantics.

Until that second scope passes QA:

```text
historical-record preservation    repaired by this scope
current-state split/repair        still required
semantic concept verdicts         unchanged
REOPEN caused by this audit       0
```
