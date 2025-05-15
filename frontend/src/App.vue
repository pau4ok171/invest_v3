<script setup lang="ts">
// Components
import AppLayout from '@/layouts/AppLayout.vue'
import PageNotFoundView from "@/views/PageNotFoundView.vue";
import PageLoading from "@/components/UI/PageLoading.vue";

// Composables
import { useAuthStore } from '@/store/auth'
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import axios from 'axios'

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
  <v-app>
    <app-layout>
      <page-loading />
      <RouterView v-if="!pageStore.notFound" />
      <page-not-found-view v-else/>
    </app-layout>
  </v-app>
</template>
