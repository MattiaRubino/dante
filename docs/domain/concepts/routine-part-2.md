<!-- LIFEOS-CANONICAL-CONTINUATION document="routine.md" follows="routine.md" -->
> **Canonical continuation of the logical Routine v0 concept.** Earlier Routine v0 content remains unchanged; this continuation records only the downstream Conditional Policy / Trigger resolution.

# 2026-08-15 — Routine versus Conditional Policy

Routine v0 already established:

```text
Routine != Trigger
arbitrary IF condition THEN action logic must not be hidden inside Routine
```

Conditional Policy v0 now provides the separately owned conditional-response semantics.

```text
Routine
= persistent reusable policy for repeated behavior/execution expectation

Conditional Policy
= bounded response when an activation basis is established
```

Therefore:

```text
Routine != Conditional Policy
Routine identity != fallback/adaptation rule
```

A Routine may reference or be coordinated with one or more Conditional Policies without absorbing them.

## Adaptive/fallback examples

```text
Routine
Training Mon/Wed/Fri

Conditional Policy
if Wednesday session becomes infeasible within approved scope
→ propose replacement slot
```

```text
Routine
Weekly review

Conditional Policy
if unresolved high-impact items remain at review time
→ surface them in review
```

```text
Routine
Medication expectation

Conditional Policy
if required Confirmation remains unresolved under explicit policy
→ remind / escalate / review
```

The Routine remains the repeating behavioral/execution policy. The Conditional Policy owns the bounded conditional response.

## No automatic Actual/completion

```text
Conditional Policy activated
!= Routine Occurrence completed
!= Actual execution
!= Outcome
```

A policy may initiate a reminder, proposal, request or bounded authorized change. The relevant owning concepts determine what becomes effective and what actually happens.

## No hidden Authority

A Routine may carry user-defined adaptive rules, but neither Routine nor Conditional Policy grants itself Authority.

Any automatic adaptation is effective only within separately established autonomy/Authority boundaries.

## Material change

A material Routine change and a material Conditional Policy change remain independently versionable/applicable.

A response to or activation under an earlier Routine/Policy material state does not silently carry into a materially changed state.

## Result

```text
ROUTINE v0
verdict unchanged
REOPEN 0

Conditional Policy
separate accepted conditional-response family

Trigger
activation role/facet
NOT Routine identity
```

The former Trigger boundary is resolved without turning Routine into a workflow/automation engine.