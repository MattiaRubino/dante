# `src/ui`

Owns reusable DANTE Mobile visual and interaction primitives.

## Allowed

- typography and layout primitives;
- surfaces/cards/buttons/headers when repeated real usage exists;
- theme adapters;
- loading/empty/error presentation primitives;
- reusable motion primitives with clear semantic purpose;
- accessibility behavior intrinsic to reusable controls.

## Not allowed

- feature workflows;
- HTTP/storage ownership;
- canonical domain logic;
- copies of Web implementation components;
- speculative mega component libraries.

Use shared semantic design tokens where available, while keeping the renderer and interaction implementation Mobile-specific.

Feature-specific components stay with the feature until repeated cross-feature use proves that moving them here is the cleaner boundary.