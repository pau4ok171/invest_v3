<script lang="ts">
// Utilities
import { h } from 'vue'
import { convertToUnit, defineComponent } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'

export default defineComponent({
  name: 'BaseDataTableColumn',
  methods: { convertToUnit },
  props: {
    align: {
      type: String as PropType<'start' | 'center' | 'end'>,
      default: 'start',
    },
    fixed: Boolean,
    fixedOffset: [Number, String],
    height: [Number, String],
    lastFixed: Boolean,
    noPadding: Boolean,
    tag: String,
    width: [Number, String],
    maxWidth: [Number, String],
    nowrap: Boolean,
  },
  setup(props, { slots }) {
    const Tag = props.tag ?? 'td'

    return () =>
      h(
        Tag,
        {
          class: [
            'base-data-table__td',
            {
              'base-data-table-column--fixed': props.fixed,
              'base-data-table-column--last-fixed': props.lastFixed,
              'base-data-table-column--no-padding': props.noPadding,
              'base-data-table-column--nowrap': props.nowrap,
            },
            `base-data-table-column--align-${props.align}`,
          ],
          style: {
            height: convertToUnit(props.height),
            width: convertToUnit(props.width),
            maxWidth: convertToUnit(props.maxWidth),
            left: convertToUnit(props.fixedOffset || null),
          },
        },
        {
          default: () => slots.default?.(),
        }
      )
  },
})
</script>
