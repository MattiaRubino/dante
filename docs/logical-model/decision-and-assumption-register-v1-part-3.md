<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-2.md" -->
> **Canonical continuation of `decision-and-assumption-register-v1.md`.** This physical file is Part 3 of the same logical register and records integrated A+B+C decisions, alternatives, assumptions and deferrals.

# 2026-08-17 — Integrated A+B+C decisions

## DEC-ABC01 — Occurrence identity is semantic, not materialization-granted

```text
DECISION
Once an individual canonical Occurrence is semantically distinguished, it has LR-01 identity regardless of whether a physical row already exists.

STATUS
ACCEPTED WITH HARDENING
```

## DEC-ABC02 — unordered quota recurrence delays individual identity until differentiation where semantics provide no coordinate

```text
DECISION
Equivalent expected quota slots need not receive arbitrary semantic ordinal/deterministic identity before one slot becomes individually distinguished.
Once distinguished, stable Occurrence identity is preserved.

STATUS
ACCEPTED
```

## DEC-ABC03 — canonical Actual is LR-02 + LR-06

```text
DECISION
Every canonical Actual is a persistent contextual realization record with dependent scoped identity plus realization semantics.
Address with ScopedRecordRef where needed; do not promote to NativeRef.

STATUS
ACCEPTED WITH HARDENING
```

## DEC-ABC04 — source assertion does not establish Actual/Outcome

```text
DECISION
Provider events, user assertions, device telemetry and AI inferences remain source/assertion state until applicable Confirmation/Reconciliation/Authority/policy establishes canonical Actual/Outcome.

STATUS
ACCEPTED
```

## DEC-ABC05 — preserve zoned intent and accepted resolution basis

```text
DECISION
Where consequential historical reconstruction matters, preserve originating wall-clock/frame semantics plus enough accepted resolution basis to explain/reproduce the interpretation actually used.
Future named-zone recurrence is not frozen to historical offsets.

STATUS
ACCEPTED WITH Slice-D/Physical proof obligation
```

## DEC-ABC06 — integrated technology/mechanism result

```text
SELECTED
Layered Typed Time & Reality
+ discriminated ReferenceAddress
+ typed temporal values

VERDICT
RETAIN + HARDEN
```

## Reopened alternatives

### ALT-ABC01 — owner-specific temporal representation only

```text
RESULT
RETAINED AS STRONG PHYSICAL INGREDIENT
NOT SELECTED AS COMPLETE LOGICAL BASELINE
```

### ALT-ABC02 — universal TemporalEvent / Timeline root

```text
RESULT
LOGICALLY REJECTED
```

### ALT-ABC03 — universal event-sourced/bitemporal fact ledger

```text
RESULT
REJECTED AS UNIVERSAL LOGICAL REQUIREMENT
RETAINED AS POSSIBLE BOUNDED PHYSICAL/HISTORY TECHNIQUE
```

### ALT-ABC04 — provider/calendar recurrence kernel

```text
RESULT
REJECTED
```

## Assumptions

### ASM-ABC01 — Slice D can realize Actual/temporal material-state history without semantic collapse

```text
STATEMENT
A Version/Provenance/Reconciliation mechanism can preserve Actual identity/state separation, Schedule history, governing recurrence state and accepted temporal resolution basis without requiring one universal event root.

CONFIDENCE
HIGH

STATUS
ACCEPTED WITH Slice-D PROOF OBLIGATION

FAILURE CONSEQUENCE
reopen mechanism under LM-WF-21 before changing Domain semantics
```

### ASM-ABC02 — physical occurrence identity can support both deterministic-locator and lazy opaque-ID families

```text
STATEMENT
The Physical Model can preserve stable canonical Occurrence identity while allowing recurrence-family-specific pre-materialization locators and opaque identity establishment for previously indistinguishable quota slots.

CONFIDENCE
HIGH logical plausibility

STATUS
ACCEPTED WITH PHYSICAL PROOF OBLIGATION
```

### ASM-ABC03 — historical zoned-resolution basis can be stored without freezing future recurrence

```text
STATEMENT
Physical time representation can retain past accepted interpretation while future recurrence continues under applicable named-zone rules/policy.

CONFIDENCE
HIGH

STATUS
ACCEPTED WITH PHYSICAL PROOF OBLIGATION
```

## Evidence register

```text
EVID-ABC01 RFC 5545 recurring-instance identity             STRUCTURAL PRINCIPLE
EVID-ABC02 Google Calendar originalStartTime               CURRENT PRODUCT / INSTANCE IDENTITY
EVID-ABC03 RFC 9557 zone + offset inconsistency/rule drift  STRUCTURAL PRINCIPLE / TZ HISTORY
EVID-ABC04 PostgreSQL current timezone docs                 PHYSICAL FEASIBILITY / TZ RULE PRESSURE
```

## Physical/later-slice deferrals

```text
DEFER-ABC01 exact virtual/lazy Occurrence key strategy
DEFER-ABC02 exact Actual table/record identity strategy
DEFER-ABC03 exact MaterialStateRef persistence
DEFER-ABC04 tzdb version / resolved instant / offset capture strategy
DEFER-ABC05 event/bitemporal history use, if any
DEFER-ABC06 exact source assertion -> canonical Actual reconciliation persistence
```

None of these deferrals permits weakening INV-131..142.
