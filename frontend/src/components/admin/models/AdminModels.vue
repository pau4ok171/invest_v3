<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()

const items = [
  { title: 'Models', type: 'subheader' },
  { title: 'Companies', props: { to: { name: 'adminModelsCompanies' } } },
]

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <v-navigation-drawer floating color="background">
    <v-list :items nav />
  </v-navigation-drawer>

  <router-view />
</template>
