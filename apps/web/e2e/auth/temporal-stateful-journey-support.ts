/**
 * Real UI and canonical HTTP primitives for the v2 stateful Temporal matrix.
 *
 * No mocked backend, direct SQL setup of a subject, fabricated timelines or
 * snapshot-derived expectations. Existing Life Areas can be fixture-authored
 * with real authenticated API commands; all tested Event/Activity subjects
 * are created by a browser through the production composer.
 */
import { randomUUID } from 'node:crypto';

import {
  expect,
  type Browser,
  type Locator,
  type Page,
  type TestInfo,
} from '@playwright/test';

import {
  configureCreate,
  openCreate,
  serverRead,
  submitCreate,
  type CreatedItem,
} from './temporal-user-journey-support';
import type {
  GoalKind,
  PersonaCase,
} from './temporal-stateful-case-matrix';

const PASSWORD = 'correct horse battery staple';
const TZ = { 'X-Dante-Time-Zone': 'Europe/Rome' } as const;
const HEX_COLORS = ['#4285F4', '#33B679', '#FFD600', '#8E24AA'] as const;
const COLOR_BUTTONS = ['Blu', 'Verde menta', 'Giallo', 'Prugna'] as const;

export type ObjectiveTruth = Readonly<{
  label: string;
  kind: GoalKind;
  target: number | null;
  minimum: number | null;
  maximum: number | null;
  verification: 'none' | 'review_on_end';
}>;
export type PersonaTruth = Readonly<{
  title: string;
  description: string | null;
  areaRef: string | null;
  areaName: string | null;
  agenda: readonly string[];
  objectives: readonly ObjectiveTruth[];
  sessions: readonly string[];
  explicitExtraIntervals: number;
}>;
export type AuthoredPersona = Readonly<{
  item: CreatedItem;
  truth: PersonaTruth;
  areaColor: string | null;
}>;

function accountIndex(info: TestInfo, ordinal: number): number {
  const projects: Record<string, number> = {
    chromium: 0, firefox: 1, webkit: 2,
  };
  const project = projects[info.project.name];
  if (project === undefined || !Number.isInteger(ordinal) ||
      ordinal < 0 || ordinal >= 102) {
    throw new Error('Stateful E2E account partition is invalid');
  }
  // 1..101 existing; 102..401 matrix; 402..407 runtime-guard personas.
  return ordinal < 100
    ? 102 + project * 100 + ordinal
    : 402 + project * 2 + ordinal - 100;
}

export async function signedInPersona(
  browser: Browser,
  info: TestInfo,
  ordinal: number,
): Promise<Readonly<{ page: Page; close: () => Promise<void> }>> {
  const context = await browser.newContext({
    ignoreHTTPSErrors: true,
    timezoneId: 'Europe/Rome',
    locale: 'it-IT',
  });
  try {
    const page = await context.newPage();
    await page.addInitScript(() => localStorage.setItem('dante.locale', 'it'));
    await page.goto('/');
    await expect(
      page.getByRole('heading', { level: 1, name: 'Accedi a DANTE' }),
    ).toBeVisible();
    await page.getByLabel('Email').fill(
      'synthetic.user+e2e-' + accountIndex(info, ordinal) + '@example.com',
    );
    await page.getByLabel('Password', { exact: true }).fill(PASSWORD);
    const signin = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/signin') &&
        response.request().method() === 'POST',
    );
    await page.getByRole('button', { name: 'Accedi', exact: true }).click();
    expect((await signin).status()).toBe(200);
    await expect(
      page.getByRole('heading', { level: 1, name: 'Accesso confermato' }),
    ).toBeVisible();
    return { page, close: () => context.close() };
  } catch (reason) {
    await context.close();
    throw reason;
  }
}

async function sessionCsrf(page: Page): Promise<string> {
  const raw = await serverRead(page, '/api/v1/auth/session') as {
    csrf_token?: string;
  };
  expect(raw.csrf_token).toEqual(expect.any(String));
  return raw.csrf_token!;
}

