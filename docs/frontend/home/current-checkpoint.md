# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct current state from older phase labels or chat summaries.

## 1. Branch workstreams

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

## 2. Live World Focus state

```text
WF0 route/shell                         FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 visual treatment                 CANDIDATE
B0 foundation                          ENGINEERING CLOSED
WR0–WR2                                CLOSED
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS
Workspace Platform                     ENGINEERING CLOSED
D0 contextual DANTE spatial contract   ACCEPTED
D1 quiet invoke + compact composer      CLOSED FOR SEQUENCING
WS0–WS8                                CLOSED
POST-WS8 HYGIENE                       CLOSED / APPLIED
PRE-M0 FALSIFICATION                   CLOSED / PASS
M0 Materialization Mapping             CLOSED
M1 Core Non-Visual Materialization     CLOSED / VALIDATED
M1-1 identity/reference ownership      CLOSED / VALIDATED
M1-2 facets + WP/O2/O5/O8 seams        CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION           CLOSED / PASS
M2 Shared Visual Primitive Layer       CLOSED / VALIDATED
M2-1 shared presentation + L1 renderers CLOSED / VALIDATED
M2-2 truthfulness + direct output       CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION          CLOSED / PASS
M3 Adaptive World Composition           ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver        NEXT
M4–M7                                  BLOCKED BY SEQUENCE
D2–D6                                  DEFERRED TO M4
BACKEND                                BLOCKED UNTIL M7
assistant manual visual review         NOT PERFORMED
```

## 3. Current validated evidence

```text
M0 docs closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 production identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 non-visual production materialization
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final production falsification — red discovery
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE
1 failed / 288 passed — hidden cursor contextReferences representation only

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety falsification — red discovery
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL
7 / 9 hostile tests PASS; 296 PASS / 2 FAIL overall web units

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
9 / 9 hostile tests PASS; 56 / 56 web test files; 301 / 301 web unit tests

M2-1 shared visual primitive validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS
61 / 61 web test files; 312 / 312 web unit tests
262 modules / 684 dependencies / 0 architecture violations
Chromium pressure at 720 / 719 / 390 PASS
frozen Timeline Firefox PASS

M2-2 red-first owner proof
HEAD 5374f77d7cf7b52ef87ce64315a606bc1d96cf0b
CI   33787162755 EXPECTED FAILURE
Lint PASS; Typecheck FAIL on exactly 8 unresolved M2-2 presentation owners

M2-2 production fix baseline
HEAD b9856d497273d22face94fcd14f0deda853bbdb8
CI   33787905171 PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS

M2 final hostile falsification — red discovery
HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011
CI   33790674375 EXPECTED FAILURE
hostile tests 4 / 5 PASS; web units 331 PASS / 1 FAIL
sole finding: unbounded display-binding label/supporting copy

M2 final code closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
hostile tests 5 / 5 PASS; web test files 70 / 70; web unit tests 332 / 332
279 modules / 770 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS

M3-1 red-first owner proof
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
frontend pre-production contracts PASS; Quality failed from unresolved M3-1 owner modules

M3-1 composition configuration foundation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 architecture violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

## 4. M1 + safety closed result

M1 has production-grade non-visual ownership for:

```text
open-ended World identity + explicit descriptor
neutral bounded context-reference sets
canonical workspace/cursor context
reference resolution: usable / unresolved / retired
freshness/as-of
validity: current / superseded / retracted / unresolved
coverage: complete / incomplete / conflicted / unknown
material payload: present / retired with exact material-state reference
evidence / provenance / integrity-attestation as distinct bounded roles
sanitized disclosure: available / restricted / unavailable
effect presentation + execution revalidation
connectivity / replay / provider delivery / request timing
O2 Situation
O5 Next
O8 Evidence / History
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
World-scoped validated/cancellable read mechanics
deterministic pre-backend adapters
unknown-future World compatibility
basic useful path without DANTE
```

The final M1 falsification closed the hidden non-enumerable `cursor.contextReferences` compatibility residue.

The bounded post-M1 safety gate then found and closed two concrete implementation defects without introducing new semantic owners:

```text
cancelled non-cooperative World read
  -> late adapter completion is rejected before validation

O8 Evidence/History caller alias
  -> projection owns a normalized frozen evidence snapshot
