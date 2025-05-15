<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()

onMounted(() => {
  document.title = 'ADMIN PANEL'
  store.loading = false
})
</script>

<template>
  <div class="admin-view">
    <router-view />
  </div>
</template>

<style scoped>
.admin-view {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: start;
  width: 100%;
}
</style>
