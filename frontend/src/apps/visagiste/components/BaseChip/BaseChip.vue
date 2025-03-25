<script lang="ts">
// Styles
import './BaseChip.scss'

// Components
import { BaseChipGroupSymbol } from '../BaseChipGroup/BaseChipGroup.vue'
import { BaseExpandXTransition } from '@/apps/visagiste/components/transitions'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import { BaseIcon } from '@/apps/visagiste/components/BaseIcon'
import BaseAvatar from '@/apps/visagiste/components/BaseAvatar/BaseAvatar.vue'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useElevation,
  useElevationProps,
} from '@/apps/visagiste/composables/elevation'
import {
  useGroupItem,
  useGroupItemProps,
} from '@/apps/visagiste/composables/group'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import {
  genOverlays,
  useVariant,
  useVariantProps,
} from '@/apps/visagiste/composables/variant'
import { useLink, useRouterProps } from '@/apps/visagiste/composables/router'
import { useBorder, useBorderProps } from '@/apps/visagiste/composables/border'
import { provideTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useProxiedModel } from '@/apps/visagiste/composables/proxiedModel'
import { useSize, useSizeProps } from '@/apps/visagiste/composables/size'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useLocale } from '@/apps/visagiste/composables'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'

// Directives
import { Ripple } from '@/apps/visagiste/directives/ripple'

// Utilities
import { computed } from 'vue'
import {
  defineComponent,
  EventProp,
  propsFactory,
} from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { RippleDirectiveBinding } from '@/apps/visagiste/directives/ripple'

export type BaseChipSlots = {
  default: {
    isSelected: boolean | undefined
    selectedClass: boolean | (string | undefined)[] | undefined
    select: ((value: boolean) => void) | undefined
    toggle: (() => void) | undefined
    value: unknown
    disabled: boolean
  }
  label: never
  prepend: never
  append: never
  close: never
  filter: never
}

export const useBaseChipProps = propsFactory(
  {
    activeClass: String,
    appendAvatar: String,
    appendIcon: IconValue,
    closable: Boolean,
    closeIcon: {
      type: IconValue,
      default: '$delete',
    },
    closeLabel: {
      type: String,
      default: '$visagiste.close',
    },
    draggable: Boolean,
    filter: Boolean,
    filterIcon: {
      type: IconValue,
      default: '$complete',
    },
    label: Boolean,
    link: {
      type: Boolean,
      default: undefined,
    },
    pill: Boolean,
    prependAvatar: String,
    prependIcon: IconValue,
    ripple: {
      type: [Boolean, Object] as PropType<RippleDirectiveBinding['value']>,
      default: true,
    },
    text: String,
    modelValue: {
      type: Boolean,
      default: true,
    },

    onClick: EventProp<[MouseEvent]>(),
    onClickOnce: EventProp<[MouseEvent]>(),

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useElevationProps(),
    ...useGroupItemProps(),
    ...useRoundedProps(),
    ...useRouterProps(),
    ...useSizeProps(),
    ...useTagProps({ tag: 'span' }),
    ...useThemeProps(),
    ...useVariantProps({ variant: 'tonal' } as const),
  },
  'BaseChip'
)

export default defineComponent({
  name: 'BaseChip',
  components: {
    BaseAvatar,
    BaseIcon,
    BaseDefaultsProvider,
    BaseExpandXTransition,
  },
  methods: {
    genOverlays,
  },
  directives: { Ripple },
  props: useBaseChipProps(),
  emits: {
    'click:close': (e: MouseEvent) => true,
    'update:modelValue': (value: boolean) => true,
    'group:selected': (val: { value: boolean }) => true,
    click: (e: MouseEvent | KeyboardEvent) => true,
  },
  setup(props, { attrs, emit }) {
    const { t } = useLocale()
    const { borderClasses } = useBorder(props)
    const { colorClasses, colorStyles, variantClasses } = useVariant(props)
    const { densityClasses } = useDensity(props)
    const { elevationClasses } = useElevation(props)
    const { roundedClasses } = useRounded(props)
    const { sizeClasses } = useSize(props)
    const { themeClasses } = provideTheme(props)

    const isActive = useProxiedModel(props, 'modelValue')
    const group = useGroupItem(props, BaseChipGroupSymbol, false)
    const link = useLink(props, attrs)
    const isLink = computed(() => props.link !== false && link.isLink.value)
    const isClickable = computed(
      () =>
        !props.disabled &&
        props.link !== false &&
        (!!group || props.link || link.isClickable.value)
    )
    const closeProps = computed(() => ({
      'aria-label': t(props.closeLabel),
      onClick(e: MouseEvent) {
        e.preventDefault()
        e.stopPropagation()

        isActive.value = false

        emit('click:close', e)
      },
    }))

    function onClick(e: MouseEvent) {
      emit('click', e)

      if (!isClickable.value) return

      link.navigate?.(e)
      group?.toggle()
    }

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault()
        onClick(e as any as MouseEvent)
      }
    }

    const appendIsEmpty = useSlotIsEmpty('append')
    const prependIsEmpty = useSlotIsEmpty('prepend')
    const closeIsEmpty = useSlotIsEmpty('close')
    const filterIsEmpty = useSlotIsEmpty('filter')

    const Tag = computed(() => (link.isLink.value ? 'a' : props.tag))
    const hasAppendMedia = computed(
      () => !!(props.appendIcon || props.appendAvatar)
    )
    const hasAppend = computed(() => hasAppendMedia.value || !appendIsEmpty.value)
    const hasClose = computed(() => !!(!closeIsEmpty.value || props.closable))
    const hasFilter = computed(() => !!(!filterIsEmpty.value || props.filter) && group)
    const hasPrependMedia = computed(
      () => !!(props.prependIcon || props.prependAvatar)
    )
    const hasPrepend = computed(() => hasPrependMedia.value || !prependIsEmpty.value)
    const hasColor = computed(() => !group || group.isSelected.value)

    return {
      Tag,
      closeProps,
      isClickable,
      hasFilter,
      hasColor,
      hasPrepend,
      hasClose,
      hasAppend,
      hasPrependMedia,
      hasAppendMedia,
      isLink,
      isActive,
      link,
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      roundedClasses,
      sizeClasses,
      variantClasses,
      colorStyles,
      group,
      onClick,
      onKeyDown,
    }
  },
})
</script>

