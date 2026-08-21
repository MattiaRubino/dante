# DANTE Backend CP4 — Quality and CI enforcement contract

- Status: **M1–M4 MATERIALIZED / M4 POST-MERGE REGRESSION PASS / M5 NEXT**
- Workstream: `feature/backend-scaffold`
- CP4 design PRE-SCOPE: `495e484c6ac729f24dc43dc2dbba8cc4d359a568`
- CP3 implementation/direct-QA HEAD consumed: `35cf6440bc121a38342f6bbee72e210435a788a4`
- M4 PRE-SCOPE / post-merge regression HEAD: `ba0d994e983cf3e5add6ad640c238999f418e236`
- M4 main consumed: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- M4 two-parent merge commit: `6a8122249f13f9b8553f511c47b4185c6e3e6540`
- Scope: backend repository quality/CI enforcement only
- Concrete Logical → PostgreSQL business mapping: **OUT OF SCOPE**
- Frontend CI: **OUT OF SCOPE**

## 1. Purpose

CP1–CP3 established real backend commands, a reproducible PostgreSQL 18.4 image, application persistence, migrations, privileges and directly passing test suites. CP4 makes those already-proven checks run remotely and become enforceable before protected-main integration.

CP4 is not permission to invent new quality mechanisms merely to make the repository look mature. It converts proven local boundaries into a small, trustworthy GitHub Actions surface, then calibrates the exact emitted checks before any branch-protection requirement is changed.

```text
CP1 / CP2 / CP3
real commands + real PostgreSQL + direct QA
                 ↓
CP4
remote deterministic execution
+ supply-chain hardening
+ stable check calibration
                 ↓
required-check promotion
ONLY after direct remote evidence
```

## 2. Existing evidence consumed by CP4

CP4 does not reopen the closed CP1–CP3 design by default.

Direct CP3 closure evidence already established on the canonical WSL/Docker workstation:

```text
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS
ruff format --check .                    PASS
ruff check .                             PASS
mypy                                    PASS
pytest -m "not postgres"                PASS — 32/32
pytest -m postgres                       PASS — 18/18
full pytest                              PASS — 50/50
uv build                                 PASS
PostgreSQL 18.4 acceptance               PASS
Alembic migration acceptance             PASS
privilege acceptance                     PASS
transaction acceptance                   PASS
outage/recovery acceptance               PASS
```

The 97.42% full-run coverage recorded at CP3 closure remains evidence only. CP4 does not create an arbitrary global percentage threshold.

## 3. CP4 repository inventory at design time

Read-only inspection before this contract established:

```text
repository                              MattiaRubino/dante
visibility                              public
default branch                          main
active backend branch                   feature/backend-scaffold
.github workflows                       0
.github current content                 pull_request_template.md only
protected main                          yes
required status checks                  0
backend branch vs current main          diverged
```

At design time the backend branch was 86 commits ahead and 28 behind current `main`. Those counts are historical inventory evidence, not a permanent invariant. The branch/main relation must be re-read before materialization calibration, PR work or repository-setting changes.

The absence of existing workflows means CP4 is not duplicating a pre-existing CI implementation.

## 4. Primary workflow architecture

The primary backend workflow is intentionally small:

```text
Workflow: Backend CI

quality
  display name: Backend Quality

postgres
  display name: Backend PostgreSQL

quality + postgres
        ↓
gate
  display name: Backend CI Gate
```

Stable intended identities are frozen now because future required-check promotion depends on stable emitted checks.

The actual GitHub required-check context string is **not** guessed from these names. It must be observed remotely on a real pull request before any ruleset change.

No extra placeholder job is created merely to reserve future architecture/security/product checks.

## 5. Backend Quality job

The `quality` job runs only already-proven backend quality boundaries.

Expected responsibilities:

```text
checkout exact workflow revision
install the selected exact uv version
install Python from apps/backend/.python-version
verify lock consistency
sync locked backend dev dependencies
Ruff format check
Ruff lint
mypy strict
fast/non-PostgreSQL pytest
backend package build
```

The materialized command sequence preserves frozen/locked semantics. `uv run --locked` is used where supported/applicable so an individual CI command cannot silently rewrite dependency resolution. `uv build` is executed only after the lock has been explicitly checked and the environment synchronized from locked state.

The job does not upload the built wheel/sdist merely to create an artifact. CP4 proves buildability; release artifact retention/promotion belongs to a later release boundary.

## 6. Backend PostgreSQL job

The `postgres` job proves the real database boundary rather than substituting SQLite or mocks.

