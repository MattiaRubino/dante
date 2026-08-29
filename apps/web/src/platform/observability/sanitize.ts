import type { TransportItem } from '@grafana/faro-web-sdk';

const MAX_DEPTH = 8;
const MAX_ARRAY_ITEMS = 50;
const MAX_OBJECT_KEYS = 100;
const MAX_STRING_CHARACTERS = 2_048;

const SENSITIVE_KEY =
  /(?:authorization|cookie|csrf|email|password|pepper|secret|token|verifier|account[_-]?ref|identity[_-]?ref|auth[_-]?session|\buser\b)/i;
const EMAIL_PATTERN = /[\w.+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,63}/i;
const EMAIL = /[\w.+-]{1,64}@[A-Za-z0-9.-]{1,253}\.[A-Za-z]{2,63}/g;
const AUTHORIZATION = /\b(?:basic|bearer)\s+[A-Za-z0-9._~+/=-]+/gi;
const SECRET_ASSIGNMENT =
  /\b(?:authorization|cookie|csrf|password|pepper|secret|token|verifier)(?:\s*[:=]\s*|%3[dD])(?:[^\s,;]+)/gi;
const JWT = /\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g;
const UUID_PATTERN =
  /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/i;
const UUID =
  /\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b/gi;
const URL_VALUE = /https?:\/\/[^\s"'<>]+/gi;
const DSN_USERINFO = /(?<scheme>postgres(?:ql)?(?:\+\w+)?:\/\/)[^\s/@]+@/gi;
const IPV4 =
  /(?<![\d.])(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![\d.])/g;
const CONTROL_CHARACTERS = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g;

function truncate(value: string): string {
  return value.length <= MAX_STRING_CHARACTERS
    ? value
    : `${value.slice(0, MAX_STRING_CHARACTERS)}…[TRUNCATED]`;
}

export function sanitizeUrl(value: string): string {
  try {
    const parsed = new URL(
      value,
      globalThis.location?.origin ?? 'https://dante.invalid',
    );
    parsed.search = '';
    parsed.hash = '';
    parsed.pathname = parsed.pathname
      .split('/')
      .map((segment) => {
        if (!segment) {
          return segment;
        }
        const decoded = decodeURIComponent(segment);
        if (
          EMAIL_PATTERN.test(decoded) ||
          UUID_PATTERN.test(decoded) ||
          decoded.length > 64
        ) {
          return '[redacted]';
        }
        return segment;
      })
      .join('/');
    return parsed.toString();
  } catch {
    return '[REDACTED_URL]';
  }
}

export function sanitizeText(value: string): string {
  const sanitized = value
    .replace(CONTROL_CHARACTERS, '�')
    .replace(DSN_USERINFO, '$<scheme>[REDACTED]@')
    .replace(AUTHORIZATION, '[REDACTED_AUTHORIZATION]')
    .replace(SECRET_ASSIGNMENT, '[REDACTED_SECRET]')
    .replace(JWT, '[REDACTED_TOKEN]')
    .replace(EMAIL, '[REDACTED_EMAIL]')
    .replace(UUID, '[REDACTED_REFERENCE]')
    .replace(IPV4, '[REDACTED_IP]')
    .replace(URL_VALUE, (url) => sanitizeUrl(url));
  return truncate(sanitized);
}

function sanitizeValue(value: unknown, key: string, depth: number): unknown {
  if (SENSITIVE_KEY.test(key)) {
    return '[REDACTED]';
  }
  if (depth > MAX_DEPTH) {
    return '[TRUNCATED_DEPTH]';
  }
  if (typeof value === 'string') {
    return sanitizeText(value);
  }
  if (
    value === null ||
    typeof value === 'boolean'
  ) {
    return value;
  }
  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : '[NON_FINITE]';
  }
  if (Array.isArray(value)) {
    return value
      .slice(0, MAX_ARRAY_ITEMS)
      .map((entry) => sanitizeValue(entry, key, depth + 1));
  }
  if (typeof value === 'object') {
    const output: Record<string, unknown> = {};
    for (const [childKey, childValue] of Object.entries(value).slice(
      0,
      MAX_OBJECT_KEYS,
    )) {
      const sanitizedKey = sanitizeText(childKey);
      output[sanitizedKey] = sanitizeValue(childValue, childKey, depth + 1);
    }
    return output;
  }
  return `[${typeof value}]`;
}

export function sanitizeTransportItem(
  item: TransportItem,
): TransportItem | null {
  return sanitizeValue(item, '', 0) as TransportItem;
}
