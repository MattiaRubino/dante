import { describe, expect, it } from 'vitest';

import {
  isWorldFocusFeatureAvailable,
  parseWorldFocusSafeExternalUrl,
  WORLD_FOCUS_COMPOSITION_ORIGINS,
  WORLD_FOCUS_COMPOSITION_STABILITIES,
  WORLD_FOCUS_INTERACTION_DEPTHS,
  WORLD_FOCUS_PRESENTATION_SURFACES,
  WORLD_FOCUS_RESOURCE_STATUSES,
} from './world-focus-platform';

describe('World Focus B0 platform primitives', () => {
  it('keeps the shared status and ownership vocabularies finite', () => {
    expect(WORLD_FOCUS_RESOURCE_STATUSES).toEqual([
      'loading',
      'ready',
      'empty',
      'partial',
      'stale',
      'error',
      'unavailable',
    ]);
    expect(WORLD_FOCUS_COMPOSITION_STABILITIES).toEqual([
      'stable',
      'adaptive',
      'ephemeral',
    ]);
    expect(WORLD_FOCUS_COMPOSITION_ORIGINS).toEqual([
      'system-default',
      'user',
      'dante-proposed',
      'application-derived',
    ]);
    expect(WORLD_FOCUS_INTERACTION_DEPTHS).toEqual([
      'peek',
      'insight',
      'explore',
    ]);
    expect(WORLD_FOCUS_PRESENTATION_SURFACES).toEqual([
      'inline',
      'popover',
      'sidecar',
      'modal',
      'full-screen',
      'route',
    ]);
  });

  it('does not confuse disabled/unavailable capability state with available', () => {
    expect(isWorldFocusFeatureAvailable({ status: 'available' })).toBe(true);
    expect(
      isWorldFocusFeatureAvailable({
        status: 'disabled',
        reasonCode: 'rollout-disabled',
      }),
    ).toBe(false);
    expect(
      isWorldFocusFeatureAvailable({
        status: 'unavailable',
        reasonCode: 'provider-offline',
        retryable: true,
      }),
    ).toBe(false);
  });

  it('accepts only credential-free absolute HTTPS links', () => {
    expect(parseWorldFocusSafeExternalUrl(' https://example.com/path?q=1 ')).toEqual({
      href: 'https://example.com/path?q=1',
      protocol: 'https:',
      hostname: 'example.com',
    });

    expect(parseWorldFocusSafeExternalUrl('http://example.com')).toBeNull();
    expect(parseWorldFocusSafeExternalUrl('javascript:alert(1)')).toBeNull();
    expect(parseWorldFocusSafeExternalUrl('data:text/html,hello')).toBeNull();
    expect(parseWorldFocusSafeExternalUrl('/worlds/music')).toBeNull();
    expect(parseWorldFocusSafeExternalUrl('https://user:secret@example.com')).toBeNull();
    expect(parseWorldFocusSafeExternalUrl('not a url')).toBeNull();
  });
});
