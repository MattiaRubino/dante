import { randomUUID } from 'node:crypto';

import { Temporal } from '@dante/time';
import {
  expect,
  type Browser,
  type Locator,
  type Page,
  type TestInfo,
} from '@playwright/test';

/**
 * Real-stack user journeys deliberately do not mock auth, authoring,
 * scheduling, recurrence, materialization or deletion.
 * Each scenario uses a dedicated seeded account; mutations are never shared.
 */
const ACCOUNT_BASE: Readonly<Record<string, number>> = {
  chromium: 80,
  firefox: 87,
  webkit: 94,
};
const PASSWORD = 'correct horse battery staple';
const REQUEST_TIMEOUT = 25_000;

export type Subject = 'activity' | 'event';
export type Cadence = 'none' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';

export type CreatedItem = Readonly<{
  kind: Subject;
  title: string;
  sourceRef: string;
  scheduleRef: string | null;
  firstRef: string | null;
  payload: Record<string, unknown>;
}>;

export type CreateOptions = Readonly<{
  kind: Subject;
  title: string;
  date: string;
  clock?: string;
  allDay?: boolean;
  recurrence?: Cadence;
  interval?: number;
  monthlyOrdinal?: boolean;
  repeatCount?: number;
  objective?: string;
  plannedSession?: string;
  agenda?: string;
  placementProtected?: boolean;
}>;

export function scenarioEmail(info: TestInfo, slot: 1 | 2 | 3 | 4 | 5 | 6 | 7): string {
  const base = ACCOUNT_BASE[info.project.name];
  if (base === undefined) {
    throw new Error('No isolated user for browser project ' + info.project.name);
  }
  return 'synthetic.user+e2e-' + String(base + slot) + '@example.com';
}

export function scenarioDate(daysAhead = 4): string {
  return Temporal.Now.plainDateISO('Europe/Rome')
    .add({ days: daysAhead })
    .toString();
}

export function dateAfter(date: string, days: number): string {
  return Temporal.PlainDate.from(date).add({ days }).toString();
}

export function uniqueTitle(label: string): string {
  return 'Journey ' + label + ' ' + randomUUID().slice(0, 8);
}

export async function signedInPage(
  browser: Browser,
  info: TestInfo,
  slot: 1 | 2 | 3 | 4 | 5 | 6 | 7,
): Promise<Readonly<{ page: Page; close: () => Promise<void> }>> {
  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    timezoneId: 'Europe/Rome',
    locale: 'it-IT',
  });
  try {
    const page = await context.newPage();
    await page.addInitScript(() => {
      localStorage.setItem('dante.locale', 'it');
    });
    await page.goto('/');
    await expect(
      page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
    ).toBeVisible();
    await page.getByLabel('Email').fill(scenarioEmail(info, slot));
    await page.getByLabel('Password', { exact: true }).fill(PASSWORD);
    const authentication = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signin') &&
        response.request().method() === 'POST',
      { timeout: REQUEST_TIMEOUT },
    );
    await page.getByRole('button', { name: 'Accedi', exact: true }).click();
    expect((await authentication).status()).toBe(200);
    await expect(
      page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
    ).toBeVisible();
    return { page, close: () => context.close() };
  } catch (error) {
    await context.close();
    throw error;
  }
}

export async function openHome(page: Page, date: string): Promise<void> {
  const read = page.waitForResponse(
    (response) =>
      response.url().includes('/api/v1/temporal/timeline/window') &&
      response.request().method() === 'GET',
    { timeout: REQUEST_TIMEOUT },
  );
  await page.goto('/home?date=' + date);
  expect((await read).status()).toBe(200);
  await expect(page.locator('[data-temporal-read-state="ready"]')).toBeVisible();
}

export async function reloadHome(page: Page, date: string): Promise<void> {
  await openHome(page, date);
}

