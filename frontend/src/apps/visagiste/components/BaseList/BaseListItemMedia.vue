<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { h } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseListItemMediaProps = propsFactory(
  {
    start: Boolean,
    end: Boolean,

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseListItemMedia'
)

export default defineComponent({
  name: 'BaseListItemMedia',
  props: useBaseListItemMediaProps(),
  setup(props, { slots }) {
    return () =>
      h(
        props.tag,
        {
          class: [
            'base-list-item-media',
            {
              'base-list-item-media--start': props.start,
              'base-list-item-media--end': props.end,
            },
            props.class,
          ],
          style: props.style,
        },
        slots.default?.()
      )
  },
})
</script>
