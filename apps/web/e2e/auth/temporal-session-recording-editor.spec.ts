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
  interval: number,
  edge: 'Inizio' | 'Fine',
  date: string,
  time: string,
) {
  const label = `Intervallo ${interval}`;
  const dateLabel = `${label} · Data ${edge === 'Inizio' ? 'inizio' : 'fine'}`;
  const dateTrigger = row.getByRole('button', {
    name: new RegExp(`^${dateLabel}:`),
  });
  if ((await dateTrigger.getAttribute('data-temporal-date')) !== date) {
    await dateTrigger.click();
    await row
      .getByRole('dialog', { name: dateLabel })
      .locator(`button[data-temporal-date="${date}"]`)
      .click();
  }
  await row
    .getByRole('textbox', { name: `${label} · ${edge}: ore` })
    .fill(time.slice(0, 2));
  await row
    .getByRole('textbox', { name: `${label} · ${edge}: minuti` })
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
    await setClock(row, 1, 'Inizio', date, '09:05');
    await setClock(row, 1, 'Fine', date, '09:25');
    const firstWrite = page.waitForResponse(
      (response) =>
        response
          .url()
          .endsWith(
            `/api/v1/temporal/activities/${item.sourceRef}/sessions/editor/batch`,
          ) && response.request().method() === 'POST',
      { timeout: 15_000 },
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
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
    await row.getByRole('button', { name: /Aggiungi intervallo/ }).click();
    await setClock(row, 1, 'Fine', date, '09:15');
    await setClock(row, 2, 'Inizio', date, '09:20');
    await setClock(row, 2, 'Fine', date, '09:25');
    const correction = page.waitForResponse(
      (response) =>
        response
          .url()
          .endsWith(
            `/api/v1/temporal/activities/${item.sourceRef}/sessions/editor/batch`,
          ) && response.request().method() === 'POST',
      { timeout: 15_000 },
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
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

test('Inspector configures main and named child together with one atomic save and canonical readback', async ({
  browser,
}, info) => {
  test.setTimeout(120_000);
  const user = await signedInPage(browser, info, 7);
  const { page } = user;
  try {
    const date = scenarioDate(-1);
    await openHome(page, date);
    const title = uniqueTitle('Intervalli Sessione attività');
    const composer = await openCreate(page, 'activity');
    await configureCreate(composer, {
      kind: 'activity', title, date, clock: '09:00', plannedSession: 'Lettura',
    });
    await composer.getByRole('checkbox', { name: 'Sessione', exact: true }).check();
    const item = await submitCreate(page, composer, {
      kind: 'activity', title, recurring: false,
    });
    await openHome(page, date);
    const inspector = await openInspector(page, item);
    await inspector.getByRole('button', { name: 'Registrazioni delle Sessioni' }).click();
    const editor = page.getByRole('dialog', { name: 'Registrazioni delle Sessioni' });
    const main = editor.locator('section.timeline-session-editor__group.has-main');
    await setClock(main, 1, 'Inizio', date, '09:05');
    await setClock(main, 1, 'Fine', date, '09:15');
    await main.getByRole('button', { name: /Aggiungi intervallo/ }).click();
    await setClock(main, 2, 'Inizio', date, '09:20');
    await setClock(main, 2, 'Fine', date, '09:30');
    const intervals = editor.locator('.timeline-session-editor__parent-interval');
    await expect(intervals).toHaveCount(2);
    await intervals.nth(1).getByRole('button', { name: /Registra sessione/ }).click();
    await intervals.nth(1).getByRole('button', { name: 'Lettura' }).click();
    const child = intervals.nth(1).locator('article.is-child');
    await expect(child).toBeVisible();
    await setClock(child, 1, 'Inizio', date, '09:22');
    await setClock(child, 1, 'Fine', date, '09:27');

    const target = '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor/batch';
    const groupWrite = page.waitForResponse(
      (response) => response.url().endsWith(target) && response.request().method() === 'POST',
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
    const groupReceipt = await groupWrite;
    expect(groupReceipt.status()).toBe(201);
    const submitted = groupReceipt.request().postDataJSON() as {
      commands: Array<{ planned_schedule_ref: string | null }>;
    };
    expect(submitted.commands).toHaveLength(2);
    expect(submitted.commands[0]?.planned_schedule_ref).toBeNull();
    expect(submitted.commands[1]?.planned_schedule_ref).not.toBeNull();
    await expect(editor.locator('article.is-child').getByRole('button', { name: 'Correggi' })).toBeVisible();
    const recordings = (await serverRead(
      page, '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor',
    )) as Array<{
      session_ref: string;
      planned_schedule_ref: string | null;
      pause_ranges: unknown[];
      ended_at: string | null;
    }>;
    expect(recordings).toHaveLength(2);
    expect(recordings.find((row) => row.planned_schedule_ref === null)?.pause_ranges).toHaveLength(1);
    expect(recordings.filter((row) => row.planned_schedule_ref !== null)).toHaveLength(1);
    expect(recordings.every((row) => Boolean(row.ended_at))).toBe(true);
  } finally {
    await user.close().catch(() => {});
  }
});
