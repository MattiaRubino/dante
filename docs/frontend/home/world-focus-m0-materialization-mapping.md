# DANTE — World Focus M0 Materialization Mapping / Scope Freeze

**Status:** M0 CLOSED — COMPLETE PRODUCTION-DISPOSITION MAP / M1 NEXT  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`

M0 maps the closed WS0–WS8 substrate and the post-closure executable evidence onto the real current frontend implementation. It does not create a second architecture and does not promote proof/oracle code into production merely because it exists.

Primary inputs:

```text
world-focus-product-contract.md
world-focus-platform-contract.md
world-focus-ws6-universal-work-primitives.md
world-focus-ws7-executable-harness-review.md
world-focus-ws8-final-falsification-review.md
world-focus-post-ws8-hygiene-audit.md
world-focus-pre-m0-falsification-review.md
current apps/web/src/features/world-focus/{model,application,ui}
```

---

# 1. Disposition vocabulary

```text
A — ALREADY SATISFIED
B — BOUNDED GENERALIZATION
C — MISSING MODEL / APPLICATION PRODUCTION CODE
D — MISSING SHARED RENDERER
E — SPECIALIST EXTENSION
F — DANTE SEAM
G — BACKEND-DEFERRED AUTHORITY
```

No row may resolve to a generic `Thing`, arbitrary property bag, remote executable UI, World-owned ACL, World-owned canonical truth or page-per-World implementation.

---

# 2. Core host / foundation map

| ID | Requirement | Current reality | Disposition | Stage / freeze decision |
| --- | --- | --- | --- | --- |
| M0-01 | route-owned World lifecycle, entry/return, focus | `WorldFocusPage` + transient handoff + focus restoration are production code | **A** | preserve |
| M0-02 | WF0/WF-G3 shell + geometry | frozen shell/workspace + geometry constants implemented/tested | **A** | preserve |
| M0-03 | World identity/purpose renderer | `WorldFocusContext` is correct owner but consumes fixed fixture/i18n identity | **B** | M1 descriptor generalization |
| M0-04 | shell loading/error/unavailable | `WorldFocusWorkspace` owns truthful shell states | **A** | preserve |
| M0-05 | runtime boundary validation | validator-neutral boundary exists | **A** | reuse |
| M0-06 | latest-read race/cancellation | latest-read coordinator prevents obsolete commit | **A** | reuse |
| M0-07 | safe external URL policy | HTTPS-only credential-free parser exists | **A** | preserve |
| M0-08 | open-to-usable instrumentation | vendor-neutral User Timing span exists | **A** | M6 may add measured budgets |
| M0-09 | open-ended frontend World identity | current `WorldFocusId` is the fixed ten-fixture union | **B** | M1 separates opaque production identity/descriptor from fixtures |
| M0-10 | fixture catalog | explicitly synthetic/pre-backend | **A** | retain as deterministic adapter/test data only |

M1 must not make `body/music/travel/study/finance/relationships/work/growth/routine/projects` the permanent World taxonomy. M5 must be able to pressure an unknown future World without branch-per-World code.

---

# 3. Reference ownership map

| ID | Requirement | Current reality | Disposition | Stage |
| --- | --- | --- | --- | --- |
| M0-11 | generic bounded context reference | type currently declared inside workspace but reused by WP/oracle | **B** | M1 extracts neutral model ownership |
| M0-12 | primary + bounded ordered supporting refs | proved in WS7; production workspace only has `selection` | **B** | M1 generalizes cursor/selection |
| M0-13 | surface-bound reference | descriptor already carries bounded reference + generation | **A** | preserve |
| M0-14 | World + generation stale guard | `expectedWorkspace` + keyed workspace owner exist | **A** | preserve |
| M0-15 | ambiguity/retire/merge/split safe presentation state | proof exists; production application state missing | **C** | M1 narrow state vocabulary |
| M0-16 | authoritative ref resolution | frontend must not decide canonical retarget truth | **G** | later authority |

References remain identity/hints only, never copied canonical payload.

---

# 4. L1 work primitives

| ID | Primitive | Current reality | Disposition | Stage |
| --- | --- | --- | --- | --- |
| M0-17 | WP-01 Continuity | constructor exists; B2 real reader/validator/renderer uses narrower pre-M0 projection | **B** | M1 align production semantics without regressing B2 |
| M0-18 | WP-02 Attention | constructor exists; application seam absent | **C** | M1 |
| M0-19 | WP-02 shared rendering | absent | **D** | M2 |
| M0-20 | WP-03 Comparison | constructor exists; application seam absent | **C** | M1 |
| M0-21 | WP-03 shared rendering | absent | **D** | M2 |
| M0-22 | WP-04 Trajectory | constructor exists; application seam absent | **C** | M1 |
| M0-23 | WP-04 shared rendering | absent | **D** | M2 |

```text
primitive != module
primitive != card
primitive != canonical source
primitive != mandatory first-open content
```

A World may use zero L1 primitives.

---

# 5. Output Grammar O1–O11

```text
O1  Orientation             existing renderer + M1 descriptor generalization
O2  Situation               M1 typed direct projection seams; no universal Situation entity
O3  Continuity / Resume     M1 align WP-01 production model
O4  Attention / Resolution  M1 WP-02/application; M2 renderer; resolution remains proper owner
O5  Next                    M1 typed application query/projection; no universal Next entity
O6  Change                  M1 WP-03; M2 renderer
O7  Trajectory/Comparison   M1 WP-03/WP-04; M2 rendering
O8  Evidence / History      M1 safe basis/evidence projection; M2 affordance; authority later
O9  Explore                 existing L4/L7 mechanics; specialist extension when earned
O10 Act / Decide            M1 presentation vocabulary; M4 DANTE seam; backend effect authority
O11 Intelligence            M4
```

All eleven families are assigned. No fifth L1 primitive is required.

---

# 6. L2 — Evidence / Basis

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-24 | resource lifecycle vocabulary | **A** | preserve |
| M0-25 | freshness/as-of/material basis frontend semantics | **B** | M1 narrow reusable metadata |
| M0-26 | conflict/incomplete/superseded/retracted/redacted/tombstoned safe disposition | **C** | M1 |
| M0-27 | evidence/provenance/integrity/attestation presentation metadata | **C** | M1 only where real projections need it |
| M0-28 | shared evidence/history affordance | **D** | M2 |
| M0-29 | specialist evidence renderer | **E** | M5/real vertical |
| M0-30 | authoritative history/provenance/source validity | **G** | later authority |

Do not create a giant universal projection envelope carrying every L2–L6 field. Use narrow shared facets plus module-specific projections.

---

# 7. L3 — Coordination / Disclosure

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-31 | sanitized safe frontend result after disclosure filtering | **C** | M1 safe `available/restricted/unavailable` outcomes |
| M0-32 | recipient/purpose authorization + revocation authority | **G** | backend/AuthZ/Context Builder authority |
| M0-33 | Agreement/Consent/Delegation/Acceptance material semantics | **G** | consume typed higher-authority projections later |
| M0-34 | derived-output non-interference after revocation/purpose change | **F** | M4 result binding + later authority |

---

# 8. L4 — Interaction / Reference

Existing production assets are retained:

```text
workspace generation
expectedWorkspace stale guard
surface context reference
interaction cursor
peek / insight / explore depth
inline / popover / sidecar / modal / full-screen / route
blocking-tail rules
World-switch remount
```

Only M0-11/M0-12/M0-15 require M1 materialization.

---

# 9. L5 — Composition Configuration

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-35 | stability/origin semantics | **A** | preserve |
| M0-36 | prominence/footprint/grid planner | **A** | preserve |
| M0-37 | production candidate resolver from meaningful projections | **C** | M3 |
| M0-38 | Customize Draft -> Apply/Cancel, pin/hide/reorder/promote | **C** | M3 |
| M0-39 | client config revision/conflict/migration representation | **C** | M3 |
| M0-40 | durable config persistence/cross-device sync/conflict authority | **G** | backend |

---

# 10. L6 — Operation / Effect Presentation

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-41 | frontend effect lifecycle vocabulary/presentation contract | **C** | M1 non-visual model only |
| M0-42 | shared pending/ambiguous/partial/reversal/receipt presentation | **D** | M2 |
| M0-43 | DANTE Proposal/confirmation/receipt | **F** | M4 D5/D6 |
| M0-44 | execution-time AuthZ/freshness revalidation | **G** | backend governed operation |
| M0-45 | execute/cancel/reverse/refund/compensate/reconcile | **G** | backend/effect architecture |

```text
cancel != reverse
provider ACK != canonical completion
partial real effect cannot be erased by UI state
```

---

# 11. L7 — Renderer / Specialist Extension

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-46 | finite module registry | **A** | preserve |
| M0-47 | finite surface registry | **A** | preserve |
| M0-48 | local render failure isolation | **A** | preserve |
| M0-49 | WP shared renderer family | **D** | M2 |
| M0-50 | specialist map/media/high-density/technical renderers | **E** | M5/real vertical |

Remote/model-generated executable UI remains forbidden.

---

# 12. L8 — Platform / User Policies

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-51 | responsive workspace allocation | **A** | preserve |
| M0-52 | keyboard/focus/Escape/inert/reduced-motion foundation | **A** | preserve; M6 integrated review |
| M0-53 | local failure isolation | **A** | preserve |
| M0-54 | offline/replay/lag presentation semantics | **C** | M1 narrow frontend representation |
| M0-55 | authoritative sync/replay/conflict | **G** | backend |
| M0-56 | large-data bounding/downsampling/special visualization | **E** | M5/M6 |
| M0-57 | integrated performance budgets | **B** | M6 |

---

# 13. DANTE map

| ID | Requirement | Disposition | Stage |
| --- | --- | --- | --- |
| M0-58 | D0/P0 quiet presence | **A** | preserve |
| M0-59 | D1/P1 compact composer | **A** | preserve |
| M0-60 | D2 ongoing conversation surface | **F** | M4 |
| M0-61 | D3 deterministic pre-backend conversation adapter | **F** | M4 |
| M0-62 | D4 explicit contextual/deictic invocation | **F** | M4 consuming M1 refs |
| M0-63 | D5 Insight | **F** | M4 |
| M0-64 | D6 Proposal/confirmation/receipt | **F** | M4 |
| M0-65 | authoritative Context Builder / recipient-purpose filtering | **G** | backend Intelligence boundary |
| M0-66 | durable Runs/model routing/streaming/tools/effects | **G** | backend Intelligence vertical |

Basic World usefulness must remain possible with DANTE unavailable.

---

# 14. M1 scope freeze

M1 is strictly **Core Non-Visual Production Materialization**.

## M1 MUST do

```text
1. decouple production World identity/descriptor from fixed fixture IDs
2. extract neutral context-reference ownership from workspace
3. materialize primary + bounded ordered supporting references
4. connect WP-01..WP-04 to production application seams
5. add narrow basis/freshness/validity/reference-resolution/disclosure/offline/effect-presentation facets
6. add direct typed application seams needed for O2 Situation / O5 Next / O8 Evidence
7. retain deterministic pre-backend adapters and aggressive tests
```

## M1 MUST NOT do

```text
shared Attention/Comparison/Trajectory visual renderers       -> M2
visual skin/polish                                             -> M2/M6
dynamic ranking/composition resolver                           -> M3
pin/hide/reorder/customization                                 -> M3
config persistence/sync                                        -> backend
D2–D6                                                          -> M4
complete Music/Travel/Finance/etc Worlds                       -> M5
human integrated visual acceptance                             -> M6
backend/API/DB/Alembic/AuthZ/provider/LLM/tools/effects         -> after M7
```

---

# 15. M2–M7 assignment freeze

```text
M2 Shared Visual Primitive Layer
M3 Adaptive World Composition
M4 Contextual DANTE
M5 Contrasting Complete Worlds
M6 Integrated Product / Visual / Accessibility / Performance Review
M7 Pre-Backend Frontend Freeze
```

M4 preserves D0/D1 and resumes D2–D6. Backend opens only after M7.

---

# 16. Adversarial pressure

Rejected mutations:

```text
proof/oracle promoted to runtime authority                 REJECTED
giant generic projection envelope/property bag            REJECTED
frontend World relevance/cursor used as AuthZ              REJECTED
ten fixture IDs promoted to permanent World taxonomy       REJECTED
AI required for useful first-open                          REJECTED
M3 customization pulled into M1                            REJECTED
M2 renderer built before M1 semantics                      REJECTED
backend/API/DB/LLM/effects pulled forward for realism      REJECTED
```

Coverage:

```text
L0–L8              covered
WP-01..WP-04       covered
O1–O11             covered
D0–D6              covered
config             covered
reference identity covered
effect lifecycle   covered
privacy/disclosure covered
responsive/a11y    covered
offline/sync       covered
unknown World      covered
large data         covered
```

Unowned material rows: **0**.

---

# 17. Sequencing authority cleanup

`world-focus-product-contract.md` and `world-focus-platform-contract.md` retain authoritative semantic/product/platform invariants, but their historical paragraphs that call the contextual DANTE spatial review the current/next gate predate D0/D1 and WS closure.

Those historical phase-order statements are explicitly superseded by:

```text
world-focus-current-checkpoint.md
world-focus-m0-materialization-mapping.md
world-focus-frontend-roadmap.md
```

They must not be used to move D2 ahead of M1–M3. This supersession changes sequencing only, not their semantic contracts.

---

# 18. Closure matrix

```text
closed substrate primitives classified       4 / 4
layers classified                            L0–L8
Output Grammar classified                    O1–O11
DANTE stages classified                      D0–D6
backend authority pulled forward             0
generic semantic roots introduced            0
page-per-World architecture introduced        0
AI-required basic path introduced             0
unowned material rows                         0
```

No M0 evidence requires reopening WS0–WS8.

---

# 19. Final disposition

```text
WS0–WS8                 CLOSED
POST-WS8 HYGIENE        CLOSED
PRE-M0 FALSIFICATION    CLOSED / PASS
M0                      CLOSED
M1                      NEXT ACTIVE GATE — NOT STARTED BY THIS DOCUMENT
M2–M7                   BLOCKED BY SEQUENCE
D2–D6                   DEFERRED TO M4
BACKEND                  BLOCKED UNTIL M7
```

Immediate continuation:

> **M1 — Core Non-Visual Production Materialization**

M1 begins only under a fresh write gate derived from section 14.
