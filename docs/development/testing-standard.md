# DANTE — Mandatory Test Engineering Standard

- **Status:** CURRENT / NORMATIVE (active workstream candidate until integrated into protected `main`)
- **Audience:** every human contributor, AI coding agent, reviewer, and future workstream
- **Scope:** the entire monorepo: Backend, PostgreSQL, API/client, Web, Mobile, World Focus, AI, infrastructure, and cross-cutting services
- **Policy owner:** repository engineering governance; product/domain authorities own the behavior under test
- **One-line rule:** no behavior change is Done without the appropriate regression evidence, documented test intent, and an honest verification result.

This is the **canonical operational testing policy**. It is introduced from the repository root via `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, and `docs/README.md`, and is part of the agent bootstrap. The detailed verification architecture lives in [dante-verification-architecture.md](dante-verification-architecture.md); naming details live in [test-naming-and-discovery.md](test-naming-and-discovery.md). The [Temporal regression matrix](temporal-regression-testing.md) is a domain-specific supplement, **not** the whole testing standard. Historical audits and test results are evidence, not replacements for this policy.

## 1. Obligations for every code change

**Before editing:** determine what behavior, contract, security invariant, or operating constraint the change touches; read the authoritative Domain/Logical/Physical/DB/API/UI source and the owning tests. Identify whether the change is a defect correction, new behavior, refactoring, migration, removal, or tooling-only change. Determine the smallest faithful test boundary and affected neighboring boundaries. Never guess an undefined product rule merely to make a test green.

**Before claiming implementation complete:**

1. Add or update the **specific regression** that reproduces the bug or proves the new behavior. For a reproducible bug prefer red-before/green-after evidence. A safe structural refactor needs behavior-preserving equivalence checks; pure documentation edits need link/contract checks rather than fabricated application tests.
2. Exercise the **positive path, relevant refusal/error or boundary path, and high-risk interaction** with adjacent capabilities where applicable. For stateful data include replay/idempotency, historical truth, owner isolation, transaction rollback, concurrent revisions and persistence readback when relevant. For visual behavior include responsive/keyboard/accessibility/browser checks; for time include timezone/DST and clock control.
3. Keep test names, fixture boundaries, registration, documentation and impacted executable scripts current **in the same change**. Never leave an unexplained orphan file or a stale import after a rename.
4. Run focused checks during development; before full acceptance run **all** groups of `bash tooling/verify-all-current-tests-local.sh` on one candidate SHA and worktree fingerprint. Capture failures and blockers instead of hiding them. The user's WSL/PostgreSQL/browser environment remains the authoritative local execution setting.
5. For real-app UI, external provider, device, restore, and security/environment-dependent work, obtain the required separate acceptance evidence. A mocked browser run, bundle build or lint PASS never proves the real end-to-end outcome.
6. Record what ran and what did not: exact SHA/worktree state, group, command, environment, failures, log location, and acceptance status. Any subsequent source/test change reopens the gate. Never combine green results from different revisions into a fictional all-green gate.

Quality is **risk- and boundary-based**. Do not impose an arbitrary number of tests or a coverage percentage that rewards meaningless assertions. Do not skip, delete, mark xfail, weaken an assertion, or mock away the authoritative system merely to improve a gate summary.

## 2. Where tests belong (layout contract)

| Test boundary / owner | Canonical or current location | Responsibility |
| --- | --- | --- |
| Backend pure domain and application | `apps/backend/tests/unit/<capability>/test_<behavior>.py` | State transitions, algorithms, policies and validation without artificial DB claims |
| Existing Backend contract/unit legacy files | `apps/backend/tests/test_*.py` | Supported and collected; progressively classify/move during semantic qualification, **not** by cosmetic bulk relocation |
| Backend HTTP/OpenAPI | Existing relevant `apps/backend/tests/test_*_contract.py` and domain integration tests; eventual `tests/contract/` **only after a planned migration** | Request/response shape, status/error types, authz, serialization, OpenAPI compatibility |
| PostgreSQL, Alembic, Dictionary | `apps/backend/tests/integration/database/test_<behavior>.py` | Real disposable PostgreSQL 18.6, schema/ACL/constraint, fresh migration and data-bearing upgrade evidence |
| Backend cross-domain integration | `apps/backend/tests/integration/<capability>/test_<behavior>.py` | Application + persistence, authorization, transactions, time, concurrency |
| Web component/model | `apps/web/src/**/<feature>.<test>.ts(x)` — actual convention is `*.test.ts` / `*.test.tsx` next to owners | Vitest/jsdom, state, DOM, interactions, rendering |
| Browser fixture / frontend contract | `apps/web/e2e/*.spec.ts`, `apps/web/tests-browser/**/*.spec.ts` | Browser real geometry, interactions and accessibility with explicit deterministic fixture boundary |
| Browser full-stack | `apps/web/e2e/auth/*.spec.ts` (current real-stack project) | Browser → actual API → isolated PostgreSQL, reload and session/auth behavior |
| Shared packages | `packages/<package>/**/(*.test.ts|*.test.tsx)` | API client, time, i18n and package-level contracts |
| Mobile | `apps/mobile/**` as platform harnesses are genuinely implemented | Typecheck/build now; native Android/iOS/device test coverage must not be claimed until executed |
| Platform/evals/prototypes | `tooling/ai-evals/tests/`, `tooling/observability/tests/`, `tests/prototypes/` | Evaluation harness, governance, observability, prototype contracts; not substitutes for production E2E |
| Test infrastructure and evidence | `tooling/testing/`, `docs/development/`, `docs/workstreams/` | Runners, structural validators, durable rules, current workstream evidence |

**A test stays with the owner and at the boundary it actually verifies**; never invent an alternate global `tests/` hierarchy for every Web feature. Shared fixtures belong in scoped `conftest.py`, a deliberate `support/` package, or a TypeScript fixture/factory module. **Do not introduce new imports from arbitrary executable `test_*.py` files**, circular fixture dependencies, nondeterministic network calls, or reliance on the developer's persistent DB. Existing cross-test imports are known migration debt and must be removed safely, not silently broken.

## 3. Naming and test readability (mandatory)

- **Python:** `test_<capability>_<behavior>.py` with `test_<action>_<expected_outcome>[_under_condition]` functions. Prefer precise concepts, e.g. `test_session_hierarchy.py` and `test_pausing_parent_does_not_auto_resume_children`.
- **Web unit/component:** `<feature>-<behavior>.test.ts(x)`, expressive `it('...', ...)` descriptions naming observed consequence.
- **Browser:** `<user-journey>-<behavior>.spec.ts`, distinguish fixture/browser from real-stack claims in its comment and registry.
- **Never:** milestone identifiers such as `B14`, `CP6`, `M5`, `U2`; `final`, `v2`, `whole_block`, `fix_test`, `temp`, `test_new` or `hostile` used without a meaningful behavior.
- **Test body:** `Arrange → Act → Assert`, one principal observable claim; related assertions may protect the same invariant. Make failures diagnose the violated rule. Parameterize legitimate variants rather than copy/paste large suites.
- **Time/concurrency:** deterministic synthetic data, fixed/controlled clock, explicit timezone/DST, isolated actor and resources, separate readback transaction when persistence matters. Test historical facts as immutable unless the accepted correction policy permits specific edits.
- **Fidelity:** use mocks/fakes for genuinely external or nondeterministic boundaries, never replace PostgreSQL/ACL/real browser behavior with mocks and then claim authoritative coverage.

## 4. Traceability and documentation contract

`docs/development/test-case-registry.json` is the **machine-readable inventory** and routing index, not an independently authoritative product spec. Each executable test file needs a record with the real `path`, owner `suite`, `contract_id`, concrete `purpose`, enforced `invariant`, and `status`. The associated product/domain/database contract must remain the source of truth for expected behavior. Comments/docstrings in the test explain unusual fixtures, reproduction, preconditions and refusal semantics without repeating the whole spec.

For **new test files**: register them as `QUALIFIED` in the same commit, with meaningful (not placeholder) `purpose` and `invariant`, an appropriate contract, executable assertions and relevant negative/boundary coverage. `tooling/testing/verify_test_integrity.py` rejects unregistered new files, unqualified new files, placeholder-length intent, and selected broken references. Update the owning workstream map/coverage matrix if a scenario or gap has changed.

For **existing tests**: initial `UNREVIEWED` reflects a name-based structural inventory, **not** an audit of their assertions, quality, or PASS. Promote to `QUALIFIED` only after checking the actual test cases, accepted contract, rejection path, overlap, fixtures and execution proof. File-level inventory is the current implemented granularity: future per-case IDs/invariant mappings need explicit design and cannot be claimed as already implemented. Do not stamp hundreds of existing tests QUALIFIED based on filenames alone.

A test may be `DEPRECATED_PENDING_REPLACEMENT` only with a reason, an explicit current product rule, replacement test(s), and recorded review/evidence. Retire obsolete tests only when the replacement covers the still-accepted invariant or a superseding authoritative decision deliberately removes it. Keep historical results immutable; reconcile current docs and executable references rather than rewriting past evidence.

### Example traceability record (illustrative, not permission to bypass review)

```json
{
  "path": "apps/backend/tests/integration/temporal/test_session_hierarchy.py",
  "suite": "temporal-postgresql-integration",
  "contract_id": "T06",
  "purpose": "Verify that pausing the parent session pauses actively running child sessions in canonical persistence.",
  "invariant": "Resuming the parent never resumes a child that remains explicitly paused.",
  "status": "QUALIFIED"
}
```

This example is **not** a claim that the current file was audited; its real registry record stays UNREVIEWED until qualified. For new cases, choose the exact justified contract; provisional T/P categories inherited from the migration are not automatic coverage certification.

## 5. Running tests and labeling results

From the repo root, first check structural integrity:

```bash
python3 tooling/check-test-file-names.py
python3 tooling/testing/verify_test_integrity.py
```

For focused Backend verification use the backend workspace and pytest/ruff/mypy for changed paths; for Web use Vitest from `apps/web` and the appropriate Playwright config. For data changes validate with the repository's isolated real PostgreSQL fixtures. Then run the **single full local gate**:

```bash
bash tooling/verify-all-current-tests-local.sh
```

That runner includes naming/registry, Python quality, TypeScript lint/typecheck, architecture, generated drift, build, mobile bundle, Backend non-PostgreSQL and PostgreSQL, eval/observability/prototype checks, package/Web tests, browser fixtures and real-stack browser. Specialized safety, destructive recovery, provider UAT, performance, native device and release tests have their own evidence/acceptance boundaries and are not magically included just because the runner finishes.

Use only `PASS`, `FAIL`, `BLOCKED_ENV`, `NOT_RUN` and `NON_APPLICABILE` (with explanation) against **the exact test/scope/SHA**. One failure, missing mandatory suite, or blocked required acceptance means **no global PASS**. Never reinterpret an earlier RED as green because imports were edited or a renamed file exists.

## 6. Quality gate and review checklist

Reviewers and agents must verify:
- The feature/fix has its correct owning test boundary and contract, not just a renamed/green file.
- Positive, refusal, boundary and cross-capability risks were considered and selected with justification; code and assertions match actual accepted product semantics.
- Registry record, names, fixture ownership, generated artefact discipline, test commands and evidence are updated; new test files are QUALIFIED.
- PostgreSQL checks use disposable real PostgreSQL; no production/customer data, shared destructive operations or unsafe provider actions.
- A full gate result is reported honestly on the same candidate; visual/device/provider proof is kept separate when needed.
- Deprecations, changed requirements, skips, flaky tests and missing coverage have a named owner/replacement or explicit unresolved state. No silent weakening.

## 7. What is enforced today versus planned

**Automated today (in the candidate branch):** filename-stage check, test-file inventory against actual discovery, new-file registry/QUALIFIED obligation, basic purpose/invariant fields, stale Python imports/plugins and script references; quality and test groups through the WSL full gate. This policy's discoverability from mandatory entry points is also checked by the integrity gate.

**Not yet automatically certified:** quality or adequacy of each assertion, the exact coverage of every contract/case, complete upgrade/recovery/provider/native-device acceptance and semantic qualification of existing UNREVIEWED tests. These are tracked obligations, not implicit PASS.

No new GitHub Actions or protected-main required check is established by this document. It governs the active candidate branch immediately; propagation to protected `main` follows its normal review/integration rules.

## Complete single-run gate and diagnostic archive

From a clean checkout of feature/timeline-temporal-operational, run:

    python3 tooling/testing/run_complete_gate.py

For a clean review branch, set `DANTE_GATE_BRANCH` to the checked-out branch
when invoking either the sequential or parallel runner. The runner still
checks the branch, clean worktree, pinned SHA and full test inventory.

The wrapper invokes the entire existing tooling/verify-all-current-tests-local.sh
inventory: 27 checks across PostgreSQL/Alembic, backend, API/TypeScript,
architecture, generation, build, mobile, lint, formatting, frontend, tooling
and both fixture and real-stack browser tests. It neither selects a subset
nor hides failed tests; the authoritative gate remains unchanged.

It refuses dirty worktrees, records the pinned candidate SHA and complete
console output, aggregates each group result, and packages original unedited
group logs plus FULL_GATE_SUMMARY.md into one private .tar.gz archive under
<repo>/temp/dante-all-tests.XXXXXX/FULL_GATE_LOGS.tar.gz. The root temp/
directory is explicitly ignored by Git, Prettier, and ESLint.
For a short copy/paste use <repo>/temp/LATEST_GATE_SUMMARY.md; for
the complete evidence upload the archive. Each run gets its own folder.
Share that archive for batch diagnosis instead of five-test microcycles.
Group failures and an incomplete run keep the full gate RED.
For each Playwright gate, the full runner also preserves every available
`error-context.md` and up to three original `trace.zip` artifacts under
`<repo>/temp/dante-all-tests.XXXXXX/<WEB_BROWSER_GROUP>_BROWSER_ARTIFACTS/`
**before** the next browser group overwrites `apps/web/test-results`.
These are diagnostic evidence, not fixture substitutes; larger artifacts
remain in the WSL test-results directory and may need separate review.


Concurrent writes to generated sources and shared Playwright build outputs
have not been proven isolated. This wrapper deliberately does not change
worker counts or relax the source-stability gate. Review logs for locally
sensitive information before sharing or publishing.

## Optional parallel gate (the sequential reference stays unchanged)

**Reference/sequential:** `python3 tooling/testing/run_complete_gate.py`.

**Separate, opt-in parallel runner:**
`python3 tooling/testing/run_parallel_gate.py --group-workers 3 --postgres-workers 5`.
To use ten PostgreSQL processes, specify `--postgres-workers 10`
only when Docker has adequate available RAM/CPU; to inspect commands only,
use `--dry-run`. Do not run parallel and sequential gates concurrently.

The parallel runner parses all actual gate declarations from the original
`tooling/verify-all-current-tests-local.sh`, refuses to execute if any group
is added, renamed or removed without an isolation review, and executes all 27
original commands. It never changes the original suite or quality thresholds.
Independent read-only groups use concurrent subprocesses. Generated sources,
builds, and browser gates stay serialized where their outputs or server ports
might conflict. PostgreSQL uses a **dynamic job queue**, with four queued jobs per
PostgreSQL worker by default (adjustable via
`--postgres-jobs-per-worker 2..8`). Once any pytest subprocess ends, its
worker takes the next available job immediately. Up to 5 or 10 disposable
PostgreSQL containers remain active at once; the number of processes/jobs
executed over the complete run may be larger than that limit. The PostgreSQL
queue starts while the independent quality/test groups and serial
build lane run, so there is no full-phase barrier before database work.
No running individual test can be divided across threads: jobs are
whole test modules and worker processes, never interrupted or duplicated.

PostgreSQL is divided by complete test module, using
`pytest --collect-only -m postgres` as its inventory: every selected case
belongs to exactly one shard, and each separate pytest process has its own
session-scoped disposable Docker PostgreSQL 18.6 cluster, uniquely named and
labelled PostgreSQL data volume, and unique database fixture. Fixture teardown
removes that exact container and its data volume. Before the queue starts, the
runner also removes only dangling volumes that carry the same DANTE acceptance
label and matching generated name; it never prunes anonymous Docker resources
or Compose/local named volumes. Each shard keeps its complete original pytest
log and explicit node-id manifest. No `pytest-xdist` installation or test-fixture
rewrite is required.

The resulting logs and archive are saved under the Git-ignored
`temp/dante-parallel-gate.XXXXXX/`; `LATEST_GATE_SUMMARY.md` is updated.
Browser screenshots/errors and at most three traces are copied before the next
Playwright gate overwrites test-results. A failed shard fails the entire
PostgreSQL group; missing groups, failures, or a dirty/changed source tree
keep the whole parallel gate RED. The parallel implementation itself requires
a real WSL run before its performance or behavioral equivalence can be
certified. The sequential gate remains the fallback authoritative mode.


### Resource-aware parallel gate (13 October 2026 candidate)

The **opt-in** `tooling/testing/run_parallel_gate.py` retains the exact
27-group inventory from the authoritative sequential runner. Its default
budgets are now `--group-workers 5 --postgres-workers 3
--postgres-jobs-per-worker 3 --nonauth-workers 3`, chosen for the recorded
Docker loopback-port and restart failures at 5–10 disposable PG containers.
These are **independent limits**, not one pool of 15 PostgreSQL containers.
Override them for an observed machine budget; no speedup or complete PASS is
claimed without measured WSL evidence.

PostgreSQL modules stay indivisible to preserve fixtures/test order. Jobs run
in a refilling shared queue (next free worker pulls the next job), prioritized
by prior per-module pytest setup/call/teardown durations when present. The
first run falls back to collected-test counts. The runner writes an
ignored `temp/POSTGRES_MODULE_TIMINGS.json` profile for subsequent runs and
full shard timing evidence in `BACKEND_POSTGRES_SHARD_TIMINGS.json` inside
the gate log archive. It also writes `temp/GATE_GROUP_TIMINGS.json` to
prioritize long read-only groups on later runs. Timing files affect **order
only**, never the number of cases selected or any PASS/FAIL requirement.

After the serial generated/build lane, the browser fixture gate and the
non-auth browser gate run one after the other **while** the PostgreSQL
queue may still be active; their server ports remain separate, and browser
test-results are archived before another browser gate runs. Only the
opt-in parallel runner sets `DANTE_E2E_NONAUTH_WORKERS` (default 3);
direct `playwright.config.ts` usage remains one worker. The real-stack
auth Playwright gate stays **one worker** and starts **after** PostgreSQL
has completely drained, because several of its actual tests deliberately
stop and restart a real PostgreSQL instance. It cannot safely join the
other PostgreSQL or browser pools without stronger resource isolation.

Use:
```bash
python3 tooling/testing/run_parallel_gate.py --self-test
python3 tooling/testing/run_parallel_gate.py --dry-run
python3 tooling/testing/run_parallel_gate.py \
  --group-workers 5 --postgres-workers 3 \
  --postgres-jobs-per-worker 3 --nonauth-workers 3
```
The timing profiles and artifacts remain in ignored `temp/`; source must
remain clean and on the same SHA. Historical result `6476a5c1`: 1713.3s
total, `WEB_BROWSER_REAL_STACK` 918.6s, `WEB_BROWSER_NONAUTH` 395.5s,
`BACKEND_POSTGRES` 392.5s. Most of the total duration was in the two
**serial browser gates**; more PostgreSQL workers alone cannot fix that.
These scheduler changes are unverified on WSL and must not be presented as
a demonstrated speed gain or a green full gate.
