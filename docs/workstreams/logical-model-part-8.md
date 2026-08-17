<!-- LIFEOS-CANONICAL-CONTINUATION document="logical-model.md" follows="logical-model-part-7.md" -->
> **Canonical continuation of the Logical Model workstream record.** Earlier history remains preserved. This continuation records Slice F — Relationships / Multi-Actor / Governance read-only validation, approved write scope and activation gate.

# 2026-08-17 — Slice F: Relationships / Multi-Actor / Governance

## Entry condition

Integrated A+B+C+D+E is remotely QA-closed and ACTIVE.

Verified pre-Slice-F state:

```text
branch
feature/logical-model

PRE-SCOPE
ad0c314ddf117ab958ba0033707f769ce739b9b3

main
068da4cc66620b3f3811051170e4913097091a04
```

Slice F began only after the cumulative A+B+C+D+E checkpoint authorized read-only analysis.

## Purpose

Validate the final thematic Logical Model slice against the accepted Domain semantics for:

```text
Actor
Collective
Membership
Interpersonal Relationship
Participation
Responsibility
Coordination Stewardship
Contribution
Ownership
Possession
Authority
Consent
Agreement
Visibility
Representation / On-Behalf-Of
multi-actor shared reality
selective disclosure
domain governance vs technical authorization
```

The central risk is that implementation convenience could reintroduce the rejected generic semantic graph through:

```text
Relationship(from,type,to,payload)
RelationRef
Permission/Access mega-concept
ReBAC tuple ontology
ABAC/policy ontology
capability-grant ontology
```

## Read-only workflow completion

```text
F0  canonical reconstruction                              DONE
F1  relation/governance requirement + query corpus       DONE
F2  multiple candidate architectures                     DONE
F3  Actor / Collective / Membership                      DONE
F4  Participation / Responsibility / Stewardship         DONE
F5  Contribution / interpersonal / ownership/possession  DONE
F6  Authority / Consent / Agreement                      DONE
F7  Visibility / Representation / multi-actor privacy    DONE
F8  ReBAC / ABAC / capability external benchmark         DONE
F9  mutation / counterfactual / A-E regression           DONE
F10 reverse mapping + technology reconsideration         DONE READ-ONLY
```

## Preferred logical candidate

```text
Layered Typed Relations & Governance Model
```

Core representation:

```text
ReferenceAddress
        ↓
specific semantic relation family
        ↓
Reference Contract + relation profile
        ↓
direct typed relation
OR
qualified LR-02 material relation
        ↓
ScopedRecordRef + MaterialStateRef where consequential
```

Governance/enforcement split:

```text
Authority / Consent / Visibility / Agreement / Membership / Representation / policy
        ↓
Effective governance projection
        ↓
Principal + Action + Resource + Context
        ↓
replaceable AuthZ engine
        ↓
allow / deny
```

Mandatory invariant:

```text
DOMAIN GOVERNANCE STATE
!=
TECHNICAL AUTHORIZATION DECISION
```

## Candidate comparison

```text
F-A Universal semantic Relationship/Edge
REJECTED LOGICAL CANDIDATE

F-B Fully owner-specific relation structures
VIABLE STRONG ALTERNATIVE / PHYSICAL INGREDIENT

F-C Layered Typed Relations & Governance
SELECTED — PASS WITH HARDENING

F-D ReBAC graph as canonical model
REJECTED AS DOMAIN MODEL
RETAINED AS AUTHZ PROJECTION/ENFORCEMENT CANDIDATE

F-E ABAC/policy language as canonical model
REJECTED AS DOMAIN MODEL
RETAINED AS POLICY/ENFORCEMENT CANDIDATE

F-F Universal capability/grant ledger
REJECTED AS COMPLETE MODEL
RETAINED FOR BOUNDED DELEGATION

F-G Universal governance event log
REJECTED AS LOGICAL ONTOLOGY
RETAINED AS POSSIBLE PHYSICAL HISTORY MECHANISM
```

## Slice F hardening package

