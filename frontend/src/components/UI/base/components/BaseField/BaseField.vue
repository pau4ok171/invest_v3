<script lang="ts">
import {computed, defineComponent, ref} from 'vue'

// Types
import type { PropType, SlotsType } from 'vue'
import {EventProp, getUid} from "@/components/UI/base/util";
import type {Theme} from "@/components/UI/base/components/BaseTheme/baseTheme.d";
import {allowedThemes} from "@/components/UI/base/components/BaseTheme/baseTheme.d";
import {useFocus} from "@/components/UI/base/composable/focus";
import {provideTheme} from "@/components/UI/base/composable/theme";
import {useBackgroundColor, useTextColor} from "@/components/UI/base/composable/color";
import type {
  BaseFieldSlots,
  DefaultInputSlot,
  Variant
} from "./BaseField.types";
import {allowedVariants} from "./BaseField.types";

export default defineComponent({
  name: "BaseField",
  props: {
    id: String,
    appendInnerIcon: {
      type: undefined, //TODO: Create IconValue type
    },
    bgColor: String,
    clearable: Boolean,
    clearIcon: {
      type: undefined, //TODO: Create IconValue type
      default: '$clear',
    },
    active: Boolean,
    centerAffix: {
      type: Boolean,
      default: undefined,
    },
    color: String,
    baseColor: String,
    dirty: Boolean,
    disabled: {
      type: Boolean,
      default: null,
    },
    error: Boolean,
    flat: Boolean,
    label: String,
    persistentClear: Boolean,
    prependInnerIcon: {
      type: undefined, //TODO: Create IconValue type
    },
    reverse: Boolean,
    singleLine: Boolean,
    variant: {
      type: String as PropType<Variant>,
      default: 'filled',
      validator: (v: any) => allowedVariants.includes(v),
    },
    modelValue: {
      type: [String, Number],
      default: undefined,
    },
    'onClick:clear': EventProp<[MouseEvent]>(),
    'onClick:appendInner': EventProp<[MouseEvent]>(),
    'onClick:prependInner': EventProp<[MouseEvent]>(),
    theme: {
      type: String as PropType<Theme>,
      default: 'light',
      validator: (v: any) => allowedThemes.includes(v)
    },
    focused: Boolean,
  },
  slots: Object as SlotsType<BaseFieldSlots>,
  emits: {
    'update:focused': (focused: boolean) => true,
    'update:modelValue': (value: any) => true,
  },
  setup(props, { slots }) {
    const { themeClasses } = provideTheme(props) // TODO: Create provideTheme
    const { focusClasses, isFocused, blur, focus } = useFocus(props)
    // const { InputIcon } = '' // TODO: Create useInputIcon
    // const { roundedClasses } = '' // TODO: Create useRounded
    // const { rtlClasses } = '' // TODO: Create useRtl

    const isActive = computed(() => props.dirty || props.active)
    const hasLabel = computed(() => !props.singleLine && !!(props.label || slots.label))

    const uid = getUid()
    const id = computed(() => props.id || `input-${uid}`)
    const messageId = computed(() => `${id.value}-messages`)

    // const labelRef = ref<BaseFieldLabel>() // TODO: Create BaseFieldLabel
    // const floatingLabelRef = ref<BaseFieldLabel>() // TODO: Create BaseFieldLabel
    const controlRef = ref<HTMLElement>()
    const isPlainOrUnderlined = computed(() => ['plain', 'underlined'].includes(props.variant))

    const { backgroundColorClasses, backgroundColorStyles } = useBackgroundColor(props, 'bgColor')
    const { textColorClasses, textColorStyles } = useTextColor(computed(() => {
      return props.error || props.disabled ? undefined
          : isActive.value && isFocused.value ? props.color
          : props.baseColor
    }))
    const isOutlined = props.variant === 'outlined'
    const hasPrepend = !!(slots['prepend-inner'] || props.prependInnerIcon)
    const hasClear = (props.clearable || slots.clear)
    const hasAppend = !!(slots['append-inner'] || props.appendInnerIcon || hasClear)

    const slotProps = computed<DefaultInputSlot>(() => ({
      isActive,
      isFocused,
      controlRef,
      blur,
      focus,
    }))

    function onClick (e: MouseEvent) {
      if (e.target !== document.activeElement) {
        e.preventDefault()
      }
    }

    return {
      isActive,
      hasAppend,
      hasPrepend,
      isPlainOrUnderlined,
      backgroundColorClasses,
      backgroundColorStyles,
      textColorClasses,
      textColorStyles,
      focusClasses,
      themeClasses,
      onClick,
      isOutlined,
    }
  },
})
</script>

<template>
<div
  :class="[
    'base-field',
    {
      'base-field--active': isActive,
      'base-field--appended': hasAppend,
      'base-field--center-affix': centerAffix ?? isPlainOrUnderlined,
      'base-field--disabled': disabled,
      'base-field--dirty': dirty,
      'base-field--error': error,
      'base-field--flat': flat,
      'base-field--has-background': bgColor,
      'base-field--persistent-clear': persistentClear,
      'base-field--prepended': hasPrepend,
      'base-field--reverse': reverse,
      'base-field--single-line': singleLine,
      'base-field--no-label': !label,
      [`base-field--variant-${variant}`]: true
    },
    themeClasses,
    backgroundColorClasses,
    focusClasses,
  ]"
  :style="[
    backgroundColorStyles
  ]"
  @click="onClick"
>

  <div class="base-field__overlay"/>

  <!--     TODO: ADD LOADER-->

  <!--   TODO: ADD PREPEND-->

  <div class="base-field__field">

    <!--  TODO: ADD FLOATING LABEL  -->

    <!--  TODO: ADD LABEL  -->

    <slot class="base-field__input"/>

    <!--   TODO: ADD CLEARABLE-->

  </div>

  <!--   TODO: ADD APPEND-->

  <div :class="['base-field__outline', textColorClasses]" :style="[textColorStyles]">
    <template v-if="isOutlined">
      <div class="base-field__outline__start"></div>
      <div class="base-field__outline__notch"></div>
      <div class="base-field__outline__end"></div>
    </template>
  </div>

</div>
</template>

<style lang="scss" scoped>
@use "BaseField";
</style>