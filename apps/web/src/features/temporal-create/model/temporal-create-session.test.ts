import { describe, expect, it } from 'vitest';

import {
  continueTemporalCreateEditing,
  createTemporalCreateSession,
  discardTemporalCreateSession,
  requestTemporalCreateClose,
  updateTemporalCreateTitle,
} from './temporal-create-session';

describe('temporal create session', () => {
  it('starts with a clean title draft', () => {
    const session = createTemporalCreateSession();

    expect(session.closeDecision).toBe('none');
    expect(session.draft.current.title).toBe('');
    expect(session.draft.dirty).toBe(false);
    expect(session.draft.editRevision).toBe(0);
  });

  it('marks title edits dirty and returning to baseline clean', () => {
    const initial = createTemporalCreateSession();
    const edited = updateTemporalCreateTitle(initial, 'Allenamento');
    const restored = updateTemporalCreateTitle(edited, '');

    expect(edited.draft.current.title).toBe('Allenamento');
    expect(edited.draft.dirty).toBe(true);
    expect(edited.draft.editRevision).toBe(1);
    expect(restored.draft.dirty).toBe(false);
    expect(restored.draft.editRevision).toBe(2);
  });

  it('closes a clean session without a discard decision', () => {
    const session = createTemporalCreateSession();
    const request = requestTemporalCreateClose(session);

    expect(request.shouldClose).toBe(true);
    expect(request.session).toBe(session);
  });

  it('protects a dirty title behind an explicit discard decision', () => {
    const edited = updateTemporalCreateTitle(
      createTemporalCreateSession(),
      'Studiare inglese',
    );
    const request = requestTemporalCreateClose(edited);

    expect(request.shouldClose).toBe(false);
    expect(request.session.closeDecision).toBe('confirm-discard');
    expect(request.session.draft.current.title).toBe('Studiare inglese');
    expect(request.session.draft.dirty).toBe(true);
  });

  it('continues editing without losing the dirty draft', () => {
    const edited = updateTemporalCreateTitle(
      createTemporalCreateSession(),
      'Scrivere una canzone',
    );
    const protectedSession = requestTemporalCreateClose(edited).session;
    const resumed = continueTemporalCreateEditing(protectedSession);

    expect(resumed.closeDecision).toBe('none');
    expect(resumed.draft.current.title).toBe('Scrivere una canzone');
    expect(resumed.draft.dirty).toBe(true);
  });

  it('discard creates a fresh clean session', () => {
    const discarded = discardTemporalCreateSession();

    expect(discarded.closeDecision).toBe('none');
    expect(discarded.draft.current.title).toBe('');
    expect(discarded.draft.dirty).toBe(false);
    expect(discarded.draft.editRevision).toBe(0);
  });
});
