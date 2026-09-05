import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

async function openContextualInsight(page: Page) {
  const contextualInvoker = page
    .getByRole('button', { name: 'Chiedi a DANTE: Continua da qui' })
    .first();
  await expect(contextualInvoker).toBeVisible();
  await contextualInvoker.click();

  const composer = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await expect(composer).toHaveValue('Continua da qui');
  await composer.fill('Continua da qui: prepara un prossimo passo governato');
  await page.getByRole('button', { name: 'Invia richiesta' }).click();
  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();

  await page.getByRole('button', { name: 'Apri come Insight' }).click();
  const insight = page.getByRole('dialog', { name: 'Insight contestuale' });
  await expect(insight).toBeVisible();
  return insight;
}

async function openProposal(page: Page) {
  const insight = await openContextualInsight(page);
  const proposalInvoker = page.getByRole('button', { name: 'Prepara proposta' });
  await expect(proposalInvoker).toBeVisible();
  const invokerBox = await proposalInvoker.boundingBox();
  expect(invokerBox).not.toBeNull();
  if (invokerBox === null) {
    throw new Error('Expected D6 Proposal invoker geometry');
  }
  expect(invokerBox.height).toBeGreaterThanOrEqual(44);
  await proposalInvoker.click();

  const proposal = page.getByRole('dialog', { name: 'Proposta contestuale' });
  await expect(proposal).toBeVisible();
  await expect(proposal).toContainText('Nessuna operazione è stata eseguita.');
  const proposalSurface = page.locator(
    '[data-world-focus-surface-id="dante:proposal"]',
  );
  await expect(proposalSurface).toHaveAttribute(
    'data-world-focus-surface-kind',
    'dante-proposal',
  );
  await expect(proposalSurface).toHaveAttribute(
    'data-world-focus-surface-origin',
    'dante',
  );

  return { insight, proposal, proposalInvoker, proposalSurface };
}

async function expectNoHorizontalOverflow(page: Page) {
  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
}

async function expectAxeClean(page: Page) {
  const results = await new AxeBuilder({ page })
    .include('.world-focus-shell')
    .analyze();
  expect(results.violations).toEqual([]);
}

test('D6 keeps wide Proposal, blocking Confirmation and confirmed Receipt distinct with deterministic focus restoration', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  const { proposal, proposalInvoker, proposalSurface } = await openProposal(page);
  await expect(proposalSurface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(
    page.getByRole('button', { name: 'Rivedi conferma' }),
  ).toBeFocused();
  await expectAxeClean(page);

  await page.getByRole('button', { name: 'Rivedi conferma' }).click();
  const confirmation = page.getByRole('alertdialog', { name: 'Conferma proposta' });
  const confirmationSurface = page.locator(
    '[data-world-focus-surface-id="dante:confirmation"]',
  );
  const workspace = page.locator('[data-world-focus-region="workspace"]');
  await expect(confirmation).toBeVisible();
  await expect(confirmationSurface).toHaveAttribute(
    'data-world-focus-surface-kind',
    'dante-confirmation',
  );
  await expect(confirmationSurface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(workspace).toHaveAttribute('inert', '');
  await expect(page.getByRole('button', { name: 'Rifiuta' })).toBeFocused();
  await expectAxeClean(page);

  await page.keyboard.press('Escape');
  await expect(confirmation).toBeVisible();
  await expect(page).toHaveURL(/\/worlds\/music$/);

  await page.getByRole('button', { name: 'Conferma', exact: true }).click();
  const receipt = page.getByRole('dialog', { name: 'Ricevuta decisione' });
  const receiptSurface = page.locator(
    '[data-world-focus-surface-id="dante:receipt"]',
  );
  await expect(receipt).toBeVisible();
  await expect(receipt).toHaveAttribute(
    'data-world-focus-dante-decision',
    'confirmed',
  );
  await expect(receipt).toHaveAttribute(
    'data-world-focus-dante-effect-execution',
    'not-executed',
  );
  await expect(receipt).toContainText('Nessuna operazione è stata eseguita.');
  await expect(receipt).toContainText(
    'non prova completamento provider, runtime o canonico',
  );
  await expect(receipt).not.toContainText('Operazione completata');
  await expect(receiptSurface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'sidecar',
  );
  await expect(
    page.getByRole('button', { name: 'Chiudi ricevuta DANTE' }),
  ).toBeFocused();
  await expectAxeClean(page);

  await page.getByRole('button', { name: 'Chiudi ricevuta DANTE' }).click();
  await expect(receipt).toHaveCount(0);
  await expect(proposal).toBeVisible();
  await expect(
    page.getByRole('button', { name: 'Chiudi proposta DANTE' }),
  ).toBeFocused();

  await page.getByRole('button', { name: 'Chiudi proposta DANTE' }).click();
  await expect(proposal).toHaveCount(0);
  await expect(page.getByRole('dialog', { name: 'Insight contestuale' })).toBeVisible();
  await expect(proposalInvoker).toBeFocused();
});

test('D6 inherits compact route blocking geometry, records decline locally and never overflows', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/worlds/music');

  const { proposalSurface } = await openProposal(page);
  const workspace = page.locator('[data-world-focus-region="workspace"]');
  await expect(proposalSurface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(workspace).toHaveAttribute('data-world-focus-route-focus', 'active');
  await expect(workspace).toHaveAttribute('inert', '');
  await expectNoHorizontalOverflow(page);
  await expectAxeClean(page);

  await page.getByRole('button', { name: 'Rivedi conferma' }).click();
  const confirmation = page.getByRole('alertdialog', { name: 'Conferma proposta' });
  await expect(confirmation).toBeVisible();
  await expect(workspace).toHaveAttribute('inert', '');
  await expectNoHorizontalOverflow(page);
  await expectAxeClean(page);

  await page.keyboard.press('Escape');
  await expect(confirmation).toBeVisible();

  await page.getByRole('button', { name: 'Rifiuta' }).click();
  const receipt = page.getByRole('dialog', { name: 'Ricevuta decisione' });
  const receiptSurface = page.locator(
    '[data-world-focus-surface-id="dante:receipt"]',
  );
  await expect(receipt).toHaveAttribute(
    'data-world-focus-dante-decision',
    'declined',
  );
  await expect(receipt).toHaveAttribute(
    'data-world-focus-dante-effect-execution',
    'not-executed',
  );
  await expect(receiptSurface).toHaveAttribute(
    'data-world-focus-surface-presentation',
    'route',
  );
  await expect(receipt).toContainText('Nessuna operazione è stata eseguita.');
  await expectNoHorizontalOverflow(page);
  await expectAxeClean(page);
});

test('D6 remains unreachable from context-free global DANTE because no validated Insight exists', async ({
  page,
}) => {
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto('/worlds/music');

  await page.getByRole('button', { name: 'Apri DANTE per il Mondo Musica' }).click();
  const composer = page.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  await composer.fill('Prepara direttamente una proposta senza contesto');
  await page.getByRole('button', { name: 'Invia richiesta' }).click();
  await expect(
    page.getByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    ),
  ).toBeVisible();

  await expect(page.getByRole('button', { name: 'Apri come Insight' })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Prepara proposta' })).toHaveCount(0);
});
