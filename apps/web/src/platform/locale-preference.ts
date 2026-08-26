import {
  defaultLocale,
  supportedLocales,
  type SupportedLocale,
} from '@dante/i18n';

const localeStorageKey = 'dante.locale';

function normalizeLocale(
  value: string | null | undefined,
): SupportedLocale | null {
  if (!value) {
    return null;
  }

  const language = value.toLowerCase().split('-')[0];
  return supportedLocales.find((locale) => locale === language) ?? null;
}

export function resolvePreferredLocale(): SupportedLocale {
  if (typeof window === 'undefined') {
    return defaultLocale;
  }

  try {
    const persistedLocale = normalizeLocale(
      window.localStorage.getItem(localeStorageKey),
    );
    if (persistedLocale) {
      return persistedLocale;
    }
  } catch {
    // Storage may be unavailable in hardened/private browser contexts.
  }

  const browserLanguages =
    window.navigator.languages.length > 0
      ? window.navigator.languages
      : [window.navigator.language];

  for (const language of browserLanguages) {
    const locale = normalizeLocale(language);
    if (locale) {
      return locale;
    }
  }

  return defaultLocale;
}

export function persistPreferredLocale(locale: SupportedLocale) {
  try {
    window.localStorage.setItem(localeStorageKey, locale);
  } catch {
    // Changing language must still work when storage is unavailable.
  }
}
