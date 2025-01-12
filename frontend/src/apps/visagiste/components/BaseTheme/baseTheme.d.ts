export const allowedThemes = [
    'light',
    'dark',
    'blue',
    'dark-blue',
    'error',
    'grey',
    'success',
] as const
export type Theme = typeof allowedThemes[number]