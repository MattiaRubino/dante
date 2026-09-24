import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { TemporalSessionView } from './remote-session-data-source';
import { SessionSubjectControls } from './session-subject-controls';

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

const activityRef = 'activity-native-ref';
const occurrenceRef = 'occurrence-native-ref';
const sessionRef = 'session-ref-1';
const minimum = {
  constraintRef: 'constraint-ref',
  materialStateRef: 'rule-state-ref',
  minimumDurationMicroseconds: 86_400_000_000,
  strength: 'soft' as const,
  evaluation: 'pending' as const,
};

function session(
  overrides: Partial<TemporalSessionView> = {},
): TemporalSessionView {
  return {
    sessionRef,
    subjectNativeRef: activityRef,
    timingMaterialStateRef: 'timing-start',
    startedAt: '2026-09-24T10:00:00Z',
    endedAt: null,
    open: true,
    replayed: false,
    paused: false,
    evaluatedAt: '2026-09-24T10:00:01Z',
    elapsedSeconds: 0,
    pausedSeconds: 0,
    activeSeconds: 0,
    durationEvaluations: [minimum],
    ...overrides,
  };
}

beforeEach(() => {
  vi.stubGlobal('crypto', { randomUUID: () => 'operation-id' });
  Object.values(source).forEach((mock) => mock.mockReset());
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('SessionSubjectControls B08-D whole workflow', () => {
  it('rehydrates an unplaced Activity through pause, resume, end and a separate start', async () => {
    const started = session();
    const paused = session({
      timingMaterialStateRef: 'timing-paused',
      paused: true,
      elapsedSeconds: 70,
      pausedSeconds: 10,
      activeSeconds: 60,
    });
    const resumed = session({
      timingMaterialStateRef: 'timing-resumed',
      elapsedSeconds: 85,
      pausedSeconds: 25,
      activeSeconds: 60,
    });
    const ended = session({
      timingMaterialStateRef: 'timing-ended',
      open: false,
      endedAt: '2026-09-24T10:02:00Z',
      elapsedSeconds: 120,
      pausedSeconds: 25,
      activeSeconds: 95,
      durationEvaluations: [{ ...minimum, evaluation: 'violated' }],
    });
    const second = session({
      sessionRef: 'session-ref-2',
      timingMaterialStateRef: 'timing-second',
    });
    let canonical: TemporalSessionView[] = [];
    source.list.mockImplementation(async () => canonical);
    source.start.mockImplementation(async () => {
      canonical = canonical.length === 0 ? [started] : [ended, second];
      return canonical[canonical.length - 1];
    });
    source.pause.mockImplementation(async () => {
      canonical = [paused];
      return paused;
    });
    source.resume.mockImplementation(async () => {
      canonical = [resumed];
      return resumed;
    });
    source.end.mockImplementation(async () => {
      canonical = [ended];
      return ended;
    });

    const mounted = render(
      <SessionSubjectControls kind="activity" subjectRef={activityRef} label="Focus" />,
    );
    await waitFor(() => expect(source.list).toHaveBeenCalledWith('activity', activityRef));
    fireEvent.click(screen.getByRole('button', { name: 'Avvia' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Pausa' })).toBeTruthy());
    expect(source.start).toHaveBeenCalledWith('activity', activityRef, 'operation-id');
    expect(document.querySelector('[data-session-duration-evaluation="pending"]')?.textContent)
      .toContain('in corso');

    fireEvent.click(screen.getByRole('button', { name: 'Pausa' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Riprendi' })).toBeTruthy());
    expect(source.pause).toHaveBeenCalledWith(sessionRef, 'timing-start', 'operation-id');
    expect(screen.queryByRole('button', { name: 'Termina' })).toBeNull();
    mounted.unmount();

    render(<SessionSubjectControls kind="activity" subjectRef={activityRef} label="Focus" />);
    await waitFor(() => expect(screen.getByRole('button', { name: 'Riprendi' })).toBeTruthy());
    expect(screen.getByLabelText('Durata sessione').textContent)
      .toContain('Attiva 1:00 · Pausa 0:10 · Totale 1:10');
    fireEvent.click(screen.getByRole('button', { name: 'Riprendi' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Termina' })).toBeTruthy());
    expect(source.resume).toHaveBeenCalledWith(sessionRef, 'timing-paused', 'operation-id');

    fireEvent.click(screen.getByRole('button', { name: 'Termina' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Avvia' })).toBeTruthy());
    expect(source.end).toHaveBeenCalledWith(sessionRef, 'timing-resumed', 'operation-id');
    expect(document.querySelector('[data-session-duration-evaluation="violated"]')?.textContent)
      .toContain('non raggiunto');

    fireEvent.click(screen.getByRole('button', { name: 'Avvia' }));
    await waitFor(() => expect(screen.getByRole('button', { name: 'Pausa' })).toBeTruthy());
    expect(source.start).toHaveBeenCalledTimes(2);
    expect(document.querySelector('[data-session-duration-evaluation="pending"]')?.textContent)
      .toContain('in corso');
  });


  it('reloads canonical state and exposes the conflict when this view is stale', async () => {
    const started = session();
    const paused = session({
      timingMaterialStateRef: 'timing-paused',
      paused: true,
      elapsedSeconds: 90,
      pausedSeconds: 30,
      activeSeconds: 60,
    });
    source.list.mockResolvedValueOnce([started]).mockResolvedValue([paused]);
    source.pause.mockRejectedValue(
      new Error('Session pause conflicts with current timing.'),
    );

    render(
      <SessionSubjectControls kind="activity" subjectRef={activityRef} label="Focus" />,
    );
    await waitFor(() => expect(screen.getByRole('button', { name: 'Pausa' })).toBeTruthy());

    fireEvent.click(screen.getByRole('button', { name: 'Pausa' }));

    await waitFor(() => expect(screen.getByRole('button', { name: 'Riprendi' })).toBeTruthy());
    expect(screen.getByRole('status').textContent)
      .toContain('Session pause conflicts with current timing.');
  });

  it('keeps an Occurrence Session free of the direct Activity TC-009 badge', async () => {
    source.list.mockResolvedValue([
      session({ subjectNativeRef: occurrenceRef, durationEvaluations: [] }),
    ]);
    render(
      <SessionSubjectControls kind="occurrence" subjectRef={occurrenceRef} label="Routine" />,
    );
    await waitFor(() => expect(screen.getByRole('button', { name: 'Pausa' })).toBeTruthy());
    expect(source.list).toHaveBeenCalledWith('occurrence', occurrenceRef);
    expect(document.querySelector('[data-session-duration-evaluation]')).toBeNull();
  });
});
