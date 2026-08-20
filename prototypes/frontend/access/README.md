# DANTE Access prototypes

Status: **approved cross-platform pre-implementation review workspace**.

Access uses one semantic system with separate visual/behavior oracles for desktop and mobile.

## Current authorities

### Desktop — A3.4

```text
archive    archive/a3-4-approved-2026-08-20/
size       93897 bytes
SHA-256    b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
status     APPROVED DESKTOP REVIEW ORACLE
```

Restore:

```bash
cd prototypes/frontend/access/archive/a3-4-approved-2026-08-20
python restore.py
```

### Mobile — M1.2 + PRG-0

```text
archive    archive/mobile-m1-2-approved-2026-08-20/
size       107010 bytes
SHA-256    2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
status     APPROVED MOBILE REVIEW ORACLE / PRODUCTION-READY SPECIFICATION
```

Restore:

```bash
cd prototypes/frontend/access/archive/mobile-m1-2-approved-2026-08-20
python restore.py
```

## Documentation authority

- `docs/frontend/access/contract.md`
- `docs/frontend/access/state-model.md`
- `docs/frontend/access/current-checkpoint.md`
- `docs/frontend/access/benchmark-2026-08-20.md`
- `docs/frontend/access/mobile-technical-contract.md`
- `docs/frontend/access/mobile-research-matrix.md`
- `docs/frontend/access/mobile-production-readiness.md`
- `docs/frontend/access/mobile-qa.md`

## Important boundaries

These coded artifacts are UX/behavior/security-contract oracles. They do not imply:

- production provider calls;
- implemented backend AuthN/AuthZ;
- final API route/DTO/token design;
- React/component architecture;
- native Keychain/Keystore integration;
- real App/Universal Link association;
- real Play Integrity/App Attest integration;
- canonical Home implementation.

Production code should migrate semantic states, locale keys, interaction outcomes, capability/security requirements and release gates. It should **not** mechanically reproduce the standalone HTML DOM.

Earlier A3/A3.1 archives remain historical restore evidence. A3.5 remains rejected. The immutable A3.4 archive retains its historical 15+ password copy; future implementation uses the approved M1.2/shared-locale 12+ V1 policy.
