# DANTE AI-05 — Whole-System Implementation Readiness Hardening

- **Status:** WHOLE-SYSTEM DESTRUCTIVE PASS FAIL BOUNDED / AI05-H01 MATERIALIZED / FINAL RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Established:** 2026-09-02
- **Upstream:** AI-05A CLOSED / AI-05B CLOSED
- **PRE-SCOPE:** `9e4d80a89b485aeec8f43a2aaba9372b0cd6c630`
- **Architecture reopen:** NONE
- **Database/Alembic change:** NONE
- **Provider/model/SDK selection:** NONE
- **Runtime implementation:** NONE

The first whole-AI-05 destructive composition pass found one cross-subphase ambiguity: architecture closure could otherwise be misread as permission to activate every part of the first vertical immediately.

AI-05A and AI-05B already define the necessary boundaries. This hardening makes the implementation-entry and activation sequencing explicit so downstream work cannot skip prerequisites while still claiming compliance.

---

# 1. AI05-H01 — Build-ready != integration-ready != activation-ready

Keep three readiness classes distinct:

```text
BUILD-READY
= repository/application contracts may be implemented and tested in isolation
  using accepted fakes/synthetic trusted contexts where appropriate

INTEGRATION-READY
= required real owning seams/data/capabilities exist and can be wired
  without temporary authority or semantic substitutes

ACTIVATION-READY
= the user-visible/production path has passed every applicable
  security/privacy/qualification/operational/release gate
```

Binding:

```text
AI-05 STRUCTURALLY CLOSED
!= FIRST VERTICAL PRODUCTION ACTIVE

BUILD-READY
!= INTEGRATION-READY
!= ACTIVATION-READY
```

No temporary bypass may be introduced merely to advance the implementation sequence.

---

# 2. Implementation readiness matrix

| Step/capability | Build-ready after AI-05 | Integration prerequisites | Activation prerequisites |
|---|---|---|---|
| I0 repository/application ownership skeleton | YES | none beyond current backend foundation | not user-visible |
| I1 Search public contract + bounded adapter shell | YES | existing database runtime; concrete family registrations only when their owning data exists | no public Global Search until at least one useful permission-safe family is proven |
| I2 pure Intelligence contracts + deterministic fakes | YES | Search-owned public fake/protocol; synthetic trusted request/security contexts allowed only in tests | not production Ask |
| I3 deterministic Global Search | CONDITIONAL | at least one real useful `SearchFamilyRegistration`; material source/current/history semantics; authoritative eligibility seam | authenticated route; current permission/disclosure proof; non-interference tests; product-safe result projection |
| I4 concrete provider adapter | NO concrete provider until evidence gate | selected provider/model/SDK/binding after direct decision evidence | adapter conformance + live compatibility + current eligibility/config controls |
| I5 DANTE route/model qualification | CONDITIONAL | material production composition available | direct eval + applicable capacity/security/privacy/evidence gates |
| I6 read-only Ask DANTE | application shell BUILD-READY; real model route conditional | authoritative Access/Auth seam; active Search/public sources; qualified provider route or deterministic no-model behavior where sufficient | private authenticated in-app route; current authorization; route eligibility; resource admission where applicable; safe publication; evidence/rollout gates |
| I7 production hardening | incremental | real observability/control/resource components as justified | mandatory before corresponding production activation |
| I8 scenario/planning proposal | NOT activated by AI-05 closure | owning product semantics + scenario contracts | preview/approval/current basis/safety gates |
| I9 consequential Effect | NOT activated by AI-05 closure | owning application mutation use case + target/current-state + policy/approval/effect evidence | consequential audit/idempotency/reconciliation/rollback requirements proven |
| I10 proactive/background/durable/external-agent | NOT activated by AI-05 closure | real trigger + lifecycle owner + durability/security need | dedicated qualification/operations/privacy/recovery gates |

---

# 3. Current concrete blockers are truthful dependencies, not architecture defects

At AI-05 closure time, the following remain intentionally unresolved outside the design workstream:

```text
real integrated Access/Auth application seam on this branch
at least one useful product Search family backed by materialized product data
provider/model/SDK selection
live provider compatibility
DANTE direct eval
production capacity qualification
real resource/commercial authority when required
production observability/control-plane implementation
```

These do not reopen AI-05.

They constrain which implementation step may advance from BUILD-READY to INTEGRATION-READY or ACTIVATION-READY.

Rejected shortcuts:

```text
temporary trusted-user header
hard-coded production principal
AI-owned shadow authorization database
searching all 69 tables because they exist
fake Search family declared product-ready
provider chosen by preference without decision evidence
production Ask enabled because fake ModelAccess passes unit tests
NO_EFFECT convention without Effect boundary
skip direct qualification because adapter conformance passed
```

---

# 4. Database posture

This readiness hardening does not create a schema need.

```text
DATABASE CHANGE = NONE
ALEMBIC CHANGE = NONE
```

A future product capability may legitimately require normal forward database evolution. That decision is owned by the concrete product vertical and current PostgreSQL same-change rule, not by AI implementation convenience.

---

# 5. Whole-system final retest requirement

Final AI-05 destructive acceptance must prove at least:

```text
W05-01 AI-05A ownership and AI-05B concrete contracts compose without duplicate owners.
W05-02 BUILD-READY cannot be mistaken for production activation.
W05-03 missing Access/Auth blocks public private-data Search/Ask activation without blocking isolated contract implementation.
W05-04 missing useful Search family blocks fake Global Search readiness without forcing generic DB search schema.
W05-05 missing provider selection blocks concrete provider integration without blocking deterministic Search/I0-I2.
W05-06 adapter conformance cannot substitute for direct model/route qualification.
W05-07 no new AI persistence is required to begin I0-I2.
W05-08 consequential effects remain outside first read-only activation envelope.
W05-09 future DB evolution remains product-triggered and normal forward change.
W05-10 reverse Product/Domain/Logical/Physical/PostgreSQL/AI authority remains unchanged.
```

Compound cases:

```text
implementation team starts I0-I2 while Auth branch is unavailable
Search shell exists but zero useful families are materially ready
provider adapter fake passes while no provider has been selected
provider selected but route config/direct eval not qualified
Ask route receives valid HTTP with no authoritative Auth seam
future product vertical needs new field/table for real Search semantics
```

Only a clean full retest may close AI-05.

---

# 6. Current status

```text
AI-05A                               CLOSED / STRUCTURALLY ACCEPTED
AI-05B                               CLOSED / STRUCTURALLY ACCEPTED
AI05-H01                             MATERIALIZED
AI-05 WHOLE-SYSTEM FINAL RETEST      REQUIRED
AI-05 CLOSED                         NO
IMPLEMENTATION                       NONE
PROVIDER/MODEL/SDK                   OPEN
DATABASE/ALEMBIC CHANGE              NONE
```
