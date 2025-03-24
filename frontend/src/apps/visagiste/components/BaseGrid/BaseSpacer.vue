<script lang="ts">
// Styles
import './BaseGrid.scss'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'

// Utilities
import { h } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseSpacerProps = propsFactory(
  {
    tag: {
      type: String,
      default: 'div',
    },

    ...useComponentProps(),
  },
  'BaseSpacer'
)

export default defineComponent({
  name: 'BaseSpacer',
  props: useBaseSpacerProps(),
  setup(props, { slots }) {
    return () => {
      return h(
        props.tag,
        {
          class: ['base-spacer', props.class],
          style: props.style,
        },
        slots.default?.()
      )
    }
  },
})
</script>
