<script lang="ts">
// Styles
import "./BaseField.scss";

// Components
import BaseFieldLabel from "./BaseFieldLabel.vue";
import { BaseExpandXTransition } from "@/apps/visagiste/components/transitions";
import BaseDefaultsProvider from "@/apps/visagiste/components/BaseDefaultsProvider/BaseDefaultsProvider.vue";
import { useInputIcon } from "@/apps/visagiste/components/BaseInput/InputIcon.vue";

// Composables
import { useFocus, useFocusProps } from "@/apps/visagiste/composables/focus";
import {
  provideTheme,
  useThemeProps,
} from "@/apps/visagiste/composables/theme";
import {
  useBackgroundColor,
  useTextColor,
} from "@/apps/visagiste/composables/color";
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  LoaderSlot,
  useLoader,
  useLoaderProps,
} from "@/apps/visagiste/composables/loader";
import {
  useRounded,
  useRoundedProps,
} from "@/apps/visagiste/composables/rounded";
import { useRtl } from "@/apps/visagiste/composables";
import { IconValue } from "@/apps/visagiste/composables/icons";
import { useSlotIsEmpty } from "@/apps/visagiste/composables/slotIsEmpty";

// Utilities
import { computed, ref, watch } from "vue";
import {
  animate,
  convertToUnit,
  defineComponent,
  EventProp,
  getUid,
  nullifyTransforms,
  propsFactory,
  standardEasing,
} from "@/apps/visagiste/utils";

// Types
import type { PropType, SlotsType, Ref } from "vue";
import type { LoaderSlotProps } from "@/apps/visagiste/composables/loader";

const allowedVariants = [
  "underlined",
  "outlined",
  "filled",
  "solo",
  "solo-inverted",
  "solo-filled",
  "plain",
] as const;
type Variant = (typeof allowedVariants)[number];

export interface DefaultInputSlot {
  isActive: Ref<boolean>;
  isFocused: Ref<boolean>;
  controlRef: Ref<HTMLElement | undefined>;
  focus: () => void;
  blur: () => void;
}

export interface BaseFieldSlot extends DefaultInputSlot {
  props: Record<string, unknown>;
}

