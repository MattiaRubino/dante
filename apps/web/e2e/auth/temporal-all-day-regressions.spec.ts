/**
 * All-day end-to-end acceptance: real browser, authenticated API, isolated
 * PostgreSQL account per case. Do not stub Schedule/Session/Objective flows.
 * The sole deliberate API stub is the explicitly labelled renewal UI-only
 * probe; its server state transitions are covered by Python/PostgreSQL tests.
 */
import { Temporal } from '@dante/time';
import { expect, test, type Locator, type Page } from '@playwright/test';

import {
  configureCreate,
  create,
  dateAfter,
  openCreate,
  openHome,
  scenarioDate,
  serverRead,
  submitCreate,
  uniqueTitle,
  type Subject,
} from './temporal-user-journey-support';
import { signedInPersona } from './temporal-stateful-journey-support';

test.describe('All-day real-stack acceptance', () => {
  test.describe.configure({ timeout: 180_000 });
  test.use({ actionTimeout: 15_000, navigationTimeout: 20_000 });

  function lane(page: Page, day: string): Locator {
    return page.locator(
      '[data-timeline-all-day-lane="' + day + '"]',
    );
  }

  function bar(page: Page, day: string, title: string): Locator {
    return lane(page, day)
      .locator('[data-timeline-all-day-item]')
      .filter({ has: page.getByText(title, { exact: true }) });
  }

  async function extendAllDayEnd(
    composer: Locator,
    endDate: string,
  ): Promise<void> {
    const trigger = composer.getByRole('button', { name: /^Data fine:/ });
    if (await trigger.getAttribute('data-temporal-date') === endDate) return;
    await trigger.click();
    const picker = composer.getByRole('dialog', { name: 'Data fine' });
    const option = picker.locator(
      'button[data-temporal-date="' + endDate + '"]',
    );
    for (let attempt = 0; attempt < 12; attempt += 1) {
      if (await option.isVisible() && await option.isEnabled()) break;
      await picker.getByRole('button', { name: 'Mese successivo' }).click();
    }
    await expect(option, 'end date must be selectable').toBeEnabled();
    await option.click();
    await expect(trigger).toHaveAttribute('data-temporal-date', endDate);
  }

  async function authorMultiDay(
    page: Page,
    kind: Subject,
    title: string,
    start: string,
    end: string,
    enableMainSession = false,
  ) {
    const composer = await openCreate(page, kind);
    await configureCreate(composer, { kind, title, date: start, allDay: true });
    await extendAllDayEnd(composer, end);
    if (enableMainSession) {
      await composer.getByRole('button', { name: /Opzioni avanzate/ }).click();
      await expect(composer).toHaveAttribute(
        'data-temporal-create-surface',
        'advanced',
      );
      await composer
        .locator('label[data-session-capability="activity"] input[type="checkbox"]')
        .check();
    }
    return submitCreate(page, composer, { kind, title, recurring: false });
  }

  for (const [kind, ordinal] of [
    ['activity', 103],
    ['event', 104],
  ] as const) {
    test('AD-01 ' + kind + ': real all-day Save closes Inspector and reload keeps the new title', async (
      { browser }, info,
    ) => {
      const user = await signedInPersona(browser, info, ordinal);
      const { page } = user;
      const day = scenarioDate(4);
      const original = uniqueTitle(kind + ' all-day');
      const revised = original + ' aggiornato';
      try {
        await openHome(page, day);
        const created = await authorMultiDay(
          page, kind, original, day, dateAfter(day, 2),
        );
        expect(created.sourceRef).toMatch(/^[\da-f-]{36}$/i);
        await openHome(page, day);
        const initialBar = bar(page, day, original);
        await expect(initialBar).toHaveCount(1);
        await expect(initialBar).toHaveAttribute(
          'data-timeline-date-lane-kind', /^(all-day|multi-day)$/,
        );
        await expect(initialBar).toHaveAttribute('data-range-start', 'true');
        await expect(bar(page, dateAfter(day, 1), original)).toHaveCount(1);
        await expect(initialBar.locator('.timeline-all-day-item__continuation'))
          .toHaveCount(0);

        await initialBar.click();
        const inspector = page.locator('.timeline-event-modal[role="dialog"]');
        await expect(inspector).toBeVisible();
        await inspector.getByRole('button', {
          name: 'Modifica', exact: true,
        }).click();
        await inspector.getByRole('textbox', {
          name: kind === 'event' ? 'Titolo Event' : 'Titolo',
        }).fill(revised);
        await inspector.getByRole('button', {
          name: 'Salva modifiche',
        }).click();
        await expect(
          inspector,
          'successful Save must close the old Inspector, not strand it at its stale anchor',
        ).toHaveCount(0);
        await openHome(page, day);
        await expect(bar(page, day, original)).toHaveCount(0);
        await expect(bar(page, day, revised)).toHaveCount(1);
        await expect(bar(page, dateAfter(day, 1), revised)).toHaveCount(1);
        const persisted = await serverRead(
          page,
          kind === 'event'
            ? '/api/v1/temporal/events/' + created.sourceRef
            : '/api/v1/temporal/activities/' + created.sourceRef + '/profile',
        ) as { title: string };
        expect(persisted.title).toBe(revised);
      } finally {
        await user.close();
      }
    });
  }

  test('AD-02 12 bars: two visible, expansion in the same panel, bounded inner scrolling', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 105);
    const { page } = user;
    const day = scenarioDate(3);
    try {
      await openHome(page, day);
      const titles: string[] = [];
      for (let i = 0; i < 12; i += 1) {
        const title = uniqueTitle('all-day overflow ' + (i + 1));
        await create(page, { kind: 'event', title, date: day, allDay: true });
        titles.push(title);
      }
      await openHome(page, day);
      const container = lane(page, day);
      await expect(container).toBeVisible();
      await expect(
        container.locator('.timeline-all-day-lane__items .timeline-all-day-item'),
      ).toHaveCount(2);
      const toggle = container.getByRole('button', { name: 'Mostra altri 10' });
      await expect(toggle).toBeVisible();
      const collapsed = await container.boundingBox();
      expect(collapsed).not.toBeNull();
      await toggle.click();
      const additional = container.getByRole('region', { name: 'Altre barre' });
      await expect(additional).toBeVisible();
      await expect(additional.locator('.timeline-all-day-item')).toHaveCount(10);
      const expanded = await container.boundingBox();
      expect(expanded).not.toBeNull();
      expect(Math.round(expanded!.height - collapsed!.height)).toBe(252);
      const sizes = await additional.evaluate((element) => ({
        client: element.clientHeight,
        scroll: element.scrollHeight,
        overflowing: getComputedStyle(element).overflowY,
      }));
      expect(sizes.scroll).toBeGreaterThan(sizes.client);
      expect(sizes.overflowing).toBe('auto');
      await additional.evaluate((element) => { element.scrollTop = element.scrollHeight; });
      await expect(bar(page, day, titles[11]!)).toHaveCount(1);
      await container.getByRole('button', {
        name: 'Nascondi altri elementi',
      }).click();
      await expect(additional).toHaveCount(0);
      const closed = await container.boundingBox();
      expect(Math.round(closed!.height)).toBe(Math.round(collapsed!.height));
    } finally {
      await user.close();
    }
  });

  test('AD-03 main Activity Session Stop removes subsequent all-day bars, not recorded reality', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 106);
    const { page } = user;
    const day = Temporal.Now.plainDateISO('Europe/Rome').toString();
    const title = uniqueTitle('main all-day stop');
    try {
      await openHome(page, day);
      const created = await authorMultiDay(
        page, 'activity', title, day, dateAfter(day, 3), true,
      );
      await openHome(page, day);
      const item = bar(page, day, title);
      await expect(item).toHaveCount(1);
      const row = item.locator('xpath=..');
      const start = row.getByRole('button', { name: 'Avvia' });
      await expect(start).toBeEnabled();
      await start.click();
      const stop = row.getByRole('button', { name: 'Termina' });
      await expect(stop).toBeEnabled();
      const stopped = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        /\/api\/v1\/temporal\/sessions\/[^/]+\/end$/.test(
          new URL(response.url()).pathname,
        ),
      );
      await stop.click();
      expect((await stopped).ok()).toBe(true);
      const sessions = await serverRead(
        page, '/api/v1/temporal/activities/' + created.sourceRef + '/sessions',
      ) as Array<{ open: boolean; started_at: string; ended_at: string | null }>;
      expect(sessions.some((record) => !record.open && record.ended_at !== null))
        .toBe(true);
      await openHome(page, day);
      await expect(bar(page, day, title)).toHaveCount(1);
      await openHome(page, dateAfter(day, 1));
      await expect(bar(page, dateAfter(day, 1), title)).toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      await expect(bar(page, dateAfter(day, 2), title)).toHaveCount(0);
    } finally {
      await user.close();
    }
  });

  test('AD-04 all-day Activity keeps Objective and planned Session after real reload', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 107);
    const { page } = user;
    const day = scenarioDate(5);
    const title = uniqueTitle('all-day objective');
    const objective = uniqueTitle('obiettivo');
    const session = uniqueTitle('sessione');
    try {
      await openHome(page, day);
      const item = await create(page, {
        kind: 'activity', title, date: day, allDay: true,
        objective, objectiveQuantity: 3, plannedSession: session,
      });
      await openHome(page, day);
      await expect(bar(page, day, title)).toHaveCount(1);
      const goals = await serverRead(
        page, '/api/v1/temporal/activities/' + item.sourceRef + '/objectives',
      ) as Array<{ title?: string; label?: string; observation_ref?: string | null }>;
      expect(goals).toHaveLength(1);
      expect(JSON.stringify(goals[0])).toContain(objective);
      expect(goals[0]?.observation_ref ?? null).toBeNull();
      const details = await serverRead(
        page, '/api/v1/temporal/activities/' + item.sourceRef + '/children',
      ) as Record<string, unknown>;
      expect(JSON.stringify(details)).toContain(session);
      await openHome(page, day);
      await expect(bar(page, day, title)).toHaveCount(1);
    } finally {
      await user.close();
    }
  });

  test('AD-05 Dopo all-day 3 occurrences: Activity/Event stop at final authorized date', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 108);
    const { page } = user;
    const day = scenarioDate(6);
    try {
      await openHome(page, day);
      for (const kind of ['activity', 'event'] as const) {
        const title = uniqueTitle('all-day Dopo ' + kind);
        const composer = await openCreate(page, kind);
        await configureCreate(composer, {
          kind, title, date: day, allDay: true,
          recurrence: 'daily', repeatCount: 3,
        });
        const count = composer.getByRole('spinbutton', {
          name: 'Numero di occorrenze',
        });
        await count.fill('9999');
        await expect(count).toHaveValue('730');
        await count.fill('3');
        await submitCreate(page, composer, { kind, title, recurring: true });
        await openHome(page, day);
        await expect(bar(page, day, title)).toHaveCount(1);
        await openHome(page, dateAfter(day, 1));
        await expect(bar(page, dateAfter(day, 1), title)).toHaveCount(1);
        await openHome(page, dateAfter(day, 2));
        await expect(bar(page, dateAfter(day, 2), title)).toHaveCount(1);
        await openHome(page, dateAfter(day, 3));
        await expect(bar(page, dateAfter(day, 3), title)).toHaveCount(0);
      }
    } finally {
      await user.close();
    }
  });

  test('AD-06 renewal notice UI 30 -> 29, multiple series and conflict is isolated from backend', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 109);
    const { page } = user;
    const day = scenarioDate(3);
    let remaining = 30;
    let simulatedConflict = true;
    const notices = () => [
      {
        owner: 'routine', source_ref: '00000000-0000-4000-8000-000000000011',
        title: 'Serie di prova Activity',
        material_state_ref: '00000000-0000-4000-8000-000000000021',
        allowed_count: 730, remaining_count: remaining, revision: 12,
      },
      {
        owner: 'event', source_ref: '00000000-0000-4000-8000-000000000012',
        title: 'Serie di prova Event',
        material_state_ref: '00000000-0000-4000-8000-000000000022',
        allowed_count: 730, remaining_count: 1, revision: 5,
      },
    ];
    try {
      await page.route('**/api/v1/temporal/open-recurrence-allowances', async (route) => {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify(notices()),
        });
      });
      await page.route('**/api/v1/temporal/open-recurrence-allowances/**/decision', async (route) => {
        await route.fulfill({
          status: simulatedConflict ? 409 : 200,
          contentType: 'application/json',
          body: '{}',
        });
      });
      await openHome(page, day);
      const trigger = page.getByRole('button', { name: 'Serie da rinnovare: 2' });
      await expect(trigger).toBeVisible();
      await expect(trigger).toHaveCSS('width', '44px');
      await expect(trigger.locator('svg')).toHaveCSS('width', '21px');
      await expect(trigger.locator('.timeline-renewals__badge')).toHaveCSS(
        'height',
        '19px',
      );
      await trigger.click();
      const panel = page.locator('.timeline-renewals__panel');
      await expect(panel).toContainText('30 occorrenze rimaste su 730');
      await expect(panel).toContainText('1 occorrenze rimaste su 730');
      await panel.locator('section').first()
        .getByRole('button', { name: 'Continua' }).click();
      await expect(panel.getByRole('alert'))
        .toContainText('La serie è cambiata');
      remaining = 29;
      simulatedConflict = false;
      await openHome(page, day);
      await expect(page.getByRole('button', { name: 'Serie da rinnovare: 2' }))
        .toBeVisible();
      await page.getByRole('button', { name: 'Serie da rinnovare: 2' }).click();
      await expect(page.locator('.timeline-renewals__panel'))
        .toContainText('29 occorrenze rimaste su 730');
      remaining = 0;
      await openHome(page, day);
      await page.getByRole('button', { name: 'Serie da rinnovare: 2' }).click();
      await expect(page.locator('.timeline-renewals__panel'))
        .toContainText('0 occorrenze rimaste su 730');
    } finally {
      await user.close();
    }
  });
});
