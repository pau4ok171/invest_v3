<script lang="ts">
// Styles
import './BaseSelectionControl.scss'

// Components
import {
  useSelectionControlGroupProps,
  BaseSelectionControlGroupSymbol,
} from '@/apps/visagiste/components/BaseSelectionGroupControl/BaseSelectionControlGroup.vue'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import BaseLabel from '@/apps/visagiste/components/BaseLabel/BaseLabel.vue'

// Composables
import {
  useBackgroundColor,
  useTextColor,
} from '@/apps/visagiste/composables/color'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useDensity } from '@/apps/visagiste/composables/density'

// Directives
import Ripple from '@/directives/ripple'

// Utilities
import { computed, h, inject, nextTick, ref, shallowRef } from 'vue'
import {
  propsFactory,
  defineComponent,
  EventProp,
  wrapInArray,
  getUid,
  matchesSelector,
  filterInputAttrs,
} from '@/apps/visagiste/utils'

// Types
import type {
  VNode,
  WritableComputedRef,
  CSSProperties,
  ExtractPropTypes,
  Ref,
} from 'vue'
import type { IconValue } from '@/apps/visagiste/composables/icons'

export type SelectionControlSlot = {
  model: WritableComputedRef<boolean>
  textColorClasses: Ref<string[]>
  textColorStyles: Ref<CSSProperties>
  backgroundColorClasses: Ref<string[]>
  backgroundColorStyles: Ref<CSSProperties>
  inputMode: VNode
  icon: IconValue | undefined
  props: {
    onBlur: (e: Event) => void
    onFocus: (e: Event) => void
    id: string
  }
}

export type BaseSelectionControlSlots = {
  default: {
    backgroundColorClasses: Ref<string[]>
    backgroundColorStyles: Ref<CSSProperties>
  }
  label: { label: string | undefined; props: Record<string, unknown> }
  input: SelectionControlSlot
}

export const useBaseSelectionControlProps = propsFactory(
  {
    label: String,
    baseColor: String,
    trueValue: null,
    falseValue: null,
    value: null,

    ...useComponentProps(),
    ...useSelectionControlGroupProps(),
  },
  'BaseSelectionControl'
)

export function useSelectionControl(
  props: ExtractPropTypes<ReturnType<typeof useBaseSelectionControlProps>> & {
    'onUpdate:modelValue': EventProp | undefined
  }
) {
  const group = inject(BaseSelectionControlGroupSymbol, undefined)
  const { densityClasses } = useDensity(props)
  const modelValue = useProxiedModel(props, 'modelValue')
  const trueValue = computed(() =>
    props.trueValue !== undefined
      ? props.trueValue
      : props.value !== undefined
        ? props.value
        : true
  )
  const falseValue = computed(() =>
    props.falseValue !== undefined ? props.falseValue : false
  )
  const isMultiple = computed(
    () =>
      !!props.multiple ||
      (props.multiple == null && Array.isArray(modelValue.value))
  )
  const model = computed({
    get() {
      const val = group ? group.modelValue.value : modelValue.value

      return isMultiple.value
        ? wrapInArray(val).some((v: any) =>
            props.valueComparator(v, trueValue.value)
          )
        : props.valueComparator(val, trueValue.value)
    },
    set(val: boolean) {
      if (props.readonly) return

      const currentValue = val ? trueValue.value : falseValue.value

      let newVal = currentValue

      if (isMultiple.value) {
        newVal = val
          ? [...wrapInArray(modelValue.value), currentValue]
          : wrapInArray(modelValue.value).filter(
              (item: any) => !props.valueComparator(item, trueValue.value)
            )
      }

      if (group) {
        group.modelValue.value = newVal
      } else {
        modelValue.value = newVal
      }
    },
  })
  const { textColorClasses, textColorStyles } = useTextColor(
    computed(() => {
      if (props.error || props.disabled) return undefined

      return modelValue.value ? props.color : props.baseColor
    })
  )
  const { backgroundColorClasses, backgroundColorStyles } = useBackgroundColor(
    computed(() => {
      return model.value && !props.error && !props.disabled
        ? props.color
        : props.baseColor
    })
  )
  const icon = computed(() => (model.value ? props.trueIcon : props.falseIcon))

  return {
    group,
    densityClasses,
    trueValue,
    falseValue,
    model,
    textColorClasses,
    textColorStyles,
    backgroundColorClasses,
    backgroundColorStyles,
    icon,
  }
}

