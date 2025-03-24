// Utilities
import {propsFactory} from "@/apps/visagiste/utils";

// Types
import type {Ref} from "vue";
import {computed, isRef} from "vue";

type ElevationData = {
  elevationClasses: Ref<string[]>
}

export interface ElevationProps {
  elevation?: number | string | null
}

// Composables
export const useElevationProps = propsFactory({
  elevation: {
    type: [Number, String],
    validator (v: any) {
      const value = parseInt(v)
      return (
        !isNaN(value) && value >= 0 && value <= 24
      )
    }
  }
}, 'elevation')

export function useElevation (
  props: ElevationProps | Ref<number | string | undefined>
): ElevationData {
  const elevationClasses = computed(() => {
    const elevation = isRef(props) ? props.value : props.elevation
    const classes: string[] = []

    if (elevation == null) return classes

    classes.push(`elevation-${elevation}`)

    return classes
  })

  return { elevationClasses }
}