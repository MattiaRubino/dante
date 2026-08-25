import { createI18nOptions, type SupportedLocale } from '@dante/i18n';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import { resolvePreferredLocale } from '../platform/locale-preference';

function normalizeDocumentLocale(
  language: string | undefined,
): SupportedLocale {
  return language?.toLowerCase().startsWith('en') ? 'en' : 'it';
}

function syncDocumentLocale(language: string | undefined) {
  if (typeof document === 'undefined') {
    return;
  }

  document.documentElement.lang = normalizeDocumentLocale(language);
}

if (!i18n.isInitialized) {
  void i18n
    .use(initReactI18next)
    .init(createI18nOptions(resolvePreferredLocale()));
}

syncDocumentLocale(i18n.resolvedLanguage);
i18n.on('languageChanged', syncDocumentLocale);

export { i18n };
