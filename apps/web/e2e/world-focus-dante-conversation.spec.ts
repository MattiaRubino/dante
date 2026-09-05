import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openConversation(page: import('@playwright/test').Page, input: string) {
  await page
    .getByRole('button', { name: 'Apri DANTE per il Mondo Musica' })
    .click();
  const composer = page.getByRole('dialog', { name: 'DANTE' });
  const textarea = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await textarea.fill(input);
  await page.getByRole('button', { name: 'Invia richiesta' }).click();
  await expect(composer).toHaveCount(0);

  const conversation = page.getByRole('dialog', {
    name: 'Conversazione con DANTE',
  });
  await expect(conversation).toBeVisible();
  await expect(page.getByText(input)).toBeVisible();
  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();
  return conversation;
}

test('D3 hands the composer into one deterministic sidecar conversation and preserves identity through maximize/restore', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  const invoke = page.getByRole('button', {
    name: 'Apri DANTE per il Mondo Musica',
  });
  const conversation = await openConversation(
    page,
    'Perché questo progetto è in pausa?',
  );
  const surface = page.locator(
    '[data-world-focus-surface-id="dante:conversation"]',
  );

  await expect(surface).toHaveCount(1);
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(invoke).toBeDisabled();
  await expect(
    page.locator('[data-world-focus-dante-response="true"]'),
  ).toHaveAttribute('data-world-focus-dante-result-class', 'explanation');

  await page.getByRole('button', { name: 'Massimizza' }).click();
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(
    page.locator('[data-world-focus-region="workspace"]'),
  ).toHaveAttribute('data-world-focus-route-focus', 'active');
  await expect(page.getByText('Perché questo progetto è in pausa?')).toBeVisible();
  await expect(conversation).toBeVisible();

  await page.getByRole('button', { name: 'Ripristina' }).click();
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(surface).toHaveCount(1);
  await expect(page.getByText('Perché questo progetto è in pausa?')).toBeVisible();

  const followUp = page.getByRole('textbox', {
    name: 'Continua la conversazione',
  });
  await followUp.fill('E adesso cosa posso continuare?');
  await page.getByRole('button', { name: 'Invia richiesta' }).click();
  await expect(page.getByText('E adesso cosa posso continuare?')).toBeVisible();
  await expect(
    page.locator('[data-world-focus-dante-response="true"]'),
  ).toHaveCount(2);

  await page.keyboard.press('Escape');
  await expect(conversation).toHaveCount(0);
  await expect(invoke).toBeFocused();
  await expect(page).toHaveURL(/\/worlds\/music$/);
});

test('D3 uses route-owned focus at 390px instead of trapping the ongoing conversation inside the narrow World workspace', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const workspace = page.locator('[data-world-focus-region="workspace"]');
  const conversation = await openConversation(page, 'Apri una conversazione mobile');
  const surface = page.locator(
    '[data-world-focus-surface-id="dante:conversation"]',
  );

  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(page.locator('.world-focus-route-surface-layer')).toHaveAttribute(
    'data-world-focus-route-surface-count',
    '1',
  );
  await expect(workspace).toHaveAttribute('data-world-focus-route-focus', 'active');
  await expect(workspace).toHaveAttribute('inert', '');

  const workspaceBox = await workspace.boundingBox();
  const conversationBox = await conversation.boundingBox();
  expect(workspaceBox).not.toBeNull();
  expect(conversationBox).not.toBeNull();
  if (workspaceBox === null || conversationBox === null) {
    throw new Error('Expected D3 mobile route-focus geometry');
  }
  expect(conversationBox.width).toBeGreaterThan(workspaceBox.width);

  const closeBox = await page
    .getByRole('button', { name: 'Chiudi conversazione DANTE' })
    .boundingBox();
  expect(closeBox).not.toBeNull();
  if (closeBox === null) {
    throw new Error('Expected D3 route-focus close geometry');
  }
  expect(closeBox.width).toBeGreaterThanOrEqual(44);
  expect(closeBox.height).toBeGreaterThanOrEqual(44);

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
});

test('D3 conversation has no detectable axe violations at wide sidecar and compact route-focus widths', async ({
  page,
}) => {
  for (const viewport of [
    { width: 1600, height: 900 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto('/worlds/music');
    await openConversation(page, `Richiesta accessibile ${viewport.width}`);

    const results = await new AxeBuilder({ page })
      .include('.world-focus-shell')
      .analyze();
    expect(results.violations).toEqual([]);
  }
});
