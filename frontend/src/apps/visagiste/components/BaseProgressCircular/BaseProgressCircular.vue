<script lang="ts">
// Styles
import "./BaseProgressCircular.scss";

// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useIntersectionObserver } from "@/apps/visagiste/composables/intersectionObserver";
import { useResizeObserver } from "@/apps/visagiste/composables/resizeObserver";
import {
  provideTheme,
  useThemeProps,
} from "@/apps/visagiste/composables/theme";
import { useTagProps } from "@/apps/visagiste/composables/tag";
import { useTextColor } from "@/apps/visagiste/composables/color";
import { useSize, useSizeProps } from "@/apps/visagiste/composables/size";

// Utilities
import { computed, ref, toRef, watchEffect } from "vue";
import {
  convertToUnit,
  defineComponent,
  propsFactory,
} from "@/apps/visagiste/utils";

// Types
import type { PropType, SlotsType } from "vue";

type BaseProgressCircularSlots = {
  default: (props?: any) => void;
};

export const useBaseProgressCircularProps = propsFactory(
  {
    bgColor: String,
    color: String,
    indeterminate: [Boolean, String] as PropType<boolean | "disable-shrink">,
    modelValue: {
      type: [Number, String],
      default: 0,
    },
    rotate: {
      type: [Number, String],
      default: 4,
    },
    width: {
      type: [Number, String],
      default: 4,
    },

    ...useComponentProps(),
    ...useSizeProps(),
    ...useTagProps({ tag: "div" }),
    ...useThemeProps(),
  },
  "BaseProgressCircular",
);

export default defineComponent({
  name: "BaseProgressCircular",
  props: useBaseProgressCircularProps(),
  slots: Object as SlotsType<BaseProgressCircularSlots>,
  setup(props) {
    const MAGIC_RADIUS_CONSTANT = 20;
    const CIRCUMFERENCE = 2 * Math.PI * MAGIC_RADIUS_CONSTANT;

    const root = ref<HTMLElement>();

    const { themeClasses } = provideTheme(props);
    const { sizeClasses, sizeStyles } = useSize(props);
    const { textColorClasses, textColorStyles } = useTextColor(
      toRef(props, "color"),
    );
    const {
      textColorClasses: underlayColorClasses,
      textColorStyles: underlayColorStyles,
    } = useTextColor(toRef(props, "bgColor"));
    const { intersectionRef, isIntersecting } = useIntersectionObserver();
    const { resizeRef, contentRect } = useResizeObserver();

    const normalizedValue = computed(() =>
      Math.max(0, Math.min(100, parseFloat(props.modelValue))),
    );
    const width = computed(() => Number(props.width));
    const size = computed(() => {
      // Get size from element if size prop value is small, large etc
      return sizeStyles.value
        ? Number(props.size)
        : contentRect.value
          ? contentRect.value.width
          : Math.max(width.value, 32);
    });
    const diameter = computed(
      () => (MAGIC_RADIUS_CONSTANT / (1 - width.value / size.value)) * 2,
    );
    const strokeWidth = computed(
      () => (width.value / size.value) * diameter.value,
    );
    const strokeDashOffset = computed(() =>
      convertToUnit(((100 - normalizedValue.value) / 100) * CIRCUMFERENCE),
    );

    watchEffect(() => {
      intersectionRef.value = root.value;
      resizeRef.value = root.value;
    });

    return {
      root,
      themeClasses,
      sizeClasses,
      sizeStyles,
      textColorClasses,
      textColorStyles,
      underlayColorClasses,
      underlayColorStyles,
      normalizedValue,
      diameter,
      MAGIC_RADIUS_CONSTANT,
      CIRCUMFERENCE,
      isIntersecting,
      strokeWidth,
      strokeDashOffset,
    };
  },
});
</script>

<template>
  <component
    :is="$props.tag"
    ref="root"
    :class="[
      'base-progress-circular',
      {
        'base-progress-circular--indeterminate': !!$props.indeterminate,
        'base-progress-circular--visible': isIntersecting,
        'base-progress-circular--disable-shrink':
          $props.indeterminate === 'disable-shrink',
      },
      themeClasses,
      sizeClasses,
      textColorClasses,
      $props.class,
    ]"
    :style="[sizeStyles, textColorStyles, $props.style]"
    role="progressbar"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="$props.indeterminate ? undefined : normalizedValue"
  >
    <svg
      :style="{
        transform: `rotate(calc(-90deg + ${Number($props.rotate)}deg))`,
      }"
      xmlns="http://www.w3.org/2000/svg"
      :viewBox="`0 0 ${diameter} ${diameter}`"
    >
      <circle
        :class="['base-progress-circular__underlay', underlayColorClasses]"
        :style="underlayColorStyles"
        fill="transparent"
        cx="50%"
        cy="50%"
        :r="MAGIC_RADIUS_CONSTANT"
        :stroke-width="strokeWidth"
        :stroke-dasharray="CIRCUMFERENCE"
        stroke-dashoffset="0"
      />
      <circle
        class="base-progress-circular__overlay"
        fill="transparent"
        cx="50%"
        cy="50%"
        :r="MAGIC_RADIUS_CONSTANT"
        :stroke-width="strokeWidth"
        :stroke-dasharray="CIRCUMFERENCE"
        :stroke-dashoffset="strokeDashOffset"
      />
    </svg>

    <template v-if="$slots.default">
      <div class="base-progress-circular__content">
        <slot v-bind="{ value: normalizedValue }" />
      </div>
    </template>
  </component>
</template>
