export const allowedHeaderType = [
  'default',
  'withoutCloseButton',
  'withoutHeader',
] as const
export type HeaderType = typeof allowedHeaderType[number]

export const allowedFooterType = [
  'withOk',
  'withClose',
  'withYesNo',
  'withYesNoCancel',
  'withoutFooter',
] as const
export type FooterType = typeof allowedFooterType[number]