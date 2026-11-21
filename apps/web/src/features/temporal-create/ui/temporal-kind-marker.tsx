import './temporal-kind-marker.css';

/** One optical size and stroke for the two canonical Timeline item types. */
export function TemporalKindMarker({
  kind,
}: Readonly<{ kind: 'activity' | 'event' }>) {
  return (
    <svg
      className="temporal-kind-marker"
      data-temporal-kind-marker={kind}
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      aria-hidden="true"
      focusable="false"
    >
      {kind === 'activity' ? (
        <path d="M8 2.75 13.25 8 8 13.25 2.75 8Z" />
      ) : (
        <circle cx="8" cy="8" r="5.25" />
      )}
    </svg>
  );
}
