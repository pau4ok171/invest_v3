<script lang="ts">
// Styles
import './BaseTextarea.scss'
import '../BaseTextField/BaseTextField.scss'

// Components
import { BaseCounter } from '@/apps/visagiste/components/BaseCounter'
import {
  BaseField,
  useBaseFieldProps,
} from '@/apps/visagiste/components/BaseField'
import {
  BaseInput,
  useBaseInputProps,
} from '@/apps/visagiste/components/BaseInput'

// Composables
import { useFocus } from '@/apps/visagiste/composables/focus'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import {useSlotIsEmpty} from "@/apps/visagiste/composables/slotIsEmpty";

// Directives
import Intersect from "@/apps/visagiste/directives/intersect";

// Utilities
import {computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef, watch, watchEffect} from "vue";
import {callEvent, clamp, convertToUnit, defineComponent, filterInputAttrs, propsFactory} from '@/apps/visagiste/utils'

// Types
import type {PropType} from "vue";
import type {BaseInputSlot} from "@/apps/visagiste/components/BaseInput/BaseInput.vue";
import type {BaseFieldSlots} from "@/apps/visagiste/components/BaseField/BaseField.vue";
import type {BaseCounterSlot} from "@/apps/visagiste/components/BaseCounter/BaseCounter.vue";

export const useBaseTextareaProps = propsFactory({
  autoGrow: Boolean,
  autofocus: Boolean,
  counter: [Boolean, Number, String] as PropType<true | number | string>,
  counterValue: Function as PropType<(value: any) => number>,
  prefix: String,
  placeholder: String,
  persistentPlaceholder: Boolean,
  persistentCounter: Boolean,
  noResize: Boolean,
  rows: {
    type: [Number, String],
    default: 5,
    validator: (v: any) => !isNaN(parseFloat(v)),
  },
  maxRows: {
    type: [Number, String],
    validator: (v: any) => !isNaN(parseFloat(v)),
  },
  suffix: String,
  modelModifiers: Object as PropType<Record<string, boolean>>,

  ...useBaseInputProps(),
  ...useBaseFieldProps(),
}, 'BaseTextArea')

type BaseTextareaSlots = Omit<BaseInputSlot & BaseFieldSlots, 'default'> & {
  counter: BaseCounterSlot
}

