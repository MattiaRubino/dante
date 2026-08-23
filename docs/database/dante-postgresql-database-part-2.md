# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 2

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md`
- **Continuation numbering:** future substantive sections begin at section 31
- **Structural split anchor:** `efb80da23db60b82f641b6e9329500af00cbbf46`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of `dante-postgresql-database.md`. It does not replace, summarize or supersede Part 1 as a whole.

The human-readable DANTE Database Architecture & Reference is one logical authority physically split across active parts:

```text
dante-postgresql-database.md
PART 1
sections 1–30
+

dante-postgresql-database-part-2.md
PART 2
section 31 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

A reader, reviewer, implementation task, migration plan, Database Dictionary reconciliation or whole-database audit MUST consume all active parts. The latest part alone is never the whole database reference.

The split exists solely to keep future Git writes bounded, reviewable and safe as the database reference grows. It does not change database meaning, authority ordering, Gate-03 requirements or any previously accepted physical decision.

Part 1 remains authoritative and intact for every decision recorded in sections 1–30 unless a later numbered section in an active continuation explicitly identifies a narrower earlier statement that it supersedes after the required cumulative audit.

---

## Authority and derivation contract

The derivation chain remains exactly:

```text
closed Domain
→ closed Whole-Logical model
→ CP6-01 persistence coverage / pressure
→ accepted PostgreSQL Physical mapping
→ CP6-02 PostgreSQL Persistence Constitution / ADR-010
→ concrete CP6-03 PostgreSQL blueprint
→ CP6-04 Alembic + SQLAlchemy + real PostgreSQL materialization
→ CP6-05 direct PostgreSQL / consistency proof
```

This continuation does not gain authority to redefine upstream semantics merely because it is later in file order.

For every later database fact:

```text
semantic meaning
→ must remain traceable to upstream authority

physical PostgreSQL decision
→ must preserve that meaning

fact not determinable from accepted authority
→ explicit classified non-materialization / future trigger
→ never an invented placeholder
```

The existing non-collapse and anti-shortcut rules remain in force across every part, including the rejection of universal Entity/Thing, universal Relationship/edge, canonical EAV/property bags, universal Fact/Version payload roots, universal Rule(type,payload), generic semantic JSON fallbacks and application-only heterogeneous `kind + uuid` references without database integrity.

---

## Explicit supersession rule

Later numbered sections may supersede an earlier provisional or candidate statement only when all of the following are true:

```text
1. the later section names the affected earlier area explicitly;
2. the replacement is derived from the accepted authority chain;
3. the complete accumulated database is regressed after the change;
4. every B/C finding is repaired before PASS;
5. no unrelated earlier decision is silently reinterpreted;
6. the write is bounded by an approved Git scope and remotely QA'd.
```

Therefore:

```text
later file position
!= blanket higher semantic authority

new checkpoint
!= permission to rewrite unrelated accepted history

physical convenience
!= authority to change Domain/Logical meaning
```

Where no explicit later supersession exists, the applicable Part-1 contract remains fully in force.

---

## Write-preservation rule

The multi-part layout exists to preserve detail, not to reduce it.

Future database-reference writes MUST NOT simplify Git operations by deleting, condensing or replacing accepted detailed content with summaries.

Forbidden write behavior:

```text
replace detailed approved sections with a shorter recap
remove negative dispositions because a later section mentions the result
collapse table/constraint/test detail into prose for file-size reasons
rewrite historical PASS/audit evidence as if it had always existed
move content between parts without a dedicated structural gate
silently renumber previously approved sections
truncate an earlier part while creating a continuation
use a "latest state" summary as a substitute for the canonical prior derivation
```

Required behavior:

```text
new independently audited block
→ detailed numbered section in the active continuation
→ explicit relationship to earlier provisional statements where necessary
→ exact Git delta QA
→ earlier canonical content retained
```

If another physical split becomes necessary for write safety or maintainability, a later `part-3` may be introduced through a dedicated structural gate using the same no-loss rules. The existence of multiple parts never changes the requirement to consume them together.

Any future re-fusion into one physical file is itself a dedicated structural documentation migration and requires full content-equivalence QA. Re-fusion must concatenate/reorganize without semantic loss; it must never replace the parts with a summary.

---

## Cumulative whole-database audit rule

Splitting the reference does not split the database audit.

Every future substantive block beginning with section 31 MUST be evaluated against the complete accumulated authority:

```text
all active Database Architecture & Reference parts
+
closed Domain
+
closed Logical
+
accepted Physical PostgreSQL mapping
+
CP6-01
+
CP6-02 Constitution / ADR
+
real backend/PostgreSQL foundation where relevant
```

The required block loop remains:

```text
derive one concrete block
→ classify candidate only
→ audit the ENTIRE accumulated database
→ A = sound / retained
→ B = underspecified / closed too early / hardening needed
→ C = contradiction / defect / missing contract
→ repair every B/C
→ repeat whole-database audit
→ PASS only when C defects = 0 and no unclassified item remains
→ exact bounded Git write gate
→ write
→ remote readback + exact PRE-SCOPE→HEAD QA
→ only then open the next block
```

A block-local PASS without accumulated regression is insufficient for CP6-03.

---

## Part 1 continuity anchor

This structural split begins immediately after the final saved state of Part 1.

```text
PART 1 FILE
docs/database/dante-postgresql-database.md

PART 1 FINAL NUMBERED SECTION
30. Consolidation checkpoint C — Recurrence / Occurrence-generation physical closure

PART 1 REPOSITORY HEAD AT SPLIT
efb80da23db60b82f641b6e9329500af00cbbf46

DB-U12
CLOSED

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER REPAIR

GLOBAL UNRESOLVED DB-U ITEMS
9

LOCAL EXACT UNRESOLVED ITEMS
6

UNCLASSIFIED NEW ITEMS
0

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

The globally unresolved set at this continuity anchor is exactly:

```text
DB-U08  final PostgreSQL object naming
DB-U09  Account persistence disposition
DB-U10  Principal/security persistence disposition
DB-U15  final structural/query index matrix
DB-U17  provider/integration object shapes
DB-U18  idempotency persistence timing
DB-U19  transactional outbox timing
DB-U20  derived/search/vector persisted structures
DB-U21  exact object-by-object runtime privilege matrix

COUNT = 9
```

The exact local unresolved set is exactly:

```text
OUT-U01
MIL-U01
AGR-U01
CRT-U01
EVL-U01
TC-U01

COUNT = 6
```

These identifiers retain the exact meanings established in Part 1. This structural file creation does not close, reopen or reinterpret any of them.

---

## Section numbering and continuation discipline

Part 1 owns numbered sections:

```text
1 through 30
```

Part 2 reserves future substantive numbering beginning at:

```text
31
```

This structural preamble is intentionally unnumbered so that the first future semantic/technical checkpoint can begin cleanly at section 31.

Numbering across active parts is one continuous logical sequence. A future Part 3, if justified, continues from the next unused number rather than resetting numbering.

---

## Structural split scope — no semantic database change

This file creation is documentation structure only.

It introduces no new:

```text
Domain concept
Logical representation
native owner
ScopedRecordRef owner
MaterialState facet
PostgreSQL table/view/type/domain/routine/index
column
constraint
Reference Contract
lifecycle rule
ACL
migration
SQLAlchemy mapping
test result
provider/search/security object
```

It also does not authorize CP6 business DDL or earn Gate 03.

The next substantive database block must start at section 31 and must begin from the exact accumulated state above rather than reconstructing or abbreviating Part 1.