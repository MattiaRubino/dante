# DANTE Development Operating Rules

- Status: **CURRENT**

These rules govern repository-backed project work. Durable repository truth outranks conversational memory.

## 1. Authority order

When sources conflict:

1. current `main` code/migrations/tests and current accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current sources inside that workstream;
5. historical evidence/closed branches/Git history;
6. conversation memory.

A user instruction may clarify/reopen a decision, but durable project truth changes only through an approved repository scope.

## 2. Mandatory bootstrap before design or writes

Read in order:

```text
README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/development/operating-rules.md
→ docs/development/documentation-and-handoff.md
→ docs/development/branching-and-environments.md
→ docs/development/repository-engineering-safety.md
→ active workstream handoff, if any
→ current model/architecture index + linked accepted sources
→ relevant ADR/evidence/methodology
→ relevant code/tests/manifests
→ current Git refs and relation to main
```

For Physical-consuming implementation also reread the accepted Physical target and applicable post-selection validation register.

For a production scaffold/materialization scope inspect the exact root tree, `.github`, existing config/manifests/workflows, current remote settings where relevant and the applicable closed/accepted Foundation sources.

## 3. Current closed/active engineering baseline

Engineering Foundation v0 is **CLOSED / ACCEPTED** and is not reopened by default.

Backend baseline:

```text
one product monorepo
apps/backend + apps/web + apps/mobile
backend capability-first modular monolith
Python 3.14.x / initial 3.14.7
uv / Ruff / mypy strict / pytest / Hypothesis
WSL2/Linux canonical backend semantics on Windows
PyCharm WSL supported; repo IDE-neutral
Docker Compose for LOCAL stateful infra
PostgreSQL 18.4 + full selected extension envelope from first LOCAL DB
SQLAlchemy 2.0 stable + psycopg 3 + Alembic
pydantic-settings typed config
risk-layered real-PostgreSQL testing
GitHub Actions / protected main / supply-chain hardening
LOCAL → DEV → UAT → PROD environments, not branches
```

Frontend Engineering Foundation is **DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS / INTEGRATED VIA PR #22**. Its specifications/ADRs/final-review evidence are current `main` authority. The former `feature/frontend-foundation` branch was merged and auto-deleted. Direct implementation validation remains **NOT RUN**.

Backend cloud compute/IaC remains deferred to first real remote infrastructure boundary.

## 4. Current next boundary

Production implementation remains in the current repository. Do not create a new repository.

Frontend sequence:

```text
fresh exact materialization/scaffold scope
→ materialize only accepted real workspace/app/package artifacts
→ execute direct frontend validations progressively
→ open product-surface implementation only when relevant foundation/contracts exist
```

Backend production scaffold remains a separate **NOT STARTED** implementation scope and requires its own fresh gate.

Repository rename history/governance is not an implicit prerequisite for frontend materialization and must not be reintroduced as a blocking pseudo-phase.

## 5. No silent scope expansion

A bounded task does not authorize adjacent work.

Examples:

- backend scaffold does not authorize concrete Domain/Logical schema unless explicitly included;
- Foundation closure does not authorize production code;
- frontend architecture does not authorize product-surface implementation;
- prototype/design does not override production architecture truth;
- selected Physical/frontend component does not mean activated/deployed component;
- cloud/provider decision is not inferred from recovery/object/delivery providers already selected for bounded roles.

When a material new decision appears, stop that decision and establish the appropriate approval/gate before durable write.

## 6. Exact remote Git write gate

