<script lang="ts">
// Composables
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useLink, useRouterProps } from '@/apps/visagiste/composables/router'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { useTextColor } from '@/apps/visagiste/composables/color'

// Utilities
import { computed } from 'vue'
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseBreadcrumbsItemProps = propsFactory(
  {
    active: Boolean,
    activeClass: String,
    activeColor: String,
    color: String,
    disabled: Boolean,
    title: String,

    ...useComponentProps(),
    ...useRouterProps(),
    ...useTagProps({ tag: 'li' }),
  },
  'BaseBreadcrumbsItem'
)

export default defineComponent({
  name: 'BaseBreadcrumbsItem',
  props: useBaseBreadcrumbsItemProps(),
  setup(props, { attrs }) {
    const link = useLink(props, attrs)
    const isActive = computed(() => props.active || link.isActive?.value)
    const color = computed(() =>
      isActive.value ? props.activeColor : props.color
    )

    const { textColorClasses, textColorStyles } = useTextColor(color)

    return {
      link,
      isActive,
      textColorClasses,
      textColorStyles,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-breadcrumbs-item',
      {
        'base-breadcrumbs-item--active': isActive,
        'base-breadcrumbs-item--disabled': $props.disabled,
        [`${$props.activeClass}`]: isActive && $props.activeClass,
      },
      textColorClasses,
      $props.class,
    ]"
    :style="[textColorStyles, $props.style]"
    :aria-current="isActive ? 'page' : undefined"
  >
    <slot v-if="!link.isLink">{{ $props.title }}</slot>
    <a
      v-else
      class="base-breadcrumbs-item--link"
      @click="link.navigate"
      v-bind="link.linkProps"
    >
      <slot>{{ $props.title }}</slot>
    </a>
  </component>
</template>
