<script lang="ts">
// Styles
import '../../styles/main.scss'
import './BaseApp.scss'

// Composables
import { provideTheme } from '@/apps/visagiste/composables/theme'
import { createLayout } from '@/apps/visagiste/composables/layout'
import { useRtl } from '@/apps/visagiste/composables/locale'
import { useComponentProps } from '@/apps/visagiste/composables/component'
import { useLayoutProps } from '@/apps/visagiste/composables/layout'
import { useThemeProps } from '@/apps/visagiste/composables/theme'

// Utilities
import { defineComponent, propsFactory } from '@/apps/visagiste/utils'

export const useBaseAppProps = propsFactory(
  {
    ...useComponentProps(),
    ...useLayoutProps({ fullHeight: true }),
    ...useThemeProps(),
  },
  'BaseApp'
)

export default defineComponent({
  name: 'BaseApplication',
  props: useBaseAppProps(),
  setup(props) {
    const theme = provideTheme(props)
    const { layoutClasses, getLayoutItem, items, layoutRef } =
      createLayout(props)
    const { rtlClasses } = useRtl()

    return {
      theme,
      layoutClasses,
      rtlClasses,
      getLayoutItem,
      items,
      layoutRef,
    }
  },
})
</script>

<template>
  <div
    :ref="layoutRef"
    :class="[
      'base-application',
      theme.themeClasses.value,
      layoutClasses,
      rtlClasses,
      $props.class,
    ]"
    :style="[$props.style]"
  >
    <div class="base-application__wrap">
      <slot />
    </div>
  </div>
</template>
