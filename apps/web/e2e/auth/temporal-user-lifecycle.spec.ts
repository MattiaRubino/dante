import { expect, test, type Locator, type Page } from '@playwright/test';

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
test.describe('Timeline — real user Activity/Event lifecycle matrix', () => {
  test.describe.configure({ timeout: 300_000 });

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
    expect(accepted.status()).toBe(200);
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
        // Advancing the Timeline and checkpointing a later day must never
        // regenerate a deleted one-off or move an unrelated duplicate.
        await openHome(page, dateAfter(day, 1));
        await expect(
          page.locator('[data-timeline-event="' + original.scheduleRef + '"]'),
        ).toHaveCount(0);
        await expect(
          page.locator('[data-timeline-event="' + duplicate.scheduleRef + '"]'),
        ).toHaveCount(0);
        await openHome(page, day);
        await expect(
          page.locator('[data-timeline-event="' + original.scheduleRef + '"]'),
        ).toHaveCount(0);
        await expect(
          page.locator('[data-timeline-event="' + duplicate.scheduleRef + '"]'),
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
          const dialog = await openCreate(page, kind);
          await configureCreate(dialog, options);
          const panel = dialog.getByRole('region', {
            name: 'Ripetizione',
            exact: true,
          });
          await expect(panel.getByRole('combobox', { name: 'Ripeti' }))
            .toHaveValue(variant.monthlyOrdinal ? 'custom' : variant.cadence);
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
        for (const item of created) {
          await expect(
            page.locator('[data-timeline-event]').filter({
              hasText: item.title,
            }).first(),
          ).toBeVisible();
        }
        // A second Timeline checkpoint on the next calendar day must keep
        // the daily source consistent and must not create duplicate cards.
        await openHome(page, dateAfter(day, 1));
        const dailyFuture = page.locator('[data-timeline-event]').filter({
          hasText: created[0]!.title,
        });
        await expect(dailyFuture).toHaveCount(1);
        const dailyFutureSchedule = await dailyFuture.getAttribute(
          'data-timeline-event',
        );
        expect(dailyFutureSchedule).toMatch(/^[\da-f-]{36}$/i);
        if (created[0]!.scheduleRef) {
          expect(dailyFutureSchedule).not.toBe(created[0]!.scheduleRef);
        }
        await openHome(page, day);
        await expect(
          page.locator('[data-timeline-event]').filter({
            hasText: created[0]!.title,
          }),
        ).toHaveCount(1);
        await openHome(page, dateAfter(day, 1));
        await expect(
          page.locator('[data-timeline-event="' + dailyFutureSchedule + '"]'),
        ).toHaveCount(1);
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
    const user = await signedInPage(browser, testInfo, 5);
    try {
      const { page } = user;
      const day = scenarioDate();
      await openHome(page, day);
      for (const kind of ['activity', 'event'] as const) {
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
        const startPath =
          '/api/v1/temporal/recurring/' +
          (kind === 'event' ? 'events/' : 'activities/') +
          original.sourceRef + '/start';
        const conversion = page.waitForResponse(
          (response) =>
            response.url().endsWith(startPath) &&
            response.request().method() === 'POST',
        );
        await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
        const accepted = await conversion;
        expect(accepted.status()).toBe(200);
        const body = (await accepted.json()) as Record<string, unknown>;
        expect(body).toMatchObject({
          owner_kind: kind === 'event' ? 'event' : 'routine',
          replayed: false,
        });
        expect(body.source_ref).toEqual(expect.stringMatching(/^[\da-f-]{36}$/i));
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
        const future = page.locator('[data-timeline-event]').filter({
          hasText: title,
        });
        await expect(future).toHaveCount(1);
        const firstFutureSchedule = await future.getAttribute(
          'data-timeline-event',
        );
        expect(firstFutureSchedule).toMatch(/^[\da-f-]{36}$/i);
        expect(firstFutureSchedule).not.toBe(original.scheduleRef);

        await openHome(page, dateAfter(day, 2));
        const later = page.locator('[data-timeline-event]').filter({
          hasText: title,
        });
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
        await expect(
          page.locator('[data-timeline-event="' + original.scheduleRef + '"]'),
        ).toHaveCount(1);
        await assertPersistedTitle(page, original, title);
        await openHome(page, dateAfter(day, 1));
        await expect(
          page.locator('[data-timeline-event="' + firstFutureSchedule + '"]'),
        ).toHaveCount(1);
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
      const card = page.locator('[data-timeline-event]')
        .filter({ hasText: title }).first();
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
      await expect(page.locator('[data-timeline-event]').filter({
        hasText: changedTitle,
      }).first()).toBeVisible();
      await openHome(page, dateAfter(day, 1));
      // Local mutation must not propagate to a clean following instance.
      await expect(page.locator('[data-timeline-event]').filter({
        hasText: changedTitle,
      })).toHaveCount(0);
      const following = page.locator('[data-timeline-event]')
        .filter({ hasText: title }).first();
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
      await confirmation.getByRole('button', {
        name: 'Conferma salvataggio',
      }).click();
      await openHome(page, dateAfter(day, 1));
      await expect(page.locator('[data-timeline-event]').filter({
        hasText: seriesTitle,
      }).first()).toBeVisible();

      const current = page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle }).first();
      await current.getByRole('button', { name: seriesTitle, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina' }).click();
      // Both scoped destructive choices must be explicit and cancellable.
      await expect(
        inspector.getByRole('button', { name: 'Solo questa istanza' }),
      ).toBeVisible();
      await expect(
        inspector.getByRole('button', { name: 'Tutta la serie' }),
      ).toBeVisible();
      await inspector.getByRole('button', { name: 'Annulla' }).click();

      await inspector.getByRole('button', { name: 'Elimina' }).click();
      const localDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await inspector.getByRole('button', { name: 'Solo questa istanza' }).click();
      expect((await localDelete).status()).toBe(200);
      await openHome(page, dateAfter(day, 2));
      const future = page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle }).first();
      await expect(future).toBeVisible();
      await future.getByRole('button', { name: seriesTitle, exact: true }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina' }).click();
      const seriesDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await inspector.getByRole('button', { name: 'Tutta la serie' }).click();
      expect((await seriesDelete).status()).toBe(200);
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
      const first = page.locator('[data-timeline-event]')
        .filter({ hasText: title }).first();
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
      await expect(page.locator('[data-timeline-event]')
        .filter({ hasText: localTitle }).first()).toBeVisible();
      await openHome(page, dateAfter(day, 1));
      await expect(page.locator('[data-timeline-event]')
        .filter({ hasText: localTitle })).toHaveCount(0);

      const following = page.locator('[data-timeline-event]')
        .filter({ hasText: title }).first();
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
      const current = page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle }).first();
      await expect(current).toBeVisible();
      await current.getByRole('button', {
        name: seriesTitle, exact: true,
      }).click();
      inspector = page.locator('.timeline-event-modal[role="dialog"]');
      await inspector.getByRole('button', { name: 'Elimina Event' }).click();
      await expect(
        inspector.getByRole('button', { name: 'Solo questa istanza' }),
      ).toBeVisible();
      await expect(
        inspector.getByRole('button', { name: 'Tutta la serie' }),
      ).toBeVisible();
      await inspector.getByRole('button', { name: 'Annulla' }).click();

      // Delete the selected generated instance without touching the source.
      await inspector.getByRole('button', { name: 'Elimina Event' }).click();
      const instanceDelete = page.waitForResponse(
        (response) =>
          response.url().includes('/api/v1/temporal/hard-deletion/') &&
          response.request().method() === 'DELETE',
      );
      await inspector.getByRole('button', {
        name: 'Solo questa istanza',
      }).click();
      expect((await instanceDelete).status()).toBe(200);
      await openHome(page, dateAfter(day, 2));
      const future = page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle }).first();
      await expect(future).toBeVisible();
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
      await inspector.getByRole('button', { name: 'Tutta la serie' }).click();
      expect((await seriesDelete).status()).toBe(200);
      await openHome(page, dateAfter(day, 3));
      await expect(page.locator('[data-timeline-event]')
        .filter({ hasText: seriesTitle })).toHaveCount(0);
    } finally {
      await user.close();
    }
  });

});
