<script lang="ts">
// Styles
import './BaseCard.scss'

// Components
import { default as BaseCardActions } from './BaseCardActions.vue'
import { default as BaseCardItem } from './BaseCardItem.vue'
import { default as BaseCardText } from './BaseCardText.vue'
import { BaseDefaultsProvider } from '@/apps/visagiste/components/BaseDefaultsProvider'
import { BaseImage } from '@/apps/visagiste/components/BaseImage'

// Composables
import { useBorder, useBorderProps } from '@/apps/visagiste/composables/border'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import {
  useDimension,
  useDimensionProps,
} from '@/apps/visagiste/composables/dimensions'
import {
  useElevation,
  useElevationProps,
} from '@/apps/visagiste/composables/elevation'
import {
  default as LoaderSlot,
  useLoader,
  useLoaderProps,
} from '@/apps/visagiste/composablesV2/loader.vue'
import {
  useLocation,
  useLocationProps,
} from '@/apps/visagiste/composables/location'
import {
  usePosition,
  usePositionProps,
} from '@/apps/visagiste/composables/position'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { useLink, useRouterProps } from '@/apps/visagiste/composables/router'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import {
  genOverlays,
  useVariant,
  useVariantProps,
} from '@/apps/visagiste/composables/variant'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Directives
import { Ripple } from '@/apps/visagiste/directives/ripple'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType, SlotsType } from 'vue'
import type { RippleDirectiveBinding } from '@/apps/visagiste/directives/ripple'
import type { BaseCardItemSlots } from '@/apps/visagiste/components/BaseCard/BaseCardItem.vue'
import type { LoaderSlotProps } from '@/apps/visagiste/composablesV2/loader.vue'

export const useBaseCardProps = propsFactory(
  {
    appendAvatar: String,
    appendIcon: IconValue,
    disabled: Boolean,
    flat: Boolean,
    hover: Boolean,
    image: String,
    link: {
      type: Boolean,
      default: undefined,
    },
    prependAvatar: String,
    prependIcon: IconValue,
    ripple: {
      type: [Boolean, Object] as PropType<RippleDirectiveBinding['value']>,
      default: true,
    },
    subtitle: [String, Number],
    text: [String, Number],
    title: [String, Number],

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useDimensionProps(),
    ...useElevationProps(),
    ...useLoaderProps(),
    ...useLocationProps(),
    ...usePositionProps(),
    ...useRoundedProps(),
    ...useRouterProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'elevated' } as const),
  },
  'BaseCard'
)

export type BaseCardSlots = BaseCardItemSlots & {
  default: never
  actions: never
  text: never
  loader: LoaderSlotProps
  image: never
  item: never
}

