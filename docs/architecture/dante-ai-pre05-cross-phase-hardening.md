# DANTE PRE-AI05 — Cross-Phase Hardening Candidate

- **Status:** CANDIDATE / SECOND FULL RETEST FAIL BOUNDED / FRESH RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **Upstream:** AI-02.1 CLOSED / AI-03 CLOSED / AI-04 CLOSED STRUCTURALLY
- **Implementation:** NONE
- **Provider/model selection:** OPEN
- **Database change:** NONE
- **Retest history:** initial whole-chain audit → H01..H14; first post-write retest → H15..H16; second full retest → H17..H18

This is a bounded supplement discovered by repeatedly testing AI-01→AI-04 as one system. It does not reopen AI-02/03/04 wholesale and makes no implementation/provider PASS claim.

## 1. Refreshed 2026 evidence

Current product/engineering evidence supports these durable conclusions:

- background/event-triggered agents are mainstream, but work admission, permissions, approval and activity evidence remain explicit;
- preview/staging before compound live effects is a strong consequential-change pattern;
- continuous replanning/proactivity creates attention and self-trigger pressure that needs runtime control;
- agent security separates identity, least privilege, current per-action authorization, human oversight, runtime loop/step/cost limits and autonomy;
- multi-turn agent evaluation needs task/trial/trajectory/outcome evidence and repeated reliability;
- recent privacy research shows disclosure risk can accumulate across steps, tasks and known related sinks;
- portable agent-control standards are useful challengers/adapters but must not replace DANTE semantics.

Formal IFC, posterior-leakage budgets and ACS-style middleware remain implementation challengers, not baseline dependencies.

## 2. PRE05-H01 — AttentionBudget is separate

```text
ATTENTION BUDGET
!= RESOURCE BUDGET
!= COMMERCIAL QUOTA
!= PROVIDER QUOTA
```

ResourceBudget governs compute/model/tool/sandbox/external consumption. AttentionBudget governs justified interruption/review/notification pressure.

Relevant inputs may include trigger provenance/currentness, materiality, urgency, consequence, user mode/quiet hours, recent interruptions, duplicates, expiry and causal lineage.

Attention outcomes are limited to attention/publication behavior:

```text
SILENT
DEFER / BATCH
REVIEW
NOTIFY
ESCALATE
```

Attention is not work/effect authorization. Commercial tier alone may not weaken attention policy.

## 3. PRE05-H02 — Trigger fired != work eligible

```text
TRIGGER FIRED
!= MATERIAL CHANGE
!= CURRENT WORK ELIGIBILITY
!= USER INTERRUPTION REQUIRED
```

A scheduled/event/monitoring callback is rechecked for authenticity, governing purpose, current Actor/represented party, source/material state, supersession/cancellation and material delta before it can initiate new work.

Potential proactive work enters ordinary Work Intake / WorkContract and current governance.

## 4. PRE05-H03 — Causal-loop / oscillation safety

DANTE effects can create signals that trigger more DANTE work. Repetition without a new material external delta must not recurse indefinitely.

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

Representative cases include meaningful vs immaterial change, duplicate signals, own-effect loops, quiet-hours deferral, urgent escalation, stale callbacks, superseded watches, attention storms, repeated dismissal, silent attention with otherwise eligible background work, and notification with an ineligible effect.

Useful evidence includes hard effect/privacy failures, oscillation count, missed escalation, false/duplicate intervention rate, loop depth, unnecessary model/tool work and material-alert latency.

## 6. PRE05-H05 — Cumulative disclosure can outlive one Run

```text
SAFE SINGLE DISCLOSURE
!= SAFE CUMULATIVE DISCLOSURE
```

Individually eligible outputs may jointly reveal protected information. Relevant exposure may occur within one Run or across related Runs/Interactions when the protected inference risk persists.

Where material, Publication/Egress policy may consume bounded prior-disclosure state keyed to relevant recipient/purpose/scope/sink threat model.

```text
DISCLOSURE ACCOUNTING
!= DOMAIN Visibility
!= PERMANENT TRANSCRIPT LOG
```

If cross-Run survival is justified, retain the minimum sufficient policy/accounting state for the minimum justified lifetime and apply AI-03 purpose, retention, deletion/source-lifecycle and anti-resurrection rules.

Known/related sinks may be composed when the threat model requires. Arbitrary unknown external collusion is an explicit limit, not a fabricated guarantee.

Exact enforcement remains open: bounded rules/counters, structured ledger, IFC, posterior-leakage budgets or future mechanisms may compete.

## 7. PRE05-H06 — Recipient != surface != channel

The same recipient may require different safe representations on a private DANTE screen, lock screen, shared display, voice, email/push or external AI client.

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

Possible metrics include unsafe autonomous action count, missed approval count, unnecessary approval/interruption rate, correct autonomous completion within scope and correct escalation rate. Hard gates precede autonomy optimization.

## 10. PRE05-H09 — Current-tree executable eval detail

AI-05 must not require Git archaeology to reconstruct the current eval contract.

