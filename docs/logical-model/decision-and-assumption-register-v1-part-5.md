<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-4.md" -->
> **Canonical continuation of `decision-and-assumption-register-v1.md`.** This Part 5 records Integrated A+B+C+D decisions.

# 2026-08-17 — Integrated A+B+C+D decisions

## DEC-ABCD01 — current is axis-specific

```text
DECISION
`current` must be qualified by meaning. Knowledge/acceptance currentness and world/effective applicability are distinct axes.

STATUS
ACCEPTED WITH HARDENING
```

## DEC-ABCD02 — unknown applicability is valid

```text
DECISION
When applicability cannot be established, LifeOS preserves unknown/unresolved rather than forcing active/inactive/permanent.

STATUS
ACCEPTED
```

## DEC-ABCD03 — historical relevance survives resolution

```text
DECISION
No-longer-applicable state may remain relevant to later queries. Retrieval relevance does not change canonical applicability.

STATUS
ACCEPTED
```

## DEC-ABCD04 — no implicit continuing-state promotion

```text
DECISION
A point Observation or AI/provider inference cannot silently establish a continuing condition/state.

STATUS
ACCEPTED
```

## DEC-ABCD05 — MaterialStateRef remains state-only addressability

```text
DECISION
MaterialStateRef does not encode universal truth/currentness/applicability/relevance/Visibility.

STATUS
ACCEPTED
```

## DEC-ABCD06 — bitemporality remains physical-stage candidate

```text
DECISION
Valid-time/transaction-time techniques are retained as serious Physical Model candidates but are not adopted as a universal semantic Fact/State root.

STATUS
RETAIN + HARDEN
```

## DEC-ABCD07 — no new reference/category root

```text
DECISION
No ApplicabilityRef, CurrentRef, KnowledgeRef or FactRef is introduced.

STATUS
ACCEPTED
```

## DEC-ABCD08 — WD-03 current-scope status

```text
DECISION
WD-03 is PASS WITH HARDENING at A+B+C+D scope; final Whole-Logical discharge waits for E/F and final regression.

STATUS
ACCEPTED
```

# Rejected alternatives

```text
one generic `current` boolean
one universal active/inactive status
latest stored record = currently applicable
applicable_now=false => discard from all retrieval
point Observation => condition automatically
AI inference => current condition automatically
MaterialStateRef => universal truth/current flag
universal bitemporal Fact root
```

# Assumption updates

## ASM-ABCD01

```text
ASSUMPTION
Most current-product queries can use a projection that separately carries/derives knowledge-currentness and world applicability without user-visible complexity.

REFRESH
Physical Model / retrieval design / whole-logical regression.
```

## ASM-ABCD02

```text
ASSUMPTION
Owner-specific lifecycle/applicability semantics remain sufficient; no universal Applicability primitive is required.

REFRESH
Slice E/F, specialist profiles, Whole-Logical.
```

## ASM-ABCD03

```text
ASSUMPTION
Bitemporal or event-history storage may be selectively applied without changing Logical owner semantics.

REFRESH
Physical Model candidate comparison.
```