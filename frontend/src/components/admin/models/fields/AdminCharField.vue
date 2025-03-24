<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminCharField",
  props: {
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
      type: String,
      default: '',
      required: true,
    },
    fieldStatus: {
      type: String,
      required: true,
    },
  },
  methods: {
    updateModelValue(event: Event) {
      this.$emit('update:modelValue', (event.target as HTMLInputElement).value)
      this.$emit('touch')
    }
  },
})
</script>

<template>
<div
    class="admin-char-field"
    :class="{'admin-char-field--valid': fieldStatus === 'valid', 'admin-char-field--invalid': fieldStatus === 'invalid'}"
>
  <input
    :required="isRequired"
    :disabled="isDisabled"
    :value="modelValue"
    @input="updateModelValue"
    @blur="$emit('commitValidator')"
    class="admin-char-field__input"
    placeholder=" "
  />
  <label class="admin-char-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
</div>
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

.admin-char-field {
  position: relative;
  line-height: .875rem;
  &--valid .admin-char-field__input {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-success-start, $gradient-color-success-finish);
  }
  &--invalid .admin-char-field__input {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-error-start, $gradient-color-error-finish);
  }
}
.admin-char-field__input {
  position: relative;
  width: 400px;
  font-size: .875rem;
  color: #fff;
  outline: none;
  padding: 10px 20px;
  border: 3px solid transparent;
  border-radius: 20px;
  background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-default-start, $gradient-color-default-finish);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  &:disabled {
    background: #1b222d;
    border-color: #92969c;
  }
  &:placeholder-shown + label {
    transform: translateY(0);
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
.admin-char-field__label {
  color: #fff;
  border-radius: 20px;
  font-size: .875rem;
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
</style>