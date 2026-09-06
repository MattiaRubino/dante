# Authenticated DANTE Application Context

- **Status:** CURRENT / BRANCH-LOCAL PV-02 IMPLEMENTED
- **Branch:** `feature/pre-vertical-foundation`
- **Introduced by:** `20260906_18`
- **Scope:** authenticated Account → DANTE-facing self context and user/default timezone policy

## 1. Purpose

PV-02 closes one deliberately narrow seam between Access/Auth and future product operations. An admitted `Principal` identifies an authenticated `Account`, but neither object is a DANTE Domain `Person` and neither is a persisted Domain `Actor`.

The permanent boundary remains:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
```

Future application operations therefore consume an explicit DANTE context rather than treating `account_ref` as a generic domain owner.

## 2. Resolution contract

The request-level flow is:

```text
AuthSession
→ admitted Principal
→ Account
→ AccountApplicationContext
→ self Person NativeRef
→ user/default timezone policy
→ effective request timezone
```

`AccountApplicationContext` is a bounded application-context mapping. It is not a universal User/Profile model, workspace, world, tenant, Ownership relation or Visibility relation.

The initial `self_person_ref` is created lazily on the first authenticated DANTE-context resolution. No email address, provider identity, display name or other Auth/profile field is used to infer or reconcile an existing Person.

## 3. Account and Person remain distinct

The persistence row contains:

```text
account_ref       -> dante.account
self_person_ref   -> dante.person
timezone_mode     -> follow_device | fixed
fixed_zone_id     -> named IANA timezone only when mode=fixed
```

The table has one row per Account because `account_ref` is its primary key. `self_person_ref` is intentionally not globally unique: PV-02 does not freeze a universal Account↔Person cardinality rule beyond the one self reference owned by this application-context row.

The mapping does not make Account a 16th native Domain owner. `Person` remains one of the existing 15 NativeRef owners.

`self_person_ref` is a homogeneous reference whose semantic target is specifically `Person`, so the canonical integrity mechanism is a direct FK to `dante.person`. `dante.native_address` remains the bounded address/control projection used when a consumer accepts genuinely heterogeneous NativeRef families. The bootstrap capability also creates the Person's `native_address(owner_family='person')` atomically, but the application-context FK does not reinterpret that projection as a semantic parent required by every homogeneous Person reference.

## 4. Bounded Person bootstrap capability

Ordinary runtime `INSERT` on `dante.person` remains denied. PV-02 does not reopen generic Person creation.

The only new bootstrap path is:

```text
dante.ensure_account_application_context(account_ref, candidate_self_person_ref)
```

The function is a narrow `SECURITY DEFINER` capability owned by `dante_owner`. `dante_runtime` receives only `EXECUTE`; PUBLIC and `dante_migrator` do not.

The capability:

1. locks the requested Account row;
2. requires the Account to exist and be active;
3. returns the existing context when already established;
4. otherwise requires an application-issued UUIDv7 candidate;
5. creates exactly one `Person` plus its `native_address(owner_family='person')`;
6. creates the Account application context with `follow_device` timezone policy;
7. returns the committed context.

This is a concrete creation profile for one self Person. It is not permission for arbitrary runtime Person shells.

## 5. Concurrent first use

First-use creation is serialized on the Account row, not by UUID ordering or optimistic guessing.

If requests A and B race with different candidate Person refs:

```text
A locks Account
A creates Person P1 + address + context
A commits
B acquires Account lock
B sees existing context
B returns P1
P2 is never inserted
```

The Account row is therefore the deterministic concurrency arbiter for this one capability.

## 6. Timezone policy

PV-02 reuses the PV-01 time contract. It does not introduce a second timezone framework.

Two user/default modes exist:

```text
follow_device
fixed(named IANA zone)
```

For Web requests, the browser/device supplies its current named timezone through:

```text
X-Dante-Time-Zone: Europe/Rome
```

The Web transport obtains that value from the existing `@dante/time` device-timezone primitive. Numeric UTC offsets are not accepted as named timezone identity.

`follow_device` resolves the effective request timezone from the current device header. `fixed` resolves from the stored named IANA zone and does not change merely because the device moved.

A malformed/missing device timezone under `follow_device` is a request validation error. An impossible persisted mode/fixed-zone policy is instead an internal context-integrity failure: the server must not blame the client for corrupted or no-longer-valid stored state.

This policy is a user/application default only. It never overrides the temporal semantics owned by a concrete DANTE object. In particular:

```text
Schedule/Event/Routine named-zone semantics
!= user default timezone
!= current device timezone
```

A future object carrying `America/New_York` remains semantically New York even when the user's effective display/default zone is `Europe/Rome`.

## 7. Application consumption

Backend product operations should depend on the typed request-scoped `DanteContext`, which carries:

- the admitted Auth `Principal`;
- the self `Person` NativeRef;
- the persisted user/default timezone policy;
- the effective timezone resolved for the current request.

They should not repeatedly rediscover Account→Person linkage or parse transport headers independently.

This dependency is foundation only. PV-02 does not add product endpoints.

## 8. Persistence delta

Branch-local topology after `20260906_18`:

```text
PostgreSQL          18.6
Alembic head        20260906_18

tables              89
views                 5
routines             18
triggers             77
indexes             173
foreign keys          91
CHECK constraints    272

enum/domain            0
sequences              0
materialized views      0
partitioned tables      0
RLS policies            0
```

The protected-main `20260904_17` contract remains protected-main truth until normal branch integration completes.

### 8.1 Truthful downgrade behavior

`account_ref → self_person_ref` is semantic linkage, not disposable migration scaffolding. A downgrade that dropped `account_application_context` after real rows existed would sever that linkage while leaving the minted Person identities behind; a later upgrade could then create a different self Person for the same Account.

Therefore `20260906_18` follows the persistence constitution's truthful-reversibility rule:

```text
empty account_application_context
→ downgrade may remove PV-02 schema

non-empty account_application_context
→ downgrade REFUSED
→ bindings and Person identities remain intact
→ use a separately reviewed forward migration for any real semantic transition
```

The ordinary fresh-schema `head → base → head` proof remains valid because no semantic rows exist in that test. A populated database is fail-closed rather than silently orphaned.

## 9. Acceptance boundary

PV-02 implementation is complete on `feature/pre-vertical-foundation`. Its branch-local contract, changed-path scope and semantic boundaries have been reconciled.

This status does **not** claim protected-main acceptance. Whole-branch executable acceptance is deliberately centralized in PV-04, including:

```text
backend quality / unit-integration validation
real PostgreSQL acceptance
frontend quality / typecheck / tests / build
recovery rehearsal where required by the final database head
final exact changed-path QA
reconciliation with then-current protected main
required PR checks
post-merge readback
```

Until PV-04 completes, `20260906_18` remains branch-local implementation truth rather than protected-main truth.

## 10. Explicit non-goals

PV-02 does not introduce:

- a generic `user_id` ownership model;
- a universal User/Profile/preferences JSON document;
- workspace/world/tenant persistence;
- generic Ownership or Visibility materialization;
- Settings API or UI;
- Person merge/reconciliation;
- email/provider/name-based Person inference;
- Timeline or other product APIs;
- Activity/Event/Routine CRUD;
- Session lifecycle product endpoints;
- AI/Search product integration;
- generic CAS, versioning or idempotency frameworks;
- Access/Auth lifecycle redesign.

Those concerns require their own concrete semantic owner and operation before persistence is added.
