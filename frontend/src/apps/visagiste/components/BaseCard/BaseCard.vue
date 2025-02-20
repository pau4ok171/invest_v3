<script lang="ts">
// Styles
import "./BaseCard.scss";

// Components
import { default as BaseCardActions } from "./BaseCardActions.vue";
import { default as BaseCardItem } from "./BaseCardItem.vue";
import { default as BaseCardText } from "./BaseCardText.vue";
import { BaseDefaultsProvider } from "@/apps/visagiste/components/BaseDefaultsProvider";
import { BaseImage } from "@/apps/visagiste/components/BaseImage";

// Composables
import { useBorder, useBorderProps } from "@/apps/visagiste/composables/border";
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  useDensity,
  useDensityProps,
} from "@/apps/visagiste/composables/density";
import {
  useDimension,
  useDimensionProps,
} from "@/apps/visagiste/composables/dimensions";
import {
  useElevation,
  useElevationProps,
} from "@/apps/visagiste/composables/elevation";
import {
  LoaderSlot,
  useLoader,
  useLoaderProps,
} from "@/apps/visagiste/composables/loader";
import {
  useLocation,
  useLocationProps,
} from "@/apps/visagiste/composables/location";
import {
  usePosition,
  usePositionProps,
} from "@/apps/visagiste/composables/position";
import {
  useRounded,
  useRoundedProps,
} from "@/apps/visagiste/composables/rounded";
import { useLink, useRouterProps } from "@/apps/visagiste/composables/router";
import { useTagProps } from "@/apps/visagiste/composables/tag";
import {
  provideTheme,
  useThemeProps,
} from "@/apps/visagiste/composables/theme";
import {
  genOverlays,
  useVariant,
  useVariantProps,
} from "@/apps/visagiste/composables/variant";
import { IconValue } from "@/apps/visagiste/composables/icons";

// Directives
import { Ripple } from "@/apps/visagiste/directives/ripple";

// Utilities
import { computed } from "vue";
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";

// Types
import type { PropType, SlotsType } from "vue";
import type { RippleDirectiveBinding } from "@/apps/visagiste/directives/ripple";
import type { BaseCardItemSlots } from "@/apps/visagiste/components/BaseCard/BaseCardItem.vue";
import type { LoaderSlotProps } from "@/apps/visagiste/composables/loader";

export const useBaseCardProps = propsFactory(
  {
    appendAvatar: String,
    appendIcon: IconValue,
    disabled: Boolean,
    flat: Boolean,
    hover: Boolean,
    image: String,
    link: {
      type: Boolean,
      default: undefined,
    },
    prependAvatar: String,
    prependIcon: IconValue,
    ripple: {
      type: [Boolean, Object] as PropType<RippleDirectiveBinding["value"]>,
      default: true,
    },
    subtitle: [String, Number],
    text: [String, Number],
    title: [String, Number],

    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useDimensionProps(),
    ...useElevationProps(),
    ...useLoaderProps(),
    ...useLocationProps(),
    ...usePositionProps(),
    ...useRoundedProps(),
    ...useRouterProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps({ variant: "elevated" } as const),
  },
  "BaseCard",
);

export type BaseCardSlots = BaseCardItemSlots & {
  default: never;
  actions: never;
  text: never;
  loader: LoaderSlotProps;
  image: never;
  item: never;
};

