/**
 * Same-browser ordering for operations that change or fingerprint generated
 * Occurrence identities. A checkpoint can alter the selected-and-following
 * inventory between a series preview and its acceptance.
 *
 * Reserve queue position synchronously, including the CSRF fetch, so a
 * checkpoint already started cannot overtake an upcoming preview. Rejections
 * release the next operation. Cross-tab writers and changes after a review
 * are still rejected by the server's source-revision and preview-fingerprint
 * CAS: this is NOT an authorization or an automatic stale-preview retry.
 *
 * Read-only Timeline requests stay concurrent; no user data is retained.
 */
let settled = Promise.resolve();

export function withTemporalOccurrenceInventoryFence<T>(
  operation: () => Promise<T>,
): Promise<T> {
  const result = settled.then(operation);
  settled = result.then(() => undefined, () => undefined);
  return result;
}
