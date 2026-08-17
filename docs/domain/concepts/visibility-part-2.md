<!-- LIFEOS-CANONICAL-CONTINUATION document="visibility.md" follows="visibility.md" -->
> **Canonical continuation of `visibility.md`.** The accepted Visibility v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource planning visibility boundary

Resource Requirement / Allocation v0 confirms that resource-planning visibility has several independently governed surfaces:

```text
Requirement visibility
Candidate Set visibility
Allocation result visibility
provider identity/details visibility
private qualification / matching basis visibility
Capacity Claim visibility
Allocation history/rationale visibility
Actual use visibility
```

None is automatically implied by another.

A shared/authorized result may expose:

```text
Allocated provider: Anna
```

while keeping private:

- Anna's detailed availability reason;
- private qualification Evidence;
- ranking inputs;
- health/family constraints;
- hidden alternative candidates;
- sensitive Provenance.

Therefore:

```text
Allocation visible
!= candidate set visible
!= Requirement details visible
!= matching basis visible
!= private source visible
```

Likewise being selected as a Resource does not itself grant visibility to the Requirement, other candidates, rationale or shared context.

AI may use authorized private context for matching, but access/reasoning does not create disclosure permission or justify leaking private eligibility basis in explanations.

Visibility v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.