Expected responsibilities:

```text
checkout exact workflow revision
install the selected exact uv version
install Python from apps/backend/.python-version
sync locked backend dev dependencies
build the repository-owned dante-postgres-local:18.4 image
run pytest -m postgres against the disposable CP3 harness
```

The job reuses:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/010-extensions.sql
dante-postgres-local:18.4
```

The PostgreSQL Dockerfile already pins its base image by digest and pins the PostGIS/pgvector packages used by CP2. CI does not introduce a second PostgreSQL implementation or a generic service image with weaker semantics.

`quality` and `postgres` remain independent mandatory upstream jobs. One does not depend on the other merely to save compute; independent execution preserves diagnostic evidence when one boundary fails.

## 7. Aggregation-gate semantics

`gate` exists to provide one stable backend integration signal without producing a false green above a failed/skipped upstream job.

Required conceptual semantics:

```text
gate:
  needs:
    - quality
    - postgres
  if: always()
```

Execution alone is not sufficient. The gate step MUST fail unless every mandatory upstream result is exactly `success`.

```text
quality  = success
postgres = success
        ↓
Backend CI Gate = PASS

quality  != success
OR
postgres != success
        ↓
Backend CI Gate = FAIL
```

For this gate, `failure`, `cancelled` and `skipped` are all non-success outcomes.

The gate itself must not have a path/event condition that can silently skip it on a relevant pull request.

## 8. Workflow triggers

Initial `Backend CI` trigger contract:

```text
pull_request targeting main
push to main
workflow_dispatch
```

Do not use workflow-level `paths` / `paths-ignore` on a workflow intended to become required. A skipped required workflow can leave an expected status unresolved and block integration.

Change-aware/path-aware optimization may be introduced later only after correctness is proven and only if the required aggregate signal still emits reliably for every relevant PR.

No `pull_request_target` is used for normal backend validation.

## 9. Concurrency and cancellation

Superseded pull-request CI may be cancelled because a newer commit replaces the older candidate.

Accepted policy:

```text
pull_request run superseded by newer head
→ cancellation allowed

push to accepted main
→ do NOT cancel merely because a newer main commit appears
```

Every integrated main commit should be allowed to complete its own validation evidence.

The materialized workflow implements this policy with event-aware concurrency; real behavior still requires M5/M6 remote calibration.

## 10. Runner posture

Initial runner:

```text
ubuntu-24.04
GitHub-hosted standard Linux runner
```

Do not use `ubuntu-latest` because DANTE wants an explicit OS family/version boundary.

`ubuntu-24.04` is still a GitHub-maintained image whose patch-level contents evolve. CP4 therefore does not claim a completely hermetic operating-system image. Correctness-sensitive project components remain explicitly pinned/locked where DANTE owns that control.

No self-hosted runner is introduced without a measured network/hardware/cost reason and an explicit maintenance/security owner.

## 11. Shell posture

Run steps use explicit Bash semantics appropriate to the Linux runner. Multi-line shell execution must fail on command errors and pipeline failures; workflow materialization must not hide failures with broad `continue-on-error` behavior.

No quality, PostgreSQL, dependency or aggregation check that protects correctness is allowed to become informational-only merely to keep CI green.

## 12. GitHub token and PR security

Workflow permissions are denied by default and granted only per job as needed.

Primary posture:

```text
workflow default permissions           none
quality job                             contents: read
postgres job                            contents: read
gate job                                no repository permission required
```

Checkout uses:

```text
persist-credentials: false
```

Normal PR validation receives:

```text
no PROD secrets
no deployment identity
no cloud credential
no administrative repository token
```

The initial workflow must be able to validate public fork PRs using read-only repository access only; it must not require secrets to become green.

## 13. Python version authority

Python has one project authority:

```text
apps/backend/.python-version
```

Current accepted pin:

```text
3.14.7
```

CI consumes that file rather than maintaining a second hand-written Python version in workflow YAML.

The bootstrap runs in the backend project context so `uv python install` and subsequent commands respect `.python-version`.

## 14. uv version authority and parity

M1/M2 established and materialized one exact uv tool-version authority in:

```text
apps/backend/pyproject.toml

