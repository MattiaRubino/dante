import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const source = vi.hoisted(() => ({
  list: vi.fn(),
  start: vi.fn(),
  pause: vi.fn(),
  resume: vi.fn(),
  end: vi.fn(),
}));

vi.mock('./remote-session-data-source', () => ({
  createRemoteTemporalSessionDataSource: () => source,
}));

import { SessionSubjectControls } from './session-subject-controls';

beforeEach(() => {
  Object.values(source).forEach((mock) => mock.mockReset());
});

afterEach(() => cleanup());

describe('compact Session runtime on created cards', () => {
  it('shows runtime buttons without detail duration/policy prose', async () => {
    source.list.mockResolvedValue([
      {
        sessionRef: 'session-ref',
        subjectNativeRef: 'activity-ref',
        timingMaterialStateRef: 'timing-ref',
        startedAt: '2026-10-01T20:00:00Z',
        endedAt: null,
        open: true,
        replayed: false,
        paused: false,
        evaluatedAt: '2026-10-01T20:05:00Z',
        elapsedSeconds: 300,
        pausedSeconds: 0,
        activeSeconds: 300,
        durationEvaluations: [
          {
            constraintRef: 'constraint-ref',
            materialStateRef: 'rule-state-ref',
            minimumDurationMicroseconds: 1_800_000_000,
            strength: 'soft',
            evaluation: 'pending',
          },
        ],
      },
    ]);

    render(
      <SessionSubjectControls
        kind="activity"
        subjectRef="activity-ref"
        label="Focus"
        variant="card"
      />,
    );

    await waitFor(() => expect(screen.getByRole('button', { name: 'Pausa' })).toBeTruthy());
    expect(screen.getByRole('button', { name: 'Termina' })).toBeTruthy();
    expect(screen.queryByLabelText('Durata sessione')).toBeNull();
    expect(document.querySelector('[data-session-duration-evaluation]')).toBeNull();
  });

  it('makes card runtime inert when the Timeline card is not the active focus target', async () => {
    source.list.mockResolvedValue([]);

    render(
      <SessionSubjectControls
        kind="activity"
        subjectRef="activity-ref"
        label="Focus"
        variant="card"
        interactive={false}
      />,
    );

    const start = await screen.findByRole('button', { name: 'Avvia' });
    expect(start.hasAttribute('disabled')).toBe(true);
    expect(start.tabIndex).toBe(-1);
  });
});
