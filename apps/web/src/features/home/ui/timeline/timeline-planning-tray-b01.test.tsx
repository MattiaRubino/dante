// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type { TemporalPlanningTrayDataSource } from '../../../temporal/planning-tray-data-source';
import type { TemporalCreateRuntime } from '../../../temporal-create';
import { TimelinePlanningTrayB01 } from './timeline-planning-tray-b01';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

const items = Object.freeze([
  Object.freeze({
    kind: 'activity' as const,
    state: 'unplaced' as const,
    subjectRef: '0199a111-1111-7111-8111-111111111111',
    title: 'Preparare documenti',
    createdAt: Temporal.Instant.from('2026-10-01T08:00:00Z'),
    lifeAreaRef: null,
    lifeAreaAssignmentRevision: null,
    scheduleRef: null,
  }),
  Object.freeze({
    kind: 'event' as const,
    state: 'unplaced' as const,
    subjectRef: '0199a222-2222-7222-8222-222222222222',
    title: 'Cena da organizzare',
    createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
    lifeAreaRef: null,
    lifeAreaAssignmentRevision: null,
    scheduleRef: null,
  }),
  Object.freeze({
    kind: 'event' as const,
    state: 'postponed' as const,
    subjectRef: '0199a333-3333-7333-8333-333333333333',
    title: 'Visita medica',
    createdAt: Temporal.Instant.from('2026-10-01T10:00:00Z'),
    lifeAreaRef: null,
    lifeAreaAssignmentRevision: null,
    scheduleRef: '0199a444-4444-7444-8444-444444444444',
  }),
]);

describe('TimelinePlanningTrayB01 unified product tray', () => {
  it('shows Activity, never-placed Event and postponed Event in one Da collocare surface', async () => {
    const source: TemporalPlanningTrayDataSource = {
      listItems: vi.fn(async () => items),
      placeItem: vi.fn(async (request) => ({
        kind: request.kind,
        subjectRef: request.subjectRef,
        scheduleRef: '0199a555-5555-7555-8555-555555555555',
        placementMaterialStateRef: '0199a666-6666-7666-8666-666666666666',
        replayed: false,
      })),
    };

    render(
      <>
        <div className="dante-timeline-actions" />
        <TimelinePlanningTrayB01
          runtime={{} as TemporalCreateRuntime}
          defaultDate={Temporal.PlainDate.from('2026-10-02')}
          source={source}
        />
      </>,
    );

    const trigger = await screen.findByRole('button', { name: 'Apri Da collocare' });
    await waitFor(() => expect(source.listItems).toHaveBeenCalled());
    fireEvent.click(trigger);

    expect(await screen.findByRole('heading', { name: 'Da collocare' })).toBeTruthy();
    expect(screen.getByText('Preparare documenti')).toBeTruthy();
    expect(screen.getByText('Cena da organizzare')).toBeTruthy();
    expect(screen.getByText('Visita medica')).toBeTruthy();
    expect(screen.getByText('Attività')).toBeTruthy();
    expect(screen.getByText('Evento')).toBeTruthy();
    expect(screen.getByText('Posticipato')).toBeTruthy();
    expect(document.querySelector('.timeline-postponed')).toBeNull();
  });
});
