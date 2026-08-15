<!-- LIFEOS-CANONICAL-CONTINUATION document="recurrence.md" follows="recurrence.md" -->
> **Canonical continuation of the logical Recurrence v0 concept.** Earlier Recurrence v0 content remains unchanged; this continuation records only the downstream Conditional Policy / Trigger resolution.

# 2026-08-15 — Recurrence versus Conditional Policy

Recurrence v0 already excluded generic IF/THEN automation and identified threshold/state/usage Trigger semantics as outside Recurrence.

Conditional Policy v0 now resolves that open boundary.

```text
Recurrence
= structured repeated temporal/generative pattern

Conditional Policy
= bounded downstream response when an activation basis is established

Trigger
= activation role/facet within Conditional Policy semantics
```

Therefore:

```text
Recurrence != Conditional Policy
Recurrence != Trigger
```

## Examples

```text
Every Monday at 18:00
→ Recurrence
```

```text
3 expected practices per week
→ Recurrence
```

```text
30 days after qualifying completion
→ Recurrence
```

```text
when balance crosses below €500
→ notify
→ Conditional Policy
```

```text
when temperature > 30°C
→ propose lighter training
→ Conditional Policy
```

```text
when vehicle usage reaches 10,000 km
→ propose maintenance
→ Conditional Policy
```

A Conditional Policy can itself have repeated applicability, and a Recurrence can supply a repeated temporal basis used by a policy. Reuse does not collapse the concepts.

## Anchor-stream guardrail

Recurrence may legitimately generate expected instances relative to a qualifying anchor stream, for example:

```text
one expected backup after each qualifying photography Session
```

That remains Recurrence when the meaning is repeated expected-instance generation.

By contrast:

```text
when a photography Session ends
→ send reminder to back up if no backup exists after N hours
```

is Conditional Policy semantics.

The boundary depends on meaning, not syntax alone.

## No generic automation engine

Recurrence remains free of:

- generic condition expressions;
- arbitrary downstream action semantics;
- Authority/Decision semantics;
- reminder/notification semantics;
- retries/debounce/idempotency;
- workflow execution architecture.

Conditional Policy v0 also does not force Recurrence into a provider cron/RRULE schema.

## History

A material Recurrence change and a material Conditional Policy change have independent applicability/history.

One does not silently version, replace, or inherit the other's prior state.

## Result

The historical Trigger/automation boundary is now **RESOLVED downstream** without reopening Recurrence.

```text
RECURRENCE v0
verdict unchanged
REOPEN 0

Conditional Policy
separate accepted family

Trigger
activation role/facet, not Recurrence primitive
```
