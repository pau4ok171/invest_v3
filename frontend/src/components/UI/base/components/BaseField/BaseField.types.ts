import type {Ref} from "vue";

export const allowedVariants = ['filled', 'outlined', 'plain', 'solo', 'solo-filled', 'solo-inverted', 'solo-lined'] as const
export type Variant = typeof allowedVariants[number]

export interface DefaultInputSlot {
  isActive: Ref<boolean>
  isFocused: Ref<boolean>
  controlRef: Ref<HTMLElement | undefined>
  focus: () => void,
  blur: () => void,
}

export interface BaseFieldSlot extends DefaultInputSlot {
  props: Record<string, unknown>
}

export type BaseFieldSlots = {
  clear: DefaultInputSlot & { props: Record<string, any> }
  'prepend-inner': DefaultInputSlot
  'append-inner': DefaultInputSlot
  label: DefaultInputSlot & { label: string | undefined, props: Record<string, any> }
  default: BaseFieldSlot
}