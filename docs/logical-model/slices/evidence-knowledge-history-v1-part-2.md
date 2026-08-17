<!-- LIFEOS-CANONICAL-CONTINUATION document="evidence-knowledge-history-v1.md" follows="evidence-knowledge-history-v1.md" -->
> **Canonical continuation of `evidence-knowledge-history-v1.md`.** This Part 2 records Integrated A+B+C+D hardening and supersedes broader wording where explicitly stated.

# 2026-08-17 — Integrated A+B+C+D hardening

## 21. Knowledge-current versus world-current

The word `current` is ambiguous unless the axis is named.

Canonical distinction:

```text
knowledge-current
= the interpretation/state LifeOS currently accepts for a bounded context

world-current / applicable-now
= whether the represented state currently applies in the modeled world
```

These may differ.

Example:

```text
LifeOS currently accepts:
"fracture resolved on 12 Aug"

knowledge-current = yes
fracture applicable now = no
```

No generic `current=true/false` field may silently represent both meanings.

---

## 22. Unknown applicability

The earlier applicability categories are hardened with an explicit unknown state requirement.

```text
applicable now
not applicable now
unknown / unresolved applicability
```

The final owner-specific vocabulary may differ, but the semantic uncertainty must remain representable.

```text
no known end
!= permanent
!= active automatically
!= resolved automatically
```

---

## 23. Historical relevance versus current applicability

A state that is not applicable now may remain relevant to a query.

Examples:

```text
healed fracture
-> not an active injury now
-> may remain relevant to rehabilitation/history/risk context

past fever
-> not current by default
-> may remain relevant to medical history/trend analysis
```

Therefore retrieval must distinguish:

```text
current applicability
historical relevance
query-purpose relevance
```

A knowledge projection must not universally drop non-current states.

---

## 24. Point Observation and inferred continuing state

A point Observation does not establish a continuing condition/state merely because a derived model finds that continuation plausible.

```text
Observation at T1
high temperature

AI inference
possible fever
```

remains distinct from an established bounded/ongoing fever episode or specialist condition state.

Canonical rule:

```text
point source fact
+ inference
!= continuing canonical state automatically
```

The inferred candidate must retain provenance/uncertainty and follow the applicable typed owner/reconciliation/acceptance path before becoming a current owner state.

---

## 25. MaterialStateRef boundary

MaterialStateRef addresses a target state. It does not by itself mean:

```text
state is currently applicable
state is current knowledge
state is true
state is visible
state is relevant to current query
```

Those questions remain separate semantic axes.

No new `ApplicabilityRef`, `CurrentRef`, `KnowledgeRef` or `FactRef` is introduced.

---

## 26. Retrieval contract

A current knowledge/retrieval projection may use denormalized indicators for performance, but must be able to distinguish/recover at least where material:

```text
source semantic owner
material state
world/effective applicability
knowledge/acceptance currentness
epistemic/source nature
query-purpose relevance
Visibility
```

The projection is allowed to rank/retrieve historical information when relevant; ranking does not convert historical state into currently applicable truth.

---

## 27. Integrated verdict

```text
SLICE D
REMAINS ACTIVE
PASS WITH HARDENING

Integrated A+B+C+D
PASS WITH HARDENING — pending remote QA

ReferenceAddress
RETAIN + HARDEN

MaterialStateRef
RETAIN + HARDEN

Universal bitemporal Fact root
REJECTED

DOMAIN REOPEN
0
```