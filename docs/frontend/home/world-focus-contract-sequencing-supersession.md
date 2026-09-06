# DANTE — World Focus Contract Sequencing Supersession

**Status:** CURRENT SEQUENCING ERRATA — SEMANTIC CONTRACTS PRESERVED — POST-M1 SAFETY CLOSED / M2 NEXT  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This file resolves sequencing drift without rewriting or weakening the semantic payload of:

```text
world-focus-product-contract.md
world-focus-platform-contract.md
```

Those documents remain authoritative for product/platform invariants. Their phase-time statements that name the World contextual DANTE spatial/presence review as the current or next gate are historical and are superseded.

Specifically superseded for sequencing:

```text
product contract section 25 — Immediate product gate — World contextual DANTE spatial/presence model
platform contract section 1 — spatial relation described as current product gate
platform contract section 13 — geometry described as current next gate
platform contract section 19/21 — current DANTE spatial gate language
platform contract section 26 — Current next platform gate
```

Historical work represented by those sections has already progressed through:

```text
D0 contextual DANTE spatial contract — ACCEPTED
D1 quiet invoke + compact composer — CLOSED FOR SEQUENCING
WS0–WS8 — CLOSED
POST-WS8 hygiene — CLOSED
PRE-M0 falsification — CLOSED / PASS
M0 — CLOSED
M1-1 identity/reference ownership — CLOSED / VALIDATED
M1-2 non-visual facets + application seams — CLOSED / VALIDATED
M1 final red-first falsification — CLOSED / PASS AFTER REAL CURSOR HARDENING
M1 — CLOSED
POST-M1 safety audit/falsification — CLOSED / PASS AFTER REAL BOUNDARY HARDENING
```

The post-M1 safety gate was intentionally run before M2 implementation. It found two concrete production defects — cancelled non-cooperative reads reaching validation and O8 evidence caller-alias retention — and both were repaired under existing owners without weakening the hostile test.

Durable safety evidence:

```text
RED HEAD  0b674effa292881303288dd90c88db2c14e61872
RED CI    33747167897 FAIL
7 / 9 hostile tests PASS
296 PASS / 2 FAIL overall web units

FIX HEAD  ecc2128b62395f82eab9ee7ff239355b4ca81ee4
FIX CI    33754084001 PASS
9 / 9 hostile tests PASS
56 / 56 web test files PASS
301 / 301 web unit tests PASS
full Frontend CI Gate PASS
```

This closes the pre-M2 safety hold. It does not reopen M1 or WS0–WS8 and does not create any new semantic owner.

Current sequencing authority order:

```text
1. world-focus-current-checkpoint.md
2. world-focus-post-m1-safety-falsification-review.md
3. world-focus-m1-operational-handoff.md
4. world-focus-m1-core-nonvisual-materialization-review.md
5. world-focus-m0-materialization-mapping.md
6. world-focus-frontend-roadmap.md
7. world-focus-substrate-closure-plan.md
8. this sequencing supersession record
9. product/platform contracts for semantic invariants
```

Current live sequence:

```text
M1                         CLOSED / VALIDATED
POST-M1 SAFETY             CLOSED / PASS
M2 Shared Visual Primitives NEXT
M3                         BLOCKED BY M2
M4 D2–D6 Contextual DANTE  BLOCKED BY M3
M5–M7                      BLOCKED BY SEQUENCE
BACKEND                     BLOCKED UNTIL M7
```

This supersession does NOT change:

```text
World definition
World/DANTE role
Output Grammar
DANTE P0–P5 distinctions
Domain/Logical boundaries
WF0/WF-G3
privacy/disclosure rules
Proposal != Decision != effect
provider ACK != canonical completion
backend stop line
```

D2–D6 remain intentionally deferred to M4. They must not be pulled forward merely because an older contract says the DANTE spatial gate is next.

Immediate continuation:

> **Begin M2 only. M3 customization, M4 DANTE D2–D6 and backend work remain blocked by sequence.**
