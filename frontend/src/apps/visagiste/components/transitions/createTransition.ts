// Utilities
import {defineComponent, h, Transition, TransitionGroup} from "vue";

// Types
import type { PropType, FunctionalComponent } from 'vue';


export function createJavascriptTransition (
  name: string,
  functions: Record<string, any>,
  mode?: string
) {
  return defineComponent({
    name,
    props: {
      mode: {
        type: String as PropType<'in-out' | 'out-in' | 'default'>,
        default: mode,
      },
      disabled: Boolean,
      group: Boolean,
    },

    setup(props, { slots }) {
      const tag = props.group ? TransitionGroup : Transition
      
      return () => {
        return h(tag as FunctionalComponent, {
          name: props.disabled ? '' : name,
          css: !props.disabled,
          // mode: props.mode, TODO: vuejs/vue-next#3104
          ...(props.disabled ? {} : functions),
        }, slots.default)
      }
    },
  })
}
