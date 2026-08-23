# Repository Engineering Safety

- Status: **CURRENT — BACKEND REQUIRED CHECKS ACTIVE / FRONTEND GATE CALIBRATION ACTIVE**
- Repository: `MattiaRubino/dante`
- Default branch: `main`
- Main ruleset: `lifeos-main-safety`
- Backend CP4: **CLOSED / DIRECT REMOTE QA PASS**
- Backend scaffold: **CLOSED / integrated via PR #24**
- Frontend materialization: **CLOSED / PASS — FM-00..FM-07**
- Frontend integration hardening: **ACTIVE — PR #28**

## Purpose

Make repository enforcement match documented DANTE engineering policy without fake review ceremony, guessed check names or unproven security gates.

```text
DOCUMENTED POLICY != GITHUB CONTROL ACTUALLY APPLIED
WORKFLOW EXISTS != TRUSTED CHECK
TRUSTED CHECK != REQUIRED CHECK UNTIL CALIBRATED
```

A repository-side control is recorded as effective only after direct evidence exists. Connector limitations are stated instead of converted into false PASS.

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

## Current protected-main posture

The `lifeos-main-safety` ruleset currently enforces:

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
Backend PostgreSQL    SUCCESS — independent diagnostic preserved
Backend CI Gate       FAILURE — mandatory failure propagated
Dependency Review     FAILURE — intentional dependency policy denial

RECOVERY GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

Only after that sequence were `Backend CI Gate` and `Dependency Review` promoted to required checks.

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

## Frontend CI current state

Frontend materialization directly proved the hosted workflow before integration. PR #28 now exercises the combined repository candidate.

Current frontend workflow structure:

```text
Frontend CI
├── Quality
├── Web E2E
├── Mobile Bundle
└── Frontend CI Gate
```

Current hardening includes:

- workflow default `permissions: {}`;
- `contents: read` only on checkout jobs;
- `persist-credentials: false`;
- full immutable Action SHA pins;
- exact Node 24.19.0 / pnpm 11.22.0 bootstrap;
- `pnpm install --frozen-lockfile`;
- format/lint/strict TS/architecture/generated/unit/build;
- Web Chromium E2E;
- Expo `install --check` compatibility;
- Android Hermes bundle smoke;
- tracked **and untracked** repository-mutation detection;
- aggregate `Frontend CI Gate` depending on all mandatory frontend jobs.

Real PR #28 candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06` observed:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

`Frontend CI Gate` is therefore a real emitted green context, but **NOT REQUIRED** on `main` yet.

Still pending:

```text
controlled deliberate red
-> prove mandatory upstream frontend failure propagates to Frontend CI Gate
-> restore intended workflow
-> recovery green
-> separate ruleset-promotion decision
```

## Dependency Review posture

Dependency Review is repository-wide and remains fail-closed at:

```text
fail-on-severity   moderate
fail-on-scopes     runtime, development, unknown
comment writing    disabled
```

PR #28 introduced the real pnpm dependency graph and surfaced three transitive tooling advisories that cannot currently be repaired safely within the qualified Expo graph without unsupported overrides.

Only these exact advisory IDs are temporarily allowed:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
GHSA-w5hq-g745-h8pq
```

Accepted-risk review deadline:

```text
2026-09-23
```

The first two belong to `image-size` reached through Metro build/development asset processing. The third belongs to `uuid@7.0.3` reached through Expo/Xcode configuration tooling. Detailed dependency paths, exposure analysis and removal triggers are authoritative in `../workstreams/frontend-materialization-integration.md`.

This is deliberately **not**:

```text
warn-only
severity reduction
scope reduction
global vulnerability suppression
forced Metro/Expo override
forced uuid multi-major override
```

Remove/requalify an exception as soon as the qualified dependency graph no longer needs it, a safe patched path becomes available, or a newly activated DANTE path changes exposure.

## Dependabot

Current intended ecosystems after frontend integration hardening:

```text
uv /apps/backend
npm/pnpm workspace /
GitHub Actions /
```

Dependabot proposes updates; Dependency Review evaluates dependency changes in PRs. Native/framework dependency updates are never auto-accepted merely because Dependabot produced them.

## GitHub Actions full-SHA policy

Repository owner previously enabled the Actions setting requiring full-length commit SHA pins.

Evidence classification remains:

```text
owner/admin application         confirmed by owner
connector direct readback       unavailable
workflow compatibility          PASS — current workflows use full SHAs
negative non-SHA rejection      not directly re-proved
```

Do not call this connector-verified when it is not.

## CodeQL

CodeQL is not currently active.

Accepted next security boundary after TypeScript + Python integration reaches protected `main`:

```text
verify current default-setup support
-> activate CodeQL default setup
-> observe real emitted contexts/results
-> fix/classify real findings
-> consider required-check promotion separately
```

Do not create a custom CodeQL workflow merely to duplicate default setup.

## CODEOWNERS / reviews

`CODEOWNERS` remains intentionally absent while one regular maintainer exists. Introduce it only when distributed ownership/reviewer responsibility becomes real.

## SECURITY.md

Public vulnerability intake remains deferred until public production/release makes the process operationally meaningful. The activation register requires revisiting it before production maturity.

## Branch hygiene

Delete branches only after proving:

```text
unique accepted work not integrated   0
active work owned by branch           0
required evidence preserved           PASS
```

Relevant branch truth:

```text
feature/backend-scaffold
closed historical evidence / integrated via PR #24

feature/frontend-materialization
closed frontend evidence source / FM-00..FM-07 PASS

chore/frontend-materialization-integration
active PR #28 integration branch
```

The closed frontend evidence branch must not be repurposed for integration cleanup.

## Merge/history posture

DANTE preserves useful checkpoint/evidence history and permits merge commits. The frontend integration branch itself preserves the closed materialization history through a real two-parent merge rather than rewriting/squashing it away before review.

A future linear-history/squash-only policy requires explicit evaluation of evidence consequences.

## Current verification classification

```text
main deletion protection                  PASS / preserved
main force-push protection                PASS / preserved
PR-before-merge                           PASS / preserved
review-thread resolution                  PASS / preserved
required approvals                        0 / intentional
Backend CI Gate calibration               PASS
Backend CI Gate required                  APPLIED
Dependency Review calibration             PASS
Dependency Review required                APPLIED
branch-up-to-date requirement             APPLIED
Frontend CI real PR green                  PASS
Frontend CI Gate emitted green             PASS
Frontend CI Gate deliberate red            PENDING
Frontend CI Gate recovery green             PENDING
Frontend CI Gate required                  NOT APPLIED
CodeQL                                    NOT ACTIVE
```

## Persistent non-claims

Repository safety does not imply complete security assurance, independent human review, production deployment safety, restore/PITR rehearsal, CodeQL PASS, iOS release validation or blanket Physical/PSV PASS.

Each future control is activated only when its real boundary exists and direct evidence supports it.

## Current next repository-safety step

```text
PR #28 docs/current-truth reconciliation
-> combined PR green
-> Frontend CI Gate deliberate red
-> restore / recovery green
-> separate explicit ruleset gate if promotion is still justified
-> final protected-main merge review
```

Any ruleset mutation, merge, CodeQL activation or branch deletion requires its own authorization.