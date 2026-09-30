// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
    configurable: true,
    value: vi.fn(),
  });
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

afterAll(() => {
  Reflect.deleteProperty(HTMLElement.prototype, 'scrollIntoView');
});

function renderEntry() {
  const rendered = render(
    <>
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from('2026-09-30')}
        contexts={[
          {
            id: 'personale',
            label: 'Personale',
            tone: 'personal',
          },
        ]}
        onPreview={() => undefined}
        onApplied={() => false}
        creationEnabled={false}
      />
    </>,
  );
  const quickAdd = rendered.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!quickAdd) {
    throw new Error('Expected Create trigger.');
  }
  fireEvent.click(quickAdd);
  return rendered;
}

function addMinutes(value: string, delta: number): string {
  const [hour = '0', minute = '0'] = value.split(':');
  const total =
    ((Number(hour) * 60 + Number(minute) + delta) % 1440 + 1440) % 1440;
  return `${String(Math.floor(total / 60)).padStart(2, '0')}:${String(
    total % 60,
  ).padStart(2, '0')}`;
}

describe('Temporal Create U1 top controls', () => {
  it('keeps the top hierarchy compact and honest about deferred types', () => {
    renderEntry();

    expect(screen.getByPlaceholderText('Titolo')).toBeTruthy();
    expect(screen.getByRole('radio', { name: 'Attività' })).toBeTruthy();
    expect(screen.getByRole('radio', { name: 'Evento' })).toBeTruthy();

    const timer = screen.getByRole('button', { name: /Timer/ });
    const alarm = screen.getByRole('button', { name: /Sveglia/ });
    expect((timer as HTMLButtonElement).disabled).toBe(true);
    expect((alarm as HTMLButtonElement).disabled).toBe(true);

    expect(screen.getByRole('radio', { name: 'Orario' })).toBeTruthy();
    expect(screen.getByRole('radio', { name: 'Tutto il giorno' })).toBeTruthy();
    expect(screen.getByRole('radio', { name: 'Da collocare' })).toBeTruthy();
    expect(screen.queryByRole('radio', { name: 'Fascia' })).toBeNull();

    expect(
      document.querySelector('.temporal-create-composer__heading-copy'),
    ).toBeNull();
    expect(document.querySelector('.temporal-create-intent-summary')).toBeNull();
  });

  it('supports protected manual time, split stepping, picker presets and timezone selection', () => {
    renderEntry();

    const start = screen.getByLabelText('Inizio') as HTMLInputElement;
    const before = start.value;

    fireEvent.focus(start);
    expect(
      screen.getByRole('group', { name: 'Inizio: modifica ore e minuti' }),
    ).toBeTruthy();
    fireEvent.click(
      screen.getByRole('button', { name: 'Inizio: aumenta 15 minuti' }),
    );
    expect(start.value).toBe(addMinutes(before, 15));

    const lastValid = start.value;
    fireEvent.change(start, { target: { value: '15:asdo' } });
    expect(start.value).toBe(lastValid);

    fireEvent.change(start, { target: { value: '29:99' } });
    expect(start.value).toBe('29:99');
    fireEvent.blur(start);
    expect(start.value).toBe(lastValid);

    fireEvent.click(
      screen.getByRole('button', { name: 'Inizio: scegli orario' }),
    );
    const picker = screen.getByRole('dialog', { name: 'Inizio' });
    fireEvent.click(within(picker).getByRole('button', { name: /Mattina/ }));
    expect(start.value).toBe('08:00');

    const zoneTrigger = screen.getByRole('button', {
      name: /Fuso orario: Ora locale/,
    });
    fireEvent.click(zoneTrigger);
    fireEvent.click(screen.getByRole('button', { name: 'Europe/Rome' }));

    expect(
      screen.getByRole('button', { name: /Fuso orario: Europe\/Rome/ }),
    ).toBeTruthy();
  });

  it('toggles advanced options from the footer action row', () => {
    renderEntry();

    const advanced = screen.getByRole('button', { name: /Opzioni avanzate/ });
    expect(advanced.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(advanced);

    const hide = screen.getByRole('button', { name: /Nascondi opzioni avanzate/ });
    expect(hide.getAttribute('aria-expanded')).toBe('true');
    fireEvent.click(hide);

    expect(
      screen.getByRole('button', { name: /Opzioni avanzate/ }).getAttribute(
        'aria-expanded',
      ),
    ).toBe('false');
  });
});
