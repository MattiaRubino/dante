# Repository Engineering Safety

- Status: **CURRENT — FRONTEND GATE CALIBRATION COMPLETE / PROMOTION DOCUMENTED / GITHUB APPLY PENDING**
- Repository: `MattiaRubino/dante`
- Default branch: `main`
- Main ruleset: `lifeos-main-safety`
- Backend CP4: **CLOSED / DIRECT REMOTE QA PASS**
- Backend scaffold: **CLOSED / integrated via PR #24**
- Frontend materialization: **CLOSED / PASS — FM-00..FM-07**
- Frontend integration hardening: **ACTIVE — PR #28**

## Purpose

Repository enforcement must match DANTE engineering policy without fake review ceremony, guessed check names or unproven gates.

```text
DOCUMENTED POLICY != GITHUB CONTROL ACTUALLY APPLIED
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
```

A repository-side control is called effective only after direct evidence exists and the GitHub setting itself has been applied. Connector limitations are recorded rather than converted into false PASS.

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

## Current protected-main posture — effective GitHub state before this UI promotion

The effective `lifeos-main-safety` ruleset currently requires:

```text
main deletion                         blocked
main force push / non-fast-forward   blocked
pull request before merge            required
required approving reviews           0
review-thread resolution             required
allowed merge method                 merge
required checks                      Backend CI Gate
                                     Dependency Review
required-check source                GitHub Actions
branch up to date                    required
merge queue                          not enabled
```

Zero approvals remains intentional while one regular maintainer exists. Add real human-review enforcement only when independent ownership/review responsibility exists.

The branch-local canonical ruleset definition now stages the already-calibrated `Frontend CI Gate` as the third required context. That JSON is desired repository state; until the owner applies the one-time GitHub ruleset UI change and it is verified, this document does **not** claim the third check is effective on protected `main`.

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
required on GitHub main                PENDING OWNER UI APPLICATION
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

The branch-local `docs/development/github-main-ruleset.json` now contains the desired three-check definition. The GitHub ruleset UI must be updated once; afterward repository truth must be reread before this control is called APPLIED.

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

Intended ecosystems after frontend integration:

```text
uv /apps/backend
npm/pnpm workspace /
GitHub Actions /
```

Dependabot proposes updates; Dependency Review evaluates them. Native/framework updates are never auto-accepted merely because Dependabot produced them.

## GitHub Actions full-SHA policy

Repository owner previously enabled full-length Action SHA enforcement. Connector direct readback remains unavailable; current workflows are compatible and pinned to full immutable SHAs.

## CodeQL

CodeQL is not active yet. Accepted post-integration boundary:

```text
TypeScript + Python integrated on main
-> verify current GitHub default setup
-> activate CodeQL default setup
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
active PR #28 integration branch
```

## Merge/history posture

DANTE preserves useful checkpoint/evidence history and permits merge commits. The integration branch preserves the closed frontend history through a real two-parent merge.

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
Frontend CI Gate desired ruleset JSON     STAGED
Frontend CI Gate GitHub ruleset setting   PENDING OWNER UI APPLICATION
CodeQL                                    NOT ACTIVE
```

## Persistent non-claims

Repository safety does not imply complete security assurance, independent human review, production deployment safety, restore/PITR rehearsal, CodeQL PASS, iOS release validation or blanket Physical/PSV PASS.

## Exact next repository-safety step

```text
apply Frontend CI Gate to GitHub ruleset UI
-> verify effective protected-main context
-> ensure PR #28 remains green/current
-> final PR diff/current-docs/accepted-risk review
-> separate protected-main merge authorization
```

Any merge, CodeQL activation or branch deletion remains separately authorized.
