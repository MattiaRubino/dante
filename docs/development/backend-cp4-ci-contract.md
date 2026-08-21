# DANTE Backend CP4 — Quality and CI enforcement contract

- Status: **CLOSED / DIRECT REMOTE QA PASS**
- Workstream: `feature/backend-scaffold`
- CP4 design PRE-SCOPE: `495e484c6ac729f24dc43dc2dbba8cc4d359a568`
- CP3 implementation/direct-QA HEAD consumed: `35cf6440bc121a38342f6bbee72e210435a788a4`
- M4 tested post-main-reconciliation HEAD: `ba0d994e983cf3e5add6ad640c238999f418e236`
- M5 green-calibration HEAD: `bf9d364c59f02857125e228c6b223c13650ab78f`
- M6 deliberate-red HEAD: `739680d11fe5c33a4974f069c2fdcce9e71a4fe0`
- M7 recovery-green HEAD / M9 PRE-SCOPE: `df0a7c4fd3c7fe844fe56052fe7999732f186ee5`
- Calibration PR: `#24`
- Scope: backend repository quality/CI enforcement only
- Concrete Logical → PostgreSQL business mapping: **OUT OF SCOPE**
- Frontend CI: **OUT OF SCOPE**

## 1. Purpose

CP1–CP3 established real backend commands, a reproducible PostgreSQL 18.4 image, persistence/migration/privilege boundaries and directly passing tests. CP4 turns those proven local boundaries into remote GitHub Actions checks and promotes only calibrated checks into protected-main enforcement.

CP4 follows one rule:

```text
workflow exists
!=
workflow is trusted
```

A check becomes required only after real green execution, deliberate failure for the intended reason, recovery green and stable emitted identity have all been observed.

## 2. Closed CP4 architecture

Materialized repository surface:

```text
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
apps/backend/pyproject.toml
```

Primary workflow:

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate
```

Separate repository-wide workflow:

```text
Dependency Review
```

The backend gate has mandatory upstream dependencies on `quality` and `postgres`, uses `if: ${{ always() }}` and explicitly fails unless both upstream results equal `success`.

## 3. Toolchain authority

Canonical versions:

```text
Python                         3.14.7
uv                             0.12.5
pyproject required-version     ==0.12.5
runner                         ubuntu-24.04
```

Python authority is `apps/backend/.python-version`; workflow YAML does not maintain a second handwritten Python version.

uv 0.12.5 Linux x86_64 archive SHA-256:

```text
68a509da24b06b4223a1c0175fb5eb5bc79342b76cbeff0cfe51ac3f5b17b6b2
```

The setup action performs checksum-backed installation; checksum verification is not disabled.

## 4. Immutable Action pins

```text
actions/checkout v7.0.1
3d3c42e5aac5ba805825da76410c181273ba90b1

astral-sh/setup-uv v9.0.0
c771a70e6277c0a99b617c7a806ffedaca235ff9

