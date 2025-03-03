<script lang="ts">
// Styles
import './BaseListItem.scss'

// Components
import BaseListItemSubtitle from './BaseListItemSubtitle.vue'
import BaseListItemTitle from './BaseListItemTitle.vue'
import BaseAvatar from '@/apps/visagiste/components/BaseAvatar/BaseAvatar.vue'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'

// Composables
import { useList } from './list'
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
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useNestedItem } from '@/apps/visagiste/composables/nested/nested'
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

// Directives
import { Ripple } from '@/apps/visagiste/directives'

// Utilities
import { computed, onBeforeMount, watch } from 'vue'
import {
  defineComponent,
  EventProp,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { RippleDirectiveBinding } from '@/directives/ripple'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

export type ListItemSlot = {
  isActive: boolean
  isOpen: boolean
  isSelected: boolean
  isIndeterminate: boolean
  select: (value: boolean) => void
}

export type ListItemTitleSlot = {
  title?: string | number
}

export type ListItemSubtitleSlot = {
  subtitle?: string | number
}

export type BaseListItemSlots = {
  prepend: ListItemSlot
  append: ListItemSlot
  default: ListItemSlot
  title: ListItemTitleSlot
  subtitle: ListItemSubtitleSlot
}

export const useBaseListItemProps = propsFactory(
  {
    active: {
      type: Boolean,
      default: undefined,
    },
    activeClass: String,
    appendAvatar: String,
    appendIcon: IconValue,
    baseColor: String,
    disabled: Boolean,
    lines: [Boolean, String] as PropType<'one' | 'two' | 'three' | false>,
    link: {
      type: Boolean,
      default: undefined,
    },
    nav: Boolean,
    prependAvatar: String,
    prependIcon: IconValue,
    ripple: {
      type: [Boolean, Object] as PropType<RippleDirectiveBinding['value']>,
      default: true,
    },
    slim: Boolean,
    subtitle: [String, Number],
    title: [String, Number],
    value: null,

    onClick: EventProp<[MouseEvent | KeyboardEvent]>(),
    onClickOnce: EventProp<[MouseEvent]>(),

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useDimensionProps(),
    ...useElevationProps(),
    ...useRoundedProps(),
    ...useRouterProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'text' } as const),
  },
  'BaseListItem'
)

export default defineComponent({
  name: 'BaseListItem',
  components: {
    BaseDefaultsProvider,
    BaseIcon,
    BaseAvatar,
    BaseListItemTitle,
    BaseListItemSubtitle,
  },
  methods: {
    genOverlays,
  },
  directives: {
    Ripple,
  },
  props: useBaseListItemProps(),
  emits: {
    click: (e: MouseEvent | KeyboardEvent) => true,
  },
  setup(props, { attrs, emit }) {
    const link = useLink(props, attrs)
    const id = computed(() =>
      props.value === undefined ? link.href.value : props.value
    )
    const {
      activate,
      isActivated,
      select,
      isOpen,
      isSelected,
      isIndeterminate,
      isGroupActivator,
      root,
      parent,
      openOnSelect,
      id: uid,
    } = useNestedItem(id, false)
    const list = useList()
    const isActive = computed(
      () =>
        props.active !== false &&
        (props.active ||
          link.isActive?.value ||
          (root.activatable.value ? isActivated.value : isSelected.value))
    )
    const isLink = computed(() => props.link !== false && link.isLink.value)
    const isSelectable = computed(
      () =>
        !!list &&
        (root.selectable.value || root.activatable.value || props.value != null)
    )
    const isClickable = computed(
      () =>
        !props.disabled &&
        props.link !== false &&
        (props.link || link.isClickable.value || isSelectable.value)
    )

    const roundedProps = computed(() => props.rounded || props.nav)
    const color = computed(() => props.color)
    const variantProps = computed(() => ({
      color: isActive.value
        ? (color.value ?? props.baseColor)
        : props.baseColor,
      variant: props.variant,
    }))

    // useNestedItem doesn't call register until beforeMount,
    // so this can't be an immediate watcher as we don't know parent yet
    watch(
      () => link.isActive?.value,
      (val) => {
        if (!val) return
        handleActiveLink()
      }
    )
    onBeforeMount(() => {
      if (link.isActive?.value) handleActiveLink()
    })
    function handleActiveLink() {
      if (parent.value != null) {
        root.open(parent.value, true)
      }
      openOnSelect(true)
    }

    const { themeClasses } = provideTheme(props)
    const { borderClasses } = useBorder(props)
    const { colorClasses, colorStyles, variantClasses } =
      useVariant(variantProps)
    const { densityClasses } = useDensity(props)
    const { dimensionStyles } = useDimension(props)
    const { elevationClasses } = useElevation(props)
    const { roundedClasses } = useRounded(roundedProps)
    const lineClasses = computed(() =>
      props.lines ? `base-list-item--${props.lines}-line` : undefined
    )

    const slotProps = computed(
      () =>
        ({
          isActive: isActive.value,
          select,
          isOpen: isOpen.value,
          isSelected: isSelected.value,
          isIndeterminate: isIndeterminate.value,
        }) satisfies ListItemSlot
    )

    function onClick(e: MouseEvent) {
      emit('click', e)

      if (!isClickable.value) return

      link.navigate?.(e)

      if (isGroupActivator) return

      if (root.activatable.value) {
        activate(!isActivated.value, e)
      } else if (root.selectable.value) {
        select(!isSelected.value, e)
      } else if (props.value != null) {
        select(!isSelected.value, e)
      }
    }

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault()
        e.target!.dispatchEvent(new MouseEvent('click', e))
      }
    }

    const prependIsEmpty = useSlotIsEmpty('prepend')
    const appendIsEmpty = useSlotIsEmpty('append')
    const titleIsEmpty = useSlotIsEmpty('title')
    const subtitleIsEmpty = useSlotIsEmpty('subtitle')

    const Tag = computed(() => (isLink.value ? 'a' : props.tag))
    const hasTitle = computed(() => !titleIsEmpty.value || props.title != null)
    const hasSubtitle = computed(
      () => !subtitleIsEmpty.value || props.subtitle != null
    )
    const hasAppendMedia = computed(
      () => !!(props.appendAvatar || props.appendIcon)
    )
    const hasAppend = computed(
      () => hasAppendMedia.value || !appendIsEmpty.value
    )
    const hasPrependMedia = computed(
      () => !!(props.prependAvatar || props.prependIcon)
    )
    const hasPrepend = computed(
      () => hasPrependMedia.value || !prependIsEmpty.value
    )

    watch(
      () => hasPrepend.value,
      () => list?.updateHasPrepend(hasPrepend.value)
    )

    return {
      uid,
      list,
      root,
      link,
      slotProps,
      Tag,
      hasTitle,
      hasSubtitle,
      hasAppendMedia,
      hasAppend,
      hasPrependMedia,
      hasPrepend,
      isActive,
      isActivated,
      isClickable,
      isSelected,
      isSelectable,
      isLink,
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      lineClasses,
      roundedClasses,
      variantClasses,
      colorStyles,
      dimensionStyles,
      onClick,
      onKeyDown,
    }
  },
})
</script>

