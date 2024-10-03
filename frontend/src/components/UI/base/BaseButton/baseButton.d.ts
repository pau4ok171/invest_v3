export const allowedVariants = [
  'elevated',
  'flat',
  'tonal',
  'outlined',
  'text',
  'plain',
] as const
export type Variant = typeof allowedVariants[number]

export const allowedDensities = [
  'compact',
  'comfortable',
  'default',
] as const
export type Density = typeof allowedDensities[number]

export const allowedSizes = [
  'x-small',
  'small',
  'default',
  'large',
  'x-large',
] as const
export type Size = typeof allowedSizes[number]

export const allowedRounded = [
  '0',
  'x-small',
  'default',
  'large',
  'x-large',
] as const
export type Rounded = typeof allowedRounded[number]

export const allowedElevations = [
  '2',
  '4',
  '8',
  '12',
  '16',
  '20',
  '24',
] as const
export type Elevation = typeof allowedElevations[number]