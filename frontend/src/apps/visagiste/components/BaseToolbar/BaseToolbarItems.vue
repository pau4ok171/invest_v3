<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { provideDefaults } from "@/apps/visagiste/composables/defaults";
import { useVariantProps } from "@/apps/visagiste/composables/variant";

// Utilities
import { toRef } from "vue";
import { defineComponent, propsFactory } from "@/apps/visagiste/utils";

export const useBaseToolbarItemsProps = propsFactory(
  {
    ...useComponentProps(),
    ...useVariantProps({ variant: "text" } as const),
  },
  "BaseToolbarItems",
);

export default defineComponent({
  name: "BaseToolbarItems",
  props: useBaseToolbarItemsProps(),
  setup(props) {
    provideDefaults({
      BaseButton: {
        color: toRef(props, "color"),
        height: "inherit",
        variant: toRef(props, "variant"),
      },
    });
  },
});
</script>

<template>
  <div :class="['base-toolbar-item', $props.class]" :style="$props.style">
    <slot />
  </div>
</template>
