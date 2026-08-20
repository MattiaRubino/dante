# DANTE Access — current checkpoint

- Status: **A3.4 SELECTED / APPROVED REVIEW CHECKPOINT**
- Date: **2026-08-20**
- Branch: `prototype/access-system`
- Production frontend: **not started here**
- Backend auth/session contract: **not frozen here**

## Selected artifact

```text
review artifact
DANTE Access A3.4 — strong corner mark

size
93897 bytes

SHA-256
b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
```

Exact recoverable archive:

`prototypes/frontend/access/archive/a3-4-approved-2026-08-20/`

The raw standalone is intentionally preserved through a hash-verified XZ/Base64 archive because the repository connector used during review has a payload-size limit. `restore.py` reconstructs the exact HTML bytes.

## Why A3.4 is selected

A3.1 established the approved functional/visual Access system and direct DANTE-owned account-creation flow. A3.4 adds the selected desktop brand treatment: a larger, more visible but still muted crop of the locked Living Orbits symbol on the left brand stage.

A3.5 tested the symbol at full opacity and was rejected as too strong. A3.4 is therefore the selected balance.

## Browser QA

Fresh local Chromium QA against the exact selected artifact:

```text
default sign-in                         PASS
DANTE signup email → password          PASS
password → email verification          PASS
verification → setup                   PASS
Italian / English switching            PASS
18 declared screens render             PASS
reauth overlay                          PASS
mobile 390×844 brand stage hidden      PASS
browser page errors                     0
corner mark desktop opacity             0.22
```

QA record:

`prototypes/frontend/access/archive/a3-4-approved-2026-08-20/qa.json`

## Accepted product/UX boundary

The checkpoint includes:

- Google / Apple / DANTE email-password entry routes;
- DANTE-owned staged account creation;
- email verification UX;
- neutral recovery/reset UX;
- provider pending/error/account-linking states;
- session-expired re-auth overlay;
- IT/EN selector;
- lightweight preferred-name + locale/time-zone setup;
- first-run choice: real item / import / isolated demo / skip;
- handoff mock toward Home.

It does not freeze:

- API routes;
- DB/auth schema;
- provider linking implementation;
- session/token format/lifetime;
- exact OTP implementation/lifetime;
- final backend password policy;
- production React/framework/form/auth libraries;
- canonical Home implementation.

## Previous checkpoints

- A3 — archived research/review baseline before direct-sign-up refinement.
- A3.1 — approved direct-sign-up baseline before corner-mark experiments.
- A3.4 — **current selected review checkpoint**.

## Next boundary

Fine visual/microcopy details may be revisited during production React/frontend implementation or when real backend responses exist. Until then, A3.4 is the restore/reference artifact for Access.
