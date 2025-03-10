<script lang="ts">
// Styles
import './BaseButton.scss'

// Components
import { BaseButtonToggleSymbol } from '../BaseButtonToggle/BaseButtonToggle.vue'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import { BaseProgressCircular } from '@/apps/visagiste/components/BaseProgressCircular'

// Composables
import { IconValue } from '@/apps/visagiste/composables/icons'
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
import { useGroupItem, useGroupProps } from '@/apps/visagiste/composables/group'
import {
  useLoader,
  useLoaderProps,
} from '@/apps/visagiste/composablesV2/loader.vue'
import {
  useLocation,
  useLocationProps,
} from '@/apps/visagiste/composables/location'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { useLink, useRouterProps } from '@/apps/visagiste/composables/router'
import { useSize, useSizeProps } from '@/apps/visagiste/composables/size'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import {
  genOverlays,
  useVariant,
  useVariantProps,
} from '@/apps/visagiste/composables/variant'
import {
  usePosition,
  usePositionProps,
} from '@/apps/visagiste/composables/position'
import { useSelectLink } from '@/apps/visagiste/composables/selectLink'

// Directives
import { Ripple } from '@/apps/visagiste/directives/ripple'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { RippleDirectiveBinding } from '@/apps/visagiste/directives/ripple'

export type BaseButtonSlots = {
  default: never
  prepend: never
  append: never
  loader: never
}

export const useBaseButtonProps = propsFactory(
  {
    active: {
      type: Boolean,
      default: undefined,
    },
    activeColor: String,
    baseColor: String,
    symbol: {
      type: null,
      default: BaseButtonToggleSymbol,
    },
    flat: Boolean,
    icon: [Boolean, String, Function, Object] as PropType<boolean | IconValue>,
    prependIcon: IconValue,
    appendIcon: IconValue,

    block: Boolean,
    readonly: Boolean,
    slim: Boolean,
    stacked: Boolean,

    ripple: {
      type: [Boolean, Object] as PropType<RippleDirectiveBinding['value']>,
      default: true,
    },

    text: String,

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useDimensionProps(),
    ...useElevationProps(),
    ...useGroupProps(),
    ...useLoaderProps(),
    ...useLocationProps(),
    ...usePositionProps(),
    ...useRoundedProps(),
    ...useRouterProps(),
    ...useSizeProps(),
    ...useTagProps({ tag: 'button' }),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'elevated' } as const),
  },
  'BaseButton'
)

export default defineComponent({
  name: 'BaseButton',
  components: { BaseProgressCircular, BaseDefaultsProvider, BaseIcon },
  methods: { genOverlays },
  props: useBaseButtonProps(),
  emits: {
    'group: selected': (val: { value: boolean }) => true,
  },
  directives: {
    Ripple,
  },
  setup(props, { attrs, slots }) {
    const { themeClasses } = provideTheme(props)
    const { borderClasses } = useBorder(props)
    const { densityClasses } = useDensity(props)
    const { dimensionStyles } = useDimension(props)
    const { elevationClasses } = useElevation(props)
    const { loaderClasses } = useLoader(props)
    const { locationStyles } = useLocation(props)
    const { positionClasses } = usePosition(props)
    const { roundedClasses } = useRounded(props)
    const { sizeClasses, sizeStyles } = useSize(props)
    const group = useGroupItem(props, props.symbol, false)
    const link = useLink(props, attrs)

    const isActive = computed(() => {
      if (props.active !== undefined) {
        return props.active
      }

      if (link.isLink.value) {
        return link.isActive?.value
      }

      return group?.isSelected.value
    })

    const color = computed(() =>
      isActive.value ? (props.activeColor ?? props.color) : props.color
    )
    const variantProps = computed(() => {
      const showColor =
        (group?.isSelected.value &&
          (!link.isLink.value || link.isActive?.value)) ||
        !group ||
        link.isActive?.value
      return {
        color: showColor ? (color.value ?? props.baseColor) : props.baseColor,
        variant: props.variant,
      }
    })
    const { colorClasses, colorStyles, variantClasses } =
      useVariant(variantProps)

    const isDisabled = computed(() => group?.disabled.value || props.disabled)
    const isElevated = computed(() => {
      return (
        props.variant === 'elevated' &&
        !(props.disabled || props.flat || props.border)
      )
    })
    const valueAttr = computed(() => {
      if (props.value === undefined || typeof props.value === 'symbol')
        return undefined

      return Object(props.value) === props.value
        ? JSON.stringify(props.value, null, 0)
        : props.value
    })

    function onClick(e: MouseEvent) {
      if (
        isDisabled.value ||
        (link.isLink.value &&
          (e.metaKey ||
            e.ctrlKey ||
            e.shiftKey ||
            e.button !== 0 ||
            attrs.target === '_blank'))
      )
        return

      link.navigate?.(e)
      group?.toggle()
    }

    useSelectLink(link, group?.select)

    const Tag = computed(() => (link.isLink.value ? 'a' : props.tag))
    const hasPrepend = computed(() => !!(props.prependIcon || slots.prepend))
    const hasAppend = computed(() => !!(props.appendIcon || slots.append))
    const hasIcon = computed(() => !!(props.icon && props.icon !== true))

    const rippleConfig = computed(() => {
      if (props.icon)
        return {
          center: true,
          enabled: !isDisabled && props.ripple,
        }
      return {
        enabled: !isDisabled && props.ripple,
      }
    })

    return {
      themeClasses,
      borderClasses,
      densityClasses,
      dimensionStyles,
      elevationClasses,
      loaderClasses,
      locationStyles,
      positionClasses,
      roundedClasses,
      sizeClasses,
      sizeStyles,
      colorClasses,
      colorStyles,
      variantClasses,
      Tag,
      hasPrepend,
      hasAppend,
      hasIcon,
      isActive,
      isDisabled,
      isElevated,
      group,
      link,
      valueAttr,
      rippleConfig,
      onClick,
    }
  },
})
</script>

