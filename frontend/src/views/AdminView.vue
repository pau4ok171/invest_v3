<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.admin.main')

onMounted(() => {
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
