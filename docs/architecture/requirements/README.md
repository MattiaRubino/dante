# Pre-Physical Requirements

- Status: **CURRENT — Phase 5 requirement package index**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Backend production implementation: **NOT STARTED / DEFERRED**

## Purpose

This directory contains the current requirements that later Physical, runtime, API and backend work must satisfy before implementation mechanisms are selected.

These documents answer:

```text
WHAT MUST BE TRUE
```

They deliberately do **not** answer:

```text
WHICH DATABASE / POLICY ENGINE / TOKEN / SESSION STORE / QUEUE /
WORKFLOW ENGINE / OUTBOX / CRDT / API ROUTE / TABLE / INDEX
IMPLEMENTS IT
```

A requirement may constrain later technology selection without selecting that technology here.

## Authority and interpretation

Requirements in this directory consume, and do not reopen or replace:

1. the current Product/North Star and applicable product safety/privacy requirements;
2. the CLOSED Domain Atlas;
3. the CLOSED Logical Model and `WL-H01..WL-H12`;
4. current ADR statuses;
5. current architecture sources, especially `../pre-physical-architecture-baseline.md` and `../system-overview.md`.

If a requirement appears to require new Domain/Logical meaning rather than technical enforcement of accepted meaning, stop and open a separate semantic-reopen analysis. Do not solve the problem by inventing a generic ontology, permission root, fact root, entity root or physical convenience model.

## Phase 5 packages

Read all four current packages:

1. [`authn-authz.md`](authn-authz.md) — authentication identity/context and authorization enforcement requirements;
2. [`security-privacy-retention-recovery.md`](security-privacy-retention-recovery.md) — confidentiality, privacy, minimization, retention, deletion/redaction and security-aware recovery requirements;
3. [`consistency-side-effects.md`](consistency-side-effects.md) — expected state, idempotency, concurrency, multi-owner consistency, provider/external effects and reconciliation/compensation requirements;
4. [`nonfunctional-multidevice-recovery.md`](nonfunctional-multidevice-recovery.md) — scale/latency/availability classes, multi-device/offline behavior, resilience and operational recovery requirements.

These are four distinct logical documents. If a future tool/size limit requires one of them to be physically split, that split is a lossless partition of that document's complete payload, not a summary or condensed replacement.

## Requirement vocabulary

Each package separates three classes:

```text
MUST / MUST NOT
accepted requirement that downstream design must satisfy

OPEN PARAMETER / OPEN DECISION
required value or policy that is not yet responsibly fixed

DEFERRED MECHANISM
implementation choice intentionally left to later architecture/Physical/runtime work
```

`OPEN` never means optional or forgotten. It means the project must resolve the value at the stated later gate before a design depending on it may be accepted.

## Cross-package invariants

All packages preserve at minimum:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical LifeOS state
derived projection != canonical truth
absence / unknown != false
MaterialStateRef != ETag / MVCC token / provider revision
idempotency != semantic identity
HTTP route / UI button / technical AuthZ action != canonical governed effect
```

The full `WL-H01..WL-H12` set remains mandatory downstream.

## Recovery ownership split

The word `recovery` has two different requirement owners here.

### Security/privacy recovery

Owned by `security-privacy-retention-recovery.md`:

- protection of backup/recovery data;
- authorization and audit of backup/restore access;
- retention/deletion/redaction correctness through restore;
- prevention of unauthorized resurrection or exposure of sensitive data.

### Operational recovery

Owned by `nonfunctional-multidevice-recovery.md`:

- RPO/RTO classes and targets;
- service restore behavior;
- degraded-mode behavior;
- restore testing;
- operational resilience/capacity recovery.

The two packages must remain consistent but must not redefine one another.

## External standards/evidence boundary

External security/privacy standards and regulations may pressure-test these requirements, but they do not become LifeOS ontology and do not automatically select an implementation mechanism.

Where a legal value, retention duration, data classification, identity-assurance level or operational target requires qualified evidence not yet accepted, the requirement records it as an explicit open parameter rather than inventing a value.

## Downstream gate — current

Phase 10 has already consumed these packages into the current Physical benchmark method, hard gates, scenario corpus and sensitivity treatment.

The later separately authorized Physical Model workstream MUST therefore:

- execute the applicable accepted requirements as hard benchmark/design constraints;
- resolve any still-open parameter whose value materially changes candidate scoring before claiming a final result;
- preserve explicit uncertainty/sensitivity where the product has not responsibly fixed one value;
- reject a Physical/runtime design that cannot preserve an accepted requirement unless a separate authorized upstream reopen changes that requirement.

```text
PHASE 10
method + benchmark pressure defined

PHYSICAL MODEL
actual candidate execution / design / selection
```

These packages remain current requirements throughout that later work.