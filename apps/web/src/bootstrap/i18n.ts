import { createI18nOptions } from '@dante/i18n';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import { resolvePreferredLocale } from '../platform/locale-preference';

if (!i18n.isInitialized) {
  void i18n
    .use(initReactI18next)
    .init(createI18nOptions(resolvePreferredLocale()));
}

export { i18n };
