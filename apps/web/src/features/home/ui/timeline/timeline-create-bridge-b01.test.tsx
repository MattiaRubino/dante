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
import type { TimelineGroup } from './model/timeline-types';
import { TimelineCreateBridge } from './timeline-create-bridge';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const GROUP = Object.freeze({
  id: 'personale',
  label: 'Personale',
  tone: 'personal',
}) satisfies TimelineGroup;

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
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

function renderBridge(
  runtime: ReturnType<typeof runtimeWithUnplaced>['runtime'],
) {
  return render(
    <TimelineCreateBridge
      defaultDate={Temporal.PlainDate.from('2026-09-08')}
      groups={Object.freeze([GROUP])}
      filters={new Set()}
      runtime={runtime}
      onRevealDate={vi.fn()}
      onCreateContext={() => GROUP}
      onMaterializeCreatedEvent={vi.fn()}
      onMaterializeCreatedAllDay={vi.fn()}
      onRemoveCreatedEvent={vi.fn()}
      onRemoveCreatedAllDay={vi.fn()}
    />,
  );
}

function installTimelineHosts(): void {
  document.body.innerHTML = [
    '<div class="home-timeline--production"></div>',
    '<div class="dante-timeline-actions"></div>',
  ].join('');
}

describe('Timeline B01 canonical Planning Tray bridge', () => {
  it('deduplicates canonical identity and refetches the same Activity after remount', async () => {
    vi.stubEnv('MODE', 'production');
    installTimelineHosts();
    const canonical = Object.freeze({
      activityRef: ACTIVITY_REF,
      title: 'Activity persistita nel Planning Tray',
      createdAt: Temporal.Instant.from('2026-09-08T08:00:00Z'),
    });
    const source = runtimeWithUnplaced(Object.freeze([canonical, canonical]));

    const first = renderBridge(source.runtime);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(1));
    const firstTrigger = await screen.findByRole('button', {
      name: 'Apri attività da collocare',
    });
    fireEvent.click(firstTrigger);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(2));

    expect(
      document.querySelectorAll(
        `[data-temporal-activity-ref="${ACTIVITY_REF}"]`,
      ),
    ).toHaveLength(1);
    expect(screen.getByText('Activity persistita nel Planning Tray')).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Colloca' })).toBeNull();

    first.unmount();
    const second = renderBridge(source.runtime);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(3));
    const secondTrigger = await screen.findByRole('button', {
      name: 'Apri attività da collocare',
    });
    fireEvent.click(secondTrigger);
    await waitFor(() => expect(source.loadUnplaced).toHaveBeenCalledTimes(4));

    expect(
      document.querySelectorAll(
        `[data-temporal-activity-ref="${ACTIVITY_REF}"]`,
      ),
    ).toHaveLength(1);
    expect(screen.getByText('Activity persistita nel Planning Tray')).toBeTruthy();
    second.unmount();
  });

  it('shows read failure instead of replacing it with a fake empty Planning Tray', async () => {
    vi.stubEnv('MODE', 'production');
    installTimelineHosts();
    const source = runtimeWithUnplaced(Object.freeze([]), true);

    renderBridge(source.runtime);
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
