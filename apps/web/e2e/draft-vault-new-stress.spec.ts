/**
 * New independent non-auth browser journeys for Vault UX at maximum capacity.
 * The network fixture models the public API; real DB ownership/concurrency,
 * data loss and rollback are tested by draft-vault-real-lifecycle.spec.ts
 * and the PostgreSQL integration gate.
 */
import { randomUUID } from 'node:crypto';

import { expect, test, type Locator, type Page } from '@playwright/test';

import { createTemporalCreateFields } from '../src/features/temporal-create/model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../src/features/temporal-create/model/temporal-create-u2-authoring';

test.use({ locale: 'it-IT' });

type Kind = 'activity' | 'event';
type DraftRow = {
  draft_ref: string;
  subject_kind: Kind;
  title: string;
  revision: number;
  payload: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};
const now = '2026-11-23T15:00:00Z';

function draftRow(index: number, title: string, kind: Kind): DraftRow {
  const base = createTemporalCreateFields({
    title,
    kind,
    date: '2026-11-23',
    timeSemantics: index % 6 === 0 ? 'all-day' : 'timed',
    startTime: index % 2 ? '16:15' : '11:30',
    durationMinutes: 45,
    timeZoneId: 'Europe/Rome',
    timeMode: 'zoned',
  });
  const fields =
    kind === 'event'
      ? { ...base, event: {
          ...base.event,
          agendaParts: [`Agenda ${index} / 1`, `Agenda ${index} / 2`],
        } }
      : base;
  const advancedBase = createTemporalCreateU2AuthoringDraft(fields);
  const advanced = {
    ...advancedBase,
    itemColorCode: index % 2 ? '#8E24AA' : '#4285F4',
    objectives: [{
      id: `goal-${index}`,
      label: `Obiettivo ${index}`,
      resultKind: 'boolean',
      comparatorCode: null,
      targetValue: '',
      targetMin: '',
      targetMax: '',
      unitCode: '',
      verificationMode: 'none',
    }],
    activityStructure: {
      ...advancedBase.activityStructure,
      plannedSlices: kind === 'activity'
        ? Array.from({ length: 3 }, (_, ordinal) => ({
            id: `session-${index}-${ordinal}`,
            title: `Sessione ${index} ${ordinal + 1}`,
            timeEnabled: false,
            date: '2026-11-23',
            startTime: '11:30',
            endTime: '11:30',
          }))
        : [],
    },
  };
  return {
    draft_ref: `draft-stress-${index}`,
    subject_kind: kind,
    title,
    revision: 1,
    payload: { version: 1, fields, advanced, surface: 'full' },
    created_at: now,
    updated_at: now,
  };
}

async function installVaultApi(page: Page, initial: readonly DraftRow[]) {
  const records = new Map(initial.map((row) => [row.draft_ref, row]));
  const calls: string[] = [];
  await page.route('**/api/v1/auth/session', (route) =>
    route.fulfill({
      status: 200,
      json: { authenticated: true, csrf_token: 'fixture-csrf' },
    }),
  );
  await page.route('**/api/v1/temporal/drafts**', async (route) => {
    const req = route.request();
    const url = new URL(req.url());
    const method = req.method();
    const ref = url.pathname.slice('/api/v1/temporal/drafts/'.length);
    calls.push(method + ' ' + url.pathname);
    if (method === 'GET') {
      await route.fulfill({ status: 200, json: [...records.values()] });
      return;
    }
    if (method === 'PUT') {
      const body = req.postDataJSON() as {
        draft_ref: string;
        operation_id: string;
        expected_revision: number | null;
        title: string;
        subject_kind: Kind;
        payload: Record<string, unknown>;
      };
      const existing = records.get(ref);
      if (
        body.draft_ref !== ref ||
        (existing?.revision ?? null) !== body.expected_revision
      ) {
        await route.fulfill({
          status: 409,
          json: { code: 'temporal.drafts.conflict' },
        });
        return;
      }
      if (!existing && records.size >= 100) {
        await route.fulfill({
          status: 409,
          json: {
            code: 'temporal.drafts.capacity',
            detail: 'Hai raggiunto il limite di 100 Bozze.',
          },
        });
        return;
      }
      const row: DraftRow = {
        draft_ref: ref,
        subject_kind: body.subject_kind,
        title: body.title,
        revision: (existing?.revision ?? 0) + 1,
        payload: body.payload,
        created_at: existing?.created_at ?? now,
        updated_at: new Date().toISOString(),
      };
      records.set(ref, row);
      await route.fulfill({ status: 200, json: row });
      return;
    }
    if (method === 'DELETE') {
      const existing = records.get(ref);
      const expected = url.searchParams.get('expected_revision');
      if (!existing || expected !== String(existing.revision)) {
        await route.fulfill({
          status: 409,
          json: { code: 'temporal.drafts.conflict' },
        });
        return;
      }
      records.delete(ref);
      await route.fulfill({ status: 204, body: '' });
      return;
    }
    await route.fulfill({ status: 405, body: '' });
  });
  return { records, calls };
}

