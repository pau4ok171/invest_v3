<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminCheckBoxField",
  props: {
    label: {
      string: '',
      default: 'Label',
    }
  },
})
</script>

<template>
<div>
  <div class="admin-checkbox-label">{{ label }}</div>
  <div class="admin-checkbox-fieldset">
    <div class="admin-checkbox-field">
      <div class="admin-checkbox-field__wrapper">
        <input
          type="checkbox"
          class="admin-checkbox-field__input"
          :checked="($attrs.modelValue as boolean)"
          @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).checked)"
        />
        <div class="admin-checkbox-field__outer"></div>
        <div class="admin-checkbox-field__inner"></div>
      </div>
    </div>
    <div class="admin-checkbox-value">{{ $attrs.modelValue?'Yes': 'No' }}</div>
  </div>
</div>
</template>

<style scoped lang="scss">
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

.admin-checkbox-field {
  position: relative;
  width: $checkbox_width;
  height: $checkbox_height;
  margin-bottom: 8px;
}
.admin-checkbox-field__wrapper {
  width: 100%;
  height: 100%;
  position: absolute;
  left: $checkbox_wrapper_left;
  top: $checkbox_wrapper_top;
}
.admin-checkbox-field__outer, .admin-checkbox-field__input {
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
.admin-checkbox-field__input:checked ~ .admin-checkbox-field__outer {
  animation: shift 0.8s ease-in-out 1 forwards;
  transform: rotate(180deg);
}
.admin-checkbox-field__input:checked ~ .admin-checkbox-field__outer:before {
  background: linear-gradient(to left, #03001e, #7303c0, #ec38bc);
}
.admin-checkbox-field__outer {
  background: linear-gradient(to right, #03001e, #7303c0, #ec38bc);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .25), 0 0 20px 0 rgba(0, 0, 0, .15);
  opacity: 1;
  z-index: 0;
  transform-origin: $checkbox_outer_transform_origin_x $checkbox_outer_transform_origin_y;
  transition: transform 0.3s ease-in-out, margin 0.3s ease-in-out;
  transition-delay: 0s, .3s;
}
.admin-checkbox-field__outer::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  border-radius: 80px;
  background: linear-gradient(to right, #03001e, #7303c0, #ec38bc);
}
.admin-checkbox-field__inner {
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
.admin-checkbox-field__input:checked ~ .admin-checkbox-field__outer ~ .admin-checkbox-field__inner {
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
.admin-checkbox-fieldset {
  display: flex;
  gap: 8px;
}
.admin-checkbox-value {
  font-size: 1.4rem;
}
</style>