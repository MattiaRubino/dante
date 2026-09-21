# Timeline / Temporal-Operational — B05 Product Organization Execution Plan

- **Status:** B05 ✅ CLOSED / PROVEN
- **Date:** 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Entering candidate DB:** PostgreSQL 18.6 / Alembic `20260920_42` / `116|5|44|90|233|153|331|0|0|0`
- **B05-A proved head / topology:** `20260920_45` / `119|5|48|90|239|158|344|0|0|0`
- **B05-B proved head / topology:** `20260920_46` / `123|5|54|90|245|170|354|0|0|0`
- **B05-C proved head / expected topology:** `20260920_47` / `129|5|60|90|254|185|366|0|0|0` (26 selected direct PostgreSQL tests passed)
- **B05-D proved head / topology:** `20260921_48` / `129|5|62|90|254|185|366|0|0|0` (24 PostgreSQL + 41 selected web tests passed; see [closure](timeline-temporal-operational-b05-d-closure-2026-09-21.md)).
- **Previous block:** B04 ✅ CLOSED / PROVEN
- **CI / Actions:** not authorized by this plan

This is the B05 entry gate required by the [current roadmap](timeline-temporal-operational-roadmap.md). It fixes the semantic contract and implementation order. B05-A and B05-B are closed with direct PostgreSQL evidence in their [catalog](timeline-temporal-operational-b05-a-closure-2026-09-20.md) and [assignment](timeline-temporal-operational-b05-b-closure-2026-09-20.md) closure records. B05-C is closed with direct PostgreSQL evidence in its [Tag closure record](timeline-temporal-operational-b05-c-closure-2026-09-20.md). B05-D is closed with the user-run evidence recorded in its [closure record](timeline-temporal-operational-b05-d-closure-2026-09-21.md). The whole block is closed by the [B05-E closure record](timeline-temporal-operational-b05-e-closure-2026-09-21.md).

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
| **B05-A — Life Area catalog** | LR-12 identity, guarded create/list, rename, reorder, archive, hide/show and optional icon/color; self-scoped reads/mutations. | ✅ CLOSED / PROVEN at `_45`; no kernel/native-address pollution; self isolation, concurrency/idempotency, DB/ACL, Dictionary and API/client parity. |
| **B05-B — primary assignment** | ✅ CLOSED / PROVEN at `_46`: typed actor-local one-primary-area relation for Activity/Event, creation and reassignment; explicit legacy inventory. | 16 selected direct PostgreSQL tests passed at the proved branch head. |
| **B05-C — secondary Tags** | ✅ CLOSED / PROVEN at `_47`: distinct actor-local multi-valued product Tag and typed item relations. | 26 selected direct PostgreSQL tests passed at the proved branch head. |
| **B05-D — product integration** | Timeline unified/grouped/focused filtering over canonical assignments, create/edit/read of real catalog; postponed/TBD Event rediscovery and explicit replanning. | Real-stack coverage for scheduled/all-day/coarse/floating/unscheduled items, hidden conflicts, no fake Event time, Activity Planning Tray stays distinct, accessibility without color-only indication. |
| **B05-E — whole-block closure** | Reconcile lifecycle, assignment, Tags, frontend, manual userTest, docs and workstream ledger. | ORG-001..015 and B05-T01..06 explicitly discharged; PostgreSQL catalog/owner/ACL, Dictionary, Alembic, SQLAlchemy, Temporal API inventory, OpenAPI snapshot/client and manual proof all current. |

These letters are execution subdivisions **within documented B05**, not a renumbering of B06 Routine/Recurrence or B07 UI/UX consolidation. B05-D implements only the grouping/organization UI necessary for B05; broad UI cleanup stays B07. B03-E's postponed/TBD Event rediscovery is explicitly transferred into B05-D, without turning an Event into an Activity Planning Tray entry.

## 4. B05-A physical/API decision and lifecycle invariants

`_43` establishes the actor-local LR-12 `life_area` profile with a Person FK, application UUIDv7 and immutable create receipt. `_44` adds positive current revision, complete actor-local order, non-destructive archive, actor-local visibility, optional bounded icon and uppercase RGB color, `updated_at`, and immutable lifecycle/reorder receipts. These profile revisions and receipts are product metadata, not Domain MaterialStateRefs; no `native_address` entry exists for an area. Creation and every mutation lock the self Person to serialize catalog changes. Each single-area mutation compares the expected revision and records acceptance atomically; reorder requires a complete permutation and expected revisions for every row, including archived rows. Replays return their accepted revision/count without altering later state. A no-op single-area mutation returns conflict; an unchanged complete reorder is recorded with zero changes. Mutation operation IDs are actor-local within the lifecycle/reorder receipt namespace, fingerprinted against normalized typed intent and never reused there for another verb or payload. Creation uses its separate immutable create receipt namespace. Names can duplicate; IDs remain distinct. Archive retains the row and history; hidden state and styling never change temporal/scheduling truth. B05-B must define assignment policy for archived targets and discoverability of already-assigned items before binding items. The runtime has only four bounded function EXECUTE privileges and no raw profile table access. A downgrade refuses to erase accepted profile lifecycle state.

