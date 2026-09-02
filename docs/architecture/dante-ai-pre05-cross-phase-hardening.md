# DANTE PRE-AI05 — Cross-Phase Hardening Candidate

- **Status:** CANDIDATE / FIRST POST-MATERIALIZATION RETEST FAIL BOUNDED / FULL RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED / AI-04 CLOSED STRUCTURALLY
- **Implementation:** NONE
- **Provider/model selection:** OPEN
- **Database change:** NONE

This is a bounded supplement discovered by testing AI-01→AI-04 as one system. It does not reopen AI-02/03/04 wholesale and makes no implementation/provider PASS claim.

## 1. Refreshed 2026 evidence

Current product/engineering evidence supports five conclusions:

1. Background/event-triggered agents are mainstream, but work admission, permissions, approval and audit remain explicit (Notion Custom Agents, ChatGPT Scheduled Tasks).
2. Preview/staging before compound live effects is a strong pattern for consequential replanning (Reclaim 2.0).
3. Continuous replanning/proactive risk detection is valuable but creates interruption and self-trigger pressure that must be governed (Motion).
4. Modern agent security separates identity, least privilege, per-action authorization, human oversight, runtime loop/step/cost controls and autonomy rather than collapsing them (Microsoft 2026 guidance/research).
5. Multi-turn agent evals and privacy need trajectory-level evidence; recent OCELOT/GAAP/FIDES-style research shows cumulative disclosure can span steps and tasks. Formal IFC/leakage-budget mechanisms remain challengers, not automatic DANTE dependencies.

OWASP Agent Control Standard (2026-09-01) further supports inspectable runtime enforcement hooks. DANTE may later evaluate it as an adapter/control technology; it does not replace DANTE semantic owners or PEPs.

## 2. PRE05-H01 — AttentionBudget is separate

```text
ATTENTION BUDGET
!= RESOURCE BUDGET
!= COMMERCIAL QUOTA
!= PROVIDER QUOTA
```

`ResourceBudget` governs compute/model/tool/sandbox/external consumption.
`AttentionBudget` governs justified interruption/review/notification pressure.

Relevant inputs may include trigger provenance/currentness, materiality, urgency, consequence, quiet hours/current mode, recent interruptions, duplicate signals, expiry and causal lineage.

Attention outcomes are limited to publication/attention behavior:

```text
SILENT
DEFER / BATCH
REVIEW
NOTIFY
ESCALATE
```

Attention is not work/effect authorization. High-consequence policy may override ordinary interruption pressure; commercial tier alone may not.

## 3. PRE05-H02 — Trigger fired != work eligible

```text
TRIGGER FIRED
!= MATERIAL CHANGE
!= CURRENT WORK ELIGIBILITY
!= USER INTERRUPTION REQUIRED
```

A scheduled/event/monitoring callback is rechecked for authenticity, current source/material state, governing purpose, Actor/represented party, supersession/cancellation and material delta before it can initiate new work.

Potential proactive work enters ordinary Work Intake / WorkContract and current governance.

## 4. PRE05-H03 — Causal-loop / oscillation safety

DANTE effects can produce signals that trigger more DANTE work. Repetition without a new material external delta must not recurse indefinitely.

Possible controls include causal lineage, minimum material delta, hysteresis, cooldown, recent-effect awareness, duplicate/symmetric adaptation detection, bounded adaptation depth and stable-state detection.

```text
RECENT DANTE CAUSE
!= FOREVER IGNORE GENUINELY NEW EXTERNAL CHANGE
```

## 5. PRE05-H04 — DANTE-E14 is core

```text
DANTE-E14  PROACTIVITY / ATTENTION / CAUSAL-LOOP SAFETY
```

E14 is core because watches/reminders/adaptation/proactivity are already accepted product/runtime behavior.

Representative cases:

```text
meaningful external change → bounded proactive work and/or appropriate attention
no material change → no new work; silence where appropriate
repeated identical signal → dedupe/batch/silence
own effect causes equivalent signal → no oscillation
own effect + genuinely new external change → normal re-evaluation
quiet hours + nonurgent result → defer/silent
urgent material result → consequence-aware escalation
stale callback → no new work/effect
superseded watch/run → no current notification/effect
100 low-value signals → aggregate attention pressure
repeated dismissal → reduce interruption without laundering dismissal into canonical preference
attention silent + bounded work eligible → work may proceed only through normal admission
attention notify + effect ineligible → notification does not authorize effect
```

Useful evidence includes hard effect/privacy failures, oscillation count, missed required escalation, false/duplicate intervention rate, loop depth, unnecessary model/tool work and material-alert latency.

## 6. PRE05-H05 — Cumulative disclosure can outlive one Run

```text
SAFE SINGLE DISCLOSURE
!= SAFE CUMULATIVE DISCLOSURE
```

Individually eligible outputs may jointly reveal protected information. Relevant exposure may occur inside one Run or across related Runs/Interactions when the protected inference risk persists.

Where material, Publication/Egress policy may consume bounded prior-disclosure state keyed to the relevant recipient/purpose/scope/sink threat model.