actions/dependency-review-action v5.0.0
a1d282b36b6f3519aa1f3fc636f609c47dddb294
```

Checkout uses `persist-credentials: false`.

Repository Actions settings were also updated by the repository owner during M8 to require full-length Action SHAs. The connected GitHub integration cannot directly read that repository setting, so evidence remains explicitly classified as **USER-APPLIED / CONNECTOR-UNVERIFIABLE** rather than API-verified.

## 5. Permissions and secret posture

Workflow-level permissions are denied by default.

```text
Backend Quality       contents: read
Backend PostgreSQL    contents: read
Dependency Review     contents: read
Backend CI Gate       no repository permission grant
```

GitHub may expose implicit metadata read permission. Ordinary PR validation requires no PROD secret, deployment identity, cloud credential or administrative repository token.

`pull_request_target` is not used for normal validation.

## 6. Triggers and concurrency

Backend CI triggers:

```text
pull_request targeting main
push to main
workflow_dispatch
```

Dependency Review triggers on pull requests repository-wide.

No workflow-level path filter is used on a future-required check.

Concurrency allows superseded PR runs to be cancelled while accepted `main` pushes are not cancelled merely because a newer main commit arrives.

## 7. Finite timeouts

```text
Backend Quality      15 minutes
Backend PostgreSQL   30 minutes
Backend CI Gate       5 minutes
Dependency Review    10 minutes
```

Timeout is failure; CP4 does not use retry-until-green behavior.

## 8. Backend Quality contract

Remote quality execution proves:

```text
uv lock --check
uv sync --locked
uv 0.12.5
Python 3.14.7
ruff format --check .
ruff check .
mypy strict
pytest -m "not postgres"
uv build
```

No arbitrary global coverage threshold is introduced. Coverage remains evidence only.

## 9. Backend PostgreSQL contract

The PostgreSQL job builds the repository-owned image rather than substituting SQLite or a generic service image:

```text
docker build --pull --tag dante-postgres-local:18.4 infra/local/postgres
uv run --locked pytest -m postgres -vv
```

The image retains the CP2 PostgreSQL 18.4 + PostGIS 3.6.4 + pgvector 0.8.6 envelope and the CP3 disposable acceptance harness.

## 10. Dependency Review contract

Policy:

```text
fail-on-severity    moderate
fail-on-scopes      runtime, development, unknown
comment-summary     never
permissions         contents: read
```

No license allow/deny policy is invented without a real DANTE license policy.

M5 directly proved that GitHub Dependency Review sees `apps/backend/uv.lock` and enumerates its real Python dependency delta.

M6 proved blocking semantics safely by temporarily adding:

```text
deny-packages: pkg:pypi/fastapi
```

The action failed because `fastapi@0.141.1` was denied. No vulnerable package was introduced merely for calibration.

## 11. M1–M4 local/materialization evidence

### M1

```text
canonical workstation uv      0.12.5
Python authority              3.14.7
selected Action SHAs          frozen
uv checksum                   frozen
```

### M2

Materialized:

```text
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
apps/backend/pyproject.toml [tool.uv].required-version
```

`apps/backend/uv.lock` was not modified by the uv tool-version pin.

### M3

On exact materialized HEAD `eb8d33fa85d6409dfcc60eba663cb32b64d65aee`:

```text
uv lock --check                 PASS
uv sync --locked                PASS
Ruff format                     PASS — 23 files
Ruff lint                       PASS
mypy strict                     PASS — 20 source files
fast pytest                     PASS — 32/32
uv build                        PASS
PostgreSQL image rebuild        PASS
PostgreSQL pytest               PASS — 18/18 in 15.59s
worktree                        CLEAN
```

### M4

Current protected `main` consumed:

```text
ff46eb16b971b1fde96eef9047b09faa02e1a5db
```

Two-parent merge:

```text
6a8122249f13f9b8553f511c47b4185c6e3e6540
```

Tested reconciled HEAD:

```text
ba0d994e983cf3e5add6ad640c238999f418e236
```

After reconciliation:

```text
main ancestor                    YES
behind_by                        0
unexpected backend/CI/DB paths   0
```

The complete locked quality + build + PostgreSQL 18/18 regression was rerun on the reconciled tree and directly passed.

## 12. M5 — real PR green calibration — PASS

PR #24 was opened from `feature/backend-scaffold` to protected `main` without auto-merge.

Green-calibration HEAD:

```text
bf9d364c59f02857125e228c6b223c13650ab78f
```

Workflow runs:

```text
Dependency Review   32477974220   SUCCESS
Backend CI          32477974221   SUCCESS
```

Observed emitted jobs/check identities:

```text
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

Remote logs directly proved:

```text
runner OS                     Ubuntu 24.04.4 LTS
runner image                  ubuntu-24.04
uv                            0.12.5
Python                        3.14.7
uv checksum-backed setup      PASS
uv lock --check               PASS
uv sync --locked              PASS
Ruff format/lint              PASS
mypy strict                   PASS
fast pytest                   PASS — 32/32
uv build                      PASS
PostgreSQL image build        PASS
PostgreSQL pytest             PASS — 18/18 in 14.56s
```

Dependency Review also directly showed the `apps/backend/uv.lock` dependency changes, closing the uv-lock visibility question before promotion.

## 13. M6 — deliberate red calibration — PASS

Final deliberate-red HEAD:

```text
739680d11fe5c33a4974f069c2fdcce9e71a4fe0
```

Workflow runs:

```text
Backend CI          32478656632
Dependency Review   32478656892
```

Expected and observed result:

```text
Backend Quality       FAILURE
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE
```

Backend Quality failed only at the explicit temporary `CP4-M6 deliberate calibration failure` step.

Backend PostgreSQL continued independently and completed successfully, proving that diagnostic isolation was preserved.

The gate log directly observed:

```text
QUALITY_RESULT:  failure
POSTGRES_RESULT: success
```

and exited with code 1. Therefore `if: always()` does not produce a false green above a failed mandatory upstream job.

Dependency Review failed for the intentional FastAPI deny policy and explicitly reported:

```text
fastapi@0.141.1 is denied
pkg:pypi/fastapi@0.141.1 is denied
Dependency review detected denied packages.
```

## 14. M7 — recovery green — PASS

The two temporary workflow mutations were restored exactly to their M5 green blobs:

```text
backend-ci.yml blob
20056674477dd0fc2778d7f4d217a7158f0cd2c0

dependency-review.yml blob
c311f1e0df157b518a7b9883eeaa1a3f96833874
```

Recovery HEAD:

```text
df0a7c4fd3c7fe844fe56052fe7999732f186ee5
```

Workflow runs:

```text
Backend CI          32478852443   SUCCESS
Dependency Review   32478852454   SUCCESS
```

Observed recovery:

```text
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

No production backend source, test, dependency, lockfile or PostgreSQL infrastructure change was used to obtain recovery.

## 15. M8 — protected-main enforcement — APPLIED

After M5 green → M6 red → M7 green, the existing `lifeos-main-safety` ruleset was updated through GitHub repository settings.

Required contexts:

```text
Backend CI Gate
Dependency Review
```

UI evidence shows both selected with source **GitHub Actions**. The canonical ruleset definition records GitHub Actions integration ID `15368`.

Also enabled:

```text
Require branches to be up to date before merging        true
Do not require status checks on creation                 false
```

Preserved:

```text
ruleset enforcement              active
ruleset target                   ~DEFAULT_BRANCH
bypass                           none
main deletion                    blocked
force push/non-fast-forward      blocked
pull request before merge        required
required approving reviews       0
review-thread resolution         required
allowed merge method             merge
merge queue                      absent
```

Repository Actions setting applied by the repository owner:

```text
Require actions to be pinned to a full-length commit SHA
```

Connector limitation: the available GitHub integration cannot directly read repository rulesets or this Actions setting after mutation. Therefore those settings are recorded from owner/UI application and canonical repository configuration, not falsely labeled as connector API readback.

The raw PR API continued to report PR #24 open, unmerged, mergeable and `mergeable_state: clean` on the M7 green head after M8 application.

## 16. Required-check policy after CP4

Protected-main required checks are now intentionally minimal:

```text
Backend CI Gate
Dependency Review
```

`Backend Quality` and `Backend PostgreSQL` remain mandatory upstream jobs but are not separately required because the calibrated gate already fails if either mandatory upstream result is non-success.

Future frontend/mobile/security checks must earn promotion independently through the same green → deliberate-red → recovery protocol.

## 17. Dependabot posture

Weekly version-update scopes:

```text
uv             /apps/backend
GitHub Actions /
```

No Docker auto-update is enabled for the certified PostgreSQL base because changing that digest is an explicit environment revalidation event, not a routine bot bump.

## 18. CodeQL boundary

CodeQL remains outside CP4 closure.

Accepted later boundary:

```text
backend integrated into current main
→ verify GitHub default setup support
→ activate default setup
→ observe real emitted checks
→ consider separate required-check promotion
```

No custom CodeQL workflow is introduced by CP4.

## 19. Coverage and architecture-check policy

```text
coverage = signal
coverage != semantic proof
```

No arbitrary global coverage threshold is introduced.

Automated import/layer enforcement remains deferred until a meaningful domain/application/adapter graph exists. CP4 does not add a dependency merely to prove trivial package structure.

## 20. CP4 final acceptance matrix

```text
DESIGN / SCOPE
bounded gates                                 PASS
unexpected executable paths                  0

BOOTSTRAP
workstation uv                               0.12.5 PASS
pyproject required-version                   ==0.12.5 PASS
CI uv                                        0.12.5 PASS
CI Python                                    3.14.7 PASS
uv checksum-backed setup                     PASS
locked dependency bootstrap                  PASS

QUALITY
Ruff format                                  PASS
Ruff lint                                    PASS
mypy strict                                  PASS
fast pytest                                  32/32 PASS
uv build                                     PASS

POSTGRESQL
repository image build                       PASS
PostgreSQL acceptance                        18/18 PASS
SQLite substitution                          0

AGGREGATION
quality + postgres green → gate green        PASS
mandatory upstream deliberate failure        PASS
gate red on upstream failure                 PASS
recovery green                               PASS

DEPENDENCY REVIEW
real PR execution                            PASS
uv.lock delta visibility                     PASS
policy deliberate violation                  PASS
failure emitted                              PASS
recovery green                               PASS

SECURITY
workflow default permissions                 deny-by-default PASS
checkout credentials                         not persisted PASS
PROD/deployment secrets required             0
pull_request_target                          absent
Actions in repository workflows              full-SHA pinned
finite timeouts                              PASS

REPOSITORY PROMOTION
stable required context Backend CI Gate       PASS
stable required context Dependency Review     PASS
GitHub Actions source selected                PASS — UI evidence
branch up-to-date required                    ENABLED — UI evidence
checks-on-creation exception                  DISABLED — UI evidence
full-SHA repository setting                  USER-APPLIED / CONNECTOR-UNVERIFIABLE
classic branch-protection contexts            not authority; ruleset is authority
```

## 21. Closure decision

CP4 is **CLOSED / DIRECT REMOTE QA PASS**.

The connector limitation on direct ruleset/Actions-setting readback is explicitly documented and does not masquerade as direct API evidence. The actual workflow behavior, emitted contexts, deliberate-red semantics and recovery behavior were all directly observed on GitHub Actions before required-check promotion.

## 22. Explicit non-claims

CP4 does not prove or implement:

```text
frontend/web/mobile CI
frontend package-manager/toolchain validation
CodeQL PASS
business/domain schema
business repositories/use cases/API
production deployment
DEV/UAT/PROD infrastructure
cloud deployment identity
release artifact promotion
SBOM/provenance release flow
containerized backend runtime image
complete security assurance
Physical HG/PSV blanket PASS
frozen/blackholed PostgreSQL readiness hardening
restore/PITR rehearsal
```

## 23. Next boundary

```text
CP4
CLOSED / DIRECT REMOTE QA PASS
        ↓
CP5
full production-backend scaffold QA / closure
        ↓
concrete Logical → PostgreSQL mapping
only after scaffold closure
```

Do not reopen CP4 by default. Reopen only if direct evidence proves a defect in the closed CI/enforcement contract.