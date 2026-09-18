export const accessTheme = {
  colors: {
    background: '#f7f5f1',
    surface: '#ffffff',
    surfaceMuted: '#efeee9',
    ink: '#222f37',
    textSecondary: '#53616a',
    textMuted: '#69757c',
    border: '#89969d',
    borderHover: '#738188',
    divider: '#e3e6e7',
    accent: '#ea5c12',
    accentText: '#c84a00',
    onInk: '#ffffff',
  },
  radii: {
    input: 12,
    control: 14,
    card: 20,
  },
  spacing: {
    xs: 6,
    sm: 10,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },
  decorative: {
    backgroundMarkOpacity: 0.12,
    backgroundMarkMinSize: 520,
    backgroundMarkScale: 1.45,
    backgroundMarkLeftCrop: 0.46,
    backgroundMarkBottomCrop: 0.38,
  },
} as const;

export type AccessTheme = typeof accessTheme;
