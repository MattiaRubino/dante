# Repository Engineering Safety

- Status: **CURRENT — FRONTEND MATERIALIZATION + INTEGRATION CLOSED / REQUIRED-CHECK PROMOTION OWNER-CONFIRMED**
- Repository: `MattiaRubino/dante`
- Default branch: `main`
- Main ruleset: `lifeos-main-safety`
- Backend CP4: **CLOSED / DIRECT REMOTE QA PASS**
- Backend scaffold: **CLOSED / integrated via PR #24**
- Frontend materialization: **CLOSED / PASS — FM-00..FM-07**
- Frontend integration hardening: **CLOSED / integrated via PR #28**

## Purpose

Repository enforcement must match DANTE engineering policy without fake review ceremony, guessed check names or unproven gates.

```text
DOCUMENTED POLICY != GITHUB CONTROL ACTUALLY APPLIED
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
```

A repository-side control is called effective only after direct evidence exists and the GitHub setting itself has been applied. Where the connector cannot directly read an administrative setting, owner/admin application is recorded explicitly as owner-confirmed rather than misrepresented as API-verified.

## Persistent operating rules

```text
main = one integrated source truth
normal work = bounded branch
integration = pull request
exact write gate before remote mutation
no force-push of shared history for cosmetic cleanup
remote evidence required before PASS / CLOSED
branches != environments
```

## Current protected-main posture — owner-confirmed GitHub state

The repository owner has confirmed applying the staged `Frontend CI Gate` promotion in the `lifeos-main-safety` ruleset. The GitHub connector available to this workstream does not expose direct ruleset readback, so the administrative application is classified **OWNER-CONFIRMED / DIRECT API READBACK UNAVAILABLE**, not independently API-verified.

The protected-main policy is therefore recorded as:

```text
main deletion                         blocked
main force push / non-fast-forward   blocked
pull request before merge            required
required approving reviews           0
review-thread resolution             required
allowed merge method                 merge
required checks                      Backend CI Gate
                                     Dependency Review
                                     Frontend CI Gate
required-check source                GitHub Actions
branch up to date                    required
merge queue                          not enabled
```

Zero approvals remains intentional while one regular maintainer exists. Add real human-review enforcement only when independent ownership/review responsibility exists.

The canonical definition in `docs/development/github-main-ruleset.json` matches this intended three-check state. Administrative application was confirmed by the repository owner after the calibrated promotion decision; connector limitations remain an evidence boundary, not a reason to invent direct verification.

## Backend CI calibration — established precedent

Backend CP4 directly proved on PR #24:

```text
GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS

DELIBERATE RED
Backend Quality       FAILURE — intentional
Backend PostgreSQL    SUCCESS — independent path preserved
Backend CI Gate       FAILURE — mandatory failure propagated
Dependency Review     FAILURE — intentional dependency policy denial

RECOVERY GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

Only after that sequence were `Backend CI Gate` and `Dependency Review` promoted.

## Required-check promotion protocol

Permanent protocol:

```text
real workflow/job exists
+ runs on relevant PR
+ exact emitted context observed
+ real green observed
+ bounded deliberate failure observed
+ failure means merge must stop
+ exact intended configuration restored
+ recovery green observed
-> separate explicit ruleset mutation may promote context
```

Never promote a guessed or documentation-only check name.

## Frontend CI Gate calibration — COMPLETE

Frontend workflow structure:

```text
Frontend CI
├── Quality
├── Web E2E
├── Mobile Bundle
└── Frontend CI Gate
```

Hardening includes:

- workflow default `permissions: {}`;
- `contents: read` only on checkout jobs;
- `persist-credentials: false`;
- immutable full-SHA Action pins;
- exact Node 24.19.0 / pnpm 11.22.0 bootstrap;
- frozen install;
- format/lint/strict TS/architecture/generated/unit/build;
- Web Chromium E2E;
- Expo compatibility check;
- Android Hermes bundle smoke;
- tracked and untracked repository-mutation detection;
- aggregate gate over all mandatory frontend jobs.

### Real green

PR #28 current-truth candidate `79b55b3a1986cc910af0ce84df411314e8453e80` observed:

```text
Dependency Review   PASS
Backend CI Gate     PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### Deliberate red

Commit `6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8` added one temporary workflow-only `exit 1` in Quality.

Observed remotely:

```text
Quality             FAILURE — intentional
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    FAILURE — mandatory failure propagated
Backend CI          PASS
Dependency Review   PASS
```

No product source, dependency or security policy was weakened.

### Exact restore and recovery green

Recovery commit:

```text
02ee9034f37000819afb2c27b0bd826b128f69b5
```

The workflow was restored to the exact previously-green blob:

```text
14626e696d91d3f184b58dac111cd88102832e91
```

Hosted recovery result:

