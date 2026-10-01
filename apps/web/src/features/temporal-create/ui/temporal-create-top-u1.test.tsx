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

  it('keeps explicit start/end dates on the timed row and uses only the DANTE calendar', () => {
    renderEntry();

    const startDate = screen.getByRole('button', { name: /Data inizio:/ });
    const endDate = screen.getByRole('button', { name: /Data fine:/ });
    expect(startDate).toBeTruthy();
    expect(endDate).toBeTruthy();
    expect(document.querySelector('input[type="date"]')).toBeNull();

    fireEvent.click(startDate);
    const calendar = screen.getByRole('dialog', { name: 'Data inizio' });
    expect(calendar).toBeTruthy();
    expect(within(calendar).queryByText('Cancella')).toBeNull();
  });

  it('keeps start/end time controls independent and rejects invalid manual time', () => {
    renderEntry();

    const startRaw = document.querySelector<HTMLInputElement>(
      '[data-create-path="startTime"]',
    );
    const endRaw = document.querySelector<HTMLInputElement>(
      '[data-create-path="endTime"]',
    );
    if (!startRaw || !endRaw) {
      throw new Error('Expected canonical start/end time inputs.');
    }
    const before = startRaw.value;
    const endBefore = endRaw.value;

    const hour = screen.getByLabelText('Inizio: ore') as HTMLInputElement;
    const minute = screen.getByLabelText('Inizio: minuti') as HTMLInputElement;

    fireEvent.click(
      screen.getByRole('button', { name: 'Inizio: aumenta 15 minuti' }),
    );
    expect(startRaw.value).toBe(addMinutes(before, 15));
    expect(endRaw.value).toBe(endBefore);

    const validHour = hour.value;
    fireEvent.change(hour, { target: { value: 'ab' } });
    expect(hour.value).toBe(validHour);

    fireEvent.change(hour, { target: { value: '99' } });
    expect(hour.value).toBe('99');
    fireEvent.blur(hour);
    expect(hour.value).toBe(validHour);

    const validMinute = minute.value;
    fireEvent.change(minute, { target: { value: '99' } });
    expect(minute.value).toBe('99');
    fireEvent.blur(minute);
    expect(minute.value).toBe(validMinute);
  });

  it('uses the clock only for quarter-hour choices and the arrow for day bands', () => {
    renderEntry();

    const startRaw = document.querySelector<HTMLInputElement>(
      '[data-create-path="startTime"]',
    );
    const endRaw = document.querySelector<HTMLInputElement>(
      '[data-create-path="endTime"]',
    );
    if (!startRaw || !endRaw) {
      throw new Error('Expected canonical time inputs.');
    }

    fireEvent.click(
      screen.getByRole('button', { name: 'Inizio: scegli orario' }),
    );
    const picker = screen.getByRole('dialog', { name: 'Inizio' });
    expect(within(picker).queryByText('Mattina')).toBeNull();
    fireEvent.click(within(picker).getByRole('button', { name: '17:15' }));
    expect(startRaw.value).toBe('17:15');

    fireEvent.click(screen.getByRole('button', { name: 'Fasce orarie' }));
    const bands = screen.getByRole('dialog', { name: 'Fasce orarie' });
    fireEvent.click(
      within(bands).getByRole('button', { name: /Mattina.*06:00.*12:00/ }),
    );
    expect(startRaw.value).toBe('06:00');
    expect(endRaw.value).toBe('12:00');

    const zoneTrigger = screen.getByRole('button', {
      name: /Fuso orario:/,
    });
    fireEvent.click(zoneTrigger);
    fireEvent.click(screen.getByRole('button', { name: 'Ora locale' }));
    expect(
      screen.getByRole('button', { name: /Fuso orario: Ora locale/ }),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: /Fuso orario: Ora locale/ }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Europe/Rome' }));
    expect(
      screen.getByRole('button', { name: /Fuso orario: Europe\/Rome/ }),
    ).toBeTruthy();
  });

  it('keeps the rail open on backdrop clicks while pinned', () => {
    renderEntry();

    const backdrop = document.querySelector<HTMLElement>(
      '[data-temporal-create="backdrop"]',
    );
    if (!backdrop) throw new Error('Expected Create backdrop.');

    const pin = screen.getByRole('button', {
      name: 'Mantieni aperto il pannello Crea',
    });
    fireEvent.click(pin);
    expect(pin.getAttribute('aria-pressed')).toBe('true');

    fireEvent.pointerDown(backdrop);
    expect(document.querySelector('[data-temporal-create="composer"]')).toBeTruthy();

    const unpin = screen.getByRole('button', { name: 'Sblocca pannello Crea' });
    fireEvent.click(unpin);
    fireEvent.pointerDown(backdrop);
    expect(document.querySelector('[data-temporal-create="composer"]')).toBeNull();
  });

  it('promotes Advanced to a central viewport surface without losing the Quick draft', () => {
    renderEntry();

    const quickComposer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    expect(quickComposer?.closest('[data-home-context-create-host]')).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Annulla' })).toBeNull();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Bozza preservata' },
    });
    fireEvent.change(screen.getByLabelText('Life Area (opzionale)'), {
      target: { value: 'Nuova area' },
    });

    const advanced = screen.getByRole('button', { name: /Opzioni avanzate/ });
    expect(advanced.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(advanced);

    const advancedComposer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    expect(advancedComposer?.dataset.temporalCreateSurface).toBe('advanced');
    expect(advancedComposer?.closest('[data-home-context-create-host]')).toBeNull();
    expect(advancedComposer?.parentElement?.parentElement).toBe(document.body);
    expect((screen.getByPlaceholderText('Titolo') as HTMLInputElement).value).toBe(
      'Bozza preservata',
    );
    expect(
      (screen.getByLabelText('Life Area (opzionale)') as HTMLInputElement).value,
    ).toBe('Nuova area');

    const hide = screen.getByRole('button', { name: /Nascondi opzioni avanzate/ });
    expect(hide.getAttribute('aria-expanded')).toBe('true');
    fireEvent.click(hide);

    const restoredQuick = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    expect(restoredQuick?.dataset.temporalCreateSurface).toBe('base');
    expect(restoredQuick?.closest('[data-home-context-create-host]')).toBeTruthy();
    expect((screen.getByPlaceholderText('Titolo') as HTMLInputElement).value).toBe(
      'Bozza preservata',
    );
  });
});
