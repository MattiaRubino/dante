# `src/testing`

Owns reusable Mobile-specific test support after repeated test needs exist.

Potential future responsibilities:

- render/provider helpers;
- deterministic fixtures/builders;
- fake platform adapters;
- navigation harnesses;
- stable E2E identifiers/constants;
- test clocks or controlled environment seams when justified.

## Rules

- production business logic never lives here;
- do not mirror the production tree just for symmetry;
- prefer local test helpers until real reuse appears;
- avoid fixtures that encode false canonical domain assumptions;
- manual/device validation evidence remains separate from automated test fixtures.

This README establishes ownership only; additional test infrastructure is created when the first real Mobile feature requires it.