[tool.uv]
required-version = "==0.12.5"
```

Canonical workstation evidence for CP4:

```text
uv 0.12.5
```

Desired and materialized pre-PR invariant:

```text
workstation uv version        0.12.5
pyproject required-version    ==0.12.5
CI requested uv authority     apps/backend/pyproject.toml
```

The exact installed CI version still requires direct M5 workflow evidence. A mismatch must fail rather than silently using another uv version.

## 15. uv binary checksum verification

Pinning the setup Action commit is not by itself the entire uv binary trust boundary.

M1/M2 selected `astral-sh/setup-uv` v9.0.0 at immutable commit `c771a70e6277c0a99b617c7a806ffedaca235ff9` and materialized explicit checksum verification for uv 0.12.5:

```text
68a509da24b06b4223a1c0175fb5eb5bc79342b76cbeff0cfe51ac3f5b17b6b2
```

Verification is not disabled. Direct remote checksum/install evidence is still earned only when M5 executes the workflow.

## 16. Action pinning

Protected/relevant workflows use external and official Actions by immutable full-length commit SHA.

Materialized pins:

```text
actions/checkout
3d3c42e5aac5ba805825da76410c181273ba90b1  # v7.0.1

astral-sh/setup-uv
c771a70e6277c0a99b617c7a806ffedaca235ff9  # v9.0.0

actions/dependency-review-action
a1d282b36b6f3519aa1f3fc636f609c47dddb294  # v5.0.0
```

These pins are materialized repository truth. M5 still must prove that the selected revisions execute correctly in DANTE's real PR context.

## 17. Action-source repository policy

After the first real workflow has passed and the chosen Actions are known to work, CP4 may enforce repository-level full-length-SHA pinning **where the repository/account settings expose that control and it is directly verifiable**.

Do not activate a narrow Action-source allowlist now. DANTE is a monorepo and future frontend/mobile CI will legitimately introduce other reviewed Actions; premature allowlisting would create ceremony and break adjacent work without adding meaningful current safety.

## 18. Finite timeouts and hang policy

Materialized finite job timeouts are:

```text
Backend Quality      15 minutes
Backend PostgreSQL   30 minutes
Backend CI Gate       5 minutes
Dependency Review    10 minutes
```

These values provide bounded failure while retaining cold-run margin for the real PostgreSQL image build. M5 will provide the first remote timing evidence.

A timeout is a failure, not a hidden retry-until-green policy.

CP3's `docker pause` finding is useful precedent: a hung dependency path is investigated as a defect/failure-mode question rather than masked with an enormous/unbounded timeout.

## 19. Dependency Review workflow

Dependency review is repository-wide rather than nested under backend CI.

Materialized structure:

```text
Workflow: Dependency Review

job id: dependency-review
display name: Dependency Review
```

It runs on pull requests and has its own future required-check promotion path.

Materialized initial policy:

```text
fail-on-severity     moderate
fail-on-scopes       runtime, development, unknown
permissions          contents: read
PR comment writing   disabled
```

No license allowlist/denylist is invented without a real DANTE license policy. License policy is separate from vulnerability detection.

Dependency Review is not considered proven for DANTE's uv dependency graph merely because YAML exists. CP4 must directly exercise a real `uv.lock` dependency change and verify that the workflow detects/evaluates the intended dependency delta.

If uv dependency review is not correctly represented, the check remains non-required until the actual supported mechanism is identified and proven.

## 20. Separate required-check candidates

The intended future candidates are separate:

```text
Backend CI Gate
Dependency Review
```

Dependency Review is not hidden behind the backend gate because it is repository-wide and will eventually protect backend and frontend dependency changes.

Neither candidate is required at workflow creation time.

## 21. Dependabot posture

M2 materialized weekly Dependabot version updates for:

```text
uv            /apps/backend
GitHub Actions /
```

Dependabot PRs must run the same applicable validation as human dependency PRs.

Dependency Review and Dependabot are complementary:

```text
Dependency Review
→ evaluates dependency changes in a PR

Dependabot
→ proposes dependency/tooling updates
```

Neither replaces locked installs, tests or review.

## 22. CodeQL boundary

Python production source now exists on the backend feature branch, but CP4 does not activate a custom CodeQL workflow merely to duplicate GitHub's supported default setup.

Accepted boundary:

```text
backend integrated into current main
        ↓
verify current GitHub default-setup support
        ↓
activate CodeQL default setup
        ↓
observe real emitted checks/results
        ↓
