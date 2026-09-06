# DANTE — World Focus Post-M1 Safety Falsification Review

**Status:** CLOSED / PASS — M2 UNBLOCKED BY THIS GATE  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This review records the bounded post-M1 safety audit/falsification that ran after formal M1 closure and before M2 visual materialization.

The gate was intentionally adversarial and red-first. It did not exist to reopen M1 by default; it existed to test whether the closed non-visual substrate still had concrete production safety defects at the read boundary or snapshot boundary before renderers were layered on top.

---

# 1. Scope

The safety gate pressure focused on:

```text
cancelled World-scoped reads
non-cooperative adapter completion after abort
validator/commit suppression after cancellation
O8 Evidence/History ownership and immutability
caller alias mutation after projection creation
post-M1 hostile cross-axis behavior already exercised by the falsification suite
```

Out of scope remained:

```text
M2 visual renderers
M3 customization
M4 D2–D6 contextual DANTE
M5 complete Worlds
M6 integrated visual/a11y/performance acceptance
M7 frontend freeze
backend/API/DB/Alembic/AuthZ/provider/LLM/tool/effect execution
```

---

# 2. Red-first evidence

Red commit:

```text
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL
```

Hostile result:

```text
post-M1 safety falsification  7 PASS / 2 FAIL
whole web unit suite           296 PASS / 2 FAIL
```

The two failures were production findings, not flaky infrastructure and not test-spec disagreements.

## Finding A — cancelled non-cooperative read could still validate

A World-scoped read could be aborted upstream while the adapter ignored cancellation and later resolved. The shared reader relayed the abort signal but did not reject the late adapter result before runtime validation.

Required property:

> Once the caller has cancelled the read, a later non-cooperative adapter result must not reach the semantic validator or be returned as a usable result.

Owner remained the existing shared B0 read mechanics in `world-focus-foundation.ts`. No new semantic layer or backend owner was required.

## Finding B — O8 projection retained caller evidence aliases

`createWorldFocusEvidenceHistoryProjection()` normalized/froze its history references but reused the caller-provided `WorldFocusEvidenceReferenceFacet` object by reference.

That meant caller-side mutation of nested evidence arrays could alter the already-created projection snapshot.

Required property:

> O8 projection creation must own a normalized frozen snapshot of its evidence-reference facet, just as it owns the normalized history-reference snapshot.

Owner remained the existing L2 evidence creator plus O8 application seam. No new projection envelope or generic semantic root was required.

---

# 3. Production hardening

The adversarial test itself was not weakened.

The bounded production fixes were:

```text
world-focus-foundation.ts
  reject aborted reads both before adapter execution and after adapter await
  prevent late non-cooperative adapter results from reaching validation

world-focus-direct-projections.ts
  rebuild O8 evidence through the existing L2 evidence creator
  projection receives its own normalized frozen evidence snapshot

existing focused tests
  encode the corrected production ownership/abort behavior
```

No change was made to:

```text
World identity semantics
WP-01..WP-04 semantics
freshness/validity/coverage/disclosure/effect/sync vocabularies
DANTE context semantics
Workspace composition ownership
Domain/Logical/Physical/DB authority
backend stop line
```

---

# 4. Green evidence

Final code HEAD:

```text
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
```

Validated result:

```text
post-M1 safety falsification  9 / 9 PASS
web test files                56 / 56 PASS
web unit tests                301 / 301 PASS
contract drift                PASS
active Home format            PASS
lint                          PASS
typecheck                     PASS
architecture                  PASS
generated-source drift        PASS
production build              PASS
diff check                    PASS
repository mutation check     PASS
Mobile Bundle                 PASS
Chromium Web E2E              PASS
Firefox frozen Timeline       PASS
Frontend CI Gate              PASS
```

The final CI completed `success` on the exact closure HEAD.

---

# 5. Architectural disposition

The safety gate found two concrete implementation defects and both fit existing owners.

Therefore:

```text
new semantic primitive required        NO
new substrate layer required           NO
M1 reopen required                     NO
WS0–WS8 reopen required                NO
Domain/Logical/Physical contradiction  NO
frontend AuthZ introduced              NO
ProjectionEnvelope introduced          NO
backend authority pulled forward       NO
AI-required path introduced            NO
```

Permanent distinctions remain intact:

```text
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
Evidence != Provenance != integrity attestation
restricted != nonexistent
offline != source absent
provider lag != canonical stale
timeout != semantic negative
partial-real != failed != completed
cancel != reverse != compensate
World relevance != AuthZ
AI output != fact
```

---

# 6. Sequencing result

```text
M0                         CLOSED / VALIDATED
M1                         CLOSED / VALIDATED
POST-M1 SAFETY             CLOSED / PASS
M2 Shared Visual Primitives NEXT
M3–M7                      BLOCKED BY SEQUENCE
D2–D6                      DEFERRED TO M4
BACKEND                     BLOCKED UNTIL M7
```

This gate therefore removes the final pre-M2 safety hold. It does not itself implement M2.

Immediate continuation:

> **Begin M2 only: shared visual primitives over already-closed M1 semantics. Do not start M3 customization, M4 DANTE D2–D6 or backend work.**