export default defineComponent({
  name: 'BaseSelectionControl',
  components: {
    BaseLabel,
    BaseIcon,
  },
  directives: {
    Ripple,
  },
  inheritAttrs: false,
  props: useBaseSelectionControlProps(),
  emits: {
    'update:modelValue': (value: any) => true,
  },
  setup(props, { attrs }) {
    const {
      group,
      densityClasses,
      icon,
      model,
      textColorClasses,
      textColorStyles,
      backgroundColorClasses,
      backgroundColorStyles,
      trueValue,
    } = useSelectionControl(props)
    const uid = getUid()
    const isFocused = shallowRef(false)
    const isFocusVisible = shallowRef(false)
    const input = ref<HTMLInputElement>()
    const id = computed(() => props.id || `input-${uid}`)
    const isInteractive = computed(() => !props.disabled && !props.readonly)

    group?.onForceUpdate(() => {
      if (input.value) {
        input.value.checked = model.value
      }
    })

    function onFocus(e: FocusEvent) {
      if (!isInteractive.value) return

      isFocused.value = true
      if (
        matchesSelector(e.target as HTMLElement, ':focus-visible') !== false
      ) {
        isFocusVisible.value = true
      }
    }

    function onBlur() {
      isFocused.value = false
      isFocusVisible.value = false
    }

    function onClickLabel(e: Event) {
      e.stopPropagation()
    }

    function onInput(e: Event) {
      if (!isInteractive.value) {
        if (input.value) {
          // model value is not updated when input is not interactive
          // but the internal checked state of the input is still updated,
          // so here it's value is restored
          input.value.checked = model.value
        }

        return
      }

      if (props.readonly && group) {
        nextTick(() => group.forceUpdate())
      }

      model.value = (e.target as HTMLInputElement).checked
    }

    const [rootAttrs, inputAttrs] = filterInputAttrs(attrs)
    const inputNode = () =>
      h('input', {
        ref: input,
        checked: model.value,
        disabled: !!props.disabled,
        id: id.value,
        onBlur,
        onFocus,
        onInput,
        'aria-disabled': !!props.disabled,
        'aria-label': props.label,
        type: props.type,
        value: trueValue.value,
        name: props.name,
        'aria-checked': props.type === 'checkbox' ? model.value : undefined,
        ...inputAttrs,
      })
    return {
      model,
      id,
      isFocused,
      isFocusVisible,
      densityClasses,
      textColorClasses,
      textColorStyles,
      backgroundColorClasses,
      backgroundColorStyles,
      icon,
      rootAttrs,
      inputNode,
      onFocus,
      onBlur,
      onClickLabel,
    }
  },
})
</script>

<template>
  <div
    :class="[
      'base-selection-control',
      {
        'base-selection-control--dirty': model,
        'base-selection-control--disabled': $props.disabled,
        'base-selection-control--error': $props.error,
        'base-selection-control--focused': isFocused,
        'base-selection-control--focus-visible': isFocusVisible,
        'base-selection-control--inline': $props.inline,
      },
      densityClasses,
      $props.class,
    ]"
    :style="$props.style"
    v-bind="{ ...rootAttrs }"
  >
    <div
      :class="['base-selection-control__wrapper', textColorClasses]"
      :style="textColorStyles"
    >
      <slot
        v-bind="{
          backgroundColorClasses,
          backgroundColorStyles,
        }"
      />

      <div
        :class="['base-selection-control__input']"
        v-ripple="
          $props.ripple && [
            !$props.disabled && !$props.readonly,
            null,
            ['center', 'circle'],
          ]
        "
      >
        <slot
          name="input"
          v-bind="{
            model,
            textColorClasses,
            textColorStyles,
            backgroundColorClasses,
            backgroundColorStyles,
            inputNode,
            icon: icon,
            props: {
              onFocus,
              onBlur,
              id: id,
            },
          }"
        >
          <BaseIcon v-if="icon" key="icon" :icon />

          <component :is="inputNode" />
        </slot>
      </div>
    </div>

    <BaseLabel
      v-if="$props.label || $slots.label"
      :for="id"
      @click="onClickLabel"
    >
      <slot name="label">
        {{ $props.label }}
      </slot>
    </BaseLabel>
  </div>
</template>
