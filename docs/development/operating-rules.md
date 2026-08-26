# DANTE Development Operating Rules

- **Status:** CURRENT
- **Last reconciled:** 2026-08-26

These rules govern repository-backed project work. Durable repository truth outranks conversational memory.

## 1. Authority order

When sources conflict:

1. current protected-`main` code/migrations/tests and current accepted model/ADR decisions;
2. current durable product/domain/logical/architecture/engineering/database docs on protected `main`;
3. active bounded unmerged branch workstream record for its own scope;
4. other explicit current sources inside that branch;
5. historical evidence, archive, closed branches and Git/PR history;
6. conversation memory.

A user instruction may clarify or deliberately reopen a decision, but durable project truth changes only through the appropriate repository scope.

An unmerged branch may contain newer truth for its bounded workstream. It is not a second global source of truth.

## 2. Mandatory bootstrap before design or writes

Read in order:

```text
README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ docs/ROADMAP.md when sequence matters
→ docs/development/agent-operating-manual.md
→ docs/development/operating-rules.md
→ docs/development/documentation-and-handoff.md
→ docs/development/documentation-lifecycle-policy.md
→ docs/development/branching-and-environments.md
→ docs/development/repository-engineering-safety.md
→ current subsystem/model/architecture authority
→ relevant ADR/evidence/methodology
→ relevant code/tests/manifests/migrations
→ current Git refs and relation to main
→ active branch-local workstream record/handoff only when that branch is the target
```

Do not infer current state from a historical file merely because it is detailed or marked Accepted.

For Physical-consuming implementation, reread the accepted Physical target and applicable post-selection validation register.

For production scaffold/materialization/evolution scopes inspect exact root tree, `.github`, existing config/manifests/workflows, current remote settings where relevant and the applicable accepted Foundation/subsystem sources.

## 3. Current closed/active engineering baseline

Current protected-main baseline:

```text
Product / North Star                    CURRENT
Domain Model                            CLOSED
Logical Model                           CLOSED
Pre-Physical coherence                  CLOSED
Physical target                         CLOSED / ACCEPTED
Engineering Foundation                  CLOSED / ACCEPTED
Frontend Engineering Foundation         CLOSED / INTEGRATED VIA PR #22
Frontend Materialization                CLOSED / PASS / INTEGRATED VIA PR #28
Backend CP1–CP5 Scaffold                CLOSED / DIRECT QA / INTEGRATED VIA PR #24
Backend CP6 Database                    CLOSED / DIRECT QA / INTEGRATED VIA PR #42
PostgreSQL                              18.6 current patch
Alembic                                 20260826_08
Access frontend                         ACTIVE / UNMERGED ON feature/access-frontend
Post-CP6 backend product vertical       NOT STARTED ON A DEDICATED BRANCH
```

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
PostgreSQL 18 major family / current patch 18.6
SQLAlchemy 2.0 stable + psycopg 3 + Alembic
pydantic-settings typed config
risk-layered real-PostgreSQL testing
GitHub Actions / protected main / supply-chain hardening
LOCAL → DEV → UAT → PROD environments, not branches
```

Current materialized DANTE database baseline:

```text
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

Frontend Engineering Foundation and generic production materialization are closed/integrated. New frontend work is bounded product/vertical work, not another generic foundation/materialization phase.

Backend cloud compute/IaC remains deferred to the first real remote infrastructure boundary.

## 4. Current next boundaries

Production implementation remains in this repository. Do not create a new implementation repository.

Current active product branch:

```text
feature/access-frontend
→ continue the existing Access frontend workstream
→ do not create another Access branch/worktree merely because a chat changes
→ Access remains unmerged/open until real backend/full-stack/release closure
```

Backend next:

```text
post-CP6 product vertical
→ create a new bounded branch from current protected main only when explicitly scoped
→ consume the already-materialized database
→ use normal forward schema evolution only for genuine new requirements
```

Documentation maintenance follows the current lifecycle/current-truth policy. Create a bounded `docs/` or `chore/` branch only when real documentation work exists; there is no permanent documentation-cleanup development line.

