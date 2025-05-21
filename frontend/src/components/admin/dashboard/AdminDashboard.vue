<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.admin.dashboard')

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <div class="page-not-found">ADMIN DASHBOARD</div>
</template>

<style scoped>
.page-not-found {
  display: flex;
  font-size: 5rem;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin: 100px 0;
}
</style>
