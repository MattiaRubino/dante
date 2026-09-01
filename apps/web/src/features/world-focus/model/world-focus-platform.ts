export const WORLD_FOCUS_RESOURCE_STATUSES = [
  'loading',
  'ready',
  'empty',
  'partial',
  'stale',
  'error',
  'unavailable',
] as const;

export type WorldFocusResourceStatus =
  (typeof WORLD_FOCUS_RESOURCE_STATUSES)[number];

export type WorldFocusShellStatus = Extract<
  WorldFocusResourceStatus,
  'loading' | 'ready' | 'error' | 'unavailable'
>;

export const WORLD_FOCUS_COMPOSITION_STABILITIES = [
  'stable',
  'adaptive',
  'ephemeral',
] as const;

export type WorldFocusCompositionStability =
  (typeof WORLD_FOCUS_COMPOSITION_STABILITIES)[number];

export const WORLD_FOCUS_COMPOSITION_ORIGINS = [
  'system-default',
  'user',
  'dante-proposed',
  'application-derived',
] as const;

export type WorldFocusCompositionOrigin =
  (typeof WORLD_FOCUS_COMPOSITION_ORIGINS)[number];

export type WorldFocusCompositionOwnership = Readonly<{
  stability: WorldFocusCompositionStability;
  origin: WorldFocusCompositionOrigin;
}>;

export const WORLD_FOCUS_INTERACTION_DEPTHS = [
  'peek',
  'insight',
  'explore',
] as const;

export type WorldFocusInteractionDepth =
  (typeof WORLD_FOCUS_INTERACTION_DEPTHS)[number];

export const WORLD_FOCUS_PRESENTATION_SURFACES = [
  'inline',
  'popover',
  'sidecar',
  'modal',
  'full-screen',
  'route',
] as const;

export type WorldFocusPresentationSurface =
  (typeof WORLD_FOCUS_PRESENTATION_SURFACES)[number];

export type WorldFocusFeatureAvailability =
  | Readonly<{ status: 'available' }>
  | Readonly<{ status: 'disabled'; reasonCode: string }>
  | Readonly<{
      status: 'unavailable';
      reasonCode: string;
      retryable: boolean;
    }>;

export function isWorldFocusFeatureAvailable(
  availability: WorldFocusFeatureAvailability,
): availability is Extract<
  WorldFocusFeatureAvailability,
  Readonly<{ status: 'available' }>
> {
  return availability.status === 'available';
}

export type WorldFocusVersionedPayload<
  Version extends string | number = string | number,
> = Readonly<{
  schemaVersion: Version;
}>;

export type WorldFocusSafeExternalUrl = Readonly<{
  href: string;
  protocol: 'https:';
  hostname: string;
}>;

/**
 * Converts untrusted user/provider/AI text into a clickable external URL only
 * when it is an absolute HTTPS URL without embedded credentials. Internal app
 * navigation remains a router concern and never passes through this helper.
 */
export function parseWorldFocusSafeExternalUrl(
  input: string,
): WorldFocusSafeExternalUrl | null {
  const candidate = input.trim();
  if (candidate.length === 0) {
    return null;
  }

  try {
    const url = new URL(candidate);
    if (
      url.protocol !== 'https:' ||
      url.username.length > 0 ||
      url.password.length > 0
    ) {
      return null;
    }

    return Object.freeze({
      href: url.href,
      protocol: 'https:' as const,
      hostname: url.hostname,
    });
  } catch {
    return null;
  }
}