export async function seedExistingArea(
  page: Page,
  name: string,
  color: string,
): Promise<string> {
  const csrf = await sessionCsrf(page);
  const created = await page.request.post('/api/v1/temporal/life-areas', {
    headers: { ...TZ, 'X-Dante-CSRF': csrf },
    data: { name, operation_id: randomUUID() },
  });
  expect(created.status(), 'create authenticated Life Area fixture').toBe(201);
  const area = await created.json() as {
    life_area_ref: string; revision: number;
  };
  const appearance = await page.request.patch(
    '/api/v1/temporal/life-areas/' + area.life_area_ref + '/appearance',
    {
      headers: { ...TZ, 'X-Dante-CSRF': csrf },
      data: {
        operation_id: randomUUID(),
        expected_revision: area.revision,
        color_code: color,
        icon_code: null,
      },
    },
  );
  expect(appearance.status(), 'seed existing Life Area color').toBe(200);
  return area.life_area_ref;
}

async function pickColor(
  page: Page,
  composer: Locator,
  index: number,
): Promise<void> {
  await composer.getByRole('button', { name: 'Colore Life Area' }).click();
  const picker = page.getByRole('dialog', { name: 'Scegli colore' });
  await expect(picker).toBeVisible();
  await picker.getByRole('button', {
    name: COLOR_BUTTONS[index % COLOR_BUTTONS.length]!,
    exact: true,
  }).click();
}

function truthFor(
  persona: PersonaCase,
  title: string,
  areaName: string | null,
  areaRef: string | null,
): PersonaTruth {
  return Object.freeze({
    title,
    description: persona.description ? title + ' descrizione persistita' : null,
    areaName,
    areaRef,
    agenda: Object.freeze(
      persona.kind === 'event'
        ? Array.from({ length: persona.agendaCount }, (_, i) =>
            title + ' scaletta ' + (i + 1))
        : [],
    ),
    objectives: Object.freeze(
      persona.goalKinds.map((kind, i) => Object.freeze({
        label: title + ' obiettivo ' + (i + 1),
        kind,
        target: kind === 'quantity' ? 10 + i : null,
        minimum: kind === 'range' ? i + 1 : null,
        maximum: kind === 'range' ? i + 8 : null,
        verification: i % 2 === 0 ? 'review_on_end' as const : 'none' as const,
      })),
    ),
    sessions: Object.freeze(
      persona.kind === 'activity'
        ? Array.from({ length: persona.plannedSessionCount }, (_, i) =>
            title + ' Sessione ' + (i + 1))
        : [],
    ),
    explicitExtraIntervals:
      persona.kind === 'activity' && !persona.allDay
        ? persona.intervalCount - 1
        : 0,
  });
}

async function setObjective(
  composer: Locator,
  objective: ObjectiveTruth,
  index: number,
): Promise<void> {
  const nth = index + 1;
  if (index > 0) {
    await composer.getByRole('button', { name: 'Aggiungi obiettivo' }).click();
    await composer.getByRole('textbox', { name: 'Obiettivo ' + nth })
      .fill(objective.label);
  }
  const row = composer.locator('[data-create-objective]').nth(index);
  await expect(row).toBeVisible();
  if (objective.kind !== 'boolean') {
    await row.getByRole('combobox', {
      name: 'Tipo risultato obiettivo ' + nth,
    }).selectOption(objective.kind);
  }
  if (objective.target !== null) {
    await row.getByRole('spinbutton', { name: 'Target obiettivo' })
      .fill(String(objective.target));
    await row.getByRole('textbox', { name: 'Unità obiettivo' }).fill('ore');
  }
  if (objective.minimum !== null && objective.maximum !== null) {
    await row.getByRole('spinbutton', { name: 'Minimo obiettivo' })
      .fill(String(objective.minimum));
    await row.getByRole('spinbutton', { name: 'Massimo obiettivo' })
      .fill(String(objective.maximum));
    await row.getByRole('textbox', { name: 'Unità obiettivo' }).fill('punti');
  }
  await row.getByRole('combobox', { name: 'Verifica obiettivo ' + nth })
    .selectOption(objective.verification);
}

