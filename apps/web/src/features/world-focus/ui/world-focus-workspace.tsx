import {
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusShellStatus } from '../model/world-focus-platform';
import { WORLD_FOCUS_REGION } from '../model/world-focus-structure';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

type WorldFocusWorkspaceProps = Readonly<{
  worldLabel: string;
  status: WorldFocusShellStatus;
  context?: ReactNode;
  children?: ReactNode;
  surfaces?: ReactNode;
}>;

function getObservedInlineSize(entry: ResizeObserverEntry): number {
  const boxSize = entry.contentBoxSize;
  const firstBox = Array.isArray(boxSize) ? boxSize[0] : boxSize;
  return firstBox?.inlineSize ?? entry.contentRect.width;
}

/**
 * Owns the persistent rectangular World Focus workspace and only its physical
 * allocation. It measures the space actually granted to this workspace,
 * delegates deterministic surface allocation to the pure model, and exposes
 * that plan to descendants. It does not rank World content or own canonical
 * reality, authorization, DANTE runs or product-specific module semantics.
 */
export function WorldFocusWorkspace({
  worldLabel,
  status,
  context,
  children,
  surfaces,
}: WorldFocusWorkspaceProps) {
  const { t } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const sectionRef = useRef<HTMLElement | null>(null);
  const [inlineSize, setInlineSize] = useState(0);
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

  useLayoutEffect(() => {
    const section = sectionRef.current;
    if (section === null) {
      return;
    }

    const commitInlineSize = (nextInlineSize: number) => {
      const normalized = Math.max(0, nextInlineSize);
      setInlineSize((current) =>
        Math.abs(current - normalized) < 0.5 ? current : normalized,
      );
    };

    commitInlineSize(section.getBoundingClientRect().width);

    if (typeof ResizeObserver === 'undefined') {
      return;
    }

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry !== undefined) {
        commitInlineSize(getObservedInlineSize(entry));
      }
    });
    observer.observe(section);

    return () => observer.disconnect();
  }, []);

  const allocationPlan = useMemo(
    () => resolveWorldFocusWorkspaceAllocation(workspace.state, inlineSize),
    [inlineSize, workspace.state],
  );
  const allocationStyle = {
    '--world-focus-main-inline-size': `${allocationPlan.mainInlineSize}px`,
    '--world-focus-sidecar-inline-size': `${allocationPlan.sidecarInlineSize ?? 0}px`,
    '--world-focus-split-gap': `${allocationPlan.splitGap}px`,
  } as CSSProperties;
  const mainIsInert = allocationPlan.mainInteraction === 'inert';

  return (
    <section
      ref={sectionRef}
      className="world-focus-workspace"
      data-world-focus-region={WORLD_FOCUS_REGION.workspace}
      data-world-focus-main-allocation={allocationPlan.mainAllocation}
      data-world-focus-top-layer={allocationPlan.topLayer}
      data-world-focus-main-interaction={allocationPlan.mainInteraction}
      data-world-focus-inline-size={Math.round(allocationPlan.workspaceInlineSize)}
      aria-label={t(($) => $.common.worldFocus.canvasLabel, {
        world: worldLabel,
      })}
      aria-busy={status === 'loading' ? true : undefined}
      style={allocationStyle}
    >
      <WorldFocusWorkspaceAllocationProvider plan={allocationPlan}>
        <div
          className="world-focus-main-plane"
          data-world-focus-main-plane="true"
          inert={mainIsInert ? true : undefined}
        >
          {context}
          {statusMessage === null ? null : (
            <p
              className="world-focus-state"
              role={status === 'loading' ? 'status' : 'alert'}
            >
              {statusMessage}
            </p>
          )}
          {status === 'ready' ? children : null}
        </div>
        {status === 'ready' ? surfaces : null}
      </WorldFocusWorkspaceAllocationProvider>
    </section>
  );
}
