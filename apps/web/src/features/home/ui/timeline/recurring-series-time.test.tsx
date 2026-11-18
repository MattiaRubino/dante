// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { SeriesIntervalFields } from './recurring-series-editor';

beforeAll(async () => {
  Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    configurable: true,
    value: vi.fn(),
  });
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function renderInterval(onChange = vi.fn(), onTimeZoneChange = vi.fn()) {
  render(
    <SeriesIntervalFields
      selectedDate="2026-11-18"
      wallTime="09:00:00"
      row={{ start_offset_minutes: 0, duration_minutes: 30 }}
      index={0}
      showLabel={false}
      zoneId="Europe/Rome"
      onTimeZoneChange={onTimeZoneChange}
      onChange={onChange}
    />,
  );
  return { onChange, onTimeZoneChange };
}

it('uses the same time bands as Create, including a night that crosses midnight', () => {
  const { onChange } = renderInterval();
  fireEvent.click(screen.getByRole('button', { name: 'Fasce orarie' }));
  const bands = screen.getByRole('dialog', { name: 'Fasce orarie' });
  fireEvent.click(within(bands).getByRole('button', { name: /Notte.*23:00.*06:00/ }));
  expect(onChange).toHaveBeenLastCalledWith({
    start_offset_minutes: 840,
    duration_minutes: 420,
  });
  expect(screen.queryByRole('dialog', { name: 'Fasce orarie' })).toBeNull();
});

it('preserves duration when editing start and resizes the interval when editing end', () => {
  const { onChange } = renderInterval();
  fireEvent.click(screen.getByRole('button', { name: 'Inizio: scegli orario' }));
  const start = screen.getByRole('dialog', { name: 'Inizio' });
  fireEvent.click(within(start).getByRole('button', { name: '10:00' }));
  expect(onChange).toHaveBeenLastCalledWith({
    start_offset_minutes: 60,
    duration_minutes: 30,
  });
  fireEvent.click(screen.getByRole('button', { name: 'Fine: scegli orario' }));
  const end = screen.getByRole('dialog', { name: 'Fine' });
  fireEvent.click(within(end).getByRole('button', { name: '10:30' }));
  expect(onChange).toHaveBeenLastCalledWith({
    start_offset_minutes: 0,
    duration_minutes: 90,
  });
});

it('opens the common timezone sidecar while retaining the series-wide zone contract', () => {
  const { onTimeZoneChange } = renderInterval();
  fireEvent.click(screen.getByRole('button', { name: 'Inizio: scegli orario' }));
  const picker = screen.getByRole('dialog', { name: 'Inizio' });
  fireEvent.click(within(picker).getByRole('button', { name: /Inizio: Fuso orario:/ }));
  const zones = screen.getByRole('dialog', { name: 'Scegli fuso orario' });
  expect(zones.hasAttribute('data-temporal-create-portal')).toBe(true);
  fireEvent.change(within(zones).getByRole('searchbox', { name: 'Cerca fuso orario' }), {
    target: { value: 'Europe/Paris' },
  });
  const paris = within(zones).getByRole('button', { name: 'Europe/Paris' });
  fireEvent.pointerDown(paris);
  expect(zones.isConnected).toBe(true);
  fireEvent.click(paris);
  expect(onTimeZoneChange).toHaveBeenCalledTimes(1);
  expect(onTimeZoneChange).toHaveBeenCalledWith('Europe/Paris');
});
