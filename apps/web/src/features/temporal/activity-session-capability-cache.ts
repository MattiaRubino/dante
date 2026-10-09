import {
  createRemoteTemporalSessionCapabilityDataSource,
  type SessionCaptureMode,
} from './remote-session-capability-data-source';

export const defaultActivitySessionSource = createRemoteTemporalSessionCapabilityDataSource();
const capabilityReads = new Map<string, Promise<SessionCaptureMode>>();

export function cachedActivitySessionCapability(activityRef: string): Promise<SessionCaptureMode> {
  const existing = capabilityReads.get(activityRef);
  if (existing) return existing;
  const pending = defaultActivitySessionSource.activityMode!(activityRef).catch((error: unknown) => {
    capabilityReads.delete(activityRef);
    throw error;
  });
  capabilityReads.set(activityRef, pending);
  return pending;
}

export function invalidateActivitySessionCardCapability(activityRef?: string): void {
  if (activityRef === undefined) capabilityReads.clear();
  else capabilityReads.delete(activityRef);
}
