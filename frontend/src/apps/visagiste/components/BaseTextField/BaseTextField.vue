<script lang="ts">
// Styles
import './BaseTextField.scss'

// Components
import {
  BaseField,
  useBaseFieldProps,
} from '@/apps/visagiste/components/BaseField'
import BaseInput, {
  useBaseInputProps,
} from '@/apps/visagiste/components/BaseInput/BaseInput.vue'
import BaseCounter from '@/apps/visagiste/components/BaseCounter/BaseCounter.vue'

// Composables
import type { BaseCounterSlot } from '@/apps/visagiste/components/BaseCounter/BaseCounter.vue'
import type { BaseInputSlots } from '@/apps/visagiste/components/BaseInput/BaseInput.vue'
import type { BaseFieldSlots } from '@/apps/visagiste/components/BaseField/BaseField.vue'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useFocus } from '@/apps/visagiste/composables/focus'

// Directives
import Intersect from '@/apps/visagiste/directives/intersect'

// Utilities
import { computed, nextTick, ref } from 'vue'
import {
  callEvent,
  defineComponent,
  filterInputAttrs,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType, SlotsType } from 'vue'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

const activeTypes = [
  'color',
  'file',
  'time',
  'date',
  'datetime-local',
  'week',
  'month',
]

export const useBaseTextFieldProps = propsFactory(
  {
    autofocus: Boolean,
    counter: [Boolean, Number, String],
    counterValue: [Number, Function] as PropType<
      number | ((value: any) => number)
    >,
    prefix: String,
    placeholder: String,
    persistentPlaceholder: Boolean,
    persistentCounter: Boolean,
    suffix: String,
    role: String,
    type: {
      type: String,
      default: 'text',
    },
    modelModifiers: Object as PropType<Record<string, boolean>>,

    ...useBaseInputProps(),
    ...useBaseFieldProps(),
  },
  'BaseTextField'
)

export type BaseTextFieldSlots = Omit<
  BaseInputSlots & BaseFieldSlots,
  'default'
> & {
  default: never
  counter: BaseCounterSlot
}

export default defineComponent({
  name: 'BaseTextField',
  components: { BaseCounter, BaseField, BaseInput },
  directives: {
    Intersect,
  },
  inheritAttrs: false,
  props: useBaseTextFieldProps(),
  slots: Object as SlotsType<BaseTextFieldSlots>,
  emits: {
    'click:control': (e: MouseEvent) => true,
    'mousedown:control': (e: MouseEvent) => true,
    'update:focused': (focused: boolean) => true,
    'update:modelValue': (val: string) => true,
  },
  setup(props, { attrs, emit }) {
    const model = useProxiedModel(props, 'modelValue')
    const { isFocused, focus, blur } = useFocus(props)
    const counterValue = computed(() => {
      return typeof props.counterValue === 'function'
        ? props.counterValue(model.value)
        : typeof props.counterValue === 'number'
          ? props.counterValue
          : (model.value ?? '').toString().length
    })
    const max = computed(() => {
      if (attrs.maxlength) return attrs.maxlength as unknown as undefined

      if (
        !props.counter ||
        (typeof props.counter !== 'number' && typeof props.counter !== 'string')
      )
        return undefined

      return props.counter
    })

    const isPlainOrUnderlined = computed(() =>
      ['plain', 'underlined'].includes(props.variant)
    )

    function onIntersect(
      isIntersecting: boolean,
      entries: IntersectionObserverEntry[]
    ) {
      if (!props.autofocus || !isIntersecting) return
      ;(entries[0].target as HTMLInputElement)?.focus?.()
    }

    const baseInputRef = ref<InstanceType<typeof BaseInput>>()
    const baseFieldRef = ref<InstanceType<typeof BaseField>>()
    const inputRef = ref<HTMLInputElement>()
    const isActive = computed(
      () =>
        activeTypes.includes(props.type) ||
        props.persistentPlaceholder ||
        isFocused.value ||
        props.active
    )

    function onFocus() {
      if (inputRef.value !== document.activeElement) {
        inputRef.value?.focus()
      }

      if (!isFocused.value) focus()
    }
    function onControlMousedown(e: MouseEvent) {
      emit('mousedown:control', e)

      if (e.target === inputRef.value) return

      onFocus()
      e.preventDefault()
    }
    function onControlClick(e: MouseEvent) {
      onFocus()

      emit('click:control', e)
    }
    function onClear(e: MouseEvent) {
      e.stopPropagation()

      onFocus()

      nextTick(() => {
        model.value = null

        callEvent(props['onClick:clear'], e)
      })
    }
    function onInput(e: Event) {
      const el = e.target as HTMLInputElement
      model.value = el.value
      if (
        props.modelModifiers?.trim &&
        ['text', 'search', 'password', 'tel', 'url'].includes(props.type)
      ) {
        const caretPosition = [el.selectionStart, el.selectionEnd]
        nextTick(() => {
          el.selectionStart = caretPosition[0]
          el.selectionEnd = caretPosition[1]
        })
      }
    }
    const isCounterEmpty = useSlotIsEmpty('counter')
    const isDetailsEmpty = useSlotIsEmpty('details')
    const hasCounter = computed(
      () =>
        !isCounterEmpty.value ||
        (props.counter !== false && props.counter != null)
    )
    const hasDetails = computed(() => hasCounter || !isDetailsEmpty.value)
    const { rootAttrs, inputAttrs } = computed(() => {
      const [root, input] = filterInputAttrs(attrs)
      return { rootAttrs: root, inputAttrs: input }
    }).value
    const inputProps = computed(() => {
      const { modelValue: _, ...rest } = BaseInput.filterProps(props)
      return rest
    })
    const fieldProps = computed(() => BaseField.filterProps(props))

    return {
      baseInputRef,
      baseFieldRef,
      inputRef,
      model,
      counterValue,
      max,
      isPlainOrUnderlined,
      isActive,
      isFocused,
      hasDetails,
      hasCounter,
      rootAttrs,
      inputAttrs,
      inputProps,
      fieldProps,
      onIntersect,
      onControlMousedown,
      onControlClick,
      onClear,
      onInput,
      onFocus,
      blur,
      focus,
    }
  },
})
</script>

