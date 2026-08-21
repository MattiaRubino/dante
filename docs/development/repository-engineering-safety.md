# Repository Engineering Safety

- Status: **CURRENT — Phase 11 QA PASS + CP4 REQUIRED-CHECK PROMOTION APPLIED**
- Scope: repository integration safety for DANTE production workstreams
- Repository: `MattiaRubino/dante`
- Default branch: `main`
- Main ruleset: `lifeos-main-safety`
- Backend CP4: **CLOSED / DIRECT REMOTE QA PASS**
- Frontend materialization: **ACTIVE ON `feature/frontend-materialization`**

## Purpose

Make the repository enforce the Git discipline DANTE documents without inventing fake review ceremony or unproven CI gates.

```text
DOCUMENTED REPOSITORY POLICY
!=
GITHUB SETTING ACTUALLY APPLIED
```

A repository-side control is recorded as effective only after the relevant evidence exists. When the connected GitHub integration cannot read a setting directly, that limitation is stated instead of converting user/admin application into false API evidence.

## Authority

This file complements, and does not replace:

- `agent-operating-manual.md`;
- `operating-rules.md`;
- `branching-and-environments.md`;
- `documentation-and-handoff.md`;
- `github-main-ruleset.json`;
- the active workstream handoff.

Persistent operating rules:

```text
main = one integrated source of truth
normal work = bounded branch
integration = pull request
no direct main work except explicitly approved emergency repair
no force-push of shared history for cosmetic cleanup
remote evidence required before PASS / CLOSED
```

## Historical Phase 11 baseline

Phase 11 established the first protected-main posture before real CI existed:

```text
ruleset                            lifeos-main-safety
ruleset enforcement                active
ruleset target                     ~DEFAULT_BRANCH
ruleset bypass                     none
main deletion                      blocked
main non-fast-forward / force push blocked
pull request before merge          required
required approving reviews         0
review-thread resolution           required
allowed merge method               merge
required status checks             0
GitHub Actions workflows           0
```

Zero required checks was correct at that time because no stable workflow context existed. That historical state remains evidence, not current policy.

## Current main protection after Backend CP4

CP4 created, calibrated and recovered the first stable integration checks on real PR #24 before promotion.

Current intended/effective ruleset definition is stored in:

`docs/development/github-main-ruleset.json`

Current protection posture:

```text
name                                   lifeos-main-safety
target                                 ~DEFAULT_BRANCH
enforcement                            active
bypass                                 none
main deletion                          blocked
main force push / non-fast-forward     blocked
pull request before merge              required
required approving reviews             0
review-thread resolution                required
allowed merge method                   merge
required checks                        Backend CI Gate
                                       Dependency Review
required-check source                  GitHub Actions
require branch up to date              enabled
do not enforce checks on creation      false
merge queue                            not enabled
```

The two required checks were promoted only after this direct sequence on PR #24:

