import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useState } from 'react';

import { HomeCreateInteractionBridge } from './home-create-interaction-bridge';

function Harness({ onEscape }: { onEscape: () => void }) {
  const [date, setDate] = useState('2026-10-01');
  const [time, setTime] = useState('09:00');

  return (
    <>
      <HomeCreateInteractionBridge />
      <div
        data-temporal-create="composer"
        onKeyDown={(event) => {
          if (event.key === 'Escape') onEscape();
        }}
      >
        <fieldset data-create-path="timeSemantics">
          <button type="button" role="radio" aria-checked="true">
            Orario
          </button>
        </fieldset>
        <input
          aria-label="Data"
          data-create-path="date"
          value={date}
          onChange={(event) => setDate(event.currentTarget.value)}
        />
        <input
          aria-label="Ora"
          data-create-path="startTime"
          value={time}
          onChange={(event) => setTime(event.currentTarget.value)}
        />
      </div>
      <section
        className="timeline-day-section"
        data-timeline-date="2026-10-02"
        data-testid="timeline-day"
      />
      <button type="button">Fuori</button>
    </>
  );
}

afterEach(() => {
  cleanup();
});

describe('Home U1 Create interaction bridge', () => {
  it('requests close when pointer input happens outside Create and outside Timeline', () => {
    const onEscape = vi.fn();
    render(<Harness onEscape={onEscape} />);

    fireEvent.pointerDown(screen.getByRole('button', { name: 'Fuori' }));

    expect(onEscape).toHaveBeenCalledOnce();
  });

  it('re-seeds an open Create draft from an empty Timeline point instead of closing it', () => {
    const onEscape = vi.fn();
    render(<Harness onEscape={onEscape} />);
    const day = screen.getByTestId('timeline-day');
    vi.spyOn(day, 'getBoundingClientRect').mockReturnValue({
      x: 0,
      y: 0,
      width: 400,
      height: 1440,
      top: 0,
      right: 400,
      bottom: 1440,
      left: 0,
      toJSON: () => ({}),
    });

    fireEvent.pointerDown(day, { clientY: 615 });

    expect((screen.getByLabelText('Data') as HTMLInputElement).value).toBe(
      '2026-10-02',
    );
    expect((screen.getByLabelText('Ora') as HTMLInputElement).value).toBe(
      '10:15',
    );
    expect(onEscape).not.toHaveBeenCalled();
  });
});
