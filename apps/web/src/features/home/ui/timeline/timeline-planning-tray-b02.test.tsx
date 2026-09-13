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
const SCHEDULE_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const MATERIAL_STATE_REF = '0199a8c0-7e73-7de2-8cf2-c4062517839f';

const ACTIVITY: TemporalActivityRecord = Object.freeze({
  activityRef: ACTIVITY_REF,
  title: 'Activity esistente da collocare',
  createdAt: Temporal.Instant.from('2026-09-08T08:00:00Z'),
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

function installTimelineHosts(): void {
  document.body.innerHTML = '<div class="dante-timeline-actions"></div>';
}

function createHarness(rejectPlacement = false) {
  let unplaced: readonly TemporalActivityRecord[] = Object.freeze([ACTIVITY]);
  const createActivity = vi.fn<TemporalActivityDataSource['createActivity']>(
    () => Promise.reject(new Error('B02-B must not create Activity')),
  );
  const createScheduledActivity = vi.fn<
    TemporalActivityDataSource['createScheduledActivity']
  >(() => Promise.reject(new Error('B02-B must not use atomic create')));
  const establishActivitySchedule = vi.fn<
    TemporalActivityDataSource['establishActivitySchedule']
  >((request) => {
    if (rejectPlacement) {
      return Promise.reject(new Error('schedule unavailable'));
    }
    unplaced = Object.freeze([]);
    return Promise.resolve(
      Object.freeze({
        activity: ACTIVITY,
        schedule: Object.freeze({
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: MATERIAL_STATE_REF,
          temporalForm: 'floating-local' as const,
          startsLocalAt: request.placement.startsLocalAt,
          endsLocalAt: request.placement.endsLocalAt,
        }),
        replayed: false,
      }),
    );
  });
  const loadUnplaced = vi.fn<TemporalActivityDataSource['loadUnplaced']>(() =>
    Promise.resolve(unplaced),
  );
  const source = Object.freeze({
    createActivity,
    createScheduledActivity,
    establishActivitySchedule,
    loadUnplaced,
  }) satisfies TemporalActivityDataSource;
  const runtime = createLocalTemporalCreateRuntime({
    mode: 'production',
    ids: createDeterministicTemporalIdFactory('b02-b-planning-tray'),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-08T08:00:00Z'),
      'Europe/Rome',
    ),
    activityDataSource: source,
  });
  return Object.freeze({
    runtime,
    createActivity,
    createScheduledActivity,
    establishActivitySchedule,
    loadUnplaced,
  });
}

async function openTray(
  runtime: ReturnType<typeof createHarness>['runtime'],
): Promise<void> {
  installTimelineHosts();
  render(
    <TimelinePlanningTrayB01
      items={Object.freeze([])}
      runtime={runtime}
      defaultDate={Temporal.PlainDate.from('2026-09-09')}
    />,
  );
  fireEvent.click(
    await screen.findByRole('button', {
      name: 'Apri attività da collocare',
    }),
  );
  await screen.findByText(ACTIVITY.title);
}

describe('Timeline B02-B canonical Planning Tray placement', () => {
  it('places the same Activity, then removes it only after canonical refetch', async () => {
    const harness = createHarness();
    await openTray(harness.runtime);

    fireEvent.click(
      screen.getByRole('button', {
        name: `Colloca: ${ACTIVITY.title}`,
      }),
    );
    fireEvent.change(screen.getByLabelText('Inizio'), {
      target: { value: '14:15' },
    });
    fireEvent.change(screen.getByLabelText('Durata (minuti)'), {
      target: { value: '45' },
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Colloca in Timeline' }),
    );

    await waitFor(() =>
      expect(harness.establishActivitySchedule).toHaveBeenCalledTimes(1),
    );
    const request = harness.establishActivitySchedule.mock.calls[0]?.[0];
    expect(request).toMatchObject({
      activityRef: ACTIVITY_REF,
      placement: { kind: 'floating-local-interval' },
    });
    expect(request?.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T14:15:00',
    );
    expect(request?.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T15:00:00',
    );
    expect(harness.createActivity).not.toHaveBeenCalled();
    expect(harness.createScheduledActivity).not.toHaveBeenCalled();
    await waitFor(() => expect(screen.queryByText(ACTIVITY.title)).toBeNull());
    expect(harness.loadUnplaced.mock.calls.length).toBeGreaterThanOrEqual(3);
  });

  it('keeps the Activity visible when canonical Schedule persistence fails', async () => {
    const harness = createHarness(true);
    await openTray(harness.runtime);

    fireEvent.click(
      screen.getByRole('button', {
        name: `Colloca: ${ACTIVITY.title}`,
      }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Colloca in Timeline' }),
    );

    expect(
      await screen.findByText(
        'Lo Schedule non è stato accettato. L’Activity resta qui.',
      ),
    ).toBeTruthy();
    expect(screen.getByText(ACTIVITY.title)).toBeTruthy();
    expect(harness.loadUnplaced).toHaveBeenCalledTimes(2);
  });
});
