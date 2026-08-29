export type RecoveryProof = Readonly<{
  password_recovery_ref: string;
  secret: string;
}>;

export type RecoveryProofStore = Readonly<{
  peek: () => RecoveryProof | null;
  clear: () => void;
}>;

type RecoveryLocation = Pick<Location, 'pathname' | 'search' | 'hash'>;
type RecoveryHistory = Pick<History, 'state' | 'replaceState'>;

const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const MAX_RECOVERY_SECRET_LENGTH = 128;

function recoveryProofFromLocation(location: RecoveryLocation): RecoveryProof | null {
  const params = new URLSearchParams(location.search);
  const recoveryRefs = params.getAll('recovery');
  const secret = location.hash.startsWith('#') ? location.hash.slice(1) : '';

  if (
    recoveryRefs.length !== 1 ||
    !UUID_PATTERN.test(recoveryRefs[0] ?? '') ||
    secret.length === 0 ||
    secret.length > MAX_RECOVERY_SECRET_LENGTH
  ) {
    return null;
  }

  return Object.freeze({
    password_recovery_ref: recoveryRefs[0]!,
    secret,
  });
}

function locationWithoutRecoveryQuery(location: RecoveryLocation): string {
  const params = new URLSearchParams(location.search);
  params.delete('recovery');
  const query = params.toString();
  return `${location.pathname}${query ? `?${query}` : ''}`;
}

export function captureRecoveryProof(
  location: RecoveryLocation,
  history: RecoveryHistory,
): RecoveryProofStore {
  const params = new URLSearchParams(location.search);
  const hasRecoveryEntry = params.has('recovery');
  let proof = recoveryProofFromLocation(location);

  if (hasRecoveryEntry && location.hash) {
    history.replaceState(history.state, '', `${location.pathname}${location.search}`);
  }

  return Object.freeze({
    peek: () => proof,
    clear: () => {
      proof = null;
      if (hasRecoveryEntry) {
        history.replaceState(
          history.state,
          '',
          locationWithoutRecoveryQuery(location),
        );
      }
    },
  });
}

export function captureWindowRecoveryProof(): RecoveryProofStore {
  return captureRecoveryProof(window.location, window.history);
}
