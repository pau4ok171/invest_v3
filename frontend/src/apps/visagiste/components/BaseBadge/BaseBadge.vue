<script lang="ts">
// Styles
import './BaseBadge.scss'

// Components
import BaseIcon from "@/apps/visagiste/components/BaseIcon/BaseIcon.vue";

// Composables
import { IconValue } from '@/apps/visagiste/composables/icons'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import {
  useLocation,
  useLocationProps,
} from '@/apps/visagiste/composables/location'
import {
  useRounded,
  useRoundedProps,
} from '@/apps/visagiste/composables/rounded'
import { useTagProps } from '@/apps/visagiste/composables/tag'
import { useTheme, useThemeProps } from '@/apps/visagiste/composables/theme'
import { useTransitionProps } from '@/apps/visagiste/composables/transition'
import {
  useBackgroundColor,
  useTextColor,
} from '@/apps/visagiste/composables/color'
import { useLocale } from '@/apps/visagiste/composables/locale'
import MaybeTransition from '@/apps/visagiste/composablesV2/transition.vue'

// Utilities
import { defineComponent, toRef, computed } from 'vue'
import { pickWithRest, propsFactory } from '@/apps/visagiste/utils'

export const useBaseBadgeProps = propsFactory(
  {
    bordered: Boolean,
    color: String,
    content: [Number, String],
    dot: Boolean,
    floating: Boolean,
    icon: IconValue,
    inline: Boolean,
    label: {
      type: String,
      default: '$visagiste.badge',
    },
    max: [Number, String],
    modelValue: {
      type: Boolean,
      default: true,
    },
    offsetX: [Number, String],
    offsetY: [Number, String],
    textColor: String,

    ...useComponentProps(),
    ...useLocationProps({ location: 'top end' } as const),
    ...useRoundedProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useTransitionProps({ transition: 'scale-rotate-transition' }),
  },
  'BaseBadge'
)

export default defineComponent({
  name: 'BaseBadge',
  components: {BaseIcon, MaybeTransition },
  inheritAttrs: false,
  props: useBaseBadgeProps(),
  setup(props, { attrs }) {
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, 'color'))
    const { roundedClasses } = useRounded(props)
    const { t } = useLocale()
    const { textColorClasses, textColorStyles } = useTextColor(
      toRef(props, 'textColor')
    )
    const { themeClasses } = useTheme()

    const { locationStyles } = useLocation(props, true, (side) => {
      const base = props.floating ? (props.dot ? 2 : 4) : props.dot ? 8 : 12
      return (
        base +
        (['top', 'bottom'].includes(side)
          ? Number(props.offsetY ?? 0)
          : ['left', 'right'].includes(side)
            ? Number(props.offsetX ?? 0)
            : 0)
      )
    })

    const { badgeAttrs, rootAttrs } = computed(() => {
      const [badge, root] = pickWithRest(attrs, [
        'aria-atomic',
        'aria-label',
        'aria-live',
        'role',
        'title',
      ])
      return { badgeAttrs: badge, rootAttrs: root }
    }).value

    const value = computed(() => Number(props.content))
    const content = computed(() =>
      !props.max || isNaN(value.value)
        ? props.content
        : value.value <= Number(props.max)
          ? value.value
          : `${props.max}+`
    )

    return {
      badgeAttrs,
      rootAttrs,
      value,
      content,
      backgroundColorClasses,
      backgroundColorStyles,
      roundedClasses,
      textColorClasses,
      textColorStyles,
      themeClasses,
      locationStyles,
      t,
    }
  },
})
</script>

<template>
  <component
    :is="$props.tag as string"
    :class="[
      'base-badge',
      {
        'base-badge--bordered': $props.bordered,
        'base-badge--dot': $props.dot,
        'base-badge--floating': $props.floating,
        'base-badge--inline': $props.inline,
      },
      $props.class,
    ]"
    v-bind="rootAttrs"
    :style="$props.style"
  >
    <div class="base-badge__wrapper">
      <slot />

      <MaybeTransition :transition="$props.transition">
        <span
          v-show="$props.modelValue"
          :class="[
            'base-badge__badge',
            themeClasses,
            backgroundColorClasses,
            roundedClasses,
            textColorClasses,
          ]"
          :style="[
            backgroundColorStyles,
            textColorStyles,
            $props.inline ? {} : locationStyles,
          ]"
          aria-atomic="true"
          :aria-label="t($props.label as string, value)"
          aria-live="polite"
          role="status"
          v-bind="badgeAttrs"
        >
          <slot
            v-if="!$props.dot"
            name="badge"
          >
            <BaseIcon
              v-if="$props.icon"
              :icon="$props.icon"
            />
            <template v-else>{{ content }}</template>
          </slot>
        </span>
      </MaybeTransition>
    </div>
  </component>
</template>