export async function authorPersona(
  page: Page,
  persona: PersonaCase,
  title: string,
  date: string,
  recurrence?: Readonly<{
    cadence: 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';
    interval: number;
    monthlyOrdinal: boolean;
    repeatCount: number | null;
  }>,
  enableLiveSession = false,
  clockOverride?: string,
): Promise<AuthoredPersona> {
  const colorIndex = Number(persona.id.slice(1)) - 1;
  const color = HEX_COLORS[colorIndex % HEX_COLORS.length]!;
  const areaName =
    persona.area === 'none' ? null : title + ' area ' + persona.area;
  let areaRef: string | null = null;
  if (areaName && persona.area === 'existing') {
    areaRef = await seedExistingArea(page, areaName, color);
  }
  const truth = truthFor(persona, title, areaName, areaRef);
  const dialog = await openCreate(page, persona.kind);
  await configureCreate(dialog, {
    kind: persona.kind,
    title,
    date,
    clock: clockOverride ?? (persona.kind === 'event' ? '11:20' : '09:10'),
    ...(persona.allDay ? { allDay: true } : {}),
    ...(areaName ? { lifeArea: areaName } : {}),
    ...(recurrence
      ? {
          recurrence: recurrence.cadence,
          interval: recurrence.interval,
          ...(recurrence.monthlyOrdinal ? { monthlyOrdinal: true } : {}),
          ...(recurrence.repeatCount !== null
            ? { repeatCount: recurrence.repeatCount }
            : {}),
        }
      : {}),
    ...(persona.placementProtected ? { placementProtected: true } : {}),
    objective: truth.objectives[0]!.label,
    ...(persona.kind === 'event'
      ? { agenda: truth.agenda[0]! }
      : { plannedSession: truth.sessions[0]! }),
  });

  if (enableLiveSession) {
    if (persona.kind !== 'activity') {
      throw new Error('Live Sessions are Activity-only.');
    }
    await dialog.locator(
      'label[data-session-capability="activity"] input[type="checkbox"',
    ).check();
  }
  if (truth.description) {
    await dialog.getByRole('textbox', { name: 'Descrizione avanzata' })
      .fill(truth.description);
  }
  for (const [i, objective] of truth.objectives.entries()) {
    await setObjective(dialog, objective, i);
  }
  if (persona.kind === 'event') {
    for (let i = 1; i < truth.agenda.length; i += 1) {
      await dialog.getByRole('button', { name: 'Aggiungi punto alla scaletta' })
        .click();
      await dialog.getByRole('textbox', { name: 'Punto scaletta ' + (i + 1) })
        .fill(truth.agenda[i]!);
    }
  } else {
    for (let i = 1; i < truth.sessions.length; i += 1) {
      await dialog.locator('[aria-label="Aggiungi Sessione pianificata"]')
        .getByRole('button', { name: 'Sessione' }).click();
      await dialog.locator('[data-create-planned-session]').nth(i)
        .getByRole('textbox', { name: 'Nome Sessione' })
        .fill(truth.sessions[i]!);
    }
    for (let i = 0; i < truth.explicitExtraIntervals; i += 1) {
      await dialog.getByRole('button', { name: 'Aggiungi intervallo' })
        .click();
    }
  }
  if (areaName && persona.area === 'new') {
    await pickColor(page, dialog, colorIndex);
  }

  await expect(dialog.locator('[data-create-objective]'))
    .toHaveCount(truth.objectives.length);
  if (persona.kind === 'event') {
    await expect(dialog.locator('[data-temporal-create-agenda-part]'))
      .toHaveCount(truth.agenda.length);
  } else {
    await expect(dialog.locator('[data-create-planned-session]'))
      .toHaveCount(truth.sessions.length);
    await expect(dialog.locator('.temporal-create-activity-interval'))
      .toHaveCount(truth.explicitExtraIntervals);
  }

  const item = await submitCreate(page, dialog, {
    kind: persona.kind,
    title,
    recurring: recurrence !== undefined,
  });
  const catalog = await serverRead(page, '/api/v1/temporal/life-areas') as
    readonly Record<string, unknown>[];
  const found = areaName ? catalog.filter((area) => area.name === areaName) : [];
  if (areaName) {
    expect(found).toHaveLength(1);
    areaRef = String(found[0]!.life_area_ref);
    expect(found[0]!.color_code).toBe(color);
  }
  return {
    item,
    truth: Object.freeze({ ...truth, areaRef }),
    areaColor: areaName ? color : null,
  };
}

