/**
 * New independent authenticated Vault + Duplica acceptance matrix.
 * Browser UI -> canonical HTTP -> real PostgreSQL. No route interception.
 * Accounts 411..417 per browser are reserved by signedInPersona(103..109).
 * Existing E2E suites are not modified or reused as a shortcut.
 */
import { randomUUID } from 'node:crypto';

import { Temporal } from '@dante/time';
import { expect, test, type Locator, type Page } from '@playwright/test';

import {
  openHome,
  scenarioDate,
  serverRead,
  submitCreate,
  uniqueTitle,
} from './temporal-user-journey-support';
import { ACTIVITY_CASES, EVENT_CASES, recurrenceFor } from './temporal-stateful-case-matrix';
import {
  assertOneOffTruth,
  authorPersona,
  signedInPersona,
  type AuthoredPersona,
} from './temporal-stateful-journey-support';

type DraftRow = {
  draft_ref: string;
  subject_kind: 'activity' | 'event';
  title: string;
  revision: number;
  payload: Record<string, unknown>;
};
const TZ = { 'X-Dante-Time-Zone': 'Europe/Rome' };

const cardOn = (page: Page, title: string): Locator =>
  page.locator('[data-timeline-event], [data-timeline-all-day-item]')
    .filter({ hasText: title });

async function inspectorFor(page: Page, day: string, title: string): Promise<Locator> {
  await openHome(page, day);
  const card = cardOn(page, title).first();
  await expect(card).toBeVisible({ timeout: 20_000 });
  if ((await card.getAttribute('data-timeline-all-day-item')) !== null) {
    await card.click();
  } else {
    await card.getByRole('button', { name: title, exact: true }).click();
  }
  const inspector = page.locator('.timeline-event-modal[role="dialog"]');
  await expect(inspector).toBeVisible();
  return inspector;
}

async function vaultRows(page: Page): Promise<DraftRow[]> {
  return (await serverRead(page, '/api/v1/temporal/drafts')) as DraftRow[];
}

async function csrf(page: Page): Promise<string> {
  const auth = (await serverRead(page, '/api/v1/auth/session')) as {
    csrf_token: string;
  };
  expect(auth.csrf_token).toEqual(expect.any(String));
  return auth.csrf_token;
}

async function clearVault(page: Page): Promise<void> {
  const token = await csrf(page);
  for (const row of await vaultRows(page)) {
    const removed = await page.request.delete(
      '/api/v1/temporal/drafts/' + row.draft_ref +
        '?expected_revision=' + row.revision,
      { headers: { ...TZ, 'X-Dante-CSRF': token } },
    );
    expect(removed.status(), 'clean up isolated Vault fixture').toBe(204);
  }
}

async function seedDrafts(page: Page, count: number): Promise<DraftRow[]> {
  const token = await csrf(page);
  const created: DraftRow[] = [];
  for (let index = 0; index < count; index += 1) {
    const ref = randomUUID();
    const kind = index % 2 === 0 ? 'activity' : 'event';
    const title = index % 11 === 0 ? '' : 'Capienza ' + index;
    const accepted = await page.request.put(
      '/api/v1/temporal/drafts/' + ref,
      {
        headers: { ...TZ, 'X-Dante-CSRF': token },
        data: {
          draft_ref: ref,
          operation_id: randomUUID(),
          expected_revision: null,
          subject_kind: kind,
          title,
          payload: {
            version: 1,
            fields: { kind, title },
            advanced: { objectives: [], eventParticipants: [] },
            surface: 'full',
          },
        },
      },
    );
    expect(accepted.status(), 'accepted Draft #' + index).toBe(200);
    created.push((await accepted.json()) as DraftRow);
  }
  return created;
}

async function openVault(page: Page): Promise<Locator> {
  const trigger = page.getByRole('button', { name: 'Apri Bozze' });
  await expect(trigger).toBeVisible();
  if ((await trigger.getAttribute('aria-expanded')) !== 'true') {
    await trigger.click();
  }
  const vault = page.locator('[data-timeline-draft-vault="true"]');
  await expect(vault).toBeVisible();
  return vault;
}