async function vault(page: Page): Promise<Locator> {
  const button = page.getByRole('button', { name: 'Apri Bozze' });
  if ((await button.getAttribute('aria-expanded')) !== 'true') {
    await button.click();
  }
  const panel = page.locator('[data-timeline-draft-vault="true"]');
  await expect(panel).toBeVisible();
  return panel;
}

async function refreshedVault(page: Page): Promise<Locator> {
  await page.evaluate(() => {
    window.dispatchEvent(new Event('dante:draft-vault-updated'));
  });
  return vault(page);
}

async function create(page: Page, title: string): Promise<Locator> {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toBeVisible();
  await composer.getByRole('textbox', { name: 'Titolo' }).fill(title);
  return composer;
}

test('DV-STRESS-08 100 mixed drafts: bounded vertical scroll, fixed search, untitled aliases, deletion and mobile', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  const initial = Array.from({ length: 100 }, (_, i) =>
    draftRow(i, i % 9 === 0 ? '' : `Stress ${i + 1}`, i % 2 ? 'event' : 'activity'),
  );
  const { records } = await installVaultApi(page, initial);
  await page.goto('/home');
  const panel = await vault(page);
  await expect(panel.locator('article')).toHaveCount(100);
  await expect(panel).toContainText('100/100');
  const list = panel.locator('.timeline-planning-tray__body');
  const search = panel.getByRole('searchbox', { name: 'Cerca Bozze' });
  const initialGeometry = await panel.evaluate((node) => {
    const input = node.querySelector<HTMLInputElement>('input[type="search"]')!;
    const body = node.querySelector<HTMLElement>('.timeline-planning-tray__body')!;
    return {
      top: input.getBoundingClientRect().top,
      scrollHeight: body.scrollHeight,
      clientHeight: body.clientHeight,
    };
  });
  expect(initialGeometry.scrollHeight).toBeGreaterThan(initialGeometry.clientHeight);
  const scroll = await list.evaluate((element) => {
    element.scrollTop = element.scrollHeight;
    return element.scrollTop;
  });
  expect(scroll).toBeGreaterThan(0);
  await expect.poll(() => search.evaluate((element) =>
    Math.round(element.getBoundingClientRect().top),
  )).toBe(Math.round(initialGeometry.top));
  for (const phrase of ['senza titolo', 'SENZA NOME']) {
    await search.fill(phrase);
    await expect(panel.locator('article')).toHaveCount(12);
    await expect(panel.locator('article').first()).toContainText('Senza titolo');
  }
  await search.fill('Stress 99');
  await expect(panel.locator('article')).toHaveCount(1);
  await search.fill('');
  await expect(panel.locator('article')).toHaveCount(100);
  const chosen = panel.locator('article').filter({ hasText: 'Stress 99' });
  await chosen.getByRole('button', { name: 'Elimina' }).click();
  await chosen.getByRole('button', { name: 'Annulla' }).click();
  expect(records).toHaveProperty('size', 100);
  await chosen.getByRole('button', { name: 'Elimina' }).click();
  await chosen.getByRole('button', { name: 'Conferma eliminazione' }).click();
  await expect(panel).toContainText('99/100');
  expect(records.size).toBe(99);
  await page.setViewportSize({ width: 390, height: 844 });
  const box = await panel.boundingBox();
  if (!box) throw new Error('Missing mobile Vault box');
  expect(box.x).toBeGreaterThanOrEqual(0);
  expect(box.x + box.width).toBeLessThanOrEqual(391);
  await expect(search).toBeInViewport();
  await panel.getByRole('button', { name: 'Chiudi Bozze' }).click();
  await vault(page);
  await expect(search).toHaveValue('');
  await expect(panel.locator('article')).toHaveCount(99);
});

