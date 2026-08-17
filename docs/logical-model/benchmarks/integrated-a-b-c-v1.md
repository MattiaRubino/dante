# LifeOS Logical Model — Integrated A+B+C Mechanism Benchmark v1

**Verified:** 2026-08-17  
**Scope:** cumulative identity/reference + intention/execution + time/reality mechanism reconsideration  
**Policy:** current external systems/standards are evidence, not ontology authority

## 1. Trigger

LM-WF-21 was triggered by five cumulative findings after Slice C: Occurrence identity vs materialization, Actual scoped identity, unordered quota-slot identity, zoned-time reconstruction under changing time-zone rules, and source-assertion vs established Actual/Outcome.

## 2. Reopened mechanisms

```text
A owner-specific temporal records/fields only
B universal TemporalEvent / Timeline / Node root
C universal event-sourced or bitemporal fact ledger
D provider/calendar-series kernel
E Layered Typed Time & Reality + discriminated ReferenceAddress + typed temporal values
```

## 3. External structural evidence

### RFC 5545 / Google Calendar

Useful principle:

```text
recurring instance identity can remain anchored to the original series instance
while current placement changes
```

LifeOS disposition: retain `Occurrence identity != current Schedule`. Do not universalize original datetime as LifeOS identity because quota/completion/anchor recurrence lacks such a coordinate.

### RFC 9557

Useful principles:

```text
named time zone carries rule semantics beyond a numeric offset
named-zone rules can change over time
offset + zone may later become inconsistent after political/tzdb changes
```

LifeOS disposition: historical consequential temporal states need originating wall-clock/frame semantics plus sufficient accepted resolution basis. Do not reduce canonical meaning to either UTC-only or zone-name-only.

### PostgreSQL current date/time documentation

Useful principles:

```text
full zone names imply rule sets and DST transitions
political/time-zone rules change
numeric offsets do not substitute for named-zone arithmetic
```

LifeOS disposition: physical PostgreSQL types remain deferred; the logical model must preserve semantics before selecting column types.

### Google Calendar recurring instances

Useful principle: `originalStartTime` identifies an instance inside a series even if `start` moves.

LifeOS disposition: strong instance-identity benchmark, not universal occurrence-key schema.

## 4. Candidate verdicts

### A — owner-specific only

**Status:** retained as physical ingredient.

Strength: local relational specificity.

Weakness as complete logical baseline: repeats temporal interpretation, history, recurrence and reconciliation mechanics and makes cross-owner historical queries ad hoc.

### B — universal TemporalEvent / Node

**Status:** rejected as logical baseline.

The new findings require more—not less—distinction among identity spaces and establishment semantics.

### C — universal event-sourced / bitemporal ledger

**Status:** rejected as universal logical requirement; retained as possible bounded physical/history technique.

Chronology and valid/transaction-time tracking can be useful, but they do not define Occurrence identity, Actual establishment, recurrence family or Outcome meaning.

### D — provider/calendar-series kernel

**Status:** rejected.

Excellent calendar interoperability pattern; insufficient for quota, completion-relative, anchor-stream recurrence and LifeOS reality establishment.

### E — layered typed model

**Status:** selected.

Why it still wins:

```text
preserves Domain owners
separates native/scoped/material/external address spaces
allows lazy identity without eager rows
supports multiple recurrence families
preserves wall-clock intent + accepted resolution
keeps Actual establishment separate from source assertions
leaves SQL/history implementation open
```

## 5. Final mechanism verdict

```text
RETAIN + HARDEN

new universal root        NO
new generic address type  NO
Domain reopen             NO
```

## 6. Refresh policy

Re-check this comparison when:

- Slice D reveals a materially different Version/Provenance mechanism;
- Physical Model begins;
- a concrete recurrence/history implementation cannot satisfy the accepted contract;
- external standard/provider behavior materially influences an implementation decision;
- Whole-Logical final regression runs.
