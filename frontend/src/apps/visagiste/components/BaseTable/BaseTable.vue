<script lang="ts">
// Styles
import './BaseTable.scss';

// Composables
import { useThemeProps, provideTheme } from "@/apps/visagiste/composables/theme";
import { useDensityProps, useDensity } from "@/apps/visagiste/composables/density";

// Utilities
import { defineComponent } from "vue";
import {convertToUnit} from "@/apps/visagiste/utils";

export default defineComponent({
  name: 'BaseTable',
  props: {
    fixedHeader: Boolean,
    fixedFooter: Boolean,
    height: [Number, String],
    hover: Boolean,
    ...useThemeProps(),
    ...useDensityProps(),
  },
  methods: {
    convertToUnit
  },
  setup(props) {
    const { themeClasses } = provideTheme(props)
    const { densityClasses } = useDensity(props)

    return {
      themeClasses,
      densityClasses,
    }
  },
})

</script>

<template>
<div
  :class="[
    'base-table',
    {
      'base-table--fixed-height': height,
      'base-table--fixed-header': fixedHeader,
      'base-table--fixed-footer': fixedFooter,
      'base-table--has-top': $slots.top,
      'base-table--has-bottom': $slots.bottom,
      'base-table--hover': hover,
    },
    themeClasses,
    densityClasses,
  ]"
>
  <slot name="top"/>

  <template v-if="$slots.default">
    <div
      class="base-table__wrapper"
      :style="{height: convertToUnit(height)}"
    >
      <table>
        <slot/>
      </table>
    </div>
  </template>

  <template v-else>
    <slot name="wrapper"/>
  </template>

  <slot name="bottom"/>
</div>
</template>
