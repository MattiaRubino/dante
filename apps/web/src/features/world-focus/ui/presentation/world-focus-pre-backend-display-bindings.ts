import type { WorldFocusId } from '../../model/world-focus-identity';
import {
  createWorldFocusDisplayBindingSet,
  type WorldFocusDisplayBindingSet,
} from './world-focus-display-bindings';

const EMPTY_BINDINGS = createWorldFocusDisplayBindingSet([]);

const MUSIC_BINDINGS = createWorldFocusDisplayBindingSet([
  {
    reference: { kind: 'release', key: 'neon-static' },
    label: 'Neon Static',
    supportingText: 'Release',
  },
  {
    reference: { kind: 'material-state', key: 'neon-static-master-v3' },
    label: 'Master v3',
  },
  {
    reference: { kind: 'schedule', key: 'neon-static-release' },
    label: 'Release schedule',
  },
  {
    reference: { kind: 'dependency', key: 'neon-static-artwork-approval' },
    label: 'Artwork approval',
  },
  {
    reference: { kind: 'observation', key: 'neon-static-mix-review' },
    label: 'Mix review',
  },
  {
    reference: { kind: 'provenance', key: 'neon-static-studio-import' },
    label: 'Studio import',
  },
  {
    reference: { kind: 'material-state', key: 'neon-static-master-v2' },
    label: 'Master v2',
  },
  {
    reference: { kind: 'request', key: 'artwork-review-request' },
    label: 'Artwork review request',
  },
  {
    reference: { kind: 'comparison-basis', key: 'master-review' },
    label: 'Master review',
  },
  {
    reference: { kind: 'observation', key: 'release-day-minus-1' },
    label: 'Day before release',
  },
  {
    reference: { kind: 'observation', key: 'release-day' },
    label: 'Release day',
  },
  {
    reference: { kind: 'window', key: 'release-window' },
    label: 'Release window',
  },
]);

const TRAVEL_BINDINGS = createWorldFocusDisplayBindingSet([
  {
    reference: { kind: 'plan', key: 'japan-2027' },
    label: 'Japan 2027',
    supportingText: 'Planning',
  },
  {
    reference: { kind: 'checkpoint', key: 'japan-flight-shortlist' },
    label: 'Flight shortlist',
  },
  {
    reference: { kind: 'continuation-intent', key: 'japan-flight-review' },
    label: 'Review flight shortlist',
  },
  {
    reference: { kind: 'observation', key: 'japan-flight-price-check' },
    label: 'Flight price check',
  },
  {
    reference: { kind: 'provenance', key: 'japan-flight-search-import' },
    label: 'Flight search import',
  },
]);

/**
 * Bounded pre-backend display adapter. Copy is presentation fixture data only;
 * it is not canonical Domain truth and reference keys are never shown as copy.
 */
export function getWorldFocusPreBackendDisplayBindings(
  worldId: WorldFocusId,
): WorldFocusDisplayBindingSet {
  if (worldId === 'music') return MUSIC_BINDINGS;
  if (worldId === 'travel') return TRAVEL_BINDINGS;
  return EMPTY_BINDINGS;
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
