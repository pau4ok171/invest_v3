// Utilities
import {propsFactory} from "@/apps/visagiste/utils";


// Types
import type {PropType, StyleValue} from "vue";

export type ClassValue = any

export interface ComponentProps {
  class: ClassValue
  style: StyleValue | undefined
}

// Composables
export const useComponentProps = propsFactory({
  class: [String, Array, Object] as PropType<ClassValue>,
  style: {
    type: [String, Array, Object] as PropType<StyleValue>,
    default: null,
  },
}, 'component')
