<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useResizeObserver } from "@/apps/visagiste/composables/resizeObserver";

// Utilities
import { h, watch } from "vue";
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";

export const useBaseVirtualScrollItemProps = propsFactory(
  {
    renderless: Boolean,

    ...useComponentProps(),
  },
  "BaseVirtualScrollItem",
);

export default defineComponent({
  name: "BaseVirtualScrollItem",
  props: useBaseVirtualScrollItemProps(),
  inheritAttrs: false,
  emits: {
    "update:height": (height: number) => true,
  },
  setup(props, { attrs, emit, slots }) {
    const { resizeRef, contentRect } = useResizeObserver(undefined, "border");

    watch(
      () => contentRect.value?.height,
      (height) => {
        if (height != null) emit("update:height", height);
      },
    );

    return () =>
      props.renderless
        ? slots.default?.({ itemRef: resizeRef })
        : h(
            "div",
            {
              ref: resizeRef,
              class: ["base-virtual-scroll__item", props.class],
              style: props.style,
              ...attrs,
            },
            slots.default?.(),
          );
  },
});
</script>
