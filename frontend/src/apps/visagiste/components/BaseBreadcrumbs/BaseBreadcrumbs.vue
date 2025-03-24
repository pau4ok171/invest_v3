<script lang="ts">
// Styles
import './BaseBreadcrumbs.scss'

// Components
import { IconValue } from '@/apps/visagiste/composables/icons'
import BaseIcon from '@/apps/visagiste/components/BaseIcon/BaseIcon.vue'
import BaseDefaultsProvider from '@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue'
import BaseBreadcrumbsItem from '@/apps/visagiste/components/BaseBreadcrumbs/BaseBreadcrumbsItem.vue'
import BaseBreadcrumbsDivider from '@/apps/visagiste/components/BaseBreadcrumbs/BaseBreadcrumbsDivider.vue'

// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useBackgroundColor } from '@/apps/visagiste/composables/color'
import { useSlotIsEmpty } from '@/apps/visagiste/composables/slotIsEmpty'
import { provideDefaults } from '@/apps/visagiste/composables/defaults'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import {
  useDensity,
  useDensityProps,
} from '@/apps/visagiste/composables/density'
import { useTagProps } from '@/apps/visagiste/composables/tag'

// Utilities
import { computed, toRef } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

// Types
import type { PropType } from 'vue'
import type { LinkProps } from '@/apps/visagiste/composables/router'

export type InternalBreadcrumbItem = Partial<LinkProps> & {
  title: string
  disabled?: boolean
}

export type BreadcrumbItem = string | InternalBreadcrumbItem

export const useBaseBreadcrumbProps = propsFactory(
  {
    activeClass: String,
    activeColor: String,
    bgColor: String,
    color: String,
    disabled: Boolean,
    divider: {
      type: String,
      default: '/',
    },
    icon: IconValue,
    items: {
      type: Array as PropType<readonly BreadcrumbItem[]>,
      default: () => [],
    },

    ...useComponentProps(),
    ...useDensityProps(),
    ...useRoundedProps(),
    ...useTagProps({ tag: 'ul' }),
  },
  'BaseBreadcrumbs'
)

export default defineComponent({
  name: 'BaseBreadcrumbs',
  components: {
    BaseBreadcrumbsDivider,
    BaseBreadcrumbsItem,
    BaseDefaultsProvider,
    BaseIcon,
  },
  props: useBaseBreadcrumbProps(),
  setup(props) {
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, 'bgColor'))
    const { densityClasses } = useDensity(props)
    const { roundedClasses } = useRounded(props)

    provideDefaults({
      BaseBreadcrumbsDivider: {
        divider: toRef(props, 'divider'),
      },
      BaseBreadcrumbsItem: {
        activeClass: toRef(props, 'activeClass'),
        activeColor: toRef(props, 'activeColor'),
        color: toRef(props, 'color'),
        disabled: toRef(props, 'disabled'),
      },
    })

    const items = computed(() =>
      props.items.map((item) => {
        return typeof item === 'string'
          ? { item: { title: item }, raw: item }
          : { item, raw: item }
      })
    )

    const prependIsEmpty = useSlotIsEmpty('prepend')
    const hasPrepend = computed(() => !prependIsEmpty.value || props.icon)

    return {
      backgroundColorClasses,
      backgroundColorStyles,
      densityClasses,
      roundedClasses,
      items,
      hasPrepend,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-breadcrumbs',
      backgroundColorClasses,
      densityClasses,
      roundedClasses,
      $props.class,
    ]"
    :style="[backgroundColorStyles, $props.style]"
  >
    <li v-if="hasPrepend" key="prepend" class="base-breadcrumbs__prepend">
      <BaseDefaultsProvider
        v-if="$slots.prepend"
        key="prepend-defaults"
        :disabled="!$props.icon"
        :defaults="{
          BaseIcon: {
            icon: $props.icon,
            start: true,
          },
        }"
      >
        <slot name="prepend" />
      </BaseDefaultsProvider>

      <BaseIcon v-else key="prepend-icon" start :icon="$props.icon" />
    </li>

    <template v-for="({ item, raw }, index) in items">
      <slot name="item" v-bind="{ item, index }">
        <BaseBreadcrumbsItem
          :key="index"
          :disabled="index >= items.length - 1"
          :activeClass="$props.activeClass"
          :activeColor="$props.activeColor"
          :color="$props.color"
          v-bind="{ ...(typeof item === 'string' ? { title: item } : item) }"
        >
          <slot name="title" v-bind="{ item, index }" />
        </BaseBreadcrumbsItem>
      </slot>

      <BaseBreadcrumbsDivider
        :divider="$props.divider"
        v-if="index < items.length - 1"
      >
        <slot name="divider" v-bind="{ item: raw, index }" />
      </BaseBreadcrumbsDivider>
    </template>

    <slot />
  </component>
</template>
