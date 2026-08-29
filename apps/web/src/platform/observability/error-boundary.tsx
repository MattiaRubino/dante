import {
  Component,
  useEffect,
  useRef,
  type ErrorInfo,
  type PropsWithChildren,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import { observeRenderFailure } from './runtime';
import './error-boundary.css';

type FailureProps = Readonly<{
  resetError: VoidFunction;
}>;

function ApplicationFailure({ resetError }: FailureProps) {
  const { t } = useTranslation('common');
  const headingReference = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    headingReference.current?.focus();
  }, []);

  return (
    <main className="observability-failure" role="main">
      <section
        className="observability-failure__panel"
        aria-labelledby="observability-failure-title"
      >
        <p className="observability-failure__eyebrow">
          {t(($) => $.common.observability.failure.eyebrow)}
        </p>
        <h1
          id="observability-failure-title"
          ref={headingReference}
          tabIndex={-1}
        >
          {t(($) => $.common.observability.failure.title)}
        </h1>
        <p>{t(($) => $.common.observability.failure.description)}</p>
        <div className="observability-failure__actions">
          <button type="button" onClick={resetError}>
            {t(($) => $.common.observability.failure.retry)}
          </button>
          <button type="button" onClick={() => globalThis.location.reload()}>
            {t(($) => $.common.observability.failure.reload)}
          </button>
        </div>
      </section>
    </main>
  );
}

type BoundaryState = Readonly<{
  error: Error | null;
}>;

const INITIAL_STATE: BoundaryState = { error: null };

class DanteErrorBoundary extends Component<PropsWithChildren, BoundaryState> {
  override state: BoundaryState = INITIAL_STATE;

  static getDerivedStateFromError(error: Error): BoundaryState {
    return { error };
  }

  override componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    observeRenderFailure(error, errorInfo.componentStack ?? undefined);
  }

  private readonly resetError = (): void => {
    this.setState(INITIAL_STATE);
  };

  override render(): ReactNode {
    if (this.state.error !== null) {
      return <ApplicationFailure resetError={this.resetError} />;
    }

    return this.props.children;
  }
}

export function ObservabilityErrorBoundary({ children }: PropsWithChildren) {
  return <DanteErrorBoundary>{children}</DanteErrorBoundary>;
}
