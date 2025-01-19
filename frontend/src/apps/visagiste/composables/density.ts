// Utilities

// Types
import type { PropType } from "vue";
import {getCurrentInstanceName} from "@/apps/visagiste/utils";
import {computed} from "vue";

const allowedDensities = [null, 'default', 'comfortable', 'compact'] as const

export type Density = typeof allowedDensities[number]

export interface DensityProps {
  density?: Density
}

// Composables
export const densityProps = {
  density: {
    type: String as PropType<Density>,
    default: 'default',
    validator: (v: any) => allowedDensities.includes(v),
  }
}

export function useDensity (
  props: DensityProps,
  name = getCurrentInstanceName(),
) {
  const densityClasses = computed(() => {
    return `${name}--density-${props.density}`
  })

  return { densityClasses }
}