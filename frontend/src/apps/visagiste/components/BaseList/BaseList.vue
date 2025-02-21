<script lang="ts">
// Styles
import "./BaseList.scss";

// Components
import BaseListChildren from "./BaseListChildren.vue";

// Composables
import { createList } from "./list";
import { IconValue } from "@/apps/visagiste/composables/icons";
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
import { useItemsProps } from "@/apps/visagiste/composables/list-items";
import {
  useRounded,
  useRoundedProps,
} from "@/apps/visagiste/composables/rounded";
import { useTagProps } from "@/apps/visagiste/composables/tag";
import {
  provideTheme,
  useThemeProps,
} from "@/apps/visagiste/composables/theme";
import { useVariantProps } from "@/apps/visagiste/composables/variant";
import {
  useNested,
  useNestedProps,
} from "@/apps/visagiste/composables/nested/nested";

// Utilities
import { computed, ref, shallowRef, toRef } from "vue";
import {
  defineComponent,
  EventProp,
  focusChild,
  getPropertyFromItem,
  isPrimitive,
  omit,
  propsFactory,
} from "@/apps/visagiste/utils";

// Types
import type {
  ItemProps,
  ListItem,
} from "@/apps/visagiste/composables/list-items";
import type { PropType } from "vue";
import { useBackgroundColor } from "@/apps/visagiste/composables/color";
import { provideDefaults } from "@/apps/visagiste/composables/defaults";

export interface InternalListItem<T = any> extends ListItem<T> {
  type?: "item" | "subheader" | "divider";
}

function transformItem(
  props: ItemProps & { itemType?: string },
  item: any,
): InternalListItem {
  const type = getPropertyFromItem(item, props.itemType, "item");
  const title = isPrimitive(item)
    ? item
    : getPropertyFromItem(item, props.itemTitle);
  const value = getPropertyFromItem(item, props.itemValue, undefined);
  const children = getPropertyFromItem(item, props.itemChildren);
  const itemProps =
    props.itemProps === true
      ? omit(item, ["children"])
      : getPropertyFromItem(item, props.itemProps);

  const _props = {
    title,
    value,
    ...itemProps,
  };

  return {
    type,
    title: _props.title,
    value: _props.value,
    props: _props,
    children:
      type === "item" && children ? transformItems(props, children) : undefined,
    raw: item,
  };
}

function transformItems(
  props: ItemProps & { itemType?: string },
  items: (string | object)[],
) {
  const array: InternalListItem[] = [];

  for (const item of items) {
    array.push(transformItem(props, item));
  }

  return array;
}

export function useListItems(props: ItemProps & { itemType?: string }) {
  const items = computed(() => transformItems(props, props.items));

  return { items };
}

export const useBaseListProps = propsFactory(
  {
    baseColor: String,
    /* @deprecated */
    activeColor: String,
    activeClass: String,
    bgColor: String,
    disabled: Boolean,
    expandIcon: IconValue,
    collapseIcon: IconValue,
    lines: {
      type: [Boolean, String] as PropType<"one" | "two" | "three" | false>,
      default: "one",
    },
    slim: Boolean,
    nav: Boolean,

    "onClick:open":
      EventProp<[{ id: unknown; value: boolean; path: unknown }]>(),
    "onClick:select":
      EventProp<[{ id: unknown; value: boolean; path: unknown }]>(),
    "onClick:opened": EventProp<[]>(),
    ...useNestedProps({
      selectStrategy: "single-leaf" as const,
      openStrategy: "list" as const,
    }),
    ...useBorderProps(),
    ...useComponentProps(),
    ...useDensityProps(),
    ...useDimensionProps(),
    ...useElevationProps(),
    itemType: {
      type: String,
      default: "type",
    },
    ...useItemsProps(),
    ...useRoundedProps(),
    ...useTagProps(),
    ...useThemeProps(),
    ...useVariantProps({ variant: "text" } as const),
  },
  "BaseList",
);

type ItemType<T> = T extends readonly (infer U)[] ? U : never;

