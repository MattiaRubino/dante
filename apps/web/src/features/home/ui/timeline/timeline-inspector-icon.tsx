import type { ReactNode } from 'react';

type InspectorIconName = 'edit' | 'copy' | 'trash' | 'unschedule';

export function TimelineInspectorIcon({ name }: Readonly<{ name: InspectorIconName }>) {
  const paths = {
    edit: <><path d="M4 20h4l11-11a2 2 0 0 0-4-4L4 16v4Z" /><path d="m13.5 6.5 4 4" /></>,
    copy: <><rect x="8" y="8" width="12" height="12" rx="2" /><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" /></>,
    trash: <><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13" /><path d="M10 11v5M14 11v5" /></>,
    unschedule: <><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M7 3v4M17 3v4M3 10h18M8 15h8M13 12l3 3-3 3" /></>,
  } satisfies Record<InspectorIconName, ReactNode>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor"
    strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}