export default defineComponent({
  name: 'BaseTextarea',
  components: {BaseCounter, BaseField, BaseInput},
  directives: { Intersect },
  inheritAttrs: false,
  props: useBaseTextareaProps(),
  emits: {
    'click:control': (e: MouseEvent) => true,
    'mousedown:control': (e: MouseEvent) => true,
    'update:focused': (focused: boolean) => true,
    'update:modelValue': (value: string) => true,
  },
  setup (props, { attrs, emit }) {
    const model = useProxiedModel(props, 'modelValue')
    const { isFocused, focus, blur } = useFocus(props)
    const counterValue = computed(() => {
      return typeof props.counterValue === 'function'
        ? props.counterValue(model.value)
        : (model.value || '').toString().length
    })
    const max = computed(() => {
      if (attrs.maxlength) return attrs.maxlength as string | number

      if (
        !props.counter ||
        (typeof props.counter !== 'number' &&
        typeof props.counter !== 'string')
      ) return undefined

      return props.counter
    })

    function onIntersect (
      isIntersecting: boolean,
      entries: IntersectionObserverEntry[]
    ) {
      if (!props.autofocus || !isIntersecting) return

      (entries[0].target as HTMLInputElement)?.focus?.()
    }

    const baseInputRef = ref<InstanceType<typeof BaseInput>>()
    const baseFieldRef = ref<InstanceType<typeof BaseInput>>()
    const controlHeight = shallowRef('')
    const textareaRef = ref<HTMLInputElement>()
    const isActive = computed(() => (
      props.persistentPlaceholder ||
      isFocused.value ||
      props.active
    ))

    function onFocus () {
      if (textareaRef.value !== document.activeElement) {
        textareaRef.value?.focus()
      }

      if (!isFocused.value) focus()
    }
    function onControlClick (e: MouseEvent) {
      onFocus()

      emit('click:control', e)
    }
    function onControlMousedown (e: MouseEvent) {
      emit('mousedown:control', e)
    }
    function onClear (e: MouseEvent) {
      e.stopPropagation()

      onFocus()

      nextTick(() => {
        model.value = ''

        callEvent(props['onClick:clear'], e)
      })
    }
    function onInput (e: Event) {
      const el = e.target as HTMLTextAreaElement
      model.value = el.value
      if (props.modelModifiers?.trim) {
        const caretPosition = [el.selectionStart, el.selectionEnd]
        nextTick(() => {
          el.selectionStart = caretPosition[0]
          el.selectionEnd = caretPosition[1]
        })
      }
    }

    const sizerRef = ref<HTMLTextAreaElement>()
    const rows = ref(+props.rows)
    const isPlainOrUnderlined = computed(() => ['plain', 'underlined'].includes(props.variant))
    watchEffect(() => {
      if (!props.autoGrow) rows.value = +props.rows
    })
    function calculateInputHeight () {
      if (!props.autoGrow) return

      nextTick(() => {
        if (!sizerRef.value || !baseFieldRef.value) return

        const style = getComputedStyle(sizerRef.value)
        const fieldStyle = getComputedStyle(baseFieldRef.value.$el)

        const padding = parseFloat(style.getPropertyValue('--base-field-padding-top')) +
          parseFloat(style.getPropertyValue('--base-input-padding-top')) +
          parseFloat(style.getPropertyValue('--base-field-padding-bottom'))

        const height = sizerRef.value?.scrollHeight
        const lineHeight = parseFloat(style.lineHeight)
        const minHeight = Math.max(
          parseFloat(props.rows) * lineHeight + padding,
            parseFloat(fieldStyle.getPropertyValue('--base-input-control-height'))
        )
        const maxHeight = parseFloat(props.maxRows!) * lineHeight + padding || Infinity
        const newHeight = clamp(height ?? 0, minHeight, maxHeight)
        rows.value = Math.floor(newHeight - padding) * lineHeight

        controlHeight.value = convertToUnit(newHeight)
      })
    }

    onMounted(calculateInputHeight)
    watch(model, calculateInputHeight)
    watch(() => props.rows, calculateInputHeight)
    watch(() => props.maxRows, calculateInputHeight)
    watch(() => props.density, calculateInputHeight)

    let observer: ResizeObserver | undefined
    watch(sizerRef, val => {
      if (val) {
        observer = new ResizeObserver(calculateInputHeight)
        observer.observe(sizerRef.value!)
      } else {
        observer?.disconnect()
      }
    })
    onBeforeUnmount(() => {
      observer?.disconnect()
    })

    const counterIsEmpty = useSlotIsEmpty('counter')
    const detailsIsEmpty = useSlotIsEmpty('details')
    const hasCounter = computed(() => !!(!counterIsEmpty.value || props.counter || props.counterValue))
    const hasDetails = computed(() => (hasCounter.value || !detailsIsEmpty.value))
    const { rootAttrs, inputAttrs } = computed(() => {
      const [root, input] = filterInputAttrs(attrs);
      return { rootAttrs: root, inputAttrs: input };
    }).value;
    const inputProps = computed(() => {
      const { modelValue: _, ...rest } = BaseInput.filterProps(props);
      return rest;
    });
    const fieldProps = computed(() => BaseField.filterProps(props));

    return {
      hasCounter,
      hasDetails,
      rootAttrs,
      inputAttrs,
      inputProps,
      fieldProps,
      baseInputRef,
      baseFieldRef,
      textareaRef,
      sizerRef,
      model,
      rows,
      controlHeight,
      counterValue,
      max,
      isPlainOrUnderlined,
      isFocused,
      isActive,
      onControlClick,
      onControlMousedown,
      onClear,
      onInput,
      onIntersect,
      onFocus,
      blur,
    }
  },
})
</script>

