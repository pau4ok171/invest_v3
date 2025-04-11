<script setup lang="ts">
// Utilities
import { onMounted } from 'vue'

onMounted(() => {
  document.title = 'ADMIN SETTINGS'
})
</script>

<template>
  <div class="page-not-found">ADMIN SETTINGS</div>
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
