/**
 * Stateful v2: real authenticated browser -> canonical HTTP -> PostgreSQL.
 *
 * Every scenario is a separate Playwright test/account. Known product bugs
 * remain red and never become test.skip/test.fail/conditional assertions.
 * See docs/development/temporal-user-lifecycle-journey-matrix.md.
 */
import { Temporal } from '@dante/time';
import {
  expect, test, type Locator, type Page,
} from '@playwright/test';

import {
  create, dateAfter, openHome, scenarioDate, serverRead, submitCreate,
  uniqueTitle, type CreatedItem,
} from './temporal-user-journey-support';
import {
  ACTIVITY_CASES, EVENT_CASES, PERSONA_CASES, recurrenceFor,
  type PersonaCase,
} from './temporal-stateful-case-matrix';
import {
  assertOneOffTruth, authorPersona, signedInPersona,
  type AuthoredPersona, type PersonaTruth,
} from './temporal-stateful-journey-support';

const UUID = /^[\da-f-]{36}$/i;
const TZ = { 'X-Dante-Time-Zone': 'Europe/Rome' } as const;

function onDay(page: Page, day: string, title: string): Locator {
  return page.locator(
    '[data-timeline-event][data-planned-date="' + day + '"]',
  ).filter({ hasText: title });
}

function nextOccurrence(
  day: string,
  recurrence: ReturnType<typeof recurrenceFor>,
): string {
  const start = Temporal.PlainDate.from(day);
  switch (recurrence.cadence) {
    case 'daily':
      return start.add({ days: recurrence.interval }).toString();
    case 'weekly':
    case 'custom':
      return start.add({ weeks: recurrence.interval }).toString();
    case 'yearly':
      return start.add({ years: recurrence.interval }).toString();
    case 'monthly': {
      if (!recurrence.monthlyOrdinal) {
        return start.add({ months: recurrence.interval }).toString();
      }
      const next = start.with({ day: 1 }).add({
        months: recurrence.interval,
      });
      const delta = (start.dayOfWeek - next.dayOfWeek + 7) % 7;
      const ordinal = Math.ceil(start.day / 7);
      if (ordinal === 5) {
        const last = next.add({ months: 1 }).subtract({ days: 1 });
        const back = (last.dayOfWeek - start.dayOfWeek + 7) % 7;
        return last.subtract({ days: back }).toString();
      }
      return next.add({ days: delta + (ordinal - 1) * 7 }).toString();
    }
  }
}

async function assertCard(
  page: Page, day: string, title: string,
): Promise<Locator> {
  await openHome(page, day);
  const card = onDay(page, day, title);
  await expect(card, 'exactly one materialized card on ' + day).toHaveCount(1);
  return card;
}

async function openEdit(
  page: Page, day: string, title: string,
): Promise<Locator> {
  const card = await assertCard(page, day, title);
  await card.getByRole('button', { name: title, exact: true }).click();
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await expect(inspector).toBeVisible();
  await inspector.getByRole('button', { name: 'Modifica', exact: true }).click();
  return inspector;
}

async function editOneOff(
  page: Page, day: string, authored: AuthoredPersona,
  persona: PersonaCase,
): Promise<AuthoredPersona> {
  const { item, truth } = authored;
  const editor = await openEdit(page, day, truth.title);
  const newTitle = truth.title + ' revisionato';
  await editor.getByRole('textbox', {
    name: item.kind === 'event' ? 'Titolo Event' : 'Titolo',
  }).fill(newTitle);
  const goals = [...truth.objectives];
  const firstGoal = goals[0]!;
  const renamedGoal = {
    ...firstGoal, label: firstGoal.label + ' corretto',
  };
  await editor.locator('[data-create-objective]').first()
    .getByRole('textbox', { name: 'Nome obiettivo' })
    .fill(renamedGoal.label);
  goals[0] = renamedGoal;

  let agenda = [...truth.agenda];
  let sessions = [...truth.sessions];
  if (item.kind === 'event') {
    // An existing agenda row is changed, the final row removed, and a new
    // row added. Array order and absence of deleted rows are later asserted.
    const initial = editor.locator('[data-temporal-create-agenda-part]');
    const changed = agenda[0]! + ' aggiornata';
    await initial.first()
      .getByRole('textbox', { name: 'Punto scaletta 1' }).fill(changed);
    agenda[0] = changed;
    await initial.last().getByRole('button', { name: 'Rimuovi punto' }).click();
    agenda = agenda.slice(0, -1);
    await editor.getByRole('button', { name: 'Aggiungi punto alla scaletta' })
      .click();
    const appended = newTitle + ' scaletta aggiunta';
    await editor.getByRole('textbox', {
      name: 'Punto scaletta ' + (agenda.length + 1),
    }).fill(appended);
    agenda.push(appended);
  } else {
    // Removal is intentional; a stale Session row must not resurrect.
    const planned = editor.locator('[data-edit-planned-session]');
    await expect(planned).toHaveCount(truth.sessions.length);
    await planned.last().getByRole('button', { name: 'Rimuovi Sessione' })
      .click();
    sessions = sessions.slice(0, -1);
    await editor.locator('.timeline-activity-editor__sessions')
      .getByRole('button', { name: 'Sessione', exact: true }).click();
    const appended = newTitle + ' Sessione aggiunta';
    await editor.locator('[data-edit-new-session]').last()
      .getByRole('textbox', { name: 'Nome Sessione' }).fill(appended);
    sessions.push(appended);
  }
  await editor.getByRole('button', { name: 'Salva modifiche' }).click();
  const updated = {
    ...authored,
    item: { ...item, title: newTitle },
    truth: {
      ...truth, title: newTitle,
      objectives: goals,
      agenda, sessions,
    } satisfies PersonaTruth,
  } satisfies AuthoredPersona;
  await assertCard(page, day, newTitle);
  await assertOneOffTruth(page, updated);
  return updated;
}

