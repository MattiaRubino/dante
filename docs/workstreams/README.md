# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-03
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

### AI architecture — closed branch-local design workstream

On `feature/ai-architecture`:

- `ai-architecture.md` — closed durable architecture workstream record;
- `../architecture/dante-ai-implementation-baseline-final.md` — **CURRENT / ACCEPTED implementation-facing authority**;
- `../architecture/dante-ai-post05-final-mega-acceptance.md` — final independent post-AI05 acceptance evidence;
- `../architecture/dante-ai-05-whole-system-destructive-acceptance.md` — AI-05 whole-system structural closure;
- `../architecture/dante-ai-05b-concrete-implementation-blueprint-acceptance.md` — AI-05B closure evidence;
- `../architecture/dante-ai-05a-whole-system-build-boundary-acceptance.md` — AI-05A closure authority;
- `../architecture/dante-ai-pre05-cross-phase-hardening.md` — PRE-AI05 closure;
- AI-04 / AI-03 / AI-02 documents remain upstream architecture authority/evidence.

The temporary `ai-architecture-live-handoff.md` has been deleted after durable knowledge coverage and must not be recreated merely for chronology.

Architecture status:

```text
AI-00  COMPLETE
AI-01  COMPLETE
AI-02  CLOSED / STRUCTURALLY ACCEPTED
AI-03  CLOSED / STRUCTURALLY ACCEPTED
AI-04  CLOSED / STRUCTURALLY ACCEPTED
PRE05  CLOSED / STRUCTURALLY ACCEPTED
AI-05  CLOSED / STRUCTURALLY ACCEPTED
POST05 PRE-IMPLEMENTATION MEGA TEST
       CLOSED / PASS
       POST05-H01..H25
       MKT-001..MKT-100 PASS
       C01..C20 PASS
       reverse authority PASS
       Product/simulation replay PASS

CURRENT IMPLEMENTATION AUTHORITY
       ../architecture/dante-ai-implementation-baseline-final.md
```

### AI implementation — active branch-local workstream

On `feature/ai-implementation`:

- `ai-implementation.md` — current implementation state, validation evidence and executable gate;
- `../ROADMAP.md` — current cross-workstream execution overlay;
- `../PROJECT-STATUS.md` — project-level current state.

Current implementation state:

```text
I0  CLOSED / PASS
I1  CLOSED / PASS
I2  CLOSED / PASS
I3/C3 real deterministic Search/structured family
    DEFERRED / WAITING OWNER DATA + SEAMS

CURRENT EXECUTABLE
C6 Policy / Resource / Verification / Publication /
   Effect / Egress / Evidence contracts
→ C7 route-config identity / loader / digest snapshot
→ I4 provider candidate admission
→ I5 adapter qualification

MANDATORY CONVERGENCE
I3/C3 must re-enter when owner seams are ready and converge
before I6 whenever the accepted first vertical requires the real
Search/structured source path.
```

The baseline I0-I10 identifiers remain architectural stage labels. The execution overlay may defer trigger-gated I3 without renumbering or falsely closing it.

Provider/model/SDK selection remains open and evidence-driven. No AI runtime/provider/database activation is implied by architecture closure or I0-I2 completion.

Binding implementation separations include:

```text
GLOBAL SEARCH != INTELLIGENCE
SEMANTIC QUERY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
PROVIDER SDK != APPLICATION CONTRACT
MODEL OUTPUT != PUBLISHABLE OUTPUT
Context != Retrieval != Memory
DEFAULT NONCANONICAL AI PERSISTENCE = NO
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
```

### Domain / Logical

Current semantic authority lives in:

- `../domain/README.md`
- `../logical-model/README.md`

## PostgreSQL Recovery

The LOCAL PostgreSQL Recovery workstream is **closed and integrated into protected `main` via PR #47**.

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

## Current bounded unmerged workstreams

Current project authority includes bounded unmerged work such as:

```text
feature/access-auth             active product vertical
feature/home-react              active frontend workstream
feature/platform-observability  active platform workstream
feature/ai-implementation       active AI implementation / I0-I2 closed / C6 next
feature/ai-architecture         architecture design closed / retained authority/evidence
```

Live Git refs and each branch's durable authority outrank this index for later movement.

## Operational continuation rule

Before continuing a workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read the branch-local durable workstream record where one exists;
4. prefer repository/code/tests over conversation memory;
5. do not write to protected `main` outside the integration path;
6. do not treat selected/unimplemented capability as PASS;
7. keep current docs aligned with materialized repository truth;
8. temporary live/session handoffs must not enter protected `main`.

## Carry-forward engineering rules

```text
SELECTED != IMPLEMENTED
IMPLEMENTED != PROVEN
PROVEN != CLOSED UNTIL THE CHECKPOINT CONTRACT IS SATISFIED
UNMERGED BRANCH TRUTH != protected-main TRUTH
VERSION-SENSITIVE CLAIMS REQUIRE CURRENT EVIDENCE
CURRENT DOCUMENTATION != DEPRECATED SNAPSHOT
TEMPORARY HANDOFF != DURABLE main DOCUMENTATION
```
