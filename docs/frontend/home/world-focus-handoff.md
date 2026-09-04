# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — WS0–WS8 / M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read in order:

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-m2-shared-visual-primitives.md
4. world-focus-post-m1-safety-falsification-review.md
5. world-focus-m1-core-nonvisual-materialization-review.md
6. world-focus-m1-next-subblock.md
7. world-focus-m0-materialization-mapping.md
8. world-focus-contract-sequencing-supersession.md
9. world-focus-pre-m0-falsification-review.md
10. world-focus-post-ws8-hygiene-audit.md
11. world-focus-substrate-closure-plan.md
12. world-focus-ws8-final-falsification-review.md
13. world-focus-ws7-executable-harness-review.md
14. world-focus-ws6-universal-work-primitives.md
15. world-focus-ws6-primitive-pressure-matrix.md
16. world-focus-substrate-final-convergence-proof.md
17. world-focus-substrate-combinatorial-evidence.md
18. world-focus-frontend-roadmap.md
19. world-focus-evidence-index.md
20. product/platform/structure/geometry contracts as needed
```

Older `NEXT` or `ACTIVE` prose is phase-time evidence only unless adopted by a newer live authority.

---

# 1. Current status

```text
WF0 route/shell                         FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 visual treatment                 CANDIDATE
B0 foundation                          ENGINEERING CLOSED
WR0–WR2                                CLOSED
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS
Workspace Platform                     ENGINEERING CLOSED
D0 DANTE spatial/presence              ACCEPTED
D1 quiet invoke/composer               CLOSED FOR SEQUENCING
WS0–WS8                                CLOSED
POST-WS8 HYGIENE                       CLOSED / APPLIED
PRE-M0 FALSIFICATION                   CLOSED / PASS
M0 Materialization Mapping             CLOSED
M1 Core Non-Visual Materialization     CLOSED / VALIDATED
M1-1 identity/reference ownership      CLOSED / VALIDATED
M1-2 non-visual facets + seams         CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION           CLOSED / PASS
M2 shared visual primitive layer       CLOSED / VALIDATED
M2-1 shared presentation/L1 renderers  CLOSED / VALIDATED
M2-2 truthfulness/direct output        CLOSED / VALIDATED
M2 FINAL HOSTILE CLOSURE               CLOSED / PASS
M3 Adaptive World Composition          ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver       NEXT
M3-3 manual Customize UX               BLOCKED BY M3-2
M3-4 integrated adaptive composition   BLOCKED BY M3-3
M4–M7                                  BLOCKED BY SEQUENCE
BACKEND                                BLOCKED UNTIL M7
D2–D6                                  PRESERVED / DEFERRED TO M4
assistant manual visual review         NOT PERFORMED
```

Key executable evidence:

```text
WS8
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
CI   33639741630 PASS

PRE-M0 fix
HEAD 7c9feab50c6e2a04a9a3b1e36c92958362dba704
CI   33664655614 PASS

M0 closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 code
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 code
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final red
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety red
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2-1 validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS

M2-2 red
HEAD 5374f77d7cf7b52ef87ce64315a606bc1d96cf0b
CI   33787162755 EXPECTED FAILURE
exactly 8 unresolved presentation owners at Typecheck

M2-2 production baseline
HEAD b9856d497273d22face94fcd14f0deda853bbdb8
CI   33787905171 PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS

M2 final hostile red
HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011
CI   33790674375 EXPECTED FAILURE
hostile 4 / 5 PASS; web 331 PASS / 1 FAIL
sole defect: display copy not actually length bounded

M2 final hostile closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
hostile 5 / 5 PASS; web files 70 / 70; web units 332 / 332
279 modules / 770 dependencies / 0 architecture violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS

M3-1 red-first owner proof
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
frontend pre-production contracts PASS; Quality failed from unresolved M3-1 owner modules

M3-1 production validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
web test files 72 / 72; web unit tests 344 / 344
283 modules / 777 dependencies / 0 architecture violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

Later documentation synchronization is a separate evidence point and does not replace validated code heads above.

---

# 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World is a user-recognizable continuity context for a significant part of reality.

