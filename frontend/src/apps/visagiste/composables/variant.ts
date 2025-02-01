// Composables
import {useColor} from "@/apps/visagiste/composables/color";

// Utilities
import {computed, Fragment, h, unref} from "vue";
import {getCurrentInstanceName, propsFactory} from "@/apps/visagiste/utils";

// Types
import type { MaybeRef, PropType } from 'vue';

export const allowedVariants = [
  'elevated',
  'flat',
  'tonal',
  'outlined',
  'text',
  'plain'
] as const
export type Variant = typeof allowedVariants[number]

export interface VariantProps {
  color?: string
  variant: Variant
}

export function genOverlays (isClickable: boolean, name: string) {
  return () => {
    return h(Fragment, null, [
      isClickable ?
      h('span', {
        key: 'overlay',
        class: `${name}__overlay`
      }) : null,
      h('span', {
        key: 'underlay',
        class: `${name}__underlay`
      })
    ])
  }
}

export const useVariantProps = propsFactory({
  color: String,
  variant: {
    type: String as PropType<Variant>,
    default: 'elevated',
    validator: (v: any) => allowedVariants.includes(v),
  }
}, 'variant')

export function useVariant (
  props: MaybeRef<VariantProps>,
  name = getCurrentInstanceName(),
) {
  const variantClasses = computed(() => {
    const { variant } = unref(props)
    return `${name}--variant-${variant}`
  })

  const { colorClasses, colorStyles } = useColor(computed(() => {
    const { variant, color } = unref(props)
    return {
      [['elevated', 'flat'].includes(variant) ? 'background' : 'text']: color,
    }
  }))

  return { colorClasses, colorStyles, variantClasses }
}