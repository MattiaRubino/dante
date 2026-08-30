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
