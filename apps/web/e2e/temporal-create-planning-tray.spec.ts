import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

type DraftResponse = {
  draft_ref: string;
  subject_kind: 'activity' | 'event';
  title: string;
  revision: number;
  payload: unknown;
  created_at: string;
  updated_at: string;
};

/**
 * Non-auth Playwright exercises the Draft Vault's UI/HTTP contract with an
 * explicit local fixture. Durable PostgreSQL/API acceptance belongs to the
 * separate auth/full-stack browser project.
 */
async function installDraftVaultFixture(page: Page) {
  const records = new Map<string, DraftResponse>();
  await page.route('**/api/v1/auth/session', (route) =>
    route.fulfill({
      status: 200,
      json: { authenticated: true, csrf_token: 'fixture-csrf' },
    }),
  );
  await page.route('**/api/v1/temporal/drafts**', async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    const key = path.slice('/api/v1/temporal/drafts/'.length);
    const method = request.method();
    if (method === 'GET') {
      await route.fulfill({ status: 200, json: [...records.values()] });
      return;
    }
    if (method === 'PUT') {
      const body = request.postDataJSON() as {
        draft_ref: string;
        title: string;
        subject_kind: 'activity' | 'event';
        expected_revision: number | null;
        payload: unknown;
      };
      const existing = records.get(key);
      if (
        body.draft_ref !== key ||
        (existing?.revision ?? null) !== body.expected_revision
      ) {
        await route.fulfill({
          status: 409,
          json: { error: 'revision_conflict' },
        });
        return;
      }
      const now = new Date().toISOString();
      const row: DraftResponse = {
        draft_ref: key,
        subject_kind: body.subject_kind,
        title: body.title,
        revision: (existing?.revision ?? 0) + 1,
        payload: body.payload,
        created_at: existing?.created_at ?? now,
        updated_at: now,
      };
      records.set(key, row);
      await route.fulfill({ status: 200, json: row });
      return;
    }
    if (method === 'DELETE') {
      const existing = records.get(key);
      const expected = new URL(request.url()).searchParams.get(
        'expected_revision',
      );
      if (!existing || String(existing.revision) !== expected) {
        await route.fulfill({
          status: 409,
          json: { error: 'revision_conflict' },
        });
        return;
      }
      records.delete(key);
      await route.fulfill({ status: 204, body: '' });
      return;
    }
    await route.fulfill({ status: 405, body: '' });
  });
  return records;
}

async function saveDraft(page: Page, title: string) {
  await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog).toBeVisible();
  await dialog.getByRole('textbox', { name: 'Titolo' }).fill(title);
  await dialog.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(dialog).toHaveCount(0);
}

async function openDraftVault(page: Page) {
  const trigger = page.getByRole('button', { name: 'Apri Bozze' });
  await expect(trigger).toBeVisible();
  if ((await trigger.getAttribute('aria-expanded')) !== 'true') {
    await trigger.click();
  }
  const vault = page.locator('[data-timeline-draft-vault="true"]');
  await expect(vault).toBeVisible();
  return vault;
}

function draft(vault: ReturnType<Page['locator']>, title: string) {
  return vault.locator('article').filter({ hasText: title });
}

test('Draft Vault keeps search fixed while many full-size cards scroll and filter live', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const records = await installDraftVaultFixture(page);
  await saveDraft(page, 'Bozza 1');
  const seed = [...records.values()][0]!;
  for (let index = 2; index <= 8; index += 1) {
    const ref = `draft-${index}`;
    records.set(ref, { ...seed, draft_ref: ref, title: `Bozza ${index}` });
  }

  const vault = await openDraftVault(page);
  // The fixture changes its in-memory API rows outside a user command.
  // Publish the same invalidation that a draft write would send.
  await page.evaluate(() =>
    window.dispatchEvent(new Event('dante:draft-vault-updated')),
  );
  await expect(vault.locator('article')).toHaveCount(8);
  const search = vault.getByRole('searchbox', { name: 'Cerca Bozze' });
  const list = vault.locator('.timeline-planning-tray__body');
  const geometry = await vault.evaluate((panel) => {
    const input = panel.querySelector<HTMLInputElement>('input[type="search"]')!;
    const body = panel.querySelector<HTMLElement>('.timeline-planning-tray__body')!;
    return {
      width: panel.getBoundingClientRect().width,
      inputHeight: input.getBoundingClientRect().height,
      searchBottom: input.getBoundingClientRect().bottom,
      listTop: body.getBoundingClientRect().top,
      listClientHeight: body.clientHeight,
      listScrollHeight: body.scrollHeight,
      scrollbarGutter: getComputedStyle(body).scrollbarGutter,
    };
  });
  expect(geometry.width).toBeGreaterThanOrEqual(500);
  expect(geometry.inputHeight).toBe(42);
  expect(geometry.searchBottom).toBeLessThan(geometry.listTop);
  expect(geometry.listScrollHeight).toBeGreaterThan(geometry.listClientHeight);
  expect(geometry.scrollbarGutter).toBe('stable');

  const cardStyle = await vault.locator('article').first().evaluate((card) => {
    const title = card.querySelector<HTMLElement>(
      '.timeline-planning-card__copy strong',
    )!;
    const schedule = card.querySelector<HTMLElement>(
      '.timeline-planning-card__schedule',
    )!;
    const action = card.querySelector<HTMLButtonElement>(
      '.timeline-planning-card__actions button',
    )!;
    return {
      accent: getComputedStyle(card)
        .getPropertyValue('--timeline-group-color')
        .trim(),
      titleSize: Number.parseFloat(getComputedStyle(title).fontSize),
      scheduleSize: Number.parseFloat(getComputedStyle(schedule).fontSize),
      actionSize: Number.parseFloat(getComputedStyle(action).fontSize),
      actionWeight: Number.parseInt(getComputedStyle(action).fontWeight, 10),
      actionColor: getComputedStyle(action).color,
    };
  });
  expect(cardStyle.accent).toBe('#ea5c12');
  expect(cardStyle.titleSize).toBeGreaterThanOrEqual(15);
  expect(cardStyle.scheduleSize).toBeGreaterThanOrEqual(12);
  expect(cardStyle.actionSize).toBeGreaterThanOrEqual(12);
  expect(cardStyle.actionWeight).toBeGreaterThanOrEqual(600);
  expect(cardStyle.actionColor).toBe('rgb(243, 246, 251)');

  await search.fill('bozza 7');
  await expect(vault.locator('article')).toHaveCount(1);
  await expect(draft(vault, 'Bozza 7')).toBeVisible();
  await expect(list).not.toContainText('Bozza 1');

  await page.setViewportSize({ width: 390, height: 800 });
  await expect(vault).toBeInViewport();
  await expect(search).toBeInViewport();
});

