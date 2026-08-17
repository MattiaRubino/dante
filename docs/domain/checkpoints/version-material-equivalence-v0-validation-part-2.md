<!-- LIFEOS-CANONICAL-CONTINUATION document="version-material-equivalence-v0-validation.md" follows="version-material-equivalence-v0-validation.md" -->
> **Canonical continuation of `version-material-equivalence-v0-validation.md`.** This file is Part 2 of the same logical Version / Material-Equivalence validation checkpoint. The historical payload in the base file is restored byte-for-byte from the pre-Proposal/Request baseline; this continuation records only the later Proposal / Request closure. Physical split != additional logical document.

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 2026-08-15 — Downstream closure: Proposal / Request v0

Proposal / Request v0 resolves the reusable candidate/ask identity boundary that Version must preserve without becoming that identity itself.

```text
Proposal / Request
= attributable semantic act with a materially specific candidate/ask

Version / Material-State
= which materially relevant state that act concerned
```

Therefore:

```text
Version != Proposal
Version != Request
Proposal/Request != target Version
```

A materially different counter-Proposal is a distinct Proposal rather than a silent mutation inheriting prior response/Decision. A materially changed Request likewise does not silently preserve prior Acknowledgement, response, Agreement, Consent or Decision. Technical provider/storage revisions do not decide whether the candidate/ask changed materially.

Version preserves or reconstructs the relevant proposal/request material state and history; Decision, Authority, applicable policy and the affected domain concept still own response legitimacy, applicability and effective result.

Withdrawal or expiry affects future Proposal/Request applicability without erasing historical state binding or automatically undoing an already-established downstream effect.

Downstream classification:

```text
Version ↔ Proposal / Request      RESOLVED
technical revision = Proposal     REJECTED
Version owns proposal response    REJECTED
Version owns request fulfillment  REJECTED
```

Regression consequences retained:

- stale-base AI/system Proposal/Request must be re-evaluated after material divergence where consequence requires it;
- prior Acknowledgement/response does not automatically carry to a materially changed Proposal/Request;
- a counter-Proposal is distinct rather than mutation-with-inherited-state;
- actor-scoped history remains bound to the materially relevant candidate/ask state;
- provider revision/ETag/hash remains technical evidence, not semantic materiality;
- retention may preserve minimal reconstructible state without requiring indefinite full payload retention.

No Version hardening failed. **Version remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/proposal.md`;
- `../concepts/request.md`;
- `proposal-request-v0-validation.md` and its canonical continuation.