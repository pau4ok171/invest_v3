<script lang="ts">
// Styles
import './BaseButtonGroup.scss'

// Composables
import { useBorder, useBorderProps } from '@/apps/visagiste/composables/border'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import {
  useElevation,
  useElevationProps,
} from '@/apps/visagiste/composables/elevation'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useVariantProps } from '@/apps/visagiste/composables/variant'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'

// Utilities
import { defineComponent, h, toRef } from 'vue'
import { propsFactory } from '@/apps/visagiste/utils'

export const useBaseButtonGroupProps = propsFactory(
  {
    baseColor: String,
    divided: Boolean,

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useElevationProps(),
    ...useRoundedProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps(),
  },
  'BaseButtonGroup'
)

export default defineComponent({
  name: 'BaseButtonGroup',
  props: useBaseButtonGroupProps(),
  setup(props, { slots }) {
    const { themeClasses } = provideTheme(props)
    const { densityClasses } = useDensity(props)
    const { borderClasses } = useBorder(props)
    const { elevationClasses } = useElevation(props)
    const { roundedClasses } = useRounded(props)

    provideDefaults({
      BaseButton: {
        height: 'auto',
        baseColor: toRef(props, 'baseColor'),
        color: toRef(props, 'color'),
        density: toRef(props, 'density'),
        flat: true,
        variant: toRef(props, 'variant'),
      },
    })

    return () =>
      h(
        props.tag,
        {
          class: [
            'base-button-group',
            { 'base-button-group--divided': props.divided },
            themeClasses.value,
            borderClasses.value,
            densityClasses.value,
            elevationClasses.value,
            roundedClasses.value,
            props.class,
          ],
          style: props.style,
        },
        {
          default: () => slots.default?.(),
        }
      )
  },
})
</script>
