import type { InitOptions } from 'i18next';

import { common as enCommon } from './resources/en/common';
import { common as itCommon } from './resources/it/common';

export const supportedLocales = ['it', 'en'] as const;
export type SupportedLocale = (typeof supportedLocales)[number];

export const defaultLocale = 'it' satisfies SupportedLocale;
export const fallbackLocale = 'it' satisfies SupportedLocale;

export const defaultNamespace = 'common' as const;
export const namespaces = [defaultNamespace] as const;

export const resources = {
  it: {
    common: itCommon,
  },
  en: {
    common: enCommon,
  },
} as const;

export function createI18nOptions(
  lng: SupportedLocale = defaultLocale,
): InitOptions {
  return {
    lng,
    fallbackLng: fallbackLocale,
    supportedLngs: [...supportedLocales],
    nonExplicitSupportedLngs: true,
    load: 'languageOnly',
    ns: [...namespaces],
    defaultNS: defaultNamespace,
    resources,
    enableSelector: 'strict',
    initAsync: false,
    returnNull: false,
    interpolation: {
      escapeValue: false,
    },
  };
}

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: typeof defaultNamespace;
    resources: (typeof resources)['it'];
    returnNull: false;
    strictKeyChecks: true;
    enableSelector: 'strict';
  }
}
