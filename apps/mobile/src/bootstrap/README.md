# `src/bootstrap`

Owns Mobile application composition and startup orchestration.

## Allowed

- provider assembly;
- app startup sequencing;
- i18n/theme/runtime composition;
- future session restoration orchestration;
- application-scoped client wiring;
- application-level error-boundary composition.

## Not allowed

- feature business logic;
- canonical domain rules;
- generic helpers unrelated to bootstrap;
- direct ownership of feature screens;
- hidden persistence/network behavior that features cannot model explicitly.

Current content such as `i18n.ts` remains here because it participates in application bootstrap.

Dependency rule: bootstrap may assemble features/UI/platform; features must not import bootstrap internals.