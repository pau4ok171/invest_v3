<script lang="ts">
// Styles
import './BaseProgressLinear.scss';

// Composables
import {useComponentProps} from "@/apps/visagiste/composables/component";
import {provideTheme, useThemeProps} from "@/apps/visagiste/composables/theme";
import {useLocation, useLocationProps} from "@/apps/visagiste/composables/location";
import {useRounded, useRoundedProps} from "@/apps/visagiste/composables/rounded";
import {useTagProps} from "@/apps/visagiste/composables/tag";
import {useProxiedModel} from "@/apps/visagiste/composables/proxiedModel";
import {useRtl} from "@/apps/visagiste/composables";
import {useBackgroundColor, useTextColor} from "@/apps/visagiste/composables/color";
import {useIntersectionObserver} from "@/apps/visagiste/composables/intersectionObserver";

// Utilities
import {computed, defineComponent} from 'vue'
import {clamp, convertToUnit, IN_BROWSER, propsFactory} from "@/apps/visagiste/utils";

type BaseProgressLinearSlots = {
  default: { value: number, buffer: number }
}

export const useBaseProgressLinearProps = propsFactory({
  absolute: Boolean,
  active: {
    type: Boolean,
    default: true
  },
  bgColor: String,
  bgOpacity: [Number, String],
  bufferValue: {
    type: [Number, String],
    default: 0,
  },
  bufferColor: String,
  bufferOpacity: [Number, String],
  clickable: Boolean,
  color: String,
  height: {
    type: [Number, String],
    default: 4,
  },
  indeterminate: Boolean,
  max: {
    type: [Number, String],
    default: 100,
  },
  modelValue: {
    type: [Number, String],
    default: 0,
  },
  opacity: [Number, String],
  reverse: Boolean,
  stream: Boolean,
  striped: Boolean,
  roundedBar: Boolean,
  ...useComponentProps(),
  ...useLocationProps(),
  ...useRoundedProps(),
  ...useTagProps(),
  ...useThemeProps(),
}, 'BaseProgressLinear')

export default defineComponent({
  name: "BaseProgressLinear",
  methods: {convertToUnit},
  props: {
    ...useBaseProgressLinearProps()
  },
  emits: {
    'update:modelValue': (value: number) => true,
  },
  setup (props) {
    const progress = useProxiedModel(props, 'modelValue')
    const { isRtl, rtlClasses } = useRtl()
    const { themeClasses } = provideTheme(props)
    const { locationStyles } = useLocation(props)
    const { textColorClasses, textColorStyles } = useTextColor(props, 'color')
    const {
      backgroundColorClasses,
      backgroundColorStyles,
    } = useBackgroundColor(computed(() => props.bgColor || props.color))
    const {
      backgroundColorClasses: bufferColorClasses,
      backgroundColorStyles: bufferColorStyles,
    } = useBackgroundColor(computed(() => props.bufferColor || props.bgColor || props.color))
    const {
      backgroundColorClasses: barColorClasses,
      backgroundColorStyles: barColorStyles,
    } = useBackgroundColor(props, 'color')
    const { roundedClasses } = useRounded(props)
    const { intersectionRef, isIntersecting } = useIntersectionObserver()

    const max = computed(() => parseFloat(props.max))
    const height = computed(() => parseFloat(props.height))
    const normalizedBuffer = computed(() => clamp(parseFloat(props.bufferValue) / max.value * 100, 0, 100))
    const normalizedValue = computed(() => clamp(parseFloat(progress.value) / max.value * 100, 0, 100))
    const isReversed = computed(() => isRtl.value !== props.reverse)
    const transition = computed(() => props.indeterminate ? 'fade-transition' : 'slide-x-transition')
    const isForcedColorsModeActive = IN_BROWSER && window.matchMedia?.('(forced-colors: active)').matches

    function handleClick (e: MouseEvent) {
      if (!intersectionRef.value) return

      const { left, right, width } = intersectionRef.value.getBoundingClientRect()
      const value = isReversed.value ? (width - e.clientX) : e.clientX - left

      progress.value = Math.round(value / width * max.value)
    }

    return {
      intersectionRef,
      isIntersecting,
      isReversed,
      roundedClasses,
      textColorClasses,
      themeClasses,
      rtlClasses,
      backgroundColorClasses,
      bufferColorClasses,
      barColorClasses,
      locationStyles,
      textColorStyles,
      backgroundColorStyles,
      bufferColorStyles,
      barColorStyles,
      handleClick,
      height,
      normalizedBuffer,
      normalizedValue,
      isForcedColorsModeActive,
      transition,
    }
  }
})
</script>

