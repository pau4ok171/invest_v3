<script lang="ts">
// Styles
import './BaseAvatar.scss'

// Components
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import BaseImage from '@/apps/visagiste/components/BaseImage/BaseImage.vue'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'

// Composables
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useBorder, useBorderProps } from '@/apps/visagiste/composables/border'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { useSize, useSizeProps } from '@/apps/visagiste/composables/size'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import {
  useVariant,
  useVariantProps,
  genOverlays,
} from '@/apps/visagiste/composables/variant'

// Utilities
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseAvatarProps = propsFactory(
  {
    start: Boolean,
    end: Boolean,
    icon: IconValue,
    image: String,
    text: String,

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useRoundedProps(),
    ...useSizeProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'flat' } as const),
  },
  'BaseAvatar'
)

export default defineComponent({
  name: 'BaseAvatar',
  methods: { genOverlays },
  components: { BaseDefaultsProvider, BaseIcon, BaseImage },
  props: useBaseAvatarProps(),
  setup(props) {
    const { themeClasses } = provideTheme(props)
    const { borderClasses } = useBorder(props)
    const { colorClasses, colorStyles, variantClasses } = useVariant(props)
    const { densityClasses } = useDensity(props)
    const { roundedClasses } = useRounded(props)
    const { sizeClasses, sizeStyles } = useSize(props)

    return {
      themeClasses,
      borderClasses,
      colorClasses,
      colorStyles,
      variantClasses,
      densityClasses,
      roundedClasses,
      sizeClasses,
      sizeStyles,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag"
    :class="[
      'base-avatar',
      {
        'base-avatar--start': $props.start,
        'base-avatar--end': $props.end,
      },
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      roundedClasses,
      sizeClasses,
      variantClasses,
      $props.class,
    ]"
    :style="[colorStyles, sizeStyles, $props.style]"
  >
    <BaseDefaultsProvider
      v-if="$slots.default"
      key="content-defaults"
      :defaults="{
        BaseImage: {
          cover: true,
          src: $props.image,
        },
        BaseIcon: {
          icon: $props.icon,
        },
      }"
    >
      <slot />
    </BaseDefaultsProvider>

    <template v-else>
      <BaseImage
        v-if="$props.image"
        key="image"
        :src="$props.image"
        alt=""
        cover
      />

      <BaseIcon v-else key="icon" :icon="$props.icon" />
    </template>

    <component :is="genOverlays(false, 'base-avatar')" />
  </component>
</template>
