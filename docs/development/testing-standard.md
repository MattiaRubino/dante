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

Concurrent writes to generated sources and shared Playwright build outputs
have not been proven isolated. This wrapper deliberately does not change
worker counts or relax the source-stability gate. Review logs for locally
sensitive information before sharing or publishing.
