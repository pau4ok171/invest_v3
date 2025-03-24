// Utilities

// Types
import type { PropType } from "vue";
import {getCurrentInstanceName, propsFactory} from "@/apps/visagiste/utils";
import {computed} from "vue";

const allowedDensities = [null, 'default', 'comfortable', 'compact'] as const

export type Density = typeof allowedDensities[number]

export interface DensityProps {
  density?: Density
}

// Composables
export const useDensityProps = propsFactory({
  density: {
    type: String as PropType<Density>,
    default: 'default',
    validator: (v: any) => allowedDensities.includes(v),
  }
}, 'density')

export function useDensity (
  props: DensityProps,
  name = getCurrentInstanceName(),
) {
  const densityClasses = computed(() => {
    return `${name}--density-${props.density}`
  })

  return { densityClasses }
}