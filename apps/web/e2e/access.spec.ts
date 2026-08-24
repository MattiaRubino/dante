import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const signInHeading = 'Accedi a DANTE';

async function expectNoHorizontalOverflow(page: Page) {
  const hasOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth,
  );

  expect(hasOverflow).toBe(false);
}

test.describe('DANTE Access', () => {
  test('renders the approved desktop A3.4 sign-in shell', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Lingua: Italiano' })).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Google' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Apple' }),
    ).toBeVisible();
    await expect(page.getByLabel('Email')).toHaveAttribute(
      'autocomplete',
      'email',
    );
    await expect(page.getByLabel('Password')).toHaveAttribute(
      'autocomplete',
      'current-password',
    );
    await expect(page.locator('.access-brand-stage')).toBeVisible();
    await expect(page.locator('.access-panel')).toHaveCSS(
      'border-radius',
      '26px',
    );
    await expectNoHorizontalOverflow(page);
  });

  test('switches to the narrow single-column composition', async ({ page }) => {
    await page.setViewportSize({ width: 800, height: 1000 });
    await page.goto('/');

    await expect(page.locator('.access-brand-stage')).toBeHidden();
    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(
      page.getByRole('heading', { level: 1, name: signInHeading }),
    ).toBeVisible();
    await expectNoHorizontalOverflow(page);
  });

  test('remains usable at a phone-width browser viewport', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');

    await expect(page.locator('.access-brand-lockup')).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Google' }),
    ).toBeVisible();
    await expect(
      page.getByRole('button', { name: 'Continua con Apple' }),
    ).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expectNoHorizontalOverflow(page);
  });

  test('exposes a keyboard-focusable sign-in path', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const localeButton = page.getByRole('button', { name: 'Lingua: Italiano' });
    const googleButton = page.getByRole('button', {
      name: 'Continua con Google',
    });

    await page.keyboard.press('Tab');
    await expect(localeButton).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(googleButton).toBeFocused();
  });

  test('has no automated WCAG A/AA violations on the sign-in surface', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