async function duplicateAndCompare(
  page: Page, day: string, authored: AuthoredPersona,
): Promise<CreatedItem> {
  const { item, truth } = authored;
  const card = await assertCard(page, day, truth.title);
  await card.getByRole('button', { name: truth.title, exact: true }).click();
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await inspector.getByRole('button', { name: 'Duplica' }).click();
  const composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toBeVisible();
  await expect(composer.getByRole('textbox', { name: 'Titolo' }))
    .toHaveValue(truth.title);
  await expect(composer.locator('[data-create-objective]'))
    .toHaveCount(truth.objectives.length);
  const labels = await composer.locator('[data-create-objective]')
    .getByRole('textbox', { name: /^Obiettivo \d+$/ }).allInputValues();
  expect(labels).toEqual(truth.objectives.map((objective) => objective.label));
  if (item.kind === 'event') {
    await expect(composer.locator('[data-temporal-create-agenda-part]'))
      .toHaveCount(truth.agenda.length);
    expect(await composer.locator('[data-temporal-create-agenda-input]')
      .allInputValues()).toEqual(truth.agenda);
  } else {
    expect(await composer.locator('[data-create-planned-session]')
      .getByRole('textbox', { name: 'Nome Sessione' }).allInputValues())
      .toEqual(truth.sessions);
  }
  const duplicateTitle = uniqueTitle('v2 copia ' + item.kind);
  await composer.getByRole('textbox', { name: 'Titolo' }).fill(duplicateTitle);
  const copy = await submitCreate(page, composer, {
    kind: item.kind, title: duplicateTitle, recurring: false,
  });
  expect(copy.sourceRef).not.toBe(item.sourceRef);
  expect(copy.scheduleRef).not.toBe(item.scheduleRef);
  await assertOneOffTruth(page, {
    ...authored,
    item: copy,
    truth: { ...truth, title: duplicateTitle },
  });
  return copy;
}

async function deleteOneOff(
  page: Page, day: string, item: CreatedItem,
): Promise<void> {
  const card = await assertCard(page, day, item.title);
  await card.getByRole('button', { name: item.title, exact: true }).click();
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  const action = item.kind === 'event' ? 'Elimina Event' : 'Elimina';
  await inspector.getByRole('button', { name: action, exact: true }).click();
  const confirm = page.getByRole('alertdialog', {
    name: item.kind === 'event' ? 'Elimina evento' : 'Elimina attività',
  });
  await expect(confirm).toBeVisible();
  await confirm.getByRole('button', { name: 'Annulla' }).click();
  await expect(confirm).toHaveCount(0);
  await assertCard(page, day, item.title);
  await inspector.getByRole('button', { name: action, exact: true }).click();
  const removed = page.waitForResponse((response) =>
    response.request().method() === 'DELETE' &&
    response.url().includes(item.sourceRef),
  );
  await confirm.getByRole('button', { name: 'Elimina definitivamente' })
    .click();
  expect((await removed).status()).toBe(200);
  await expect(confirm).toHaveCount(0);
  await openHome(page, day);
  await expect(onDay(page, day, item.title)).toHaveCount(0);
  const detail = await page.request.get(
    item.kind === 'event'
      ? '/api/v1/temporal/events/' + item.sourceRef
      : '/api/v1/temporal/activities/' + item.sourceRef + '/profile',
    { headers: TZ },
  );
  expect(detail.status()).toBe(404);
}

