<script setup lang="ts">
// Utilities
import { onMounted } from 'vue'

onMounted(() => {
  document.title = 'Page Not Found - Finargo'
})
</script>

<template>
  <div class="page-not-found">PAGE NOT FOUND</div>
</template>

<style scoped>
.page-not-found {
  display: flex;
  font-size: 3.125rem;
  align-items: center;
  justify-content: center;
  margin: 100px 0;
}
</style>
