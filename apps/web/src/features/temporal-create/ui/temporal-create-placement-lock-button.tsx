import { useTranslation } from 'react-i18next';

import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

export function TemporalCreatePlacementLockButton({
  locked,
  onToggle,
  kind,
  italian = true,
  disabled = false,
}: Readonly<{
  locked: boolean;
  onToggle: () => void;
  kind: 'activity' | 'event';
  italian?: boolean;
  disabled?: boolean;
}>) {
  const label = italian
    ? locked
      ? 'Sblocca spostamenti'
      : 'Blocca spostamenti'
    : locked
      ? 'Unlock placement'
      : 'Lock placement';
  const title = italian
    ? disabled
      ? 'Protezione disponibile solo per una collocazione salvata'
      : locked
        ? 'Consenti di nuovo gli spostamenti della collocazione'
        : 'Blocca gli spostamenti della collocazione'
    : disabled
      ? 'Protection requires an accepted Schedule'
      : locked
        ? 'Allow placement changes again'
        : 'Block placement changes';

  return (
    <button
      type="button"
      className="temporal-create-placement-lock"
      data-placement-protection={kind}
      aria-pressed={locked}
      aria-label={label}
      title={title}
      disabled={disabled}
      onClick={onToggle}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <rect x="5" y="10" width="14" height="11" rx="2" />
        {locked ? (
          <path d="M8 10V7a4 4 0 0 1 8 0v3" />
        ) : (
          <path d="M8 10V7a4 4 0 0 1 7.5-1.9" />
        )}
      </svg>
      <span>{label}</span>
    </button>
  );
}

export function TemporalCreateAdvancedEventHeaderActions() {
  const { i18n } = useTranslation('common');
  const { draft, patch } = useTemporalCreateU2Draft();
  const locked = draft.eventPlacementProtected === true;
  return (
    <TemporalCreatePlacementLockButton
      kind="event"
      italian={i18n.language.toLowerCase().startsWith('it')}
      locked={locked}
      onToggle={() => patch({ eventPlacementProtected: !locked })}
    />
  );
}
