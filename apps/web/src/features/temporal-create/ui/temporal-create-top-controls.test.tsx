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

  it.each([
    ['Quick', 'Attività'],
    ['Quick', 'Evento'],
    ['Advanced', 'Attività'],
    ['Advanced', 'Evento'],
  ] as const)(
    'uses one timezone dialog, never a clock sidecar: %s %s',
    (surface, kind) => {
      renderEntry();
      if (kind === 'Evento') {
        fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
      }
      if (surface === 'Advanced') {
        fireEvent.click(screen.getByRole('button', { name: /Opzioni avanzate/ }));
      }
      fireEvent.click(screen.getByRole('button', { name: 'Inizio: scegli orario' }));
      const clock = screen.getByRole('dialog', { name: 'Inizio' });
      expect(within(clock).queryByRole('button', { name: /Fuso orario/ })).toBeNull();
      fireEvent.click(screen.getByRole('button', { name: 'Inizio: scegli orario' }));
      expect(screen.getAllByRole('button', { name: /^Fuso orario:/ })).toHaveLength(1);

      fireEvent.click(screen.getByRole('button', { name: /^Fuso orario:/ }));
      const panel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
      expect(panel.hasAttribute('data-temporal-create-portal')).toBe(true);
      expect(within(panel).getByRole('checkbox', {
        name: 'Utilizza fusi orari diversi per inizio e fine',
      })).toHaveProperty('checked', false);
      fireEvent.click(within(panel).getByRole('button', { name: /GMT/ }));
      fireEvent.change(within(panel).getByRole('searchbox', { name: 'Cerca fuso orario' }), {
        target: { value: 'Europe/Rome' },
      });
      fireEvent.click(within(panel).getByRole('option', { name: /Europe\/Rome/ }));
      fireEvent.click(within(panel).getByRole('button', { name: 'OK' }));
      expect(screen.queryByRole('dialog', { name: 'Imposta fuso orario' })).toBeNull();

      fireEvent.click(screen.getByRole('button', { name: /^Fuso orario:/ }));
      const customPanel = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
      fireEvent.click(within(customPanel).getByRole('checkbox', {
        name: 'Utilizza fusi orari diversi per inizio e fine',
      }));
      const endPicker = within(customPanel).getByText('Fuso orario di fine')
        .closest('.temporal-zone-dialog__picker');
      if (!endPicker) throw new Error('Expected the shared end timezone field.');
      fireEvent.click(within(endPicker as HTMLElement).getByRole('button'));
      fireEvent.change(within(endPicker as HTMLElement).getByRole('searchbox', {
        name: 'Cerca fuso orario',
      }), { target: { value: 'Asia/Tokyo' } });
      fireEvent.click(within(endPicker as HTMLElement).getByRole('option', {
        name: /Asia\/Tokyo/,
      }));
      fireEvent.click(within(customPanel).getByRole('button', { name: 'OK' }));

      expect(screen.getByRole('button', {
        name: 'Fuso orario: Personalizzato',
      })).toBeTruthy();
      fireEvent.click(screen.getByRole('button', {
        name: 'Fuso orario: Personalizzato',
      }));
      const reopened = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
      expect(within(reopened).getByRole('checkbox', {
        name: 'Utilizza fusi orari diversi per inizio e fine',
      })).toHaveProperty('checked', true);
      expect(within(reopened).getByText(/GMT\+09:00.*Asia\/Tokyo/)).toBeTruthy();
      fireEvent.click(within(reopened).getByRole('button', { name: 'Annulla' }));
      expect(screen.getByRole('button', {
        name: 'Fuso orario: Personalizzato',
      })).toBeTruthy();
    },
  );

  it('keeps the selected same-day end date after an explicit valid end edit', () => {
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
    'golden clock contract: %s %s start changes preserve duration and end changes resize',
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
        '13:00',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('3 h'),
      ).toBeTruthy();

      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: diminuisci 1 minuto' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '09:59',
        '12:59',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '3 h',
        ),
      ).toBeTruthy();

      fireEvent.click(
        screen.getByRole('button', { name: 'Fine: diminuisci ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '09:59',
        '11:59',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '2 h',
        ),
      ).toBeTruthy();

      setClock('Inizio', '08:30');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '08:30',
        '10:30',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '2 h',
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

      fireEvent.click(
        screen.getByRole('button', { name: 'Fine: scegli orario' }),
      );
      const picker = screen.getByRole('dialog', { name: 'Fine' });
      const custom = within(picker).getByRole('button', { name: '10:31' });
      expect(custom.classList.contains('is-selected')).toBe(true);
      expect(
        within(picker)
          .getByRole('button', { name: '10:30' })
          .classList.contains('is-selected'),
      ).toBe(false);
      fireEvent.click(custom);
      expect(clockValues().end.value).toBe('10:31');

      fireEvent.click(
        screen.getByRole('button', { name: 'Fine: aumenta 1 minuto' }),
      );
      expect(clockValues().end.value).toBe('10:32');
      fireEvent.click(
        screen.getByRole('button', { name: 'Fine: diminuisci 1 minuto' }),
      );
      expect(clockValues().end.value).toBe('10:31');

      // Moving start keeps the precise 1-minute span instead of freezing end.
      setClock('Inizio', '10:29');
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '10:29',
        '10:30',
      ]);
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText('1 min'),
      ).toBeTruthy();
    },
  );

  it.each(['Quick', 'Advanced'] as const)(
    'golden overnight contract: %s start moves across midnight preserving duration',
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
        '00:00',
      ]);
      fireEvent.click(
        screen.getByRole('button', { name: 'Inizio: aumenta ora' }),
      );
      expect([clockValues().start.value, clockValues().end.value]).toEqual([
        '23:30',
        '01:00',
      ]);
      expect(
        screen.getByRole('button', { name: /Data fine:.*1 ott/i }),
      ).toBeTruthy();
      expect(
        within(screen.getByRole('group', { name: 'Fine' })).getByText(
          '1 h 30 min',
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

  it('moves the end with the start while rejecting invalid manual time', () => {
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
    expect(endRaw.value).toBe(addMinutes(endBefore, 1));

    fireEvent.change(hour, { target: { value: '23' } });
    fireEvent.blur(hour);
    expect(startRaw.value).toMatch(/^23:/);
    expect(endRaw.value).not.toBe(endBefore);

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

    const zoneTrigger = screen.getByRole('button', { name: /Fuso orario:/ });
    fireEvent.click(zoneTrigger);
    const localDialog = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    fireEvent.click(within(localDialog).getByRole('button', { name: /GMT/ }));
    fireEvent.click(within(localDialog).getByRole('option', { name: /Ora locale/ }));
    fireEvent.click(within(localDialog).getByRole('button', { name: 'OK' }));
    expect(
      domElement(screen.getByLabelText('Ricorda'), HTMLSelectElement).disabled,
    ).toBe(true);

    fireEvent.click(screen.getByRole('button', { name: /Fuso orario:/ }));
    const zoneDialog = screen.getByRole('dialog', { name: 'Imposta fuso orario' });
    fireEvent.click(within(zoneDialog).getByRole('button', { name: /GMT/ }));
    fireEvent.change(
      within(zoneDialog).getByRole('searchbox', { name: 'Cerca fuso orario' }),
      { target: { value: 'Europe/Rome' } },
    );
    expect(
      within(zoneDialog).queryByRole('option', { name: /Africa\/Abidjan/ }),
    ).toBeNull();
    fireEvent.click(
      within(zoneDialog).getByRole('option', { name: /Europe\/Rome/ }),
    );
    fireEvent.click(within(zoneDialog).getByRole('button', { name: 'OK' }));
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

  it('preserves the Quick draft on Advanced, then resets everything but title on Activity/Event switch', () => {
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
    fireEvent.change(screen.getByLabelText('Area (opzionale)'), {
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
      domElement(screen.getByLabelText('Area (opzionale)'), HTMLInputElement)
        .value,
    ).toBe('Nuova Area');

    const timing = advancedComposer?.querySelector<HTMLElement>(
      '.temporal-create-timing-section.is-activity',
    );
    if (!timing) throw new Error('Expected the Activity timing section.');
    const zone = within(timing).getByRole('button', {
      name: /Fuso orario:/,
    });
    expect(zone.closest('.temporal-time-mode-toolbar')).toBeTruthy();
    expect(
      zone.querySelector('.temporal-create-timezone-label')?.textContent,
    ).toBeTruthy();
    expect(zone.textContent).not.toContain('Fuso orario');
    expect(within(timing).queryByText('Intervallo 1')).toBeNull();
    const primaryGrid = timing.querySelector('.temporal-create-u2-when');
    expect(primaryGrid?.classList.contains('temporal-schedule-time-grid')).toBe(true);
    expect(primaryGrid?.classList.contains('has-remove-track')).toBe(false);
    const areaSection = within(advancedComposer!).getByRole('region', {
      name: 'Area',
    });
    expect(areaSection.classList.contains('temporal-editor-area-section')).toBe(
      true,
    );
    expect(within(areaSection).getByText('Area')).toBeTruthy();
    expect(
      within(areaSection).getByRole('textbox', { name: 'Area (opzionale)' }),
    ).toBeTruthy();
    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
    const eventTiming = advancedComposer?.querySelector<HTMLElement>(
      '.temporal-create-timing-section:not(.is-activity)',
    );
    if (!eventTiming) throw new Error('Expected the Event timing section.');
    expect(
      within(eventTiming).getByRole('button', { name: /Fuso orario:/ }),
    ).toBeTruthy();
    expect(within(eventTiming).queryByText('Intervallo 1')).toBeNull();
    expect(eventTiming.querySelector('.temporal-create-u2-when')?.classList
      .contains('temporal-schedule-time-grid')).toBe(true);
    expect(eventTiming.querySelector('.temporal-create-u2-when')?.classList
      .contains('has-remove-track')).toBe(false);
    const eventAreaSection = within(advancedComposer!).getByRole('region', {
      name: 'Area',
    });
    expect(eventAreaSection).not.toBe(areaSection);
    expect(
      within(eventAreaSection).getByRole('textbox', {
        name: 'Area (opzionale)',
      }),
    ).toHaveProperty('value', '');
    expect(screen.getByPlaceholderText('Titolo')).toHaveProperty(
      'value',
      'Bozza preservata',
    );

    fireEvent.click(screen.getByRole('radio', { name: 'Attività' }));
    const resetActivityTiming = advancedComposer?.querySelector<HTMLElement>(
      '.temporal-create-timing-section.is-activity',
    );
    if (!resetActivityTiming) throw new Error('Expected fresh Activity timing.');
    fireEvent.click(
      within(resetActivityTiming).getByRole('button', {
        name: /Aggiungi intervallo/,
      }),
    );
    expect(within(resetActivityTiming).getByText('Intervallo 1')).toBeTruthy();
    expect(within(resetActivityTiming).getByText('Intervallo 2')).toBeTruthy();
    expect(resetActivityTiming.querySelector('.temporal-create-u2-when')?.classList
      .contains('has-remove-track')).toBe(true);
    expect(resetActivityTiming.querySelector('.temporal-create-activity-interval__fields')
      ?.classList.contains('has-remove-track')).toBe(true);

    // Reminder remains one primary Create control, not a second Advanced copy.
    expect(screen.getAllByLabelText('Ricorda')).toHaveLength(1);
    // Completion policy is no longer a global authoring control.
    expect(
      screen.queryByRole('radiogroup', {
        name: 'Modalità svolgimento dell’attività',
      }),
    ).toBeNull();
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
      domElement(screen.getByLabelText('Area (opzionale)'), HTMLInputElement)
        .value,
    ).toBe('');
  });
});
