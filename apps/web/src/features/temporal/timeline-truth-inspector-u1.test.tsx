// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { TemporalTimelineRuntimeBoundary } from './timeline-runtime-boundary';
import { TimelineTruthInspector } from './timeline-truth-inspector';

afterEach(() => {
  cleanup();
});

describe('Timeline Reality Outcome U1 shell', () => {
  it('stays visible above Plan even when the current Timeline window has no subjects', async () => {
    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-30"
        dataSource={{
          loadWindow: async () => ({
            kind: 'empty',
            startDate: '2026-09-30',
            endDateExclusive: '2026-10-01',
            effectiveZoneId: 'Europe/Rome',
          }),
        }}
        mode="development"
      >
        <TimelineTruthInspector />
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(await screen.findByText('Realtà / Outcome')).toBeTruthy();
    expect(
      document.querySelector('[data-timeline-truth-inspector]'),
    ).not.toBeNull();
  });
});