```text
Dependency Review   PASS
Backend CI          PASS
Backend CI Gate     PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

Therefore:

```text
Frontend CI Gate context emitted       PASS
real green                              PASS
deliberate-red failure propagation     PASS
exact restoration                      PASS
recovery green                         PASS
eligible for required-check promotion  YES
required on GitHub main                OWNER-CONFIRMED / DIRECT API READBACK UNAVAILABLE
```

## Frontend required-check promotion decision

Promotion is approved for exactly:

```text
Frontend CI Gate
source / integration: GitHub Actions
integration_id: 15368
```

Retain exactly:

```text
Backend CI Gate
Dependency Review
strict branch-up-to-date policy
PR-before-merge
0 required approvals
review-thread resolution
merge commits only
main deletion protection
non-fast-forward / force-push protection
```

The canonical `docs/development/github-main-ruleset.json` contains the desired three-check definition. The repository owner confirmed applying the corresponding GitHub ruleset UI change. Because the connector cannot directly read rulesets, this administrative fact remains classified owner-confirmed rather than independently API-verified.

## Frontend protected-main integration — VERIFIED

PR #28 integrated the closed frontend materialization and bounded hardening into protected `main`.

```text
final PR head        a6607ceabd35f874dc9e5f63fe8f57f71a92bf80
prior main           fd3bc8dd918cf6aadeff4572221af68612c3cb42
merge commit         f1aacb0724088e0b4b086008a5219c2fba5ce0cf
PR #28               MERGED
merge parentage      PASS — exactly prior main + final PR head
merged tree identity PASS — 0 file delta from final PR head to merged main tree
```

The final PR head directly passed Dependency Review, Backend Quality, Backend PostgreSQL, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate before merge.

The available connector's commit-workflow lookup exposes PR-associated runs only. Push-main CI for `f1aacb...` is therefore **DIRECT READBACK UNAVAILABLE** and is not inferred PASS.

The integration branch was observed absent after merge. No manual branch deletion was performed during the merge operation; do not invent an auto-delete cause or recreate the branch without a new explicit gate.

## Dependency Review posture

Dependency Review remains fail-closed:

```text
fail-on-severity   moderate
fail-on-scopes     runtime, development, unknown
comment writing    disabled
```

Only these exact temporary transitive-tooling advisories are allowed:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
GHSA-w5hq-g745-h8pq
```

Accepted-risk review deadline: **2026-09-23**.

The first two are `image-size` through Metro build/development asset processing. The third is `uuid@7.0.3` through Expo/Xcode configuration tooling. Full paths, exposure classification and removal triggers live in `../workstreams/frontend-materialization-integration.md`.

This is not warn-only, severity reduction, scope reduction, global suppression or an unsupported Expo/Metro/uuid override.

## Dependabot

Current ecosystems after frontend integration:

```text
uv /apps/backend
npm/pnpm workspace /
GitHub Actions /
```

Dependabot proposes updates; Dependency Review evaluates them. Native/framework updates are never auto-accepted merely because Dependabot produced them.

## GitHub Actions full-SHA policy

Repository owner previously enabled full-length Action SHA enforcement. Connector direct readback remains unavailable; current workflows are compatible and pinned to full immutable SHAs.

## CodeQL

CodeQL is not active yet. The post-integration activation candidate is now eligible for a fresh explicit gate:

```text
TypeScript + Python integrated on main
-> verify current GitHub default setup
-> activate CodeQL default setup under separate authorization
-> observe real findings/contexts
-> classify/fix findings
-> consider required promotion separately
```

Do not create a custom CodeQL workflow merely to duplicate supported default setup.

## CODEOWNERS / reviews

`CODEOWNERS` remains intentionally absent while one regular maintainer exists. Revisit only when distributed ownership or independent review becomes real.

## SECURITY.md

Public vulnerability intake remains deferred until public production/release makes the process operationally meaningful; it is explicitly carried in the future activation register.

## Branch hygiene

Delete branches only after proving:

```text
unique accepted work not integrated   0
active work owned by branch           0
required evidence preserved           PASS
```

Relevant truth:

```text
feature/backend-scaffold
closed / integrated via PR #24

feature/frontend-materialization
closed evidence / FM-00..FM-07 PASS

chore/frontend-materialization-integration
closed / integrated via PR #28
observed absent after merge
manual deletion during merge operation: NO
```

## Merge/history posture

DANTE preserves useful checkpoint/evidence history and permits merge commits. PR #28 preserved the closed frontend history and was merged using the accepted two-parent merge posture.

The final protected-main merge commit `f1aacb0724088e0b4b086008a5219c2fba5ce0cf` has exactly the expected two parents and the same tree as final PR head `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80`.

## Current verification classification

```text
main deletion protection                  PASS / preserved
main force-push protection                PASS / preserved
PR-before-merge                           PASS / preserved
review-thread resolution                  PASS / preserved
required approvals                        0 / intentional
Backend CI Gate required                  APPLIED
Dependency Review required                APPLIED
branch-up-to-date requirement             APPLIED
Frontend CI Gate real green               PASS
Frontend CI Gate deliberate red           PASS
Frontend CI Gate failure propagation      PASS
Frontend CI Gate exact restore            PASS
Frontend CI Gate recovery green           PASS
Frontend CI Gate promotion decision       APPROVED
Frontend CI Gate desired ruleset JSON     UPDATED
Frontend CI Gate GitHub ruleset setting   OWNER-CONFIRMED APPLIED
Frontend CI Gate direct ruleset readback  UNAVAILABLE IN CONNECTOR
PR #28                                    MERGED
PR #28 merge parentage                    PASS
PR #28 merged tree identity               PASS
PR #28 exact-head hosted CI               PASS
PR #28 push-main CI readback              UNAVAILABLE IN CONNECTOR
CodeQL                                    NOT ACTIVE
```

## Persistent non-claims

Repository safety does not imply complete security assurance, independent human review, production deployment safety, restore/PITR rehearsal, CodeQL PASS, iOS release validation or blanket Physical/PSV PASS.

## Exact next repository-safety step

```text
CodeQL default setup evaluation
-> fresh explicit branch/write gate
-> observe real findings/contexts
-> consider any required-check promotion separately
```

Backend Concrete Logical -> PostgreSQL and first product vertical work remain separately gated. Any CodeQL activation, branch recreation/deletion, ruleset mutation or product/backend implementation requires separate authorization.