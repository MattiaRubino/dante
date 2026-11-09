/**
 * Two independent real-stack regressions for the non-trivial facts that an
 * ordinary CRUD suite cannot verify: confirmed Objective results, and active
 * Session/Edit protection. Neither test is xfailed or skipped for known bugs.
 */
import { Temporal } from '@dante/time';
import {
  expect, test, type Locator, type Page,
} from '@playwright/test';

import { openHome, scenarioDate, serverRead, uniqueTitle } from
  './temporal-user-journey-support';
import { ACTIVITY_CASES, EVENT_CASES } from
  './temporal-stateful-case-matrix';
import { authorPersona, signedInPersona } from
  './temporal-stateful-journey-support';

function cardOn(page: Page, date: string, title: string): Locator {
  return page.locator(
    '[data-timeline-event][data-planned-date="' + date + '"]',
  ).filter({ hasText: title });
}

test.describe('Temporal v2 — recorded facts survive Edit', () => {
  test.describe.configure({ timeout: 300_000 });

  test('V2-RT-01 Event: confirmed Objective remains a registered result in Edit', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 100);
    const { page } = user;
    const day = scenarioDate(5);
    const title = uniqueTitle('v2 obiettivo confermato');
    try {
      await openHome(page, day);
      const authored = await authorPersona(page, EVENT_CASES[0]!, title, day);
      const goal = authored.truth.objectives[0]!;
      expect(goal.kind).toBe('boolean');
      const before = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(before).toHaveLength(1);
      expect(before[0]!.observation_ref).toBeNull();
      await openHome(page, day);

      // The actual user confirmation is through the Work/Obiettivi panel.
      await page.getByRole('tab', { name: 'Obiettivi' }).click();
      const pending = page.locator('.home-resolution-card')
        .filter({ hasText: title });
      await expect(pending).toHaveCount(1);
      await pending.getByRole('button', { name: 'Compila obiettivi' }).click();
      const control = pending.locator('[data-objective-ref]')
        .filter({ hasText: goal.label });
      await expect(control).toBeVisible();
      await control.getByRole('combobox', {
        name: 'Valore per ' + goal.label,
      }).selectOption('true');
      const accepted = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().endsWith('/confirm-input'),
      );
      await control.getByRole('button', {
        name: 'Conferma obiettivo ' + goal.label,
      }).click();
      expect((await accepted).status()).toBe(200);

      const after = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(after).toHaveLength(1);
      expect(after[0]!.objective_ref).toBe(before[0]!.objective_ref);
      expect(after[0]!.observation_ref).toEqual(expect.any(String));
      expect(after[0]!.observed_boolean).toBe(true);

      await openHome(page, day);
      const card = cardOn(page, day, title);
      await card.getByRole('button', { name: title, exact: true }).click();
      const inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      const recorded = inspector.getByRole('group', {
        name: 'Obiettivo registrato ' + goal.label,
      });
      await expect(recorded).toBeVisible();
      await expect(recorded.getByText('Risultato: Sì')).toBeVisible();
      await expect(recorded.getByRole('button', {
        name: 'Correggi risultato',
      })).toBeVisible();
      // The confirmed Objective is not a disabled editable form.
      // It is an independent read-only row with an explicit deletion path.
      await expect(recorded.getByRole('textbox', {
        name: 'Nome obiettivo',
      })).toHaveCount(0);
      // Independent unsaved draft: reproduces the real visual-test report.
      // Deleting a different accepted result must neither demand Save nor
      // erase the incomplete Objective, even after canonical readback.
      await inspector.getByRole('button', {
        name: /Aggiungi obiettivo/,
      }).click();
      await expect(inspector.getByRole('textbox', {
        name: 'Nome obiettivo',
      })).toHaveValue('');
      await recorded.getByRole('button', {
        name: 'Elimina registrazione',
      }).click();
      const confirmation = page.getByRole('alertdialog', {
        name: 'Eliminare la registrazione?',
      });
      await expect(confirmation).toBeVisible();
      await confirmation.getByRole('button', { name: 'Annulla' }).click();
      await expect(confirmation).toHaveCount(0);
      const stillRecorded = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(stillRecorded[0]!.observation_ref).toBe(after[0]!.observation_ref);
      await recorded.getByRole('button', {
        name: 'Elimina registrazione',
      }).click();
      const deleted = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().endsWith(
          '/api/v1/temporal/objectives/' + after[0]!.objective_ref +
            '/delete-recording',
        ),
      );
      await confirmation.getByRole('button', { name: 'Sì, elimina' }).click();
      expect((await deleted).status()).toBe(200);
      await expect(confirmation).toHaveCount(0);
      const restored = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(restored).toHaveLength(1);
      expect(restored[0]!.objective_ref).toBe(before[0]!.objective_ref);
      expect(restored[0]!.observation_ref).toBeNull();
      expect(restored[0]!.evaluation_state_ref).toBeNull();
      await expect(recorded).toHaveCount(0);
      await expect(
        inspector.getByRole('textbox', { name: 'Nome obiettivo' }),
      ).toHaveCount(2);
      await expect(
        inspector.getByRole('textbox', { name: 'Nome obiettivo' }).nth(0),
      ).toHaveValue(goal.label);
      await expect(
        inspector.getByRole('textbox', { name: 'Nome obiettivo' }).nth(1),
      ).toHaveValue('');
      // The incomplete draft exists only in the editor and has not
      // accidentally been persisted by the independent result deletion.
      const noUnexpectedObjective = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(noUnexpectedObjective).toHaveLength(1);
      await openHome(page, day);
      const persisted = await serverRead(
        page,
        '/api/v1/temporal/events/' + authored.item.sourceRef + '/objectives',
      ) as Record<string, unknown>[];
      expect(persisted[0]!.observation_ref).toBeNull();
    } finally {
      await user.close();
    }
  });

  test('V2-RT-02 Activity: live Session blocks replan and persists pause/end', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 101);
    const { page } = user;
    // Run during a genuinely current, in-progress Activity. A future
    // planned Activity cannot be started by Play merely to satisfy a test.
    const start = Temporal.Now.zonedDateTimeISO('Europe/Rome').subtract({
      minutes: 15,
    });
    const day = start.toPlainDate().toString();
    const clock = start.toPlainTime().toString({ smallestUnit: 'minute' });
    const title = uniqueTitle('v2 sessione in esecuzione');
    try {
      await openHome(page, day);
      const authored = await authorPersona(
        page, ACTIVITY_CASES[0]!, title, day, undefined, true, clock,
      );
      await openHome(page, day);
      const card = cardOn(page, day, title);
      await expect(card).toHaveCount(1);
      const controls = card.locator(
        '[data-timeline-session-subject="' + authored.item.sourceRef + '"]',
      );
      await expect(controls.getByRole('button', { name: 'Avvia' }))
        .toBeEnabled();
      await controls.getByRole('button', { name: 'Avvia' }).click();
      await expect(controls.getByRole('button', { name: 'Termina' }))
        .toBeEnabled();

      const list = async (): Promise<Record<string, unknown>[]> =>
        (await serverRead(
          page,
          '/api/v1/temporal/activities/' + authored.item.sourceRef + '/sessions',
        )) as Record<string, unknown>[];
      const started = await list();
      const open = started.filter((session) => session.open === true);
      expect(open).toHaveLength(1);
      const sessionRef = open[0]!.session_ref;
      expect(sessionRef).toEqual(expect.any(String));
      expect(open[0]!.ended_at).toBeNull();

      await card.getByRole('button', { name: title, exact: true }).click();
      const inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      await expect(inspector.getByText(
        /Orari e intervalli restano bloccati finché esistono registrazioni/,
      )).toBeVisible();
      await expect(
        inspector.getByRole('button', { name: 'Aggiungi intervallo' }),
      ).toBeDisabled();
      await inspector.getByRole('button', { name: 'Annulla' }).click();
      await inspector.getByRole('button', { name: 'Chiudi Inspector' }).click();

      await controls.getByRole('button', { name: 'Pausa' }).click();
      await expect.poll(async () => {
        const rows = await list();
        return rows.find((session) => session.session_ref === sessionRef)?.paused;
      }).toBe(true);
      await controls.getByRole('button', { name: 'Riprendi' }).click();
      await expect.poll(async () => {
        const rows = await list();
        return rows.find((session) => session.session_ref === sessionRef)?.paused;
      }).toBe(false);
      await controls.getByRole('button', { name: 'Termina' }).click();
      const finished = await list();
      const recorded = finished.find((session) =>
        session.session_ref === sessionRef,
      );
      expect(recorded?.open).toBe(false);
      expect(recorded?.ended_at).toEqual(expect.any(String));
      expect(recorded?.session_ref).toBe(sessionRef);

      await openHome(page, day);
      const persisted = await list();
      expect(persisted.filter((session) =>
        session.session_ref === sessionRef,
      )).toHaveLength(1);
    } finally {
      await user.close();
    }
  });
});
