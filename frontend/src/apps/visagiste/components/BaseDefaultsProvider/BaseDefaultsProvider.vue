<script lang="ts">
// Composables
import { provideDefaults } from '@/apps/visagiste/composables/defaults'

// Utilities
import { toRefs } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { DefaultsOptions } from '@/apps/visagiste/composables/defaults'

export const useBaseDefaultsProviderProps = propsFactory(
  {
    defaults: Object as PropType<DefaultsOptions>,
    disabled: Boolean,
    reset: [Number, String],
    root: [Boolean, String],
    scoped: Boolean,
  },
  'BaseDefaultsProvider'
)

export default defineComponent({
  name: 'BaseDefaultsProvider',
  props: useBaseDefaultsProviderProps(),
  setup(props, { slots }) {
    const { defaults, disabled, reset, root, scoped } = toRefs(props)

    provideDefaults(defaults, {
      reset,
      root,
      scoped,
      disabled,
    })

    return () => slots.default?.()
  },
})
</script>
