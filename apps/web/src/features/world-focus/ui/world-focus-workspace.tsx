import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusShellStatus } from '../model/world-focus-platform';
import { WORLD_FOCUS_REGION } from '../model/world-focus-structure';

type WorldFocusWorkspaceProps = Readonly<{
  worldLabel: string;
  status: WorldFocusShellStatus;
  children?: ReactNode;
}>;

/**
 * Owns the persistent rectangular World Focus workspace without owning any
 * future module/composition semantics. Later stable/adaptive mini-verticals
 * render inside this boundary rather than adding lifecycle to WorldFocusPage.
 */
export function WorldFocusWorkspace({
  worldLabel,
  status,
  children,
}: WorldFocusWorkspaceProps) {
  const { t } = useTranslation('common');
  const statusMessage =
    status === 'loading'
      ? t(($) => $.common.worldFocus.states.loading, { world: worldLabel })
      : status === 'error'
        ? t(($) => $.common.worldFocus.states.error, { world: worldLabel })
        : status === 'unavailable'
          ? t(($) => $.common.worldFocus.states.unavailable, {
              world: worldLabel,
            })
          : null;

  return (
    <section
      className="world-focus-workspace"
      data-world-focus-region={WORLD_FOCUS_REGION.workspace}
      aria-label={t(($) => $.common.worldFocus.canvasLabel, {
        world: worldLabel,
      })}
      aria-busy={status === 'loading' ? true : undefined}
    >
      {statusMessage === null ? null : (
        <p
          className="world-focus-state"
          role={status === 'loading' ? 'status' : 'alert'}
        >
          {statusMessage}
        </p>
      )}
      {status === 'ready' ? children : null}
    </section>
  );
}
