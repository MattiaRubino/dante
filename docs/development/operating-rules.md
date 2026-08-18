# LifeOS Operating Rules

- Status: Accepted project workflow
- Last updated: 2026-08-18

## Purpose

These rules define where work happens, which source wins when information conflicts, how parallel workstreams avoid overwriting one another, and what every human or AI agent must do before and after modifying LifeOS.

The stricter execution mechanics in [`agent-operating-manual.md`](agent-operating-manual.md) are mandatory and apply together with this file.

Repository-level enforcement and the lifecycle for branch protection/rulesets/required checks/security settings are defined in [`repository-engineering-safety.md`](repository-engineering-safety.md). That file implements this workflow at GitHub level; it does not create a separate source-precedence or branching model.

## 1. Authority order

When two sources disagree, use this order unless a newer accepted decision explicitly supersedes it:

1. current `main` code/migrations/tests and current accepted model/ADR decisions;
2. current durable product/domain/logical/architecture documentation on `main`;
3. active workstream handoff for newer bounded unmerged work;
4. other explicit current files on the active branch inside that workstream;
5. historical evidence, old branches, closed/merged PRs and Git history;
6. conversation memory.

An old/detailed document never overrides newer current truth merely because it contains more prose.

An ADR may preserve original rationale while being superseded/qualified for current execution. Historical checkpoints preserve truthful chronology but are not current execution instructions unless explicitly designated as such.

## 2. Where work happens

- `main` is the only integrated source of truth for accepted project state.
- Normal implementation work uses bounded `feature/*` / `fix/*` branches.
- Documentation/governance/coherence work may use `docs/*` or `chore/*`.
- Exploratory UX/technical experiments may use `prototype/*`.
- One primary branch per workstream where practical.
- Do not work directly on `main` except an explicitly approved emergency repair.
- Changes integrate to `main` through pull requests under the current repository-safety policy.
- Do not bypass an active `main` ruleset merely to avoid normal review/coherence checks.
- DEV/UAT/PROD are environments, not branches.

## 3. Workstream path ownership

Parallel workstreams should avoid shared-file churn.

Current ownership:

- Phase 4 Home/Today: relevant Phase-4/UX/prototype/archive/regression paths + `docs/workstreams/today-home.md`.
- Pre-Physical Repository & Architecture Coherence: exact gated current global/index/architecture/workflow docs + `docs/workstreams/pre-physical-coherence.md` until that branch is integrated/closed.
- Backend Foundation: **not started**; future backend bootstrap/config/infrastructure/tests/docs only after prerequisites are accepted.
- Physical Model: **not started / not authorized**; future work requires its own branch/gate after definitive Pre-Physical closure and separate user authorization.
- Domain Model / Domain Atlas: **closed**; historical branch does not reopen semantics.
- Logical Model: **closed**; historical branch does not reopen semantics.

Shared/current files (`README.md`, `docs/README.md`, `PROJECT-STATUS.md`, `ROADMAP.md`, broad architecture docs, ADRs) change only when global/current truth genuinely changes and exact paths are in an approved gate.

## 4. Start-of-work protocol

Before changes:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read this file + `documentation-and-handoff.md`;
6. read `branching-and-environments.md`;
7. read `repository-engineering-safety.md`;
8. read the complete active workstream handoff;
9. read current model/architecture index and linked current sources;
10. read relevant ADRs/evidence/methodologies;
11. inspect branch/PR and relation to current `main`;
12. inspect relevant implementation/tests before assuming something is missing;
13. check whether the requested decision already exists.

Do not start from an old branch merely because it contains a familiar file.

## 5. During-work protocol

- Stay inside the approved exact write gate.
- Keep the handoff resumable after meaningful milestones.
- Prefer workstream-local progress over repeated global-file churn.
- Do not change closed Domain/Logical semantics implicitly.
- Do not silently replace newer current truth with older material.
- Do not leave important new project knowledge only in chat.
- Do not create schema/provider/cross-cutting conventions solely because an AI suggested them.
- Do not force-push shared history for cosmetic cleanliness.
- Do not treat runtime/technical convenience as new Domain ownership.
- Do not invent required CI/status checks before the real workflow/check context exists and has been validated.
- Do not report an unexecuted benchmark tier/test as verified evidence.
- Do not promote a materially consequential AI behavior change without the applicable versioned/reproducible evaluation required by the current Phase 6 contract.

### Current documentation rule

Current specifications describe **current truth only**. They are not append-only historical logs.

When current truth changes, obsolete prose should be replaced after a knowledge-coverage check. Useful rationale/history belongs in ADRs, checkpoints/evidence or Git.

Historical evidence/checkpoints retain truthful chronology and must not be rewritten to appear current.

Before deleting/replacing stale current documentation, verify:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

## 6. Global-status rule

The workstream handoff is the live save-game.

`docs/PROJECT-STATUS.md` changes only for globally meaningful state such as workstream start/finish/block, durable decision changes, integrated milestones or immediate sequence changes.