test('saving a Draft never creates an executable Timeline card and Resume preserves its identity', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const records = await installDraftVaultFixture(page);

  await saveDraft(page, 'Preparare portfolio');
  expect(records.size).toBe(1);
  await expect(
    page
      .locator('.timeline-event-card')
      .filter({ hasText: 'Preparare portfolio' }),
  ).toHaveCount(0);
  const vault = await openDraftVault(page);
  const item = draft(vault, 'Preparare portfolio');
  await expect(item).toBeVisible();
  await expect(item).toContainText('Non attiva');

  const accessibility = await new AxeBuilder({ page })
    .include('[data-timeline-draft-vault="true"]')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(accessibility.violations).toEqual([]);

  const originalId = [...records.keys()][0];
  await item.getByRole('button', { name: 'Riprendi' }).click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await expect(dialog.getByRole('textbox', { name: 'Titolo' })).toHaveValue(
    'Preparare portfolio',
  );
  await dialog.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(dialog).toHaveCount(0);
  expect([...records.keys()]).toEqual([originalId]);
  expect(records.get(originalId ?? '')?.revision).toBe(2);
});

test('duplicating a Draft creates a separate inert draft without mutating the original', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/home');
  const records = await installDraftVaultFixture(page);
  await saveDraft(page, 'Scrivere proposta');
  const originalId = [...records.keys()][0];
  const vault = await openDraftVault(page);
  await draft(vault, 'Scrivere proposta')
    .getByRole('button', { name: 'Duplica' })
    .click();
  const dialog = page.locator('[data-temporal-create="composer"]');
  await dialog
    .getByRole('textbox', { name: 'Titolo' })
    .fill('Proposta duplicata');
  await dialog.getByRole('button', { name: 'Salva bozza' }).click();
  await expect(dialog).toHaveCount(0);
  expect(records.size).toBe(2);
  expect(records.get(originalId ?? '')?.title).toBe('Scrivere proposta');
  expect(
    [...records.values()].some((value) => value.title === 'Proposta duplicata'),
  ).toBe(true);
  await expect(
    page
      .locator('.timeline-event-card')
      .filter({ hasText: 'Proposta duplicata' }),
  ).toHaveCount(0);
});

test('deleting a Draft requires explicit confirmation and does not affect other drafts', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1280, height: 820 });
  await page.goto('/home');
  const records = await installDraftVaultFixture(page);
  await saveDraft(page, 'Pulire archivio');
  await saveDraft(page, 'Rivedere note');
  const vault = await openDraftVault(page);
  const item = draft(vault, 'Pulire archivio');
  await item.getByRole('button', { name: 'Elimina' }).click();
  await expect(item).toContainText('Eliminare definitivamente questa bozza?');
  await item.getByRole('button', { name: 'Annulla' }).click();
  await expect(item).toBeVisible();
  expect(records.size).toBe(2);
  await item.getByRole('button', { name: 'Elimina' }).click();
  await item.getByRole('button', { name: 'Conferma eliminazione' }).click();
  await expect(draft(vault, 'Pulire archivio')).toHaveCount(0);
  await expect(draft(vault, 'Rivedere note')).toBeVisible();
  expect(records.size).toBe(1);
});

test('Draft Vault stays inside the mobile viewport without horizontal overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/home');
  await installDraftVaultFixture(page);
  await saveDraft(page, 'Telefonare assicurazione');
  const vault = await openDraftVault(page);
  const bounds = await vault.boundingBox();
  if (!bounds) throw new Error('Expected mobile Draft Vault geometry');
  expect(bounds.x).toBeGreaterThanOrEqual(0);
  expect(bounds.x + bounds.width).toBeLessThanOrEqual(390.5);
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth <=
        document.documentElement.clientWidth,
    ),
  ).toBe(true);
  await expect(draft(vault, 'Telefonare assicurazione')).toBeVisible();
});
