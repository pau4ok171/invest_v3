<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import AdminSelectorDropDownMenu from "@/components/admin/models/fields/AdminSelectorDropDownMenu.vue";
import type {FormattedSector, FormattedSelector} from "@/types/admin.types";

export default defineComponent({
  name: "AdminSelectorField",
  components: {
    AdminSelectorDropDownMenu,
    CompanyListFilterDropDownMenu,
    DropDownMenuBox,
    ArrowDownIcon,
    CheckedIcon
  },
  props: {
    hasSearch: {
      type: Boolean,
      default: false,
    },
    options: {
      type: Array<FormattedSector>,
      required: true,
    },
    label: {
      type: String,
      default: 'Label',
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Object as PropType<FormattedSelector>,
      default: {name: '', slug: '', key: ''},
      required: true,
    },
    fieldStatus: {
      type: String,
      required: true,
    },
  },
  methods: {
    updateSelectorOption(option: FormattedSelector) {
      this.$emit('update:modelValue', option)
      this.$emit('touch')
      this.$emit('commitValidator')
    }
  },
  computed: {
    areOptionsEmpty () {
      return !this.options.length
    }
  },
})
</script>

<template>
<DropDownMenuBox>
  <template v-slot:button>
    <button
      class="admin-selector-field"
      :class="{'admin-selector-field--valid': fieldStatus === 'valid', 'admin-selector-field--invalid': fieldStatus === 'invalid'}"
      :disabled="isDisabled || areOptionsEmpty"
    >
      <span>{{ modelValue.name }}</span>
      <ArrowDownIcon/>
    </button>
   <label :class="['admin-selector-field__label', {'admin-selector-field__label--active': !modelValue.slug}]">
     {{ label }}{{ isRequired?'*':'' }}
   </label>
  </template>
  <template v-slot:menu>
    <AdminSelectorDropDownMenu
      :model-value="modelValue"
      @update:model-value="updateSelectorOption"
      :options
      :hasSearch
    />
  </template>
</DropDownMenuBox>
</template>

<style scoped lang="scss">
$bg-default-color: var(--admin-field-default-backgroud-color);
$bg-focus-color: var(--admin-field-focus-backgroud-color);
$gradient-color-default-start: var(--admin-field-default-gradient-color-start);
$gradient-color-default-finish: var(--admin-field-default-gradient-color-finish);
$gradient-color-success-start: var(--admin-field-success-gradient-color-start);
$gradient-color-success-finish: var(--admin-field-success-gradient-color-finish);
$gradient-color-error-start: var(--admin-field-error-gradient-color-start);
$gradient-color-error-finish: var(--admin-field-error-gradient-color-finish);

.admin-selector-field {
  display: flex;
  position: relative;
  justify-content: space-between;
  align-items: center;
  width: 280px;
  padding: 6px 20px;

  outline: none;
  border: 3px solid transparent;
  border-radius: 20px;
  background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-default-start, $gradient-color-default-finish);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  font-size: 1.4rem;
  color: #fff;
  &--valid {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-success-start, $gradient-color-success-finish);
  }
  &--invalid {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-error-start, $gradient-color-error-finish);
  }

  & > * {
    pointer-events: none;
  }
  &:disabled {
    background: #1b222d;
    border-color: #92969c;
  }
  &:focus {
    border-color: #2b96f1;
    box-shadow: inset 1px 2px 4px 0 rgb(179 30 30 / 10%), 3px 5px 12px 2px rgb(43 150 241 / 40%);
    background-image: linear-gradient($bg-focus-color, $bg-focus-color), linear-gradient(315deg, $gradient-color-default-start, $gradient-color-default-finish);


    & + label {
      color: #2b96f1;
      transform: translateY(-20px);
    }
  }
}
.admin-selector-field__label {
  color: #fff;
  border-radius: 20px;
  font-size: 1.4rem;
  text-transform: uppercase;
  position: absolute;
  z-index: 2;
  left: 20px;
  top: 14px;
  padding: 0 5px;
  pointer-events: none;
  background: #1b222d;
  transition: transform .1s ease;
  transform: translateY(-20px);
}
.admin-selector-field__label--active {
    transform: translateY(0);
  }
</style>