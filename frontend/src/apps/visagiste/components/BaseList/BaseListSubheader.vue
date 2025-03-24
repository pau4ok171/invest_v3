<script lang="ts">
// Composables
import { useTextColor } from '@/apps/visagiste/composables/color'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { h, toRef } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseListSubheaderProps = propsFactory(
  {
    color: String,
    inset: Boolean,
    sticky: Boolean,
    title: String,

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseListSubheader'
)

export default defineComponent({
  name: 'BaseListSubheader',
  props: useBaseListSubheaderProps(),
  setup(props, { slots }) {
    const { textColorClasses, textColorStyles } = useTextColor(
      toRef(props, 'color')
    )
    return () => {
      const hasText = !!(slots.default || props.title)

      return h(
        props.tag,
        {
          class: [
            'base-list-subheader',
            {
              'base-list-subheader--inset': props.inset,
              'base-list-subheader--sticky': props.sticky,
            },
            textColorClasses.value,
            props.class,
          ],
          style: [textColorStyles.value, props.style],
        },
        {
          default: () => [
            hasText
              ? h(
                  'div',
                  { class: 'base-list-subheader__text' },
                  slots.default?.() ?? props.title
                )
              : null,
          ],
        }
      )
    }
  },
})
</script>
