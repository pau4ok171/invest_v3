<script lang="ts">
// Styles
import "./BaseVirtualScroll.scss";

// Components
import BaseVirtualScrollItem from "./BaseVirtualScrollItem.vue";

// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import {
  useDimension,
  useDimensionProps,
} from "@/apps/visagiste/composables/dimensions";
import {
  useVirtual,
  useVirtualProps,
} from "@/apps/visagiste/composables/virtual";

// Utilities
import {
  convertToUnit,
  defineComponent,
  getCurrentInstance,
  getScrollParent,
  propsFactory,
} from "@/apps/visagiste/utils";
import type { PropType } from "vue";
import { onMounted, onScopeDispose, toRef } from "vue";
import { useToggleScope } from "@/apps/visagiste/composables/toggleScope";

export const useBaseVirtualScrollProps = propsFactory(
  {
    items: {
      type: Array as PropType<readonly unknown[]>,
      default: () => [],
    },
    renderless: Boolean,

    ...useVirtualProps(),
    ...useComponentProps(),
    ...useDimensionProps(),
  },
  "BaseVirtualScroll",
);

export default defineComponent({
  name: "BaseVirtualScroll",
  methods: { convertToUnit },
  components: { BaseVirtualScrollItem },
  props: useBaseVirtualScrollProps(),
  setup(props) {
    const vm = getCurrentInstance("BaseVirtualScroll");
    const { dimensionStyles } = useDimension(props);
    const {
      calculateVisibleItems,
      containerRef,
      markerRef,
      handleScroll,
      handleScrollend,
      handleItemResize,
      scrollToIndex,
      paddingTop,
      paddingBottom,
      computedItems,
    } = useVirtual(props, toRef(props, "items"));

    useToggleScope(
      () => props.renderless,
      () => {
        function handleListeners(add = false) {
          const method = add ? "addEventListener" : "removeEventListener";

          if (containerRef.value === document.documentElement) {
            document[method]("scroll", handleScroll, { passive: true });
            document[method]("scrollend", handleScrollend);
          }
        }

        onMounted(() => {
          containerRef.value = getScrollParent(
            vm.vnode.el as HTMLElement,
            true,
          );
          handleListeners(true);
        });
        onScopeDispose(handleListeners);
      },
    );

    return {
      containerRef,
      markerRef,
      computedItems,
      handleItemResize,
      paddingTop,
      paddingBottom,
      dimensionStyles,
      handleScroll,
      handleScrollend,
    };
  },
});
</script>

<template>
  <template v-if="$props.renderless">
    <div
      ref="markerRef"
      class="base-virtual-scroll__spacer"
      :style="{ paddingTop: convertToUnit(paddingTop) }"
    />

    <BaseVirtualScrollItem
      v-for="item in computedItems"
      :key="item.key"
      :renderless="$props.renderless"
      @update:height="(height) => handleItemResize(item.index, height)"
    >
      <template #default="slotProps">
        <slot :item="item.raw" :index="item.index" v-bind="slotProps" />
      </template>
    </BaseVirtualScrollItem>

    <div
      ref="markerRef"
      class="base-virtual-scroll__spacer"
      :style="{ paddingTop: convertToUnit(paddingBottom) }"
    />
  </template>
  <template v-else>
    <div
      ref="containerRef"
      :class="['base-virtual-scroll', $props.class]"
      :style="[dimensionStyles, $props.style]"
      @scroll.passive="handleScroll"
      @scrollend="handleScrollend"
    >
      <div
        ref="markerRef"
        class="base-virtual-scroll__container"
        :style="{
          paddingTop: convertToUnit(paddingTop),
          paddingBottom: convertToUnit(paddingBottom),
        }"
      >
        <BaseVirtualScrollItem
          v-for="item in computedItems"
          :key="item.key"
          :renderless="$props.renderless"
          @update:height="(height) => handleItemResize(item.index, height)"
        >
          <template #default="slotProps">
            <slot :item="item.raw" :index="item.index" v-bind="slotProps" />
          </template>
        </BaseVirtualScrollItem>
      </div>
    </div>
  </template>
</template>
