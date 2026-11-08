import type { ReactNode } from 'react';

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
}: Readonly<{
  kind: 'activity' | 'event';
  children: ReactNode;
  className?: string;
  compact?: boolean;
}>) {
  return (
    <div
      className={`temporal-create-title-row temporal-authoring-title-row ${compact ? 'is-quick' : 'has-tools'} temporal-authoring-title-row--${kind} ${className}`.trim()}
      data-authoring-title-kind={kind}
    >
      <span className="temporal-authoring-title-row__marker" aria-hidden="true">
        {kind === 'activity' ? '◇' : '○'}
      </span>
      {children}
    </div>
  );
}
