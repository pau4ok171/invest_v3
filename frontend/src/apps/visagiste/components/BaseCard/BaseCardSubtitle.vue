<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { h } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseCardSubtitleProps = propsFactory(
  {
    opacity: [Number, String],

    ...useComponentProps(),
    ...useTagProps(),
  },
  'BaseCardSubtitle'
)

export default defineComponent({
  name: 'BaseCardSubtitle',
  props: useBaseCardSubtitleProps(),
  setup(props, { slots }) {
    return () =>
      h(
        props.tag,
        {
          class: ['base-card-subtitle', props.class],
          style: [
            { '--base-card-subtitle-opacity': props.opacity },
            props.style,
          ],
        },
        slots.default?.()
      )
  },
})
</script>
