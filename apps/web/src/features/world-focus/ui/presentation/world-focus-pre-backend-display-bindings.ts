import type { WorldFocusId } from '../../model/world-focus-identity';
import {
  createWorldFocusDisplayBindingSet,
  type WorldFocusDisplayBindingSet,
} from './world-focus-display-bindings';

const EMPTY_BINDINGS = createWorldFocusDisplayBindingSet([]);

const MUSIC_BINDINGS = createWorldFocusDisplayBindingSet([
  { reference: { kind: 'release', key: 'neon-static' }, label: 'Neon Static', supportingText: 'Release' },
  { reference: { kind: 'material-state', key: 'neon-static-master-v3' }, label: 'Master v3' },
  { reference: { kind: 'schedule', key: 'neon-static-release' }, label: 'Release schedule' },
  { reference: { kind: 'dependency', key: 'neon-static-artwork-approval' }, label: 'Artwork approval' },
  { reference: { kind: 'observation', key: 'neon-static-mix-review' }, label: 'Mix review' },
  { reference: { kind: 'provenance', key: 'neon-static-studio-import' }, label: 'Studio import' },
  { reference: { kind: 'material-state', key: 'neon-static-master-v2' }, label: 'Master v2' },
  { reference: { kind: 'request', key: 'artwork-review-request' }, label: 'Artwork review request' },
  { reference: { kind: 'comparison-basis', key: 'master-review' }, label: 'Master review' },
  { reference: { kind: 'observation', key: 'release-day-minus-1' }, label: 'Day before release' },
  { reference: { kind: 'observation', key: 'release-day' }, label: 'Release day' },
  { reference: { kind: 'window', key: 'release-window' }, label: 'Release window' },
]);

/**
 * Bounded pre-backend display adapter. Copy is presentation fixture data only;
 * it is not canonical Domain truth and reference keys are never shown as copy.
 */
export function getWorldFocusPreBackendDisplayBindings(
  worldId: WorldFocusId,
): WorldFocusDisplayBindingSet {
  return worldId === 'music' ? MUSIC_BINDINGS : EMPTY_BINDINGS;
}

export function getWorldFocusPreBackendAttentionReasonText(
  worldId: WorldFocusId,
  reasonCode: string,
): string {
  if (worldId === 'music' && reasonCode === 'release-blocked') {
    return 'Artwork approval is blocking the release.';
  }
  throw new Error('World Focus attention reason display copy is unavailable');
}
