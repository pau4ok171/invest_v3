<script lang="ts">
import {defineComponent, nextTick} from 'vue'
import type {PropType} from 'vue'
import BaseField from "@/components/UI/base/components/BaseField/BaseField.vue";
import {useProxiedModel} from "@/components/UI/base/composable/proxiedModel";

export default defineComponent({
  name: "BaseOtpInput",
  components: {
    BaseField,
  },
  data() {
    return {
      isFocused: false,
      focusIndex: -1,
      model: useProxiedModel(
          this.$props,
          'modelValue',
          '',
          val => val == null ? [] : String(val).split(''),
          val => val.join('')
      ),
      inputRef: [] as HTMLInputElement[],
    }
  },
  props: {
    autofocus: Boolean,
    divider: String,
    focusAll: Boolean,
    disabled: Boolean,
    label: {
      type: String,
      default: 'Please enter OTP character',
    },
    length: {
      type: [Number, String],
      default: 4,
    },
    modelValue: {
      type: [Number, String],
      default: undefined,
    },
    placeholder: String,
    type: {
      type: String as PropType<'text' | 'password' | 'number'>,
      default: 'number'
    },
  },
  computed: {
    fields() {
      return Array(Number(this.length)).fill(0)
    },
    current() {
      return this.inputRef[this.focusIndex].value
    },
  },
  methods: {
    onInput(e: Event) {
      // The maxlength attribute doesn't work for the number type input, so the text type is used.
      // The following logic simulates the behavior of a number input.
      const inputTarget = e.target as HTMLInputElement
      console.log(inputTarget)
      console.log(this.current)
      console.log(this.isValidNumber(this.current))
      if (this.isValidNumber(this.current)) {
        inputTarget.value = ''
        return
      }

      const array = this.model.slice()
      array[this.focusIndex] = this.current

      let target: any = null

      if (this.focusIndex > this.model.value.length) {
        target = this.model.value.length + 1
      } else if (this.focusIndex + 1 !== this.length) {
        target = 'next'
      }

      this.model = array

      if (target) this.focusChild(this.$refs.contentRef as Element, target)

    },
    onFocus(e: FocusEvent, index: number) {
      focus()

      this.focusIndex = index

    },
    onBlur() {
      blur()

      this.focusIndex = -1
    },
    onKeyDown(e: KeyboardEvent) {
      const array = this.model.value.slice()
      const index = this.focusIndex
      let target: 'next' | 'prev' | 'first' | 'last' | number | null = null

      if (![
        'ArrowLeft',
        'ArrowRight',
        'Backspace',
        'Delete',
      ].includes(e.key)) return

      e.preventDefault()

      if (e.key === 'ArrowLeft') {
        target = 'prev'
      } else if (e.key === 'ArrowRight') {
        target = 'next'
      } else if (['Backspace', 'Delete'].includes(e.key)) {
        array[this.focusIndex] = ''
      }

      this.model = array

      if (this.focusIndex > 0 && e.key === 'Backspace') {
        target = 'prev'
      } else {
        requestAnimationFrame(() => {
          this.inputRef[index]?.select()
        })
      }

      requestAnimationFrame(() => {
        if (target != null) {
          this.focusChild(this.$refs.contentRef as HTMLElement, target)
        }
      })
    },
    onPaste(e: ClipboardEvent, index: number) {
      e.preventDefault()
      e.stopPropagation()

      const clipboardText = e?.clipboardData?.getData('Text').slice(0, length) ?? ''

      if (this.isValidNumber(clipboardText)) return

      this.model.value = clipboardText.split('')

      this.inputRef[index].blur()
    },
    isValidNumber(value: string) {
      return this.type === 'number' && /[^0-9]/g.test(value)
    },
    focusChild(el: Element, location?: 'next' | 'prev' | 'first' | 'last' | number) {
      const focusable = this.focusableChildren(el)

      if (!location) {
        if (el === document.activeElement || !el.contains(document.activeElement)) {
          focusable[0]?.focus()
        }
      } else if (location === 'first') {
        focusable[0]?.focus()
      } else if (location === 'last') {
        focusable.at(-1)?.focus()
      } else if (typeof location === 'number') {
        focusable[location]?.focus()
      } else {
        const _el = this.getNextElement(focusable, location)
        if (_el) _el.focus()
        else this.focusChild(el, location === 'next' ? 'first': 'last')
      }
    },
    focusableChildren(el: Element, filterByTabIndex = true) {
      const targets = ['button', '[href]', 'input:not([type="hidden"])', 'select', 'textarea', '[tabindex]']
          .map(s => `${s}${filterByTabIndex ? ':not([tabindex="-1"])' : ''}:not([disabled])`)
          .join(', ')
      return [...el.querySelectorAll(targets)] as HTMLElement[]
    },
    getNextElement(elements: HTMLElement[], location?: 'next' | 'prev', condition?: (el: HTMLElement) => boolean) {
      let _el
      let idx = elements.indexOf(document.activeElement as HTMLElement)
      const inc = location === 'next' ? 1 : -1
      do {
        idx += inc
        _el = elements[idx]
      } while ((!_el || _el.offsetParent == null || !(condition?.(_el) ?? true)) && idx < elements.length && idx >= 0)
      return _el
    },
  },
  watch: {
    model: {
      handler(val) {
        if (val.length === this.length) this.$emit('finish', val.join(''))
      },
      deep: true
    },
    focusIndex(val) {
      if (val < 0) return

      nextTick(() => {
        this.inputRef[val]?.select()
      })
    }
  },
})
</script>

<template>
<div :class="['base-otp-input', {'base-otp-input--divided': divider}]">
  <div
    ref="contentRef"
    class="base-otp-input__content"
  >
    <template v-for="(_, i) in fields" :key="i">

      <span
        v-if="divider && i !== 0"
        class="base-otp-input__divider"
      >
        {{ divider }}
      </span>

      <base-field
        :focused="(isFocused && focusAll) || focusIndex === i"
      >
        <input
          :ref="val => inputRef[i] = val as HTMLInputElement"
          :aria-label="`${label} ${i+1}`"
          :autofocus="i === 0 && autofocus"
          autocomplete="one-time-code"
          class="base-otp-input__field"
          :disabled="disabled"
          :inputmode="type === 'number' ? 'numeric' : 'text'"
          :min="type === 'number' ? 0: undefined"
          maxlength="1"
          :placeholder="placeholder"
          :type="type === 'number' ? 'text' : type"
          :value="model.value[i]"
          @input="onInput"
          @focus="e => onFocus(e, i)"
          @blur="onBlur"
          @keydown="onKeyDown"
          @paste="e => onPaste(e, i)"
        >
      </base-field>
    </template>

    <input
      class="base-otp-input-input"
      type="hidden"
      :value="model.value.join('')"
    >

  </div>
</div>
</template>

<style lang="scss" scoped>
.base-otp-input {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: .5rem 0;
  border-radius: 4px;
  & .base-field {
    height: 100%;
  }
  &--divided .base-otp-input__content {
    max-width: 360px;
  }
}
.base-otp-input__content {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  height: 64px;
  max-width: 320px;
  border-radius: inherit;
}
.base-otp-input__divider {
  margin: 0 8px;
}
.base-otp-input__field {
  height: 100%;
  width: 100%;
  color: inherit;
  font-size: 1.25rem;
  outline: none;
  text-align: center;
  background-color: transparent;
  border: 1px solid rgb(255,255,255);
  border-radius: 8px;
  }
</style>