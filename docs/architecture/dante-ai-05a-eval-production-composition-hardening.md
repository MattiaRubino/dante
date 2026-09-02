# DANTE AI-05A — Eval ↔ Production Composition Hardening

- **Status:** CANDIDATE HARDENING / SECOND PASS FAIL BOUNDED / FRESH RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05A — Whole-System Build Boundary / Ownership Map
- **Established:** 2026-09-02
- **Upstream candidate:** `docs/architecture/dante-ai-05a-whole-system-build-boundary.md`
- **Upstream accepted architecture:** AI-02.1 / AI-03 / AI-04 / PRE-AI05 CLOSED / STRUCTURALLY ACCEPTED
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN
- **Database change:** NONE

This supplement records the single bounded gap exposed after the first AI-05A hardening was retested. It does not reopen AI-04 or PRE-AI05 and it does not claim provider qualification.

## 1. Retest chronology

The original AI-05A candidate failed its first `T01..T26` destructive pass and was hardened with `BD-31..BD-40`.

The second pass then produced:

```text
T01..T26 individual cases            PASS CANDIDATE
Search + Intelligence + outage       PASS CANDIDATE
hidden-result + Ask synthesis        PASS CANDIDATE
config snapshot + emergency deny     PASS CANDIDATE
quota + retry/failover + settlement  PASS CANDIDATE
inline stream + disconnect           PASS CANDIDATE
cumulative privacy + zero-persist    PASS CANDIDATE

compound/reverse qualification seam  FAIL BOUNDED
```

The failure was not in DANTE eval semantics. It was in the implementation boundary between `tooling/ai-evals` and the material production route.

## 2. Failure mode

A superficially clean design could implement:

```text
EVAL PATH
provider SDK direct
+ prompt/harness A
+ config A

PRODUCTION PATH
ProviderAdapter
+ HarnessProfile B
+ feature/control transforms
+ config B
```

and then incorrectly claim:

```text
EVAL PASS
→ PRODUCTION ROUTE QUALIFIED
```

That is invalid whenever the difference is material to quality, semantics, privacy, safety, tool behavior, streaming, structured output, retry/fallback, or provider/data eligibility.

AI-04 whole-phase already established:

```text
EVAL CANDIDATE != PRODUCTION ROUTE
DIRECT EVAL != PRODUCTION CAPACITY QUALIFICATION
```

AI-05A must now make the build seam explicit.

## 3. BD-41 — Qualification must exercise the material production composition

```text
BD-41
QUALIFICATION EVIDENCE MUST EXERCISE THE SAME MATERIAL PRODUCTION
COMPOSITION THAT WILL BE PROMOTED, OR EVERY MATERIAL DELTA MUST BE
INDEPENDENTLY QUALIFIED BEFORE PROMOTION.
```

The material composition includes, where applicable:

```text
ModelTarget
HarnessProfile
ProviderBinding
ProviderAdapter / protocol translation
feature mode
structured-output/tool projection
security/guard transformations
data/egress controls
retry/fallback behavior material to the route
other behavior-bearing production transformations
```

The eval runner itself remains replaceable and outside the ordinary production request path.

```text
SAME MATERIAL COMPOSITION
!= SAME HTTP ENTRYPOINT
!= EVAL TOOLING INSIDE PRODUCTION REQUEST PATH
```

The goal is semantic/behavioral fidelity, not forcing evaluation traffic through the public product surface.

## 4. Bounded qualification seam

Candidate direction for AI-05B:

```text
tooling/ai-evals
        ↓
bounded qualification seam
        ↓
DANTE-owned production route composition
        ├ HarnessProfile
        ├ ProviderBinding
        ├ ProviderAdapter
        ├ material feature/control transforms
        └ route evidence identity
```

The qualification seam may invoke production-owned route components directly through a dedicated test/eval composition boundary. It must not fork a second provider integration stack whose behavior materially differs from production.

