import { createI18nOptions } from '@dante/i18n';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

if (!i18n.isInitialized) {
  void i18n.use(initReactI18next).init(createI18nOptions());
}

export { i18n };
