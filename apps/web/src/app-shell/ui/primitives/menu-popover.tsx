import {
  useEffect,
  useEffectEvent,
  useRef,
  type KeyboardEvent,
  type ReactNode,
  type RefObject,
} from 'react';

type MenuPopoverProps = {
  id: string;
  label: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  triggerRef: RefObject<HTMLElement | null>;
  align?: 'start' | 'end';
  className?: string;
  children: ReactNode;
};

const MENU_ITEM_SELECTOR = '[role="menuitem"]:not(:disabled)';

export function MenuPopover({
  id,
  label,
  open,
  onOpenChange,
  triggerRef,
  align = 'end',
  className = '',
  children,
}: MenuPopoverProps) {
  const panelRef = useRef<HTMLDivElement>(null);
  const setOpenFromEffect = useEffectEvent(onOpenChange);

  useEffect(() => {
    if (!open) {
      return;
    }

    const handlePointerDown = (event: PointerEvent) => {
      const target = event.target as Node | null;

      if (
        target &&
        !panelRef.current?.contains(target) &&
        !triggerRef.current?.contains(target)
      ) {
        setOpenFromEffect(false);
      }
    };

    const handleDocumentKeyDown = (event: globalThis.KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        setOpenFromEffect(false);
        triggerRef.current?.focus();
      } else if (event.key === 'Tab') {
        setOpenFromEffect(false);
      }
    };

    document.addEventListener('pointerdown', handlePointerDown, true);
    document.addEventListener('keydown', handleDocumentKeyDown, true);

    queueMicrotask(() => {
      const firstItem = panelRef.current?.querySelector<HTMLElement>(
        MENU_ITEM_SELECTOR,
      );
      firstItem?.focus();
    });

    return () => {
      document.removeEventListener('pointerdown', handlePointerDown, true);
      document.removeEventListener('keydown', handleDocumentKeyDown, true);
    };
  }, [open, triggerRef]);

  if (!open) {
    return null;
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
      return;
    }

    const items = Array.from(
      panelRef.current?.querySelectorAll<HTMLElement>(MENU_ITEM_SELECTOR) ?? [],
    );

    if (items.length === 0) {
      return;
    }

    event.preventDefault();
    const currentIndex = Math.max(
      0,
      items.indexOf(document.activeElement as HTMLElement),
    );
    let nextIndex = currentIndex;

    if (event.key === 'ArrowDown') {
      nextIndex = (currentIndex + 1) % items.length;
    } else if (event.key === 'ArrowUp') {
      nextIndex = (currentIndex - 1 + items.length) % items.length;
    } else if (event.key === 'Home') {
      nextIndex = 0;
    } else if (event.key === 'End') {
      nextIndex = items.length - 1;
    }

    items[nextIndex]?.focus();
  };

  return (
    <div
      ref={panelRef}
      id={id}
      className={`app-popover-panel app-popover-panel-${align} ${className}`.trim()}
      role="menu"
      aria-label={label}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}
