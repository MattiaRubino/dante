/**
 * Stateful v2: real authenticated browser -> canonical HTTP -> PostgreSQL.
 *
 * Every scenario is a separate Playwright test/account. Known product bugs
 * remain red and never become test.skip/test.fail/conditional assertions.
 * See docs/development/temporal-user-lifecycle-journey-matrix.md.
 */
import { Temporal } from '@dante/time';
import { expect, test, type Locator, type Page } from '@playwright/test';

import {
  dateAfter,
  openHome,
  scenarioDate,
  serverRead,
  submitCreate,
  uniqueTitle,
  type CreatedItem,
} from './temporal-user-journey-support';
import {
  ACTIVITY_CASES,
  EVENT_CASES,
  PERSONA_CASES,
  recurrenceFor,
  type PersonaCase,
} from './temporal-stateful-case-matrix';
import {
  assertOneOffTruth,
  authorPersona,
  signedInPersona,
  type AuthoredPersona,
  type PersonaTruth,
} from './temporal-stateful-journey-support';

const UUID = /^[\da-f-]{36}$/i;
const TZ = { 'X-Dante-Time-Zone': 'Europe/Rome' } as const;

function onDay(page: Page, day: string, title: string): Locator {
  return page
    .locator(
      '[data-timeline-event][data-planned-date="' +
        day +
        '"], [data-timeline-all-day-lane="' +
        day +
        '"] [data-timeline-all-day-item]',
    )
    .filter({ hasText: title });
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

// Per-test browser Pages have an immutable expected number of physical
// placements. An Activity with 2 intervals has 2 real cards but 1 logical
// Activity. Counting a single card would produce a false duplicate failure.
const placementExpectations = new WeakMap<Page, number>();
function registerPersona(page: Page, persona: PersonaCase): void {
  placementExpectations.set(
    page,
    persona.kind === 'activity' ? Math.max(1, persona.intervalCount) : 1,
  );
}
async function assertCard(
  page: Page,
  day: string,
  title: string,
): Promise<Locator> {
  await openHome(page, day);
  const card = onDay(page, day, title);
  const expected = placementExpectations.get(page) ?? 1;
  await expect(card, 'exact physical placements on ' + day).toHaveCount(
    expected,
  );
  return card.first();
}

async function clickCard(card: Locator, title: string): Promise<void> {
  if ((await card.getAttribute('data-timeline-all-day-item')) !== null) {
    await card.click();
  } else {
    await card.getByRole('button', { name: title, exact: true }).click();
  }
}

async function openEdit(
  page: Page,
  day: string,
  title: string,
): Promise<Locator> {
  const card = await assertCard(page, day, title);
  await clickCard(card, title);
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await expect(inspector).toBeVisible();
  await inspector
    .getByRole('button', { name: 'Modifica', exact: true })
    .click();
  return inspector;
}

/**
 * A Save click only submits intent. Before reading canonical state or
 * navigating, prove the exact self-scoped mutation has committed.
 *
 * The 2026-11-09 Chromium/Firefox/WebKit traces prove that a GET issued
 * immediately after click can overtake the PUT, producing a false missing
 * Life Area and cancelling the request during test teardown.
 */
async function saveOneOffEditor(
  page: Page,
  editor: Locator,
  item: CreatedItem,
): Promise<void> {
  const endpoint =
    '/api/v1/temporal/' +
    (item.kind === 'event' ? 'events/' : 'activities/') +
    item.sourceRef +
    '/atomic-edit';
  let accepted: Awaited<ReturnType<Page['waitForResponse']>>;
  try {
    [accepted] = await Promise.all([
      page.waitForResponse(
        (response) =>
          response.request().method() === 'PUT' &&
          response.url().endsWith(endpoint),
        { timeout: 15_000 },
      ),
      editor.getByRole('button', { name: 'Salva modifiche' }).click(),
    ]);
  } catch (reason) {
    // A rejected client-side edit never sends PUT. Report the real field
    // errors rather than hiding them behind a generic 30-second wait.
    const alerts = await editor
      .locator('[role="alert"]')
      .allTextContents()
      .catch(() => []);
    const invalidFields = await editor
      .locator('[aria-invalid="true"]')
      .evaluateAll((elements) =>
        elements.map(
          (node) =>
            node.getAttribute('aria-label') ??
            node.getAttribute('name') ??
            node.getAttribute('placeholder') ??
            'unknown',
        ),
      )
      .catch(() => []);
    throw new Error(
      'Atomic Edit did not complete for ' +
        item.kind +
        ' ' +
        item.sourceRef +
        '; alerts=' +
        JSON.stringify(alerts) +
        '; invalidFields=' +
        JSON.stringify(invalidFields),
      { cause: reason },
    );
  }
  expect(
    accepted.status(),
    'atomic Edit must succeed before canonical read: ' + endpoint,
  ).toBe(200);
  if (item.kind === 'event') {
    await expect(editor.getByText('Evento aggiornato.')).toBeVisible();
  } else {
    await expect(
      editor.getByRole('button', { name: 'Salva modifiche' }),
    ).toHaveCount(0);
  }
}

async function editOneOff(
  page: Page,
  day: string,
  authored: AuthoredPersona,
): Promise<AuthoredPersona> {
  const { item, truth } = authored;
  const goalEndpoint =
    '/api/v1/temporal/' +
    (item.kind === 'event' ? 'events/' : 'activities/') +
    item.sourceRef +
    '/objectives';
  const originalGoals = (await serverRead(
    page,
    goalEndpoint,
  )) as readonly Record<string, unknown>[];
  expect(originalGoals).toHaveLength(truth.objectives.length);
  const beforePlanned =
    item.kind === 'activity'
      ? ((
          (await serverRead(
            page,
            '/api/v1/temporal/activities/' + item.sourceRef + '/edit-snapshot',
          )) as Record<string, unknown>
        ).schedules as Record<string, unknown>[])
      : [];
  const originalPlannedRefs = beforePlanned
    .filter((row) => row.role_code === 'planned')
    .map((row) => String(row.schedule_ref));
  const editor = await openEdit(page, day, truth.title);
  const newTitle = truth.title + ' revisionato';
  const newDescription =
    truth.description === null
      ? newTitle + ' descrizione aggiunta'
      : truth.description + ' modificata';
  await editor
    .getByRole('textbox', {
      name: item.kind === 'event' ? 'Titolo Event' : 'Titolo',
    })
    .fill(newTitle);
  await editor
    .getByRole('textbox', { name: 'Descrizione' })
    .fill(newDescription);
  const goals = [...truth.objectives];
  const firstGoal = goals[0]!;
  const renamedGoal = {
    ...firstGoal,
    label: firstGoal.label + ' corretto',
  };
  await editor
    .locator('[data-create-objective]')
    .first()
    .getByRole('textbox', { name: 'Nome obiettivo' })
    .fill(renamedGoal.label);
  goals[0] = renamedGoal;
  // Modify, REMOVE and ADD in one transaction; the removed ID must not
  // survive as a ghost, and all untouched Objective definitions must remain.
  const removedGoal = goals.pop()!;
  await editor
    .locator('[data-create-objective]')
    .last()
    .getByRole('button', {
      name:
        'Rimuovi obiettivo ' +
        (truth.objectives.length === 1 ? renamedGoal.label : removedGoal.label),
    })
    .click();
  await editor.getByRole('button', { name: '+ Obiettivo' }).click();
  const replacementGoal = {
    label: newTitle + ' obiettivo aggiunto',
    kind: 'boolean' as const,
    target: null,
    minimum: null,
    maximum: null,
    verification: 'none' as const,
  };
  await editor
    .locator('[data-create-objective]')
    .last()
    .getByRole('textbox', { name: 'Nome obiettivo' })
    .fill(replacementGoal.label);
  goals.push(replacementGoal);

  let agenda = [...truth.agenda];
  let sessions = [...truth.sessions];
  if (item.kind === 'event') {
    // An existing agenda row is changed, the final row removed, and a new
    // row added. Array order and absence of deleted rows are later asserted.
    const initial = editor.locator('[data-temporal-create-agenda-part]');
    const changed = agenda[0]! + ' aggiornata';
    await initial
      .first()
      .getByRole('textbox', { name: 'Punto scaletta 1', exact: true })
      .fill(changed);
    agenda[0] = changed;
    await initial.last().getByRole('button', { name: 'Rimuovi punto' }).click();
    agenda = agenda.slice(0, -1);
    await editor
      .getByRole('button', { name: 'Aggiungi punto alla scaletta' })
      .click();
    const appended = newTitle + ' scaletta aggiunta';
    await editor
      .getByRole('textbox', {
        name: 'Punto scaletta ' + (agenda.length + 1),
      })
      .fill(appended);
    agenda.push(appended);
  } else {
    // Removal is intentional; a stale Session row must not resurrect.
    const planned = editor.locator('[data-edit-planned-session]');
    await expect(planned).toHaveCount(truth.sessions.length);
    await planned
      .last()
      .getByRole('button', { name: 'Rimuovi Sessione' })
      .click();
    sessions = sessions.slice(0, -1);
    await editor
      .locator('.timeline-activity-editor__sessions')
      .getByRole('button', { name: 'Sessione', exact: true })
      .click();
    const appended = newTitle + ' Sessione aggiunta';
    await editor
      .locator('[data-edit-new-session]')
      .last()
      .getByRole('textbox', { name: 'Nome Sessione' })
      .fill(appended);
    sessions.push(appended);
  }
  await saveOneOffEditor(page, editor, item);
  const updated = {
    ...authored,
    item: { ...item, title: newTitle },
    truth: {
      ...truth,
      title: newTitle,
      description: newDescription,
      objectives: goals,
      agenda,
      sessions,
    } satisfies PersonaTruth,
  } satisfies AuthoredPersona;
  await assertCard(page, day, newTitle);
  await assertOneOffTruth(page, updated);
  const afterGoals = (await serverRead(page, goalEndpoint)) as readonly Record<
    string,
    unknown
  >[];
  const afterRefs = afterGoals.map((row) => String(row.objective_ref));
  const oldRefs = originalGoals.map((row) => String(row.objective_ref));
  for (const survived of oldRefs.slice(0, -1)) {
    expect(afterRefs, 'untouched Objective identity survives Edit').toContain(
      survived,
    );
  }
  expect(afterRefs, 'removed Objective never resurrects').not.toContain(
    oldRefs.at(-1),
  );
  expect(
    afterRefs.filter((ref) => !oldRefs.includes(ref)),
    'only one genuinely new Objective identity',
  ).toHaveLength(1);
  if (item.kind === 'activity') {
    const afterSnapshot = (await serverRead(
      page,
      '/api/v1/temporal/activities/' + item.sourceRef + '/edit-snapshot',
    )) as Record<string, unknown>;
    const afterSchedules = afterSnapshot.schedules as Record<string, unknown>[];
    const afterPlannedRefs = afterSchedules
      .filter((row) => row.role_code === 'planned')
      .map((row) => String(row.schedule_ref));
    for (const survived of originalPlannedRefs.slice(0, -1)) {
      expect(afterPlannedRefs, 'unchanged planned Session identity').toContain(
        survived,
      );
    }
    expect(
      afterPlannedRefs,
      'removed planned Session stays deleted',
    ).not.toContain(originalPlannedRefs.at(-1));
    expect(
      afterPlannedRefs.filter((ref) => !originalPlannedRefs.includes(ref)),
      'only one replacement planned Session identity',
    ).toHaveLength(1);
  }
  return updated;
}

async function reassignAreaAndCancel(
  page: Page,
  day: string,
  authored: AuthoredPersona,
): Promise<AuthoredPersona> {
  const { item, truth } = authored;
  const editor = await openEdit(page, day, truth.title);
  const nextArea = uniqueTitle('nuova area dopo modifica');
  await editor
    .getByRole('textbox', {
      name: item.kind === 'event' ? 'Life Area (opzionale)' : 'Area assegnata',
    })
    .fill(nextArea);
  await editor
    .getByRole('button', {
      name:
        item.kind === 'event' ? 'Colore nuova Life Area' : 'Colore Life Area',
    })
    .click();
  await page
    .getByRole('dialog', { name: 'Scegli colore' })
    .getByRole('button', { name: 'Prugna', exact: true })
    .click();
  // This new-area Save is asynchronous: never allow a catalog GET to
  // overtake its atomic PUT. No retry/sleep or weaker cardinality check.
  await saveOneOffEditor(page, editor, item);
  const catalog = (await serverRead(
    page,
    '/api/v1/temporal/life-areas',
  )) as readonly Record<string, unknown>[];
  const matches = catalog.filter((row) => row.name === nextArea);
  expect(matches, 'exactly one new Life Area after reassign').toHaveLength(1);
  expect(matches[0]!.color_code).toBe('#8E24AA');
  const updated: AuthoredPersona = {
    ...authored,
    truth: {
      ...truth,
      areaName: nextArea,
      areaRef: String(matches[0]!.life_area_ref),
    },
    areaColor: '#8E24AA',
  };
  await openHome(page, day);
  await assertOneOffTruth(page, updated);

  const cancelEditor = await openEdit(page, day, truth.title);
  await cancelEditor
    .getByRole('textbox', {
      name: item.kind === 'event' ? 'Titolo Event' : 'Titolo',
    })
    .fill(truth.title + ' NON SALVATO');
  await cancelEditor.getByRole('button', { name: 'Annulla' }).click();
  const discard = page.getByRole('alertdialog', {
    name: 'Modifiche non salvate',
  });
  await expect(discard).toBeVisible();
  await discard.getByRole('button', { name: 'Continua a modificare' }).click();
  await expect(
    cancelEditor.getByRole('textbox', {
      name: item.kind === 'event' ? 'Titolo Event' : 'Titolo',
    }),
  ).toHaveValue(truth.title + ' NON SALVATO');
  await cancelEditor.getByRole('button', { name: 'Annulla' }).click();
  await discard.getByRole('button', { name: 'Scarta modifiche' }).click();
  await expect(discard).toHaveCount(0);
  await openHome(page, day);
  await assertOneOffTruth(page, updated);
  await expect(onDay(page, day, truth.title + ' NON SALVATO')).toHaveCount(0);
  return updated;
}

async function inputValues(fields: Locator): Promise<string[]> {
  const inputs = await fields.all();
  return Promise.all(inputs.map((input) => input.inputValue()));
}

async function duplicateAndCompare(
  page: Page,
  day: string,
  authored: AuthoredPersona,
): Promise<CreatedItem> {
  const { item, truth } = authored;
  const card = await assertCard(page, day, truth.title);
  await clickCard(card, truth.title);
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await inspector.getByRole('button', { name: 'Duplica' }).click();
  const composer = page.locator('[data-temporal-create="composer"]');
  await expect(composer).toBeVisible();
  await expect(composer.getByRole('textbox', { name: 'Titolo' })).toHaveValue(
    truth.title,
  );
  await expect(composer.locator('[data-create-objective]')).toHaveCount(
    truth.objectives.length,
  );
  const labels = await inputValues(
    composer
      .locator('[data-create-objective]')
      .getByRole('textbox', { name: /^Obiettivo \d+$/ }),
  );
  expect(labels).toEqual(truth.objectives.map((objective) => objective.label));
  if (item.kind === 'event') {
    await expect(
      composer.locator('[data-temporal-create-agenda-part]'),
    ).toHaveCount(truth.agenda.length);
    expect(
      await inputValues(
        composer.locator('[data-temporal-create-agenda-input]'),
      ),
    ).toEqual(truth.agenda);
  } else {
    expect(
      await inputValues(
        composer
          .locator('[data-create-planned-session]')
          .getByRole('textbox', { name: 'Nome Sessione' }),
      ),
    ).toEqual(truth.sessions);
  }
  const duplicateTitle = uniqueTitle('v2 copia ' + item.kind);
  await composer.getByRole('textbox', { name: 'Titolo' }).fill(duplicateTitle);
  const copy = await submitCreate(page, composer, {
    kind: item.kind,
    title: duplicateTitle,
    recurring: false,
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
  page: Page,
  day: string,
  item: CreatedItem,
): Promise<void> {
  const card = await assertCard(page, day, item.title);
  await clickCard(card, item.title);
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  const action = item.kind === 'event' ? 'Elimina Event' : 'Elimina';
  await inspector.getByRole('button', { name: action, exact: true }).click();
  const confirm = page.getByRole('alertdialog', {
    name: item.kind === 'event' ? 'Elimina evento' : 'Elimina attività',
  });
  await expect(confirm).toBeVisible();
  await confirm.getByRole('button', { name: 'Annulla' }).click();
  await expect(confirm).toHaveCount(0);
  // assertCard performs full Home navigation, which unmounts the inspector
  // that owned the first (cancelled) delete. Open a NEW inspector before
  // attempting the second, destructive confirmation.
  const retained = await assertCard(page, day, item.title);
  await clickCard(retained, item.title);
  await expect(inspector).toBeVisible({ timeout: 10_000 });
  const secondDelete = inspector.getByRole('button', {
    name: action,
    exact: true,
  });
  await expect(secondDelete).toBeVisible({ timeout: 10_000 });
  await secondDelete.click({ timeout: 10_000 });
  const removed = page.waitForResponse(
    (response) =>
      response.request().method() === 'DELETE' &&
      response.url().includes(item.sourceRef),
  );
  await confirm
    .getByRole('button', { name: 'Elimina definitivamente' })
    .click();
  expect(
    (await removed).status(),
    'confirmed one-off DELETE must succeed',
  ).toBe(200);
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

async function draftAndVerify(
  page: Page,
  day: string,
  item: CreatedItem,
  truth: PersonaTruth,
): Promise<void> {
  const card = await assertCard(page, day, item.title);
  await clickCard(card, item.title);
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  const vault = page.waitForResponse(
    (response) =>
      response.request().method() === 'PUT' &&
      response.url().includes('/api/v1/temporal/drafts/'),
  );
  if (item.kind === 'activity') {
    await inspector.getByRole('button', { name: 'Sposta in Bozze' }).click();
    await inspector
      .getByRole('button', {
        name: 'Conferma spostamento in Bozze',
      })
      .click();
  } else {
    await inspector.getByRole('button', { name: 'Copia in Bozze' }).click();
  }
  expect((await vault).ok(), 'draft snapshot accepted').toBe(true);
  const drafts = (await serverRead(
    page,
    '/api/v1/temporal/drafts',
  )) as readonly Record<string, unknown>[];
  const matching = drafts.filter(
    (draft) => draft.title === item.title && draft.subject_kind === item.kind,
  );
  expect(matching, 'exactly one independent Draft Vault snapshot').toHaveLength(
    1,
  );
  const payload = matching[0]!.payload as Record<string, unknown>;
  const fields = payload.fields as Record<string, unknown>;
  expect(fields.title).toBe(truth.title);
  expect(fields.kind).toBe(item.kind);
  expect(
    fields.contextId,
    'draft must retain accepted Life Area reference',
  ).toBe(truth.areaRef ?? '');
  expect(matching[0]!.draft_ref).toEqual(expect.stringMatching(UUID));
  await openHome(page, day);
  if (item.kind === 'activity') {
    // Move removes the operational Activity, not its independent draft.
    await expect(onDay(page, day, item.title)).toHaveCount(0);
  } else {
    // Event offers Copy to Drafts: the source Event stays operational.
    await expect(onDay(page, day, item.title)).toHaveCount(1);
  }
}

async function assertDayHasNoDuplicatePlacements(
  page: Page,
  day: string,
  originalTitle: string,
  currentTitle: string,
  persona: PersonaCase,
): Promise<void> {
  // This is a canonical server read, not a DOM count. Physical Activity
  // intervals are distinct Schedule identities of ONE Activity.
  const window = (await serverRead(
    page,
    '/api/v1/temporal/timeline/window?start_date=' +
      day +
      '&end_date_exclusive=' +
      dateAfter(day, 1),
  )) as Record<string, unknown>;
  expect(window.kind).toBe('window');
  const rows = (window.items as Record<string, unknown>[]).filter((row) => {
    if (
      typeof row.title !== 'string' ||
      !row.title.startsWith(originalTitle) ||
      typeof row.schedule_ref !== 'string'
    )
      return false;
    // Materialized recurring Events carry time within their nested
    // SchedulePlacement. Ordinary Events and Activities use flat fields.
    // Both shape families are legitimate in the same canonical Timeline.
    const placement =
      row.placement && typeof row.placement === 'object'
        ? (row.placement as Record<string, unknown>)
        : null;
    const start =
      row.display_starts_local_at ??
      row.starts_local_at ??
      row.start_date ??
      row.local_date ??
      placement?.display_starts_local_at ??
      placement?.starts_local_at ??
      placement?.start_date ??
      placement?.local_date;
    return typeof start === 'string' && start.startsWith(day);
  });
  const required =
    persona.kind === 'activity' ? Math.max(1, persona.intervalCount) : 1;
  expect(
    rows,
    'exact physical placement count for this series or conversion/' + day,
  ).toHaveLength(required);
  expect(
    rows.map((row) => String(row.title)),
    'only expected title for this scoped Edit',
  ).toEqual(Array.from({ length: required }, () => currentTitle));
  expect(
    new Set(rows.map((row) => String(row.schedule_ref))).size,
    'no duplicate physical Schedule identity',
  ).toBe(required);
  if (persona.kind === 'activity') {
    expect(
      new Set(rows.map((row) => String(row.activity_ref))).size,
      'interval cards belong to a single logical Activity',
    ).toBe(1);
  }
}

async function assertNoOccurrenceBeyondFiniteEnd(
  page: Page,
  lastDay: string,
  recurrence: ReturnType<typeof recurrenceFor>,
  uniqueSourceTitle: string,
): Promise<void> {
  // "This and following" and "From next" may split a bounded source,
  // but can never revive a sixth/seventh occurrence after its finite end.
  // Read the real canonical window: DOM title and visibility alone are
  // insufficient to prove the source did not regenerate a hidden item.
  let next = lastDay;
  for (let i = 0; i < 2; i += 1) {
    next = nextOccurrence(next, recurrence);
    const window = (await serverRead(
      page,
      '/api/v1/temporal/timeline/window?start_date=' +
        next +
        '&end_date_exclusive=' +
        dateAfter(next, 1),
    )) as Record<string, unknown>;
    // An entirely empty canonical Timeline uses kind='empty' and omits
    // items. Do not require a nonempty-window envelope to prove a finite
    // recurrence stopped generating; reject malformed responses instead.
    expect(['window', 'empty']).toContain(window.kind);
    const items = window.items;
    if (window.kind === 'empty') {
      expect(items, 'empty Timeline must have no item payload').toBeUndefined();
    } else {
      expect(Array.isArray(items), 'window Timeline must expose items').toBe(
        true,
      );
    }
    const rows: Record<string, unknown>[] = Array.isArray(items)
      ? (items as Record<string, unknown>[])
      : [];
    const unauthorized = rows.filter(
      (row) =>
        typeof row.title === 'string' &&
        row.title.startsWith(uniqueSourceTitle),
    );
    expect(
      unauthorized,
      'bounded recurrence must not generate occurrence beyond final ' +
        lastDay +
        ' on ' +
        next,
    ).toHaveLength(0);
  }
}

async function assertOriginalScheduleIdentity(
  page: Page,
  day: string,
  item: CreatedItem,
): Promise<void> {
  expect(item.scheduleRef, 'source must retain a physical Schedule').toEqual(
    expect.stringMatching(UUID),
  );
  if (item.kind === 'activity') {
    // A multi-interval Activity renders interval Schedules in the timeline;
    // its original envelope Schedule is retained in the edit snapshot.
    const snapshot = (await serverRead(
      page,
      '/api/v1/temporal/activities/' + item.sourceRef + '/edit-snapshot',
    )) as Record<string, unknown>;
    const schedules = snapshot.schedules as Record<string, unknown>[];
    expect(
      schedules.filter(
        (row) =>
          row.schedule_ref === item.scheduleRef && row.role_code === 'envelope',
      ),
      'converted original Activity envelope identity',
    ).toHaveLength(1);
    return;
  }
  const read = (await serverRead(
    page,
    '/api/v1/temporal/timeline/window?start_date=' +
      day +
      '&end_date_exclusive=' +
      dateAfter(day, 1),
  )) as Record<string, unknown>;
  expect(read.kind).toBe('window');
  const items = read.items as readonly Record<string, unknown>[];
  expect(
    items.filter((row) => row.schedule_ref === item.scheduleRef),
    'converted original Event Schedule identity',
  ).toHaveLength(1);
}

async function readActivityPlacements(
  page: Page,
  day: string,
  expectedTitle: string,
  expectedCount: number,
): Promise<readonly Record<string, unknown>[]> {
  const window = (await serverRead(
    page,
    '/api/v1/temporal/timeline/window?start_date=' +
      day +
      '&end_date_exclusive=' +
      dateAfter(day, 1),
  )) as Record<string, unknown>;
  expect(window.kind).toBe('window');
  const rows = (window.items as Record<string, unknown>[]).filter(
    (row) =>
      row.kind === 'scheduled_activity' &&
      row.title === expectedTitle &&
      String(row.starts_local_at ?? row.start_date).startsWith(day),
  );
  expect(
    rows,
    'physical interval placements for ' + expectedTitle,
  ).toHaveLength(expectedCount);
  expect(
    new Set(rows.map((row) => row.activity_ref)).size,
    'one logical Activity despite multiple intervals',
  ).toBe(1);
  expect(
    new Set(rows.map((row) => row.schedule_ref)).size,
    'distinct canonical Schedule for each interval',
  ).toBe(expectedCount);
  return rows;
}

async function occurrence(
  page: Page,
  day: string,
  sourceRef: string,
): Promise<Record<string, unknown>> {
  const end = dateAfter(day, 1);
  const window = (await serverRead(
    page,
    '/api/v1/temporal/timeline/window?start_date=' +
      day +
      '&end_date_exclusive=' +
      end,
  )) as Record<string, unknown>;
  expect(window.kind).toBe('window');
  const rows = window.items as Record<string, unknown>[];
  const matching = rows.filter(
    (row) =>
      row.source_native_ref === sourceRef && row.occurrence_ref !== undefined,
  );
  expect(matching, 'unique canonical occurrence on ' + day).toHaveLength(1);
  expect(matching[0]!.occurrence_ref).toEqual(expect.stringMatching(UUID));
  return matching[0]!;
}

async function assertRecurringTruth(
  page: Page,
  day: string,
  sourceRef: string,
  truth: PersonaTruth,
  persona: PersonaCase,
): Promise<void> {
  if (persona.kind === 'activity') {
    // Routine occurrences materialize ordinary Activities with multiple
    // physical interval Schedules, NOT scheduled_occurrence timeline rows.
    const rows = await readActivityPlacements(
      page,
      day,
      truth.title,
      Math.max(1, persona.intervalCount),
    );
    const materializedActivityRef = String(rows[0]!.activity_ref);
    expect(materializedActivityRef).toEqual(expect.stringMatching(UUID));
    const snapshot = (await serverRead(
      page,
      '/api/v1/temporal/activities/' +
        materializedActivityRef +
        '/edit-snapshot',
    )) as Record<string, unknown>;
    const objectives = snapshot.objectives as Record<string, unknown>[];
    expect(
      objectives.map((item) => item.label),
      'persisted recurring Activity Objective order for ' + persona.id,
    ).toEqual(truth.objectives.map((item) => item.label));
    const schedules = snapshot.schedules as Record<string, unknown>[];
    expect(
      schedules
        .filter((row) => row.role_code === 'planned')
        .map((row) => row.display_name),
      'recurring planned Sessions',
    ).toEqual(truth.sessions);
    // The first ordinary placement can be represented by the envelope
    // rather than an explicit role_code=interval. Compare physical Schedule
    // identities across the Timeline and the edit snapshot instead of
    // falsely requiring every visible card to carry the "interval" role.
    const placedRefs = rows.map((row) => String(row.schedule_ref));
    const persistedPlacements = schedules.filter(
      (row) =>
        placedRefs.includes(String(row.schedule_ref)) &&
        (row.role_code === 'envelope' || row.role_code === 'interval'),
    );
    expect(
      persistedPlacements.map((row) => String(row.schedule_ref)).sort(),
      'every displayed recurring Activity Schedule has its own canonical snapshot row',
    ).toEqual([...placedRefs].sort());
    // All-day Activities have no explicit interval, but still carry one
    // physical envelope Schedule. Zero authored intervals does not mean
    // zero persisted Timeline placements.
    const expectedPhysicalCount = persona.allDay
      ? 1
      : truth.expectedIntervalCount;
    expect(
      persistedPlacements,
      'exact physical interval identity mapping',
    ).toHaveLength(expectedPhysicalCount);
    expect(snapshot.life_area_ref ?? null, 'recurring Activity Life Area').toBe(
      truth.areaRef,
    );
    return;
  }
  const current = await occurrence(page, day, sourceRef);
  const ref = String(current.occurrence_ref);
  const loaded = (await serverRead(
    page,
    '/api/v1/temporal/occurrences/' + ref + '/series-edit-source',
  )) as Record<string, unknown>;
  expect(loaded.source_native_ref).toBe(sourceRef);
  const structure = loaded.structure_snapshot as Record<string, unknown>;
  // Activity takes the early return and checks its materialized snapshot.
  // Only Event source snapshots reach this branch.
  const objectives = structure.objectives as Record<string, unknown>[];
  expect(
    objectives.map((item) => item.label),
    'persisted recurring Objective order for ' + persona.id,
  ).toEqual(truth.objectives.map((item) => item.label));
  expect(structure.agenda_parts, 'persisted recurring Event agenda').toEqual(
    truth.agenda,
  );
  expect(
    structure.life_area_ref ?? null,
    'persisted recurring Event Life Area',
  ).toBe(truth.areaRef);
}

async function seriesRevision(
  page: Page,
  day: string,
  originalTitle: string,
  nextTitle: string,
  persona: PersonaCase,
  originalTruth: PersonaTruth,
  fromNext = false,
): Promise<PersonaTruth> {
  const inspector = await openEdit(page, day, originalTitle);
  const scope = page.getByRole('dialog', { name: 'Modifica ricorrenza' });
  await scope
    .getByRole('button', {
      name: fromNext ? 'Dalla prossima istanza' : 'Questa e le successive',
    })
    .click();
  await inspector.getByRole('textbox', { name: 'Titolo' }).fill(nextTitle);
  const changedGoals = [...originalTruth.objectives];
  const revisedGoal = {
    ...changedGoals[0]!,
    label: changedGoals[0]!.label + ' serie',
  };
  await inspector
    .locator('[data-create-objective]')
    .first()
    .getByRole('textbox', { name: 'Nome obiettivo' })
    .fill(revisedGoal.label);
  changedGoals[0] = revisedGoal;
  const removedObjective = changedGoals.pop()!;
  await inspector
    .locator('[data-create-objective]')
    .last()
    .getByRole('button', { name: 'Rimuovi obiettivo' })
    .click();
  await inspector.getByRole('button', { name: '+ Obiettivo' }).click();
  const newObjective = {
    label: nextTitle + ' obiettivo nuovo',
    kind: 'boolean' as const,
    target: null,
    minimum: null,
    maximum: null,
    verification: 'none' as const,
  };
  await inspector
    .locator('[data-create-objective]')
    .last()
    .getByRole('textbox', { name: 'Nome obiettivo' })
    .fill(newObjective.label);
  changedGoals.push(newObjective);
  expect(removedObjective.label).not.toBe(newObjective.label);
  const agenda = [...originalTruth.agenda];
  const sessions = [...originalTruth.sessions];
  if (persona.kind === 'event') {
    const revised = agenda[0]! + ' serie';
    await inspector
      .getByRole('textbox', { name: 'Punto scaletta 1', exact: true })
      .fill(revised);
    agenda[0] = revised;
    await inspector
      .locator('[data-temporal-create-agenda-part]')
      .last()
      .getByRole('button', { name: 'Rimuovi punto' })
      .click();
    agenda.pop();
    await inspector
      .getByRole('button', { name: 'Aggiungi punto alla scaletta' })
      .click();
    const appended = nextTitle + ' scaletta nuova';
    await inspector
      .getByRole('textbox', {
        name: 'Punto scaletta ' + (agenda.length + 1),
      })
      .fill(appended);
    agenda.push(appended);
  } else {
    const revised = sessions[0]! + ' serie';
    await inspector
      .getByRole('textbox', { name: 'Nome Sessione 1' })
      .fill(revised);
    sessions[0] = revised;
    await inspector
      .locator('.temporal-create-tree-item.is-session')
      .last()
      .getByRole('button', { name: /^Rimuovi Sessione \d+$/ })
      .click();
    sessions.pop();
    await inspector
      .locator('.temporal-create-activity-tree__root-actions')
      .getByRole('button', { name: 'Sessione', exact: true })
      .click();
    const appended = nextTitle + ' Sessione nuova';
    await inspector
      .getByRole('textbox', {
        name: 'Nome Sessione ' + (sessions.length + 1),
      })
      .fill(appended);
    sessions.push(appended);
  }
  const areaName = nextTitle + ' nuova area';
  await inspector
    .getByRole('textbox', { name: 'Area assegnata' })
    .fill(areaName);
  await expect(
    inspector.getByText(
      'La nuova Life Area sarà creata insieme al salvataggio della serie.',
    ),
  ).toBeVisible();
  await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
  const confirmation = page.getByRole('dialog', {
    name: 'Controlla prima di salvare',
  });
  await expect(confirmation).toBeVisible();
  const accepted = page.waitForResponse(
    (response) =>
      response.url().endsWith('/series-edit') &&
      response.request().method() === 'POST',
  );
  await confirmation
    .getByRole('button', { name: 'Conferma salvataggio' })
    .click();
  const response = await accepted;
  expect(response.status(), 'series edit must succeed').toBe(200);
  await expect(confirmation).toHaveCount(0);
  const areas = (await serverRead(
    page,
    '/api/v1/temporal/life-areas',
  )) as readonly Record<string, unknown>[];
  const matching = areas.filter((area) => area.name === areaName);
  expect(
    matching,
    'exactly one transactional recurring Life Area',
  ).toHaveLength(1);
  return {
    ...originalTruth,
    title: nextTitle,
    areaName,
    areaRef: String(matching[0]!.life_area_ref),
    objectives: changedGoals,
    agenda,
    sessions,
  };
}

async function recolorExistingSeriesArea(
  page: Page,
  day: string,
  title: string,
  truth: PersonaTruth,
): Promise<void> {
  expect(truth.areaRef, 'precondition: assigned existing Life Area').toEqual(
    expect.stringMatching(UUID),
  );
  const originalCatalog = (await serverRead(
    page,
    '/api/v1/temporal/life-areas',
  )) as readonly Record<string, unknown>[];
  const originalArea = originalCatalog.filter(
    (area) => area.life_area_ref === truth.areaRef,
  );
  expect(
    originalArea,
    'one existing Life Area before global recolor',
  ).toHaveLength(1);
  const originalColor = String(originalArea[0]!.color_code).toUpperCase();
  expect(originalColor).toMatch(/^#[0-9A-F]{6}$/);
  const newColor = originalColor === '#FFD600' ? '#4285F4' : '#FFD600';
  const newColorName = newColor === '#4285F4' ? 'Blu' : 'Giallo';
  expect(newColor).not.toBe(originalColor);
  const editor = await openEdit(page, day, title);
  await page
    .getByRole('dialog', { name: 'Modifica ricorrenza' })
    .getByRole('button', { name: 'Questa e le successive' })
    .click();
  const areaColorButton = editor.getByRole('button', {
    name: 'Colore Life Area',
  });
  await expect(areaColorButton).toBeEnabled();
  await areaColorButton.click();
  const picker = page.getByRole('dialog', { name: 'Scegli colore' });
  await expect(picker).toBeVisible();
  await picker
    .getByRole('button', {
      name: newColorName,
      exact: true,
    })
    .click();
  await expect(
    editor.getByText(/Modificare il colore della Life Area aggiorna/),
  ).toBeVisible();
  await editor.getByRole('button', { name: 'Salva modifiche' }).click();
  const review = page.getByRole('dialog', {
    name: 'Controlla prima di salvare',
  });
  await expect(review).toBeVisible();
  const accepted = page.waitForResponse(
    (response) =>
      response.url().endsWith('/series-edit') &&
      response.request().method() === 'POST',
  );
  await review.getByRole('button', { name: 'Conferma salvataggio' }).click();
  const response = await accepted;
  expect(response.status(), 'Life Area series edit must succeed').toBe(200);
  const catalog = (await serverRead(
    page,
    '/api/v1/temporal/life-areas',
  )) as readonly Record<string, unknown>[];
  const persisted = catalog.filter(
    (area) => area.life_area_ref === truth.areaRef,
  );
  expect(persisted).toHaveLength(1);
  expect(persisted[0]!.color_code).toBe(newColor);
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
  await inspector
    .getByRole('textbox', {
      name: kind === 'event' ? 'Titolo Event' : 'Titolo',
    })
    .fill(changedTitle);
  // The Activity submit button changes its accessible name to "Salvataggio…"
  // immediately on submission. Waiting for "Salva modifiche" to disappear
  // proves only that the request STARTED, not that PostgreSQL accepted it.
  // Navigating at that point can abort the actual atomic PUT. Observe the
  // precise mutation response and the editor closing before reloading Home.
  if (kind === 'event') {
    await inspector.getByRole('button', { name: 'Salva modifiche' }).click();
    await expect(inspector.getByText('Evento aggiornato.')).toBeVisible({
      timeout: 15_000,
    });
  } else {
    const isAtomicActivityEdit = (url: string, method: string) =>
      method === 'PUT' &&
      url.includes('/api/v1/temporal/activities/') &&
      url.endsWith('/atomic-edit');
    let started = false;
    let failed: string | null = null;
    const onRequest = (request: import('@playwright/test').Request) => {
      if (isAtomicActivityEdit(request.url(), request.method())) {
        started = true;
      }
    };
    const onRequestFailed = (request: import('@playwright/test').Request) => {
      if (isAtomicActivityEdit(request.url(), request.method())) {
        failed = request.failure()?.errorText ?? 'unknown transport error';
      }
    };
    page.on('request', onRequest);
    page.on('requestfailed', onRequestFailed);
    const saveButton = inspector.getByRole('button', {
      name: 'Salva modifiche',
    });
    try {
      await expect(
        saveButton,
        'Activity editor must be ready before Save',
      ).toBeEnabled({ timeout: 5_000 });
      const [accepted] = await Promise.all([
        page.waitForResponse(
          (response) =>
            isAtomicActivityEdit(response.url(), response.request().method()),
          { timeout: 12_000 },
        ),
        saveButton.click(),
      ]);
      expect(
        accepted.status(),
        'Activity occurrence edit must commit: ' + (await accepted.text()),
      ).toBe(200);
      await expect(
        inspector.locator('form.timeline-activity-editor'),
        'Activity editor must finish saving before Timeline navigation',
      ).toHaveCount(0, { timeout: 15_000 });
    } catch (reason) {
      const alerts = await inspector
        .locator('[role="alert"]')
        .allTextContents()
        .catch(() => []);
      const invalidFields = await inspector
        .locator('[aria-invalid="true"]')
        .evaluateAll((nodes) =>
          nodes.map(
            (node) =>
              node.getAttribute('aria-label') ??
              node.getAttribute('name') ??
              'unnamed',
          ),
        )
        .catch(() => []);
      throw new Error(
        'Activity local edit did not commit: PUT started=' +
          started +
          '; failed=' +
          failed +
          '; alerts=' +
          JSON.stringify(alerts) +
          '; invalidFields=' +
          JSON.stringify(invalidFields),
        { cause: reason },
      );
    } finally {
      page.off('request', onRequest);
      page.off('requestfailed', onRequestFailed);
    }
  }
  await assertCard(page, day, changedTitle);
}

async function deleteRecurringAndProveNoResurrection(
  page: Page,
  selectedDay: string,
  laterDay: string,
  earlierDay: string,
  originalTitle: string,
  currentTitle: string,
  kind: PersonaCase['kind'],
  laterTitle = currentTitle,
): Promise<void> {
  const card = await assertCard(page, selectedDay, currentTitle);
  await clickCard(card, currentTitle);
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  const deletionButton = kind === 'event' ? 'Elimina Event' : 'Elimina';
  await inspector
    .getByRole('button', { name: deletionButton, exact: true })
    .click();
  const dialog = page.getByRole('alertdialog', {
    name: kind === 'event' ? 'Elimina evento' : 'Elimina attività',
  });
  await expect(
    dialog.getByRole('button', { name: 'Solo questa istanza' }),
  ).toBeVisible();
  await expect(
    dialog.getByRole('button', { name: 'Tutta la serie' }),
  ).toBeVisible();
  await dialog.getByRole('button', { name: 'Annulla' }).click();
  await expect(dialog).toHaveCount(0);
  await inspector
    .getByRole('button', { name: deletionButton, exact: true })
    .click();
  const removed = page.waitForResponse(
    (response) =>
      response.request().method() === 'DELETE' &&
      response.url().includes('/api/v1/temporal/hard-deletion/'),
  );
  await dialog.getByRole('button', { name: 'Solo questa istanza' }).click();
  expect((await removed).status()).toBe(200);
  await expect(dialog).toHaveCount(0);
  await openHome(page, selectedDay);
  await expect(onDay(page, selectedDay, currentTitle)).toHaveCount(0);
  await assertCard(page, laterDay, laterTitle);
  await openHome(page, selectedDay);
  await expect(onDay(page, selectedDay, currentTitle)).toHaveCount(0);

  const future = await assertCard(page, laterDay, laterTitle);
  await clickCard(future, laterTitle);
  await inspector
    .getByRole('button', { name: deletionButton, exact: true })
    .click();
  // Whole-series deletion atomically removes every materialized Activity
  // lifecycle graph; the ordinary 15s click timeout is too short for this
  // intentionally bounded, destructive database transaction. Await the
  // actual HTTP response, never infer success from dialog disappearance.
  const removedSeries = page.waitForResponse(
    (response) =>
      response.request().method() === 'DELETE' &&
      response.url().includes('/api/v1/temporal/hard-deletion/'),
    { timeout: 90_000 },
  );
  await dialog.getByRole('button', { name: 'Tutta la serie' }).click();
  const seriesResponse = await removedSeries;
  const failureBody =
    seriesResponse.status() === 200
      ? ''
      : await Promise.race([
          seriesResponse.text().catch(() => 'response body unavailable'),
          new Promise<string>((resolve) => {
            setTimeout(
              () => resolve('response body timed out after 3s'),
              3_000,
            );
          }),
        ]);
  expect(
    seriesResponse.status(),
    `Whole-series DELETE returned HTTP ${seriesResponse.status()}: ${failureBody}`,
  ).toBe(200);
  await expect(dialog).toHaveCount(0);
  await openHome(page, laterDay);
  await expect(onDay(page, laterDay, laterTitle)).toHaveCount(0);
  await expect(onDay(page, laterDay, currentTitle)).toHaveCount(0);
  await openHome(page, selectedDay);
  await expect(onDay(page, selectedDay, currentTitle)).toHaveCount(0);
  await openHome(page, earlierDay);
  await expect(onDay(page, earlierDay, originalTitle)).toHaveCount(0);
}

// Fail a missing or disabled UI action promptly with the exact locator.
// The 300-second journey deadline still covers legitimate multi-step work.
test.use({ actionTimeout: 15_000, navigationTimeout: 15_000 });

test.describe('Temporal v2 — real stateful user personas', () => {
  test.describe.configure({ timeout: 300_000 });

  // Phase 1: forty distinct independent subjects, each with multiple fields,
  // a successive destructive/edit mutation, full reload, duplicate and delete.
  for (const [ordinal, persona] of PERSONA_CASES.entries()) {
    test(
      'V2-P1-' + persona.id + ' rich create → mutate → duplicate → delete',
      async ({ browser }, info) => {
        const user = await signedInPersona(browser, info, ordinal);
        const { page } = user;
        registerPersona(page, persona);
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
            persona.id + '/2 Create from production UI',
            async () => authorPersona(page, persona, title, day),
          );
          await test.step(
            persona.id + '/3 Canonical full readback',
            async () => {
              await openHome(page, day);
              await assertOneOffTruth(page, authored);
            },
          );
          const updated = await test.step(
            persona.id + '/4 Edit, remove and add nested data',
            async () => editOneOff(page, day, authored),
          );
          const reassigned = await test.step(
            persona.id + '/5 Reassign area, reload, cancel an unsaved edit',
            async () => reassignAreaAndCancel(page, day, updated),
          );
          const copy = await test.step(
            persona.id + '/6 Duplicate the FINAL state, not initial',
            async () => duplicateAndCompare(page, day, reassigned),
          );
          await test.step(
            persona.id + '/7 Delete original; duplicate survives',
            async () => {
              await deleteOneOff(page, day, reassigned.item);
              await assertOneOffTruth(page, {
                ...reassigned,
                item: copy,
                truth: { ...reassigned.truth, title: copy.title },
              });
            },
          );
          if (ordinal % 4 === 0) {
            await test.step(
              persona.id +
                '/8 Save to Draft Vault without copied runtime facts',
              async () =>
                draftAndVerify(page, day, copy, {
                  ...reassigned.truth,
                  title: copy.title,
                }),
            );
          }
        } finally {
          await user.close();
        }
      },
    );
  }

  // Phase 2: forty native recurring sources built with the same rich matrix.
  // Source, local exception and future revision are separate server operations.
  for (const [index, persona] of PERSONA_CASES.entries()) {
    test(
      'V2-P2-' + persona.id + ' native series → local → following',
      async ({ browser }, info) => {
        const user = await signedInPersona(browser, info, 40 + index);
        const { page } = user;
        registerPersona(page, persona);
        const day = scenarioDate(5);
        const recurrence = recurrenceFor(persona);
        const future = nextOccurrence(day, recurrence);
        const title = uniqueTitle('v2 serie ' + persona.id);
        await info.attach('scenario', {
          body: Buffer.from(
            JSON.stringify(
              {
                phase: 2,
                persona,
                recurrence,
                day,
                future,
              },
              null,
              2,
            ),
          ),
          contentType: 'application/json',
        });
        try {
          await openHome(page, day);
          const authored = await test.step(
            persona.id + '/1 Create rich native series',
            async () => authorPersona(page, persona, title, day, recurrence),
          );
          await test.step(
            persona.id + '/2 Initial and future readback',
            async () => {
              await assertCard(page, day, title);
              await assertRecurringTruth(
                page,
                day,
                authored.item.sourceRef,
                authored.truth,
                persona,
              );
              await assertCard(page, future, title);
              await assertRecurringTruth(
                page,
                future,
                authored.item.sourceRef,
                authored.truth,
                persona,
              );
            },
          );
          // Finite series have a real final boundary. Exercise it before any
          // scope split, then prove it stays a protected exception after edits
          // from first, middle and the following segment.
          const finalDay =
            recurrence.repeatCount === null
              ? null
              : Array.from({
                  length: recurrence.repeatCount - 1,
                }).reduce<string>(
                  (date) => nextOccurrence(date, recurrence),
                  day,
                );
          const finalTitle = title + ' ultima istanza';
          if (finalDay) {
            await test.step(
              persona.id + '/2B Final occurrence is editable and bounded',
              async () => {
                await assertCard(page, finalDay, title);
                await assertDayHasNoDuplicatePlacements(
                  page,
                  finalDay,
                  title,
                  title,
                  persona,
                );
                await localRevision(
                  page,
                  finalDay,
                  title,
                  persona.kind,
                  finalTitle,
                );
                await assertCard(page, finalDay, finalTitle);
                await assertDayHasNoDuplicatePlacements(
                  page,
                  finalDay,
                  title,
                  finalTitle,
                  persona,
                );
                const beyondLast = nextOccurrence(finalDay, recurrence);
                await openHome(page, beyondLast);
                await expect(
                  onDay(page, beyondLast, title),
                  'bounded recurrence must not create a sixth instance',
                ).toHaveCount(0);
              },
            );
          }
          const localTitle = title + ' solo questa';
          await test.step(
            persona.id + '/3 Local exception on initial instance',
            async () => {
              await localRevision(page, day, title, persona.kind, localTitle);
              await assertCard(page, future, title);
              await assertCard(page, day, localTitle);
              await assertDayHasNoDuplicatePlacements(
                page,
                day,
                title,
                localTitle,
                persona,
              );
              if (finalDay) {
                await assertDayHasNoDuplicatePlacements(
                  page,
                  finalDay,
                  title,
                  finalTitle,
                  persona,
                );
              }
            },
          );
          if (persona.area === 'existing') {
            await test.step(
              persona.id + '/4 Change assigned Life Area global color',
              async () => {
                await recolorExistingSeriesArea(
                  page,
                  future,
                  title,
                  authored.truth,
                );
                await assertCard(page, day, localTitle);
                await assertRecurringTruth(
                  page,
                  future,
                  authored.item.sourceRef,
                  authored.truth,
                  persona,
                );
              },
            );
          }
          const revisedTitle = title + ' questa e successive';
          const followingTruth = await test.step(
            persona.id + '/5 Following-series revision',
            async () => {
              const revisedTruth = await seriesRevision(
                page,
                future,
                title,
                revisedTitle,
                persona,
                authored.truth,
              );
              await assertCard(page, future, revisedTitle);
              await assertRecurringTruth(
                page,
                future,
                authored.item.sourceRef,
                revisedTruth,
                persona,
              );
              const later = nextOccurrence(future, recurrence);
              await assertCard(page, later, revisedTitle);
              await assertRecurringTruth(
                page,
                later,
                authored.item.sourceRef,
                revisedTruth,
                persona,
              );
              await assertCard(page, day, localTitle);
              await expect(onDay(page, day, revisedTitle)).toHaveCount(0);
              await assertDayHasNoDuplicatePlacements(
                page,
                future,
                title,
                revisedTitle,
                persona,
              );
              if (finalDay) {
                await assertDayHasNoDuplicatePlacements(
                  page,
                  finalDay,
                  title,
                  finalTitle,
                  persona,
                );
              }
              if (persona.kind === 'activity') {
                await readActivityPlacements(
                  page,
                  day,
                  localTitle,
                  Math.max(1, persona.intervalCount),
                );
              } else {
                const earlier = await occurrence(
                  page,
                  day,
                  authored.item.sourceRef,
                );
                expect(earlier.title, 'local exception must be protected').toBe(
                  localTitle,
                );
              }
              return revisedTruth;
            },
          );
          const middle = nextOccurrence(future, recurrence);
          const later = nextOccurrence(middle, recurrence);
          const anotherLocal = revisedTitle + ' eccezione intermedia';
          const fromNextTitle = revisedTitle + ' dalla prossima';
          await test.step(
            persona.id + '/6 Another local exception, then FROM NEXT',
            async () => {
              await localRevision(
                page,
                middle,
                revisedTitle,
                persona.kind,
                anotherLocal,
              );
              await assertCard(page, future, revisedTitle);
              if (persona.kind === 'activity') {
                await readActivityPlacements(
                  page,
                  middle,
                  anotherLocal,
                  Math.max(1, persona.intervalCount),
                );
              } else {
                const current = await occurrence(
                  page,
                  middle,
                  authored.item.sourceRef,
                );
                expect(current.title).toBe(anotherLocal);
              }
              // This is the previously modified selected instance: choosing
              // "Dalla prossima istanza" must EXCLUDE the selected boundary.
              const nextTruth = await seriesRevision(
                page,
                middle,
                anotherLocal,
                fromNextTitle,
                persona,
                followingTruth,
                true,
              );
              await assertCard(page, middle, anotherLocal);
              await expect(onDay(page, middle, fromNextTitle)).toHaveCount(0);
              await assertCard(page, later, fromNextTitle);
              await assertRecurringTruth(
                page,
                later,
                authored.item.sourceRef,
                nextTruth,
                persona,
              );
              await assertCard(page, future, revisedTitle);
              await assertCard(page, day, localTitle);
            },
          );
          if (finalDay) {
            await test.step(
              persona.id +
                '/7 Final exception survives edits of first and middle',
              async () => {
                await assertCard(page, finalDay, finalTitle);
                await assertDayHasNoDuplicatePlacements(
                  page,
                  finalDay,
                  title,
                  finalTitle,
                  persona,
                );
                await assertDayHasNoDuplicatePlacements(
                  page,
                  later,
                  title,
                  fromNextTitle,
                  persona,
                );
                await assertDayHasNoDuplicatePlacements(
                  page,
                  middle,
                  title,
                  anotherLocal,
                  persona,
                );
                await assertDayHasNoDuplicatePlacements(
                  page,
                  day,
                  title,
                  localTitle,
                  persona,
                );
                await assertNoOccurrenceBeyondFiniteEnd(
                  page,
                  finalDay,
                  recurrence,
                  title,
                );
              },
            );
          }
          await test.step(
            persona.id + '/8 Delete single → checkpoint → whole series',
            async () => {
              await deleteRecurringAndProveNoResurrection(
                page,
                later,
                finalDay ?? nextOccurrence(later, recurrence),
                day,
                localTitle,
                revisedTitle + ' dalla prossima',
                persona.kind,
                finalDay ? finalTitle : revisedTitle + ' dalla prossima',
              );
            },
          );
        } finally {
          await user.close();
        }
      },
    );
  }

  // Phase 3: twenty rich one-offs become recurring through Edit.
  // Unlike a native series, original physical identity must be retained.
  for (const [index, persona] of [
    ...EVENT_CASES.slice(0, 10),
    ...ACTIVITY_CASES.slice(0, 10),
  ].entries()) {
    test(
      'V2-P3-' + persona.id + ' one-off → series → scoped edits',
      async ({ browser }, info) => {
        const user = await signedInPersona(browser, info, 80 + index);
        const { page } = user;
        registerPersona(page, persona);
        const day = scenarioDate(5);
        const title = uniqueTitle('v2 conversione ' + persona.id);
        await info.attach('scenario', {
          body: Buffer.from(JSON.stringify({ phase: 3, persona }, null, 2)),
          contentType: 'application/json',
        });
        try {
          await openHome(page, day);
          const authored = await test.step(
            persona.id + '/1 Rich ordinary source',
            async () => authorPersona(page, persona, title, day),
          );
          await test.step(
            persona.id + '/2 Read full source state',
            async () => {
              await assertOneOffTruth(page, authored);
            },
          );
          let seriesSourceRef = authored.item.sourceRef;
          await test.step(
            persona.id + '/3 Convert through real Edit',
            async () => {
              const editor = await openEdit(page, day, title);
              const recurrence = editor.getByRole('region', {
                name: 'Ripetizione',
                exact: true,
              });
              await recurrence
                .getByRole('combobox', { name: 'Ripeti' })
                .selectOption('daily');
              const conversion = page.waitForResponse(
                (response) =>
                  response.request().method() === 'POST' &&
                  response
                    .url()
                    .endsWith(
                      '/api/v1/temporal/recurring/' +
                        (persona.kind === 'event' ? 'events/' : 'activities/') +
                        authored.item.sourceRef +
                        '/start',
                    ),
              );
              await editor
                .getByRole('button', { name: 'Salva modifiche' })
                .click();
              expect((await conversion).status()).toBe(200);
              if (persona.kind === 'event') {
                // Conversion preserves the physical first Event but creates a
                // distinct canonical recurring Event source. The original
                // one-off Event ref is NOT its future occurrence source ref.
                const seed = await serverRead(
                  page,
                  '/api/v1/temporal/recurring/events/' +
                    authored.item.sourceRef +
                    '/seed',
                );
                expect(seed).toEqual(expect.stringMatching(UUID));
                seriesSourceRef = String(seed);
                expect(seriesSourceRef).not.toBe(authored.item.sourceRef);
              }
              const originalCard = await assertCard(page, day, title);
              await expect(originalCard).toBeVisible();
              await assertOriginalScheduleIdentity(page, day, authored.item);
              await assertCard(page, dateAfter(day, 1), title);
            },
          );
          const firstTitle = title + ' prima istanza';
          await test.step(
            persona.id +
              '/4 Edit ORIGINAL physical first instance after conversion',
            async () => {
              // This was the formerly untested user trigger. A duplicate
              // generated card and/or a replaced original Schedule must RED.
              await localRevision(page, day, title, persona.kind, firstTitle);
              await assertOriginalScheduleIdentity(page, day, authored.item);
              await assertDayHasNoDuplicatePlacements(
                page,
                day,
                title,
                firstTitle,
                persona,
              );
              // A substring DOM selector would also match firstTitle;
              // the canonical exact-title assertion above is authoritative.
              await assertCard(page, dateAfter(day, 1), title);
              await assertDayHasNoDuplicatePlacements(
                page,
                dateAfter(day, 1),
                title,
                title,
                persona,
              );
            },
          );
          await test.step(
            persona.id + '/5 Edit generated future instance independently',
            async () => {
              await localRevision(
                page,
                dateAfter(day, 1),
                title,
                persona.kind,
                title + ' locale',
              );
              await assertCard(page, day, firstTitle);
              await assertDayHasNoDuplicatePlacements(
                page,
                day,
                title,
                firstTitle,
                persona,
              );
              await assertDayHasNoDuplicatePlacements(
                page,
                dateAfter(day, 1),
                title,
                title + ' locale',
                persona,
              );
              await assertCard(page, dateAfter(day, 2), title);
            },
          );
          await test.step(
            persona.id +
              '/6 Future revision preserves physical first and local exception',
            async () => {
              const updatedTruth = await seriesRevision(
                page,
                dateAfter(day, 2),
                title,
                title + ' futuro',
                persona,
                authored.truth,
              );
              await assertCard(page, dateAfter(day, 2), title + ' futuro');
              await assertRecurringTruth(
                page,
                dateAfter(day, 2),
                seriesSourceRef,
                updatedTruth,
                persona,
              );
              await assertCard(page, dateAfter(day, 3), title + ' futuro');
              await assertCard(page, dateAfter(day, 1), title + ' locale');
              const first = await assertCard(page, day, firstTitle);
              await expect(first).toBeVisible();
              await assertOriginalScheduleIdentity(page, day, authored.item);
              for (const [checkedDay, checkedTitle] of [
                [day, firstTitle],
                [dateAfter(day, 1), title + ' locale'],
                [dateAfter(day, 2), title + ' futuro'],
                [dateAfter(day, 3), title + ' futuro'],
                [dateAfter(day, 4), title + ' futuro'],
              ] as const) {
                await assertDayHasNoDuplicatePlacements(
                  page,
                  checkedDay,
                  title,
                  checkedTitle,
                  persona,
                );
              }
            },
          );
          await test.step(
            persona.id + '/7 Delete generated instance and converted series',
            async () => {
              await deleteRecurringAndProveNoResurrection(
                page,
                dateAfter(day, 2),
                dateAfter(day, 3),
                day,
                firstTitle,
                title + ' futuro',
                persona.kind,
              );
            },
          );
        } finally {
          await user.close();
        }
      },
    );
  }

  // Focused regression for the reported first-day duplicate after converting
  // an ordinary Event and immediately editing "This and following" from the
  // ORIGINAL physical first Event. P3-E01 only used "Only this" on day one.
  test('V2-P3-EFIRST converted first Event following-edit has one card', async ({
    browser,
  }, info) => {
    const persona = EVENT_CASES[0]!;
    const user = await signedInPersona(browser, info, 102);
    const { page } = user;
    registerPersona(page, persona);
    const day = scenarioDate(5);
    const nextDay = dateAfter(day, 1);
    const title = uniqueTitle('v2 prima Event senza doppioni');
    const editedTitle = title + ' modificato dalla prima';
    try {
      await openHome(page, day);
      const authored = await authorPersona(page, persona, title, day);
      const editor = await openEdit(page, day, title);
      await editor
        .getByRole('region', { name: 'Ripetizione', exact: true })
        .getByRole('combobox', { name: 'Ripeti' })
        .selectOption('daily');
      const conversion = page.waitForResponse(
        (response) =>
          response.request().method() === 'POST' &&
          response
            .url()
            .endsWith(
              '/api/v1/temporal/recurring/events/' +
                authored.item.sourceRef +
                '/start',
            ),
      );
      await editor.getByRole('button', { name: 'Salva modifiche' }).click();
      expect(
        (await conversion).status(),
        'first Event conversion accepted',
      ).toBe(200);

      await assertOriginalScheduleIdentity(page, day, authored.item);
      await assertDayHasNoDuplicatePlacements(page, day, title, title, persona);
      await assertCard(page, nextDay, title);

      const firstEditor = await openEdit(page, day, title);
      await page
        .getByRole('dialog', { name: 'Modifica ricorrenza' })
        .getByRole('button', { name: 'Questa e le successive' })
        .click();
      await firstEditor
        .getByRole('textbox', { name: 'Titolo' })
        .fill(editedTitle);
      await firstEditor
        .getByRole('textbox', { name: 'Punto scaletta 1', exact: true })
        .fill(title + ' scaletta aggiornata');
      await firstEditor
        .getByRole('button', { name: 'Salva modifiche' })
        .click();
      const confirmation = page.getByRole('dialog', {
        name: 'Controlla prima di salvare',
      });
      await expect(confirmation).toBeVisible();
      const accepted = page.waitForResponse(
        (response) =>
          response.request().method() === 'POST' &&
          response.url().endsWith('/series-edit'),
      );
      await confirmation
        .getByRole('button', { name: 'Conferma salvataggio' })
        .click();
      const response = await accepted;
      expect(
        response.status(),
        'converted first Event series edit must succeed',
      ).toBe(200);

      // A NEW Home checkpoint after series Edit is essential: the duplication
      // was not observable by only reading the old stored first Event.
      await assertCard(page, day, editedTitle);
      await assertOriginalScheduleIdentity(page, day, authored.item);
      await assertDayHasNoDuplicatePlacements(
        page,
        day,
        title,
        editedTitle,
        persona,
      );
      // The first physical Event becomes an Occurrence of the series.
      // Its raw Event descriptor is NOT the user-facing effective profile:
      // the canonical Event-detail view must merge series structure and
      // selected-Occurrence overrides, exactly like later instances.
      const firstRef = await serverRead(
        page,
        '/api/v1/temporal/recurring/events/' +
          authored.item.sourceRef +
          '/first-occurrence',
      );
      expect(firstRef, 'linked first Occurrence ref').toEqual(
        expect.stringMatching(/^[\da-f-]{36}$/i),
      );
      const physicalFirst = (await serverRead(
        page,
        '/api/v1/temporal/occurrences/' + String(firstRef) + '/event-detail',
      )) as Record<string, unknown>;
      expect(physicalFirst.title, 'first effective Event title').toBe(
        editedTitle,
      );
      expect(
        physicalFirst.agenda_parts,
        'the first effective Event carries the edited Agenda',
      ).toEqual([
        title + ' scaletta aggiornata',
        ...authored.truth.agenda.slice(1),
      ]);
      const firstDayCards = page.locator(
        '[data-timeline-event][data-planned-date="' +
          day +
          '"], [data-timeline-all-day-lane="' +
          day +
          '"] [data-timeline-all-day-item]',
      );
      await expect(
        firstDayCards,
        'one rendered card, not both an old and a regenerated first Event',
      ).toHaveCount(1);
      await expect(
        firstDayCards.getByRole('button', {
          name: title,
          exact: true,
        }),
        'old unmodified first Event must not remain visible',
      ).toHaveCount(0);
      await assertCard(page, nextDay, editedTitle);
      await assertDayHasNoDuplicatePlacements(
        page,
        nextDay,
        title,
        editedTitle,
        persona,
      );
      await openHome(page, day);
      await expect(
        onDay(page, day, title),
        'the first Event must remain single after full Home reload',
      ).toHaveCount(1);

      // "Solo questa" on the physical first Event must hydrate through the
      // Occurrence-effective API. Then change it locally without changing
      // the next generated Event or creating a second first-day card.
      const localTitle = editedTitle + ' solo questa';
      const localAgenda = title + ' scaletta solo questa';
      const localEditor = await openEdit(page, day, editedTitle);
      await page
        .getByRole('dialog', { name: 'Modifica ricorrenza' })
        .getByRole('button', { name: 'Solo questa' })
        .click();
      await expect(
        localEditor.getByRole('textbox', { name: 'Titolo' }),
      ).toHaveValue(editedTitle);
      await expect(
        localEditor.getByRole('textbox', {
          name: 'Punto scaletta 1',
          exact: true,
        }),
      ).toHaveValue(title + ' scaletta aggiornata');
      await localEditor
        .getByRole('textbox', { name: 'Titolo' })
        .fill(localTitle);
      await localEditor
        .getByRole('textbox', { name: 'Punto scaletta 1', exact: true })
        .fill(localAgenda);
      const localSaved = page.waitForResponse(
        (response) =>
          response.request().method() === 'POST' &&
          response.url().endsWith('/event-local-edit'),
      );
      await localEditor
        .getByRole('button', { name: 'Salva modifiche' })
        .click();
      const saved = await localSaved;
      // Response headers arrive before the body. A rejected local-edit
      // returned HTTP 409 but waiting on response.text() blocked until the
      // *global five-minute timeout*, masking the real failure. Assert the
      // status directly so a regression fails immediately and diagnostically.
      expect(
        saved.status(),
        'converted first Event Only-this must accept the local edit',
      ).toBe(200);

      // Verify the actual post-save UI *in place*. The old assertCard()
      // navigated again before checking; Chromium's trace proved the card
      // briefly rendered with the correct local title, then a fresh
      // navigation/virtualized-day recycle removed that date from the DOM.
      // A virtualized day not present in the viewport is NOT evidence of a
      // failed local edit. This expectation still insists on exactly one
      // physical card with the newly saved title on the editing screen.
      const firstDayCardsAfterLocal = page.locator(
        '[data-timeline-event][data-planned-date="' + day + '"]',
      );
      await expect(
        firstDayCardsAfterLocal,
        'one physical first Event card after Only-this',
      ).toHaveCount(1);
      await expect(
        firstDayCardsAfterLocal.getByRole('button', {
          name: localTitle,
          exact: true,
        }),
        'the first Event exposes its full accessible title',
      ).toHaveCount(1);
      await expect(
        firstDayCardsAfterLocal.getByRole('button', {
          name: editedTitle,
          exact: true,
        }),
        'stale first-day series title must not remain',
      ).toHaveCount(0);
      await assertOriginalScheduleIdentity(page, day, authored.item);
      await assertDayHasNoDuplicatePlacements(
        page,
        day,
        title,
        localTitle,
        persona,
      );
      const effectiveLocal = (await serverRead(
        page,
        '/api/v1/temporal/occurrences/' + String(firstRef) + '/event-detail',
      )) as Record<string, unknown>;
      expect(effectiveLocal.title).toBe(localTitle);
      expect(effectiveLocal.agenda_parts).toEqual([
        localAgenda,
        ...authored.truth.agenda.slice(1),
      ]);
      await assertCard(page, nextDay, editedTitle);
      await assertDayHasNoDuplicatePlacements(
        page,
        nextDay,
        title,
        editedTitle,
        persona,
      );
    } finally {
      await user.close();
    }
  });
});
