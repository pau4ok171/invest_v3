<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AdminYearField",
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
  data() {
    return {
      isFocused: false,
      timeoutID: 0,
    }
  },
  methods: {
    processInput(event: Event) {
      const target: HTMLHtmlElement | any = event.target
      const next: HTMLInputElement | any = target.nextSibling
      const previous: HTMLHtmlElement | any = target.previousSibling

      if (target.value.length === 1 && !/\d/.exec(target.value)) {
        target.value = ''
        return false
      }
      if (target.value.length > 1 && !/\d/.exec(target.value[1])) {
        target.value = target.value[0]
        return false
      }
      if (target.value.length > 1 && next) {
        const value = target.value
        target.value = value[0]
        next.value = value.slice(1)
        next.focus()
      }
      if (!target.value && previous) {
        previous.focus()
      }
      const value: string = Array.from(target.parentNode.children).reduce((acc: string, el: any) => {
        acc+= String(el.value)
        return acc
      }, '')

      this.$emit('update:model-value', value)
      this.$emit('touch')
    },
    processBlur() {
      if (this.timeoutID !== 0) {
        clearTimeout(this.timeoutID)
      }
      this.timeoutID = setTimeout(this.checkIfBlured, 50)
    },
    checkIfBlured() {
      if (document.activeElement?.parentNode !== this.$refs.adminYearField) {
        this.isFocused = false
        this.$emit('commitValidator')
      }
  },
  },
})
</script>

<template>
<div
    class="admin-year-field"
    :class="{'admin-year-field--valid': fieldStatus === 'valid', 'admin-year-field--invalid': fieldStatus === 'invalid'}"
>
  <div
    :class="['admin-year-field__inputs', {'admin-year-field__inputs--focus': isFocused, 'admin-year-field__inputs--disabled': isDisabled}]"
    @focus.capture="isFocused=true"
    @blur.capture="processBlur"
    @input.capture="processInput"
    ref="adminYearField"
  >
    <input class="admin-year-field__input" tabindex="0" :required="isRequired" :disabled="isDisabled" :value="String(modelValue)[0]" pattern="[0-9]" maxlength="4" placeholder="•">
    <input class="admin-year-field__input" tabindex="-1" :required="isRequired" :disabled="isDisabled" :value="String(modelValue)[1]" pattern="[0-9]" maxlength="4" placeholder="•">
    <input class="admin-year-field__input" tabindex="-1" :required="isRequired" :disabled="isDisabled" :value="String(modelValue)[2]" pattern="[0-9]" maxlength="4" placeholder="•">
    <input class="admin-year-field__input" tabindex="-1" :required="isRequired" :disabled="isDisabled" :value="String(modelValue)[3]" pattern="[0-9]" maxlength="4" placeholder="•">
  </div>
  <label class="admin-year-field__label">{{ label }}{{ isRequired?'*':'' }}</label>
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


.admin-year-field {
  position: relative;
  line-height: 1.4rem;
  &--valid .admin-year-field__inputs {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-success-start, $gradient-color-success-finish);
  }
  &--invalid .admin-year-field__inputs {
    background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-error-start, $gradient-color-error-finish);
  }
}
.admin-year-field__inputs {
  position: relative;
  display: flex;
  justify-content: center;
  width: 200px;
  font-size: 1.4rem;
  color: #fff;
  outline: none;
  padding: 5px 10px;
  border: 3px solid transparent;
  border-radius: 20px;
  background-image: linear-gradient($bg-default-color, $bg-default-color), linear-gradient(315deg, $gradient-color-default-start, $gradient-color-default-finish);
  background-origin: border-box;
  background-clip: padding-box, border-box;

  &--disabled {
    background: #1b222d;
    border-color: #92969c;
  }
  &--focus {
    border-color: #2b96f1;
    box-shadow: inset 1px 2px 4px 0 rgb(179 30 30 / 10%), 3px 5px 12px 2px rgb(43 150 241 / 40%);
    background-image: linear-gradient($bg-focus-color, $bg-focus-color), linear-gradient(315deg, $gradient-color-default-start, $gradient-color-default-finish);
  }
}
.admin-year-field__input {
  width: 32px;
  height: 32px;
  line-height: 100%;
  background-color: transparent;
  border: 0;
  outline: 0;
  color: white;
  font-size: 32px;
  word-spacing: 0;
  overflow: hidden;
  text-align: center;
}
.admin-year-field__label {
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