consider future required-check promotion separately
```

CodeQL activation is therefore outside the initial branch YAML materialization and cannot be claimed PASS before post-integration direct evidence.

## 23. Coverage policy

CP4 preserves the accepted Foundation rule:

```text
coverage = signal
coverage != semantic proof
```

No arbitrary global or changed-code percentage threshold is introduced now.

Coverage thresholds may be introduced later when a meaningful application/domain denominator exists and the threshold can be justified without encouraging bad tests or excluding important integration behavior.

## 24. Architecture-check defer

Automated import/layer enforcement is valuable only after the concrete package graph contains meaningful domain/application/adapter/module boundaries.

Current backend scaffold is intentionally too small to justify an additional architecture-linter dependency merely to prove trivial imports.

CP4 therefore records:

```text
architecture dependency enforcement
DEFERRED until meaningful package graph exists
```

When activated, use the lightest reliable mechanism that enforces actual accepted boundaries.

## 25. Required-check promotion protocol

No required status check is configured during initial workflow materialization.

For each candidate:

```text
1. real workflow/job exists
2. relevant real PR emits the check
3. successful execution observed
4. exact emitted context/name recorded
5. deliberate failure introduced in a bounded calibration change
6. candidate becomes red for the intended reason
7. recovery change restores green
8. no secret/deployment privilege is required for ordinary PR validation
9. current main and branch relation is reconciled/verified
10. only then open a separate repository-setting/ruleset gate
```

For `Backend CI Gate`, deliberate failure must prove that a failed/non-success mandatory upstream job makes the aggregate gate fail.

For `Dependency Review`, deliberate failure must prove that an intentionally introduced dependency-policy violation is detected and blocks that candidate check.

Where GitHub rulesets support binding the required status check to its expected GitHub App/source, use the observed GitHub Actions source rather than trusting an identically named status from another producer.

After applying required checks, reread effective protection/ruleset state and prove that `main` remains mergeable only when the intended checks pass.

## 26. Main reconciliation requirement — M4 COMPLETE

At CP4 design time, `feature/backend-scaffold` was behind current `main` because frontend Foundation/current-truth work had been integrated separately.

M4 consumed current `main`:

```text
main consumed
ff46eb16b971b1fde96eef9047b09faa02e1a5db

M4 PRE-SCOPE / tested post-merge HEAD
ba0d994e983cf3e5add6ad640c238999f418e236

two-parent merge commit
6a8122249f13f9b8553f511c47b4185c6e3e6540
```

The merge imported the 14 non-overlapping `main` paths byte-identically and reconciled the four shared current-truth documents semantically:

```text
README.md
docs/PROJECT-STATUS.md
docs/README.md
docs/ROADMAP.md
```

Remote reconciliation evidence before the regression run:

```text
main → feature/backend-scaffold
behind_by       0
ahead_by        97
main ancestor   YES
```

M4 PRE-SCOPE → reconciled HEAD contained exactly 18 expected paths and no unexpected backend/CI/database mutations.

After reconciliation, the canonical WSL/Docker workstation reran the accepted backend regression surface on exact HEAD `ba0d994e983cf3e5add6ad640c238999f418e236` and directly reported all commands PASS:

```text
git status --short                       CLEAN
uv --version                             0.12.5
uv lock --check                          PASS
uv sync --locked                         PASS
ruff format --check .                    PASS
ruff check .                             PASS
mypy                                    PASS
pytest -m "not postgres"                PASS — 32/32
uv build                                PASS
docker build --pull dante-postgres...   PASS
pytest -m postgres -vv                   PASS — 18/18
final git status                         CLEAN
final HEAD                               ba0d994e983cf3e5add6ad640c238999f418e236
```

Therefore M4 reconciliation/regression is **DIRECT PASS**. This does not imply remote GitHub Actions PASS; that begins at M5.

## 27. CP4 materialization sequence

Proceed without another broad research phase:

```text
CP4-M1
read exact canonical workstation uv version
revalidate selected Action releases/full SHAs/checksum support
choose finite initial job timeouts
STATUS: COMPLETE

CP4-M2
materialize exact uv required-version
materialize Backend CI workflow
materialize Dependency Review workflow
materialize Dependabot config where still supported
STATUS: COMPLETE

CP4-M3
run local non-mutating validation where meaningful
remote exact-delta/readback QA
STATUS: COMPLETE

CP4-M4
reconcile current main before calibration PR
rerun applicable backend regression suite after reconciliation
STATUS: COMPLETE / DIRECT PASS

CP4-M5
real PR green calibration
inspect workflow runs/jobs/logs/exact emitted contexts
STATUS: NEXT / NOT STARTED

CP4-M6
deliberate red calibration
prove aggregate-gate failure semantics
prove Dependency Review behavior on a real dependency-policy violation/uv delta
STATUS: NOT STARTED