export default defineComponent({
  name: 'BaseCard',
  components: {
    LoaderSlot,
    BaseCardText,
    BaseCardItem,
    BaseDefaultsProvider,
    BaseImage,
    BaseCardActions,
  },
  methods: {
    genOverlays,
  },
  directives: {
    Ripple,
  },
  props: useBaseCardProps(),
  slots: Object as SlotsType<BaseCardSlots>,
  setup(props, { attrs }) {
    const { themeClasses } = provideTheme(props)
    const { borderClasses } = useBorder(props)
    const { colorClasses, colorStyles, variantClasses } = useVariant(props)
    const { densityClasses } = useDensity(props)
    const { dimensionStyles } = useDimension(props)
    const { elevationClasses } = useElevation(props)
    const { loaderClasses } = useLoader(props)
    const { locationStyles } = useLocation(props)
    const { positionClasses } = usePosition(props)
    const { roundedClasses } = useRounded(props)
    const link = useLink(props, attrs)

    const isLink = computed(() => props.link !== false && link.isLink.value)
    const isClickable = computed(
      () =>
        !props.disabled &&
        props.link !== false &&
        (props.link || link.isClickable.value)
    )

    const Tag = computed(() => (isLink.value ? 'a' : props.tag))

    const titleIsEmpty = useSlotIsEmpty('title')
    const subtitleIsEmpty = useSlotIsEmpty('subtitle')
    const appendIsEmpty = useSlotIsEmpty('append')
    const prependIsEmpty = useSlotIsEmpty('prepend')
    const imageIsEmpty = useSlotIsEmpty('image')
    const textIsEmpty = useSlotIsEmpty('text')

    const hasTitle = computed(() => !titleIsEmpty.value || props.title != null)
    const hasSubtitle = computed(
      () => !subtitleIsEmpty.value || props.subtitle != null
    )
    const hasHeader = computed(() => hasTitle.value || hasSubtitle.value)
    const hasAppend = computed(
      () => !!(!appendIsEmpty.value || props.appendAvatar || props.appendIcon)
    )
    const hasPrepend = computed(
      () =>
        !!(!prependIsEmpty.value || props.prependAvatar || props.prependIcon)
    )
    const hasImage = computed(() => !!(!imageIsEmpty.value || props.image))
    const hasCardItem = computed(
      () => hasHeader.value || hasPrepend.value || hasAppend.value
    )
    const hasText = computed(() => !textIsEmpty.value || props.text != null)

    return {
      themeClasses,
      borderClasses,
      colorClasses,
      colorStyles,
      variantClasses,
      densityClasses,
      dimensionStyles,
      elevationClasses,
      loaderClasses,
      locationStyles,
      positionClasses,
      roundedClasses,
      link,
      isLink,
      isClickable,
      Tag,
      hasTitle,
      hasSubtitle,
      hasHeader,
      hasAppend,
      hasPrepend,
      hasImage,
      hasCardItem,
      hasText,
    }
  },
})
</script>

<template>
  <component
    :is="Tag"
    :class="[
      'base-card',
      {
        'base-card-disabled': $props.disabled,
        'base-card--flat': $props.flat,
        'base-card--hover': $props.hover && !($props.disabled || $props.flat),
        'base-card--link': isClickable,
      },
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      loaderClasses,
      positionClasses,
      roundedClasses,
      variantClasses,
      $props.class,
    ]"
    :style="[colorStyles, dimensionStyles, locationStyles, $props.style]"
    @click="isClickable && link.navigate"
    v-ripple="isClickable && $props.ripple"
    :tabindex="$props.disabled ? -1 : undefined"
    v-bind="{ ...link.linkProps }"
  >
    <template v-if="hasImage">
      <div key="image" class="base-card__image">
        <template v-if="!$slots.image">
          <BaseImage key="image-defaults" cover :src="$props.image" />
        </template>

        <template v-else>
          <BaseDefaultsProvider
            key="image-defaults"
            :disabled="!$props.image"
            :defaults="{
              BaseImage: {
                cover: true,
                src: $props.image,
              },
            }"
          >
            <slot name="image" />
          </BaseDefaultsProvider>
        </template>
      </div>
    </template>

    <LoaderSlot
      name="base-card"
      :active="!!$props.loading"
      :color="typeof $props.loading === 'boolean' ? undefined : $props.loading"
    >
      <slot name="loader" />
    </LoaderSlot>

    <template v-if="hasCardItem">
      <BaseCardItem
        key="item"
        :prepend-avatar="$props.prependAvatar"
        :prepend-icon="$props.prependIcon"
        :title="$props.title"
        :subtitle="$props.subtitle"
        :append-avatar="$props.appendAvatar"
        :append-icon="$props.appendIcon"
      >
        <template #default><slot name="item" /></template>
        <template #prepend><slot name="prepend" /></template>
        <template #title><slot name="title" /></template>
        <template #subtitle><slot name="subtitle" /></template>
        <template #append><slot name="append" /></template>
      </BaseCardItem>
    </template>

    <template v-if="hasText">
      <BaseCardText key="text">
        <slot name="text">{{ $props.text }}</slot>
      </BaseCardText>
    </template>

    <slot name="default" />

    <template v-if="$slots.actions">
      <BaseCardActions>
        <slot name="actions" />
      </BaseCardActions>
    </template>

    <component :is="genOverlays(isClickable, 'base-card')" />
  </component>
</template>
