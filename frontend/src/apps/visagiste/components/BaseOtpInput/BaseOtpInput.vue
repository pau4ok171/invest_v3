<script lang="ts">
// Utilities
import {computed, defineComponent, nextTick, ref, watch} from 'vue'
import BaseField from "@/apps/visagiste/components/BaseField/BaseField.vue";
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";
import {focusChild} from "@/apps/visagiste/utils";
import {useFocus} from "@/apps/visagiste/composables/focus";
import {allowedThemes} from "../BaseTheme/baseTheme.d";
import {allowedVariants} from "../BaseField/BaseField.types";

// Types
import type {PropType} from 'vue'
import type {Theme} from "@/apps/visagiste/components/BaseTheme/baseTheme";
import type {Variant} from "@/apps/visagiste/components/BaseField/BaseField.types";

// Component
export default defineComponent({
    name: "BaseOtpInput",
    components: {
      BaseField,
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
      focused: Boolean,
      variant: {
        type: String as PropType<Variant>,
        default: 'filled',
        validator: (v: any) => allowedVariants.includes(v),
      },
      baseColor: String,
      bgColor: String,
      color: String,
      error: Boolean,
      loading: Boolean,
      rounded: Boolean,
      theme: {
        type: String as PropType<Theme>,
        default: 'light',
        validator: (v: any) => allowedThemes.includes(v)
      },
    },
    emits: {
      finish: (val: string) => true,
      'update:focused': (val: boolean) => true,
      'update:modelValue': (val: string) => true,
    },
    setup(props, { emit }) {
      const { isFocused, focus, blur } = useFocus(props)
      const model = useProxiedModel(
        props,
        'modelValue',
        '',
        val => val == null ? [] : String(val).split(''),
        val => val.join('')
      )

      const length = computed(() => Number(props.length))
      const fields = computed(() => Array(length.value).fill(0))
      const focusIndex = ref(-1)
      const contentRef = ref<HTMLElement>()
      const inputRef = ref<HTMLInputElement[]>([])
      const current = computed(() => inputRef.value[focusIndex.value])

      function onInput() {
        // The maxlength attribute doesn't work for the number type input, so the text type is used.
        // The following logic simulates the behavior of a number input.
        if (isValidNumber(current.value.value)) {
          current.value.value = ''
          return
        }

        const array = model.value.slice()
        const value = current.value.value

        array[focusIndex.value] = value

        let target: any = null

        if (focusIndex.value > model.value.length) {
          target = model.value.length + 1
        } else if (focusIndex.value + 1 !== length.value) {
          target = 'next'
        }

        model.value = array

        if (target) focusChild(contentRef.value!, target)
      }

      function onKeyDown(e: KeyboardEvent) {
        const array = model.value.slice()
        const index = focusIndex.value
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
          array[focusIndex.value] = ''

          model.value = array

          if (focusIndex.value > 0 && e.key === 'Backspace') {
            target = 'prev'
          } else {
            requestAnimationFrame(() => {
              inputRef.value[index]?.select()
            })
          }
        }

        requestAnimationFrame(() => {
          if (target != null) {
            focusChild(contentRef.value!, target)
          }
        })
      }

      function onPaste(e: ClipboardEvent, index: number) {
        e.preventDefault()
        e.stopPropagation()

        const clipboardText = e?.clipboardData?.getData('Text').slice(0, length.value) ?? ''

        if (isValidNumber(clipboardText)) return

        model.value = clipboardText.split('')

        inputRef.value?.[index].blur()
      }

      function reset () {
        model.value = []
      }

      function onFocus(e: FocusEvent, index: number) {
        focus()

        focusIndex.value = index

      }

      function onBlur() {
        blur()

        focusIndex.value = -1
      }

      function isValidNumber(value: string) {
        return props.type === 'number' && /[^0-9]/g.test(value)
      }

      watch(model, val => {
        if (val.length === length.value) emit('finish', val.join(''))
      }, { deep:true })

      watch(focusIndex, val => {
        if (val < 0) return

        nextTick(() => {
          inputRef.value[val]?.select()
        })
      })

      return {
        blur: () => {
          inputRef.value?.some(input => input.blur())
        },
        focus: () => {
          inputRef.value?.[0].focus()
        },
        isFocused,
        focusIndex,
        inputRef,
        contentRef,
        onInput,
        onKeyDown,
        onPaste,
        onBlur,
        onFocus,
        fields,
        model,
      }
    },
  })
</script>

<template>
<div :class="[
  'base-otp-input',
  {
    'base-otp-input--divided': divider
  }]"
>
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
        :theme
        :color
        :variant
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
          :value="model[i]"
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
      :value="model.join('')"
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