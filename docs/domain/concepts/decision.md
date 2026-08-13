# Decision v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Decision is the contextual resolution semantics through which a bounded decision question is explicitly determined to a specific result for a defined target, materially relevant version and context by an Actor or applicable decision process. Where the resolution itself is materially relevant, it must remain historically reconstructible together with its result, decision-maker/process and, where justified, alternatives, rationale and basis. Decision does not by itself create Authority, prove truth, guarantee downstream effect, replace the resulting domain state, establish Actual, or replace Provenance.**

Decision answers:

> **What bounded question was resolved to what result, by whom/what, about which target/version/context?**

Decision is deliberately narrow. It preserves meaningful resolution where the resolution itself matters; it is not a universal wrapper for every mutation, click, workflow state, acceptance, approval, reconciliation step, or event in LifeOS.

---

# 1. Why Decision exists

LifeOS already distinguishes proposal, Acknowledgement, family-specific positive response, Authority, current state, Provenance and Actual. Those distinctions still leave a real gap when a bounded question is explicitly resolved and that resolution must remain reconstructible.

Representative examples:

- choose one restaurant/time among alternatives;
- approve or reject a responsibility hand-off under applicable governance;
- decide whether conflicting observations establish a current contextual interpretation;
- approve a reviewed material version;
- retain the current state after considering a proposed change;
- resolve which source/version should govern an imported conflict;
- explicitly decide not to proceed.

Without Decision semantics, LifeOS tends toward weak alternatives:

```text
latest state = decision
last write wins
approved = true
creator changed it so creator decided
Authority = Decision
Provenance = rationale
state history = decision history
```

All of those collapse distinct questions.

---

# 2. Decision is not every state change

A Decision may exist without a material target-state mutation.

```text
proposal: change Schedule to Tuesday
Decision: reject proposal / retain current Schedule
```

The resolution may matter historically even though the current Schedule does not change.

Conversely, an effective domain change may occur without a new explicit Decision when an already-authorized deterministic policy/process legitimately produces the effect.

```text
bounded policy already authorized
condition becomes true
→ resulting domain state changes
```

Therefore:

```text
Decision != state transition
Decision existence != target changed
state transition != new human Decision
```

The affected domain concept owns the resulting effective state transition.

---

# 3. Decision versus Authority

Authority answers:

> **Who/what may legitimately make a bounded governance effect effective?**

Decision answers:

> **What bounded question was resolved to what result?**

Therefore:

```text
Decision != Authority
```

A Decision does not manufacture Authority. An Actor may decide something personally without possessing Authority to impose the result on another governed context.

Likewise, an Actor may possess Authority but never exercise it in a Decision.

Where a Decision is intended to produce a governed effect, applicable Authority/policy must be evaluated separately.

---

# 4. Decision versus Approval

Approval is retained as scoped Decision/review semantics, not as a universal standalone primitive.

> **Approval is a scoped Decision/review result concerning a bounded proposal, action or materially relevant version, whose governance significance depends on applicable Authority/policy.**

Therefore:

```text
Approval != Authority
Approval != effective change
Approval != Actual
```

A workflow may require one or several approvals, review results, conditions or policy checks before an effect becomes current.

A derived state such as:

```text
approval requirements satisfied
```

need not create one universal `approved=true` kernel field.

Material change matters:

```text
Approval(target v1)
!= Approval(target v2) automatically
```

unless the applicable policy explicitly defines the change as non-material/equivalent.

---

# 5. Decision versus Reconciliation

Reconciliation is a process/pattern over competing, duplicate, inconsistent or revised representations.

It may:

- select one representation;
- merge compatible information;
- correct a current interpretation;
- split conflated identities/records;
- supersede an earlier interpretation;
- retain the conflict as unresolved.

An explicit consequential reconciliation may culminate in a Decision.

A deterministic policy reconciliation may occur without a new human Decision.

Therefore:

```text
Reconciliation != Decision universally
```

No universal Reconciliation entity/root is accepted.

---

# 6. Decision versus effective canonical change

Effective change belongs to the affected semantic owner.

Examples:

```text
Schedule changes
→ Schedule owns current temporal state

Responsibility transfers
→ Responsibility owns current accountability state

Actual interpretation is corrected
→ Actual owns current realization interpretation

Visibility changes
→ Visibility owns current exposure state
```

