type AccessProvider = 'google' | 'apple';

type ProviderButtonProps = Readonly<{
  provider: AccessProvider;
  label: string;
}>;

function GoogleMark() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 18 18"
      focusable="false"
      aria-hidden="true"
    >
      <path
        fill="#4285F4"
        d="M17.64 9.205c0-.638-.057-1.252-.164-1.841H9v3.481h4.844a4.14 4.14 0 0 1-1.796 2.715v2.258h2.909c1.702-1.567 2.683-3.875 2.683-6.613Z"
      />
      <path
        fill="#34A853"
        d="M9 18c2.43 0 4.468-.806 5.957-2.182l-2.91-2.258c-.805.54-1.835.859-3.047.859-2.344 0-4.328-1.585-5.037-3.714H.956v2.332A9 9 0 0 0 9 18Z"
      />
      <path
        fill="#FBBC05"
        d="M3.963 10.705A5.41 5.41 0 0 1 3.68 9c0-.592.102-1.167.283-1.705V4.963H.956A9 9 0 0 0 0 9c0 1.452.347 2.827.956 4.037l3.007-2.332Z"
      />
      <path
        fill="#EA4335"
        d="M9 3.58c1.322 0 2.508.454 3.443 1.345l2.581-2.581C13.463.892 11.425 0 9 0A9 9 0 0 0 .956 4.963l3.007 2.332C4.672 5.166 6.656 3.58 9 3.58Z"
      />
    </svg>
  );
}

function AppleMark() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      focusable="false"
      aria-hidden="true"
    >
      <path
        fill="currentColor"
        d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.27-.07 2.15.7 2.9.76 1.12-.23 2.19-.89 3.39-.8 1.44.12 2.53.69 3.25 1.73-2.97 1.78-2.27 5.69.46 6.79-.55 1.44-1.26 2.87-2 3.95l.01.54ZM12.03 7.25c-.15-2.14 1.59-3.9 3.58-4.07.27 2.47-2.24 4.32-3.58 4.07Z"
      />
    </svg>
  );
}

export function ProviderButton({ provider, label }: ProviderButtonProps) {
  const iconClassName =
    provider === 'apple'
      ? 'access-provider-mark access-provider-mark-apple'
      : 'access-provider-mark';

  return (
    <button
      className="access-provider-button"
      type="button"
      data-provider={provider}
    >
      <span className={iconClassName} aria-hidden="true">
        {provider === 'google' ? <GoogleMark /> : <AppleMark />}
      </span>
      <span>{label}</span>
    </button>
  );
}
