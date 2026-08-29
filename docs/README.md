# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-08-27

This directory is the durable documentation surface for DANTE. Current specifications describe the present directly; historical evidence, phase-time continuations and completed workstream records do not silently override current truth.

---

## 1. Authority order

When sources conflict, use this order unless a narrower accepted authority explicitly governs the subject:

```text
1. current protected-main executable truth
   code / migrations / tests / governed generated artifacts

2. accepted semantic + architectural authority
   Product / Domain / Logical / Physical / ADRs / current architecture

3. current durable subsystem reference
   Database System of Record / frontend contracts / engineering contracts

4. current project status + roadmap

5. active unmerged branch-local current truth
   only for that branch's bounded scope

6. retained evidence / branch history / archive

7. Git / PR chronology

8. conversation memory
```

An unmerged branch may contain newer truth for its bounded scope, but it is not protected-main authority until integration.

---

## 2. Current lifecycle

```text
PRODUCT / NORTH STAR                 CURRENT
DOMAIN MODEL                         CLOSED
LOGICAL MODEL                        CLOSED / 57 OF 57 / REMOTE QA PASS
PRE-PHYSICAL COHERENCE               CLOSED / FINAL QA PASS
PHYSICAL TARGET                      CLOSED / ACCEPTED
ENGINEERING FOUNDATION               CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION      CLOSED / INTEGRATED VIA PR #22
FRONTEND MATERIALIZATION             CLOSED / PASS / INTEGRATED VIA PR #28
BACKEND CP1–CP5 SCAFFOLD             CLOSED / DIRECT QA / INTEGRATED VIA PR #24
BACKEND CP6 DATABASE                 CLOSED / DIRECT QA / INTEGRATED VIA PR #42
CURRENT POSTGRESQL                   18.6
CURRENT ALEMBIC HEAD                 20260826_08
CURRENT DATABASE TOPOLOGY            68/5/14/75/95/68/120
ACCESS PRE-BACKEND FRONTEND          CLOSED / ACCEPTED / RELEASE-HARDENED
FULL ACCESS/AUTH PRODUCT VERTICAL    ACTIVE / UNMERGED ON feature/access-auth
ACCESS/AUTH M2                       CLOSED / M2.1–M2.11 ACCEPTED / DOCUMENTED
ACCESS/AUTH M3                       NEXT / NOT STARTED
```

For exact integrated project state, read `PROJECT-STATUS.md`. While `feature/access-auth` remains unmerged, its Access/Auth M2 truth is branch-local and must not be mistaken for protected-main truth.

---

## 3. Mandatory project entry points

Read in this order for general continuation:

1. `../README.md`
2. `README.md` — this index
3. `PROJECT-STATUS.md`
4. `ROADMAP.md`
5. `development/agent-operating-manual.md`
6. `development/operating-rules.md`
7. `development/documentation-and-handoff.md`
8. `development/documentation-lifecycle-policy.md`
9. `development/branching-and-environments.md`
10. `development/repository-engineering-safety.md`
11. current subsystem/workstream sources relevant to the task
12. current branch/ref and relation to protected `main`

Repository truth beats conversation memory.

For the active Access/Auth branch, then read:

- `workstreams/access-auth.md` — operational continuation/state;
- `frontend/access.md` — accepted Access frontend/product UI authority;
- `architecture/access-auth-architecture.md` — identity/authenticator/session/transaction/generated-client architecture;
- `architecture/access-auth-security-contract.md` — security/session/password/email/provider/passkey contract;
- `architecture/access-auth-api-contract.md` — API/naming/RFC9457/OpenAPI/Orval contract;
- `architecture/access-auth-testing-contract.md` — real-boundary test/CI/full-stack proof contract;
- `decisions/ADR-011-access-auth-architecture.md` — architecture rationale/rejected alternatives.

---

## 4. Documentation lifecycle

Current documentation is not an append-only diary.

Temporary branch-operational handoffs may exist while a branch is active, but they must not become the sole durable source of truth and must not silently merge to protected `main` as active handoffs.

Before branch integration:

```text
temporary handoffs
→ knowledge coverage
→ current truth propagated to subject owners
→ rationale/evidence propagated to ADR/reference owners
→ optional one durable branch-history record
→ temporary handoffs removed/consolidated
```

Normative lifecycle source:

- `development/documentation-lifecycle-policy.md`

Archive boundary:

- `archive/README.md`

`docs/archive/` is selective non-authoritative history, not a backup mirror. Git remains complete recoverable chronology.

Frozen/read-only split documents may be recomposed only through lossless knowledge coverage. Do not summarize away requirements, invariants, accepted decisions, rationale, assumptions, counterexamples or material evidence merely to reduce file count.

Long-lived current/reference docs should be partitioned by stable subject rather than conversation/phase chronology. Access/Auth now follows this rule:

