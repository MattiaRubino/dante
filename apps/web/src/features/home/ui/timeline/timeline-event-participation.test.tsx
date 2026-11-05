// @vitest-environment jsdom
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import { TimelineEventParticipation } from './timeline-event-participation';

const listExpectedParticipation = vi.fn();
const listOccurrenceExpectedParticipation = vi.fn();
const listPersonReferents = vi.fn();
const invalidation: { read: (() => void) | null } = { read: null };

vi.mock('../../../temporal/remote-responsibility-data-source', () => ({
  createRemoteTemporalResponsibilityDataSource: () => ({
    listExpectedParticipation,
    listOccurrenceExpectedParticipation,
    listPersonReferents,
  }),
}));
vi.mock('../../../temporal/timeline-invalidation', () => ({
  subscribeTemporalTimelineInvalidation: (read: () => void) => {
    invalidation.read = read;
    return () => {
      invalidation.read = null;
    };
  },
}));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  invalidation.read = null;
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
    ])
    .mockResolvedValueOnce([]);
  render(<TimelineEventParticipation eventRef="event-1" />);
  expect(await screen.findByText('Ada')).toBeTruthy();
  expect(screen.getByText('Richiesto')).toBeTruthy();
  invalidation.read?.();
  await waitFor(() => expect(screen.getByText('Opzionale')).toBeTruthy());
  invalidation.read?.();
  await waitFor(() => expect(screen.queryByText('Ada')).toBeNull());
});

it('reads the selected recurring instance policy rather than the current Event source', async () => {
  listPersonReferents.mockResolvedValue([
    { personRef: 'person-1', displayLabel: 'Ada' },
  ]);
  listOccurrenceExpectedParticipation.mockResolvedValue([
    {
      participantPersonRef: 'person-1',
      participantIsSelf: false,
      requirementCode: 'optional',
    },
  ]);
  render(
    <TimelineEventParticipation
      eventRef="event-1"
      occurrenceRef="occurrence-1"
    />,
  );
  expect(await screen.findByText('Ada')).toBeTruthy();
  expect(screen.getByText('Opzionale')).toBeTruthy();
  expect(listOccurrenceExpectedParticipation).toHaveBeenCalledWith('occurrence-1');
  expect(listExpectedParticipation).not.toHaveBeenCalled();
});
