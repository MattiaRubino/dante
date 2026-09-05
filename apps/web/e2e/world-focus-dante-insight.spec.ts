import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

function contextualContinue(page: Page) {
  return page
    .getByRole('button', { name: 'Chiedi a DANTE: Continua da qui' })
    .first();
}

async function openContextualInsight(page: Page) {
  const contextualInvoker = contextualContinue(page);
  await expect(contextualInvoker).toBeVisible();
  await contextualInvoker.click();

  const composer = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await expect(composer).toHaveValue('Continua da qui');
  await composer.fill('Continua da qui: trasformalo in un insight esplicito');
  await page.getByRole('button', { name: 'Invia richiesta' }).click();

  const conversation = page.getByRole('dialog', {
    name: 'Conversazione con DANTE',
    exact: true,
  });
  await expect(conversation).toBeVisible();
  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();

  const insightInvoker = page.getByRole('button', { name: 'Apri come Insight' });
  await expect(insightInvoker).toBeVisible();
  await insightInvoker.focus();
  await insightInvoker.click();

  const insight = page.getByRole('dialog', { name: 'Insight contestuale' });
  await expect(insight).toBeVisible();
  const surface = page.locator('[data-world-focus-surface-id="dante:insight"]');
  await expect(surface).toHaveAttribute('data-world-focus-surface-kind', 'dante-insight');
  await expect(surface).toHaveAttribute('data-world-focus-surface-depth', 'insight');
  await expect(surface).toHaveAttribute('data-world-focus-surface-origin', 'dante');
  await expect(insight).toContainText('Riferimenti contestuali espliciti:');
  await expect(insight).toContainText('Artefatto locale pre-backend');

  return { contextualInvoker, insightInvoker, insight, surface };
}

test('D5 materializes a standalone wide Insight sidecar and restores the exact logical invoker', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  const { insightInvoker, insight, surface } = await openContextualInsight(page);
  await expect(surface).toHaveAttribute('data-world-focus-surface-presentation', 'sidecar');
  await expect(page.getByRole('button', { name: 'Chiudi Insight DANTE' })).toBeFocused();

  await page.getByRole('button', { name: 'Chiudi Insight DANTE' }).click();
  await expect(insight).toHaveCount(0);
  await expect(insightInvoker).toBeFocused();
  await expect(
    page.getByRole('dialog', { name: 'Conversazione con DANTE', exact: true }),
  ).toBeVisible();
});

test('D5 inherits route-owned blocking geometry at 390px without horizontal overflow', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const { insight, surface } = await openContextualInsight(page);
  const workspace = page.locator('[data-world-focus-region="workspace"]');
  await expect(surface).toHaveAttribute('data-world-focus-surface-presentation', 'route');
  await expect(workspace).toHaveAttribute('data-world-focus-route-focus', 'active');
  await expect(workspace).toHaveAttribute('inert', '');

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);

  await page.getByRole('button', { name: 'Chiudi Insight DANTE' }).click();
  await expect(insight).toHaveCount(0);
});

test('D5 standalone Insight scene has no detectable axe violations at wide and compact widths', async ({
  page,
}) => {
  for (const viewport of [
    { width: 1600, height: 900 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto('/worlds/music');
    await openContextualInsight(page);

    const results = await new AxeBuilder({ page })
      .include('.world-focus-shell')
      .analyze();
    expect(results.violations).toEqual([]);
  }
});

test('D5 is not offered from global DANTE without explicit contextual references', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  await page.getByRole('button', { name: 'Apri DANTE per il Mondo Musica' }).click();
  const composer = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await composer.fill('Domanda globale senza riferimento contestuale');
  await page.getByRole('button', { name: 'Invia richiesta' }).click();

  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Apri come Insight' }),
  ).toHaveCount(0);
});