```text
architecture        → access-auth-architecture.md
security            → access-auth-security-contract.md
API/client          → access-auth-api-contract.md
testing/proof       → access-auth-testing-contract.md
rationale           → ADR-011
operational state   → workstreams/access-auth.md
```

---

## 5. Product

Entry point:

- `product/README.md`

Key durable product-definition sources include:

- `product/product-identity-and-north-star.md`
- `product/scope.md`
- accepted `product/v1-*.md` specifications where current

Research/simulation material is evidence, not automatic current product truth.

---

## 6. Domain Model

Current entry point:

- `domain/README.md`

Domain Model is CLOSED / semantically complete for current accepted scope.

Current concept-level semantics remain under:

- `domain/concepts/`

Validation methodology/evidence remains under the Domain directory and checkpoints/history.

Important current rule:

```text
domain/README-part-2.md ... domain/README-part-20.md
= HISTORICAL / EVIDENCE ONLY
```

Other Domain split files are classified by explicit purpose; chronology alone does not create higher authority.

Do not infer semantic kernel primitives merely from UI, provider or persistence naming.

---

## 7. Logical Model

Current entry point:

- `logical-model/README.md`

Logical Model is CLOSED / 57 of 57 classified / REMOTE QA PASS.

Primary integrated contract/evidence:

- `logical-model/whole-logical-model-v1.md`
- `logical-model/checkpoints/whole-logical-v1-validation.md`
- `logical-model/checkpoints/whole-logical-v1-remote-qa.md`

Binding hardenings `WL-H01..WL-H12` remain implementation regression contracts unless deliberately superseded.

Detailed split registers/ledgers are retained where they still contain non-duplicated rationale, assumptions, rejected alternatives or test corpus.

---

## 8. Physical Model

Entry point:

- `physical-model/README.md`

Current selected target:

```text
PostgreSQL 18 major family
sole canonical persistence + material-history authority
```

PostgreSQL 18.4 remains historical exact Physical/CP2/CP3 execution evidence. Current repository/database patch is 18.6. Maintenance inside major line 18 does not reopen architecture.

Specialist capabilities remain activation-triggered and direct-validation-specific.

---

## 9. Architecture and decisions

Entry points:

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`
- `architecture/domain-model-logical-readiness.md`
- `architecture/observability-runtime-contract.md`
- `decisions/`

Current branch-local Access/Auth architecture authorities:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `decisions/ADR-011-access-auth-architecture.md`

These own accepted M2.1–M2.11 truth on `feature/access-auth`. M2 is CLOSED. M3 production implementation has not started.

Important persistence ADRs:

- `decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `decisions/ADR-003-primary-database.md` where explicitly historical

Important frontend ADRs:

- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`

Current branch-local platform-observability owners:

- `architecture/observability-runtime-contract.md`
- `development/observability-runbook.md`
- `workstreams/platform-observability.md`
- `../infra/observability/`

They are current only for the pinned `feature/platform-observability` scope
until normal protected-main integration. They do not override Access/Auth or
Home/Today product authority.

---

## 10. Database System of Record

Start here:

- `database/README.md`
- `database/dictionary/README.md`
- `database/dictionary/scope.json`

Current baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
68 tables
5 views
14 routines
75 triggers
95 physical indexes
68 foreign keys
120 CHECK constraints
```

Machine-readable Dictionary:

```text
68 table entries
5 view entries
14 routine entries
87 standalone entries
```

Permanent consistency invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata/mappings
≈ Alembic head
≈ real PostgreSQL schema
```

The human-readable Database Architecture & Reference remains a frozen logical payload split across `database/dante-postgresql-database.md` and continuation parts. Reorganization requires lossless content-equivalence/knowledge-coverage QA.

CP6 final acceptance:

- `development/backend-cp6-05-whole-database-qa.md`

Historical CP6 branch record:

- `archive/branches/2026-08-feature-logical-postgresql.md` — NON-AUTHORITATIVE

Access/Auth has not yet materialized Account/credential/AuthSession persistence. M3 structural Auth changes inherit the same-change migration/mapping/Dictionary/reference/constraint/index/ACL/test/catalog-parity obligations.

---

## 11. Backend

Application documentation:

- `../apps/backend/README.md`

Durable backend contracts include:

- `development/backend-cp1-contract.md`
- `development/backend-cp2-postgres-contract.md`
- `development/backend-cp3-persistence-contract.md`
- `development/backend-cp4-ci-contract.md`
- `development/backend-cp6-01-concrete-persistence-coverage.md`
- `development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- `development/backend-cp6-01-concrete-persistence-coverage-closure.md`
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `development/backend-cp6-02-postgresql-persistence-constitution-closure.md`
- `development/backend-cp6-03-gate-03-closure.md`
- `development/backend-cp6-05-whole-database-qa.md`

