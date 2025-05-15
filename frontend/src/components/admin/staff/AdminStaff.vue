<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()

onMounted(() => {
  document.title = 'ADMIN STAFF'
  store.loading = false
})
</script>

<template>
  <div class="page-not-found">ADMIN STAFF</div>
</template>

<style scoped>
.page-not-found {
  display: flex;
  font-size: 5rem;
  align-items: center;
  justify-content: center;
  margin: 100px 0;
}
</style>
