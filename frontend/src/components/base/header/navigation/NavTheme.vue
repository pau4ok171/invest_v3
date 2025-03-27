<script setup lang="ts">
// Composables
import { useTheme } from 'vuetify'

// Utilities
import { computed } from 'vue'

const theme = useTheme()
const isDarkTheme = computed(() => theme.global.name.value === 'finargo-dark')
const changeThemeMode = () =>
  (theme.global.name.value = isDarkTheme.value
    ? 'finargo-light'
    : 'finargo-dark')
</script>

<template>
  <v-btn
    :icon="isDarkTheme ? '$iDarkMode' : '$iLightMode'"
    variant="text"
    rounded="lg"
    @click="changeThemeMode"
  />
</template>
