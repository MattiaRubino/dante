/** Durable, append-only observed test results for interrupted V2 matrices.

The definitive acceptance report remains JUnit. This reporter never marks
pending/not-run tests green; each record is emitted synchronously on test end.
*/
import { appendFileSync } from 'node:fs';

import type { Reporter, TestCase, TestResult } from '@playwright/test/reporter';

class DanteProgressReporter implements Reporter {
  onTestEnd(test: TestCase, result: TestResult): void {
    const file = process.env.DANTE_E2E_PROGRESS_JSONL;
    if (!file) return;
    const record = {
      title: test.titlePath().join(' › '),
      status: result.status,
      outcome: test.outcome(),
      duration_ms: result.duration,
      retry: result.retry,
    };
    appendFileSync(file, JSON.stringify(record) + '\n', 'utf8');
  }
}

export default DanteProgressReporter;