For every slice changing persistence, complete **in the same change**: forward-only Alembic → SQLAlchemy → Dictionary objects/scope → real PostgreSQL catalog + owner/ACL → DB README + candidate overlay → direct PostgreSQL tests → map/roadmap/handoff. Do not edit historical migrations or claim a calculated catalog topology as observed. For every new Temporal public operation: explicit stable `temporal_*` operationId → exact inventory test → exported OpenAPI snapshot → generated client (`pnpm api:generate`) → affected API/frontend tests and docs. No manual editing of generated code. A slice cannot be marked CLOSED/PROVEN while a current representation is known stale.

B05-A spans `_43`–`_45`: three mapped tables, four scoped functions, seven explicit Temporal endpoints, Dictionary/`scope.json`, API inventory and generated client. `_44` passed seven of eight selected PostgreSQL tests and exposed a single generated CHECK name mismatch; `_45` renamed that validated CHECK without changing data or topology. The final `_45` direct catalog proof passed; evidence is recorded in the B05-A closure record.

## 5. B05-B typed primary assignment decision

`_46` adds exactly two actor-local current typed relations (`activity_life_area_assignment`, `event_life_area_assignment`) and two immutable typed acceptance-receipt tables. Their keys are `(self_person_ref, activity_ref)` or `(self_person_ref, event_ref)`, not a polymorphic `item_type/item_id` relation. Three real foreign keys per table bind the canonical typed item, Person and LR-12 Life Area. DB security-definer functions check existing self-owned item descriptors, application context, current non-archived self area and optimistic assignment revision under a serialized Person lock. The initial assignment expects revision 0; reassignment advances exactly once. The idempotent receipt is checked before current archive/revision state so a historic accepted command remains replayable. Archived areas refuse new assignments but keep their current associations and receipts; hidden areas do not affect assignments or any B04 Schedule truth.

New Activity/Event creation uses atomic wrappers around existing canonical create/Agenda capabilities and initial typed assignment with a fingerprint including the Life Area; scheduled and constrained authoring compose those wrappers in the same transaction. Direct runtime EXECUTE on all three old bare Activity/Event create helpers is revoked. Old rows remain genuinely unassigned, discoverable via `list_self_unassigned_life_area_items` and assignable explicitly; no `NOT NULL`, synthetic default or bulk rewrite occurs until reconciliation is complete. Public create requests require `life_area_ref`; reads expose nullable area/revision for historical rows, with separate actor-local assignment and inventory endpoints. B05-D is responsible for replacing the prototype `personale` frontend paths with these canonical operations; this B05-B step does not pretend the frontend migration already happened.

The `_46` topology `123|5|54|90|245|170|354|0|0|0` was asserted by the user's direct PostgreSQL catalog test; all 16 selected tests passed. B09, not B05-B, grants authority to any additional participant; no shared-item data or access is invented here.

## 6. B05-C secondary Tag decision

Tag is an actor-local LR-12 product label, not a Domain owner, primary Life Area,
Goal, Plan, Context, Place, Schedule, provider calendar, semantic type or hierarchy.
The catalog uses an application UUIDv7, a bounded display name and non-destructive
archive; duplicate visible names are legal. Renames/archive use a revision and
immutable actor-local operation receipts. Attach/detach uses two distinct typed
Activity/Event relations and typed immutable operation receipts: zero to many tags
per item, zero to many items per tag, and exactly one current edge per actor/item/tag.
No single polymorphic item-type/id escape and no inferred canonical hierarchy.
An archived Tag cannot be newly attached; existing associations remain visible
and may be detached. Accepted operation replay remains stable after later changes.
Every write checks self item ownership and self Tag ownership behind bounded
security-definer functions. Runtime has no raw Tag/edge/receipt table access.
Tag CRUD/association read APIs, exact inventory, generated OpenAPI/client,
Dictionary/mappings, current catalog and direct PostgreSQL tests are same-change
obligations. B05-D owns real frontend Tag editing and grouped presentation.

## 7. Exit boundary and explicit exclusions

## 6A. B05-D implemented candidate — strict integration boundary

`_48` adds one read-only, actor-scoped PostgreSQL capability for Event Schedules whose
current placement was explicitly withdrawn. It returns retained EventRef/ScheduleRef,
the actor-local Life Area basis and the exact unschedule receipt; it returns neither a
made-up interval nor a synthetic time. Replan is a single application transaction that
first performs the governed Undo of that exact receipt and then a normal governed
Schedule revision. It therefore preserves identity, monotonic Schedule history,
idempotent operation receipts and the existing B04 hard-admissibility path.

The production Timeline obtains its groups from actor-local Life Areas and maps canonical
Activity/Event reads through the typed assignment relation. Legacy items remain in an
explicit unassigned group. Hide is presentation-only; it cannot delete an assignment,
alter Schedule truth or make an item unavailable to the postponed Event panel. Creation
is disabled until an active canonical Life Area exists; the prototype `personale` value
is no longer a production fallback. Tags remain secondary associations. Postponed Events
have their own Event-only panel and can be replanned as timed, all-day/date-span or
coarse-period intent; they never enter the Activity Planning Tray.

B05 closes only when a user can create and organize their Activity/Event items in real areas, use separate Tags, inspect unified/grouped/focused views and find postponed Events without inventing times; hidden areas continue to participate in authorized scheduling/conflict truth. Re-run actor-local and access proofs, reconciliation of legacy items and applicable manual userTest. A visual prototype or a green mock-only test is insufficient.

Do not pull in B06 Routine/Recurrence/Occurrence implementation, B07 general UI redesign, B09 multi-actor authorization, B12 solver/conflict engine, or B13 provider synchronization; B05 preserves the necessary boundaries and later integration points.