Core thesis:

> **World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, permission boundary, AI memory bucket, chat room, mandatory Goal/time/KPI surface or dashboard ontology.

---

# 3. Output Grammar and substrate

```text
O1 Orientation
O2 Situation
O3 Continuity / Resume
O4 Attention / Resolution
O5 Next
O6 Change
O7 Trajectory / Comparison
O8 Evidence / History
O9 Explore
O10 Act / Decide
O11 Intelligence
```

Output Grammar families are product questions, not automatically primitives/modules/renderers.

Closed/active layers:

```text
L0 Higher Authorities
L1 Work-Semantic Projections
L2 Evidence / Basis
L3 Coordination / Disclosure
L4 Interaction / Reference
L5 Composition Configuration        M3 ACTIVE
L6 Operation / Effect Presentation
L7 Renderer / Specialist Extension
L8 Platform / User Policies
```

Finite L1:

```text
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
```

L1 is optional; direct Domain/application projection may be correct.

---

# 4. Permanent non-collapses

```text
Person != Account != Principal != Actor
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Provenance != integrity attestation
Authority != Visibility
Agreement != Consent
Proposal != Decision != effect
provider state != canonical state
absence/unknown != false
idempotency != semantic identity
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
timeout != semantic negative
offline != source absent
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
```

No generic Entity/Thing/Relationship/Fact/property-bag root.

---

# 5. Retained executable proof

WS7:

```text
HEAD ca89e733893959af7dcc40fd0b8c8ba08e056ba4
CI   33633635890 PASS
67 fixed 3-way rows / 4,455 interactions
157 fixed high-risk 4-way rows / 2,835 interactions
```

WS8:

```text
stateful hostile pressure
mutation-kill
independent post-hardening confirmation
0 unresolved substrate gaps after final hardening
```

Pre-M0 discovered and fixed stale route-origin handoff resurrection without a new substrate owner.

M1 final hostile pressure found only the planned transitional cursor representation residue and closed it red-first.

The post-M1 safety gate found two implementation defects at existing boundaries: cancelled non-cooperative reads could reach validation, and O8 could retain caller evidence aliases. Both were fixed without reopening M1 or WS0–WS8.

M2-1 red-first proved the shared presentation layer had no pre-existing owner and closed the L1 renderer/display-binding foundation.

M2-2 red-first proved the remaining truthfulness/direct-output visual owners were absent. Production materialized them with no semantic-test weakening.

M2 final hostile pressure then found one remaining implementation gap at the existing display-binding boundary: display copy had no finite maximum. The hostile test stayed unchanged; the boundary was hardened and the full suite passed.

M3-1 red-first fixed the configuration/draft contract before implementation. The expected red run failed because the two new owner modules did not exist yet; production then passed the entire frontend CI without weakening the red tests.

---

# 6. Platform + M1 production substrate

Reuse remains:

```text
stable/adaptive/ephemeral composition
finite module/surface registries
12-unit planner
workspace generation
expected-workspace stale guard
surface open/replace/promote/close
blocking-tail barrier
full/split allocation
overlay/focus/inert semantics
ResizeObserver/container-query ownership
local failure isolation
latest-read coordination
boundary validation
safe external URL policy
```

M1 production materialization adds:

```text
neutral production World identity / descriptor
fixture identity separated from production identity
neutral bounded context references
canonical enumerable frozen cursor.contextReferences
selection compatibility projection of primary only
surface primary-only inheritance
reference-resolution presentation
freshness/as-of, validity, coverage, material retirement facets
evidence/provenance/integrity role-preserving metadata
sanitized disclosure outcome
effect lifecycle presentation + execution revalidation
sync/offline/replay/provider lag/request timing axes
O2/O5/O8 direct typed seams
WP-01..WP-04 production/application seams
World-scoped cancellable validated read mechanics
deterministic local adapters
unknown future World support at the non-visual seam
```

Post-M1 hardening strengthens existing ownership only:

```text
aborted read results are rejected before semantic validation
O8 evidence/history owns a normalized frozen evidence snapshot
```

