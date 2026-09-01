import { createInstance } from 'i18next';
import { describe, expect, it } from 'vitest';

import {
  createI18nOptions,
  defaultLocale,
  defaultNamespace,
  fallbackLocale,
  namespaces,
  resources,
  supportedLocales,
} from './index';

function collectLeafPaths(
  value: unknown,
  prefix = '',
  paths: string[] = [],
): string[] {
  if (typeof value === 'string') {
    paths.push(prefix);
    return paths;
  }

  if (typeof value !== 'object' || value === null) {
    throw new TypeError(`Unexpected non-resource value at "${prefix}"`);
  }

  for (const [key, child] of Object.entries(value)) {
    collectLeafPaths(child, prefix ? `${prefix}.${key}` : key, paths);
  }

  return paths;
}

async function createRuntime(locale: 'it' | 'en' = defaultLocale) {
  const runtime = createInstance();
  await runtime.init(createI18nOptions(locale));
  return runtime;
}

describe('@dante/i18n', () => {
  it('keeps the accepted locale and namespace contract', () => {
    expect(supportedLocales).toEqual(['it', 'en']);
    expect(defaultLocale).toBe('it');
    expect(fallbackLocale).toBe('it');
    expect(defaultNamespace).toBe('common');
    expect(namespaces).toEqual(['common']);
  });

  it('boots Italian as the default runtime locale', async () => {
    const runtime = await createRuntime();

    expect(runtime.language).toBe('it');
    expect(runtime.t(($) => $.common.runtime.web.title)).toBe(
      'Frontend pronto',
    );
    expect(runtime.t(($) => $.common.gesture.title)).toBe('Test gesto');
  });

  it('resolves the complete Temporal Create authoring tree at runtime', async () => {
    const runtime = await createRuntime();

    expect(runtime.t(($) => $.common.home.timeline.create.kind.activity)).toBe(
      'Attività',
    );
    expect(runtime.t(($) => $.common.home.timeline.create.kind.event)).toBe(
      'Evento',
    );
    expect(
      runtime.t(($) => $.common.home.timeline.create.timeSemantics.timed),
    ).toBe('Orario');
    expect(
      runtime.t(($) => $.common.home.timeline.create.timeSemantics.allDay),
    ).toBe('Tutto il giorno');
    expect(
      runtime.t(($) => $.common.home.timeline.create.timeSemantics.unscheduled),
    ).toBe('Da pianificare');
    expect(runtime.t(($) => $.common.home.timeline.create.date)).toBe('Data');
    expect(runtime.t(($) => $.common.home.timeline.create.start)).toBe('Ora');
    expect(runtime.t(($) => $.common.home.timeline.create.duration)).toBe(
      'Durata prevista',
    );
    expect(runtime.t(($) => $.common.home.timeline.create.context)).toBe(
      'Contesto',
    );
    expect(runtime.t(($) => $.common.home.timeline.create.details.show)).toBe(
      'Dettagli e pianificazione',
    );
    expect(
      runtime.t(($) => $.common.home.timeline.create.planning.constraintOpen),
    ).toBe('Senza collocazione');
    expect(
      runtime.t(($) => $.common.home.timeline.create.execution.splittable),
    ).toBe('Divisibile in sessioni');
    expect(
      runtime.t(($) => $.common.home.timeline.create.recurrence.weekly),
    ).toBe('Settimanale');
    expect(
      runtime.t(($) => $.common.home.timeline.create.integrations.providerRequired),
    ).toContain('provider/backend');
    expect(runtime.t(($) => $.common.home.timeline.create.cancel)).toBe(
      'Annulla',
    );
    expect(runtime.t(($) => $.common.home.timeline.create.submit)).toBe(
      'Aggiungi',
    );
  });

  it('boots English through the same shared resource contract', async () => {
    const runtime = await createRuntime('en');

    expect(runtime.language).toBe('en');
    expect(runtime.t(($) => $.common.runtime.web.title)).toBe(
      'Frontend runtime ready',
    );
    expect(runtime.t(($) => $.common.gesture.title)).toBe('Gesture probe');
    expect(runtime.t(($) => $.common.home.timeline.create.duration)).toBe(
      'Expected duration',
    );
    expect(runtime.t(($) => $.common.home.timeline.create.details.show)).toBe(
      'Details and planning',
    );
  });

  it('falls back to Italian for an unsupported locale', async () => {
    const runtime = await createRuntime('en');

    await runtime.changeLanguage('fr-FR');

    expect(runtime.t(($) => $.common.runtime.web.title)).toBe(
      'Frontend pronto',
    );
    expect(runtime.t(($) => $.common.gesture.title)).toBe('Test gesto');
  });

  it('keeps Italian and English runtime resource leaf shapes identical', () => {
    const italianPaths = collectLeafPaths(resources.it.common).sort();
    const englishPaths = collectLeafPaths(resources.en.common).sort();

    expect(englishPaths).toEqual(italianPaths);
    expect(italianPaths.length).toBeGreaterThan(0);
  });
});