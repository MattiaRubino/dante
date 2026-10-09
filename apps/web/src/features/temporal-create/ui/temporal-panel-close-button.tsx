import type { Ref } from 'react';

import './temporal-panel-controls.css';

export function TemporalPanelCloseButton({ label, onClick, disabled, title, buttonRef,
}: Readonly<{
  label: string;
  onClick: () => void;
  disabled?: boolean;
  title?: string;
  buttonRef?: Ref<HTMLButtonElement>;
}>) {
  return <button ref={buttonRef} className="dante-temporal-panel-close"
    type="button" disabled={disabled} onClick={onClick}
    aria-label={label} title={title ?? label}>
    <span aria-hidden="true">×</span>
  </button>;
}
