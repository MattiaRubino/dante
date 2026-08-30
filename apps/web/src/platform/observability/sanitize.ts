import type { TransportItem } from '@grafana/faro-web-sdk';

const MAX_DEPTH = 8;
const MAX_ARRAY_ITEMS = 50;
const MAX_OBJECT_KEYS = 100;
const MAX_STRING_CHARACTERS = 2_048;
const MAX_TOTAL_NODES = 1_000;
const MAX_URL_CHARACTERS = 4_096;

const SENSITIVE_KEY =
  /(?:authorization|cookie|csrf|email|password|pepper|secret|token|verifier|account[_-]?ref|identity[_-]?ref|auth[_-]?session|\buser(?:[_-]?(?:id|ref|name))?\b)/i;
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
const IDENTIFIER_LIKE_SEGMENT =
  /^(?:\d{4,}|[A-Fa-f0-9]{12,}|[A-Za-z0-9_-]{24,})$/;

type SanitizationState = {
  remainingNodes: number;
  readonly seen: WeakSet<object>;
};

function truncate(value: string): string {
  return value.length <= MAX_STRING_CHARACTERS
    ? value
    : `${value.slice(0, MAX_STRING_CHARACTERS)}…[TRUNCATED]`;
}

function replaceControlCharacters(value: string): string {
  let output = '';
  for (const character of value) {
    const codePoint = character.codePointAt(0) ?? 0;
    output +=
      codePoint <= 8 ||
      codePoint === 11 ||
      codePoint === 12 ||
      (codePoint >= 14 && codePoint <= 31) ||
      codePoint === 127
        ? '�'
        : character;
  }
  return output;
}

export function sanitizeUrl(value: string): string {
  if (value.length > MAX_URL_CHARACTERS) {
    return '[REDACTED_URL]';
  }
  try {
    const parsed = new URL(
      value,
      globalThis.location?.origin ?? 'https://dante.invalid',
    );
    if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
      return '[REDACTED_URL]';
    }
    parsed.username = '';
    parsed.password = '';
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
          IDENTIFIER_LIKE_SEGMENT.test(decoded) ||
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
  const sanitized = replaceControlCharacters(value)
    .replace(URL_VALUE, (url) => sanitizeUrl(url))
    .replace(DSN_USERINFO, '$<scheme>[REDACTED]@')
    .replace(AUTHORIZATION, '[REDACTED_AUTHORIZATION]')
    .replace(SECRET_ASSIGNMENT, '[REDACTED_SECRET]')
    .replace(JWT, '[REDACTED_TOKEN]')
    .replace(EMAIL, '[REDACTED_EMAIL]')
    .replace(UUID, '[REDACTED_REFERENCE]')
    .replace(IPV4, '[REDACTED_IP]');
  return truncate(sanitized);
}

function sanitizeValue(
  value: unknown,
  key: string,
  depth: number,
  state: SanitizationState,
): unknown {
  if (SENSITIVE_KEY.test(key)) {
    return '[REDACTED]';
  }
  if (state.remainingNodes <= 0) {
    return '[TRUNCATED_BUDGET]';
  }
  state.remainingNodes -= 1;
  if (depth > MAX_DEPTH) {
    return '[TRUNCATED_DEPTH]';
  }
  if (typeof value === 'string') {
    return sanitizeText(value);
  }
  if (value === null || typeof value === 'boolean') {
    return value;
  }
  if (typeof value === 'number') {
    return Number.isFinite(value) ? value : '[NON_FINITE]';
  }
  if (Array.isArray(value)) {
    if (state.seen.has(value)) {
      return '[CIRCULAR]';
    }
    state.seen.add(value);
    return value
      .slice(0, MAX_ARRAY_ITEMS)
      .map((entry) => sanitizeValue(entry, key, depth + 1, state));
  }
  if (typeof value === 'object') {
    if (state.seen.has(value)) {
      return '[CIRCULAR]';
    }
    state.seen.add(value);
    const output = Object.create(null) as Record<string, unknown>;
    for (const childKey of Object.keys(value).slice(0, MAX_OBJECT_KEYS)) {
      const sanitizedKey = sanitizeText(childKey);
      const descriptor = Object.getOwnPropertyDescriptor(value, childKey);
      output[sanitizedKey] =
        descriptor !== undefined && 'value' in descriptor
          ? sanitizeValue(descriptor.value, childKey, depth + 1, state)
          : '[ACCESSOR_REDACTED]';
    }
    return output;
  }
  return `[${typeof value}]`;
}

export function sanitizeTransportItem(
  item: TransportItem,
): TransportItem | null {
  try {
    return sanitizeValue(item, '', 0, {
      remainingNodes: MAX_TOTAL_NODES,
      seen: new WeakSet<object>(),
    }) as TransportItem;
  } catch {
    return null;
  }
}
