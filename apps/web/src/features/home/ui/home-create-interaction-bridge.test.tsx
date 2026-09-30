import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useState } from 'react';

import { HomeCreateInteractionBridge } from './home-create-interaction-bridge';

function Harness({ onEscape }: { onEscape: () => void }) {
  const [date, setDate] = useState('2026-10-01');
  const [time, setTime] = useState('09:00');
  const [pickerOpen, setPickerOpen] = useState(false);

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
        <div className="temporal-create-time-control">
          <div className="temporal-create-inline-time-editor">
            <div className="temporal-create-time-segment">
              <input aria-label="Inizio: ore" defaultValue="17" />
            </div>
            <div className="temporal-create-time-segment">
              <input aria-label="Inizio: minuti" defaultValue="30" />
            </div>
          </div>
          <button
            type="button"
            className="temporal-create-clock-trigger"
            aria-label="Inizio: scegli orario"
            aria-expanded={pickerOpen}
            onClick={() => setPickerOpen((current) => !current)}
          >
            clock
          </button>
          {pickerOpen ? <div role="dialog" aria-label="Inizio" /> : null}
        </div>
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

  it('consumes Timeline double-click while Create is open so no second invocation leaks through', () => {
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
    const leakedDoubleClick = vi.fn();
    document.addEventListener('dblclick', leakedDoubleClick, true);

    fireEvent.doubleClick(day, { clientY: 720 });

    expect((screen.getByLabelText('Data') as HTMLInputElement).value).toBe(
      '2026-10-02',
    );
    expect((screen.getByLabelText('Ora') as HTMLInputElement).value).toBe(
      '12:00',
    );
    expect(leakedDoubleClick).not.toHaveBeenCalled();
    expect(onEscape).not.toHaveBeenCalled();

    document.removeEventListener('dblclick', leakedDoubleClick, true);
  });

  it('selects a time segment, closes its clock picker and advances hours to minutes', async () => {
    const onEscape = vi.fn();
    render(<Harness onEscape={onEscape} />);
    const hour = screen.getByLabelText('Inizio: ore') as HTMLInputElement;
    const minute = screen.getByLabelText('Inizio: minuti') as HTMLInputElement;
    const clock = screen.getByRole('button', { name: 'Inizio: scegli orario' });

    fireEvent.click(clock);
    expect(screen.getByRole('dialog', { name: 'Inizio' })).toBeTruthy();

    fireEvent.focus(hour);
    await Promise.resolve();
    expect(screen.queryByRole('dialog', { name: 'Inizio' })).toBeNull();
    expect(hour.selectionStart).toBe(0);
    expect(hour.selectionEnd).toBe(2);

    fireEvent.input(hour, { target: { value: '18' } });
    await Promise.resolve();
    expect(document.activeElement).toBe(minute);
    expect(minute.selectionStart).toBe(0);
    expect(minute.selectionEnd).toBe(2);
  });
});
