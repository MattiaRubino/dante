# Pre-Physical Architecture Baseline

- Status: **CURRENT — Phase 4 bridge baseline**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Backend: **NOT STARTED / DEFERRED**

## Purpose

Current bridge between the closed Domain + Logical Models and later requirements, benchmark, Physical and backend work. It does not replace Domain, Logical, ADRs, `system-overview.md` or `technical-decisions.md`; it states the downstream assumptions, prohibitions, mandatory hardenings, open owners and authorization boundary.

## Authority

Read current truth through Product/North Star, the complete Domain Atlas + Language Map logical documents, the closed Whole Logical Model + full decision/register chain + remote closure, current ADR status, current architecture specs, this baseline, then the active workstream for open obligations.

A physical `*-part-N` chain is one logical document. Never infer current state from only the first or last physical part.

## Decided != authorized

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
```

Current stage:

```text
Product/North Star        CURRENT
Domain Atlas              CLOSED
Logical Model             CLOSED
Pre-Physical Coherence    IN PROGRESS
Physical Model            NOT STARTED / NOT AUTHORIZED
Backend Foundation        NOT STARTED / DEFERRED
```

## Current direction

- Web: Next.js + React + TypeScript.
- Mobile: Expo + React Native + TypeScript.
- Backend direction: Python + FastAPI + Pydantic.
- Modular monolith first.
- Domain/application logic stays independent from HTTP/framework handling.
- Clients use governed backend contracts, not direct canonical persistence.
- Object/file storage stays behind a provider abstraction.
- AI stays behind replaceable/provider-neutral boundaries and a bounded Context Builder.
- Provider state remains distinct from canonical LifeOS state.
- Specialized infrastructure requires demonstrated measured or structural benefit.
- SQLAlchemy/Alembic remain conditional on accepted Physical design.

## Semantic guardrails

Do not manufacture universal owners or collapse accepted distinctions for implementation convenience.

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Actor / Subject / Resource = contextual roles/capabilities, not universal native owners
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Responsibility != Participation != Coordination Stewardship
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical state
derived projection != canonical truth
AI/solver inference != accepted canonical effect
```

Product/runtime labels such as Project, Program, Workspace, Task, Reminder, Agent, Workflow or Notification do not create new universal Domain roots by naming alone.

Hard rejects for the canonical kernel include universal Entity/Thing, universal generic Relationship/edge, generic EAV/property-bag ontology, generic unresolved-AI relation/property fallback, provider schema/IDs as ontology/identity, and product/UI vocabulary as ontology authority.

Storage coincidence != semantic equivalence. Addressability != Domain identity.

## Representation and state separation

The Logical Model keeps `LR-01..LR-13` distinct and uses discriminated `NativeRef`, `ScopedRecordRef`, `MaterialStateRef`, `ExternalRef`; do not collapse them into one identifier model.

Preserve separation among:

```text
canonical state
material history / lineage / correction
derived or effective projection
provider / external state
unresolved / candidate interpretation
security / AuthZ runtime state
```

Phase 6 must additionally distinguish retrieved context, live external context and transient LLM working context.

## Mandatory WL-H01..WL-H12

- **H01** Agreement terms bind justified material owner/facet/state; no universal Terms root.
- **H02** consequential operations use a governed operation/effect contract; route/UI/AuthZ strings are not the canonical effect.
- **H03** projection/disclosure surfaces are bounded by source, derivation/version, purpose and exposure/disclosure boundaries.
- **H04** absence/unknown != false.
- **H05** consequential writes require expected-state semantics.
- **H06** idempotency != semantic identity; conflicting reuse rejects.
- **H07** multi-owner mutation is atomic where required or explicitly staged/partial with reconciliation/compensation.
- **H08** canonical LifeOS state != provider sync state.
- **H09** consequential derived-state use requires freshness revalidation or bound material basis/snapshot.
- **H10** retention/redaction/tombstone handling preserves historical integrity; native identity is not reused.
- **H11** consequential AuthZ provenance reconstructs Actor, represented party, Principal/security context, Authority/Consent/Visibility basis, policy/model version and effect.
- **H12** non-interference/inference leakage includes existence, counts, ranking, errors, timing, free-busy, candidates, explanations and aggregates.

## Runtime/technical != Domain

Account, Principal, Credential, AuthZ decision, Agent, Tool, Workflow, Automation runtime, Notification delivery, Job, queue/outbox, cache/index, API DTO/route and protocol adapter are technical/product concepts unless separately revalidated. Authentication/security session concepts must not be conflated with Domain `Session`.

## AI and integrations

Already decided: provider-neutral AI boundaries; AI output remains proposal/candidate unless accepted through governed effects; deterministic constraints stay deterministic where appropriate; retrieved/provider context does not become canonical truth merely because AI consumed it.

Integration modes remain distinct:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

MCP/A2A/future protocols are adapters, not ontology.

## Benchmark posture

No Physical technology is selected:

```text
PostgreSQL hybrid         preferred baseline — not selected
TypeDB                     mandatory challenger
Neo4j/property graph       serious secondary/read-projection candidate
event/document mechanisms bounded candidates
pgvector                   bounded semantic-retrieval candidate
generic EAV/generic edge/universal meta-model HARD REJECT
```

No durable-workflow winner is selected. Phase 7 compares at least PostgreSQL+worker+transactional outbox, Temporal, Restate and DBOS.

## Open owners before Physical authorization

- **Phase 5:** AuthN/AuthZ; security/privacy/retention/recovery; transaction/consistency/outbox/side effects; non-functional/multi-device/recovery requirements.
- **Phase 6:** AI/context/runtime/integration boundaries.
- **Phase 7:** durable workflow/async benchmark.
- **Phase 8:** governed API/command/effect contract before concrete routes/DTOs.
- **Phase 9:** search/observability/calendar/solver pressure.
- **Phase 10:** Physical benchmark specification/register.
- **Phase 11:** repository engineering safety.
- **Phase 12:** clean-room coherence QA and closure.

## Explicitly unauthorized now

No Physical schema/tables/keys/indexes/constraints, concrete PostgreSQL/TypeDB/Neo4j design, SQL/migrations, concrete API routes/DTOs, AuthN/AuthZ engine/provider implementation, workflow/automation/notification engine, provider adapters, production backend code or `feature/backend-foundation`. Domain/Logical changes require a separate explicit reopen gate.

## Backend consumption contract

Backend Foundation must consume this baseline plus complete current Domain/Logical authorities and later accepted Physical/runtime/security/API contracts. Implementation convenience, product labels and stale evidence cannot redefine semantics.

## Documentation/evidence rule

Current specs = current truth. ADRs = rationale + explicit supersession/qualification. Historical checkpoints = truthful chronology. Git = recoverable history.

This baseline closes only Phase 4. It does not close Pre-Physical Coherence or authorize Physical work. After Phase 4 QA the next current work is **Phase 5 requirements**.