```text
F-H01  No universal semantic Relationship/Edge root.
F-H02  No universal RelationRef; use ScopedRecordRef/MaterialStateRef when material.
F-H03  Reference Contract gains relation-profile constraints without becoming ontology.
F-H04  Direct relation vs qualified material relation is consequence-sensitive.
F-H05  Actor remains role/capability; specific actor role wins over generic actor edge.
F-H06  Membership never implies Participation/Authority/Visibility/Consent/Agreement.
F-H07  Interpersonal Relationship does not grant Authority/Visibility/Consent.
F-H08  Responsibility, Stewardship, performer and Participation remain independent.
F-H09  Participation != Contribution.
F-H10  Ownership != Possession != Authority/Visibility.
F-H11  Authority may be explicit or derived; historical action-time basis reconstructible.
F-H12  Consent is scope/purpose/target/time/material-state sensitive.
F-H13  Agreement is n-ary and materially terms/version-bound.
F-H14  Collective Agreement/action does not rewrite member personal state.
F-H15  Visibility can govern relation/projection/source independently from endpoints.
F-H16  Representation preserves actual Actor separately from represented party and basis.
F-H17  Domain governance != technical AuthZ allow/deny.
F-H18  ReBAC/ABAC/capability systems remain replaceable enforcement candidates.
F-H19  Delayed consequential effects cannot rely indefinitely on stale authorization.
F-H20  Unknown/conflicting governance remains representable; no universal winner.
```

## External benchmark

Current primary-source benchmark set:

```text
Google Zanzibar
OpenFGA
Cedar
Open Policy Agent
SCIM RFC 7643
OAuth Token Exchange RFC 8693
HL7 FHIR Consent
AWS IAM policy evaluation
Macaroons / contextual caveats
```

Cross-source result:

```text
relationship / policy / capability mechanisms
can be excellent authorization infrastructure

but

do not justify replacing LifeOS semantic relation/governance owners
```

## Mutation / counterfactual pressure

```text
mutation tests              38
mutation failures            0

counterfactual pairs        22
counterfactual failures      0

A-E carry-forward cases      7
A-E carry-forward failures   0
```

Critical destructive mutations rejected include:

```text
generic Relationship root
RelationRef hierarchy
Membership -> Authority/Visibility
Relationship label -> Authority
Responsibility = performer/Stewardship
Participation = Contribution
Consent = Visibility/technical Permission
Agreement = pairwise edges
Collective state -> member personal state
Representation -> represented party as Actor
technical ALLOW/DENY -> domain governance truth
AuthZ tuple store -> domain source truth
stale queued allow -> permanent authorization
```

## Product Reality replay

Slice F successfully represents:

```text
one Household Collective
independent Membership
Responsibility
Coordination Stewardship
Participation
private health source
safe shared Availability projection
bounded Authority
separate Consent
relation-level Visibility
AI/service Representation
separate technical Principal
```

without per-user duplication or a generic semantic relationship graph.

Agreement pressure additionally proves that a materially specific common-ground relation may require an n-ary LR-02 record bound to exact terms MaterialStateRef rather than pairwise edges.

## A+B+C+D+E regression

```text
A regression fail 0
B regression fail 0
C regression fail 0
D regression fail 0
E regression fail 0
```

The cumulative carry-forward selective-disclosure requirement is now closed locally:

```text
private source
-> authorized computation
-> shareable bounded consequence
without source disclosure
```

No accepted Slice A-E architecture is reopened.

## LM-WF-21 — mechanism / technology reconsideration

Reopened candidates:

```text
Layered typed semantic relations
fully owner-specific relation structures
shared typed edge/reference substrate
Zanzibar/OpenFGA ReBAC
Cedar / ABAC
OPA/Rego
capability credentials
governance event/history ledger
```

Verdict:

```text
Layered typed semantic relations
RETAIN + HARDEN

ReferenceAddress
RETAIN

ScopedRecordRef
RETAIN

MaterialStateRef
RETAIN

Reference Contract
RETAIN + RELATION PROFILE HARDENING

fully owner-specific physical structures
RETAIN AS STRONG PHYSICAL INGREDIENT

shared typed edge/reference substrate
RETAIN ONLY IF SEMANTIC OWNER REMAINS DETERMINISTIC

Zanzibar/OpenFGA
RETAIN AS AUTHZ PROJECTION/ENFORCEMENT CANDIDATE

Cedar
RETAIN AS TYPED POLICY/AUTHZ CANDIDATE

OPA/Rego
RETAIN AS POLICY DECISION CANDIDATE

capability credentials
RETAIN FOR BOUNDED DELEGATION

universal Relationship ontology
REJECT

universal Permission/Access ontology
REJECT

universal capability ledger
REJECT
```

