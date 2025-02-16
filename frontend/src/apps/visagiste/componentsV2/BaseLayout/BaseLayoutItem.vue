<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useLayoutItemProps } from "@/apps/visagiste/composables/layout";

// Utilities
import { propsFactory } from "@/apps/visagiste/utils";

// Types
import type { PropType } from "vue";

export const useBaseLayoutItemProps = propsFactory(
  {
    position: {
      type: String as PropType<"top" | "right" | "bottom" | "left">,
      required: true,
    },
    size: {
      type: [Number, String],
      default: 300,
    },
    modelValue: Boolean,

    ...useComponentProps(),
    ...useLayoutItemProps(),
  },
  "BaseLayoutItem",
);
</script>

<script setup lang="ts">
// Styles
import "./BaseLayoutItem.scss";
import { useLayoutItem } from "@/apps/visagiste/composables/layout";
import { computed, toRef } from "vue";

const props = defineProps(useBaseLayoutItemProps());

const { layoutItemStyles } = useLayoutItem({
  id: props.name,
  order: computed(() => parseInt(props.order, 10)),
  position: toRef(props, "position"),
  elementSize: toRef(props, "size"),
  layoutSize: toRef(props, "size"),
  active: toRef(props, "modelValue"),
  absolute: toRef(props, "absolute"),
});
</script>

<template>
  <div
    :class="['base-layout-item', props.class]"
    :style="[layoutItemStyles, props.style]"
  >
    <slot />
  </div>
</template>