Decision, Authority and Provenance may explain respectively:

```text
what was resolved
who/what could legitimately govern the effect
how the target/version came to change
```

They do not replace the target's own current state.

Canonical rule:

> **The affected domain concept owns its effective state transition. Decision, Authority and Provenance explain the resolution, legitimacy and lineage where material.**

No universal `EffectiveChange` root/object is accepted.

---

# 7. Decision versus Provenance and rationale

Provenance answers how a Decision or target/version came to exist/change.

Decision answers what bounded question was resolved to what result.

Rationale answers why a result was selected where that explanation is materially useful.

Therefore:

```text
Decision != Provenance
Decision rationale != Provenance
Provenance != Decision result
```

A Decision may have Provenance. Its rationale may refer to Evidence, policy, constraints, alternatives or explanation, but none of those become the Decision merely by influencing it.

---

# 8. Decision versus Evidence, Confirmation and Acknowledgement

```text
Evidence
= information used evaluatively

Confirmation
= contextual attestation toward a target/version

Acknowledgement
= explicit taking-notice of a target/version/change/request

Decision
= bounded resolution to a result
```

Therefore:

```text
Evidence != Decision
Confirmation != Decision
Acknowledgement != Decision
```

A person may acknowledge a proposal and oppose it. A person may confirm that a fact/report is accurately stated without deciding what to do. Evidence may support competing alternatives without itself choosing one.

---

# 9. Decision versus Acceptance, Agreement and Consent

Generic cross-domain Acceptance remains rejected.

Family-specific positive response may contribute to a later Decision but does not become Decision automatically.

Agreement and Consent are now separate canonical semantic families:

```text
Decision
what bounded question was resolved?

Agreement
which applicable parties mutually assented to the same materially specific terms/version?

Consent
what bounded action/use/exposure did an eligible actor explicitly permit for which scope/purpose/context?
```

Therefore:

```text
Decision != Agreement
Decision != Consent
```

A manager may decide something without employee Agreement. Two parties may agree before an authorized third-party Decision/effect. Consent withdrawal may affect future action without erasing historical Decisions.

Decision must not absorb those semantics.

---

# 10. Version and materiality

A consequential Decision must target the materially relevant question/target/version.

```text
proposal v1
→ approved

proposal materially changes to v2
```

The prior Decision/Approval does not silently apply to v2 by default.

Exact Version/material-equivalence persistence is deferred, but the semantic requirement is fixed now:

> **A Decision binds to the materially relevant state it actually resolved.**

Non-material equivalence may be policy-defined later; it must never be silently inferred from implementation convenience.

---

# 11. Time and history

Where consequence warrants persistence, LifeOS must distinguish:

```text
proposal/question time
Decision time
effective-change time
Actual realization time
later correction/reversal time
```

These may be different.

A superseded or reversed Decision remains part of history where materially relevant.

```text
revoked / reversed / superseded
!= never decided
```

Current state must not rewrite earlier resolution history.

---

# 12. Multi-actor semantics

Decision is multi-actor-ready without requiring voting/groupware infrastructure.

One Actor's position is not automatically the shared Decision.

```text
Actor A supports option X
Actor B opposes option X
Authorized decision process resolves X
```

LifeOS may preserve all three facts without pretending that B agreed.

A shared Decision may coexist with:

- different actor stances;
- different Acknowledgement states;
- Agreement or lack of Agreement;
- actor-scoped Consent states;
- unequal Authority;
- accountless external approvers;
- represented parties;
- private rationale/Evidence;
- later dispute or appeal;
- a specialist source of record.

No universal Group, quorum, voting or committee primitive is implied.

---

# 13. Assisted, delegated and on-behalf-of decisions

A helper/recorder is not automatically the decision-maker.

Where representation/delegation matters, future modeling must preserve at least the distinction between:

```text
actual acting Actor/process
represented party/Subject where applicable
applicable Authority/delegation basis
authenticated Account/Principal where materially relevant
recorder/transcriber where different
```

Decision v0 does not finalize Principal/delegation mechanics.

A representative Decision must not be laundered into the represented person's personal Agreement, Consent, Acknowledgement or authorship.

