import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  type TemporalActivityDataSource,
  type TemporalActivityRecord,
} from '../../../temporal';
import { createLocalTemporalCreateRuntime } from '../../../temporal-create';
import { TimelinePlanningTrayB01 } from './timeline-planning-tray-b01';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

function runtimeWithUnplaced(
  records: readonly TemporalActivityRecord[],
  rejectRead = false,
) {
  const loadUnplaced = vi.fn<TemporalActivityDataSource['loadUnplaced']>(() =>
    rejectRead
      ? Promise.reject(new Error('read unavailable'))
      : Promise.resolve(Object.freeze([...records])),
  );
  const source = Object.freeze({
    createActivity: vi.fn<TemporalActivityDataSource['createActivity']>(() =>
      Promise.reject(new Error('create is not part of this read proof')),
    ),
    createScheduledActivity: vi.fn<
      TemporalActivityDataSource['createScheduledActivity']
    >(() =>
      Promise.reject(new Error('scheduled create outside B01 read proof')),
    ),
    loadUnplaced,
  }) satisfies TemporalActivityDataSource;
  const runtime = createLocalTemporalCreateRuntime({
    mode: 'production',
    ids: createDeterministicTemporalIdFactory('b01-planning-tray'),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-08T08:00:00Z'),
      'Europe/Rome',
    ),
    activityDataSource: source,
  });
  return Object.freeze({ runtime, loadUnplaced });
}

function renderPlanningTray(
  runtime: ReturnType<typeof runtimeWithUnplaced>['runtime'],
) {
  return render(
    <TimelinePlanningTrayB01 items={Object.freeze([])} runtime={runtime} />,
  );
}

function installTimelineHosts(): void {
  document.body.innerHTML = '<div class="dante-timeline-actions"></div>';
}

describe('Timeline B01 canonical Planning Tray bridge', () => {
  it('deduplicates canonical identity and refetches after remount', async () => {
    installTimelineHosts();
    const canonical = Object.freeze({
      activityRef: ACTIVITY_REF,
      title: 'Activity persistita nel Planning Tray',
      createdAt: Temporal.Instant.from('2026-09-08T08:00:00Z'),
    });
    const source = runtimeWithUnplaced(Object.freeze([canonical, canonical]));

    const first = renderPlanningTray(source.runtime);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(1));
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Apri attività da collocare',
      }),
    );
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(2));

    expect(
      document.querySelectorAll(
        `[data-temporal-activity-ref="${ACTIVITY_REF}"]`,
      ),
    ).toHaveLength(1);
    expect(
      screen.getByText('Activity persistita nel Planning Tray'),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Colloca' })).toBeNull();

    first.unmount();
    const second = renderPlanningTray(source.runtime);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(3));
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Apri attività da collocare',
      }),
    );
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(4));

    expect(
      document.querySelectorAll(
        `[data-temporal-activity-ref="${ACTIVITY_REF}"]`,
      ),
    ).toHaveLength(1);
    expect(
      screen.getByText('Activity persistita nel Planning Tray'),
    ).toBeTruthy();
    second.unmount();
  });

  it('shows read failure instead of a fake empty state', async () => {
    installTimelineHosts();
    const source = runtimeWithUnplaced(Object.freeze([]), true);

    renderPlanningTray(source.runtime);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(1));
    fireEvent.click(
      await screen.findByRole('button', {
        name: 'Apri attività da collocare',
      }),
    );

    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(2));
    expect(
      await screen.findByText('Le attività da collocare non sono disponibili.'),
    ).toBeTruthy();
    expect(screen.queryByText('Niente da collocare')).toBeNull();
    expect(screen.getByRole('button', { name: 'Riprova' })).toBeTruthy();
  });
});