Current-tree workload coverage is:

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
E14 proactivity/Attention/causal-loop/notification truth
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
scoped autonomy posture + current autonomy revision/state
provider/data eligibility
required capabilities / resource envelope
expected outcome / hard assertions / forbidden actions
grading profile / repetition profile
```

Hard failures explicitly include wrong target, unauthorized/autonomously over-permitted effect, private/cross-actor/surface/cumulative disclosure, fabricated truth, false effect/Actual, stale publication, Reality Scope laundering, invalid memory reuse/promotion, resurrection, approximate-as-complete, ineligible failover, data→instruction laundering, current AuthZ/Consent/Visibility/autonomy bypass, unbounded consequential oscillation, treating Attention/publication as work/effect authorization, or claiming stronger notification transport state than evidence proves.

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

Any older local reading such as:

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

Current navigation must classify it as historical/superseded for runtime authority while preserving it as evidence.

## 14. PRE05-H13 — Formal IFC/leakage-budget/ACS remain challengers

Required now:

```text
DANTE semantic/privacy contract
trajectory/cross-work cumulative-disclosure tests
bounded disclosure-accounting responsibility where material
```

Not selected now:

```text
formal IFC implementation
posterior/inference-leakage algorithm
specific ACS middleware
```

Any challenger must preserve DANTE Authority/Visibility/Consent/Reality/Source semantics.

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

The first post-materialization retest found that carrying `Attention → start work` literally could turn Attention into hidden execution authority.

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

```text
CUMULATIVE DISCLOSURE RISK
MAY SPAN RELATED RUNS / INTERACTIONS / SURFACES
AND KNOWN RELATED SINKS WHEN THE THREAT MODEL REQUIRES.
```

Any surviving disclosure-accounting state is minimized, purpose-bound, retention-bounded and lifecycle/anti-resurrection governed. No indefinite content log is implied.

## 18. PRE05-H17 — Run-start autonomy is not perpetual autonomy

The second full retest found a distinct case in which Authority/AuthZ remain valid while the user's/current policy autonomy posture changes during a Run.

Binding:

```text
RUN-START AUTONOMY
!= PERPETUAL AUTONOMY
```

Before an autonomous consequential dispatch, especially after waits, approval delays, replanning, material target/basis change or a current policy/config change, DANTE re-evaluates the applicable current scoped-autonomy posture in addition to current Authority/AuthZ/Consent/Visibility and other effect gates.

Example:

```text
T0  AUTO_WITHIN_SCOPE
Run starts
T1  user/policy changes same scope to PROPOSE_ONLY
T2  effect otherwise remains authorized

→ no autonomous dispatch at T2
→ produce proposal/review path instead
```

Past legitimate work is not retroactively erased, and already-dispatched effects remain subject to verification/reconciliation rather than fictional rollback.

Autonomy currentness is policy/runtime state, not a new Domain Authority.

## 19. PRE05-H18 — Notify decision is not communication-state truth

AI-02 already preserves:

```text
SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
```

The second full retest found this needed explicit E14 traceability.

Binding:

```text
ATTENTION DECISION = NOTIFY
!= MESSAGE SENT
!= MESSAGE DELIVERED
!= USER SAW IT
!= USER ACKNOWLEDGED IT
!= USER ACCEPTED/ACTED
```

The selected notification/publication transport remains governed by the applicable capability/effect/publication contract and produces only the communication state supported by actual receipts/evidence.

A timeout or missing delivery receipt may remain `UNKNOWN`; DANTE must not upgrade it to delivered/seen/acknowledged.

E14 therefore grades both the attention decision and, where a real/simulated transport is part of the fixture, truthful transport outcome handling and deduplication/retry semantics.

## 20. Current composed responsibility path

```text
Trigger / Interaction
→ current trigger/work eligibility
→ WorkContract
→ Context / Retrieval / Memory
→ Basis / Reality / currentness
→ current scoped autonomy + policy + resource/provider/data eligibility
→ deterministic need or eligible qualified model route composition
→ current egress authorization
→ Reason / Compute / Capability Runtime
→ Verifier
→ current effect governance / approval / autonomy revalidation
→ verify / reconcile
→ Result Maturity
→ AttentionPolicy / AttentionBudget when attention is possible
→ recipient + surface + channel Disclosure Projection
→ cumulative disclosure check where material
→ governed publication/notification transport
→ truthful sent/delivered/seen/acknowledged state only from evidence
```

Responsibility boundary != service/table.

## 21. Fresh full retest corpus

The next retest restarts from zero and must cover at least:

```text
1 own-effect loop without new material delta
2 own-effect loop + genuine new external change
3 attention storm under quiet hours
4 urgent material signal under high attention pressure
5 cumulative protected inference inside one interaction
6 cumulative protected inference across separate Runs
7 same recipient across private/lock/shared/voice surfaces
8 known related sinks compose protected information
9 AUTO_WITHIN_SCOPE then Authority/AuthZ revoked
10 AUTO_WITHIN_SCOPE then autonomy alone changes to PROPOSE_ONLY
11 PROPOSE_ONLY with mutation technically available
12 attention silent while background work is otherwise eligible
13 attention notify while consequential work is ineligible
14 notification decision + transport timeout/unknown delivery
15 duplicate/replayed notification transport event
16 commercial quota exhausted during optional proactive work
17 quota exhausted after outcome-unknown effect
18 failover with context/capability contraction
19 continuation after policy/tool/Harness change
20 stale callback after supersession
21 provider/cache memory after deletion/revocation
22 auxiliary router/verifier/judge as governed recipient
23 model outage while deterministic route remains valid
24 compound: proactive Run + autonomy change + provider failover + surface change + quota pressure
25 compound: private source + cumulative disclosure + deletion + old cache/restore + new Run
```

PASS requires no unexplained responsibility gap, no new generic semantic owner and no hidden safety downgrade.

## 22. Non-claims / next action

```text
PRE-AI05 HARDENING MATERIALIZED      YES
FIRST RETEST                         FAIL BOUNDED / H15-H16
SECOND FULL RETEST                   FAIL BOUNDED / H17-H18
FRESH RETEST AFTER H17-H18           NOT YET EXECUTED
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