<template>
  <component
    :is="Tag"
    :class="[
      'base-list-item',
      {
        'base-list-item--active': isActive,
        'base-list-item--disabled': $props.disabled,
        'base-list-item--link': isClickable,
        'base-list-item--nav': $props.nav,
        'base-list-item--prepend': !hasPrepend && list?.hasPrepend,
        'base-list-item--slim': $props.slim,
        [`${$props.activeClass}`]: $props.activeClass && isActive,
      },
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      lineClasses,
      roundedClasses,
      variantClasses,
      $props.class,
    ]"
    :style="[colorStyles, dimensionStyles, $props.style]"
    :tabindex="isClickable ? (list ? -2 : 0) : undefined"
    :aria-selected="
      isSelectable
        ? root.activatable
          ? isActivated
          : root.selectable
            ? isSelected
            : isActive
        : undefined
    "
    @click="onClick"
    @keydown="isClickable && !isLink && onKeyDown"
    v-ripple="isClickable && $props.ripple"
    v-bind="{ ...link.linkProps }"
  >
    <component :is="genOverlays(isClickable || isActive, 'base-list-item')" />

    <div v-if="hasPrepend" key="prepend" class="base-list-item__prepend">
      <template v-if="!$slots.prepend">
        <BaseAvatar
          v-if="$props.prependAvatar"
          key="prepend-avatar"
          :density="$props.density"
          :image="$props.prependAvatar"
        />
        <BaseIcon
          v-if="$props.prependIcon"
          key="prepend-icon"
          :density="$props.density"
          :icon="$props.prependIcon"
        />
      </template>

      <BaseDefaultsProvider
        v-else
        key="prepend-defaults"
        :disabled="!hasPrependMedia"
        :defaults="{
          BaseAvatar: {
            density: $props.density,
            image: $props.prependAvatar,
          },
          BaseIcon: {
            density: $props.density,
            icon: $props.prependIcon,
          },
          BaseListItemAction: {
            start: true,
          },
        }"
      >
        <slot name="prepend" v-bind="slotProps" />
      </BaseDefaultsProvider>

      <div class="base-list-item__spacer" />
    </div>

    <div class="base-list-item__content" data-no-activator="">
      <BaseListItemTitle v-if="hasTitle" key="title">
        <slot name="title" v-bind="{ title: $props.title }">
          {{ $props.title }}
        </slot>
      </BaseListItemTitle>

      <BaseListItemSubtitle v-if="hasSubtitle" key="subtitle">
        <slot name="subtitle" v-bind="{ subtitle: $props.subtitle }">
          {{ $props.subtitle }}
        </slot>
      </BaseListItemSubtitle>

      <slot v-bind="slotProps" />
    </div>

    <div v-if="hasAppend" key="append" class="base-list-item__append">
      <template v-if="!$slots.append">
        <BaseAvatar
          v-if="$props.appendAvatar"
          key="append-avatar"
          :density="$props.density"
          :image="$props.appendAvatar"
        />
        <BaseIcon
          v-if="$props.appendIcon"
          key="append-icon"
          :density="$props.density"
          :icon="$props.appendIcon"
        />
      </template>

      <BaseDefaultsProvider
        v-else
        key="append-defaults"
        :disabled="!hasAppendMedia"
        :defaults="{
          BaseAvatar: {
            density: $props.density,
            image: $props.appendAvatar,
          },
          BaseIcon: {
            density: $props.density,
            icon: $props.appendIcon,
          },
          BaseListItemAction: {
            start: true,
          },
        }"
      >
        <slot name="append" v-bind="slotProps" />
      </BaseDefaultsProvider>

      <div class="base-list-item__spacer" />
    </div>
  </component>
</template>
