<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-2.md" -->
> **Canonical continuation of `test-corpus-v1.md`.** This physical file is Part 3 of the same logical corpus. Earlier scenarios remain permanent; this continuation adds integrated A+B+C regression pressure.

# Q. Integrated A+B+C cumulative regression expansion

## TC-Q01 — Lazy calendar Occurrence identity

A weekly Event instance is derivable from the recurring source but has no physical row yet. It is later rescheduled individually.

Required:

```text
same semantic Occurrence before/after materialization
materialization != new identity
Occurrence -> LR-01
```

## TC-Q02 — Unordered quota slots before differentiation

Routine requires `3x/week`; no dates/order are yet assigned.

Required:

```text
expected cardinality = 3
no semantic first/second/third invented
no universal deterministic per-slot identity required yet
```

When one slot is scheduled/edited/skipped/reconciled, that individual expected instance receives/preserves one stable Occurrence identity.

## TC-Q03 — Actual identity survives correction

Actual A1 initially establishes `performed`; later authoritative reconciliation corrects one material facet.

Required:

```text
ScopedRecordRef(A1) remains same contextual Actual identity where owning identity survives
MaterialStateRef(A1,v1) != MaterialStateRef(A1,v2)
correction history preserved
```

## TC-Q04 — Source assertion is not Actual

Provider says `completed`; user says `not performed`; device is silent.

Required:

```text
three source/assertion states may coexist
no provider/newest/confidence auto-winner
no established Actual until applicable reconciliation/confirmation/governance resolves it
```

## TC-Q05 — AI inferred Outcome is provisional

AI infers `passed` from partial evidence.

Required: inference can be preserved as candidate/assertion/evaluation support but does not establish canonical Outcome by itself.

## TC-Q06 — Historical zoned placement after tzdb change

A Schedule was accepted/resolved as a named-zone wall-clock placement. Later the IANA zone rules are revised.

Required:

```text
original wall-clock/zone intention preserved
historically accepted resolved interpretation remains reconstructible
later tzdb update does not silently rewrite past accepted state
```

## TC-Q07 — Future recurrence after zone-rule change

Same recurring source as Q06 has future unmaterialized instances.

Required:

```text
past resolved state remains historical
future named-zone recurrence follows current accepted recurrence/time-zone policy
historical preservation != freezing all future offsets
```

## TC-Q08 — UTC-only mutation

Candidate representation stores only resolved UTC for a wall-clock recurring intention.

Required: FAIL where wall-clock/zone semantics matter because future recurrence/travel/DST intention is lost.

## TC-Q09 — Zone-only historical mutation

Candidate stores only `09:00 Europe/Rome` for a consequential historical accepted placement and later re-resolves it using changed rules.

Required: FAIL where exact previously accepted resolution matters.

## TC-Q10 — Occurrence DB-row identity mutation

Candidate gives no Occurrence identity until insert time and treats materialization as creation.

Required: FAIL for already-distinguished virtual instances.

## TC-Q11 — Actual promoted to NativeRef

Candidate represents every Actual as a universal native reality object.

Required: FAIL. Actual remains contextual LR-02 + LR-06 and does not become a universal native root.

## TC-Q12 — Bitemporal ledger as ontology

Candidate stores all changes in one valid-time/transaction-time fact ledger and treats that ledger row type as the semantic owner.

Required: FAIL as universal logical model; typed owners/relations still determine meaning. Bitemporal/event history may remain bounded implementation infrastructure.

## Integrated A+B+C high-value queries

76. Can LifeOS distinguish an individually known virtual Occurrence from an unordered quota slot not yet individually distinguished?
77. Can an Occurrence keep identity across lazy materialization and later rescheduling?
78. Can a canonical Actual be addressed independently from its current MaterialStateRef without becoming NativeRef?
79. Can conflicting source assertions be retrieved without treating one as established Actual automatically?
80. Which source/reconciliation/confirmation basis established the current Actual at time T?
81. Can historical zoned Schedule state reproduce the interpretation actually accepted at T after time-zone-rule changes?
82. Can future named-zone recurrence adapt to later rules without rewriting past resolved states?
83. Can the system compare intended wall-clock meaning with resolved instant/offset without collapsing either?
84. Can current state remain queryable without universal event-log replay?
85. If a mechanism hardening changes identity/history pressure, which rejected alternatives were re-opened and why did the current mechanism still win or get replaced?

## Integrated result

```text
TC-Q01..Q12
PASS / PASS WITH Slice-D exact history/provenance proof obligations

DOMAIN REOPEN REQUIRED       0
LOGICAL STRUCTURAL BLOCKER   0
MECHANISM VERDICT            RETAIN + HARDEN
```
