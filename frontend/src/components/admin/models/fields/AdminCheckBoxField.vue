<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminCheckBoxField",
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
      type: Boolean,
      default: false,
    },
    fieldStatus: {
      type: String,
      required: true,
    },
  },
  methods: {
    updateModelValue(event: Event) {
      this.$emit('update:modelValue', (event.target as HTMLInputElement).checked)
      this.$emit('touch')
      this.$emit('commitValidator')
    },
  },
})
</script>

<template>
<div>
<div class="admin-checkbox-label">{{ label }}</div>

<div
  class="admin-checkbox-field"
  :class="{'admin-checkbox-field--valid': fieldStatus === 'valid', 'admin-checkbox-field--invalid': fieldStatus === 'invalid'}"
>
  <div :class="['admin-checkbox-button', {'admin-checkbox-button--disabled': isDisabled}]">
    <div class="admin-checkbox-button__wrapper">
      <input
        type="checkbox"
        class="admin-checkbox-button__input"
        :checked="modelValue"
        :disabled="isDisabled"
        @input="updateModelValue"
      />
      <div class="admin-checkbox-button__outer"></div>
      <div class="admin-checkbox-button__inner"></div>
    </div>
  </div>
  <div class="admin-checkbox-value">{{ modelValue?'Yes': 'No' }}</div>
</div>
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

$checkbox_width: 40px;
$checkbox_height: 20px;
$checkbox_wrapper_left: calc(50% - $checkbox_width / 2);
$checkbox_wrapper_top: calc(50% - $checkbox_height / 2);
$checkbox_inner_width: 16px;
$checkbox_inner_height: 16px;
$checkbox_inner_left: calc(($checkbox_height - $checkbox_inner_height) / 2);
$checkbox_inner_top: calc(($checkbox_height - $checkbox_inner_height) / 2);
$checkbox_outer_transform_origin_x: calc($checkbox_height / 2);
$checkbox_outer_transform_origin_y: calc($checkbox_height / 2);
$checkbox_animation_width: calc($checkbox_inner_height + $checkbox_inner_left + $checkbox_inner_top);
$checkbox_animation_translate_x: calc($checkbox_width - $checkbox_inner_width - $checkbox_inner_left - $checkbox_inner_left);

.admin-checkbox-button {
  position: relative;
  width: $checkbox_width;
  height: $checkbox_height;
  margin-bottom: 8px;
}
.admin-checkbox-button__wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  left: $checkbox_wrapper_left;
  top: $checkbox_wrapper_top;
}
.admin-checkbox-button__outer, .admin-checkbox-button__input {
  width: 100%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 9;
  border-radius: 80px;
  opacity: 0;
  cursor: pointer;
}
.admin-checkbox-button__input:checked ~ .admin-checkbox-button__outer {
  animation: shift 0.8s ease-in-out 1 forwards;
  transform: rotate(180deg);
}
.admin-checkbox-button__input:checked ~ .admin-checkbox-button__outer:before {
  background: linear-gradient(to left, #03001e, #7303c0, #ec38bc);
}
.admin-checkbox-button__outer {
  background: linear-gradient(to right, #03001e, #7303c0, #ec38bc);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .25), 0 0 20px 0 rgba(0, 0, 0, .15);
  opacity: 1;
  z-index: 0;
  transform-origin: $checkbox_outer_transform_origin_x $checkbox_outer_transform_origin_y;
  transition: transform 0.3s ease-in-out, margin 0.3s ease-in-out;
  transition-delay: 0s, .3s;
}
.admin-checkbox-button__outer::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  border-radius: 80px;
  background: linear-gradient(to right, #03001e, #7303c0, #ec38bc);
}
.admin-checkbox-button__inner {
  position: absolute;
  width: $checkbox_inner_width;
  height: $checkbox_inner_height;
  box-shadow: inset -5px -10px 15px 0 rgba(0, 0, 0, .5);
  background: #fff -35px -30px;
  background-size: 120%;
  left: $checkbox_inner_left;
  top: $checkbox_inner_top;
  border-radius: 500%;
  transition: margin .3s ease-in-out, box-shadow .6s ease-in-out, all .4s ease-in-out;
  transition-delay: .3s, 0s;
}
.admin-checkbox-button__input:checked ~ .admin-checkbox-button__outer ~ .admin-checkbox-button__inner {
  transition-delay: .4s;
  transform: translateX($checkbox_animation_translate_x);
  box-shadow: inset 5px -10px 15px 0 rgba(0, 0, 0, .5);
}
@keyframes shift {
  0% {
    width: $checkbox_width;
    transform: rotate(0deg);
  }
  25% {
    width: $checkbox_animation_width;
    transform: rotate(0deg);
  }
  50% {
    width: $checkbox_animation_width;
    transform: rotate(180deg);
  }
  100% {
    width: $checkbox_width;
    transform: translateX($checkbox_animation_translate_x) rotate(180deg);
  }
}
.admin-checkbox-label {
  font-size: 1.4rem;
  margin-bottom: 8px;
}
.admin-checkbox-field {
  display: flex;
  gap: 8px;
}
.admin-checkbox-value {
  font-size: 1.4rem;
}
.admin-checkbox-button--disabled {
  & .admin-checkbox-button__outer:before,
  .admin-checkbox-button__input ~ .admin-checkbox-button__outer:before,
  .admin-checkbox-button__input ~ .admin-checkbox-button__outer {
    background: #242f3c;
    border-color: #92969c;
  }
  & .admin-checkbox-button__input {
    cursor: auto;
  }
}
.admin-checkbox-field--valid {
  & .admin-checkbox-button__input:checked ~ .admin-checkbox-button__outer:before {
    background: linear-gradient(to left, #03001e, $gradient-color-success-finish, $gradient-color-success-start);
  }
  & .admin-checkbox-button__outer {
    background: linear-gradient(to right, #03001e, $gradient-color-success-finish, $gradient-color-success-start);
  }
  & .admin-checkbox-button__outer::before {
    background: linear-gradient(to right, #03001e, $gradient-color-success-finish, $gradient-color-success-start);
  }
}
.admin-checkbox-field--invalid {
  & .admin-checkbox-button__input:checked ~ .admin-checkbox-button__outer:before {
    background: linear-gradient(to left, #03001e, $gradient-color-error-finish, $gradient-color-error-start);
  }
  & .admin-checkbox-button__outer {
    background: linear-gradient(to right, #03001e, $gradient-color-error-finish, $gradient-color-error-start);
  }
  & .admin-checkbox-button__outer::before {
    background: linear-gradient(to right, #03001e, $gradient-color-error-finish, $gradient-color-error-start);
  }
}
</style>