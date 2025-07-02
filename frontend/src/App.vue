<script setup lang="ts">
// Components
import AppLayout from '@/layouts/AppLayout.vue'
import PageNotFoundView from '@/views/PageNotFoundView.vue'
import PageLoading from '@/components/UI/PageLoading.vue'

// Composables
import { useAuthStore } from '@/store/auth'
import { usePageStore } from '@/store/page'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

const authStore = useAuthStore()
const pageStore = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.default')

onMounted(async () => {
  await authStore.checkAuth()
})
</script>

<template>
  <v-app>
    <app-layout>
      <page-loading />
      <RouterView v-if="!pageStore.notFound" />
      <page-not-found-view v-else />
    </app-layout>
  </v-app>
</template>
