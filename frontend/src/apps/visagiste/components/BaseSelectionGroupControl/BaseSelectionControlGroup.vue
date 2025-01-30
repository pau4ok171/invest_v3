<script lang="ts">
// Styles
import './BaseSelectionControlGroup.scss'

// Composables
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {useThemeProps} from "@/apps/visagiste/composables/theme";
import {useDensityProps} from "@/apps/visagiste/composables/density";
import {IconValue} from "@/apps/visagiste/composables/icons";
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";
import {provideDefaults} from "@/apps/visagiste/composables/defaults";

// Utilities
import { computed, provide, toRef, onScopeDispose } from 'vue'
import { deepEqual, getUid, propsFactory, defineComponent } from "@/apps/visagiste/utils";

// Types
import type { InjectionKey, PropType, Ref } from 'vue'
import type { RippleDirectiveBinding } from "@/directives/ripple";

export interface BaseSelectionControlGroupContext {
  modelValue: Ref<any>
  forceUpdate: () => void
  onForceUpdate: (fn: () => void) => void
}

export const BaseSelectionControlGroupSymbol: InjectionKey<BaseSelectionControlGroupContext> = Symbol.for('visagiste:selection-control-group')

export const useSelectionControlGroupProps = propsFactory({
  color: String,
  disabled: {
    type: Boolean as PropType<boolean | null>,
    default: null,
  },
  defaultsTarget: String,
  error: Boolean,
  id: String,
  inline: Boolean,
  falseIcon: IconValue,
  trueIcon: IconValue,
  ripple: {
    type: [Boolean, Object] as PropType<RippleDirectiveBinding['value']>,
    default: true,
  },
  multiple: {
    type: Boolean as PropType<boolean | null>,
    default: null,
  },
  name: String,
  readonly: {
    type: Boolean as PropType<boolean | null>,
    default: null,
  },
  modelValue: null,
  type: String,
  valueComparator: {
    type: Function as PropType<typeof deepEqual>,
    default: deepEqual,
  },

  ...useComponentProps(),
  ...useDensityProps(),
  ...useThemeProps(),
}, 'SelectionControlGroup')

export const useBaseSelectionControlGroupProps = propsFactory({
  ...useSelectionControlGroupProps({
    defaultsTarget: 'BaseSelectionControl',
  }),
}, 'BaseSelectionControlGroupProps')

export default defineComponent({
  name: "BaseSelectionControlGroup",
  props: useBaseSelectionControlGroupProps(),
  emits: {
    'update:modelValue': (value: any) => true,
  },
  setup (props) {
    const modelValue = useProxiedModel(props, 'modelValue')
    const uid = getUid()
    const id = computed(() => props.id || `base-selection-control-group-${uid}`)
    const name = computed(() => props.name || id.value)

    const updateHandlers = new Set<() => void>()
    provide(BaseSelectionControlGroupSymbol, {
      modelValue,
      forceUpdate: () => {
        updateHandlers.forEach(fn => fn())
      },
      onForceUpdate: cb => {
        updateHandlers.add(cb)
        onScopeDispose(() => {
          updateHandlers.delete(cb)
        })
      },
    })

    provideDefaults({
      [props.defaultsTarget]: {
        color: toRef(props, 'color'),
        disabled: toRef(props, 'disabled'),
        density: toRef(props, 'density'),
        error: toRef(props, 'error'),
        inline: toRef(props, 'inline'),
        modelValue,
        multiple: computed(() => !!props.multiple || (props.multiple == null && Array.isArray(modelValue.value))),
        name,
        falseIcon: toRef(props, 'falseIcon'),
        trueIcon: toRef(props, 'trueIcon'),
        readonly: toRef(props, 'readonly'),
        ripple: toRef(props, 'ripple'),
        type: toRef(props, 'type'),
        valueComparator: toRef(props, 'valueComparator'),
      },
    })
  },
})
</script>

<template>
  <div
    :class="[
      'base-selection-control-group',
      {
        'base-selection-control-group--inline': $props.inline,
      },
      $props.class,
    ]"
    :style="$props.style"
    :role="$props.type === 'radio' ? 'radiogroup' : undefined"
  >
    <slot/>
  </div>
</template>
