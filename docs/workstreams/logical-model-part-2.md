<!-- LIFEOS-CANONICAL-CONTINUATION document="logical-model.md" follows="logical-model.md" -->
> **Canonical continuation of `docs/workstreams/logical-model.md`.** This physical file is Part 2 of the same logical workstream handoff. The base file is preserved unchanged. This continuation records integrated A+B remote closure and the Slice-C Time / Reality checkpoint. Where the base status/header says integrated A+B remote QA is pending or Slice C is not started, this continuation supersedes that operational status.

# Logical Model Workstream — Part 2

**Date:** 2026-08-17  
**Branch:** `feature/logical-model`  
**Base main:** `068da4cc66620b3f3811051170e4913097091a04`

---

## 1. Integrated A+B final remote closure

The integrated A+B hardening package was previously written and then independently remote-QA-closed.

Canonical QA record:

```text
docs/logical-model/checkpoints/integrated-a-b-v1-remote-qa.md
```

Verified branch state after closure:

```text
feature/logical-model
HEAD
221325defb577f28168363f45a61ce06462167ba

main
068da4cc66620b3f3811051170e4913097091a04
UNCHANGED
```

Therefore the operational state before Slice C was:

```text
STAGE 0    ACTIVE / REMOTE QA PASS
STAGE 0H   ACTIVE / REMOTE QA PASS
SLICE A    ACTIVE / REMOTE QA PASS
SLICE B    ACTIVE / REMOTE QA PASS
A+B        ACTIVE / REMOTE QA PASS
```

The base workstream wording that still described integrated A+B activation as conditional is now superseded by this verified state.

---

## 2. Slice C — Time / Reality read-only validation completed

The mandatory read-only design/falsification phases were completed before the Slice-C write gate.

```text
C0  canonical Domain/product reconstruction                 DONE
C1  temporal/reality requirement + query corpus             DONE
C2  multiple logical candidate architectures                DONE
C3  temporal value / timezone / precision pressure          DONE
C4  recurrence family / occurrence identity pressure        DONE
C5  lazy occurrence materialization / reference pressure    DONE
C6  Schedule / Session / Actual / Outcome pressure          DONE
C7  Temporal Constraint / Conditional Policy boundary       DONE
C8  provider / external synchronization pressure            DONE
C9  historical replay / scale / evolution                   DONE
C10 mutation / counterfactual / A+B regression              DONE
C11 broad current external benchmark                        DONE
C12 LM-WF-21 mechanism reconsideration                      DONE
C13 reverse mapping + LM gate review                        DONE
```

No SQL/API/runtime implementation was part of this work.

---

## 3. Selected Slice-C logical model

```text
Layered Typed Time & Reality Model
```

Canonical separation:

```text
recurring/generative source
!= Recurrence
!= Occurrence
!= Schedule
!= Session
!= Actual
!= Outcome
!= Temporal Constraint
!= Conditional Policy
```

Primary representation decisions:

```text
Typed temporal values                -> LR-04
Recurrence                           -> LR-05
Occurrence, when persistently addressable/history-bearing
                                     -> LR-01 / NativeRef
Schedule                             -> LR-02 / ScopedRecordRef where material
Session                              -> LR-01 / NativeRef
Actual                               -> LR-06 + LR-02/ScopedRecordRef where material
Outcome                              -> LR-06 + LR-02 where material
Temporal Constraint                  -> LR-05
Conditional Policy                   -> LR-05
Provider/source identity             -> LR-09 / ExternalRef
Historical governing material state  -> MaterialStateRef pressure for Slice D
```

Critical rules:

```text
native semantic identity != eager physical materialization
Occurrence identity != current/original datetime universally
Schedule != Actual
Schedule elapsed != completion
no Actual != known non-realization
pause/resume != new Session by default
one Activity may have multiple Schedule placements
same time geometry != same semantic meaning
hard planning constraint != unrecordable reality
provider identity != LifeOS identity
lossy provider export != kernel weakening
```

---

## 4. Virtual/lazy Occurrence hardening

Slice C added a material new architecture pressure:

> how can future generated Occurrences remain lazy without either eager persistence or unstable/ephemeral identity?

The selected rule is:

```text
source + governing material state + bounded generation context
        ↓
derivable semantic Occurrence
        ↓ meaningful history/addressability
same semantic Occurrence
        ↓
NativeRef + persistent reconstructible state
```

No generic `VirtualRef` is introduced.

```text
virtual/lazy
!= new semantic reference-space family
```

The exact physical locator/key-issuance/materialization algorithm remains deferred.

---

## 5. LM-WF-21 mechanism/technology reconsideration

Slice C reopened the previously accepted shared reference mechanism because lazy occurrence identity changed the constraint surface.

Reconsidered:

```text
owner-specific references only
global Node/TemporalObject registry
generic VirtualRef
discriminated ReferenceAddress + bounded occurrence locator/generation context
```

Verdict:

```text
ReferenceAddress family + Reference Contract
RETAIN + HARDEN

new generic VirtualRef
REJECTED
```

Owner-specific refs remain a strong later physical ingredient. A technical registry remains physically possible if representation-only. No semantic Node/Thing/TemporalObject root is accepted.

---

## 6. Slice-C validation summary

Canonical Slice-C package:

```text
docs/logical-model/slices/time-reality-v1.md
docs/logical-model/checkpoints/time-reality-v1-validation.md
docs/logical-model/benchmarks/time-reality-v1.md
docs/logical-model/representation-framework-v1-part-2.md
docs/logical-model/test-corpus-v1-part-2.md
docs/logical-model/traceability-and-regression-ledger-v1-part-2.md
docs/logical-model/decision-and-assumption-register-v1-part-2.md
docs/workstreams/logical-model-part-2.md
```

