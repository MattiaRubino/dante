<!-- LIFEOS-CANONICAL-CONTINUATION document="README.md" follows="README-part-3.md" prior-total="3" -->
> **Canonical continuation of the LifeOS Domain Atlas README.** This is the next physical part of the same logical `README.md` document. Parts 1–3 remain preserved; this continuation records later current-state amendments. Physical split != additional logical document.

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 2026-08-15 — Proposal / Request v0 integration amendment

Relationships / Reasoning now includes accepted Proposal / Request v0 semantics under Domain Validation Methodology v3.

Current canonical separation:

```text
Proposal
= contextual semantic act/state that puts forward a materially specific candidate action, state, terms, rule, option or change for consideration

Request
= contextual directed semantic act/state that asks one or more Actors/systems for a bounded action, information, response, Decision, participation, permission or change

Proposal != Request
Proposal / Request != Message / Notification
Proposal / Request != delivery / view / Acknowledgement
Proposal != Agreement / Decision / effective state
Request != Responsibility / Participation / Authority / Consent
requested action != Actual execution
```

The accepted minimum is two contextual semantic families/capabilities, without a common universal ProposalRequest root, universal Interaction/Message root, generic Acceptance primitive, generic Response root, universal table or state machine.

Material-state and multi-actor hardenings are mandatory:

- material Proposal/Request state may be Version-aware where consequence requires it;
- prior Acknowledgement/response does not silently carry over after material change;
- real counter-Proposal is a distinct Proposal;
- silence is not acceptance/rejection;
- withdrawal/expiry changes future applicability without erasing history or automatically undoing an already-effective downstream result;
- proposer/requester/recipient/responsible actor/performer/Subject may differ;
- Representation preserves actual Actor and represented party;
- Account is not required for every relevant party;
- Visibility of content/history is independently governed;
- AI Proposal != human intention/Decision and AI/system Request preserves actual attribution;
- persistence is consequence-sensitive rather than universally materialized.

Downstream propagation touches the relevant Time, Responsibility, Participation, Acknowledgement, Decision, Agreement/Consent, Authority, Representation, Version, Criterion/Evaluation, Multi-Actor, Language Map, deferred-dependency and cross-cluster documents without reopening their accepted verdicts.

## Preservation repair recorded in this integration

During post-write audit, two earlier Proposal/Request propagation writes were found to have replaced large historical payloads instead of preserving them:

```text
docs/domain/concepts/schedule.md
docs/domain/checkpoints/version-material-equivalence-v0-validation.md
```

The repair rule is lossless:

```text
restore exact pre-Proposal/Request historical blob
+
move only the later Proposal/Request amendment into a canonical continuation part
```

Accordingly:

```text
schedule.md + schedule-part-2.md
= 1 logical Schedule document

version-material-equivalence-v0-validation.md
+ version-material-equivalence-v0-validation-part-2.md
= 1 logical Version validation checkpoint
```

No split changes the logical document count. Git QA still counts every physical path independently.

## Current stage rule

Proposal / Request semantic validation is `PASS WITH HARDENING`, with `REOPEN = 0` and no unclassified material dependencies. The authoritative final post-write closure is the Proposal / Request checkpoint and its canonical continuation; this README amendment does not independently declare QA complete before that checkpoint is closed.

After truthful Proposal / Request post-write closure, the next semantic action remains:

```text
fresh Relationships / Reasoning candidate re-score
→ select one candidate/family from the new accepted baseline
→ execute full Methodology v3
```

No next candidate is preselected by this amendment. No SQL/API/backend/auth/prototype/main synchronization is authorized by Proposal / Request closure.