CP1–CP6 are closed.

The first complete post-CP6 backend/product vertical is Access/Auth. Its M2 architecture freeze is closed; production Auth code remains not started until a separate M3 write gate.

---

## 12. Frontend

Current frontend documentation:

- `frontend/README.md`
- `frontend/access.md`
- `frontend/design-tokens.md`
- `frontend/localization.md`
- `frontend/terminology.md`
- `frontend/ui-registry.md`
- `frontend/home/`
- `frontend/production-readiness/`

Generic frontend foundation/materialization is closed/integrated.

### Access frontend baseline

The completed pre-backend Access frontend materialization is the accepted Web baseline for the active full-stack Access/Auth product vertical.

Accepted checkpoints:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

Current authority:

- `frontend/access.md`
- current `../apps/web/src/features/access/` implementation/tests

The whole Access/Auth product vertical is not closed. Real backend authentication/session/provider/recovery behavior, generated client integration, full-stack E2E, native Access and release/legal gates remain later macro-phases.

Historical Access-frontend branch narrative:

- `archive/branches/2026-08-feature-access-frontend.md` — NON-AUTHORITATIVE

---

## 13. Access/Auth M2 closure

M2 closed on `feature/access-auth` after subject-oriented documentation consolidation and consistency review preparation.

Accepted M2 subjects:

```text
M2.1  same-origin deployment/browser topology
M2.2  session cookie / CSRF / CORS
M2.3  Account / EmailIdentity / PasswordCredential / AuthSession / Principal
M2.4  multi-session and credential/session lifecycle
M2.5  Argon2id + pepper + HIBP password policy
M2.6  passkey-ready / MFA-compatible boundary
M2.7  email normalization/comparison
M2.8  /api/v1 + RFC 9457 machine contract
M2.9  transaction/concurrency/session-expiry behavior
M2.10 OpenAPI → Orval → first-party Web/Native client boundary
M2.11 real PostgreSQL/API/browser test/full-stack proof contract
```

M2 closure is architecture/documentation readiness only. It does not claim production Auth schema, API, generated client, session runtime or browser signin proof.

M3 is the first executable slice.

---

## 14. Workstream records

Entry point:

- `workstreams/README.md`

On protected `main`, closed workstream files are durable records/evidence, not active chat handoffs.

Active unmerged records remain branch-local until integration.

Current Access/Auth workstream:

- `workstreams/access-auth.md` — operational authority/save-game; durable M2 truth belongs to the four Access/Auth contracts + ADR-011.

Current independent platform workstream:

- `workstreams/platform-observability.md` — branch evidence/state only; durable
  runtime truth belongs to the observability architecture contract, code,
  infrastructure and runbook.

---

## 15. Development governance

Primary sources:

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/documentation-lifecycle-policy.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`
- `development/local-backend-workstation-bootstrap.md`
- `development/testing-and-ci-v0.md`
- `development/toolchain-and-dx-v0.md`
- `development/observability-runbook.md`

Environment vocabulary remains exactly:

```text
LOCAL
DEV
UAT
PROD
```

Environment != Git branch.

---

## 16. Protected-main integration truth

Effective protected-main policy requires normal PR-based integration and repository-enforced current checks.

Current required contexts:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

Current repository rules, not stale prose, are effective enforcement. Do not use squash/rebase/force-push/ruleset weakening to bypass integration policy.

No Access/Auth branch documentation or implementation becomes protected-main authority until normal integration.

M3 may later introduce an Access/Auth CI Gate; it does not exist merely because M2 selected the testing contract.

---

## 17. Evidence and current claims

Executable truth beats documentation claims.

Historical successful runs remain evidence for the exact commit/environment on which they executed. Later patch/runtime/schema claims require evidence appropriate to the later state.

No blanket semantic/direct-pass claim is inferred merely because a technology or test architecture was selected.

M2 documentation records accepted architecture decisions, not proof that production Auth runtime behavior exists.

---

## 18. Brand / UX / prototypes

Brand:

- `brand/README.md`

UX:

- `ux/README.md`

Prototypes live outside production runtime authority. Prototype/UI exploration does not automatically define production architecture, Domain semantics or backend behavior.

---

## 19. Historical material

Use:

- `archive/README.md`

Everything under `archive/` is non-authoritative unless a current source explicitly references it for historical evidence.

Do not copy current files into archive as backup. Git preserves exact old payloads.

---

## 20. Current continuation rule

Before modifying a subsystem:

```text
read current global status
→ read current subsystem authority
→ verify current branch/ref + relation to main
→ inspect relevant executable truth
→ use branch-local workstream only while active
→ update durable subject docs when architecture/behavior changes
→ preserve exact Git/write safety
→ remove temporary handoffs before integration
```

Current truth should be findable without archaeological reconstruction of obsolete overlays.
