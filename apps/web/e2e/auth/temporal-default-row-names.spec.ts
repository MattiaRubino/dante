import { expect, test } from '@playwright/test';

import {
  configureCreate,
  openCreate,
  openHome,
  openInspector,
  scenarioDate,
  serverRead,
  signedInPage,
  submitCreate,
  uniqueTitle,
} from './temporal-user-journey-support';

test.describe('Timeline — unnamed rows persist through real Create and Edit', () => {
  test.describe.configure({ mode: 'parallel' });

  test('Event Scaletta keeps blank, named and blank rows across Create, Edit and reload', async ({ browser }, info) => {
    test.setTimeout(120_000);
    const user = await signedInPage(browser, info, 6);
    const { page } = user;
    try {
      const date = scenarioDate();
      await openHome(page, date);
      const title = uniqueTitle('Scaletta senza nome');
      const composer = await openCreate(page, 'event');
      await configureCreate(composer, {
        kind: 'event',
        title,
        date,
        clock: '14:10',
        agenda: 'Introduzione',
      });
      await composer.getByRole('textbox', { name: 'Punto scaletta 1' }).fill('');
      await composer.getByRole('button', { name: 'Aggiungi punto alla scaletta' }).click();
      await composer.getByRole('textbox', { name: 'Punto scaletta 2' }).fill('Domande');
      await composer.getByRole('button', { name: 'Aggiungi punto alla scaletta' }).click();
      const item = await submitCreate(page, composer, { kind: 'event', title, recurring: false });
      const read = () =>
        serverRead(page, `/api/v1/temporal/events/${item.sourceRef}`) as Promise<{
          agenda_parts: string[];
        }>;
      expect((await read()).agenda_parts).toEqual(['Scaletta 1', 'Domande', 'Scaletta 3']);

      await openHome(page, date);
      const inspector = await openInspector(page, item);
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      await inspector.getByRole('textbox', { name: 'Punto scaletta 2' }).fill('');
      await inspector.getByRole('button', { name: 'Aggiungi punto alla scaletta' }).click();
      const saved = page.waitForResponse(
        (response) =>
          response.url().endsWith(`/api/v1/temporal/events/${item.sourceRef}/atomic-edit`) &&
          response.request().method() === 'PUT',
      );
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
      expect((await saved).status()).toBe(200);
      expect((await read()).agenda_parts).toEqual([
        'Scaletta 1',
        'Scaletta 2',
        'Scaletta 3',
        'Scaletta 4',
      ]);
      await page.reload();
      expect((await read()).agenda_parts).toEqual([
        'Scaletta 1',
        'Scaletta 2',
        'Scaletta 3',
        'Scaletta 4',
      ]);
    } finally {
      await user.close();
    }
  });

  test('Activity unnamed planned Sessions keep their canonical names after Edit', async ({ browser }, info) => {
    test.setTimeout(120_000);
    const user = await signedInPage(browser, info, 7);
    const { page } = user;
    try {
      const date = scenarioDate(5);
      await openHome(page, date);
      const title = uniqueTitle('Sessioni senza nome');
      const composer = await openCreate(page, 'activity');
      await configureCreate(composer, {
        kind: 'activity',
        title,
        date,
        clock: '15:10',
        plannedSession: 'Lettura',
      });
      await composer.getByRole('textbox', { name: 'Nome Sessione' }).fill('');
      const addSession = composer.getByLabel('Aggiungi Sessione pianificata');
      await addSession.getByRole('button', { name: 'Sessione' }).click();
      await composer.getByRole('textbox', { name: 'Nome Sessione' }).nth(1).fill('Riepilogo');
      const item = await submitCreate(page, composer, { kind: 'activity', title, recurring: false });
      const readNames = async () => {
        const snapshot = (await serverRead(
          page,
          `/api/v1/temporal/activities/${item.sourceRef}/edit-snapshot`,
        )) as {
          schedules: Array<{ role_code: string; display_name: string | null }>;
        };
        return snapshot.schedules
          .filter((row) => row.role_code === 'planned')
          .map((row) => row.display_name);
      };
      expect(await readNames()).toEqual(['Sessione 1', 'Riepilogo']);

      await openHome(page, date);
      const inspector = await openInspector(page, item);
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      await inspector.locator('.timeline-activity-editor__sessions')
        .getByRole('button', { name: 'Sessione', exact: true }).click();
      const saved = page.waitForResponse(
        (response) =>
          response.url().endsWith(`/api/v1/temporal/activities/${item.sourceRef}/atomic-edit`) &&
          response.request().method() === 'PUT',
      );
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
      expect((await saved).status()).toBe(200);
      expect(await readNames()).toEqual(['Sessione 1', 'Riepilogo', 'Sessione 3']);
      await page.reload();
      expect(await readNames()).toEqual(['Sessione 1', 'Riepilogo', 'Sessione 3']);
    } finally {
      await user.close();
    }
  });
});
