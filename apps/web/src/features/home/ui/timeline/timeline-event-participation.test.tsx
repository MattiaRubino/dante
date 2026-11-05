// @vitest-environment jsdom
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import { TimelineEventParticipation } from './timeline-event-participation';

const listExpectedParticipation = vi.fn();
const listPersonReferents = vi.fn();
let invalidate: (() => void) | null = null;

vi.mock('../../../temporal/remote-responsibility-data-source', () => ({
  createRemoteTemporalResponsibilityDataSource: () => ({
    listExpectedParticipation,
    listPersonReferents,
  }),
}));
vi.mock('../../../temporal/timeline-invalidation', () => ({
  subscribeTemporalTimelineInvalidation: (read: () => void) => {
    invalidate = read;
    return () => {
      invalidate = null;
    };
  },
}));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  invalidate = null;
});

it('shows Event participants and refreshes after a timeline invalidation', async () => {
  listPersonReferents.mockResolvedValue([
    { personRef: 'person-1', displayLabel: 'Ada' },
  ]);
  listExpectedParticipation
    .mockResolvedValueOnce([
      {
        participantPersonRef: 'person-1',
        participantIsSelf: false,
        requirementCode: 'required',
      },
    ])
    .mockResolvedValueOnce([
      {
        participantPersonRef: 'person-1',
        participantIsSelf: false,
        requirementCode: 'optional',
      },
    ]);
  render(<TimelineEventParticipation eventRef="event-1" />);
  expect(await screen.findByText('Ada')).toBeTruthy();
  expect(screen.getByText('Richiesto')).toBeTruthy();
  invalidate?.();
  await waitFor(() => expect(screen.getByText('Opzionale')).toBeTruthy());
});
