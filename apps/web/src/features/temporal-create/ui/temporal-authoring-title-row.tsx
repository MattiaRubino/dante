import type { ReactNode } from 'react';
import { TemporalKindMarker } from './temporal-kind-marker';

import './temporal-authoring-title-row.css';

/** One DOM contract for title/placement actions in Create, Edit and Series Edit.
 * The marker is a real grid child. CSS pseudo-elements must never participate
 * in the grid's track placement. Keep input/action state with the caller.
 */
export function TemporalAuthoringTitleRow({
  kind,
  children,
  className = '',
  compact = false,
  invalid = false,
  shakeAttempt = 0,
}: Readonly<{
  kind: 'activity' | 'event';
  children: ReactNode;
  className?: string;
  compact?: boolean;
  invalid?: boolean;
  shakeAttempt?: number;
}>) {
  return (
    <div
      className={[
        'temporal-create-title-row',
        'temporal-authoring-title-row',
        compact ? 'is-quick' : 'has-tools',
        `temporal-authoring-title-row--${kind}`,
        kind === 'event' ? 'temporal-event-title-row' : '',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      data-authoring-title-kind={kind}
      data-title-invalid={invalid || undefined}
      data-title-shake={invalid ? (shakeAttempt % 2 ? 'odd' : 'even') : undefined}
    >
      <span className="temporal-authoring-title-row__marker" aria-hidden="true">
        <TemporalKindMarker kind={kind} />
      </span>
      {children}
    </div>
  );
}
