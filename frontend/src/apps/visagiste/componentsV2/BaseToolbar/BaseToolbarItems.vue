<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useVariantProps } from "@/apps/visagiste/composables/variant";

// Utilities
import { propsFactory } from "@/apps/visagiste/utils";

export const useBaseToolbarItemsProps = propsFactory(
  {
    ...useComponentProps(),
    ...useVariantProps({ variant: "text" } as const),
  },
  "BaseToolbarItems",
);
</script>

<script setup lang="ts">
// Composables
import { provideDefaults } from "@/apps/visagiste/composables/defaults";

// Utilities
import { toRef } from "vue";

const props = defineProps(useBaseToolbarItemsProps());

provideDefaults({
  BaseButton: {
    color: toRef(props, "color"),
    height: "inherit",
    variant: toRef(props, "variant"),
  },
});
</script>

<template>
  <div :class="['base-toolbar-item', props.class]" :style="props.style">
    <slot />
  </div>
</template>
