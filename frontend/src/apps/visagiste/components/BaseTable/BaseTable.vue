<script lang="ts">
// Styles
import './BaseTable.scss'

// Composables
import { useThemeProps, provideTheme } from '@/apps/visagiste/composables/theme'
import {
  useDensityProps,
  useDensity,
} from '@/apps/visagiste/composables/density'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from '@/apps/visagiste/utils'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'
import { computed } from 'vue'

export type BaseTableSlots = {
  default: never
  top: never
  bottom: never
  wrapper: never
}

export const useBaseTableProps = propsFactory(
  {
    fixedHeader: Boolean,
    fixedFooter: Boolean,
    height: [Number, String],
    hover: Boolean,

    ...useComponentProps(),
    ...useDensityProps(),
    ...useTagProps(),
    ...useThemeProps(),
  },
  'BaseTable'
)

export default defineComponent({
  name: 'BaseTable',
  props: useBaseTableProps(),
  methods: {
    convertToUnit,
  },
  setup(props) {
    const { themeClasses } = provideTheme(props)
    const { densityClasses } = useDensity(props)

    const topIsEmpty = useSlotIsEmpty('top')
    const bottomIsEmpty = useSlotIsEmpty('bottom')

    const hasTop = computed(() => !topIsEmpty.value)
    const hasBottom = computed(() => !bottomIsEmpty.value)

    return {
      themeClasses,
      densityClasses,
      hasTop,
      hasBottom,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-table',
      {
        'base-table--fixed-height': !!$props.height,
        'base-table--fixed-header': $props.fixedHeader,
        'base-table--fixed-footer': $props.fixedFooter,
        'base-table--has-top': hasTop,
        'base-table--has-bottom': hasBottom,
        'base-table--hover': $props.hover,
      },
      themeClasses,
      densityClasses,
      $props.class,
    ]"
    :style="$props.style"
  >
    <slot name="top" />

    <template v-if="$slots.default">
      <div
        class="base-table__wrapper"
        :style="{ height: convertToUnit($props.height) }"
      >
        <table>
          <slot />
        </table>
      </div>
    </template>

    <template v-else>
      <slot name="wrapper" />
    </template>

    <slot name="bottom" />
  </component>
</template>