The same discipline applies to root README, docs index, roadmap, architecture indexes and ADRs.

Repository settings/rulesets are operational state, not documentation state. A document saying a protection **should** exist is not evidence that it **does** exist; read back the remote setting before declaring the corresponding safety milestone PASS.

## 7. Documentation status semantics

- **Accepted** — durable decision/current baseline at its stated scope; later supersession may qualify it.
- **Current** — authoritative current operational/specification truth.
- **In progress** — active unmerged work.
- **Draft / Proposed** — not accepted.
- **Study / Exploration** — evidence/discovery, not binding implementation truth.
- **Historical / Superseded** — preserved evidence/rationale, not current execution authority.
- **Partially superseded / Qualified** — some decision/rationale remains useful while later sources constrain current effect.

Current navigation should point directly to current truth rather than requiring agents to infer authority from historical files.

## 8. Pre-merge coherence gate

Before merge:

1. compare branch against current `main`;
2. synchronize if needed;
3. inspect shared docs changed by both sides;
4. verify no old decision overwrites newer current truth;
5. verify ADR/model status + supersession/reopen links;
6. verify handoff/tests/validation;
7. update global status only if globally meaningful;
8. check secrets/personal production data/local artifacts;
9. verify any repository-required checks that actually exist are passing;
10. verify blocking review conversations are resolved where active main rules require it;
11. verify branch-specific final closure/evidence activation conditions are satisfied;
12. merge through PR only after semantic/documentation coherence.

A clean Git merge is not enough.

## 9. After-merge protocol

- verify `main` contains intended final versions;
- verify the merge commit and branch relation remotely;
- refresh global status if required;
- update workstream completion/next phase;
- synchronize long-running overlapping branches;
- old branches/history cease to be authoritative once accepted work is integrated;
- allow repository auto-delete of merged head branches where enabled, except when a branch is intentionally retained as active/historical evidence for a documented reason.

Historical files need not remain in the current working tree merely to preserve history if Git/ADR/evidence already retains the useful knowledge and deletion is explicitly gated.

## 10. Handoff to another AI/chat

The outgoing workstream records:

- last completed change;
- exact current task and next steps;
- branch/PR;
- important current files;
- validation performed;
- problems/open questions;
- last validated commit where relevant;
- approved PRE-SCOPE/write state when a gate is in flight;
- failed/no-op tool operations that affect continuation.

If critical continuation state exists only in conversation, the handoff is incomplete.

## 11. Repository coherence baseline

Accepted Pre-Physical workstream base:

```text
main
148a4cb5d5741b4a5b9667cf8d30231ebc0545f0
```

At that base:

- Domain Atlas was closed/integrated via PR #10;
- Logical Model was closed/integrated via PR #11;
- global main alignment was PR #12;
- `chore/pre-physical-coherence` became the bounded architecture/repository-coherence workstream;
- Phase 4 UX remained separate;
- Backend Foundation was not started;
- Physical Model was not started/authorized.

The Pre-Physical branch has since completed Phase 0–12 and is in its independent final-audit closure gate. Future contributors must re-check refs/handoffs rather than treating this dated base as current `main` after integration.

## 12. Current stage boundary — Pre-Physical final closure

Current branch-local state:

```text
DOMAIN
CLOSED / unchanged

LOGICAL
CLOSED / unchanged

PHASE 0–11
PASS

PHASE 12
QA PASS / CLOSED

INDEPENDENT TOTAL AUDIT
CORE PASS
bounded final repairs incorporated / final remote activation QA pending

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND
NOT STARTED / DEFERRED

MAIN INTEGRATION
NOT PERFORMED
```

Until the final audit activation conditions pass:

- no implicit Physical Model;
- no implicit SQL/schema/migrations/API/backend/Auth/provider implementation;
- no implicit Domain/Logical reopen;
- genuine semantic contradiction → record + separate reopen scope;
- architecture/ADR cleanup may replace stale current prose while keeping meaningful rationale/evidence recoverable;
- benchmark preparation/evidence may evaluate technologies without adopting them;
- repository-safety state may be verified without starting production implementation.

After definitive branch-local Pre-Physical closure, `main` integration remains a separate later PR/merge/post-merge QA step.

Active detailed handoff: [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md).

## 13. Mandatory execution hardening

The agent operating manual is authoritative for:

- exact Git gate + PRE-SCOPE;
- re-fetch before first real write;
- exact post-write physical-path QA;
- no scope expansion;
- current-truth vs historical-evidence distinction;
- knowledge-coverage gate before stale-doc replace/delete;
- no connector/context-limit knowledge loss;
- canonical split counting/chronology where evidence genuinely requires it;
- truthful tool-failure reporting;
- remote evidence for PASS/CLOSED;
- Domain Validation Methodology v3 for any separately authorized Domain reopen/new validation.

The repository engineering safety contract additionally governs:

- effective `main` ruleset/protection verification;
- required-check activation only after real stable check contexts exist;
- branch-hygiene deletion only after unique-work classification;
- repository security settings whose state must be verified rather than inferred.