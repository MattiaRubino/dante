# DANTE — World Focus WS8 Final Falsification Review

**Status:** WS8 CLOSED — EXECUTABLE FINAL FALSIFICATION PASS  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`

This document is the final closure authority for WS8. It records the hostile executable falsification performed after WS7 and the hardening required before materialization may begin.

## 1. Final validated code state

Validated runtime/proof HEAD:

```text
88db899391a3a41e23e76177d4896a657232b5eb
```

Final Frontend CI:

```text
33639741630 — PASS — attempt 1
```

All required jobs passed on that exact SHA:

```text
Quality
  contract drift
  active Home prettier
  lint
  typecheck
  architecture check
  generated-source drift
  unit tests
  production build
  diff check
  repository mutation check

Web E2E Chromium
frozen Timeline interaction contract in Firefox
Mobile Bundle
Frontend CI Gate
```

This is the executable closure evidence. Any later documentation-only commit does not replace this validated code HEAD.

---

## 2. Falsification chain

WS8 was not a ceremonial rerun of WS7.

### A — Stateful hostile falsification

Commit:

```text
eeaa13d19dc94fb6453b6863ed9e6ac5a54f7438
```

Added `world-focus-substrate-final-falsification.test.ts` and pressure for:

```text
wrong-World late async attachment
same-generation cross-World races
unknown future World
revoked / ambiguous / retired identity
partial real effects after later invalidation
saved output + shared config conflict
offline / provider-lag / time uncertainty
consequential DANTE execution revalidation
5,000-candidate density with bounded composition
responsive semantic invariance
current / conflicted / retracted basis
```

The first CI exposed a stale UI test still using `expectedGeneration` after WS7 had closed `expectedWorkspace { worldId, generation }`.

### B — Contract regression repair

Commit:

```text
b7afb57feecd0d75cc0f6618de3835bed153d03f
```

Only the stale surface-layer test was aligned to the already accepted WS7 contract.

Frontend CI:

```text
33637869896 — PASS — attempt 1
```

No substrate runtime redesign was required.

### C — Independent mutation-kill / transition pressure

Commit:

```text
ea85733c708dc1f43c2e0d261ed6d9265febebe1
```

Added `world-focus-substrate-final-mutation.test.ts`.

It deliberately falsified outcomes such as:

```text
revoked disclosure -> allowed
purpose mismatch -> attach true
revoked saved output -> reuse true
ambiguous identity -> usable
ambiguous identity -> saved reuse true
shared config conflict -> transient
shared config conflict -> saved reuse true
partial real effect -> blocked/erased obligation
DANTE consequential proposal -> no execution revalidation
constrained/a11y -> semantic mutation
```

It also attacked wrong-World/stale-generation open/replace/promote sequences, generation semantics, blocking-tail behavior and hostile no-DANTE operation.

This cycle intentionally FAILED and found a real proof gap.

---

## 3. Real WS8 finding — CG-40 audit gap

The surviving mutant was:

```text
revoked / disclosure-invalid context
+
mutated canReuseSavedDerivedResult = true
```

The resolver already computed the correct result (`false`), but the auditor could not independently kill a falsified saved/cached reuse outcome.

This mattered because CG-40 requires recipient/purpose-bound non-interference for derived, cached, pinned and DANTE output — not only initial attachment.

Hardening commit:

```text
22fee0d610636be2f9a4abf9b0fe76c6fd5a74e4
```

The auditor now rejects any positive saved-derived reuse if any of these are invalid:

```text
basis != current
disclosure != allowed
identity != stable
config == concurrent-shared
```

The adversarial mutation test was not weakened or rewritten to obtain green.

No new Domain owner, World layer, primitive or generic root was required.

---

## 4. Post-last-gap independent confirmation

Commit:

```text
161caf5a4e9d90824edb56e30249ef079b4baf34
```

Added `world-focus-substrate-final-confirmation.test.ts`.

This confirmation was deliberately different from mutation-kill.

It re-ran all canonical WS7 vectors after the final CG-40 hardening:

```text
67 general vectors
4,455 / 4,455 3-way interactions

157 high-risk vectors
2,835 / 2,835 4-way interactions
```

and applied new metamorphic transformations:

```text
with-DANTE -> no-DANTE while preserving truth/disclosure/ref semantics
normal -> constrained/a11y while preserving substrate semantics
unknown future Worlds using the same reducer contract
independent invalidation of every saved-result reuse prerequisite
wrong-World expectation on unknown Worlds
```

Result:

```text
0 new material substrate classes
0 new primitive
0 new ownership layer
0 new generic escape hatch
0 page-per-World requirement
0 AI-only basic usefulness path
```

---

## 5. CI hygiene regression closed separately

The confirmation SHA's browser suite encountered a pre-existing intermittent Access keyboard test failure: the test pressed the first `Tab` immediately after navigation without first establishing that the interactive surface was ready.

This was not a World substrate failure and no Access production code was changed.

Commit:

```text
88db899391a3a41e23e76177d4896a657232b5eb
```

The test now waits for the sign-in heading, locale trigger and Google button to be visible/enabled before asserting the exact keyboard sequence.

It does **not** retry Tab, loop until focus appears, or weaken tab-order assertions.

The final CI on this SHA passed at the first attempt.

---

## 6. WS8 closure matrix

Final unresolved material findings:

```text
new work-semantic primitive                    0
new World substrate ownership layer           0
generic Entity/Thing/Fact/property root        0
page-per-World architecture requirement        0
AI-required basic World path                   0
Domain/Logical/Physical contradiction          0
privacy/disclosure/non-interference gap        0
state/race class requiring core redesign       0
responsive/a11y class requiring semantic redesign 0
new consequential-effect ownership class       0
unresolved mutation survivor                   0
```

Therefore:

> **WS8 — CLOSED.**

and the complete pre-materialization substrate program is now:

```text
WS0      CLOSED
WS1–WS5  CLOSED
WS6      CLOSED
WS7      CLOSED
WS8      CLOSED
```

---

## 7. What WS8 does not claim

WS8 does not prove:

```text
real backend/AuthZ enforcement
real PostgreSQL/Alembic World persistence
real provider/LLM correctness
real tool/effect execution
real distributed/offline synchronization
production visual quality
human visual acceptance
```

Those remain later work under their proper owners.

---

## 8. Strict reopen rule

WS0–WS8 do not reopen for a new World name, provider, API, model, renderer, viewport, config store or larger dataset.

Reopen only when concrete executable/production evidence demonstrates a real job that cannot be represented without:

```text
a new semantic/ownership/state family
a generic escape hatch
a privacy/non-interference violation
an unrepairable race/security failure in the existing owner
an accepted upstream Domain/Logical contradiction
a consequential effect that cannot fit existing revalidation/reconciliation ownership
```

The earliest necessary phase reopens; the whole program does not restart automatically.

---

## 9. Next gate

> **M0 — Materialization Mapping / Scope Freeze**

M0 must map the closed substrate to existing production code, required generalization, missing non-visual semantics, visual/shared renderers, specialist seams, DANTE seams and backend-deferred seams.

WS8 closure does not authorize M1–M7 or backend work by itself.
