<script lang="ts">
// Composables
import { useComponentProps } from "@/apps/visagiste/composables/component";
import { useThemeProps } from "@/apps/visagiste/composables/theme";
import { useLayoutProps } from "@/apps/visagiste/composables/layout";

// Utilities
import { propsFactory } from "@/apps/visagiste/utils";

export const useBaseAppProps = propsFactory(
  {
    ...useComponentProps(),
    ...useLayoutProps({ fullHeight: true }),
    ...useThemeProps(),
  },
  "BaseApp",
);
</script>

<script setup lang="ts">
// Styles
import "./../../styles/main.scss";
import "./BaseApp.scss";

// Composables
import { provideTheme } from "@/apps/visagiste/composables/theme";
import { createLayout } from "@/apps/visagiste/composables/layout";
import { useRtl } from "@/apps/visagiste/composables/locale";

const props = defineProps(useBaseAppProps());

const theme = provideTheme(props);
const { layoutClasses, getLayoutItem, items, layoutRef } = createLayout(props);
const { rtlClasses } = useRtl();

defineExpose({
  getLayoutItem,
  items,
  theme,
});
</script>

<template>
  <div
    :ref="layoutRef"
    :class="[
      'base-application',
      theme.themeClasses.value,
      layoutClasses,
      rtlClasses,
      props.class,
    ]"
    :style="[props.style]"
  >
    <div class="base-application__wrap">
      <slot />
    </div>
  </div>
</template>
