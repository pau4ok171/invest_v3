<script lang="ts">
// Styles
import "./BaseLayoutItem.scss";

// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  useLayoutItem,
  useLayoutItemProps,
} from "@/apps/visagiste/composables/layout";

// Utilities
import { computed, defineComponent, toRef } from "vue";
import { propsFactory } from "@/apps/visagiste/utils";

// Types
import type { PropType } from "vue/";

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

export default defineComponent({
  name: "BaseLayoutItem",
  props: useBaseLayoutItemProps(),
  setup(props) {
    const { layoutItemStyles } = useLayoutItem({
      id: props.name,
      order: computed(() => parseInt(props.order, 10)),
      position: toRef(props, "position"),
      elementSize: toRef(props, "size"),
      layoutSize: toRef(props, "size"),
      active: toRef(props, "modelValue"),
      absolute: toRef(props, "absolute"),
    });

    return {
      layoutItemStyles,
    };
  },
});
</script>

<template>
  <div
    :class="['base-layout-item', $props.class]"
    :style="[layoutItemStyles, $props.style]"
  >
    <slot />
  </div>
</template>
