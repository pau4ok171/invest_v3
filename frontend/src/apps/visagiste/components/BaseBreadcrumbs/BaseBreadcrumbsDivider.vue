<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'

// Utilities
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

const useBaseBreadcrumbsDividerProps = propsFactory(
  {
    divider: [Number, String],

    ...useComponentProps(),
  },
  'BaseBreadcrumbsDivider'
)

export default defineComponent({
  name: 'BaseBreadcrumbsDivider',
  props: useBaseBreadcrumbsDividerProps(),
})
</script>

<template>
  <li
    aria-hidden="true"
    :class="['base-breadcrumbs-divider', $props.divider]"
    :style="[$props.style]"
  >
    <slot name="divider">
      {{ $props.divider }}
    </slot>
  </li>
</template>