export default defineComponent({
  name: "BaseList",
  components: { BaseListChildren },
  props: useBaseListProps(),
  emits: {
    "update:selected": (value: unknown) => true,
    "update:activated": (value: unknown) => true,
    "update:opened": (value: unknown) => true,
    "click:open": (value: { id: unknown; value: boolean; path: unknown[] }) =>
      true,
    "click:activate": (value: {
      id: unknown;
      value: boolean;
      path: unknown[];
    }) => true,
    "click:select": (value: { id: unknown; value: boolean; path: unknown[] }) =>
      true,
  },
  setup(props) {
    const { items } = useListItems(props);
    const { themeClasses } = provideTheme(props);
    const { backgroundColorClasses, backgroundColorStyles } =
      useBackgroundColor(toRef(props, "bgColor"));
    const { borderClasses } = useBorder(props);
    const { densityClasses } = useDensity(props);
    const { dimensionStyles } = useDimension(props);
    const { elevationClasses } = useElevation(props);
    const { roundedClasses } = useRounded(props);
    const { children, open, parents, select, getPath } = useNested(props);
    const lineClasses = computed(() =>
      props.lines ? `base-list--${props.lines}-line` : undefined,
    );
    const activeColor = toRef(props, "activeColor");
    const baseColor = toRef(props, "color");
    const color = toRef(props, "color");

    createList();

    provideDefaults({
      BaseListGroup: {
        activeColor,
        baseColor,
        color,
        expandIcon: toRef(props, "expandIcon"),
        collapseIcon: toRef(props, "collapseIcon"),
      },
      BaseListItem: {
        activeClass: toRef(props, "activeClass"),
        activeColor,
        baseColor,
        color,
        density: toRef(props, "density"),
        disabled: toRef(props, "disabled"),
        lines: toRef(props, "lines"),
        nav: toRef(props, "nav"),
        slim: toRef(props, "slim"),
        variant: toRef(props, "variant"),
      },
    });

    const isFocused = shallowRef(false);
    const contentRef = ref<HTMLElement>();
    function onFocusin(e: FocusEvent) {
      isFocused.value = true;
    }

    function onFocusout(e: FocusEvent) {
      isFocused.value = false;
    }

    function onFocus(e: FocusEvent) {
      if (
        !isFocused.value &&
        !(
          e.relatedTarget && contentRef.value?.contains(e.relatedTarget as Node)
        )
      )
        focus();
    }

    function onKeydown(e: KeyboardEvent) {
      const target = e.target as HTMLElement;

      if (!contentRef.value || ["INPUT", "TEXTAREA"].includes(target.tagName))
        return;

      if (e.key === "ArrowDown") {
        focus("next");
      } else if (e.key === "ArrowUp") {
        focus("prev");
      } else if (e.key === "Home") {
        focus("first");
      } else if (e.key === "End") {
        focus("last");
      } else {
        return;
      }

      e.preventDefault();
    }

    function onMousedown(e: MouseEvent) {
      isFocused.value = true;
    }

    function focus(location?: "next" | "prev" | "first" | "last") {
      if (contentRef.value) {
        return focusChild(contentRef.value, location);
      }
    }

    return {
      items,
      contentRef,
      themeClasses,
      backgroundColorClasses,
      borderClasses,
      densityClasses,
      elevationClasses,
      lineClasses,
      roundedClasses,
      backgroundColorStyles,
      dimensionStyles,
      isFocused,
      onFocusin,
      onFocusout,
      onFocus,
      onKeydown,
      onMousedown,
      open,
      select,
      focus,
      children,
      parents,
      getPath,
    };
  },
});
</script>

<template>
  <component
    :is="$props.tag"
    :ref="contentRef"
    :class="[
      'base-list',
      {
        'base-list--disabled': $props.disabled,
        'base-list--nav': $props.nav,
        'base-list--slim': $props.slim,
      },
      themeClasses,
      backgroundColorClasses,
      borderClasses,
      densityClasses,
      elevationClasses,
      lineClasses,
      roundedClasses,
      $props.class,
    ]"
    :style="[backgroundColorStyles, dimensionStyles, $props.style]"
    :tabindex="$props.disabled || isFocused ? -1 : 0"
    role="listbox"
    :aria-activedescendant="undefined"
    @focusin="onFocusin"
    @focusout="onFocusout"
    @focus="onFocus"
    @keydown="onKeydown"
    @mousedown="onMousedown"
  >
    <BaseListChildren :items :returnObject="$props.returnObject">
      <template #default>
        <slot name="default" />
      </template>
      <template #activator>
        <slot name="activator" />
      </template>
    </BaseListChildren>
  </component>
</template>