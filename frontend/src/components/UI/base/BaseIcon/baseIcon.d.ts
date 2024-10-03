import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import BackArrowIcon from "@/components/icons/BackArrowIcon.vue";
import BoldIcon from "@/components/icons/BoldIcon.vue";
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import CheckIcon from "@/components/icons/CheckIcon.vue";
import CheckmarkCircleIcon from "@/components/icons/CheckmarkCircleIcon.vue";
import CopyIcon from "@/components/icons/CopyIcon.vue";
import CrossIcon from "@/components/icons/CrossIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import DotsIcon from "@/components/icons/DotsIcon.vue";
import EditIcon from "@/components/icons/EditIcon.vue";
import EmailIcon from "@/components/icons/EmailIcon.vue";
import ExpandIcon from "@/components/icons/ExpandIcon.vue";
import ExtraLinkIcon from "@/components/icons/ExtraLinkIcon.vue";
import FilterIcon from "@/components/icons/FilterIcon.vue";
import GoogleIcon from "@/components/icons/GoogleIcon.vue";
import HeaderIcon from "@/components/icons/HeaderIcon.vue";
import InfoIcon from "@/components/icons/InfoIcon.vue";
import InputCrossIcon from "@/components/icons/InputCrossIcon.vue";
import ListIcon from "@/components/icons/ListIcon.vue";
import MegaphoneIcon from "@/components/icons/MegaphoneIcon.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import NotificationIcon from "@/components/icons/NotificationIcon.vue";
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import PlusIcon from "@/components/icons/PlusIcon.vue";
import ReduceIcon from "@/components/icons/ReduceIcon.vue";
import ResetIcon from "@/components/icons/ResetIcon.vue";
import SearchIcon from "@/components/icons/SearchIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import SortDownIcon from "@/components/icons/SortDownIcon.vue";
import SortUpIcon from "@/components/icons/SortUpIcon.vue";
import TableModeIcon from "@/components/icons/TableModeIcon.vue";
import TileModeIcon from "@/components/icons/TileModeIcon.vue";
import TrashIcon from "@/components/icons/TrashIcon.vue";
import UploadIcon from "@/components/icons/UploadIcon.vue";
import UserIcon from "@/components/icons/UserIcon.vue";

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