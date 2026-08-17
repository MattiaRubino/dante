<!-- LIFEOS-CANONICAL-CONTINUATION document="time-reality-v1.md" follows="time-reality-v1.md" -->
> **Canonical continuation of `time-reality-v1.md`.** This Part 2 records integrated A+B+C hardening and supersedes broader Slice-C wording where explicitly stated.

# 2026-08-17 — Integrated A+B+C hardening

## 22. Occurrence identity supersession

The earlier disposition `LR-01 once persistently addressable/materially historical` is too permissive if read as making identity a storage choice.

Current rule:

```text
once one canonical individual Occurrence is semantically distinguished
-> LR-01 logical identity

lazy / virtual / non-row representation
!= identity-less Occurrence

physical materialization
!= granting a different identity
```

This does not require eager materialization.

For unordered quota recurrence, the source may initially express only bounded expected cardinality / equivalent virtual slots. LifeOS need not pre-invent a deterministic semantic ordinal or identity for every indistinguishable future slot. Once one expected instance becomes individually distinguished by interaction, Schedule, exception, provider mapping, Actual, Evidence or another material fact, one stable opaque Occurrence identity is established/preserved without creating `first/second/third` semantics.

```text
deterministic virtual locator
= recurrence-family-specific capability
!= universal Occurrence identity requirement
```

## 23. Actual identity supersession

The earlier wording `LR-02 when persistent identity/reference is required` is superseded.

Every canonical Actual is the accepted Domain persistent contextual realization record and therefore carries:

```text
Actual
-> LR-06 material realization
+  LR-02 dependent contextual semantic record
```

When addressability is required:

```text
ScopedRecordRef(Actual)
```

is used under the applicable Reference Contract.

```text
Actual identity != NativeRef/native referent identity
Actual identity != MaterialStateRef(Actual state)
```

Correction normally changes material state/current interpretation, not Actual identity by default.

## 24. Establishment barrier

External or asserted reality is source state until the applicable semantics establish canonical realization/result.

```text
user assertion
provider status/event
sensor telemetry
AI inference
imported completion flag
!= established Actual automatically
!= established Outcome automatically
```

These may become Evidence/support for Confirmation/Reconciliation/Decision/authorized policy. Conflicting assertions may remain unresolved. Time passage/provider silence is likewise not establishment.

## 25. Zoned temporal reconstruction hardening

When a named-zone wall-clock state is consequentially accepted/resolved, later historical reconstruction must retain both:

```text
originating civil/wall-clock meaning + zone/frame semantics
AND
sufficient accepted resolution basis to reproduce/explain the interpretation actually used
```

A later IANA/tzdb rule change must not silently rewrite past accepted/resolved meaning.

This does not freeze future recurring instances to historical offsets. Future named-zone recurrence follows its accepted recurrence/time-zone policy and applicable rules unless that policy itself changes.

Exact persistence may use resolved instant/offset, rule-set/version context or another reviewed mechanism. Slice C fixes the reconstruction requirement; Slice D/Physical Model selects the mechanism.

## 26. Mechanism reconsideration result

Integrated A+B+C reopened:

```text
owner-specific temporal records only
universal TemporalEvent/Timeline root
universal event-sourced/bitemporal fact ledger
provider/calendar-series kernel
Layered Typed Time & Reality + ReferenceAddress + typed temporal values
```

Verdict:

```text
SELECTED
Layered Typed Time & Reality Model

MECHANISM / TECHNOLOGY
RETAIN + HARDEN
```

Event/bitemporal infrastructure remains a possible bounded physical history technique. It is not a universal semantic root.

## 27. Integrated status

```text
SLICE C
PASS WITH HARDENING / REMOTE QA PASS at original Slice-C scope

INTEGRATED A+B+C
PASS WITH HARDENING
activation conditional on integrated hardening remote QA and closure

DOMAIN REOPEN REQUIRED 0
```