<template>
<div
  ref="intersectionRef"
  :class="[
    'base-progress-linear',
    {
      'base-progress-linear--absolute': absolute,
      'base-progress-linear--active': active && isIntersecting,
      'base-progress-linear--reverse': isReversed,
      'base-progress-linear--rounded': rounded,
      'base-progress-linear--rounded-bar': roundedBar,
      'base-progress-linear--striped': striped,
    },
    roundedClasses,
    themeClasses,
    rtlClasses,
    $props.class,
  ]"
  :style="[
    {
      bottom: location === 'bottom' ? 0 : undefined,
      top: location === 'top' ? 0: undefined,
      height: active ? convertToUnit(height) : 0,
      '--base-progress-linear-height': convertToUnit(height),
      ...(absolute ? locationStyles : {}),
    },
    $props.style,
  ]"
  role="progressbar"
  :aria-hidden="active ? 'false' : 'true'"
  aria-valuemin="0"
  :aria-valuemax="$props.max"
  @click="clickable && handleClick"
>
  <template v-if="$props.stream">
    <div
      key="stream"
      :class="[
        'base-progress-linear__stream',
        textColorClasses,
      ]"
      :style="{
        ...textColorStyles,
        [isReversed ? 'left' : 'right']: convertToUnit(-height),
        borderTop: `${convertToUnit(height / 2)} dotted`,
        opacity: parseFloat(bufferOpacity!),
        top: `calc(50% - ${convertToUnit(height / 4)})`,
        width: convertToUnit(100 - normalizedBuffer, '%'),
        '--base-progress-linear-stream-to': convertToUnit(height * (isReversed ? 1 : -1)),
      }"
    />
  </template>

  <div
    :class="[
      'base-progress-linear__background',
      !isForcedColorsModeActive ? backgroundColorClasses : undefined,
    ]"
    :style="[
      backgroundColorStyles,
      {
        opacity: parseFloat(bgOpacity!),
        width: $props.stream ? 0 : undefined,
      },
    ]"
  />

  <div
    :class="[
      'base-progress-linear__buffer',
      !isForcedColorsModeActive ? bufferColorClasses : undefined,
    ]"
    :style="[
      bufferColorStyles,
      {
        opacity: parseFloat(bufferOpacity!),
        width: convertToUnit(normalizedBuffer, '%'),
      },
    ]"
  />

  <Transition :name="transition">
    <div
      v-if="!indeterminate"
      :class="[
        'base-progress-linear__determinate',
         !isForcedColorsModeActive ? barColorClasses : undefined,
      ]"
      :style="[
        barColorStyles,
        {
          width: convertToUnit(normalizedValue, '%')
        }
      ]"
    />
  </Transition>
  <Transition :name="transition">
    <div v-if="indeterminate" class="base-progress-linear__indeterminate">
      <div
        v-for="bar in ['long', 'short']"
        :key="bar"
        :class="[
          'base-progress-linear__indeterminate',
          bar,
          !isForcedColorsModeActive ? barColorClasses : undefined
        ]"
        :style="barColorStyles"
      />
    </div>
  </Transition>

  <div v-if="$slots.default" class="base-progress-linear__content">
    <slot name="default" :value="normalizedValue" :buffer="normalizedBuffer"/>
  </div>

</div>
</template>
