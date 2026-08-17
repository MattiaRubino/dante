<!-- LIFEOS-CANONICAL-CONTINUATION document="domain-model.md" follows="domain-model-part-2.md" prior-total="2" -->
> **Canonical continuation of `domain-model.md`.** This is the next physical part of the same logical Domain Model workstream handoff. Earlier parts remain preserved; this continuation records current operational state after Proposal / Request v0. Physical split != additional logical document.

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# ACTIVE HANDOFF — Proposal / Request v0 closure

**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Stage:** Relationships / Reasoning  
**Validation standard:** Domain Validation Methodology v3  
**Pre-final-closure parent:** `7312e8eb527c1e6b8b575e8ecc885786cac15a0c`  
**Final closure authority:** `../domain/checkpoints/proposal-request-v0-validation.md` + `../domain/checkpoints/proposal-request-v0-validation-part-2.md`

## Current semantic result

Proposal / Request v0 is accepted as:

```text
PROPOSAL / REQUEST v0
PASS WITH HARDENING

Proposal
✅ contextual semantic family/capability
✅ materially targetable/version-aware where consequence requires
❌ universal root/table/workflow

Request
✅ contextual directed semantic family/capability
✅ reusable across bounded asks
❌ Responsibility
❌ Participation
❌ Authority
❌ Consent
❌ effective state
❌ universal root/table/workflow

ProposalRequest common root
❌ REJECTED

Generic Acceptance
❌ REJECTED

Generic Response root
❌ REJECTED

REOPEN        0
UNCLASSIFIED  0
```

Critical barrier:

```text
proposed / requested
!= delivered / seen
!= acknowledged
!= responded to
!= agreed / consented / decided
!= effective state
!= Actual
```

Proposal and Request remain distinct from Message/Notification transport, from downstream effect and from family-specific response semantics.

## Propagation and preservation state

Proposal / Request propagation has been carried across the approved adjacent domain documents, including Time, Responsibility, Participation, Acknowledgement, Decision, Agreement/Consent, Authority, Representation, Version, Criterion/Evaluation, deferred-dependency, cross-cluster, Multi-Actor and Language Map material.

Large-document continuations are canonical physical splits only. They do not create new logical documents.

During final preservation QA, two earlier propagation writes were proven to have truncated historical payloads:

```text
docs/domain/concepts/schedule.md
docs/domain/checkpoints/version-material-equivalence-v0-validation.md
```

They were repaired losslessly by restoring their exact pre-Proposal/Request Git blobs and placing only the later Proposal / Request amendments in:

```text
docs/domain/concepts/schedule-part-2.md
docs/domain/checkpoints/version-material-equivalence-v0-validation-part-2.md
```

Repair invariants:

```text
schedule.md SHA
= 7a2cf9ffc00e0e4112e848ad2059dd6421517b6e

version checkpoint SHA
= 0f387f4f599c7c7b1fac542c3ab12cfbf87ffaa3
```

The Proposal / Request closure must be counted as:

```text
30 logical documents affected
31 physical Git paths changed from the pre-Proposal baseline
```

The extra physical path exists because the Proposal / Request checkpoint itself is now continued physically rather than rewritten as one oversized file. Split parts never increase the logical-document count.

A separate approved Operating Manual scope changed four additional physical paths during this workstream. Those four paths are governance work and must remain excluded from Proposal / Request semantic/propagation counts.

## Completed operating-standard hardening

The repository now also contains `docs/development/agent-operating-manual.md`, linked from the existing operating/handoff/index documentation. New chats/agents must follow it rather than reconstructing operating discipline from conversation history.

Among other rules it makes mandatory:

- exact Git write gate with branch/pre-scope/path scope;
- refetch-and-stop on SHA mismatch;
- remote post-write QA;
- append/preservation-first documentation handling;
- logical-document vs physical-path split counting;
- safe canonical continuation for large files;
- explicit Git/tool failure reporting instead of blind retries;
- Domain Validation Methodology v3 for active Domain Atlas validation;
- fresh candidate re-score after semantic milestones rather than inherited roadmap selection.

## Next exact semantic step

Only after the Proposal / Request final checkpoint continuation is QA-closed:

```text
fresh Relationships / Reasoning candidate re-score
→ score the remaining candidate space from the new accepted baseline
→ select one candidate/family only
→ execute full Methodology v3
```

Do not preselect the next candidate from an older ranking.

Still out of scope unless separately gated:

```text
main synchronization
SQL / migrations
API
backend implementation
auth / Principal implementation
prototype / frontend
logical / physical model
Trigger / conditional policy
Resource Requirement / Allocation / Reservation
Verification / comprehension
collective / Group / quorum
universal Response / Acceptance primitives
historical-record deletion/rewrite
docs/domain/concepts/relationship.md
```

`docs/domain/concepts/relationship.md` remains intentionally absent by accepted Relationship v0 design.