export const useBaseFieldProps = propsFactory(
  {
    appendInnerIcon: IconValue,
    bgColor: String,
    clearable: Boolean,
    clearIcon: {
      type: IconValue,
      default: "$clear",
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
    prependInnerIcon: IconValue,
    reverse: Boolean,
    singleLine: Boolean,
    variant: {
      type: String as PropType<Variant>,
      default: "filled",
      validator: (v: any) => allowedVariants.includes(v),
    },

    "onClick:clear": EventProp<[MouseEvent]>(),
    "onClick:appendInner": EventProp<[MouseEvent]>(),
    "onClick:prependInner": EventProp<[MouseEvent]>(),

    ...useComponentProps(),
    ...useLoaderProps(),
    ...useRoundedProps(),
    ...useThemeProps(),
  },
  "BaseField",
);

export type BaseFieldSlots = {
  clear: DefaultInputSlot & { props: Record<string, any> };
  "prepend-inner": DefaultInputSlot;
  "append-inner": DefaultInputSlot;
  label: DefaultInputSlot & {
    label: string | undefined;
    props: Record<string, any>;
  };
  loader: LoaderSlotProps;
  default: BaseFieldSlot;
};

export default defineComponent({
  name: "BaseField",
  computed: {
    BaseExpandXTransition() {
      return BaseExpandXTransition;
    },
    LoaderSlot() {
      return LoaderSlot;
    },
  },
  components: {
    BaseDefaultsProvider,
    BaseFieldLabel,
  },
  inheritAttrs: false,
  props: {
    id: String,

    ...useFocusProps(),
    ...useBaseFieldProps(),
  },
  slots: Object as SlotsType<BaseFieldSlots>,
  emits: {
    "update:focused": (focused: boolean) => true,
    "update:modelValue": (value: any) => true,
  },
  setup(props, { slots }) {
    const { themeClasses } = provideTheme(props);
    const { loaderClasses } = useLoader(props);
    const { focusClasses, isFocused, blur, focus } = useFocus(props);
    const { InputIcon } = useInputIcon(props);
    const { roundedClasses } = useRounded(props);
    const { rtlClasses } = useRtl();

    const isActive = computed(() => props.dirty || props.active);
    const isLabelEmpty = useSlotIsEmpty("label");
    const hasLabel = computed(() => !!props.label || !isLabelEmpty.value);
    const hasFloatingLabel = computed(
      () => !props.singleLine && hasLabel.value,
    );

    const uid = getUid();
    const id = computed(() => props.id || `input-${uid}`);
    const messagesId = computed(() => `${id.value}-messages`);

    const labelRef = ref<BaseFieldLabel>();
    const floatingLabelRef = ref<BaseFieldLabel>();
    const controlRef = ref<HTMLElement>();
    const isPlainOrUnderlined = computed(() =>
      ["plain", "underlined"].includes(props.variant),
    );

    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(props, "bgColor");
    const { textColorClasses, textColorStyles } = useTextColor(
      computed(() => {
        return props.error || props.disabled
          ? undefined
          : isActive.value && isFocused.value
            ? props.color
            : props.baseColor;
      }),
    );

    watch(
      isActive,
      (val) => {
        if (hasFloatingLabel.value) {
          const el: HTMLElement = labelRef.value!.$el;
          const targetEl: HTMLElement = floatingLabelRef.value!.$el;

          requestAnimationFrame(() => {
            const rect = nullifyTransforms(el);
            const targetRect = targetEl.getBoundingClientRect();

            const x = targetRect.x - rect.x;
            const y =
              targetRect.y - rect.y - (rect.height / 2 - targetRect.height / 2);

            const targetWidth = targetRect.width / 0.75;
            const width =
              Math.abs(targetWidth - rect.width) > 1
                ? { maxWidth: convertToUnit(targetWidth) }
                : undefined;

            const style = getComputedStyle(el);
            const targetStyle = getComputedStyle(targetEl);
            const duration = parseFloat(style.transitionDuration) * 1000 || 150;
            const scale = parseFloat(
              targetStyle.getPropertyValue("--base-field-label-scale"),
            );
            const color = targetStyle.getPropertyValue("color");

            el.style.visibility = "visible";
            targetEl.style.visibility = "hidden";

            animate(
              el,
              {
                transform: `translate(${x}px, ${y}px) scale(${scale})`,
                color,
                ...width,
              },
              {
                duration,
                easing: standardEasing,
                direction: val ? "normal" : "reverse",
              },
            ).finished.then(() => {
              el.style.removeProperty("visibility");
              targetEl.style.removeProperty("visibility");
            });
          });
        }
      },
      { flush: "post" },
    );

    const slotProps = computed<DefaultInputSlot>(() => ({
      isActive,
      isFocused,
      controlRef,
      blur,
      focus,
    }));

    function onClick(e: MouseEvent) {
      if (e.target !== document.activeElement) {
        e.preventDefault();
      }
    }

    const isOutlined = computed(() => props.variant === "outlined");
    const isPrependInnerEmpty = useSlotIsEmpty("prepend-inner");
    const isClearEmpty = useSlotIsEmpty("clear");
    const isAppendInnerEmpty = useSlotIsEmpty("append-inner");
    const hasPrepend = computed(
      () => !isPrependInnerEmpty.value || !!props.prependInnerIcon,
    );
    const hasClear = computed(
      () => (!!props.clearable || !isClearEmpty.value) && !props.disabled,
    );
    const hasAppend = computed(
      () =>
        !isAppendInnerEmpty.value || !!props.appendInnerIcon || hasClear.value,
    );
    const label = computed(() => {
      if (!isLabelEmpty.value) {
        return () =>
          slots.label({
            ...slotProps.value,
            label: props.label,
            props: { for: id.value },
          });
      }
      return () => props.label;
    });

    return {
      InputIcon,
      backgroundColorClasses,
      backgroundColorStyles,
      blur,
      floatingLabelRef,
      focus,
      focusClasses,
      hasAppend,
      hasClear,
      hasFloatingLabel,
      hasLabel,
      hasPrepend,
      id,
      isActive,
      isOutlined,
      isPlainOrUnderlined,
      label,
      labelRef,
      loaderClasses,
      messagesId,
      onClick,
      roundedClasses,
      rtlClasses,
      slotProps,
      textColorClasses,
      textColorStyles,
      themeClasses,
    };
  },
});
</script>

<template>
  <div
    :class="[
      'base-field',
      {
        'base-field--active': isActive,
        'base-field--appended': hasAppend,
        'base-field--center-affix': $props.centerAffix ?? !isPlainOrUnderlined,
        'base-field--disabled': $props.disabled,
        'base-field--dirty': $props.dirty,
        'base-field--error': $props.error,
        'base-field--flat': $props.flat,
        'base-field--has-background': !!$props.bgColor,
        'base-field--persistent-clear': $props.persistentClear,
        'base-field--prepended': hasPrepend,
        'base-field--reverse': $props.reverse,
        'base-field--single-line': $props.singleLine,
        'base-field--no-label': !label(),
        [`base-field--variant-${$props.variant}`]: true,
      },
      themeClasses,
      backgroundColorClasses,
      focusClasses,
      loaderClasses,
      roundedClasses,
      rtlClasses,
      $props.class,
    ]"
    :style="[backgroundColorStyles, $props.style]"
    @click="onClick"
    v-bind="{ ...$attrs }"
  >
    <div class="base-field__overlay" />

    <component
      :is="LoaderSlot"
      name="base-field"
      :active="!!$props.loading"
      :color="
        $props.error
          ? 'error'
          : typeof $props.loading === 'string'
            ? $props.loading
            : $props.color
      "
    >
      <slot name="loader" />
    </component>

    <template v-if="hasPrepend">
      <div key="prepend" class="base-field__prepend-inner">
        <component
          v-if="$props.prependInnerIcon"
          :is="InputIcon"
          key="prepend-icon"
          name="prependInner"
        />

        <slot name="prepend-inner" v-bind="slotProps" />
      </div>
    </template>

    <div class="base-field__field" data-no-activator="">
      <template
        v-if="
          ['filled', 'solo', 'solo-inverted', 'solo-filled'].includes(
            $props.variant,
          ) && hasFloatingLabel
        "
      >
        <BaseFieldLabel
          key="floating-label"
          ref="floatingLabelRef"
          :class="textColorClasses"
          floating
          :for="id"
          :style="textColorStyles"
        >
          <component :is="label" />
        </BaseFieldLabel>
      </template>

      <template v-if="hasLabel">
        <BaseFieldLabel key="label" ref="labelRef" :for="id">
          <slot
            name="label"
            v-bind="{ ...slotProps, label: $props.label, props: { for: id } }"
          >
            {{ $props.label }}
          </slot>
        </BaseFieldLabel>
      </template>

      <slot
        v-bind="{
          ...slotProps,
          props: {
            id,
            class: 'base-field__input',
            'aria-describedby': messagesId,
          },
          focus,
          blur,
        }"
      />
    </div>

    <template v-if="hasClear">
      <component :is="BaseExpandXTransition" key="clear">
        <div
          class="base-field__clearable"
          v-show="$props.dirty"
          @mousedown="
            (e: MouseEvent) => {
              e.preventDefault();
              e.stopPropagation();
            }
          "
        >
          <BaseDefaultsProvider
            :defaults="{
              BaseIcon: {
                icon: $props.clearIcon,
              },
            }"
          >
            <slot
              name="clear"
              v-bind="{
                ...slotProps,
                props: {
                  onFocus: focus,
                  onBlur: blur,
                  onClick: $props['onClick:clear'],
                },
              }"
            >
              <component
                :is="InputIcon"
                name="clear"
                @focus="focus"
                @blur="blur"
              />
            </slot>
          </BaseDefaultsProvider>
        </div>
      </component>
    </template>

    <template v-if="hasAppend">
      <div key="append" class="base-field__append-inner">
        <slot name="append-inner" v-bind="slotProps" />

        <component
          v-if="$props.appendInnerIcon"
          :is="InputIcon"
          key="append-icon"
          name="appendInner"
        />
      </div>
    </template>

    <div
      :class="['base-field__outline', textColorClasses]"
      :style="textColorStyles"
    >
      <template v-if="isOutlined">
        <div class="base-field__outline__start"></div>

        <template v-if="hasFloatingLabel">
          <div class="base-field__outline__notch">
            <BaseFieldLabel ref="floatingLabelRef" floating :for="id">
              <component :is="label" />
            </BaseFieldLabel>
          </div>
        </template>

        <div class="base-field__outline__end"></div>
      </template>

      <template v-if="isPlainOrUnderlined && hasFloatingLabel">
        <BaseFieldLabel ref="floatingLabelRef" floating :for="id">
          <component :is="label" />
        </BaseFieldLabel>
      </template>
    </div>
  </div>
</template>
