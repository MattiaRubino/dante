<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-2.md" -->
> **Canonical continuation of `representation-framework-v1.md`.** This physical file is Part 3 of the same logical document. It appends integrated A+B+C hardening.

# 2026-08-17 — Integrated A+B+C representation hardening

## 22. Identity is not materialization

`LR-01` classifies semantic identity, not row existence.

```text
canonical individually distinguished Occurrence
-> LR-01

eager physical row
not required
```

A lazy derivation may remain non-materialized while preserving the same semantic instance where the recurrence family provides a stable locator/context.

For unordered quota recurrence, the logical model does not require every indistinguishable future slot to have preassigned deterministic identity. Stable Occurrence identity begins no later than the point the individual expected instance becomes semantically distinguished. This distinction does not create a new Domain owner or generic reference space.

## 23. Persistent contextual realization

Canonical Actual disposition is hardened to:

```text
Actual
-> LR-06 material realization
+  LR-02 dependent contextual semantic record
```

Its stable semantic-record address, when required, is `ScopedRecordRef`.

```text
ScopedRecordRef(Actual)
!= NativeRef
!= MaterialStateRef(Actual)
```

## 24. Establishment boundary

Canonical/source/derived layering applies directly to realized reality:

```text
EXTERNAL / ASSERTED
provider event, user assertion, device telemetry, AI inference

CANONICAL
established Actual / Outcome under applicable reconciliation/confirmation/governance

DERIVED
comparison, deviation, adherence, summaries, predictions
```

No source item crosses these layers merely because it is recent, confident or provider-authenticated.

## 25. Temporal value + resolution contract

For consequential zoned temporal states, LR-04 temporal semantics must be able to preserve:

```text
originating civil/wall-clock expression
zone/frame semantics
precision/granularity
accepted resolved interpretation basis where material
```

The accepted resolved interpretation may include an instant/offset/rule context through later physical design. A named zone by itself is not guaranteed to preserve the exact past interpretation if zone rules later change; an instant by itself does not preserve the wall-clock intention.

## 26. Recurrence-family-specific occurrence location

A pre-materialization occurrence locator is not a universal reference type.

```text
calendar/wall-clock recurrence
may expose stable generation coordinate

completion-relative recurrence
may expose qualifying Actual anchor

anchor-stream recurrence
may expose qualifying source occurrence/session

unordered quota recurrence
may expose only expected cardinality until a slot becomes individually distinguished
```

Therefore:

```text
universal deterministic occurrence key
NOT REQUIRED
```

## 27. Integrated mechanism verdict

```text
ReferenceAddress
RETAIN + HARDEN

Layered Typed Time & Reality
RETAIN + HARDEN

universal TemporalEvent / Node
REJECTED

universal event/bitemporal ledger
REJECTED AS LOGICAL REQUIREMENT
RETAINED AS POSSIBLE BOUNDED PHYSICAL/HISTORY TECHNIQUE
```

All later slices must replay INV-131..142 in addition to prior invariants.
