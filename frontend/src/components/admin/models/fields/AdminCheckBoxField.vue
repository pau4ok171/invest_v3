<script lang="ts">
import {defineComponent} from 'vue'
import type {PropType} from "vue";
import type {ErrorObject} from "@vuelidate/core";
import ResetIcon from "@/components/icons/ResetIcon.vue";

export default defineComponent({
  name: "AdminCheckBoxField",
  components: {ResetIcon},
  props: {
    label: {
      type: String,
      default: 'Label',
    },
    helpText: {
      type: String
    },
    isDisabled: {
      type: Boolean,
      default: false,
    },
    modelValue: {
      type: Boolean,
      default: false,
    },
    errors: {
      type: Object as PropType<ErrorObject[]>,
    },
    wasModified: {
      type: Boolean,
      default: false,
    },
  },
})
</script>

<template>
<div class="admin-checkbox-fieldset">

  <button
    class="admin-checkbox__reset-button"
    v-show="wasModified"
    @click="$emit('resetField')"
    v-tippy="{content: 'Click to reset field changes'}"
  >
    <ResetIcon/>
  </button>

  <div class="admin-checkbox-label">{{ label }}</div>

  <div class="admin-checkbox-field">
    <div :class="['admin-checkbox-button', {'admin-checkbox-button--disabled': isDisabled}]">
      <div class="admin-checkbox-button__wrapper">
        <input
          type="checkbox"
          class="admin-checkbox-button__input"
          :checked="modelValue"
          :disabled="isDisabled"
          @input="(event: Event) => $emit('update:modelValue', (event.target as HTMLInputElement).checked)"
        />
        <div class="admin-checkbox-button__outer"></div>
        <div class="admin-checkbox-button__inner"></div>
      </div>
    </div>
    <div class="admin-checkbox-value">{{ modelValue?'Yes': 'No' }}</div>
  </div>

  <div v-if="helpText" class="admin-checkbox__help-text">{{ helpText }}</div>

  <div v-if="errors?.length" class="admin-checkbox__errors">
    <div
        v-for="error in errors"
        :key="error.$uid"
        class="admin-checkbox__error"
    >
      {{ error.$message }}
    </div>
  </div>

</div>
</template>

<style scoped lang="scss">
.admin-checkbox-fieldset {
  position: relative;
  padding: 2px 18px 0 0;
  width: max-content;
  margin: 16px 0;
}

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
}
.admin-checkbox__help-text {
  color: #92969c;
  font-size: 1.2rem;
  padding-left: 20px;
  margin-top: 4px;
}
.admin-checkbox__errors {
  width: max-content;
  margin: 10px 0 0 20px;
  border: 1px solid #c92432;
  border-radius: 8px;
  font-size: 1.2rem;
}
.admin-checkbox__error {
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
.admin-checkbox__reset-button {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 0;
  right: -4px;
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