```text
DISCLOSURE ACCOUNTING
!= DOMAIN Visibility
!= PERMANENT TRANSCRIPT LOG
```

If cross-Run survival is justified, retain the minimum sufficient policy/accounting state for the minimum justified lifetime and apply AI-03 purpose, retention, deletion/source-lifecycle and anti-resurrection rules.

Known/related sinks may be composed when the threat model requires. Arbitrary unknown external collusion is an explicit limit, not a fabricated guarantee.

Exact enforcement remains open: bounded rules/counters, structured ledger, IFC, posterior-leakage budgets or future mechanisms may compete.

## 7. PRE05-H06 — Recipient != surface != channel

Same recipient may receive different safe representations on:

```text
private DANTE screen
lock screen
shared display
voice
email/push
external AI client
```

The eval/publication contract therefore carries, where material:

```text
recipient
surface
channel / delivery context
prior disclosure state
```

Transport optimization never weakens Disclosure Projection or Result Maturity.

## 8. PRE05-H07 — Scoped autonomy is a policy ceiling

```text
AUTHORITY / AUTHZ
= may this operation legitimately occur now?

AUTONOMY POLICY
= may DANTE perform this otherwise eligible bounded work
  without fresh user intervention now?
```

Autonomy is not one global boolean and not model confidence.

Candidate bounded postures include:

```text
PROPOSE_ONLY
CONFIRM_EACH_TIME
AUTO_WITHIN_SCOPE
EXTERNAL_APPROVAL_REQUIRED
```

```text
AUTO_WITHIN_SCOPE
!= PERPETUAL AUTHORIZATION
!= BROADER AUTHORITY
```

## 9. PRE05-H08 — Safe-autonomy evaluation

Evaluate separately:

```text
unsafe under-asking
→ mandatory approval omitted
→ hard failure

excessive over-asking
→ safe bounded action repeatedly asks unnecessarily
→ quality/autonomy-efficiency failure unless stronger harm occurs
```

Possible metrics: unsafe autonomous action count, missed approval count, unnecessary approval/interruption rate, correct autonomous completion within scope and correct escalation rate.

Hard gates always precede autonomy optimization.

## 10. PRE05-H09 — Current-tree executable eval detail

AI-05 must not require Git archaeology to reconstruct the current eval contract. Current-tree workload coverage is therefore:

```text
E01 deterministic/model avoidance
E02 intent/reference/target resolution
E03 structured extraction
E04 native query/history/absence
E05 context/privacy/Reality Scope + cumulative disclosure
E06 planning/replanning/scenario
E07 document/long-context/multimodal
E08 tool/capability use
E09 consequential effect + scoped autonomy
E10 multi-actor/delegation/disclosure + recipient/surface/channel
E11 adaptive memory/learning
E12 currentness/failure/supersession/failover
E13 open-world research/grounding
E14 proactivity/Attention/causal-loop safety
```

Common fixture dimensions, where applicable:

```text
fixture/version
family
risk/consequence
locale
purpose
Actor / represented party / Subject
recipient / surface / channel
Reality Scope / Runtime Interpretation Frame
initial state/source refs
prior disclosure state / related-work disclosure basis
trigger provenance / causal lineage
attention state / user mode
scoped autonomy posture
provider/data eligibility
required capabilities / resource envelope
expected outcome / hard assertions / forbidden actions
grading profile / repetition profile
```

Hard failures explicitly include wrong target, unauthorized/autonomously over-permitted effect, private/cross-actor/surface/cumulative disclosure, fabricated truth, false effect/Actual, stale publication, Reality Scope laundering, invalid memory reuse/promotion, resurrection, approximate-as-complete, ineligible failover, instruction-authority laundering, current AuthZ/Consent/Visibility bypass, unbounded consequential oscillation, and treating Attention/publication as work/effect authorization.

## 11. PRE05-H10 — AI-01 ModelTarget terminology is historical

AI-01 research used an earlier shorthand that could collapse concrete provider/model/deployment into `ModelTarget`.

Current normative rule is AI-04:

```text
MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT
MODEL VENDOR != SERVING PLATFORM != PROTOCOL FAMILY
HARNESSPROFILE != PROVIDERBINDING
```

AI-01 remains research evidence, not current vocabulary authority.

## 12. PRE05-H11 — Whole-phase route composition wins

Any older AI-04B local reading such as:

```text
ModelTarget → Routing → HarnessProfile → ProviderBinding
```

is superseded by current whole-phase composition:

```text
WorkContract + consequence + current eligibility
→ ModelTarget / deterministic need
→ eligible qualified route compositions
→ Routing Policy
→ compatible HarnessProfile + ProviderBinding + feature/capability/control composition
→ route-specific admission
→ current egress authorization
```

`WP-03` governs.

## 13. PRE05-H12 — Old pre-Physical AI/context file is historical

`docs/architecture/ai-context-runtime-boundaries.md` remains useful pre-Physical evidence but its old `CURRENT — Phase 6` header is not current AI authority.

