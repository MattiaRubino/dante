import type { ChangeEventHandler } from 'react';
import { useTranslation } from 'react-i18next';

import { temporalCreateProductCopy } from './temporal-create-product-copy';

import './temporal-create-core-u2.css';

/** Same quick recurrence choice in Create and existing-item Edit. */
export type QuickRecurrence =
  'none' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';

export function TemporalCreateQuickRecurrenceSelect({
  value,
  onChange,
}: Readonly<{
  value: QuickRecurrence;
  onChange: (value: QuickRecurrence) => void;
}>) {
  const { i18n } = useTranslation('common');
  const copy = temporalCreateProductCopy(
    i18n.resolvedLanguage ?? i18n.language ?? 'it',
  ).event;
  const handleChange: ChangeEventHandler<HTMLSelectElement> = (event) => {
    onChange(event.currentTarget.value as QuickRecurrence);
  };

  return (
    <select aria-label={copy.repeat} value={value} onChange={handleChange}>
      <option value="none">{copy.repeatNever}</option>
      <option value="daily">{copy.repeatDaily}</option>
      <option value="weekly">{copy.repeatWeekly}</option>
      <option value="monthly">{copy.repeatMonthly}</option>
      <option value="yearly">{copy.repeatYearly}</option>
      <option value="custom">{copy.repeatCustom}</option>
    </select>
  );
}
