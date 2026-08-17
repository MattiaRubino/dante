<!-- LIFEOS-CANONICAL-CONTINUATION document="participation-v0-validation.md" follows="participation-v0-validation-part-2.md" -->
> **Canonical continuation of the single logical Participation v0 validation checkpoint.** Earlier validation remains preserved; this physical continuation records Collective / Membership downstream resolution only.

# 2026-08-16 — Collective / Membership downstream resolution

Collective v0 resolves the previously deferred distinction between a true collective participant and several individual participants.

Current rules:

```text
Collective may participate
YES, where Collective is the true bounded participant

Membership != Participation
member != participant automatically
participant != member automatically
participant set != Collective automatically
Collective Participation != every member participated
```

Representative regression:

```text
Committee C attends external hearing as institutional participant
Anna and Luca are members
Sara, a non-member adviser, also attends
```

The model can represent:

```text
Participation(C)
Participation(Sara)
Membership(Anna,C)
Membership(Luca,C)
```

without fabricating Anna/Luca attendance or Sara membership.

Re-test results:

```text
CORE-03 reductio           PASS WITH HARDENING
CORE-04 redundancy         PASS WITH HARDENING
CORE-05 traceability       PASS
MA-02 shared fact          PASS WITH HARDENING
MA-09 external participant PASS
MA-20 attribution          PASS WITH HARDENING
XCON-01 identity           PASS
XCON-04 relationships      PASS WITH HARDENING
```

Participation v0 remains **PASS WITH HARDENING; REOPEN = 0; UNCLASSIFIED = 0**.

Normative references:

- `../concepts/collective.md`;
- `../concepts/membership.md`;
- `../concepts/participation-part-5.md`;
- `collective-membership-quorum-v0-validation.md`.
