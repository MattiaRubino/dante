import type { TransportItem } from '@grafana/faro-web-sdk';
import { describe, expect, it, vi } from 'vitest';

import { sanitizeText, sanitizeTransportItem, sanitizeUrl } from './sanitize';

const EMAIL = 'person@example.com';
const REFERENCE = '018f47ab-5c21-7c5e-923b-5b8cc48bd871';

describe('browser telemetry sanitization', () => {
  it('removes query, fragment and identifiers from URLs', () => {
    const sanitized = sanitizeUrl(
      `https://dante.example/api/accounts/${REFERENCE}/${EMAIL}?token=secret#private`,
    );

    expect(sanitized).toBe(
      'https://dante.example/api/accounts/[redacted]/[redacted]',
    );
  });

  it('removes URL credentials and identifier-like numeric path segments', () => {
    const sanitized = sanitizeUrl(
      'https://person:secret@dante.example/api/accounts/123456?token=secret',
    );

    expect(sanitized).toBe('https://dante.example/api/accounts/[redacted]');
    expect(sanitized).not.toContain('person');
    expect(sanitized).not.toContain('secret');
  });

  it('redacts credentials and identifiers embedded in unstructured text', () => {
    const sanitized = sanitizeText(
      `Bearer top.secret-token for ${EMAIL} at https://dante.example/a/${REFERENCE}?code=secret`,
    );

    expect(sanitized).not.toContain('top.secret-token');
    expect(sanitized).not.toContain(EMAIL);
    expect(sanitized).not.toContain(REFERENCE);
    expect(sanitized).not.toContain('code=secret');
    expect(sanitized).toContain('[REDACTED_AUTHORIZATION]');
  });

  it('redacts sensitive fields recursively while preserving low-cardinality dimensions', () => {
    const item = {
      type: 'event',
      payload: {
        attributes: {
          route_id: '/access',
          outcome: 'invalid_credentials',
          password: 'never-export-this',
          email: EMAIL,
          nested: {
            authorization: 'Bearer never-export-this-either',
            account_ref: REFERENCE,
          },
        },
      },
    } as unknown as TransportItem;

    const sanitized = sanitizeTransportItem(item);
    const serialized = JSON.stringify(sanitized);

    expect(serialized).toContain('/access');
    expect(serialized).toContain('invalid_credentials');
    expect(serialized).not.toContain('never-export');
    expect(serialized).not.toContain(EMAIL);
    expect(serialized).not.toContain(REFERENCE);
  });

  it('bounds untrusted strings before export', () => {
    const sanitized = sanitizeText('x'.repeat(3_000));

    expect(sanitized.length).toBeLessThan(2_100);
    expect(sanitized.endsWith('…[TRUNCATED]')).toBe(true);
  });

  it('redacts user identifiers across common field naming conventions', () => {
    const item = {
      type: 'event',
      payload: {
        attributes: {
          user_id: '123456',
          userName: 'private-name',
          user_ref: REFERENCE,
        },
      },
    } as unknown as TransportItem;

    const serialized = JSON.stringify(sanitizeTransportItem(item));

    expect(serialized).not.toContain('123456');
    expect(serialized).not.toContain('private-name');
    expect(serialized).not.toContain(REFERENCE);
  });

  it('normalizes SDK-v2 event attributes to Alloy v1.19 string maps', () => {
    const item = {
      type: 'event',
      meta: {
        user: { id: 'private-user-id' },
        browser: { userAgent: 'private browser fingerprint' },
        page: { url: 'https://dante.example/private-path?token=never-export' },
        session: { id: 'private-session-id' },
      },
      payload: {
        attributes: 'not-a-string-map',
      },
    } as unknown as TransportItem;

    const sanitized = sanitizeTransportItem(item) as unknown as {
      meta: Record<string, unknown>;
      payload: Record<string, unknown>;
    };

    expect(sanitized.meta).not.toHaveProperty('user');
    expect(sanitized.meta).not.toHaveProperty('browser');
    expect(sanitized.meta).not.toHaveProperty('page');
    expect(sanitized.meta).not.toHaveProperty('session');
    expect(sanitized.payload).not.toHaveProperty('attributes');
  });

  it('normalizes or removes trace context at the Alloy protocol boundary', () => {
    const item = {
      type: 'measurement',
      meta: {},
      payload: {
        context: {},
        trace: {
          traceId: '0123456789abcdef0123456789abcdef',
          spanId: '0123456789abcdef',
        },
        values: { duration: 12.5 },
      },
    } as unknown as TransportItem;
    const malformedItem = {
      type: 'measurement',
      meta: {},
      payload: { trace: 'not-a-trace-context' },
    } as unknown as TransportItem;

    const sanitized = sanitizeTransportItem(item) as unknown as {
      payload: Record<string, unknown>;
    };
    const malformed = sanitizeTransportItem(malformedItem) as unknown as {
      payload: Record<string, unknown>;
    };

    expect(sanitized.payload.trace).toEqual({
      trace_id: '0123456789abcdef0123456789abcdef',
      span_id: '0123456789abcdef',
    });
    expect(malformed.payload).not.toHaveProperty('trace');
  });

  it('removes automatic Web Vitals context before it reaches the collector', () => {
    const item = {
      type: 'measurement',
      meta: {},
      payload: {
        context: {
          element: 'main>section>input#private-id',
          id: 'v6-1788116460400-6582841316571',
          navigation_entry_id: 'zXamkWxPJ',
          navigation_type: 'reload',
          rating: 'good',
        },
        values: { lcp: 92, resource_load_delay: 68 },
      },
    } as unknown as TransportItem;

    const sanitized = sanitizeTransportItem(item) as unknown as {
      payload: Record<string, unknown>;
    };

    expect(sanitized.payload).not.toHaveProperty('context');
    expect(sanitized.payload.values).toEqual({
      lcp: 92,
      resource_load_delay: 68,
    });
    expect(JSON.stringify(sanitized)).not.toContain('private-id');
    expect(JSON.stringify(sanitized)).not.toContain('6582841316571');
  });

  it('handles circular objects and accessors without evaluating untrusted code', () => {
    const getter = vi.fn(() => 'never-read-this');
    const attributes: Record<string, unknown> = {};
    Object.defineProperty(attributes, 'computed', {
      enumerable: true,
      get: getter,
    });
    attributes.circular = attributes;
    const item = {
      type: 'event',
      payload: { attributes },
    } as unknown as TransportItem;

    const serialized = JSON.stringify(sanitizeTransportItem(item));

    expect(getter).not.toHaveBeenCalled();
    expect(serialized).toContain('[ACCESSOR_REDACTED]');
    expect(serialized).toContain('[CIRCULAR]');
    expect(serialized).not.toContain('never-read-this');
  });

  it('drops an item when an adversarial object prevents safe inspection', () => {
    const item = new Proxy(
      { type: 'event' },
      {
        ownKeys() {
          throw new Error('private proxy failure');
        },
      },
    ) as unknown as TransportItem;

    expect(sanitizeTransportItem(item)).toBeNull();
  });
});
