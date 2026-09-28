import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
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
const ROUTINE = '01991f2a-1234-7abc-8def-1234567890b1';
const OCCURRENCE = '01991f2a-1234-7abc-8def-1234567890b2';
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
      {
        kind: 'expected_occurrence',
        occurrenceRef: OCCURRENCE,
        sourceKind: 'routine',
        sourceNativeRef: ROUTINE,
        title: 'Routine completata',
        coordinate: {
          familyCode: 'elapsed-interval',
          expectedAt: Temporal.Instant.from('2026-09-26T11:00:00Z'),
        },
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
        timelineLabel: '2026-09-26',
        recurrenceOwner: null,
      },
      {
        key: `event:${EVENT}`,
        kind: 'event',
        ref: EVENT,
        title: 'Cena',
        timelineLabel: '2026-09-26',
        recurrenceOwner: { kind: 'event', ref: EVENT },
      },
      {
        key: `occurrence:${OCCURRENCE}`,
        kind: 'occurrence',
        ref: OCCURRENCE,
        title: 'Routine completata',
        timelineLabel: '2026-09-26T11:00:00Z',
        recurrenceOwner: { kind: 'routine', ref: ROUTINE },
      },
    ]);
  });

  it('shows the occurrence timing in the selector, not only its repeated title', async () => {
    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-26"
        dataSource={{ loadWindow: async () => windowFixture() }}
        mode="development"
      >
        <TimelineTruthInspector />
      </TemporalTimelineRuntimeBoundary>,
    );

    const picker = await screen.findByLabelText('Elemento per stato reale');
    expect(picker.textContent).toContain(
      'occurrence · Routine completata · 2026-09-26T11:00:00Z',
    );
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
    expect(screen.getByText('Condizione Actual', { selector: 'strong' })).toBeTruthy();
  });

  it('keeps Condition on the Occurrence and Recurrence on its Routine source', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>(async () =>
      Response.json(
        {
          code: 'temporal.not_found',
          category: 'not_found',
          title: 'Not found',
          detail: 'Canonical state is unavailable.',
        },
        { status: 404 },
      ),
    );
    vi.stubGlobal('fetch', fetchFn);
    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-26"
        dataSource={{ loadWindow: async () => windowFixture() }}
        mode="development"
      >
        <TimelineTruthInspector />
      </TemporalTimelineRuntimeBoundary>,
    );

    const picker = await screen.findByLabelText('Elemento per stato reale');
    fireEvent.change(picker, { target: { value: `occurrence:${OCCURRENCE}` } });
    await waitFor(() => {
      expect(
        document.querySelector(
          `[data-advanced-recurrence-owner="routine:${ROUTINE}"]`,
        ),
      ).toBeTruthy();
      expect(
        fetchFn.mock.calls.some(([input]) =>
          String(input).includes(`/routines/${ROUTINE}/recurrence`),
        ),
      ).toBe(true);
      expect(
        fetchFn.mock.calls.some(([input]) =>
          String(input).includes('subject_kind=occurrence') &&
          String(input).includes(OCCURRENCE),
        ),
      ).toBe(true);
    });
    expect(screen.getByText('Condizione Actual', { selector: 'strong' })).toBeTruthy();
    fireEvent.change(picker, { target: { value: `event:${EVENT}` } });
    await waitFor(() => {
      expect(
        document.querySelector(`[data-advanced-recurrence-owner="event:${EVENT}"]`),
      ).toBeTruthy();
      expect(
        document.querySelector(`[data-advanced-recurrence-owner="routine:${ROUTINE}"]`),
      ).toBeNull();
      expect(
        fetchFn.mock.calls.some(([input]) =>
          String(input).includes('subject_kind=event') &&
          String(input).includes(EVENT),
        ),
      ).toBe(true);
    });
  });
});
