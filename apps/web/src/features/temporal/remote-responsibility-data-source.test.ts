import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalResponsibilityDataSource } from './remote-responsibility-data-source';

const PERSON = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const EVENT = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';

describe('Person referent remote commands', () => {
  it('creates, lists and renames a native Person with CSRF and revision', async () => {
    const calls: Array<{ url: string; method: string; body: unknown }> = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input, init) => {
      const url = String(input);
      const method = init?.method ?? 'GET';
      if (url.endsWith('/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (method !== 'GET') {
        expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf');
      }
      calls.push({
        url, method,
        body: init?.body ? JSON.parse(String(init.body)) as unknown : null,
      });
      if (url.endsWith('/person-referents') && method === 'GET') {
        return Response.json([{
          person_ref: PERSON, display_label: 'Anna', revision: 1, replayed: false,
        }]);
      }
      return Response.json({
        person_ref: PERSON,
        display_label: method === 'PATCH' ? 'Anna Rossi' : 'Anna',
        revision: method === 'PATCH' ? 2 : 1,
        replayed: false,
      });
    });
    const source = createRemoteTemporalResponsibilityDataSource(fetchFn);
    expect(await source.listPersonReferents()).toEqual([
      { personRef: PERSON, displayLabel: 'Anna', revision: 1, replayed: false },
    ]);
    expect((await source.createPersonReferent('op1', 'Anna')).personRef).toBe(PERSON);
    expect((await source.renamePersonReferent(PERSON, 'op2', 1, 'Anna Rossi'))
      .displayLabel).toBe('Anna Rossi');
    expect(calls.map(({ method }) => method)).toEqual(['GET', 'POST', 'PATCH']);
    expect(calls[2]?.body).toMatchObject({
      expected_revision: 1, display_label: 'Anna Rossi',
    });
  });

  it('sends the selected Person and the current holder without collapsing roles', async () => {
    const bodies: unknown[] = [];
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input, init) => {
      if (String(input).endsWith('/auth/session')) {
        return Response.json({ authenticated: true, csrf_token: 'csrf' });
      }
      bodies.push(JSON.parse(String(init?.body)) as unknown);
      if (String(input).endsWith('/expected-participation')) {
        return Response.json({
          event_ref: EVENT, participant_person_ref: PERSON,
          participant_is_self: false, requirement_code: 'optional',
          established_at: '2026-09-25T08:00:00Z', replayed: false,
        });
      }
      return Response.json({
        subject_kind: 'event', subject_native_ref: EVENT,
        responsible_person_ref: PERSON, responsible_is_self: false,
        established_at: '2026-09-25T08:00:00Z', replayed: false,
      });
    });
    const source = createRemoteTemporalResponsibilityDataSource(fetchFn);
    await source.setResponsibility('event', EVENT, {
      operationId: 'assign', holder: PERSON, expectedHolder: 'self',
    });
    await source.setExpectedParticipation(EVENT, {
      operationId: 'expect', participant: PERSON, requirementCode: 'optional',
      expectedRequirementCode: null,
    });
    expect(bodies).toEqual([
      { operation_id: 'assign', holder: PERSON, expected_holder: 'self' },
      {
        operation_id: 'expect', participant: PERSON,
        requirement_code: 'optional', expected_requirement_code: null,
      },
    ]);
  });
});
