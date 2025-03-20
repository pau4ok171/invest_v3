<script lang="ts">
// Styles
import './BaseButtonToggle.scss'

// Components
import BaseButtonGroup, {
  useBaseButtonGroupProps,
} from '../BaseButtonGroup/BaseButtonGroup.vue'

// Composables
import { useGroup, useGroupProps } from '@/apps/visagiste/composables/group'

// Utilities
import { h } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { InjectionKey } from 'vue'
import type { GroupProvide } from '@/apps/visagiste/composables/group'

export type ButtonToggleSlotProps =
  | 'isSelected'
  | 'select'
  | 'selected'
  | 'next'
  | 'prev'
export interface DefaultButtonToggleSlot
  extends Pick<GroupProvide, ButtonToggleSlotProps> {}

export const BaseButtonToggleSymbol: InjectionKey<GroupProvide> = Symbol.for(
  'visagiste:base-button-toggle'
)

type BaseButtonToggleSlots = {
  default: DefaultButtonToggleSlot
}

export const useBaseButtonToggleProps = propsFactory(
  {
    ...useBaseButtonGroupProps(),
    ...useGroupProps(),
  },
  'BaseButtonToggle'
)

export default defineComponent({
  name: 'BaseButtonToggle',
  props: useBaseButtonToggleProps(),
  setup(props, { slots, expose }) {
    const { isSelected, next, prev, select, selected } = useGroup(
      props,
      BaseButtonToggleSymbol
    )

    expose({
      next,
      prev,
      select,
    })

    return () => {
      const buttonGroupProps = BaseButtonGroup.filterProps(props)

      return h(
        BaseButtonGroup,
        {
          class: ['base-button-toggle', props.class],
          ...buttonGroupProps,
          style: props.style,
        },
        {
          default: () =>
            slots.default?.({ isSelected, next, prev, select, selected }),
        }
      )
    }
  },
})
</script>
