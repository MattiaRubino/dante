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
    expect(within(panel).queryByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    })).toBeNull();
    expect(within(panel).queryByText('Per questa programmazione è disponibile un solo fuso orario.')).toBeNull();
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

  it('shows only one picker when distinct end zones are disallowed, even for a legacy custom selection', () => {
    const onZonesChange = vi.fn();
    render(
      <TemporalTimeZoneControl
        zoneId="Europe/Rome"
        endZoneId="Asia/Tokyo"
        allowDistinctZones={false}
        allowFloating={false}
        date="2026-11-18"
        onChange={vi.fn()}
        onZonesChange={onZonesChange}
      />,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fuso orario: Personalizzato' }));
    const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    expect(within(panel).queryByRole('checkbox', {
      name: 'Utilizza fusi orari diversi per inizio e fine',
    })).toBeNull();
    expect(within(panel).queryByText('Fuso orario di fine')).toBeNull();
    expect(within(panel).getByRole('heading', { name: 'Fuso orario' })).toBeTruthy();
    fireEvent.click(within(panel).getByRole('button', { name: 'OK' }));
    expect(onZonesChange).toHaveBeenCalledTimes(1);
    expect(onZonesChange).toHaveBeenCalledWith('Europe/Rome', null);
  });

  it('keeps a local modal active on outside interaction and traps focus until OK/Annulla/Escape', () => {
    const onChange = vi.fn();
    const outsideClick = vi.fn();
    const { container } = render(
      <div className="temporal-create-composer">
        <button type="button" onClick={outsideClick}>Other editor control</button>
        <TemporalTimeZoneControl
          zoneId="Europe/Rome"
          date="2026-11-18"
          onChange={onChange}
        />
      </div>,
    );
    const editor = container.querySelector<HTMLElement>('.temporal-create-composer');
    const trigger = screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' });
    if (!editor) throw new Error('Missing modal owner.');
    trigger.focus();
    fireEvent.click(trigger);

    const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    expect(panel.getAttribute('aria-modal')).toBe('true');
    expect(editor.inert).toBe(true);
    expect(document.querySelector('.temporal-create-timezone-interaction-shield')).toBeTruthy();
    expect(document.querySelector('.temporal-create-timezone-editor-dimmer')).toBeTruthy();
    expect(panel.contains(document.activeElement)).toBe(true);

    const outside = screen.getByRole('button', { name: 'Other editor control' });
    fireEvent.pointerDown(outside);
    fireEvent.click(outside);
    expect(outsideClick).not.toHaveBeenCalled();
    fireEvent.pointerDown(document.querySelector('.temporal-create-timezone-interaction-shield')!);
    expect(panel.isConnected).toBe(true);
    expect(onChange).not.toHaveBeenCalled();

    const first = within(panel).getByRole('button', { name: /GMT/ });
    const last = within(panel).getByRole('button', { name: 'OK' });
    last.focus();
    fireEvent.keyDown(last, { key: 'Tab' });
    expect(document.activeElement).toBe(first);
    first.focus();
    fireEvent.keyDown(first, { key: 'Tab', shiftKey: true });
    expect(document.activeElement).toBe(last);

    outside.focus();
    expect(panel.contains(document.activeElement)).toBe(true);
    fireEvent.keyDown(panel, { key: 'Escape' });
    expect(screen.queryByRole('dialog', { name: 'Imposta fuso orario' })).toBeNull();
    expect(editor.inert).toBe(false);
    expect(document.activeElement).toBe(trigger);
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not discard a staged timezone selection on an outside click', () => {
    const onChange = vi.fn();
    const { container } = render(
      <div className="temporal-create-composer">
        <button type="button">Background control</button>
        <TemporalTimeZoneControl zoneId="Europe/Rome"
          date="2026-11-18" onChange={onChange} />
      </div>,
    );
    const trigger = screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' });
    fireEvent.click(trigger);
    const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    fireEvent.click(within(panel).getByRole('button', { name: /GMT/ }));
    fireEvent.change(within(panel).getByRole('searchbox', { name: 'Cerca fuso orario' }), {
      target: { value: 'Europe/Paris' },
    });
    fireEvent.click(within(panel).getByRole('option', { name: /Europe\/Paris/ }));
    fireEvent.pointerDown(container);
    expect(panel.isConnected).toBe(true);
    expect(onChange).not.toHaveBeenCalled();
    fireEvent.click(within(panel).getByRole('button', { name: 'OK' }));
    expect(onChange).toHaveBeenCalledTimes(1);
    expect(onChange).toHaveBeenCalledWith('Europe/Paris');
    expect(document.activeElement).toBe(trigger);
  });

  it.each(['timeline-event-modal--edit', 'timeline-recurring-series-editor'] as const)(
    'dims and locks the %s editor with the shared modal dialog',
    (ownerClass) => {
      const onChange = vi.fn();
      const { container } = render(
        <div className={ownerClass}>
          <TemporalTimeZoneControl zoneId="Europe/Rome"
            date="2026-11-18" onChange={onChange} />
        </div>,
      );
      const owner = container.querySelector<HTMLElement>(`.${ownerClass}`);
      if (!owner) throw new Error('Missing edit surface.');
      const trigger = screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' });
      fireEvent.click(trigger);
      expect(owner.inert).toBe(true);
      const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
      expect(panel.getAttribute('aria-modal')).toBe('true');
      expect(document.querySelector('.temporal-create-timezone-editor-dimmer')).toBeTruthy();
      fireEvent.click(within(panel).getByRole('button', { name: 'Annulla' }));
      expect(owner.inert).toBe(false);
      expect(document.activeElement).toBe(trigger);
      expect(onChange).not.toHaveBeenCalled();
    },
  );

  it('locks the outer Edit modal rather than only the nested recurring form', () => {
    const { container } = render(
      <div className="timeline-event-modal--edit">
        <div className="timeline-recurring-series-editor">
          <TemporalTimeZoneControl zoneId="Europe/Rome"
            date="2026-11-18" onChange={vi.fn()} />
        </div>
      </div>,
    );
    fireEvent.click(screen.getByRole('button', { name: 'Fuso orario: Europe/Rome' }));
    const outer = container.querySelector<HTMLElement>('.timeline-event-modal--edit');
    const inner = container.querySelector<HTMLElement>('.timeline-recurring-series-editor');
    expect(outer?.inert).toBe(true);
    expect(inner?.inert).not.toBe(true);
    fireEvent.keyDown(screen.getByRole('dialog', { name: 'Imposta fuso orario' }), {
      key: 'Escape',
    });
    expect(outer?.inert).toBe(false);
  });
});
