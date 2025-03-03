<script lang="ts">
// Components
import BaseSelectionControl, {
  useBaseSelectionControlProps,
} from '@/apps/visagiste/components/BaseSelectionControl/BaseSelectionControl.vue'

// Composables
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { IconValue } from '@/apps/visagiste/composables/icons'

// Utilities
import { computed } from 'vue'
import { propsFactory, defineComponent, omit } from '@/apps/visagiste/utils'

export const useBaseCheckboxButtonProps = propsFactory(
  {
    indeterminate: Boolean,
    indeterminateIcon: {
      type: IconValue,
      default: '$checkboxIndeterminate',
    },
    ...useBaseSelectionControlProps({
      falseIcon: '$checkboxOff',
      trueIcon: '$checkboxOn',
    }),
  },
  'BaseCheckboxButton'
)

export default defineComponent({
  name: 'BaseCheckboxButton',
  components: { BaseSelectionControl },
  props: useBaseCheckboxButtonProps(),
  emits: {
    'update:modelValue': (value: any) => true,
    'update:indeterminate': (value: boolean) => true,
  },
  setup(props) {
    const indeterminate = useProxiedModel(props, 'indeterminate')
    const model = useProxiedModel(props, 'modelValue')

    function onChange(v: any) {
      if (indeterminate.value) {
        indeterminate.value = false
      }
    }

    const falseIcon = computed(() => {
      return indeterminate.value ? props.indeterminateIcon : props.falseIcon
    })

    const trueIcon = computed(() => {
      return indeterminate.value ? props.indeterminateIcon : props.trueIcon
    })

    const controlProps = computed(() =>
      omit(BaseSelectionControl.filterProps(props), ['modelValue'])
    )

    return {
      model,
      onChange,
      falseIcon,
      trueIcon,
      indeterminate,
      controlProps,
    }
  },
})
</script>

<template>
  <BaseSelectionControl
    v-bind="controlProps"
    v-model="model"
    :class="['base-checkbox-button', $props.class]"
    :style="$props.style"
    type="checkbox"
    @update:modelValue="onChange"
    :false-icon="falseIcon"
    :true-icon="trueIcon"
    :aria-checked="indeterminate ? 'mixed' : undefined"
  >
    <template #input>
      <slot name="input" />
    </template>

    <template #label>
      <slot name="label" />
    </template>
  </BaseSelectionControl>
</template>
