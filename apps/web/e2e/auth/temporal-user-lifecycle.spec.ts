import {
  expect,
  test,
  type Locator,
  type Page,
  type Response as PlaywrightResponse,
} from '@playwright/test';
import { Temporal } from '@dante/time';

import {
  configureCreate,
  create,
  dateAfter,
  openCreate,
  openHome,
  openInspector,
  scenarioDate,
  serverRead,
  signedInPage,
  submitCreate,
  uniqueTitle,
  type Cadence,
  type CreatedItem,
  type Subject,
} from './temporal-user-journey-support';

/**
 * Stateful real-user journeys. Production UI -> authenticated HTTP -> real
 * PostgreSQL -> reload is required; the isolated /home fixture is insufficient.
 * Each test owns one disposable seeded E2E account and its own created data.
 */
/** HTTP 200 is not sufficient when the browser response body never finishes.
 * Keep that failure explicit and bounded instead of consuming the entire
 * 120-second user journey budget on an unresolved response.json().
 */
async function boundedJsonResponse(
  response: PlaywrightResponse,
  timeoutMs = 12_000,
): Promise<Record<string, unknown>> {
  let timeout: ReturnType<typeof setTimeout> | undefined;
  try {
    return (await Promise.race([
      response.json(),
      new Promise<never>((_resolve, reject) => {
        timeout = setTimeout(() => {
          reject(
            new Error(
              `HTTP ${response.status()} body did not finish within ${timeoutMs} ms: ${response.url()}`,
            ),
          );
        }, timeoutMs);
      }),
    ])) as Record<string, unknown>;
  } finally {
    if (timeout !== undefined) clearTimeout(timeout);
  }
}