Do not turn proof/oracle-only structures into production owners automatically.

---

# 7. M2 closed production presentation state

M2-1 owns:

```text
WorldFocusDisplayBinding
  exact semantic reference match
  display-safe label/supporting text
  no semantic key fallback

shared presentation grammar
  semantic section/heading
  textual finite state
  existing DANTE tokens
  container-query adaptation
  forced-colors support

finite work-semantic renderers
  WP-02 Attention
  WP-03 Comparison
  WP-04 Trajectory

real live vertical
  WP-01 Continuity
```

M2-2 extends the same grammar with:

```text
WorldFocusQualifier / QualifierGroup
WorldFocusPresentationSubsection

L2 truthfulness
  freshness
  validity
  coverage
  material retirement

L3
  sanitized disclosure

L6
  effect state
  execution revalidation kept separate

L8
  connectivity
  replay
  provider delivery
  request timing

O2 Situation renderer
O5 Next renderer
O8 Evidence / History renderer
```

O8 presentation preserves distinct accessible roles:

```text
Evidence
Provenance
Integrity / attestation
History
```

Continuity uses qualifier axes only for the degraded read states it already owned:

```text
partial -> coverage/incomplete
stale   -> freshness/stale
```

The final hostile closure added finite display-copy enforcement:

```text
label max          512
supportingText max 2048
blank/oversize     fail closed
silent truncation  forbidden
```

Presentation must not promote internal semantics:

```text
reasonCode != display explanation
reference key != display copy
available disclosure != AuthZ
stale != invalid
incomplete != empty
conflicted != winner
offline != content absent
timeout != semantic negative
partial-real != failed
reversed != compensated
execution revalidation != effect state
Comparison != winner/recommendation/Decision
Trajectory missing != zero
renderer != semantic owner
responsive adaptation != semantic rewrite
```

WP-02..WP-04 and O2/O5/O8 renderer capabilities are **not live composition claims**. Repository inspection at M2 closure confirms live core composition still mounts only Continuity.

---

# 8. DANTE disposition

D0 accepted:

> **AI availability is persistent; AI footprint is not.**

D1 global invoke remains `contextReference: null`; no implicit selection leakage.

D2–D6 remain deferred to M4.

DANTE is never truth, authorization, mandatory navigation or automatic effect completion.

M1's useful World path remains functional without DANTE.

Permanent cross-product capability rule added at M3-1:

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI product path where they are meaningful application functions.

For composition customization this means manual UI and future DANTE proposals share the same finite draft command language and the same Apply/revision guard.

---

# 9. M0 disposition audit after M2 closure

All mapped shared visual dispositions assigned to M2 have owners and final hostile evidence:

```text
M0-19 WP-02 shared rendering                  M2-1 DONE
M0-21 WP-03 shared rendering                  M2-1 DONE
M0-23 WP-04 shared rendering                  M2-1 DONE
M0-28 shared Evidence / History affordance    M2-2 DONE
M0-42 shared effect presentation              M2-2 DONE
M0-49 WP shared renderer family               M2-1 DONE
O2 Situation visual presentation              M2-2 DONE
O5 Next visual presentation                   M2-2 DONE
O8 Evidence / History visual presentation     M2-2 DONE
L2/L3/L6/L8 truthfulness presentation         M2-2 DONE
```

No generic M2-3 renderer family is justified.

---

# 10. M2 final hostile closure result

Red:

```text
HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011
CI   33790674375 EXPECTED FAILURE
hostile 4 / 5 PASS
web 331 PASS / 1 FAIL
```

The four immediate PASS cases proved cross-axis independence/non-leakage, unknown-future World O2/O5/O8 rendering, wrong-reference fail-closed binding and nominal-state quietness.

The sole red found unbounded display copy. Fix:

```text
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
hostile 5 / 5 PASS
web files 70 / 70
web units 332 / 332
architecture 279 modules / 770 dependencies / 0 violations
full Frontend CI Gate PASS
```

M2 is **CLOSED / VALIDATED**.

---

# 11. M3-1 validated composition configuration foundation

M0 remains the production-disposition authority in `world-focus-m0-materialization-mapping.md`.

