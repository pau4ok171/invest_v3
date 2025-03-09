<script lang="ts">
// Styles
import './BaseDivider.scss'

// Composables
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'

// Utilities
import { computed, toRef } from 'vue'
import { useTextColor } from '@/apps/visagiste/composables/color'
import { convertToUnit, defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
type DividerKey = 'borderRightWidth' | 'borderTopWidth' | 'height' | 'width'
type DividerStyles = Partial<Record<DividerKey, string>>

export const useBaseDividerProps = propsFactory(
  {
    color: String,
    inset: Boolean,
    length: [Number, String],
    opacity: [Number, String],
    thickness: [Number, String],
    vertical: [Boolean],

    ...useThemeProps(),
  },
  'BaseDivider'
)

// Component
export default defineComponent({
  name: 'BaseDivider',
  props: useBaseDividerProps(),
  setup(props) {
    const { themeClasses } = provideTheme(props)
    const { textColorClasses, textColorStyles } = useTextColor(
      toRef(props, 'color')
    )
    const dividerStyles = computed(() => {
      const styles: DividerStyles = {}

      if (props.length) {
        styles[props.vertical ? 'height' : 'width'] = convertToUnit(
          props.length
        )
      }

      if (props.thickness) {
        styles[props.vertical ? 'borderRightWidth' : 'borderTopWidth'] =
          convertToUnit(props.thickness)
      }

      return styles
    })

    return {
      themeClasses,
      textColorClasses,
      textColorStyles,
      dividerStyles,
    }
  },
})
</script>

<template>
  <template v-if="!$slots.default">
    <hr
      :class="[
        'base-divider',
        {
          'base-divider--vertical': vertical,
          'base-divider--inset': inset,
        },
        themeClasses,
        textColorClasses,
      ]"
      :style="[
        dividerStyles,
        textColorStyles,
        { '--base-border-opacity': opacity },
      ]"
      :aria-orientation="
        !$attrs.role || $attrs.role === 'separator'
          ? vertical
            ? 'vertical'
            : 'horizontal'
          : undefined
      "
      :role="`${$attrs.role || 'separator'}`"
    />
  </template>

  <template v-else>
    <div
      :class="[
        'base-divider__wrapper',
        {
          'base-divider__wrapper--vertical': vertical,
          'base-divider__wrapper--inset': inset,
        },
      ]"
    >
      <hr
        :class="[
          'base-divider',
          {
            'base-divider--vertical': vertical,
            'base-divider--inset': inset,
          },
          themeClasses,
          textColorClasses,
        ]"
        :style="[
          dividerStyles,
          textColorStyles,
          { '--base-border-opacity': opacity },
        ]"
        :aria-orientation="
          !$attrs.role || $attrs.role === 'separator'
            ? vertical
              ? 'vertical'
              : 'horizontal'
            : undefined
        "
        :role="`${$attrs.role || 'separator'}`"
      />

      <div class="base-divider__content">
        <slot />
      </div>

      <hr
        :class="[
          'base-divider',
          {
            'base-divider--vertical': vertical,
            'base-divider--inset': inset,
          },
          themeClasses,
          textColorClasses,
        ]"
        :style="[
          dividerStyles,
          textColorStyles,
          { '--base-border-opacity': opacity },
        ]"
        :aria-orientation="
          !$attrs.role || $attrs.role === 'separator'
            ? vertical
              ? 'vertical'
              : 'horizontal'
            : undefined
        "
        :role="`${$attrs.role || 'separator'}`"
      />
    </div>
  </template>
</template>