<template>
  <component
    v-if="isActive"
    :is="Tag"
    :class="[
      'base-chip',
      {
        'base-chip--disabled': $props.disabled,
        'base-chip--label': $props.label,
        'base-chip--link': isClickable,
        'base-chip--filter': hasFilter,
        'base-chip--pill': $props.pill,
        [`${$props.activeClass}`]: $props.activeClass && link.isActive,
      },
      themeClasses,
      borderClasses,
      hasColor ? colorClasses : undefined,
      densityClasses,
      elevationClasses,
      roundedClasses,
      sizeClasses,
      variantClasses,
      group?.selectedClass,
      $props.class,
    ]"
    :style="[hasColor ? colorStyles : undefined, $props.style]"
    :disabled="$props.disabled || undefined"
    :draggable="$props.draggable"
    :tabindex="isClickable ? 0 : undefined"
    @click="onClick"
    @keydown="isClickable && !isLink && onKeyDown"
    v-ripple="isClickable && $props.ripple"
    v-bind="{ ...link.linkProps }"
  >
    <component :is="genOverlays(isClickable, 'base-chip')" />

    <template v-if="hasFilter">
      <BaseExpandXTransition key="filters">
        <div v-show="group!.isSelected" class="base-chip__filter">
          <BaseDefaultsProvider
            v-if="$slots.filter"
            key="filter-defaults"
            :disalbed="!$props.filterIcon"
            :defaults="{
              BaseIcon: { icon: $props.filterIcon },
            }"
          >
            <slot name="filter" />
          </BaseDefaultsProvider>
          <BaseIcon v-else key="filter-icon" :icon="$props.filterIcon" />
        </div>
      </BaseExpandXTransition>
    </template>

    <template v-if="hasPrepend">
      <div key="prepend" class="base-chip__prepend">
        <BaseDefaultsProvider
          v-if="$slots.prepend"
          key="prepend-defaults"
          :disabled="!hasPrependMedia"
          :defaults="{
            BaseAvatar: {
              image: $props.prependAvatar,
              start: true,
            },
            BaseIcon: {
              icon: $props.prependIcon,
              start: true,
            },
          }"
        >
          <slot name="prepend" />
        </BaseDefaultsProvider>

        <template v-else>
          <BaseIcon
            v-if="$props.prependIcon"
            key="prepend-icon"
            :icon="$props.prependIcon"
            start
          />
          <BaseAvatar
            v-if="$props.prependAvatar"
            key="prepend-avatar"
            :image="$props.prependAvatar"
            start
          />
        </template>
      </div>
    </template>

    <div class="base-chip__content" data-no-activator="">
      <slot
        v-bind="{
          isSelected: group?.isSelected.value,
          selectedClass: group?.selectedClass.value,
          select: group?.select,
          toggle: group?.toggle,
          value: group?.value.value,
          disabled: group?.disabled,
        }"
      >
        {{ $props.text }}
      </slot>
    </div>

    <template v-if="hasAppend">
      <div key="append" class="base-chip__append">
        <BaseDefaultsProvider
          v-if="$slots.append"
          key="append-defaults"
          :disabled="!hasAppendMedia"
          :defaults="{
            BaseAvatar: {
              image: $props.appendAvatar,
              end: true,
            },
            BaseIcon: {
              icon: $props.appendIcon,
              end: true,
            },
          }"
        >
          <slot name="append" />
        </BaseDefaultsProvider>

        <template v-else>
          <BaseIcon
            v-if="$props.appendIcon"
            key="append-icon"
            :icon="$props.appendIcon"
            end
          />
          <BaseAvatar
            v-if="$props.appendAvatar"
            key="append-avatar"
            :image="$props.appendAvatar"
            end
          />
        </template>
      </div>
    </template>

    <template v-if="hasClose">
      <button
        key="close"
        class="base-chip__close"
        type="button"
        data-testid="close-chip"
        v-bind="{ ...closeProps }"
      >
        <BaseDefaultsProvider
          v-if="$slots.close"
          key="close-defaults"
          :defaults="{
            BaseIcon: {
              icon: $props.closeIcon,
              size: 'x-small',
            },
          }"
        >
          <slot name="close" />
        </BaseDefaultsProvider>
        <BaseIcon v-else key="close-icon" :icon="$props.closeIcon" />
      </button>
    </template>
  </component>
</template>
