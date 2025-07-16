<script setup lang="ts">
// Composables
import { useTheme } from 'vuetify'
import { useAuthStore } from '@/store/auth'

// Utilities
import { computed } from 'vue'

const theme = useTheme()
const authStore = useAuthStore()
const isDarkTheme = computed(() => theme.name.value === 'finargo-dark')

theme.change(
  authStore.profile?.theme || localStorage.getItem('theme') || 'finargo-light'
)

const changeThemeMode = async () => {
  const newTheme = isDarkTheme.value ? 'finargo-light' : 'finargo-dark'
  theme.change(newTheme)
  localStorage.setItem('theme', newTheme)

  try {
    if (authStore.isAuthenticated && authStore.profile) {
      await authStore.patchProfile({ theme: newTheme })
    }
  } catch (error) {
    console.error('Failed to change theme:', error)
  }
}
</script>

<template>
  <v-btn
    :icon="isDarkTheme ? '$iDarkMode' : '$iLightMode'"
    variant="text"
    rounded="lg"
    @click="changeThemeMode"
  />
</template>
