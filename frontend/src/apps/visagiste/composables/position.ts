// Utilities
import {computed} from "vue";
import {getCurrentInstanceName, propsFactory} from "@/apps/visagiste/utils";

// Types
import type {PropType} from "vue";

const positionValues = ['static', 'relative', 'fixed', 'absolute', 'sticky'] as const

type Position = typeof positionValues[number]

export interface PositionProps {
  position: Position | undefined
}

// Composables
export const usePositionProps = propsFactory({
  position: {
    type: String as PropType<Position>,
    validator: (v: any) => positionValues.includes(v),
  },
}, 'position')

export function usePosition (
  props: PositionProps,
  name = getCurrentInstanceName(),
) {
  const positionClasses = computed(() => {
    return props.position ? `${name}--${props.position}` : undefined
  })

  return { positionClasses }
}