CP4-M7
recovery green
STATUS: NOT STARTED

CP4-M8
only then propose a separate repository/ruleset-settings gate
for required-check/full-SHA enforcement that is actually supported and verified
STATUS: NOT STARTED

CP4-M9
record CP4 closure evidence
STATUS: NOT STARTED
```

Any direct failure may reopen only the affected CP4 implementation detail. Do not weaken CP1–CP3 semantics to fit CI convenience.

### M1–M4 materialized evidence snapshot

```text
uv authority                            0.12.5 / pyproject exact match
Backend CI YAML                         MATERIALIZED
Dependency Review YAML                  MATERIALIZED
Dependabot uv/github-actions             MATERIALIZED
Actions full-SHA pins                   MATERIALIZED
uv checksum                             MATERIALIZED
finite timeouts                         MATERIALIZED
local fast suite                        PASS — 32/32
local PostgreSQL suite                  PASS — 18/18
post-main regression                    PASS
main behind_by                          0
required checks                         0 / unchanged
remote PR workflow calibration          NOT RUN
exact emitted check contexts            NOT RECORDED
remote deliberate-red calibration       NOT RUN
```

## 28. CP4 direct acceptance matrix

CP4 cannot close from YAML existence or M4 local regression alone.

Required evidence, as applicable:

```text
DESIGN/SCOPE
approved CP4 exact gates                        PASS
remote changed paths exact                     PASS
unexpected paths                               0

BOOTSTRAP
canonical workstation uv exact version         RECORDED — 0.12.5
pyproject exact required-version                MATCH — ==0.12.5
CI uv version                                   PENDING M5 REMOTE EXECUTION
Python .python-version                          MATERIALIZED / M5 EXECUTION PENDING
CI Python version                               PENDING M5 REMOTE EXECUTION
uv checksum verification                        MATERIALIZED / M5 EXECUTION PENDING
locked dependency bootstrap                     LOCAL PASS / REMOTE PENDING

BACKEND QUALITY
Ruff format                                     LOCAL PASS / REMOTE PENDING
Ruff lint                                       LOCAL PASS / REMOTE PENDING
mypy strict                                     LOCAL PASS / REMOTE PENDING
fast pytest                                     LOCAL PASS — 32/32 / REMOTE PENDING
uv build                                        LOCAL PASS / REMOTE PENDING

POSTGRESQL
repository PostgreSQL image build               LOCAL PASS / REMOTE PENDING
PostgreSQL-marked acceptance                    LOCAL PASS — 18/18 / REMOTE PENDING
no SQLite substitution                          PASS BY MATERIALIZED DESIGN/HARNESS

AGGREGATION
quality success + postgres success              PENDING M5
gate PASS                                       PENDING M5
mandatory upstream deliberate failure           PENDING M6
gate FAIL on non-success upstream                PENDING M6
recovery                                        PENDING M7

DEPENDENCY REVIEW
workflow executes on real PR                    PENDING M5
exact emitted context                           PENDING M5
real dependency-policy deliberate violation     PENDING M6
uv.lock delta visibility/evaluation             PENDING M6
recovery                                        PENDING M7

SECURITY
workflow default permissions                    MATERIALIZED none
checkout jobs                                   MATERIALIZED contents: read only
checkout credentials persistence                MATERIALIZED disabled
PROD/deployment secrets in PR CI                0 BY WORKFLOW DESIGN; REMOTE PENDING
pull_request_target                             absent
Actions                                         full-SHA pinned
finite timeouts                                 present

REPOSITORY PROMOTION
required checks before calibration              0
exact real check names observed                 PENDING M5
expected source binding                         PENDING where supported
full-SHA repository enforcement                 PENDING separate M8 gate where supported
ruleset reread after mutation                   PENDING when mutation occurs
```

Items marked `where supported` remain explicitly unsupported/unverified rather than being converted into false PASS evidence.

## 29. Explicit non-claims

CP4 does not prove or implement:

```text
frontend/web/mobile CI
frontend package-manager/toolchain materialization
business/domain schema
business repositories/use cases/API
production deployment
DEV/UAT/PROD infrastructure
cloud deployment identity
release artifact promotion
SBOM/provenance production release flow
containerized backend runtime image
CodeQL post-main activation before it actually occurs
complete security assurance
Physical HG/PSV blanket PASS
frozen/blackholed PostgreSQL readiness hardening
```

CP4 quality enforcement must remain proportional to the real repository: strong enough to stop regressions, small enough that every check has a concrete reason to exist.