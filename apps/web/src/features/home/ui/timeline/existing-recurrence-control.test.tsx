// @vitest-environment jsdom
import { createRef } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  ExistingRecurrenceControl,
  type ExistingRecurrenceControlHandle,
} from './existing-recurrence-control';

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('Existing recurring Activity/Event Save staging', () => {
  it.each(['activity', 'event'] as const)(
    'stages a %s recurrence with no independent mutation button',
    (kind) => {
      const selection = vi.fn();
      const ref = createRef<ExistingRecurrenceControlHandle>();
      render(
        <ExistingRecurrenceControl
          ref={ref}
          kind={kind}
          date="2026-10-09"
          startTime="09:00"
          allDay={false}
          zoneId="Europe/Rome"
          disambiguation="earlier"
          onSelectionChange={selection}
        />,
      );

      const repeat = screen.getByRole('combobox', { name: 'Ripeti' });
      expect(ref.current?.getRule()).toBeNull();
      fireEvent.change(repeat, { target: { value: 'daily' } });
      expect(selection).toHaveBeenLastCalledWith(true);
      expect(
        screen.queryByRole('button', { name: /Avvia ripetizione/ }),
      ).toBeNull();
      expect(ref.current?.getRule()).toMatchObject({
        family_code: 'calendar_wall_clock',
        effective_from: '2026-10-09',
        zone_id: 'Europe/Rome',
        wall_times: ['09:00'],
      });

      fireEvent.change(repeat, { target: { value: 'none' } });
      expect(selection).toHaveBeenLastCalledWith(false);
      expect(ref.current?.getRule()).toBeNull();
    },
  );
});
