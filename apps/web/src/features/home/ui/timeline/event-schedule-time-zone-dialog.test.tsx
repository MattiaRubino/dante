// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { EventScheduleEditor, type EventScheduleDraft } from './event-schedule-editor';

afterEach(() => cleanup());

const savedDraft: EventScheduleDraft = {
  kind: 'timed',
  startDate: '2026-11-18',
  endDate: '2026-11-18',
  startTime: '09:00',
  endTime: '09:30',
  zoneId: 'Europe/Rome',
  endZoneId: null,
  disambiguation: 'earlier',
};

describe('Event Edit uses the single shared timezone dialog', () => {
  it('commits independent zones in one operation while preserving 30 elapsed minutes', () => {
    const onChange = vi.fn();
    const { rerender } = render(
      <EventScheduleEditor draft={savedDraft} onChange={onChange} disabled={false} error="" />,
    );
    fireEvent.click(screen.getByRole('button', {
      name: 'Fuso orario: Europe/Rome',
    }));
    const dialog = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    fireEvent.click(within(dialog).getByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    }));
    const endField = within(dialog).getByText('Fuso orario di fine')
      .closest('.temporal-zone-dialog__picker');
    if (!endField) throw new Error('Expected end-zone editor.');
    fireEvent.click(within(endField as HTMLElement).getByRole('button'));
    fireEvent.change(within(endField as HTMLElement).getByRole('searchbox', {
      name: 'Cerca fuso orario',
    }), { target: { value: 'Asia/Tokyo' } });
    fireEvent.click(within(endField as HTMLElement).getByRole('option', {
      name: /Asia\/Tokyo/,
    }));
    expect(onChange).not.toHaveBeenCalled();
    fireEvent.click(within(dialog).getByRole('button', { name: 'OK' }));
    expect(onChange).toHaveBeenCalledTimes(1);
    const updated = onChange.mock.calls[0]?.[0] as EventScheduleDraft;
    expect(updated).toMatchObject({
      zoneId: 'Europe/Rome',
      endZoneId: 'Asia/Tokyo',
      startTime: '09:00',
      endTime: '17:30',
      endDate: '2026-11-18',
    });
    rerender(
      <EventScheduleEditor draft={updated} onChange={onChange} disabled={false} error="" />,
    );
    fireEvent.click(screen.getByRole('button', {
      name: 'Fuso orario: Personalizzato',
    }));
    const reopened = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    expect(within(reopened).getByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    })).toHaveProperty('checked', true);
    fireEvent.click(within(reopened).getByRole('button', { name: 'Annulla' }));
    expect(onChange).toHaveBeenCalledTimes(1);
  });

  it('does not put timezone choices inside the start or end clocks', () => {
    render(
      <EventScheduleEditor draft={savedDraft} onChange={vi.fn()} disabled={false} error="" />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fine: scegli orario' }));
    const clock = screen.getByRole('dialog', { name: 'Fine' });
    expect(within(clock).queryByRole('button', { name: /Fuso orario/ })).toBeNull();
    expect(within(clock).getByRole('button', { name: '09:30' })).toBeTruthy();
  });
});
