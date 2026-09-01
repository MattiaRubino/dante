import type { ReactNode } from 'react';

import type { WorldFocusSurfaceDescriptor } from '../model/world-focus-workspace';

export type WorldFocusSurfaceRendererProps<Kind extends string = string> = Readonly<{
  surface: WorldFocusSurfaceDescriptor<Kind>;
  isCurrentGeneration: boolean;
  onRequestClose: () => void;
}>;

export type WorldFocusSurfaceRegistration<Kind extends string = string> = Readonly<{
  kind: Kind;
  render: (props: WorldFocusSurfaceRendererProps<Kind>) => ReactNode;
}>;

/**
 * Finite presentation registry for transient/deeper World workspace surfaces.
 *
 * The registry is deliberately local and executable only from code shipped by
 * DANTE. Unknown future kinds fail locally; remote/model-generated executable
 * UI never enters this boundary.
 */
export class WorldFocusSurfaceRegistry<
  Registration extends WorldFocusSurfaceRegistration,
> {
  readonly #byKind: ReadonlyMap<string, Registration>;
  readonly kinds: readonly Registration['kind'][];

  constructor(registrations: readonly Registration[]) {
    const byKind = new Map<string, Registration>();
    const kinds: Registration['kind'][] = [];

    for (const registration of registrations) {
      const kind = registration.kind.trim();
      if (kind.length === 0) {
        throw new Error('World Focus surface kind must not be empty');
      }
      if (byKind.has(kind)) {
        throw new Error(`Duplicate World Focus surface kind: ${kind}`);
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
