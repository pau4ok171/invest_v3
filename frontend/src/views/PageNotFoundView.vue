<script setup lang="ts">
// Components
import PageNotFound from '@/components/base/page_not_found/PageNotFound.vue'

// Composables
import { usePageStore } from '@/store/page'
import { useTitle } from '@/composables/documentTitle'

// Utilities
import { onMounted } from 'vue'

const store = usePageStore()
const { setTitle } = useTitle()
setTitle('pageTitles.page404')

onMounted(() => {
  store.loading = false
})
</script>

<template>
  <div class="d-flex justify-center w-100 h-100">
    <page-not-found />
  </div>
</template>