```text
M5 GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS

M6 DELIBERATE RED
Backend Quality       FAILURE — explicit calibration step
Backend PostgreSQL    SUCCESS — independent path preserved
Backend CI Gate       FAILURE — mandatory upstream failure propagated
Dependency Review     FAILURE — denied existing FastAPI dependency

M7 RECOVERY GREEN
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

The M6 dependency-policy failure did **not** add a vulnerable dependency. It temporarily used the supported `deny-packages` policy against `pkg:pypi/fastapi`, which Dependency Review had already proven visible through the real `apps/backend/uv.lock` PR delta. The temporary workflow changes were then restored byte-for-byte to their M5 green blobs before M7.

## Required-check identities

Promoted contexts:

```text
Backend CI Gate
Dependency Review
```

Both were selected in the GitHub ruleset UI with source **GitHub Actions**. The canonical JSON records GitHub Actions integration ID `15368` so the repository definition does not intentionally degrade source binding to an arbitrary producer.

`Backend Quality` and `Backend PostgreSQL` are intentionally not separately required. They are mandatory upstream jobs of `Backend CI Gate`; M6 proved that the gate fails when a mandatory upstream result is non-success.

## Why zero approvals remains intentional

A required approval adds real safety only when an independent reviewer exists. DANTE is currently owner-driven, so requiring one approval would either block legitimate work or encourage artificial bypass behavior.

Current policy therefore remains:

```text
required approving reviews = 0
review-thread resolution    = required
```

Reconsider `0 → 1+` only when another regular human maintainer/reviewer exists or an accepted governance process assigns independent review responsibility.

## Required-check promotion protocol

The permanent protocol is now exercised rather than theoretical:

```text
workflow/job exists
+ runs on relevant PR
+ stable emitted context observed remotely
+ success observed
+ deliberate failure observed
+ failure genuinely means merge must stop
+ recovery green observed
→ exact context may become required
```

For future checks:

1. create the real workflow/check in an approved scope;
2. run it on a real PR;
3. record the exact emitted context;
4. prove normal green behavior;
5. prove a bounded deliberate failure for the intended reason;
6. restore green without weakening policy;
7. only then open a repository/ruleset mutation gate;
8. update `github-main-ruleset.json` and this file with the resulting truth.

A workflow name that merely sounds desirable is never sufficient.

## Branch-up-to-date policy

`Require branches to be up to date before merging` is enabled for the required checks.

This is intentional for the current monorepo because backend and frontend workstreams can advance independently. A candidate integration must therefore be tested against the latest protected `main`, rather than relying on a green run against stale base code.

This setting does not authorize merge queues. Merge queue remains deferred until actual merge volume or contention justifies it.

## GitHub Actions full-SHA policy

Repository Actions settings were updated by the repository owner during CP4 M8 to enable:

```text
Require actions to be pinned to a full-length commit SHA
```

The connected GitHub integration does not expose a read endpoint for this repository setting, so evidence classification is:

```text
owner/admin application         CONFIRMED BY USER
connector direct readback       UNAVAILABLE
workflow compatibility          PASS — current workflows already use full SHAs
negative non-SHA rejection test NOT RUN
```

Do not call this connector-verified when it is not. The backend workflows themselves already use immutable full-length Action SHAs and continued to execute successfully.

## Workflow security posture

Backend CP4 directly proved the following on GitHub-hosted `ubuntu-24.04` runners:

```text
workflow default permissions        none
Backend Quality                     contents: read
Backend PostgreSQL                  contents: read
Dependency Review                   contents: read
Backend CI Gate                     no repository grant; metadata read implicit
checkout persist-credentials        false
pull_request_target                 absent
PROD/deployment credentials         absent from ordinary PR validation
```

The selected external Actions are pinned by full commit SHA. `setup-uv` also verifies the selected uv 0.12.5 Linux archive with the recorded SHA-256.

## Dependency Review posture

Dependency Review is repository-wide and currently protects PR dependency changes at:

```text
fail-on-severity   moderate
fail-on-scopes     runtime, development, unknown
comment writing    disabled
```

M5 directly proved that GitHub Dependency Review sees the real `apps/backend/uv.lock` dependency delta. M6 directly proved that an intentional denied-package policy violation makes the check fail. M7 proved recovery.

No license allowlist/denylist is introduced without a real DANTE license policy.

## Dependabot

`.github/dependabot.yml` now exists because real package ecosystems exist. Current version-update scopes are:

```text
uv             /apps/backend
GitHub Actions /
```

Dependabot and Dependency Review are complementary: Dependabot proposes updates; Dependency Review evaluates dependency changes in PRs.

Alert/security dashboard APIs may remain connector-limited. Do not infer their state when the connector cannot read it.

## Code scanning / CodeQL

CodeQL is intentionally not activated by Backend CP4.

Accepted later boundary:

```text
backend integrated into current main
→ verify current GitHub default-setup support
→ activate CodeQL default setup
→ observe emitted results/checks
→ consider required-check promotion separately
```

Do not create a custom CodeQL workflow merely to duplicate supported default setup.

## CODEOWNERS

`CODEOWNERS` remains intentionally absent while one owner is the only regular maintainer. A self-review requirement does not create independent review safety.

Introduce CODEOWNERS only when ownership/reviewer responsibility becomes meaningfully distributed.

## SECURITY.md

A public vulnerability-reporting policy remains deferred until a production/released security process exists. Revisit before public production release or when external vulnerability reporting becomes operationally meaningful.

## Branch hygiene

Do not delete branches merely because they look old. Delete only after proving:

```text
unique accepted work not integrated       0
current active work owned by branch       0
required evidence available elsewhere     PASS
```

Current relevant active branches include:

```text
feature/backend-scaffold
feature/frontend-materialization
prototype/phase-4-today-home   where still active/current
```

Merged branches may be auto-deleted because repository auto-delete for merged head branches is enabled. Git/PR history remains the evidence source.

Confirmed accidental refs previously cleaned remain historical evidence and must not be recreated.

## Merge/history posture

DANTE preserves checkpoint SHAs and intermediate evidence in Git history. The protected-main ruleset therefore continues to allow merge commits rather than requiring linear history.

A future merge-policy change requires an explicit evaluation of evidence/history consequences.

## Current verification classification

```text
Phase 11 baseline protections             PASS
Backend CP4 real PR green                  PASS
Backend CP4 deliberate red                 PASS
Backend CP4 recovery green                 PASS
Backend CI Gate failure propagation        PASS
Dependency Review uv.lock visibility       PASS
Dependency Review policy failure           PASS
required contexts selected                 PASS — UI evidence
required context source                    GitHub Actions — UI evidence
branch-up-to-date requirement              ENABLED — UI evidence
full-SHA repository requirement            USER-APPLIED / CONNECTOR-UNVERIFIABLE
main deletion protection                   preserved
main force-push protection                 preserved
PR-before-merge                            preserved
required approvals                         0 / preserved
review-thread resolution                   preserved
merge method                               merge / preserved
merge queue                                absent
```

Classic branch-protection readback may continue to show zero classic required contexts because DANTE uses a repository ruleset. Do not misread classic branch protection as the ruleset authority.

## Persistent non-claims

Repository safety does not imply:

```text
complete security assurance
CodeQL PASS
frontend CI PASS
production deployment safety
restore/PITR rehearsal
Physical HG/PSV blanket PASS
independent human review
```

Each future control is promoted only after its real boundary exists and is directly proven.

## Current downstream state

```text
PHYSICAL MODEL
CLOSED / SELECTED / ACCEPTED

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED

FRONTEND MATERIALIZATION
ACTIVE

BACKEND CP1
CLOSED / DIRECT QA PASS

BACKEND CP2
CLOSED / DIRECT QA PASS

BACKEND CP3
CLOSED / DIRECT QA PASS

BACKEND CP4
CLOSED / DIRECT REMOTE QA PASS

BACKEND CP5
NEXT
```

Any later repository-policy mutation requires its own exact authorization. CP4 closure does not authorize PR #24 merge, CodeQL activation, CP5 implementation, frontend integration or concrete Logical → PostgreSQL business mapping.