export async function openCreate(page: Page, kind: Subject): Promise<Locator> {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toBeVisible();
  if (kind === 'event') {
    await composer.getByRole('radio', { name: 'Evento', exact: true }).click();
    await expect(
      composer.getByRole('radio', { name: 'Evento', exact: true }),
    ).toHaveAttribute('aria-checked', 'true');
  }
  return composer;
}

async function setStartDate(composer: Locator, date: string): Promise<void> {
  const trigger = composer.getByRole('button', { name: /^Data inizio:/ });
  if ((await trigger.getAttribute('data-temporal-date')) !== date) {
    await trigger.click();
    const picker = composer.getByRole('dialog', { name: 'Data inizio' });
    const day = picker.locator('button[data-temporal-date="' + date + '"]');
    await expect(day).toBeVisible();
    await day.click();
  }
  await expect(trigger).toHaveAttribute('data-temporal-date', date);
}

async function setClock(composer: Locator, value: string): Promise<void> {
  const trigger = composer.getByRole('button', { name: /^Fuso orario:/ });
  if (!(await trigger.getAttribute('aria-label'))?.includes('Europe/Rome')) {
    await trigger.click();
    await composer.getByRole('button', { name: 'Europe/Rome', exact: true }).click();
  }
  const [hour, minute] = value.split(':');
  if (hour === undefined || minute === undefined) {
    throw new Error('Clock must be HH:MM: ' + value);
  }
  const end = Temporal.PlainTime.from(value).add({ minutes: 40 });
  await composer.getByRole('textbox', { name: 'Inizio: ore' }).fill(hour);
  await composer.getByRole('textbox', { name: 'Inizio: minuti' }).fill(minute);
  await composer.getByRole('textbox', { name: 'Fine: ore' }).fill(
    String(end.hour).padStart(2, '0'),
  );
  await composer.getByRole('textbox', { name: 'Fine: minuti' }).fill(
    String(end.minute).padStart(2, '0'),
  );
}

export async function configureCreate(
  composer: Locator,
  options: CreateOptions,
): Promise<void> {
  await composer.getByRole('textbox', { name: 'Titolo' }).fill(options.title);
  if (options.allDay) {
    await composer.getByRole('radio', { name: 'Tutto il giorno' }).click();
  }
  await setStartDate(composer, options.date);
  if (!options.allDay) await setClock(composer, options.clock ?? '09:10');
  const advanced =
    options.recurrence !== undefined ||
    options.objective !== undefined ||
    options.plannedSession !== undefined ||
    options.agenda !== undefined ||
    options.placementProtected === true;
  if (advanced) {
    await composer.getByRole('button', { name: /Opzioni avanzate/ }).click();
    await expect(composer).toHaveAttribute('data-temporal-create-surface', 'full');
  }
  if (options.placementProtected) {
    await composer.getByRole('button', { name: 'Blocca spostamenti' }).click();
    await expect(
      composer.getByRole('button', { name: 'Sblocca spostamenti' }),
    ).toHaveAttribute('aria-pressed', 'true');
  }
  if (options.plannedSession) {
    await composer
      .locator('[aria-label="Aggiungi Sessione pianificata"]')
      .getByRole('button', { name: 'Sessione' })
      .click();
    await composer.getByRole('textbox', { name: 'Nome Sessione' })
      .fill(options.plannedSession);
  }
  if (options.agenda) {
    await composer.getByRole('button', { name: 'Aggiungi punto alla scaletta' }).click();
    await composer.getByRole('textbox', { name: 'Punto scaletta 1' })
      .fill(options.agenda);
  }
  if (options.objective) {
    await composer.getByRole('button', { name: 'Aggiungi obiettivo' }).click();
    await composer.getByRole('textbox', { name: 'Obiettivo 1' })
      .fill(options.objective);
  }
  if (options.recurrence && options.recurrence !== 'none') {
    const panel = composer.getByRole('region', {
      name: 'Ripetizione', exact: true,
    });
    await panel.getByRole('combobox', { name: 'Ripeti' })
      .selectOption(options.recurrence);
    await expect(panel).toHaveAttribute('data-recurrence-expanded', 'true');
    if (options.monthlyOrdinal) {
      if (options.recurrence !== 'monthly') {
        throw new Error('Ordinal weekdays require a monthly recurrence.');
      }
      await panel.getByRole('button', { name: 'Per posizione' }).click();
      await expect(
        panel.getByRole('combobox', { name: 'Posizione nel mese' }),
      ).toBeVisible();
    }
    if (options.repeatCount) {
      await panel.getByRole('radio', { name: 'Dopo' }).click();
      await panel.getByRole('spinbutton', { name: 'Numero di occorrenze' })
        .fill(String(options.repeatCount));
    }
    if (options.interval && options.interval !== 1) {
      await panel.getByRole('spinbutton', { name: 'Intervallo di ripetizione' })
        .fill(String(options.interval));
    }
  }
}