async function occurrence(
  page: Page, day: string, sourceRef: string,
): Promise<Record<string, unknown>> {
  const end = dateAfter(day, 1);
  const window = await serverRead(
    page,
    '/api/v1/temporal/timeline/window?start_date=' + day +
      '&end_date_exclusive=' + end,
  ) as Record<string, unknown>;
  expect(window.kind).toBe('window');
  const rows = window.items as Record<string, unknown>[];
  const matching = rows.filter((row) =>
    row.source_native_ref === sourceRef &&
    row.occurrence_ref !== undefined,
  );
  expect(matching, 'unique canonical occurrence on ' + day).toHaveLength(1);
  expect(matching[0]!.occurrence_ref).toEqual(expect.stringMatching(UUID));
  return matching[0]!;
}

async function seriesRevision(
  page: Page,
  day: string,
  originalTitle: string,
  nextTitle: string,
): Promise<void> {
  const inspector = await openEdit(page, day, originalTitle);
  const scope = page.getByRole('dialog', { name: 'Modifica ricorrenza' });
  await scope.getByRole('button', { name: 'Questa e le successive' })
    .click();
  await inspector.getByRole('textbox', { name: 'Titolo' }).fill(nextTitle);
  await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
  const confirmation = page.getByRole('dialog', {
    name: 'Controlla prima di salvare',
  });
  await expect(confirmation).toBeVisible();
  const accepted = page.waitForResponse((response) =>
    response.url().endsWith('/series-edit') &&
    response.request().method() === 'POST',
  );
  await confirmation.getByRole('button', { name: 'Conferma salvataggio' })
    .click();
  const response = await accepted;
  expect(response.status(), await response.text()).toBe(200);
  await expect(confirmation).toHaveCount(0);
}

async function localRevision(
  page: Page,
  day: string,
  title: string,
  kind: PersonaCase['kind'],
  changedTitle: string,
): Promise<void> {
  const inspector = await openEdit(page, day, title);
  const scope = page.getByRole('dialog', { name: 'Modifica ricorrenza' });
  await scope.getByRole('button', { name: 'Solo questa istanza' }).click();
  await inspector.getByRole('textbox', {
    name: kind === 'event' ? 'Titolo Event' : 'Titolo',
  }).fill(changedTitle);
  await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
  await assertCard(page, day, changedTitle);
}

