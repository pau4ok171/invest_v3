<script lang="ts">
import type {PropType} from "vue";
import {defineComponent} from 'vue'
import ResetIcon from "@/components/icons/ResetIcon.vue";
import type {ErrorObject} from "@vuelidate/core";
import AdminImageField from "@/components/admin/models/fields/AdminImageField.vue";
import AdminSelectorField from "@/components/admin/models/fields/AdminSelectorField.vue";
import AdminCheckBoxField from "@/components/admin/models/fields/AdminCheckBoxField.vue";
import AdminTextField from "@/components/admin/models/fields/AdminTextField.vue";
import AdminCharField from "@/components/admin/models/fields/AdminCharField.vue";
import AdminYearField from "@/components/admin/models/fields/AdminYearField.vue";
import {FieldStatusEnum} from "@/types/admin.types";
import type {AdminModelValue, FormattedSector} from "@/types/admin.types";

export default defineComponent({
  name: "AdminField",
  components: {
    AdminImageField,
    AdminSelectorField,
    AdminCheckBoxField,
    AdminTextField,
    AdminCharField,
    AdminYearField,
    ResetIcon,
  },
  props: {
    field: {
      type: String,
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
      type: [String, Boolean, Object],
      default: '',
      required: true,
    },
    errors: {
      type: Object as PropType<ErrorObject[]>,
    },
    wasModified: {
      type: Boolean,
      default: false,
    },
    hasSearch: {
      type: Boolean,
      default: false,
    },
    options: {
      type: Array<FormattedSector>,
      default: [],
    },
  },
  computed: {
    getFieldStatus(): FieldStatusEnum {
      if (this.isDisabled) {
        return FieldStatusEnum.DISABLED
      }
      if (this.errors?.length) {
        return FieldStatusEnum.INVALID
      }
      if (this.wasModified && !this.errors?.length) {
        return FieldStatusEnum.VALID
      }
      return FieldStatusEnum.VIRGIN
    }
  },
  methods: {
    updateModelValue(value: AdminModelValue) {
      this.$emit('update:modelValue', value)
    }
  },
})
</script>

<template>
<div class="admin-field__fieldset">

  <button
    class="admin-field__reset-button"
    v-show="wasModified"
    @click="$emit('resetField')"
    v-tippy="{content: 'Click to reset field changes'}"
  >
    <ResetIcon/>
  </button>

  <component
    :is="field"
    :label
    :isRequired
    :isDisabled
    :modelValue
    :options
    :hasSearch
    :fieldStatus="getFieldStatus"
    @update:model-value="updateModelValue"
    @commitValidator="$emit('commitValidator')"
    @touch="$emit('touch')"
  />

  <div v-if="helpText" class="admin-field__help-text">{{ helpText }}</div>

  <div v-if="errors?.length" class="admin-field__errors">
    <div
        v-for="error in errors"
        :key="error.$uid"
        class="admin-field__error"
    >
      {{ error.$message }}
    </div>
  </div>

</div>
</template>
<style>
:root {
  --admin-field-default-gradient-color-start: #ee4297;
  --admin-field-default-gradient-color-finish: #9176c6;
  --admin-field-success-gradient-color-start: #71a13a;
  --admin-field-success-gradient-color-finish: #09461d;
  --admin-field-error-gradient-color-start: #ff0000;
  --admin-field-error-gradient-color-finish: #2a1910;
  --admin-field-default-backgroud-color: #1b222d;
  --admin-field-focus-backgroud-color: #0d4370;
}
</style>
<style scoped lang="scss">
.admin-field__fieldset {
  margin: 16px 0;
  position: relative;
  width: max-content;
  padding: 2px 18px 0 0;
}
.admin-field__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
.admin-field__errors {
  width: max-content;
  margin: 10px 0 0 20px;
  border: 1px solid #c92432;
  border-radius: 8px;
  font-size: 1.2rem;
}
.admin-field__error {
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
.admin-field__reset-button {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 0;
  right: 0;
  border: 1px solid transparent;
  border-radius: 4px;
  background-color: rgba(53, 110, 233, .1);
  transition: background-color .4s;
  cursor: pointer;

  &:hover {
    background-color: rgba(53, 110, 233, .2);
  }

  & svg {
    fill: var(--blue);
    width: 16px;
    height: 16px;
    user-select: none;
  }
}
</style>