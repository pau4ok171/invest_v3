<script lang="ts">
// Styles
import './BaseResponsive.scss'

// Composables
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {useDimension, useDimensionProps} from "@/apps/visagiste/composables/dimensions";

// Utilities
import { computed } from "vue";
import {defineComponent, propsFactory} from "@/apps/visagiste/utils";

export type BaseResponsiveSlots = {
  default: never
  additional: never
}

export function useAspectStyles (props: { aspectRatio?: string | number }) {
  return {
    aspectStyles: computed(() => {
      const ratio = Number(props.aspectRatio)

      return ratio
        ? { paddingBottom: String(1 / ratio * 100) + '%' }
        : undefined
    }),
  }
}

export const useBaseResponsiveProps = propsFactory({
  aspectRatio: [String, Number],
  contentClass: null,
  inline: Boolean,

  ...useComponentProps(),
  ...useDimensionProps(),
}, 'BaseResponsive')

export default defineComponent({
  name: 'BaseResponsive',
  props: useBaseResponsiveProps(),
  setup (props) {
    const { aspectStyles } = useAspectStyles(props)
    const { dimensionStyles } = useDimension(props)

    return {
      aspectStyles,
      dimensionStyles,
    }
  },
})

</script>

<template>
<div
  :class="[
    'base-responsive',
    {
      'base-responsive--inline': $props.inline,
    },
    $props.class,
  ]"
  :style="[
    dimensionStyles,
    $props.style
  ]"
>

  <div class="base-responsive__sizer" :style="aspectStyles"/>

  <slot name="additional"/>

  <div v-if="$slots.default" :class="['base-responsive__content', $props.contentClass]"><slot name="default"/></div>

</div>
</template>
