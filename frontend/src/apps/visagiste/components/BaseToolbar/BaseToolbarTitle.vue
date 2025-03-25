<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseToolbarTitleProps = propsFactory(
  {
    text: String,

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseToolbarItem'
)

export type BaseToolbarTitleSlots = {
  default: never
  text: never
}

export default defineComponent({
  name: 'BaseToolbarTitle',
  props: useBaseToolbarTitleProps(),
  setup(props) {
    const defaultIsEmpty = useSlotIsEmpty('default')
    const textIsEmpty = useSlotIsEmpty('text')

    const hasText = computed(
      () => !!(!defaultIsEmpty.value || !textIsEmpty.value || props.text)
    )
    return {
      hasText,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag"
    :class="['base-toolbar-title', $props.class]"
    :style="$props.style"
  >
    <template v-if="hasText">
      <div class="base-toolbar-title__placeholder">
        <slot name="text">
          {{ $props.text }}
        </slot>

        <slot name="default" />
      </div>
    </template>
  </component>
</template>
