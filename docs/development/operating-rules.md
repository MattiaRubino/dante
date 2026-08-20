# DANTE Development Operating Rules

- Status: **CURRENT**

Durable repository truth outranks conversational memory.

## 1. Authority order

1. current `main` code/migrations/tests and accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current active-workstream sources;
5. historical evidence/closed branches/Git history;
6. conversation memory.

A user instruction may reopen a decision, but durable truth changes only through approved repository scope.

## 2. Mandatory bootstrap

```text
README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ agent-operating-manual.md
→ operating-rules.md
→ documentation-and-handoff.md
→ branching-and-environments.md
→ repository-engineering-safety.md
→ active workstream handoff if any
→ current architecture/model index + linked sources
→ relevant ADR/evidence
→ relevant code/tests/manifests
→ Git refs/relation to main
```

Physical-consuming implementation also reads accepted Physical targets/registers. Production materialization inspects actual root/config/workflows/settings and applicable Foundation sources.

## 3. Current engineering baseline

Engineering Foundation v0: **CLOSED / ACCEPTED**.

Frontend Engineering Foundation: **DESIGN/ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS on `feature/frontend-foundation`, PENDING MAIN INTEGRATION**.

Direct frontend implementation validation remains **NOT RUN**.

Backend cloud compute/IaC remains deferred to its real remote boundary.

## 4. Current next boundary

```text
Frontend Foundation
prepare protected-main integration
→ PR only with explicit authorization
→ merge only with explicit authorization/expected-head safety
→ post-merge readback
→ new bounded materialization/direct-validation scope
```

Backend production scaffold remains a separate NOT STARTED scope.

## 5. No silent scope expansion

A bounded task does not authorize adjacent work. Foundation closure does not authorize production code. Frontend architecture does not authorize product-surface implementation. Selected component does not mean activated/deployed. Provider decisions are not inferred from providers already selected for bounded roles.

New material decisions require appropriate approval/gate.

## 6. Exact remote Git write gate

Before any remote content write state exact:

```text
BRANCH
PRE-SCOPE
CREATE
UPDATE
DELETE
PURPOSE
EXPLICITLY OUT OF SCOPE
```

Immediately before first write verify current HEAD == PRE-SCOPE; if moved, stop/inspect/re-gate.

## 7. Protected main

`main` is only integrated truth.

```text
bounded branch
→ reviewed/validated commits
→ PR
→ protected-main integration
```

No direct-main convenience bypass. Use expected-head safety when merging through tooling.

## 8. Commit/write discipline

Commits are bounded, reviewable, truthful and free from unrelated churn. Do not manufacture micro-commits or combine unrelated changes merely for count. Shared history rewrite requires explicit reason/authorization/safety proof.

## 9. Post-write QA

Prove against PRE-SCOPE:

- expected paths == actual;
- CREATE/UPDATE/DELETE match;
- unexpected == 0;
- branch relation expected;
- remote readback matches;
- PR paths/checks exact where applicable;
- expected-head merge safety;
- post-merge main readback;
- branch lifecycle verification where relevant.

Never call PASS/CLOSED merely from a successful write API.

## 10. Required-check activation

A check becomes required only after the real workflow/job runs on relevant PRs, emits a stable observed context, success/failure is observed and failure genuinely must block merge. Never guess future check names.

## 11. Documentation is implementation

```text
CURRENT SPECIFICATION    current truth
ADR                      decision/rationale/status/supersession
HISTORICAL/VALIDATION    truthful chronology
GIT/PR HISTORY           recoverable history
```

Before replacing/deleting meaningful current docs prove no valid requirement/rationale is lost and navigation/current truth is repaired. Tool-limit splits are lossless, not summaries.

## 12. Historical evidence protection

Historical/closure evidence is not rewritten merely to align wording with later state. Corrections require an explicit evidence reason.

## 13. Reopen rule

Implementation consumes closed Domain/Logical/Physical/Engineering/Frontend Foundation decisions. A concrete contradiction may reopen only the affected decision under explicit scope. Never weaken semantics to fit convenient tools.

Failed validation may reopen an affected technology/adapter/Physical decision but not silently weaken Domain/Logical authority.

## 14. Evidence truth

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != whole-system PASS
```

Architecture closure may precede implementation and must never be relabeled as direct PASS.

## 15. Secrets / production data

Never commit credentials/tokens/secrets/raw production dumps. Lower-environment data synthetic by default; production-derived clones require explicit sanitization/minimization/authorization. Normal PR CI gets no PROD identity. Anything shipped in Web/mobile client bundles is public config, not a secret.

## 16. Development environment discipline

Primary Windows posture uses one authoritative WSL-backed checkout. Python/backend and selected Node/frontend tooling use that source tree under their accepted semantics; JetBrains/PyCharm supported; Docker Compose owns stateful LOCAL dependencies.

No divergent Windows/WSL source clones and no cross-OS environment sharing that violates runtime semantics. WSL↔Windows Android/ADB/Metro is a directly validated tooling adapter.

Repository commands remain CLI reproducible and IDE neutral.

## 17. No enterprise cosplay

Do not introduce without measured need: microservices, Kubernetes, broker/service zoo, self-hosted CI, merge queue, multiple repos, permanent environment branches, fake reviewers, placeholder infra/services/directories, speculative shared frontend packages or dormant specialist libraries without consumers.

## 18. Current continuation instruction

Until Frontend Foundation integrates:

```text
verify feature/frontend-foundation relation to main
→ read closure handoff + both frontend specs + final review + ADR-008/009
→ do not restart technology/architecture selection
→ perform integration work only under explicit scope/authorization
```

After integration, open a fresh frontend materialization/direct-validation workstream. Backend production scaffold remains separate/not implicitly authorized.