test('DV-STRESS-09 full Vault: new and duplicated Saves fail safely, one deletion restores capacity', async ({
  page,
}) => {
  const initial = Array.from({ length: 100 }, (_, i) =>
    draftRow(i, 'Quota ' + i, i % 2 ? 'event' : 'activity'),
  );
  const { records, calls } = await installVaultApi(page, initial);
  await page.goto('/home');
  const title = 'Compilazione conservata quando archivio pieno';
  const composer = await create(page, title);
  await composer.getByRole('button', { name: 'Salva bozza' }).click();
  const popup = page.getByRole('alertdialog', { name: 'Spazio Bozze esaurito' });
  await expect(popup).toBeVisible();
  expect(records.size).toBe(100);
  await expect(composer.getByRole('textbox', { name: 'Titolo' })).toHaveValue(title);
  await popup.getByRole('button', { name: 'Chiudi' }).click();
  await expect(popup).toHaveCount(0);
  // Dismissing the quota portal must not be interpreted as clicking outside
  // Create, which otherwise opens a blocking "discard changes" confirmation.
  await expect(
    page.locator('[data-temporal-create="discard-modal"]'),
  ).toHaveCount(0);
  await expect(
    composer.getByRole('textbox', { name: 'Titolo' }),
  ).toHaveValue(title);
  const toFree = [...records.keys()][0]!;
  records.delete(toFree);
  await composer.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(composer).toHaveCount(0);
  expect(records.size).toBe(100);
  const created = [...records.values()].find((row) => row.title === title);
  expect(created).toBeTruthy();

  const panel = await refreshedVault(page);
  await expect(panel).toContainText('100/100');
  await panel.locator('article').filter({ hasText: title })
    .getByRole('button', { name: 'Duplica' }).click();
  const duplicated = page.locator('[data-temporal-create="composer"]');
  await expect(duplicated).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await duplicated.getByRole('textbox', { name: 'Titolo' })
    .fill('Seconda copia al limite');
  await duplicated.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(popup).toBeVisible();
  await expect(duplicated.getByRole('textbox', { name: 'Titolo' }))
    .toHaveValue('Seconda copia al limite');
  expect(records.size).toBe(100);
  expect(records.get(created!.draft_ref)?.title).toBe(title);
  expect(calls.filter((path) => path.startsWith('PUT ')).length)
    .toBeGreaterThanOrEqual(3);
});

test('DV-STRESS-10 advanced mixed archive: Resume CAS, session/agenda/objectives fidelity, Duplicate and Delete', async ({
  page,
}) => {
  const initial = Array.from({ length: 8 }, (_, i) =>
    draftRow(i, `Configurazione ${i + 1}`, i % 2 ? 'event' : 'activity'),
  );
  const { records } = await installVaultApi(page, initial);
  await page.goto('/home');
  let panel = await vault(page);

  const activity = panel.locator('article').filter({ hasText: 'Configurazione 1' });
  await activity.getByRole('button', { name: 'Riprendi' }).click();
  let composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await expect(composer.locator('[data-create-planned-session]')).toHaveCount(3);
  await expect(composer.locator('[data-create-objective]')).toHaveCount(1);
  await expect(composer.getByRole('textbox', { name: 'Titolo' }))
    .toHaveValue('Configurazione 1');
  await composer.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(composer).toHaveCount(0);
  expect(records.get('draft-stress-0')?.revision).toBe(2);
  expect(records.size).toBe(8);

  panel = await refreshedVault(page);
  const event = panel.locator('article').filter({ hasText: 'Configurazione 2' });
  await event.getByRole('button', { name: 'Duplica' }).click();
  composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toHaveAttribute('data-temporal-create-surface', 'advanced');
  await expect(composer.locator('[data-temporal-create-agenda-part]')).toHaveCount(2);
  await expect(composer.locator('[data-create-objective]')).toHaveCount(1);
  await composer.getByRole('textbox', { name: 'Titolo' })
    .fill('Nuovo Event duplicato');
  await composer.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(composer).toHaveCount(0);
  expect(records.size).toBe(9);
  expect(records.get('draft-stress-1')?.title).toBe('Configurazione 2');
  const copy = [...records.values()].filter((row) => row.title === 'Nuovo Event duplicato');
  expect(copy).toHaveLength(1);
  expect(copy[0]!.draft_ref).not.toBe('draft-stress-1');
  expect(JSON.stringify(copy[0]!.payload)).toContain('Agenda 1 / 1');

  panel = await refreshedVault(page);
  const row = panel.locator('article').filter({ hasText: 'Nuovo Event duplicato' });
  await row.getByRole('button', { name: 'Elimina' }).click();
  await expect(row).toContainText('Eliminare definitivamente questa bozza?');
  await row.getByRole('button', { name: 'Annulla' }).click();
  expect(records.size).toBe(9);
  await row.getByRole('button', { name: 'Elimina' }).click();
  await row.getByRole('button', { name: 'Conferma eliminazione' }).click();
  await expect(panel.locator('article')).toHaveCount(8);
  expect(records.size).toBe(8);
  await expect(panel.locator('article').filter({ hasText: 'Configurazione 2' }))
    .toBeVisible();
  await expect(panel.getByRole('button', { name: 'Play' })).toHaveCount(0);
  await expect(panel.getByRole('button', { name: 'Pausa' })).toHaveCount(0);
});