Local validation counters:

```text
TRACE ENTRIES               24 / 24 CLOSED
NEW INVARIANTS              30 / 30 PASS
MUTATION TESTS              22 / 22 PASS
COUNTERFACTUAL FAMILIES     18 / 18 PASS
HISTORICAL REPLAY FAIL       0
SLICE-A/B REGRESSION FAIL    0
DOMAIN REOPEN REQUIRED       0
NEW DOMAIN OWNER REQUIRED    0
LOGICAL STRUCTURAL BLOCKER   0
```

New cumulative invariant range:

```text
INV-101..INV-130
```

New permanent test range:

```text
TC-P01..TC-P30
```

New high-value queries:

```text
52..75
```

---

## 7. External benchmark calibration

Current official/primary evidence was refreshed on 2026-08-17 across:

```text
RFC 5545 / iCalendar
Google Calendar
Microsoft Graph
Todoist
Reclaim
Motion
Android Health Connect
Apple HealthKit
HL7 FHIR R5
PostgreSQL current documentation
```

The cross-source structural result supports separation rather than one copied schema:

```text
policy/source
!= recurrence pattern
!= instance identity
!= accepted placement
!= actual execution
!= result
!= provider identity
```

No Domain reopen evidence emerged.

Canonical detail:

```text
docs/logical-model/benchmarks/time-reality-v1.md
```

---

## 8. Slice-C bounded write gate

User explicitly approved proceeding with the Slice-C checkpoint.

Approved remote scope:

```text
BRANCH
feature/logical-model

PRE-SCOPE SHA
221325defb577f28168363f45a61ce06462167ba

CREATE 8
UPDATE 0
DELETE 0
```

Exact CREATE paths are the eight canonical Slice-C package paths listed in section 6.

Why five cross-cutting files are continuations rather than replacements:

- the base framework/corpus/ledgers/workstream are already large canonical history-bearing documents;
- LifeOS documentation rules allow physically split canonical documents;
- the continuation approach preserves previous payload byte-for-byte;
- physical split != new logical document.

Explicitly out of scope:

```text
Domain Atlas changes
main writes
SQL DDL
migrations
ORM schema
API resources
backend services
runtime scheduler/replanner
AuthN/AuthZ implementation
frontend/prototype
physical indexes/partitions
provider adapter implementation
```

---

## 9. Conditional activation rule for this write

This continuation is written as part of the same atomic Slice-C package. It must not self-certify remote closure.

Slice C becomes ACTIVE only when post-write remote QA proves:

```text
feature/logical-model PRE-SCOPE matched immediately before ref write
exactly 8 expected paths added
0 modified
0 deleted
0 unexpected
all 8 remote payloads readable
branch HEAD equals the intended Slice-C commit
PRE-SCOPE -> HEAD is fast-forward and not behind
main remains exactly 068da4cc66620b3f3811051170e4913097091a04
```

Once these conditions are satisfied, the following operational state becomes effective without requiring a status-only rewrite:

```text
SLICE C — TIME / REALITY
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

REFERENCE MECHANISM
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED
0
```

If any condition fails, Slice C remains not remotely active until the discrepancy is resolved and QA reruns.

---

## 10. Mandatory next gate after Slice-C activation

A local/remote Slice-C PASS does **not** authorize Slice D directly.

Next required semantic step:

```text
CUMULATIVE INTEGRATED CHECKPOINT
Stage 0 + Stage 0H + Slice A + Slice B + Slice C
```

Required pressure includes:

```text
INV-001..130
TC-M / TC-N / TC-O / TC-P affected scenarios
ReferenceAddress + lazy Occurrence interaction
MaterialStateRef obligations accumulated by B+C
planned vs actual history
provider reconciliation chronology
simple-case compactness
worst-case/10-year recurrence
multi-actor/shared Actual boundaries
Product Reality cross-domain history pressure
LM-24 cumulative integrated coherence
LM-25 mechanism reconsideration if new trade-offs appear
```

If cumulative findings materially change a shared mechanism, LM-WF-21 runs again with no incumbent preference.

Only after cumulative A+B+C passes and any hardening is remote-QA-closed may Slice D begin.

---

## 11. Current roadmap after conditional Slice-C activation

```text
STAGE 0
ACTIVE / REMOTE QA PASS

STAGE 0H
ACTIVE / REMOTE QA PASS

SLICE A
ACTIVE / REMOTE QA PASS

SLICE B
ACTIVE / REMOTE QA PASS

INTEGRATED A+B
ACTIVE / REMOTE QA PASS

SLICE C
LOCAL PASS WITH HARDENING
REMOTE ACTIVATION CONDITIONAL ON CURRENT WRITE QA

INTEGRATED A+B+C
NEXT REQUIRED GATE AFTER SLICE-C QA
NOT YET EXECUTED

SLICE D — Evidence / Knowledge / History
HOLD

SLICE E — Resources / Values / Capacity
HOLD

SLICE F — Relationships / Multi-Actor / Governance
HOLD

FINAL
Whole-Logical integrated regression
clean-room reconstruction
WD-03 discharge
WD-05 discharge
Logical closure
```

---

## 12. Continuation rule

Any future session/model resuming from Git should:

1. read the base `docs/workstreams/logical-model.md`;
2. read this canonical Part 2 continuation;
3. verify current remote branch/main state rather than assuming the status text is still current;
4. if Slice-C remote QA is present and passing, run cumulative A+B+C before Slice D;
5. preserve the exact out-of-scope implementation boundary until separately authorized.
