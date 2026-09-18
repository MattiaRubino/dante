# `src/platform`

Owns Mobile integrations whose behavior is inherently native, device-specific, or OS-specific.

Potential future responsibilities include secure storage, permissions, notifications, deep-link/native-intent adaptation, lifecycle/device signals, haptics, background execution and Android/iOS-specific behavior.

## Rules

- expose narrow capability-oriented adapters to features;
- contain `Platform.OS` branching where practical instead of spreading it through feature code;
- keep platform state noncanonical unless the product contract explicitly says otherwise;
- do not hide security-relevant behavior behind generic utility functions;
- platform-specific files (`*.android.ts`, `*.ios.ts`) are appropriate when implementations genuinely differ;
- do not install native dependencies until a real capability requires them and the dependency scope is approved.

This directory is not a generic `services` layer.