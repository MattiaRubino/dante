import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type {
  TemporalPlanningTrayDataSource,
  TemporalPlanningTrayItem,
} from '../../../temporal/planning-tray-data-source';
import type { TemporalCreateRuntime } from '../../../temporal-create';
import {
  invalidateTemporalPlanningRead,
  invalidateTemporalTimelineRead,
} from '../../../temporal/timeline-invalidation';
import { TimelinePlanningTrayB01 } from './timeline-planning-tray-b01';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const MATERIAL_STATE_REF = '0199a8c0-7e73-7de2-8cf2-c4062517839f';
const activity: TemporalPlanningTrayItem = Object.freeze({
  kind: 'activity',
  state: 'unplaced',
  subjectRef: ACTIVITY_REF,
  title: 'Activity esistente da collocare',
  createdAt: Temporal.Instant.from('2026-09-08T08:00:00Z'),
  lifeAreaRef: null,
  lifeAreaAssignmentRevision: null,
  scheduleRef: null,
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

function createHarness(rejectPlacement = false, initiallyUnplaced = true) {
  let currentItems: readonly TemporalPlanningTrayItem[] = initiallyUnplaced ? [activity] : [];
  const listItems = vi.fn<TemporalPlanningTrayDataSource['listItems']>(() => Promise.resolve(currentItems));
  const placeItem = vi.fn<TemporalPlanningTrayDataSource['placeItem']>((request) => {
    if (rejectPlacement) return Promise.reject(new Error('schedule unavailable'));
    currentItems = [];
    return Promise.resolve({
      kind: request.kind,
      subjectRef: request.subjectRef,
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: MATERIAL_STATE_REF,
      replayed: false,
    });
  });
  const source: TemporalPlanningTrayDataSource = { listItems, placeItem };
  return {
    source,
    listItems,
    placeItem,
    restoreUnplaced: () => { currentItems = [activity]; },
  };
}

function renderTray(source: TemporalPlanningTrayDataSource) {
  document.body.innerHTML = '<div class="dante-timeline-actions"></div>';
  return render(
    <TimelinePlanningTrayB01
      source={source}
      runtime={{} as TemporalCreateRuntime}
      defaultDate={Temporal.PlainDate.from('2026-09-09')}
    />,
  );
}

async function openTray(source: TemporalPlanningTrayDataSource) {
  renderTray(source);
  fireEvent.click(await screen.findByRole('button', { name: 'Apri elementi già creati' }));
  await screen.findByText(activity.title);
}

function openPlacement() {
  fireEvent.click(screen.getByRole('button', { name: `Colloca: ${activity.title}` }));
}

function submitPlacement() {
  fireEvent.submit(
    screen.getByRole('button', { name: 'Colloca in Timeline' }).closest('form') as HTMLFormElement,
  );
}

describe('Timeline B02 canonical Planning Tray placement and invalidation', () => {
  it('chooses duration and named zone at placement without requiring either at creation', async () => {
    const harness = createHarness();
    await openTray(harness.source);
    openPlacement();
    fireEvent.change(screen.getByLabelText('Data'), { target: { value: '2026-10-02' } });
    fireEvent.change(screen.getByLabelText('Inizio'), { target: { value: '10:00' } });
    fireEvent.change(screen.getByLabelText('Durata (minuti)'), { target: { value: '60' } });
    fireEvent.change(screen.getByLabelText('Riferimento orario'), { target: { value: 'zoned' } });
    fireEvent.change(screen.getByLabelText('Fuso orario'), { target: { value: 'Europe/Rome' } });
    submitPlacement();
    await waitFor(() => expect(harness.placeItem).toHaveBeenCalledTimes(1));
    const request = harness.placeItem.mock.calls[0]?.[0];
    expect(request).toMatchObject({ kind: 'activity', subjectRef: ACTIVITY_REF });
    expect(request?.operationId).toMatch(/^planning-tray:activity:/);
    const placement = request?.placement;
    expect(placement?.kind).toBe('named-zone-local-interval');
    if (placement?.kind !== 'named-zone-local-interval') throw new Error('Expected named zone');
    expect(placement.zoneId).toBe('Europe/Rome');
    expect(placement.startsLocalAt.toString()).toBe('2026-10-02T10:00:00');
    expect(placement.endsLocalAt.toString()).toBe('2026-10-02T11:00:00');
  });

  it('places the same Activity and removes it only after canonical refetch', async () => {
    const harness = createHarness();
    await openTray(harness.source);
    openPlacement();
    fireEvent.change(screen.getByLabelText('Inizio'), { target: { value: '14:15' } });
    fireEvent.change(screen.getByLabelText('Durata (minuti)'), { target: { value: '45' } });
    submitPlacement();
    await waitFor(() => expect(harness.placeItem).toHaveBeenCalledTimes(1));
    const request = harness.placeItem.mock.calls[0]?.[0];
    expect(request).toMatchObject({ kind: 'activity', subjectRef: ACTIVITY_REF });
    const placement = request?.placement;
    if (placement?.kind !== 'floating-local-interval') throw new Error('Expected floating interval');
    expect(placement.startsLocalAt.toString()).toBe('2026-09-09T14:15:00');
    expect(placement.endsLocalAt.toString()).toBe('2026-09-09T15:00:00');
    await waitFor(() => expect(screen.queryByText(activity.title)).toBeNull());
    expect(harness.listItems.mock.calls.length).toBeGreaterThanOrEqual(3);
  });

  it('keeps the Activity visible when canonical Schedule persistence fails', async () => {
    const harness = createHarness(true);
    await openTray(harness.source);
    openPlacement();
    submitPlacement();
    expect(await screen.findByText('Lo Schedule non è stato accettato. L’elemento resta qui.')).toBeTruthy();
    expect(screen.getByText(activity.title)).toBeTruthy();
    expect(harness.placeItem).toHaveBeenCalledTimes(1);
    expect(harness.listItems).toHaveBeenCalledTimes(2);
  });

  it.each([
    ['planning', invalidateTemporalPlanningRead],
    ['timeline', invalidateTemporalTimelineRead],
  ])('reloads the same identity on %s invalidation after unschedule', async (_, invalidate) => {
    const harness = createHarness(false, false);
    renderTray(harness.source);
    await waitFor(() => expect(harness.listItems).toHaveBeenCalledTimes(1));
    harness.restoreUnplaced();
    invalidate();
    await waitFor(() => expect(harness.listItems).toHaveBeenCalledTimes(2));
    fireEvent.click(await screen.findByRole('button', { name: 'Apri elementi già creati' }));
    expect(await screen.findByText(activity.title)).toBeTruthy();
    expect(document.querySelectorAll(`[data-temporal-subject-ref="${ACTIVITY_REF}"]`)).toHaveLength(1);
  });
});
