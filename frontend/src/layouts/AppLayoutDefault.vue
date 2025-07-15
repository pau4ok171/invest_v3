<script setup lang="ts">
// Components
import TheHeader from '@/components/base/header/TheHeader.vue'
import TheMain from '@/components/base/main/TheMain.vue'
import TheFooter from '@/components/base/footer/TheFooter.vue'

// Composables
import { useAuthStore } from '@/store/auth'

// Utilities
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.fetchOptions()
})
</script>

<template>
  <the-header />

  <the-main><slot /></the-main>

  <the-footer />
</template>
