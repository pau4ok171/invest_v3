<script lang="ts">
// Styles
import "./BaseLayout.scss";

// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  createLayout,
  useLayoutProps,
} from "@/apps/visagiste/composables/layout";
import {
  useDimension,
  useDimensionProps,
} from "@/apps/visagiste/composables/dimensions";

// Utilities
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";

export const useBaseLayoutProps = propsFactory(
  {
    ...useComponentProps(),
    ...useDimensionProps(),
    ...useLayoutProps(),
  },
  "BaseLayout",
);

export default defineComponent({
  name: "BaseLayout",
  props: useBaseLayoutProps(),
  setup(props) {
    const { layoutClasses, layoutStyles, getLayoutItem, items, layoutRef } =
      createLayout(props);
    const { dimensionStyles } = useDimension(props);

    return {
      layoutClasses,
      layoutStyles,
      getLayoutItem,
      items,
      layoutRef,
      dimensionStyles,
    };
  },
});
</script>

<template>
  <div
    ref="layoutRef"
    :class="[layoutClasses, props.class]"
    :style="[dimensionStyles, layoutStyles, props.style]"
  >
    <slot />
  </div>
</template>