<template>
  <BaseInput
    ref="baseInputRef"
    v-model="model"
    :class="[
      'base-textarea base-text-field',
      {
        'base-textarea--prefixed': $props.prefix,
        'base-textarea--suffixed': $props.suffix,
        'base-text-field--prefixed': $props.prefix,
        'base-text-field--suffixed': $props.suffix,
        'base-textarea--auto-grow': $props.autoGrow,
        'base-textarea--no-resize': $props.noResize || $props.autoGrow,
        'base-input--plain-underlined': isPlainOrUnderlined,
      },
      $props.class,
    ]"
    :style="$props.style"
    v-bind="{ ...rootAttrs, ...inputProps }"
    :center-affix="rows === 1 && !isPlainOrUnderlined"
    :focused="isFocused"
  >
    <template #prepend>
      <slot name="prepend"/>
    </template>

    <template #append>
      <slot name="append"/>
    </template>

    <template #message>
      <slot name="message"/>
    </template>

    <template #default="{ id, isDisabled, isDirty, isReadonly, isValid }">
      <BaseField
        ref="baseFieldRef"
        :style="{
          '--base-textarea-control-height': controlHeight,
        }"
        :onClick="onControlClick"
        :onClick:clear="onClear"
        :onClick:prependInner="$props['onClick:prependInner']"
        :onClick:appendInner="$props['onClick:appendInner']"
        v-bind="fieldProps"
        :id="id.value"
        :active="isActive || isDirty.value"
        :center-affix="rows === 1 && !isPlainOrUnderlined"
        :dirty="isDirty.value || $props.dirty"
        :disabled="isDisabled.value"
        :focused="isFocused"
        :error="isValid.value === false"
      >
        <template #loader>
          <slot name="loader"/>
        </template>

        <template #prepend-inner>
          <slot name="prepend-inner"/>
        </template>

        <template #append-inner>
          <slot name="append-inner"/>
        </template>

        <template #clear>
          <slot name="clear"/>
        </template>

        <template #label>
          <slot name="label"/>
        </template>

        <template #default="{ props: { class: fieldClass, ...slotProps } }">

          <template v-if="$props.prefix">
            <span class="base-text-field__prefix">
              {{ $props.prefix }}
            </span>
          </template>

          <textarea
            ref="textareaRef"
            :class="fieldClass"
            :value="model"
            @input="onInput"
            v-intersect.once="{ handler: onIntersect }"
            :autofocus="$props.autofocus"
            :readonly="isReadonly.value"
            :disabled="isDisabled.value"
            :placeholder="$props.placeholder"
            :rows="$props.rows"
            :name="$props.name"
            @focus="onFocus"
            @blur="blur"
            v-bind="{ ...slotProps, ...inputAttrs }"
          />

          <template v-if="$props.autoGrow">
            <textarea
              :class="[
                fieldClass,
                'base-textarea__sizer',
              ]"
              :id="`${slotProps.id}--sizer`"
              v-model="model"
              ref="sizerRef"
              readonly
              aria-hidden="true"
            />
          </template>

          <template v-if="$props.suffix">
            <span class="base-text-field__suffix">
              {{ $props.suffix }}
            </span>
          </template>

        </template>
      </BaseField>
    </template>

    <template #details="slotProps">
      <template v-if="hasDetails">
        <slot name="details" v-bind="slotProps"/>

        <template v-if="hasCounter">
          <span />

          <BaseCounter
            :active="$props.persistentCounter || isFocused"
            :value="counterValue"
            :max="max"
            :disabled="$props.disabled"
          >
            <slot name="counter"/>
          </BaseCounter>
        </template>
      </template>
    </template>
  </BaseInput>
</template>
