<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import CheckedIcon from "@/components/icons/CheckedIcon.vue";
import BaseInput from "@/components/UI/base/BaseInput.vue";
import ArrowDownIcon from "@/components/icons/ArrowDownIcon.vue";
import DropDownMenuBox from "@/components/UI/DropDownMenuBox.vue";
import CompanyListFilterDropDownMenu from "@/components/company_list/CompanyListFilterDropDownMenu.vue";
import AdminSelectorDropDownMenu from "@/components/admin/models/fields/AdminSelectorDropDownMenu.vue";
import type {FormattedSector, FormattedSelector} from "@/types/admin";
import type {ErrorObject} from "@vuelidate/core";

export default defineComponent({
  name: "AdminSelectorField",
  components: {
    AdminSelectorDropDownMenu,
    CompanyListFilterDropDownMenu,
    DropDownMenuBox,
    ArrowDownIcon,
    BaseInput,
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
    helpText: {
      type: String
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
    errors: {
      type: Object as PropType<ErrorObject[]>,
    },
  },
  methods: {
    updateSelectorOption(option: FormattedSelector) {
      this.$emit('update:modelValue', option)
    }
  },
})
</script>

<template>
<div class="admin-selector-fieldset">
  <DropDownMenuBox>
    <template v-slot:button>
        <button
            class="admin-selector-field"
            :disabled="isDisabled"
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
  <div v-if="helpText" class="admin-selector-field__help-text">{{ helpText }}</div>
  <div v-if="errors?.length" class="admin-selector-field__errors">
    <div
        v-for="error in errors"
        :key="error.$uid"
        class="admin-selector-field__error"
    >
      {{ error.$message }}
    </div>
  </div>
</div>
</template>

<style scoped lang="scss">
.admin-selector-fieldset {
  margin: 16px 0;
}
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
  background-image: linear-gradient(#1b222d, #1b222d), linear-gradient(315deg, #ee4297, #9176c6);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  font-size: 1.4rem;
  color: #fff;

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
.admin-selector-field__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
.admin-selector-field__errors {
  width: max-content;
  margin: 10px 0 0 20px;
  border: 1px solid #c92432;
  border-radius: 8px;
  font-size: 1.2rem;
}
.admin-selector-field__error {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  color: #c92432;

  &::before {
    content: '';
    display: inline-block;
    margin-right: 1px;
    width: 5px;
    height: 5px;
    background-color: #c92432;
    border-radius: 2.5px;
  }
}
</style>