import { describe, expect, it, vi } from 'vitest';

import {
  createRemoteRecurringSeriesEdit,
  type RecurringSeriesReview,
} from './remote-recurring-series-edit';

const SOURCE = '0199a111-1111-7111-8111-111111111111';
const FIRST = '0199a222-2222-7222-8222-222222222222';
const NEXT = '0199a333-3333-7333-8333-333333333333';
const OLD_STATE = '0199a444-4444-7444-8444-444444444444';
const NEW_STATE = '0199a555-5555-7555-8555-555555555555';

const intent = {
  selectedRef: FIRST,
  source: {
    sourceRef: SOURCE,
    owner: 'event' as const,
    selectedDate: '2026-11-10',
    editRevision: 2,
    recurrenceStateRef: OLD_STATE,
    title: 'Evento con un titolo abbastanza lungo e una scaletta',
    description: null,
    location: null,
    colorCode: null,
    recurrence: { pattern_code: 'daily' },
    structure: { agenda_parts: ['Primo punto della scaletta'] },
  },
  scope: 'this_and_following' as const,
  recurrence: { pattern_code: 'daily' },
  structure: { agenda_parts: ['Scaletta aggiornata'] },
  profilePatch: { title: 'Evento con titolo lungo modificato nella serie' },
  operationId: 'first-event-regression',
};

const review: RecurringSeriesReview = {
  fingerprint: 'a'.repeat(64),
  targetRefs: [FIRST, NEXT],
  newExpectedCount: 2,
  protected: [],
};

function remoteWithAcceptedCount(
  count: number,
  preservedRef: string | null = null,
  overrides: Record<string, unknown> = {},
) {
  const fetchFn = vi.fn<typeof fetch>()
    .mockResolvedValueOnce(
      Response.json({ authenticated: true, csrf_token: 'test-csrf' }),
    )
    .mockResolvedValueOnce(
      Response.json({
        source_native_ref: SOURCE,
        recurrence_state_ref: NEW_STATE,
        superseded_count: count,
        protected_count: 0,
        preserved_occurrence_ref: preservedRef,
        replayed: false,
        ...overrides,
      }),
    );
  return createRemoteRecurringSeriesEdit(fetchFn);
}

describe('Converted first Event series confirmation', () => {
  it('accepts the physical first Event preserved by the backend', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST).accept(intent, review))
      .resolves.toBeUndefined();
  });

  it('accepts the ordinary case when all targets are superseded', async () => {
    await expect(remoteWithAcceptedCount(2).accept(intent, review))
      .resolves.toBeUndefined();
  });

  it('accepts the idempotent replay with the same first identity', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST, {
      replayed: true,
    }).accept(intent, review)).resolves.toBeUndefined();
  });

  it('rejects an unrelated preserved Occurrence', async () => {
    await expect(remoteWithAcceptedCount(1, NEW_STATE).accept(intent, review))
      .rejects.toThrow('Conferma della serie non coerente.');
  });

  it('rejects falsely preserving the following Occurrence', async () => {
    await expect(remoteWithAcceptedCount(1, NEXT).accept(intent, review))
      .rejects.toThrow('Conferma della serie non coerente.');
  });

  it('rejects preserved-first metadata for from-next', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST).accept(
      { ...intent, scope: 'from_next' }, review,
    )).rejects.toThrow('Conferma della serie non coerente.');
  });

  it('rejects preserved-first metadata for Routine', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST).accept(
      { ...intent, source: { ...intent.source, owner: 'routine' } }, review,
    )).rejects.toThrow('Conferma della serie non coerente.');
  });

  it('rejects a wrong supersession count despite valid identity', async () => {
    await expect(remoteWithAcceptedCount(2, FIRST).accept(intent, review))
      .rejects.toThrow('Conferma della serie non coerente.');
  });

  it('rejects missing preservation metadata', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST, {
      preserved_occurrence_ref: undefined,
    }).accept(intent, review)).rejects.toThrow(
      'Conferma della serie non coerente.',
    );
  });

  it('rejects a protected-count mismatch', async () => {
    await expect(remoteWithAcceptedCount(1, FIRST, {
      protected_count: 1,
    }).accept(intent, review)).rejects.toThrow(
      'Conferma della serie non coerente.',
    );
  });
});
