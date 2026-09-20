# Timeline / Temporal-Operational — B05 Product Organization Execution Plan

- **Status:** PRE-SCOPE FROZEN / B05-A1 CREATE-LIST IMPLEMENTED, POSTGRESQL PROOF PENDING; B05 NOT CLOSED
- **Date:** 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Entering candidate DB:** PostgreSQL 18.6 / Alembic `20260920_42` / `116|5|44|90|233|153|331|0|0|0`
- **B05-A1 source head / expected topology:** `20260920_43` / `118|5|46|90|237|156|335|0|0|0` (direct PostgreSQL proof pending)
- **Previous block:** B04 ✅ CLOSED / PROVEN
- **CI / Actions:** not authorized by this plan

This is the B05 entry gate required by the [current roadmap](timeline-temporal-operational-roadmap.md). It fixes the semantic contract and implementation order. The pre-scope itself introduced no migration/API; subsequent B05-A1 implementation adds create/list catalog at `_43`, with direct PostgreSQL proof still outstanding. It does not close B05-A or user acceptance.

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
| **B05-A — Life Area catalog** | **A1:** LR-12 identity plus guarded create/list; **A2:** rename, reorder, archive, hide/show and optional icon/color; self-scoped reads/mutations. | A1 implemented, direct PG proof pending; no kernel/native-address pollution; self isolation, concurrency/idempotency, DB/ACL, Dictionary and API/client parity. A2 remains wholly open. |
| **B05-B — primary assignment** | Typed actor-local one-primary-area relation for Activity/Event, creation and reassignment; inventory and transition for older rows; later eligible item families only when activated. | Referential integrity and actor authorization at DB/application boundary; atomic create/replay; no duplicate canonical item; archived target policy; existing-row reconciliation; B04 scheduling unchanged. |
| **B05-C — secondary Tags** | Distinct actor-local multi-valued product Tag and item relation; no Goal/Plan or semantic hierarchy inference. | Tag is not primary owner, labels do not identify Domain concepts, independent many-valued association and cross-actor isolation. |
| **B05-D — product integration** | Timeline unified/grouped/focused filtering over canonical assignments, create/edit/read of real catalog; postponed/TBD Event rediscovery and explicit replanning. | Real-stack coverage for scheduled/all-day/coarse/floating/unscheduled items, hidden conflicts, no fake Event time, Activity Planning Tray stays distinct, accessibility without color-only indication. |
| **B05-E — whole-block closure** | Reconcile lifecycle, assignment, Tags, frontend, manual userTest, docs and workstream ledger. | ORG-001..015 and B05-T01..06 explicitly discharged; PostgreSQL catalog/owner/ACL, Dictionary, Alembic, SQLAlchemy, Temporal API inventory, OpenAPI snapshot/client and manual proof all current. |

These letters are execution subdivisions **within documented B05**, not a renumbering of B06 Routine/Recurrence or B07 UI/UX consolidation. B05-D implements only the grouping/organization UI necessary for B05; broad UI cleanup stays B07. B03-E's postponed/TBD Event rediscovery is explicitly transferred into B05-D, without turning an Event into an Activity Planning Tray entry.

## 4. B05-A1 physical/API decision and outstanding lifecycle freeze

B05-A1 inspected existing `account_application_context`, self Person, Activity/Event ownership and prototype grouping. It introduces `dante.life_area(life_area_ref, self_person_ref, name, created_at)` as an actor-local LR-12 profile with a direct Person FK and independent application UUIDv7 identifier; there is **no** registration in `native_address` or generic `scoped_address`. `dante.life_area_create_operation` records immutable `(self_person_ref, operation_id)` create receipts; a bounded SECURITY DEFINER create routine verifies/serializes/fingerprints/replays creation, and a bounded read routine returns only that self Person's catalog. Runtime has EXECUTE on those two routines and no raw table access. The HTTP create/list operations have explicit `temporal_*` IDs. This is the exact A1 physical choice, subject to direct PostgreSQL catalog/ACL proof, not an assertion that all of B05-A is frozen.

B05-A2 must still freeze consequential change history/CAS per CP6 MAT-01, concurrent reorder, archive/visibility, icon/color, idempotent lifecycle mutations, policy for already-assigned items, owner/ACL and non-destructive rollback before adding those fields/operations. A stable application ID alone does not justify a MaterialStateRef. Do not add placeholders for future lifecycle to A1.

For every slice changing persistence, complete **in the same change**: forward-only Alembic → SQLAlchemy → Dictionary objects/scope → real PostgreSQL catalog + owner/ACL → DB README + candidate overlay → direct PostgreSQL tests → map/roadmap/handoff. Do not edit historical migrations or claim a calculated catalog topology as observed. For every new Temporal public operation: explicit stable `temporal_*` operationId → exact inventory test → exported OpenAPI snapshot → generated client (`pnpm api:generate`) → affected API/frontend tests and docs. No manual editing of generated code. A slice cannot be marked CLOSED/PROVEN while a current representation is known stale.

The **pre-scope step** changed no structural artifacts. The subsequent B05-A1 slice adds `_43`, two mapped tables, two scoped functions and two explicit Temporal endpoints, with Dictionary/`scope.json`, API inventory and generated client updated in the same working change. `_43` direct migrated-PostgreSQL proof remains open: do not confuse source alignment with a real-catalog PASS.

## 5. Exit boundary and explicit exclusions

B05 closes only when a user can create and organize their Activity/Event items in real areas, use separate Tags, inspect unified/grouped/focused views and find postponed Events without inventing times; hidden areas continue to participate in authorized scheduling/conflict truth. Re-run actor-local and access proofs, reconciliation of legacy items and applicable manual userTest. A visual prototype or a green mock-only test is insufficient.

Do not pull in B06 Routine/Recurrence/Occurrence implementation, B07 general UI redesign, B09 multi-actor authorization, B12 solver/conflict engine, or B13 provider synchronization; B05 preserves the necessary boundaries and later integration points.
