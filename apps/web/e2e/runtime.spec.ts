import { expect, test } from '@playwright/test';

test('renders the real DANTE Web diagnostic runtime from a production build', async ({
  page,
}) => {
  await page.goto('/');

  await expect(page).toHaveURL('http://127.0.0.1:4173/');
  await expect(
    page.getByRole('heading', { level: 1, name: 'Frontend pronto' }),
  ).toBeVisible();
  await expect(page.getByText('DANTE Web', { exact: true })).toBeVisible();

  const routeRow = page.getByText('Percorso', { exact: true }).locator('..');
  await expect(routeRow).toContainText('/');

  const purposeRow = page.getByText('Scopo', { exact: true }).locator('..');
  await expect(purposeRow).toContainText('Scaffold diagnostico FM-03');
  await expect(
    purposeRow.getByText('2026-08-22T20:00:00+02:00[Europe/Rome]', {
      exact: true,
    }),
  ).toBeVisible();
});
