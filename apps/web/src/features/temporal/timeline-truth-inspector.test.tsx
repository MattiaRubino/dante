import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { Temporal } from '@dante/time';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TemporalTimelineRuntimeBoundary } from './timeline-runtime-boundary';
import {
  TimelineTruthInspector,
  timelineTruthSubjects,
} from './timeline-truth-inspector';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from './timeline-read';

const ACTIVITY = '01991f2a-1234-7abc-8def-1234567890ab';
const EVENT = '01991f2a-1234-7abc-8def-1234567890ac';
const SCHEDULE_A = '01991f2a-1234-7abc-8def-1234567890ad';
const SCHEDULE_B = '01991f2a-1234-7abc-8def-1234567890ae';
const STATE_A = '01991f2a-1234-7abc-8def-1234567890af';
const STATE_B = '01991f2a-1234-7abc-8def-1234567890b0';

function windowFixture(): TemporalTimelineWindow {
  return {
    kind: 'window',
    startDate: '2026-09-26',
    endDateExclusive: '2026-09-28',
    effectiveZoneId: 'Europe/Rome',
    items: [
      {
        kind: 'scheduled_activity',
        activityRef: ACTIVITY,
        scheduleRef: SCHEDULE_A,
        placementMaterialStateRef: STATE_A,
        title: 'Allenamento',
        temporalForm: 'date-span',
        startDate: Temporal.PlainDate.from('2026-09-26'),
        endDateExclusive: Temporal.PlainDate.from('2026-09-27'),
      },
      {
        kind: 'scheduled_event',
        eventRef: EVENT,
        scheduleRef: SCHEDULE_B,
        placementMaterialStateRef: STATE_B,
        title: 'Cena',
        temporalForm: 'date-span',
        startDate: Temporal.PlainDate.from('2026-09-26'),
        endDateExclusive: Temporal.PlainDate.from('2026-09-27'),
      },
    ],
  };
}

describe('Timeline truth inspector', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('derives stable B10 subjects from the canonical timeline window', () => {
    expect(timelineTruthSubjects(windowFixture())).toEqual([
      {
        key: `activity:${ACTIVITY}`,
        kind: 'activity',
        ref: ACTIVITY,
        title: 'Allenamento',
      },
      {
        key: `event:${EVENT}`,
        kind: 'event',
        ref: EVENT,
        title: 'Cena',
      },
    ]);
  });

  it('mounts the full Actual-to-Reconciliation controls from the real timeline runtime', async () => {
    const dataSource: TemporalTimelineDataSource = {
      loadWindow: async () => windowFixture(),
    };
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        Response.json(
          {
            code: 'temporal.actual.not_found',
            category: 'not_found',
            title: 'Actual unavailable',
            detail: 'No Actual is established for this subject.',
          },
          { status: 404 },
        ),
      ),
    );

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-26"
        dataSource={dataSource}
        mode="development"
      >
        <TimelineTruthInspector />
      </TemporalTimelineRuntimeBoundary>,
    );

    await screen.findByText('Realtà / Outcome');
    await waitFor(() => {
      expect(screen.getByLabelText('Elemento per stato reale')).toBeTruthy();
    });
    expect(screen.getByText('Stato reale: sconosciuto')).toBeTruthy();
    expect(screen.getByText('Outcome', { selector: 'strong' })).toBeTruthy();
    expect(screen.getByText('Confirmation', { selector: 'strong' })).toBeTruthy();
    expect(screen.getByText('Reconciliation', { selector: 'strong' })).toBeTruthy();
  });
});
