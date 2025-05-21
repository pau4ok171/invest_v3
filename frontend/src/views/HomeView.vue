<script setup lang="ts">
// Composables
import { usePageStore } from '@/store/page'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.home')

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <div class="d-flex justify-center w-100 h-100">
    <div class="page-not-found">HOME VIEW</div>
  </div>
</template>

<style scoped>
.page-not-found {
  height: 100vh;
  display: flex;
  font-size: 3.125rem;
  align-items: center;
  justify-content: center;
  margin: 100px 0;
}
</style>