Before a remote Git write, state:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact current SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<what will not be touched>
```

Immediately before the first write:

```text
current HEAD == approved PRE-SCOPE → proceed
current HEAD != approved PRE-SCOPE → STOP / inspect / re-gate
```

Never silently continue on a moved branch.

## 7. Protected main

`main` is the only integrated source truth.

Normal flow:

```text
bounded branch
→ reviewed/validated commits
→ PR
→ protected-main integration
```

No direct-main bypass merely for convenience. Use expected-head protection when merging through tooling so a moved PR head cannot be merged silently.

## 8. Commit/write discipline

Commits should be bounded, reviewable, truthful and free from unrelated churn.

Do not manufacture one commit per tiny file when one coherent commit is safer. Do not combine unrelated decisions merely to reduce commit count.

Do not rewrite/force-push shared history casually; any history rewrite requires explicit reason/authorization and proof of safety.

## 9. Post-write QA

Against the approved PRE-SCOPE prove:

- expected changed paths == actual;
- CREATE/UPDATE/DELETE classification matches;
- unexpected/out-of-scope == 0;
- ahead/behind relation is expected;
- remote payload/readback matches intended content;
- PR changed paths are exact where applicable;
- real checks/statuses are inspected where applicable;
- protected-main integration uses expected head;
- post-merge `main` is reread/compared;
- branch lifecycle/autodelete is verified when relevant.

Never call a workstream PASS/CLOSED only because a write API returned success.

## 10. Required-check activation rule

Never configure a guessed future status-check name.

```text
workflow/job exists
+ runs on relevant PR
+ stable emitted context verified remotely
+ success/failure observed
+ failure genuinely means merge must stop
→ only then exact context may become required
```

This applies equally to backend and frontend workflows.

## 11. Documentation is implementation

Distinguish:

```text
CURRENT SPECIFICATION      current truth only
ADR / TECH DECISION       current decision + rationale/status/supersession
HISTORICAL / VALIDATION   truthful chronology/evidence
GIT / PR HISTORY          recoverable history
```

Do not rewrite historical evidence to pretend it knew later decisions.

Before deleting/replacing meaningful current docs prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

Tool/size-driven document splits must be lossless physical partitioning, not silent summaries.

## 12. Historical evidence protection

Closed validation/closure evidence remains historical and is not edited merely to align wording with a later state.

Changes to historical artifacts require an explicit evidence-correction reason rather than current-truth cleanup.

## 13. Domain/Logical/Physical/Engineering/Frontend reopen rule

Implementation consumes closed models/Foundation decisions.

A concrete contradiction may reopen only the affected decision under an explicit scope.

Do not weaken accepted semantics to fit a convenient database/ORM/API/frontend/tool behavior.

A failed applicable validation may reopen the affected Physical/frontend technology/adapter decision but cannot silently weaken Domain/Logical requirements.

## 14. Implementation evidence truth

Keep distinctions explicit:

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != complete system PASS
```

Direct evidence remains NOT RUN until real artifacts/harness exist.

Architecture/design closure may be truthful before implementation; it must not be mislabeled as implementation PASS.

## 15. Secrets / production data

Never commit live credentials, keys, tokens, `.env` secrets or raw production dumps.

Lower-environment data is synthetic by default. Production-derived clones require explicit sanitization/minimization/authorization.

Normal PR CI receives no PROD deployment identity.

Anything shipped in Web/mobile client bundles is public client configuration, not a secret.

## 16. Development environment discipline

Backend canonical semantics are Linux.

Primary Windows posture:

- one authoritative repository/worktree in WSL filesystem;
- Python/uv/backend under WSL/Linux semantics;
- Node/pnpm/Turbo/Vite/Metro/Expo CLI may use the same WSL-backed checkout for the selected frontend posture;
- PyCharm/JetBrains may use WSL tooling/interpreters;
- Docker Compose owns stateful LOCAL dependencies;
- do not maintain divergent Windows/WSL source clones;
- do not share one virtualenv/node_modules environment across incompatible OS semantics.

WSL↔Windows Android/ADB/Metro mechanics remain a directly validated tooling adapter, not a product architecture invariant.

Repository commands remain CLI-reproducible and IDE-neutral.

## 17. No enterprise cosplay

Professional quality means real boundaries/evidence, not maximum component count.

Do not introduce without measured need:

- microservices;
- Kubernetes;
- brokers/service zoo;
- self-hosted CI runners;
- merge queues;
- multiple repositories;
- extra permanent environment branches;
- fake reviewer requirements;
- placeholder IaC/services/directories;
- speculative shared frontend packages;
- dormant specialist libraries without a real consumer.

Introduce mechanisms only when scale/ownership/security/product requirements create a real need.

## 18. Current continuation instruction

A new chat must first read current `main`, current global status and any active bounded workstream handoff.

Frontend Foundation is integrated through PR #22. Do not restart stack/architecture selection without concrete contradictory evidence or a materially changed requirement.

Current frontend continuation:

```text
read integrated frontend Foundation specs + ADR-008/009 + closure evidence
→ verify current main/root/manifests/workflows before writes
→ open fresh bounded production materialization/scaffold/direct-validation scope
→ materialize and validate progressively
```

Backend production scaffold remains separate and not implicitly authorized by frontend closure/integration.
