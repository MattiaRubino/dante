import { expect, test, type Locator, type Page } from '@playwright/test';

test.use({ locale: 'it-IT' });

const PRESSURE_WIDTHS = [
  1856, 1600, 1366, 1200, 1121, 1120, 1024, 901, 900, 760, 390,
] as const;

const AI_ROUND_TRIP_WIDTHS = [1856, 1366, 1024, 901] as const;
const STAGE_MODE_WIDTHS = [1366, 901, 900] as const;
const TIMELINE_EXPANSION_WIDTHS = [1856, 1366, 1121] as const;

const REQUIRED_HOME_REGIONS = [
  'shell',
  'ai-surface',
  'orientation',
  'central-stage',
  'timeline',
  'context-rail',
] as const;

type Box = NonNullable<Awaited<ReturnType<Locator['boundingBox']>>>;

async function visibleBox(locator: Locator): Promise<Box> {
  await expect(locator).toBeVisible();
  const box = await locator.boundingBox();
  expect(box).not.toBeNull();
  if (!box) {
    throw new Error('Expected visible structural geometry');
  }
  return box;
}

async function documentBox(locator: Locator): Promise<Box> {
  await expect(locator).toBeVisible();
  return locator.evaluate((element) => {
    const rect = element.getBoundingClientRect();
    return {
      x: rect.left + window.scrollX,
      y: rect.top + window.scrollY,
      width: rect.width,
      height: rect.height,
    };
  });
}

function expectClose(actual: number, expected: number, tolerance = 1.5) {
  expect(Math.abs(actual - expected)).toBeLessThanOrEqual(tolerance);
}

function expectSameBox(actual: Box, expected: Box, tolerance = 1.5) {
  expectClose(actual.x, expected.x, tolerance);
  expectClose(actual.y, expected.y, tolerance);
  expectClose(actual.width, expected.width, tolerance);
  expectClose(actual.height, expected.height, tolerance);
}

async function expectNoHorizontalPageOverflow(page: Page) {
  const overflow = await page.evaluate(() => {
    const root = document.documentElement;
    const body = document.body;
    return Math.max(root.scrollWidth, body.scrollWidth) - window.innerWidth;
  });
  expect(overflow).toBeLessThanOrEqual(1);
}

