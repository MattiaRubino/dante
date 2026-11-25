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
    await expect(editor).toBeHidden();
    await expect(inspector).toBeHidden();
    await openHome(page, date);
    const reopened = await openInspector(page, item);
    await reopened.getByRole('button', { name: 'Registrazioni delle Sessioni' }).click();
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
    await expect(editor).toBeHidden();
    await expect(reopened).toBeHidden();
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
    await expect(editor).toBeHidden();
    await expect(inspector).toBeHidden();
    await openHome(page, date);
    const reopened = await openInspector(page, item);
    await reopened.getByRole('button', { name: 'Registrazioni delle Sessioni' }).click();
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


test('Inspector distributes one child Session across two main intervals, pauses it, corrects it, and closes to Home', async ({
  browser,
}, info) => {
  test.setTimeout(120_000);
  const user = await signedInPage(browser, info, 6);
  const { page } = user;
  try {
    const date = scenarioDate(-1);
    await openHome(page, date);
    const title = uniqueTitle('Sessione secondaria ripresa');
    const composer = await openCreate(page, 'activity');
    await configureCreate(composer, {
      kind: 'activity',
      title,
      date,
      clock: '09:00',
      plannedSession: 'Lettura',
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

    await intervals.nth(0).getByRole('button', { name: /Registra sessione/ }).click();
    await intervals.nth(0).getByRole('button', { name: 'Lettura' }).click();
    const first = intervals.nth(0).locator('article.is-child');
    await setClock(first, 1, 'Inizio', date, '09:06');
    await setClock(first, 1, 'Fine', date, '09:14');

    await intervals.nth(1).getByRole('button', { name: /Registra sessione/ }).click();
    await intervals.nth(1).getByRole('button', { name: 'Lettura · Riprendi' }).click();
    const second = intervals.nth(1).locator('article.is-child');
    await expect(first).toBeVisible();
    await expect(second).toBeVisible();
    await setClock(second, 2, 'Inizio', date, '09:21');
    await setClock(second, 2, 'Fine', date, '09:29');

    // Only the middle section scrolls: title/header and Save stay fixed.
    const scrolling = editor.getByRole('region', { name: 'Intervalli e Sessioni' });
    await expect(scrolling).toHaveCSS('overflow-y', 'auto');
    expect(await scrolling.evaluate((element) => element.scrollHeight > element.clientHeight)).toBe(true);
    await scrolling.evaluate((element) => { element.scrollTop = element.scrollHeight; });
    await expect(editor.locator('.timeline-session-editor__footer')).toBeVisible();
    await expect(editor.getByRole('button', { name: 'Salva registrazioni' })).toBeVisible();

    const target = '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor/batch';
    const write = page.waitForResponse(
      (response) => response.url().endsWith(target) && response.request().method() === 'POST',
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
    const receipt = await write;
    expect(receipt.status()).toBe(201);
    const submitted = receipt.request().postDataJSON() as {
      commands: Array<{
        planned_schedule_ref: string | null;
        pause_ranges: Array<{ started_at: string; ended_at: string }>;
      }>;
    };
    expect(submitted.commands).toHaveLength(2);
    expect(submitted.commands[0]?.planned_schedule_ref).toBeNull();
    expect(submitted.commands[1]?.planned_schedule_ref).not.toBeNull();
    expect(submitted.commands[1]?.pause_ranges).toHaveLength(1);
    await expect(editor).toBeHidden();
    await expect(inspector).toBeHidden();

    const read = () => serverRead(
      page, '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor',
    ) as Promise<Array<{
      session_ref: string;
      planned_schedule_ref: string | null;
      timing_material_state_ref: string;
      pause_ranges: unknown[];
    }>>;
    const stored = await read();
    expect(stored).toHaveLength(2);
    const child = stored.find((record) => record.planned_schedule_ref !== null);
    expect(child?.pause_ranges).toHaveLength(1);

    await openHome(page, date);
    const inspectedAgain = await openInspector(page, item);
    await inspectedAgain.getByRole('button', { name: 'Registrazioni delle Sessioni' }).click();
    await expect(intervals).toHaveCount(2);
    await expect(intervals.nth(0).locator('article.is-child')).toHaveCount(1);
    await expect(intervals.nth(1).locator('article.is-child')).toHaveCount(1);
    await intervals.nth(0).locator('article.is-child')
      .getByRole('button', { name: 'Correggi' }).click();
    const correctionRow = intervals.nth(0).locator('article.is-child');
    await setClock(correctionRow, 1, 'Inizio', date, '09:07');
    const correction = page.waitForResponse(
      (response) => response.url().endsWith(target) && response.request().method() === 'POST',
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
    expect((await correction).status()).toBe(200);
    await expect(editor).toBeHidden();
    await expect(inspectedAgain).toBeHidden();
    const after = await read();
    expect(after).toHaveLength(2);
    const corrected = after.find((record) => record.planned_schedule_ref !== null);
    expect(corrected?.session_ref).toBe(child?.session_ref);
    expect(corrected?.timing_material_state_ref).not.toBe(child?.timing_material_state_ref);
    expect(corrected?.pause_ranges).toHaveLength(1);
  } finally {
    await user.close().catch(() => {});
  }
});

test('Inspector preserves editable child clock and parent placement across invalid drafts and a date popup', async ({
  browser,
}, info) => {
  test.setTimeout(120_000);
  const user = await signedInPage(browser, info, 5);
  const { page } = user;
  try {
    const date = scenarioDate(-1);
    await openHome(page, date);
    const title = uniqueTitle('Registrazioni editabili');
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
    await setClock(main, 1, 'Inizio', date, '09:00');
    await setClock(main, 1, 'Fine', date, '08:50');
    const parent = editor.locator('.timeline-session-editor__parent-interval').first();
    // Preparing a child must remain possible while the main's end time is
    // temporarily earlier than its start.
    await expect(parent.getByRole('button', { name: /Registra sessione/ })).toBeEnabled();
    await parent.getByRole('button', { name: /Registra sessione/ }).click();
    await parent.getByRole('button', { name: 'Lettura' }).click();
    const child = parent.locator('article.is-child');
    await expect(child).toBeVisible();
    const mainFieldsBefore = parent.locator(':scope > .timeline-session-editor__interval-block');
    await setClock(mainFieldsBefore, 1, 'Fine', date, '09:30');

    // Typed values outside the main are not immediately clamped or unmounted.
    await setClock(child, 1, 'Inizio', date, '08:10');
    await expect(child.getByRole('textbox', { name: 'Intervallo 1 · Inizio: ore' })).toHaveValue('08');
    await expect(child.getByText(/supera il tratto attivo della principale/)).toBeVisible();
    await expect(child).toHaveCount(1);
    await child.getByRole('button', { name: 'Adatta ai limiti' }).click();
    await expect(child.getByRole('textbox', { name: 'Intervallo 1 · Inizio: ore' })).toHaveValue('09');
    await expect(child.getByText(/supera il tratto attivo/)).toHaveCount(0);
    await setClock(child, 1, 'Fine', date, '09:20');

    // Inverting a main interval is allowed temporarily while editing.
    const mainFields = parent.locator(':scope > .timeline-session-editor__interval-block');
    await setClock(mainFields, 1, 'Fine', date, '08:50');
    await expect(child).toHaveCount(1);
    await expect(child.getByRole('textbox', { name: 'Intervallo 1 · Fine: minuti' })).toHaveValue('20');
    await setClock(mainFields, 1, 'Fine', date, '09:30');
    await expect(child).toHaveCount(1);

    // The last inline calendar must be usable inside the scrolling body.
    const scrolling = editor.getByRole('region', { name: 'Intervalli e Sessioni' });
    await scrolling.evaluate((element) => { element.scrollTop = element.scrollHeight; });
    await child.getByRole('button', { name: /^Intervallo 1 · Data fine:/ }).click();
    const picker = child.getByRole('dialog', { name: 'Intervallo 1 · Data fine' });
    await expect(picker).toBeVisible();
    const [pickerBox, scrollBox] = await Promise.all([picker.boundingBox(), scrolling.boundingBox()]);
    expect(pickerBox).not.toBeNull();
    expect(scrollBox).not.toBeNull();
    expect(pickerBox!.y + pickerBox!.height).toBeLessThanOrEqual(
      scrollBox!.y + scrollBox!.height + 3,
    );
    await picker.locator('button[data-temporal-date="' + date + '"]').click();
    await expect(picker).toBeHidden();

    const target = '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor/batch';
    const writing = page.waitForResponse(
      (response) => response.url().endsWith(target) && response.request().method() === 'POST',
    );
    await editor.getByRole('button', { name: 'Salva registrazioni' }).click();
    expect((await writing).status()).toBe(201);
    await expect(editor).toBeHidden();
    await expect(inspector).toBeHidden();
    const records = (await serverRead(
      page, '/api/v1/temporal/activities/' + item.sourceRef + '/sessions/editor',
    )) as Array<{
      session_ref: string;
      planned_schedule_ref: string | null;
      pause_ranges: unknown[];
    }>;
    expect(records).toHaveLength(2);
    expect(records.filter((record) => record.planned_schedule_ref !== null)).toHaveLength(1);
  } finally {
    await user.close().catch(() => {});
  }
});
