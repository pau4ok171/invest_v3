<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'

// Utilities
import { h } from 'vue'
import { defineComponent } from '@/apps/visagiste/utils'

export default defineComponent({
  name: 'BaseListImage',
  props: {
    ...useComponentProps(),
  },
  setup(props, { slots }) {
    return () => {
      return h(
        'div',
        {
          class: ['base-list-image', props.class],
          style: props.style,
        },
        slots.default?.()
      )
    }
  },
})
</script>
