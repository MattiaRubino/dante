import type { ReactNode } from 'react';

import './temporal-recurrence-panel.css';

/**
 * One presentation boundary for all scheduled Activity/Event recurrence editing.
 *
 * The caller owns recurrence state and the canonical serialization.
 * Rendering is intentionally independent from frequency family and persistence.
 */
export function TemporalRecurrencePanel({
  kind,
  choice,
  children,
  expanded,
  className = '',
}: Readonly<{
  kind: 'activity' | 'event';
  choice: ReactNode;
  children?: ReactNode;
  expanded: boolean;
  className?: string;
}>) {
  return (
    <section
      className={['temporal-recurrence-panel', className]
        .filter(Boolean)
        .join(' ')}
      aria-label="Ripetizione"
      data-recurrence-owner={kind}
      data-recurrence-expanded={expanded}
    >
      <h3 className="temporal-recurrence-panel__heading">Ripetizione</h3>
      <div className="temporal-recurrence-panel__choice">{choice}</div>
      {expanded ? (
        <div className="temporal-recurrence-panel__details">{children}</div>
      ) : null}
    </section>
  );
}
