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

Read, in order:

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

For Physical-consuming backend implementation also reread at minimum:

- PM-11 accepted Physical target;
- PM-12 operational/stack posture;
- post-selection validation register.

For the next production scaffold specifically, also inspect the exact root tree, `.github`, existing config/manifests/workflows, current branch protections/settings where relevant and the Engineering Foundation closure sources.

## 3. Current closed engineering baseline

Engineering Foundation v0 is **CLOSED / ACCEPTED**.

Do not reopen it by default.

Key backend decisions:

```text
one existing product monorepo
apps/backend + apps/web + apps/mobile
backend capability-first modular monolith
Python 3.14.x / initial 3.14.7
uv / Ruff / mypy strict / pytest / Hypothesis
Windows backend through WSL2/Linux semantics
PyCharm WSL workflow supported; repo IDE-neutral
Docker Compose for LOCAL stateful infra
PostgreSQL 18.4 + full selected extension envelope enabled from first LOCAL DB
SQLAlchemy 2.0 stable line + psycopg 3 + Alembic
typed pydantic-settings config
risk-layered real-PostgreSQL testing
GitHub Actions / protected main / supply-chain hardening
LOCAL → DEV → UAT → PROD environments, not branches
```

Frontend internal tooling/testing/release implementation is deferred to the frontend workstream.

Cloud provider/IaC engine is deferred to first remote infrastructure.

## 4. Current next boundary

Production implementation continues in the current repository. Do not create a new repository.

Before scaffold:

```text
repository rename decision
lifeos → dante recommended
```

Execute it in its own explicit governance scope or explicitly defer it.

Then open the production scaffold workstream/gate under `apps/backend`.

## 5. No silent scope expansion

A bounded task does not authorize adjacent work.

Examples:

- backend scaffold does not authorize concrete Domain/Logical schema unless explicitly included;
- Foundation closure does not authorize production code;
- frontend prototype/design does not override backend architecture truth;
- selected Physical component does not mean activated/deployed component;
- cloud/provider decision is not inferred from recovery/object providers already selected for bounded roles.

When a material new decision appears, stop the decision—not necessarily the entire task—and establish the appropriate approval/gate before durable write.

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

Immediately before first write:

```text
current HEAD == approved PRE-SCOPE → proceed
current HEAD != approved PRE-SCOPE → STOP, inspect, re-gate
```

Never silently continue on a moved branch.

## 7. Protected main

`main` is the only integrated source truth.

Normal durable flow:

```text
bounded branch
→ reviewed/validated commits
→ PR
→ protected-main integration
```

No direct protected-main edit/merge bypass is accepted merely for convenience.

Use expected-head protection when merging through automation/tooling so a moved PR head cannot be merged silently.

## 8. Commit/write discipline

Prefer commits that are:

- bounded by one coherent purpose;
- reviewable;
- truthful about what changed;
- free from unrelated formatting/content churn.

Do not manufacture one commit per tiny file when one atomic coherent commit is safer, and do not combine unrelated decisions merely to reduce commit count.

Do not rewrite/force-push shared history casually. Any history rewrite requires an explicit reason/authorization and proof of branch ownership/safety.

## 9. Post-write QA

Against the approved PRE-SCOPE prove:

- expected changed paths == actual;
- expected CREATE == actual adds;
- expected UPDATE == actual modifications;
- expected DELETE == actual deletes;
- unexpected/out-of-scope == 0;
- branch ahead/behind relationship is expected;
- remote payload/readback matches intended content;
- PR changed paths are exact where a PR exists;
- real checks/statuses are inspected when applicable;
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

This remains true during the production scaffold.

## 11. Documentation is implementation

Distinguish:

```text
CURRENT SPECIFICATION
current truth only

ADR / TECHNICAL DECISION
current decision + rationale/status/supersession

HISTORICAL / VALIDATION EVIDENCE
truthful chronology

GIT / PR HISTORY
recoverable implementation history
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

Closed validation/closure evidence remains historical and must not be edited merely to align wording with a later state.

In particular, PM-14 closure evidence remains protected historical evidence. Changes to historical artifacts require an explicit evidence-correction reason, not current-truth cleanup.

## 13. Domain/Logical/Physical reopen rule

Engineering implementation consumes closed models.

A concrete contradiction found during implementation may reopen only the affected decision under an explicit architecture/model reopen scope.

Do not weaken accepted semantics to fit a convenient database/ORM/API/tool behavior.

A failed applicable PSV may reopen the affected Physical decision but cannot silently weaken Domain/Logical requirements.

## 14. Implementation evidence truth

Keep these distinctions explicit:

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != complete system PASS
```

Current direct selected-stack evidence remains NOT RUN until real artifacts/harness exist.

## 15. Secrets / production data

Never commit live credentials, keys, tokens, `.env` secrets or raw production DB dumps.

Lower-environment data is synthetic by default. Production-derived clones require explicit sanitization/minimization and authorization.

Normal PR CI receives no PROD deployment identity.

## 16. Development environment discipline

Backend canonical semantics are Linux.

For the primary Windows workflow:

- keep backend repo/worktree in WSL filesystem;
- run Python/uv/backend commands under WSL/Linux;
- PyCharm may use a WSL interpreter for run/debug/test;
- use Docker Compose for stateful LOCAL dependencies;
- do not share one virtualenv between native Windows and WSL execution.

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
- placeholder IaC/services/directories.

When scale/ownership/security creates a real need, introduce the mechanism through explicit architecture change.

## 18. Current continuation instruction

A new chat should:

1. read current main and the Engineering Foundation closure handoff;
2. verify repository/ref state;
3. **not** restart Foundation selection;
4. keep the current repository;
5. address repository rename `lifeos → dante` as the first small governance decision/action, or explicitly defer;
6. then create a fresh branch/gate for real `apps/backend` scaffold;
7. run scaffold QA before concrete schema/business implementation.
