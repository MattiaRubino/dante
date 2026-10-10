import { expect, test } from '@playwright/test';

// Real browser + Timeline integration; API is deterministic here. PostgreSQL
// command/ownership proof belongs to test_b14_session_panel.py, not this fixture.
const activity = '0199a111-1111-7111-8111-111111111111';
const schedule = '0199a222-2222-7222-8222-222222222222';
const session = '0199a333-3333-7333-8333-333333333333';
const state = '0199a444-4444-7444-8444-444444444444';

for (const width of [1440, 390]) {
  test(`session panel geometry and lifecycle at ${width}px`, async ({
    page,
  }, testInfo) => {
    await page.setViewportSize({ width, height: 900 });
    let execution: {
      session_ref: string;
      timing_material_state_ref: string;
      paused: boolean;
    } | null = null;
    const commands: string[] = [];
    let stopped = false;
    const now = '2026-10-09T10:00:00Z';
    await page.route('**/api/v1/**', async (route) => {
      const path = new URL(route.request().url()).pathname;
      if (path.endsWith('/session-panel')) {
        await route.fulfill({
          json: {
            evaluated_at: now,
            next_change_at: null,
            visuals: [],
            groups: stopped ? [] : [
              {
                activity_ref: activity,
                title: 'Studio e preparazione di una presentazione molto lunga',
                rows: [
                  {
                    planned_schedule_ref: schedule,
                    name: 'Ripasso',
                    starts_at: null,
                    execution,
                  },
                ],
              },
            ],
          },
        });
      } else if (path.endsWith('/auth/session')) {
        await route.fulfill({
          json: { authenticated: true, csrf_token: 'test-csrf' },
        });
      } else if (
        route.request().method() === 'POST' &&
        path.includes('/sessions')
      ) {
        commands.push(path);
        const paused = path.endsWith('/pause');
        const open = !path.endsWith('/end');
        stopped = !open;
        execution = open
          ? { session_ref: session, timing_material_state_ref: state, paused }
          : null;
        await route.fulfill({
          json: {
            session_ref: session,
            subject_native_ref: activity,
            timing_material_state_ref: state,
            planned_schedule_ref: schedule,
            started_at: now,
            ended_at: open ? null : now,
            paused,
            open,
            replayed: false,
            evaluated_at: now,
            elapsed_seconds: 0,
            active_seconds: 0,
            paused_seconds: 0,
            duration_evaluations: [],
          },
        });
      } else await route.fulfill({ json: [] });
    });
    await page.goto('/tests-browser/session-panel/index.html');
    const panel = page.getByRole('complementary', {
      name: 'Sessioni disponibili',
    });
    await expect(panel).toBeVisible();
    const timeline = page.locator('[data-home-region="timeline"]');
    const box = await panel.boundingBox();
    const parent = await timeline.boundingBox();
    expect(box).not.toBeNull();
    expect(parent).not.toBeNull();
    expect(box!.x).toBeGreaterThanOrEqual(parent!.x);
    expect(box!.x + box!.width).toBeLessThanOrEqual(
      Math.min(width, parent!.x + parent!.width),
    );
    expect(
      Math.abs(box!.x + box!.width - (parent!.x + parent!.width - 12)),
    ).toBeLessThanOrEqual(2);
    // Closing and reopening is independent from the top toolbar icon.
    await panel
      .getByRole('button', { name: 'Chiudi pannello sessioni' })
      .click();
    const toggle = page.getByRole('button', {
      name: 'Sessioni disponibili · 1',
    });
    await expect(toggle).toBeFocused();
    await expect(panel).toHaveCount(0);
    await toggle.press('Enter');
    await expect(panel).toBeVisible();
    await panel.getByRole('button', { name: 'Avvia · Ripasso' }).click();
    await panel.getByRole('button', { name: 'Pausa · Ripasso' }).click();
    await panel.getByRole('button', { name: 'Riprendi · Ripasso' }).click();
    await panel.getByRole('button', { name: 'Termina · Ripasso' }).click();
    await expect(panel).toHaveCount(0);
    await expect(toggle).toHaveCount(0);
    expect(commands).toHaveLength(4);
    await page.screenshot({
      path: testInfo.outputPath(`session-panel-${width}.png`),
      fullPage: true,
    });
  });
}
