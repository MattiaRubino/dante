import { expect, test } from '@playwright/test';
import type { Locator } from '@playwright/test';

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

async function setClock(
  row: Locator,
  label: string,
  date: string,
  time: string,
) {
  const dateTrigger = row.getByRole('button', {
    name: new RegExp(`^${label} · Data:`),
  });
  if ((await dateTrigger.getAttribute('data-temporal-date')) !== date) {
    await dateTrigger.click();
    await row
      .getByRole('dialog', { name: `${label} · Data` })
      .locator(`button[data-temporal-date="${date}"]`)
      .click();
  }
  await row
    .getByRole('textbox', { name: `${label} · Ora: ore` })
    .fill(time.slice(0, 2));
  await row
    .getByRole('textbox', { name: `${label} · Ora: minuti` })
    .fill(time.slice(3));
}

test('Inspector records and corrects a concluded named Session without offering Registra again', async ({
  browser,
}, info) => {
  test.setTimeout(120_000);
  const user = await signedInPage(browser, info, 8);
  const { page } = user;
  try {
    const date = scenarioDate(-1);
    await openHome(page, date);
    const title = uniqueTitle('Registrazione Sessione');
    const composer = await openCreate(page, 'activity');
    await configureCreate(composer, {
      kind: 'activity',
      title,
      date,
      clock: '09:00',
      plannedSession: 'Lettura',
    });
    const item = await submitCreate(page, composer, {
      kind: 'activity',
      title,
      recurring: false,
    });
    await openHome(page, date);
    const inspector = await openInspector(page, item);
    await inspector
      .getByRole('button', { name: 'Registrazioni delle Sessioni' })
      .click();
    const editor = page.getByRole('dialog', {
      name: 'Registrazioni delle Sessioni',
    });
    await expect(editor).toBeVisible();
    const row = editor.locator('article').filter({ hasText: 'Lettura' });
    await row.getByRole('button', { name: 'Registra' }).click();
    await setClock(row, 'Lettura · Inizio', date, '09:05');
    await setClock(row, 'Lettura · Fine', date, '09:25');
    const firstWrite = page.waitForResponse(
      (response) =>
        response
          .url()
          .endsWith(
            `/api/v1/temporal/activities/${item.sourceRef}/sessions/editor`,
          ) && response.request().method() === 'POST',
      { timeout: 15_000 },
    );
    await row.getByRole('button', { name: 'Salva registrazione' }).click();
    const firstResponse = await firstWrite;
    expect(firstResponse.status()).toBe(201);
    await expect(row.getByRole('button', { name: 'Correggi' })).toBeVisible();
    await expect(row.getByRole('button', { name: 'Registra' })).toHaveCount(0);

    const read = () =>
      serverRead(
        page,
        `/api/v1/temporal/activities/${item.sourceRef}/sessions/editor`,
      ) as Promise<
        Array<{
          session_ref: string;
          ended_at: string;
          pause_ranges: unknown[];
        }>
      >;
    const [recorded] = await read();
    expect(recorded?.ended_at).toBeTruthy();
    await row.getByRole('button', { name: 'Correggi' }).click();
    await row.getByRole('button', { name: '+ Pausa' }).click();
    await setClock(row, 'Pausa 1 · Da', date, '09:15');
    await setClock(row, 'Pausa 1 · A', date, '09:20');
    const correction = page.waitForResponse(
      (response) =>
        response
          .url()
          .endsWith(
            `/api/v1/temporal/activities/${item.sourceRef}/sessions/editor`,
          ) && response.request().method() === 'POST',
      { timeout: 15_000 },
    );
    await row.getByRole('button', { name: 'Salva registrazione' }).click();
    const correctionResponse = await correction;
    expect(correctionResponse.status()).toBe(200);
    const [corrected] = await read();
    expect(corrected?.session_ref).toBe(recorded?.session_ref);
    expect(corrected?.pause_ranges).toHaveLength(1);
  } finally {
    // A test timeout can close the browser before cleanup. Preserve the
    // original assertion/timeout instead of replacing it with a close error.
    await user.close().catch(() => {});
  }
});
