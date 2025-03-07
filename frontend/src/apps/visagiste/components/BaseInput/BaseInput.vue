<script lang="ts">
// Styles
import "./BaseInput.scss";

// Components
import { useInputIcon } from "@/apps/visagiste/components/BaseInput/InputIcon.vue";
import BaseMessages from "@/apps/visagiste/components/BaseMessages/BaseMessages.vue";

// Composables
import {
  useValidation,
  useValidationProps,
} from "@/apps/visagiste/composables/validation";
import {
  useDimension,
  useDimensionProps,
} from "@/apps/visagiste/composables/dimensions";
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  provideTheme,
  useThemeProps,
} from "@/apps/visagiste/composables/theme";
import {
  useDensity,
  useDensityProps,
} from "@/apps/visagiste/composables/density";
import { IconValue } from "@/apps/visagiste/composables/icons";
import { useRtl } from "@/apps/visagiste/composables";
import { useSlotIsEmpty } from "@/apps/visagiste/composables/slotIsEmpty";

// Utilities
import { computed } from "vue";
import {
  defineComponent,
  EventProp,
  getUid,
  pick,
  propsFactory,
} from "@/apps/visagiste/utils";

// Types
import type { ComputedRef, PropType, SlotsType, Ref } from "vue";
import type { BaseMessageSlot } from "@/apps/visagiste/components/BaseMessages/BaseMessages.vue";

export interface BaseInputSlot {
  id: ComputedRef<string>;
  messagesId: ComputedRef<string>;
  isDirty: ComputedRef<boolean>;
  isDisabled: ComputedRef<boolean>;
  isReadonly: ComputedRef<boolean>;
  isPristine: Ref<boolean>;
  isValid: ComputedRef<boolean | null>;
  isValidating: Ref<boolean>;
  reset: () => void;
  resetValidation: () => void;
  validate: () => void;
}

export const useBaseInputProps = propsFactory(
  {
    id: String,
    appendIcon: IconValue,
    centerAffix: {
      type: Boolean,
      default: true,
    },
    prependIcon: IconValue,
    hideDetails: [Boolean, String] as PropType<boolean | "auto">,
    hideSpinButtons: Boolean,
    hint: String,
    persistentHint: Boolean,
    messages: {
      type: [Array, String] as PropType<string | readonly string[]>,
      default: () => [],
    },
    direction: {
      type: String as PropType<"horizontal" | "vertical">,
      default: "horizontal",
      validator: (v: any) => ["horizontal", "vertical"].includes(v),
    },

    "onClick:prepend": EventProp<[MouseEvent]>(),
    "onClick:append": EventProp<[MouseEvent]>(),

    ...useComponentProps(),
    ...useDensityProps(),
    ...pick(useDimensionProps(), ["maxWidth", "minWidth", "width"]),
    ...useThemeProps(),
    ...useValidationProps(),
  },
  "BaseInput",
);

export type BaseInputSlots = {
  default: BaseInputSlot;
  prepend: BaseInputSlot;
  append: BaseInputSlot;
  details: BaseInputSlot;
  message: BaseMessageSlot;
};

export default defineComponent({
  name: "BaseInput",
  components: {
    BaseMessages,
  },
  props: {
    ...useBaseInputProps(),
  },
  slots: Object as SlotsType<BaseInputSlots>,
  emits: {
    "update:modelValue": (value: any) => true,
  },
  setup(props) {
    const { densityClasses } = useDensity(props);
    const { dimensionStyles } = useDimension(props);
    const { themeClasses } = provideTheme(props);
    const { rtlClasses } = useRtl();
    const { InputIcon } = useInputIcon(props);

    const uid = getUid();
    const id = computed(() => props.id || `input-${uid}`);
    const messagesId = computed(() => `${id.value}-messages`);

    const {
      errorMessages,
      isDirty,
      isDisabled,
      isReadonly,
      isPristine,
      isValid,
      isValidating,
      reset,
      resetValidation,
      validate,
      validationClasses,
    } = useValidation(props, "base-input", id);

    const slotProps = computed<BaseInputSlot>(() => ({
      id,
      messagesId,
      isDirty,
      isDisabled,
      isReadonly,
      isPristine,
      isValid,
      isValidating,
      reset,
      resetValidation,
      validate,
    }));

    const messages = computed(() => {
      if (
        props.errorMessages?.length ||
        (isPristine.value && errorMessages.value.length)
      ) {
        return errorMessages.value;
      } else if (props.hint && (props.persistentHint || props.focused)) {
        return props.hint;
      } else {
        return props.messages;
      }
    });

    const isPrependEmpty = useSlotIsEmpty("prepend");
    const isAppendEmpty = useSlotIsEmpty("append");
    const isDetailsEmpty = useSlotIsEmpty("details");
    const hasPrepend = computed(
      () => !isPrependEmpty.value || !!props.prependIcon,
    );
    const hasAppend = computed(
      () => !isAppendEmpty.value || !!props.appendIcon,
    );
    const hasMessages = computed(() => messages.value?.length > 0);
    const hasDetails = computed(
      () =>
        !props.hideDetails ||
        (props.hideDetails === "auto" &&
          (hasMessages || !isDetailsEmpty.value)),
    );

    return {
      messagesId,
      messages,
      InputIcon,
      densityClasses,
      themeClasses,
      rtlClasses,
      validationClasses,
      dimensionStyles,
      hasPrepend,
      hasAppend,
      hasMessages,
      hasDetails,
      slotProps,
      reset,
      resetValidation,
      validate,
      isValid,
      errorMessages,
    };
  },
});
</script>

<template>
  <div
    :class="[
      'base-input',
      `base-input--${$props.direction}`,
      {
        'base-input--center-affix': $props.centerAffix,
        'base-input--hide-spin-buttons': $props.hideSpinButtons,
      },
      densityClasses,
      themeClasses,
      rtlClasses,
      validationClasses,
      $props.class,
    ]"
    :style="[dimensionStyles, $props.style]"
  >
    <div v-if="hasPrepend" key="prepend" class="base-input__prepend">
      <slot name="prepend" v-bind="slotProps" />

      <component
        v-if="$props.prependIcon"
        :is="InputIcon"
        key="prepend-icon"
        name="prepend"
      />
    </div>

    <div v-if="$slots.default" class="base-input__control">
      <slot name="default" v-bind="slotProps" />
    </div>

    <div v-if="hasAppend" class="base-input__append">
      <component
        v-if="$props.appendIcon"
        :is="InputIcon"
        key="append-icon"
        name="append"
      />

      <slot name="append" v-bind="slotProps" />
    </div>

    <div
      v-if="hasDetails"
      :id="messagesId"
      class="base-input__details"
      role="alert"
      aria-live="polite"
    >
      <BaseMessages :active="hasMessages" :messages="messages">
        <template #message>
          <slot name="message" />
        </template>
      </BaseMessages>

      <slot name="details" v-bind="slotProps" />
    </div>
  </div>
</template>
