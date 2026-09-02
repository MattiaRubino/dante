# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology.

## Current authority

Protected-main project truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Branch-local workstream files may describe newer unmerged implementation/design only inside their own bounded branch. They never silently become protected-main truth.

## Current durable subsystem entry points

### Database

- `../database/README.md` — current DANTE PostgreSQL System of Record.
- `../database/dante-postgresql-database.md` + current continuation parts — human-readable database reference.
- `../database/dictionary/` — machine-readable current database contract.

### Backend

- `backend-scaffold.md` — accepted backend foundation/closure record.

### Frontend

- `frontend-foundation.md`
- `frontend-materialization.md`
- `frontend-materialization-integration.md`
- `../frontend/access.md`

### Engineering / architecture

- `engineering-foundation.md`
- `physical-model.md`
- `pre-physical-coherence.md`

### AI architecture — active branch-local workstream

On `feature/ai-architecture`:

- `ai-architecture.md` — durable branch-local workstream record; current phase AI-04 Productionization Architecture;
- `ai-architecture-live-handoff.md` — **TEMPORARY / MUST NOT MERGE TO protected main**; session/context save-game only;
- `../architecture/dante-ai-03-context-retrieval-memory.md` — closed AI-03 Context/Retrieval/Memory authority;
- `../architecture/dante-ai-03a-full-context-architecture.md` — AI-03A closed / C01..C33;
- `../architecture/dante-ai-03b-retrieval-memory-architecture.md` — AI-03B closed / B01..B35;
- `../architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md` — AI-03C closed / MAT-01..MAT-15.

Current branch-local AI state:

```text
AI-00  COMPLETE
AI-01  COMPLETE
AI-02  COMPLETE / STRUCTURALLY ACCEPTED
AI-02.1 v0.5 CLOSED
AI-03  CLOSED / STRUCTURALLY ACCEPTED
AI-03A CLOSED / C01..C33
AI-03B CLOSED / B01..B35
AI-03C CLOSED / MAT-01..MAT-15
AI-04  ACTIVE / CURRENT — PRODUCTIONIZATION ARCHITECTURE
AI-05  FUTURE — WHOLE-SYSTEM ACCEPTANCE + IMPLEMENTATION BLUEPRINT
```

AI-04 begins from representative DANTE workloads/evals and quality floors before concrete provider/model selection. Provider replaceability is binding:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
DANTE FEATURE/BUSINESS CODE != CONCRETE PROVIDER SDK
PROVIDER REPLACEABLE != LOWEST-COMMON-DENOMINATOR PROVIDER USAGE
```

The temporary live handoff must be deleted/consolidated before integration. Durable architecture decisions must not live only in that file.

### Domain / Logical

Current semantic authority lives in:

- `../domain/README.md`
- `../logical-model/README.md`

## PostgreSQL Recovery

The LOCAL PostgreSQL Recovery workstream is **closed and integrated into protected `main` via PR #47**. It no longer has an active workstream file or execution-plan overlay in current navigation.

Current durable operational authority:

```text
database contract   ../database/README.md
operator runbook    ../operations/postgres-recovery-runbook.md
bootstrap           ../../infra/local/postgres/recovery/bootstrap-local-recovery.sh
whole rehearsal     ../../infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Closed branch history:

- `../archive/branches/2026-08-feature-postgres-recovery.md` — **NON-AUTHORITATIVE**

Current protected-main Recovery truth:

```text
PostgreSQL                              18.6
Alembic                                 20260830_09
topology                                69|5|15|76|97|69|123|0|0|0
CP01–CP07                               LOCAL PASS / CLOSED
exact reusable-runner proof HEAD        789e946a8f096b52f2a440b967120cc3e0a340a3
final Recovery branch HEAD              e46ae3d9d5918b27ebf86f4e291b51312f1e7c4d
integration PR                          #47
protected-main merge commit             bdd2b2370d41423dbaecd00fde86bb2bf2466f2b
remote backup provider                  TBD / NOT ACTIVATED
production/cloud recovery               NOT CLAIMED
```

Permanent rules:

```text
PostgreSQL = sole canonical persistence authority
backup repository != canonical truth
restored bytes != accepted semantic truth
pg_isready != traffic-open proof
pg_is_in_recovery=false + semantic acceptance required
old backup restore != permission to resurrect retired payload
recovery suppression ledger != second canonical database
successful LOCAL proof != remote/cloud production proof
```

The permanent bootstrap/runner is branch-agnostic and fails closed unless the current branch is attached, clean, has a configured upstream and exact `HEAD == upstream` after fetch. The historical `feature/postgres-recovery` branch name is evidence only and is not a current execution requirement.

Detailed CP01–CP07 chronology, proof heads, failure findings, measurements and the disposition of removed active-workstream documents are retained in the single Recovery branch-history record plus Git history.

## Current bounded unmerged workstreams

At the 2026-09-01 reconciliation, current project authority records bounded unmerged work including:

```text
feature/access-auth             active product vertical
feature/home-react              active frontend workstream
feature/platform-observability  active platform workstream
feature/ai-architecture         active AI architecture workstream
```

PostgreSQL Recovery is intentionally absent: it is already integrated in protected `main` via PR #47.

Live Git refs and each active branch's own durable authority outrank this index for later movement.

## Operational continuation rule

Before continuing an active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read the active branch-local workstream record when one legitimately exists;
4. read a temporary live/session handoff only when it genuinely exists on that active branch;
5. prefer repository/code/tests over conversation memory;
6. do not write to protected `main` outside the repository integration path;
7. do not treat selected/unimplemented capability as PASS;
8. keep current docs aligned with materialized repository truth;
9. remove live/session/resume handoffs before integration;
10. after merge, reconcile candidate/branch-local wording to protected-main truth and repair links to intentionally removed overlays.

## Carry-forward engineering rules

```text
SELECTED != IMPLEMENTED
IMPLEMENTED != PROVEN
PROVEN != CLOSED UNTIL THE CHECKPOINT CONTRACT IS SATISFIED
UNMERGED BRANCH TRUTH != protected-main TRUTH
MERGED BRANCH CANDIDATE STATE != CURRENT protected-main STATUS
VERSION-SENSITIVE CLAIMS REQUIRE CURRENT EVIDENCE
CURRENT DOCUMENTATION != DEPRECATED SNAPSHOT
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
```
