import type { TransportItem } from '@grafana/faro-web-sdk';
import { describe, expect, it } from 'vitest';

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
});