No technology benchmark requires restructuring A-E.

## WD-03 pressure

Slice F requires consequential history to preserve/reconstruct:

```text
relation material state
Membership/quorum basis
Authority action-time basis
Consent applicability / withdrawal
Agreement terms/version
Visibility applicability/disclosure
Representation actual Actor / represented party / legitimacy basis
stale/delayed authorization effect-time validity
```

Slice F advances but does not alone close whole-model WD-03. Final A+B+C+D+E+F replay owns the integrated discharge decision.

## WD-05 pressure

Slice F keeps Physical Model freedom among:

```text
owner-specific relation tables
shared typed edge infrastructure where safe
qualified relation records
MaterialStateRef-backed history
ReBAC/ABAC projection stores
runtime policy engines
capability mechanisms
hybrid
```

The integrated final checkpoint must pressure whether those distinctions can survive concrete persistence/API/security implementation before Physical Model authorization.

## Local verdict

```text
SLICE F — RELATIONSHIPS / MULTI-ACTOR / GOVERNANCE

PREFERRED
Layered Typed Relations & Governance Model

PASS WITH HARDENING

DOMAIN REOPEN REQUIRED        0
NEW DOMAIN OWNER REQUIRED     0
A+B+C+D+E REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER    0

TECHNOLOGY
RETAIN + HARDEN

REMOTE QA
PENDING
```

## Exact approved Slice F write scope

```text
BRANCH
feature/logical-model

PRE-SCOPE
ad0c314ddf117ab958ba0033707f769ce739b9b3

CREATE
8

UPDATE
0

DELETE
0
```

Approved CREATE paths:

```text
docs/logical-model/slices/relationships-multi-actor-governance-v1.md
docs/logical-model/checkpoints/relationships-multi-actor-governance-v1-validation.md
docs/logical-model/benchmarks/relationships-multi-actor-governance-v1.md
docs/logical-model/representation-framework-v1-part-8.md
docs/logical-model/test-corpus-v1-part-8.md
docs/logical-model/traceability-and-regression-ledger-v1-part-8.md
docs/logical-model/decision-and-assumption-register-v1-part-8.md
docs/workstreams/logical-model-part-8.md
```

## Explicit out of scope

```text
Domain changes
SQL / tables / FKs / indexes / migrations
OpenFGA/Cedar/OPA/custom-engine selection
runtime authorization implementation
Principal/AuthN implementation
OAuth/token implementation
ACL/ReBAC tuple projection implementation
API/backend
frontend
main
Physical Model
```

## Activation rule

Slice F must not be called ACTIVE/CLOSED until all conditions hold:

1. branch HEAD equalled exact PRE-SCOPE immediately before the first approved write;
2. compare PRE-SCOPE -> content HEAD reports exactly eight added approved paths and no modified/deleted/unexpected path;
3. all eight remote payloads are read back successfully;
4. `main` remains exactly `068da4cc66620b3f3811051170e4913097091a04`;
5. a separately gated remote-QA closure record binds PRE-SCOPE, content HEAD, compare result and main-protection check.

## Next step after Slice F closure

Only after remote-QA closure may the workstream open:

```text
INTEGRATED A+B+C+D+E+F
WHOLE-LOGICAL VALIDATION
READ-ONLY FIRST
```

That checkpoint must be materially stronger than an ordinary slice replay and must include:

- complete reverse mapping from logical representation to Domain owner;
- clean-room reconstruction;
- whole-system mutation/counterfactual replay;
- cross-slice Product Reality scenarios;
- historical reconstruction sufficient to evaluate WD-03 discharge;
- concrete persistence/API/AuthZ pressure sufficient to evaluate WD-05 discharge;
- full mechanism/technology reconsideration;
- simple-case compactness versus worst-case correctness;
- explicit determination of whether Physical Model work can begin without semantic reopen.

No Physical Model write or implementation work is pre-authorized by this continuation.