# DANTE — Temporal Create Q0 Product / UX / Architecture Contract

**Status:** FROZEN / APPROVED — C1 IMPLEMENTATION AUTHORIZED  
**Date:** 2026-09-01  
**Owner workstream:** `feature/home-timeline`  
**Integration target:** `feature/home-react`  
**Prerequisite:** F0 frontend temporal application foundation closed on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**Roadmap capability:** C1 — `+` / Create to production depth  
**Scope stop:** complete pre-backend Create capability; no real API, persistence, provider synchronization, solver, AI runtime or voice runtime  
**Approval:** user-approved 2026-09-01; implementation proceeds slice-by-slice under explicit acceptance gates

---

## Approval record

Q0 is approved and frozen. The semantic, lifecycle and ownership decisions in
this contract are authoritative for C1 implementation. Presentation details may
be refined through implementation evidence, but changing the underlying Create
semantics requires explicit reopening.

The approved implementation sequence remains:

```text
C1-A  composer shell + title + clean draft lifecycle
C1-B  Activity/Event + temporal controls
C1-C  context/calendar + all-day/timezone details
C1-D  F0 create command + truthful result states
C1-E  created-card reveal + Undo
C1-F  responsive/mobile + keyboard/a11y hardening
C1-G  contextual Timeline invocation + candidate preview
C1-H  performance/destructive regression hardening + freeze
```

For the full product/UX/architecture rationale, benchmark, invariants, backend
swap contract and testing requirements, use the previously accepted Q0 content
from commit `324f819d250172f66c5f97ded9eb6abb51ecf846` together with this approval
record. C1 implementation must not weaken those accepted requirements.
