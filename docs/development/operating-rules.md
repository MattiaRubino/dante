# DANTE Operating Rules

- Status: Accepted project workflow
- Last updated: 2026-08-19
- Naming continuity: `LifeOS` may remain in historical evidence, Git history and legacy technical identifiers for the same DANTE product lineage.

## Purpose

These rules define where work happens, which source wins when information conflicts, how parallel workstreams avoid overwriting one another, and what every human or AI agent must do before and after modifying DANTE.

The stricter execution mechanics in [`agent-operating-manual.md`](agent-operating-manual.md) are mandatory and apply together with this file.

Repository-level enforcement and the lifecycle for branch protection/rulesets/required checks/security settings are defined in [`repository-engineering-safety.md`](repository-engineering-safety.md). Engineering implementation structure is defined by the active/accepted Engineering Foundation sources when applicable.

## 1. Authority order

When two sources disagree, use this order unless a newer accepted decision explicitly supersedes it:

1. current `main` code/migrations/tests and current accepted model/ADR decisions;
2. current durable product/domain/logical/architecture/engineering documentation on `main`;
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
- LOCAL/DEV/UAT/PROD are execution/deployment contexts, not long-lived Git branches.

## 3. Workstream path ownership

Parallel workstreams should avoid shared-file churn.

Current ownership/state:

- Phase 4 Home/Today: relevant Phase-4/UX/prototype/archive/regression paths + `docs/workstreams/today-home.md`; active separately.
- Pre-Physical Repository & Architecture Coherence: **DEFINITIVE CLOSED / FINAL QA PASS / integrated via PR #13 / post-merge aligned via PR #14**.
- Physical Model: **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / integrated via PR #15**; authority lives in `docs/physical-model/**` and `docs/workstreams/physical-model.md`; direct selected-stack validation remains carried forward.
- Engineering Foundation v0: **ACTIVE / UNMERGED** on `chore/engineering-foundation-v0`; owns its approved `docs/workstreams/engineering-foundation.md`, `docs/development/*-v0.md` foundation sources and the explicitly gated current-truth alignment files.
- Standalone Development Profile v0: **no longer the next separate phase**; useful operational concerns are absorbed by Engineering Foundation and the actual capability/release boundary that needs them.
- Backend / production application implementation: **NOT STARTED**; begins only after Engineering Foundation closure/integration and a fresh exact implementation scope.
- Domain Model / Domain Atlas: **CLOSED**; historical branches do not reopen semantics.
- Logical Model: **CLOSED**; historical branches do not reopen semantics.

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
9. read current model/architecture/engineering indexes and linked current sources relevant to the task;
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

For implementation after Engineering Foundation acceptance, also read:

