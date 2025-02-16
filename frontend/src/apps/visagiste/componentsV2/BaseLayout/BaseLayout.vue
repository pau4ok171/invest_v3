<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useDimensionProps } from "@/apps/visagiste/composables/dimensions";
import { useLayoutProps } from "@/apps/visagiste/composables/layout";

// Utilities
import { propsFactory } from "@/apps/visagiste/utils";

export const useBaseLayoutProps = propsFactory(
  {
    ...useComponentProps(),
    ...useDimensionProps(),
    ...useLayoutProps(),
  },
  "BaseLayout",
);
</script>

<script setup lang="ts">
// Styles
import "./BaseLayout.scss";
import { createLayout } from "@/apps/visagiste/composables/layout";
import { useDimension } from "@/apps/visagiste/composables/dimensions";

defineOptions({
  name: 'BaseLayout'
})

const props = defineProps(useBaseLayoutProps());

const { layoutClasses, layoutStyles, getLayoutItem, items, layoutRef } =
  createLayout(props);
const { dimensionStyles } = useDimension(props);

defineExpose({
  getLayoutItem,
  items,
});
</script>

<template>
  <div
    :ref="layoutRef"
    :class="[layoutClasses, props.class]"
    :style="[dimensionStyles, layoutStyles, props.style]"
  >
    <slot />
  </div>
</template>