function objectiveRows(value: unknown): readonly Record<string, unknown>[] {
  expect(Array.isArray(value)).toBe(true);
  return value as Record<string, unknown>[];
}

/** All supported fields, not just the most recently edited field. */
export async function assertOneOffTruth(
  page: Page,
  actual: AuthoredPersona,
): Promise<void> {
  const { item, truth } = actual;
  const base = await serverRead(
    page,
    item.kind === 'event'
      ? '/api/v1/temporal/events/' + item.sourceRef
      : '/api/v1/temporal/activities/' + item.sourceRef + '/profile',
  ) as Record<string, unknown>;
  expect(base.title, 'canonical title').toBe(truth.title);
  expect(base.description ?? null, 'canonical description')
    .toBe(truth.description);
  const persisted = await serverRead(
    page,
    '/api/v1/temporal/' + (item.kind === 'event' ? 'events/' : 'activities/') +
      item.sourceRef + '/objectives',
  );
  const rows = objectiveRows(persisted);
  expect(rows.map((row) => row.label), 'ordered Objectives')
    .toEqual(truth.objectives.map((row) => row.label));
  for (const [i, objective] of truth.objectives.entries()) {
    const row = rows[i]!;
    expect(row.result_kind, objective.label + ' type').toBe(objective.kind);
    expect(row.verification_mode, objective.label + ' verification')
      .toBe(objective.verification);
    if (objective.target !== null) {
      expect(Number(row.target_value), objective.label + ' target')
        .toBe(objective.target);
    }
    if (objective.minimum !== null) {
      expect(Number(row.target_min), objective.label + ' minimum')
        .toBe(objective.minimum);
      expect(Number(row.target_max), objective.label + ' maximum')
        .toBe(objective.maximum);
    }
    expect(row.objective_ref).toEqual(expect.stringMatching(/^[\da-f-]{36}$/i));
  }
  if (item.kind === 'event') {
    expect(base.agenda_parts, 'Event agenda order').toEqual(truth.agenda);
    expect(base.life_area_ref ?? null, 'Event Life Area')
      .toBe(truth.areaRef);
  } else {
    const snapshot = await serverRead(
      page,
      '/api/v1/temporal/activities/' + item.sourceRef + '/edit-snapshot',
    ) as Record<string, unknown>;
    expect(snapshot.life_area_ref ?? null, 'Activity Life Area')
      .toBe(truth.areaRef);
    const schedules = snapshot.schedules as Record<string, unknown>[];
    const sessions = schedules.filter((schedule) => schedule.role_code === 'planned');
    expect(sessions.map((session) => session.name), 'planned Session order')
      .toEqual(truth.sessions);
    expect(
      schedules.filter((schedule) => schedule.role_code === 'interval').length,
      'explicit extra Activity intervals',
    ).toBe(truth.explicitExtraIntervals);
    expect(new Set(schedules.map((row) => row.schedule_ref)).size)
      .toBe(schedules.length);
  }
}
