<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { h } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseListItemActionProps = propsFactory(
  {
    start: Boolean,
    end: Boolean,

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseListAction'
)

export default defineComponent({
  name: 'BaseListItemAction',
  props: useBaseListItemActionProps(),
  setup(props, { slots }) {
    return () =>
      h(
        props.tag,
        {
          class: [
            'base-list-item-action',
            {
              'base-list-item-action--start': props.start,
              'base-list-item-action--end': props.end,
            },
            props.class,
          ],
          style: props.style,
        },
        slots.default
      )
  },
})
</script>
