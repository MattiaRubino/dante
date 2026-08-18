# PM-08 Local / Offline Lane v1

- Status: **COMPLETE — SQLITE ADMIT AS BOUNDED LOCAL/OFFLINE CANDIDATE**
- Workstream: `feature/physical-model`
- Direct execution: **NOT RUN**
- Selection: **NONE**

## Question

Does LifeOS need a bounded local persistence mechanism that improves client/offline behavior without creating competing canonical authority?

## Candidate

Frozen PM-08 subject:

```text
SQLite 3.53.4
public domain
```

SQLite solves a problem distinct from the canonical server primary:

```text
device-local persistence
offline availability
local cache / projection
local draft state
pending-operation staging
sync/reconciliation support
```

That distinct role is sufficient for PM-08 admission as a bounded candidate.

## Authority boundary

Non-negotiable:

```text
SQLITE LOCAL STATE
!=
CANONICAL LIFEOS TRUTH

OFFLINE COPY
!=
CURRENT SERVER STATE

SYNC DELIVERY
!=
SEMANTIC ACCEPTANCE

LOCAL LAST-WRITE-WINS
!=
LIFEOS DEFAULT CONFLICT POLICY
```

NativeRef/MaterialStateRef semantics and consequential expected-state rules remain server/canonical contracts even when a client holds local representations.

## Platform evidence

SQLite supports WAL and full-text capabilities. Official SQLite WASM distributions also provide browser persistence options through OPFS-class mechanisms.

PM-08 does not select one universal web/mobile/desktop configuration because browser/WASM VFS and locking behavior has real concurrency trade-offs. For example, some OPFS/WAL combinations require exclusive locking and do not provide normal WAL concurrency benefits.

Therefore:

```text
PM-08 SELECTS
bounded semantic role / candidate

PM-08 DOES NOT SELECT
exact mobile adapter
exact desktop adapter
exact browser WASM/OPFS VFS
exact sync engine
```

## Verdict

```text
SQLITE 3.53.4
ADMIT
BOUNDED LOCAL/OFFLINE CANDIDATE

CANONICAL AUTHORITY
NO

EXACT CLIENT IMPLEMENTATION
DEFER
```

Admission is not final technology selection. PM-09 may treat the local/offline lane as an architecture implication; actual client selection/configuration belongs to the relevant implementation design after the Physical Model establishes the role.

## Required future contract

A later implementation using SQLite must define at least:

```text
what data may be cached/materialized locally
local encryption/security requirements
local lifecycle/retention
offline mutation representation
base MaterialStateRef / expected-state basis
sync/retry/idempotency behavior
conflict surfacing and reconciliation
provider/derived freshness boundaries
logout/account-switch cleanup
schema migration strategy
corruption/recovery behavior
```

No local write may silently overwrite canonical state because it arrived later.

## Scenario carry-forward

Relevant existing scenarios include:

```text
SC-009 web/mobile offline divergence
primary semantics evidence-qualified;
actual client sync/reconciliation remains implementation validation

SC-001 same-base consequential race
local client cannot bypass expected-state conflict

SC-007 / SC-008
stale local/derived basis cannot create permanent governance authority

SC-033 older client/effect-contract version
local persisted request format cannot bypass newer safety rules
```

## Direct execution decision

```text
SQLITE LOCAL BENCHMARK
NOT ADMITTED NOW

BROWSER CONCURRENCY TEST
NOT ADMITTED NOW
reopen only when actual client architecture depends on a specific WASM/OPFS mode

PM-08 EXECUTION-WORTHY LOCAL GAP
0
```

## Source ledger

- SQLite 3.53.4 official release history.
- SQLite WAL documentation.
- SQLite WASM/OPFS persistence documentation and locking caveats.

## Closure

```text
LOCAL/OFFLINE LANE
ADMITTED AS BOUNDED ROLE

CANDIDATE
SQLite 3.53.4

CANONICAL
NO

SELECTED
NO
```