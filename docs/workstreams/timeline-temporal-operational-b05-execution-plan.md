# Timeline / Temporal-Operational — B05 Product Organization Execution Plan

- **Status:** PRE-SCOPE FROZEN / FULL B05-A IMPLEMENTED, POSTGRESQL PROOF PENDING; B05 NOT CLOSED
- **Date:** 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Entering candidate DB:** PostgreSQL 18.6 / Alembic `20260920_42` / `116|5|44|90|233|153|331|0|0|0`
- **B05-A source head / expected topology:** `20260920_45` / `119|5|48|90|239|158|344|0|0|0` (direct PostgreSQL proof pending)
- **Previous block:** B04 ✅ CLOSED / PROVEN
- **CI / Actions:** not authorized by this plan

This is the B05 entry gate required by the [current roadmap](timeline-temporal-operational-roadmap.md). It fixes the semantic contract and implementation order. The pre-scope itself introduced no migration/API; B05-A implementation spans `_43`–`_45`, with final direct PostgreSQL proof outstanding. It does not close B05-A or user acceptance.

## 1. Authority and representation

- Product capability: [calendar contexts and grouped views](../product/v1-calendar-contexts-and-grouped-views.md), [core glossary](../product/v1-core-domain-glossary.md).
- Domain classification: [language map](../domain/language-map-part-5.md), [later Life Area disposition](../domain/language-map-part-22.md), [Tag disposition](../domain/language-map-part-2.md).
- Logical classification: [LR-12 product / organizational profile](../logical-model/representation-framework-v1.md); item relations must be typed and bounded.
- Physical constitution: [PostgreSQL mapping](../physical-model/mappings/postgresql-18.4-v1.md) and [CP6-02](../development/backend-cp6-02-postgresql-persistence-constitution.md), especially REF, MAT, REL, IDEM, TX, MIG and access-control rules.
- Detailed workstream obligations: [archived semantic freeze](archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md) B05 and [archived ledger](archive/timeline-temporal-operational-live-ledger-snapshot-2026-09-16-pre-b03.md) ORG-001..015 / B05-T01..06.
- Existing implementation and transport gates: [pre-B04 governance](timeline-temporal-operational-pre-b04-governance-2026-09-18.md).

`Calendar / Life Area` is a durable **product organizational profile (LR-12)**, with an application-local identifier where needed, **not** an LR-01 NativeRef owner, generic Domain `Context`, Goal, Plan, Tag, Place, Schedule or provider calendar. An ID for a profile does not make it a kernel owner. Tags are secondary many-valued product labels; they neither own nor schedule the item. Sharing is independent from organization. Scheduling/conflict truth cannot be changed by hiding/filtering a group.

## 2. B05 contract and transitional invariant

At the completed V1 product boundary every applicable planning item has **one primary Life Area per organizing actor**. A shared canonical item may be placed in different areas by its participants, without duplicating its canonical item or changing shared facts. The current self-only capability must be keyed to the authenticated actor's self Person and must not conflate that Person with the Account. B09 owns activation of actual shared-participant authority; B05 must not invent grants or pretend that actor-local organization already confers access to another participant.

Existing B01/B03 Activity/Event rows predate Life Area. They must be inventoried and transitioned explicitly. Until their assignment is established, read paths may truthfully expose **unassigned legacy state**; this is an implementation transition, **not** an acceptable permanent product state. No arbitrary `Personal`, `Work`, prototype `personale`, inferred Goal or color assignment may be silently manufactured. The migration strategy (user-confirmed default, explicit reconciliation or another proven migration path) must be frozen before enabling a database `NOT NULL`/totality constraint or claiming the product invariant is met. New create paths must make an authorized primary assignment atomic with item creation once assignment is activated; replay must not produce an item in another area. Do not assume existing backend/prototype create paths already satisfy this.

Life Area archive is non-destructive: assignments/history must not vanish; define new-assignment policy and how already-assigned items remain discoverable before implementing archive. Hide/show is an actor-local view preference, **not** retirement, authorization or exclusion from conflict evaluation. Reorder is actor-local presentation order; icon/color are bounded presentation data, never source of semantic type, status, ownership or identity. Retained names/IDs must distinguish two areas even if they share a visible label with a Goal or Tag.

Current frontend inspection shows `contextId` as prototype metadata, a literal `personale` in Timeline hydration and a remote-create boundary that only admits `personale` (`apps/web/src/features/home/ui/timeline/timeline-authoritative-hydration.ts`, `apps/web/src/features/temporal-create/application/temporal-create-b03-runtime.ts`, `temporal-create-b04-runtime.ts`). This is a **migration target**, not existing canonical Life Area support. B05-D must replace/reconcile those paths when B05-B authorizes real primary assignments; it must not simply relabel the prototype string as a database identity.

## 3. Execution slices and proof gates