async function openHomeAt(page: Page, width: number) {
  await page.setViewportSize({ width, height: 1000 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/home');
  await expect(page.getByRole('main', { name: 'Home DANTE' })).toBeVisible();
}

for (const width of PRESSURE_WIDTHS) {
  test(`H0 structural composition remains bounded at ${width}px`, async ({
    page,
  }) => {
    await openHomeAt(page, width);

    const shell = page.locator('[data-home-region="shell"]');
    const topbar = page.locator('[data-app-region="topbar"]');
    const ai = page.locator('[data-home-region="ai-surface"]');
    const upper = page.locator('[data-home-layout="upper-workspace"]');
    const orientation = page.locator('[data-home-region="orientation"]');
    const stage = page.locator('[data-home-region="central-stage"]');
    const timeline = page.locator('[data-home-region="timeline"]');
    const rail = page.locator('[data-home-region="context-rail"]');

    await expect(shell).toHaveCount(1);
    await expect(topbar).toHaveCount(1);
    await expect(shell.locator('[data-app-region="topbar"]')).toHaveCount(0);

    for (const region of REQUIRED_HOME_REGIONS) {
      await expect(page.locator(`[data-home-region="${region}"]`)).toHaveCount(
        1,
      );
    }

    await expectNoHorizontalPageOverflow(page);

    const aiBox = await visibleBox(ai);
    const upperBox = await visibleBox(upper);
    const timelineBox = await visibleBox(timeline);

    if (width >= 1121) {
      const railBox = await visibleBox(rail);
      expect(aiBox.x + aiBox.width).toBeLessThanOrEqual(upperBox.x + 2);
      expect(timelineBox.x + timelineBox.width).toBeLessThanOrEqual(
        railBox.x + 2,
      );
      expect(railBox.x).toBeGreaterThan(timelineBox.x);
      return;
    }

    await expect(rail).toBeHidden();
    expect(timelineBox.x + timelineBox.width).toBeGreaterThanOrEqual(width - 2);

    if (width >= 901) {
      expect(aiBox.x + aiBox.width).toBeLessThanOrEqual(upperBox.x + 2);
      return;
    }

    expect(aiBox.y + aiBox.height).toBeLessThanOrEqual(upperBox.y + 2);
    const orientationBox = await visibleBox(orientation);
    const stageBox = await visibleBox(stage);
    expect(orientationBox.y).toBeLessThan(stageBox.y);
  });
}

for (const width of AI_ROUND_TRIP_WIDTHS) {
  test(`H0 AI collapse round-trip restores macro geometry at ${width}px`, async ({
    page,
  }) => {
    await openHomeAt(page, width);

    const shell = page.locator('[data-home-region="shell"]');
    const upper = page.locator('[data-home-layout="upper-workspace"]');
    const today = page.locator('[data-home-layout="today"]');
    const beforeUpper = await visibleBox(upper);
    const beforeToday = await visibleBox(today);

    await page.getByRole('button', { name: 'Comprimi assistente' }).click();
    await expect(shell).toHaveAttribute('data-home-ai-state', 'collapsed');

    await page.getByRole('button', { name: 'Espandi assistente' }).click();
    await expect(shell).toHaveAttribute('data-home-ai-state', 'expanded');

    const afterUpper = await visibleBox(upper);
    const afterToday = await visibleBox(today);
    expectSameBox(afterUpper, beforeUpper);
    expectSameBox(afterToday, beforeToday);
    await expectNoHorizontalPageOverflow(page);
  });
}

for (const width of STAGE_MODE_WIDTHS) {
  test(`H0 Stage mode switch cannot reauthor Home macro geometry at ${width}px`, async ({
    page,
  }) => {
    await openHomeAt(page, width);

    const hero = page.locator('[data-home-layout="hero"]');
    const today = page.locator('[data-home-layout="today"]');
    const stage = page.locator('[data-home-region="central-stage"]');
    const beforeHero = await visibleBox(hero);
    const beforeToday = await visibleBox(today);
    const beforeStage = await visibleBox(stage);

    await stage.getByRole('button', { name: 'Proiezione successiva' }).click();
    await expect(stage).toHaveAttribute('data-home-stage-mode', 'signals');

    const afterHero = await visibleBox(hero);
    const afterToday = await visibleBox(today);
    const afterStage = await visibleBox(stage);
    expectSameBox(afterHero, beforeHero);
    expectSameBox(afterToday, beforeToday);
    expectSameBox(afterStage, beforeStage);
    await expectNoHorizontalPageOverflow(page);
  });
}

for (const width of TIMELINE_EXPANSION_WIDTHS) {
  test(`H0 Timeline expansion only consumes Today rail space at ${width}px`, async ({
    page,
  }) => {
    await openHomeAt(page, width);

    const shell = page.locator('[data-home-region="shell"]');
    const hero = page.locator('[data-home-layout="hero"]');
    const timeline = page.locator('[data-home-region="timeline"]');
    const beforeHero = await documentBox(hero);
    const beforeTimeline = await documentBox(timeline);

    await page.getByRole('button', { name: 'Espandi timeline' }).click();
    await expect(shell).toHaveAttribute('data-home-timeline-state', 'expanded');

    const expandedHero = await documentBox(hero);
    const expandedTimeline = await documentBox(timeline);
    expectSameBox(expandedHero, beforeHero);
    expect(expandedTimeline.width).toBeGreaterThan(beforeTimeline.width + 100);
    await expectNoHorizontalPageOverflow(page);

    await page.getByRole('button', { name: 'Riduci timeline' }).click();
    await expect(shell).toHaveAttribute('data-home-timeline-state', 'normal');

    const restoredHero = await documentBox(hero);
    const restoredTimeline = await documentBox(timeline);
    expectSameBox(restoredHero, beforeHero);
    expectSameBox(restoredTimeline, beforeTimeline, 2);
  });
}
