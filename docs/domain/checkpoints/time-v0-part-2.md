<!-- LIFEOS-CANONICAL-CONTINUATION document="time-v0.md" part="2" -->
> **Canonical continuation — Part 2.** This file continues `time-v0.md` as the same logical canonical document. The historical payload in `time-v0.md` remains authoritative for the state at the time it was written; this continuation records later downstream closure in chronological order. Physical file count does not change the logical-document count.

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 2026-08-15 — Proposal / Request downstream closure

Proposal / Request v0 closes the Time checkpoint's remaining proposal/request boundary around temporal coordination without changing the original Time-cluster verdict.

Canonical temporal separation now includes:

```text
proposed Schedule / temporal candidate
!= Request for temporal action/change
!= delivery / view
!= Acknowledgement
!= family-specific response
!= Agreement / Consent / Decision
!= current accepted Schedule
!= Session / Actual
```

A Proposal may put forward a materially specific Schedule candidate without making that Schedule current merely by proposing it. A Request may ask an Actor/system to schedule, reschedule, cancel, confirm, provide information, respond or perform another bounded temporal action without itself creating Responsibility, Participation, Authority, Consent or effective temporal state.

Time-specific hardenings:

- a proposed temporal placement remains distinct from current accepted Schedule;
- a request to reschedule does not itself reschedule;
- a request to attend does not itself create Participation;
- a request to take responsibility for a temporal commitment does not itself create Responsibility;
- a request for consent/permission around a temporal action is not Consent;
- delivery, display or view of a temporal Proposal/Request is not Acknowledgement;
- Acknowledgement is not positive response, approval or acceptance;
- silence does not establish acceptance/rejection;
- a materially changed temporal Proposal/Request must remain bound to the applicable Version/material state; prior acknowledgement/response does not silently carry forward;
- a real counter-proposal is a distinct Proposal rather than silent mutation of the earlier candidate;
- withdrawal/expiry changes future applicability without deleting proposal/request history;
- a withdrawn Proposal that already produced an effective Schedule does not automatically undo that Schedule;
- requested temporal action remains distinct from Session/Actual execution;
- AI/system temporal proposals and requests preserve actual Actor attribution and do not become human intention/Decision automatically;
- persistence remains consequence-sensitive; no universal Proposal, Request or scheduling workflow table/state machine is required by this closure.

Current classification:

```text
Time / Schedule ↔ Proposal              RESOLVED
Time / Schedule ↔ Request               RESOLVED
Proposal / Request ↔ effective Schedule RESOLVED — Schedule owns current state
Proposal / Request ↔ Session / Actual   RESOLVED — distinct
Proposal / Request ↔ Version            RESOLVED — material target binding where consequence requires
```

Still independently SAFE DEFERRED from the Time domain are Trigger/Reminder automation, exact provider mapping/materialization, DST/travel policy types, Principal/enforcement, retention and final logical/physical/API representation.

No Time hardening failed. **Time v0 remains PASS, REOPEN = 0.**

Normative downstream references:

- `../concepts/proposal.md`;
- `../concepts/request.md`;
- `proposal-request-v0-validation.md` and its canonical continuation parts.
