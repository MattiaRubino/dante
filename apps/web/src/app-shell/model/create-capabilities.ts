export type CreateCapabilityId = 'event' | 'task' | 'capture';

export type CreateCapability = {
  id: CreateCapabilityId;
  status: 'deferred';
  owner: 'timeline' | 'tasks' | 'capture';
};

export const CREATE_CAPABILITIES = [
  { id: 'event', status: 'deferred', owner: 'timeline' },
  { id: 'task', status: 'deferred', owner: 'tasks' },
  { id: 'capture', status: 'deferred', owner: 'capture' },
] as const satisfies readonly CreateCapability[];
