<script lang="ts">
// Styles
import './BaseGrid.scss'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { useRtl } from '@/apps/visagiste/composables'

//Utilities
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseContainerProps = propsFactory(
  {
    fluid: {
      type: Boolean,
      default: false,
    },

    ...useComponentProps(),
    ...useDimensionProps(),
    ...useTagProps(),
  },
  'BaseContainer'
)

export default defineComponent({
  name: 'BaseContainer',
  props: useBaseContainerProps(),
  setup(props) {
    const { rtlClasses } = useRtl()
    const { dimensionStyles } = useDimension(props)

    return {
      rtlClasses,
      dimensionStyles,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-container',
      { 'base-container--fluid': $props.fluid },
      rtlClasses,
      $props.class,
    ]"
    :style="[dimensionStyles, $props.style]"
  >
    <slot />
  </component>
</template>
