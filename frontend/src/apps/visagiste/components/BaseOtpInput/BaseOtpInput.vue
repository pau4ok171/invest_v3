<script lang="ts">
// Styles
import './BaseOtpInput.scss'

// Components
import {
  BaseField,
  useBaseFieldProps,
} from '@/apps/visagiste/components/BaseField'
import { BaseOverlay } from '@/apps/visagiste/components/BaseOverlay'
import { BaseProgressCircular } from '@/apps/visagiste/components/BaseProgressCircular'

// Composables
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import { useFocus, useFocusProps } from '@/apps/visagiste/composables/focus'
import { useLocale } from '@/apps/visagiste/composables'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'

// Utilities
import { computed, nextTick, ref, watch } from 'vue'
import {
  defineComponent,
  filterInputAttrs,
  focusChild,
  pick,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'

export const useBaseOtpInputProps = propsFactory(
  {
    autofocus: Boolean,
    divider: String,
    focusAll: Boolean,
    label: {
      type: String,
      default: '$visagiste.input.otp',
    },
    length: {
      type: [Number, String],
      default: 6,
    },
    modelValue: {
      type: [Number, String],
      default: undefined,
    },
    placeholder: String,
    type: {
      type: String as PropType<'text' | 'password' | 'number'>,
      default: 'number',
    },

    ...useDimensionProps(),
    ...useFocusProps(),
    ...pick(
      useBaseFieldProps({
        variant: 'outlined' as const,
      }),
      [
        'baseColor',
        'bgColor',
        'class',
        'color',
        'disabled',
        'error',
        'loading',
        'rounded',
        'style',
        'theme',
        'variant',
      ]
    ),
  },
  'BaseOtpInput'
)

// Component
export default defineComponent({
  name: 'BaseOtpInput',
  components: {
    BaseProgressCircular,
    BaseField,
    BaseOverlay,
  },
  props: useBaseOtpInputProps(),
  emits: {
    finish: (val: string) => true,
    'update:focused': (val: boolean) => true,
    'update:modelValue': (val: string) => true,
  },
  setup(props, { attrs, emit }) {
    const { dimensionStyles } = useDimension(props)
    const { isFocused, focus, blur } = useFocus(props)
    const model = useProxiedModel(
      props,
      'modelValue',
      '',
      (val) => (val == null ? [] : String(val).split('')),
      (val) => val.join('')
    )

    const { t } = useLocale()

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

      if (!['ArrowLeft', 'ArrowRight', 'Backspace', 'Delete'].includes(e.key))
        return

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

      const clipboardText =
        e?.clipboardData?.getData('Text').slice(0, length.value) ?? ''

      if (isValidNumber(clipboardText)) return

      model.value = clipboardText.split('')

      inputRef.value?.[index].blur()
    }

    function reset() {
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

    watch(
      model,
      (val) => {
        if (val.length === length.value) emit('finish', val.join(''))
      },
      { deep: true }
    )

    watch(focusIndex, (val) => {
      if (val < 0) return

      nextTick(() => {
        inputRef.value[val]?.select()
      })
    })

    const { rootAttrs, inputAttrs } = computed(() => {
      const [root, input] = filterInputAttrs(attrs)
      return { rootAttrs: root, inputAttrs: input }
    }).value

    return {
      blur: () => {
        inputRef.value?.some((input) => input.blur())
      },
      focus: () => {
        inputRef.value?.[0].focus()
      },
      reset,
      isFocused,
      focusIndex,
      inputRef,
      contentRef,
      rootAttrs,
      inputAttrs,
      dimensionStyles,
      onInput,
      onKeyDown,
      onPaste,
      onBlur,
      onFocus,
      fields,
      model,
      t,
    }
  },
})
</script>

<template>
  <div
    :class="[
      'base-otp-input',
      {
        'base-otp-input--divided': !!$props.divider,
      },
      $props.class,
    ]"
    :style="$props.style"
    v-bind="rootAttrs"
  >
    <div
      ref="contentRef"
      class="base-otp-input__content"
      :style="[dimensionStyles]"
    >
      <template v-for="(_, i) in fields" :key="i">
        <span v-if="$props.divider && i !== 0" class="base-otp-input__divider">
          {{ $props.divider }}
        </span>

        <BaseField
          :focused="(isFocused && $props.focusAll) || focusIndex === i"
          :color="$props.color"
          :bgColor="$props.color"
          :baseColor="$props.baseColor"
          :disabled="$props.disabled"
          :error="$props.error"
          :variant="$props.variant"
        >
          <input
            :ref="(val) => (inputRef[i] = val as HTMLInputElement)"
            :aria-label="t($props.label, i + 1)"
            :autofocus="i === 0 && $props.autofocus"
            autocomplete="one-time-code"
            class="base-otp-input__field"
            :disabled="$props.disabled"
            :inputmode="$props.type === 'number' ? 'numeric' : 'text'"
            :min="$props.type === 'number' ? 0 : undefined"
            maxlength="1"
            :placeholder="$props.placeholder"
            :type="$props.type === 'number' ? 'text' : $props.type"
            :value="model[i]"
            @input="onInput"
            @focus="(e) => onFocus(e, i)"
            @blur="onBlur"
            @keydown="onKeyDown"
            @paste="(e) => onPaste(e, i)"
          />
        </BaseField>
      </template>

      <input
        class="base-otp-input-input"
        type="hidden"
        :value="model.join('')"
        v-bind="inputAttrs"
      />

      <BaseOverlay
        contained
        content-class="base-otp-input__loader"
        :model-value="!!$props.loading"
        persistent
      >
        <slot name="loader">
          <BaseProgressCircular
            :color="
              typeof $props.loading === 'boolean' ? undefined : $props.loading
            "
            indeterminate
            size="24"
            width="2"
          />
        </slot>
      </BaseOverlay>

      <slot />
    </div>
  </div>
</template>
