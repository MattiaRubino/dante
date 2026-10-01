// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { TimelineEvent, TimelineGroup } from './model/timeline-types';
import { EventDetailDialog, detailFromEvent } from './timeline-overlays';

vi.mock('../../../temporal/actual-realization-controls', () => ({
  ActualRealizationControls: ({ kind, subjectRef }: { kind: string; subjectRef: string }) => (
    <div data-testid="reality-controls">{`${kind}:${subjectRef}`}</div>
  ),
}));

vi.mock('../../../temporal/session-subject-controls', () => ({
  SessionSubjectControls: ({ kind, subjectRef }: { kind: string; subjectRef: string }) => (
    <div data-testid="session-controls">{`${kind}:${subjectRef}`}</div>
  ),
}));

vi.mock('../../../temporal/responsibility-controls', () => ({
  ResponsibilityControls: () => null,
}));

vi.mock('../../../temporal/schedule-reminder-controls', () => ({
  ScheduleReminderControls: () => null,
}));

vi.mock('./timeline-event-agenda-editor', () => ({
  TimelineEventAgendaEditor: () => null,
}));

const ACTIVITY_REF = '0199a111-1111-7111-8111-111111111111';
const EVENT_REF = '0199a222-2222-7222-8222-222222222222';
const OCCURRENCE_REF = '0199a333-3333-7333-8333-333333333333';
const SCHEDULE_REF = '0199a444-4444-7444-8444-444444444444';
const STATE_REF = '0199a555-5555-7555-8555-555555555555';

const groups: readonly TimelineGroup[] = [
  {
    id: 'personale',
    label: 'Personale',
    tone: 'personal',
  },
];

function baseEvent(): Omit<TimelineEvent, 'canonicalBasis'> {
  return {
    id: SCHEDULE_REF,
    startMinute: 600,
    endMinute: 660,
    title: 'Soggetto canonico',
    groupId: 'personale',
  };
}

afterEach(() => cleanup());

describe('Timeline post-create runtime destinations', () => {
  it('derives B10 subjects for Activity, Event and Occurrence independently from Session', () => {
    const activity = detailFromEvent(
      {
        ...baseEvent(),
        canonicalBasis: {
          kind: 'scheduled-activity',
          activityRef: ACTIVITY_REF,
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: STATE_REF,
          placement: {
            kind: 'coarse-local-period',
            localDate: { toString: () => '2026-10-01' } as never,
            period: 'afternoon',
          },
        },
      },
      groups,
    );
    const event = detailFromEvent(
      {
        ...baseEvent(),
        canonicalBasis: {
          kind: 'scheduled-event',
          eventRef: EVENT_REF,
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: STATE_REF,
          placement: {
            kind: 'coarse-local-period',
            localDate: { toString: () => '2026-10-01' } as never,
            period: 'afternoon',
          },
        },
      },
      groups,
    );
    const occurrence = detailFromEvent(
      {
        ...baseEvent(),
        canonicalBasis: {
          kind: 'scheduled-occurrence',
          occurrenceRef: OCCURRENCE_REF,
          sourceKind: 'routine',
          sourceNativeRef: ACTIVITY_REF,
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: STATE_REF,
          placement: {
            kind: 'coarse-local-period',
            localDate: { toString: () => '2026-10-01' } as never,
            period: 'afternoon',
          },
        },
      },
      groups,
    );

    expect(activity.realitySubject).toEqual({ kind: 'activity', ref: ACTIVITY_REF });
    expect(event.realitySubject).toEqual({ kind: 'event', ref: EVENT_REF });
    expect(occurrence.realitySubject).toEqual({
      kind: 'occurrence',
      ref: OCCURRENCE_REF,
    });
  });

  it('mounts B10 reality controls on the post-create detail without requiring B08 Session controls', () => {
    render(
      <EventDetailDialog
        detail={{
          title: 'Attività senza Session runtime aperto',
          startMinute: 600,
          endMinute: 660,
          groupLabel: 'Personale',
          meta: '',
          ownerKind: 'activity',
          realitySubject: { kind: 'activity', ref: ACTIVITY_REF },
        }}
        opener={null}
        canUnschedule={false}
        pending={false}
        sessionSubject={null}
        onUnschedule={() => undefined}
        onClose={() => undefined}
      />,
    );

    expect(screen.getByTestId('reality-controls').textContent).toBe(
      `activity:${ACTIVITY_REF}`,
    );
    expect(screen.queryByTestId('session-controls')).toBeNull();
  });
});
