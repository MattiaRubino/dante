// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TemporalTimeZoneControl, timeZoneGmtOffset } from './temporal-time-zone-control';

afterEach(() => {
  cleanup();
});

describe('shared temporal timezone configuration dialog', () => {
  it('computes the GMT offset for the selected date, including DST and fractional offsets', () => {
    expect(timeZoneGmtOffset('Europe/Rome', '2026-01-15')).toBe('GMT+01:00');
    expect(timeZoneGmtOffset('Europe/Rome', '2026-07-15')).toBe('GMT+02:00');
    expect(timeZoneGmtOffset('Asia/Kathmandu', '2026-07-15')).toBe('GMT+05:45');
  });

  it('keeps a selected zone in the draft until OK and discards it on Annulla', () => {
    const onChange = vi.fn();
    render(
      <TemporalTimeZoneControl
        zoneId="Europe/Rome"
        date="2026-11-18"
        onChange={onChange}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' }));
    const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    expect(within(panel).getByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    })).toHaveProperty('disabled', true);
    fireEvent.click(within(panel).getByRole('button', { name: /GMT\+01:00.*Europe\/Rome/ }));
    fireEvent.change(within(panel).getByRole('searchbox', { name: 'Cerca fuso orario' }), {
      target: { value: 'Europe/Paris' },
    });
    const paris = within(panel).getByRole('option', { name: /Europe\/Paris/ });
    fireEvent.pointerDown(paris);
    expect(panel.isConnected).toBe(true);
    fireEvent.click(paris);
    expect(onChange).not.toHaveBeenCalled();
    fireEvent.click(within(panel).getByRole('button', { name: 'Annulla' }));
    expect(onChange).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' })).toBeTruthy();
  });

  it('commits both zones atomically, preserves selections when reopened, and collapses to one', () => {
    const onChange = vi.fn();
    const onZonesChange = vi.fn();
    const { rerender } = render(
      <TemporalTimeZoneControl
        zoneId="Europe/Rome"
        date="2026-11-18"
        onChange={onChange}
        onZonesChange={onZonesChange}
        allowDistinctZones
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' }));
    const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    fireEvent.click(within(panel).getByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    }));
    const endPicker = within(panel).getByText('Fuso orario di fine')
      .closest('.temporal-zone-dialog__picker');
    if (!endPicker) throw new Error('Missing end-zone picker');
    fireEvent.click(within(endPicker as HTMLElement).getByRole('button'));
    fireEvent.change(within(endPicker as HTMLElement).getByRole('searchbox', {
      name: 'Cerca fuso orario',
    }), { target: { value: 'Asia/Tokyo' } });
    fireEvent.click(within(endPicker as HTMLElement).getByRole('option', {
      name: /Asia\/Tokyo/,
    }));
    fireEvent.click(within(panel).getByRole('button', { name: 'OK' }));
    expect(onChange).not.toHaveBeenCalled();
    expect(onZonesChange).toHaveBeenCalledTimes(1);
    expect(onZonesChange).toHaveBeenCalledWith('Europe/Rome', 'Asia/Tokyo');

    rerender(
      <TemporalTimeZoneControl
        zoneId="Europe/Rome"
        endZoneId="Asia/Tokyo"
        date="2026-11-18"
        onChange={onChange}
        onZonesChange={onZonesChange}
        allowDistinctZones
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fuso orario: Personalizzato' }));
    const reopened = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    const checkbox = within(reopened).getByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    });
    expect(checkbox).toHaveProperty('checked', true);
    expect(within(reopened).getByText(/GMT\+09:00.*Asia\/Tokyo/)).toBeTruthy();
    fireEvent.click(checkbox);
    fireEvent.click(within(reopened).getByRole('button', { name: 'OK' }));
    expect(onZonesChange).toHaveBeenLastCalledWith('Europe/Rome', null);
  });
});
