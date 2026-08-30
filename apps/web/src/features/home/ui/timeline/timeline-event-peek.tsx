import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import './timeline-peek.css';

import { formatTimelineMinute } from './model/timeline-temporal';
import type { TimelineEvent, TimelineGroup } from './model/timeline-types';

type PeekPlacement = 'left' | 'right' | 'above' | 'below';

type PeekPosition = Readonly<{
  left: number;
  top: number;
  placement: PeekPlacement;
}>;

type TimelineEventPeekProps = Readonly<{
  event: TimelineEvent;
  group: TimelineGroup | undefined;
  opener: HTMLElement;
  focused: boolean;
  onDismiss: (restoreFocus: boolean) => void;
  onHandoff: () => void;
  onOpenDetail: (event: TimelineEvent, opener: HTMLElement) => void;
  onToggleFocus: (eventId: string) => void;
}>;

export const TIMELINE_EVENT_PEEK_ID = 'timeline-event-peek';

const PEEK_GAP_PX = 10;
const PEEK_VIEWPORT_GUTTER_PX = 8;
const PEEK_DESKTOP_WIDTH_PX = 304;
const PEEK_ESTIMATED_HEIGHT_PX = 190;
const PEEK_COMPACT_BREAKPOINT_PX = 720;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function computePeekPosition(
  opener: HTMLElement,
  width: number,
  height: number,
): PeekPosition {
  const rect = opener.getBoundingClientRect();
  const gutter = PEEK_VIEWPORT_GUTTER_PX;
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const maxLeft = Math.max(gutter, viewportWidth - width - gutter);
  const maxTop = Math.max(gutter, viewportHeight - height - gutter);

  if (viewportWidth <= PEEK_COMPACT_BREAKPOINT_PX) {
    const fitsBelow = rect.bottom + PEEK_GAP_PX + height <= viewportHeight - gutter;
    const placement: PeekPlacement = fitsBelow ? 'below' : 'above';
    const rawTop = fitsBelow
      ? rect.bottom + PEEK_GAP_PX
      : rect.top - height - PEEK_GAP_PX;
    return {
      left: clamp(rect.left, gutter, maxLeft),
      top: clamp(rawTop, gutter, maxTop),
      placement,
    };
  }

  const fitsRight =
    rect.right + PEEK_GAP_PX + width <= viewportWidth - gutter;
  const fitsLeft = rect.left - PEEK_GAP_PX - width >= gutter;

  if (fitsRight || !fitsLeft) {
    return {
      left: clamp(rect.right + PEEK_GAP_PX, gutter, maxLeft),
      top: clamp(rect.top, gutter, maxTop),
      placement: 'right',
    };
  }

  return {
    left: clamp(rect.left - width - PEEK_GAP_PX, gutter, maxLeft),
    top: clamp(rect.top, gutter, maxTop),
    placement: 'left',
  };
}

export function TimelineEventPeek({
  event,
  group,
  opener,
  focused,
  onDismiss,
  onHandoff,
  onOpenDetail,
  onToggleFocus,
}: TimelineEventPeekProps) {
  const { t } = useTranslation('common');
  const peekRef = useRef<HTMLDivElement | null>(null);
  const [position, setPosition] = useState<PeekPosition>(() =>
    computePeekPosition(
      opener,
      Math.min(
        PEEK_DESKTOP_WIDTH_PX,
        Math.max(0, window.innerWidth - PEEK_VIEWPORT_GUTTER_PX * 2),
      ),
      PEEK_ESTIMATED_HEIGHT_PX,
    ),
  );

  useLayoutEffect(() => {
    const update = () => {
      if (!opener.isConnected) {
        onDismiss(false);
        return;
      }
      const peekRect = peekRef.current?.getBoundingClientRect();
      const width = Math.min(
        peekRect?.width ?? PEEK_DESKTOP_WIDTH_PX,
        Math.max(0, window.innerWidth - PEEK_VIEWPORT_GUTTER_PX * 2),
      );
      const height = peekRect?.height ?? PEEK_ESTIMATED_HEIGHT_PX;
      setPosition(computePeekPosition(opener, width, height));
    };

    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);

    const resizeObserver =
      typeof ResizeObserver === 'undefined'
        ? null
        : new ResizeObserver(() => update());
    resizeObserver?.observe(opener);
    if (peekRef.current) {
      resizeObserver?.observe(peekRef.current);
    }

    return () => {
      resizeObserver?.disconnect();
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, [onDismiss, opener]);

  useEffect(() => {
    const onPointerDown = (pointerEvent: PointerEvent) => {
      const target = pointerEvent.target;
      if (!(target instanceof Node)) {
        return;
      }
      if (
        peekRef.current?.contains(target) ||
        (opener.isConnected && opener.contains(target))
      ) {
        return;
      }
      onDismiss(false);
    };

    const onKeyDown = (keyboardEvent: globalThis.KeyboardEvent) => {
      if (keyboardEvent.key !== 'Escape') {
        return;
      }
      keyboardEvent.preventDefault();
      keyboardEvent.stopPropagation();
      onDismiss(true);
    };

    document.addEventListener('pointerdown', onPointerDown, true);
    document.addEventListener('keydown', onKeyDown, true);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown, true);
      document.removeEventListener('keydown', onKeyDown, true);
    };
  }, [onDismiss, opener]);

  const subitemsCount = event.subitems?.length ?? 0;

  return createPortal(
    <div
      id={TIMELINE_EVENT_PEEK_ID}
      ref={peekRef}
      className="timeline-event-peek"
      role="dialog"
      aria-modal="false"
      aria-label={t(($) => $.common.home.timeline.peek.dialogLabel, {
        title: event.title,
      })}
      data-placement={position.placement}
      data-timeline-tone={group?.tone ?? 'personal'}
      style={{ left: position.left, top: position.top }}
    >
      <div className="timeline-event-peek__header">
        <div className="timeline-event-peek__identity">
          <span className="timeline-event-peek__tone" aria-hidden="true" />
          <div>
            <h3>{event.title}</h3>
            <p>
              {formatTimelineMinute(event.startMinute)}–
              {formatTimelineMinute(event.endMinute)}
              {group ? ` · ${group.label}` : ''}
            </p>
          </div>
        </div>
        <button
          className="timeline-event-peek__close"
          type="button"
          onClick={() => onDismiss(true)}
          aria-label={t(($) => $.common.home.timeline.peek.close)}
        >
          ×
        </button>
      </div>

      {event.meta || subitemsCount > 0 ? (
        <div className="timeline-event-peek__summary">
          {event.meta ? <span>{event.meta}</span> : null}
          {subitemsCount > 0 ? (
            <span>
              {t(($) => $.common.home.timeline.peek.subitems, {
                count: subitemsCount,
              })}
            </span>
          ) : null}
        </div>
      ) : null}

      <div className="timeline-event-peek__actions">
        <button
          className="timeline-event-peek__action is-primary"
          type="button"
          onClick={() => {
            onHandoff();
            onOpenDetail(event, opener);
          }}
        >
          {t(($) => $.common.home.timeline.peek.openDetail)}
        </button>
        <button
          className="timeline-event-peek__action"
          type="button"
          aria-pressed={focused}
          onClick={() => onToggleFocus(event.id)}
        >
          {focused
            ? t(($) => $.common.home.timeline.peek.clearFocus)
            : t(($) => $.common.home.timeline.peek.focus)}
        </button>
      </div>
    </div>,
    document.body,
  );
}