No current workstream should be restarted from an older Foundation/CP6 roadmap merely because historical records remain in the tree.

## 5. No silent scope expansion

A bounded task does not authorize adjacent work.

Examples:

- documentation cleanup does not authorize code/schema behavior changes;
- backend product vertical does not authorize reopening closed Domain/Logical/Physical semantics without a concrete contradiction;
- a later DB evolution does not authorize redesigning CP6 wholesale;
- frontend vertical work does not authorize generic stack re-selection;
- prototype/design does not override production architecture truth;
- selected Physical/frontend component does not mean activated/deployed component;
- cloud/provider decision is not inferred from bounded recovery/object/delivery providers already selected for other roles.

When a material new decision appears, establish the appropriate scope before durable write.

## 6. Exact remote Git write gate

Before a remote Git write, establish:

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

For a clearly approved multi-file cleanup/workstream, later sequential commits on the same already-approved bounded scope do not require inventing a new branch merely because HEAD advances from the assistant's own preceding approved writes. Unexpected external movement still requires inspection.

## 7. Protected main

`main` is the only integrated source truth.

Normal flow:

```text
bounded branch
→ reviewed/validated commits
→ PR
→ required checks
→ protected-main integration
```

Effective live ruleset `lifeos-main-safety` currently requires:

```text
merge commit only
branch current with main
review threads resolved
Backend CI Gate
Dependency Review
Frontend CI Gate
no bypass actors
non-fast-forward protection
deletion protection
```

No direct-main bypass merely for convenience. Use expected-head protection when merging through tooling so a moved PR head cannot be merged silently.

## 8. Commit/write discipline

Commits should be bounded, reviewable, truthful and free from unrelated churn.

Do not manufacture one commit per tiny file when one coherent commit is safer. Tooling that writes one file per contents-API commit is acceptable when the resulting PR diff remains bounded and reviewable; do not confuse connector commit granularity with architectural scope.

Do not combine unrelated decisions merely to reduce commit count.

Do not rewrite/force-push shared history casually; any history rewrite requires explicit reason/authorization and proof of safety.

## 9. Post-write QA

Against the intended scope prove:

- expected changed paths == actual;
- CREATE/UPDATE/DELETE classification matches;
- unexpected/out-of-scope == 0;
- ahead/behind relation is expected;
- remote payload/readback matches intended content;
- links/references remain valid where documentation changes;
- PR changed paths are exact where applicable;
- real checks/statuses are inspected where applicable;
- protected-main integration uses expected current head;
- post-merge `main` is reread/compared;
- branch lifecycle/autodelete is verified when relevant.

Never call a workstream PASS/CLOSED only because a write API returned success.

A failed/conflicted/no-op write is not completion.

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

Current exact required contexts are remotely verified as:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

## 11. Documentation is implementation

Distinguish:

```text
CURRENT SPECIFICATION      current truth only
ADR / DURABLE REFERENCE   accepted contract/rationale + explicit evolution
HISTORICAL / VALIDATION   truthful chronology/evidence
BRANCH WORKSTREAM RECORD  current only for its active unmerged branch
TEMPORARY HANDOFF          branch-local resume aid only
GIT / PR HISTORY          complete recoverable history
```

Do not rewrite historical evidence to pretend it knew later decisions.

Do not leave obsolete current status in a document merely because a newer banner at the top says to ignore it.

