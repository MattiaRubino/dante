import { domElement } from '../../../test-support/dom-element';
// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react';
import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomeCreateInteractionBridge } from '../../home/ui/home-create-interaction-bridge';
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
      <HomeCreateInteractionBridge />
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
    (((Number(hour) * 60 + Number(minute) + delta) % 1440) + 1440) % 1440;
  return `${String(Math.floor(total / 60)).padStart(2, '0')}:${String(
    total % 60,
  ).padStart(2, '0')}`;
}

function clockValues() {
  const start = document.querySelector<HTMLInputElement>(
    '[data-create-path="startTime"]',
  );
  const end = document.querySelector<HTMLInputElement>(
    '[data-create-path="endTime"]',
  );
  if (!start || !end) throw new Error('Expected both canonical time inputs.');
  return { start, end };
}

function setClock(label: 'Inizio' | 'Fine', value: string) {
  const { start, end } = clockValues();
  fireEvent.change(label === 'Inizio' ? start : end, {
    target: { value },
  });
}

describe('Temporal Create U1 top controls', () => {
  it('returns an automatically rolled end date to today when the user enters a later end clock', () => {
    renderEntry();
    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));

    const startHour = domElement(
      screen.getByLabelText('Inizio: ore'),
      HTMLInputElement,
    );
    const endHour = screen.getByLabelText('Fine: ore');
    const endMinute = screen.getByLabelText('Fine: minuti');
    fireEvent.change(startHour, { target: { value: '15' } });
    fireEvent.blur(startHour);
    fireEvent.change(endHour, { target: { value: '15' } });
    fireEvent.blur(endHour);
    fireEvent.change(endMinute, { target: { value: '45' } });
    fireEvent.blur(endMinute);

    expect(clockValues().start.value).toBe('15:00');
    expect(clockValues().end.value).toBe('15:45');
    expect(
      screen
        .getByRole('button', { name: /^Data fine:/ })
        .getAttribute('data-temporal-date'),
    ).toBe('2026-09-30');
    expect(
      within(screen.getByRole('group', { name: 'Fine' })).getByText('45 min'),
    ).toBeTruthy();
  });

  it.each([
    ['Quick', 'Attività'],
    ['Quick', 'Evento'],
    ['Advanced', 'Attività'],
    ['Advanced', 'Evento'],
  ] as const)(
    'golden clock contract: %s %s arrows and manual edits change only their own endpoint',
    (surface, kind) => {
      renderEntry();
      if (kind === 'Evento') {
        fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
      }
      if (surface === 'Advanced') {
        fireEvent.click(
          screen.getByRole('button', { name: /Opzioni avanzate/ }),
        );
      }

      setClock('Inizio', '09:00');
      setClock('Fine', '12:00');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '09:00',
        '12:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('3 h'),
      ).toBeTruthy();

      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: aumenta ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '10:00',
        '12:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('2 h'),
      ).toBeTruthy();

      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: diminuisci 1 minuto' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '09:59',
        '12:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '2 h 1 min',
        ),
      ).toBeTruthy();

      fireEvent.click(
        screen.getByRole('button', { name: 'Fine: diminuisci ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '09:59',
        '11:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '1 h 1 min',
        ),
      ).toBeTruthy();

      setClock('Inizio', '08:30');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '08:30',
        '11:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '2 h 30 min',
        ),
      ).toBeTruthy();
    },
  );

  it.each([
    ['Quick', 'Attività'],
    ['Quick', 'Evento'],
    ['Advanced', 'Attività'],
    ['Advanced', 'Evento'],
  ] as const)(
    'never rounds a one-minute %s %s interval, including a custom picker value',
    (surface, kind) => {
      renderEntry();
      if (kind === 'Evento') {
        fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
      }
      if (surface === 'Advanced') {
        fireEvent.click(
          screen.getByRole('button', { name: /Opzioni avanzate/ }),
        );
      }

      setClock('Inizio', '10:30');
      setClock('Fine', '10:31');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '10:30',
        '10:31',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('1 min'),
      ).toBeTruthy();

      fireEvent.click(screen.getByRole('button', { name: 'Fine: scegli orario' }));
      const picker = screen.getByRole('dialog', { name: 'Fine' });
      const custom = within(picker).getByRole('button', { name: '10:31' });
      expect(custom.classList.contains('is-selected')).toBe(true);
      expect(
        within(picker).getByRole('button', { name: '10:30' }).classList.contains('is-selected'),
      ).toBe(false);
      fireEvent.click(custom);
      expect(clockValues().end.value).toBe('10:31');

      fireEvent.click(screen.getByRole('button', { name: 'Fine: aumenta 1 minuto' }));
      expect(clockValues().end.value).toBe('10:32');
      fireEvent.click(screen.getByRole('button', { name: 'Fine: diminuisci 1 minuto' }));
      expect(clockValues().end.value).toBe('10:31');

      setClock('Inizio', '10:29');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '10:29',
        '10:31',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('2 min'),
      ).toBeTruthy();
    },
  );

  it.each(['Quick', 'Advanced'] as const)(
    'golden overnight contract: %s preserves the end clock when start crosses it',
    (surface) => {
      renderEntry();
      if (surface === 'Advanced') {
        fireEvent.click(
          screen.getByRole('button', { name: /Opzioni avanzate/ }),
        );
      }
      setClock('Inizio', '21:30');
      setClock('Fine', '23:00');
      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: aumenta ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '22:30',
        '23:00',
      ]);
      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: aumenta ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '23:30',
        '23:00',
      ]);
      expect(
        screen.getByRole('button', { name: /Data fine:.*1 ott/i }),
      ).toBeTruthy();
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '23 h 30 min',
        ),
      ).toBeTruthy();
    },
  );

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
    expect(screen.queryByRole('radio', { name: 'Da collocare' })).toBeNull();
    expect(screen.getByRole('button', { name: 'Salva bozza' })).toBeTruthy();
    expect(screen.queryByRole('radio', { name: 'Fascia' })).toBeNull();

    expect(
      document.querySelector('.temporal-create-composer__heading-copy'),
    ).toBeNull();
    expect(
      document.querySelector('.temporal-create-intent-summary'),
    ).toBeNull();
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

  it('keeps the end clock stable when start time changes and rejects invalid manual time', () => {
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

    const hour = domElement(
      screen.getByLabelText('Inizio: ore'),
      HTMLInputElement,
    );
    const minute = domElement(
      screen.getByLabelText('Inizio: minuti'),
      HTMLInputElement,
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Inizio: aumenta 1 minuto' }),
    );
    expect(startRaw.value).toBe(addMinutes(before, 1));
    expect(endRaw.value).toBe(endBefore);

    fireEvent.change(hour, { target: { value: '23' } });
    fireEvent.blur(hour);
    expect(startRaw.value).toMatch(/^23:/);
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
    expect(
      domElement(screen.getByLabelText('Ricorda'), HTMLSelectElement).disabled,
    ).toBe(true);

    fireEvent.click(
      screen.getByRole('button', { name: /Fuso orario: Ora locale/ }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Europe/Rome' }));
    expect(
      screen.getByRole('button', { name: /Fuso orario: Europe\/Rome/ }),
    ).toBeTruthy();
    expect(
      domElement(screen.getByLabelText('Ricorda'), HTMLSelectElement).disabled,
    ).toBe(false);
  });

  it('keeps the rail open on outside clicks while pinned, including the global Home bridge', () => {
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
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeTruthy();

    const outside = document.createElement('div');
    document.body.append(outside);
    fireEvent.pointerDown(outside);
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeTruthy();
    outside.remove();

    const unpin = screen.getByRole('button', { name: 'Sblocca pannello Crea' });
    fireEvent.click(unpin);
    fireEvent.pointerDown(backdrop);
    expect(
      document.querySelector('[data-temporal-create="composer"]'),
    ).toBeNull();
  });

  it('promotes Advanced to a central viewport surface without losing the Quick draft', () => {
    renderEntry();

    const quickComposer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    expect(
      quickComposer?.closest('[data-home-context-create-host]'),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Annulla' })).toBeNull();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Bozza preservata' },
    });
    fireEvent.change(screen.getByLabelText('Life Area (opzionale)'), {
      target: { value: 'Nuova Area' },
    });

    const advanced = screen.getByRole('button', { name: /Opzioni avanzate/ });
    expect(advanced.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(advanced);

    const advancedComposer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    const advancedBackdrop = advancedComposer?.closest<HTMLElement>(
      '[data-temporal-create="backdrop"]',
    );
    expect(advancedComposer?.dataset.temporalCreateSurface).toBe('advanced');
    expect(advancedComposer?.parentElement).toBe(advancedBackdrop);
    expect(advancedBackdrop?.parentElement).toBe(document.body);
    expect(
      domElement(screen.getByPlaceholderText('Titolo'), HTMLInputElement).value,
    ).toBe('Bozza preservata');
    expect(
      domElement(
        screen.getByLabelText('Life Area (opzionale)'),
        HTMLInputElement,
      ).value,
    ).toBe('Nuova Area');

    // Advanced owns the full timezone field and continues to edit the same
    // timeMode/timeZoneId values as Quick.
    expect(screen.getByRole('button', { name: /Fuso orario:/ })).toBeTruthy();

    // Reminder remains one primary Create control, not a second Advanced copy.
    expect(screen.getAllByLabelText('Ricorda')).toHaveLength(1);
    expect(
      screen.getByRole('radiogroup', {
        name: 'Modalità svolgimento dell’attività',
      }),
    ).toBeTruthy();
    expect(screen.queryByText('Aspetto')).toBeNull();

    const backToQuick = screen.getByRole('button', {
      name: /Nascondi opzioni avanzate/,
    });
    expect(backToQuick.getAttribute('aria-expanded')).toBe('true');
    fireEvent.click(backToQuick);

    const returnedComposer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    expect(returnedComposer?.dataset.temporalCreateSurface).toBe('base');
    expect(
      returnedComposer?.closest('[data-home-context-create-host]'),
    ).toBeTruthy();
    expect(
      domElement(screen.getByPlaceholderText('Titolo'), HTMLInputElement).value,
    ).toBe('Bozza preservata');
    expect(
      domElement(
        screen.getByLabelText('Life Area (opzionale)'),
        HTMLInputElement,
      ).value,
    ).toBe('Nuova Area');
  });
});
