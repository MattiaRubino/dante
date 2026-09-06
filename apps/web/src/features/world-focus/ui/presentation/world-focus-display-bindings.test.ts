import { describe, expect, it } from 'vitest';

import {
  createWorldFocusDisplayBinding,
  createWorldFocusDisplayBindingSet,
  requireWorldFocusDisplayBinding,
} from './world-focus-display-bindings';

describe('World Focus M2 display bindings', () => {
  it('normalizes a display-safe label while preserving the exact semantic reference', () => {
    const binding = createWorldFocusDisplayBinding({
      reference: { kind: 'project', key: 'neon-static' },
      label: '  Neon Static  ',
      supportingText: '  Release · Master v3  ',
    });

    expect(binding).toEqual({
      reference: { kind: 'project', key: 'neon-static' },
      label: 'Neon Static',
      supportingText: 'Release · Master v3',
    });
    expect(Object.isFrozen(binding)).toBe(true);
    expect(Object.isFrozen(binding.reference)).toBe(true);
  });

  it('fails closed on blank user-facing labels instead of falling back to raw reference keys', () => {
    expect(() =>
      createWorldFocusDisplayBinding({
        reference: { kind: 'project', key: 'internal-project-42' },
        label: '   ',
      }),
    ).toThrow(/label/i);
  });

  it('rejects duplicate semantic references and resolves only exact kind/key matches', () => {
    const set = createWorldFocusDisplayBindingSet([
      { reference: { kind: 'project', key: 'a' }, label: 'A' },
      { reference: { kind: 'project', key: 'b' }, label: 'B' },
    ]);

    expect(
      requireWorldFocusDisplayBinding(set, { kind: 'project', key: 'b' }).label,
    ).toBe('B');
    expect(() =>
      requireWorldFocusDisplayBinding(set, { kind: 'task', key: 'b' }),
    ).toThrow(/display binding/i);

    expect(() =>
      createWorldFocusDisplayBindingSet([
        { reference: { kind: 'project', key: 'same' }, label: 'One' },
        { reference: { kind: 'project', key: 'same' }, label: 'Two' },
      ]),
    ).toThrow(/duplicate/i);
  });
});
