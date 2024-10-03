<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from 'vue'
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import BackArrowIcon from "@/components/icons/BackArrowIcon.vue";
import BoldIcon from "@/components/icons/BoldIcon.vue";
import type {IconValue} from "@/components/UI/base/BaseIcon/baseIcon";
import CheckIcon from "@/components/icons/CheckIcon.vue";
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import CheckmarkCircleIcon from "@/components/icons/CheckmarkCircleIcon.vue";
import FilterIcon from "@/components/icons/FilterIcon.vue";
import CopyIcon from "@/components/icons/CopyIcon.vue";
import CrossIcon from "@/components/icons/CrossIcon.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import DotsIcon from "@/components/icons/DotsIcon.vue";
import EditIcon from "@/components/icons/EditIcon.vue";
import EmailIcon from "@/components/icons/EmailIcon.vue";
import ExpandIcon from "@/components/icons/ExpandIcon.vue";
import HeaderIcon from "@/components/icons/HeaderIcon.vue";
import GoogleIcon from "@/components/icons/GoogleIcon.vue";
import ExtraLinkIcon from "@/components/icons/ExtraLinkIcon.vue";
import InfoIcon from "@/components/icons/InfoIcon.vue";
import OutlineStarIcon from "@/components/icons/OutlineStarIcon.vue";
import NotificationIcon from "@/components/icons/NotificationIcon.vue";
import ModalMenuCloseIcon from "@/components/icons/ModalMenuCloseIcon.vue";
import MegaphoneIcon from "@/components/icons/MegaphoneIcon.vue";
import InputCrossIcon from "@/components/icons/InputCrossIcon.vue";
import ListIcon from "@/components/icons/ListIcon.vue";
import SolidStarIcon from "@/components/icons/SolidStarIcon.vue";
import PenIcon from "@/components/icons/PenIcon.vue";
import PlusIcon from "@/components/icons/PlusIcon.vue";
import ReduceIcon from "@/components/icons/ReduceIcon.vue";
import ResetIcon from "@/components/icons/ResetIcon.vue";
import SearchIcon from "@/components/icons/SearchIcon.vue";
import SortDownIcon from "@/components/icons/SortDownIcon.vue";
import SortUpIcon from "@/components/icons/SortUpIcon.vue";
import TableModeIcon from "@/components/icons/TableModeIcon.vue";
import TileModeIcon from "@/components/icons/TileModeIcon.vue";
import TrashIcon from "@/components/icons/TrashIcon.vue";
import UploadIcon from "@/components/icons/UploadIcon.vue";
import UserIcon from "@/components/icons/UserIcon.vue";

export default defineComponent({
  name: "BaseIcon",
  components: {
    ArrowDownIcon,
    BackArrowIcon,
    BoldIcon,
    CheckedIcon,
    CheckIcon,
    CheckmarkCircleIcon,
    CopyIcon,
    CrossIcon,
    DeleteIcon,
    DotsIcon,
    EditIcon,
    EmailIcon,
    ExpandIcon,
    ExtraLinkIcon,
    FilterIcon,
    GoogleIcon,
    HeaderIcon,
    InfoIcon,
    InputCrossIcon,
    ListIcon,
    MegaphoneIcon,
    ModalMenuCloseIcon,
    NotificationIcon,
    OutlineStarIcon,
    PenIcon,
    PlusIcon,
    ReduceIcon,
    ResetIcon,
    SearchIcon,
    SolidStarIcon,
    SortDownIcon,
    SortUpIcon,
    TableModeIcon,
    TileModeIcon,
    TrashIcon,
    UploadIcon,
    UserIcon,
  },
  props: {
    icon: {
      type: String as PropType<IconValue>,
      required: true,
    }
  }
})
</script>

<template>
<i class="base-icon"><component class="base-icon__svg" :is="icon"/></i>
</template>

<style scoped>
.base-icon {
  font-size: calc(var(--base-icon-size-multiplier) * 1.5em);
  align-items: center;
  display: inline-flex;
  font-feature-settings: "liga";
  height: 1em;
  justify-content: center;
  letter-spacing: normal;
  line-height: 1;
  position: relative;
  text-indent: 0;
  text-align: center;
  -webkit-user-select: none;
  user-select: none;
  vertical-align: middle;
  width: 1em;
  min-width: 1em;
}
.base-icon__svg {
  fill: currentColor;
  width: 100%;
  height: 100%;
}
</style>