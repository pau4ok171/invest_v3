<script setup lang="ts">
// Styles
import './../../styles/main.scss'
import './BaseApp.scss';

// Composables
import { useRtl } from "@/apps/visagiste/composables";
import { themeProps, provideTheme } from '../../composables/theme';

const props = defineProps({
  ...themeProps
})

const { themeClasses } = provideTheme(props)
const { rtlClasses } = useRtl()
</script>

<template>
<div
  :class="[
    'base-application',
     themeClasses,
     rtlClasses,
  ]"
>
  <div class="base-application__wrap">
    <slot/>
  </div>
</div>
</template>