export default defineComponent({
  name: "BaseCard",
  components: {
    BaseCardText,
    BaseCardItem,
    BaseDefaultsProvider,
    BaseImage,
    BaseCardActions,
  },
  methods: {
    genOverlays,
    LoaderSlot,
  },
  directives: {
    Ripple,
  },
  props: useBaseCardProps(),
  slots: Object as SlotsType<BaseCardSlots>,
  setup(props, { attrs, slots }) {
    const { themeClasses } = provideTheme(props);
    const { borderClasses } = useBorder(props);
    const { colorClasses, colorStyles, variantClasses } = useVariant(props);
    const { densityClasses } = useDensity(props);
    const { dimensionStyles } = useDimension(props);
    const { elevationClasses } = useElevation(props);
    const { loaderClasses } = useLoader(props);
    const { locationStyles } = useLocation(props);
    const { positionClasses } = usePosition(props);
    const { roundedClasses } = useRounded(props);
    const link = useLink(props, attrs);

    const isLink = computed(() => props.link !== false && link.isLink.value);
    const isClickable = computed(
      () =>
        !props.disabled &&
        props.link !== false &&
        (props.link || link.isClickable.value),
    );

    const Tag = computed(() => (isLink.value ? "a" : props.tag));
    const hasTitle = computed(() => slots.title || props.title != null);
    const hasSubtitle = computed(
      () => slots.subtitle || props.subtitle != null,
    );
    const hasHeader = computed(() => hasTitle.value || hasSubtitle.value);
    const hasAppend = computed(
      () => !!(slots.append || props.appendAvatar || props.appendIcon),
    );
    const hasPrepend = computed(
      () => !!(slots.prepend || props.prependAvatar || props.prependIcon),
    );
    const hasImage = computed(() => !!(slots.image || props.image));
    const hasCardItem = computed(() => hasHeader.value || hasPrepend.value || hasAppend.value);
    const hasText = computed(() => slots.text || props.text != null);

    return {
      themeClasses,
      borderClasses,
      colorClasses,
      colorStyles,
      variantClasses,
      densityClasses,
      dimensionStyles,
      elevationClasses,
      loaderClasses,
      locationStyles,
      positionClasses,
      roundedClasses,
      link,
      isLink,
      isClickable,
      Tag,
      hasTitle,
      hasSubtitle,
      hasHeader,
      hasAppend,
      hasPrepend,
      hasImage,
      hasCardItem,
      hasText,
    };
  },
});
</script>

<template>
  <component
    :is="Tag"
    :class="[
      'base-card',
      {
        'base-card-disabled': $props.disabled,
        'base-card--flat': $props.flat,
        'base-card--hover': $props.hover && !($props.disabled || $props.flat),
        'base-card--link': isClickable,
      },
      themeClasses,
      borderClasses,
      colorClasses,
      densityClasses,
      elevationClasses,
      loaderClasses,
      positionClasses,
      roundedClasses,
      variantClasses,
      $props.class,
    ]"
    :style="[colorStyles, dimensionStyles, locationStyles, $props.style]"
    @click="isClickable && link.navigate"
    v-ripple="isClickable && $props.ripple"
    :tabindex="$props.disabled ? -1 : undefined"
    v-bind="{ ...link.linkProps }"
  >
    <template v-if="hasImage">
      <div key="image" class="base-card__image">
        <template v-if="!$slots.image">
          <BaseImage key="image-defaults" cover :src="$props.image" />
        </template>

        <template v-else>
          <BaseDefaultsProvider
            key="image-defaults"
            :disabled="!$props.image"
            :defaults="{
              BaseImage: {
                cover: true,
                src: $props.image,
              },
            }"
          >
            <slot name="image" />
          </BaseDefaultsProvider>
        </template>
      </div>
    </template>

    <component
      :is="LoaderSlot"
      name="base-card"
      :active="!!$props.loading"
      :color="typeof $props.loading === 'boolean' ? undefined : $props.loading"
    >
      <slot name="loader" />
    </component>

    <template v-if="hasCardItem">
      <BaseCardItem
        key="item"
        :prepend-avatar="$props.prependAvatar"
        :prepend-icon="$props.prependIcon"
        :title="$props.title"
        :subtitle="$props.subtitle"
        :append-avatar="$props.appendAvatar"
        :append-icon="$props.appendIcon"
      >
        <template #default><slot name="item" /></template>
        <template #prepend><slot name="prepend" /></template>
        <template #title><slot name="title" /></template>
        <template #subtitle><slot name="subtitle" /></template>
        <template #append><slot name="append" /></template>
      </BaseCardItem>
    </template>

    <template v-if="hasText">
      <BaseCardText key="text">
        <slot name="text">{{ $props.text }}</slot>
      </BaseCardText>
    </template>

    <slot name="default" />

    <template v-if="$slots.actions">
      <BaseCardActions>
        <slot name="actions" />
      </BaseCardActions>
    </template>

    <component :is="genOverlays(isClickable, 'base-card')" />
  </component>
</template>