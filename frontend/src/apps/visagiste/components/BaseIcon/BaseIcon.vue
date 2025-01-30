<script lang="ts">
// Styles
import './BaseIcon.scss';

// Composables
import {useTextColor} from "@/apps/visagiste/composables/color";
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {IconValue, useIcon} from "@/apps/visagiste/composables/icons";
import {useSize, useSizeProps} from "@/apps/visagiste/composables/size";
import {useTagProps} from "@/apps/visagiste/composables/tag";
import {provideTheme, useThemeProps} from "@/apps/visagiste/composables/theme";

// Utilities
import {computed, ref, Text, toRef} from "vue";
import {convertToUnit, defineComponent, flattenFragments, propsFactory} from '@/apps/visagiste/utils';

export const useBaseIconProps = propsFactory({
  color: String,
  disabled: Boolean,
  start: Boolean,
  end: Boolean,
  icon: IconValue,

  ...useComponentProps(),
  ...useSizeProps(),
  ...useTagProps({ tag: 'i' }),
  ...useThemeProps(),
}, 'BaseIcon')

export default defineComponent({
  name: "BaseIcon",
  methods: {
    convertToUnit
  },
  props: useBaseIconProps(),
  setup (props, { attrs, slots }) {
    const slotIcon = ref<string>()

    const { themeClasses } = provideTheme(props)
    const { iconData } = useIcon(computed(() => slotIcon.value || props.icon))
    const { sizeClasses } = useSize(props)
    const { textColorClasses, textColorStyles } = useTextColor(toRef(props, 'color'))

    const slotValue = slots.default?.()

    if (slotValue) {
      slotIcon.value = flattenFragments(slotValue).filter(node =>
        node.type === Text && node.children && typeof node.children === 'string'
      )[0]?.children as string
    }
    const hasClick = !!(attrs.onClick || attrs.onClickOnce)

    return {
      themeClasses,
      iconData,
      sizeClasses,
      textColorClasses,
      textColorStyles,
      hasClick,
    }
  },
})
</script>

<template>
<component
  :is="iconData.component"
  :tag="tag"
  :icon="iconData.icon"
  :class="[
    'base-icon',
    'notranslate',
    themeClasses,
    sizeClasses,
    textColorClasses,
    {
      'base-icon--clickable': hasClick,
      'base-icon--disabled': $props.disabled,
      'base-icon--start': $props.start,
      'base-icon--end': $props.end,
    },
    $props.class,
  ]"
  :style="[
    !sizeClasses
      ? {
        fontSize: convertToUnit($props.size),
        height: convertToUnit($props.size),
        width: convertToUnit($props.size),
      }
      : undefined,
    textColorStyles,
    $props.style,
  ]"
  :role="hasClick ? 'button' : undefined"
  :aria-hidden="!hasClick"
  :tabindex="hasClick ? $props.disabled ? -1 : 0 : undefined"
>
  <slot/>
</component>
</template>
