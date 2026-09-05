export type HomeWorldFocusOrigin = Readonly<{
  left: number;
  top: number;
  width: number;
  height: number;
}>;

export type HomeWorldOpenIntent = Readonly<{
  label: string;
  origin: HomeWorldFocusOrigin;
}>;
