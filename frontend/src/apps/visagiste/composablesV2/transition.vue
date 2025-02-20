<script lang="ts">
// Utilities
import {defineComponent, Transition, TransitionGroup, mergeProps, h} from "vue";
import {propsFactory} from "@/apps/visagiste/utils";

// Types
import type {Component, PropType, TransitionProps} from "vue";

export const useTransitionProps = propsFactory({
	transition: {
		type: [Boolean, String, Object] as PropType<string | boolean | TransitionProps & { component?: Component }>,
		default: 'fade-transition',
		validator: value => value !== true,
	},
}, 'transition')

export default defineComponent({
  name: 'MaybeTransition',
  props: {
    disabled: Boolean,
    group: Boolean,

    ...useTransitionProps(),
  },
  setup (props, { slots }) {
    const { transition, disabled, group, ...rest } = props

    const {
      component = group ? TransitionGroup : Transition,
      ...customProps
    } = typeof transition === 'object' ? transition : {}

    const transitionProps = mergeProps(
      typeof transition === 'string'
        ? { name: disabled ? '' : transition }
        : customProps as any,
      typeof transition === 'string'
        ? {}
        : Object.fromEntries(Object.entries({ disabled, group }).filter(([_, v]) => v !== undefined)),
      rest as any,
    )

    return () => h(
      component,
      {...transitionProps},
      {
        default: () => slots.default?.()
      }
    )
  }
})
</script>