```

The hostile safety test was not weakened. M1 and WS0–WS8 remain closed.

No universal `ProjectionEnvelope`, generic `Thing/Entity/Fact/PropertyBag`, frontend ACL/AuthZ, World canonical ownership or backend authority was introduced.

## 5. M2-1 validated result

M2-1 materializes a bounded shared visual language over M1 without acquiring semantic ownership:

```text
display-safe reference binding boundary
shared semantic section/state presentation grammar
WP-02 Attention renderer
WP-03 Comparison renderer
WP-04 Trajectory renderer
WP-01 Continuity migrated as the real production vertical
existing DANTE design tokens only
English/Italian finite presentation labels
container-query + forced-colors support
real-browser 720/719/390 pressure coverage
```

Critical scope truth:

```text
WP-01 Continuity is live and uses the M2 grammar
WP-02..WP-04 renderer contracts exist and are tested
WP-02..WP-04 are NOT injected into live composition merely as demonstrations
```

## 6. M2-2 validated result

M2-2 completes the mapped shared truthfulness/direct-output presentation owners over the same M2-1 grammar:

```text
shared qualifier grammar
L2 freshness / validity / coverage / material-retirement presentation
L3 sanitized disclosure presentation
L6 effect + execution-revalidation presentation
L8 connectivity / replay / provider-delivery / request-timing presentation
O2 Situation renderer
O5 Next renderer
O8 Evidence / History renderer with separate Evidence / Provenance / Integrity / History roles
accessible presentation subsections
Continuity partial -> coverage/incomplete qualifier
Continuity stale -> freshness/stale qualifier
English/Italian finite copy
```

Permanent visual non-collapses:

```text
stale != invalid
retracted != stale
incomplete != empty
conflicted != winner
retired payload != missing reference
available disclosure != frontend AuthZ
restricted != unavailable
offline != content absent
provider lag != stale
timeout != semantic negative
partial-real != failure
reversed != compensated
execution revalidation != effect state
Evidence != Provenance != integrity attestation
reasonCode != display copy
reference key != display copy
```

Nominal states remain quiet; M2-2 does not create badge soup. O2/O5/O8 and WP-02..04 remain **unmounted unless real application/composition evidence justifies them**.

## 7. M2 final closure result

The final hostile falsification attacked the combined M2-1/M2-2 layer rather than adding another renderer family.

Four of five hostile cases passed immediately:

```text
simultaneous degraded truthfulness axes remain orthogonal
unknown future World renders through O2/O5/O8 with order/role separation
wrong-reference display binding fails closed even with convincing copy
combined nominal basis/disclosure/sync state remains visually quiet
```

The only red finding was a real presentation-boundary gap: `WorldFocusDisplayBinding` accepted pathological 100,000-character label/supporting copy even though the boundary was defined as bounded. The fix remained under the existing M2 owner:

```text
label max           512 characters
supportingText max  2048 characters
blank or over-bound copy -> fail closed
no truncation
```

The hostile test was not weakened. Final CI proves 5/5 hostile PASS and full frontend green. The M0 disposition audit has no remaining known shared visual owner assigned to M2. Therefore M2 is closed without pulling M3 customization, DANTE D2–D6 or backend authority forward.

## 8. M3-1 validated result

M3-1 materializes client-side composition configuration ownership without ranking, live integration or persistence:

```text
WorldFocusCompositionConfig
  schemaVersion
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

The constructor reconstructs allowed fields only. Canonical Domain payload, AuthZ/disclosure authority, provider/runtime truth, executable renderer code and arbitrary property bags are not retained.

Version compatibility is explicit:

```text
current
migration-required
unsupported
```

Customization uses an isolated draft:

```text
CURRENT revision N
  ↓
DRAFT(baseRevision=N)
  ↓
pin / unpin / hide / show / move / promote / restore
  ↓
Apply | Cancel
```

Apply is the only transition that can produce revision `N+1`. A stale base returns `revision-conflict`; cross-World Apply fails closed; no implicit merge occurs. Cancel returns the base snapshot without committing draft state.

Permanent product rule encoded at this boundary:

```text
manual UI [M3-3] ----\
                       -> same finite commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful application functions. `dante-proposed` commands cannot bypass Apply/revision guards.

M3-1 explicitly does **not** implement candidate ranking, Customize UI, localStorage/server persistence, new live module mounting or DANTE runtime work.

## 9. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-m2-shared-visual-primitives.md
4. world-focus-post-m1-safety-falsification-review.md
5. world-focus-m1-core-nonvisual-materialization-review.md
6. world-focus-m1-next-subblock.md
7. world-focus-m0-materialization-mapping.md
8. world-focus-contract-sequencing-supersession.md
9. world-focus-frontend-roadmap.md
10. world-focus-handoff.md
11. world-focus-evidence-index.md
12. world-focus-substrate-closure-plan.md
13. product/platform/structure/geometry contracts as needed
```

## 10. Current gate — M3-2 next, not started

M3 is **ACTIVE**. M3-1 is **CLOSED / VALIDATED**. The next phase is M3-2 Adaptive Candidate Resolver.

M3-2 must derive bounded candidates from meaningful already-authorized application projections plus current composition config and feed the existing `resolveWorldFocusCompositionPlan()` rather than replacing it.

Permanent M3-2 constraints:

```text
stable/pinned user intent cannot be silently overridden
sparse World remains sparse
renderer availability != mandatory mounting
no AI relevance score as sole authority
no universal confidence score
candidate resolver != AuthZ
ranking != semantic truth
```

M3-2 remains unstarted until a fresh explicit write gate.

## 11. Permanent barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
derived output != disclosure permission
AI output != accepted fact
Proposal != Decision != effect
provider ACK != canonical completion
absence/unknown != false
Evidence != Provenance
Provenance != integrity attestation
Authority != Visibility
timeout != semantic negative
offline != source absent
retired reference != replacement reference
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
```

## 12. Backend stop line

```text
frontend view model != backend DTO != Domain model != persistence row
NO World DB/Alembic
NO real business API merely for frontend completeness
NO real AuthZ/provider runtime
NO localStorage fake durable config
NO real LLM routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

## 13. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before every new write scope;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not modify Access/Auth, frozen Timeline or AppShell as collateral work;
- generated route tree is never manually edited;
- fix CI root causes rather than weaken tests;
- human visual review is recorded only when actually performed.
