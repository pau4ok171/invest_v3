<script setup lang="ts">
import './BaseApp.scss';
// Utilities
import { themeProps, provideTheme } from '../../composables/theme';

// Types

// Composables
const props = defineProps({
  ...themeProps
})

const { themeClasses } = provideTheme(props)
</script>

<template>
<div
  :class="[
    'base-application',
     themeClasses
  ]"
>
  <div class="base-application__wrap">
    <slot/>
  </div>
</div>
</template>
