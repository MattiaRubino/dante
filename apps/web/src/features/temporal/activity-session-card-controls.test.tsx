import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { TemporalSessionCapabilityDataSource } from './remote-session-capability-data-source';
import { ActivitySessionCardControls } from './activity-session-card-controls';

vi.mock('./session-subject-controls', () => ({
  SessionSubjectControls: (props: Record<string, unknown>) => (
    <div
      data-testid="session-runtime"
      data-kind={String(props.kind)}
      data-subject={String(props.subjectRef)}
      data-variant={String(props.variant)}
      data-interactive={String(props.interactive)}
    />
  ),
}));

const ACTIVITY_REF = '0199a111-1111-7111-8111-111111111111';

afterEach(() => cleanup());

describe('Activity Session controls on Timeline cards', () => {
  it('mounts compact B08 runtime only when canonical Session capability is enabled', async () => {
    const source: TemporalSessionCapabilityDataSource = {
      activityEnabled: vi.fn(async () => true),
    };

    render(
      <ActivitySessionCardControls
        activityRef={ACTIVITY_REF}
        label="Scrivere articolo"
        source={source}
      />,
    );

    const runtime = await screen.findByTestId('session-runtime');
    expect(runtime.dataset.kind).toBe('activity');
    expect(runtime.dataset.subject).toBe(ACTIVITY_REF);
    expect(runtime.dataset.variant).toBe('card');
    expect(runtime.dataset.interactive).toBe('true');
  });

  it('fails closed when Session capability is absent or unreadable', async () => {
    const disabled: TemporalSessionCapabilityDataSource = {
      activityEnabled: vi.fn(async () => false),
    };
    const first = render(
      <ActivitySessionCardControls
        activityRef={ACTIVITY_REF}
        label="Senza sessione"
        source={disabled}
      />,
    );
    await waitFor(() => expect(disabled.activityEnabled).toHaveBeenCalled());
    expect(screen.queryByTestId('session-runtime')).toBeNull();
    first.unmount();

    const unavailable: TemporalSessionCapabilityDataSource = {
      activityEnabled: vi.fn(async () => {
        throw new Error('offline');
      }),
    };
    render(
      <ActivitySessionCardControls
        activityRef={ACTIVITY_REF}
        label="Capability non leggibile"
        source={unavailable}
      />,
    );
    await waitFor(() => expect(unavailable.activityEnabled).toHaveBeenCalled());
    expect(screen.queryByTestId('session-runtime')).toBeNull();
  });
});
