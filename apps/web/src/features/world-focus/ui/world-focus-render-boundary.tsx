import { Component, type ErrorInfo, type ReactNode } from 'react';

type WorldFocusRenderBoundaryProps = Readonly<{
  resetKey: string;
  children: ReactNode;
  fallback: (controls: Readonly<{ reset: () => void }>) => ReactNode;
  onError?: ((error: unknown, info: ErrorInfo) => void) | undefined;
}>;

type WorldFocusRenderBoundaryState = Readonly<{
  hasError: boolean;
}>;

/**
 * Small feature-local React error boundary for future module/surface isolation.
 * It deliberately does not expose raw errors to fallback UI; operational error
 * details belong in the optional reporting callback, not user-visible copy.
 */
export class WorldFocusRenderBoundary extends Component<
  WorldFocusRenderBoundaryProps,
  WorldFocusRenderBoundaryState
> {
  override state: WorldFocusRenderBoundaryState = { hasError: false };

  static getDerivedStateFromError(): WorldFocusRenderBoundaryState {
    return { hasError: true };
  }

  override componentDidCatch(error: unknown, info: ErrorInfo) {
    this.props.onError?.(error, info);
  }

  override componentDidUpdate(previousProps: WorldFocusRenderBoundaryProps) {
    if (
      this.state.hasError &&
      previousProps.resetKey !== this.props.resetKey
    ) {
      this.setState({ hasError: false });
    }
  }

  readonly reset = () => {
    if (this.state.hasError) {
      this.setState({ hasError: false });
    }
  };

  override render() {
    return this.state.hasError
      ? this.props.fallback({ reset: this.reset })
      : this.props.children;
  }
}
