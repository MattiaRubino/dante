// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { TimelineEvent, TimelineGroup } from './model/timeline-types';
import {
  EventDetailDialog,
  detailFromEvent,
  inspectorAppearanceForEvent,
} from './timeline-overlays';
import { fetchRequestUrl } from '../../../../test-support/fetch-request';

vi.mock('../../../temporal/actual-realization-controls', () => ({
  ActualRealizationControls: ({
    kind,
    subjectRef,
  }: {
    kind: string;
    subjectRef: string;
  }) => <div data-testid="reality-controls">{`${kind}:${subjectRef}`}</div>,
}));

vi.mock('./timeline-inspector-reality', () => ({
  TimelineInspectorReality: ({
    kind,
    subjectRef,
  }: {
    kind: string;
    subjectRef: string;
  }) => <div data-testid="reality-controls">{`${kind}:${subjectRef}`}</div>,
}));

vi.mock('../../../temporal/session-subject-controls', () => ({
  SessionSubjectControls: ({
    kind,
    subjectRef,
  }: {
    kind: string;
    subjectRef: string;
  }) => <div data-testid="session-controls">{`${kind}:${subjectRef}`}</div>,
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

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('Timeline post-create runtime destinations', () => {
  it('anchors the Inspector beside the card without a dimming backdrop and truncates its title', () => {
    const opener = document.createElement('button');
    const card = document.createElement('article');
    card.dataset.timelineEvent = SCHEDULE_REF;
    card.append(opener);
    document.body.append(card);
    card.getBoundingClientRect = () => ({
      left: 100,
      right: 300,
      top: 120,
      bottom: 200,
      width: 200,
      height: 80,
      x: 100,
      y: 120,
      toJSON: () => ({}),
    });
    const close = vi.fn();
    render(
      <EventDetailDialog
        detail={{
          title: 'X'.repeat(400),
          startMinute: 600,
          endMinute: 660,
          groupLabel: 'Personale',
        }}
        opener={opener}
        onClose={close}
      />,
    );
    const dialog = screen.getByRole('dialog');
    expect(dialog.getAttribute('aria-modal')).toBe('true');
    expect(dialog.style.left).toBe('312px');
    expect(dialog.style.top).toBe('120px');
    expect(dialog.closest('.timeline-modal-backdrop--inspector')).toBeTruthy();
    expect(document.body.style.overflow).toBe('hidden');
    expect(document.body.firstElementChild?.hasAttribute('inert')).toBe(true);
    fireEvent.pointerDown(
      dialog.closest('.timeline-modal-backdrop--inspector')!,
    );
    expect(close).toHaveBeenCalledOnce();
    card.remove();
  });

  it('shows the planned calendar date and Life Area beneath the unchanged action bar without a timezone label', () => {
    render(
      <EventDetailDialog
        detail={{
          title: 'Scrivere',
          dateKey: '2026-10-18',
          startMinute: 870,
          endMinute: 900,
          groupLabel: 'Creatività',
          accentColorCode: '#80aaff',
        }}
        opener={null}
        locale="it-IT"
        timeZone="Europe/Rome"
        onClose={() => undefined}
      />,
    );
    const dialog = screen.getByRole('dialog');
    expect(screen.getByText('Domenica 18 Ottobre · 14:30–15:00')).toBeTruthy();
    expect(screen.getByRole('region', { name: 'Area' }).textContent).toContain(
      'Creatività',
    );
    expect(dialog.style.getPropertyValue('--timeline-inspector-accent')).toBe(
      '#80aaff',
    );
    expect(dialog.textContent).not.toContain('Europe/Rome');
    expect(
      dialog.querySelector('.timeline-event-modal__header-actions'),
    ).toBeTruthy();
  });

  it('reads the existing Activity description and places it after Objectives without duplicating the main Session row', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn<typeof fetch>((input) => {
        const url = fetchRequestUrl(input);
        if (url.endsWith('/profile')) {
          return Promise.resolve(
            Response.json({
              activity_ref: ACTIVITY_REF,
              title: 'Scrivere',
              description: 'Preparare la bozza.',
              location: 'Ufficio',
              color_code: null,
              revision: 1,
            }),
          );
        }
        if (url.endsWith('/children')) {
          return Promise.resolve(
            Response.json({
              parent_activity_ref: ACTIVITY_REF,
              schedules: [],
            }),
          );
        }
        return Promise.resolve(Response.json([]));
      }),
    );
    render(
      <EventDetailDialog
        detail={{
          title: 'Scrivere',
          startMinute: 870,
          endMinute: 900,
          groupLabel: 'Creatività',
          contextLabel: 'Elemento dell’attività Scrivere',
          ownerKind: 'activity',
          realitySubject: { kind: 'activity', ref: ACTIVITY_REF },
        }}
        opener={null}
        sessionSubject={{ kind: 'activity', ref: ACTIVITY_REF }}
        onClose={() => undefined}
      />,
    );
    const description = await screen.findByRole('region', {
      name: 'Descrizione',
    });
    expect(description.textContent).toContain('Preparare la bozza.');
    const inspector = screen.getByRole('dialog');
    const objectives = screen.getByTestId('reality-controls');
    const context = screen.getByRole('region', { name: 'Contesto' });
    const location = screen.getByRole('region', { name: 'Località' });
    expect(location.textContent).toContain('Ufficio');
    expect(
      location.compareDocumentPosition(description) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(description.firstElementChild?.textContent).toBe('Descrizione');
    expect(
      description.querySelector('.timeline-event-modal__description-body')
        ?.textContent,
    ).toBe('Preparare la bozza.');
    expect(
      inspector.querySelector('.timeline-event-modal__title-row')?.contains(context),
    ).toBe(false);
    expect(
      objectives.compareDocumentPosition(context) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      context.compareDocumentPosition(description) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(inspector.lastElementChild).toBe(description);
    expect(
      objectives.compareDocumentPosition(description) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      inspector.querySelectorAll('.timeline-activity-planned-sessions__row'),
    ).toHaveLength(0);
  });


  it('renders all Activity intervals ahead of Area and child Sessions', async () => {
    const fetchFn = vi.fn<typeof fetch>((input) => {
      const url = fetchRequestUrl(input);
      if (url.endsWith('/children')) {
        return Promise.resolve(Response.json({
          parent_activity_ref: ACTIVITY_REF,
          session_capture_mode: 'record',
          schedules: [
            {
              schedule_ref: 'envelope-technical',
              role_code: 'envelope',
              starts_local_at: '2026-11-20T09:00:00',
              ends_local_at: '2026-11-20T15:15:00',
            },
            {
              schedule_ref: 'interval-afternoon',
              role_code: 'interval',
              presentation_order: 2,
              temporal_form: 'named_zone_local',
              zone_id: 'Europe/Rome',
              resolved_start_at: '2026-11-20T13:45:00Z',
              resolved_end_at: '2026-11-20T14:15:00Z',
            },
            {
              schedule_ref: 'interval-morning',
              role_code: 'interval',
              presentation_order: 1,
              temporal_form: 'named_zone_local',
              zone_id: 'Europe/Rome',
              resolved_start_at: '2026-11-20T08:00:00Z',
              resolved_end_at: '2026-11-20T09:30:00Z',
            },
            {
              schedule_ref: 'planned-child',
              role_code: 'planned',
              display_name: 'Lettura',
              presentation_order: 1,
            },
          ],
        }));
      }
      if (url.endsWith('/profile')) {
        return Promise.resolve(Response.json({
          activity_ref: ACTIVITY_REF,
          title: 'Attività',
          description: null,
          location: null,
          color_code: null,
          revision: 1,
        }));
      }
      return Promise.resolve(Response.json([]));
    });
    vi.stubGlobal('fetch', fetchFn);
    render(
      <EventDetailDialog
        detail={{
          title: 'Attività',
          dateKey: '2026-11-20',
          startMinute: 885,
          endMinute: 915,
          groupLabel: 'Salute',
          accentColorCode: '#12ab9d',
          ownerKind: 'activity',
          realitySubject: { kind: 'activity', ref: ACTIVITY_REF },
        }}
        opener={null}
        timeZone="Europe/Rome"
        sessionSubject={{ kind: 'activity', ref: ACTIVITY_REF }}
        onClose={() => undefined}
      />,
    );
    const intervals = await screen.findByRole('list', {
      name: 'Intervalli dell’attività',
    });
    expect(intervals.querySelectorAll('li')).toHaveLength(2);
    expect(intervals.textContent).toContain('09:00–10:30');
    expect(intervals.textContent).toContain('14:45–15:15');
    expect(intervals.textContent).not.toContain('envelope-technical');
    const area = screen.getByRole('region', { name: 'Area' });
    const planned = await screen.findByText('Lettura');
    expect(
      intervals.compareDocumentPosition(area) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      area.compareDocumentPosition(planned) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      fetchFn.mock.calls.filter(([input]) =>
        fetchRequestUrl(input).endsWith('/children'),
      ),
    ).toHaveLength(1);
  });

  it('uses the personal color for an Activity or Event without a Life Area', () => {
    const noArea = detailFromEvent(
      {
        ...baseEvent(),
        groupId: 'Senza Area',
        appearanceColorCode: '#13bbaa',
      },
      groups,
    );
    expect(noArea.accentColorCode).toBe('#13bbaa');
    render(
      <EventDetailDialog
        detail={{ ...noArea, groupLabel: 'Senza Area' }}
        opener={null}
        onClose={() => undefined}
      />,
    );
    const dialog = screen.getByRole('dialog');
    expect(dialog.style.getPropertyValue('--timeline-inspector-accent')).toBe(
      '#13bbaa',
    );
    expect(screen.queryByRole('region', { name: 'Area' })).toBeNull();

    const unassigned = [
      {
        id: 'legacy-unassigned',
        label: 'Senza Area',
        tone: 'personal' as const,
        itemColorCodes: {
          [`event:${EVENT_REF}`]: '#4A33DD',
        },
      },
    ];
    const event: TimelineEvent = {
      ...baseEvent(),
      groupId: 'legacy-unassigned',
      canonicalBasis: {
        kind: 'scheduled-event',
        eventRef: EVENT_REF,
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef: STATE_REF,
        placement: {
          kind: 'floating-local',
          startsLocalAt: { toString: () => '2026-11-20T10:00' } as never,
          endsLocalAt: { toString: () => '2026-11-20T11:00' } as never,
        },
      },
    };
    expect(
      inspectorAppearanceForEvent(event, unassigned).accentColorCode,
    ).toBe('#4A33DD');
    expect(
      inspectorAppearanceForEvent(
        { ...event, appearanceColorCode: '#223344' },
        unassigned,
      ).accentColorCode,
    ).toBe('#223344');
    expect(inspectorAppearanceForEvent(event, []).accentColorCode).toBeNull();
  });

  it('updates the open Inspector when the assigned Area or its color changes', () => {
    const detail = detailFromEvent(baseEvent(), groups);
    const onClose = () => undefined;
    const { rerender } = render(
      <EventDetailDialog
        detail={detail}
        appearance={{ groupLabel: 'Personale', accentColorCode: '#AA2233' }}
        opener={null}
        onClose={onClose}
      />,
    );
    const dialog = screen.getByRole('dialog');
    expect(dialog.style.getPropertyValue('--timeline-inspector-accent')).toBe(
      '#AA2233',
    );

    rerender(
      <EventDetailDialog
        detail={detail}
        appearance={{ groupLabel: 'Lavoro', accentColorCode: '#2266BB' }}
        opener={null}
        onClose={onClose}
      />,
    );
    expect(screen.getByRole('dialog')).toBe(dialog);
    expect(dialog.style.getPropertyValue('--timeline-inspector-accent')).toBe(
      '#2266BB',
    );
    expect(screen.getByRole('region', { name: 'Area' }).textContent).toContain(
      'Lavoro',
    );

    rerender(
      <EventDetailDialog
        detail={detail}
        appearance={{ groupLabel: 'Senza Area', accentColorCode: null }}
        opener={null}
        onClose={onClose}
      />,
    );
    expect(dialog.style.getPropertyValue('--timeline-inspector-accent')).toBe('');
    expect(screen.queryByRole('region', { name: 'Area' })).toBeNull();
  });

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
    const eventOccurrence = detailFromEvent(
      {
        ...baseEvent(),
        canonicalBasis: {
          kind: 'scheduled-occurrence',
          occurrenceRef: OCCURRENCE_REF,
          sourceKind: 'event',
          sourceNativeRef: EVENT_REF,
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

    expect(activity.realitySubject).toEqual({
      kind: 'activity',
      ref: ACTIVITY_REF,
    });
    expect(event.realitySubject).toEqual({ kind: 'event', ref: EVENT_REF });
    expect(event.eventScheduleRef).toBe(SCHEDULE_REF);
    expect(event.eventPlacementMaterialStateRef).toBe(STATE_REF);
    expect(occurrence.eventScheduleRef).toBeUndefined();
    expect(eventOccurrence.eventRef).toBe(EVENT_REF);
    expect(eventOccurrence.occurrenceRef).toBe(OCCURRENCE_REF);
    expect(eventOccurrence.eventScheduleRef).toBe(SCHEDULE_REF);
    expect(eventOccurrence.eventPlacementMaterialStateRef).toBe(STATE_REF);
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
          ownerKind: 'activity',
          realitySubject: { kind: 'activity', ref: ACTIVITY_REF },
        }}
        opener={null}
        sessionSubject={null}
        onClose={() => undefined}
      />,
    );

    expect(screen.getByTestId('reality-controls').textContent).toBe(
      `activity:${ACTIVITY_REF}`,
    );
    expect(screen.queryByTestId('session-controls')).toBeNull();
  });
});
