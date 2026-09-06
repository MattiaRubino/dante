# DANTE — World Focus Pre-M0 Falsification Review

**Status:** CLOSED — ADVERSARIAL GATE PASSED / M0 ENTRY CLEARED  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`

This review records the final executable gate run after WS8 closure and the subsequent post-WS8 hygiene work, immediately before entering M0 Materialization Mapping / Scope Freeze.

It is deliberately separate from WS8: the objective was not to reopen substrate convergence, but to attack the real post-cleanup production seams that M0 would otherwise inherit.

---

## 1. Gate baseline

Pre-test HEAD:

```text
75c4179682320850e2cddb31fa4a55e35b67a30e
```

That baseline already had a complete green Frontend CI:

```text
33660916088 — PASS
```

The branch at that point already contained the WS0–WS8 closure, post-WS8 hygiene, AppShell legacy Review removal and the final Stats -> Signals cleanup.

---

## 2. Adversarial method

A new executable test was added without changing production behavior:

```text
apps/web/src/features/world-focus/model/world-focus-pre-m0-falsification.test.ts
```

The test attacked the short-lived Home/Worlds -> World Focus route handoff rather than replaying the WS7/WS8 oracle corpus.

Pressure cases:

```text
1. stale opener must not resurrect after another World/source crosses the route boundary
2. stale opener must not resurrect after the same World is entered through a different source
3. clearing an older token must not erase a newer handoff
4. TTL expiry must remain terminal
5. non-finite / non-positive opener geometry must normalize safely
```

The test was intentionally written against the desired invariant before any runtime fix.

---

## 3. Red evidence — real bug discovered

Test-only discovery commit:

```text
798170e0c1ad12e0263364ab5c542a6ffe3d5e06
```

Workflow run:

```text
33664435710
```

The run reached Quality and produced an actual unit-test failure before being superseded/cancelled by the subsequent fix push.

Failure evidence:

```text
world-focus-pre-m0-falsification.test.ts
5 tests total
2 failed
3 passed

whole web test suite at failure:
2 failed
227 passed
```

The two failing cases were exactly the two stale-handoff resurrection attacks.

Existing behavior was:

```text
prime music/home
-> read with mismatched World or source
-> mismatch returned null
-> pending handoff remained alive
-> later music/home read within TTL could reuse the old opener
```

Therefore a route boundary could reject an entry for the current navigation yet leave it available to become falsely `live` again on a later navigation.

This was a real runtime-local lifecycle bug, not test noise.

---

## 4. Root-cause fix

Fix HEAD:

```text
7c9feab50c6e2a04a9a3b1e36c92958362dba704
```

Production change was limited to:

```text
apps/web/src/features/world-focus/model/world-focus-transition.ts
```

The mismatch rule is now terminal for that pending handoff:

```text
World/source mismatch
-> discard pendingEntry
-> return null
```

The adversarial test was not weakened or rewritten.

Preserved behavior:

```text
matching handoff remains readable
newer token supersedes older token
old-token clear cannot erase newer token
TTL expiry remains terminal
origin normalization remains bounded
handoff remains in-memory / non-durable / non-product state
```

---

## 5. Green evidence

Validation run on the unchanged adversarial test + runtime fix:

```text
Frontend CI 33664655614 — PASS
HEAD        7c9feab50c6e2a04a9a3b1e36c92958362dba704
```

Passed:

```text
Frontend contract drift
active Home formatting
lint
typecheck
architecture check
generated-source drift
unit tests
production build
diff check
repository mutation check
Mobile Bundle
Chromium Web E2E
Firefox frozen Timeline interaction contract
Frontend CI Gate
```

The five new pre-M0 falsification cases pass on the fix.

---

## 6. Classification

```text
new L1 primitive required                 NO
new substrate layer required              NO
WS0–WS8 reopen required                   NO
new Domain/Logical/Physical owner          NO
backend work required                      NO
M1 implementation required to repair bug   NO
```

Classification:

> runtime-local transient route-handoff lifecycle invariant, repaired in its existing UI transition owner.

This result strengthens the post-WS8 branch without changing closed substrate semantics.

---

## 7. Entry disposition

With the adversarial gate green:

```text
WS0–WS8                 CLOSED
POST-WS8 HYGIENE        CLOSED / APPLIED
PRE-M0 FALSIFICATION    CLOSED / PASS
M0                      CLEARED TO START
M1–M7                   STILL BLOCKED
BACKEND                  STILL BLOCKED
```

The next phase is M0 only:

> **Materialization Mapping / Scope Freeze**

M0 may map and freeze production dispositions. It must not silently implement M1, D2–D6 or backend/API/DB/AuthZ/provider/LLM/effect work.
