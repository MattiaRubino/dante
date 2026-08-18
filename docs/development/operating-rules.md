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

Current ownership/state:

- Phase 4 Home/Today: relevant Phase-4/UX/prototype/archive/regression paths + `docs/workstreams/today-home.md`; active separately.
- Pre-Physical Repository & Architecture Coherence: **DEFINITIVE CLOSED / FINAL QA PASS / integrated into `main` via PR #13 / POST-MERGE VERIFIED**.
- Physical Model: **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED**; authority lives in `docs/physical-model/**` and `docs/workstreams/physical-model.md`; PM-13 clean-room architecture/documentation QA is PASS; direct selected-stack implementation validation remains carried forward.
- Development Profile v0: **NOT STARTED**; future bounded operational-deployment scope for the genuinely unresolved initial activation/deployment/configuration choices against the already-selected Physical target. It must consume, not reopen, the fixed initial dormant posture for Restate and pgBackRest/AWS S3.
- Backend Foundation: **NOT STARTED / DEFERRED**; future backend bootstrap/config/infrastructure/tests/docs only after separate explicit authorization.
- Domain Model / Domain Atlas: **CLOSED**; historical branch does not reopen semantics.
- Logical Model: **CLOSED**; historical branch does not reopen semantics.

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

For work that depends on the accepted Physical target, also read at minimum:

```text
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

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
- For version-sensitive Physical capability claims, use current official primary documentation and pin product + version + edition + deployment mode where material.
- A marketing/official capability claim is not direct execution evidence; distinguish the two.
- Missing/contradictory implementation evidence becomes `HOLD`, not assumption.
- `SELECTED != DEPLOYED` and `SELECTED != DIRECT PASS`.
- Development Profile v0 must not reopen a current activation decision already fixed by repository truth.
- Restate is selected but **DORMANT / NOT ACTIVE in initial DEV** until a real Class-B durable-workflow need exists; self-hosted vs Cloud EU is decided only when that activation trigger exists.
- pgBackRest + AWS S3 eu-south-1 are selected recovery targets but **DORMANT / NOT ACTIVE in initial DEV** until the recovery/production boundary or a real recovery-rehearsal requirement exists.
- A selected-stack validation failure that invalidates the Physical choice requires an explicit reopen; do not weaken Domain/Logical semantics to force a PASS.

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

The workstream handoff is the live save-game while a workstream is active and the closure handoff/evidence remains the durable resume point after closure.

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

## 8. Physical evidence/status semantics

Use exact result words where applicable:

```text
NOT RUN
PASS
PASS-CONDITIONAL
HOLD
REJECT
SENSITIVITY-DEPENDENT
PREFERRED
SELECTED
```

Additional Physical evidence rules:

```text
nominal benchmark tier != executed dataset
unexecuted HIGH != VERIFIED-RUN
official documentation claim != benchmark execution
brand != benchmark subject
product + version + edition + deployment = benchmark subject
raw evidence before summary
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
```

Current accepted Physical target is selected by PM-11 and accepted by PM-12. Direct selected-stack validation remains explicitly unexecuted where the PSV register says `NOT RUN`.

## 9. Pre-merge coherence gate

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
12. merge only after semantic/documentation coherence.

For Physical closure/integration, also verify PM-11 explicit selection exists, PM-12 accepted target is coherent, PM-13 clean-room QA is PASS, direct `NOT RUN` truth is preserved and the PSV register is carried forward.

A clean Git merge is not enough.

## 10. After-merge protocol

- verify `main` contains intended final versions;
- verify the merge commit and branch relation remotely;
- refresh global status if required;
- update workstream completion/next phase when a separate post-merge alignment scope is needed;
- synchronize long-running overlapping branches;
- old branches/history cease to be authoritative once accepted work is integrated;
- allow repository auto-delete of merged head branches where enabled, except when a branch is intentionally retained for a documented reason.

Historical files need not remain in the current working tree merely to preserve history if Git/ADR/evidence already retains the useful knowledge and deletion is explicitly gated.

## 11. Handoff to another AI/chat

The outgoing workstream records:

- last completed change;
- exact current task and next steps;
- branch/PR;
- important current files;
- validation performed;
- problems/open questions;
- last validated commit where relevant;
- approved/current scope;
- failed/no-op tool operations that affect continuation.

For implementation based on the closed Physical target, the handoff must additionally preserve:

- selected exact product/version subjects where still pinned;
- deployment mode where actually chosen;
- current direct PSV/HG status;
- evidence locations/hashes;
- unresolved HOLD items;
- any explicit Physical reopen trigger.

If critical continuation state exists only in conversation, the handoff is incomplete.

## 12. Repository coherence baseline

The Pre-Physical workstream started from `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`, completed Phase 0–12 plus independent total audit and exact final activation QA, integrated through protected PR #13, then received post-merge current-truth alignment through PR #14.

The Physical workstream started from:

```text
main
3de84bb49f9cef30e88e9bde4961ed84335daa79

branch
feature/physical-model
```

It completed PM-00..PM-14 at the target-architecture layer, selected PostgreSQL 18.4 as canonical primary and established the bounded target companion stack documented in PM-11/12.

Future contributors must re-check current refs rather than treating dated SHAs as permanently current `main`.

## 13. Current stage boundary

```text
DOMAIN
CLOSED / unchanged

LOGICAL
CLOSED / WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS
INTEGRATED / POST-MERGE VERIFIED

PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PM-13 clean-room architecture/documentation QA PASS
selected canonical primary PostgreSQL 18.4

DIRECT SELECTED-STACK VALIDATION
NOT STARTED / carried forward

BACKEND
NOT STARTED / DEFERRED

DEVELOPMENT PROFILE v0
NOT STARTED / next separate operational scope
Restate initial DEV posture FIXED = DORMANT UNTIL REAL CLASS-B NEED
pgBackRest + AWS S3 initial DEV posture FIXED = DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY
```

No production backend/API/Auth implementation is authorized solely by Physical closure.

## 14. Mandatory execution hardening

The agent operating manual is authoritative for:

- exact Git gate + PRE-SCOPE;
- re-fetch before first real write;
- exact post-write physical-path QA;
- no scope expansion;
- current-truth vs historical-evidence distinction;
- knowledge-coverage gate before stale-doc replace/delete;
- no connector/context-limit knowledge loss;
- truthful tool-failure reporting;
- remote evidence for PASS/CLOSED;
- Domain Validation Methodology v3 for any separately authorized Domain reopen/new validation.

The repository engineering safety contract additionally governs effective main rules/settings and branch hygiene.

The closed Physical methodology/evidence additionally governs:

- exact selected target ownership boundaries;
- `SELECTED != DIRECT PASS`;
- honest direct PSV status;
- explicit reopen if selected-stack implementation evidence invalidates a decision;
- Development Profile choices must not silently change the accepted target or reopen already-fixed initial activation posture.
