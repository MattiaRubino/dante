/** Durable, append-only observed test results for interrupted V2 matrices.

The definitive acceptance report remains JUnit. This reporter never marks
pending/not-run tests green; each record is emitted synchronously on test end.
*/
import { appendFileSync } from 'node:fs';

import type {
  Reporter,
  TestCase,
  TestResult,
  TestStep,
} from '@playwright/test/reporter';

function activity(test: TestCase, event: string, step?: TestStep): void {
  const file = process.env.DANTE_E2E_ACTIVITY_JSONL;
  if (!file) return;
  appendFileSync(
    file,
    JSON.stringify({
      title: test.titlePath().join(' › '),
      event,
      step: step?.title,
    }) + '\n',
    'utf8',
  );
}

class DanteProgressReporter implements Reporter {
  onTestBegin(test: TestCase): void {
    activity(test, 'begin');
  }

  onStepBegin(test: TestCase, _result: TestResult, step: TestStep): void {
    if (step.category === 'test.step') activity(test, 'step', step);
  }

  onTestEnd(test: TestCase, result: TestResult): void {
    activity(test, 'end');
    const file = process.env.DANTE_E2E_PROGRESS_JSONL;
    if (!file) return;
    const record = {
      title: test.titlePath().join(' › '),
      status: result.status,
      outcome: test.outcome(),
      duration_ms: result.duration,
      retry: result.retry,
      steps: result.steps
        .filter((step) => step.category === 'test.step')
        .map((step) => ({ title: step.title, duration_ms: step.duration })),
    };
    appendFileSync(file, JSON.stringify(record) + '\n', 'utf8');
  }
}

export default DanteProgressReporter;