Current navigation must classify it as historical/superseded for runtime authority while preserving the file as evidence.

## 14. PRE05-H13 — Formal IFC/leakage-budget/ACS are challengers

Required now:

```text
DANTE semantic/privacy contract
trajectory/cross-work cumulative disclosure tests
bounded disclosure-accounting responsibility where material
```

Not selected now:

```text
formal IFC implementation
posterior/inference-leakage algorithm
specific ACS middleware
```

Any challenger must preserve DANTE Authority/Visibility/Consent/Reality/Source semantics and remain an implementation mechanism rather than semantic owner.

## 15. PRE05-H14 — Commercial tier cannot buy weaker safety

```text
HIGHER COMMERCIAL TIER
!= BROADER AUTHORITY
!= WEAKER PRIVACY
!= AUTOMATICALLY GREATER AUTONOMY
!= LICENSE TO INTERRUPT MORE OFTEN
```

A tier may grant more compute/concurrency/background work/context or features only inside current safety/privacy/autonomy/attention policy.

## 16. PRE05-H15 — AttentionDecision != proactive work admission

The first post-materialization retest found a real ambiguity in the original candidate: carrying `Attention → start work` literally could turn Attention into hidden execution authority.

Binding correction:

```text
ATTENTION DECISION
!= PROACTIVE WORK ADMISSION
!= EFFECT AUTHORIZATION
```

Correct composition:

```text
Trigger / Signal
→ authenticity/currentness/materiality
→ Work Intake / WorkContract when work may be justified
→ current autonomy + policy + provider/data + resource admission
→ optional bounded work

Result / Signal that may require user attention
→ AttentionPolicy / AttentionBudget
→ surface/disclosure checks
→ silent / defer / batch / review / notify / escalate
```

Background work may be permitted while publication stays silent; notification may be permitted while an effect remains forbidden.

## 17. PRE05-H16 — Cross-work/known-sink disclosure scope

The first post-materialization retest also found that `trajectory` could be read too narrowly as one Run.

```text
CUMULATIVE DISCLOSURE RISK
MAY SPAN RELATED RUNS / INTERACTIONS / SURFACES
AND KNOWN RELATED SINKS WHEN THE THREAT MODEL REQUIRES.
```

Any surviving disclosure-accounting state is minimized, purpose-bound, retention-bounded and lifecycle/anti-resurrection governed. No indefinite content log is implied.

## 18. Current composed responsibility path

```text
Trigger / Interaction
→ current trigger/work eligibility
→ WorkContract
→ Context / Retrieval / Memory
→ Basis / Reality / currentness
→ scoped autonomy + policy + resource/provider/data eligibility
→ deterministic need or eligible qualified model route composition
→ current egress authorization
→ Reason / Compute / Capability Runtime
→ Verifier
→ Effect governance / approval
→ verify / reconcile
→ Result Maturity
→ AttentionPolicy / AttentionBudget when attention is possible
→ recipient + surface + channel Disclosure Projection
→ cumulative disclosure check where material
→ Safe Publication / defer / batch / review / notify / escalate
```

Responsibility boundary != service/table.

## 19. Full retest corpus

The next retest restarts from zero and must cover at least:

```text
1 own-effect loop without new material delta
2 own-effect loop + genuine new external change
3 100 low-value signals under quiet hours
4 urgent material signal under high attention pressure
5 individually safe outputs jointly reveal protected information
6 protected inference reconstructed across separate Runs
7 same recipient across private/lock/shared/voice surfaces
8 known related sinks jointly reveal protected information
9 AUTO_WITHIN_SCOPE then Authority/AuthZ revoked
10 PROPOSE_ONLY despite available mutation capability
11 attention silent while bounded background work is eligible
12 attention notify while consequential work is ineligible
13 commercial quota exhausted during optional proactive work
14 quota exhausted after outcome-unknown effect
15 provider failover with context/capability contraction
16 provider continuation after policy/tool/Harness change
17 stale callback after supersession
18 memory/provider cache after deletion/revocation
19 auxiliary judge/router/verifier as governed recipient
20 model outage while deterministic route remains valid
```

PASS requires no unexplained responsibility gap, no new generic semantic owner and no hidden safety downgrade.

## 20. Non-claims / next action

```text
PRE-AI05 HARDENING MATERIALIZED      YES
FIRST RETEST                         FAIL BOUNDED / H15-H16
FULL RETEST AFTER H15-H16            NOT YET EXECUTED
PRE-AI05 PASS                        NO
AI-02/03/04 BROAD REOPEN             NO
PROVIDER/MODEL SELECTED              NO
DIRECT PROVIDER EVAL                 NO
IMPLEMENTATION                       NO
DB/ALEMBIC CHANGE                    NO
AI-05 STARTED                        NO
```

Next:

```text
READ BACK CURRENT TREE
→ restart full AI-01→AI-04 destructive retest
→ reverse-order retest
→ refreshed state-of-the-art regression check
```

Only after PASS may current navigation be reconciled and AI-05 become current.