```text
docs/development/engineering-foundation-v0.md
and every detailed foundation source relevant to the change
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
- Do not report an unexecuted benchmark/test/PSV item as verified evidence.
- Do not promote a materially consequential AI behavior change without the applicable versioned/reproducible evaluation required by Phase 6.
- For version-sensitive Physical/toolchain capability claims, use current official primary documentation and pin version/edition/deployment mode where material.
- An official capability claim is not direct DANTE execution evidence.
- Missing/contradictory implementation evidence becomes `HOLD`, not assumption.
- `SELECTED != DEPLOYED` and `SELECTED != DIRECT PASS`.
- Restate remains **DORMANT / NOT ACTIVE in initial DEV** until a real Class-B durable-workflow need exists; self-hosted vs Cloud EU is decided only when that activation trigger exists.
- pgBackRest + AWS S3 eu-south-1 remain **DORMANT / NOT ACTIVE in initial DEV** until recovery/production boundary or a real recovery-rehearsal requirement.
- Other selected components activate when their real implementation capability requires them; that is not a technology reopen.
- A selected-stack validation failure that invalidates the Physical choice requires an explicit reopen; never weaken Domain/Logical semantics to force a PASS.
- After Engineering Foundation is accepted, implementation must follow its repository, dependency, environment, migration, testing, config/secrets and CI contracts unless a later explicit decision supersedes them.

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
- **In progress / Active** — bounded work exists but is not yet integrated/closed.
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

Additional evidence rules:

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

The accepted Physical target is selected by PM-11 and accepted by PM-12. Direct selected-stack validation remains explicitly unexecuted where the PSV register says `NOT RUN`.

## 9. Engineering Foundation execution rules

Once accepted/integrated, production engineering uses these baseline rules unless an explicit later decision changes them:

```text
repository           polyglot monorepo
backend              capability-first modular monolith
canonical DB         PostgreSQL 18.4
DB tests             real PostgreSQL, not SQLite substitution
migrations           Alembic release artifacts; no replica auto-migrate-on-start
Python               3.14 line + uv + lockfile + Ruff + mypy + pytest
JS                   Node 24 LTS + pnpm 11 + lockfile + strict TypeScript
CI/CD                GitHub Actions primary orchestration
remote envs          DEV / UAT / PROD, isolated and not Git branches
secrets              external / least privilege / OIDC where supported
release identity     exact source/build/artifact digest where available
```

The exact compute host, exact IaC engine, artifact registry and provider-specific mechanisms remain deferred until a real implementation boundary supplies the missing facts.

No heavy infrastructure such as microservices/Kubernetes/brokers is introduced merely to look enterprise-grade. Such mechanisms require a measured need and an explicit decision.

## 10. Pre-merge coherence gate

Before merge:

1. compare branch against current `main`;
2. synchronize/review if `main` moved materially;
3. inspect shared docs changed by both sides;
4. verify no old decision overwrites newer current truth;
5. verify ADR/model/engineering status + supersession/reopen links;
6. verify handoff/tests/validation appropriate to claimed scope;
7. update global status only if globally meaningful;
8. check secrets/personal production data/local artifacts;
9. verify any repository-required checks that actually exist are passing;
10. verify blocking review conversations are resolved where active main rules require it;
11. verify branch-specific final closure/evidence activation conditions are satisfied;
12. verify exact approved PRE-SCOPE path delta;
13. merge only after semantic/documentation/engineering coherence.

A clean Git merge is not enough.

## 11. After-merge protocol

- verify `main` contains intended final versions;
- verify the merge commit and branch relation remotely;
- refresh global status if required;
- synchronize long-running overlapping branches;
- old branches/history cease to be authoritative once accepted work is integrated;
- allow repository auto-delete of merged head branches where enabled, except when a branch is intentionally retained for a documented reason.

Historical files need not remain in the current working tree merely to preserve history if Git/ADR/evidence already retains useful knowledge and deletion is explicitly gated.

## 12. Handoff to another AI/chat

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

For implementation based on the closed Physical target, the handoff additionally preserves:

- selected exact product/version subjects where still pinned;
- deployment mode where actually chosen;
- current direct PSV/HG status;
- evidence locations/hashes;
- unresolved HOLD items;
- any explicit Physical reopen trigger;
- applicable Engineering Foundation contract and any explicit implementation-stage defer resolved.

If critical continuation state exists only in conversation, the handoff is incomplete.

## 13. Repository coherence baseline

Pre-Physical completed Phase 0–12 plus independent audit, integrated through protected PR #13 and post-merge alignment PR #14.

Physical Model completed PM-00..PM-14 at the target-architecture layer, selected PostgreSQL 18.4 as canonical primary, established the bounded target companion stack in PM-11/12 and integrated through protected PR #15.

The current Engineering Foundation workstream started from:

```text
main / PRE-SCOPE
ebc3616956faeabd99d90f5f32458b284be218e4

branch
chore/engineering-foundation-v0
```

Future contributors must re-check current refs rather than treating dated SHAs as permanently current `main`.

## 14. Current stage boundary

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
selected canonical primary PostgreSQL 18.4

DIRECT SELECTED-STACK VALIDATION
NOT STARTED / carried forward

ENGINEERING FOUNDATION v0
ACTIVE / UNMERGED

BACKEND / PRODUCTION IMPLEMENTATION
NOT STARTED
NEXT AFTER FOUNDATION ACCEPTANCE/INTEGRATION

STANDALONE DEVELOPMENT PROFILE v0
NO LONGER NEXT / absorbed into Foundation + capability/release implementation
```

No production backend/API/Auth/database-schema implementation is authorized solely by Foundation documentation work.

## 15. Mandatory execution hardening

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

Repository engineering safety additionally governs effective main rules/settings and branch hygiene.

Closed Physical authority additionally governs:

- exact selected target ownership boundaries;
- `SELECTED != DIRECT PASS`;
- honest direct PSV status;
- explicit reopen if selected-stack implementation evidence invalidates a decision.

Engineering Foundation additionally governs, once accepted:

- repository/application structure;
- environment/promotion contract;
- configuration/secrets;
- toolchain/reproducibility;
- migration discipline;
- testing/CI/CD/supply-chain baseline.
