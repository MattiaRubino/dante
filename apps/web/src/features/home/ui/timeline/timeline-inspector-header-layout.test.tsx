// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import type { ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { EventDetailDialog } from './timeline-overlays';

const main = vi.hoisted(() => ({
  multipleIntervals: false,
  recorded: false,
}));

vi.mock('../../../temporal/activity-session-card-controls', () => ({
  ActivitySessionCardControls: ({ label }: { label: string }) => (
    <div
      className="timeline-activity-session-card-controls"
      data-testid="main-session"
    >
      <div className="timeline-session-controls">
        <div
          className="timeline-session-controls__runtime-actions"
          aria-label={`Sessione · ${label}`}
        >
          <button type="button" aria-label="Avvia">
            ▶
          </button>
          <button type="button" aria-label="Termina">
            ■
          </button>
        </div>
        <span className="timeline-session-controls__inspector-summary">
          {main.recorded
            ? '13:48–13:50 · Totale attivo 00:01:44'
            : 'Avviata alle 13:51 · In corso 00:00:02'}
        </span>
      </div>
    </div>
  ),
}));

vi.mock('../../../temporal/activity-planned-sessions-card-detail', () => ({
  ActivityPlannedSessionsCardDetail: ({
    renderInspectorLeading,
  }: {
    renderInspectorLeading?: (
      intervals: readonly Readonly<{
        scheduleRef: string;
        order: number;
        start: string;
        end: string;
        instant: boolean;
        zoneId: string;
      }>[],
    ) => ReactNode;
  }) => {
    const intervals = main.multipleIntervals
      ? [
          {
            scheduleRef: 'interval-1',
            order: 1,
            start: '2026-11-20T08:00:00Z',
            end: '2026-11-20T08:30:00Z',
            instant: true,
            zoneId: 'Europe/Rome',
          },
          {
            scheduleRef: 'interval-2',
            order: 2,
            start: '2026-11-20T14:00:00Z',
            end: '2026-11-20T14:30:00Z',
            instant: true,
            zoneId: 'Europe/Rome',
          },
        ]
      : [];
    return (
      <>
        {renderInspectorLeading?.(intervals)}
        <div data-testid="child-sessions">Sessioni secondarie</div>
      </>
    );
  },
}));

vi.mock('./timeline-event-agenda-editor', () => ({
  TimelineEventAgendaEditor: ({
    afterAgenda,
    descriptionTarget,
  }: {
    afterAgenda?: ReactNode;
    descriptionTarget?: HTMLElement | null;
  }) => (
    <>
      <section className="timeline-event-agenda" aria-label="Scaletta" />
      {afterAgenda}
      {descriptionTarget
        ? createPortal(
            <section aria-label="Descrizione" />,
            descriptionTarget,
          )
        : null}
    </>
  ),
}));

afterEach(() => {
  cleanup();
  main.multipleIntervals = false;
  main.recorded = false;
});

function renderActivityInspector() {
  render(
    <EventDetailDialog
      detail={{
        title: 'Allenamento',
        dateKey: '2026-11-20',
        startMinute: 900,
        endMinute: 930,
        groupLabel: 'Salute',
        ownerKind: 'activity',
      }}
      sessionSubject={{ kind: 'activity', ref: 'activity-1' }}
      opener={null}
      locale="it-IT"
      timeZone="Europe/Rome"
      onClose={() => undefined}
    />,
  );
}

describe('Activity/Event Inspector main Session header', () => {
  it.each([false, true])(
    'keeps a single main Play/Stop on the title row with multiple intervals=%s',
    (multipleIntervals) => {
      main.multipleIntervals = multipleIntervals;
      renderActivityInspector();
      const dialog = screen.getByRole('dialog');
      expect(dialog.querySelector('.timeline-event-modal__title [data-temporal-kind-marker="activity"] path')).toBeTruthy();
      const titleRow = dialog.querySelector(
        '.timeline-event-modal__title-row',
      );
      const scheduleRow = dialog.querySelector(
        '.timeline-event-modal__schedule-row',
      );
      const mainSession = screen.getByTestId('main-session');
      expect(titleRow?.contains(mainSession)).toBe(true);
      expect(scheduleRow?.contains(mainSession)).toBe(false);
      expect(dialog.querySelectorAll('[data-testid="main-session"]')).toHaveLength(1);
      expect(titleRow?.querySelectorAll('button')).toHaveLength(2);
      expect(titleRow?.textContent).toContain('In corso 00:00:02');
      expect(
        (titleRow!.compareDocumentPosition(scheduleRow!) &
          Node.DOCUMENT_POSITION_FOLLOWING) !== 0,
      ).toBe(true);
      if (multipleIntervals) {
        expect(scheduleRow?.querySelectorAll('.timeline-inspector-intervals li')).toHaveLength(2);
        expect(scheduleRow?.textContent).toContain('09:00–09:30');
        expect(scheduleRow?.textContent).toContain('15:00–15:30');
      } else {
        expect(scheduleRow?.textContent).toContain('15:00–15:30');
      }
      const area = screen.getByRole('region', { name: 'Area' });
      expect(
        (scheduleRow!.compareDocumentPosition(area) &
          Node.DOCUMENT_POSITION_FOLLOWING) !== 0,
      ).toBe(true);
    },
  );

  it('keeps the recorded main duration above all intervals', () => {
    main.multipleIntervals = true;
    main.recorded = true;
    renderActivityInspector();
    const dialog = screen.getByRole('dialog');
    const summary = dialog.querySelector(
      '.timeline-event-modal__title-row .timeline-session-controls__inspector-summary',
    );
    const intervalList = dialog.querySelector('.timeline-inspector-intervals');
    expect(summary?.textContent).toContain('Totale attivo 00:01:44');
    expect(
      (summary!.compareDocumentPosition(intervalList!) &
        Node.DOCUMENT_POSITION_FOLLOWING) !== 0,
    ).toBe(true);
  });

  it('keeps Event Inspector free of Activity main Session controls', () => {
    render(
      <EventDetailDialog
        detail={{
          title: 'Riunione',
          dateKey: '2026-11-20',
          startMinute: 900,
          endMinute: 930,
          groupLabel: 'Lavoro',
          ownerKind: 'event',
          eventRef: 'event-1',
        }}
        opener={null}
        onClose={() => undefined}
      />,
    );
    expect(screen.getByRole('dialog').querySelector('.timeline-event-modal__title [data-temporal-kind-marker="event"] circle')).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Riunione' })).toBeTruthy();
    expect(screen.queryByTestId('main-session')).toBeNull();
    expect(screen.getByRole('region', { name: 'Area' })).toBeTruthy();
    const dialog = screen.getByRole('dialog');
    const schedule = dialog.querySelector(
      '.timeline-event-modal__schedule-row',
    )!;
    const agenda = screen.getByRole('region', { name: 'Scaletta' });
    const area = screen.getByRole('region', { name: 'Area' });
    const description = screen.getByRole('region', { name: 'Descrizione' });
    const slot = description.parentElement;
    expect(
      schedule.compareDocumentPosition(agenda) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      agenda.compareDocumentPosition(area) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(
      area.compareDocumentPosition(description) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(dialog.lastElementChild).toBe(slot);
  });
});
