<script setup lang="ts">
// Components
import PageNotFound from '@/components/base/page_not_found/PageNotFound.vue'

// Composables
import { usePageStore } from '@/store/page'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <div class="d-flex justify-center w-100 h-100">
    <page-not-found />
  </div>
</template>
