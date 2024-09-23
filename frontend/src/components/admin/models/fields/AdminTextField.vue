<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminTextField",
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
    },
  },
})
</script>

<template>
<div
  class="admin-text-field"
  :class="{'admin-text-field--valid': fieldStatus === 'valid', 'admin-text-field--invalid': fieldStatus === 'invalid'}"
>
  <div class="admin-text-field__tab"></div>
  <textarea
      :required="isRequired"
      :disabled="isDisabled"
      @input="updateModelValue"
      @blur="$emit('commitValidator')"
      :value="modelValue"
      class="admin-text-field__textarea"
      cols="50"
      rows="15"
      placeholder=" "
  />
  <label class="admin-text-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
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


.admin-text-field {
  position: relative;
  display: inline-block;
  line-height: 1.4rem;
  &::after {
    content: "";
    border-top: 2px solid #555;
    width: 16px;
    transform: rotate(-45deg);
    background: transparent;
    position: absolute;
    right: 4px;
    bottom: 16px;
    pointer-events: none;
    border-radius: 25%;
  }
  &--valid .admin-text-field__textarea {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-success-start, $gradient-color-success-finish);
  }
  &--invalid .admin-text-field__textarea {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-error-start, $gradient-color-error-finish);
  }
}
.admin-text-field__textarea {
  position: relative;
  min-height: 200px;
  max-height: 800px;
  min-width: 600px;
  max-width: 800px;
  font-size: 1.4rem;
  scroll-padding: 50px 0 50px 0;
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
.admin-text-field__textarea::-webkit-scrollbar {
  width: 10px;
}
.admin-text-field__textarea::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, .2);
  background-color: #f9f9fd;
  border-radius: 10px;
  margin: 15px 0 25px;
}
.admin-text-field__textarea::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, #00c6fb, #005bea);
}
.admin-text-field__textarea::-webkit-resizer {
  display: none;
}
/* White square */
.admin-text-field__textarea::-webkit-scrollbar-corner {
  display: none;
}
.admin-text-field__tab {
  border-top: 2px solid #555;
  width:10px;
  transform: rotate(-45deg);
  position: absolute;
  bottom: 12px;
  right: 4px;
  z-index: 1;
  pointer-events: none;
  border-radius:25%;
}
.admin-text-field__label {
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
</style>