M3-1 closes the client configuration/revision/draft foundation:

```text
WorldFocusCompositionConfig
  schemaVersion = 1
  revision
  worldId
  ordered entries[]

entry
  instanceId
  kind
  visibility: visible | hidden
  pinned: boolean
  prominenceOverride: lead | null
```

The config constructor reconstructs only allowed metadata. It does not retain canonical Domain payload, frontend AuthZ/disclosure authority, provider/runtime truth, executable renderer code or arbitrary property bags. Unknown future `kind` values remain representable.

Version disposition is explicit:

```text
current
migration-required
unsupported
```

No fake automatic migration or durable persistence is introduced.

Customization is a revision-bound draft:

```text
CURRENT CONFIG revision N
        ↓
DRAFT(baseRevision=N)
        ↓
pin / unpin / hide / show / move / promote / restore
        ↓
Apply | Cancel
```

`Apply` is the only transition that creates revision `N+1`. Stale revision returns `revision-conflict`; cross-World Apply fails closed; no implicit merge occurs. Cancel returns the base config without committed draft side effects.

The command source is finite:

```text
manual
dante-proposed
```

Both sources use the same command semantics. A DANTE proposal cannot bypass Apply/revision checks.

M3-1 does **not** touch live core composition and does not mount O2/O5/O8 or WP-02..04 merely because renderers exist.

---

# 12. M0 L5 disposition after M3-1

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 NEXT
M0-38 Customize Draft/Apply/Cancel + commands            M3-1 FOUNDATION CLOSED; UI M3-3
M0-39 client config revision/conflict/migration          M3-1 CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict     BACKEND-DEFERRED
```

M3-1 deliberately does not claim the manual Customize interaction UI as closed.

---

# 13. Current M3 handoff

M3 is **ACTIVE**. M3-1 is **CLOSED / VALIDATED**. M3-2 Adaptive Candidate Resolver is next but has not started.

Expected M3-2 path:

```text
meaningful available application projections
+ current user composition config
+ bounded product ranking inputs
        ↓
M3-2 candidate resolver
        ↓
WorldFocusCompositionCandidate[]
        ↓
existing resolveWorldFocusCompositionPlan()
        ↓
existing CompositionHost
```

Hard constraints:

```text
stable/pinned user intent cannot be silently overridden
sparse World remains sparse
renderer availability != mandatory mounting
no AI relevance score as sole authority
no universal confidence score
candidate resolver != AuthZ
ranking != semantic truth
```

M3-3 later materializes the manual Customize UX on the same M3-1 command language. M3-4 later integrates config + resolver + planner into live composition. Contextual DANTE D2–D6 remains M4.

---

# 14. Backend stop line

```text
NO World DB/Alembic
NO real World API merely for demos
NO real AuthZ/provider runtime
NO localStorage fake durable composition persistence
NO server persistence/cross-device sync
NO real model routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

---

# 15. Strict reopen policy

Do not restart WS0–WS8 or M1 for a new provider, World noun, renderer, viewport, AI model, config store or larger dataset.

Reopen only when later executable evidence shows a concrete semantic/ownership/state/security/privacy/effect contradiction that cannot fit an existing owner, and reopen only the earliest necessary phase.

M2-1 should reopen only for a contradiction in display-binding/shared-presentation ownership. M2-2 should reopen only for a contradiction in shared truthfulness/direct-output presentation semantics, not merely because M5 later earns a specialist renderer.

M3-1 should reopen only for a concrete contradiction in client composition config/revision/draft-command ownership, not because M3-2 ranking or M3-3 interaction needs additional behavior.

---

# 16. Repository discipline

Authority order:

```text
protected-main accepted executable/docs
current main authority
active bounded branch record for its scope
other current branch evidence
Git history
conversation
```

Every new write scope needs exact branch/PRE-SCOPE/path gate and live HEAD recheck. No merge/rebase/force/main mutation without explicit authorization.

Immediate continuation:

> **M3-2 is NEXT but unstarted. Start only with a fresh bounded M3-2 gate. M3-3, M4–M7 and backend remain blocked by sequence.**
