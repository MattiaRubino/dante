import { useTranslation } from 'react-i18next';

import { temporalCreateProductCopy } from './temporal-create-product-copy';
import { TemporalRecurrenceChoice } from './temporal-recurrence-panel';

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
  return (
    <TemporalRecurrenceChoice
      label={copy.repeat}
      value={value}
      onChange={(next) => onChange(next as QuickRecurrence)}
      options={[
        { value: 'none', label: copy.repeatNever },
        { value: 'daily', label: copy.repeatDaily },
        { value: 'weekly', label: copy.repeatWeekly },
        { value: 'monthly', label: copy.repeatMonthly },
        { value: 'yearly', label: copy.repeatYearly },
        { value: 'custom', label: copy.repeatCustom },
      ]}
    />
  );
}