test.describe('Timeline — real user Activity/Event lifecycle matrix', () => {
  // Seven independent seeded users: allow this suite (and only this suite)
  // to run concurrently when Playwright is invoked with --workers=2.
  test.describe.configure({ mode: 'parallel', timeout: 300_000 });

  // Home renders a multi-day viewport. A card visible after navigating to
  // another day does not belong to that day. Match the source planned date.
  function onDay(page: Page, day: string, title: string): Locator {
    return page
      .locator('[data-timeline-event][data-planned-date="' + day + '"]')
      .filter({ hasText: title });
  }

  function scheduleOnDay(page: Page, day: string, scheduleRef: string): Locator {
    return page.locator(
      '[data-timeline-event="' + scheduleRef + '"][data-planned-date="' + day + '"]',
    );
  }

  async function titleEditor(inspector: Locator, kind: Subject): Promise<Locator> {
    await inspector.getByRole('button', { name: 'Modifica', exact: true }).click();
    const input = inspector.getByRole('textbox', {
      name: kind === 'event' ? 'Titolo Event' : 'Titolo',
    });
    await expect(input).toBeVisible();
    return input;
  }

  async function assertPersistedTitle(
    page: Page,
    item: CreatedItem,
    expected: string,
  ): Promise<void> {
    const url = item.kind === 'activity'
      ? '/api/v1/temporal/activities/' + item.sourceRef + '/profile'
      : '/api/v1/temporal/events/' + item.sourceRef;
    await expect
      .poll(async () => {
        const response = await page.request.get(url, {
          headers: { 'X-Dante-Time-Zone': 'Europe/Rome' },
        });
        if (response.status() !== 200) return 'HTTP ' + response.status();
        const persisted = (await response.json()) as Record<string, unknown>;
        return persisted.title;
      }, { timeout: 20_000 })
      .toBe(expected);
  }

  async function duplicateFromInspector(
    page: Page,
    item: CreatedItem,
    targetTitle: string,
  ): Promise<CreatedItem> {
    const inspector = await openInspector(page, item);
    await inspector.getByRole('button', { name: 'Duplica' }).click();
    const composer = page.locator('[data-temporal-create="composer"]');
    await expect(composer).toBeVisible();
    // The new draft must be independent, not a second alias to the source.
    await composer.getByRole('textbox', { name: 'Titolo' }).fill(targetTitle);
    const duplicated = await submitCreate(page, composer, {
      kind: item.kind,
      title: targetTitle,
      recurring: false,
    });
    expect(duplicated.sourceRef).not.toBe(item.sourceRef);
    expect(duplicated.scheduleRef).not.toBe(item.scheduleRef);
    return duplicated;
  }

  async function deleteOneOff(
    page: Page,
    item: CreatedItem,
  ): Promise<void> {
    const inspector = await openInspector(page, item);
    await inspector.getByRole('button', {
      name: item.kind === 'event' ? 'Elimina Event' : 'Elimina',
      exact: true,
    }).click();
    // The shared destructive confirmation is portaled to document.body.
    // It is an alertdialog, never a button nested under the Inspector.
    const deletion = page.getByRole('alertdialog', {
      name: item.kind === 'event' ? 'Elimina evento' : 'Elimina attività',
    });
    await expect(
      deletion.getByRole('button', { name: 'Elimina definitivamente' }),
    ).toBeVisible();
    await deletion.getByRole('button', { name: 'Annulla', exact: true }).click();
    await expect(deletion).toHaveCount(0);
    await expect(
      page.locator('[data-timeline-event="' + item.scheduleRef + '"]'),
    ).toHaveCount(1);
    // Cancelling must preserve persisted profile, not merely a stale card.
    await assertPersistedTitle(page, item, item.title);

    await inspector.getByRole('button', {
      name: item.kind === 'event' ? 'Elimina Event' : 'Elimina',
      exact: true,
    }).click();
    const endpoint = item.kind === 'event'
      ? '/api/v1/temporal/hard-deletion/' + item.sourceRef
      : '/api/v1/temporal/activities/' + item.sourceRef;
    const responsePromise = page.waitForResponse(
      (response) =>
        response.url().endsWith(endpoint) &&
        response.request().method() === 'DELETE',
    );
    await expect(deletion).toBeVisible();
    await deletion.getByRole('button', {
      name: 'Elimina definitivamente',
    }).click();
    const accepted = await responsePromise;
    // The UI can navigate immediately after deletion, which makes the
    // response body unavailable in Playwright even after a successful 200.
    // Assert status here and verify persistence through the fresh read below.
    expect(accepted.status(), `${item.kind} destructive command`).toBe(200);
    // Finish the UI's onDeleted transition before a new page navigation.
    await expect(deletion).toHaveCount(0);
    await expect(inspector).toHaveCount(0);
  }

  for (const [slot, kind] of [
    [1, 'activity'],
    [2, 'event'],
  ] as const) {
    test('one-off ' + kind + ': Create → Edit → Duplica → Elimina → reload', async ({
      browser,
    }, testInfo) => {
      const user = await signedInPage(browser, testInfo, slot);
      try {
        const { page } = user;
        const day = scenarioDate();
        await openHome(page, day);
        const initialTitle = uniqueTitle(kind + ' semplice');
        const original = await create(page, {
          kind,
          title: initialTitle,
          date: day,
          clock: kind === 'event' ? '10:20' : '09:10',
        });
        expect(original.scheduleRef).not.toBeNull();
        await openHome(page, day);
        const inspector = await openInspector(page, original);
        const editedTitle = uniqueTitle(kind + ' aggiornato');
        await (await titleEditor(inspector, kind)).fill(editedTitle);
        await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
        await assertPersistedTitle(page, original, editedTitle);

        await openHome(page, day);
        const edited = { ...original, title: editedTitle };
        const copiedTitle = uniqueTitle(kind + ' duplicato');
        const duplicate = await duplicateFromInspector(page, edited, copiedTitle);
        await openHome(page, day);
        await assertPersistedTitle(page, duplicate, copiedTitle);
        await deleteOneOff(page, edited);

        await openHome(page, day);
        await expect(
          page.locator('[data-timeline-event="' + original.scheduleRef + '"]'),
        ).toHaveCount(0);
        await expect(
          page.locator('[data-timeline-event="' + duplicate.scheduleRef + '"]'),
        ).toHaveCount(1);
        await assertPersistedTitle(page, duplicate, copiedTitle);
        const deletedRead = await page.request.get(
          kind === 'activity'
            ? '/api/v1/temporal/activities/' + original.sourceRef + '/profile'
            : '/api/v1/temporal/events/' + original.sourceRef,
          { headers: { 'X-Dante-Time-Zone': 'Europe/Rome' } },
        );
        expect(deletedRead.status()).toBe(404);
        // Navigating to day+1 keeps day-0 cards in the multi-day
        // viewport; their planned date must remain day, never day+1.
        await openHome(page, dateAfter(day, 1));
        await expect(
          scheduleOnDay(page, dateAfter(day, 1), original.scheduleRef!),
        ).toHaveCount(0);
        await expect(
          scheduleOnDay(page, dateAfter(day, 1), duplicate.scheduleRef!),
        ).toHaveCount(0);
        await openHome(page, day);
        await expect(
          scheduleOnDay(page, day, original.scheduleRef!),
        ).toHaveCount(0);
        await expect(
          scheduleOnDay(page, day, duplicate.scheduleRef!),
        ).toHaveCount(1);
        await assertPersistedTitle(page, duplicate, copiedTitle);
      } finally {
        await user.close();
      }
    });
  }

  type Variant = Readonly<{
    cadence: Cadence;
    interval: number;
    allDay?: boolean;
    complex?: boolean;
    monthlyOrdinal?: boolean;
    repeatCount?: number;
  }>;

  const activityVariants: readonly Variant[] = [
    { cadence: 'daily', interval: 1, complex: true },
    { cadence: 'weekly', interval: 2 },
    { cadence: 'monthly', interval: 1 },
    { cadence: 'monthly', interval: 1, monthlyOrdinal: true },
    { cadence: 'yearly', interval: 1 },
    { cadence: 'custom', interval: 3, repeatCount: 4 },
  ];
  const eventVariants: readonly Variant[] = [
    { cadence: 'daily', interval: 1, complex: true },
    { cadence: 'weekly', interval: 1 },
    { cadence: 'monthly', interval: 2, allDay: true },
    { cadence: 'monthly', interval: 1, monthlyOrdinal: true },
    { cadence: 'yearly', interval: 1 },
    { cadence: 'custom', interval: 2, repeatCount: 3 },
  ];

  for (const [slot, kind, variants] of [
    [3, 'activity', activityVariants],
    [4, 'event', eventVariants],
  ] as const) {
    test('recurring ' + kind + ': multi-frequency Create + advanced policies + reload', async ({
      browser,
    }, testInfo) => {
      const user = await signedInPage(browser, testInfo, slot);
      try {
        const { page } = user;
        const day = scenarioDate();
        await openHome(page, day);
        const created: CreatedItem[] = [];
        let dailyLifeArea: string | null = null;
        for (const [index, variant] of variants.entries()) {
          const label = uniqueTitle(kind + ' ' + variant.cadence);
          const options = {
            kind,
            title: label,
            date: day,
            clock: [
              '08:10', '10:10', '12:10', '14:10', '16:10', '18:10',
            ][index] ?? '09:10',
            recurrence: variant.cadence,
            interval: variant.interval,
            ...(variant.monthlyOrdinal ? { monthlyOrdinal: true } : {}),
            ...(variant.repeatCount ? { repeatCount: variant.repeatCount } : {}),
            ...(variant.allDay ? { allDay: true } : {}),
            ...(variant.complex && kind === 'activity'
              ? {
                  plannedSession: 'Studio approfondito',
                  objective: 'Risultato verificato',
                  objectiveQuantity: 5,
                  lifeArea: uniqueTitle('area studio'),
                  placementProtected: true,
                }
              : {}),
            ...(variant.complex && kind === 'event'
              ? {
                  agenda: 'Introduzione partecipanti',
                  objective: 'Presenza confermata',
                  lifeArea: uniqueTitle('area eventi'),
                  placementProtected: true,
                }
              : {}),
          } as const;
          if (index === 0) dailyLifeArea = options.lifeArea ?? null;
          const dialog = await openCreate(page, kind);
          await configureCreate(dialog, options);
          const panel = dialog.getByRole('region', {
            name: 'Ripetizione',
            exact: true,
          });
          // Non-unit intervals are accurately represented as Custom in
          // the compact selector; the full payload must still preserve the
          // chosen frequency and exact interval.
          await expect(panel.getByRole('combobox', { name: 'Ripeti' }))
            .toHaveValue(
              variant.monthlyOrdinal || variant.interval !== 1
                ? 'custom'
                : variant.cadence,
            );
          const createdPromise = page.waitForResponse(
            (response) =>
              response.url().endsWith(
                kind === 'activity'
                  ? '/api/v1/temporal/recurring/routines'
                  : '/api/v1/temporal/recurring/events',
              ) && response.request().method() === 'POST',
          );
          const saving = submitCreate(page, dialog, {
            kind,
            title: label,
            recurring: true,
          });
          const response = await createdPromise;
          expect(response.ok()).toBe(true);
          const request = response.request().postDataJSON() as {
            recurrence: Record<string, unknown>;
          };
          const patternCode = variant.monthlyOrdinal
            ? 'monthly_ordinal_weekdays'
            : variant.cadence === 'weekly' || variant.cadence === 'custom'
              ? 'weekly_weekdays'
              : variant.cadence === 'monthly'
                ? 'monthly_month_days'
                : variant.cadence === 'yearly'
                  ? 'yearly_month_days'
                  : 'daily';
          expect(request.recurrence).toMatchObject({
            pattern_code: patternCode,
            interval_count: variant.interval,
            effective_from: day,
            clock_basis_code: 'named_zone',
            ...(variant.monthlyOrdinal
              ? {
                  ordinal_weekdays: [
                    {
                      weekday_number: Temporal.PlainDate.from(day).dayOfWeek,
                      ordinal:
                        Math.ceil(Temporal.PlainDate.from(day).day / 7) === 5
                          ? -1
                          : Math.ceil(Temporal.PlainDate.from(day).day / 7),
                    },
                  ],
                }
              : {}),
            ...(variant.repeatCount
              ? {
                  range_kind: 'expected_count',
                  expected_occurrence_count: variant.repeatCount,
                }
              : {}),
          });
          created.push(await saving);
        }
        await openHome(page, day);
        const allRefs = new Set(created.map((item) => item.sourceRef));
        expect(allRefs.size).toBe(variants.length);
        // Independent, versioned series are visible after a fresh Timeline GET.
        for (const [index, item] of created.entries()) {
          const variant = variants[index]!;
          // A scheduled all-day Event is displayed in the civil-date lane,
          // not the timed grid. Both representations must still be visible.
          const card = variant.allDay
            ? page.locator('[data-timeline-all-day-lane="' + day + '"]')
                .locator('[data-timeline-all-day-item]')
                .filter({ hasText: item.title })
                .first()
            : page.locator('[data-timeline-event]').filter({
                hasText: item.title,
              }).first();
          await expect(
            card,
            `Missing ${kind} recurrence on the materialized Timeline: ${JSON.stringify({
              title: item.title,
              cadence: variant.cadence,
              interval: variant.interval,
              allDay: variant.allDay ?? false,
              monthlyOrdinal: variant.monthlyOrdinal ?? false,
              effectiveDate: day,
              sourceRef: item.sourceRef,
            })}`,
          ).toBeVisible();
        }
        const dailyFirst = onDay(page, day, created[0]!.title);
        await expect(dailyFirst).toHaveCount(1);
        if (dailyLifeArea !== null) {
          await expect(
            dailyFirst.locator('.timeline-event-card__meta'),
          ).toContainText(dailyLifeArea);
        }
        // A second Timeline checkpoint on the next calendar day must keep
        // the daily source and its inherited Life Area consistent.
        await openHome(page, dateAfter(day, 1));
        const dailyFuture = onDay(page, dateAfter(day, 1), created[0]!.title);
        await expect(dailyFuture).toHaveCount(1);
        if (dailyLifeArea !== null) {
          await expect(
            dailyFuture.locator('.timeline-event-card__meta'),
          ).toContainText(dailyLifeArea);
        }
        const dailyFutureSchedule = await dailyFuture.getAttribute(
          'data-timeline-event',
        );
        expect(dailyFutureSchedule).toMatch(/^[\da-f-]{36}$/i);
        if (created[0]!.scheduleRef) {
          expect(dailyFutureSchedule).not.toBe(created[0]!.scheduleRef);
        }
        await openHome(page, day);
        await expect(onDay(page, day, created[0]!.title)).toHaveCount(1);
        await openHome(page, dateAfter(day, 1));
        await expect(
          onDay(page, dateAfter(day, 1), created[0]!.title),
        ).toHaveAttribute('data-timeline-event', dailyFutureSchedule!);
        if (kind === 'activity') {
          const routines = (await serverRead(
            page,
            '/api/v1/temporal/routines',
          )) as Array<Record<string, unknown>>;
          for (const item of created) {
            expect(routines).toContainEqual(
              expect.objectContaining({
                routine_ref: item.sourceRef,
                title: item.title,
              }),
            );
          }
        }
      } finally {
        await user.close();
      }
    });
  }

  test('standalone Activity and Event: Edit → Ripeti → Save → first-identity + next day', async ({
    browser,
  }, testInfo) => {
    // A missing conversion POST should produce a bounded failure rather
    // than keeping this single test opaque for five minutes.
    test.setTimeout(120_000);
    const user = await signedInPage(browser, testInfo, 5);
    try {
      const { page } = user;
      const day = scenarioDate();
      await openHome(page, day);
      for (const kind of ['activity', 'event'] as const) {
        await test.step(
          `${kind}: convert once to recurring and preserve identity`,
          async () => {
            const title = uniqueTitle(kind + ' conversione');
            const original = await create(page, {
              kind,
              title,
              date: day,
              clock: kind === 'activity' ? '08:20' : '15:20',
              placementProtected: true,
            });
            await openHome(page, day);
            const inspector = await openInspector(page, original);
            await titleEditor(inspector, kind);
            const panel = inspector.getByRole('region', {
              name: 'Ripetizione',
              exact: true,
            });
            await panel.getByRole('combobox', { name: 'Ripeti' })
              .selectOption('daily');
            await expect(panel).toHaveAttribute('data-recurrence-expanded', 'true');
            if (kind === 'activity') {
              // Before conversion this physical Activity has no Occurrence.
              const initial = (await serverRead(
                page,
                '/api/v1/temporal/activities/' +
                  original.sourceRef +
                  '/recurrence-origin',
              )) as { activity_ref: string; occurrence_ref: string | null };
              expect(initial).toMatchObject({
                activity_ref: original.sourceRef,
                occurrence_ref: null,
              });
            }
            const startPath =
              '/api/v1/temporal/recurring/' +
              (kind === 'event' ? 'events/' : 'activities/') +
              original.sourceRef + '/start';
            const conversion = page.waitForResponse(
              (response) =>
                response.url().endsWith(startPath) &&
                response.request().method() === 'POST',
              { timeout: 35_000 },
            );
            await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
            const accepted = await conversion;
            expect(accepted.status()).toBe(200);
            if (kind === 'event') {
              // Event production client consumes the accepted JSON.
              const body = await boundedJsonResponse(accepted);
              expect(body).toMatchObject({ owner_kind: 'event', replayed: false });
              expect(body.source_ref).toEqual(
                expect.stringMatching(/^[\da-f-]{36}$/i),
              );
            } else {
              // Activity production client intentionally does not consume
              // response.json(). Chrome can discard the response body after
              // the component closes even though the HTTP command succeeds.
              // Prove the canonical persisted Occurrence association instead.
              await expect
                .poll(async () => {
                  const origin = (await serverRead(
                    page,
                    '/api/v1/temporal/activities/' +
                      original.sourceRef +
                      '/recurrence-origin',
                  )) as { activity_ref: string; occurrence_ref: string | null };
                  expect(origin.activity_ref).toBe(original.sourceRef);
                  return origin.occurrence_ref;
                }, { timeout: 12_000 })
                .toMatch(/^[\da-f-]{36}$/i);
            }
            const intent = accepted.request().postDataJSON() as Record<string, unknown>;
            expect(intent.recurrence).toMatchObject({
              pattern_code: 'daily',
              effective_from: day,
              clock_basis_code: 'named_zone',
            });
            await openHome(page, day);
            await expect(
              page.locator('[data-timeline-event="' + original.scheduleRef + '"]'),
            ).toHaveCount(1);
            await assertPersistedTitle(page, original, title);
            await openHome(page, dateAfter(day, 1));
            const future = onDay(page, dateAfter(day, 1), title);
            await expect(future).toHaveCount(1);
            const firstFutureSchedule = await future.getAttribute(
              'data-timeline-event',
            );
            expect(firstFutureSchedule).toMatch(/^[\da-f-]{36}$/i);
            expect(firstFutureSchedule).not.toBe(original.scheduleRef);

            await openHome(page, dateAfter(day, 2));
            const later = onDay(page, dateAfter(day, 2), title);
            await expect(later).toHaveCount(1);
            const secondFutureSchedule = await later.getAttribute(
              'data-timeline-event',
            );
            expect(secondFutureSchedule).not.toBe(firstFutureSchedule);
            expect(secondFutureSchedule).not.toBe(original.scheduleRef);

            // After materializing later Occurrences, revisit both earlier dates:
            // the first physical identity and accepted future identities must not
            // be replaced or rewritten by checkpoint/reconciliation.
            await openHome(page, day);
            await expect(onDay(page, day, title))
              .toHaveAttribute('data-timeline-event', original.scheduleRef!);
            await assertPersistedTitle(page, original, title);
            await openHome(page, dateAfter(day, 1));
            await expect(onDay(page, dateAfter(day, 1), title))
              .toHaveAttribute('data-timeline-event', firstFutureSchedule!);
          },
        );
      }
    } finally {
      await user.close();
    }
  });

  test('recurring Activity: instance-only Edit, following-series Edit and delete choices', async ({
    browser,
  }, testInfo) => {
    const user = await signedInPage(browser, testInfo, 6);
    try {
      const { page } = user;
      const day = scenarioDate();
      await openHome(page, day);
      const title = uniqueTitle('serie modificabile');
      await create(page, {
        kind: 'activity',
        title,
        date: day,
        recurrence: 'daily',
        clock: '11:20',
      });
      await openHome(page, day);
      const card = onDay(page, day, title);
      await expect(card).toBeVisible();
      await card.getByRole('button', { name: title, exact: true }).click();
      let inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      const chooseScope = page.getByRole('dialog', { name: 'Modifica ricorrenza' });
      await expect(chooseScope).toBeVisible();
      await chooseScope.getByRole('button', { name: 'Solo questa istanza' }).click();
      await expect(
        inspector.getByRole('region', { name: 'Ripetizione' }),
      ).toHaveCount(0);
      const local = inspector.getByRole('textbox', { name: 'Titolo' });
      await expect(local).toBeVisible();
      const changedTitle = title + ' locale';
      await local.fill(changedTitle);
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();

      await openHome(page, day);
      await expect(onDay(page, day, changedTitle)).toHaveCount(1);
      await openHome(page, dateAfter(day, 1));
      // Local mutation must not propagate to a clean following instance.
      await expect(onDay(page, dateAfter(day, 1), changedTitle))
        .toHaveCount(0);
      // A later checkpoint must not propagate a local exception through the
      // entire series or mutate another date's stored profile.
      await openHome(page, dateAfter(day, 2));
      await expect(onDay(page, dateAfter(day, 2), changedTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 1));
      const following = onDay(page, dateAfter(day, 1), title);
      await expect(following).toBeVisible();
      await following.getByRole('button', { name: title, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      const scope = page.getByRole('dialog', { name: 'Modifica ricorrenza' });
      await scope.getByRole('button', {
        name: 'Questa e le successive',
      }).click();
      const panel = inspector.getByRole('region', {
        name: 'Ripetizione',
        exact: true,
      });
      await expect(panel).toHaveAttribute('data-recurrence-expanded', 'true');
      const seriesTitle = title + ' futuro';
      await inspector.getByRole('textbox', { name: 'Titolo' }).fill(seriesTitle);
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
      const confirmation = page.getByRole('dialog', {
        name: 'Controlla prima di salvare',
      });
      await expect(confirmation).toBeVisible();
      // Navigation before the accepted server command can abort the POST and
      // produce a false negative: wait for authoritative persistence first.
      const acceptedSeries = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/occurrences/') &&
          response.url().endsWith('/series-edit') &&
          response.request().method() === 'POST',
      );
      await confirmation.getByRole('button', {
        name: 'Conferma salvataggio',
      }).click();
      const seriesResponse = await acceptedSeries;
      expect(
        seriesResponse.status(),
        `Series revision rejected: ${await seriesResponse.text()}`,
      ).toBe(200);
      await expect(confirmation).toHaveCount(0);
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), seriesTitle))
        .toHaveCount(1);
      await openHome(page, day);
      await expect(onDay(page, day, changedTitle)).toHaveCount(1);
      await expect(onDay(page, day, seriesTitle)).toHaveCount(0);
      await openHome(page, dateAfter(day, 1));

      const current = onDay(page, dateAfter(day, 1), seriesTitle);
      await current.getByRole('button', { name: seriesTitle, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina' }).click();
      // Both scoped destructive choices must be explicit and cancellable.
      const deletion = page.getByRole('alertdialog', {
        name: 'Elimina attività',
      });
      await expect(
        deletion.getByRole('button', { name: 'Solo questa istanza' }),
      ).toBeVisible();
      await expect(
        deletion.getByRole('button', { name: 'Tutta la serie' }),
      ).toBeVisible();
      await deletion.getByRole('button', { name: 'Annulla' }).click();
      await expect(deletion).toHaveCount(0);

      await inspector.getByRole('button', { name: 'Elimina' }).click();
      const localDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await deletion.getByRole('button', { name: 'Solo questa istanza' })
        .click();
      expect((await localDelete).status()).toBe(200);
      await expect(deletion).toHaveCount(0);
      await expect(inspector).toHaveCount(0);
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), seriesTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      const future = onDay(page, dateAfter(day, 2), seriesTitle);
      await expect(future).toHaveCount(1);
      // Backtracking after materializing the next future day must never
      // resurrect the explicitly hard-deleted single Occurrence.
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), seriesTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      await future.getByRole('button', { name: seriesTitle, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina' }).click();
      const seriesDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await deletion.getByRole('button', { name: 'Tutta la serie' })
        .click();
      expect((await seriesDelete).status()).toBe(200);
      await expect(deletion).toHaveCount(0);
      await expect(inspector).toHaveCount(0);
      await openHome(page, dateAfter(day, 3));
      await expect(page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle })).toHaveCount(0);
    } finally {
      await user.close();
    }
  });
  test('recurring Event: instance-only and following edits, scoped deletion then whole-series deletion', async ({
    browser,
  }, testInfo) => {
    const user = await signedInPage(browser, testInfo, 7);
    try {
      const { page } = user;
      const day = scenarioDate();
      await openHome(page, day);
      const title = uniqueTitle('evento serie');
      await create(page, {
        kind: 'event',
        title,
        date: day,
        clock: '14:20',
        recurrence: 'daily',
        agenda: 'Ordine del giorno',
      });
      await openHome(page, day);
      const first = onDay(page, day, title);
      await expect(first).toBeVisible();
      await first.getByRole('button', { name: title, exact: true }).click();
      let inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      const scope = page.getByRole('dialog', {
        name: 'Modifica ricorrenza',
      });
      await expect(scope).toBeVisible();
      await scope.getByRole('button', { name: 'Solo questa istanza' }).click();
      await expect(inspector.getByRole('region', {
        name: 'Ripetizione', exact: true,
      })).toHaveCount(0);
      const localTitle = title + ' locale';
      await inspector.getByRole('textbox', { name: 'Titolo Event' })
        .fill(localTitle);
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();

      await openHome(page, day);
      await expect(onDay(page, day, localTitle)).toHaveCount(1);
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), localTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      await expect(onDay(page, dateAfter(day, 2), localTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 1));

      const following = onDay(page, dateAfter(day, 1), title);
      await expect(following).toBeVisible();
      await following.getByRole('button', { name: title, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Modifica' }).click();
      await page.getByRole('dialog', { name: 'Modifica ricorrenza' })
        .getByRole('button', { name: 'Questa e le successive' }).click();
      const repeat = inspector.getByRole('region', {
        name: 'Ripetizione', exact: true,
      });
      await expect(repeat).toHaveAttribute('data-recurrence-expanded', 'true');
      const seriesTitle = title + ' futuro';
      await inspector.getByRole('textbox', { name: 'Titolo' })
        .fill(seriesTitle);
      await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
      const review = page.getByRole('dialog', {
        name: 'Controlla prima di salvare',
      });
      await expect(review).toBeVisible();
      await review.getByRole('button', { name: 'Conferma salvataggio' }).click();

      await openHome(page, dateAfter(day, 1));
      const current = onDay(page, dateAfter(day, 1), seriesTitle);
      await expect(current).toHaveCount(1);
      await openHome(page, day);
      await expect(onDay(page, day, localTitle)).toHaveCount(1);
      await expect(onDay(page, day, seriesTitle)).toHaveCount(0);
      await openHome(page, dateAfter(day, 1));
      await current.getByRole('button', {
        name: seriesTitle, exact: true,
      }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina Event' }).click();
      const deletion = page.getByRole('alertdialog', {
        name: 'Elimina evento',
      });
      await expect(
        deletion.getByRole('button', { name: 'Solo questa istanza' }),
      ).toBeVisible();
      await expect(
        deletion.getByRole('button', { name: 'Tutta la serie' }),
      ).toBeVisible();
      await deletion.getByRole('button', { name: 'Annulla' }).click();
      await expect(deletion).toHaveCount(0);

      // Delete the selected generated instance without touching the source.
      await inspector.getByRole('button', { name: 'Elimina Event' }).click();
      const instanceDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await deletion.getByRole('button', {
        name: 'Solo questa istanza',
      }).click();
      expect((await instanceDelete).status()).toBe(200);
      await expect(deletion).toHaveCount(0);
      await expect(inspector).toHaveCount(0);
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), seriesTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      const future = onDay(page, dateAfter(day, 2), seriesTitle);
      await expect(future).toHaveCount(1);
      await openHome(page, dateAfter(day, 1));
      await expect(onDay(page, dateAfter(day, 1), seriesTitle))
        .toHaveCount(0);
      await openHome(page, dateAfter(day, 2));
      await future.getByRole('button', {
        name: seriesTitle, exact: true,
      }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina Event' }).click();
      const seriesDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await deletion.getByRole('button', { name: 'Tutta la serie' })
        .click();
      expect((await seriesDelete).status()).toBe(200);
      await expect(deletion).toHaveCount(0);
      await expect(inspector).toHaveCount(0);
      await openHome(page, dateAfter(day, 3));
      await expect(page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle })).toHaveCount(0);
    } finally {
      await user.close();
    }
  });

});
