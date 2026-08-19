# DANTE Documentation Index

This directory is the durable documentation authority for DANTE.

## Current authority order

When sources conflict, use this order:

1. current `main` code/migrations/tests and current accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current sources inside that workstream;
5. historical evidence/closed branches/Git history;
6. conversation memory.

Conversation instructions may clarify intent but do not silently override durable repository truth.

## Current lifecycle status

```text
Product/North Star                 CURRENT
Domain Model                       CLOSED
Logical Model                      CLOSED
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
Engineering Foundation v0          CLOSED / ACCEPTED
Production backend scaffold        ACTIVE — CP1-01..03 APPROVED / IMPLEMENTATION NOT STARTED
Concrete PostgreSQL schema         NOT STARTED
Direct HG / PSV                    NOT RUN
```

## Mandatory entry points

### Project/current truth

- `../README.md`
- `PROJECT-STATUS.md`
- `ROADMAP.md`

### Active implementation workstream

- `workstreams/backend-scaffold.md` — active production-backend scaffold handoff, checkpoint plan, quality bar and exact resume point
- `development/backend-cp1-contract.md` — frozen CP1-01/02/03 technical contract: dependency/version policy, `pyproject`/quality tooling, complete `DANTE_*` variable registry, FastAPI/settings/health behavior, commands/tests and rationale
- `development/local-backend-workstation-bootstrap.md` — verified clean-machine/WSL2/Docker developer bootstrap

### Development governance

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`

### Engineering Foundation — closed

- `workstreams/engineering-foundation.md` — closure/handoff and inherited implementation boundary
- `development/engineering-foundation-v0.md` — master engineering contract
- `development/repository-layout-v0.md` — monorepo/path ownership
- `development/application-structure-v0.md` — backend modular architecture
- `development/environments-and-promotion-v0.md` — LOCAL/DEV/UAT/PROD
- `development/config-and-secrets-v0.md` — backend configuration/secrets
- `development/toolchain-and-dx-v0.md` — Python/WSL2/PyCharm/Docker/PostgreSQL local developer baseline
- `development/testing-and-ci-v0.md` — backend testing/CI/security/supply-chain baseline

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

### Domain / Logical / Physical

Use the model indexes and their linked accepted sources. For any Physical-consuming implementation, at minimum reread:

- PM-11 accepted target;
- PM-12 selected stack/operational posture;
- post-selection validation register.

Historical evidence remains historical. Do not rewrite it to pretend it knew later decisions.

## Engineering Foundation final decisions

The closed backend/repository baseline is:

```text
one product monorepo
apps/backend + apps/web + apps/mobile
backend capability-first modular monolith
Python 3.14.x / initial 3.14.7
uv / Ruff / mypy strict / pytest / Hypothesis
Windows 11 host supported via WSL2/Linux backend semantics
PyCharm WSL interpreter supported; repo remains IDE-neutral
Docker Compose for LOCAL stateful infrastructure
PostgreSQL 18.4 with full selected extension envelope enabled from first LOCAL DB
SQLAlchemy 2.0 stable line + psycopg 3 + Alembic
risk-governed migrations / logical copy / recovery separation
typed pydantic-settings configuration
workload identity + secret manager + OIDC target
risk-layered real-PostgreSQL testing
GitHub Actions / protected main / supply-chain hardening
```

Frontend internal tooling/testing/release implementation is explicitly deferred to the dedicated frontend workstream.

Cloud/compute provider and IaC engine are explicitly deferred until first remote infrastructure.

## Repository identity

Production implementation continues in the existing repository. Creating a new repo is not the plan.

Repository identity governance is complete:

```text
historical repository   MattiaRubino/lifeos
current repository      MattiaRubino/dante
rename                   COMPLETE
```

Historical/closed documents may still record the pre-rename repository decision as historical truth. Current-truth documents and new implementation work use `MattiaRubino/dante`.

## Exact next handoff

```text
1. Read `workstreams/backend-scaffold.md` and `development/backend-cp1-contract.md` after the normal mandatory bootstrap.
2. Verify `feature/backend-scaffold`, current HEAD and clean local/remote state.
3. CP1-01 dependency/version policy is approved.
4. CP1-02 pyproject/Ruff/mypy/pytest/coverage policy is approved.
5. CP1-03 FastAPI/settings/environment-variable/health policy is approved.
6. CP1 implementation files and `uv.lock` do not exist yet.
7. Re-check upstream versions only if the version-sensitive evidence has materially changed since 2026-08-19.
8. Open a fresh exact CP1 implementation Git write gate.
9. Materialize and QA CP1 only after approval.
10. Proceed through CP2 PostgreSQL → CP3 persistence/migrations → CP4 CI → CP5 closure.
11. Only after scaffold QA begin concrete Logical → PostgreSQL implementation.
```

No production application code or concrete schema is authorized merely by Engineering Foundation closure or by the scaffold planning/CP1 design documents; every implementation write still requires its own exact scope.