Application-state fixtures may still be synthetic/fake/minimized where DANTE semantics permit it. That does not authorize faking the exact provider/route behavior being qualified.

## 5. Delta qualification

Perfect identity is not always possible. A controlled eval may intentionally differ from production, for example by using:

```text
synthetic DANTE state
non-production account/project
a dedicated provider deployment
lower traffic/capacity envelope
safe test credentials
```

Such differences are acceptable only when they are classified.

```text
NON-MATERIAL DELTA
→ document why it cannot affect the promoted claim

MATERIAL DELTA
→ independent qualification required
   before production promotion
```

Examples of material deltas include:

```text
provider protocol/SDK translation
model snapshot/deployment
HarnessProfile behavior
provider feature mode
structured-output/tool semantics
context/security transformations
retry/fallback behavior
retention/data-processing posture
capacity/service-envelope behavior
```

## 6. Evidence identity / promotion record

A qualification result promoted toward production must identify the material route composition it supports, including as applicable:

```text
model/version/deployment
HarnessProfile revision
ProviderBinding revision
ProviderAdapter/protocol implementation revision
feature/control profile revisions
qualification fixture/suite revision
material delta list + delta evidence references
result / hard-failure status
```

```text
QUALIFICATION RECORD
!= RUNTIME CANONICAL STATE
!= BUSINESS AUDIT AUTHORITY
```

Initial durable home may be repository/CI engineering evidence rather than a runtime database.

## 7. Test-plane distinctions remain binding

```text
APPLICATION FAKE
!= PROVIDER ADAPTER CONFORMANCE
!= LIVE PROVIDER SMOKE / COMPATIBILITY PROOF
!= DIRECT DANTE MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

Their responsibilities are complementary:

```text
application fake
→ deterministic application semantics

adapter conformance
→ protocol/translation correctness

live smoke
→ current provider endpoint/feature compatibility

direct DANTE eval
→ DANTE workload quality + hard semantic/privacy/safety gates

production capacity qualification
→ intended service envelope / reliability / operational viability
```

No one layer inherits the proof claims of another.

## 8. Relationship to AI-04 / PRE-AI05

BD-41 is an implementation-boundary materialization of existing accepted rules; it does not create a new semantic owner.

It preserves:

```text
DANTE OWNS EVAL SEMANTICS
EVAL CANDIDATE != PRODUCTION ROUTE
HARNESSPROFILE != PROVIDERBINDING
PROVIDER SDK != APPLICATION CONTRACT
FEATURE AVAILABLE != FEATURE ELIGIBLE
QUALIFIED != CURRENTLY ELIGIBLE / AVAILABLE / ENTITLED
```

Provider/model selection remains OPEN.

## 9. Fresh retest required

AI-05A does not close from this document alone.

Rerun from zero:

```text
T01..T26
+
Search + Intelligence + provider outage
Search hidden-result + Ask synthesis
config rollout + invocation snapshot + emergency deny
quota admission + retry/failover + settlement
inline stream + disconnect + no durable Run
cumulative disclosure + zero-persistence envelope
direct eval + exact material production composition / qualified deltas
+
reverse AI-05A → AI-04 → PRE-AI05 → AI-03 → AI-02
```

PASS requires no unexplained ownership/proof gap and no qualification claim that outruns the composition actually tested.

## 10. Non-claims

```text
BD-41 MATERIALIZED                    YES
SECOND AI-05A PASS                    FAIL BOUNDED / BD-41
FRESH RETEST AFTER BD-41              NOT YET EXECUTED
AI-05A PASS/CLOSED                    NO
AI-05B STARTED                        NO
PROVIDER/MODEL/SDK SELECTED           NO
DIRECT PROVIDER EVAL EXECUTED         NO
PRODUCTION CAPACITY PASS              NO
IMPLEMENTATION                        NO
POSTGRESQL/ALEMBIC CHANGE             NO
```
