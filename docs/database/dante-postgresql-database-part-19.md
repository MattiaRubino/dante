<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-18.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 19

**Status:** CP6-05 FINAL QA REPAIR CANDIDATE / DIRECT POSTGRESQL ACCEPTANCE REQUIRED  
**Scope:** final clean-room reconciliation after CP6-04 materialization and persistent LOCAL proof  
**Authority:** narrow supersession only where this Part is more exact than Parts 14/17/18  
**Topology:** unchanged — 68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs  

---

## 56. CP6-05 final clean-room repair

### 56.1 Why a final repair exists

CP6-04 successfully materialized M1..M7 and proved the persistent LOCAL database, but the mandatory CP6-05 replay found one technical contract mismatch and two repository-consistency gaps:

```text
CP6F-01  Role-13 did not independently acquire the source occurrence-generation lock
CP6F-02  Part-14 BLAKE2b personalized key could not be reproduced by PostgreSQL core
CP6F-03  historical M6 scope proof was stage-absolute after M7 closure
CP6F-04  occurrence mapping filename in Part 14 differed from the accepted implementation filename
CP6F-05  final cross-representation / concurrency proof needed one clean-room head-level suite
```

No semantic owner, relation, constraint, index or ACL family is reopened.

### 56.2 Forward-only corrective revision

The accepted repair is a normal Alembic revision above M7:

```text
20260826_07  CP6-M07 runtime ACL activation
    ↓
20260826_08  CP6-05 final QA hardening
```

`20260826_08` is **not CP6-M08** and does not append a materialization stage. `scope.json.completed_stages` remains exactly CP6-M01..CP6-M07 because all baseline objects were already introduced by M1..M7.

The revision changes only the body of the existing Role-13 routine. Object counts remain frozen.

### 56.3 Advisory key digest — narrow supersession of 48.29 / 48.31

The high-level key layout and namespace registry remain unchanged:

```text
bits 62..56 = 7-bit namespace code
bits 55..0  = 56-bit deterministic digest
sign bit    = 0
one-argument PostgreSQL bigint advisory lock
namespace codes 1..7 unchanged
```

Part 14's BLAKE2b `digest_size=7, person=b"dante-lock-v1"` digest is narrowly superseded because PostgreSQL 18 core cannot reproduce that personalized variable-output BLAKE2b contract without adding a new extension, new helper routine family, or a bespoke cryptographic implementation. Any of those would be worse than changing a non-persisted lock-key derivation before CP6 closure.

Final digest contract:

```text
domain prefix = b"dante-lock-v2"
input         = domain prefix || UUID canonical 16 raw bytes
hash          = SHA-256
low digest    = first 7 bytes of SHA-256 output
interpretation= unsigned big-endian 56-bit integer
```

Python:

```python
digest56 = int.from_bytes(
    sha256(b"dante-lock-v2" + semantic_ref.bytes).digest()[:7],
    "big",
)
lock_key = (namespace_code << 56) | digest56
```

PostgreSQL uses only core functions:

```text
sha256(convert_to('dante-lock-v2','UTF8') || uuid_send(source_ref))
get_byte(..., 0..6)
```

This is cross-language deterministic and introduces no new extension or persisted object.

### 56.4 Final golden vector

For:

```text
UUID 018f1f26-8b2e-7abc-8000-000000000001
SHA-256 prefix digest56 bytes = 97 02 ff de 8c 05 09
```

exact keys are:

```text
namespace 1 = 114563613494871305
namespace 2 = 186621207532799241
namespace 3 = 258678801570727177
namespace 4 = 330736395608655113
namespace 5 = 402793989646583049
namespace 6 = 474851583684510985
namespace 7 = 546909177722438921
```

Routine generation pair:

```text
330736395608655113
474851583684510985
```

Event generation pair:

```text
402793989646583049
546909177722438921
```

### 56.5 Role-13 defense in depth — final contract

Section 55.16 remains authoritative in intent and is now fully materializable.

For every `origin_code='recurrence_generated'`, after resolving `source_family` and before final coordinate/cardinality validation, Role 13 acquires the exact source occurrence-generation transaction lock:

```text
Routine → namespace 6 + source RoutineRef
Event   → namespace 7 + source EventRef
```

The application operation still acquires the sorted pair:

```text
source current-recurrence lock + source occurrence-generation lock
```

Role 13 reuses the same generation lock. PostgreSQL transaction advisory locks are re-entrant for the same transaction, so accepted application paths do not deadlock themselves.

The final database proof must also omit the application lock intentionally and show that two concurrent quota writers or duplicate non-quota writers still serialize at deferred Role-13 validation, producing exactly one accepted generation and one SQLSTATE `23514` rejection.

No owner-row `FOR UPDATE`, synthetic runtime UPDATE privilege, extra lock table, extra routine or extra index is introduced.

### 56.6 Mapping module filename — narrow supersession of 48.4 / 48.12 filename only

The implemented module is accepted as:

```text
dante/platform/database/mappings/occurrence_generation.py
```

rather than the earlier planning handle `occurrence.py`.

Reason: the same package already keeps `OccurrenceRow` in `identity.py`; `occurrence_generation.py` names the five actual mapping rows more precisely and prevents ambiguity between semantic Occurrence identity and generation provenance.

Only the Python module filename statement is superseded. The exact five Row classes, five tables, 68-mapping total, relationship-free posture and SQLAlchemy semantics remain unchanged.

### 56.7 Historical-stage test doctrine

A historical stage test may prove the accepted stage prefix without requiring the repository's current `scope.json` to stop at that historical stage.

Therefore:

```text
M4 → completed_stages[:4]
M5 → completed_stages[:5]
M6 → completed_stages[:6]
```

is the correct pattern. A later accepted stage or corrective revision must not falsify an earlier structural proof merely because current repository metadata advanced.

### 56.8 CP6-05 acceptance

CP6 is not closed by publication of this Part or revision 08. Closure requires one direct acceptance on the exact candidate HEAD proving:

```text
Draft 2020-12 Dictionary schemas + 87 object instances
semantic Dictionary validator clean
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL clean
fresh → head and head → base → head
Alembic check clean
68 / 5 / 14 / 75 / 95 / 68 / 120 exact topology
exact M7 ACL posture preserved
Python ↔ PostgreSQL lock golden vectors identical
real async lock helper transaction behavior
Role-13 exact lock present
quota two-connection race: one PASS + one 23514
non-quota duplicate race: one PASS + one 23514
full backend pytest
Ruff
mypy strict
persistent LOCAL upgrade 20260826_07 → 20260826_08
LOCAL restart persistence + backend readiness
```

Until that direct run is green, status remains **CANDIDATE / ACCEPTANCE REQUIRED**.