<template>
  <component
    :is="Tag"
    :type="Tag === 'a' ? undefined : 'button'"
    :class="[
      'base-button',
      group?.selectedClass,
      {
        'base-button--active': isActive,
        'base-button--block': $props.block,
        'base-button--disabled': isDisabled,
        'base-button--elevated': isElevated,
        'base-button--flat': $props.flat,
        'base-button--icon': $props.icon,
        'base-button--loading': $props.loading,
        'base-button--readonly': $props.readonly,
        'base-button--slim': $props.slim,
        'base-button--stacked': $props.stacked,
      },
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      loaderClasses,
      positionClasses,
      roundedClasses,
      sizeClasses,
      variantClasses,
      $props.class,
    ]"
    :style="[
      colorStyles,
      dimensionStyles,
      locationStyles,
      sizeStyles,
      $props.style,
    ]"
    :aria-busy="$props.loading ? true : undefined"
    :disabled="isDisabled || undefined"
    :tabindex="$props.loading || $props.readonly ? -1 : undefined"
    @click="onClick"
    :value="valueAttr"
    v-bind="{ ...link.linkProps }"
    v-ripple="rippleConfig"
  >
    <!-- TODO: TOGGLE center if isIcon in v-ripple -->
    <component :is="genOverlays(true, 'base-button')" />

    <template v-if="!$props.icon && hasPrepend">
      <span key="prepend" class="base-button__prepend">
        <BaseIcon
          v-if="!$slots.prepend"
          key="prepend-icon"
          :icon="$props.prependIcon"
        />

        <BaseDefaultsProvider
          v-else
          key="prepend-defaults"
          :disabled="!$props.prependIcon"
          :defaults="{
            BaseIcon: {
              icon: $props.prependIcon,
            },
          }"
        >
          <slot name="prepend" />
        </BaseDefaultsProvider>
      </span>
    </template>

    <span class="base-button__content" data-no-activator="">
      <BaseIcon
        v-if="!$slots.default && hasIcon"
        key="content-icon"
        :icon="$props.icon"
      />
      <BaseDefaultsProvider
        v-else
        key="content-defaults"
        :disabled="!hasIcon"
        :defaults="{
          BaseIcon: {
            icon: $props.icon,
          },
        }"
      >
        <slot>
          {{ $props.text }}
        </slot>
      </BaseDefaultsProvider>
    </span>

    <template v-if="!$props.icon && hasAppend">
      <span key="append" class="base-button__append">
        <BaseIcon
          v-if="!$slots.append"
          key="append-icon"
          :icon="$props.appendIcon"
        />

        <BaseDefaultsProvider
          v-else
          key="append-defaults"
          :disabled="!$props.appendIcon"
          :defaults="{
            BaseIcon: {
              icon: $props.appendIcon,
            },
          }"
        >
          <slot name="append" />
        </BaseDefaultsProvider>
      </span>
    </template>

    <template v-if="!!$props.loading">
      <span key="loader" class="base-button__loader">
        <slot name="loader">
          <BaseProgressCircular
            :color="
              typeof $props.loading === 'boolean' ? undefined : $props.loading
            "
            indeterminate
            width="2"
          />
        </slot>
      </span>
    </template>
  </component>
</template>