---

# 14. AI boundary

AI may:

- propose alternatives;
- rank options;
- summarize Evidence;
- explain tradeoffs;
- prepare a Decision;
- execute a bounded decision process where explicit policy/Authority legitimately delegates that function.

AI must not silently:

- turn a recommendation into a human Decision;
- infer a human Decision from behavior;
- infer Agreement or Consent from a Decision;
- exceed applicable Authority;
- expose private rationale/Evidence merely because it was used;
- rewrite a prior human Decision to match later Actual;
- claim objective truth merely because an automated policy selected a result.

Canonical rules:

```text
AI proposal != Decision
AI recommendation != human Decision
AI/system Decision requires explicit bounded policy/Authority
```

---

# 15. Visibility and privacy

Decision result Visibility, rationale Visibility and supporting Evidence/Provenance Visibility are separate questions.

Example:

```text
shared result
meeting remains at 15:00

private rationale
one participant disclosed a medical constraint
```

The result may be visible while the private reason remains hidden.

Therefore:

```text
Decision result visible
!= rationale visible
!= Evidence visible
!= Provenance visible
```

Agreement/Consent existence and histories also have their own Visibility. AI explanations must respect these boundaries and avoid inferential disclosure.

---

# 16. Simple UI versus kernel semantics

Most ordinary LifeOS actions should not expose `Decision` as ontology language.

Possible UI labels include:

```text
Keep current
Use this
Apply
Approve
Reject
Choose
Finalize
Resolve
```

The UI label does not determine the domain primitive.

Low-consequence edits may produce no independent Decision record where the resolution itself has no durable value.

High-consequence or disputed flows may expose decision history, reviewer, rationale, alternatives or applicable governance.

---

# 17. Persistence/API implications — deliberately not physical design

Future logical modeling must be capable of representing/reconstructing, where materially required:

- bounded decision question/context;
- target and materially relevant version;
- result;
- actual decision Actor/process;
- applicable Authority/policy basis separately;
- decision time;
- effect time separately;
- alternatives/rationale where justified;
- supporting Evidence/Provenance references without payload duplication;
- supersession/reversal/correction history;
- actor-specific Visibility;
- accountless/external decision-makers;
- delegated/on-behalf-of attribution;
- zero/one/multiple downstream effects.

This does **not** pre-approve:

- one universal `decisions` table for every mutation;
- one polymorphic target foreign key strategy;
- one universal `approved` status;
- one universal state-transition/event log as domain truth;
- one generic workflow engine;
- one arbitrary JSON payload containing every Decision type;
- one universal Reconciliation or EffectiveChange entity.

---

# 18. Core invariants

1. Decision is contextual bounded resolution semantics, not a universal entity/root.
2. Decision must identify the bounded question/context it resolves.
3. Consequential Decision binds to the materially relevant target/version.
4. Material target change does not inherit prior Decision/Approval automatically.
5. Decision != Authority.
6. Decision != effective domain change.
7. Decision != Actual or objective truth.
8. Decision != Acknowledgement, Confirmation or family-specific Acceptance.
9. Decision != Agreement or Consent.
10. Decision != Provenance; rationale != Provenance.
11. Decision != Evidence/evaluation.
12. Decision may produce zero, one or multiple downstream effects.
13. Effective change may occur without a new explicit Decision under an already-authorized bounded policy/process.
14. Decision time != effect time != Actual realization time.
15. Superseded/reversed Decisions remain historical facts where material.
16. One Actor's Decision/Approval != collective Decision automatically.
17. Aggregate approval state may be derived from policy requirements.
18. Decision result Visibility != rationale/Evidence/Provenance Visibility.
19. AI proposal/recommendation != Decision.
20. AI/system Decision requires explicit bounded policy/Authority.
21. Deterministic reconciliation != human Decision automatically.
22. The affected domain concept owns the resulting effective state.
23. Ordinary low-consequence edits do not require a durable Decision record merely because a choice occurred.
24. No universal Approval/Reconciliation/EffectiveChange root is accepted.

---

# 19. Rejected alternatives

Rejected:

- no Decision semantics at all;
- Decision = state change;
- Decision = Authority;
- Decision = Provenance/rationale;
- Decision = Confirmation/Acknowledgement/Acceptance;
- Decision = Agreement/Consent;
- every mutation creates a Decision;
- universal Approval primitive/root;
- universal Reconciliation primitive/root;
- universal EffectiveChange object/root;
- one `approved=true` cross-domain field;
- last-write-wins as universal reconciliation;
- AI recommendation as human Decision;
- silent inheritance of approval across material versions.

---

# 20. SAFE DEFERRED dependencies

Decision v0 deliberately leaves the following independently owned areas open:

- exact Version / material-equivalence mechanics;
- Principal / delegation / on-behalf-of;
- proposal/request reusable identity;
- detailed reconciliation/source-precedence policy;
- collective Decision / quorum / voting semantics;
- GoalCriterion / evaluation relationship;
- exact persistence/cardinality/API representation;
- specialist approval/signature/legal workflows.

Agreement / Consent is now downstream RESOLVED at the semantic-boundary level and is no longer an open Decision dependency.

Each remaining dependency has an owner/reopening trigger/test set in `checkpoints/decision-v0-validation.md`.

---

# 21. Decision note

Decision v0 accepts only the narrow reusable semantic family:

```text
bounded question
        ↓
contextual resolution
        ↓
specific result
        ↓
optional governed effect(s) owned by affected concepts
```

It does not accept a universal workflow/state-transition ontology.

Future evidence may reopen the boundary, but any broader proposal must demonstrate that the narrow model loses required identity, history, Authority, privacy, queryability or product value.

---

# 22. Downstream closure — Agreement / Consent v0 (2026-08-13)

Agreement / Consent v0 closes Decision's former `Agreement / Consent` SAFE DEFERRED dependency without changing Decision semantics.

Current canonical decomposition:

```text
Decision
= bounded contextual resolution to a result

Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure under defined scope/purpose/context
```

Therefore:

```text
Decision ↔ Agreement  RESOLVED
Decision ↔ Consent    RESOLVED
```

A shared Decision may exist without Agreement of all affected parties. Agreement may exist before any governed effect or authoritative Decision. Consent may be a precondition/basis for some actions but is neither the Decision nor Authority and can later be withdrawn for future use without erasing historical Decisions.

Generic cross-domain Assent/Acceptance remains rejected. Remaining Decision dependencies are Version/material equivalence, Principal/delegation, Proposal identity, detailed reconciliation/source precedence, collective Decision, GoalCriterion/evaluation, exact persistence/API and specialist approval/signature/legal workflows.

No Decision hardening failed; **Decision remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `agreement.md`;
- `consent.md`;
- `../checkpoints/agreement-consent-v0-validation.md`.

---

# 23. Downstream closure — Representation / on-behalf-of v0 (2026-08-13)

Representation v0 closes Decision's former `Principal / delegation / on-behalf-of` semantic dependency without changing Decision.

Canonical separation:

```text
actual decision Actor/process
= who/what actually performed the bounded resolution

Representation / on-behalf-of
= the actual decision Actor acted for a distinct represented party in that bounded decision context

Authority / delegation basis
= whether the decision/effect is legitimate for the represented context

Principal
= technical request identity
```

Therefore:

```text
actual decision Actor != represented party by default
Representation != Decision
Representation != Authority
Principal != decision Actor
```

A representative may make a Decision with effect for another party when applicable Authority/process permits it. That does not turn the represented party into the historical decision-maker and does not imply the represented party personally agreed, consented, acknowledged or confirmed.

AI/service actors follow the same rule: if they perform the decision process under bounded policy, they remain attributable as the actual Actor/process rather than being laundered into a human Decision.

Downstream classification:

```text
Decision ↔ Representation/on-behalf-of   RESOLVED
Principal as domain primitive            REJECTED
universal Delegation primitive           REJECTED
```

Exact Principal/AuthN/AuthZ mechanics, action-specific delegability, Version/material equivalence, collective Decision, proposal identity, detailed reconciliation, GoalCriterion/evaluation and specialist legal/signature validity remain SAFE DEFERRED.

No Decision hardening failed. **Decision remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `representation.md`;
- `../checkpoints/representation-delegation-principal-v0-validation.md`.
