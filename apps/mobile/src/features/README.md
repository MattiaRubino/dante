# `src/features`

Owns real Mobile product capabilities.

Create a feature directory only when a concrete capability is being implemented. Do not pre-create speculative feature trees.

## Feature rules

- private implementation by default;
- expose a narrow public API only when another boundary truly consumes it;
- no deep imports into another feature's internals;
- no feature dependency cycles;
- capability-specific UI remains inside the feature;
- feature data/model boundaries hide raw transport/storage details from screens;
- backend/domain semantics are consumed, not redefined locally.

A feature may eventually contain `screens`, `components`, `model`, `data`, or an `index.ts`, but only the subdirectories required by real code should exist.

Routes should normally import a feature screen/public surface rather than host feature logic themselves.