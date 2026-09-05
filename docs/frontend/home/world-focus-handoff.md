# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 / M3 CLOSED — M4 ACTIVE / D2–D4 CLOSED / D5 NEXT  
**Date:** 2026-09-05  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff lets a new chat/agent continue without reconstructing the workstream from conversation history. Read repository live before every write.

Read first:

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
10. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by current checkpoint authority.

## 1. Current sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED / VALIDATED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0                                         ACCEPTED
D1                                         CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M3                                         CLOSED / VALIDATED
M3 final hostile closure                   CLOSED / PASS
M4 D2–D6                                   ACTIVE
D2 adaptive conversation surface           CLOSED / VALIDATED
D3 deterministic conversation adapter      CLOSED / VALIDATED
D4 contextual/deictic invocation           CLOSED / VALIDATED
D5 Insight presentation integration        NEXT / NOT STARTED
D6 Proposal/confirmation/receipt           BLOCKED BY D5
M5–M7                                      BLOCKED BY SEQUENCE
BACKEND                                    BLOCKED UNTIL M7
human/manual visual acceptance             NOT PERFORMED
```

## 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

Core thesis:

> **A World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, security boundary, AI memory bucket, chat room or mandatory Goal/KPI/time surface.

## 3. Permanent semantic barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend AuthZ
offline != source absent
timeout != semantic negative
Proposal != Decision != effect
provider ACK != canonical completion
Comparison != Decision
AI output != fact
client composition config != Domain state
presentation geometry != conversation identity
route presentation != automatically blocking interaction
context/selection != authorization
context reference != canonical truth
mounted frontend transcript != durable DANTE Run
cancelled/aborted request != semantic success
conversation message != Insight
Insight != Proposal != Decision != effect
```

## 4. Closed platform foundation

Workspace Platform remains the only planning/packing/transient-placement authority. M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. M3 owns revisioned client composition metadata, canonical draft transaction, meaningful opportunity extraction, candidate resolution, explicit Customize UX and normal live adaptive composition.

No later DANTE slice may bypass those owners for convenience.

## 5. D2–D3 retained result

D2:

```text
wide viable workspace -> non-modal DANTE sidecar
constrained/mobile -> route-owned DANTE focus
maximize/restore -> same conversation surface identity
```

D3:

```text
D1 composer
-> same dante:conversation
-> mounted transcript
-> typed request bound to World + Workspace generation + requestId
-> deterministic local reader
-> validated finite result or truthful unavailable/error/cancelled/superseded
```

Pending work is abortable/latest-only. Actual conversation close restores the exact original DANTE invoker.

Detailed authorities remain in the D2/D3 review files.

## 6. D4 closed result

D4 owns bounded **contextual/deictic invocation** only.

Canonical path:

```text
explicit semantic affordance
-> finite WorldFocusContextReferenceSet
-> same D1 composer
-> editable seeded prompt
-> World + Workspace generation validation
-> same D3 conversation
-> same context on valid follow-ups
```

Finite entry mapping:

```text
Continuity -> continue
Attention  -> why
Comparison -> compare
Evidence   -> open-source
```

Critical laws:

```text
global invoke remains contextReferences: null
Workspace selection != implicit DANTE context
context reference != authorization
context reference != canonical truth
reference exists != payload available/disclosable/fresh
arbitrary DOM/component state != conversation payload
stale contextual generation -> fail closed
Evidence source action != Provenance/Integrity/History
```

Stale before submit preserves the edited draft and keeps composer focus. A settled contextual session is superseded when Workspace generation changes; stale follow-up context is not silently reused.

D4 reuses D1 entry/composer, D2 presentation, D3 conversation, existing Workspace host/allocator and finite registry. No second DANTE state engine exists.

Closure evidence:

```text
PRE-SCOPE c6f5b7bcf5cdd3aa927a05668e5a146ba3ab5d1a
VALID RED 1cbcc27bf19c91e195dd1f0f4a5c57915facb432
CODE/TEST e8ab022b9b00b958235ac7d09e757b45227a4356
CI        33967719861 / run #1038 PASS
87 / 87 web test files
422 / 422 web unit tests
317 modules / 1021 dependencies / 0 architecture violations
```

Browser evidence uses the real `/worlds/music` Continuity flow at 1600 and 390, proves existing sidecar/route-focus handoff, target >=44px, no compact overflow, exact contextual focus return and automated axe checks.

Detailed authority: `world-focus-d4-contextual-invocation-review.md`.

## 7. D5 next read-only preflight

D5 owns Insight presentation integration and is **NOT STARTED**.

Before writes inspect live:

```text
D4 bounded contextual request/session boundary
D3 mounted transcript and typed result classes
existing finite registered World surfaces/renderers
existing semantic/basis/evidence owners capable of supporting an Insight
truth/reference/disclosure qualifiers
current responsive/a11y/browser harness
```

D5 must preserve:

```text
conversation message != Insight
assistant prose != validated Insight
Insight != canonical World/Domain truth
Insight != Proposal != Decision != effect
context reference != authorization
```

Then state exact PRE-SCOPE / CREATE / UPDATE / DELETE / RED-FIRST / OUT-OF-SCOPE gate. Do not pull D6 or backend/provider integration forward.

## 8. Visual strategy

```text
After M4: structural visual check only
M5: build contrasting complete Worlds
After M5: serious product/visual review
M6: visual polish + responsive + motion + a11y + performance
M7: frontend/backend seam freeze
```

## 9. Explicit out-of-scope

```text
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO localStorage fake persistence
NO durable server/cross-device persistence
NO Timeline/Access/Auth collateral work
NO GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO D6 hidden inside D5
NO arbitrary DOM/component payload serialization as DANTE context
NO generated route-tree edits without later explicit authority
NO history rewrite / force push
```

## 10. Human visual status

Automated browser coverage is green. Human/manual visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.
