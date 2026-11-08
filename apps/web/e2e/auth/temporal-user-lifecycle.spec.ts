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
    const persisted = (await serverRead(page, url)) as Record<string, unknown>;
    expect(persisted.title).toBe(expected);
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
    // Cancel must not mutate anything.
    await expect(
      inspector.getByRole('button', { name: 'Conferma eliminazione definitiva' }),
    ).toBeVisible();
    await inspector.getByRole('button', { name: 'Annulla', exact: true }).click();
    await expect(
      page.locator('[data-timeline-event="' + item.scheduleRef + '"]'),
    ).toHaveCount(1);

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
    await inspector.getByRole('button', {
      name: 'Conferma eliminazione definitiva',
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
  }>;

  const activityVariants: readonly Variant[] = [
    { cadence: 'daily', interval: 1, complex: true },
    { cadence: 'weekly', interval: 2 },
    { cadence: 'monthly', interval: 1 },
    { cadence: 'yearly', interval: 1 },
  ];
  const eventVariants: readonly Variant[] = [
    { cadence: 'daily', interval: 1, complex: true },
    { cadence: 'weekly', interval: 1 },
    { cadence: 'monthly', interval: 2, allDay: true },
    { cadence: 'yearly', interval: 1 },
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
              '08:10', '10:10', '12:10', '14:10',
            ][index] ?? '09:10',
            recurrence: variant.cadence,
            interval: variant.interval,
            ...(variant.allDay ? { allDay: true } : {}),
            ...(variant.complex && kind === 'activity'
              ? {
                  plannedSession: 'Studio approfondito',
                  objective: 'Risultato verificato',
                  placementProtected: true,
                }
              : {}),
            ...(variant.complex && kind === 'event'
              ? {
                  agenda: 'Introduzione partecipanti',
                  objective: 'Presenza confermata',
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
            .toHaveValue(variant.cadence);
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
          const patternCode = variant.cadence === 'weekly'
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
        await expect(
          page.locator('[data-timeline-event]').filter({
            hasText: title,
          }).first(),
        ).toBeVisible();
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
});
