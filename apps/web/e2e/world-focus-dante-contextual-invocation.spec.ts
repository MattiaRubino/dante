import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test.use({ locale: 'it-IT' });

function contextualContinue(page: import('@playwright/test').Page) {
  return page
    .getByRole('button', { name: 'Chiedi a DANTE: Continua da qui' })
    .first();
}

async function openContextualComposer(page: import('@playwright/test').Page) {
  const action = contextualContinue(page);
  await expect(action).toBeVisible();
  await action.click();

  const composer = page.getByRole('dialog', { name: 'DANTE', exact: true });
  const textarea = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await expect(composer).toBeVisible();
  await expect(composer).toHaveAttribute('data-world-focus-dante-contextual', 'true');
  await expect(textarea).toHaveValue('Continua da qui');
  await expect(textarea).toBeFocused();
  return { action, composer, textarea };
}

async function submitContextualConversation(
  page: import('@playwright/test').Page,
  input: string,
) {
  const opened = await openContextualComposer(page);
  await opened.textarea.fill(input);
  await page.getByRole('button', { name: 'Invia richiesta' }).click();

  const conversation = page.getByRole('dialog', {
    name: 'Conversazione con DANTE',
    exact: true,
  });
  await expect(conversation).toBeVisible();
  await expect(page.getByText(input)).toBeVisible();
  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();
  return { ...opened, conversation };
}

test('D4 enters the existing wide DANTE conversation from a real Continuity coordinate and restores exact focus', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  const action = contextualContinue(page);
  const actionBox = await action.boundingBox();
  expect(actionBox).not.toBeNull();
  if (actionBox === null) {
    throw new Error('Expected D4 Continuity action geometry');
  }
  expect(actionBox.width).toBeGreaterThanOrEqual(44);
  expect(actionBox.height).toBeGreaterThanOrEqual(44);

  const { conversation } = await submitContextualConversation(
    page,
    'Continua da qui: qual è il prossimo passo?',
  );
  const surface = page.locator(
    '[data-world-focus-surface-id="dante:conversation"]',
  );
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(conversation).toBeVisible();

  await page
    .getByRole('button', { name: 'Chiudi conversazione DANTE' })
    .click();
  await expect(conversation).toHaveCount(0);
  await expect(action).toBeFocused();
  await expect(page).toHaveURL(/\/worlds\/music$/);
});

test('D4 remains reachable at 390px and hands the same conversation to route-owned focus without overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const action = contextualContinue(page);
  const actionBox = await action.boundingBox();
  expect(actionBox).not.toBeNull();
  if (actionBox === null) {
    throw new Error('Expected D4 compact Continuity action geometry');
  }
  expect(actionBox.width).toBeGreaterThanOrEqual(44);
  expect(actionBox.height).toBeGreaterThanOrEqual(44);

  const { conversation } = await submitContextualConversation(
    page,
    'Continua da qui su mobile',
  );
  const surface = page.locator(
    '[data-world-focus-surface-id="dante:conversation"]',
  );
  const workspace = page.locator('[data-world-focus-region="workspace"]');
  await expect(surface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(workspace).toHaveAttribute('data-world-focus-route-focus', 'active');
  await expect(workspace).toHaveAttribute('inert', '');

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);

  await page
    .getByRole('button', { name: 'Chiudi conversazione DANTE' })
    .click();
  await expect(conversation).toHaveCount(0);
  await expect(action).toBeFocused();
});

test('D4 contextual entry and seeded composer have no detectable axe violations at wide and compact widths', async ({
  page,
}) => {
  for (const viewport of [
    { width: 1600, height: 900 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto('/worlds/music');
    await openContextualComposer(page);

    const results = await new AxeBuilder({ page })
      .include('.world-focus-shell')
      .analyze();
    expect(results.violations).toEqual([]);

    await page.getByRole('button', { name: 'Chiudi DANTE' }).click();
  }
});