Before deleting/replacing/compacting meaningful docs prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
continuing rationale mapped = PASS
important evidence mapped = PASS
references/navigation repaired = PASS
```

Tool/size-driven document splits must be lossless physical partitioning, not silent summaries.

Frozen/read-only split documents may be recomposed into fewer/topic-based files only under the lossless lifecycle policy.

## 12. Temporary handoff lifecycle

Temporary live/session/resume handoffs may exist only on an active unmerged branch when genuinely useful.

Before integration:

```text
temporary handoffs
→ knowledge coverage
→ durable current docs updated
→ important evidence/rationale retained
→ optional ONE branch-history record
→ temporary handoffs deleted
```

Protected `main` must not depend on live/session handoffs for current truth.

See `documentation-and-handoff.md` and `documentation-lifecycle-policy.md`.

## 13. Historical evidence protection

Closed validation/closure evidence remains historical and is not edited merely to align wording with a later state.

Changes to historical artifacts require an explicit evidence-correction reason rather than current-truth cleanup.

Historical exact PostgreSQL 18.4 evidence remains 18.4 even though current runtime/database patch is 18.6.

## 14. Domain/Logical/Physical/Engineering/Frontend reopen rule

Implementation consumes closed models/Foundation decisions.

A concrete contradiction may reopen only the affected decision under an explicit scope.

Do not weaken accepted semantics to fit a convenient database/ORM/API/frontend/tool behavior.

A failed applicable validation may reopen the affected Physical/frontend technology/adapter decision but cannot silently weaken Domain/Logical requirements.

## 15. Implementation evidence truth

Keep distinctions explicit:

```text
selected != installed
installed != configured
configured != directly validated
direct scenario PASS != complete system PASS
closed database != complete product behavior
unmerged branch PASS != protected-main integration
```

Direct evidence remains NOT RUN until real artifacts/harness exist.

Architecture/design closure may be truthful before implementation; it must not be mislabeled as implementation PASS.

## 16. Secrets / production data

Never commit live credentials, keys, tokens, `.env` secrets or raw production dumps.

Lower-environment data is synthetic by default. Production-derived clones require explicit sanitization/minimization/authorization.

Normal PR CI receives no PROD deployment identity.

Anything shipped in Web/mobile client bundles is public client configuration, not a secret.

## 17. Development environment discipline

Backend canonical semantics are Linux.

Primary Windows posture:

- authoritative repository worktrees live in the WSL filesystem;
- Python/uv/backend use WSL/Linux semantics;
- Node/pnpm/Turbo/Vite/Metro/Expo CLI use the authoritative WSL-backed frontend worktree;
- PyCharm/JetBrains may use WSL tooling/interpreters;
- Docker Compose owns stateful LOCAL dependencies;
- multiple worktrees are allowed for genuinely concurrent branches;
- do not maintain divergent duplicate Windows/WSL source clones;
- do not share one virtualenv/node_modules environment across incompatible OS semantics;
- do not switch the wrong worktree onto another active branch.

WSL↔Windows Android/ADB/Metro mechanics remain a directly validated tooling adapter, not a product architecture invariant.

Repository commands remain CLI-reproducible and IDE-neutral.

## 18. No enterprise cosplay

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

## 19. Current continuation instruction

A new chat must first read current protected-main/global truth, then the target branch if the requested workstream is unmerged.

Current frontend continuation:

```text
feature/access-frontend
→ continue existing Access branch/worktree
→ consume branch-local Access record/contracts
→ preserve backend-authoritative boundaries
→ reconcile with current main before final integration
```

Current backend continuation:

```text
CP1–CP6 CLOSED / INTEGRATED
→ do not resume feature/logical-postgresql as active work
→ next post-CP6 product vertical only when explicitly scoped
→ branch from current protected main
```

Current documentation continuation:

```text
current protected-main documentation
→ read current entry points before historical evidence
→ apply documentation-lifecycle-policy.md continuously
→ use bounded docs/chore branch only when a real maintenance subject exists
→ do not create live/session handoffs on main
→ do not compact split references unless lossless knowledge coverage is proven
```

## 20. Persistent operating principles

```text
CURRENT TRUTH FIRST
NEW CHAT != NEW BRANCH
UNMERGED BRANCH TRUTH != PROTECTED-main TRUTH
NO SILENT SCOPE EXPANSION
NO HISTORY REWRITE FOR CONVENIENCE
NO TEMPORARY HANDOFFS ON main
NO KNOWLEDGE LOSS DURING DOC CLEANUP
NO SELECTED-CAPABILITY PASS WITHOUT REAL EVIDENCE
```