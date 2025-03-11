<script setup lang="ts">
// Components
import { BaseApp } from '@/apps/visagiste/components/BaseApp'

// Composables
import { useAuthStore } from '@/store/auth'

// Utilities
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import axios from 'axios'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.init()
  axios.defaults.headers.common['Authorization'] = authStore.token
    ? `Token ${authStore.token}`
    : ''
  authStore.fetchUserInfo()
})
</script>

<template>
  <base-app>
    <AppLayout>
      <RouterView />
    </AppLayout>
  </base-app>
</template>
