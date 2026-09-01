export type WorldFocusModuleRegistration<Kind extends string = string> = Readonly<{
  kind: Kind;
}>;

/**
 * Finite, deterministic presentation registry foundation. Real module
 * registrations later add validators/renderers/presentation profiles while
 * retaining duplicate-kind fail-fast and unknown-kind fail-safe behavior.
 */
export class WorldFocusModuleRegistry<
  Registration extends WorldFocusModuleRegistration,
> {
  readonly #byKind: ReadonlyMap<string, Registration>;
  readonly kinds: readonly Registration['kind'][];

  constructor(registrations: readonly Registration[]) {
    const byKind = new Map<string, Registration>();
    const kinds: Registration['kind'][] = [];

    for (const registration of registrations) {
      const kind = registration.kind.trim();
      if (kind.length === 0) {
        throw new Error('World Focus module kind must not be empty');
      }
      if (byKind.has(kind)) {
        throw new Error(`Duplicate World Focus module kind: ${kind}`);
      }

      byKind.set(kind, registration);
      kinds.push(registration.kind);
    }

    this.#byKind = byKind;
    this.kinds = Object.freeze(kinds.slice());
  }

  resolve(kind: string): Registration | null {
    return this.#byKind.get(kind) ?? null;
  }

  has(kind: string): boolean {
    return this.#byKind.has(kind);
  }
}
