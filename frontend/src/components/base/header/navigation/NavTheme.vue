<script setup lang="ts">

// Utilities
import BaseButton from "@/apps/visagiste/components/BaseButton/BaseButton.vue";
import {useTheme } from "@/apps/visagiste/composables";
import {computed} from "vue";

// Types

// Composables
const theme = useTheme()
const isDarkTheme = computed(() => theme.global.name.value === 'finargo-dark')
const changeThemeMode = () => theme.global.name.value = isDarkTheme.value ? 'finargo-light' : 'finargo-dark'
</script>

<template>
<div class="nav-theme">
  <base-button
    :icon="isDarkTheme ? 'DarkThemeIcon' : 'LightThemeIcon'"
    variant="text"
    rounded="x-small"
    @click="changeThemeMode"
/>
</div>
</template>

<style scoped>
.nav-theme {
  display: flex;
  color: #92969c;
  justify-content: center;
  align-items: center;
  position: relative;
  height: 64px;
  padding-left: 8px;
  user-select: none;
  cursor: pointer;
}
</style>