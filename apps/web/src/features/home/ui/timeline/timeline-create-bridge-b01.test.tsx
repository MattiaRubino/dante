import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type {
  TemporalPlanningTrayDataSource,
  TemporalPlanningTrayItem,
} from '../../../temporal/planning-tray-data-source';
import type { TemporalCreateRuntime } from '../../../temporal-create';
import { TimelinePlanningTrayB01 } from './timeline-planning-tray-b01';

const ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const activity: TemporalPlanningTrayItem = Object.freeze({
  kind: 'activity',
  state: 'unplaced',
  subjectRef: ACTIVITY_REF,
  title: 'Activity persistita nel Planning Tray',
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

function renderPlanningTray(source: TemporalPlanningTrayDataSource) {
  return render(
    <>
      <div className="dante-timeline-actions" />
      <TimelinePlanningTrayB01
        source={source}
        runtime={{} as TemporalCreateRuntime}
        defaultDate={Temporal.PlainDate.from('2026-09-08')}
      />
    </>,
  );
}

describe('Timeline B01 canonical Planning Tray bridge', () => {
  it('deduplicates canonical identity and refetches after remount', async () => {
    const listItems = vi.fn<TemporalPlanningTrayDataSource['listItems']>(() => Promise.resolve([activity, activity]));
    const source: TemporalPlanningTrayDataSource = {
      listItems,
      placeItem: vi.fn(),
    };

    const first = renderPlanningTray(source);
    await waitFor(() => expect(listItems).toHaveBeenCalledTimes(1));
    fireEvent.click(await screen.findByRole('button', { name: 'Apri elementi già creati' }));
    await waitFor(() => expect(listItems).toHaveBeenCalledTimes(2));

    expect(document.querySelectorAll(`[data-temporal-subject-ref="${ACTIVITY_REF}"]`)).toHaveLength(1);
    expect(screen.getByText(activity.title)).toBeTruthy();
    expect(screen.getByRole('button', { name: `Colloca: ${activity.title}` })).toBeTruthy();
    const planIntent = vi.fn();
    window.addEventListener('dante:open-plan-for-activity', planIntent);
    fireEvent.click(screen.getByRole('button', { name: `Apri Plan per ${activity.title}` }));
    expect(planIntent).toHaveBeenCalledOnce();
    expect(planIntent.mock.calls[0]?.[0]).toMatchObject({
      detail: { activityRef: ACTIVITY_REF, title: activity.title },
    });
    window.removeEventListener('dante:open-plan-for-activity', planIntent);

    first.unmount();
    const second = renderPlanningTray(source);
    await waitFor(() => expect(listItems).toHaveBeenCalledTimes(3));
    fireEvent.click(await screen.findByRole('button', { name: 'Apri elementi già creati' }));
    await waitFor(() => expect(listItems).toHaveBeenCalledTimes(4));
    expect(document.querySelectorAll(`[data-temporal-subject-ref="${ACTIVITY_REF}"]`)).toHaveLength(1);
    second.unmount();
  });

  it('shows read failure instead of a fake empty state, and retries the canonical read', async () => {
    const listItems = vi.fn<TemporalPlanningTrayDataSource['listItems']>()
      .mockRejectedValueOnce(new Error('read unavailable'))
      .mockRejectedValueOnce(new Error('read unavailable'))
      .mockResolvedValueOnce([activity]);
    const source: TemporalPlanningTrayDataSource = { listItems, placeItem: vi.fn() };

    renderPlanningTray(source);
    await waitFor(() => expect(listItems).toHaveBeenCalledTimes(1));
    fireEvent.click(await screen.findByRole('button', { name: 'Apri elementi già creati' }));
    expect(await screen.findByText('Gli elementi esistenti non sono disponibili.')).toBeTruthy();
    expect(screen.queryByText('Niente da collocare')).toBeNull();
    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));
    expect(await screen.findByText(activity.title)).toBeTruthy();
    expect(listItems).toHaveBeenCalledTimes(3);
  });
});