<template>
  <BaseInput
    ref="baseInputRef"
    v-model="model"
    :class="[
      'base-text-field',
      {
        'base-text-field--prefixed': $props.prefix,
        'base-text-field--suffixed': $props.suffix,
        'base-input-plain-underlined': isPlainOrUnderlined,
      },
      $props.class,
    ]"
    :style="$props.style"
    v-bind="{ ...rootAttrs, ...inputProps }"
    :centerAffix="!isPlainOrUnderlined"
    :focused="isFocused"
  >
    <template #append="slotProps"
      ><slot name="append" v-bind="slotProps"
    /></template>
    <template #prepend="slotProps"
      ><slot name="prepend" v-bind="slotProps"
    /></template>
    <template #details="slotProps"
      ><slot name="details" v-bind="slotProps"
    /></template>
    <template #message="slotProps"
      ><slot name="message" v-bind="slotProps"
    /></template>

    <template #default="{ id, isDisabled, isDirty, isReadonly, isValid }">
      <BaseField
        ref="baseFieldRef"
        v-bind="fieldProps"
        :id="id.value"
        :active="isActive || isDirty.value"
        :dirty="isDirty.value || $props.dirty"
        :disabled="isDisabled.value"
        :focused="isFocused"
        :error="isValid.value === false"
        :role="$props.role"
        :onMousedown="onControlMousedown"
        :onClick="onControlClick"
        :onClick:clear="onClear"
        :onClick:prependInner="$props['onClick:prependInner']"
        :onClick:appendInner="$props['onClick:appendInner']"
      >
        <template #append-inner="slotProps"
          ><slot name="append-inner" v-bind="slotProps"
        /></template>
        <template #prepend-inner="slotProps"
          ><slot name="prepend-inner" v-bind="slotProps"
        /></template>
        <template #clear="slotProps"
          ><slot name="clear" v-bind="slotProps"
        /></template>
        <template #loader="slotProps"
          ><slot name="loader" v-bind="slotProps"
        /></template>
        <template #label="slotProps"
          ><slot name="label" v-bind="slotProps"
        /></template>

        <template #default="{ props: { class: fieldClass, ...slotProps } }">
          <template v-if="$props.prefix">
            <span class="base-text-field__prefix">
              <span class="base-text-field__prefix__text">
                {{ $props.prefix }}
              </span>
            </span>
          </template>

          <template v-if="$slots.default">
            <div :class="fieldClass" data-no-activator="">
              <slot />

              <input
                ref="inputRef"
                :value="model"
                @input="onInput"
                v-intersect.once="{ handler: onIntersect }"
                :autofocus="$props.autofocus"
                :readonly="isReadonly.value"
                :disabled="isDisabled.value"
                :name="$props.name"
                :placeholder="$props.placeholder"
                :size="1"
                :type="$props.type"
                @focus="onFocus"
                @blur="blur"
                v-bind="{ ...slotProps, ...inputAttrs }"
              />
            </div>
          </template>
          <template v-else>
            <input
              ref="inputRef"
              :class="fieldClass"
              :value="model"
              @input="onInput"
              v-intersect.once="{ handler: onIntersect }"
              :autofocus="$props.autofocus"
              :readonly="isReadonly.value"
              :disabled="isDisabled.value"
              :name="$props.name"
              :placeholder="$props.placeholder"
              :size="1"
              :type="$props.type"
              @focus="onFocus"
              @blur="blur"
              v-bind="{ ...slotProps, ...inputAttrs }"
            />
          </template>

          <template v-if="$props.suffix">
            <span class="base-text-field__suffix">
              <span class="base-text-field__suffix__text">
                {{ $props.suffix }}
              </span>
            </span>
          </template>
        </template>
      </BaseField>
    </template>

    <template v-if="hasDetails" #details="slotProps">
      <slot name="details" v-bind="slotProps" />
      <template v-if="hasCounter">
        <span />

        <BaseCounter
          :active="$props.persistentCounter || isFocused"
          :value="counterValue"
          :max="max"
          :disabled="$props.disabled"
        >
          <slot name="counter" />
        </BaseCounter>
      </template>
    </template>
  </BaseInput>
</template>