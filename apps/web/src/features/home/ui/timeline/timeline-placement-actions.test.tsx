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
import { createDeterministicTemporalIdFactory } from '../../../temporal/model';
import type { TemporalScheduleDataSource } from '../../../temporal/schedule-data-source';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from '../../../temporal/timeline-read';
import { TemporalTimelineRuntimeBoundary } from '../../../temporal/timeline-runtime-boundary';
import { TimelineSurface } from './timeline-surface';

vi.mock('../../../temporal/remote-placement-lock-data-source', () => ({
  createRemotePlacementLockDataSource: () => ({
    get: (scheduleRef: string) =>
      Promise.resolve({ scheduleRef, locked: false, revision: 0 }),
  }),
}));

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const CURRENT_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';

beforeAll(async () => {
  await i18n.changeLanguage('it');
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    value: 1440,
    writable: true,
  });
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

describe('governed Schedule Inspector actions', () => {
  it('does not offer a move into the retired Da collocare workflow', async () => {
    const window: TemporalTimelineWindow = {
      kind: 'window',
      startDate: '2026-09-02',
      endDateExclusive: '2026-10-15',
      effectiveZoneId: 'Europe/Rome',
      items: [
        {
          kind: 'scheduled_activity',
          activityRef: ACTIVITY_REF,
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: CURRENT_STATE_REF,
          title: 'Governed B02-D',
          temporalForm: 'floating-local',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T10:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T11:00'),
        },
      ],
    };
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockResolvedValue(window);
    const unscheduleSchedule =
      vi.fn<TemporalScheduleDataSource['unscheduleSchedule']>();
    const scheduleDataSource: TemporalScheduleDataSource = {
      reviseSchedule: vi.fn(),
      unscheduleSchedule,
      undoScheduleUnschedule: vi.fn(),
    };

    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-09"
        dataSource={{ loadWindow }}
        scheduleDataSource={scheduleDataSource}
        ids={createDeterministicTemporalIdFactory('b02-d-ui')}
        mode="production"
      >
        <TimelineSurface
          expanded={false}
          viewedDateIso="2026-09-09"
          onExpandedChange={vi.fn()}
          onExpansionProgress={vi.fn()}
        />
      </TemporalTimelineRuntimeBoundary>,
    );
    const card = await waitFor(() => {
      const match = container.querySelector<HTMLElement>(
        `[data-timeline-event="${SCHEDULE_REF}"]`,
      );
      expect(match).toBeTruthy();
      return match as HTMLElement;
    });
    fireEvent.click(card);
    fireEvent.click(
      await screen.findByRole('button', { name: 'Governed B02-D' }),
    );
    expect(
      screen.queryByRole('button', { name: 'Sposta in Da collocare' }),
    ).toBeNull();
    expect(
      screen.queryByRole('group', { name: 'Sposta in Da collocare' }),
    ).toBeNull();
    expect(unscheduleSchedule).not.toHaveBeenCalled();
  });
});
