# DANTE — World Focus D5 Insight Presentation Integration Review

**Status:** D5 CLOSED / VALIDATED  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`  
**PRE-SCOPE:** `62b52137ab30778aae968f80fac59496c87171bf`  
**Final code/test HEAD:** `0873153d8b390b99c5b3aa024e0735c82a89660d`

## 1. Closure statement

D5 is closed as a pre-backend frontend materialization of a standalone DANTE Insight presentation. It does not turn assistant prose into truth, does not widen D3 conversation result classes, does not create a second Workspace/surface engine, and does not pull D6 Proposal/Decision/effect semantics forward.

Permanent D5 law now executable:

```text
conversation message != Insight
assistant prose != validated Insight
Insight != canonical World/Domain truth
Insight != Proposal != Decision != effect
context reference != authorization
reference exists != payload available != disclosable != fresh
```

## 2. Materialized path

```text
explicit D4 contextual invocation
-> same D1 composer
-> same D3 conversation
-> validated answer | explanation
-> explicit user action: Open as Insight
-> D5 request correlated by World + Workspace generation + source message
-> deterministic pre-backend Insight reader
-> validated finite Insight artifact
-> finite registered dante-insight surface
```

The D3 conversation contract remains finite `answer | explanation`; `insight` was not added as a conversation result class.

The D5 Insight artifact is separately validated and carries:

```text
schemaVersion
insightId
worldId
workspaceGeneration
kind: observation | pattern | change
title
summary
basisReferences
```

The adapter cannot widen the reference basis. `basisReferences` are reconstructed from the exact bounded D4 request context; adapter-owned or forged basis fields fail boundary validation.

## 3. Presentation behavior

D5 reuses the existing Workspace/surface stack and finite core surface registry.

```text
wide viable conversation geometry
-> standalone dante-insight sidecar

constrained/mobile route-focus conversation geometry
-> standalone route-owned dante-insight
-> blocks Workspace interaction through the existing barrier
```

D5 does not modify the Workspace reducer or allocator.

The conversation remains mounted as a distinct semantic object. Closing Insight returns to the conversation and restores the current logical `Open as Insight` invoker identified by the exact source message id; DOM node identity itself is not treated as product state.

## 4. Truth / privacy boundary

The surface presents the validated local artifact and a bounded reference count, not raw context-reference keys. The UI explicitly states that the artifact is pre-backend, not an accepted fact, and does not imply authorization.

Global DANTE invocation remains context-free and does not offer Insight promotion without explicit contextual references.

A Workspace-generation change supersedes pending Insight work; a late result cannot attach after the context generation has changed.

## 5. RED evidence

```text
PRE-SCOPE  62b52137ab30778aae968f80fac59496c87171bf
VALID RED  c803dac135c7a35d38d8eb8335f5b52c8b430114
RED CI     33969625586 / run #1045 EXPECTED FAILURE
```

The RED reached unit execution with contracts, lint, typecheck, architecture and generated checks green. Existing tests remained green and the one new intended failure proved that the shipped finite registry did not yet contain `dante-insight`.

## 6. Production and hostile hardening evidence

Primary production slice:

```text
0d56f0dcb7267214332cc613f9c40e76368143d3  feat(home): materialize D5 standalone Insight
```

The first production run exposed only lint-mechanical issues; those were corrected without weakening the RED or changing the D5 semantic boundary. CI #1048 on `bb8d258a2315098893102ea84e96c2eb4084e3ba` then passed fully.

D5 hostile hardening added pressure for:

```text
wide standalone sidecar
390px route-owned blocking presentation
no horizontal overflow
Axe wide + compact
no raw bounded reference-key disclosure
logical invoker focus restoration
no Insight from global/context-free DANTE
pending result superseded by Workspace generation change
late result cannot attach
```

The first hardening run found one test assertion that incorrectly required the same DOM node object after a renderer remount. Product behavior already restored the exact logical source-message invoker and Chromium focus behavior was green. The test was corrected to assert the product law: same logical message id + current node focused. No production code was changed for that assertion.

Final validation:

```text
CODE/TEST  0873153d8b390b99c5b3aa024e0735c82a89660d
CI         33971615312 / run #1050 PASS
89 / 89 web test files
431 / 431 web unit tests
324 modules / 1066 dependencies / 0 architecture violations
frontend pre-production contracts PASS
World Focus pre-production contracts PASS
lint PASS
typecheck PASS
generated-source drift PASS
production build PASS
diff check PASS
repository mutation check PASS
Mobile Bundle PASS
Chromium Web E2E PASS
frozen Timeline Firefox PASS
Frontend CI Gate PASS
```

## 7. Scope compare

Exact PRE-SCOPE -> final code/test HEAD:

```text
status      ahead
ahead_by    7
behind_by   0
merge-base  == PRE-SCOPE
```

Net changed paths are limited to D5 application/runtime/tests, DANTE Insight/conversation/page wiring, finite core surface registration and IT/EN i18n. The apparently large i18n deletion counts were inspected: prior D1-D4 keys remain intact; the delta is formatting compaction plus the new `dante.insight` resource block.

No Workspace reducer/allocator, AppShell, Timeline, Access/Auth, generated route tree, backend/API/DB/Alembic/AuthZ/provider/LLM/persistence path changed.

## 8. Explicit exclusions

```text
NO D6 Proposal/confirmation/receipt materialization
NO real governed effect
NO provider/LLM call
NO backend/API/DB/Alembic/AuthZ integration
NO durable Insight persistence
NO acceptance of Insight as canonical fact
NO arbitrary DOM serialization as DANTE context
NO second surface/workspace engine
```

## 9. Visual status

Automated responsive/a11y/browser validation is green. This is not human visual acceptance.

**human/manual visual review: NOT PERFORMED**

## 10. Sequencing result

D5 is **CLOSED / VALIDATED**. D6 — Proposal / confirmation / receipt — is now the only next M4 materialization block. M5 remains blocked until M4 closes.
