export const IconAliases = [
  'ArrowDownIcon',
  'BackArrowIcon',
  'BoldIcon',
  'CheckedIcon',
  'CheckIcon',
  'CheckmarkCircleIcon',
  'CopyIcon',
  'CrossIcon',
  'DeleteIcon',
  'DotsIcon',
  'EditIcon',
  'EmailIcon',
  'ExpandIcon',
  'ExtraLinkIcon',
  'FilterIcon',
  'GoogleIcon',
  'HeaderIcon',
  'InfoIcon',
  'InputCrossIcon',
  'ListIcon',
  'MegaphoneIcon',
  'ModalMenuCloseIcon',
  'NotificationIcon',
  'OutlineStarIcon',
  'PenIcon',
  'PlusIcon',
  'ReduceIcon',
  'ResetIcon',
  'SearchIcon',
  'SolidStarIcon',
  'SortDownIcon',
  'SortUpIcon',
  'TableModeIcon',
  'TileModeIcon',
  'TrashIcon',
  'UploadIcon',
  'UserIcon',
] as const
export type IconValue = typeof IconAliases[number]

export const allowedIconSizes = [
    'x-large',
    'large',
    'default',
    'small',
    'x-small',
] as const
export type IconSize = typeof allowedIconSizes[number]

export interface IBaseIcon {
  value: IconValue,
  size: IconSize,
}