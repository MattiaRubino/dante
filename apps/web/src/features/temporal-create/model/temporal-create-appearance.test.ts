import { describe, expect, it } from 'vitest';

import {
  createTemporalCreateFields,
  createTemporalCreateSession,
  setTemporalCreateSurface,
  updateTemporalCreateFields,
} from './temporal-create-session';

describe('Temporal Create appearance intent', () => {
  it('inherits Context tone by default without changing Context identity', () => {
    const fields = createTemporalCreateFields({ contextId: 'focus' });

    expect(fields.contextId).toBe('focus');
    expect(fields.appearanceTone).toBeNull();
  });

  it('preserves a presentation-only override across Quick, Expanded and Full surfaces', () => {
    const initial = createTemporalCreateSession(
      createTemporalCreateFields({
        title: 'Deep work override',
        contextId: 'focus',
      }),
    );
    const overridden = updateTemporalCreateFields(initial, {
      appearanceTone: 'urgent',
    });
    const expanded = setTemporalCreateSurface(overridden, 'expanded');
    const full = setTemporalCreateSurface(expanded, 'full');
    const compact = setTemporalCreateSurface(full, 'quick');
    const reopened = setTemporalCreateSurface(compact, 'expanded');

    expect(reopened.draft.current.contextId).toBe('focus');
    expect(reopened.draft.current.appearanceTone).toBe('urgent');
    expect(reopened.draft.dirty).toBe(true);
  });

  it('can return to inherited appearance without mutating the owning Context', () => {
    const initial = createTemporalCreateSession(
      createTemporalCreateFields({ contextId: 'salute' }),
    );
    const overridden = updateTemporalCreateFields(initial, {
      appearanceTone: 'creative',
    });
    const inherited = updateTemporalCreateFields(overridden, {
      appearanceTone: null,
    });

    expect(overridden.draft.current.contextId).toBe('salute');
    expect(overridden.draft.current.appearanceTone).toBe('creative');
    expect(inherited.draft.current.contextId).toBe('salute');
    expect(inherited.draft.current.appearanceTone).toBeNull();
    expect(inherited.draft.dirty).toBe(false);
  });
});
