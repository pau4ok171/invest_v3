<script setup lang="ts">
// Components
import { BaseApp } from '@/apps/visagiste/components/BaseApp'
import PageNotFoundView from "@/views/PageNotFoundView.vue";

// Composables
import { useAuthStore } from '@/store/auth'
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import axios from 'axios'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const pageStore = usePageStore()

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
      <RouterView v-if="!pageStore.notFound" />
      <PageNotFoundView v-else/>
    </AppLayout>
  </base-app>
</template>