async function expectOriginal(page: Page, authored: AuthoredPersona): Promise<void> {
  await assertOneOffTruth(page, authored);
  const endpoint = authored.item.kind === 'event'
    ? '/api/v1/temporal/events/' + authored.item.sourceRef
    : '/api/v1/temporal/activities/' + authored.item.sourceRef + '/profile';
  expect((await page.request.get(endpoint, { headers: TZ })).status()).toBe(200);
}

test.use({ actionTimeout: 15_000, navigationTimeout: 15_000 });

test.describe('Draft Vault — real comprehensive lifecycle', () => {
  test.describe.configure({ timeout: 300_000 });

  test('DV-REAL-01 Activity: multi-interval Area/colour/Session/Objectives → Duplica → Draft → Add', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 103);
    const { page } = user;
    const day = scenarioDate(6);
    const originalTitle = uniqueTitle('vault activity sorgente');
    try {
      await clearVault(page);
      await openHome(page, day);
      const original = await authorPersona(page, ACTIVITY_CASES[1]!, originalTitle, day);
      await expectOriginal(page, original);
      const inspector = await inspectorFor(page, day, originalTitle);
      await inspector.getByRole('button', { name: 'Duplica' }).click();
      const composer = page.locator('[data-temporal-create="composer"]');
      await expect(composer).toHaveAttribute('data-temporal-create-surface', 'advanced');
      await expect(composer.locator('[data-create-planned-session]')).toHaveCount(
        original.truth.sessions.length,
      );
      await expect(composer.locator('[data-create-objective]')).toHaveCount(
        original.truth.objectives.length,
      );
      const copyTitle = uniqueTitle('vault activity nuova');
      await composer.getByRole('textbox', { name: 'Titolo' }).fill(copyTitle);
      await composer.getByRole('button', { name: 'Salva bozza' }).click();
      await expect(composer).toHaveCount(0);
      const saved = (await vaultRows(page)).filter((row) => row.title === copyTitle);
      expect(saved).toHaveLength(1);
      expect(saved[0]!.subject_kind).toBe('activity');
      await expectOriginal(page, original);
      await openHome(page, day);
      const vault = await openVault(page);
      await vault.locator('article').filter({ hasText: copyTitle })
        .getByRole('button', { name: 'Riprendi' }).click();
      await expect(composer.locator('[data-create-planned-session]')).toHaveCount(
        original.truth.sessions.length,
      );
      const created = await submitCreate(page, composer, {
        kind: 'activity',
        title: copyTitle,
        recurring: false,
      });
      expect(created.sourceRef).not.toBe(original.item.sourceRef);
      expect((await vaultRows(page)).filter((row) => row.title === copyTitle)).toHaveLength(0);
      await expectOriginal(page, original);
      await assertOneOffTruth(page, {
        ...original,
        item: created,
        truth: { ...original.truth, title: copyTitle },
      });
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-02 Event: new Area, ordered Agenda, Objectives → Duplica → Draft → Add', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 104);
    const { page } = user;
    const day = scenarioDate(6);
    const originalTitle = uniqueTitle('vault evento sorgente');
    try {
      await clearVault(page);
      await openHome(page, day);
      const original = await authorPersona(page, EVENT_CASES[1]!, originalTitle, day);
      await expectOriginal(page, original);
      const inspector = await inspectorFor(page, day, originalTitle);
      await inspector.getByRole('button', { name: 'Duplica' }).click();
      const composer = page.locator('[data-temporal-create="composer"]');
      await expect(composer).toHaveAttribute('data-temporal-create-surface', 'advanced');
      await expect(composer.locator('[data-temporal-create-agenda-part]')).toHaveCount(
        original.truth.agenda.length,
      );
      await expect(composer.locator('[data-create-objective]')).toHaveCount(
        original.truth.objectives.length,
      );
      const copyTitle = uniqueTitle('vault evento nuovo');
      await composer.getByRole('textbox', { name: 'Titolo' }).fill(copyTitle);
      await composer.getByRole('button', { name: 'Salva bozza' }).click();
      await expect(composer).toHaveCount(0);
      const saved = (await vaultRows(page)).filter((row) => row.title === copyTitle);
      expect(saved).toHaveLength(1);
      expect(saved[0]!.subject_kind).toBe('event');
      await openHome(page, day);
      const vault = await openVault(page);
      await vault.locator('article').filter({ hasText: copyTitle })
        .getByRole('button', { name: 'Riprendi' }).click();
      await expect(composer.locator('[data-temporal-create-agenda-part]')).toHaveCount(
        original.truth.agenda.length,
      );
      const created = await submitCreate(page, composer, {
        kind: 'event',
        title: copyTitle,
        recurring: false,
      });
      expect(created.sourceRef).not.toBe(original.item.sourceRef);
      expect((await vaultRows(page)).filter((row) => row.title === copyTitle)).toHaveLength(0);
      await expectOriginal(page, original);
      await assertOneOffTruth(page, {
        ...original,
        item: created,
        truth: { ...original.truth, title: copyTitle },
      });
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-03 Activity: live and paused Session + planned Sessions → red Move → no runtime residue', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 105);
    const { page } = user;
    const start = Temporal.Now.zonedDateTimeISO('Europe/Rome').subtract({ minutes: 15 });
    const day = start.toPlainDate().toString();
    const clock = start.toPlainTime().toString({ smallestUnit: 'minute' });
    const title = uniqueTitle('vault sessione registrata');
    try {
      await clearVault(page);
      await openHome(page, day);
      const original = await authorPersona(
        page, ACTIVITY_CASES[0]!, title, day, undefined, true, clock,
      );
      await openHome(page, day);
      const card = cardOn(page, title).first();
      const controls = card.locator(
        '[data-timeline-session-subject="' + original.item.sourceRef + '"]',
      );
      await controls.getByRole('button', { name: 'Avvia' }).click();
      await expect(controls.getByRole('button', { name: 'Pausa' })).toBeEnabled();
      await controls.getByRole('button', { name: 'Pausa' }).click();
      const sessionsPath = '/api/v1/temporal/activities/' +
        original.item.sourceRef + '/sessions';
      await expect.poll(async () => {
        const sessions = (await serverRead(page, sessionsPath)) as
          Record<string, unknown>[];
        return sessions.some((row) => row.open === true && row.paused === true);
      }).toBe(true);

      const inspector = await inspectorFor(page, day, title);
      await inspector.getByRole('button', { name: 'Sposta in Bozze' }).click();
      const review = inspector.getByRole('region', { name: 'Sposta attività in Bozze' });
      await expect(review).toBeVisible();
      await expect(review.getByText(/eliminazione definitiva/i)).toBeVisible();
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      const loss = page.getByRole('alertdialog', { name: 'Conferma perdita registrazioni' });
      await expect(loss).toBeVisible();
      await loss.getByRole('button', { name: 'Annulla' }).click();
      expect((await page.request.get(
        '/api/v1/temporal/activities/' + original.item.sourceRef + '/profile',
        { headers: TZ },
      )).status()).toBe(200);
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      const committed = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().includes('/api/v1/temporal/drafts/move/'),
      );
      await loss.getByRole('button', { name: 'Elimina registrazioni e sposta' }).click();
      expect((await committed).status()).toBe(200);
      const saved = (await vaultRows(page)).filter((row) => row.title === title);
      expect(saved).toHaveLength(1);
      const snapshot = JSON.stringify(saved[0]!.payload);
      expect(snapshot).not.toContain('session_ref');
      expect(snapshot).not.toContain('started_at');
      expect(snapshot).not.toContain('observation_ref');
      expect((await page.request.get(
        '/api/v1/temporal/activities/' + original.item.sourceRef + '/profile',
        { headers: TZ },
      )).status()).toBe(404);
      await openHome(page, day);
      await expect(cardOn(page, title)).toHaveCount(0);
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-04 Event: confirmed Objective result → red irreversible Move → definitions only', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 106);
    const { page } = user;
    const day = scenarioDate(5);
    const title = uniqueTitle('vault obiettivo registrato');
    try {
      await clearVault(page);
      await openHome(page, day);
      const original = await authorPersona(page, EVENT_CASES[0]!, title, day);
      const goal = original.truth.objectives[0]!;
      expect(goal.kind).toBe('boolean');
      await openHome(page, day);
      await page.getByRole('tab', { name: 'Obiettivi' }).click();
      const pending = page.locator('.home-resolution-card').filter({ hasText: title });
      await pending.getByRole('button', { name: 'Compila obiettivi' }).click();
      const control = pending.locator('[data-objective-ref]')
        .filter({ hasText: goal.label });
      await control.getByRole('combobox', { name: 'Valore per ' + goal.label })
        .selectOption('true');
      const accepted = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().endsWith('/confirm-input'),
      );
      await control.getByRole('button', {
        name: 'Conferma obiettivo ' + goal.label,
      }).click();
      expect((await accepted).status()).toBe(200);
      const objectivePath = '/api/v1/temporal/events/' +
        original.item.sourceRef + '/objectives';
      const before = (await serverRead(page, objectivePath)) as
        Record<string, unknown>[];
      expect(before[0]!.observation_ref).toEqual(expect.any(String));
      const inspector = await inspectorFor(page, day, title);
      await inspector.getByRole('button', { name: 'Sposta in Bozze' }).click();
      const review = inspector.getByRole('region', { name: 'Sposta evento in Bozze' });
      await expect(review).toContainText('risultato');
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      const loss = page.getByRole('alertdialog', { name: 'Conferma perdita registrazioni' });
      await expect(loss).toBeVisible();
      await loss.getByRole('button', { name: 'Annulla' }).click();
      expect((await serverRead(page, objectivePath) as Record<string, unknown>[])[0]!
        .observation_ref).toEqual(expect.any(String));
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      const committed = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().includes('/api/v1/temporal/drafts/move/'),
      );
      await loss.getByRole('button', { name: 'Elimina registrazioni e sposta' }).click();
      expect((await committed).status()).toBe(200);
      const drafts = (await vaultRows(page)).filter((row) => row.title === title);
      expect(drafts).toHaveLength(1);
      expect(JSON.stringify(drafts[0]!.payload)).not.toContain('observation_ref');
      expect((await page.request.get(
        '/api/v1/temporal/events/' + original.item.sourceRef,
        { headers: TZ },
      )).status()).toBe(404);
      await openHome(page, day);
      await expect(cardOn(page, title)).toHaveCount(0);
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-05 recurring Activity and Event: no standalone Move on series/Occurrence', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 107);
    const { page } = user;
    const day = scenarioDate(6);
    try {
      await clearVault(page);
      await openHome(page, day);
      const subjects = [
        { persona: ACTIVITY_CASES[0]!, title: uniqueTitle('serie activity') },
        { persona: EVENT_CASES[0]!, title: uniqueTitle('serie event') },
      ] as const;
      for (const { persona, title } of subjects) {
        const recurrence = recurrenceFor(persona);
        const authored = await authorPersona(page, persona, title, day, recurrence);
        expect(authored.item.sourceRef).toEqual(expect.any(String));
        const inspector = await inspectorFor(page, day, title);
        await expect(inspector.getByRole('button', { name: 'Sposta in Bozze' }))
          .toHaveCount(0);
        await inspector.getByRole('button', { name: 'Chiudi Inspector' }).click();
        expect((await vaultRows(page)).filter((row) => row.title === title))
          .toHaveLength(0);
      }
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-06 full 100: Create keeps unsaved fields, deletion frees one slot', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 108);
    const { page } = user;
    const day = scenarioDate(4);
    try {
      await clearVault(page);
      await seedDrafts(page, 100);
      await openHome(page, day);
      const vault = await openVault(page);
      await expect(vault).toContainText('100/100');
      await vault.getByRole('button', { name: 'Chiudi Bozze' }).click();
      await page.getByRole('button', { name: 'Aggiungi alla timeline' }).click();
      const composer = page.locator('[data-temporal-create="composer"]');
      const title = uniqueTitle('Capienza 101 rifiutata');
      await composer.getByRole('textbox', { name: 'Titolo' }).fill(title);
      await composer.getByRole('button', { name: 'Salva bozza' }).click();
      const limit = page.getByRole('alertdialog', { name: 'Spazio Bozze esaurito' });
      await expect(limit).toBeVisible();
      await expect(composer.getByRole('textbox', { name: 'Titolo' }))
        .toHaveValue(title);
      expect(await vaultRows(page)).toHaveLength(100);
      await limit.getByRole('button', { name: 'Chiudi' }).click();
      await expect(composer).toBeVisible();
      const first = (await vaultRows(page))[0]!;
      const removed = await page.request.delete(
        '/api/v1/temporal/drafts/' + first.draft_ref +
          '?expected_revision=' + first.revision,
        { headers: { ...TZ, 'X-Dante-CSRF': await csrf(page) } },
      );
      expect(removed.status()).toBe(204);
      await composer.getByRole('button', { name: 'Salva bozza' }).click();
      await expect(composer).toHaveCount(0);
      const drafts = await vaultRows(page);
      expect(drafts).toHaveLength(100);
      expect(drafts.filter((row) => row.title === title)).toHaveLength(1);
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });

  test('DV-REAL-07 full 100: failed Event Move rolls back original; retry after freeing capacity succeeds', async (
    { browser }, info,
  ) => {
    const user = await signedInPersona(browser, info, 109);
    const { page } = user;
    const day = scenarioDate(5);
    const title = uniqueTitle('vault quota move rollback');
    try {
      await clearVault(page);
      await openHome(page, day);
      const original = await authorPersona(page, EVENT_CASES[0]!, title, day);
      await seedDrafts(page, 100);
      let inspector = await inspectorFor(page, day, title);
      await inspector.getByRole('button', { name: 'Sposta in Bozze' }).click();
      let review = inspector.getByRole('region', { name: 'Sposta evento in Bozze' });
      const rejection = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().includes('/api/v1/temporal/drafts/move/'),
      );
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      const rejected = await rejection;
      expect(rejected.status()).toBe(409);
      expect((await rejected.json() as { code: string }).code)
        .toBe('temporal.drafts.capacity');
      const popup = page.getByRole('alertdialog', { name: 'Spazio Bozze esaurito' });
      await expect(popup).toBeVisible();
      await expectOriginal(page, original);
      expect((await vaultRows(page)).filter((row) => row.title === title))
        .toHaveLength(0);
      await popup.getByRole('button', { name: 'Chiudi' }).click();
      const first = (await vaultRows(page))[0]!;
      expect((await page.request.delete(
        '/api/v1/temporal/drafts/' + first.draft_ref +
          '?expected_revision=' + first.revision,
        { headers: { ...TZ, 'X-Dante-CSRF': await csrf(page) } },
      )).status()).toBe(204);
      // The original remains accepted; reopen Inspector to obtain fresh CAS.
      await openHome(page, day);
      inspector = await inspectorFor(page, day, title);
      await inspector.getByRole('button', { name: 'Sposta in Bozze' }).click();
      review = inspector.getByRole('region', { name: 'Sposta evento in Bozze' });
      const accepted = page.waitForResponse((response) =>
        response.request().method() === 'POST' &&
        response.url().includes('/api/v1/temporal/drafts/move/'),
      );
      await review.getByRole('button', { name: 'Conferma spostamento in Bozze' }).click();
      expect((await accepted).status()).toBe(200);
      expect((await vaultRows(page)).filter((row) => row.title === title))
        .toHaveLength(1);
      expect((await page.request.get(
        '/api/v1/temporal/events/' + original.item.sourceRef,
        { headers: TZ },
      )).status()).toBe(404);
    } finally {
      await clearVault(page).catch(() => undefined);
      await user.close();
    }
  });
});