test.describe('Temporal v2 — real stateful user personas', () => {
  test.describe.configure({ timeout: 300_000 });

  // Phase 1: forty distinct independent subjects, each with multiple fields,
  // a successive destructive/edit mutation, full reload, duplicate and delete.
  for (const [ordinal, persona] of PERSONA_CASES.entries()) {
    test('V2-P1-' + persona.id + ' rich create → mutate → duplicate → delete', async (
      { browser }, info,
    ) => {
      const user = await signedInPersona(browser, info, ordinal);
      const { page } = user;
      const day = scenarioDate(5);
      const title = uniqueTitle('v2 ' + persona.id);
      await info.attach('scenario', {
        body: Buffer.from(JSON.stringify({ phase: 1, persona }, null, 2)),
        contentType: 'application/json',
      });
      try {
        await test.step(persona.id + '/1 Create multi-feature', async () => {
          await openHome(page, day);
        });
        const authored = await test.step(
          persona.id + '/2 Create from production UI', async () =>
            authorPersona(page, persona, title, day),
        );
        await test.step(persona.id + '/3 Canonical full readback', async () => {
          await openHome(page, day);
          await assertOneOffTruth(page, authored);
        });
        const updated = await test.step(
          persona.id + '/4 Edit, remove and add nested data', async () =>
            editOneOff(page, day, authored, persona),
        );
        const copy = await test.step(
          persona.id + '/5 Duplicate the FINAL state, not initial', async () =>
            duplicateAndCompare(page, day, updated),
        );
        await test.step(persona.id + '/6 Delete original; duplicate survives', async () => {
          await deleteOneOff(page, day, updated.item);
          await assertOneOffTruth(page, {
            ...updated,
            item: copy,
            truth: { ...updated.truth, title: copy.title },
          });
        });
      } finally {
        await user.close();
      }
    });
  }

  // Phase 2: forty native recurring sources built with the same rich matrix.
  // Source, local exception and future revision are separate server operations.
  for (const [index, persona] of PERSONA_CASES.entries()) {
    test('V2-P2-' + persona.id + ' native series → local → following', async (
      { browser }, info,
    ) => {
      const user = await signedInPersona(browser, info, 40 + index);
      const { page } = user;
      const day = scenarioDate(5);
      const recurrence = recurrenceFor(persona);
      const future = nextOccurrence(day, recurrence);
      const title = uniqueTitle('v2 serie ' + persona.id);
      await info.attach('scenario', {
        body: Buffer.from(JSON.stringify({
          phase: 2, persona, recurrence, day, future,
        }, null, 2)),
        contentType: 'application/json',
      });
      try {
        await openHome(page, day);
        const authored = await test.step(
          persona.id + '/1 Create rich native series', async () =>
            authorPersona(page, persona, title, day, recurrence),
        );
        await test.step(persona.id + '/2 Initial and future readback', async () => {
          await assertCard(page, day, title);
          await occurrence(page, day, authored.item.sourceRef);
          await assertCard(page, future, title);
          await occurrence(page, future, authored.item.sourceRef);
        });
        const localTitle = title + ' solo questa';
        await test.step(persona.id + '/3 Local exception on initial instance', async () => {
          await localRevision(page, day, title, persona.kind, localTitle);
          await assertCard(page, future, title);
          await assertCard(page, day, localTitle);
        });
        const revisedTitle = title + ' questa e successive';
        await test.step(persona.id + '/4 Following-series revision', async () => {
          await seriesRevision(page, future, title, revisedTitle);
          await assertCard(page, future, revisedTitle);
          await occurrence(page, future, authored.item.sourceRef);
          await assertCard(page, day, localTitle);
          await expect(onDay(page, day, revisedTitle)).toHaveCount(0);
        });
      } finally {
        await user.close();
      }
    });
  }

  // Phase 3: twenty rich one-offs become recurring through Edit.
  // Unlike a native series, original physical identity must be retained.
  for (const [index, persona] of [
    ...EVENT_CASES.slice(0, 10), ...ACTIVITY_CASES.slice(0, 10),
  ].entries()) {
    test('V2-P3-' + persona.id + ' one-off → series → scoped edits', async (
      { browser }, info,
    ) => {
      const user = await signedInPersona(browser, info, 80 + index);
      const { page } = user;
      const day = scenarioDate(5);
      const title = uniqueTitle('v2 conversione ' + persona.id);
      await info.attach('scenario', {
        body: Buffer.from(JSON.stringify({ phase: 3, persona }, null, 2)),
        contentType: 'application/json',
      });
      try {
        await openHome(page, day);
        const authored = await test.step(
          persona.id + '/1 Rich ordinary source', async () =>
            authorPersona(page, persona, title, day),
        );
        await test.step(persona.id + '/2 Read full source state', async () => {
          await assertOneOffTruth(page, authored);
        });
        await test.step(persona.id + '/3 Convert through real Edit', async () => {
          const editor = await openEdit(page, day, title);
          const recurrence = editor.getByRole('region', {
            name: 'Ripetizione', exact: true,
          });
          await recurrence.getByRole('combobox', { name: 'Ripeti' })
            .selectOption('daily');
          const conversion = page.waitForResponse((response) =>
            response.request().method() === 'POST' &&
            response.url().endsWith(
              '/api/v1/temporal/recurring/' +
              (persona.kind === 'event' ? 'events/' : 'activities/') +
              authored.item.sourceRef + '/start',
            ),
          );
          await editor.getByRole('button', { name: 'Salva modifiche' })
            .click();
          expect((await conversion).status()).toBe(200);
          const originalCard = await assertCard(page, day, title);
          expect(await originalCard.getAttribute('data-timeline-event'))
            .toBe(authored.item.scheduleRef);
          await assertCard(page, dateAfter(day, 1), title);
        });
        await test.step(persona.id + '/4 Local change on generated instance', async () => {
          await localRevision(
            page, dateAfter(day, 1), title, persona.kind, title + ' locale',
          );
          await assertCard(page, day, title);
          await assertCard(page, dateAfter(day, 2), title);
        });
        await test.step(persona.id + '/5 Future revision preserves original', async () => {
          await seriesRevision(
            page, dateAfter(day, 2), title, title + ' futuro',
          );
          await assertCard(page, dateAfter(day, 2), title + ' futuro');
          await assertCard(page, dateAfter(day, 1), title + ' locale');
          const first = await assertCard(page, day, title);
          expect(await first.getAttribute('data-timeline-event'))
            .toBe(authored.item.scheduleRef);
        });
      } finally {
        await user.close();
      }
    });
  }
});
