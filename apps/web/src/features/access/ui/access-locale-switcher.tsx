import { type SupportedLocale } from '@dante/i18n';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { persistPreferredLocale } from '../../../platform/locale-preference';

const localeMeta: Record<
  SupportedLocale,
  Readonly<{ code: string; label: string }>
> = {
  it: { code: 'IT', label: 'Italiano' },
  en: { code: 'EN', label: 'English' },
};

function currentLocale(language: string | undefined): SupportedLocale {
  return language?.toLowerCase().startsWith('en') ? 'en' : 'it';
}

export function AccessLocaleSwitcher() {
  const { i18n } = useTranslation();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const locale = currentLocale(i18n.resolvedLanguage);
  const meta = localeMeta[locale];
  const controlLabel =
    locale === 'it'
      ? `Cambia lingua. Lingua attuale: ${meta.label}`
      : `Change language. Current language: ${meta.label}`;

  useEffect(() => {
    if (!open) {
      return;
    }

    const closeOnOutsidePointer = (event: PointerEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    document.addEventListener('pointerdown', closeOnOutsidePointer);
    document.addEventListener('keydown', closeOnEscape);

    return () => {
      document.removeEventListener('pointerdown', closeOnOutsidePointer);
      document.removeEventListener('keydown', closeOnEscape);
    };
  }, [open]);

  const selectLocale = (nextLocale: SupportedLocale) => {
    persistPreferredLocale(nextLocale);
    void i18n.changeLanguage(nextLocale);
    setOpen(false);
  };

  return (
    <div className="access-locale" ref={rootRef}>
      <button
        className="access-locale-button"
        type="button"
        aria-label={controlLabel}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls="access-locale-menu"
        onClick={() => setOpen((value) => !value)}
      >
        <span>{meta.code}</span>
        <svg
          className="access-locale-chevron"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          focusable="false"
          aria-hidden="true"
        >
          <path d="m7 10 5 5 5-5" />
        </svg>
      </button>

      {open ? (
        <div className="access-locale-menu" id="access-locale-menu" role="menu">
          {(Object.keys(localeMeta) as SupportedLocale[]).map((option) => {
            const optionMeta = localeMeta[option];
            const selected = option === locale;

            return (
              <button
                className="access-locale-option"
                type="button"
                role="menuitemradio"
                aria-checked={selected}
                key={option}
                onClick={() => selectLocale(option)}
              >
                <span>{optionMeta.label}</span>
                <span className="access-locale-option-code">
                  {optionMeta.code}
                </span>
                <span className="access-locale-check" aria-hidden="true">
                  {selected ? '✓' : ''}
                </span>
              </button>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}
