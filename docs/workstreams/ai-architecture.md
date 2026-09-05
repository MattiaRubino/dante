# DANTE AI Architecture Workstream

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / READY TO HAND OFF TO IMPLEMENTATION
- **Branch:** `feature/ai-architecture`
- **Closed:** 2026-09-02
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / C01..C33 / B01..B35 / MAT-01..MAT-15
- **AI-04:** CLOSED / A01..A30 / EV01..EV20 / RT-01..RT-31 / PA-01..PA-61 / WP-01..WP-22
- **PRE-AI05:** CLOSED / PRE05-H01..H19
- **AI-05A:** CLOSED / BD-01..BD-41
- **AI-05B:** CLOSED / AI05B-H01..H15 / B05-01..B05-50 PASS
- **AI-05 whole-system:** CLOSED / STRUCTURALLY ACCEPTED
- **Post-AI05 hardening:** POST05-H01..H25
- **Final mega test:** MKT-001..MKT-100 PASS / C01..C20 PASS / reverse PASS / Product-simulation replay PASS
- **Implementation:** NONE YET
- **Provider/model/SDK:** OPEN / EVIDENCE-DRIVEN
- **Database/Alembic change:** NONE
- **Merge status:** UNMERGED
- **Next work:** actual AI implementation workstream, beginning at I0

Repository truth outranks conversation memory.

## 1. Final architecture state

```text
AI-00  Semantic & Product Foundation                         COMPLETE
AI-01  Product Form + Production Engineering Research        COMPLETE
AI-02  Intelligence Runtime Architecture                     CLOSED / STRUCTURALLY ACCEPTED
AI-03  Context / Retrieval / Memory                          CLOSED / STRUCTURALLY ACCEPTED
AI-04  Productionization Architecture                        CLOSED / STRUCTURALLY ACCEPTED
PRE05  Cross-Phase Hardening                                 CLOSED / STRUCTURALLY ACCEPTED
AI-05  Whole-System Acceptance + Implementation Blueprint    CLOSED / STRUCTURALLY ACCEPTED
POST05 Independent Pre-Implementation Mega Test              CLOSED / PASS

MKT-001..MKT-100                                             PASS / 100 OF 100
C01..C20 compound collisions                                 PASS / 20 OF 20
reverse authority                                            PASS
Product/simulation replay                                    PASS
```

No evidence required a Domain, Logical, Physical or PostgreSQL reopen.

## 2. Current implementation authority

A coder or agent starting implementation must begin from:

```text
docs/architecture/dante-ai-implementation-baseline-final.md
```

Final acceptance evidence:

```text
docs/architecture/dante-ai-post05-final-mega-acceptance.md
```

Earlier AI-05B candidates, hardenings, baseline v1/v2/v3 and post-AI05 failure reports are validation evidence. They do not override the final baseline.

## 3. Accepted implementation boundary

```text
modules/search
→ independent deterministic Global Search/discovery capability
→ bounded permission-safe read projection
→ no canonical mutation authority

modules/intelligence
→ Work/Context/Reference/SemanticQuery/Retrieval orchestration
→ optional governed model access
→ verification / Result Maturity / Effect NO_EFFECT / safe publication
→ no raw DB/canonical ownership

provider SDK/protocol
→ private admitted outbound adapter behind ModelAccessPort

bootstrap
→ composition/lifecycle only

platform
→ shared technical mechanics only

tooling/ai-evals
→ qualification tooling outside ordinary production request path
```

Search remains independent from Intelligence. Structured DANTE questions use owning capability typed query seams rather than raw SQL/model-to-SQL.

## 4. First implementation envelope

Initial technical target remains:

```text
GLOBAL SEARCH subset
+ READ-ONLY ASK DANTE

surface          private authenticated in-app
interaction      single-turn
runtime          inline / request-owned
consequence      READ_ONLY
public streaming OFF
background       OFF
durable resume   OFF
shared/external recipient surfaces OFF
consequential mutation OFF
```

```text
READ_ONLY
→ explicit EffectOutcome.NO_EFFECT
```

No generic AI table, conversation store, Run registry, memory store, Context store or embedding/vector store is justified by this envelope.

## 5. Critical retained implementation invariants

```text
PostgreSQL = sole canonical persistence/material-history authority
GLOBAL SEARCH != INTELLIGENCE
SEARCH RESULT / CURSOR / TARGET REF != AUTHORIZATION
SEMANTIC QUERY GATEWAY != INTELLIGENCE-OWNED CROSS-CAPABILITY SQL
Context != Retrieval != Memory
RetrievalCandidate != ContextFragment
ContextManifest != BasisManifest
DATA != INSTRUCTION
MASKING / REDACTION != SEMANTIC EQUIVALENCE
MODEL OUTPUT != PUBLISHABLE OUTPUT
PROVIDER COMPLETED != VERIFIED != PUBLISHABLE
PROVIDER FAILURE != DISCLOSURE DID NOT HAPPEN
AUXILIARY MODEL CALL != FREE PROVIDER CALL
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
APPLICATION FAKE != ADAPTER CONFORMANCE != LIVE COMPATIBILITY != DIRECT EVAL != CAPACITY PROOF
BUILD-READY != INTEGRATION-READY != ACTIVATION-READY
DEFAULT NONCANONICAL PERSISTENCE = NO
```

## 6. Provider and proof posture

No provider/model/SDK is selected by architecture closure.

Provider sequence remains:

```text
candidate shortlist
→ candidate admission
→ inactive adapter/binding
→ conformance
→ live compatibility on eligible/minimized test data
→ direct DANTE eval using production-owned composition
→ applicable privacy/security/capacity/economics evidence
→ qualification
→ promotion
```

Applicable direct proofs remain activation gates, including:

```text
PSV-06 / SC-017  protected Search/semantic/reference non-interference
PSV-07 / SC-018  FTS mixed filter/query when activated
PSV-08 / SC-019  vector filtered recall/relevance when activated
PSV-09 / SC-020  derived/current projection freshness
PSV-10 / SC-021  deletion/redaction propagation
PSV-21..28B      durable/Restate activation
PSV-37           pgvector provenance when activated
```

Missing applicable evidence is never treated as `N/A`.

## 7. Current next action

The architecture workstream itself is closed.

The next actual work is:

```text
ACTUAL AI IMPLEMENTATION WORKSTREAM
→ I0 repository/application ownership + architecture-test skeleton
→ I1 Search contracts/registry/application shell
→ I2 Intelligence pure contracts + deterministic fakes
→ advance later stages only when their real integration/activation prerequisites exist
```

I0 is build-authorized. This does not activate Search, Ask DANTE or any provider route in production.

## 8. Non-claims

```text
architecture design/reengineering closed      YES
post-AI05 mega structural pass                YES
implementation baseline accepted              YES
I0 implementation started                     NO
modules/search implemented                    NO
modules/intelligence implemented              NO
Auth/AuthZ integrated on this branch          NO
provider/model/SDK selected                   NO
direct provider eval executed                 NO
production capacity qualified                 NO
production Search/Ask active                  NO
PostgreSQL/Alembic changed                    NO
new AI table/index                            NO
FTS/vector activated                          NO
Restate/R2/MCP/A2A activated                  NO
Execution Environment selected                NO
```

## 9. Handoff / integration

Durable continuation is fully represented by the final implementation baseline, final mega acceptance, this closed workstream record and current project navigation.

The temporary `ai-architecture-live-handoff.md` is no longer needed and must not enter protected `main`.