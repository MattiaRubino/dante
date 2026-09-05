# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 CLOSED / VALIDATED — M4 CONTEXTUAL DANTE ACTIVE / D2–D4 CLOSED / D5 NEXT  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Historical `NEXT`/`ACTIVE` prose is evidence only unless adopted here. Fresh live code inspection is required before every write scope.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-frontend-roadmap.md
3. world-focus-handoff.md
4. world-focus-evidence-index.md
5. current-checkpoint.md
6. world-focus-d4-contextual-invocation-review.md
7. world-focus-d3-deterministic-conversation-adapter-review.md
8. world-focus-d2-adaptive-conversation-surface-review.md
9. world-focus-m3-final-hostile-closure-review.md
10. world-focus-m3-adaptive-composition.md
11. world-focus-m3-4-integrated-adaptive-composition-review.md
12. world-focus-dante-spatial-presence-review.md
13. world-focus-d1-dante-entry-review.md
14. product/platform/structure/geometry contracts as needed
```

# 2. Live sequence

```text
WF0                                      FROZEN / USER AUTHORIZED
WF-G3                                    LOCKED / USER AUTHORIZED
WF-V4                                    CANDIDATE
B0 / WR0–WR2 / B1 / B2                  CLOSED AS RECORDED
Workspace Platform                       ENGINEERING CLOSED
D0                                       ACCEPTED
D1                                       CLOSED FOR SEQUENCING
WS0–WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0                                       CLOSED
M1                                       CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2                                       CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            CLOSED / VALIDATED
M3-1 composition configuration           CLOSED / VALIDATED
M3-2 adaptive candidate resolver         CLOSED / VALIDATED
PRE-M3-3 customization safety            CLOSED / PASS
M3-3 Manual Customize UX                 CLOSED / VALIDATED
M3-4 integrated adaptive composition     CLOSED / VALIDATED
M3 final hostile closure                 CLOSED / PASS
M4 Contextual DANTE / D2–D6             ACTIVE
D2 adaptive conversation surface         CLOSED / VALIDATED
D3 deterministic conversation adapter    CLOSED / VALIDATED
D4 contextual/deictic invocation         CLOSED / VALIDATED
D5 Insight presentation integration      NEXT / NOT STARTED
D6 Proposal/confirmation/receipt         BLOCKED BY D5
M5 complete contrasting Worlds           BLOCKED BY M4
M6 integrated product/visual/a11y/perf   BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
BACKEND                                  BLOCKED UNTIL M7
human/manual visual review               NOT PERFORMED
```

# 3. Permanent product / semantic law

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World is a shared coordinate system between user and DANTE, not a shared source of truth.

Permanent non-collapses:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
AI output != accepted fact
Possibility != Goal != Proposal != Decision
planned != actual
Actual != Observation != Outcome
Proposal != Decision != effect
provider ACK != canonical completion
cancel != reverse != compensation
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
adopt != semantic truth != authorization != persistence
renderer availability != mandatory mounting
presentation geometry != conversation identity
route presentation != automatically blocking interaction
selected UI/context != authorization
context reference != canonical truth
mounted frontend transcript != durable DANTE Run
cancelled/aborted request != successful semantic result
```

# 4. Closed D2–D4 result

D2 remains the one adaptive spatial conversation presentation over the existing Workspace stack:

```text
wide viable workspace -> non-modal DANTE conversation sidecar
constrained/mobile workspace -> route-owned focus below Global Topbar
explicit maximize/restore -> same dante:conversation identity
```

D3 remains the deterministic mounted pre-backend conversation bridge:

```text
D1 composer
-> explicit submit
-> same dante:conversation surface
-> typed World/generation/request-correlated request
-> deterministic local reader
-> validated finite answer | explanation
   OR truthful unavailable/error/cancelled/superseded
```

D4 adds bounded contextual/deictic entry into those same owners. It does not create a second composer, conversation, surface stack or context engine.

Live D4 path:

```text
explicit semantic affordance
  Continuity -> continue
  Attention  -> why
  Comparison -> compare
  Evidence   -> open-source
-> finite WorldFocusContextReferenceSet
-> same D1 composer with editable seeded prompt
-> World + Workspace-generation guard
-> same D3 conversation
-> same bounded references on valid follow-up turns
```

Global DANTE invocation remains explicitly context-free (`contextReferences: null`) even when Workspace selection exists. Selection/focus is never silently promoted to DANTE context.

Contextual generation changes fail closed:

```text
before composer submit
-> request not sent
-> draft preserved
-> truthful stale-context message

settled contextual conversation + generation change
-> contextual session superseded
-> stale follow-up rejected
```

Evidence is not collapsed into Provenance/Integrity/History: only true Evidence receives the D4 `open-source` affordance.

# 5. D4 closure evidence

```text
PRE-SCOPE  c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
VALID RED  1cbcc27bf19c91e195dd1f0f4a5c57915facb432
RED CI     33966295853 / run #1030 EXPECTED FAILURE
CODE/TEST  e8ab022b9b00b958235ac7d09e757b45227a4356
CI         33967719861 / run #1038 PASS
87 / 87 web test files
422 / 422 web unit tests
317 modules / 1021 dependencies / 0 architecture violations
Contracts / lint / typecheck / generated / build / diff / mutation PASS
Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

Valid RED reached unit execution with all static gates green and exactly two intended failures: missing explicit `contextReferences: null` in the D3 request and missing live Continuity contextual entry. The D1 no-implicit-selection guard remained green.

Final code/test compare from exact PRE-SCOPE is linear:

```text
status      ahead
ahead_by    9
behind_by   0
merge-base  == PRE-SCOPE
net paths   19 D4 code/test/i18n paths
```

No Workspace reducer/allocator, AppShell, Timeline, Access/Auth, generated route tree, backend/API/DB/Alembic/provider/LLM/persistence path changed.

Detailed evidence: `world-focus-d4-contextual-invocation-review.md`.

# 6. D5 next starting point

D5 owns **Insight presentation integration**, not contextual invocation and not Proposal/Decision/effect semantics.

Before writes, perform a fresh read-only preflight of:

```text
closed D4 contextual request/session boundary
closed D3 conversation transcript/result classes
existing World registered surface/rendering grammar
existing insight-like semantic/projection owners, if any
truth/disclosure/reference boundaries
responsive/a11y/browser harness
```

D5 must preserve:

```text
conversation message != Insight
assistant prose != validated Insight
Insight != canonical World/Domain truth
Insight != Proposal != Decision != effect
context reference != authorization
reference exists != payload available/disclosable/fresh
```

D5 remains pre-backend unless a later explicit authority changes sequencing.

# 7. Visual strategy agreed with user

```text
finish M4 -> structural visual check only
finish M5 -> serious product/visual review
M6 -> integrated visual/responsive/motion/a11y/performance refinement
M7 -> pre-backend frontend freeze
```

Do not spend D5–D6 on unrelated cosmetic redesign.

# 8. Stop lines

```text
NO D6 early materialization inside D5
NO second surface/workspace/conversation state engine
NO AppShell/GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO localStorage fake persistence
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO arbitrary DOM/component payload serialization as context
NO claim of human visual acceptance from CI
```

Automated browser green is not human visual acceptance. Human/manual visual review remains **NOT PERFORMED**.
