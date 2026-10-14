/** Read the URL that a fetch mock actually received. */
export function fetchRequestUrl(input: RequestInfo | URL | undefined): string {
  if (input === undefined) throw new Error('Expected a fetch request URL.');
  if (typeof input === 'string') return input;
  if (input instanceof URL) return input.href;
  return input.url;
}

/** Require the JSON text emitted by the client instead of stringifying objects. */
export function fetchRequestBody(body: BodyInit | null | undefined): string {
  if (typeof body !== 'string') {
    throw new Error('Expected a serialized JSON request body.');
  }
  return body;
}
