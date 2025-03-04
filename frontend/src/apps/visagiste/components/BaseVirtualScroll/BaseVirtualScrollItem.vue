<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useResizeObserver } from '@/apps/visagiste/composables/resizeObserver'

// Utilities
import { watch } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseVirtualScrollItemProps = propsFactory(
  {
    renderless: Boolean,

    ...useComponentProps(),
  },
  'BaseVirtualScrollItem'
)

export default defineComponent({
  name: 'BaseVirtualScrollItem',
  props: useBaseVirtualScrollItemProps(),
  inheritAttrs: false,
  emits: {
    'update:height': (height: number) => true,
  },
  setup(props, { emit }) {
    const { resizeRef, contentRect } = useResizeObserver(undefined, 'border')

    watch(
      () => contentRect.value?.height,
      (height) => {
        if (height != null) emit('update:height', height)
      }
    )

    return {
      resizeRef,
    }
  },
})
</script>

<template>
  <template v-if="$props.renderless">
    <slot v-bind="{ itemRef: resizeRef }" />
  </template>
  <template v-else>
    <div
      ref="resizeRef"
      :class="['base-virtual-scroll__item', $props.class]"
      :style="$props.style"
      v-bind="{ ...$attrs }"
    >
      <slot />
    </div>
  </template>
</template>
