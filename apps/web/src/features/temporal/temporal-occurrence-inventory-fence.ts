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
  settled = result.then(
    () => undefined,
    () => undefined,
  );
  return result;
}

/**
 * Keep the checkpoint inventory stable for the entire human review, not only
 * the preview HTTP request. The caller MUST release on accept, back/cancel,
 * failed preview, or editor unmount. This is a same-tab scheduling lease, not
 * a database lock: other clients remain protected by the backend CAS.
 */
export type TemporalOccurrenceInventoryReviewLease = Readonly<{
  release(): void;
  run<T>(operation: () => Promise<T>): Promise<T>;
}>;

export async function holdTemporalOccurrenceInventoryReview<T>(
  operation: () => Promise<T>,
): Promise<Readonly<{ value: T; lease: TemporalOccurrenceInventoryReviewLease }>> {
  const previous = settled;
  let unlock: () => void = () => undefined;
  const held = new Promise<void>((resolve) => {
    unlock = resolve;
  });
  // Queue position is reserved synchronously, before any CSRF request.
  settled = previous.then(() => held);
  let released = false;
  const lease: TemporalOccurrenceInventoryReviewLease = {
    release() {
      if (released) return;
      released = true;
      unlock();
    },
    run<T>(next: () => Promise<T>): Promise<T> {
      if (released) {
        return Promise.reject(new Error('Recurring review already closed.'));
      }
      return next();
    },
  };
  try {
    const value = await previous.then(operation);
    return { value, lease };
  } catch (error) {
    lease.release();
    throw error;
  }
}
