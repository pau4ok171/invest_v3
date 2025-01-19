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
<base-button
  :icon="isDarkTheme ? 'DarkThemeIcon' : 'LightThemeIcon'"
  variant="text"
  rounded="x-small"
  @click="changeThemeMode"
/>
</template>