| Slice | Owned outcome | Mandatory proof before closing |
| --- | --- | --- |
| **B05-A — Life Area catalog** | LR-12 identity, guarded create/list, rename, reorder, archive, hide/show and optional icon/color; self-scoped reads/mutations. | Source implemented, direct PG proof pending; no kernel/native-address pollution; self isolation, concurrency/idempotency, DB/ACL, Dictionary and API/client parity. |
| **B05-B — primary assignment** | Typed actor-local one-primary-area relation for Activity/Event, creation and reassignment; inventory and transition for older rows; later eligible item families only when activated. | Referential integrity and actor authorization at DB/application boundary; atomic create/replay; no duplicate canonical item; archived target policy; existing-row reconciliation; B04 scheduling unchanged. |
| **B05-C — secondary Tags** | Distinct actor-local multi-valued product Tag and item relation; no Goal/Plan or semantic hierarchy inference. | Tag is not primary owner, labels do not identify Domain concepts, independent many-valued association and cross-actor isolation. |
| **B05-D — product integration** | Timeline unified/grouped/focused filtering over canonical assignments, create/edit/read of real catalog; postponed/TBD Event rediscovery and explicit replanning. | Real-stack coverage for scheduled/all-day/coarse/floating/unscheduled items, hidden conflicts, no fake Event time, Activity Planning Tray stays distinct, accessibility without color-only indication. |
| **B05-E — whole-block closure** | Reconcile lifecycle, assignment, Tags, frontend, manual userTest, docs and workstream ledger. | ORG-001..015 and B05-T01..06 explicitly discharged; PostgreSQL catalog/owner/ACL, Dictionary, Alembic, SQLAlchemy, Temporal API inventory, OpenAPI snapshot/client and manual proof all current. |

These letters are execution subdivisions **within documented B05**, not a renumbering of B06 Routine/Recurrence or B07 UI/UX consolidation. B05-D implements only the grouping/organization UI necessary for B05; broad UI cleanup stays B07. B03-E's postponed/TBD Event rediscovery is explicitly transferred into B05-D, without turning an Event into an Activity Planning Tray entry.

## 4. B05-A physical/API decision and lifecycle invariants

`_43` establishes the actor-local LR-12 `life_area` profile with a Person FK, application UUIDv7 and immutable create receipt. `_44` adds positive current revision, complete actor-local order, non-destructive archive, actor-local visibility, optional bounded icon and uppercase RGB color, `updated_at`, and immutable lifecycle/reorder receipts. These profile revisions and receipts are product metadata, not Domain MaterialStateRefs; no `native_address` entry exists for an area. Creation and every mutation lock the self Person to serialize catalog changes. Each single-area mutation compares the expected revision and records acceptance atomically; reorder requires a complete permutation and expected revisions for every row, including archived rows. Replays return their accepted revision/count without altering later state. A no-op single-area mutation returns conflict; an unchanged complete reorder is recorded with zero changes. Mutation operation IDs are actor-local within the lifecycle/reorder receipt namespace, fingerprinted against normalized typed intent and never reused there for another verb or payload. Creation uses its separate immutable create receipt namespace. Names can duplicate; IDs remain distinct. Archive retains the row and history; hidden state and styling never change temporal/scheduling truth. B05-B must define assignment policy for archived targets and discoverability of already-assigned items before binding items. The runtime has only four bounded function EXECUTE privileges and no raw profile table access. A downgrade refuses to erase accepted profile lifecycle state.

For every slice changing persistence, complete **in the same change**: forward-only Alembic → SQLAlchemy → Dictionary objects/scope → real PostgreSQL catalog + owner/ACL → DB README + candidate overlay → direct PostgreSQL tests → map/roadmap/handoff. Do not edit historical migrations or claim a calculated catalog topology as observed. For every new Temporal public operation: explicit stable `temporal_*` operationId → exact inventory test → exported OpenAPI snapshot → generated client (`pnpm api:generate`) → affected API/frontend tests and docs. No manual editing of generated code. A slice cannot be marked CLOSED/PROVEN while a current representation is known stale.

The **pre-scope step** changed no structural artifacts. B05-A spans `_43`–`_45`: three mapped tables, four scoped functions, seven explicit Temporal endpoints, Dictionary/`scope.json`, API inventory and generated client. `_44` passed seven of eight selected PostgreSQL tests and exposed a single generated CHECK name mismatch; `_45` renames that validated CHECK without changing data or topology. Final `_45` direct migrated-PostgreSQL proof remains open: do not confuse source alignment with a real-catalog PASS.

## 5. Exit boundary and explicit exclusions

B05 closes only when a user can create and organize their Activity/Event items in real areas, use separate Tags, inspect unified/grouped/focused views and find postponed Events without inventing times; hidden areas continue to participate in authorized scheduling/conflict truth. Re-run actor-local and access proofs, reconciliation of legacy items and applicable manual userTest. A visual prototype or a green mock-only test is insufficient.

Do not pull in B06 Routine/Recurrence/Occurrence implementation, B07 general UI redesign, B09 multi-actor authorization, B12 solver/conflict engine, or B13 provider synchronization; B05 preserves the necessary boundaries and later integration points.