export async function submitCreate(
  page: Page,
  composer: Locator,
  options: Readonly<{ kind: Subject; title: string; recurring: boolean }>,
): Promise<CreatedItem> {
  const path = options.recurring
    ? options.kind === 'activity'
      ? '/api/v1/temporal/recurring/routines'
      : '/api/v1/temporal/recurring/events'
    : '/api/v1/temporal/authoring/' +
      (options.kind === 'activity' ? 'activities' : 'events');
  const accepted = page.waitForResponse(
    (response) =>
      response.url().endsWith(path) &&
      response.request().method() === 'POST',
    { timeout: REQUEST_TIMEOUT },
  );
  await composer.getByRole('button', { name: 'Aggiungi', exact: true }).click();
  const response = await accepted;
  const payload = (await response.json()) as Record<string, unknown>;
  expect(response.ok(), JSON.stringify({ path, payload })).toBe(true);
  await expect(composer).toHaveCount(0);
  const sourceRef = payload[
    options.recurring
      ? 'source_ref'
      : options.kind === 'activity'
        ? 'activity_ref'
        : 'event_ref'
  ];
  expect(sourceRef).toEqual(expect.stringMatching(/^[\da-f-]{36}$/i));
  const schedule = payload.schedule as Record<string, unknown> | null;
  return {
    kind: options.kind,
    title: options.title,
    sourceRef: String(sourceRef),
    scheduleRef:
      typeof schedule?.schedule_ref === 'string' ? schedule.schedule_ref : null,
    firstRef:
      typeof payload.activity_ref === 'string'
        ? payload.activity_ref
        : typeof payload.event_ref === 'string'
          ? payload.event_ref
          : null,
    payload,
  };
}

export async function create(
  page: Page,
  options: CreateOptions,
): Promise<CreatedItem> {
  const composer = await openCreate(page, options.kind);
  await configureCreate(composer, options);
  return submitCreate(page, composer, {
    kind: options.kind,
    title: options.title,
    recurring: options.recurrence !== undefined &&
      options.recurrence !== 'none',
  });
}

export async function openInspector(
  page: Page,
  item: CreatedItem,
): Promise<Locator> {
  if (!item.scheduleRef) {
    throw new Error('A physical Schedule is required to open this instance.');
  }
  const card = page.locator(
    '[data-timeline-event="' + item.scheduleRef + '"]',
  );
  await expect(card).toHaveCount(1);
  await card.scrollIntoViewIfNeeded();
  await card.getByRole('button', { name: item.title, exact: true }).click();
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await expect(inspector).toBeVisible();
  await expect(inspector.getByRole('heading', { name: item.title })).toBeVisible();
  // The dialog's accessible name changes during Edit. Use a stable owner
  // locator for the whole journey instead of a stale title-bound role query.
  return inspector;
}

export async function serverRead(
  page: Page,
  path: string,
): Promise<unknown> {
  const response = await page.request.get(path, {
    headers: { 'X-Dante-Time-Zone': 'Europe/Rome' },
  });
  expect(response.status(), path).toBe(200);
  return response.json() as Promise<unknown>;
}
